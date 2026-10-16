# What's New / Catatan Rilis

Repository: [Book-Author-Agent-Skills](https://github.com/lensetek/Book-Author-Agent-Skills)  
License: MIT  
Total Agent Skills: **27**

---

## 🎨 Version 1.5.0

### English Summary
- **Multi-Engine Academic Graphics (`generate_image_smart.py`)**:
  - **Engine A (Pollinations.ai Flux / SDXL)**: Zero-key AI generation for book covers and thematic chapter illustrations with smart aspect ratio preservation (`1:1`, `2:3`, `16:9`).
  - **Engine C (Mermaid.ink Vector & High-Res PNG)**: Programmatic rendering of academic process flowcharts, conceptual frameworks, and system architectures into SVG and 300 DPI PNG without cloud authentication.
  - **Engine D (300 DPI Cover Rasterizer)**: Headless browser rendering of HTML/CSS book covers into 300 DPI high-resolution CMYK-ready print images (2550 x 3300 px) using PyMuPDF.
- **New Specialist Skill: `academic-figure-designer`**:
  - Dedicated agent for designing, rendering, and integrating academic figures into chapter drafts.
  - Enforces formal **APA 7th** captioning (`Figure X.Y: Descriptive Title`, `Note. Adapted from...`).
  - Produces narrative in-text explanations directly contextualized with the chapter's theoretical discussions.
- **Smart PDF & Scanned OCR Extractor (`extract_pdf_smart.py`)**:
  - Intelligent PDF text layer extraction with automatic scanned page detection.
  - Multi-tier local OCR fallback: `RapidOCRPDF` (ONNX runtime local), `pytesseract`, and native `Windows.Media.Ocr`.
  - Token-saving extraction modes: `--toc-only` (up to 95%+ token savings), `--pages`, and `--grep` query filtering. Enables non-multimodal and lightweight LLMs to digest complex academic sources and course syllabi without custom scripting.
- **Headless OMP 3.3.0.5 Submitter & Layman Wizard (`omp_headless_submitter.py`)**:
  - 100% browser- and Chrome DevTools MCP-independent publishing connector for PKP Open Monograph Press at `https://publisher.asadel.co.id/v2/index.php/ap`.
  - Interactive CLI wizard in Bahasa Indonesia with automated author account creation from manuscript metadata.
  - Headless HTTP session handling with automated CSRF token negotiation.
  - Safe Package Handoff generator (`--export-package`) with 1-second browser console auto-fill script (`autofill_helper.js`).

### Ringkasan Bahasa Indonesia
- **Generator Grafis Akademik Multi-Engine (`generate_image_smart.py`)**:
  - **Engine A (Pollinations.ai Flux / SDXL)**: Generasi gambar AI zero-key untuk ilustrasi sampul dan visual tematik bab dengan opsi rasio aspek (`1:1`, `2:3`, `16:9`).
  - **Engine C (Mermaid.ink Vektor & PNG 300 DPI)**: Render diagram alir proses, kerangka konseptual, dan arsitektur sistem ke dalam format SVG dan PNG 300 DPI tajam tanpa API key berbayar.
  - **Engine D (Rasterisasi Cover Cetak 300 DPI)**: Rendering cover HTML/CSS menjadi gambar beresolusi tinggi standar cetak 300 DPI (2550 x 3300 px) via browser headless dan PyMuPDF.
- **Skill Spesialis Baru: `academic-figure-designer` (Total: 27 Skills)**:
  - Agen khusus untuk merancang, me-render, dan menyematkan bagan ilmiah ke dalam draf bab.
  - Menegakkan penomoran dan keterangan gambar resmi standar **APA 7th** (`Gambar X.Y: Judul Deskriptif`, `Catatan. Diadaptasi dari...`).
  - Menghasilkan pembahasan naratif terintegrasi dalam paragraf bab (*in-text narrative grounding*).
- **Ekstraktor Cerdas Teks & OCR PDF Scan (`extract_pdf_smart.py`)**:
  - Ekstraksi teks lapis ganda dengan deteksi otomatis halaman hasil scan gambar.
  - Multi-tier OCR lokal: `RapidOCRPDF` (ONNX runtime lokal), `pytesseract`, dan native `Windows.Media.Ocr`.
  - Mode hemat token: `--toc-only` (hemat token hingga 95%+), pembatasan halaman `--pages`, dan filter `--grep`. Model non-multimodal dapat langsung membaca RPS dan literatur PDF tanpa script dadakan.
- **Submitter Headless OMP 3.3.0.5 & Wizard Penulis Awam (`omp_headless_submitter.py`)**:
  - Konektor penerbitan ke `https://publisher.asadel.co.id/v2/index.php/ap` 100% mandiri tanpa membutuhkan browser GUI atau Chrome DevTools MCP.
  - Menu CLI interaktif Bahasa Indonesia untuk pengguna awam dengan registrasi akun otomatis dari profil naskah.
  - Penanganan sesi CSRF HTTP headless otomatis.
  - Ekspor Paket Pengajuan Mandiri (`--export-package`) lengkap dengan panduan 3 menit dan kode autofill konsol browser 1 detik (`autofill_helper.js`).

---

## 🌐 Version 1.4.0

- **Integrasi Portal Open Monograph Press / OMP (`publisher.asadel.co.id`)**: Skill spesialis baru `omp-publisher-connector` untuk koneksi langsung ke portal OMP 3.3.0.5 di `https://publisher.asadel.co.id/v2/index.php/ap`.
- **Deteksi Bahasa Indonesia & Alur ISBN Perpusnas RI**: Menegakkan pemeriksaan bahasa naskah berbahasa Indonesia sebelum alur pendaftaran penerbitan ber-ISBN Perpusnas RI (sinopsis KDT, ORCID kontributor, dan subjek katalog Indonesia).
- **Opsi Login/Registrasi & Bantuan Auto-Fill Browser/MCP**: Mendukung alur panduan manual maupun bantuan pengisian otomatis via Browser/Chrome DevTools MCP dengan perlindungan privasi kredensial 100% aman.

---

## 📑 Version 1.3.0

- **Daftar Isi Otomatis Native Word & Auto-Formatter Standar Penerbit (`generate_standard_docx.py`)**: Generator Python langsung untuk Microsoft Word `.docx` dengan *Word XML Field Codes* bawaan (`TOC \o "1-3" \h \z \u`) yang menjamin nomor halaman dinamis, *dot leaders* rapi, tanpa perlu buat daftar isi manual.
- **Engine Layout Pembuka Bab Recto/Verso**: Memaksa setiap bab baru mulai di halaman kanan (Recto), jarak *Space Before* `120pt`, hierarki judul bab 2-baris, paragraf pertama tanpa indentasi, dan tabel standar 3-garis APA untuk semua preset penerbit (**PT. Asadel Liamsindo Teknologi**, **Asadel Publisher**, University Press, IKAPI, Springer/Elsevier).

---

## 🕸️ Version 1.2.0

- **Graphify Project-Isolated Knowledge Graph Harness**: Mengonversi Vault Obsidian, jaringan Zettelkasten, pohon prasyarat CPMK, dan kumpulan paper menjadi *knowledge graph* lokal yang dapat di-query (`graph.json` / `graph.html`) dengan isolasi data antar-proyek 100% aman.
- **Standalone Python Graphify Helper (`graphify_harness.py`)**: Memungkinkan indeksasi AST deterministik, pencarian konsep, penelusuran *neighbors*, kalkulasi *shortest-path*, dan injeksi otomatis `.gitignore` tanpa ketergantungan server cloud atau eksposur kunci API.

---

## 🛡️ Version 1.1.0

- **Verbatim Evidence Grounding & Audit Sitasi**: Menulis draf bab dalam paragraf akademis yang mengalir (*paraphrased synthesis*) sambil otomatis menarik kutipan verbatim dari OpenAlex, Crossref, dan PubMed untuk membuat matriks audit 100% faktual bebas halusinasi (`evidence_grounding_matrix.md`).
- **HITL Book Author Checklist (`hitl_book_checklist.md`)**: Menegakkan gerbang persetujuan penulis multi-fase dari Intake, Arsitektur CPMK, Draf Bab, Verifikasi Sitasi, hingga Layout/Export Final.
- **Standalone Python CLI Helpers**: Verifikasi DOI tanpa API key (`validate_references.py`), parser silabus RPS (`parse_rps.py`), dan pembuat matriks CPMK-ke-Bab (`build_cpmk_matrix.py`).
- **Jembatan Workflow Riset-ke-Buku**: Mengimpor secara langsung luaran riset (matriks SotA, pengujian hipotesis, ulasan literatur) ke pipeline ekspansi monograf dan buku referensi.
- **Engine Matematika & Formulasi LaTeX**: Penulisan formula matematika akademis cantik dan presisi di Markdown, Web Reader (MathJax/KaTeX), DOCX (persamaan interaktif Word OMML), dan PDF.
- **Integrasi Vault Obsidian**: Dukungan penuh berkas `.md` lokal, metadata YAML, tautan internal `[[...]]`, dan sintesis catatan Zettelkasten.
- **Edisi Digital Web Reader**: Hasilkan aplikasi web membaca buku berbasis *mobile-first*, serasi dengan smartphone/tablet, navigasi cepat, dan mode malam.
- **Preset Layout Penerbit Rekomendasi**: Dukungan preset tata letak langsung untuk penerbit nasional (**PT. Asadel Liamsindo Teknologi**, University Press UI/UGM/ITB/UT, IKAPI/Deepublish/Rajawali Pers) dan internasional (**Asadel Publisher**, Springer, Elsevier, Routledge, IEEE Press).
- **Dukungan CLI Installer `npx skills add`**: Instalasi cepat satu perintah melalui `npx skills add https://github.com/lensetek/Book-Author-Agent-Skills`.

---

## 🚀 Version 1.0.0

- Rilis inisial 24 agent skills untuk perancangan buku akademik (Buku Ajar, Buku Referensi, Monograf).
- Arsitektur berbasis peran: `book-author-orchestrator`, `academic-book-intake`, `academic-source-analyzer`, `academic-book-architect`, `academic-outline-builder`, `academic-chapter-writer`, `citation-integrity-reviewer`, `book-docx-exporter`, `book-pdf-exporter`, `book-cover-designer`, dll.
