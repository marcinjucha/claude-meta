---
description: "Curate memory — promote mature entries to most relevant CLAUDE.md files across project. Usage: /ai-curate-memory"
---

# Curate Memory

Review memory files and promote mature learnings to the most relevant `CLAUDE.md` across the project. Remove duplicates and outdated entries.

## Instructions

You are curating the project's memory files. Follow these steps exactly:

### Step 1: Discover and Read

1. Read `memory.md` from the project root directory. If it does not exist or is empty, tell the user and stop.
2. Discover ALL `CLAUDE.md` files across the project:
   - Use Glob: `**/CLAUDE.md`
   - **Exclude:** `.claude/` directory (EXCEPT `.claude/CLAUDE.md`) and `worktree-*` folders
   - `.claude/CLAUDE.md` is a valid discovery target — include it if it exists
3. Discover available skills:
   - Read `.claude/skills/CLAUDE.md` if it exists — this is the skills inventory
   - Note skill names and their scope/purpose for Step 5
4. Read each discovered `CLAUDE.md` to understand its scope/topic.
5. Build a scope map and display it to the user:

```
## Discovered CLAUDE.md files
- ./CLAUDE.md — [brief scope summary]
- ./.claude/CLAUDE.md — [brief scope summary] (if exists)
- ./uploads/CLAUDE.md — [brief scope summary]
- ./api/CLAUDE.md — [brief scope summary]
...

## Skills inventory
- [skill-name] — [brief scope from skills CLAUDE.md]
...
(or: No skills CLAUDE.md found)
```

### Step 2: Analyze and Target

For each entry in memory, classify it AND assign a target file:

**PROMOTE** if:
- Feedback/correction that has appeared multiple times across sessions
- Entry is clearly a universal project rule (not one-off context)
- Entry matches an existing section in any discovered CLAUDE.md

**Target selection** (for PROMOTE entries, in priority order):
1. **Content match** — entry topic matches scope of a specific CLAUDE.md (e.g., upload-related → `uploads/CLAUDE.md`)
2. **Path match** — entry references files/folders that have their own CLAUDE.md
3. **`.claude/CLAUDE.md`** — entry is about cross-project tooling/workflow preferences (conservative — only if clearly fits)
4. **Create new** — entry fits a folder that lacks CLAUDE.md but should have one (flag for creation)
5. **Fallback** — root `CLAUDE.md` if no specific match

**COMPRESS in memory** if:
- Completed feature section with implementation details now derivable from code (CSS values, RLS patterns, config, component props)
- Section longer than 5 lines where only 1-2 decisions are non-obvious
- Rule: keep only what code can't tell you — WHY decisions, production state, scoring formulas, deferred TODOs
- Target: completed feature sections → 2-4 lines (status + non-obvious decisions only)

**KEEP in memory** if:
- Entry appeared only once — not yet established as universal
- Entry is too specific to a single conversation or task
- No clear section in any CLAUDE.md where it belongs

**REMOVE from memory** if:
- Entry is already documented in any CLAUDE.md (duplicate)
- Entry is outdated or contradicted by newer entries or current code
- Entry is no longer relevant (bug was fixed, feature was removed)
- Entry is **code-derivable** — information readable from current source files (file structure, component props, CSS values, RLS policies, migration schemas). If `grep` or `Read` can answer it, memory doesn't need it.
- **Fixed bugs** where the fix is in the codebase and the pattern is generic (not project-specific). Keep only bugs with non-obvious project-specific patterns (e.g., Zod nullable vs optional, TanStack Query silent failure).

### Step 3: Present proposed changes

Show the user a clear summary:

```
## Proposed Changes

### Promote
- "[entry title]" → File: [path/CLAUDE.md] | Section: [target section]
  Reason: [why this is mature enough + why this file]

### New CLAUDE.md files to create
- [folder/CLAUDE.md] — for entries: "[entry A]", "[entry B]"
  Reason: [why this folder needs its own CLAUDE.md]

### Compress in memory
- "[section title]" — [current lines] → [target lines]. Remove: [what's code-derivable]. Keep: [what's non-obvious]

### Keep in memory
- "[entry title]" — [reason to keep]

### Remove from memory
- "[entry title]" — [reason: duplicate/outdated/code-derivable/fixed bug]
```

Then ask: **"Do you approve these changes? You can approve all, or specify which to skip."**

**WAIT for user confirmation before making any edits.**

### Step 4: Apply approved changes

After user confirms, execute in this order:

**Step 4a: Update/Create non-root CLAUDE.md files (PARALLEL)**

For each non-root CLAUDE.md that has promoted entries, invoke ai-manager-agent agent via Task tool **in parallel** (each agent modifies a different file — no conflicts):

```
Per-file Task prompt:
  MODE: [MODIFY existing / CREATE new] CLAUDE.md
  FILE: [path/CLAUDE.md]
  SCOPE: [brief scope description — what this CLAUDE.md covers, especially for CREATE mode]
  ENTRIES TO ADD:
    - "[entry]" | WHY: [rationale]
```

Agent loads `claude-md` skill — do NOT duplicate formatting/structure rules here.

**Step 4b: Update root CLAUDE.md (SEQUENTIAL — after 4a completes)**

Invoke ai-manager-agent agent via Task tool for root `CLAUDE.md` with TWO tasks combined:
1. Add promoted entries targeted at root (same format as 4a)
2. Add/update a `## Project CLAUDE.md Files` section at the end of root `CLAUDE.md`:

```
## Project CLAUDE.md Files

Index of all CLAUDE.md files in the project and their scope:
- `./uploads/CLAUDE.md` — [scope summary]
- `./api/CLAUDE.md` — [scope summary]
...
```

This gives AI awareness of the full CLAUDE.md structure.

**Step 4c: Cleanup memory (PARALLEL with 4b or after)**

Edit `memory.md` inline — remove promoted and removed entries. Keep the rest. Do not reorder kept entries.

### Step 5: Skill recommendations

Using the skills inventory from Step 1, analyze TWO sources for skill-relevant content:

**Source A: Memory entries** (promoted + kept)
For each entry, check if it contains a pattern, bug, or correction relevant to an existing skill.

**Source B: All discovered CLAUDE.md content** (including `.claude/CLAUDE.md`)
Scan for content that would be better served as a skill — patterns, workflows, or domain knowledge that is reusable across conversations and currently embedded in CLAUDE.md instead of being a loadable skill.

Print at the end:

```
## Skill recommendations

### Update existing skills
- [skill-name] — [what should be updated] (source: memory "[entry title]" / CLAUDE.md "[file path]")

### New skill candidates
- "[pattern/workflow description]" — found in [CLAUDE.md path], could become skill for [purpose]
```

If no skill recommendations → skip this section entirely.

**This step is recommendation-only.** No skill files are modified. User runs **`/ai-skill`** to act on recommendations.

### Step 6: Print summary

```
Done.
- Discovered: [N] CLAUDE.md files across project (incl. .claude/CLAUDE.md if present)
- Discovered skills: [N] (from .claude/skills/CLAUDE.md)
- Promoted: [N] entries total
  - [path/CLAUDE.md]: [n] entries
  - [path/CLAUDE.md]: [n] entries
  - ...
- Created: [N] new CLAUDE.md files
- Updated root index: Yes/No
- Compressed: [N] sections (completed features, code-derivable details)
- Removed: [N] entries (duplicates/outdated/code-derivable/fixed bugs)
- Kept: [N] entries in memory
- Skill recommendations: [N] (run /ai-skill to apply)
```

## Rules

- Default to aggressive cleanup — memory should hold only what code can't tell you
- For completed features: compress to 2-4 lines (status + non-obvious WHY decisions). Remove implementation details derivable from code.
- For fixed bugs: remove unless the pattern is non-obvious and project-specific (e.g., Zod nullable gotcha, TanStack silent failure)
- When in doubt about individual entries, KEEP — but when in doubt about verbose sections, COMPRESS
- NEVER modify skill files or command files inside `.claude/`. Exception: `.claude/CLAUDE.md` may be modified via ai-manager-agent agent (same as other CLAUDE.md files)
- Exclude `worktree-*` folders from discovery
- All CLAUDE.md modifications delegated to ai-manager-agent agent (via Task tool)
- May create new CLAUDE.md files in folders where none exist (if justified and approved)
- `memory.md` cleanup done inline (not delegated)
- Preserve existing formatting and section structure in all CLAUDE.md files
- Preserve WHY context when promoting (don't lose rationale)
- Do not reorder entries that are kept in memory — maintain original order
