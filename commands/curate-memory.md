---
description: "Curate memory — promote mature entries to most relevant CLAUDE.md files across project. Usage: /curate-memory"
---

# Curate Memory

Review memory files and promote mature learnings to the most relevant `CLAUDE.md` across the project. Remove duplicates and outdated entries.

## Instructions

You are curating the project's memory files. Follow these steps exactly:

### Step 1: Discover and Read

1. Read `memory.md` from the project root directory. If it does not exist or is empty, tell the user and stop.
2. Discover ALL `CLAUDE.md` files across the project:
   - Use Glob: `**/CLAUDE.md`
   - **Exclude:** `.claude/` directory and `worktree-*` folders
3. Read each discovered `CLAUDE.md` to understand its scope/topic.
4. Build a scope map and display it to the user:

```
## Discovered CLAUDE.md files
- ./CLAUDE.md — [brief scope summary]
- ./uploads/CLAUDE.md — [brief scope summary]
- ./api/CLAUDE.md — [brief scope summary]
...
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
3. **Create new** — entry fits a folder that lacks CLAUDE.md but should have one (flag for creation)
4. **Fallback** — root `CLAUDE.md` if no specific match

**KEEP in memory** if:
- Entry appeared only once — not yet established as universal
- Entry is too specific to a single conversation or task
- No clear section in any CLAUDE.md where it belongs

**REMOVE from memory** if:
- Entry is already documented in any CLAUDE.md (duplicate)
- Entry is outdated or contradicted by newer entries or current code
- Entry is no longer relevant (bug was fixed, feature was removed)

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

### Keep in memory
- "[entry title]" — [reason to keep]

### Remove from memory
- "[entry title]" — [reason: duplicate/outdated/irrelevant]
```

Then ask: **"Do you approve these changes? You can approve all, or specify which to skip."**

**WAIT for user confirmation before making any edits.**

### Step 4: Apply approved changes

After user confirms, execute in this order:

**Step 4a: Update/Create non-root CLAUDE.md files (PARALLEL)**

For each non-root CLAUDE.md that has promoted entries, invoke claude-manager agent via Task tool **in parallel** (each agent modifies a different file — no conflicts):

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

Invoke claude-manager agent via Task tool for root `CLAUDE.md` with TWO tasks combined:
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

### Step 5: Skill update recommendations

If `@.claude/skills/CLAUDE.md` exists, read it to see available skills.

For each entry being promoted or kept, check if it contains a pattern, bug, or correction relevant to an existing skill. If so, add to recommendations list.

Print at the end:

```
## Skills to review
- [skill-name] — [what memory entry suggests updating] (memory: "[entry title]")
```

If no skill recommendations → skip this section entirely.

**Do NOT modify skills automatically.** Only recommend. User runs `/manage-skill` to apply.

### Step 6: Print summary

```
Done.
- Discovered: [N] CLAUDE.md files across project
- Promoted: [N] entries total
  - [path/CLAUDE.md]: [n] entries
  - [path/CLAUDE.md]: [n] entries
  - ...
- Created: [N] new CLAUDE.md files
- Updated root index: Yes/No
- Removed: [N] entries (duplicates/outdated)
- Kept: [N] entries in memory
```

## Rules

- Be conservative — when in doubt, KEEP in memory
- NEVER modify files inside `.claude/` directory
- Exclude `worktree-*` folders from discovery
- All CLAUDE.md modifications delegated to claude-manager agent (via Task tool)
- May create new CLAUDE.md files in folders where none exist (if justified and approved)
- `memory.md` cleanup done inline (not delegated)
- Preserve existing formatting and section structure in all CLAUDE.md files
- Preserve WHY context when promoting (don't lose rationale)
- Do not reorder entries that are kept in memory — maintain original order
