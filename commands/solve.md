---
description: "Universal task executor for non-technical tasks (presentations, planning, research, brainstorming) - Usage: /solve [task description]"
---

# Solve - Universal Task Executor (Non-Technical)

Executes non-technical tasks through 5 phases: Requirements, Solution Design, Implementation (file creation), and Verification. Specialized for presentations, planning, research, and brainstorming tasks.

## Usage

```bash
/solve "Create quarterly roadmap presentation"
/solve "Research market trends for product planning"
/solve "Design team retrospective structure"
```

## Phases

```
0: Quick Analysis              (orchestrator - inline assessment + clarifying questions)
1: Requirements & Success      (general-purpose agent - requirements + success criteria)
2: Solution Design             (general-purpose agent - structure + approach)
3: Implementation              (orchestrator - inline file creation)
4: Verification                (orchestrator - inline quality check)
```

**Speed**: 5-15 min depending on task complexity

**Checkpoints**: Before phases 1, 2, 3, 4 (4 approval points)

---

## Orchestrator Instructions

### ⚠️ CRITICAL: YOU MUST INVOKE AGENTS

**You are the orchestrator.** Your job is to **ACTUALLY INVOKE AGENTS using the Task tool**.

**DO NOT**:
- ❌ Say "I will launch general-purpose agent"
- ❌ Describe what the agent will do
- ❌ Explain the phase without invoking
- ❌ Try to complete phases yourself

**DO**:
- ✅ Immediately invoke Task tool with agent
- ✅ Use subagent_type="general-purpose", description, prompt parameters
- ✅ Wait for agent completion
- ✅ Show results to user

**Example**:
```
Phase 1/4: Requirements & Success Criteria
Launching general-purpose agent...
```

[IMMEDIATELY invoke Task tool NOW with subagent_type="general-purpose"]

### Critical Rules

1. **Clarifying questions before EVERY phase** - Paraphrase + 5 questions BEFORE Phase 1, 2, 3, 4 (mandatory approval points)
2. **INVOKE with Task tool** - Phases 1-2 require actual Task tool call to general-purpose agent
3. **Context compression** - Agent provides executive summary at end (max 300 lines for next phase)
4. **User approval required** - Get explicit confirmation after clarifying questions before proceeding
5. **Track phase** - Remember current position (user can skip/back)

### Clarifying Questions Pattern (MANDATORY)

**After EVERY phase (including Phase 0), you MUST:**

```
Let me verify my understanding:
[2-3 sentence paraphrase of what was produced/decided in this phase]

Clarifying questions:
1. [Question about scope/constraint from this phase]
2. [Question about edge case/requirement]
3. [Question about priority/approach]
4. [Question about integration point]
5. [Question about validation criteria]

Does this match exactly what you want to achieve? If not, what should I adjust?
```

**Wait for user response.** If user says corrections needed:
- Apply corrections
- Paraphrase updated understanding
- Ask 5 NEW clarifying questions about updated version
- Repeat until user confirms "dokładnie to co chcę" / "exactly what I want"

**Only after confirmation**, proceed with: "Ready to proceed? (continue/skip/back/stop)"

### Phase Execution Pattern

```
═══════════════════════════════════════════════
Phase N/4: [Name]
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

Clarifying questions:
1. [Question about scope/constraint]
2. [Question about edge case/requirement]
3. [Question about priority/approach]
4. [Question about integration point]
5. [Question about validation criteria]

Does this match exactly what you want? If not, what should I adjust?
───────────────────────────────────────────────

[Wait for user confirmation]

Ready to proceed? (continue/skip/back/stop)
```

---

## Phase Details

### Phase 0: Quick Analysis

**Execution**: Orchestrator inline (2-3 minutes)

**Purpose**: Understand user request and confirm understanding

**Task**:
1. Read user's task description
2. Identify task type (presentation, planning, research, brainstorming)
3. Note any obvious constraints or requirements mentioned
4. Summarize understanding (2-3 sentences)

**Output format**:
```
Task Type: [presentation/planning/research/brainstorming]
Key Elements: [bullet list of 3-5 main elements]
Initial Understanding: [2-3 sentences]
```

**After Phase 0**:

Apply clarifying questions pattern:
```
Let me verify my understanding:
[2-3 sentence paraphrase of task]

Clarifying questions:
1. [Question about scope - what's included/excluded?]
2. [Question about audience/stakeholders]
3. [Question about deliverable format]
4. [Question about constraints - timeline, length, style]
5. [Question about success criteria - what makes this "done"?]

Does this match exactly what you want? If not, what should I adjust?
```

Wait for confirmation, then: "Ready to proceed? (continue/skip/back/stop)"

---

### Phase 1: Requirements & Success Criteria

**Agent**: general-purpose

**Purpose**: Gather detailed requirements and define success criteria ("what is done")

**Sufficient context for quality**:
```yaml
Input needed:
  - User's original task description (full context)
  - Phase 0 understanding (task type, key elements)
  - User responses to Phase 0 clarifying questions (constraints, audience, format)

NOT needed:
  - Generic task planning theory (agent knows)
  - How to gather requirements (agent knows)
```

**Prompt to agent**:
```
Gather requirements and define success criteria for this non-technical task.

TASK DESCRIPTION:
[User's original task description from Phase 0]

PHASE 0 UNDERSTANDING:
[Task type, key elements, constraints from Phase 0]

YOUR TASK:
1. Identify detailed requirements (functional and non-functional)
2. Define success criteria (what makes this task "done")
3. List constraints (time, format, audience, style, length)
4. Capture context (background info, purpose, goals)

CRITICAL: At end, provide EXECUTIVE SUMMARY (max 300 lines) with:
- Requirements (key points only)
- Success criteria (how to validate)
- Constraints (critical boundaries)
- Context (essential background)

Output format: YAML structure
```

**After agent completes**:

Present agent output, then apply clarifying questions pattern:
```
Let me verify my understanding:
[2-3 sentence paraphrase of requirements + success criteria]

Clarifying questions:
1. [Question about requirement completeness]
2. [Question about success criteria clarity]
3. [Question about missing constraints]
4. [Question about context sufficiency]
5. [Question about priorities among requirements]

Does this match exactly what you want? If not, what should I adjust?
```

Wait for confirmation, then: "Ready to proceed? (continue/skip/back/stop)"

---

### Phase 2: Solution Design

**Agent**: general-purpose

**Purpose**: Design solution approach and structure

**Sufficient context for quality**:
```yaml
Input needed:
  - Requirements (from Phase 1 executive summary - max 300 lines)
  - Success criteria (how to validate deliverable)
  - Constraints (format, length, style boundaries)
  - Context (purpose, goals, background)

NOT needed:
  - Full Phase 1 YAML output (use compressed executive summary)
  - Generic design theory (agent knows)
  - Detailed user stories (agent needs conclusions)
```

**Prompt to agent**:
```
Design solution approach and structure for this non-technical task.

REQUIREMENTS (from Phase 1):
[Executive summary from Phase 1: requirements, success criteria, constraints, context]

YOUR TASK:
1. Design overall structure (sections, flow, organization)
2. Define key decisions (approach, style, tone, format choices)
3. Provide implementation guidance (what to include in each section)
4. List integration points (if connecting to existing materials)

CRITICAL: At end, provide EXECUTIVE SUMMARY (max 300 lines) with:
- Structure (sections, flow)
- Key Decisions (approach chosen + WHY)
- Implementation Guidance (what goes where)
- Integration Points (connections to existing work)

Output format: YAML structure
```

**After agent completes**:

Present agent output, then apply clarifying questions pattern:
```
Let me verify my understanding:
[2-3 sentence paraphrase of design approach + structure]

Clarifying questions:
1. [Question about structure completeness]
2. [Question about approach suitability]
3. [Question about missing design elements]
4. [Question about implementation clarity]
5. [Question about integration feasibility]

Does this match exactly what you want? If not, what should I adjust?
```

Wait for confirmation, then: "Ready to proceed? (continue/skip/back/stop)"

---

### Phase 3: Implementation

**Execution**: Orchestrator inline

**Purpose**: Create deliverable files based on design

**Sufficient context for quality**:
```yaml
Input needed:
  - Design structure (from Phase 2 executive summary)
  - Key decisions (approach, style, tone)
  - Implementation guidance (what to include)
  - Requirements (from Phase 1 executive summary - for reference)

NOT needed:
  - Full Phase 1/2 YAML outputs (use compressed summaries)
  - Generic content creation theory (you know)
```

**Task**:
1. Create deliverable files following Phase 2 design structure
2. Apply key decisions (style, tone, approach from Phase 2)
3. Follow implementation guidance (Phase 2)
4. Ensure requirements met (Phase 1)

**Output**: Created files with clear file paths

**After implementation**:

Present created files and paths, then apply clarifying questions pattern:
```
Let me verify my understanding:
[2-3 sentence paraphrase of what was created]

Clarifying questions:
1. [Question about content completeness]
2. [Question about structure adherence]
3. [Question about missing elements]
4. [Question about format correctness]
5. [Question about requirement coverage]

Does this match exactly what you want? If not, what should I adjust?
```

Wait for confirmation, then: "Ready to proceed? (continue/skip/back/stop)"

---

### Phase 4: Verification

**Execution**: Orchestrator inline

**Purpose**: Verify deliverable meets requirements and follows design

**Sufficient context for quality**:
```yaml
Input needed:
  - Deliverable files (from Phase 3)
  - Requirements (from Phase 1 executive summary)
  - Success criteria (from Phase 1)
  - Design structure (from Phase 2 executive summary)

NOT needed:
  - Full Phase 1/2 YAML outputs (use compressed summaries)
  - Generic verification theory (you know)
```

**Verification checks**:
1. **Completeness**: All requirements from Phase 1 addressed
2. **Quality**: Deliverable meets success criteria
3. **Design adherence**: Follows Phase 2 structure and decisions
4. **Format**: Correct file format and organization

**Output format**:
```
VERIFICATION REPORT:

✅ PASS / ❌ FAIL: [Check name]
[Details]

Overall: PASS / FAIL
```

**Refine loop** (if FAIL):
1. Identify issues
2. Offer options:
   - FIX: Apply corrections (return to Phase 3)
   - REDESIGN: Revise design (return to Phase 2)
   - ABORT: Stop command
   - CONTINUE-ANYWAY: Accept with known issues
3. After 3 failures, recommend REDESIGN or ABORT

**Final** (if PASS):
```
═══════════════════════════════════════════════
TASK COMPLETE ✅
═══════════════════════════════════════════════

Deliverable: [file paths]
Verification: PASS

Summary:
[2-3 sentence summary of what was created and validated]
```

---

## Commands

- `continue` - Next phase
- `skip` - Skip current phase
- `back` - Previous phase
- `status` - Show progress
- `stop` - Exit workflow

---

## Sufficient Context Principle

**For each agent, provide:**
- ✅ Critical decisions from previous phases
- ✅ Requirements and success criteria
- ✅ Constraints (format, length, style, audience)
- ✅ Context compression (executive summary max 300 lines)

**Do NOT provide:**
- ❌ Full previous YAML outputs (extract decisions only)
- ❌ Detailed user stories (agent needs requirements)
- ❌ Generic explanations (agent knows)
- ❌ Intermediate analysis (agent needs conclusions)

**Test question**:
> "Can agent produce HIGH QUALITY output with this context alone?"
> If YES → sufficient
> If NO → add missing critical info (not everything)

**Context compression strategy**:
- Agent provides executive summary at end (max 300 lines)
- Orchestrator passes compressed summary to next phase
- Prevents context window bloat from multi-phase execution
