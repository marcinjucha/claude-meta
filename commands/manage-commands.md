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

**Speed**: 5-20 min depending on mode and complexity

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
3. **Clarifying questions MANDATORY** - After Phase 0 and EVERY agent phase, paraphrase + 5 questions + confirmation
4. **User checkpoints** - Get approval after confirmation before proceeding
5. **Track phase** - Remember current position and mode (CREATE or AUDIT)
6. **NEVER INVENT CONTENT** - claude-manager must NEVER make up metrics, production incidents, anti-patterns, or numbers. ONLY use user-provided data.

### Phase Execution Pattern

```
═══════════════════════════════════════════════
Phase N/M: [Name]
═══════════════════════════════════════════════

Launching claude-manager...
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

## Phase Details - Intent Detection (Universal Phase 0)

### Phase 0: Intent Detection and Mode Selection (Inline)
**You do this - no agent**

**CRITICAL: Analyze user's natural language request to determine mode.**

**Step 1: Detect Intent**

Analyze request for keywords and context:

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

If AUDIT or MODIFY detected, list commands in `.claude/commands/`:
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

Clarifying questions:
1. Intent: Should I [CREATE new / AUDIT existing / MODIFY existing] command?
2. Scope: Which command - [detected name or list options]?
3. Goal: What's the primary objective - [inferred goal]?
4. Priority: What's most important - [structure / content / both]?
5. Action: Should I [specific action] or did you mean [alternative]?

Does this match exactly what you want? If not, what should I adjust?
```

[WAIT for confirmation]

**Step 5: Proceed to Mode-Specific Phase 0**

Once mode determined with HIGH confidence:
- CREATE → Continue to CREATE Mode Phase 0 (Complexity Assessment)
- AUDIT → Continue to AUDIT Mode Phase 0 (Scope Selection)
- MODIFY → Continue to MODIFY Mode Phase 0 (Change Scope)

Ready to proceed? (continue/skip/back/stop)

---

## Phase Details - CREATE Mode

### Phase 0: Complexity Assessment (Inline)
**You do this - no agent**

**From Universal Phase 0: Mode=CREATE, Command name determined**

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

**Output**: Brief complexity note + command type

**After Phase 0 - MANDATORY clarifying questions**:

```
Let me verify my understanding:
[2-3 sentence paraphrase of complexity assessment and command type]

Clarifying questions:
1. What is the primary goal of this command - [specific outcome]?
2. Should this command handle [edge case A] or is that out of scope?
3. How many phases do you expect - simple (1-3), standard (5-6), or complex (8+)?
4. Which agents should be involved - [list potential agents]?
5. What's the success criterion - what makes this command "complete"?

Does this match exactly what you want? If not, what should I adjust?
```

[WAIT for user confirmation]

Ready to proceed? (continue/skip/back/stop)

---

### Phase 1: Requirements Gathering
**Agent**: claude-manager

**Sufficient context for quality**:
```yaml
Input needed:
  - Mode: CREATE
  - Command name (from user command)
  - Complexity (from Phase 0: simple/standard/complex)
  - Command type (from Phase 0: feature/debug/validation/refactor)
  - User's description of command purpose
  - Number of phases expected (from Phase 0 clarifying questions)

NOT needed:
  - Full conversation history
  - Generic command theory
  - Examples from other commands
```

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

Present requirements clearly.

```
Let me verify my understanding:
[2-3 sentence paraphrase of phase structure and agent assignments]

Clarifying questions:
1. The command has [N] phases - does this match your expectations from Phase 0?
2. Phase [X] uses [agent-name] - is this the right agent for [task]?
3. Should Phase [Y] include [specific context from Phase X], or is that too much?
4. The command assumes [specific constraint] - is this correct?
5. Success criterion for this command: [specific outcome] - does this match your goal?

Does this match exactly what you want? If not, what should I adjust?
```

[WAIT for confirmation]

Ready to proceed? (continue/skip/back/stop)

---

### Phase 2: Plan Creation
**Agent**: claude-manager

**Sufficient context for quality**:
```yaml
Input needed:
  - Requirements (from Phase 1: phase breakdown, agent assignments, skills, context flow)
  - User confirmations/adjustments from Phase 1 clarifying questions
  - Command name
  - Complexity level

NOT needed:
  - Full Phase 1 conversation
  - Generic command examples
  - Detailed user stories
```

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
4. Critical Rules (including clarifying questions requirement)
5. "Clarifying Questions Pattern" section
6. Phase Execution Pattern (with paraphrase + 5 questions template)
7. Phase Details with "Sufficient context for quality" sections
8. Commands section
9. "Sufficient Context Principle" section

Use command-creation skill for structure template.
Apply signal-vs-noise skill to filter context (sufficient, not excessive).
Apply Signal vs Noise: No generic orchestration, only project-specific command design

Output: Complete command plan (markdown structure)
```

**After agent**:

Present plan structure.

```
Let me verify my understanding:
[2-3 sentence paraphrase of command structure and key sections]

Clarifying questions:
1. The "Sufficient context" section for Phase [X] includes [context items] - is this sufficient for quality output?
2. Should Phase [Y] include clarifying questions about [specific aspect]?
3. The command forces Task invocation with "⚠️ CRITICAL" section - does this address your needs?
4. Phases [X, Y] have user checkpoints - are there other phases needing checkpoints?
5. The Sufficient Context Principle test question appears at [location] - does this make sense?

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

**Output**: File created confirmation with path

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
  - [ ] Critical Rules (3-5, includes clarifying questions)
  - [ ] "Clarifying Questions Pattern" section
  - [ ] Phase Execution Pattern (paraphrase + 5 questions)
  - [ ] Each phase has "Sufficient context" section
  - [ ] Commands section
  - [ ] "Sufficient Context Principle" at end

Content:
  - [ ] Phase 0 inline
  - [ ] Clarifying questions after EVERY phase
  - [ ] User checkpoints after confirmation
  - [ ] Test question in Sufficient Context Principle
  - [ ] No full YAML outputs in context sections

Content verification - Signal vs Noise per section:
  - [ ] Phases: No generic "what is a phase"
  - [ ] Critical Rules: Project-specific enforcement only
  - [ ] No standard clarifying questions pattern (AI knows this)
```

**Output**: Verification results + recommendations

```
Let me verify my understanding:
[2-3 sentence paraphrase of verification results]

Clarifying questions:
1. Verification found [N] issues - should I fix these automatically or show you first?
2. Missing section [X] - should this be added now or is it optional for this command?
3. "Sufficient context" section for Phase [Y] seems [too verbose/too sparse] - adjust?
4. Should I create example skills/agents referenced in command, or assume they exist?
5. Command is ready at [path] - should I commit this or do you want to review first?

Does this match your expectations? What should I adjust?
```

[WAIT for confirmation]

Command complete! (or back to fix issues)

---

## Phase Details - AUDIT Mode

### Phase 0: Scope Selection (Inline)
**You do this - no agent**

**From Universal Phase 0: Mode=AUDIT, Scope determined (specific command or "all")**

Determine which commands to audit:

```yaml
SCOPE:
  specific: User provided command name
  all: Audit all commands in .claude/commands/

COMMANDS_FOUND:
  - List command files
  - Check each has frontmatter
  - Note any structural issues visible
```

**Output**: Scope + list of commands to audit

**After Phase 0 - MANDATORY clarifying questions**:

```
Let me verify my understanding:
[2-3 sentence paraphrase of audit scope]

Clarifying questions:
1. Should I audit [N] commands found, or exclude some?
2. Priority focus - structure compliance, WHY over HOW, or signal vs noise?
3. If issues found, should I auto-fix or just report?
4. Should audit check for missing clarifying questions pattern?
5. What's the success criterion - all commands compliant, or report only?

Does this match what you want? If not, what should I adjust?
```

[WAIT for confirmation]

Ready to proceed? (continue/skip/back/stop)

---

### Phase 1: Structure Analysis
**Agent**: claude-manager

**Sufficient context for quality**:
```yaml
Input needed:
  - Mode: AUDIT
  - Commands to audit (names/paths from Phase 0)
  - Audit focus (from Phase 0: structure/WHY/signal-noise/all)
  - User's priority (from clarifying questions)

NOT needed:
  - Full command file contents (agent will read)
  - Generic command theory
  - Conversation history
```

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
   - [ ] "Clarifying Questions Pattern" section
   - [ ] Phase Execution Pattern (paraphrase + 5 questions)
   - [ ] Phase Details with "Sufficient context for quality"
   - [ ] Commands section
   - [ ] "Sufficient Context Principle" section

2. **Phase 0 inline?** (not agent)

3. **Clarifying questions pattern present?**
   - After Phase 0
   - After EVERY agent phase
   - Paraphrase + 5 questions + confirmation
   - Commands offered AFTER confirmation (not before)

4. **User checkpoints present?** (continue/skip/back/stop)

5. **Sufficient context sections present?** (for each agent phase)

Use command-creation skill for structure reference.

Output format:
Per-command report:
- Command name
- Structure compliance score (N/9 required sections)
- Missing sections (list)
- Issues found (specific)
```

**After agent**:

Present structure analysis.

```
Let me verify my understanding:
[2-3 sentence paraphrase of compliance results]

Clarifying questions:
1. Found [N] commands with missing sections - should I fix these or just report?
2. Command [X] missing "Clarifying Questions Pattern" - critical or optional?
3. Some commands have Phase 0 as agent (should be inline) - auto-fix?
4. Priority for fixes: [missing sections / wrong structure / content quality]?
5. Should I proceed to content audit (Phase 2) or fix structure issues first?

Does this match your expectations? What should I adjust?
```

[WAIT for confirmation]

Ready to proceed? (continue/skip/back/stop)

---

### Phase 2: Content Audit (WHY over HOW, Signal vs Noise)
**Agent**: claude-manager

**Sufficient context for quality**:
```yaml
Input needed:
  - Structure analysis results (from Phase 1)
  - User decisions (auto-fix or report, priorities)
  - Commands to audit

NOT needed:
  - Full Phase 1 conversation
  - Generic examples
```

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
   - Does command contain testing patterns? (should reference skill)

   Example violation:
   ```markdown
   ❌ "BUS architecture uses 4 layers..."
   ✅ "Use ios-bus-architecture skill for patterns"
   ```

2. **Signal vs Noise violations:**
   - Does "Sufficient context" pass full YAML outputs? (should extract decisions)
   - Does command explain generic concepts? (should be cut)
   - Does command include user stories? (should extract requirements)

   Example violation:
   ```markdown
   ❌ Input needed: Full requirements.yaml (500 lines)
   ✅ Input needed: Critical decisions (architecture, constraints, patterns)
   ```

3. **Missing WHY context:**
   - Patterns without rationale
   - Decisions without production context
   - Rules without explanation

Use signal-vs-noise skill for 3-question filter.

Output format:
Per-command report:
- Command name
- WHY over HOW violations (quote section, explain issue, suggest fix)
- Signal vs Noise violations (quote section, explain issue, suggest fix)
- Missing WHY context (list sections)
- Severity (critical/moderate/minor)
```

**After agent**:

Present content audit results.

```
Let me verify my understanding:
[2-3 sentence paraphrase of violations found]

Clarifying questions:
1. Found [N] WHY over HOW violations - should domain knowledge move to skills?
2. Command [X] passes full YAML in "Sufficient context" - extract to [specific decisions]?
3. Some commands missing production context - add placeholder or skip?
4. Priority: Fix critical violations first, or all violations?
5. Should I create skills for domain knowledge found in commands?

Does this match your expectations? What should I adjust?
```

[WAIT for confirmation]

Ready to proceed? (continue/skip/back/stop)

---

### Phase 3: Recommendations
**Agent**: claude-manager

**Sufficient context for quality**:
```yaml
Input needed:
  - Structure analysis (Phase 1 results)
  - Content audit (Phase 2 results)
  - User decisions (priorities, auto-fix preferences)

NOT needed:
  - Full audit conversation
  - Generic refactoring theory
```

**Prompt to agent**:
```
MODE: AUDIT recommendations

STRUCTURE RESULTS: [Phase 1 - missing sections, issues]
CONTENT RESULTS: [Phase 2 - violations found]
USER DECISIONS: [priorities, preferences]

Task: Create actionable recommendations for command improvements.

For each command with issues:

1. **Structure fixes** (from Phase 1)
   - Missing sections to add
   - Wrong patterns to fix
   - Order to apply fixes

2. **Content refactoring** (from Phase 2)
   - Domain knowledge to extract to skills
   - Context sections to simplify
   - WHY explanations to add

3. **New artifacts needed**
   - Skills to create (for domain knowledge)
   - Agents to create (if referenced but missing)
   - Supporting files

4. **Migration plan**
   - Priority order (critical first)
   - Dependencies (skill before command)
   - Verification steps

Use command-creation skill for structure guidance.
Use signal-vs-noise skill for filtering decisions.

Output format:
Per-command recommendations:
- Command name
- Priority (critical/high/medium/low)
- Structure fixes (specific)
- Content refactoring (specific)
- New artifacts (list)
- Migration steps (ordered)
```

**After agent**:

Present recommendations.

```
Let me verify my understanding:
[2-3 sentence paraphrase of recommended changes]

Clarifying questions:
1. Recommendations suggest creating [N] new skills - should I do this in Phase 4?
2. Priority order: [command A] → [command B] → [command C] - correct?
3. Some fixes require breaking changes (command structure) - proceed anyway?
4. Estimated time for fixes: [duration] - acceptable?
5. Should I implement all recommendations or just critical ones?

Does this match your expectations? What should I adjust?
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
5. **Verify each command** (run checklist)

**For each command:**

```yaml
Fix structure:
  - Add missing sections (use command-creation template)
  - Fix Phase 0 (make inline if agent)
  - Add clarifying questions pattern (if missing)
  - Add "Sufficient context" sections (if missing)

Refactor content:
  - Extract domain knowledge to skills
  - Simplify "Sufficient context" (extract decisions, not full YAML)
  - Add WHY explanations (production context)
  - Apply signal-vs-noise filter

Verify:
  - Run checklist from command-creation skill
  - Test structure compliance
  - Confirm content quality
```

**Output**: Summary of changes per command

```
Let me verify my understanding:
[2-3 sentence paraphrase of changes made]

Clarifying questions:
1. Made [N] changes to [M] commands - should I commit these?
2. Created [X] new skills - are these in correct location (.claude/skills/)?
3. Some commands still have minor issues [list] - fix now or later?
4. Should I create pull request with changes or just local commit?
5. Verification passed for [N] commands - what about remaining [M]?

Does this match your expectations? What should I adjust?
```

[WAIT for confirmation]

Audit complete!

---

## Phase Details - MODIFY Mode

### Phase 0: Change Scope (Inline)
**You do this - no agent**

**From Universal Phase 0: Mode=MODIFY, Command name and changes determined**

Analyze requested changes:

```yaml
COMMAND: [name from Universal Phase 0]
CHANGES_REQUESTED: [from user's natural language]

CHANGE_CATEGORIES:
  structure: Add/remove/reorder sections
  content: Update patterns, add WHY, fix examples
  quality: Apply signal-vs-noise, improve clarity
  compliance: Fix missing requirements (clarifying questions, sufficient context)
```

**Output**: Change scope + complexity estimate

**After Phase 0 - MANDATORY clarifying questions**:

```
Let me verify my understanding:
[2-3 sentence paraphrase of changes to make]

Clarifying questions:
1. Scope: Should changes affect [specific sections] or entire command?
2. Priority: What's most important - [change A] or [change B]?
3. Approach: Should I [approach A] or [approach B] for [specific change]?
4. Verification: After changes, should I verify against full checklist or just changed sections?
5. Backup: Should I create backup of original or just proceed with changes?

Does this match exactly what you want? If not, what should I adjust?
```

[WAIT for confirmation]

Ready to proceed? (continue/skip/back/stop)

---

### Phase 1: Change Analysis
**Agent**: claude-manager

**Sufficient context for quality**:
```yaml
Input needed:
  - Mode: MODIFY
  - Command name and path
  - Changes requested (from Phase 0)
  - User confirmations/adjustments (from Phase 0 clarifying questions)

NOT needed:
  - Full command content (agent will read)
  - Generic modification theory
  - Conversation history
```

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
4. Approach (how to implement changes while maintaining quality)

Use command-creation skill for structure reference.
Use signal-vs-noise skill for content quality.

Output format:
- Current state summary (what exists now)
- Change plan (section by section)
- Dependencies (what depends on what)
- Implementation steps (ordered)
- Verification checklist (how to confirm changes correct)
```

**After agent**:

Present change plan.

```
Let me verify my understanding:
[2-3 sentence paraphrase of change plan]

Clarifying questions:
1. Plan suggests [N] modifications - is this complete or should I add [X]?
2. Change order: [A] → [B] → [C] - correct priority?
3. Section [X] will be [modified/removed/added] - is this what you want?
4. Approach for [specific change]: [description] - does this make sense?
5. After changes, command will [outcome] - matches your goal?

Does this match exactly what you want? If not, what should I adjust?
```

[WAIT for confirmation]

Ready to proceed? (continue/skip/back/stop)

---

### Phase 2: Implementation (Inline)
**You do this - no agent**

Apply modifications from Phase 1 plan:

1. **Backup current version** (if requested in Phase 0)
2. **Apply changes** (section by section from plan)
3. **Verify consistency** (structure intact, references valid)
4. **Update cross-references** (if command name or sections changed)

**For each modification:**

```yaml
Structural changes:
  - Add sections (use command-creation template)
  - Remove sections (preserve content in comments if valuable)
  - Reorder sections (maintain logical flow)

Content changes:
  - Update patterns (apply signal-vs-noise)
  - Add WHY explanations (production context)
  - Fix examples (verify correctness)
  - Simplify "Sufficient context" (extract decisions)

Compliance fixes:
  - Add clarifying questions pattern (if missing)
  - Add "Sufficient context" sections (if missing)
  - Add "⚠️ CRITICAL" section (if missing)
  - Fix Phase 0 (make inline if agent)

Quality improvements:
  - Apply signal-vs-noise filter
  - Improve clarity (remove ambiguity)
  - Add missing WHY context
  - Fix outdated information
```

**Output**: Summary of changes made

No clarifying questions (implementation is mechanical based on approved plan).

Ready to proceed? (continue/skip/back/stop)

---

### Phase 3: Verification (Inline)
**You do this - no agent**

Verify modifications against quality standards:

```yaml
Structure verification:
  - [ ] All required sections present
  - [ ] Sections in logical order
  - [ ] No broken references
  - [ ] Frontmatter valid

Content verification:
  - [ ] Changes match approved plan
  - [ ] No new noise introduced
  - [ ] WHY context included (if applicable)
  - [ ] Examples correct and current

Compliance verification:
  - [ ] Clarifying questions after EVERY phase (if applicable)
  - [ ] "Sufficient context" sections present (if applicable)
  - [ ] Phase 0 inline (if applicable)
  - [ ] User checkpoints after confirmation

Quality verification:
  - [ ] Signal-focused (no generic content)
  - [ ] Clear and unambiguous
  - [ ] Complete (no missing critical info)
  - [ ] Scannable (headers, bullets, tables)
```

**Output**: Verification results + file path

```
Let me verify my understanding:
[2-3 sentence paraphrase of changes made and verification status]

Clarifying questions:
1. Made [N] changes to [sections] - all correct?
2. Verification found [N] issues - should I fix automatically or show you?
3. Modified command ready at [path] - should I commit or let you review?
4. Changes improve [aspect] - does this achieve your goal?
5. Should I test command by running it, or just structural verification?

Does this match your expectations? What should I adjust?
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

---

## Sufficient Context Principle

**For each claude-manager invocation, provide:**

- ✅ Mode (CREATE or AUDIT)
- ✅ Critical decisions from previous phases (extracted, not full conversation)
- ✅ User confirmations/adjustments (from clarifying questions)
- ✅ Specific task for this phase
- ✅ Expected output format

**Do NOT provide:**

- ❌ Full previous YAML outputs (extract decisions only)
- ❌ Entire conversation history (conclusions only)
- ❌ Generic command theory (claude-manager has skills)
- ❌ Detailed examples (skills provide these)

**Test question**:

> "Can claude-manager produce HIGH QUALITY output with this context alone?"
>
> If YES → sufficient
> If NO → add missing critical info (not everything)

---

## Key Principles

**Modes:** CREATE (new multi-phase command) vs AUDIT (check compliance)

**Clarifying Questions:** MANDATORY after Phase 0 and EVERY agent phase (paraphrase + 5 questions + confirmation)

**Sufficient Context:** claude-manager gets extracted decisions, not full conversation

**WHY over HOW:** AUDIT checks for domain knowledge in commands (should be in skills)

**Signal vs Noise:** AUDIT checks for full YAML outputs in context (should extract decisions)

**Force Invocation:** "⚠️ CRITICAL" section prevents describing instead of invoking

**User Checkpoints:** After confirmation, offer commands (continue/skip/back/stop)
