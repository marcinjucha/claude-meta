---
description: "Intelligent command management - create, audit, or modify multi-phase commands based on natural language"
---

# Manage Commands - Intelligent Command Management

Automatically detects intent from natural language and executes appropriate command management task: CREATE new multi-phase commands, AUDIT existing commands for compliance, or MODIFY commands to fix issues.

## Phases (Adaptive)

Phases are a checklist, not separate stops: merge them into as few ai-manager-agent spawns as the context allows.

**CREATE Mode:**
```
0: Intent Detection + Complexity    (orchestrator - inline)
1: Requirements Gathering            (ai-manager-agent with ai-command-creation skill)
2: Plan Creation = PLAN              (ai-manager-agent with ai-command-creation skill) → user approval
3: File Creation                     (ai-manager-agent — creates command file)
4: Verification                      (orchestrator - inline, read-only)
```

**AUDIT Mode:**
```
0: Intent Detection + Scope          (orchestrator - inline)
1: Structure Analysis                (ai-manager-agent with ai-command-creation skill)
2: Content Audit                     (ai-manager-agent with signal-vs-noise shared resource)
3: Recommendations = PLAN            (ai-manager-agent with ai-command-creation skill) → user approval
4: Implementation                    (ai-manager-agent — applies approved fixes)
```

**MODIFY Mode (Dynamic):**
```
0: Intent Detection + Change Scope   (orchestrator - inline)
1: Change Analysis = PLAN            (ai-manager-agent with ai-command-creation skill) → user approval
2: Implementation                    (ai-manager-agent — applies approved changes)
3: Verification                      (orchestrator - inline, read-only)
```

---

## Orchestrator Instructions

### ⚠️ CRITICAL: YOU MUST INVOKE AGENTS

**You are the orchestrator.** Your job is to **ACTUALLY INVOKE AGENTS using the Task tool**.

**DO NOT**:
- ❌ Say "I will launch ai-manager-agent"
- ❌ Describe what the agent will do
- ❌ Explain the phase without invoking

**DO**:
- ✅ Immediately invoke Task tool with agent
- ✅ Use subagent_type="ai-manager-agent", description, prompt parameters
- ✅ Wait for agent completion
- ✅ Show results to user

**Example**:
```
Phase 1/4: Requirements Gathering
Launching ai-manager-agent...
```
[IMMEDIATELY invoke Task tool NOW with subagent_type="ai-manager-agent"]

### Critical Rules

1. **INVOKE with Task tool** - Every phase requires actual Task tool call (except Phase 0 and Verification which are inline). Implementation/File Creation phases MUST use ai-manager-agent — never do file edits inline. Inline Verification is read-only: any fix it finds goes back to ai-manager-agent, not into an inline Edit/Write.
2. **Sufficient context** - Each ai-manager-agent invocation gets ONLY critical decisions (not full conversation history)
3. **Ask once, only about assumptions; one consent point** - Ask the user in ONE message, and only when you are assuming something about scope, location (claude-dev / brain-vault/.claude / ~/.claude / the source of a symlink) or what the change applies to; otherwise merge phases and act. The only gate: present the plan → user approves (an approval already given in the request counts) → ai-manager-agent writes. **Why:** the old per-phase questions/paraphrase/gate ceremony ran in zero observed sessions, and Marcin's rule is "decide yourself, ask only about assumptions".
4. **Track mode** - Remember mode (CREATE/AUDIT/MODIFY) and what is already done
5. **Skill loading mechanism** - Agent sees ONLY skill metadata/description before deciding which skills to load. Full skill content loads only after agent's decision. Therefore: (1) skill descriptions must precisely describe WHEN to use (not "I help with X"), (2) command prompts should contain descriptive keywords matching skill descriptions (not explicit skill names - avoids tight coupling), (3) critical rules must be in command and agent system prompt - never rely solely on skills for enforcement.
6. **NEVER INVENT CONTENT** - ai-manager-agent must NEVER make up metrics, production incidents, anti-patterns, or numbers. ONLY use user-provided data.
7. **AVOID AI-KNOWN CONTENT** - ai-manager-agent must NOT include generic multi-phase patterns Claude already knows. Focus on project-specific command design, sufficient context principles, and orchestration decisions with WHY context. Example: ❌ "Commands orchestrate multiple agents across phases" → ✅ "Extract decisions only (50 lines), not full conversation (500 lines) - agents have isolated context"

---

## Phase Details - Intent Detection (Universal Phase 0)

### Phase 0: Intent Detection and Mode Selection (Inline)
**You do this - no agent**

**Step 1: Detect Intent**

```yaml
CREATE indicators:
  - "create" / "new" / "need command"
  - "command for [new functionality]"
  - Request describes functionality NOT in existing commands

AUDIT indicators:
  - "check" / "verify" / "audit" / "validate"
  - "meets requirements" / "compliant" / "follows patterns"
  - References EXISTING command name + quality check
  - "all commands" (audit scope)

MODIFY indicators:
  - "update" / "fix" / "modify" / "change"
  - "add [section]" / "remove [section]" / "improve"
  - References EXISTING command name + specific change
  - "missing [feature]" / "[command] should have"

Ambiguous:
  - Multiple indicators present
  - Unclear command reference
  - No clear action verb
```

**Step 2: List Existing Commands (if needed for AUDIT/MODIFY)**

```bash
ls .claude/commands/*.md
```

**Step 3: Determine Mode and Scope**

```yaml
Mode: [CREATE / AUDIT / MODIFY]

Scope:
  CREATE: [command name from request]
  AUDIT: [specific command or "all"]
  MODIFY: [command name + changes requested]

Location: [claude-dev / brain-vault/.claude / ~/.claude / source of a symlink]
```

**Step 4:** If mode, scope, location or target is an assumption rather than something the request states, ask about it in ONE message (Critical Rule 3). Otherwise go straight to the mode's phases.

---

## Phase Details - CREATE Mode

### Phase 0: Complexity Assessment (Inline)
**You do this - no agent**

Assess command complexity:

```yaml
COMPLEXITY:
  simple: 1-3 phases (single task)
  standard: 5-6 phases (feature development)
  complex: 8+ phases (granular control)

COMMAND_TYPE:
  feature: Full feature implementation
  debug: Bug investigation and fix
  validation: Pre-merge checks (parallel)
  refactor: Code restructuring
```

---

### Phase 1: Requirements Gathering
**Agent**: ai-manager-agent (may be merged with Phase 2 into one spawn)

**Prompt to agent**:
```
MODE: CREATE command

⚠️ CRITICAL: NEVER INVENT OR HALLUCINATE CONTENT
- DO NOT make up metrics, numbers, or production incidents
- DO NOT invent anti-patterns without user-provided examples
- ONLY extract what user actually provided
- If no production data exists, use placeholder: [User to provide real metric/incident]

COMMAND NAME: [name]
COMPLEXITY: [simple/standard/complex from Phase 0]
TYPE: [feature/debug/validation/refactor]
PURPOSE: [user's description]
EXPECTED PHASES: [number from Phase 0]

Task: Gather requirements for new multi-phase command. Determine:
1. What phases are needed? (based on complexity)
2. Which agents should each phase use?
3. What skills should agents load?
4. What context does each agent need from previous phases?
5. Where the single consent point sits (plan → approval → write), and which assumptions (scope, location, target) the command must ask about up front
6. Does any phase do deterministic work (parse/extract/filter/count/reshape) over a long/large input? If so, prefer having it run a `scripts/` helper that returns ONLY the relevant slice over spawning an agent to load the whole input into context. WHY: cheaper, faster, more reliable signal-finding in long documents, and it preserves the phase's context budget for decisions. BOUNDARY: deterministic work only — judgment/synthesis stays with the agent; do NOT script what needs the model to think.

ANY NO = NOISE → Cut immediately.

DO NOT include:
- Generic command theory (orchestration basics)
- Standard phase patterns (AI knows workflow structure)
- Obvious agent usage

Use your ai-command-creation skill for structure patterns.

Output format:
- Phase breakdown (Phase 0, 1, 2, ...)
- Agent assignments per phase
- Skills per agent
- Context flow between phases
```

---

### Phase 2: Plan Creation (the plan)
**Agent**: ai-manager-agent

**Prompt to agent**:
```
MODE: CREATE command plan

COMMAND: [name]
COMPLEXITY: [level]

REQUIREMENTS (from Phase 1):
[Extract: phase breakdown, agent assignments, skills, context flow]

Task: Create complete command plan following ai-command-creation skill structure.

Plan must include:
1. Frontmatter (description with usage)
2. Phases overview (inline/agent markers)
3. "⚠️ CRITICAL: YOU MUST INVOKE AGENTS" section
4. Critical Rules (including the ask-once rule and the single consent point)
5. Phase Details with agent prompts and sufficient context per phase

Apply Signal vs Noise: No generic orchestration, only project-specific command design.

Apply command structure template and sufficient context patterns.

Output: Complete command plan (markdown structure)
```

**Consent point:** show the plan (target path + structure) and wait for approval before Phase 3.

---

### Phase 3: File Creation (ai-manager-agent)
**Agent**: ai-manager-agent

**Prompt to agent:**
```
MODE: CREATE command file

COMMAND: [name]
FILE PATH: .claude/commands/[command-name].md

APPROVED PLAN (from Phase 2):
[Full command plan markdown]

USER ADJUSTMENTS (from plan approval):
[Any corrections user made]

Task: Create the command file using the approved plan.

1. Write file at the specified path
2. Apply ai-command-creation skill structure
3. Include all required sections from the plan
4. Verify frontmatter format is correct

Output: Confirm file created, show file path.
```

---

### Phase 4: Verification (Inline)
**You do this - no agent (read-only).** Read the file and run the checklist. If fixes are needed, spawn ai-manager-agent with the issue list (MODE: CREATE command file - fixes) — never Edit/Write the command file yourself.

```yaml
Structure:
  - [ ] Description in frontmatter (<200 chars)
  - [ ] Phases overview (inline/agent markers)
  - [ ] "⚠️ CRITICAL" section present
  - [ ] Critical Rules (includes the ask-once rule + single consent point)
  - [ ] Phase Details with agent prompts

Content:
  - [ ] Phase 0 inline
  - [ ] Exactly one consent point before writes; no per-phase question blocks or continue/skip footer
  - [ ] No full YAML outputs in context sections
  - [ ] Signal-focused (no generic orchestration content)
```

Report the result (path, issues fixed or open). Command complete.

---

## Phase Details - AUDIT Mode

### Phase 0: Scope Selection (Inline)
**You do this - no agent**

```yaml
SCOPE:
  specific: User provided command name
  all: Audit all commands in .claude/commands/

COMMANDS_FOUND:
  - List command files
  - Check each has frontmatter
  - Note any structural issues visible
```

---

### Phase 1: Structure Analysis
**Agent**: ai-manager-agent (Phases 1-3 may run as one spawn)

**Prompt to agent**:
```
MODE: AUDIT commands (structure compliance)

COMMANDS: [list from Phase 0]
FOCUS: [structure/WHY/signal-noise/all]

Task: Analyze command structure compliance.

For each command, check:

1. **Required sections present?**
   - [ ] Description in frontmatter
   - [ ] Phases overview
   - [ ] "⚠️ CRITICAL: YOU MUST INVOKE AGENTS" section
   - [ ] Critical Rules
   - [ ] Phase Details with agent prompts

2. **Phase 0 inline?** (not agent)

3. **Question flow:** asks only about assumptions (scope, location, target) in one message, and has exactly one consent point (plan → approval → write). Flag per-phase question blocks, paraphrase loops, self-reflection gates and continue/skip footers as noise to remove.

Apply command structure patterns and multi-phase orchestration reference.

Output format:
Per-command report:
- Command name
- Missing sections (list)
- Issues found (specific)
- Severity: critical/moderate/minor
```

---

### Phase 2: Content Audit (WHY over HOW, Signal vs Noise)
**Agent**: ai-manager-agent

**Prompt to agent**:
```
MODE: AUDIT commands (content quality)

⚠️ CRITICAL: FLAG INVENTED CONTENT
Flag invented metrics/incidents for removal. Recommend placeholders or deletion.

COMMANDS: [list]
STRUCTURE RESULTS: [from Phase 1 - which commands passed/failed]

Task: Audit command content for WHY over HOW and Signal vs Noise violations.

Apply "ANY NO = NOISE" to existing command content.

For each command, check:

1. **WHY over HOW violations:**
   - Does command explain domain patterns? (should reference skill)
   - Does command include implementation steps? (should delegate to agent)
   Example: ❌ "BUS architecture uses 4 layers..." → ✅ "Use ios-bus-architecture skill for patterns"

2. **Signal vs Noise violations:**
   - Does "Sufficient context" pass full YAML outputs? (should extract decisions)
   - Does command explain generic concepts? (should be cut)
   Example: ❌ "Input needed: Full requirements.yaml (500 lines)" → ✅ "Input needed: Critical decisions (architecture, constraints)"

3. **Missing WHY context:**
   - Patterns without rationale
   - Rules without explanation

Apply signal vs noise 3-question filter (actionable, impactful, non-obvious).

Output per command:
- WHY over HOW violations (quote, issue, fix)
- Signal vs Noise violations (quote, issue, fix)
- Missing WHY context (list)
- Severity: critical/moderate/minor
```

---

### Phase 3: Recommendations (the plan)
**Agent**: ai-manager-agent

**Prompt to agent**:
```
MODE: AUDIT recommendations

STRUCTURE RESULTS: [Phase 1 - missing sections, issues]
CONTENT RESULTS: [Phase 2 - violations found]

Task: Create actionable recommendations for command improvements.

For each command with issues:

1. **Structure fixes** (from Phase 1) - missing sections, wrong patterns, order to apply
2. **Content refactoring** (from Phase 2) - domain knowledge to extract to skills, context sections to simplify, WHY to add
3. **New artifacts needed** - skills to create, agents to create
4. **Migration plan** - priority order (critical first), dependencies (skill before command)

Apply command structure and orchestration patterns.

Output per command:
- Priority (critical/high/medium/low)
- Structure fixes (specific)
- Content refactoring (specific)
- New artifacts (list)
- Migration steps (ordered)
```

**Consent point:** show the recommendations and wait for approval (all, or which items) before Phase 4.

---

### Phase 4: Implementation (ai-manager-agent)
**Agent**: ai-manager-agent

**Only if user approved in Phase 3.**

**Prompt to agent:**
```
MODE: AUDIT implementation

⚠️ CRITICAL: NEVER INVENT OR HALLUCINATE CONTENT

COMMANDS TO FIX: [list from Phase 3]

APPROVED RECOMMENDATIONS:
[Extracted recommendations user approved — per-command fixes]

USER DECISIONS: [scope, priorities from plan approval]

Task: Apply approved fixes to command files.

For each command:
1. Read current file
2. Apply structure fixes (add missing sections)
3. Apply content refactoring (extract to skills, simplify context)
4. Add WHY context where needed
5. Verify changes match approved recommendations

Track progress:
Fixed: [command]
- [violation] → [fix]
Progress: [N/M] complete

Output: Summary of all changes made, per file.
```

Report the changes. Audit complete.

---

## Phase Details - MODIFY Mode

### Phase 0: Change Scope (Inline)
**You do this - no agent**

```yaml
COMMAND: [name from Universal Phase 0]
CHANGES_REQUESTED: [from user's natural language]

CHANGE_CATEGORIES:
  structure: Add/remove/reorder sections
  content: Update patterns, add WHY, fix examples
  quality: Apply signal-vs-noise, improve clarity
  compliance: Fix missing requirements (sufficient context, single consent point)
```

---

### Phase 1: Change Analysis (the plan)
**Agent**: ai-manager-agent

**Prompt to agent**:
```
MODE: MODIFY command

COMMAND: [name and path]
CHANGES REQUESTED: [from Phase 0]

Task: Analyze current command and plan modifications.

Read command file and analyze:
1. Current structure (sections present, organization)
2. Requested changes (what needs to change)
3. Impact (what sections affected, dependencies)
4. Approach (how to implement while maintaining quality)

Apply command structure patterns and multi-phase orchestration reference.
Apply signal vs noise filter for content quality.

Output:
- Current state summary
- Change plan (section by section)
- Dependencies
- Implementation steps (ordered)
- Verification checklist
```

**Consent point:** show the change plan and wait for approval before Phase 2.

---

### Phase 2: Implementation (ai-manager-agent)
**Agent**: ai-manager-agent

**Prompt to agent:**
```
MODE: MODIFY command implementation

⚠️ CRITICAL: NEVER INVENT OR HALLUCINATE CONTENT

COMMAND: [name and path]
APPROVED CHANGE PLAN (from Phase 1):
[Extracted: section-by-section changes, implementation steps]

USER ADJUSTMENTS (from plan approval):
[Any corrections user made]

Task: Apply approved modifications to the command file.

1. Read current command file
2. Apply changes per the approved plan:
   - Structural changes (add/remove/reorder sections)
   - Content changes (update patterns, add WHY, fix examples)
   - Compliance fixes (sufficient context, single consent point)
3. Verify changes match approved plan
4. Write updated file

Output: Summary of changes made, section by section.
```

---

### Phase 3: Verification (Inline)
**You do this - no agent (read-only).** Read the file and run the checklist. If fixes are needed, spawn ai-manager-agent with the issue list (MODE: MODIFY command - fixes) — never Edit/Write the command file yourself.

```yaml
Structure:
  - [ ] All required sections present
  - [ ] No broken references
  - [ ] Frontmatter valid

Content:
  - [ ] Changes match approved plan
  - [ ] No new noise introduced
  - [ ] WHY context included (if applicable)

Compliance:
  - [ ] Phase 0 inline
  - [ ] Exactly one consent point before writes

Quality:
  - [ ] Signal-focused (no generic content)
  - [ ] Sufficient (critical info, not exhaustive)
```

Report the result (changes, issues fixed or open). Modification complete.
