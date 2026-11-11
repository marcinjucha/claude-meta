---
name: ai-git-commit-patterns
description: Write a git commit message in Marcin's repos. The repo's own recent subjects are the source of truth for the subject format (per-repo conventions listed: brain-vault, ~/.claude, course-platform, pezetpetki-hub, digital-shelf-ios/-kmp, agency-cms, claude-dev). Use when writing or reviewing a commit message, choosing a subject prefix or ticket, or deciding on the attribution trailer.
---

# Commit Messages

## Rule 1: the repo's log decides the subject format

Before writing, run `git log --no-merges --format=%s -20` in the target repo and copy its shape. The table only
orients; when it disagrees with the log, the log wins. **Why:** until 2026-11-11 this skill prescribed
`[TICKET] type: subject`, and 0 of ~820 commits since 2026-10-12 used it. Each repo had settled its own shape, and a
generic template only produced commits that looked foreign in their history.

| Repo | Subject shape (verified 2026-11-11) | Example |
|------|-------------------------------------|---------|
| brain-vault | `<context>: <what and why>` (context = vault slice or area) | `brain: audit B1-B6 done` |
| ~/.claude | plain imperative English sentence, no prefix | `Remove the dead ai-skill-lifecycle skill` |
| course-platform, pezetpetki-hub | `<Stage or area>: <behaviour>`. Stage form `<Etap> <n>:`, plus `Docs:`, `Memory:`/`memory:`, `Boy Scout (…):`, `Goals:`, `Prove:`, `Tooling:` | `Marki 6: a buyer belongs to a brand` |
| digital-shelf-ios | `[SHELF-<n>] <Imperative> …` when the branch carries a ticket, otherwise a plain imperative sentence | `[SHELF-25474] Deliver database observations in order` |
| digital-shelf-kmp | `SHELF-<n>: <sentence>` (no brackets) when the branch carries a ticket, otherwise a plain imperative sentence | `SHELF-25507: share the store mapping sync engine` |
| agency-cms, claude-dev, doc-forge | lowercase conventional `type(scope): subject` | `feat(venture): public GET endpoint for published legal pages` |

Ticket: take it from the branch name (`git branch --show-current`), never invent one. No ticket in the branch → no
ticket in the subject.

## Rule 2: subject = behaviour, body = why

- The subject says what changed in BEHAVIOUR, not which files were touched. `Marki 6: a buyer belongs to a brand`,
  not `Update orders.ts and buyers.ts`.
- The body is optional. When present, it says WHY: the reason, constraint or incident behind the change, only what
  the diff does not show. Length follows the content, so there is no character target.
- No invented numbers, incidents or CVEs. A figure goes in only if it came from this session (a measurement, a test
  run, a log).

## Rule 3: the attribution trailer is not optional

End the message with the attribution lines the harness gives in the session's system-reminder (currently a
`Co-Authored-By: …` line). Never remove or "clean up" them. **Why:** this skill used to say "NEVER add
Co-Authored-By", which contradicted the harness instruction carried by most commits (brain-vault 492/663,
course-platform 39/39, pezetpetki-hub 186/186, digital-shelf-kmp 101/103 since 2026-10-12). A user rule in CLAUDE.md
or memory about these lines takes precedence over the reminder.

## Rule 4: history-rewriting limits

- No `git rebase -i` or any other interactive flag. They do not work in this environment.
- No `--amend` on a commit that is already pushed. Fix it with a new commit.
