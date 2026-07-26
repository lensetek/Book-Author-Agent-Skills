---
name: academic-reference-finder
description: Use to find academic references and paper candidates without requiring API keys. Searches and structures references from no-key sources such as Crossref, arXiv, PubMed/NCBI E-utilities, Europe PMC, and unauthenticated Semantic Scholar when available. Produces candidate references, DOI checks, relevance notes, and citation gaps without fabricating metadata.
metadata:
  short-description: Find academic references using no-key sources
---

# Academic Reference Finder

Use this specialist when the user needs papers, references, DOI metadata, literature candidates, or source suggestions for a book chapter, outline, monograph, textbook, or reference book.

Default policy: **use no-key sources first**. Do not require API credentials unless the user explicitly asks for higher limits or a paid/private database.

## No-Key Source Priority

1. **Crossref REST API**: DOI and bibliographic metadata validation.
2. **arXiv API**: preprints in AI, computer science, mathematics, physics, quantitative biology, quantitative finance, statistics, and related fields.
3. **PubMed / NCBI E-utilities**: biomedical, health, medicine, pharmacy, life science.
4. **Europe PMC**: biomedical and life science, including open-access signals.
5. **Semantic Scholar unauthenticated access**: use only when available without API key; treat rate limits as strict.

Avoid sources that require credentials by default. Do not use Google Scholar scraping.

## Agent Contract

Input:

- topic, research question, chapter title, or claim needing support,
- discipline,
- target book type,
- date range if any,
- preferred language if any,
- required source type: journal article, book, conference paper, review, preprint, guideline, or mixed.

Output:

- `status`: ready, needs_input, blocked_security, or completed.
- `search_strategy`: keywords, synonyms, and no-key sources used.
- `reference_candidates`: title, authors, year, venue, DOI/URL if available, source API/site, and relevance note.
- `doi_metadata_checks`: validated DOI/metadata results from Crossref when available.
- `open_access_notes`.
- `citation_gaps_addressed`.
- `limitations`: missing metadata, paywalled full text, rate limits, or uncertain relevance.
- `security_privacy_notes`.

## Process

1. Check whether the query or source text contains private data or confidential unpublished findings.
2. Convert the topic into searchable keywords and synonyms.
3. Choose no-key sources by discipline.
4. Prefer metadata-rich results with DOI, year, venue, authors, and abstract.
5. Rank candidates by relevance, recency when appropriate, source quality, and book-section fit.
6. Execute `python .codex/skills/scripts/validate_references.py "<doi_list_json>"` to programmatically validate candidate DOIs, authors, titles, and publication years against Crossref and OpenAlex.
7. Mark anything uncertain instead of inventing details.

## Rules

- Never fabricate titles, authors, journals, DOI, volume, issue, pages, or year.
- If metadata is incomplete, write `[metadata perlu dilengkapi]`.
- If a claim still lacks a source, write `[perlu sitasi]`.
- Do not bypass paywalls or scrape restricted websites.
- Cache or reuse search results when possible; avoid repeated requests.
- If a user provides an API key, do not display it and route security concerns to `book-security-privacy-checker`.
