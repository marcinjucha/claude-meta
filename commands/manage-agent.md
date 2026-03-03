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

---

## Orchestrator Instructions

### ⚠️ CRITICAL: YOU MUST INVOKE claude-manager

**You are the orchestrator.** Your job is to **ACTUALLY INVOKE claude-manager using the Task tool**.

**DO NOT**:
- ❌ Say "I will launch claude-manager"
- ❌ Describe what claude-manager will do
- ❌ Explain the phase without invoking
- ❌ Try to create/audit/modify agents yourself

**DO**:
- ✅ Immediately invoke Task tool with claude-manager
- ✅ Use subagent_type="claude-manager", description, prompt parameters
- ✅ Wait for claude-manager completion
- ✅ Show results to user

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
5. **Clarifying questions** - After EVERY phase, paraphrase + 3-5 questions (scale with complexity) + confirmation
6. **NEVER INVENT CONTENT** - claude-manager must NEVER make up metrics, production incidents, anti-patterns, or numbers. ONLY use user-provided data.
7. **AVOID AI-KNOWN CONTENT** - claude-manager must NOT include generic agent patterns Claude already knows. Focus on project-specific tool restrictions, hooks, and agent design decisions with WHY context. Example: ❌ "Agents route tasks to specialized execution contexts" → ✅ "Read-only agent prevents accidental edits during code review (incident: deleted config file)"

### Clarifying Questions Pattern

**After EVERY phase (including Phase 0), you MUST:**

```
Let me verify my understanding:
[2-3 sentence paraphrase of what was produced/decided in this phase]

Clarifying questions (3-5, scale with complexity):
1. [Question about scope/constraint from this phase]
2. [Question about tool restrictions/requirements]
3. [Question about priority/approach]
[4. Question about integration with skills/commands]
[5. Question about validation criteria]

Does this match exactly what you want to achieve? If not, what should I adjust?
```

**Wait for user response.** If corrections needed:
- Apply corrections
- Paraphrase updated understanding
- Ask 3-5 NEW clarifying questions about updated version
- Repeat until user confirms "dokładnie to co chcę" / "exactly what I want"

**Only after confirmation**, proceed with: "Ready to proceed? (continue/skip/back/stop)"

---

## Phase Details - Intent Detection (Universal Phase 0)

### Phase 0: Intent Detection and Mode Selection (Inline)

**You do this - no agent**

**Step 1: Detect Intent**

```yaml
CREATE indicators:
  - "create" / "new" / "need agent"
  - "agent for [new functionality]"
  - "creating specialist in [area]"
  - Describes specialized capability not in existing agents

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

Clarifying questions (3-5, scale with complexity):
1. Intent: Should I [CREATE new / AUDIT existing / MODIFY existing] agent?
2. Scope: Which agent - [detected name or list options]?
3. Goal: What's the primary objective - [inferred goal]?
[4. Priority: What's most important - [tool restrictions / skills / system prompt]?]
[5. Action: Should I [specific action] or did you mean [alternative]?]

Does this match exactly what you want? If not, what should I adjust?
```

[WAIT for confirmation]

**Step 5: Proceed to Mode-Specific Phase 0**

- CREATE → Continue to CREATE Mode Phase 0 (Decision Framework)
- AUDIT → Continue to AUDIT Mode Phase 0 (Scope Selection)
- MODIFY → Continue to MODIFY Mode Phase 0 (Change Scope)

Ready to proceed? (continue/skip/back/stop)

---

## Phase Details - CREATE Mode

### Phase 0: Decision Framework (Inline)

**You do this - no agent**

Quick assessment before creating agent:

1. **Does this need specific tool restrictions?** YES → agent; NO → use skill instead
2. **Does this need isolation?** YES → agent; NO → use skill
3. **Does this need specialized execution?** YES → agent; NO → use skill

**Decision:** If 2-3 YES → Continue. If 0-1 YES → Recommend skill or command instead.

Apply clarifying questions pattern, then: "Ready to proceed? (continue/skip/stop)"

---

### Phase 1: Signal Extraction

**Agent**: claude-manager (with agent-creator skill)

**Prompt to claude-manager**:
```
You are creating a new agent with agent-creator skill.

⚠️ CRITICAL: NEVER INVENT OR HALLUCINATE CONTENT
- DO NOT make up metrics, numbers, or production incidents
- ONLY extract what user actually provided
- If no production data exists, use placeholder: [User to provide real metric/incident]

AGENT PURPOSE (from Phase 0):
[Purpose statement, specialized capability]

REQUIREMENTS:
- Tool restrictions: [list or "standard access"]
- Isolation needed: [yes/no with reason]
- Model preference: [sonnet/opus/haiku or inherit]

TASK: Phase 1 - Signal Extraction

Extract signal (thin router infrastructure):
1. Identify approach/workflow (how agent tackles tasks)
2. Separate domain knowledge from approach (knowledge → skills)
3. Determine tool restrictions (only what's needed)
4. Identify skills to reference (existing skills for patterns)

Apply signal vs noise filter:
- Include: Task approach, tool restrictions rationale, when to delegate
- Exclude: Domain patterns (those go in skills), generic explanations

ANY NO = NOISE → Cut immediately.

Output format (YAML):
agent_approach: [steps]
tool_restrictions: allowed/denied/rationale
skills_to_reference: name/provides
domain_knowledge_removed: pattern/destination
```

Apply clarifying questions pattern, then: "Ready to proceed? (continue/skip/back/stop)"

---

### Phase 2: Structure Design

**Agent**: claude-manager (with agent-creator skill)

**Prompt to claude-manager**:
```
You are designing agent structure with agent-creator skill.

SIGNAL EXTRACTED (from Phase 1):
Agent approach: [steps]
Tool restrictions: allowed/denied/rationale
Skills to reference: [list]

TASK: Phase 2 - Structure Design

Design agent structure:
1. Frontmatter fields (name, description, tools, skills, model)
2. System prompt sections (role, steps, guidelines, output format)
3. Verify thin router (approach only, no domain patterns)
4. Third-person description (when to delegate)

Quality standards:
- Name: lowercase-with-hyphens, max 64 chars
- Description: third-person, triggers delegation, <1024 chars
- System prompt: focused on approach, not patterns (content quality > line count)
- Skills referenced (not duplicated)
- Apply Signal vs Noise: No generic explanations, only project-specific agent design

Output: YAML with frontmatter fields + system prompt sections + thin router verification
```

Apply clarifying questions pattern, then: "Ready to proceed? (continue/skip/back/stop)"

---

### Phase 3: File Creation

**Agent**: claude-manager (with agent-creator skill)

**Prompt to claude-manager**:
```
You are creating agent file with agent-creator skill.

AGENT STRUCTURE (from Phase 2):
Frontmatter: [YAML from Phase 2]
System prompt sections: [sections from Phase 2]

FILE LOCATION:
- Project agent: .claude/agents/[name].md (check into git)
- User agent: ~/.claude/agents/[name].md (personal workflow)

TASK: Phase 3 - File Creation

Create agent .md file:
1. Write frontmatter (YAML with proper formatting)
2. Write system prompt (markdown, focused on approach)
3. Verify file structure (frontmatter + body)
4. Create file at correct location

Quality checks:
- Frontmatter valid YAML
- System prompt focused on approach (not patterns)
- Skills referenced (not duplicated)
- Third-person description
- Thin router (infrastructure only)

Output: Created file path + content preview + verification checklist results
```

Apply clarifying questions pattern, then: "Ready to proceed? (continue/skip/back/stop)"

---

### Phase 4: Verification

**Agent**: claude-manager (with agent-creator skill)

**Prompt to claude-manager**:
```
You are verifying agent quality with agent-creator skill.

CREATED AGENT (from Phase 3):
File: [path]
Name: [name]
Tools: [list]
Skills: [list]

TASK: Phase 4 - Verification

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

Output: YAML verification results with issues and recommendations
```

Apply clarifying questions pattern. If all checks pass: CREATE mode complete.

---

## Phase Details - AUDIT Mode

### Phase 0: Scope Selection (Inline)

**You do this - no agent**

```yaml
SCOPE:
  specific: Audit single agent by name
  all: Audit all agents in .claude/agents/
```

List found agents with paths.

Apply clarifying questions pattern, then: "Ready to proceed? (continue/skip/stop)"

---

### Phase 1: Structure Compliance

**Agent**: claude-manager (with agent-creator skill)

**Prompt to claude-manager**:
```
You are auditing agent structure with agent-creator skill.

AGENTS TO AUDIT (from Phase 0):
[List of agent names and paths]

TASK: Phase 1 - Structure Compliance

For each agent, check:
1. Frontmatter validity (YAML parsing, required fields)
2. System prompt length (focused on approach)
3. File structure (frontmatter + body separation)
4. Field formats (name max 64 chars, description <1024 chars)

Structure requirements:
- name: lowercase-with-hyphens, max 64 chars
- description: third-person, <1024 chars
- tools/disallowedTools: valid tool names
- model: sonnet/opus/haiku/inherit
- skills: valid skill names

Output per agent: frontmatter_valid, name_format, description_length, system_prompt_length, issues (field/issue/severity), recommendations
```

Apply clarifying questions pattern, then: "Ready to proceed? (continue/skip/back/stop)"

---

### Phase 2: Content Quality

**Agent**: claude-manager (with agent-creator skill)

**Prompt to claude-manager**:
```
You are auditing agent content quality with agent-creator skill.

⚠️ CRITICAL: FLAG INVENTED CONTENT
Flag invented metrics/incidents for removal. Recommend placeholders or deletion.

AGENTS TO AUDIT: [list]
STRUCTURE ISSUES (from Phase 1): [critical issues only]

TASK: Phase 2 - Content Quality

Apply "ANY NO = NOISE" to existing agent content.

For each agent, check:
1. Thin router principle (infrastructure only, no domain patterns)
2. Domain knowledge in system prompt (should be in skills instead)
3. Skill references (skills listed, not duplicated)
4. WHY explanations (rationale for tool restrictions, approach)

Quality checks:
- System prompt focused on approach (not patterns)
- No code patterns in agent body (those go in skills)
- Tool restrictions justified (WHY these tools?)
- Third-person description (describes WHEN, not "I help")

Output per agent: thin_router check, domain_knowledge_found (pattern/should_be_in_skill), issues (type/description/severity), recommendations
```

Apply clarifying questions pattern, then: "Ready to proceed? (continue/skip/back/stop)"

---

### Phase 3: Integration Check

**Agent**: claude-manager (with agent-creator skill)

**Prompt to claude-manager**:
```
You are checking agent integration with agent-creator skill.

AGENTS TO AUDIT: [list with skills and tools from frontmatter]

TASK: Phase 3 - Integration Check

For each agent, verify:
1. Skills exist (all referenced skills are available in .claude/skills/)
2. Tools valid (allowed/disallowed tools are real tool names)
3. Description triggers (clear when to delegate)
4. Cross-references (commands reference this agent if applicable)

Output per agent: skills_exist (skill/exists/path), tools_valid, description_triggers, referenced_by, issues (type/description/severity), recommendations
```

Apply clarifying questions pattern, then: "Ready to proceed? (continue/skip/back/stop)"

---

### Phase 4: Recommendations

**Agent**: claude-manager (with agent-creator skill)

**Prompt to claude-manager**:
```
You are prioritizing recommendations with agent-creator skill.

AUDIT RESULTS (from Phases 1-3):
Structure issues: [from Phase 1]
Content issues: [from Phase 2]
Integration issues: [from Phase 3]

TASK: Phase 4 - Recommendations

Consolidate and prioritize fixes:
1. Group by severity (critical/warning/info)
2. Group by agent (if multiple)
3. Prioritize blocking issues first
4. Estimate effort (quick fix vs refactor)

Prioritization:
- CRITICAL: Blocks agent usage (missing skill, invalid tool, broken structure)
- WARNING: Reduces quality (domain knowledge in agent, weak description)
- INFO: Improvement opportunity (add WHY, third-person description)

Output: YAML recommendations per priority level + summary (total issues, critical count)
```

Apply clarifying questions pattern, then: "Ready to proceed with implementation? (continue/skip/back/stop)"

---

### Phase 5: Implementation (If Approved)

**Agent**: claude-manager (with agent-creator skill)

**Only if user approved in Phase 4.**

**Prompt to claude-manager**:
```
You are implementing fixes with agent-creator skill.

APPROVED FIXES (from Phase 4): [list]
AGENTS TO UPDATE: [names and paths]

TASK: Phase 5 - Implementation

For each approved fix:
1. Apply fix (update frontmatter, system prompt, or create file)
2. Verify fix (re-check issue resolved)
3. Update related files (if fix affects skills/commands)

Implementation steps:
- Frontmatter fixes: Update YAML fields
- System prompt fixes: Move domain knowledge to skills, add WHY
- Integration fixes: Create missing skills, fix tool names
- Description fixes: Rewrite to third-person with triggers

Output: fixes_applied (agent/fix/files_changed/verification), skills_created, issues_remaining
```

Apply clarifying questions pattern. AUDIT mode complete.

---

## Phase Details - MODIFY Mode

### Phase 0: Change Scope (Inline)

**You do this - no agent**

Categorize changes:
- **Frontmatter field** - name, description, tools, skills, model
- **System prompt section** - role, steps, guidelines, output format
- **Both** - frontmatter + system prompt

Apply clarifying questions pattern, then: "Ready to proceed? (continue/skip/stop)"

---

### Phase 1: Change Analysis

**Agent**: claude-manager (with agent-creator skill)

**Prompt to claude-manager**:
```
You are analyzing changes with agent-creator skill.

AGENT TO MODIFY (from Phase 0):
Name: [name]
Path: [path]

CHANGE SCOPE (from Phase 0):
Type: [Frontmatter / System prompt / Both]
Specific changes: [list]

TASK: Phase 1 - Change Analysis

Analyze impact:
1. What sections affected (frontmatter fields, system prompt sections)
2. Maintain thin router (changes don't add domain knowledge)
3. Update related references (skills, commands)
4. Verify consistency (all related fields updated)

Analysis checks:
- Changes maintain thin router principle
- No domain knowledge added to system prompt
- Tool restrictions still justified
- Skill references still valid
- Description still third-person with triggers

Output: YAML with changes_planned (frontmatter/system_prompt with current/new/rationale), impact (thin_router_maintained, related_updates_needed), verification checklist
```

Apply clarifying questions pattern, then: "Ready to proceed? (continue/skip/back/stop)"

---

### Phase 2: Implementation

**Agent**: claude-manager (with agent-creator skill)

**Prompt to claude-manager**:
```
You are implementing changes with agent-creator skill.

CHANGES PLANNED (from Phase 1):
Agent: [name], Path: [path]
Frontmatter changes: [list]
System prompt changes: [list]
Related updates: [list]

TASK: Phase 2 - Implementation

Apply changes:
1. Update agent file (frontmatter, system prompt)
2. Update related files (skills, commands)
3. Verify structure (frontmatter valid, system prompt)
4. Document changes (what changed, why)

Implementation steps:
- Frontmatter: Update YAML fields, maintain format
- System prompt: Update sections, maintain thin router
- Related files: Update references, cross-checks

Output: implementation results (agent_updated, related_updated, verification: structure_valid/thin_router_maintained/references_updated)
```

Apply clarifying questions pattern, then: "Ready to proceed? (continue/skip/back/stop)"

---

### Phase 3: Verification

**Agent**: claude-manager (with agent-creator skill)

**Prompt to claude-manager**:
```
You are verifying changes with agent-creator skill.

UPDATED AGENT (from Phase 2):
Path: [path]
Changes applied: [list]

TASK: Phase 3 - Verification

Verify updated agent:
1. Structure check (frontmatter valid, system prompt)
2. Content check (thin router, no domain knowledge added)
3. Integration check (skills exist, tools valid, references updated)
4. Behavior check (description triggers, approach clear)

Verification checklist:
- [ ] Frontmatter valid YAML
- [ ] Thin router maintained
- [ ] Skills referenced correctly
- [ ] Tools valid
- [ ] Description third-person
- [ ] Related files updated

Output: YAML verification with checks (structure/content/integration), issues_found, status (success/issues_found)
```

Apply clarifying questions pattern. MODIFY mode complete.

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
