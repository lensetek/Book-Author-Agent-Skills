---
name: book-cover-designer
description: Use to create front cover, back cover, and optional spine specifications or image prompts for academic books, including textbooks, reference books, and monographs. Produces size-aware cover briefs, visual direction, typography guidance, safe area notes, and print/export requirements.
metadata:
  short-description: Design academic book cover specifications
---

# Book Cover Designer

Use this specialist when the user needs a cover concept, image-generation prompt, design brief, or print-ready cover specification.

## Agent Contract

Input:

- title, subtitle, author/editor names,
- book type and discipline,
- target readers,
- page size: UNESCO, A5, A4, or custom,
- page count if spine is needed,
- publisher/logo/branding requirements,
- back-cover blurb, testimonials, ISBN/barcode if available,
- desired visual style and constraints.

Output:

- `status`: ready, needs_input, blocked_security, or completed.
- `cover_brief`.
- `front_cover_spec`.
- `back_cover_spec`.
- `spine_spec`: if page count is available.
- `image_generation_prompt`.
- `typography_and_color_direction`.
- `safe_area_and_print_notes`.
- `missing_assets`.
- `security_privacy_notes`.

## Process

1. Check whether supplied assets contain private data, credentials, or restricted logos.
2. Identify book type and academic tone.
3. Define front cover hierarchy: title, subtitle, author, affiliation, category badge, and official Asadel Publisher logo (`https://cdn.lensetek.com/logo.png`).
4. Define back cover: book blurb/synopsis, highlights box, ISBN Perpusnas barcode area, publisher contact block (`PT. ASADEL LIAMSINDO TEKNOLOGI` / `publisher.asadel.co.id`), and logo.
5. Generate interactive HTML+CSS+JS cover preview template using `assets/book_cover_template.html` and `python .codex/skills/scripts/generate_book_cover.py`.
6. Enable print-to-PDF export (`window.print()`) formatted for UNESCO/B5 print proofing.

## Rules

- **Logo Asset**: Always use `https://cdn.lensetek.com/logo.png` for Asadel Publisher cover headers and back cover branding.
- **HTML+JS Interactive Cover Engine**: Generate customizable HTML cover file using `python .codex/skills/scripts/generate_book_cover.py --title "..." --author "..." --isbn "..." --output cover.html`.
- **Back Cover Barcode Area**: Enforce dedicated SVG/EAN-13 barcode placeholder box with `ISBN 978-623-XXXX-XX-X` label on the back cover.
- Default page size label is `UNESCO` (15.5 x 23 cm); ask for exact dimensions if custom print-ready PDF requires specific bleed measurements.
- Do not expose or repeat sensitive asset metadata.
