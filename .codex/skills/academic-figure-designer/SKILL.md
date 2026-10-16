---
name: academic-figure-designer
description: Use to design, generate, and insert academic diagrams, conceptual frameworks, process flowcharts, and scientific figures for book chapters. Produces vector SVG/PNG diagrams via Mermaid, statistical charts, and AI illustrations with formal academic captioning and Markdown integration.
metadata:
  short-description: Design and generate academic figures, diagrams, and illustrations
---

# Academic Figure Designer

Use this specialist when an academic textbook, reference book, or monograph chapter requires visual figures, conceptual frameworks, process flowcharts, architecture diagrams, or thematic illustrations.

## Agent Contract

Input:

- `figure_type`: `diagram` (Mermaid/flowchart/architecture), `ai_art` (conceptual illustration), or `chart` (data/empirical).
- `caption_title`: formal Indonesian academic title (e.g., *"Gambar 2.1: Kerangka Kerja Algoritma Agentic AI"*).
- `chapter_context`: chapter number and specific topic where the visual figure will be anchored.
- `content_spec`: process steps, entity relationships, Mermaid syntax, or AI image description prompt.
- `output_format`: `svg` (crisp vector for web/digital) or `png` (300 DPI for DOCX/PDF print proofing).

Output:

- `status`: ready, needs_input, blocked_security, or completed.
- `figure_file_path`: saved path (e.g., `figures/fig_ch2_framework.svg` or `figures/fig_ch2_framework.png`).
- `markdown_embed_code`: standard Markdown image reference with APA 7th caption.
- `in_text_discussion`: 1-2 paragraph explanatory discussion referencing the figure in academic prose.
- `security_privacy_notes`: confirmation that no private data or secrets appear in the graphic.

---

## Process

### 1. Classify Figure Requirement
- **Category A (Academic Diagrams & Frameworks - Primary)**:
  - Flowcharts, hierarchical trees, system architectures, research methodology, CPMK learning paths.
  - Generates via: `uv run python .codex/skills/scripts/generate_image_smart.py --mermaid "graph TD; ..." -o figures/fig_X_Y.png`
  - Guarantees 100% sharp text, zero typographical hallucinations, and 300 DPI vector clarity.
- **Category B (Thematic Concept Illustrations)**:
  - High-level metaphorical or contextual illustrations (e.g., *"Representasi visual interaksi agen mandiri"*).
  - Generates via: `uv run python .codex/skills/scripts/generate_image_smart.py --prompt "..." --ratio 1:1 -o figures/fig_X_Y.png`
  - Uses zero-key Pollinations.ai FLUX engine.

### 2. Standardize File Storage & Academic Captioning
- Save all generated images in the project directory: `figures/` (e.g. `figures/gambar_1_1_kerangka_konsep.png`).
- Format caption according to Indonesian academic publishing standards (APA 7th):
  ```markdown
  ![Gambar 2.1: Kerangka Kerja Arsitektur Agentic AI](figures/gambar_2_1_arsitektur.png)
  *Gambar 2.1: Kerangka Kerja Arsitektur Agentic AI (Sumber: Olahan Penulis, 2026)*
  ```

### 3. Generate In-Text Discussion
- In academic books, a figure must never stand alone without narrative explanation.
- Always provide connecting prose that references the figure directly:
  > *"Sebagaimana diilustrasikan pada Gambar 2.1, alur komunikasi antar-agen dimulai dari modul persepsi..."*

---

## Rules

- **Zero Hallucination for Scientific Diagrams**: Never use text-to-image diffusion models for complex text diagrams or mathematical equations; always use vector Mermaid or Matplotlib.
- **Print Resolution Standard**: All PNG figures must be rendered at 300 DPI for publisher readiness.
- **Self-Contained Execution**: Always invoke `.codex/skills/scripts/generate_image_smart.py` to produce visual assets without requiring manual user intervention or paid API keys.
- **Privacy & Security**: Never include real institutional passwords, private API tokens, or respondent identities inside diagram nodes or charts.
