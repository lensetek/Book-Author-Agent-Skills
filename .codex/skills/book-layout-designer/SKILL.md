---
name: book-layout-designer
description: Use to design the interior layout system for academic books, including chapter opener pages, headers, footers, page numbering, margins, heading hierarchy, tables, figures, captions, callouts, and readability guidance.
metadata:
  short-description: Design academic book interior layout
---

# Book Layout Designer

Use this specialist after the manuscript structure is stable and before DOCX/PDF export.

## Agent Contract

Input:

- manuscript structure or sample chapter,
- book type,
- page size: UNESCO, A5, A4, or custom,
- target readers,
- publisher/campus requirements,
- branding/style preferences,
- figures, tables, exercises, callouts, or special blocks.

Output:

- `status`: ready, needs_input, blocked_security, or completed.
- `layout_system`.
- `page_size_and_margin_spec`.
- `chapter_opener_design`.
- `header_footer_spec`.
- `page_numbering_spec`.
- `heading_and_body_style_spec`.
- `table_figure_caption_spec`.
- `special_blocks_spec`.
- `readability_notes`.
- `security_privacy_notes`.

## Process

1. Check for sensitive metadata or private data in sample content.
2. Confirm page size; default to `UNESCO` as a label unless exact dimensions are required.
3. Design the hierarchy for chapter title, section headings, body text, captions, and notes.
4. Define header/footer patterns, including running title and page number placement.
5. Define chapter opener page style.
6. Provide layout guidance that can be implemented in DOCX, PDF, or desktop publishing tools.

## Rules

- Prioritize readability over decoration.
- Keep academic pages clean and consistent.
- For buku ajar, include styles for learning objectives, exercises, assignments, and summaries.
- For monographs/reference books, include styles for tables, figures, quotes, and synthesis boxes.
