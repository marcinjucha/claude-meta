---
name: command-creation
description: Create or refactor multi-phase commands (multi-agent orchestration). Provides structure pattern, sufficient context principle (agents have isolated context), clarifying questions pattern (3-5 flexible), and section templates. Critical for agents receiving exactly the right information.
argument-hint: "[command-name]"
---

# Command Creation - Multi-Phase Command Pattern

## Purpose

Guide for creating multi-phase command files that orchestrate multiple agents across phases. Focus on **command structure pattern**, **sufficient context principle** (agents have isolated context), and **clarifying questions pattern** (3-5 questions, flexible). Documents anti-patterns in command CREATION process (not for inclusion in command files).

## ⚠️ CRITICAL: FACT-BASED COMMAND EXAMPLES ONLY

**Why this rule exists:** Invented rework rates or timing metrics in command anti-patterns create false expectations about command performance.

**What to do:**
- User provides real command incident → Document it
- No data → Skip metrics or use placeholder: `[Real metric needed]`
- During audit → Flag invented content for removal

**RED FLAGS - NEVER invent:**
- ❌ Metrics/percentages without source ("30% faster", "50% reduction")
- ❌ Production incidents without user verification
- ❌ Team statistics or timing data
- ❌ Anti-patterns without real examples

**GREEN LIGHT - ONLY include:**
- ✅ User-provided data and incidents
- ✅ Real patterns from codebase
- ✅ Placeholder when missing: `[User to provide: real metric]`

**Quick test:** Can you verify with user/codebase? NO → Use placeholder or skip.

## ⚠️ CRITICAL: AVOID AI-KNOWN CONTENT IN COMMANDS

**Why this rule exists:** Multi-phase command prompts to agents should contain ONLY project-specific context, not generic explanations Claude already knows. Adding AI-known content wastes tokens and dilutes signal.

**WHEN CREATING COMMANDS:**

- ✅ **Agent context** → ONLY project-specific (decisions, constraints, patterns, rules)
- ✅ **Skip generic** → Framework basics, standard patterns, architecture 101
- ✅ **Self-check**: "Does agent need this to produce quality output?" → If generic knowledge, NO

**Example:**
```markdown
❌ WRONG (AI-KNOWN CONTENT IN PROMPT):
Pass to architect-agent:
- "Repository pattern separates data access from business logic"
- "MVVM architecture has ViewModel between View and Model"
- [Generic framework explanations]

✅ CORRECT (PROJECT-SPECIFIC CONTEXT):
Pass to architect-agent:
CONSTRAINTS:
  - Offline-first (40% usage offline)
  - Query-based (300 items, can't in-memory)
EXISTING PATTERNS:
  - DataRepository, DataProvider (follow naming)
PROJECT RULES:
  - NO Component→Component (use service if 3+ repos)
```

**During command creation:**
- Extract DECISIONS from previous phases (not full explanations)
- List PROJECT CONSTRAINTS (not general best practices)
- Identify EXISTING PATTERNS to match (not pattern definitions)
- Include PROJECT RULES (not standard architecture rules)

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

**CRITICAL SECTION** - Forces understanding alignment after every phase:

```markdown
### Clarifying Questions Pattern (MANDATORY)

**After EVERY phase (including Phase 0), you MUST:**

\```
Let me verify my understanding:
[2-3 sentence paraphrase of what was produced/decided in this phase]

Clarifying questions (3-5 depending on phase complexity):
1. [Question about scope/constraint from this phase]
2. [Question about edge case/requirement]
3. [Question about priority/approach]
[4. [Question about integration point - if complex phase]]
[5. [Question about validation criteria - if complex phase]]

Does this match exactly what you want to achieve? If not, what should I adjust?
\```

**Wait for user response.** If user says corrections needed:
- Apply corrections
- Paraphrase updated understanding
- Ask 3-5 NEW clarifying questions about updated version (depending on complexity)
- Repeat until user confirms "dokładnie to co chcę" / "exactly what I want"

**Only after confirmation**, proceed with: "Ready to proceed? (continue/skip/popraw/back/stop)"

**Question count guidance:**
- Simple phases (Context, Manual Testing, Review): 3 questions
- Standard phases (Requirements, Data Flow, Single Tests): 3-4 questions
- Complex phases (Architecture, Multi-layer Implementation): 4-5 questions

**Principle**: Ask enough questions to uncover hidden constraints, not more. Quality over quantity.
```

**Why clarifying questions pattern:**

Clarifying questions after EVERY phase prevent misunderstandings:
1. **Paraphrase** forces orchestrator to demonstrate understanding (not just repeat)
2. **3-5 questions** (flexible) uncover hidden constraints, edge cases, priorities user didn't mention
3. **Confirmation loop** ensures alignment before proceeding (prevents wasted work)

**Question count flexibility:**
- **Simple phases** (Context Analysis, Manual Testing, Review): 3 questions
- **Standard phases** (Requirements, Data Flow, Single Tests): 3-4 questions
- **Complex phases** (Architecture, Multi-layer Implementation): 4-5 questions

**Principle**: Ask enough questions to uncover hidden constraints, not more. Quality over quantity.

**When to apply:**
- ✅ After Phase 0 (inline assessment)
- ✅ After EVERY agent phase
- ✅ After inline phases if significant decisions made
- ❌ NOT after final report (command complete)

**Pattern anatomy:**

```markdown
**Paraphrase (2-3 sentences):**
- Summarize what was DECIDED (not what agent did)
- Focus on KEY outcomes (architecture chosen, files to modify, tests added)
- Show understanding (not copy-paste agent output)

**3-5 Questions (depending on complexity):**
1. Scope/constraint question (boundaries, limitations) - ALWAYS
2. Edge case/requirement question (what if X happens?) - ALWAYS
3. Priority/approach question (is this approach correct?) - ALWAYS
4. Integration point question (how does this connect to existing?) - If complex phase
5. Validation criteria question (what makes this "correct"?) - If complex phase

**Count guidance**: Simple=3, Standard=3-4, Complex=4-5

**Confirmation request:**
"Does this match exactly what you want to achieve? If not, what should I adjust?"
```

**Question quality:**
- Specific, actionable ("For [X], should behavior be [A] or [B]?")
- NOT generic ("Is this correct?", "Should I continue?")
- Paraphrase shows understanding (not copy-paste)

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

---

## Phase Design Patterns

**Phase 0 always inline:** Orchestrator does quick categorization. Avoids wasting agent on trivial assessment. Must include clarifying questions.

**Parallel phases:** Multiple independent validations with no dependencies. Invoke multiple Task calls in single message.

**User checkpoints:** Get approval after EVERY phase. Prevents wasted work if direction wrong.

**Clarifying questions:** MANDATORY after every phase. Paraphrase + 3-5 questions + confirmation before commands.

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
- [ ] "⚠️ CRITICAL: YOU MUST INVOKE AGENTS" section
- [ ] Critical Rules (3-5 rules, includes clarifying questions requirement with flexible count)
- [ ] "Clarifying Questions Pattern" section (template + 3-5 flexible guidance + examples)
- [ ] Phase Execution Pattern (markdown template with paraphrase + 3-5 flexible questions)
- [ ] Each phase has "Sufficient context for quality" section
- [ ] Each phase includes clarifying questions in "After agent" subsection
- [ ] Commands section (continue, skip, back, status, stop)
- [ ] "Sufficient Context Principle" at end

**Content Quality:**
- [ ] Phase 0 inline (orchestrator assessment + clarifying questions)
- [ ] "Sufficient context" section for EVERY agent phase
- [ ] Test question applied to context decisions
- [ ] Clarifying questions after EVERY phase (paraphrase + 3-5 questions + confirmation, count depends on complexity)
- [ ] User checkpoints after confirmation (continue/skip/back/stop)
- [ ] No full YAML outputs passed (extract decisions)
- [ ] Project-specific rules included
- [ ] Existing patterns listed

**Anti-Pattern Prevention:**
- [ ] Force Task invocation (⚠️ CRITICAL section)
- [ ] Context filtered (signal only, no noise)
- [ ] Clarifying questions mandatory (prevent misunderstandings)
- [ ] Flexible question count (3-5 depending on phase complexity)
- [ ] User checkpoints after confirmation (prevent wasted phases)
- [ ] Test question documented (for future maintainers)
- [ ] Commands offered ONLY after confirmation (not before)

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

## Key Principles

**Command Structure:** Standard sections (our convention), Phase 0 inline, user checkpoints, clarifying questions mandatory

**Clarifying Questions (MANDATORY):** After EVERY phase - paraphrase + 3-5 questions (flexible, depends on complexity) + confirmation before commands

**Sufficient Context:** Test question ("Can agent produce HIGH QUALITY?"), signal/noise filter, extract decisions (not full outputs)

**Force Invocation:** "⚠️ CRITICAL" section prevents describing instead of invoking

**WHY Explanations:**
- Phase 0 inline (WHY: avoids wasting agent)
- Clarifying questions (WHY: prevents misunderstandings, ensures alignment)
- Flexible question count (WHY: match complexity, quality over rigid count)
- User checkpoints (WHY: prevents wasted phases)

---

## Resources (Tier 3 - Philosophy)

**Shared resources** (`@../resources/`) - Common across meta-skills:
- `@../resources/signal-vs-noise-reference.md` - 3-question filter for deciding what to include in commands
- `@../resources/why-over-how-reference.md` - Content quality philosophy (WHY > HOW, production context)
- `@../resources/skill-structure-reference.md` - Standard structure and best practices (adaptable to command structure)

**Use references for:**

- Signal vs Noise → Filter what context to provide agents (sufficient, not excessive)
- Why over How → Include rationale for command structure decisions (why phases, why checkpoints)
- Structure → Consistent command organization (phase structure, section patterns)

**Why included:**

- Consistent philosophy across all meta skills (skills, agents, commands)
- Decision framework for command content (what to include, what to skip)
- Quality guidelines (sufficiency > brevity, WHY explanations mandatory)

---

**Key Lesson:** Multi-phase commands need standard structure + sufficient context principle + clarifying questions (3-5 flexible) + forced invocation. Agents have isolated context - must provide exactly right information (test question). Clarifying questions after every phase prevent misunderstandings. Match question count to phase complexity.
