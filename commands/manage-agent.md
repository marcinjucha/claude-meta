---
description: "Intelligent agent management - create, audit, or modify agents based on natural language"
---

# Manage Agent - Intelligent Agent Management

Automatically detects intent from natural language and executes appropriate agent management task: CREATE new agents, AUDIT existing agents for quality, or MODIFY agents to fix issues.

## Phases (Adaptive)

**CREATE Mode:**

```
0: Intent Detection + Decision Framework    (orchestrator - inline + clarifying questions)
1: Signal Extraction                         (claude-manager with agent-creator)
2: Structure Design                          (claude-manager with agent-creator)
3: File Creation                             (claude-manager with agent-creator)
4: Verification                              (claude-manager with agent-creator)
```

**AUDIT Mode:**

```
0: Intent Detection + Scope                  (orchestrator - inline + clarifying questions)
1: Structure Compliance                      (claude-manager with agent-creator)
2: Content Quality                           (claude-manager with agent-creator)
3: Integration Check                         (claude-manager with agent-creator)
4: Recommendations                           (claude-manager with agent-creator)
5: Implementation                            (claude-manager with agent-creator - if approved)
```

**MODIFY Mode:**

```
0: Intent Detection + Change Scope           (orchestrator - inline + clarifying questions)
1: Change Analysis                           (claude-manager with agent-creator)
2: Implementation                            (claude-manager with agent-creator)
3: Verification                              (claude-manager with agent-creator)
```

**Speed**: 2-5 min (CREATE), 1-3 min (AUDIT single), 3-8 min (AUDIT all), 1-2 min (MODIFY)

---

## Orchestrator Instructions

### ⚠️ CRITICAL: YOU MUST INVOKE claude-manager

**You are the orchestrator.** Your job is to **ACTUALLY INVOKE claude-manager using the Task tool**.

**DO NOT**:

-   ❌ Say "I will launch claude-manager"
-   ❌ Describe what claude-manager will do
-   ❌ Explain the phase without invoking
-   ❌ Try to create/audit/modify agents yourself

**DO**:

-   ✅ Immediately invoke Task tool with claude-manager
-   ✅ Use subagent_type="claude-manager", description, prompt parameters
-   ✅ Wait for claude-manager completion
-   ✅ Show results to user

**Example**:

```
Phase 1/4: Signal Extraction
Launching claude-manager...
```

[IMMEDIATELY invoke Task tool NOW with subagent_type="claude-manager"]

### Critical Rules

1. **INVOKE with Task tool** - Every phase requires actual Task tool call to claude-manager
2. **Signal extraction** - Domain knowledge goes in skills, NOT agents (thin router principle)
3. **User checkpoints** - Get approval after each phase (prevents wasted work)
4. **Track phase** - Remember current position (user can skip/back)
5. **Clarifying questions** - After EVERY phase, paraphrase + 5 questions + confirmation
6. **NEVER INVENT CONTENT** - claude-manager must NEVER make up metrics, production incidents, anti-patterns, or numbers. ONLY use user-provided data.

### Clarifying Questions Pattern

**After EVERY phase (including Phase 0), you MUST:**

```
Let me verify my understanding:
[2-3 sentence paraphrase of what was produced/decided in this phase]

Clarifying questions:
1. [Question about scope/constraint from this phase]
2. [Question about tool restrictions/requirements]
3. [Question about priority/approach]
4. [Question about integration with skills/commands]
5. [Question about validation criteria]

Does this match exactly what you want to achieve? If not, what should I adjust?
```

**Wait for user response.** If user says corrections needed:

-   Apply corrections
-   Paraphrase updated understanding
-   Ask 5 NEW clarifying questions about updated version
-   Repeat until user confirms "dokładnie to co chcę" / "exactly what I want"

**Only after confirmation**, proceed with: "Ready to proceed? (continue/skip/popraw/back/stop)"

### Phase Execution Pattern

```
═══════════════════════════════════════════════
Phase N/X: [Name]
═══════════════════════════════════════════════

Launching claude-manager...
```

[Invoke Task tool with claude-manager]

```
**Phase N Complete** ✅

[Present claude-manager output clearly]

───────────────────────────────────────────────
Let me verify my understanding:
[2-3 sentence paraphrase]

Clarifying questions:
1. [Specific question]
2. [Specific question]
3. [Specific question]
4. [Specific question]
5. [Specific question]

Does this match exactly what you want? If not, what should I adjust?
───────────────────────────────────────────────

[Wait for user confirmation]

Ready to proceed? (continue/skip/popraw/back/stop)
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
  - "create" / "new" / "need agent"
  - "agent for [new functionality]"
  - "creating specialist in [area]"
  - "specialist for [task]"
  - Describes specialized capability not in existing agents
  - Agent gains knowledge through skills (mentioned in request)

AUDIT indicators:
  - "check" / "verify" / "audit" / "validate" / "review quality"
  - "meets requirements" / "compliant" / "follows patterns"
  - References EXISTING agent name + quality check
  - "all agents" (audit scope)

MODIFY indicators:
  - "update" / "fix" / "modify" / "change"
  - "add [section]" / "remove [section]" / "improve"
  - References EXISTING agent name + specific change
  - "missing [feature]" / "[agent] should have"

Ambiguous:
  - Multiple indicators present
  - Unclear agent reference
  - No clear action verb
```

**Step 2: List Existing Agents (if needed for AUDIT/MODIFY)**

If AUDIT or MODIFY detected, list agents in `.claude/agents/`:

```bash
ls .claude/agents/*.md
```

**Step 3: Determine Mode and Scope**

```yaml
Mode: [CREATE / AUDIT / MODIFY]

Scope:
    CREATE: [agent name from request or ask]
    AUDIT: [specific agent or "all"]
    MODIFY: [agent name + changes requested]

Confidence: [HIGH / MEDIUM / LOW]
```

**Step 4: If Confidence LOW - Ask Clarifying Questions**

```
Let me verify my understanding:
[2-3 sentence paraphrase of detected intent]

Clarifying questions:
1. Intent: Should I [CREATE new / AUDIT existing / MODIFY existing] agent?
2. Scope: Which agent - [detected name or list options]?
3. Goal: What's the primary objective - [inferred goal]?
4. Priority: What's most important - [tool restrictions / skills / system prompt]?
5. Action: Should I [specific action] or did you mean [alternative]?

Does this match exactly what you want? If not, what should I adjust?
```

[WAIT for confirmation]

**Step 5: Proceed to Mode-Specific Phase 0**

Once mode determined with HIGH confidence:

-   CREATE → Continue to CREATE Mode Phase 0 (Decision Framework)
-   AUDIT → Continue to AUDIT Mode Phase 0 (Scope Selection)
-   MODIFY → Continue to MODIFY Mode Phase 0 (Change Scope)

Ready to proceed? (continue/skip/back/stop)

---

## Phase Details - CREATE Mode

### Phase 0: Decision Framework (Inline)

**From Universal Phase 0: Mode=CREATE, Agent name determined**

**You do this - no agent**

Quick assessment before creating agent:

**Decision questions:**

1. **Does this need specific tool restrictions?**

    - YES → Read-only agent, SQL-only agent
    - NO → Standard tool access (use skill instead)

2. **Does this need isolation?**

    - YES → High-volume operations, context-heavy tasks
    - NO → Main conversation works (use skill)

3. **Does this need specialized execution?**
    - YES → Background processing, specific model, custom permissions
    - NO → Standard execution (use skill)

**Decision:**

-   If 2-3 YES → Continue with agent creation
-   If 0-1 YES → Recommend skill or command instead

**Output:**

```
Decision: [Create agent / Use skill instead / Use command instead]
Reasoning: [Brief explanation]
```

**After assessment:**

```
Let me verify my understanding:
[2-3 sentence paraphrase of decision and reasoning]

Clarifying questions:
1. What specific tool restrictions are needed (if any)?
2. Does this agent need isolation from main context?
3. Should this agent run automatically or only on explicit request?
4. What skills should this agent preload (if any)?
5. What's the primary success criterion - what makes this agent "useful"?

Does this match exactly what you want to achieve? If not, what should I adjust?
```

[WAIT for user confirmation]

Ready to proceed? (continue/skip/stop)

---

#### Phase 1: Signal Extraction

**Agent**: claude-manager (with agent-creator skill)

**Sufficient context for quality**:

```yaml
Input needed:
    - Agent purpose (from Phase 0: specialized capability description)
    - Tool requirements (read-only, specific tools, all tools)
    - Domain knowledge identified (patterns, rules, decisions)
    - Existing skills available (what can be referenced vs duplicated)

NOT needed:
    - Generic agent patterns (claude-manager knows)
    - Framework explanations (claude-manager knows)
    - Full skill contents (just names and purposes)
```

**Prompt to claude-manager**:

````
You are creating a new agent with agent-creator skill.

⚠️ CRITICAL: NEVER INVENT OR HALLUCINATE CONTENT
- DO NOT make up metrics, numbers, or production incidents
- DO NOT invent anti-patterns without user-provided examples
- ONLY extract what user actually provided
- If no production data exists, use placeholder: [User to provide real metric/incident]

AGENT PURPOSE (from Phase 0):
[Purpose statement, specialized capability]

REQUIREMENTS:
- Tool restrictions: [list or "standard access"]
- Isolation needed: [yes/no with reason]
- Model preference: [sonnet/opus/haiku or inherit]

TASK:
Phase 1 - Signal Extraction

Extract signal (thin router infrastructure):
1. Identify approach/workflow (how agent tackles tasks)
2. Separate domain knowledge from approach (knowledge → skills)
3. Determine tool restrictions (only what's needed)
4. Identify skills to reference (existing skills for patterns)

Apply signal vs noise filter:
- Include: Task approach, tool restrictions rationale, when to delegate
- Exclude: Domain patterns (those go in skills), generic explanations

ANY NO = NOISE → Cut immediately.

DO NOT include:
- Generic agent patterns (thin router principle covers this)
- Standard tool use (AI knows Tool API)
- Obvious delegation (basic orchestration)

Output format (YAML):
```yaml
signal_extraction:
  agent_approach:
    - [Step in agent's approach]
  tool_restrictions:
    allowed: [list]
    denied: [list]
    rationale: [why these restrictions]
  skills_to_reference:
    - skill_name: [name]
      provides: [what knowledge]
  domain_knowledge_removed:
    - pattern: [what was identified]
      destination: [which skill or "create new skill"]
````

```

**After claude-manager**:

Present extraction results clearly:
- Thin router approach identified
- Domain knowledge separated
- Skills to reference
- Tool restrictions justified

Then:
```

Let me verify my understanding:
[2-3 sentence paraphrase of agent approach and tool restrictions]

Clarifying questions:

1. Should the agent approach include [specific step], or is that too detailed?
2. Are these tool restrictions correct: [list restrictions]?
3. Should [domain pattern] go in existing [skill-name] or new skill?
4. Does the agent need [specific skill] preloaded?
5. What's the trigger - when should Claude delegate to this agent?

Does this match exactly what you want? If not, what should I adjust?

````

---

#### Phase 2: Structure Design

**Agent**: claude-manager (with agent-creator skill)

**Sufficient context for quality**:
```yaml
Input needed:
  - Agent approach (from Phase 1: steps, guidelines)
  - Tool restrictions (from Phase 1: allowed/denied with rationale)
  - Skills to reference (from Phase 1: list with purposes)
  - Trigger description (when to delegate)

NOT needed:
  - Full signal extraction YAML (extract approach only)
  - Domain patterns (already separated to skills)
  - Generic agent structure (claude-manager knows)
````

**Prompt to claude-manager**:

````
You are designing agent structure with agent-creator skill.

SIGNAL EXTRACTED (from Phase 1):
Agent approach:
[List of steps from Phase 1]

Tool restrictions:
- Allowed: [list]
- Denied: [list]
- Rationale: [why]

Skills to reference:
[List from Phase 1]

TASK:
Phase 2 - Structure Design

Design agent structure:
1. Frontmatter fields (name, description, tools, skills, model)
2. System prompt sections (role, steps, guidelines, output format)
3. Verify thin router (approach only, no domain patterns)
4. Third-person description (when to delegate)

Apply quality standards:
- Name: lowercase-with-hyphens, max 64 chars
- Description: third-person, triggers delegation, <1024 chars
- System prompt: 50-200 lines (approach, not patterns)
- Skills referenced (not duplicated)
- Apply Signal vs Noise: No generic explanations, only project-specific agent design

Output format (YAML):
```yaml
agent_structure:
  frontmatter:
    name: [lowercase-with-hyphens]
    description: [third-person, when to delegate]
    tools: [allowed tools list]
    disallowedTools: [denied tools list]
    model: [sonnet/opus/haiku/inherit]
    skills: [skill names list]
  system_prompt_sections:
    - section: [Role]
      content: [brief role description]
    - section: [When invoked]
      content: [numbered steps]
    - section: [Guidelines]
      content: [approach guidelines]
    - section: [Output Format]
      content: [how to present results]
  verification:
    thin_router: [yes/no - is this infrastructure only?]
    domain_knowledge_check: [any patterns in prompt?]
    skill_references: [skills properly referenced?]
````

```

**After claude-manager**:

Present structure design:
- Frontmatter fields
- System prompt sections
- Thin router verification

Then:
```

Let me verify my understanding:
[2-3 sentence paraphrase of agent structure - name, tools, system prompt approach]

Clarifying questions:

1. Is the agent name "[name]" clear enough, or should it be more specific?
2. Does the description trigger delegation at the right times?
3. Are [N] system prompt sections sufficient, or missing anything?
4. Should [specific guideline] be added to agent guidelines?
5. Is the output format appropriate for this agent's tasks?

Does this match exactly what you want? If not, what should I adjust?

````

---

#### Phase 3: File Creation

**Agent**: claude-manager (with agent-creator skill)

**Sufficient context for quality**:
```yaml
Input needed:
  - Agent structure (from Phase 2: frontmatter + system prompt sections)
  - File location (.claude/agents/ or ~/.claude/agents/)
  - Verification checklist (structure, thin router, skills)

NOT needed:
  - Full Phase 1 extraction (already incorporated in Phase 2)
  - Signal vs noise philosophy (claude-manager knows)
  - Generic agent examples (claude-manager knows)
````

**Prompt to claude-manager**:

```
You are creating agent file with agent-creator skill.

AGENT STRUCTURE (from Phase 2):
Frontmatter:
[YAML from Phase 2]

System prompt sections:
[Sections from Phase 2]

FILE LOCATION:
- Project agent: .claude/agents/[name].md (check into git)
- User agent: ~/.claude/agents/[name].md (personal workflow)

TASK:
Phase 3 - File Creation

Create agent .md file:
1. Write frontmatter (YAML with proper formatting)
2. Write system prompt (markdown, 50-200 lines)
3. Verify file structure (frontmatter + body)
4. Create file at correct location

Quality checks:
- Frontmatter valid YAML
- System prompt focused on approach (not patterns)
- Skills referenced (not duplicated)
- Third-person description
- Thin router (infrastructure only)

Output:
- Created file path
- File content preview
- Verification checklist results
```

```

**After claude-manager**:

Present created file:
- File path
- Frontmatter preview
- System prompt preview
- Verification results

Then:
```

Let me verify my understanding:
[2-3 sentence paraphrase of created agent file - location, key fields, system prompt approach]

Clarifying questions:

1. Is the file location correct (.claude/agents/ for project vs ~/.claude/agents/ for personal)?
2. Does the frontmatter include all necessary fields?
3. Is the system prompt length appropriate (50-200 lines)?
4. Should any additional skills be referenced?
5. Is the agent ready for testing, or needs adjustments?

Does this match exactly what you want? If not, what should I adjust?

````

---

#### Phase 4: Verification

**Agent**: claude-manager (with agent-creator skill)

**Sufficient context for quality**:
```yaml
Input needed:
  - Created file path (from Phase 3)
  - Agent structure (frontmatter + system prompt)
  - Quality standards checklist

NOT needed:
  - Previous phase YAML outputs (file already created)
  - Signal extraction details (verification focused)
````

**Prompt to claude-manager**:

````
You are verifying agent quality with agent-creator skill.

CREATED AGENT (from Phase 3):
File: [path]
Name: [name]
Tools: [list]
Skills: [list]

TASK:
Phase 4 - Verification

Verify agent quality:
1. Structure check (frontmatter valid, system prompt length)
2. Content check (thin router, no domain knowledge)
3. Integration check (skills exist, tools valid)
4. Description check (third-person, clear triggers)

Verification checklist:
- [ ] Name: lowercase + hyphens, max 64 chars
- [ ] Description: third-person, <1024 chars, describes WHEN
- [ ] Body: System prompt only (no domain knowledge)
- [ ] Tool restrictions: Only what's needed
- [ ] Skills: Referenced (not duplicated in body)
- [ ] Thin router: Infrastructure only, patterns in skills

Content verification - Signal vs Noise per section:
  - [ ] Purpose: No generic "what is an agent" explanation
  - [ ] Agent Design: Thin router validation (no thick logic)
  - [ ] No invented tool restrictions

Output format (YAML):
```yaml
verification:
  structure:
    name_valid: [yes/no]
    description_valid: [yes/no]
    frontmatter_valid: [yes/no]
    system_prompt_length: [N lines]
  content:
    thin_router: [yes/no]
    domain_knowledge_found: [yes/no - should be no]
    skills_referenced: [yes/no]
  integration:
    skills_exist: [list of skills, all exist?]
    tools_valid: [all tools are valid?]
    description_triggers: [clear when to delegate?]
  issues_found:
    - [issue description]
  recommendations:
    - [recommendation]
````

```

**After claude-manager**:

Present verification results:
- Structure validation
- Content quality
- Integration check
- Issues found
- Recommendations

Then:
```

Let me verify my understanding:
[2-3 sentence paraphrase of verification results - passed checks, issues if any]

Clarifying questions:

1. Are all verification checks passing?
2. Should any identified issues be fixed now?
3. Are the tool restrictions appropriate for the agent's purpose?
4. Should additional skills be added to the reference list?
5. Is the agent ready for production use, or needs iteration?

Does this match exactly what you want? If not, what should I adjust?

```

---

## Phase Details - AUDIT Mode

### Phase 0: Scope Selection (Inline)

**From Universal Phase 0: Mode=AUDIT, Scope determined (specific agent or "all")**

**You do this - no agent**

Determine audit scope:

**Options:**
1. **Specific agent** - Audit single agent by name
2. **All agents** - Audit all agents in .claude/agents/

**Output:**
```

Scope: [Specific: name / All agents]
Agents to audit: [list]

```

**After assessment:**

```

Let me verify my understanding:
[Paraphrase: auditing [specific agent] or [all N agents]]

Clarifying questions:

1. For [agent-name], what specific concerns do you have (if any)?
2. Should the audit focus on [structure/content/integration/all]?
3. Are there known issues with this agent I should investigate?
4. Should I recommend fixes, or just report findings?
5. If issues found, should I implement fixes automatically or ask first?

Does this match exactly what you want? If not, what should I adjust?

````

[WAIT for user confirmation]

Ready to proceed? (continue/skip/stop)

---

#### Phase 1: Structure Compliance

**Agent**: claude-manager (with agent-creator skill)

**Sufficient context for quality**:
```yaml
Input needed:
  - Agent(s) to audit (from Phase 0: names and paths)
  - Structure requirements (frontmatter fields, system prompt length)

NOT needed:
  - Agent purpose explanations (auditing structure only)
  - Full agent-creator skill content (structure checks)
````

**Prompt to claude-manager**:

````
You are auditing agent structure with agent-creator skill.

AGENTS TO AUDIT (from Phase 0):
[List of agent names and paths]

TASK:
Phase 1 - Structure Compliance

For each agent, check:
1. Frontmatter validity (YAML parsing, required fields)
2. System prompt length (50-200 lines ideal)
3. File structure (frontmatter + body separation)
4. Field formats (name max 64 chars, description <1024 chars)

Structure requirements:
- name: lowercase-with-hyphens, max 64 chars
- description: third-person, <1024 chars
- tools/disallowedTools: valid tool names
- model: sonnet/opus/haiku/inherit
- skills: valid skill names
- System prompt: 50-200 lines

Output format (YAML per agent):
```yaml
structure_audit:
  agent_name: [name]
  checks:
    frontmatter_valid: [yes/no]
    name_format: [valid/invalid - reason]
    description_length: [N chars - within limit?]
    system_prompt_length: [N lines - within 50-200?]
    required_fields: [all present?]
  issues:
    - field: [field name]
      issue: [description]
      severity: [critical/warning/info]
  recommendations:
    - [specific fix]
````

```

**After claude-manager**:

Present structure audit:
- Per-agent results
- Issues found
- Severity levels
- Recommendations

Then:
```

Let me verify my understanding:
[2-3 sentence paraphrase of structure audit - agents checked, issues found]

Clarifying questions:

1. Are the structure issues [list] critical to fix immediately?
2. Should agents with [N lines] system prompt be refactored?
3. Is the frontmatter format acceptable, or needs updates?
4. Should I proceed to content quality check despite structure issues?
5. Which issues should be fixed first (priority order)?

Does this match exactly what you want? If not, what should I adjust?

````

---

#### Phase 2: Content Quality

**Agent**: claude-manager (with agent-creator skill)

**Sufficient context for quality**:
```yaml
Input needed:
  - Agent(s) to audit (names and paths)
  - Structure audit results (from Phase 1: issues if any)
  - Thin router principle (agents = infrastructure, skills = knowledge)

NOT needed:
  - Full structure audit YAML (just critical issues)
  - Agent-creator philosophy (claude-manager knows)
````

**Prompt to claude-manager**:

````
You are auditing agent content quality with agent-creator skill.

⚠️ CRITICAL: FLAG INVENTED CONTENT
Flag invented metrics/incidents for removal. Recommend placeholders or deletion.

AGENTS TO AUDIT:
[List of agent names]

STRUCTURE ISSUES (from Phase 1):
[Critical issues only - if any affect content audit]

TASK:
Phase 2 - Content Quality

Apply "ANY NO = NOISE" to existing agent content.

For each agent, check:
1. Thin router principle (infrastructure only, no domain patterns)
2. Domain knowledge in system prompt (should be in skills instead)
3. Skill references (skills listed, not duplicated)
4. WHY explanations (rationale for tool restrictions, approach)

Quality checks:
- System prompt focused on approach (not patterns)
- No code patterns in agent body (those go in skills)
- Skills referenced in frontmatter (not duplicated in body)
- Tool restrictions justified (WHY these tools?)
- Third-person description (describes WHEN, not "I help")

Output format (YAML per agent):
```yaml
content_audit:
  agent_name: [name]
  checks:
    thin_router: [yes/no - is this infrastructure only?]
    domain_knowledge_found:
      - pattern: [what pattern found in agent]
        should_be_in_skill: [which skill]
    skill_references: [skills listed but not duplicated?]
    why_explanations: [tool restrictions explained?]
    description_type: [third-person/first-person]
  issues:
    - type: [domain_knowledge/skill_duplication/vague_description]
      description: [what's wrong]
      location: [where in file]
      severity: [critical/warning/info]
  recommendations:
    - [specific fix - e.g., "Move [pattern] to [skill-name]"]
````

```

**After claude-manager**:

Present content audit:
- Thin router violations
- Domain knowledge found
- Skill duplication
- Missing WHY
- Recommendations

Then:
```

Let me verify my understanding:
[2-3 sentence paraphrase of content issues - thin router violations, domain knowledge in agent]

Clarifying questions:

1. Should [domain pattern] in [agent] be moved to [existing skill] or new skill?
2. Are the tool restrictions justified, or need WHY explanations?
3. Should the agent description be rewritten to third-person?
4. Are all identified patterns actually domain knowledge, or some are approach?
5. Which content issues are highest priority to fix?

Does this match exactly what you want? If not, what should I adjust?

````

---

#### Phase 3: Integration Check

**Agent**: claude-manager (with agent-creator skill)

**Sufficient context for quality**:
```yaml
Input needed:
  - Agent(s) to audit (names and paths)
  - Referenced skills (from agents' frontmatter)
  - Tool restrictions (from agents' frontmatter)

NOT needed:
  - Full previous audit results (just critical issues)
  - Agent-creator advanced patterns (integration focused)
````

**Prompt to claude-manager**:

````
You are checking agent integration with agent-creator skill.

AGENTS TO AUDIT:
[List of agent names with skills and tools from frontmatter]

TASK:
Phase 3 - Integration Check

For each agent, verify:
1. Skills exist (all referenced skills are available)
2. Tools valid (allowed/disallowed tools are real tool names)
3. Description triggers (clear when to delegate)
4. Cross-references (commands/workflows reference this agent)

Integration checks:
- Skills in frontmatter actually exist in .claude/skills/
- Tools in frontmatter are valid tool names (Read, Write, Edit, Grep, Glob, Bash, etc.)
- Description enables auto-delegation (contains trigger keywords)
- Agent referenced in commands/workflows (if applicable)

Output format (YAML per agent):
```yaml
integration_audit:
  agent_name: [name]
  checks:
    skills_exist:
      - skill: [skill-name]
        exists: [yes/no]
        path: [path if exists]
    tools_valid:
      - tool: [tool-name]
        valid: [yes/no]
    description_triggers: [enables auto-delegation?]
    referenced_by:
      - type: [command/workflow/agent]
        name: [name]
  issues:
    - type: [missing_skill/invalid_tool/weak_description/not_referenced]
      description: [what's wrong]
      severity: [critical/warning/info]
  recommendations:
    - [specific fix - e.g., "Create missing skill [name]"]
````

```

**After claude-manager**:

Present integration audit:
- Skills existence check
- Tools validity
- Description triggers
- Cross-references
- Recommendations

Then:
```

Let me verify my understanding:
[2-3 sentence paraphrase of integration issues - missing skills, invalid tools, weak descriptions]

Clarifying questions:

1. Should missing skill [name] be created, or removed from agent reference?
2. Are invalid tool names [list] typos, or should different tools be used?
3. Does the agent description need rewriting to enable auto-delegation?
4. Should this agent be referenced in any commands/workflows?
5. Which integration issues are critical vs nice-to-have?

Does this match exactly what you want? If not, what should I adjust?

````

---

#### Phase 4: Recommendations

**Agent**: claude-manager (with agent-creator skill)

**Sufficient context for quality**:
```yaml
Input needed:
  - Structure audit results (from Phase 1: issues)
  - Content audit results (from Phase 2: violations)
  - Integration audit results (from Phase 3: missing refs)

NOT needed:
  - Full audit YAML outputs (extract issues only)
  - Agent file contents (already audited)
````

**Prompt to claude-manager**:

````
You are prioritizing recommendations with agent-creator skill.

AUDIT RESULTS (from Phases 1-3):
Structure issues:
[List from Phase 1]

Content issues:
[List from Phase 2]

Integration issues:
[List from Phase 3]

TASK:
Phase 4 - Recommendations

Consolidate and prioritize fixes:
1. Group by severity (critical/warning/info)
2. Group by agent (if multiple agents)
3. Prioritize (blocking issues first)
4. Estimate effort (quick fix vs refactor)

Prioritization criteria:
- CRITICAL: Blocks agent usage (missing skill, invalid tool, broken structure)
- WARNING: Reduces quality (domain knowledge in agent, weak description)
- INFO: Improvement opportunity (add WHY, third-person description)

Output format (YAML):
```yaml
recommendations:
  critical:
    - agent: [name]
      issue: [description]
      fix: [what to do]
      effort: [quick/moderate/significant]
  warning:
    - agent: [name]
      issue: [description]
      fix: [what to do]
      effort: [quick/moderate/significant]
  info:
    - agent: [name]
      issue: [description]
      fix: [what to do]
      effort: [quick/moderate/significant]
  summary:
    total_issues: [N]
    critical_count: [N]
    estimated_time: [X min]
````

```

**After claude-manager**:

Present prioritized recommendations:
- Critical issues (fix immediately)
- Warnings (should fix)
- Info (nice to have)
- Summary (total issues, estimated time)

Then:
```

Let me verify my understanding:
[2-3 sentence paraphrase of recommendations - critical issues, priority order]

Clarifying questions:

1. Should I fix critical issues automatically, or do you want to review first?
2. Are warning-level issues worth fixing now, or defer?
3. Should I create missing skills [list], or just document?
4. Is the effort estimate reasonable, or adjust expectations?
5. After fixes, should I re-audit to verify?

Does this match exactly what you want? If not, what should I adjust?

````

---

#### Phase 5: Implementation (If Approved)

**Agent**: claude-manager (with agent-creator skill)

**Sufficient context for quality**:
```yaml
Input needed:
  - Approved recommendations (from Phase 4: user selected which to fix)
  - Agent file paths (where to apply fixes)
  - Fix instructions (specific changes)

NOT needed:
  - Full audit history (just fixes to apply)
  - Unapproved recommendations (user chose subset)
````

**Prompt to claude-manager**:

````
You are implementing fixes with agent-creator skill.

APPROVED FIXES (from Phase 4):
[List of fixes user approved]

AGENTS TO UPDATE:
[List of agent names and paths]

TASK:
Phase 5 - Implementation

For each approved fix:
1. Apply fix (update frontmatter, system prompt, or create file)
2. Verify fix (re-check that issue resolved)
3. Update related files (if fix affects skills/commands)
4. Document changes (what was changed, why)

Implementation steps:
- Frontmatter fixes: Update YAML fields
- System prompt fixes: Move domain knowledge to skills, add WHY
- Integration fixes: Create missing skills, fix tool names
- Description fixes: Rewrite to third-person with triggers

Output format:
```yaml
implementation:
  fixes_applied:
    - agent: [name]
      fix: [what was fixed]
      files_changed: [list of files]
      verification: [issue resolved?]
  skills_created:
    - skill: [name]
      path: [path]
      content: [moved from agent]
  issues_remaining:
    - [any issues not fully resolved]
````

```

**After claude-manager**:

Present implementation results:
- Fixes applied
- Files changed
- Skills created (if any)
- Issues remaining
- Verification

Then:
```

Let me verify my understanding:
[2-3 sentence paraphrase of fixes applied - agents updated, skills created]

Clarifying questions:

1. Are all approved fixes applied correctly?
2. Should newly created skills be tested?
3. Are there any remaining issues that need attention?
4. Should I re-run audit to verify fixes?
5. Is the agent now ready for production use?

Does this match exactly what you want? If not, what should I adjust?

```

---

## Phase Details - MODIFY Mode

### Phase 0: Change Scope (Inline)

**From Universal Phase 0: Mode=MODIFY, Agent name and changes determined**

**You do this - no agent**

Determine what to modify:

**Change types:**
1. **Frontmatter field** - name, description, tools, skills, model
2. **System prompt section** - role, steps, guidelines, output format
3. **Both** - frontmatter + system prompt changes

**From user request:**
Analyze user's modification request:
- Changing tool restrictions? → Frontmatter (tools/disallowedTools)
- Changing description? → Frontmatter (description)
- Changing approach? → System prompt (steps/guidelines)
- Changing model? → Frontmatter (model)
- Adding skill reference? → Frontmatter (skills)

**Output:**
```

Agent: [name]
Change scope: [Frontmatter / System prompt / Both]
Specific changes:

-   [Change 1]
-   [Change 2]

```

**After assessment:**

```

Let me verify my understanding:
[2-3 sentence paraphrase of changes to make - which fields/sections, why]

Clarifying questions:

1. Should [specific field] be changed to [new value], or something else?
2. Does changing [field] require updating [related field]?
3. Should the change maintain thin router principle (no domain knowledge added)?
4. Are there related agents/skills/commands that need updating?
5. After change, what's the validation criterion - how to verify it's correct?

Does this match exactly what you want? If not, what should I adjust?

````

[WAIT for user confirmation]

Ready to proceed? (continue/skip/stop)

---

#### Phase 1: Change Analysis

**Agent**: claude-manager (with agent-creator skill)

**Sufficient context for quality**:
```yaml
Input needed:
  - Agent to modify (from Phase 0: name and path)
  - Change scope (from Phase 0: frontmatter/system prompt/both)
  - Specific changes (from Phase 0: what to change)
  - Thin router principle (maintain infrastructure only)

NOT needed:
  - Full agent file content (just relevant sections)
  - Agent-creator philosophy (claude-manager knows)
````

**Prompt to claude-manager**:

````
You are analyzing changes with agent-creator skill.

AGENT TO MODIFY (from Phase 0):
Name: [name]
Path: [path]

CHANGE SCOPE (from Phase 0):
Type: [Frontmatter / System prompt / Both]
Specific changes:
[List of changes]

TASK:
Phase 1 - Change Analysis

Analyze impact:
1. What sections affected (frontmatter fields, system prompt sections)
2. Maintain thin router (changes don't add domain knowledge)
3. Update related references (skills, commands, workflows)
4. Verify consistency (all related fields updated)

Analysis checks:
- Changes maintain thin router principle
- No domain knowledge added to system prompt
- Tool restrictions still justified
- Skill references still valid
- Description still third-person with triggers

Output format (YAML):
```yaml
change_analysis:
  agent: [name]
  changes_planned:
    frontmatter:
      - field: [field name]
        current: [current value]
        new: [new value]
        rationale: [why this change]
    system_prompt:
      - section: [section name]
        current: [current content]
        new: [new content]
        rationale: [why this change]
  impact:
    thin_router_maintained: [yes/no]
    related_updates_needed:
      - type: [skill/command/workflow]
        name: [name]
        change: [what needs updating]
  verification:
    - check: [what to verify after change]
````

```

**After claude-manager**:

Present change analysis:
- Changes planned
- Thin router maintained
- Related updates needed
- Verification checklist

Then:
```

Let me verify my understanding:
[2-3 sentence paraphrase of changes - what will change, impact on thin router]

Clarifying questions:

1. Are the planned changes exactly what you intended?
2. Should related [skill/command] be updated as part of this change?
3. Does the change maintain thin router principle (no domain knowledge added)?
4. Are there any side effects or edge cases to consider?
5. What's the rollback plan if change doesn't work as expected?

Does this match exactly what you want? If not, what should I adjust?

````

---

#### Phase 2: Implementation

**Agent**: claude-manager (with agent-creator skill)

**Sufficient context for quality**:
```yaml
Input needed:
  - Change analysis (from Phase 1: planned changes)
  - Agent file path (where to apply changes)
  - Related updates (from Phase 1: skills/commands to update)

NOT needed:
  - Full Phase 0 context (change analysis includes needed info)
  - Original user request (translated to specific changes)
````

**Prompt to claude-manager**:

````
You are implementing changes with agent-creator skill.

CHANGES PLANNED (from Phase 1):
Agent: [name]
Path: [path]

Frontmatter changes:
[List from Phase 1]

System prompt changes:
[List from Phase 1]

Related updates:
[List from Phase 1]

TASK:
Phase 2 - Implementation

Apply changes:
1. Update agent file (frontmatter, system prompt)
2. Update related files (skills, commands, workflows)
3. Verify structure (frontmatter valid, system prompt length)
4. Document changes (what changed, why)

Implementation steps:
- Frontmatter: Update YAML fields, maintain format
- System prompt: Update sections, maintain thin router
- Related files: Update references, cross-checks
- Verification: Re-check structure, content, integration

Output format:
```yaml
implementation:
  agent_updated:
    path: [path]
    changes_applied:
      - section: [frontmatter/system_prompt]
        field: [field name]
        change: [what was changed]
  related_updated:
    - type: [skill/command/workflow]
      path: [path]
      change: [what was updated]
  verification:
    structure_valid: [yes/no]
    thin_router_maintained: [yes/no]
    references_updated: [yes/no]
````

```

**After claude-manager**:

Present implementation results:
- Agent file updated
- Related files updated
- Verification results

Then:
```

Let me verify my understanding:
[2-3 sentence paraphrase of changes made - files updated, verification passed]

Clarifying questions:

1. Are all changes applied correctly?
2. Should any additional related files be updated?
3. Is the agent structure still valid (frontmatter, system prompt)?
4. Should I test the agent to verify behavior?
5. Are there any issues or concerns with the changes?

Does this match exactly what you want? If not, what should I adjust?

````

---

#### Phase 3: Verification

**Agent**: claude-manager (with agent-creator skill)

**Sufficient context for quality**:
```yaml
Input needed:
  - Updated agent (from Phase 2: path and changes applied)
  - Verification checklist (structure, content, integration)

NOT needed:
  - Full change history (just verify current state)
  - Previous phase YAML outputs (verification focused)
````

**Prompt to claude-manager**:

````
You are verifying changes with agent-creator skill.

UPDATED AGENT (from Phase 2):
Path: [path]
Changes applied:
[List from Phase 2]

TASK:
Phase 3 - Verification

Verify updated agent:
1. Structure check (frontmatter valid, system prompt length)
2. Content check (thin router, no domain knowledge added)
3. Integration check (skills exist, tools valid, references updated)
4. Behavior check (description triggers, approach clear)

Verification checklist:
- [ ] Frontmatter valid YAML
- [ ] System prompt 50-200 lines
- [ ] Thin router maintained
- [ ] Skills referenced correctly
- [ ] Tools valid
- [ ] Description third-person
- [ ] Related files updated

Output format (YAML):
```yaml
verification:
  agent: [name]
  checks:
    structure:
      frontmatter_valid: [yes/no]
      system_prompt_length: [N lines - within range?]
    content:
      thin_router: [yes/no - maintained?]
      domain_knowledge_added: [yes/no - should be no]
    integration:
      skills_exist: [yes/no - all referenced skills exist?]
      tools_valid: [yes/no - all tools are valid?]
      references_updated: [yes/no - related files updated?]
  issues_found:
    - [issue if any]
  status: [success/issues_found]
````

```

**After claude-manager**:

Present verification results:
- All checks passed / Issues found
- Structure validation
- Content quality
- Integration check

Then:
```

Let me verify my understanding:
[2-3 sentence paraphrase of verification - passed checks, issues if any]

Clarifying questions:

1. Are all verification checks passing?
2. If issues found, should they be fixed immediately?
3. Is the agent ready for production use?
4. Should I test the agent with a sample task?
5. Any concerns about the changes made?

Does this match exactly what you want? If not, what should I adjust?

```

---

## Commands

- `continue` - Next phase
- `skip` - Skip current phase (not recommended for CREATE mode)
- `back` - Previous phase
- `popraw` - Correct understanding (during clarifying questions)
- `status` - Show progress
- `stop` - Exit command

---

## Thin Router Principle (Agents)

**Agents are infrastructure, skills are knowledge.**

**Agents should contain:**
- ✅ System prompt (how to approach tasks)
- ✅ Tool restrictions (Read-only, specific tools)
- ✅ Permission mode (auto-accept, bypass, plan)
- ✅ Model selection (sonnet, opus, haiku)

**Agents should NOT contain:**
- ❌ Domain knowledge (that's for skills)
- ❌ Detailed patterns (that's for skills)
- ❌ Code examples (that's for skills)
- ❌ Project-specific rules (that's for skills)

**Test question:**
> "Is this agent just infrastructure, or does it contain knowledge?"
> If contains knowledge → Move to skills

---

## Key Principles

**Agent Architecture:** Thin routers (infrastructure only), thick skills (domain knowledge)

**Clarifying Questions (MANDATORY):** After EVERY phase (including Phase 0) - paraphrase + 5 questions + confirmation before commands

**Signal Extraction:** Domain knowledge → skills, agent approach → system prompt

**User Checkpoints:** Get approval after confirmation (prevents wasted work)

**WHY Explanations:**
- Tool restrictions (WHY these tools?)
- Model choice (WHY this model?)
- Skills referenced (WHY these skills?)
