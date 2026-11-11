---
description: "Intelligent agent management - create, audit, or modify agents based on natural language"
---

# Manage Agent - Intelligent Agent Management

Automatically detects intent from natural language and executes appropriate agent management task: CREATE new agents, AUDIT existing agents for quality, or MODIFY agents to fix issues.

## Phases (Adaptive)

**CREATE Mode:**
```
0: Intent Detection + Decision Framework    (orchestrator - inline)
1: Signal Extraction                         (ai-manager-agent)
2: Structure Design = PLAN                   (ai-manager-agent) → user approval
3: File Creation                             (ai-manager-agent)
4: Verification                              (ai-manager-agent)
```

**AUDIT Mode:**
```
0: Intent Detection + Scope                  (orchestrator - inline)
1: Structure Compliance                      (ai-manager-agent)
2: Content Quality                           (ai-manager-agent)
3: Integration Check                         (ai-manager-agent)
4: Recommendations = PLAN                    (ai-manager-agent) → user approval
5: Implementation                            (ai-manager-agent - if approved)
```

**MODIFY Mode:**
```
0: Intent Detection + Change Scope           (orchestrator - inline)
1: Change Analysis = PLAN                    (ai-manager-agent) → user approval
2: Implementation                            (ai-manager-agent)
3: Verification                              (ai-manager-agent)
```

---

## Orchestrator Instructions

### ⚠️ CRITICAL: YOU MUST INVOKE ai-manager-agent

**You are the orchestrator.** Your job is to **ACTUALLY INVOKE ai-manager-agent using the Task tool**.

**DO NOT**:
- ❌ Say "I will launch ai-manager-agent"
- ❌ Describe what ai-manager-agent will do
- ❌ Explain the phase without invoking
- ❌ Try to create/audit/modify agents yourself

**DO**:
- ✅ Immediately invoke Task tool with ai-manager-agent
- ✅ Use subagent_type="ai-manager-agent", description, prompt parameters
- ✅ Wait for ai-manager-agent completion
- ✅ Show results to user

**Example**:
```
Phase 1/4: Signal Extraction
Launching ai-manager-agent...
```
[IMMEDIATELY invoke Task tool NOW with subagent_type="ai-manager-agent"]

### Critical Rules

1. **INVOKE with Task tool** - Every phase requires actual Task tool call to ai-manager-agent
2. **Signal extraction** - Domain knowledge goes in skills, NOT agents (thin router principle)
3. **Ask once, only about assumptions; one consent point** - Ask the user in ONE message, and only when you are assuming something about scope, location (claude-dev / brain-vault/.claude / ~/.claude / the source of a symlink) or what the change applies to; otherwise merge phases and act. The only gate: present the plan → user approves (an approval already given in the request counts) → ai-manager-agent writes. **Why:** the old per-phase questions/paraphrase/gate ceremony ran in zero observed sessions, and Marcin's rule is "decide yourself, ask only about assumptions".
4. **Track mode** - Remember mode (CREATE/AUDIT/MODIFY) and what is already done
5. **Skill loading mechanism** - Agent sees ONLY skill metadata/description before deciding which skills to load. Full skill content loads only after agent's decision. Therefore: (1) skill descriptions must precisely describe WHEN to use (not "I help with X"), (2) command prompts should contain descriptive keywords matching skill descriptions (not explicit skill names - avoids tight coupling), (3) critical rules must be in command and agent system prompt - never rely solely on skills for enforcement.
6. **NEVER INVENT CONTENT** - ai-manager-agent must NEVER make up metrics, production incidents, anti-patterns, or numbers. ONLY use user-provided data.
7. **AVOID AI-KNOWN CONTENT** - ai-manager-agent must NOT include generic agent patterns Claude already knows. Focus on project-specific tool restrictions, hooks, and agent design decisions with WHY context. Example: ❌ "Agents route tasks to specialized execution contexts" → ✅ "Read-only agent prevents accidental edits during code review (incident: deleted config file)"

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
  CREATE: [agent name from request]
  AUDIT: [specific agent or "all"]
  MODIFY: [agent name + changes requested]

Location: [claude-dev / brain-vault/.claude / ~/.claude / source of a symlink]
```

**Step 4:** If mode, scope, location or target is an assumption rather than something the request states, ask about it in ONE message (Critical Rule 3).

**Step 5: Proceed to Mode-Specific Phase 0**

- CREATE → Continue to CREATE Mode Phase 0 (Decision Framework)
- AUDIT → Continue to AUDIT Mode Phase 0 (Scope Selection)
- MODIFY → Continue to MODIFY Mode Phase 0 (Change Scope)

---

## Phase Details - CREATE Mode

### Phase 0: Decision Framework (Inline)

**You do this - no agent**

Quick assessment before creating agent:

1. **Does this need specific tool restrictions?** YES → agent; NO → use skill instead
2. **Does this need isolation?** YES → agent; NO → use skill
3. **Does this need specialized execution?** YES → agent; NO → use skill

**Decision:** If 2-3 YES → Continue. If 0-1 YES → Recommend skill or command instead.

---

### Phase 1: Signal Extraction

**Agent**: ai-manager-agent

**Prompt to ai-manager-agent**:
```
You are creating a new agent. Apply thin router architecture, tool restrictions design, and agent frontmatter patterns.

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

---

### Phase 2: Structure Design

**Agent**: ai-manager-agent

**Prompt to ai-manager-agent**:
```
You are designing agent structure. Apply thin router architecture and frontmatter design patterns.

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

**Consent point:** show the plan (location + structure) and wait for approval before Phase 3.

---

### Phase 3: File Creation

**Agent**: ai-manager-agent

**Prompt to ai-manager-agent**:
```
You are creating agent file. Apply agent frontmatter format and system prompt patterns.

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

---

### Phase 4: Verification

**Agent**: ai-manager-agent

**Prompt to ai-manager-agent**:
```
You are verifying agent quality. Check thin router compliance, frontmatter validity, and system prompt quality.

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

If all checks pass: CREATE mode complete.

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

---

### Phase 1: Structure Compliance

**Agent**: ai-manager-agent

**Prompt to ai-manager-agent**:
```
You are auditing agent structure compliance.

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

---

### Phase 2: Content Quality

**Agent**: ai-manager-agent

**Prompt to ai-manager-agent**:
```
You are auditing agent content quality. Check thin router principle and signal vs noise compliance.

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

---

### Phase 3: Integration Check

**Agent**: ai-manager-agent

**Prompt to ai-manager-agent**:
```
You are checking agent integration - skills existence, tools validity, cross-references.

AGENTS TO AUDIT: [list with skills and tools from frontmatter]

TASK: Phase 3 - Integration Check

For each agent, verify:
1. Skills exist (all referenced skills are available in .claude/skills/)
2. Tools valid (allowed/disallowed tools are real tool names)
3. Description triggers (clear when to delegate)
4. Cross-references (commands reference this agent if applicable)

Output per agent: skills_exist (skill/exists/path), tools_valid, description_triggers, referenced_by, issues (type/description/severity), recommendations
```

---

### Phase 4: Recommendations

**Agent**: ai-manager-agent

**Prompt to ai-manager-agent**:
```
You are prioritizing audit recommendations by severity.

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

**Consent point:** show the recommendations and wait for approval before Phase 5.

---

### Phase 5: Implementation (If Approved)

**Agent**: ai-manager-agent

**Only if user approved in Phase 4.**

**Prompt to ai-manager-agent**:
```
You are implementing approved agent fixes.

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

AUDIT mode complete.

---

## Phase Details - MODIFY Mode

### Phase 0: Change Scope (Inline)

**You do this - no agent**

Categorize changes:
- **Frontmatter field** - name, description, tools, skills, model
- **System prompt section** - role, steps, guidelines, output format
- **Both** - frontmatter + system prompt

---

### Phase 1: Change Analysis

**Agent**: ai-manager-agent

**Prompt to ai-manager-agent**:
```
You are analyzing agent modifications. Check thin router compliance and impact on related files.

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

**Consent point:** show the change plan and wait for approval before Phase 2.

---

### Phase 2: Implementation

**Agent**: ai-manager-agent

**Prompt to ai-manager-agent**:
```
You are implementing agent changes. Update frontmatter and system prompt.

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

---

### Phase 3: Verification

**Agent**: ai-manager-agent

**Prompt to ai-manager-agent**:
```
You are verifying agent changes. Check thin router compliance and reference integrity.

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

MODIFY mode complete.

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
