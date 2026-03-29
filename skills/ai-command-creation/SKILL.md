---
name: ai-command-creation
description: Create or refactor multi-phase commands (multi-agent orchestration). Provides structure pattern, sufficient context principle (agents have isolated context), clarifying questions pattern (3-5 flexible), and section templates. Critical for agents receiving exactly the right information.
argument-hint: "[command-name]"
---

# Command Creation - Multi-Phase Command Pattern

## Purpose

Guide for creating multi-phase command files that orchestrate multiple agents across phases. Focus on **command structure pattern**, **sufficient context principle** (agents have isolated context), and **clarifying questions pattern** (3-5 questions, flexible). Documents anti-patterns in command CREATION process (not for inclusion in command files).

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
[Phase overview with inline/agent markers]

## Orchestrator Instructions

### ⚠️ CRITICAL: YOU MUST INVOKE AGENTS
[Force actual Task tool invocation]

### Critical Rules
[3-5 rules, numbered, includes clarifying questions requirement]

### Clarifying Questions Pattern (MANDATORY)
[Template with 3-5 flexible questions, guidance on count]

### Phase Execution Pattern
[Markdown template for presenting phases with clarifying questions]

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

**After agent**: [how to present results with clarifying questions]

## Commands
[continue, skip, back, status, stop]

## Sufficient Context Principle
[Test question, signal/noise examples]

### Final Phase: Knowledge Capture
**Agent**: ai-manager-agent (or project-specific agent)
[Post-workflow analysis: identify patterns worth capturing]
```

**Why this structure:**
- **Phases overview** - orchestrator sees full command before starting
- **Orchestrator Instructions** - forces actual Task invocation (anti-pattern: just describing)
- **Clarifying Questions Pattern** - MANDATORY section with 3-5 flexible questions guidance
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
2: Architecture          (agent-name with skill-name skill)
3: Implementation        (agent-name)
```

**Speed**: X-Y min
```

**Pattern:**
- Phase 0 always inline (orchestrator assessment)
- Mark which agent for each phase
- Mention key skills if relevant
- Estimated duration

**WHY Phase 0 inline:** Orchestrator does quick categorization before launching agents. Avoids wasting agent invocation on trivial assessment (complexity check, file categorization).

**CRITICAL:** Phase 0 MUST include clarifying questions pattern before proceeding to Phase 1.

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

1. **INVOKE with Task tool** - Every phase requires actual Task tool call
2. **Sufficient context** - Each agent gets ONLY what it needs for quality
3. **Clarifying questions mandatory** - Paraphrase + 3-5 questions after EVERY phase (count depends on complexity)
4. **User checkpoints** - Get approval after each phase
5. **Track phase** - Remember current position

### Phase Execution Pattern

**UPDATED TEMPLATE** (includes clarifying questions):

```
═══════════════════════════════════════════════
Phase N/5: [Name]
═══════════════════════════════════════════════

Launching [agent]...
```

[Invoke Task tool]

```
**Phase N Complete** ✅

[Present agent output clearly]

───────────────────────────────────────────────
Let me verify my understanding:
[2-3 sentence paraphrase of what was produced/decided]

Clarifying questions (3-5 depending on phase complexity):
1. [Question about scope/constraint]
2. [Question about edge case/requirement]
3. [Question about priority/approach]
[4. [Question about integration point - if complex]]
[5. [Question about validation criteria - if complex]]

Does this match exactly what you want? If not, what should I adjust?
───────────────────────────────────────────────

[Wait for user confirmation]

Ready to proceed? (continue/skip/popraw/back/stop)
```
```

**WHY this section:**
- **Anti-pattern prevention**: Orchestrator describing instead of invoking
- **Force behavior**: Explicit DO/DON'T forces actual Task tool use
- **User checkpoints**: Prevents wasting phases if direction wrong

### 4. Clarifying Questions Pattern (REQUIRED)

**After EVERY phase (including Phase 0):** Paraphrase (2-3 sentences summarizing DECISIONS, not agent output) + 3-5 questions + confirmation loop.

**Question count:** Simple phases = 3, Standard = 3-4, Complex = 4-5. Quality over quantity.

**Question types:** (1) Scope/constraint - ALWAYS, (2) Edge case - ALWAYS, (3) Priority/approach - ALWAYS, (4) Integration point - if complex, (5) Validation criteria - if complex.

**Questions must be specific and actionable** ("For [X], should behavior be [A] or [B]?"), not generic ("Is this correct?").

**Confirmation loop:** Wait for user response. If corrections needed, paraphrase updated understanding + ask new questions. Repeat until confirmed. Only then offer commands (continue/skip/back/stop).

**When to apply:** After Phase 0, after every agent phase, after inline phases with significant decisions. NOT after final report.

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

### 6. Commands Section

```markdown
## Commands

- `continue` - Next phase
- `skip` - Skip current phase
- `back` - Previous phase
- `status` - Show progress
- `stop` - Exit workflow
```

**Standard across all commands.**

### 7. Sufficient Context Principle (End Section)

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

### 8. Knowledge Capture Phase (Always Last)

**Standard final phase for any multi-phase command.** Always executes — agent decides if anything is worth capturing.

**WHY separate phase:** Structured post-workflow analysis catches project-specific patterns that an ad-hoc "should we update docs?" question misses. Patterns discovered during implementation are lost if not captured immediately.

**Template for Phase Details:**

```markdown
### Phase N: Knowledge Capture
**Agent**: ai-manager-agent (default — swap for project-specific agent if domain expertise needed, or run inline if command is simple)

**Skills to load**: signal-vs-noise-reference (shared resource, always loaded via @../resources/ — for conciseness filtering), others at agent's discretion based on what was discovered

**Sufficient context for quality**:
```yaml
Input needed:
  - Completed task name + requirements summary
  - Key implementation decisions made during workflow
  - Validation findings (blocked issues, warnings)
  - Testing outcome (pass/fail, retry count, failure descriptions)
  - Files changed (ONLY if relevant to a specific non-obvious pattern)

NOT needed:
  - Full phase outputs (extract decisions only)
  - Generic implementation details
  - File lists without non-obvious context
```

**Prompt to agent**:
```
Analyze completed workflow for knowledge worth capturing.

COMPLETED TASK: [task name + requirements summary]
KEY DECISIONS: [extracted from previous phases]
VALIDATION FINDINGS: [issues, warnings]
TESTING OUTCOME: [pass/fail, retries, failures]
FILES CHANGED: [only if non-obvious pattern]

Agent tasks:
1. Identify patterns worth capturing — non-obvious decisions, bugs, new integration patterns
2. Apply signal filter: skip generic knowledge, skip one-off details, skip patterns already in existing skills
3. Determine WHERE (which CLAUDE.md or skill) and WHAT (exact addition)
4. PROPOSE to user — never auto-update
5. If nothing worth capturing: say so explicitly

Output: Proposals with Target / Type / Content / WHY signal
  — OR "No patterns worth capturing" with brief explanation
```

**After agent**: Present proposals to user. No clarifying questions needed — this is the final phase.
```

**Key rules:**
- **Always last** — never followed by another phase
- **Always executes** — but agent may conclude "nothing worth capturing" (must say so explicitly)
- **Never auto-updates** — proposals only, user decides
- **Default agent: ai-manager-agent** — swap for project-specific agent when domain expertise helps quality of pattern identification
- **signal-vs-noise-reference always available** — shared resource ensures proposals pass 3-question filter

---

## Phase Design Patterns

- **Phase 0 always inline** — quick categorization, avoids wasting agent invocation
- **Parallel phases** — independent validations, multiple Task calls in single message
- **User checkpoints** — approval after EVERY phase (prevents wasted work)
- **Clarifying questions** — apply pattern from Section 4 after every phase
- **Knowledge Capture always last** — agent decides if anything is signal, proposals only

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

### ❌ No User Checkpoints
**Problem:** Ran 8 phases, Phase 3 wrong, all later work wasted.
**Fix:** Get approval after EACH phase. Commands: continue/skip/back/stop.

### ❌ No Clarifying Questions
**Problem:** Agent assumes, user doesn't notice misalignment until later phases.
**Fix:** MANDATORY clarifying questions after every phase. Paraphrase + 3-5 questions + confirmation.

---

## Quick Reference

### Command Creation Checklist

**Structure:**
- [ ] Description in frontmatter (<200 chars, includes usage)
- [ ] Phases overview (with inline/agent markers)
- [ ] "YOU MUST INVOKE AGENTS" section
- [ ] Clarifying Questions Pattern section
- [ ] Phase Execution Pattern template
- [ ] Each phase has "Sufficient context for quality" section
- [ ] Commands section (continue, skip, back, status, stop)
- [ ] Sufficient Context Principle at end
- [ ] Knowledge Capture as final phase

**Content Quality:**
- [ ] Phase 0 inline + clarifying questions
- [ ] Sufficient context section for EVERY agent phase (test question applied)
- [ ] Clarifying questions after EVERY phase (paraphrase + 3-5 questions + confirmation)
- [ ] No full YAML outputs passed (extract decisions only)
- [ ] Project-specific rules and existing patterns included
- [ ] Force Task invocation (not describing)
- [ ] Commands offered ONLY after user confirmation

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

---

## Resources

- `@../resources/signal-vs-noise-reference.md` - 3-question filter for context decisions
- `@../resources/why-over-how-reference.md` - WHY > HOW philosophy
- `@../resources/skill-structure-reference.md` - Structure best practices
