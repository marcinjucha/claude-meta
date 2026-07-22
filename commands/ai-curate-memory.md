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
1. **Brain knowledge note** (ONLY gdy cwd mapuje się do kontekstu brain z aktywnym obszarem knowledge — per claude-brain `config.json`) — jeśli wpis to **work-derived cross-cutting SYNTEZA** (obejmuje ≥2 atomy repo, żadna pojedyncza lokalizacja repo jej nie niesie — wiedza „dlaczego projekt/domena są jakie są"), promuj go do **notatki wiedzy mózgu** w `03-Resources/<ctx>/knowledge/` przez **`/brain-extract-knowledge`** (silnik dla syntezy wywiedzionej z PRACY), albo rozszerzając istniejącą notatkę wg reguły anty-dryf dedup. Migracja wiedzy ze SKILLA to osobne narzędzie — zostaje `/brain-knowledge-migrate` (tryb REFLECT: skill nietknięty, wiedza jako ATOMOWE noty `status: reflection` — nie stary thick-`mirror`). **Jak rozróżnić (atom-vs-synteza):** POJEDYNCZY zakotwiczony ATOM (jeden próg / jeden bug / jedna reguła-pliku, który czyta człowiek) → zostaje w repo/`CLAUDE.md`; cross-atom SYNTEZA (łączy ≥2 wcześniej osobne atomy) → notatka mózgu. Notatki mózgu tu bywają **brain-only** (nie muszą być konsumowane przez skill — Scandit trzyma syntezę brain-only). NIGDY nie wkładaj wiedzy z powrotem do ciała ścienionego skilla. Schemat notatki + brzytwa: `_system/knowledge-system.md`. **W repo BEZ kontekstu brain — pomiń tę opcję, promuj jak dotąd (CLAUDE.md).**
2. **Existing skill** — if the entry is **cross-cutting, reusable HOW / pattern / domain knowledge consumed by an agent at runtime** (TCA/SwiftUI patterns, ARKit/positioning domain, testing patterns, design-system rules), promote it INTO the relevant EXISTING skill (`.claude/skills/<name>/SKILL.md`), NOT CLAUDE.md. **How to distinguish from CLAUDE.md:** CLAUDE.md is for project rules a *human* reads; a skill is for knowledge an *agent* loads on demand. **This target applies ONLY to skills that already exist** — a genuinely NEW skill that doesn't exist yet stays a recommendation (Step 5), never a direct promotion here. Applied in Step 4d.
3. **Content match** — entry topic matches scope of a specific CLAUDE.md (e.g., upload-related → `uploads/CLAUDE.md`)
4. **Path match** — entry references files/folders that have their own CLAUDE.md
5. **`.claude/CLAUDE.md`** — entry is about cross-project tooling/workflow preferences (conservative — only if clearly fits)
6. **Create new** — entry fits a folder that lacks CLAUDE.md but should have one (flag for creation)
7. **Fallback** — root `CLAUDE.md` if no specific match

**COMPRESS in memory** if:
- Completed feature section with implementation details now derivable from code (CSS values, RLS patterns, config, component props)
- Done task status sections (AAA-T-X DONE, AAA-P-X DONE) → **REMOVE entirely** if no active decisions pending. Do not compress to 2-4 lines — remove. Only keep 'In Progress' or 'Pending' status sections.
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
- **Fixed bugs** where: (a) fix is in the codebase AND (b) pattern is either generic OR documented in skills. The bar for keeping bugs is HIGH: only keep if the bug is project-specific, non-obvious, AND recurs across sessions. When in doubt: REMOVE.
- Entry's pattern is **documented in existing skills** (ag-n8n-step-handlers, ag-workflow-engine, tanstack-setup, tanstack-routing, tanstack-server, etc.) — skills are loaded when needed; memory is not the right place.
- Entry describes **Done task implementation details** — status sections for completed work ("AAA-T-X DONE — full implementation detail") should be removed entirely, not compressed. Keep only active/in-progress work.

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

**Aggressive mode:** Default posture is removal. Every entry must justify its presence. Ask: 'Would losing this entry cause a real mistake in the next session?' If no — REMOVE.

Then ask: **"Do you approve these changes? You can approve all, or specify which to skip."**

**WAIT for user confirmation before making any edits.**

### Step 4: Apply approved changes

After user confirms, execute in this order:

**Step 4a: Update/Create non-root CLAUDE.md files (PARALLEL)**

**SELF-REFLECTION GATE: Reflect before invoking agents (see Socratic Self-Reflection Gate section below).**

**⚠️ CRITICAL: NEVER EDIT CLAUDE.md FILES DIRECTLY**
You MUST use the Agent tool with `subagent_type="ai-manager-agent"` for ALL CLAUDE.md modifications.
Using the Edit tool directly on any CLAUDE.md file is FORBIDDEN — even for "simple" additions.
The ai-manager-agent loads the `claude-md` skill which ensures correct formatting, signal vs noise filtering, and structural compliance.

For each non-root CLAUDE.md that has promoted entries, invoke ai-manager-agent agent via Task tool **in parallel** (each agent modifies a different file — no conflicts):

```
Per-file Task prompt:
  MODE: [MODIFY existing / CREATE new] CLAUDE.md
  FILE: [path/CLAUDE.md]
  SCOPE: [brief scope description — what this CLAUDE.md covers, especially for CREATE mode]
  ENTRIES TO ADD:
    - "[entry]" | WHY: [rationale]

  SELF-REFLECTION INSTRUCTION:
  Before modifying the file, ask yourself 2 questions about placement.
  Answer them based on the file's existing structure and scope. Document your reasoning.
  Focus on: does this entry fit the target section, and is WHY context preserved from memory.

  ORCHESTRATOR INSIGHTS:
  [Key insights from orchestrator self-reflection — included by orchestrator]
```

Agent loads `claude-md` skill — do NOT duplicate formatting/structure rules here.

**Step 4b: Update root CLAUDE.md (SEQUENTIAL — after 4a completes)**

**SELF-REFLECTION GATE: Reflect before invoking agent — Deep depth for root CLAUDE.md (see Socratic Self-Reflection Gate section below).**

**⚠️ CRITICAL: NEVER EDIT CLAUDE.md FILES DIRECTLY**
You MUST use the Agent tool with `subagent_type="ai-manager-agent"` for ALL CLAUDE.md modifications.
Using the Edit tool directly on any CLAUDE.md file is FORBIDDEN — even for "simple" additions.
The ai-manager-agent loads the `claude-md` skill which ensures correct formatting, signal vs noise filtering, and structural compliance.

Invoke ai-manager-agent agent via Task tool for root `CLAUDE.md` with TWO tasks combined:
1. Add promoted entries targeted at root (same format as 4a)
2. Add/update a `## Project CLAUDE.md Files` section at the end of root `CLAUDE.md`

Include in the agent prompt:
```
SELF-REFLECTION INSTRUCTION:
Before modifying root CLAUDE.md, ask yourself 3 questions about placement and scope accuracy.
Answer them based on the file's existing structure, the scope map, and the entries being promoted.
Focus on: is the Project CLAUDE.md Files index accurate after changes, does each entry land in the right section, and is WHY context preserved.

ORCHESTRATOR INSIGHTS:
[Key insights from orchestrator self-reflection — included by orchestrator]
```

```
## Project CLAUDE.md Files

Index of all CLAUDE.md files in the project and their scope:
- `./uploads/CLAUDE.md` — [scope summary]
- `./api/CLAUDE.md` — [scope summary]
...
```

This gives AI awareness of the full CLAUDE.md structure.

**Step 4b-brain: Promote target #1 entries to brain knowledge (BEFORE any memory removal) — data-loss guard**

For each entry whose target is **#1** (brain knowledge note — cross-atom synthesis), hand it to the **`/brain-extract-knowledge`** engine — its two-stage razor + verify-confirm + write pass OWNS the brain write. A target-#1 entry becomes eligible for removal from `memory.md` (Step 4c) **ONLY after its brain write is CONFIRMED**:
- Brain write performed and confirmed this run (in-flow `/brain-extract-knowledge`, or user confirms the note was written) → entry is eligible for Step 4c removal.
- Brain write NOT performed/confirmed this run → **KEEP the entry in `memory.md`** (do NOT remove) and report it as **"pending brain extraction — run /brain-extract-knowledge"**.

**NEVER remove a target-#1 entry from memory on the mere basis of being "promoted" when no brain write occurred** — the synthesis exists only in memory until the brain note exists. (This is the ONE promotion path allowed to later remove from memory, and only against a confirmed brain write; skills/CLAUDE.md promotions in 4a/4b/4d are copies, so their entries remove normally.)

Every entry left in this "pending brain extraction" state is surfaced to the user as a dedicated line in the final Step 6 summary (title list + `run /brain-extract-knowledge` reminder) — so this classification logic ends in a visible end-of-run reminder, not just a silent memory decision.

**Step 4c: Cleanup memory (after 4b-brain; PARALLEL with 4b or after)**

Edit `memory.md` inline — remove promoted and removed entries, **EXCEPT** any target-#1 (brain) entry whose brain write was NOT confirmed in Step 4b-brain — keep those (reported as "pending brain extraction"). Keep the rest. Do not reorder kept entries.

**Step 4d: Apply approved skill promotions (PARALLEL — different skill files, no conflicts)**

**SELF-REFLECTION GATE: Reflect before invoking agents — Quick depth, entries already approved (see Socratic Self-Reflection Gate section below).**

**⚠️ CRITICAL: NEVER EDIT SKILL FILES DIRECTLY**
You MUST use the Agent tool with `subagent_type="ai-manager-agent"` for ALL skill (`.claude/skills/**/SKILL.md`) modifications.
Using the Edit tool directly on any SKILL.md file is FORBIDDEN — even for "simple" additions.
The ai-manager-agent loads the `skill-fine-tuning` skill which ensures the entry integrates into the skill's existing structure, stays signal-focused, and reconciles contradictions.

For each EXISTING skill with approved entries (target #2 from Step 2), invoke ai-manager-agent via Task tool **in parallel** (each agent modifies a different skill file — no conflicts):

```
Per-skill Task prompt:
  MODE: MODIFY existing skill
  FILE: .claude/skills/[name]/SKILL.md
  ENTRIES TO ADD:
    - "[full entry text]" | WHY: [rationale]

  INSTRUCTIONS:
  - Integrate into the skill's EXISTING structure (right section) — do NOT blind-append.
  - Stay concise per signal-vs-noise — only project-specific signal with WHY.
  - RECONCILE any contradicting/outdated existing entry (update or replace it) rather than keeping both.

  SELF-REFLECTION INSTRUCTION:
  Before modifying the file, ask yourself 2 questions about placement and reconciliation.
  Answer them based on the skill's existing structure. Focus on: which section this belongs in,
  and whether any existing entry contradicts and must be reconciled (not duplicated).

  ORCHESTRATOR INSIGHTS:
  [Key insights from orchestrator self-reflection — included by orchestrator]
```

Agent loads `skill-fine-tuning` skill — do NOT duplicate skill structure rules here.

**Step 4e: Refresh brain reflection (brain context only)**

IF the cwd maps to a brain context with an active knowledge-system (per claude-brain `config.json`) AND a skill just updated in Step 4d has brain knowledge **reflection** notes (`status: reflection`) in `03-Resources/<ctx>/knowledge/`, refresh those notes by running `/brain-knowledge-migrate <skill> --reflect`.

**Discriminate note forms — refresh ONLY `reflection`:**
- `status: reflection` — atomic reflections of a team skill (skill = source of truth) → **refresh** (skill→brain re-extraction). This is the target of this step.
- `status: pointer` — link-only stub (title + gist + link, ZERO knowledge in the body; e.g. Scandit `ios-*` domain notes). A pointer carries no knowledge → refreshing it with knowledge is a **no-op / wrong** — **skip**. (A pointer only needs its link/gist kept accurate, which is not this step's job.)
- `status: mirror` — LEGACY thick single-file copy (transitional form being superseded by `reflection`). Treat exactly like `reflection` — refresh unconditionally via `--reflect` (skill→brain re-extraction). Same handling as `brain-update.md` maintenance step; no operator-judged condition.

**Where the forms live today:** the 6 meta skills (`skill-creator`, `agent-creator`, `signal-vs-noise`, `claude-md`, `skill-fine-tuning`, `command-creation`) now have ATOMIC `status: reflection` notes (8 atoms, the old thick copies removed) in the `claude-dev` context (`03-Resources/claude-dev/knowledge/`). The 7 Scandit `ios-*` domain notes are `status: pointer` (link-only) in `03-Resources/scandit/knowledge/` → NOT refreshed here.

**CRITICAL nuance:** For a TEAM skill, the SKILL is the source of truth and the brain notes only REFLECT it. Do NOT create a competing brain-owned canon note for the same knowledge, and — if the skill is a pointer-style (thinned) skill — do NOT write domain knowledge back into the skill body.

If there is no brain context, or no `reflection` note exists for the updated skill → skip this step entirely. (Distinct from Step 2 target #1: brain canon note = brain-owned evergreen knowledge; here we only refresh a reflection OF a team skill.)

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

**Scope of this step (recommendation-only):**
- (a) genuinely NEW skill candidates that do not exist yet, and
- (b) EXISTING skills where the user DECLINED the direct promotion in Step 4d.

Direct promotions INTO existing skills are handled in Step 4d (executed, not deferred) — do NOT list those here. User runs **`/ai-skill`** to act on these recommendations.

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
- Promoted to skills: [N] entries
  - [.claude/skills/name/SKILL.md]: [n] entries
  - ...
- Brain reflections refreshed: [N] (or: none — no brain context / no reflection)
- Updated root index: Yes/No
- Compressed: [N] sections (completed features, code-derivable details)
- Removed: [N] entries (duplicates/outdated/code-derivable/fixed bugs)
- Kept: [N] entries in memory
- Pending brain extraction: [N] entries — [list of entry titles] — run /brain-extract-knowledge
- Skill recommendations: [N] (new skill candidates + declined promotions — run /ai-skill to apply)
```

If no entries are pending brain extraction (N=0) → omit the `Pending brain extraction` line entirely (do not print "none"), same convention as the Skill recommendations section.

## Rules

- **Target: memory.md under 100 lines** — Aggressive cleanup means reaching this target, not just removing obvious noise.
- **NEVER edit CLAUDE.md files with the Edit tool** — ALL CLAUDE.md modifications MUST go through ai-manager-agent via the Agent tool (`subagent_type="ai-manager-agent"`). This is a BLOCKING requirement. The orchestrator must NOT use Read+Edit to modify CLAUDE.md files, even for single-line additions. ai-manager-agent loads the `claude-md` skill for correct formatting and signal filtering.
- **NEVER edit skill files (`.claude/skills/**/SKILL.md`) with the Edit tool** — ALL skill modifications (Step 4d) MUST go through ai-manager-agent via the Agent tool (`subagent_type="ai-manager-agent"`), which loads `skill-fine-tuning`. This is a BLOCKING requirement — the orchestrator must NOT use Read+Edit on any SKILL.md, even for single-line additions.
- **Socratic self-reflection before agent invocations** — Reflect before every ai-manager-agent invocation in Steps 4a, 4b, and 4d (see Socratic Self-Reflection Gate below)
- Default to aggressive cleanup — memory should hold only what code can't tell you
- For completed features: compress to 2-4 lines (status + non-obvious WHY decisions). Remove implementation details derivable from code.
- For fixed bugs: remove unless the pattern is non-obvious and project-specific (e.g., Zod nullable gotcha, TanStack silent failure)
- When in doubt about individual entries — LEAN TOWARD REMOVAL if it's not critical production state (tenant IDs, active bugs, ongoing tasks). Only keep what code + skills + CLAUDE.md can NOT tell you. Memory is for context that disappears between sessions, not documentation.
- NEVER modify skill files or command files inside `.claude/`. Exception: `.claude/CLAUDE.md` may be modified via ai-manager-agent agent (same as other CLAUDE.md files)
- Exclude `worktree-*` folders from discovery
- All CLAUDE.md modifications delegated to ai-manager-agent agent (via Task tool)
- May create new CLAUDE.md files in folders where none exist (if justified and approved)
- `memory.md` cleanup done inline (not delegated)
- Preserve existing formatting and section structure in all CLAUDE.md files
- Preserve WHY context when promoting (don't lose rationale)
- Do not reorder entries that are kept in memory — maintain original order

## Socratic Self-Reflection Gate (MANDATORY)

Before invoking ai-manager-agent in Steps 4a, 4b, and 4d, pause and ask yourself Socratic questions. This catches wrong target file selection, missing WHY context in promoted entries, unreconciled contradictions, and scope mismatches BEFORE the agent modifies CLAUDE.md or SKILL.md files.

**Socratic Questioning Methodology:**

Four moves:
1. **Question assumptions** — "I targeted this entry at apps/cms/CLAUDE.md. Does it truly belong there, or is it a cross-cutting concern?"
2. **Probe the essence** — "What is the ONE thing this promoted entry must communicate to prevent future mistakes?"
3. **Expose contradictions** — "This entry is about a bug pattern, but I'm adding it to architecture section. Is it really architecture or anti-pattern?"
4. **Consider consequences** — "If the agent adds this to the wrong section, will it be found when needed?"

| Surface (avoid) | Socratic (use) |
|-----------------|----------------|
| "Is the target file correct?" | "What would someone searching for this pattern look for, and would they find it in this file?" |
| "Should I include WHY context?" | "What WHY context would be lost if I only pass the entry text without rationale?" |

**Complexity-Based Depth:**

| Depth | When | Questions |
|-------|------|-----------|
| Quick | Step 4a — applying approved changes to non-root CLAUDE.md (mechanical from approved plan) | 2 questions per batch |
| Quick | Step 4d — applying approved skill promotions (entries already approved; reconciliation is the risk) | 2 questions per skill |
| Deep | Step 4b — root CLAUDE.md update + index (cross-cutting decisions, scope summary accuracy) | 3-4 questions |

**Default depth by step:**

| Step | Agent | Default Depth |
|------|-------|---------------|
| Step 4a (non-root CLAUDE.md) | ai-manager-agent | Quick — entries already approved, target already decided |
| Step 4b (root CLAUDE.md) | ai-manager-agent | Deep — root is high-traffic, wrong placement has wider impact |
| Step 4d (existing skills) | ai-manager-agent | Quick — entries already approved; reflect on section fit + contradiction reconciliation |

**Format:**

```
*****************************************************
SELF-REFLECTION (Step 4a/4b/4d — CLAUDE.md / SKILL.md Modification)

Q1: [Socratic question about target accuracy / section fit]
A1: [Answer based on scope map + entry content]

Q2: [Socratic question about WHY context preservation]
A2: [Answer]

[Q3-Q4 if Deep — Step 4b]

Key insights for agent:
- [Insight 1 — included in agent prompt]
- [Insight 2]
*****************************************************
```
