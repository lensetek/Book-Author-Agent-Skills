---
name: book-author-orchestrator
description: Use as the manager workflow for transforming an idea, RPS/course plan, research paper, thesis notes, or research corpus into an Indonesian academic book: buku ajar, buku referensi, or monograf. Routes work to specialist academic book agents that can also be called directly by Codex or any external agent system.
metadata:
  short-description: Build Indonesian academic books from ideas, RPS, or research papers
---

# Book Author Orchestrator

Use this skill to help a lecturer, researcher, or academic author develop a book manuscript from:

- a raw idea or topic brief,
- an RPS/course plan,
- one or more research papers,
- thesis/dissertation notes,
- research reports, datasets, or field notes.

The default output language is Indonesian academic prose. Support three book types: **buku ajar**, **buku referensi**, and **monograf**.

## First Response

Start by identifying the source path and target book type. If the user has not provided enough context, ask only for missing high-impact information:

- target book type: buku ajar, buku referensi, monograf, or undecided,
- source material: idea, RPS, single paper, multiple papers, or mixed documents,
- field/discipline and target readers,
- required standard: campus, publisher, accreditation, or grant output,
- desired output for this turn: brief, references, outline, chapter, review, edit, cover, layout, DOCX, PDF, or final package.

Before processing content, perform a security/privacy scan. If the input includes credentials, API keys, tokens, private student data, respondent identities, unpublished sensitive data, or frontend-exposed secrets, stop and ask the user to sanitize or approve a redacted workflow.

## Agent Roles

Use these specialist skills directly when the user asks for a narrow task. Use this orchestrator when the user wants end-to-end book development, is unsure which specialist to use, or provides mixed source material.

- **academic-book-intake**: clarify project goal, audience, discipline, standard, source type, book type, target length, and success criteria.
- **academic-source-analyzer**: extract concepts, findings, CPMK/sub-CPMK, key terms, argument structure, evidence, source gaps, and plagiarism/citation risks.
- **academic-reference-finder**: find paper/reference candidates using no-key sources such as Crossref, arXiv, PubMed/NCBI, Europe PMC, and unauthenticated Semantic Scholar when available.
- **academic-book-architect**: choose structure based on book type.
- **academic-outline-builder**: build table of contents, chapter objectives, chapter summaries, flow of argument, figures/tables needed, and missing sources.
- **academic-chapter-writer**: draft chapters in Indonesian academic style.
- **citation-integrity-reviewer**: mark claims needing citations, detect unsupported assertions, prevent fabricated references, and check bibliography consistency.
- **rps-to-buku-ajar**: convert RPS into buku ajar plan with pedagogy elements.
- **paper-to-monograf**: convert one paper or research project into monograph architecture.
- **research-synthesis-to-reference-book**: synthesize multiple sources into a buku referensi.
- **academic-book-reviewer**: independently review academic substance, book-type fit, contribution, pedagogy, novelty, and publication readiness.
- **academic-book-editor**: edit coherence, flow, terminology, repetition, style, readability, and academic tone.
- **format-export-preparer**: prepare final Markdown or DOCX-ready structure.
- **book-layout-designer**: design interior pages, chapter openers, headers, footers, page numbering, margins, and book typography.
- **book-cover-designer**: create front cover, back cover, and optional spine specifications or image prompts.
- **book-docx-exporter**: prepare editable DOCX export specifications for Word/Google Docs with styles, page setup, headers, footers, TOC, and metadata checks.
- **book-pdf-exporter**: prepare final PDF export specifications using default UNESCO size, A5, A4, or custom dimensions.
- **book-security-privacy-checker**: mandatory at intake and finalization. Check secrets, personal data, respondent data, metadata, and any frontend/client-side exposure risk.

## Routing Shortcuts

- User asks for cover, front/back cover, spine, or image prompt: route to `book-cover-designer`.
- User asks to find references, papers, DOI metadata, journals, or sources without credentials: route to `academic-reference-finder`.
- User asks for "referensi", "daftar pustaka", "paper pendukung", "cari jurnal", "sumber ilmiah", or "citation sources": route to `academic-reference-finder`.
- User asks for page design, chapter pages, header, footer, page numbers, typography, or interior layout: route to `book-layout-designer`.
- User asks for editable Word/Google Docs output, `.docx`, or publisher-editable manuscript: route to `book-docx-exporter`.
- User asks for final PDF, print proof, A5, A4, UNESCO, or custom book size: route to `book-pdf-exporter`.
- User asks for reviewer, kelayakan, substansi, novelty, contribution, or academic readiness: route to `academic-book-reviewer`.
- User asks for editing, style, flow, repetition, clarity, or language polish: route to `academic-book-editor`.

## External Agent Contract

These skills are portable agent specifications. Any non-Codex agent can use them by reading each `SKILL.md` as its system/task instruction.

Use this common input envelope when possible:

```json
{
  "task": "what the user wants",
  "book_type": "buku ajar | buku referensi | monograf | undecided",
  "source_type": "idea | rps | single_paper | multiple_papers | topic_needing_references | mixed",
  "discipline": "field or course",
  "audience": "target readers",
  "constraints": ["publisher/campus/style requirements"],
  "source_material": "text, file summary, or references",
  "desired_output": "brief | references | outline | chapter | review | edit | cover | layout | docx | pdf | final_package"
}
```

Every specialist should return:

- `status`: ready, needs_input, blocked_security, or completed.
- `output`: the requested artifact.
- `assumptions`: decisions made without full information.
- `reference_candidates`: candidate sources found or recommended, when relevant.
- `citation_gaps`: claims or sections needing sources.
- `security_privacy_notes`: sensitive-data findings without repeating secret values.

Reference-search default:

- Use no-key sources first: Crossref, arXiv, PubMed/NCBI E-utilities, Europe PMC, and unauthenticated Semantic Scholar when available.
- Do not require API keys for normal reference search.
- Do not scrape Google Scholar or bypass paywalls.
- If higher limits or private databases are requested, ask the user before using credentials and route any provided secret through `book-security-privacy-checker`.

## Workflow

1. **Intake**
   - Build a short project brief.
   - Confirm source path: idea, RPS, paper, multiple papers, or mixed source.
   - Run `book-security-privacy-checker`.

2. **Source Analysis**
   - Use `academic-source-analyzer`.
   - Use `academic-reference-finder` when source gaps, citation gaps, or literature expansion require online paper discovery.
   - For reference search, use no-key sources first and return DOI/metadata confidence notes.
   - Extract concepts, CPMK, methods, findings, key references, and gaps.
   - Separate facts from assumptions and missing evidence.

3. **Book Architecture**
   - Use `academic-book-architect`, or route directly to `rps-to-buku-ajar`, `paper-to-monograf`, or `research-synthesis-to-reference-book`.
   - Build a chapter map and explain why the structure fits.
   - Use `references/workflows.md` for source-specific workflows.

4. **Development**
   - Use `academic-outline-builder` before drafting unless the user asks directly for a chapter.
   - Write one chapter at a time for long manuscripts.
   - For buku ajar, include pedagogy elements.
   - For buku referensi/monograf, include synthesis and research positioning.

5. **Academic Review**
   - Apply `citation-integrity-reviewer`.
   - Apply `academic-book-reviewer` for academic substance and readiness.
   - Apply `academic-book-editor`.
   - Use `references/quality-checklists.md` for review criteria.

6. **Finalization**
   - Use `format-export-preparer`.
   - Add front matter and back matter as requested.
   - Use `book-layout-designer` for interior page design when final formatting or publishing is requested.
   - Use `book-cover-designer` when front/back cover or spine is requested.
   - Use `book-docx-exporter` for editable Word/Google Docs handoff.
   - Use `book-pdf-exporter` for final PDF proof or distribution.
   - Run `book-security-privacy-checker` before delivery.

7. **Production Order**
   - Preferred final package order: `format-export-preparer` -> `book-layout-designer` -> `book-docx-exporter` -> `academic-book-reviewer` or `academic-book-editor` if revisions are needed -> `book-pdf-exporter`.
   - DOCX is the preferred editable handoff for authors, editors, and publishers.
   - PDF is the final proof/distribution format after layout and DOCX review.
   - Default page size label is `UNESCO`; also support `A5`, `A4`, and `custom`. Ask for exact dimensions when technical export needs numerical measurements.

## Output Rules

- Use Indonesian academic prose by default.
- Never invent bibliographic details. If a source is unknown, write `[sumber perlu dilengkapi]`.
- Mark uncertain claims as assumptions or required verification.
- Keep author voice and discipline-specific terminology consistent.
- For RPS conversion, preserve CPMK/sub-CPMK alignment and learning progression.
- For paper conversion, distinguish original paper findings from broader interpretation.
- For monographs, keep focus narrow and contribution-driven.
- For book references, prioritize breadth, synthesis, and conceptual mapping.

## When To Load References

- Load `references/book-types.md` when choosing or explaining book type, chapter structure, or differences between buku ajar, buku referensi, and monograf.
- Load `references/workflows.md` when converting from a specific source type: idea, RPS, single paper, or multiple papers.
- Load `references/quality-checklists.md` when reviewing drafts, checking citations, adding pedagogy, preparing final output, or scanning security/privacy issues.
