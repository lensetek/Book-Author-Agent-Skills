---
name: format-export-preparer
description: Use to prepare final academic book manuscripts for Markdown, DOCX-ready structure, or publisher handoff, including front matter, back matter, heading consistency, glossary, figure/table lists, bibliography, and final privacy checks.
metadata:
  short-description: Prepare academic book manuscripts for export
---

# Format Export Preparer

Use this specialist near the end of the manuscript process.

## Agent Contract

Input:

- manuscript or chapter set,
- desired format: Markdown, DOCX-ready, publisher package,
- book metadata,
- bibliography,
- unresolved review notes.

Output:

- `status`.
- `final_structure`.
- `front_matter`.
- `body_structure`.
- `back_matter`.
- `formatting_notes`.
- `unresolved_items`.
- `security_privacy_notes`.

## Required Checks

- Title page fields: title, subtitle, author, affiliation, year.
- Preface/prakata if requested.
- Table of contents.
- Consistent heading levels.
- List of figures/tables when applicable.
- Glossary for technical terms when useful.
- Bibliography and unresolved citation gaps.
- Metadata/comment/privacy review if files are exported.

## Rules

- Do not silently remove unresolved citation gaps.
- Keep output structure clean enough for DOCX conversion.
- If credentials or personal data remain, return `blocked_security`.
