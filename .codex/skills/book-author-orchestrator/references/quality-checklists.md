# Quality Checklists

## Security And Privacy

Run at intake and before final delivery.

- Flag API keys, tokens, passwords, private URLs, database credentials, `.env` contents, and cloud credentials.
- Flag personal data: student names, IDs, emails, phone numbers, respondent identities, addresses, health data, grades, and consent-sensitive data.
- Flag confidential institutional data, unpublished restricted findings, or partner/client information.
- If building or reviewing an app/frontend, treat public frontend variables as exposed and ensure no credential is bundled client-side.
- Redact sensitive values before summarizing or transforming them.
- Tell the user what was found by category, not by repeating the secret value.

## Citation Integrity

- Do not invent authors, titles, journals, DOIs, page numbers, or years.
- Mark unsupported claims with `[perlu sitasi]`.
- Mark missing bibliographic details with `[detail referensi perlu dilengkapi]`.
- Distinguish direct findings from the source, interpretation by the author, and general background claims.
- Ensure every table, figure, adapted framework, statistic, and specific claim has a source or is clearly original.
- Prefer a "citation gap list" over silently smoothing unsupported text.

## Academic Quality

- The manuscript has a clear purpose and target reader.
- Chapter order moves from foundation to advanced discussion.
- Terms are defined consistently.
- Each chapter has a distinct function and avoids repetitive explanation.
- Arguments are supported by evidence.
- Transitions explain why the next section matters.
- The conclusion reflects the book type: learning mastery, field synthesis, or scholarly contribution.

## Pedagogy For Buku Ajar

- Each chapter maps to CPMK/sub-CPMK.
- Learning objectives use observable verbs.
- Examples are relevant to the discipline and student level.
- Exercises progress from recall to application/analysis.
- Assignments and rubrics match the intended learning outcomes.
- Summaries reinforce key concepts, not just repeat headings.
- Assessment prompts are fair based on material actually taught.

## Research Synthesis For Buku Referensi And Monograf

- The text compares sources instead of listing them one by one.
- The state of the art identifies patterns, disagreements, and gaps.
- Theoretical framing is explicit.
- Tables or matrices are used when they clarify comparison.
- The author's position or contribution is visible.
- Limitations are acknowledged.

## Final Packaging

- Include title page fields: title, subtitle, author, affiliation, year.
- Include preface/prakata if requested.
- Include table of contents.
- Include chapter titles and consistent heading levels.
- Include list of figures/tables when applicable.
- Include glossary for technical terms when useful.
- Include bibliography section and unresolved citation gap list.
- Check metadata and comments in final documents if files are exported.
