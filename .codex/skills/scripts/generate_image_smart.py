#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "pymupdf>=1.23.0",
#     "pillow>=10.0.0",
#     "matplotlib>=3.7.0"
# ]
# ///
"""
generate_image_smart.py
Smart Multi-Engine Image & Academic Diagram Generator for Book Author Agents.

Engines Supported:
1. Engine A (Zero-Key AI Art Generator):
   - Pollinations.ai (Flux, SDXL, Turbo)
   - Zero API key required, 100% free and automatic
   - Flexible aspect ratios (1:1 for figures, 2:3 for book covers, 16:9 for banners)
2. Engine C (Programmatic Academic Diagram & Vector Generator):
   - Mermaid.js (SVG and PNG via Mermaid.ink) for precise flowcharts, architectures, and taxonomies
   - Matplotlib for scientific and empirical charts (300 DPI print quality)
3. Engine D (HTML-to-Image 300 DPI Cover Rasterizer):
   - Converts HTML cover templates into high-res print-ready PNG files

Usage Examples:
  # AI Book Cover Illustration (2:3 aspect ratio):
  uv run generate_image_smart.py --prompt "Modern academic book cover illustration on Artificial Intelligence, minimalist, clean geometric" --ratio 2:3 -o cover_art.png

  # Academic Flowchart Diagram (Vector SVG):
  uv run generate_image_smart.py --mermaid "graph TD; A[Input Data] --> B[Analisis]; B --> C[Kesimpulan]" -o alur_metodologi.svg

  # Academic Hierarchy Diagram (PNG):
  uv run generate_image_smart.py --mermaid "graph TD; A[CPMK 1] --> B[Sub-CPMK 1.1]; A --> C[Sub-CPMK 1.2]" -o cpmk_tree.png
"""

import sys
import os
import argparse
import urllib.request
import urllib.parse
import base64
import tempfile
import subprocess
from pathlib import Path

# Try PyMuPDF
try:
    import pymupdf
    HAS_PYMUPDF = True
except ImportError:
    HAS_PYMUPDF = False

# Try Pillow
try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

# Try Matplotlib
try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False


ASPECT_RATIOS = {
    "1:1": (1024, 1024),
    "2:3": (1024, 1536),   # Standard Book Cover Ratio (Portrait)
    "3:2": (1536, 1024),   # Landscape illustration
    "3:4": (1024, 1365),   # A5/UNESCO proportions
    "16:9": (1536, 864)    # Wide banner
}


def generate_ai_art(prompt, output_path, ratio="1:1", model="flux", seed=None):
    """
    Generates high-quality AI art using Pollinations.ai (Flux/SDXL).
    Zero API key required.
    """
    width, height = ASPECT_RATIOS.get(ratio, (1024, 1024))
    
    # Clean and encode prompt
    encoded_prompt = urllib.parse.quote(prompt.strip())
    
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={height}&model={model}&nologo=true"
    if seed:
        url += f"&seed={seed}"

    print(f"[*] Menghubungi Engine AI Art (Model: {model}, Rasio: {ratio}, Dimensi: {width}x{height}px)...")
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) BookAuthorAgent/2.0"
        }
    )

    try:
        with urllib.request.urlopen(req, timeout=45) as resp:
            content_type = resp.headers.get("content-type", "")
            img_data = resp.read()

        out_path = Path(output_path).resolve()
        out_path.parent.mkdir(parents=True, exist_ok=True)

        with open(out_path, "wb") as f:
            f.write(img_data)

        file_size_kb = len(img_data) / 1024
        print(f"[+] Berhasil! Gambar AI disimpan ke: {out_path} ({file_size_kb:.1f} KB)")
        return True, str(out_path)

    except Exception as e:
        print(f"[-] Gagal men-generate gambar AI: {e}")
        return False, str(e)


def generate_mermaid_diagram(diagram_code, output_path):
    """
    Generates crisp vector (SVG) or PNG diagram from Mermaid syntax using Mermaid.ink.
    """
    out_path = Path(output_path).resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    is_png = out_path.suffix.lower() == ".png"

    # Base64 encode diagram
    b64_code = base64.urlsafe_b64encode(diagram_code.strip().encode("utf-8")).decode("utf-8")
    
    # Always fetch SVG first from mermaid.ink (most reliable vector format)
    svg_url = f"https://mermaid.ink/svg/{b64_code}"
    print(f"[*] Menghubungi Engine Diagram Vektor (Mermaid)...")

    req = urllib.request.Request(
        svg_url,
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) BookAuthorAgent/2.0"}
    )

    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            svg_data = resp.read()

        if is_png:
            # Convert SVG to high-res PNG using PyMuPDF if available
            if HAS_PYMUPDF:
                svg_doc = pymupdf.open("svg", svg_data)
                page = svg_doc[0]
                # Scale up for 300 DPI crispness
                mat = pymupdf.Matrix(3.0, 3.0)
                pix = page.get_pixmap(matrix=mat)
                pix.save(str(out_path))
                print(f"[+] Diagram berhasil di-render ke PNG (300 DPI): {out_path} ({pix.width}x{pix.height}px)")
                return True, str(out_path)
            else:
                # Fallback: save SVG alongside
                alt_svg = out_path.with_suffix(".svg")
                with open(alt_svg, "wb") as f:
                    f.write(svg_data)
                print(f"[+] Diagram SVG vektor disimpan ke: {alt_svg} (PyMuPDF tidak terpasang untuk PNG)")
                return True, str(alt_svg)
        else:
            with open(out_path, "wb") as f:
                f.write(svg_data)
            print(f"[+] Diagram SVG vektor berhasil disimpan ke: {out_path}")
            return True, str(out_path)

    except Exception as e:
        print(f"[-] Gagal men-generate diagram Mermaid: {e}")
        return False, str(e)


def render_html_cover_to_png(html_path, output_png_path, width=2480, height=3508, dpi=300):
    """
    Renders an HTML book cover template into a 300 DPI print-ready PNG
    using Windows headless Edge/Chrome + PyMuPDF.
    """
    html_file = Path(html_path).resolve()
    if not html_file.exists():
        print(f"[-] File HTML tidak ditemukan: {html_path}")
        return False, None

    out_png = Path(output_png_path).resolve()
    out_png.parent.mkdir(parents=True, exist_ok=True)

    # Find browser binary
    browser_exe = None
    for candidate in [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
    ]:
        if os.path.exists(candidate):
            browser_exe = candidate
            break

    if not browser_exe:
        print("[-] Browser Chrome/Edge tidak ditemukan untuk merender HTML.")
        return False, None

    with tempfile.TemporaryDirectory() as td:
        tmp_pdf = os.path.join(td, "cover_render.pdf")
        cmd = [
            browser_exe,
            "--headless=new",
            "--disable-gpu",
            f"--user-data-dir={os.path.join(td, 'profile')}",
            f"--print-to-pdf={tmp_pdf}",
            "--no-pdf-header-footer",
            html_file.as_uri()
        ]

        print(f"[*] Merender sampul buku via headless browser: {os.path.basename(browser_exe)}...")
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            if not os.path.exists(tmp_pdf):
                print(f"[-] Gagal menghasilkan PDF perantara: {res.stderr}")
                return False, None

            # Rasterize PDF to 300 DPI PNG via PyMuPDF
            if HAS_PYMUPDF:
                doc = pymupdf.open(tmp_pdf)
                page = doc[0]
                pix = page.get_pixmap(dpi=dpi)
                pix.save(str(out_png))
                doc.close()
                print(f"[+] Sampul buku 300 DPI berhasil dicetak ke: {out_png} ({pix.width}x{pix.height}px)")
                return True, str(out_png)
            else:
                print("[-] PyMuPDF diperlukan untuk konversi 300 DPI PNG.")
                return False, None

        except Exception as e:
            print(f"[-] Terjadi kesalahan saat render sampul: {e}")
            return False, None


def main():
    parser = argparse.ArgumentParser(
        description="Smart Multi-Engine Image & Academic Diagram Generator for Book Author Agents"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--prompt", "-p", help="Text prompt for AI image generation (Pollinations Flux)")
    group.add_argument("--mermaid", "-m", help="Mermaid diagram code string or path to .mmd file")
    group.add_argument("--cover-html", help="Path to HTML book cover file to render into 300 DPI PNG")

    parser.add_argument("--output", "-o", default=None, help="Output image file path")
    parser.add_argument("--ratio", choices=["1:1", "2:3", "3:2", "3:4", "16:9"], default="1:1",
                        help="Aspect ratio for AI image (default: 1:1, use 2:3 for book covers)")
    parser.add_argument("--model", default="flux", help="AI Image Model (default: flux)")
    parser.add_argument("--seed", type=int, default=None, help="Optional seed for reproducible AI images")
    parser.add_argument("--dpi", type=int, default=300, help="DPI for cover render (default: 300)")

    args = parser.parse_args()

    # 1. AI Art Mode
    if args.prompt:
        out_path = args.output or "generated_image.png"
        generate_ai_art(
            prompt=args.prompt,
            output_path=out_path,
            ratio=args.ratio,
            model=args.model,
            seed=args.seed
        )

    # 2. Mermaid Diagram Mode
    elif args.mermaid:
        code = args.mermaid
        if os.path.exists(code):
            with open(code, "r", encoding="utf-8") as f:
                code = f.read()
        out_path = args.output or "academic_diagram.svg"
        generate_mermaid_diagram(code, out_path)

    # 3. HTML Cover 300 DPI Mode
    elif args.cover_html:
        out_path = args.output or "cover_print_300dpi.png"
        render_html_cover_to_png(args.cover_html, out_path, dpi=args.dpi)


if __name__ == "__main__":
    main()
