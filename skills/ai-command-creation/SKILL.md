---
name: ai-command-creation
description: Create or refactor multi-phase commands (multi-agent orchestration). Provides structure pattern, sufficient context principle (agents have isolated context), the ask-once rule (one question message, only about assumptions, one consent point before writes), and section templates. Critical for agents receiving exactly the right information.
argument-hint: "[command-name]"
---

# Command Creation - Multi-Phase Command Pattern

## Purpose

Guide for creating multi-phase command files that orchestrate multiple agents across phases. Focus on **command structure pattern**, **sufficient context principle** (agents have isolated context), and **the ask-once rule** (one question message, only about assumptions; one consent point before writes). Documents anti-patterns in command CREATION process (not for inclusion in command files).

**Note:** Fact-based and signal-only rules enforced by ai-manager-agent system prompt. Agent context must contain only project-specific decisions, constraints, and patterns — not generic explanations.

## When to Use

- Creating new multi-phase command (multi-agent orchestration)
- Refactoring existing command (structure inconsistent)
- Understanding command file conventions
- Deciding what context to pass to agents
- Fixing commands where agents produce low-quality output

---

## Command File Structure Pattern

**Standard multi-phase command file structure** (our convention):

```markdown
---
description: "[one-line description] - Usage: /command-name [args]"
---

# Title - Purpose

Brief explanation (1-2 sentences).

## Usage
[bash command, arguments, examples]

## Phases
[Phase overview with inline/agent markers; mark the PLAN phase → user approval]

## Orchestrator Instructions

### ⚠️ CRITICAL: YOU MUST INVOKE AGENTS
[Force actual Task tool invocation]

### Critical Rules
[3-5 rules, numbered, includes the ask-once rule]

## Phase Details

### Phase N: Name
**Agent**: agent-name

**Sufficient context for quality**: [CRITICAL SECTION]
```yaml
Input needed:
  - [decisions from previous phases]
NOT needed:
  - [generic knowledge, noise]
```

**Prompt to agent**: [template with placeholders]

**After agent**: [what to show; on the plan phase: the consent point]

## Sufficient Context Principle
[Test question, signal/noise examples]
```

**Why this structure:**
- **Phases overview** - orchestrator sees full command before starting, and where the one consent point sits
- **Orchestrator Instructions** - forces actual Task invocation (anti-pattern: just describing)
- **Ask-once rule** - questions only where the orchestrator would otherwise assume (Section 4)
- **Phase Details** - includes "Sufficient context for quality" section (CRITICAL)
- **Sufficient Context Principle** - always at end (test question for context filtering)

---

## Section Templates

### 1. Description (Frontmatter)

```yaml
---
description: "[Tool name] - [One-line purpose] - Usage: /command [args]"
---
```

**Pattern:**
- Start with tool name
- One-line purpose (not essay)
- Include usage with command syntax
- Max 200 chars

### 2. Phases Overview

```markdown
## Phases

```
0: Context Analysis      (orchestrator - inline assessment)
1: Requirements          (agent-name)
2: Plan                  (agent-name with skill-name skill) → user approval
3: Implementation        (agent-name)
```

**Speed**: X-Y min
```

**Pattern:**
- Phase 0 always inline (orchestrator assessment)
- Mark which agent for each phase, and which phase produces the plan
- Phases are a checklist, not stops: the orchestrator merges them into as few spawns as context allows
- Mention key skills if relevant
- Estimated duration

**WHY Phase 0 inline:** Orchestrator does quick categorization before launching agents. Avoids wasting agent invocation on trivial assessment (complexity check, file categorization).

### 3. Orchestrator Instructions

**CRITICAL SECTION** - Forces actual agent invocation:

```markdown
## Orchestrator Instructions

### ⚠️ CRITICAL: YOU MUST INVOKE AGENTS

**You are the orchestrator.** Your job is to **ACTUALLY INVOKE AGENTS using the Task tool**.

**DO NOT**:
- ❌ Say "I will launch agent-name"
- ❌ Describe what the agent will do
- ❌ Explain the phase without invoking

**DO**:
- ✅ Immediately invoke Task tool with agent
- ✅ Use subagent_type, description, prompt parameters
- ✅ Wait for agent completion
- ✅ Show results to user

**Example**:
```
Phase 1/5: Requirements
Launching requirements-analyst...
```
[IMMEDIATELY invoke Task tool NOW with subagent_type="agent-name"]

### Critical Rules

1. **INVOKE with Task tool** - Every agent phase requires actual Task tool call
2. **Sufficient context** - Each agent gets ONLY what it needs for quality
3. **Ask once, only about assumptions; one consent point** - [the rule from Section 4, verbatim]
4. **Track mode** - Remember what is already done
```

**WHY this section:**
- **Anti-pattern prevention**: Orchestrator describing instead of invoking
- **Force behavior**: Explicit DO/DON'T forces actual Task tool use

### 4. Questions and Consent (the ask-once rule)

Put this rule verbatim in every generated command's Critical Rules:

> **Ask once, only about assumptions; one consent point** - Ask the user in ONE message, and only when you are assuming something about scope, location (claude-dev / brain-vault/.claude / ~/.claude / the source of a symlink) or what the change applies to; otherwise merge phases and act. The only gate: present the plan → user approves (an approval already given in the request counts) → the writing agent writes. **Why:** the old per-phase questions/paraphrase/gate ceremony ran in zero observed sessions, and Marcin's rule is "decide yourself, ask only about assumptions".

**What this means for the generated command:**
- No per-phase question blocks, paraphrase loops, self-reflection gates or continue/skip/back footers
- Phase 0 names its assumptions (scope, location, target); only those become the one question message
- The plan phase ends with a single **Consent point** line; write phases run only after it
- Read-only phases (analysis, verification) never stop for approval

### 5. Phase Details - Sufficient Context Section

**MOST CRITICAL SECTION** - What context to pass to agent:

```markdown
### Phase N: Name
**Agent**: agent-name

**Sufficient context for quality**:
```yaml
Input needed:
  - Critical decisions (from Phase M: architecture chosen, file locations)
  - Constraints (performance requirements, business rules, offline requirements)
  - Existing patterns (component names, file names to match)
  - Project-specific rules (module boundaries, naming conventions)

NOT needed:
  - Full previous YAML outputs (extract decisions only)
  - Detailed user stories (agent needs requirements, not stories)
  - Generic explanations (Claude knows framework basics)
  - Intermediate analysis (agent needs conclusions, not process)
```

**Prompt to agent**:
```
[Task description]

[Critical context from previous phases - EXTRACTED, not full output]

Use skills:
- skill-name (what it provides)

[Specific instructions]

Output: [format]
```
```

**WHY this matters:**
- Agents have **isolated context** - can't see previous conversation
- Need **sufficient context for quality** - not everything, just what's critical
- **Test question**: "Can agent produce HIGH QUALITY output with this context alone?"

#### Script deterministic phase work over large inputs

When a phase does **mechanical/deterministic** work — parsing, extracting, filtering, counting, reshaping — over a **long or large input** (transcript, log, dataset, big doc), have it run a `scripts/` helper that returns ONLY the relevant slice, instead of spawning an agent to load the whole input into context and read it.

**WHY:** a script surfaces signal in long documents more cheaply, faster, and more reliably than an agent scanning the whole thing — and it keeps the phase's context budget for decisions. This is how you extract the slice *deterministically* (complements the sufficient-context principle above: script the extraction, then hand the agent the slice).

**BOUNDARY — deterministic work ONLY.** Reasoning, judgment, and synthesis stay with the agent. Do NOT script what needs the model to think; script only what a rule/regex/parser can do exactly.

### 6. Sufficient Context Principle (End Section)

**Always include at command end:**

```markdown
## Sufficient Context Principle

**For each agent, provide:**
- ✅ Critical decisions (architecture, locations, module placement)
- ✅ Constraints (performance, business rules)
- ✅ Existing patterns (follow these)
- ✅ Project-specific rules

**Do NOT provide:**
- ❌ Full previous YAML outputs
- ❌ Detailed user stories
- ❌ Generic explanations
- ❌ Intermediate analysis

**Test question**:
> "Can agent produce HIGH QUALITY output with this context alone?"
> If YES → sufficient
> If NO → add missing critical info (not everything)
```

Optional (not a mandatory phase): when the work surfaced a non-obvious pattern, end with a one-line proposal of the CLAUDE.md/skill update — proposal only, never auto-applied.

---

## Phase Design Patterns

- **Phase 0 always inline** — quick categorization, avoids wasting agent invocation
- **Merge phases** — read-only analysis phases can run as one spawn; split only when a phase needs a different agent or the plan approval sits between them
- **Parallel phases** — independent validations, multiple Task calls in single message
- **One consent point** — plan → user approval → write; nowhere else (Section 4)

---

## Anti-Patterns (Common Mistakes)

### ❌ Too Much Context
**Problem:** Passed 500-line requirements.yaml to agent. 80% unused.
**Fix:** Extract 50 lines of critical decisions only. Apply test question.

### ❌ Too Little Context
**Problem:** Agent received "Add filtering" without constraints. Produced wrong architecture.
**Fix:** Include constraints, existing patterns, project rules. Test question: "Can agent produce HIGH QUALITY?"

### ❌ Not Invoking Task Tool
**Problem:** Orchestrator describes phase instead of invoking.
**Fix:** "⚠️ CRITICAL: YOU MUST INVOKE AGENTS" section forces behavior.

### ❌ Per-Phase Question Ceremony
**Problem:** Templates demanded paraphrase + 3-5 questions after every phase, a self-reflection gate before every spawn and a continue/skip footer. Audit 2026-11-11: executed in zero observed runs (models merged phases and asked at most once), and commands generated from the template (cp-ship, kmp-ship, ios-probe) had to be overridden in the spawn prompt.
**Fix:** The ask-once rule (Section 4): one question message only about assumptions, one consent point before writes.

---

## Quick Reference

### Command Creation Checklist

**Structure:**
- [ ] Description in frontmatter (<200 chars, includes usage)
- [ ] Phases overview (with inline/agent markers, plan phase marked)
- [ ] "YOU MUST INVOKE AGENTS" section
- [ ] Critical Rules include the ask-once rule verbatim
- [ ] Each phase has "Sufficient context for quality" section
- [ ] Exactly one Consent point line (on the plan phase)
- [ ] Sufficient Context Principle at end

**Content Quality:**
- [ ] Phase 0 inline, names its assumptions (scope, location, target)
- [ ] Sufficient context section for EVERY agent phase (test question applied)
- [ ] No per-phase question blocks, self-reflection gates or continue/skip footer
- [ ] No full YAML outputs passed (extract decisions only)
- [ ] Project-specific rules and existing patterns included
- [ ] Force Task invocation (not describing)

### Decision Tree: How Many Phases?

```
Simple command (1 task, 1 agent):
  → 3 phases: Phase 0 (inline) + Phase 1 (agent) + Phase 2 (verification inline)
  → Example: debug command (70% faster than multi-agent)

Standard command (feature development):
  → 5-6 phases: Phase 0 + Requirements + Architecture + Implementation + Testing + Review
  → Example: feature command (5 phases)

Complex command (granular control):
  → 8+ phases: Separate phases for each layer + multiple reviews
  → Example: full feature command (8 phases)

Validation command (parallel checks):
  → 4 phases: Phase 0 + Phase 1+2 (parallel) + Phase 3 (merge results)
  → Example: pre-merge check (3 agents, parallel)
```

### Context Extraction Pattern

**For every agent invocation:**

1. **Read previous phase output** (full YAML)
2. **Extract decisions** (20% of content)
3. **List constraints** (from requirements/architecture)
4. **Identify patterns** (existing code to match)
5. **Include project rules** (that apply to this agent)
6. **Test question**: Can agent produce HIGH QUALITY with this?
7. **If NO**: Add missing critical info (not everything)

**Result:** 50-80 lines of pure signal, not 500 lines with 80% noise.

---

## Resources

- `@../resources/signal-vs-noise-reference.md` - 3-question filter for context decisions
- `@../resources/why-over-how-reference.md` - WHY > HOW philosophy
- `@../resources/skill-structure-reference.md` - Structure best practices
