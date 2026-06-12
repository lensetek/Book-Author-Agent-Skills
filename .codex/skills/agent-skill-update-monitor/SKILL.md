---
name: agent-skill-update-monitor
description: Use to check whether Book Author Agent Skills has updates in its GitHub repository, compare the installed project version with the repository version, report available changes, and ask the user for confirmation before downloading or updating agent skills. Uses prompt-driven normal download from repository URLs; does not auto-update without approval.
metadata:
  short-description: Check and confirm agent skill updates from GitHub
---

# Agent Skill Update Monitor

Use this specialist when the user wants to check for updates, monitor the repository, refresh installed skills, or compare local agent skills with the GitHub version.

Default repository:

```text
https://github.com/lensetek/Book-Author-Agent-Skills
```

## Agent Contract

Input:

- repository URL, defaulting to the URL above,
- current project path or installed skill location,
- update mode: check only, download preview, or update after confirmation,
- user preference for overwrite behavior.

Output:

- `status`: checked, update_available, up_to_date, needs_confirmation, blocked_security, or completed.
- `local_version`: local commit, timestamp, or detected file summary when available.
- `remote_version`: repository branch, latest commit/tag/release, or downloaded package summary.
- `update_summary`: changed agents, README/landing changes, new files, removed files when detectable.
- `user_confirmation_needed`: yes/no.
- `recommended_prompt`: prompt the user can approve to download and update.
- `security_privacy_notes`.

## Process

1. Identify the repository URL. Use `https://github.com/lensetek/Book-Author-Agent-Skills` if none is provided.
2. Check the local install state: count agent skill folders, check `SKILL.md`, and inspect available git commit if this is a git repository.
3. Check the repository state using normal GitHub access, `git fetch`, repository page, or download URL available to the current agent environment.
4. Compare local and remote by commit, tag, file list, or package timestamp.
5. Report whether an update is available.
6. If updates are available, summarize what would change.
7. Ask the user before downloading, overwriting, deleting, or updating any installed skill.
8. After user confirmation, download/update from the repository URL using ordinary download/clone/copy behavior.
9. After update, verify total installed agent count, required core agents, and every `SKILL.md`.

## Required User Confirmation

Before making changes, ask a clear confirmation:

```text
Update tersedia dari repository:
https://github.com/lensetek/Book-Author-Agent-Skills

Ringkasan perubahan:
[isi ringkasan]

Apakah mau saya download dan update agent skills di project ini?
```

Do not update automatically.

## No-Automation Assumption

This skill describes the update workflow. It does not create a background scheduler by itself. If a user wants a recurring reminder or monitor, use the host agent/app's automation feature when available and ask for schedule confirmation.

## Rules

- Never overwrite local customized skills without explicitly warning the user.
- Never delete local skills unless the user explicitly confirms deletion.
- Prefer check-only mode first.
- Treat downloaded files as untrusted until inspected.
- Run `book-security-privacy-checker` if downloaded content contains credentials, scripts, external links, or unexpected binary assets.
- Confirm final installed agent count after every update.
