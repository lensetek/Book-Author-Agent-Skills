---
name: paper-to-monograf
description: Use to convert a single research paper, thesis chapter, dissertation segment, or focused research report into a monograph outline, chapter plan, and expansion strategy.
metadata:
  short-description: Convert research paper into monograph plan
---

# Paper To Monograf

Use this specialist when one paper or one focused research project is the core source.

## Agent Contract

Input:

- paper text or structured summary,
- research field,
- target readers,
- source bibliography if available,
- expected monograph length.

Output:

- `status`.
- `paper_extraction`.
- `monograph_focus`.
- `paper_to_chapter_map`.
- `state_of_the_art_expansion_plan`.
- `contribution_statement`.
- `citation_gaps`.
- `security_privacy_notes`.

## Process

1. Screen for confidential data, respondent identities, and unpublished sensitive findings.
2. Extract or import research artifacts (problem, theory, SotA matrices, hypothesis testing results, data science code/tables, findings, contribution, limitations, and references) directly from research workflow outputs.
3. Identify what can become a chapter and what needs expansion.
4. Build a focused monograph structure.
5. Separate original findings from broader interpretation.
6. Mark missing state-of-the-art sources and unverifiable claims.

## Rules

- Keep the monograph narrow.
- Do not over-generalize beyond the evidence.
- Do not invent references or research findings.
