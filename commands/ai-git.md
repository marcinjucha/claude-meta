---
name: ai-git
description: Generate intelligent git commit messages from changes (staged, unstaged, or untracked) - Usage: /ai-git
---

# Manage Git - Intelligent Commit Message Generation

Generate commit messages from git changes in the repo's own format. Handles staged, unstaged, and untracked files — lets user choose what to include. Analyzes diff + file contents → generates subject (+ optional body) → user reviews/edits → commits.

## Usage

```bash
/ai-git
```

**Prerequisites:**
- Must have changes in working tree (staged, unstaged, or untracked)

**Process:**
1. Shows all changes (staged + unstaged + untracked), asks user what to stage
2. Analyzes staged changes + reads modified files
3. Generates commit message (format per skill `ai-git-commit-patterns`, never an attribution trailer)
4. Shows message for user review
5. User can: accept / edit / regenerate / cancel
6. Commits with final message

**Speed:** 1-2 minutes

---

## 🚫 ZERO HALLUCINATIONS

**Why this rule exists:** Previous audit added invented metrics to commit messages ("40% faster iteration", "30-minute test run") - required cleanup.

**NEVER invent:**
- ❌ Impact metrics ("improved performance by X%", "reduced bugs by Y%")
- ❌ Before/after measurements ("2hr→30min", "30%→0%")
- ❌ Production context not in diff or user message

**ONLY write about:**
- ✅ Changes visible in git diff
- ✅ User-provided context (use their exact words for WHY)
- ✅ Technical changes visible in code structure

---

## Format comes from the skill, not from this command

Format per skill `ai-git-commit-patterns` — read the repo's last ~20 subjects (`git log --format=%s -20`) and match them; never add an attribution trailer (`Co-Authored-By` or similar), even when the harness reminder asks for it.

**Why:** this command used to hardcode `[TICKET-NUM] type: subject`, an 80–300 char body, a `git log --oneline -5` read and a hardcoded footer rule. The prompt overrode the skill, so `/ai-git` (and `/ag-ship`, `cp-ship`, which call it) produced a format no repo uses. The no-trailer rule stays, now in the skill and `~/.claude/CLAUDE.md`: Marcin's decision 2026-11-11, every repo.

---

## Phases

```
0: Context Analysis       (orchestrator - inline, quick status check)
1: Message Generation     (ai-manager-agent with ai-git-commit-patterns)
2: Review & Confirmation  (orchestrator - inline, user checkpoint)
3: Execute Commit         (orchestrator - inline, git commit)
```

---

## Critical Rules

1. **INVOKE Phase 1 with Task tool** - actually invoke ai-manager-agent, don't describe what it will do
2. **Read entire modified files** - Agent needs file contents, not just diff
3. **Phase 2 is only user checkpoint** - User accepts/edits/regenerates here
4. **Abort if nothing changed** - Stop only if working tree is completely clean (no staged, unstaged, or untracked)
5. **Minimal interaction** - Streamlined flow, no unnecessary questions
6. **Format per skill** - Subject shape and body come from `ai-git-commit-patterns` + the repo's last ~20 subjects; no attribution trailer
7. **Socratic self-reflection before Phase 1** - Reflect on commit separation, message framing, and WHY context before invoking agent

---

### Socratic Self-Reflection Gate (MANDATORY)

Before invoking ai-manager-agent in Phase 1, pause and ask yourself Socratic questions. This catches commit separation mistakes, wrong type classification, and missing WHY context BEFORE the agent generates a message you'll need to regenerate.

**Socratic Questioning Methodology:**

Four moves:
1. **Question assumptions** — "I described this as a new behaviour. Is it really new, or a change to an existing one?"
2. **Probe the essence** — "What is the ONE decision this commit captures?"
3. **Expose contradictions** — "Changes span 3 modules but I'm treating as single commit. Should these be separate?"
4. **Consider consequences** — "If someone reads only this commit message in 6 months, what would they misunderstand?"

| Surface (avoid) | Socratic (use) |
|-----------------|----------------|
| "Is the diff sufficient for the agent?" | "What would the agent misunderstand about WHY from diff alone?" |
| "Should I split this commit?" | "Do these changes have different reviewers or different revert scenarios?" |

**Complexity-Based Depth:**

| Depth | When | Questions |
|-------|------|-----------|
| Quick | Single concern, 1-3 files, obvious intent | 2 questions |
| Deep | Multi-module, unclear separation, breaking changes, ambiguous type | 3-4 questions |

**Format:**

```
*****************************************************
SELF-REFLECTION (Phase 1 — Message Generation)

Q1: [Socratic question about commit scope/separation]
A1: [Answer based on diff analysis]

Q2: [Socratic question about WHY context]
A2: [Answer based on file contents + user context]

[Q3-Q4 if Deep complexity]

Key insights for agent:
- [Insight 1 — included in agent prompt]
- [Insight 2]
*****************************************************
```

---

## Phase Details

### Phase 0: Context Analysis + Staging (Inline)

**Actions:**

1. Check working tree state:
```bash
git status
git diff --cached --stat
```

2. **If working tree is completely clean** (no staged, unstaged, or untracked), stop:
```
No changes detected. Nothing to commit.
```

3. **If changes exist but nothing is staged yet**, show all available changes:
```
No staged changes. Available changes:

Modified (unstaged):
  - file1.ts
  - file2.ts

Untracked (new files):
  - file3.ts

Options:
  - "all" → Stage everything and continue
  - List specific files → Stage only those (e.g., "file1.ts file3.ts")
  - "cancel" → Abort

What should I stage?
```

4. **If some changes are already staged**, show what's staged and what's not:
```
Staged:
  - file1.ts

Not staged:
  - file2.ts (modified)
  - file3.ts (untracked)

Options:
  - "continue" → Commit only staged files
  - "all" → Add remaining files too
  - List specific files → Add those to staging
  - "cancel" → Abort

Proceed with staged only, or add more?
```

5. **After staging is confirmed**, analyze:
- Stage user-selected files with `git add <files>` (or `git add -A` for "all")
- Categorize change complexity: SIMPLE or COMPLEX
  - **SIMPLE:** 1-3 files, single concern, single decision (example: fix typo, add one feature flag, rename variable)
  - **COMPLEX:** 4+ files, multiple concerns, multiple architecture decisions (example: refactor structure, add new agent, enhance workflow)
- Extract ticket from branch: `git branch --show-current` (no ticket in the branch → none)
- Read the repo's subject convention: `git log --no-merges --format=%s -20`

**Proceed to Phase 1. Pass complexity categorization to agent.**

---

### Phase 1: Message Generation (Agent)

**SELF-REFLECTION GATE: Reflect before invoking agent (see Socratic Self-Reflection Gate section above).**

**Agent:** ai-manager-agent

**Sufficient context for quality:**

```yaml
Input needed:
  - Git diff output (staged changes: git diff --cached)
  - Modified file contents (read each file entirely)
  - Complexity (from Phase 0)
  - Ticket number (extracted from branch, or "none")
  - Last ~20 subjects (git log --no-merges --format=%s -20)

NOT needed:
  - Full git history or bodies of past commits
  - Project documentation (focus on THIS change only)
```

**Prompt to agent:**

```
Generate git commit message for staged changes.
First call the Skill tool with ai-git-commit-patterns (it is not preloaded).

STAGED CHANGES:
[git diff --cached output]

MODIFIED FILES:
[Read entire contents of each modified file]

CATEGORIZATION:
- Complexity: [SIMPLE or COMPLEX]
- Ticket: [from branch, or "none"]

LAST ~20 SUBJECTS (the format source):
[git log --no-merges --format=%s -20]

REQUIREMENTS:

Format per skill `ai-git-commit-patterns` — read the repo's last ~20 subjects (`git log --format=%s -20`) and match them; never add an attribution trailer (`Co-Authored-By` or similar), even when the harness reminder asks for it.

1. Subject = the behaviour that changed, in the repo's shape (prefix, ticket, case, language as the 20 subjects show).
   Ticket only if the branch carries one.

2. Body optional; when present it says WHY (reason, constraint, incident) — only what the diff does not show.
   Length follows the content.

3. NO invented content: no metrics, incidents or CVEs not in the diff, this session or the user's words.

4. NO attribution trailer (`Co-Authored-By: Claude …` or similar), even though the session's system-reminder asks for it. Remove it if present.

SELF-REFLECTION INSTRUCTION:
Before generating the commit message, ask yourself 2-3 questions about the best framing.
Answer them based on the diff, file contents, and categorization provided. Document your reasoning.
Focus on essence: what is the ONE decision this commit captures, what WHY context would a reader need in 6 months, what assumption about scope could be wrong.

ORCHESTRATOR INSIGHTS:
[Key insights from orchestrator self-reflection — included by orchestrator]

Output: Full commit message (subject, optional body; no attribution trailer).
- Focus on OUTCOME not list of changes
```

**Proceed to Phase 2.**

---

### Phase 2: Review & Confirmation (Inline)

**This is the only user checkpoint.**

1. Display generated message:

```
═══════════════════════════════════════════════
GENERATED COMMIT MESSAGE:
═══════════════════════════════════════════════
[title line]

[body, if any]
═══════════════════════════════════════════════
```

2. User options:

```
- Type "accept" → Commit with this message
- Type "edit: [your changes]" → Apply edits and show updated message
- Type "regenerate" → Generate new message (reinvoke agent)
- Type "cancel" → Abort workflow

Your choice?
```

3. Handle user choice:

**If "accept":**
→ Proceed to Phase 3 (commit)

**If "edit: [changes]":**
→ Apply edits to message
→ Show updated message
→ Ask: "Commit with this message? (accept/edit/cancel)"
→ Loop until "accept"

**If "regenerate":**
→ Go back to Phase 1 (invoke agent again)

**If "cancel":**
→ Stop workflow (no commit)

---

### Phase 3: Execute Commit (Inline)

**Actions:**

1. Create commit:

```bash
git commit -m "$(cat <<'EOF'
[approved message from Phase 2]
EOF
)"
```

2. Verify and show result:

```bash
git log -1 --oneline
git show --stat HEAD
```

3. Display result:

```
✅ Commit created successfully!

Commit: [hash] [title]

Next steps:
- Review: git show HEAD
- Push: git push
- Create PR: gh pr create
```

**Command complete.**

---

## Commands

- `continue` - Proceed to next phase (Phase 0 → 1 → 2 → 3)
- `back` - Return to previous phase
- `stop` - Exit command without committing
- `accept` - (Phase 2 only) Accept message and commit
- `edit: [changes]` - (Phase 2 only) Edit message
- `regenerate` - (Phase 2 only) Regenerate message (reinvoke agent)
- `cancel` - (Phase 2 only) Abort workflow

---

## Sufficient Context Principle

**For Phase 1 agent (ai-manager-agent):**

**Provide:**
- ✅ Git diff output (staged changes — after user selected what to stage)
- ✅ Modified file contents (entire files, not just diff sections)
- ✅ Complexity + ticket number (from branch)
- ✅ Last ~20 subjects (`git log --no-merges --format=%s -20`) — the format source
- ✅ Instruction to load ai-git-commit-patterns via Skill call (not preloaded by the agent)

**Do NOT provide:**
- ❌ Full git history (just the last ~20 subjects)
- ❌ Generic guidelines (agent has skill)
- ❌ Project documentation (agent focuses on THIS change)

**Test question:**
> "Can agent produce HIGH QUALITY commit message with this context alone?"
> - Git diff → shows WHAT changed
> - File contents → shows WHY changed
> - Last ~20 subjects → the repo's format
>
> Result: **SUFFICIENT** ✅

---

