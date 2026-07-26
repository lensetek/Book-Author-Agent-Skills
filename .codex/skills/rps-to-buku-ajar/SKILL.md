---
name: rps-to-buku-ajar
description: Use to convert an RPS, syllabus, or course plan into a buku ajar structure with CPMK alignment, chapter plan, learning objectives, exercises, assignments, assessment prompts, and rubrics.
metadata:
  short-description: Convert RPS into a buku ajar plan
---

# RPS To Buku Ajar

Use this specialist when the source is RPS, syllabus, teaching plan, lecture notes, or course materials.

## Agent Contract

Input:

- RPS/syllabus text,
- course name and level,
- CPMK/sub-CPMK,
- meeting topics,
- references,
- assessment plan,
- target student profile.

Output:

- `status`.
- `rps_extraction`.
- `cpmk_chapter_matrix`.
- `buku_ajar_outline`.
- `chapter_template`.
- `exercise_assessment_plan`.
- `missing_inputs`.
- `security_privacy_notes`.

## Process

1. Screen for private student or lecturer data.
2. Execute `python .codex/skills/scripts/parse_rps.py "<rps_file_or_text>"` to programmatically extract course identity, description, CPMK/sub-CPMK, weekly topics, references, and assessments into structured JSON.
3. Execute `python .codex/skills/scripts/build_cpmk_matrix.py "<parsed_json>"` to generate `cpmk_matrix.md`.
4. Group topics into chapters based on concept progression.
5. Map each chapter to CPMK/sub-CPMK.
6. Add learning objectives, key concepts, examples, summaries, exercises, assignments, and assessment prompts.
7. Mark missing references and weak alignment.

## Rules

- Do not force one meeting into one chapter if the learning logic is better grouped.
- Use observable verbs for learning objectives.
- Keep assessment aligned with taught material.
