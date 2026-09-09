---
name: academic-book-intake
description: Use to clarify and structure an academic book project before writing. Produces a project brief for buku ajar, buku referensi, or monograf from an idea, RPS, paper, or mixed academic source.
metadata:
  short-description: Plan an Indonesian academic book project brief
---

# Academic Book Intake

Use this specialist when the user is starting a book project or when another agent needs a clear book brief before analysis, outlining, or drafting.

## Agent Contract

Portable beyond Codex: any agent can use this file as its instruction prompt.

Input:

- user goal,
- source type: idea, RPS, paper, multiple papers, mixed,
- target book type if known,
- discipline/course,
- target readers,
- institution/publisher constraints,
- expected output and deadline if available.

Output:

- `status`: ready, needs_input, blocked_security, or completed.
- `project_brief`: purpose, audience, source base, target book type, discipline, scope, constraints, and success criteria.
- `recommended_next_agent`: one of `academic-source-analyzer`, `rps-to-buku-ajar`, `paper-to-monograf`, `research-synthesis-to-reference-book`, or `academic-outline-builder`.
- `missing_inputs`: only high-impact missing information.
- `assumptions`.
- `security_privacy_notes`.

## Process

1. Run a quick security/privacy screen. Do not repeat exposed secrets.
2. If input materials include PDF documents (syllabus, RPS, papers), extract them into structured Markdown via `uv run .codex/skills/scripts/extract_pdf_smart.py <path_to_pdf>` rather than writing ad-hoc parser scripts.
3. Identify the dominant source type and likely book type.
4. Clarify the target reader: undergraduate, graduate, lecturer, researcher, practitioner, or general academic reader.
5. Capture standards: campus, publisher, accreditation, grant, or internal use.
6. Produce a concise project brief that downstream agents can use without re-asking basic questions.

## Rules

- Default to Indonesian academic context.
- When receiving PDF source files, always process them via `.codex/skills/scripts/extract_pdf_smart.py` to minimize token overhead and support scanned PDFs.
- If the user is unsure of book type, recommend one and explain the tradeoff briefly.
- Do not begin writing chapters unless explicitly asked.
- If credentials, private student/respondent data, or confidential institutional data appear, return `blocked_security` and request redaction.
