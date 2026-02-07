---
name: git-commit-patterns
description: Organize commits and write messages for PRs. Use when deciding commit structure, squashing strategy, or writing messages. Applies Signal vs Noise (WHY > HOW, natural prose). Critical for clean git history and efficient reviews.
---

# Git Commit Patterns

**Purpose:** Commit organization and message writing for clean git history. Covers commit separation logic, squashing decisions, and commit message conventions with Signal vs Noise philosophy.

## ⚠️ CRITICAL: COMMIT MESSAGES MUST BE FACT-BASED

**ABSOLUTE RULE:**

- ❌ **NEVER invent production incidents** in commit message examples
- ❌ **Don't make up bug impact** or statistics in examples
- ❌ **Example commit messages should be generic** or based on real user scenarios

**For commit message examples:**

- ✅ Use generic placeholders: "Fixed bug", "Improved performance"
- ✅ Ask user for real scenario if specific example needed
- ✅ Don't invent specific numbers or incidents in examples

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

**See:** `@../resources/signal-vs-noise-reference.md` for complete filter and examples.

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

[Paragraph 1: Business context - why this change matters]

[Paragraph 2: Technical decision with rationale - why this approach]

[Paragraph 3: Additional context - bug fixes, edge cases, constraints]

[Paragraph 4 (optional): Cross-cutting concerns - platform alignment, migration notes]
```

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

**✅ Good (Natural prose, WHY-focused, with ticket):**
```
[SHELF-5678] feat: Implement OAuth Authentication Flow

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

**❌ Bad (Template with sections, NOISE, missing ticket):**
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
Missing ticket number from branch name.

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

### When to Use This Workflow

Organize commits before merge when:
- **Multiple WIP commits** need cleanup (squashing opportunity)
- **Mixed module changes** in history (separation needed per Factor 1)
- **Breaking changes** not flagged (visibility needed)
- **PR review blocked** by messy history ("can't review this")

### Why Organize Commits

**Impact on review efficiency:**

Disorganized history:
- Reviewer sees 15 commits: "WIP", "fix", "temp", "revert", "fix again"
- Review time: 2-3 hours (must understand 15 commits)
- Questions: "What's the actual change?"

Organized history:
- Reviewer sees 3 commits: "feat: Add FeatureX", "refactor: Extract module", "fix: Edge case"
- Review time: 30-45 minutes (clear separation)
- Each commit reviewable independently

**Production example:**

Team X before organizing:
- Average PR review time: 3 hours
- 40% of PRs required "can you clean up commits?" feedback

Team X after organizing:
- Average PR review time: 45 minutes (75% faster)
- Clean commit history became standard practice

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

## Examples

### Good vs Bad Commit Structure

**✅ Good:** 3 separate commits (module boundaries + feature scope)
- feat: Add DataAccessLayer to Core module
- feat: Add filtering UI in FeatureX
- test: Add integration tests for data filtering

**❌ Bad:** Mixed modules + WIP commits
- WIP, Add filtering, Fix Core changes, Update FeatureA + FeatureB, Fix tests, Debug logging

**Fix:** Squash WIP commits, separate Core vs App, separate FeatureA vs FeatureB.

---

## Integration Notes

**Related skills:** clean-architecture (module boundaries), signal-vs-noise (commit message detail)

**Use when:** Pre-merge organization, writing messages, squashing decisions, PR preparation

---

## Resources

**Shared resources** (`@../resources/`) - Common across meta-skills:
- `@../resources/signal-vs-noise-reference.md` - Signal vs Noise filter for commit messages (3-question test, what to include/exclude)
- `@../resources/why-over-how-reference.md` - WHY over HOW philosophy (business context, technical rationale, bug context)

**Skill-specific resources** (`@resources/`) - Unique to git-commit-patterns:
- `@resources/commit-message-examples.md` - Structure patterns (template vs natural prose, transformation examples)

**Use resources for:** Signal vs Noise (3-question filter), Why over How (business context), transformation examples (template → natural prose)

---

**Remember:** Module boundaries = highest priority for commit separation. Squash WIP/fixup commits always. Breaking changes = separate commit + flagged. Commit messages = natural prose with WHY focus (not template sections). NO footer by default (no Co-Authored-By, no Signed-off-by).
