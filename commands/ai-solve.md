---
description: "Universal task executor for non-technical tasks (presentations, planning, research, brainstorming) - Usage: /ai-solve [task description]"
---

# Solve - Universal Task Executor (Non-Technical)

Executes non-technical tasks through 5 phases: Requirements, Solution Design, Implementation (file creation), and Verification. Specialized for presentations, planning, research, and brainstorming tasks.

## Usage

```bash
/ai-solve "Create quarterly roadmap presentation"
/ai-solve "Research market trends for product planning"
/ai-solve "Design team retrospective structure"
```

## Phases

```
0: Quick Analysis              (orchestrator - inline assessment + clarifying questions)
1: Requirements & Success      (general-purpose agent - requirements + success criteria)
2: Solution Design             (general-purpose agent - structure + approach)
3: Implementation              (orchestrator - inline file creation)
4: Verification                (orchestrator - inline quality check)
```

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

1. **Clarifying questions before EVERY phase** - Paraphrase + 3-5 questions (scale with complexity) BEFORE Phase 1, 2, 3, 4 (mandatory approval points)
2. **INVOKE with Task tool** - Phases 1-2 require actual Task tool call to general-purpose agent
3. **Context compression** - Agent provides executive summary at end (max 300 lines for next phase)
4. **User approval required** - Get explicit confirmation after clarifying questions before proceeding
5. **Track phase** - Remember current position (user can skip/back)

### Clarifying Questions Pattern (MANDATORY)

**After EVERY phase (including Phase 0), you MUST:**

```
Let me verify my understanding:
[2-3 sentence paraphrase of what was produced/decided in this phase]

Clarifying questions (3-5, scale with task complexity):
1. [Question about scope/constraint from this phase]
2. [Question about edge case/requirement]
3. [Question about priority/approach]
[4. Optional: Question about integration point]
[5. Optional: Question about validation criteria]

Does this match exactly what you want to achieve? If not, what should I adjust?
```

**Wait for user response.** If user says corrections needed:
- Apply corrections
- Paraphrase updated understanding
- Ask 3-5 NEW clarifying questions about updated version
- Repeat until user confirms "dokładnie to co chcę" / "exactly what I want"

**Only after confirmation**, proceed with: "Ready to proceed? (continue/skip/back/stop)"

---

## Phase Details

### Phase 0: Quick Analysis

**Execution**: Orchestrator inline

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

Apply clarifying questions pattern, then: "Ready to proceed? (continue/skip/back/stop)"

---

### Phase 1: Requirements & Success Criteria

**Agent**: general-purpose

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

Present agent output, apply clarifying questions pattern, then: "Ready to proceed? (continue/skip/back/stop)"

---

### Phase 2: Solution Design

**Agent**: general-purpose

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

Present agent output, apply clarifying questions pattern, then: "Ready to proceed? (continue/skip/back/stop)"

---

### Phase 3: Implementation

**Execution**: Orchestrator inline

**Task**:
1. Create deliverable files following Phase 2 design structure
2. Apply key decisions (style, tone, approach from Phase 2)
3. Follow implementation guidance (Phase 2)
4. Ensure requirements met (Phase 1)

**Output**: Created files with clear file paths

Present created files and paths, apply clarifying questions pattern, then: "Ready to proceed? (continue/skip/back/stop)"

---

### Phase 4: Verification

**Execution**: Orchestrator inline

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
