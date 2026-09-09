#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "pymupdf>=1.23.0",
#     "pypdf>=4.0.0",
#     "rapidocr-pdf>=0.1.0",
#     "pillow>=10.0.0"
# ]
# ///
"""
extract_pdf_smart.py
Smart PDF Text & Scanned OCR Extractor for Academic Book Agents.

Features:
- Fast text layer extraction (PyMuPDF / PyPDF)
- Automatic scanned/image-only page detection (heuristic character threshold)
- Tiered OCR Fallback:
    1. RapidOCRPDF (Self-contained, pure Python/ONNX, no external exe required)
    2. pytesseract (if tesseract is installed)
    3. Windows Native WinRT OCR fallback via PowerShell (zero external install on Windows 10/11)
- Token-saving & structured Markdown formatting:
    --toc-only : Extracts only Table of Contents / Bookmarks (95%+ token savings)
    --pages    : Page range filtering (e.g. 1-10, 5, 1,3,7-9)
    --grep     : Filter pages containing specific search terms
    --ocr      : auto (default), force, or off
- Structured output saved to Markdown with estimated token metrics.

Usage:
    uv run extract_pdf_smart.py input.pdf -o output.md
    python extract_pdf_smart.py input.pdf --toc-only
    python extract_pdf_smart.py scanned_document.pdf --pages 1-5
"""

import sys
import os
import re
import argparse
import subprocess
import tempfile
from pathlib import Path

# Try PyMuPDF
try:
    import pymupdf
    HAS_PYMUPDF = True
except ImportError:
    try:
        import fitz as pymupdf
        HAS_PYMUPDF = True
    except ImportError:
        HAS_PYMUPDF = False

# Try PyPDF
try:
    import pypdf
    HAS_PYPDF = True
except ImportError:
    HAS_PYPDF = False

# Try PIL
try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

# Try RapidOCRPDF
try:
    from rapidocr_pdf import RapidOCRPDF
    HAS_RAPIDOCR_PDF = True
except ImportError:
    HAS_RAPIDOCR_PDF = False

# Try PyTesseract
try:
    import pytesseract
    HAS_PYTESSERACT = True
except ImportError:
    HAS_PYTESSERACT = False


def parse_page_ranges(range_str, total_pages):
    """Parses a string like '1-5,8,11-13' into a zero-based list of page indices."""
    if not range_str:
        return list(range(total_pages))
    
    pages = set()
    parts = range_str.split(',')
    for part in parts:
        part = part.strip()
        if not part:
            continue
        if '-' in part:
            subparts = part.split('-')
            if len(subparts) == 2:
                try:
                    start = int(subparts[0].strip())
                    end = int(subparts[1].strip())
                    for p in range(start, end + 1):
                        if 1 <= p <= total_pages:
                            pages.add(p - 1)
                except ValueError:
                    pass
        else:
            try:
                p = int(part)
                if 1 <= p <= total_pages:
                    pages.add(p - 1)
            except ValueError:
                pass
    
    return sorted(list(pages)) if pages else list(range(total_pages))


class SmartPDFExtractor:
    def __init__(self, file_path, min_chars_per_page=40, ocr_mode="auto"):
        self.file_path = Path(file_path).resolve()
        if not self.file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        self.min_chars = min_chars_per_page
        self.ocr_mode = ocr_mode  # "auto", "force", "off"
        self.total_pages = 0
        self.toc_entries = []
        self._rapid_ocr_engine = None

    def get_document_info(self):
        """Inspects total pages and outline/bookmarks."""
        if HAS_PYMUPDF:
            doc = pymupdf.open(str(self.file_path))
            self.total_pages = len(doc)
            self.toc_entries = doc.get_toc()  # [[lvl, title, page, ...], ...]
            doc.close()
        elif HAS_PYPDF:
            reader = pypdf.PdfReader(str(self.file_path))
            self.total_pages = len(reader.pages)
            try:
                outline = reader.outline
                self.toc_entries = outline if outline else []
            except Exception:
                self.toc_entries = []
        else:
            raise RuntimeError(
                "Neither PyMuPDF nor PyPDF is available.\n"
                "Please run using: uv run extract_pdf_smart.py <file.pdf>\n"
                "Or install: pip install pymupdf pypdf"
            )
        return self.total_pages, self.toc_entries

    def extract_toc_markdown(self):
        """Extracts Table of Contents / Bookmarks into Markdown format."""
        self.get_document_info()
        md_lines = [
            f"# Daftar Isi: {self.file_path.name}",
            f"*Total Halaman Dokumen: {self.total_pages}*",
            ""
        ]

        if not self.toc_entries:
            md_lines.append("> [!NOTE]\n> Dokumen ini tidak memiliki metadata bookmark / outline digital terintegrasi.")
            return "\n".join(md_lines)

        if HAS_PYMUPDF:
            for item in self.toc_entries:
                lvl, title, page = item[0], item[1], item[2]
                indent = "  " * (lvl - 1)
                md_lines.append(f"{indent}- **{title.strip()}** (Hal. {page})")
        else:
            md_lines.append(str(self.toc_entries))

        return "\n".join(md_lines)

    def _ocr_page_windows_native(self, img_path):
        """Zero-install OCR on Windows 10/11 using Windows.Media.Ocr via PowerShell."""
        if sys.platform != "win32":
            return ""
        
        escaped_path = str(img_path).replace("'", "''")
        ps_cmd = f"""
        [Windows.Media.Ocr.OcrEngine, Windows.Foundation, ContentType = WindowsRuntime] | Out-Null
        [Windows.Graphics.Imaging.BitmapDecoder, Windows.Foundation, ContentType = WindowsRuntime] | Out-Null
        $filePath = '{escaped_path}'
        $file = [System.IO.File]::OpenRead($filePath)
        $stream = $file.AsRandomAccessStream()
        $decoder = [Windows.Graphics.Imaging.BitmapDecoder]::CreateAsync($stream).GetAwaiter().GetResult()
        $bitmap = $decoder.GetSoftwareBitmapAsync().GetAwaiter().GetResult()
        $engine = [Windows.Media.Ocr.OcrEngine]::TryCreateFromUserProfileLanguages()
        if (-not $engine) {{
            $engine = [Windows.Media.Ocr.OcrEngine]::TryCreateFromLanguage('en-US')
        }}
        $result = $engine.RecognizeAsync($bitmap).GetAwaiter().GetResult()
        $stream.Dispose()
        $file.Dispose()
        Write-Output $result.Text
        """
        try:
            res = subprocess.run(
                ["powershell", "-NoProfile", "-Command", ps_cmd],
                capture_output=True,
                text=True,
                timeout=30
            )
            return res.stdout.strip()
        except Exception:
            return ""

    def _ocr_page_with_rapidocr(self, page_num):
        """Uses RapidOCRPDF on a single page index."""
        if not HAS_RAPIDOCR_PDF:
            return ""
        try:
            if self._rapid_ocr_engine is None:
                self._rapid_ocr_engine = RapidOCRPDF()
            
            ocr_res = self._rapid_ocr_engine(str(self.file_path), force_ocr=True, page_num_list=[page_num - 1])
            # ocr_res is list of [page_idx, text, extra]
            text_lines = []
            for item in ocr_res:
                if len(item) > 1 and item[1]:
                    text_lines.append(str(item[1]).strip())
            return "\n".join(text_lines)
        except Exception:
            return ""

    def _ocr_fallback_image(self, img_path):
        """Fallback OCR using PyTesseract or Windows Native OCR."""
        # Tier 2: PyTesseract
        if HAS_PYTESSERACT and HAS_PIL:
            try:
                img = Image.open(img_path)
                text = pytesseract.image_to_string(img, lang="ind+eng")
                if text.strip():
                    return text.strip()
            except Exception:
                pass

        # Tier 3: Windows Native WinRT OCR
        if sys.platform == "win32":
            win_ocr = self._ocr_page_windows_native(img_path)
            if win_ocr:
                return win_ocr

        return ""

    def extract_content(self, page_indices=None, grep_query=None):
        """Extracts text from pages with intelligent OCR fallback."""
        self.get_document_info()
        if page_indices is None:
            page_indices = list(range(self.total_pages))

        extracted_pages = []
        stats = {
            "total_pages": self.total_pages,
            "processed_pages": len(page_indices),
            "text_layer_pages": 0,
            "ocr_pages": 0,
            "empty_pages": 0
        }

        if HAS_PYMUPDF:
            doc = pymupdf.open(str(self.file_path))
            for p_idx in page_indices:
                page_num = p_idx + 1
                page = doc[p_idx]
                text = page.get_text("text").strip()
                method_used = "Text Layer"

                # Check if scanned / image only
                needs_ocr = (self.ocr_mode == "force") or (
                    self.ocr_mode == "auto" and len(text) < self.min_chars
                )

                if needs_ocr:
                    ocr_text = ""
                    # Tier 1 OCR: RapidOCRPDF
                    if HAS_RAPIDOCR_PDF:
                        ocr_text = self._ocr_page_with_rapidocr(page_num)

                    # Tier 2/3 OCR Fallback: Render image and test Tesseract / Windows WinRT
                    if not ocr_text:
                        pix = page.get_pixmap(dpi=150)
                        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_img:
                            tmp_img_path = tmp_img.name
                        pix.save(tmp_img_path)
                        try:
                            ocr_text = self._ocr_fallback_image(tmp_img_path)
                        finally:
                            if os.path.exists(tmp_img_path):
                                os.remove(tmp_img_path)

                    if ocr_text:
                        text = ocr_text
                        method_used = "OCR Engine"
                        stats["ocr_pages"] += 1
                    else:
                        if len(text) >= self.min_chars:
                            method_used = "Text Layer (Low Density)"
                            stats["text_layer_pages"] += 1
                        else:
                            method_used = "Gambar Scan (OCR Tidak Tersedia)"
                            stats["empty_pages"] += 1
                else:
                    stats["text_layer_pages"] += 1

                # If grep query specified, filter
                if grep_query:
                    if not re.search(grep_query, text, re.IGNORECASE):
                        continue

                extracted_pages.append({
                    "page_num": page_num,
                    "text": text,
                    "method": method_used,
                    "char_count": len(text)
                })

            doc.close()

        elif HAS_PYPDF:
            reader = pypdf.PdfReader(str(self.file_path))
            for p_idx in page_indices:
                page_num = p_idx + 1
                page = reader.pages[p_idx]
                text = page.extract_text() or ""
                text = text.strip()
                method_used = "Text Layer (PyPDF)"

                if len(text) >= self.min_chars:
                    stats["text_layer_pages"] += 1
                else:
                    method_used = "Gambar Scan / Teks Kosong"
                    stats["empty_pages"] += 1

                if grep_query:
                    if not re.search(grep_query, text, re.IGNORECASE):
                        continue

                extracted_pages.append({
                    "page_num": page_num,
                    "text": text,
                    "method": method_used,
                    "char_count": len(text)
                })

        return extracted_pages, stats


def build_markdown_report(file_path, extracted_pages, stats, grep_query=None):
    """Formats extracted content into structured Markdown optimized for LLM reading."""
    file_name = Path(file_path).name
    total_words = sum(len(p["text"].split()) for p in extracted_pages)
    est_tokens = int(total_words * 1.3)

    md = []
    md.append(f"# Dokumen Terekstrak: `{file_name}`")
    md.append("")
    md.append("### Ringkasan Ekstraksi")
    md.append(f"- **Total Halaman Dokumen**: {stats['total_pages']}")
    md.append(f"- **Halaman Diproses**: {len(extracted_pages)}")
    md.append(f"- **Halaman Teks Digital**: {stats['text_layer_pages']}")
    md.append(f"- **Halaman Hasil OCR**: {stats['ocr_pages']}")
    if stats['empty_pages'] > 0:
        md.append(f"- **Halaman Gambar/Scan Tanpa Teks**: {stats['empty_pages']}")
    md.append(f"- **Total Kata**: ±{total_words:,} kata")
    md.append(f"- **Estimasi Konsumsi Token LLM**: ±{est_tokens:,} tokens")
    if grep_query:
        md.append(f"- **Filter Keyword**: `{grep_query}`")
    md.append("")
    md.append("---")
    md.append("")

    for page in extracted_pages:
        md.append(f"## Halaman {page['page_num']} `[{page['method']}]`")
        md.append("")
        if page["text"]:
            md.append(page["text"])
        else:
            md.append("> *[Halaman ini tidak memuat teks atau berupa gambar tanpa OCR]*")
        md.append("")
        md.append("---")
        md.append("")

    return "\n".join(md)


def main():
    parser = argparse.ArgumentParser(
        description="Smart PDF Text & Scanned OCR Extractor for Academic Book Agents"
    )
    parser.add_argument("input_pdf", help="Path to target PDF file")
    parser.add_argument("-o", "--output", default=None, help="Output Markdown file path (default: <name>_extracted.md)")
    parser.add_argument("--toc-only", action="store_true", help="Extract only Table of Contents / Bookmarks (huge token saver)")
    parser.add_argument("--pages", default=None, help="Page range to extract (e.g. 1-10, 5, 1,3,5-8)")
    parser.add_argument("--grep", default=None, help="Filter only pages containing this search term/regex")
    parser.add_argument("--ocr", choices=["auto", "force", "off"], default="auto", help="OCR Mode: auto (default), force, or off")
    parser.add_argument("--min-chars", type=int, default=40, help="Minimum characters threshold before triggering OCR")
    parser.add_argument("--summary", action="store_true", help="Print summary to stdout only")

    args = parser.parse_args()

    input_path = Path(args.input_pdf)
    if not input_path.exists():
        print(f"Error: Input file '{args.input_pdf}' does not exist.", file=sys.stderr)
        sys.exit(1)

    extractor = SmartPDFExtractor(
        input_path,
        min_chars_per_page=args.min_chars,
        ocr_mode=args.ocr
    )

    # 1. TOC Only Mode
    if args.toc_only:
        toc_md = extractor.extract_toc_markdown()
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(toc_md)
            print(f"[+] Daftar Isi berhasil diekstrak ke: {args.output}")
        else:
            print(toc_md)
        return

    # 2. Extract Document Pages
    total_pages, _ = extractor.get_document_info()
    page_indices = parse_page_ranges(args.pages, total_pages)

    print(f"[*] Mengekstrak {len(page_indices)} dari {total_pages} halaman: '{input_path.name}' (OCR: {args.ocr})...")
    extracted_pages, stats = extractor.extract_content(page_indices, grep_query=args.grep)

    # 3. Format to Markdown
    report_md = build_markdown_report(input_path, extracted_pages, stats, grep_query=args.grep)

    # 4. Save Output
    out_path = args.output
    if not out_path:
        out_path = input_path.with_name(f"{input_path.stem}_extracted.md")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(report_md)

    total_words = sum(len(p["text"].split()) for p in extracted_pages)
    est_tokens = int(total_words * 1.3)

    print(f"[+] Berhasil! File Markdown disimpan ke: {out_path}")
    print(f"[i] Statistik: {stats['processed_pages']} hal diproses | {stats['text_layer_pages']} teks digital | {stats['ocr_pages']} OCR | {stats['empty_pages']} gambar kosong")
    print(f"[i] Estimasi Konsumsi Token: ±{est_tokens:,} tokens (Hemat vs biner PDF)")


if __name__ == "__main__":
    main()
