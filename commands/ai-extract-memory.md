---
description: "Extract learnings from current session and save to memory.md. Usage: /ai-extract-memory"
---

# Extract Memory

This command delegates ALL work to `ai-manager-agent`. The orchestrator's only job is to invoke the agent and report results.

## Orchestrator Instructions

### CRITICAL: DELEGATE TO AI-MANAGER-AGENT

**You are the orchestrator.** Your ONLY job:

1. **Invoke** `ai-manager-agent` using the Task tool with the prompt template below
2. **Report** the agent's summary to the user

**DO NOT:**
- ❌ Read memory.md yourself
- ❌ Analyze the conversation yourself
- ❌ Edit memory.md yourself
- ❌ Ask clarifying questions (this command is fully automatic)

**DO:**
- ✅ Immediately invoke Task tool with subagent_type="ai-manager-agent"
- ✅ Forward any $ARGUMENTS to the agent prompt
- ✅ Report the agent's output to the user verbatim

### Socratic Self-Reflection Gate

Before invoking ai-manager-agent, pause and reflect:

1. **Question assumptions** — "What happened in this session that was surprising or non-obvious?"
2. **Probe the essence** — "What's the ONE learning that would most help future sessions?"
3. **Consider consequences** — "If I extract the wrong pattern, what bad decisions would future sessions make?"

**Depth:** Always Quick (2-3 questions) — this is a single-pass extraction, not a multi-phase process.

Include key insights in the agent prompt (e.g., "Focus extraction on [specific area] because [reason]").

## Agent Prompt Template

Copy this prompt and send it to ai-manager-agent via Task tool:

~~~
You are a memory extraction agent. Your task: analyze the current conversation and save learnings to the project's `memory.md` file.

**This is fully automatic — no clarifying questions, no confirmations. Just do the work.**

**User arguments (if any):** $ARGUMENTS

SELF-REFLECTION INSTRUCTION:
Before extracting, ask yourself: what was genuinely surprising this session?
Focus on essence: what pattern would prevent a real mistake in future sessions.
Skip obvious learnings — only extract what's non-obvious and actionable.

## Steps

1. **Read** `memory.md` at the project root. If the file does not exist, **create it** with this default structure:
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
- Keep total file under 200 lines
- If unsure whether something is signal → INCLUDE it (duplicates handled by /ai-curate-memory)
- Convert relative dates to absolute dates (e.g., "yesterday" → use today's date minus 1)
- After editing, confirm what was added in a short summary
- **After editing, count lines in memory.md and report status:**
  - Below 150 lines → no warning
  - 150-179 lines → warn: "memory.md at {N}/200 lines — consider running /ai-curate-memory soon"
  - 180+ lines → alert: "memory.md at {N}/200 lines — run /ai-curate-memory to free space"
~~~
