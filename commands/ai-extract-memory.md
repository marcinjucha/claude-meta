---
description: "Extract learnings from current session and save to memory.md. Usage: /ai-extract-memory"
---

# Extract Memory

This command delegates ALL work to a **fork** of the current conversation. The orchestrator's only job is to invoke the fork and report results.

## Orchestrator Instructions

### CRITICAL: DELEGATE TO A FORK

**You are the orchestrator.** Your ONLY job:

1. **Invoke** a fork (`subagent_type: "fork"`) using the Task tool with the prompt template below
2. **Report** the fork's summary to the user

**WHY a fork, never a fresh agent:** the extraction's primary source is THIS conversation, so the executor must inherit it — a fresh agent starts blank and will either return an empty extraction or invent one from whatever summary it was handed in the prompt. Commit `2587a33` ("use agents for extract memory") introduced exactly that bug by moving the work from inline to a fresh `ai-manager-agent`; do not route this command back to a fresh agent.

**DO NOT:**
- ❌ Read memory.md yourself
- ❌ Analyze the conversation yourself
- ❌ Edit memory.md yourself
- ❌ Ask clarifying questions (this command is fully automatic) — sole exception: the vault context question in **Target Path** below

**DO:**
- ✅ Immediately invoke Task tool with subagent_type="fork"
- ✅ Resolve the target path (see **Target Path**) and pass it to the fork as `<target>`
- ✅ Forward any $ARGUMENTS to the fork prompt
- ✅ Report the fork's output to the user verbatim

### Target Path

- `$ARGUMENTS` contains a path to a `memory.md` → use it.
- cwd is inside the brain vault (`/Users/marcinjucha/Prywatne/projects/brain-vault`) → the root `memory.md` does NOT exist there by design (split per context 2026-08-08); target = `01-Projects/<ctx>/memory.md` of the context this session's work belonged to. Context unclear from the session → ask the user once which context. Never create a root `memory.md` in the vault.
- cwd is inside `/Users/marcinjucha/Prywatne/projects/claude-marketing` → its root `memory.md` is a FROZEN pre-split snapshot (2026-08-06), never write there. Target = the vault buffer of the session's context, resolved as `/brain-finish` resolves `<buffer>`: `/Users/marcinjucha/Prywatne/projects/brain-vault/01-Projects/shadow-operator/memory.md` by default; agency / Halo Efekt work (declared, or clear from the session) → `/Users/marcinjucha/Prywatne/projects/brain-vault/01-Projects/agency/memory.md`. File missing → created on first write.
- Otherwise → `memory.md` at the project root.

**WHY:** the project-root default points at a vault file that no longer exists (vault) or at a frozen twin nobody reads (claude-marketing), so a run there would recreate the deleted all-contexts buffer or keep feeding the snapshot instead of writing to the one the context reads.

### Socratic Self-Reflection Gate

Before invoking the fork, pause and reflect:

1. **Question assumptions** — "What happened in this session that was surprising or non-obvious?"
2. **Probe the essence** — "What's the ONE learning that would most help future sessions?"
3. **Consider consequences** — "If I extract the wrong pattern, what bad decisions would future sessions make?"

**Depth:** Always Quick (2-3 questions) — this is a single-pass extraction, not a multi-phase process.

Include key insights in the agent prompt (e.g., "Focus extraction on [specific area] because [reason]").

## Agent Prompt Template

Copy this prompt and send it to the fork via Task tool:

~~~
You are a memory extraction agent. Your task: analyze the current conversation and save learnings to the project's `memory.md` file.

**This is fully automatic — no clarifying questions, no confirmations. Just do the work.**

**User arguments (if any):** $ARGUMENTS
**Target file:** <target>

SELF-REFLECTION INSTRUCTION:
Before extracting, ask yourself: what was genuinely surprising this session?
Focus on essence: what pattern would prevent a real mistake in future sessions.
Skip obvious learnings — only extract what's non-obvious and actionable.

## Steps

1. **Read** the target file (`<target>` above — never substitute the project root). If the file does not exist, **create it** with this default structure:
   ```markdown
   # Memory

   ## Feedback & Corrections

   ## Domain Concepts

   ## Bugs Found

   ## Architecture Decisions

   ## Preferences
   ```
2. **Analyze** the conversation for signals (see below).
3. **Edit** `memory.md` — append new entries under the matching section. If no matching section exists, create one.

## Signals to Extract

Only save if ANY of these match:

| Signal | Section |
|--------|---------|
| User said "no", "not like that", "instead", "don't", "stop" | **Feedback & Corrections** |
| User corrected or rejected AI output | **Feedback & Corrections** |
| User explained WHY something works a specific way | **Domain Concepts** |
| A bug was found or fixed | **Bugs Found** |
| A decision about WHERE code goes or WHY a pattern | **Architecture Decisions** |
| User accepted a non-obvious approach | **Preferences** |
| AI discovered something unexpected about codebase | **Bugs Found** or **Domain Concepts** |

## Entry Format

Append under the matching section:

```
- **Title** — one-line explanation with WHY context
```

## Rules

- Do NOT add framework basics or standard patterns derivable from code
- Do NOT duplicate entries already in memory.md
- If session had zero signal (only commands, no discussion) → write nothing, tell user "No signal found in this session"
- Keep the file within its size budget (see the size check below — characters for vault buffers, lines elsewhere)
- If unsure whether something is signal → INCLUDE it (duplicates handled by /ai-curate-memory)
- Convert relative dates to absolute dates (e.g., "yesterday" → use today's date minus 1)
- After editing, confirm what was added in a short summary
- **After editing, measure memory.md and report status — the unit depends on where the file lives:**
  - **Vault buffer** (`/Users/marcinjucha/Prywatne/projects/brain-vault/01-Projects/<ctx>/memory.md`) → measure in CHARACTERS, never lines: run `python3 /Users/marcinjucha/Prywatne/projects/brain-vault/.brain/scripts/brain-budget.py --context <ctx>` (`<ctx>` = the folder name under `01-Projects/`) and read the `buffer` row; the budget is `budgets.buffer` in `/Users/marcinjucha/Prywatne/projects/brain-vault/.brain/config.json`. Output listing 0 files = wrong context name, not "within budget" — fix the name and rerun.
    - Below 75% of `budgets.buffer` → no warning
    - 75–99% → warn: "memory.md at {N}/{budget} chars — consider running /ai-curate-memory soon"
    - At or over budget (the row carries `⚠`) → alert: "memory.md at {N}/{budget} chars — run /ai-curate-memory to free space"
  - **Any other repo's `memory.md`** → count lines: below 150 → no warning; 150-179 → warn "memory.md at {N}/200 lines — consider running /ai-curate-memory soon"; 180+ → alert "memory.md at {N}/200 lines — run /ai-curate-memory to free space".
  - **WHY two units:** vault buffers are budgeted in characters (`/brain-finish` Faza 0(b) and `brain-budget.py` use the same number); entries there are long single lines, so a line count reported "no warning" for a buffer almost 3x over budget.
~~~
