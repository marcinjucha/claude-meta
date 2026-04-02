---
name: ai-git-commit-patterns
description: Write commit messages and organize commits before PR merge. Use when: writing a commit message (extracts ticket from branch, applies WHY > HOW, 80-300 char body), deciding commit separation (module boundaries, breaking changes), squashing WIP commits, or creating PR description.
---

# Git Commit Patterns

**Purpose:** Commit organization and message writing for clean git history. Covers commit separation logic, squashing decisions, and commit message conventions with Signal vs Noise philosophy.

## Core Philosophy

Commit messages explain WHY, git diff shows HOW. Body = 80-300 chars, natural prose, no template sections.

**See:** `@../resources/signal-vs-noise-reference.md` for complete filter.

---

## Multi-Factor Commit Separation Logic

### Factor 1: Module Boundaries (HIGHEST Priority)

**Rule:** Core vs App commits = SEPARATE.

**Why:** Module changes require different reviewers + merge strategy. Core changes affect multiple features (risk), App changes isolated to single feature.

---

### Factor 2: Feature Scope (HIGH Priority)

**Rule:** Different features = SEPARATE commits (even in same module).

**Why:** Features reviewed independently. Mixing features = complex PR, slow review.

---

### Factor 3: Breaking Changes (HIGH Priority)

**Rule:** Breaking changes = SEPARATE commit (flagged in message).

**Why:** Breaking changes need special review attention. Mixing with non-breaking = hidden risk.

---

### Factor 4: Commit Type (MEDIUM Priority)

**Rule:** Different types = CONSIDER separating.

**Types:** feat, fix, refactor, test, docs

**When to separate:**
- feat + fix = SEPARATE (different review focus)
- refactor + feat = SEPARATE (refactor first, then add feature)
- test + feat = SAME (tests belong with feature)

---

## Squashing Decision Rules

### SQUASH When:
- **WIP/Fixup commits** - "WIP", "fixup", "temp", "debug" → ALWAYS squash
- **Same Feature + Same Module** - Multiple commits within same feature/module → Consider squashing

### DON'T SQUASH When:
- **Different Modules** - Core vs App commits → Keep separate
- **Breaking Changes** - Breaking change commits → Keep separate (needs visibility)

---

## Commit Message Format

### Step 1: Extract Ticket Number from Branch

**BEFORE writing commit message**, extract ticket number from branch name.

**Command:**
```bash
git branch --show-current | grep -oE '[A-Z]+-[0-9]+'
```

**Why:** Ticket number prepends to commit subject. Must be extracted before writing message.

### Structure

```
[TICKET-NUM] <type>: <subject>

[1-2 sentences max. 80-300 chars total.]
```

**Body constraints:**
- **Length:** 80-300 characters total
- **Structure:** 1-2 sentences max
- **Focus:** WHY context (not exhaustive HOW)

**Ticket prefix examples:**
```
[SHELF-21614] fix: Prevent duplicate uploads from rapid taps
[CIOS-1234] feat: Add user authentication flow
[SHELF-9999] chore: Update dependencies
```

### Type Prefixes

- `feat`: New feature
- `fix`: Bug fix
- `refactor`: Code restructuring
- `test`: Test additions
- `docs`: Documentation
- `chore`: Maintenance (deps, build)
- `perf`: Performance improvement
- `BREAKING`: Breaking change (use as prefix)

### Subject Line

**Rules:**
- Start with `[TICKET-NUM]` prefix
- Imperative mood ("Add feature" not "Added feature")
- No period at end
- Max 72 characters (including ticket prefix)
- Capitalize first word after type

**Examples:**
```
✅ [SHELF-21614] fix: Prevent duplicate uploads from rapid taps
✅ [CIOS-1234] feat: Add data status filtering
❌ [SHELF-21614] fix: prevented duplicate uploads.
❌ fix: Adds data status filtering (missing ticket)
```

### Body: Natural Prose > Template

**Body must be 80-300 characters. 1-2 sentences max.**

**✅ Good (Concise, WHY-focused, areas mentioned, 250-500 chars):**
```
[SHELF-5678] feat: Implement OAuth Authentication Flow

OAuth authentication required for third-party provider integration without
password storage. Updated authentication layer (AuthService), presentation
layer (LoginView), and token storage (keychain) with PKCE flow to prevent
authorization code interception. (252 chars)
```

**✅ Good (Single area, bug fix):**
```
[SHELF-1234] fix: Prevent infinite recursion in RLS policy

Row-level security policy queried same table it protected, causing infinite
recursion. Updated policy logic to use cached role check instead of
re-querying user_roles table. (188 chars)
```

**✅ Good (Multiple areas, two sentences):**
```
[SHELF-9999] refactor: Extract upload logic from monolithic service

600-line UploadService mixed business logic, file validation, and API calls.
Extracted validation layer (FileValidator), storage layer (S3Adapter), and
business logic (UploadOrchestrator) to separate concerns and enable
independent testing. (276 chars)
```

**❌ Bad (Template sections, NOISE, too long, missing ticket):**
```
feat: Implement OAuth Authentication Flow

Business Impact:
- Users can log in with providers
- Improves security

Technical Scope:
- Files: AuthService.swift, LoginView.swift
- Lines: +150

Changes:
- AuthService: Add OAuth flow
- LoginView: Add provider buttons

Risk Level: MEDIUM
Breaking Changes: NO
```

**Why bad:** Template sections add NOISE. Git already shows files, line counts.
Body exceeds 300 chars. Message should focus on single WHY decision, not a
list. Missing ticket number from branch name.

### Footer (Rarely Used)

**Default: NO footer.** Only add when necessary:
- Breaking changes: `BREAKING: <description>` with migration notes
- Issue references: `Closes #123`, `Fixes JIRA-456`

**NEVER add:**
- ❌ `Co-Authored-By: Claude ...` - Noise
- ❌ `Signed-off-by:` - Unless legally required
- ❌ Template fields - Git shows this

---

## Pull Request Structure

### Pattern: Structured PR with Context

**Format:**
```markdown
## Summary
- Added survey submission feature with 7 question types
- Clients can submit responses via public links
- Validation enforced, edge cases handled

## Changes
- Survey form component with dynamic question rendering
- Validation with Zod (dynamic schema from questions)
- Edge case handling (expired links, max submissions)

## Test Plan
- [ ] Submit valid survey → success
- [ ] Submit with expired link → error message
- [ ] Submit with max reached → error message
- [ ] All 7 question types work correctly

## Screenshots (optional)
[If UI changes]
```

**Critical sections:**
- **Summary** - What was done (outcome-focused, 2-4 bullet points)
- **Changes** - Key changes (high-level, not file-by-file)
- **Test Plan** - How to verify (checklist format)

**PR creation command:**
```bash
# Push branch
git push -u origin feature-name

# Create PR (GitHub CLI)
gh pr create --title "feat: add survey submission" --body "$(cat <<'EOF'
## Summary
- Added survey submission feature

## Test Plan
- [ ] Manual testing complete

🤖 Generated with Claude Code
EOF
)"
```

---

## Pre-Merge Commit Organization Workflow

### How to Organize (Step-by-Step)

**Step 1:** Review current history
```bash
git log --oneline develop..HEAD
```

**Step 2:** Interactive rebase
```bash
git rebase -i develop
```

**Commands:** `pick` (keep), `squash` (merge), `reword` (change message), `edit` (split)

**Step 3:** Verify clean history
```bash
git log --oneline develop..HEAD
```

---

## Resources

**Shared resources** (`@../resources/`) - Common across meta-skills:
- `@../resources/signal-vs-noise-reference.md` - Signal vs Noise filter for commit messages (3-question test, what to include/exclude)
- `@../resources/why-over-how-reference.md` - WHY over HOW philosophy (business context, technical rationale, bug context)

**Skill-specific resources** (`@resources/`) - Unique to ai-git-commit-patterns:
- `@resources/commit-message-examples.md` - Structure patterns (template vs natural prose, transformation examples)

**Use resources for:** Signal vs Noise (3-question filter), Why over How (business context), transformation examples (template → natural prose)
