---
description: "Intelligent skill management - create, audit, or modify skills based on natural language"
---

# Manage Skill - Intelligent Skill Management

Automatically detects intent from natural language and executes appropriate skill management task: CREATE new skills, AUDIT existing skills for quality, or MODIFY skills to fix issues.

## Phases (Adaptive)

Phases are a checklist, not separate stops: merge them into as few ai-manager-agent spawns as the context allows.

**CREATE Mode:**
```
0: Intent Detection + Decision Framework    (orchestrator - inline)
1: Signal Extraction                         (ai-manager-agent)
2: Structure Design = PLAN                   (ai-manager-agent) → user approval
3: File Creation                             (ai-manager-agent — writes skill files)
4: Verification                              (orchestrator - inline, read-only)
```

**AUDIT Mode:**
```
0: Intent Detection + Scope                  (orchestrator - inline)
1: Structure Compliance                      (ai-manager-agent)
2: Content Quality Audit                     (ai-manager-agent)
3: Recommendations = PLAN                    (ai-manager-agent) → user approval
4: Implementation                            (ai-manager-agent — applies approved fixes)
```

**MODIFY Mode:**
```
0: Intent Detection + Change Scope           (orchestrator - inline)
1: Change Analysis = PLAN                    (ai-manager-agent) → user approval
2: Implementation                            (ai-manager-agent — applies approved changes)
3: Verification                              (orchestrator - inline, read-only)
```

---

## Orchestrator Instructions

**You are the orchestrator.** Invoke agents using the Task tool.

Use Task tool with `subagent_type="ai-manager-agent"`, description, prompt parameters. Wait for completion, show results to user.

[IMMEDIATELY invoke Task tool with subagent_type="ai-manager-agent" when phase requires agent]

### Critical Rules

1. **INVOKE with Task tool** - Every phase requires actual Task tool call (except Phase 0 and Verification which are inline). Implementation/File Creation phases MUST use ai-manager-agent — never do file edits inline. Inline Verification is read-only: any fix it finds goes back to ai-manager-agent, not into an inline Edit/Write.
2. **Sufficient context** - Each ai-manager-agent invocation gets ONLY critical decisions (not full conversation history)
3. **Ask once, only about assumptions; one consent point** - Ask the user in ONE message, and only when you are assuming something about scope, location (claude-dev / brain-vault/.claude / ~/.claude / the source of a symlink) or what the change applies to; otherwise merge phases and act. The only gate: present the plan → user approves (an approval already given in the request counts) → ai-manager-agent writes. **Why:** the old per-phase questions/paraphrase/gate ceremony ran in zero observed sessions, and Marcin's rule is "decide yourself, ask only about assumptions".
4. **Track mode** - Remember mode (CREATE/AUDIT/MODIFY) and what is already done
5. **Skill loading mechanism** - Agent sees ONLY skill metadata/description before deciding which skills to load. Full skill content loads only after agent's decision. Therefore: (1) skill descriptions must precisely describe WHEN to use (not "I help with X"), (2) command prompts should contain descriptive keywords matching skill descriptions (not explicit skill names - avoids tight coupling), (3) critical rules must be in command and agent system prompt - never rely solely on skills for enforcement.
6. **NEVER INVENT CONTENT** - ai-manager-agent must NEVER make up metrics, production incidents, anti-patterns, or numbers. ONLY use user-provided data. Placeholder when missing: `[User to provide: real metric/incident]`
7. **AVOID AI-KNOWN CONTENT** - ai-manager-agent must NOT include generic framework knowledge. Focus on project-specific patterns with WHY context. Example: ❌ "Repository pattern separates data access from business logic" → ✅ "Never query same table in RLS policy → infinite recursion (crashed prod)"
8. **Tier 3 organization** - Detailed examples >50 lines → move to `resources/`. SKILL.md references via `@resources/filename.md`. ONE LEVEL DEEP (no nested `@resources/ → @resources/`).

---

## Phase Details - Intent Detection (Universal Phase 0)

### Phase 0: Intent Detection and Mode Selection (Inline)
**You do this - no agent**

**Step 1: Detect Intent**

```yaml
CREATE indicators:
  - "create" / "new" / "need skill for [domain]"
  - Request describes functionality NOT in existing skills

AUDIT indicators:
  - "check" / "verify" / "audit" / "validate"
  - "signal vs noise" / "compliance" / "quality"
  - References EXISTING skill name + quality check
  - "all skills" (audit scope)

MODIFY indicators:
  - "update" / "fix" / "modify" / "change"
  - "add [pattern]" / "missing [anti-pattern]" / "improve"
  - References EXISTING skill name + specific change
  - "[skill] should have" / "drift fix"

Ambiguous:
  - Multiple indicators present
  - Unclear skill reference
  - No clear action verb
```

**Step 2: List Existing Skills (if needed for AUDIT/MODIFY)**

```bash
ls -d .claude/skills/*/ | sed 's|.claude/skills/||;s|/$||'
```

**Step 3: Determine Mode and Scope**

```yaml
Mode: [CREATE / AUDIT / MODIFY]
Scope:
  CREATE: [skill name from request]
  AUDIT: [specific skill or "all"]
  MODIFY: [skill name + changes requested]
Location: [claude-dev / brain-vault/.claude / ~/.claude / source of a symlink]
```

**Step 4:** If mode, scope, location or target is an assumption rather than something the request states, ask about it in ONE message (Critical Rule 3). Otherwise go straight to the mode's phases.

---

## Phase Details - CREATE Mode

### Phase 0: Decision Framework (Inline)
**You do this - no agent**

Apply 3-question filter:

```yaml
Question 1: Is this project-specific (not generic skill)?
Question 2: Is this timeless knowledge (won't change frequently)?
Question 3: Does this help Claude make better decisions?

VERDICT:
  3 YES: Create skill
  2 YES: Consider (marginal value, ask user)
  1 YES or less: Don't create (add to CLAUDE.md instead)
```

Settle inline: where the source material is, whether Tier 3 `resources/` is needed, and whether the skill does DETERMINISTIC work (parsing, extracting, filtering, counting, reshaping) over a LONG/LARGE input — that work belongs in a `scripts/` helper returning only the relevant slice; judgment stays in-context.

---

### Phase 1: Signal Extraction
**Agent**: ai-manager-agent (may be merged with Phase 2 into one spawn)

**Prompt to agent**:
```
MODE: CREATE skill - Signal extraction

SKILL NAME: [name]
SOURCE MATERIAL: [location from Phase 0]
DECISION FRAMEWORK: Passed (3 YES - project-specific, timeless, helps decisions)
TIER 3 NEEDED: [yes/no from Phase 0]

Task: Extract pure signal from source material using Signal vs Noise 3-question filter.

⚠️ CRITICAL: FACT-BASED EXTRACTION ONLY
User provides real data → extract it. No data → use placeholder or skip section.

Apply filter to EVERY piece of content:
- Actionable? (Can Claude act on this immediately?)
- Impactful? (Does this prevent bugs, save time, or improve quality?)
- Non-obvious? (Is this project-specific, not generic knowledge?)

ANY NO = NOISE → Cut immediately.

DO NOT include:
- Generic explanations (Claude already knows frameworks)
- Standard syntax examples (available in official docs)
- Obvious practices (basic coding standards)
- Historical evolution (focus on current state)

Extract categories:
1. Core patterns (SKILL.md content): decision frameworks, integration patterns, production context
2. Detailed examples (resources/ if >50 lines): complete code examples, sufficient guides
3. Utility scripts (scripts/ if needed): any DETERMINISTIC operation the skill performs — parsing, extracting, filtering, counting, reshaping — that runs over a LONG/LARGE input is a scripts/ candidate. The helper returns ONLY the relevant slice so the skill never loads the whole input into context to read it (cheaper, faster, more reliable signal-finding, keeps context clean). BOUNDARY: deterministic work only — any judgment/reasoning stays in-context, not in a script.

Output:
**Core Patterns (SKILL.md):** [list with WHY context]
**Detailed Examples (resources/):** [list examples >50 lines]
**Scripts (scripts/):** [list utility scripts]
**Noise Cut:** [what was excluded and why]
```

---

### Phase 2: Structure Design (the plan)
**Agent**: ai-manager-agent

**Prompt to agent**:
```
MODE: CREATE skill - Structure design

SKILL NAME: [name]

EXTRACTED SIGNAL (from Phase 1):
Core Patterns: [patterns with WHY]
Detailed Examples: [for resources/]
Scripts: [utility scripts]

Task: Design skill structure including Tier 2/3 decision and resource organization.

Structure decisions:

1. Tier 2 (SKILL.md):
   - Required sections: Purpose, When to Use, Core Patterns
   - Content quality > line count (600 lines pure signal > 300 with 50% noise)
   - Decision-focused (helps Claude choose)
   - Apply Signal vs Noise: No generic explanations, only project-specific decisions

2. Tier 3 (resources/):
   - Detailed examples >50 lines
   - Sufficient guides (step-by-step, focused not exhaustive)
   - Reference syntax: @resources/filename.md
   - ONE LEVEL DEEP: SKILL.md → @resources/file.md (no nested references)

3. Scripts (scripts/):
   - Utility scripts for skill functionality
   - Proper shebang, executable permissions
   - Referenced from SKILL.md with usage examples

Output:
**SKILL.md Structure:** [section breakdown with content allocation]
**resources/ Files:** [list with purpose and content summary]
**scripts/ Files:** [list with functionality]
**References Plan:** [where SKILL.md references resources/ and scripts/]
```

**Consent point:** show the plan (target path + structure) and wait for approval before Phase 3.

---

### Phase 3: File Creation (ai-manager-agent)
**Agent**: ai-manager-agent

**Prompt to agent**:
```
MODE: CREATE skill files

SKILL NAME: [name]
TARGET PATH: [.claude/skills/[skill-name]/ or ~/.claude/skills/[skill-name]/]

APPROVED STRUCTURE (from Phase 2):
[SKILL.md section breakdown, resources/ files, scripts/ files, references plan]

EXTRACTED SIGNAL (from Phase 1): [core patterns with WHY, examples, scripts]
USER DECISIONS (from plan approval): [corrections, inclusions, exclusions]

Task: Write the skill files yourself (Edit/Write) exactly per the approved structure.

1. SKILL.md: frontmatter (name + description with WHEN-to-use keyword triggers), required sections, @resources/ references
2. resources/ files (if Tier 3): self-contained, referenced FROM SKILL.md, ONE LEVEL DEEP
3. scripts/ files (if any): proper shebang, chmod +x, usage documented in SKILL.md

⚠️ CRITICAL: NEVER INVENT CONTENT — only approved signal; placeholder when data missing.

Output: Files created (absolute paths) + any point where the approved structure was ambiguous.
```

---

### Phase 4: Verification (Inline)
**You do this - no agent (read-only).** Read the files and run the checklist. If fixes are needed, spawn ai-manager-agent with the issue list (MODE: CREATE skill files - fixes) — never Edit/Write the skill files yourself.

```yaml
Structure:
  - [ ] SKILL.md at correct path with frontmatter
  - [ ] Required sections: Purpose, When to Use, Core Patterns
  - [ ] resources/ created (if Tier 3 needed)
  - [ ] scripts/ created (if scripts needed)

Content - Signal vs Noise per section:
  - [ ] No generic technology explanation
  - [ ] WHY over HOW (problem/rationale/impact)
  - [ ] No invented metrics/incidents
  - [ ] Production context included (if available)
  - [ ] Examples are project-specific

Tier 3:
  - [ ] resources/ files referenced from SKILL.md
  - [ ] ONE LEVEL DEEP (no nested @resources/ → @resources/)
  - [ ] resources/ files self-contained

References:
  - [ ] All @resources/ references point to existing files
  - [ ] Cross-references to other skills valid (if present)
```

Report the result (path, issues fixed or open). Skill creation complete.

---

## Phase Details - AUDIT Mode

### Phase 0: Scope Selection (Inline)
**You do this - no agent**

```yaml
SCOPE:
  specific: User provided skill name
  all: Audit all skills in .claude/skills/

SKILLS_FOUND:
  - List skill directories
  - Check each has SKILL.md
  - Note resources/ and scripts/ presence
```

---

### Phase 1: Structure Compliance
**Agent**: ai-manager-agent (Phases 1-3 may run as one spawn)

**Prompt to agent**:
```
MODE: AUDIT skills (structure compliance)

SKILLS: [list from Phase 0]
FOCUS: [structure/content/both]

Task: Analyze skill structure compliance.

For each skill, check:
1. File structure (SKILL.md, frontmatter, resources/ and scripts/ if referenced)
2. Required sections (Purpose, When to Use, Core Patterns)
3. Tier 3 organization (resources/ referenced via @resources/, no orphaned files, ONE LEVEL DEEP)
4. Scripts organized (proper shebang, executable, referenced from SKILL.md)
5. References valid (@resources/ exist, cross-references to other skills valid)

Output per skill: compliance score, missing sections/files, invalid references, issues (specific)
```

---

### Phase 2: Content Quality Audit
**Agent**: ai-manager-agent

**Prompt to agent**:
```
MODE: AUDIT skills (content quality)

SKILLS: [list]
STRUCTURE RESULTS: [from Phase 1]

Task: Audit content for Signal vs Noise and WHY over HOW violations.

⚠️ CRITICAL: FLAG INVENTED CONTENT
Flag invented metrics/incidents for removal. Recommend placeholders or deletion.

For each skill, check:

1. Signal vs Noise (3-question filter: Actionable? Impactful? Non-obvious?):
   - Generic explanations (frameworks Claude knows) = NOISE
   - Standard syntax examples = NOISE
   - INVENTED metrics or production incidents = FLAG for removal

2. WHY over HOW - patterns must include problem/rationale/impact

3. Current state vs historical timeline - skills show HOW TO USE NOW

4. Tier 3 violations - detailed examples >50 lines that should move to resources/

Output per skill: violations (quote/issue/fix), WHY missing, Tier 3 violations, severity (critical/moderate/minor)
```

---

### Phase 3: Recommendations (the plan)
**Agent**: ai-manager-agent

**Prompt to agent**:
```
MODE: AUDIT recommendations

STRUCTURE RESULTS: [Phase 1]
CONTENT RESULTS: [Phase 2]

Task: Create actionable recommendations for skill improvements.

For each skill with issues:
1. Structure fixes (missing sections, broken references, Tier 3 reorganization)
2. Content refactoring (noise to cut, WHY to add, historical timeline to replace)
3. Priority: critical (broken structure, missing WHY) → high (violations) → medium (Tier 3) → low (enhancements)
4. Migration plan (structure first, then content, then verification)

Output per skill: priority, structure fixes, content refactoring, Tier 3 changes, migration steps (ordered)
```

**Consent point:** show the recommendations and wait for approval (all, or which items) before Phase 4.

---

### Phase 4: Implementation (ai-manager-agent)
**Agent**: ai-manager-agent

**Only if user approved in Phase 3.**

**Prompt to agent**:
```
MODE: AUDIT implementation

⚠️ CRITICAL: NEVER INVENT OR HALLUCINATE CONTENT

SKILLS TO FIX: [list from Phase 3, priority order]

APPROVED RECOMMENDATIONS:
[Extracted per-skill fixes the user approved]

USER DECISIONS: [scope — all vs critical+high, from plan approval]

Task: Apply approved fixes to the skill files yourself (Edit/Write), per skill in priority order.

1. Structure fixes - add missing sections, fix broken references, reorganize Tier 3
2. Content refactoring - cut noise, add WHY, replace historical timeline
3. Tier 3 reorganization - move content >50 lines to resources/, add @resources/ references, verify ONE LEVEL DEEP
4. Verify per skill - structure checklist, Signal vs Noise, WHY context, references

Apply ONLY approved items — no extra improvements riding along.

Output: Summary of changes made, per file (absolute paths).
```

Report the changes. Audit complete.

---

## Phase Details - MODIFY Mode

### Phase 0: Change Scope (Inline)
**You do this - no agent**

```yaml
SKILL: [name from Universal Phase 0]
CHANGES_REQUESTED: [from user's natural language]

CHANGE_CATEGORIES:
  pattern_update: Add/update patterns or examples
  clarification: Improve existing content clarity
  anti_pattern: Add/update anti-patterns with WHY
  drift_fix: Update outdated information
  tier3_reorganization: Move content to/from resources/
  script_addition: Add utility scripts
```

---

### Phase 1: Change Analysis (the plan)
**Agent**: ai-manager-agent

**Prompt to agent**:
```
MODE: MODIFY skill

SKILL: [name and path]
CHANGES REQUESTED: [from Phase 0]
CATEGORIES: [pattern_update, clarification, anti_pattern, drift_fix, tier3_reorganization, script_addition]

Task: Analyze current skill state and plan modifications.

UPDATE STRATEGY:
- Update existing content (replace wrong with correct)
- Skills show HOW TO USE NOW, not historical evolution

Read skill file(s) and analyze:
1. Current state (sections, content)
2. Requested changes mapped to sections
3. Impact (dependencies, cross-references)
4. Approach per category:
   - pattern_update: Replace/enhance existing patterns
   - clarification: Improve existing content
   - anti_pattern: Add WHY context
   - drift_fix: UPDATE outdated info in-place
   - tier3_reorganization: Move content to/from resources/
   - script_addition: Add utility scripts with references

Output: Current State, Change Plan (section by section), Tier 3 Changes, Scripts Changes, Dependencies, Implementation Steps, Verification Checklist
```

**Consent point:** show the change plan and wait for approval before Phase 2.

---

### Phase 2: Implementation (ai-manager-agent)
**Agent**: ai-manager-agent

**Prompt to agent**:
```
MODE: MODIFY skill - implementation

SKILL: [name and path]

APPROVED CHANGE PLAN (from Phase 1):
[Section-by-section changes, Tier 3 changes, scripts changes, implementation steps]

USER DECISIONS (from plan approval): [corrections, approach choices]

Task: Apply the approved plan to the skill files yourself (Edit/Write).

Pattern updates: Replace outdated, enhance with WHY, apply Signal vs Noise
Drift fixes: UPDATE existing content in-place, replace with current state
Tier 3 reorganization: Move >50 lines to resources/, add @resources/ refs, verify ONE LEVEL DEEP
Script additions: Create scripts/ with shebang, chmod +x, add usage to SKILL.md

⚠️ CRITICAL: NEVER INVENT CONTENT. Apply ONLY approved changes — no extra improvements riding along.

Output: Changes made per file (absolute paths).
```

---

### Phase 3: Verification (Inline)
**You do this - no agent (read-only).** Read the files and run the checklist. If fixes are needed, spawn ai-manager-agent with the issue list (MODE: MODIFY skill - fixes) — never Edit/Write the skill files yourself.

```yaml
Structure:
  - [ ] Modified sections structurally correct
  - [ ] Tier 3 references valid

References:
  - [ ] All @resources/ references point to existing files
  - [ ] Cross-references to other skills still valid
  - [ ] No broken references introduced

Content:
  - [ ] Changes match approved plan
  - [ ] Signal focused (no new noise)
  - [ ] WHY context present
  - [ ] Current state focus

Tier 3 (if reorganized):
  - [ ] resources/ files created correctly
  - [ ] ONE LEVEL DEEP (no nested references)
```

Report the result (changes, issues fixed or open). Modification complete.
