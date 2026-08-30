---
name: omp-publisher-connector
description: Use to connect, register, log in, and submit Indonesian academic books for ISBN Perpusnas publication to the Open Monograph Press (OMP) portal at publisher.asadel.co.id. Supports manual author guidance or assisted browser/Chrome DevTools MCP form filling across OMP 4-step submission workflow.
metadata:
  short-description: OMP portal submission & ISBN Perpusnas publication helper for publisher.asadel.co.id
---

# Open Monograph Press (OMP) Publisher Connector

Use this specialist when the author is ready to publish their book manuscript to **PT. Asadel Liamsindo Teknologi / Asadel Publisher** via the Open Monograph Press (OMP 3.3.0.5) portal at `https://publisher.asadel.co.id/v2/index.php/ap`.

## Portal Endpoints

- **Portal Base URL**: `https://publisher.asadel.co.id/v2/index.php/ap`
- **Registration URL**: `https://publisher.asadel.co.id/v2/index.php/ap/user/register`
- **Login URL**: `https://publisher.asadel.co.id/v2/index.php/ap/login`
- **Submissions Info**: `https://publisher.asadel.co.id/v2/index.php/ap/about/submissions`
- **Author Submission Wizard**: `https://publisher.asadel.co.id/v2/index.php/ap/submission/wizard`

---

## Agent Contract

Input:

- `manuscript_files`: path to final DOCX/PDF manuscript, cover image, and front matter.
- `book_metadata`: title, subtitle, abstract/synopsis, keywords, language, author details (ORCID, affiliation).
- `user_account_choice`: `manual` (guide author with links & prefilled data) or `assisted` (auto-fill via browser/Chrome DevTools MCP).
- `target_isbn_type`: `ISBN Perpusnas RI` (requires Indonesian language detection).

Output:

- `status`: ready, needs_input, blocked_security, or completed.
- `language_validation`: verification that manuscript is in Bahasa Indonesia (`id_ID`).
- `account_setup_status`: login/register status (manual link provided or browser form filled).
- `omp_submission_payload`: structured 4-step metadata payload ready for OMP.
- `submission_step_status`: progress through OMP Submission Steps 1 to 4.
- `security_privacy_notes`: confirmation that no credentials or secrets were stored in logs/files.

---

## Process

### Step 1: Bahasa Indonesia Pre-Detection Gate
Before starting ISBN Perpusnas RI submission:
1. Scan manuscript title, abstract, and sample body text.
2. Confirm manuscript language is **Bahasa Indonesia (`id_ID`)**.
3. If manuscript is in English or another language, notify the user that national ISBN Perpusnas RI registration requires Indonesian language text or dual-language metadata, and ask whether to proceed with International Open Access publishing via Asadel Publisher instead.

### Step 2: Interactive Confirmation & Multi-Tier Fallback Setup
Before initiating OMP submission, present an **Interactive File & Metadata Confirmation Summary** to the author:
- 📄 **Main Manuscript**: Path, file name, & size verification.
- 🖼️ **Cover Image**: Path & resolution check.
- 📑 **Front Matter**: Path verification.
- 🌐 **Target Portal**: `https://publisher.asadel.co.id/v2/index.php/ap` (Open Monograph Press 3.3.0.5).
- 🏷️ **ISBN Target**: ISBN Perpusnas RI (Katalog Dalam Terbitan / KDT).

#### Multi-Tier File Upload Fallback Strategy:
1. **Tier 1: Direct Headless API Upload (Primary - Fast 2-5s)**:
   - Uses `python .codex/skills/scripts/omp_headless_submitter.py --input metadata.json --manuscript file.docx`.
   - Executes background multipart upload to OMP REST endpoints without visual browser lag or File Picker pop-ups.
2. **Tier 2: Direct DOM File Injection (Fallback A - Browser Automation)**:
   - If Headless API is unavailable or user prefers visual browser, injects file paths directly via Chrome DevTools Protocol (`DOM.setFileInputFiles`) / Playwright `setInputFiles()`.
   - Bypasses native Windows OS File Chooser pop-ups completely.
3. **Tier 3: Guided Manual Pick Handoff (Fallback B - User Assisted)**:
   - If Tier 1 & 2 encounter environment limits, agent pre-fills all 4 steps of OMP metadata (Title, Synopsis, Authors, Keywords), navigates to the File Upload modal, and presents a clear, step-by-step prompt:
     > *"Form metadata OMP telah terisi 100%. Silakan klik 'Upload File' dan pilih berkas `manuscript.docx` dari folder ini: `[File Path]`. Tekan Lanjut setelah berkas terpilih."*

### Step 3: OMP 4-Step Monograph Submission Workflow

#### 1. Submission Preparation (Step 1 of OMP Wizard)
- Set Submission Language: `id_ID` (Bahasa Indonesia).
- Select Book Series / Category: (Buku Ajar, Buku Referensi, or Monograf).
- Confirm Author Role: `Author` / `Editor`.
- Check all OMP Submission Requirements:
  - Manuscript formatted according to publisher layout guidelines.
  - No active publication elsewhere.
  - Bibliography & DOI citations verified.
  - Privacy Statement agreed.

#### 2. Upload Submission Files (Step 2 of OMP Wizard)
Organize and upload manuscript components via Tier 1 (Headless API), Tier 2 (DOM Injection), or Tier 3 (Guided Handoff):
- **Monograph File**: Main formatted `.docx` / `.pdf` manuscript (prepared by `generate_standard_docx.py`).
- **Cover Image**: `.jpg` / `.png` front cover.
- **Front Matter**: Title page, copyright page, preface, and Table of Contents `.pdf`.

#### 3. Enter Metadata (Step 3 of OMP Wizard)
Prepare and fill metadata aligned with Perpustakaan Nasional RI (ISBN & KDT) requirements:
- **Title & Subtitle**: Complete Indonesian title.
- **Abstract / Synopsis**: 200-500 word academic summary for Katalog Dalam Terbitan (KDT).
- **Contributors**: Full Name, Email, Country (`Indonesia / ID`), Affiliation (University/Institution), ORCID ID (https://orcid.org/...), and Brief Bio Statement.
- **Keywords / Subjek Katalog**: 3-5 Indonesian academic keywords.
- **Language**: `id` / `id_ID`.
- **Supporting Agencies**: Grant or funding agency details (if applicable).

#### 4. Confirmation & Submission Finish (Step 4 of OMP Wizard)
- Review final submission summary.
- Submit monograph to OMP editorial workflow.
- Record Submission ID and direct tracking URL for the author.

---

## Rules

- **Indonesian Language Requirement**: For ISBN Perpusnas RI publication, manuscript text MUST be in Bahasa Indonesia (`id_ID`).
- **Multi-Tier Fallback Enforcement**: Always attempt Tier 1 (Headless API) first. Fall back to Tier 2 (DOM Injection) and Tier 3 (Guided Handoff) seamlessly if needed.
- **Interactive Confirmation**: Always request author confirmation of file paths and book metadata before initiating web submission.
- **Credential Protection**: NEVER write user passwords, secret keys, or authentication tokens to disk, git history, or agent transcripts.
- **OMP Version Alignment**: Use endpoints compatible with Open Monograph Press 3.3.0.5 (`/v2/index.php/ap`).
- **User Autonomy**: Always respect user's choice between manual form entry and browser/MCP automation.
