---
description: "Intelligent command management - create, audit, or modify multi-phase commands based on natural language"
---

# Manage Commands - Intelligent Command Management

Automatically detects intent from natural language and executes appropriate command management task: CREATE new multi-phase commands, AUDIT existing commands for compliance, or MODIFY commands to fix issues.

## Phases (Adaptive)

**CREATE Mode:**
```
0: Intent Detection + Complexity    (orchestrator - inline + clarifying questions)
1: Requirements Gathering            (claude-manager with command-creation skill)
2: Plan Creation                     (claude-manager with command-creation skill)
3: File Creation                     (orchestrator - inline)
4: Verification                      (orchestrator - inline + clarifying questions)
```

**AUDIT Mode:**
```
0: Intent Detection + Scope          (orchestrator - inline + clarifying questions)
1: Structure Analysis                (claude-manager with command-creation, signal-vs-noise skills)
2: Content Audit                     (claude-manager with signal-vs-noise skill)
3: Recommendations                   (claude-manager with command-creation skill)
4: Implementation                    (orchestrator - inline if user approves)
```

**MODIFY Mode (Dynamic):**
```
0: Intent Detection + Change Scope   (orchestrator - inline + clarifying questions)
1: Change Analysis                   (claude-manager with command-creation skill)
2: Implementation                    (orchestrator - inline)
3: Verification                      (orchestrator - inline + clarifying questions)
```

---

## Orchestrator Instructions

### ⚠️ CRITICAL: YOU MUST INVOKE AGENTS

**You are the orchestrator.** Your job is to **ACTUALLY INVOKE AGENTS using the Task tool**.

**DO NOT**:
- ❌ Say "I will launch claude-manager"
- ❌ Describe what the agent will do
- ❌ Explain the phase without invoking

**DO**:
- ✅ Immediately invoke Task tool with agent
- ✅ Use subagent_type="claude-manager", description, prompt parameters
- ✅ Wait for agent completion
- ✅ Show results to user

**Example**:
```
Phase 1/4: Requirements Gathering
Launching claude-manager...
```
[IMMEDIATELY invoke Task tool NOW with subagent_type="claude-manager"]

### Critical Rules

1. **INVOKE with Task tool** - Every phase requires actual Task tool call (except Phase 0 and inline phases)
2. **Sufficient context** - Each claude-manager invocation gets ONLY critical decisions (not full conversation history)
3. **Clarifying questions MANDATORY** - After Phase 0 and EVERY agent phase, paraphrase + 3-5 questions (scale with complexity) + confirmation
4. **User checkpoints** - Get approval after confirmation before proceeding
5. **Track phase** - Remember current position and mode (CREATE/AUDIT/MODIFY)
6. **Skill loading mechanism** - Agent sees ONLY skill metadata/description before deciding which skills to load. Full skill content loads only after agent's decision. Therefore: (1) skill descriptions must precisely describe WHEN to use (not "I help with X"), (2) command prompts should contain descriptive keywords matching skill descriptions (not explicit skill names - avoids tight coupling), (3) critical rules must be in command and agent system prompt - never rely solely on skills for enforcement.
7. **NEVER INVENT CONTENT** - claude-manager must NEVER make up metrics, production incidents, anti-patterns, or numbers. ONLY use user-provided data.
8. **AVOID AI-KNOWN CONTENT** - claude-manager must NOT include generic multi-phase patterns Claude already knows. Focus on project-specific command design, sufficient context principles, and orchestration decisions with WHY context. Example: ❌ "Commands orchestrate multiple agents across phases" → ✅ "Extract decisions only (50 lines), not full conversation (500 lines) - agents have isolated context"

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
  CREATE: [command name from request or ask]
  AUDIT: [specific command or "all"]
  MODIFY: [command name + changes requested]

Confidence: [HIGH / MEDIUM / LOW]
```

**Step 4: If Confidence LOW - Ask Clarifying Questions**

```
Let me verify my understanding:
[2-3 sentence paraphrase of detected intent]

Clarifying questions (3-5, scale with complexity):
1. Intent: Should I [CREATE new / AUDIT existing / MODIFY existing] command?
2. Scope: Which command - [detected name or list options]?
3. Goal: What's the primary objective - [inferred goal]?
[4. Priority: What's most important - [structure / content / both]?]
[5. Action: Should I [specific action] or did you mean [alternative]?]

Does this match exactly what you want? If not, what should I adjust?
```

[WAIT for confirmation]

**Step 5: Proceed to Mode-Specific Phase 0**

- CREATE → Continue to CREATE Mode Phase 0 (Complexity Assessment)
- AUDIT → Continue to AUDIT Mode Phase 0 (Scope Selection)
- MODIFY → Continue to MODIFY Mode Phase 0 (Change Scope)

Ready to proceed? (continue/skip/back/stop)

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

**After Phase 0 - MANDATORY clarifying questions**:

```
Let me verify my understanding:
[2-3 sentence paraphrase of complexity assessment and command type]

Clarifying questions (3-5, scale with complexity):
1. What is the primary goal of this command - [specific outcome]?
2. Should this command handle [edge case A] or is that out of scope?
3. How many phases - simple (1-3), standard (5-6), or complex (8+)?
[4. Which agents should be involved - [list potential agents]?]
[5. What's the success criterion - what makes this command "complete"?]

Does this match exactly what you want? If not, what should I adjust?
```

[WAIT for user confirmation]

Ready to proceed? (continue/skip/back/stop)

---

### Phase 1: Requirements Gathering
**Agent**: claude-manager

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

Task: Gather requirements for new multi-phase command.

Ask clarifying questions to understand:
1. What phases are needed? (based on complexity)
2. Which agents should each phase use?
3. What skills should agents load?
4. What context does each agent need from previous phases?
5. What user checkpoints are needed?

ANY NO = NOISE → Cut immediately.

DO NOT include:
- Generic command theory (orchestration basics)
- Standard phase patterns (AI knows workflow structure)
- Obvious agent usage

Use your command-creation skill for structure patterns.

Output format:
- Phase breakdown (Phase 0, 1, 2, ...)
- Agent assignments per phase
- Skills per agent
- Context flow between phases
```

**After agent**:

```
Let me verify my understanding:
[2-3 sentence paraphrase of phase structure and agent assignments]

Clarifying questions (3-5, scale with complexity):
1. The command has [N] phases - does this match your expectations?
2. Phase [X] uses [agent-name] - is this the right agent for [task]?
3. Should Phase [Y] include [specific context from Phase X], or is that too much?
[4. The command assumes [specific constraint] - is this correct?]
[5. Success criterion: [specific outcome] - does this match your goal?]

Does this match exactly what you want? If not, what should I adjust?
```

[WAIT for confirmation]

Ready to proceed? (continue/skip/back/stop)

---

### Phase 2: Plan Creation
**Agent**: claude-manager

**Prompt to agent**:
```
MODE: CREATE command plan

COMMAND: [name]
COMPLEXITY: [level]

REQUIREMENTS (from Phase 1):
[Extract: phase breakdown, agent assignments, skills, context flow]

USER ADJUSTMENTS (from Phase 1 clarifying questions):
[Extract: any corrections user made during confirmation]

Task: Create complete command plan following command-creation skill structure.

Plan must include:
1. Frontmatter (description with usage)
2. Phases overview (inline/agent markers)
3. "⚠️ CRITICAL: YOU MUST INVOKE AGENTS" section
4. Critical Rules (including clarifying questions requirement: 3-5 scaled to complexity)
5. Phase Details with agent prompts and clarifying questions after each phase
6. Commands section

Apply Signal vs Noise: No generic orchestration, only project-specific command design.

Apply command structure template and sufficient context patterns.

Output: Complete command plan (markdown structure)
```

**After agent**:

```
Let me verify my understanding:
[2-3 sentence paraphrase of command structure and key sections]

Clarifying questions (3-5, scale with complexity):
1. The "Sufficient context" for Phase [X] includes [context items] - sufficient for quality output?
2. Should Phase [Y] include clarifying questions about [specific aspect]?
3. The command forces Task invocation with "⚠️ CRITICAL" section - does this address your needs?
[4. Phases [X, Y] have user checkpoints - are there other phases needing checkpoints?]
[5. Any additional sections needed beyond the plan?]

Does this match exactly what you want? If not, what should I adjust?
```

[WAIT for confirmation]

Ready to proceed? (continue/skip/back/stop)

---

### Phase 3: File Creation (Inline)
**You do this - no agent**

Create command file at `.claude/commands/[command-name].md`:

1. Use plan from Phase 2
2. Apply command-creation skill structure
3. Include all required sections
4. Verify frontmatter format
5. Create file

No clarifying questions (file creation is mechanical based on approved plan).

Ready to proceed? (continue/skip/back/stop)

---

### Phase 4: Verification (Inline)
**You do this - no agent**

Verify command file against checklist:

```yaml
Structure:
  - [ ] Description in frontmatter (<200 chars)
  - [ ] Phases overview (inline/agent markers)
  - [ ] "⚠️ CRITICAL" section present
  - [ ] Critical Rules (includes clarifying questions 3-5)
  - [ ] Phase Details with agent prompts
  - [ ] Clarifying questions after EVERY agent phase
  - [ ] Commands section

Content:
  - [ ] Phase 0 inline
  - [ ] User checkpoints after confirmation
  - [ ] No full YAML outputs in context sections
  - [ ] Signal-focused (no generic orchestration content)
```

**Output**: Verification results

```
Let me verify my understanding:
[2-3 sentence paraphrase of verification results]

Clarifying questions (3-5, scale with complexity):
1. Verification found [N] issues - fix automatically or show you first?
2. Missing section [X] - add now or optional for this command?
3. "Sufficient context" for Phase [Y] seems [too verbose/too sparse] - adjust?
[4. Should I create example skills/agents referenced in command, or assume they exist?]
[5. Command ready at [path] - review before use?]

Does this match your expectations?
```

[WAIT for confirmation]

Command complete!

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

**After Phase 0 - MANDATORY clarifying questions**:

```
Let me verify my understanding:
[2-3 sentence paraphrase of audit scope]

Clarifying questions (3-5, scale with complexity):
1. Should I audit [N] commands found, or exclude some?
2. Priority focus - structure compliance, WHY over HOW, or signal vs noise?
3. If issues found, should I auto-fix or just report?
[4. Should audit check for missing clarifying questions pattern?]
[5. Success criterion - all commands compliant, or report only?]

Does this match what you want?
```

[WAIT for confirmation]

Ready to proceed? (continue/skip/back/stop)

---

### Phase 1: Structure Analysis
**Agent**: claude-manager

**Prompt to agent**:
```
MODE: AUDIT commands (structure compliance)

COMMANDS: [list from Phase 0]
FOCUS: [structure/WHY/signal-noise/all]
PRIORITY: [from user]

Task: Analyze command structure compliance.

For each command, check:

1. **Required sections present?**
   - [ ] Description in frontmatter
   - [ ] Phases overview
   - [ ] "⚠️ CRITICAL: YOU MUST INVOKE AGENTS" section
   - [ ] Critical Rules (includes clarifying questions requirement)
   - [ ] Phase Details with agent prompts
   - [ ] Clarifying questions after EVERY agent phase
   - [ ] Commands section

2. **Phase 0 inline?** (not agent)

3. **Clarifying questions pattern present?**
   - After Phase 0
   - After EVERY agent phase
   - Paraphrase + 3-5 questions + confirmation
   - Commands offered AFTER confirmation (not before)

4. **User checkpoints present?** (continue/skip/back/stop)

Apply command structure patterns and multi-phase orchestration reference.

Output format:
Per-command report:
- Command name
- Missing sections (list)
- Issues found (specific)
- Severity: critical/moderate/minor
```

**After agent**:

```
Let me verify my understanding:
[2-3 sentence paraphrase of compliance results]

Clarifying questions (3-5, scale with complexity):
1. Found [N] commands with missing sections - fix or just report?
2. Command [X] missing "Clarifying Questions Pattern" - critical or optional?
3. Some commands have Phase 0 as agent (should be inline) - auto-fix?
[4. Priority for fixes: [missing sections / wrong structure / content quality]?]
[5. Proceed to content audit (Phase 2) or fix structure issues first?]

Does this match your expectations?
```

[WAIT for confirmation]

Ready to proceed? (continue/skip/back/stop)

---

### Phase 2: Content Audit (WHY over HOW, Signal vs Noise)
**Agent**: claude-manager

**Prompt to agent**:
```
MODE: AUDIT commands (content quality)

⚠️ CRITICAL: FLAG INVENTED CONTENT
Flag invented metrics/incidents for removal. Recommend placeholders or deletion.

COMMANDS: [list]
STRUCTURE RESULTS: [from Phase 1 - which commands passed/failed]
USER DECISIONS: [auto-fix or report, priorities]

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

**After agent**:

```
Let me verify my understanding:
[2-3 sentence paraphrase of violations found]

Clarifying questions (3-5, scale with complexity):
1. Found [N] WHY over HOW violations - should domain knowledge move to skills?
2. Command [X] passes full YAML in context - extract to [specific decisions]?
3. Some commands missing production context - add placeholder or skip?
[4. Priority: Fix critical violations first, or all?]
[5. Create skills for domain knowledge found in commands?]

Does this match your expectations?
```

[WAIT for confirmation]

Ready to proceed? (continue/skip/back/stop)

---

### Phase 3: Recommendations
**Agent**: claude-manager

**Prompt to agent**:
```
MODE: AUDIT recommendations

STRUCTURE RESULTS: [Phase 1 - missing sections, issues]
CONTENT RESULTS: [Phase 2 - violations found]
USER DECISIONS: [priorities, preferences]

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

**After agent**:

```
Let me verify my understanding:
[2-3 sentence paraphrase of recommended changes]

Clarifying questions (3-5, scale with complexity):
1. Recommendations suggest creating [N] new skills - do this in Phase 4?
2. Priority order: [command A] → [command B] - correct?
3. Some fixes require breaking changes - proceed anyway?
[4. Handle skill extraction as part of this audit, or separate?]
[5. Implement all recommendations or just critical ones?]

Does this match your expectations?
```

[WAIT for confirmation]

Ready to proceed with implementation? (continue/skip/back/stop)

---

### Phase 4: Implementation (Inline - Conditional)
**You do this - no agent**

**Only if user approved in Phase 3.**

Apply recommended changes:

1. **Create new artifacts first** (skills, agents)
2. **Fix structure issues** (add missing sections)
3. **Refactor content** (extract to skills, simplify context)
4. **Add WHY context** (production incidents, rationale)
5. **Verify each command** (run checklist from Phase 4 CREATE)

Track progress:
```
Fixed: [command]
- [violation] → [fix]
Progress: [N/M] complete
```

```
Let me verify my understanding:
[2-3 sentence paraphrase of changes made]

Clarifying questions (3-5, scale with complexity):
1. Made [N] changes to [M] commands - commit these?
2. Created [X] new skills - correct location (.claude/skills/)?
3. Some commands still have minor issues [list] - fix now or later?
[4. Create pull request or just local commit?]
[5. Verification passed for [N] commands - what about remaining [M]?]

Does this match your expectations?
```

[WAIT for confirmation]

Audit complete!

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
  compliance: Fix missing requirements (clarifying questions, sufficient context)
```

**After Phase 0 - MANDATORY clarifying questions**:

```
Let me verify my understanding:
[2-3 sentence paraphrase of changes to make]

Clarifying questions (3-5, scale with complexity):
1. Scope: Changes affect [specific sections] or entire command?
2. Priority: What's most important - [change A] or [change B]?
3. Approach: [approach A] or [approach B] for [specific change]?
[4. Verification: After changes, full checklist or just changed sections?]
[5. Backup: Create backup of original or just proceed?]

Does this match exactly what you want?
```

[WAIT for confirmation]

Ready to proceed? (continue/skip/back/stop)

---

### Phase 1: Change Analysis
**Agent**: claude-manager

**Prompt to agent**:
```
MODE: MODIFY command

COMMAND: [name and path]
CHANGES REQUESTED: [from Phase 0]
USER ADJUSTMENTS: [from Phase 0 clarifying questions]

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

**After agent**:

```
Let me verify my understanding:
[2-3 sentence paraphrase of change plan]

Clarifying questions (3-5, scale with complexity):
1. Plan suggests [N] modifications - complete or should I add [X]?
2. Change order: [A] → [B] → [C] - correct priority?
3. Section [X] will be [modified/removed/added] - is this what you want?
[4. Approach for [specific change]: [description] - does this make sense?]
[5. After changes, command will [outcome] - matches your goal?]

Does this match exactly what you want?
```

[WAIT for confirmation]

Ready to proceed? (continue/skip/back/stop)

---

### Phase 2: Implementation (Inline)
**You do this - no agent**

Apply modifications from Phase 1 plan:

```yaml
Structural changes:
  - Add sections (use command-creation template)
  - Remove sections
  - Reorder sections (maintain logical flow)

Content changes:
  - Update patterns (apply signal-vs-noise)
  - Add WHY explanations (production context)
  - Fix examples
  - Simplify context sections (extract decisions)

Compliance fixes:
  - Add clarifying questions pattern (if missing)
  - Add "⚠️ CRITICAL" section (if missing)
  - Fix Phase 0 (make inline if agent)
```

No clarifying questions (implementation is mechanical based on approved plan).

Ready to proceed? (continue/skip/back/stop)

---

### Phase 3: Verification (Inline)
**You do this - no agent**

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
  - [ ] Clarifying questions after EVERY agent phase
  - [ ] Phase 0 inline
  - [ ] User checkpoints after confirmation

Quality:
  - [ ] Signal-focused (no generic content)
  - [ ] Sufficient (critical info, not exhaustive)
```

```
Let me verify my understanding:
[2-3 sentence paraphrase of changes and verification status]

Clarifying questions (3-5, scale with complexity):
1. Made [N] changes to [sections] - all correct?
2. Verification found [N] issues - fix automatically or show you?
3. Modified command ready at [path] - commit or review first?
[4. Changes improve [aspect] - does this achieve your goal?]
[5. Test command by running it, or just structural verification?]

Does this match your expectations?
```

[WAIT for confirmation]

Modification complete!

---

## Commands

- `continue` - Next phase
- `skip` - Skip current phase
- `back` - Previous phase
- `status` - Show progress (current phase, mode)
- `stop` - Exit command
