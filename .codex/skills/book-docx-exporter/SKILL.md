---
name: book-docx-exporter
description: Use to prepare academic book manuscripts for editable DOCX export for Microsoft Word or Google Docs, including page size, margins, heading styles, header/footer, table of contents, captions, bibliography, and metadata/privacy checks.
metadata:
  short-description: Prepare editable DOCX export for academic books
---

# Book DOCX Exporter

Use this specialist when the user needs a DOCX-ready manuscript specification or wants a manuscript prepared for Word/Google Docs editing.

## Agent Contract

Input:

- final or near-final manuscript,
- layout specification if available,
- page size: UNESCO, A5, A4, or custom,
- publisher/campus template requirements,
- bibliography and unresolved citation notes,
- desired DOCX features: TOC, headers, footers, page numbers, captions, styles.

Output:

- `status`: ready, needs_input, blocked_security, or completed.
- `docx_export_spec`.
- `style_map`: title, subtitle, Heading 1/2/3, body, caption, quote, table, exercises.
- `page_setup`: size, margins, orientation.
- `header_footer_plan`.
- `toc_and_lists_plan`.
- `metadata_privacy_check`.
- `unresolved_items`.
- `security_privacy_notes`.

## Process

1. Run security/privacy and document metadata checks.
2. Confirm publisher preset and page size; default to `PT. Asadel Liamsindo Teknologi` (UNESCO 15.5x23 cm) for Indonesian manuscripts or `Asadel Publisher` (Royal 15.6x23.4 cm) for International manuscripts. Popular publisher options (University Press, Deepublish, Erlangga, Springer, Elsevier) are also supported.
3. Map manuscript elements to editable Word styles using the standalone Python generator `python .codex/skills/scripts/generate_standard_docx.py`.
4. Generate dynamic Table of Contents using native Word XML Field Codes (`TOC \o "1-3" \h \z \u`) rather than plain text.
5. Apply Recto (Odd Page) Section Breaks and 120pt Space Before for clean Chapter Openers.
6. Enforce No-Indent on the first paragraph after any heading, followed by 0.63cm First-Line Indent on subsequent paragraphs.
7. Preserve editability; do not flatten text into images.
8. Recommend PDF export only after DOCX review/layout is approved.

## Rules

- **Default Text Alignment**: ALL body text paragraphs in generated DOCX files and export specifications MUST use **Justified (Rata Kanan-Kiri)** alignment (`alignment: justify`) by default. Headings, captions, and callout titles maintain their specified design alignment.
- **Native Word TOC**: ALL Table of Contents elements MUST be generated via Word Field Codes (`w:fldSimple` / `TOC \o "1-3" \h \z \u`) to guarantee dynamic page numbering and dot leaders.
- **Standalone Helper Execution**: Run `python .codex/skills/scripts/generate_standard_docx.py --input manuscript.md --output book.docx --preset asadel-id` for direct automated formatting.
- DOCX is the preferred editable handoff format for authors, editors, and publishers.
- Mark missing dimensions as `[exact size needed for technical export]`.
- Do not silently remove unresolved citation gaps.
- If private data or credentials remain, return `blocked_security`.
