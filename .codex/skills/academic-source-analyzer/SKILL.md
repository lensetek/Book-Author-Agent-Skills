---
name: academic-source-analyzer
description: Use to analyze ideas, RPS documents, research papers, thesis notes, or mixed academic sources before turning them into a book. Extracts concepts, findings, CPMK, evidence, gaps, citation risks, and privacy risks.
metadata:
  short-description: Analyze academic source material for book development
---

# Academic Source Analyzer

Use this specialist before outlining or drafting.

## Agent Contract

Input:

- source material or summary,
- source type,
- target book type if known,
- discipline,
- user goal.

Output:

- `status`.
- `source_summary`.
- `key_concepts`.
- `learning_outcomes`: CPMK/sub-CPMK if present.
- `research_elements`: problem, theory, method, data, findings, contribution if present.
- `book_potential`: recommended book type and rationale.
- `source_gaps`.
- `citation_gaps`.
- `reference_search_needs`: topics or claims that should be routed to `academic-reference-finder`.
- `security_privacy_notes`.

## Process

1. Screen for credentials, private data, respondent identities, and confidential material.
2. Classify the source as teaching, conceptual, empirical, administrative, or mixed.
3. Extract only what is supported by the source.
4. Separate facts, interpretations, and assumptions.
5. Identify what must be added before book drafting.
6. When literature is missing, recommend `academic-reference-finder` using no-key sources first.

## Rules

- Never invent bibliographic details.
- Preserve important terminology from the source.
- For RPS, prioritize CPMK, sub-CPMK, topics, assessment, and references.
- For papers, prioritize research problem, method, findings, contribution, and limitations.
