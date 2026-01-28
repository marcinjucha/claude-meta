---
name: git-commit-patterns
description: Git commit organization and message patterns. Use when organizing commits for PR, deciding squashing strategy, writing commit messages, or creating pull requests. Applies Signal vs Noise philosophy (WHY > HOW, natural prose over templates). Includes multi-factor separation logic and squashing decision rules. Critical for clean git history and efficient PR reviews.
---

# Git Commit Patterns

**Purpose:** Commit organization and message writing for clean git history. Covers commit separation logic, squashing decisions, and commit message conventions with Signal vs Noise philosophy.

---

## Core Philosophy

**Signal vs Noise: WHY > HOW**

Commit messages explain WHY, git diff shows HOW.

**SIGNAL (Keep):**
- Business context (why feature/fix needed)
- Technical rationale (why this approach over alternatives)
- Non-obvious decisions (architecture choices, edge cases)
- Bug context (root cause, why fix correct)
- Cross-platform alignment (if applicable)

**NOISE (Remove):**
- File names (git stat shows)
- Line counts (git diff shows)
- "Changes:" lists (redundant with git)
- HOW implementation (code shows this)
- Risk assessments (belongs in PR review)

**See:** `@resources/signal-vs-noise-reference.md` for complete filter and examples.

---

## Multi-Factor Commit Separation Logic

### Factor 1: Module Boundaries (HIGHEST Priority)

**Rule:** Core vs App commits = SEPARATE.

**Why:** Module changes require different reviewers + merge strategy. Core changes affect multiple features (risk), App changes isolated to single feature.

**Example:**
```bash
# Commit 1: Core module changes
git commit -m "Add DataAccessLayer to Core module

Implements reactive data access with observer pattern.
Adds indexes for foreign key constraints.
Used by FeatureA + FeatureB.

Module: Core/DataLayer
Breaking: No"

# Commit 2: App layer usage
git commit -m "Integrate filtering in FeatureX

Add filter UI panel.
Connect to DataAccessLayer.
Update tests.

Module: App/Features
Breaking: No"
```

---

### Factor 2: Feature Scope (HIGH Priority)

**Rule:** Different features = SEPARATE commits (even in same module).

**Why:** Features reviewed independently. Mixing features = complex PR, slow review.

**Example:**
```bash
# Commit 1: FeatureA
git commit -m "Add status filtering to FeatureA

Filter by completed/pending states.
Update list component.

Feature: FeatureA"

# Commit 2: FeatureB
git commit -m "Add name editing to FeatureB

Inline editing in list view.
Validation + persistence.

Feature: FeatureB"
```

---

### Factor 3: Breaking Changes (HIGH Priority)

**Rule:** Breaking changes = SEPARATE commit (flagged in message).

**Why:** Breaking changes need special review attention. Mixing with non-breaking = hidden risk.

**Example:**
```bash
# Commit 1: Breaking change
git commit -m "BREAKING: Change DataRepository API signature

fetchData() now requires contextId parameter.
Removed default context fallback (unreliable behavior).

BREAKING: All callers must pass contextId explicitly
Migration: Update 12 call sites (see diff)"

# Commit 2: Non-breaking implementation
git commit -m "Add caching to improve performance

Cache data in memory for 5 minutes.
Reduces database queries by 80%.

Breaking: No"
```

---

### Factor 4: Commit Type (MEDIUM Priority)

**Rule:** Different types = CONSIDER separating.

**Types:**
- **feat**: New functionality
- **fix**: Bug fix
- **refactor**: Code restructuring (no behavior change)
- **test**: Test additions/updates
- **docs**: Documentation only

**When to separate:**
- feat + fix = SEPARATE (different review focus)
- refactor + feat = SEPARATE (refactor first, then add feature)
- test + feat = SAME (tests belong with feature)

**Example:**
```bash
# Commit 1: Refactor (groundwork)
git commit -m "refactor: Extract filtering logic to service layer

Move filtering from use case to service.
Prepare for multi-feature reuse.

Type: refactor"

# Commit 2: Feature (builds on refactor)
git commit -m "feat: Add date range filtering

Add date picker UI component.
Integrate with DataService.

Type: feat
Depends-On: Previous refactor commit"
```

---

## Squashing Decision Rules

### Rule 1: WIP/Fixup Commits = SQUASH

**Pattern:** "WIP", "fixup", "temp", "debug" → ALWAYS squash.

**Example:**
```bash
# Before squash:
- feat: Add data filtering
- WIP
- fixup tests
- Fix typo
- Debug logging

# After squash:
- feat: Add data filtering with tests
```

---

### Rule 2: Same Feature + Same Module = SQUASH

**Pattern:** Multiple commits within same feature/module → Consider squashing.

**Example:**
```bash
# Before squash:
- Add filter UI
- Connect to data layer
- Add tests
- Update documentation

# After squash:
- feat: Add data filtering feature

  Implements status + date range filtering with UI panel,
  data layer integration, and comprehensive tests.
```

---

### Rule 3: Different Modules = DON'T SQUASH

**Pattern:** Core vs App commits → Keep separate.

**Example:**
```bash
# Keep separate (different modules):
- feat: Add DataAccessLayer to Core module
- feat: Integrate filtering in FeatureX (App layer)
```

---

### Rule 4: Breaking Changes = DON'T SQUASH

**Pattern:** Breaking change commits → Keep separate (needs visibility).

**Example:**
```bash
# Keep separate (breaking change needs attention):
- BREAKING: Change DataRepository API
- feat: Use new API in FeatureX
```

---

## Commit Message Format

### Structure

```
<type>: <subject>

[Paragraph 1: Business context - why this change matters]

[Paragraph 2: Technical decision with rationale - why this approach]

[Paragraph 3: Additional context - bug fixes, edge cases, constraints]

[Paragraph 4 (optional): Cross-cutting concerns - platform alignment, migration notes]
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
- Imperative mood ("Add feature" not "Added feature")
- No period at end
- Max 72 characters
- Capitalize first word

**Examples:**
```
✅ feat: Add data status filtering
❌ feat: added data status filtering.
❌ feat: Adds data status filtering
```

### Body: Natural Prose > Template

**✅ Good (Natural prose, WHY-focused):**
```
feat: Implement OAuth Authentication Flow

OAuth authentication required because third-party identity providers don't
expose passwords to apps. Delegating authentication improves security (no
password storage) and reduces user friction (single sign-on).

Authorization code flow with PKCE chosen over implicit flow because implicit
flow deprecated for security reasons. PKCE prevents authorization code
interception without adding server-side complexity.

Token refresh 5 minutes before expiry prevents authentication failures during
long-running operations. Without proactive refresh, operations spanning token
lifetime would fail mid-execution, forcing user re-authentication.
```

**❌ Bad (Template with sections, NOISE):**
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
Message should focus on WHY (business context, decisions), not WHAT (git shows).

### Footer (Rarely Used)

**IMPORTANT: Default is NO footer.** Only add when absolutely necessary.

**When to add:**
- Breaking changes: `BREAKING: <description>` with migration notes
- Issue references: `Closes #123`, `Fixes JIRA-456`

**NEVER add:**
- ❌ `Co-Authored-By: Claude ...` - Obvious noise, adds no value
- ❌ `Signed-off-by:` - Unless legally required by project
- ❌ Template fields (Risk Level, Files Changed, etc.) - Git shows this

**Example (Breaking change with footer):**
```
BREAKING: Change repository API signature

Repository methods now require explicit context parameter because default
context caused data isolation bugs in multi-user scenarios. All callers must
pass context explicitly.

Migration:
- Old: repository.fetch()
- New: repository.fetch(context: userContext)

Closes ISSUE-1234
```

**Example (Normal commit - NO footer):**
```
feat: Add survey submission feature

Clients can now submit survey responses via public links.
Form validates inputs and saves to database with tenant isolation.

[END - No footer needed]
```

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

### Step 1: Review Commits

```bash
git log --oneline develop..HEAD
```

**Look for:**
- WIP/fixup commits (squash)
- Module boundary violations (separate)
- Feature scope violations (separate)
- Breaking changes (keep separate)

### Step 2: Interactive Rebase

```bash
git rebase -i develop
```

**Commands:**
- `pick`: Keep commit as-is
- `squash`: Merge with previous commit
- `reword`: Change commit message
- `edit`: Stop to split commit

### Step 3: Verify Clean History

```bash
git log --oneline develop..HEAD
```

**Check:**
- [ ] No WIP/fixup commits
- [ ] Module boundaries respected
- [ ] Breaking changes separate + flagged
- [ ] Commit messages follow conventions

---

## Examples

### Good Commit Structure

```bash
# 3 separate commits (module boundaries + feature scope)
1. feat: Add DataAccessLayer to Core module

   Implements reactive data access with observer pattern.
   Adds indexes for foreign key constraints.

   Module: Core/DataLayer
   Breaking: No

2. feat: Add filtering UI in FeatureX

   Status + date range filters with reactive updates.
   Integrates with DataAccessLayer.

   Module: App/Features
   Breaking: No

3. test: Add integration tests for data filtering

   Covers all filter combinations + edge cases.

   Module: App/Features
```

### Bad Commit Structure

```bash
# Mixed modules + WIP commits (needs cleanup)
1. WIP
2. Add filtering
3. Fix Core changes
4. Update FeatureA + FeatureB  # Mixed features!
5. Fix tests
6. Debug logging
```

**Fix:** Squash WIP commits, separate Core vs App, separate FeatureA vs FeatureB.

---

## Integration Notes

**Related skills:**
- **clean-architecture** - Module boundaries (Core vs App)
- **signal-vs-noise** - What deserves commit message detail

**When to use this skill:**
- Pre-merge commit organization
- Writing commit messages
- Deciding when to squash commits
- PR preparation
- Creating pull requests with structured format

---

## Resources

**Philosophy and Patterns:**
- `@resources/signal-vs-noise-reference.md` - Signal vs Noise filter for commit messages (3-question test, what to include/exclude)
- `@resources/why-over-how-reference.md` - WHY over HOW philosophy (business context, technical rationale, bug context)
- `@resources/commit-message-examples.md` - Structure patterns (template vs natural prose, transformation examples)

**Use resources for:**
- Signal vs Noise → Apply 3-question filter to commit message content (Actionable? Impactful? Non-Obvious?)
- Why over How → Focus on business context and rationale, not implementation details
- Examples → See transformation from template to natural prose

**Why included:**
- Self-contained philosophy guide (consistent Signal vs Noise principles)
- Universal patterns applicable to any project
- Transformation examples (template → natural prose)

---

**Remember:** Module boundaries = highest priority for commit separation. Squash WIP/fixup commits always. Breaking changes = separate commit + flagged. Commit messages = natural prose with WHY focus (not template sections). NO footer by default (no Co-Authored-By, no Signed-off-by).
