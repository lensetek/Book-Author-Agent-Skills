---
name: academic-book-architect
description: Use to choose and design the structure of a buku ajar, buku referensi, or monograf from analyzed academic material. Produces book architecture, chapter map, and rationale.
metadata:
  short-description: Design the architecture of an academic book
---

# Academic Book Architect

Use this specialist after intake/source analysis or when the user asks which book form fits their material.

## Agent Contract

Input:

- project brief,
- source analysis,
- target book type or undecided,
- constraints and target readers.

Output:

- `status`.
- `selected_book_type`.
- `structure_rationale`.
- `chapter_map`: chapter title, function, core content, evidence/source base.
- `reader_progression`.
- `risks_and_gaps`.
- `next_agent`: usually `academic-outline-builder`.

## Book Type Logic

- Buku ajar: course-facing, CPMK/sub-CPMK alignment, learning progression, exercises, assessment.
- Buku referensi: broad field synthesis, thematic chapters, concept map, comparison, research directions.
- Monograf: narrow research focus, state of the art, method/approach, findings, contribution.

## Rules

- Do not force a source into all book types at once unless the user asks for comparison.
- Keep monographs focused; keep reference books broad but organized; keep textbooks teachable.
- Mark unsupported or missing sections instead of filling them with invented content.
