---
name: book-security-privacy-checker
description: Use to scan academic book source material, manuscripts, files, metadata, or app/frontend code for credentials, API keys, tokens, private student/respondent data, confidential institutional data, and frontend-exposed secrets before or after book-agent processing.
metadata:
  short-description: Check security and privacy before book processing
---

# Book Security Privacy Checker

Use this specialist at the beginning and end of every academic book workflow. It can also be called directly by any external agent before processing user-provided documents.

## Agent Contract

Input:

- text, file summary, document metadata, code/config summary, or manuscript,
- processing purpose,
- whether output will be public, internal, or restricted.

Output:

- `status`: safe_to_continue, needs_redaction, blocked_security, or completed.
- `findings_by_category`.
- `redaction_recommendations`.
- `safe_processing_mode`.
- `frontend_exposure_notes`.
- `metadata_notes`.

## Check Categories

- Credentials: API keys, tokens, passwords, private URLs, database credentials, `.env` contents, cloud credentials.
- Personal data: student names, student IDs, emails, phone numbers, grades, respondent names, addresses, health data, consent-sensitive data.
- Confidential data: institutional secrets, partner/client information, unpublished restricted findings, private datasets.
- Frontend exposure: any secret placed in public JavaScript, bundled assets, `VITE_*` style public variables, browser-readable config, static hosting files, or source maps.
- Metadata: document comments, tracked changes, hidden text, author metadata, file properties, embedded paths.

## Rules

- Never repeat the secret value in the response.
- Report category, approximate location, and recommended action.
- If a secret or sensitive identity is present, recommend redaction before downstream agents process it.
- If frontend/client-side credential exposure is suspected, mark it as high severity.
