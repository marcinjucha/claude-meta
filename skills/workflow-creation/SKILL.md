---
name: workflow-creation
description: Create or refactor workflow commands (multi-phase orchestration). Provides structure pattern, sufficient context principle (agents have isolated context), clarifying questions pattern (3-5 flexible), and section templates. Critical for agents receiving exactly the right information.
argument-hint: "[workflow-name]"
---

# Workflow Creation - Multi-Agent Orchestration Pattern

## Purpose

Guide for creating workflow command files that orchestrate multiple agents across phases. Focus on **workflow structure pattern**, **sufficient context principle** (agents have isolated context), and **clarifying questions pattern** (3-5 questions, flexible). Documents anti-patterns in workflow CREATION process (not for inclusion in workflow files).

## When to Use

- Creating new workflow command (multi-phase orchestration)
- Refactoring existing workflow (structure inconsistent)
- Understanding workflow file conventions
- Deciding what context to pass to agents
- Fixing workflows where agents produce low-quality output

---

## Workflow File Structure Pattern

**Standard workflow file structure** (our convention):

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
- **Phases overview** - orchestrator sees full workflow before starting
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
- **Anti-pattern prevention**: Orchestrator describing instead of invoking (happened 30% of time without this section)
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

Production validation: Workflows WITHOUT this pattern had 40% rework rate (agent produced output, user said "that's not what I wanted", had to redo phase). Workflows WITH pattern had 8% rework rate.

Root cause: User description ambiguous → agent makes assumptions → output doesn't match intent → wasted phase.

Clarifying questions after EVERY phase:
1. **Paraphrase** forces orchestrator to demonstrate understanding (not just repeat)
2. **3-5 questions** (flexible) uncover hidden constraints, edge cases, priorities user didn't mention
3. **Confirmation loop** ensures alignment before proceeding (prevents wasted work)

**Question count flexibility:**
- **Simple phases** (Context Analysis, Manual Testing, Review): 3 questions
  - Less complexity, fewer unknowns
  - Example: Phase 0 context categorization
- **Standard phases** (Requirements, Data Flow, Single Tests): 3-4 questions
  - Moderate complexity, standard patterns
  - Example: Requirements gathering
- **Complex phases** (Architecture, Multi-layer Implementation): 4-5 questions
  - High complexity, many integration points
  - Example: Architecture design with module placement

**Principle**: Ask enough questions to uncover hidden constraints, not more. Quality over quantity.

**When to apply:**
- ✅ After Phase 0 (inline assessment)
- ✅ After EVERY agent phase
- ✅ After inline phases if significant decisions made
- ❌ NOT after final report (workflow complete)

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

**Real examples from workflows:**

**ios-debug-full (Phase 0, complex debugging - 5 questions):**
```
Let me verify my understanding:
[Paraphrase: bug severity, affected areas, type]

Clarifying questions (5 for complex debugging):
1. Is this bug [specific symptom], or does it also involve [other symptom]?
2. Does this occur consistently, or only under [specific conditions]?
3. Are there specific constraints I should know about (urgent fix, affects production)?
4. What existing components might be affected (list specific BUS/modules if any)?
5. What's the primary success criterion - what makes this bug "fixed"?

Does this match exactly what you want to achieve? If not, what should I adjust?
```

**Note**: This Phase 0 example shows 5 questions (complex debugging scenario). For simpler Phase 0 (feature categorization), use 3 questions.

**ios-feature-full (Phase 1, requirements - 5 questions for complex feature):**
```
Let me verify my understanding:
[2-3 sentence paraphrase of requirements - functional goals, key edge cases, main dependencies]

Clarifying questions (5 for complex requirements):
1. Are the functional requirements complete, or should I add [specific missing item]?
2. For [specific edge case] - how should the feature behave?
3. The requirements mention [specific dependency] - is this the correct approach, or should we use [alternative]?
4. Priority: Which requirement is MUST-HAVE vs NICE-TO-HAVE for first version?
5. Testing: What's the primary success test case that proves this feature works?

Does this match exactly what you want? If not, what should I adjust?
```

**Note**: Requirements phase shown with 5 questions (complex feature). Standard requirements might need only 3-4.

**merge-check (no clarifying questions, different pattern):**
Note: merge-check uses different pattern (show findings → ask continue/stop), not clarifying questions. Clarifying questions for workflows where user defines scope iteratively.

**Common mistakes:**

❌ **Wrong question count (inflexible):**
Always asking exactly 5 questions regardless of complexity → Wastes time on simple phases.
Always asking only 3 questions for complex phases → Misses critical constraints.

✅ **Flexible question count:**
Simple phases: 3 questions (covers basics)
Complex phases: 4-5 questions (uncovers integration points, validation criteria)
Match question count to phase complexity.

❌ **Generic questions:**
"Is this correct?" → Too vague
"Should I continue?" → Not clarifying
"Any other requirements?" → Open-ended

✅ **Specific, actionable questions:**
"For [X], should behavior be [A] or [B]?"
"Does [component] live in [location A] or [location B]?"
"When [condition], should we [action A] or [action B]?"

❌ **Paraphrase repeats agent output:**
"The agent produced requirements with functional goals..." → Just describing process
"Here's what was decided..." → Not demonstrating understanding

✅ **Paraphrase shows understanding:**
"Feature adds filtering by status and date, must work offline (40% usage), max 2s response."
"Architecture uses Full BUS (has UI), Repository→UseCase→ViewModel→View flow, files in TalentDomain/AccountSubdomain."

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

**Standard across all workflows.**

### 7. Sufficient Context Principle (End Section)

**Always include at workflow end:**

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

## Sufficient Context Principle

**CORE PHILOSOPHY** - Agents have isolated context, need exactly right information.

### Why This Matters

**Agents don't see previous conversation.** Each agent invocation starts fresh. Must provide sufficient context for HIGH QUALITY output, but not noise.

**The Problem:**
- Too much context → Waste tokens, slow processing, 80% unused
- Too little context → Generic output, multiple rounds needed, wasted time

**The Solution:** Test question for every context decision.

### The Test Question

**Before passing ANY context to agent, ask:**

```
"Can this agent produce HIGH QUALITY output with this context alone?"

If YES → Context is sufficient
If NO → Add missing CRITICAL information (not everything, just what's missing)
```

**HIGH QUALITY means:**
- Project-specific (not generic)
- Follows existing patterns (knows what to match)
- Meets constraints (knows performance/business rules)
- Correct layer placement (knows architecture decisions)

### Signal vs Noise Filter

**SIGNAL (Include):**
- ✅ **Critical decisions** from previous phases
  - Example: "Architecture Phase decided: Use service pattern (combines 3 components), files in core module"
- ✅ **Constraints** that affect implementation
  - Example: "Offline-first required, query-based filtering (300 items), max 2s response"
- ✅ **Existing patterns** to follow
  - Example: "Component naming: DataAccessLayer, DataProvider (match this pattern)"
- ✅ **Project-specific rules**
  - Example: "NO Component→Component dependencies, shared code in ModuleA only"

**NOISE (Exclude):**
- ❌ **Full previous YAML outputs** (too verbose, extract decisions only)
  - Example: Don't pass 500-line requirements.yaml → Extract 50 lines of critical requirements
- ❌ **Detailed user stories** (agent doesn't need full context)
  - Example: "As a user..." → "Must work offline, 40% usage time offline"
- ❌ **Generic explanations** (Claude knows this)
  - Example: "Framework X is..." → Just say which pattern to use
- ❌ **Intermediate analysis** (agent needs conclusions, not process)
  - Example: "We considered 3 options..." → Just say which option was chosen + WHY

### Real Examples

**Example 1: architect-agent Phase (Architecture Design)**

**✅ SUFFICIENT (50 lines):**
```
INTENT: Add data filtering by status and date
CONSTRAINTS:
  - Offline-first (40% usage time offline)
  - Query-based filtering (300 items, can't load all)
  - Max 2s response time
COMPLEXITY: Simple (single feature, existing patterns)
```

**❌ TOO MUCH (500 lines):**
```
[Full requirements.yaml with:]
- Complete user stories ("As a user...")
- Acceptance criteria (15 items)
- Edge cases documentation
- UI mockups descriptions
- [80% of this is noise for architecture decisions]
```

**Result:** Agent produced same quality architecture with 50 lines vs 500 lines. 90% token savings.

**Example 2: developer-agent Phase (Implementation)**

**✅ SUFFICIENT (80 lines):**
```
ARCHITECTURE (from Phase 2):
  Layers: DataAccessLayer, BusinessLogic, Presentation
  Files:
    - core/data/DataFilter.ext
    - app/business/FilterLogic.ext
    - app/presentation/FilterUI.ext
  Module: DataAccessLayer in core, rest in app

CONSTRAINTS:
  - Offline-first: query-based filtering
  - Performance: max 2s response

EXISTING PATTERNS:
  - DataAccessLayer: DataProvider, DataRepository
  - BusinessLogic: DataProcessor, DataHandler
  - Presentation: UIComponent pattern

PROJECT RULES:
  - NO Component→Component (use service if needed)
  - Shared code: ModuleA YES, ModuleB NO
  - String constants only (never hardcoded strings)
```

**❌ TOO LITTLE (20 lines):**
```
Implement data filtering feature.
Use standard patterns.
```

**Result:** With too little context, agent produced generic implementation, didn't follow project patterns, required rework.

### Application Pattern

**For EVERY agent invocation:**

1. **Extract decisions** from previous phases (not full output)
2. **List constraints** that affect this agent's work
3. **Identify patterns** agent must follow
4. **Include project rules** that apply
5. **Apply test question**: Can agent produce HIGH QUALITY with this?
6. **If NO**: Add missing critical info (not everything)

---

## Phase Design Patterns

### When to Run Phases in Parallel

**Pattern:** Multiple independent validations, no dependencies.

**Example:** Pre-merge check - Phase 1 (Performance) + Phase 2 (Boundaries)
- Performance analyzes changed files for anti-patterns
- Boundaries check imports for module violations
- **NO dependency** between them

**How to implement:**
```markdown
### Phase 1+2: Parallel Validation

Launching:
1. quality-agent (performance)
2. architect-agent (module boundaries)

Running in parallel... ⏳
```

[Invoke BOTH Task calls in SINGLE message]

**When NOT parallel:** Phase N needs output from Phase M (sequential dependency).

### Phase 0 Always Inline

**Pattern:** Phase 0 = orchestrator does quick assessment, no agent.

**Why:**
- Quick categorization (complexity, affected files, issue type)
- Avoids wasting agent invocation on trivial task
- Orchestrator already has context (user request)

**Example:**
```markdown
### Phase 0: Context Analysis (Inline)
**You do this - no agent**

Quick assessment:
- **Type:** [categorize request]
- **Complexity:** [simple/moderate/complex]
- **Files affected:** [from git diff or description]

Output: Brief note
Decision: Continue workflow or suggest alternative
```

### User Checkpoints After Each Phase (MANDATORY)

**Pattern:** Get user approval before proceeding.

**Why:** Prevents wasting phases if direction wrong. User can adjust mid-workflow.

**CRITICAL SEQUENCE (after EVERY phase):**

```markdown
**Phase N Complete** ✅
[Present agent output clearly]

───────────────────────────────────────────────
Let me verify my understanding:
[2-3 sentence paraphrase]

Clarifying questions (3-5 depending on phase complexity):
1. [Specific question]
2. [Specific question]
3. [Specific question]
[4. [Specific question - if complex]]
[5. [Specific question - if complex]]

Does this match exactly what you want? If not, what should I adjust?
───────────────────────────────────────────────

[WAIT FOR USER CONFIRMATION]

[Only after user confirms understanding is correct:]

Ready to proceed? (continue/skip/popraw/back/stop)
```

**Timing sequence (mandatory order):**
1. Present output
2. Paraphrase understanding
3. Ask 3-5 clarifying questions (depends on complexity)
4. Wait for confirmation ("dokładnie to co chcę")
5. THEN offer commands (continue/skip/back)

**Anti-pattern:** Offering commands before confirmation
```markdown
❌ WRONG:
**Phase N Complete** ✅
[Output]
Ready to proceed? (continue/skip/back/stop)

✅ CORRECT:
**Phase N Complete** ✅
[Output]

Let me verify my understanding:
[Paraphrase + 3-5 questions]

Does this match exactly what you want?
[WAIT]

Ready to proceed? (continue/skip/back/stop)
```

**Real mistake:** Ran all 8 phases without approval. Phase 3 architecture wrong, but all implementation done. Had to rerun entire workflow.

**Why mandatory clarifying questions prevent this:** User catches wrong direction at Phase 3 (during clarifying questions), corrects understanding, continues from corrected Phase 3. Only Phase 3 wasted, not Phases 4-8.

---

## Anti-Patterns (Critical Mistakes We Made)

### ❌ Mistake 1: Too Much Context (Noise Overload)

**Problem:** Passed full 500-line requirements.yaml to developer-agent. Agent took 3x longer, output quality same.

**Why bad:**
- Wasted tokens (400 lines unused)
- Slower processing (agent must parse everything)
- Not signal (80% generic user stories, not implementation details)

**Real example:** Phase 3 - originally passed full requirements.yaml (500 lines). Reduced to 50-line architecture summary (decisions + constraints + existing patterns). Output quality identical, 90% token savings.

**Fix:** Extract only critical decisions/constraints. Apply test question: "Does agent need this to produce quality output?"

**Before (500 lines):**
```yaml
requirements:
  user_stories:
    - As a user, I want to filter data by status...
    - [20 user stories with acceptance criteria]
  edge_cases:
    - [15 edge cases documented]
  ui_mockups:
    - [Descriptions of UI screens]
  [Full user stories, acceptance criteria, etc.]
```

**After (50 lines):**
```yaml
ARCHITECTURE:
  Layers: DataAccessLayer, BusinessLogic, Presentation
  Files: [paths]
  Module: Core vs App placement

CONSTRAINTS:
  - Offline-first (40% usage offline)
  - Query-based (300 items)
  - Max 2s response

EXISTING PATTERNS:
  - DataProvider, DataRepository
  - Follow naming

PROJECT RULES:
  - NO Component→Component
  - Shared code: ModuleA YES, ModuleB NO
```

### ❌ Mistake 2: Too Little Context (Insufficient Quality)

**Problem:** architect-agent received just "Add filtering" without constraints. Produced generic solution, needed rework.

**Why bad:**
- Agent output generic (no project-specific context)
- Multiple rounds needed (back-and-forth clarification)
- Wasted time (2 invocations instead of 1)

**Real example:** Phase 2 - architect received "Add data filtering" without offline-first constraint. Designed in-memory filtering (loaded all items). But requirement: 40% offline time + 300 items. Had to redesign for query-based with database. Wasted 1 phase.

**Fix:** Apply test question. If agent can't produce QUALITY output, add missing CRITICAL info.

**Before (20 lines - insufficient):**
```
Add data filtering feature.
Use standard patterns.
```

**After (80 lines - sufficient):**
```
INTENT: Data filtering by status and date
CONSTRAINTS:
  - Offline-first (40% usage offline time)
  - Query-based filtering (300 items, can't in-memory)
  - Max 2s response
COMPLEXITY: Simple
EXISTING: DataAccessLayer (database), DataProcessor
PROJECT RULES: Query-based for >100 items
```

### ❌ Mistake 3: Not Invoking Task Tool (Just Describing)

**Problem:** Orchestrator said "I will now launch developer-agent..." but didn't invoke Task tool. Workflow stopped.

**Why bad:**
- Workflow stops (no agent actually runs)
- User confused (thinks agent is running)
- Manual intervention needed (user has to remind)

**Real example:** Before adding "⚠️ CRITICAL: YOU MUST INVOKE AGENTS" section, 30% of workflow runs had orchestrator describe phase instead of invoking. User had to say "actually run it."

**Fix:** "⚠️ CRITICAL" section in every workflow. Forces actual Task tool invocation.

**Wrong behavior:**
```
Phase 2: Architecture Design

I will now launch the architect-agent to design the architecture.
The agent will analyze the requirements and produce...

[NO Task tool invocation - workflow stops]
```

**Correct behavior:**
```
Phase 2: Architecture Design

Launching architect-agent...

[IMMEDIATELY invokes Task tool with subagent_type="architect-agent"]
```

### ❌ Mistake 4: No User Checkpoints

**Problem:** Ran all 8 phases without approval. Phase 3 architecture wrong, but all implementation done (Phase 4-8 wasted).

**Why bad:**
- Wasted 5 phases (architecture decision wrong)
- User couldn't adjust mid-workflow
- Had to rerun entire workflow

**Real example:** User wanted service pattern (3 components), but architect chose single component pattern. User only saw this after Phase 8 (all implementation done). Had to rerun workflow from Phase 3.

**Fix:** Get user approval after EACH phase. Commands: continue, skip, back, stop.

**Pattern:**
```markdown
**Phase N Complete** ✅
[Summary of agent output]

Ready to proceed? (continue/skip/back/stop)
```

**Why this works:** User can catch wrong direction early, adjust, and continue from correct point.

### ❌ Mistake 5: No Clarifying Questions (Assumption Errors)

**Problem:** Orchestrator presented phase output, immediately offered commands (continue/skip/back), no clarifying questions. User confirmed "continue" without understanding being verified.

**Why bad:**
- Orchestrator made assumptions about ambiguous user input
- User didn't realize output didn't match intent until later phases
- Rework required (redo phases already completed)

**Real example (40% rework rate before pattern):**
- Phase 1: Requirements analyst interpreted "filtering" as in-memory filtering
- User said "continue" (didn't notice assumption)
- Phase 2-4: Architecture, implementation all based on in-memory approach
- Phase 5: User testing revealed: "I meant database query-based filtering for 300 items"
- Had to redo Phases 2-5 (wasted 30 minutes)

**Root cause:** Ambiguous requirement ("filtering") → Agent assumed approach → No clarifying questions to uncover constraint (300 items, database required) → Wrong direction

**Fix:** Clarifying questions MANDATORY after EVERY phase (including Phase 0). Pattern:

```markdown
**Phase N Complete** ✅
[Present output]

───────────────────────────────────────────────
Let me verify my understanding:
[2-3 sentence paraphrase]

Clarifying questions (3-5 depending on complexity):
1. [Scope/constraint question]
2. [Edge case question]
3. [Priority/approach question]
[4. [Integration question - if complex]]
[5. [Validation question - if complex]]

Does this match exactly what you want? If not, what should I adjust?
───────────────────────────────────────────────

[WAIT for confirmation]

Ready to proceed? (continue/skip/popraw/back/stop)
```

**Production impact:**
- Before pattern: 40% rework rate (2 out of 5 workflows needed redo)
- After pattern: 8% rework rate (clarifying questions caught misunderstandings early)
- Time savings: 20 minutes average per workflow (prevented rework)

**Why clarifying questions work:**
1. **Paraphrase** forces orchestrator to demonstrate understanding (not just acknowledge)
2. **3-5 specific questions** (flexible) uncover hidden constraints, edge cases, priorities
3. **Confirmation loop** ensures alignment before proceeding
4. **Early detection** catches wrong direction at Phase N (not Phase N+3)

**When to apply:**
- ✅ After Phase 0 (inline assessment before workflow starts)
- ✅ After EVERY agent phase (Phase 1, 2, 3, 4...)
- ✅ After inline phases IF significant decisions made
- ❌ NOT after final report (workflow complete, no more phases)

---

## Quick Reference

### Workflow Creation Checklist

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
Simple workflow (1 task, 1 agent):
  → 3 phases: Phase 0 (inline) + Phase 1 (agent) + Phase 2 (verification inline)
  → Example: debug workflow (70% faster than multi-agent)

Standard workflow (feature development):
  → 5-6 phases: Phase 0 + Requirements + Architecture + Implementation + Testing + Review
  → Example: feature workflow (5 phases)

Complex workflow (granular control):
  → 8+ phases: Separate phases for each layer + multiple reviews
  → Example: full feature workflow (8 phases)

Validation workflow (parallel checks):
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

**Workflow Structure:** Standard sections (our convention), Phase 0 inline, user checkpoints, clarifying questions mandatory

**Clarifying Questions (MANDATORY):** After EVERY phase - paraphrase + 3-5 questions (flexible, depends on complexity) + confirmation before commands

**Sufficient Context:** Test question ("Can agent produce HIGH QUALITY?"), signal/noise filter, extract decisions (not full outputs)

**Force Invocation:** "⚠️ CRITICAL" section prevents describing instead of invoking

**WHY Explanations:**
- Phase 0 inline (WHY: avoids wasting agent)
- Clarifying questions (WHY: 40% → 8% rework rate, prevents misunderstandings)
- Flexible question count (WHY: match complexity, quality over rigid count)
- User checkpoints (WHY: prevents wasted phases)

---

## Resources (Tier 3 - Philosophy)

**This skill includes philosophy reference files:**

- `@resources/signal-vs-noise-reference.md` - 3-question filter for deciding what to include in workflows
- `@resources/why-over-how-reference.md` - Content quality philosophy (WHY > HOW, production context)
- `@resources/skill-structure-reference.md` - Standard structure and best practices (adaptable to workflow structure)

**Use references for:**

- Signal vs Noise → Filter what context to provide agents (sufficient, not excessive)
- Why over How → Include rationale for workflow structure decisions (why phases, why checkpoints)
- Structure → Consistent workflow organization (phase structure, section patterns)

**Why included:**

- Consistent philosophy across all meta skills (skills, agents, workflows)
- Decision framework for workflow content (what to include, what to skip)
- Quality guidelines (completeness > brevity, WHY explanations mandatory)

---

**Key Lesson:** Workflows need standard structure + sufficient context principle + clarifying questions (3-5 flexible) + forced invocation. Agents have isolated context - must provide exactly right information (test question). Clarifying questions after every phase prevent 40% rework rate. Match question count to phase complexity.
