---
description: "Intelligent skill management - create, audit, or modify skills based on natural language"
---

# Manage Skill - Intelligent Skill Management

Automatically detects intent from natural language and executes appropriate skill management task: CREATE new skills, AUDIT existing skills for compliance, or MODIFY skills to fix issues.

## Phases (Adaptive)

**CREATE Mode:**
```
0: Intent Detection + Decision Framework    (orchestrator - inline + clarifying questions)
1: Signal Extraction                         (claude-manager with skill-creator, signal-vs-noise)
2: Structure Design                          (claude-manager with skill-creator)
3: File Creation                             (orchestrator - inline)
4: Verification                              (orchestrator - inline + clarifying questions)
```

**AUDIT Mode:**
```
0: Intent Detection + Scope                  (orchestrator - inline + clarifying questions)
1: Structure Compliance                      (claude-manager with skill-creator, signal-vs-noise)
2: Content Quality Audit                     (claude-manager with signal-vs-noise, skill-creator)
3: Recommendations                           (claude-manager with skill-creator, signal-vs-noise)
4: Implementation                            (orchestrator - inline if user approves)
```

**MODIFY Mode:**
```
0: Intent Detection + Change Scope           (orchestrator - inline + clarifying questions)
1: Change Analysis                           (claude-manager with skill-fine-tuning, signal-vs-noise, skill-creator)
2: Implementation                            (orchestrator - inline)
3: Verification                              (orchestrator - inline + clarifying questions)
```

**Speed**: 5-20 min depending on mode and complexity

---

## Orchestrator Instructions

### Agent Invocation

**You are the orchestrator.** Invoke agents using the Task tool.

**Pattern:**
- Use Task tool with `subagent_type="claude-manager"`, description, prompt parameters
- Wait for agent completion
- Show results to user

**Example:**
```
Phase 1/4: Signal Extraction
Launching claude-manager...
```
[IMMEDIATELY invoke Task tool with subagent_type="claude-manager"]

---

## 🚫 ZERO HALLUCINATIONS POLICY

**ABSOLUTE REQUIREMENT - NO EXCEPTIONS:**

When creating or modifying skills, claude-manager must **NEVER invent:**
- ❌ Production metrics without user-provided data ("30% faster", "reduced by 50%")
- ❌ Production incidents without real examples from user
- ❌ Anti-patterns without user-verified mistakes
- ❌ Numbers, percentages, time measurements without source
- ❌ Team statistics or user impact claims
- ❌ Specific technical details not from source material

**ONLY include:**
- ✅ Content extracted from user-provided source material
- ✅ Real production incidents with user-verified context
- ✅ Patterns from actual codebase (files, commits, documentation)
- ✅ Placeholders when data missing: `[User to provide: real metric/incident]`

**ANY NO = HALLUCINATION → Use placeholder or skip section entirely.**

**Why this matters:** Invented content corrupts knowledge base, undermines trust in skills, causes wrong decisions.

---

### Critical Rules

1. **INVOKE with Task tool** - Every phase requires actual Task tool call (except Phase 0 and inline phases)
2. **Sufficient context** - Each claude-manager invocation gets ONLY critical decisions (not full conversation history)
3. **Clarifying questions MANDATORY** - After Phase 0 and EVERY agent phase, paraphrase + 5 questions + confirmation
4. **User checkpoints** - Get approval after confirmation before proceeding
5. **Track phase** - Remember current position and mode (CREATE/AUDIT/MODIFY)
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

**Analyze user's natural language request to determine mode.**

**Step 1: Detect Intent**

Analyze request for keywords and context:

```yaml
CREATE indicators:
  - "create" / "new" / "need skill for [domain]"
  - Request describes functionality NOT in existing skills
  - "skill for [specific task]"

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

If AUDIT or MODIFY detected, list skills in `.claude/skills/`:
```bash
ls -d .claude/skills/*/ | sed 's|.claude/skills/||;s|/$||'
```

**Step 3: Determine Mode and Scope**

```yaml
Mode: [CREATE / AUDIT / MODIFY]

Scope:
  CREATE: [skill name from request or ask]
  AUDIT: [specific skill or "all"]
  MODIFY: [skill name + changes requested]

Confidence: [HIGH / MEDIUM / LOW]
```

**Step 4: If Confidence LOW - Ask Clarifying Questions**

```
Let me verify my understanding:
[2-3 sentence paraphrase of detected intent]

Clarifying questions:
1. Intent: Should I [CREATE new / AUDIT existing / MODIFY existing] skill?
2. Scope: Which skill - [detected name or list options]?
3. Goal: What's the primary objective - [inferred goal]?
4. Priority: What's most important - [structure / content / both]?
5. Action: Should I [specific action] or did you mean [alternative]?

Does this match exactly what you want? If not, what should I adjust?
```

[WAIT for confirmation]

**Step 5: Proceed to Mode-Specific Phase 0**

Once mode determined with HIGH confidence:
- CREATE → Continue to CREATE Mode Phase 0 (Decision Framework)
- AUDIT → Continue to AUDIT Mode Phase 0 (Scope Selection)
- MODIFY → Continue to MODIFY Mode Phase 0 (Change Scope)

Ready to proceed? (continue/skip/back/stop)

---

## Phase Details - CREATE Mode

### Phase 0: Decision Framework (Inline)
**You do this - no agent**

**From Universal Phase 0: Mode=CREATE, Skill name determined**

Apply 3-question filter to determine if skill should be created:

```yaml
DECISION_FRAMEWORK:
  Question 1: Is this project-specific (not generic skill)?
    - YES: Project-specific architecture patterns, domain-specific integration logic, custom frameworks
    - NO: Generic coding, well-known frameworks, standard practices

  Question 2: Is this timeless knowledge (won't change frequently)?
    - YES: Architecture patterns, testing strategies, domain knowledge
    - NO: Temporary workarounds, version-specific fixes, experimental patterns

  Question 3: Does this help Claude make better decisions?
    - YES: Decision frameworks, anti-patterns with WHY, production context
    - NO: Pure information without guidance, HOW without WHY

VERDICT:
  - 3 YES: Create skill (high value)
  - 2 YES: Consider (marginal value, ask user)
  - 1 YES or less: Don't create (noise, add to CLAUDE.md instead)
```

**Output**: Decision framework results + verdict

**After Phase 0 - MANDATORY clarifying questions**:

```
Let me verify my understanding:
[2-3 sentence paraphrase of decision framework results]

Clarifying questions:
1. Source material location - where is the signal to extract (CLAUDE.md, conversation, files)?
2. Skill complexity - will this need Tier 3 resources/ (detailed examples >50 lines)?
3. Scripts needed - does this skill need utility scripts (scripts/ directory)?
4. Related skills - should this reference other existing skills?
5. Target: Skill should help Claude decide [specific decision] - correct?

Does this match exactly what you want? If not, what should I adjust?
```

[WAIT for user confirmation]

Ready to proceed? (continue/skip/back/stop)

---

### Phase 1: Signal Extraction
**Agent**: claude-manager

**Sufficient context for quality**:
```yaml
Input needed:
  - Mode: CREATE
  - Skill name
  - Decision framework results (3 YES from Phase 0)
  - Source material location (from Phase 0 clarifying questions)
  - Tier 3 complexity indication (from Phase 0)

NOT needed:
  - Full conversation history
  - Generic skill theory
  - Examples from other skills
```

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

ANY NO = NOISE → Cut from skill content immediately.

DO NOT include:
- Generic explanations (Claude already knows frameworks)
- Standard syntax examples (available in official docs)
- Obvious practices (basic coding standards)
- Historical evolution (focus on current state)

Extract categories:
1. **Core patterns** (SKILL.md content):
   - Decision frameworks (when/how to use)
   - Integration patterns (how layers connect)
   - Production context (real incidents, root causes, impact)

2. **Detailed examples** (resources/ if >50 lines):
   - Complete code examples with context
   - Comprehensive guides
   - Reference documentation

3. **Utility scripts** (scripts/ if needed):
   - Automation utilities
   - Helper scripts

Categorize content by destination:
- Tier 2 (SKILL.md): Interconnected patterns, decision guidance
- Tier 3 (resources/): Detailed examples >50 lines, comprehensive guides
- Scripts (scripts/): Utility automation

Use skill-creator and signal-vs-noise skills.

Output format:
**Core Patterns (SKILL.md):**
- [List patterns with WHY context]

**Detailed Examples (resources/):**
- [List examples >50 lines needing separate files]

**Scripts (scripts/):**
- [List utility scripts needed]

**Signal Summary:**
- Total items extracted
- Noise cut (what was excluded and why)
- Content categorization (Tier 2 vs Tier 3 vs scripts)
```

**After agent**:

Present extracted signal clearly.

```
Let me verify my understanding:
[2-3 sentence paraphrase of signal extracted and categorization]

Clarifying questions:
1. Extracted [N] patterns - is this complete or missing [specific pattern]?
2. Categorized [X] items as Tier 3 resources/ - should [item Y] be in SKILL.md instead?
3. Agent cut [noise items] as generic - do you want any of these included?
4. Scripts identified: [list] - are these the right utilities?
5. Missing production context for [pattern Z] - should I add placeholder or skip?

Does this match exactly what you want? If not, what should I adjust?
```

[WAIT for confirmation]

Ready to proceed? (continue/skip/back/stop)

---

### Phase 2: Structure Design
**Agent**: claude-manager

**Sufficient context for quality**:
```yaml
Input needed:
  - Extracted signal (from Phase 1: patterns, examples, scripts)
  - User confirmations/adjustments (from Phase 1 clarifying questions)
  - Skill name
  - Complexity level (Tier 3 resources needed?)

NOT needed:
  - Full Phase 1 conversation
  - Generic skill examples
  - Source material content
```

**Prompt to agent**:
```
MODE: CREATE skill - Structure design

SKILL NAME: [name]

EXTRACTED SIGNAL (from Phase 1):
**Core Patterns:**
[patterns with WHY context]

**Detailed Examples:**
[examples for resources/]

**Scripts:**
[utility scripts]

USER ADJUSTMENTS (from Phase 1):
[any corrections from clarifying questions]

Task: Design skill structure including Tier 2/3 decision and resource organization.

**Structure decisions:**

1. **Tier 2 (SKILL.md):**
   - Required sections: Purpose, When to Use, Core Patterns
   - Target: ~500 lines (150-600 acceptable)
   - Interconnected content (needs context)
   - Decision-focused (helps Claude choose)
   - Apply Signal vs Noise: No generic explanations, no standard practices, only project-specific decisions

2. **Tier 3 (resources/):**
   - Detailed examples >50 lines
   - Comprehensive guides (step-by-step)
   - Reference documentation
   - Move if: modular, detailed (>50 lines), separate concern
   - Reference syntax: `@resources/filename.md`
   - SKILL.md always read first, references resources/ when needed
   - Resources can reference OTHER skills if needed (cross-references OK)
   - ONE LEVEL DEEP: SKILL.md → @resources/file.md (no nested @resources/ → @resources/)
   - **Decision rule:** Detailed examples >50 lines → Move to resources/. SKILL.md references via @resources/filename.md

3. **Scripts (scripts/):**
   - Utility scripts for skill functionality
   - Proper shebang (#!/bin/bash, #!/usr/bin/env python3)
   - Executable permissions
   - Reference from SKILL.md with usage examples

**Design output:**
1. SKILL.md structure:
   - Section breakdown (Purpose, When to Use, Core Patterns)
   - Content allocation per section (~line count)
   - Cross-references to resources/ and scripts/

2. resources/ files (if Tier 3 needed):
   - List files with names and purpose
   - Content categorization (what goes in each file)
   - References from SKILL.md (where to reference each file)

3. scripts/ files (if needed):
   - List scripts with names and functionality
   - Usage documentation approach
   - Integration with SKILL.md

Use skill-creator skill for structure template.

Output format:
**SKILL.md Structure:**
- [Section-by-section breakdown with content allocation]

**resources/ Files:**
- [List files with purpose and content summary]

**scripts/ Files:**
- [List scripts with functionality]

**References Plan:**
- [Where SKILL.md references resources/ and scripts/]
```

**After agent**:

Present structure design.

```
Let me verify my understanding:
[2-3 sentence paraphrase of skill structure and file organization]

Clarifying questions:
1. SKILL.md has [N] sections totaling ~[X] lines - is this right scope?
2. resources/ includes [files] - should [content Y] be in SKILL.md instead of resources/?
3. Structure puts [pattern X] in [section] - does this make sense?
4. scripts/ includes [script A] - is this utility needed or over-engineering?
5. Cross-references: SKILL.md references [files] - complete or missing references?

Does this match exactly what you want? If not, what should I adjust?
```

[WAIT for confirmation]

Ready to proceed? (continue/skip/back/stop)

---

### Phase 3: File Creation (Inline)
**You do this - no agent**

Create skill files at `.claude/skills/[skill-name]/`:

**1. Create directory structure:**
```
.claude/skills/skill-name/
├── SKILL.md                # Main skill content
├── resources/              # If Tier 3 files needed from Phase 2
│   ├── example-1.md
│   └── guide.md
└── scripts/                # If scripts needed from Phase 2
    └── utility.sh
```

**2. Create SKILL.md:**
- Use structure from Phase 2 (sections, content allocation)
- Include frontmatter (description from Phase 2)
- Add required sections: Purpose, When to Use, Core Patterns
- Include references to Tier 3: `@resources/filename.md`
- Include script usage if applicable
- Apply skill-creator templates

**3. Create resources/ files (if designed in Phase 2):**
- Detailed examples or guides (>50 lines each)
- Referenced FROM SKILL.md via `@resources/filename.md`
- Can reference OTHER skills if needed (cross-references OK)
- Proper markdown formatting
- Self-contained content (no nested @resources/ → @resources/ references)

**4. Create scripts/ files (if designed in Phase 2):**
- Proper shebang (#!/bin/bash, #!/usr/bin/env python3)
- Executable permissions: `chmod +x .claude/skills/[skill-name]/scripts/*.sh`
- Usage documentation in comments
- Referenced from SKILL.md with usage examples

**Output**: File tree with paths and confirmation of creation

No clarifying questions (file creation is mechanical based on approved structure).

Ready to proceed? (continue/skip/back/stop)

---

### Phase 4: Verification (Inline)
**You do this - no agent**

Verify skill file(s) against quality checklist:

```yaml
Structure verification:
  - [ ] SKILL.md created at correct path
  - [ ] Frontmatter with description present
  - [ ] Required sections present (Purpose, When to Use, Core Patterns)
  - [ ] resources/ directory created (if Tier 3 needed)
  - [ ] scripts/ directory created (if scripts needed)

Content verification - Signal vs Noise per section:
  - [ ] Purpose: No generic technology explanation
  - [ ] When to Use: Decision framework (not generic "use when X")
  - [ ] Core Patterns: WHY over HOW (problem/rationale/impact)
  - [ ] No standard syntax examples (available in official docs)
  - [ ] No obvious practices (basic coding standards)
  - [ ] No invented metrics/incidents (only user-provided data)
  - [ ] Production context included (real incidents, root causes)
  - [ ] Examples are project-specific (not generic tutorials)

Tier 3 verification (if resources/ exists):
  - [ ] resources/ files referenced from SKILL.md (`@resources/filename.md`)
  - [ ] resources/ content is detailed (>50 lines or comprehensive guides)
  - [ ] resources/ can reference other skills (cross-references if needed)
  - [ ] ONE LEVEL DEEP: No nested @resources/ → @resources/ references
  - [ ] resources/ files are self-contained (complete within file)

Scripts verification (if scripts/ exists):
  - [ ] Proper shebang in all scripts
  - [ ] Executable permissions set (chmod +x)
  - [ ] Usage documentation in comments
  - [ ] Referenced from SKILL.md with usage examples

Reference verification:
  - [ ] All @resources/ references point to existing files
  - [ ] All script references accurate
  - [ ] Cross-references to other skills valid (if present)
  - [ ] No broken references

Quality verification:
  - [ ] 3-question filter passed (Actionable? Impactful? Non-obvious?)
  - [ ] Current state focused (HOW TO USE NOW)
  - [ ] Clear and scannable (headers, bullets, tables)
```

**Output**: Verification results + recommendations

```
Let me verify my understanding:
[2-3 sentence paraphrase of verification results]

Clarifying questions:
1. Verification found [N] issues - should I fix these automatically or show you first?
2. Missing [section/item X] - should this be added now or is it optional?
3. Signal vs Noise check: [item Y] seems generic - remove or keep with WHY?
4. Skill structure at [path] - should I add to skills list in documentation?
5. Skill is ready - should I commit this or do you want to review first?

Does this match your expectations? What should I adjust?
```

[WAIT for confirmation]

Skill creation complete! (or back to fix issues)

---

## Phase Details - AUDIT Mode

### Phase 0: Scope Selection (Inline)
**You do this - no agent**

**From Universal Phase 0: Mode=AUDIT, Scope determined (specific skill or "all")**

Determine which skills to audit:

```yaml
SCOPE:
  specific: User provided skill name
  all: Audit all skills in .claude/skills/

SKILLS_FOUND:
  - List skill directories
  - Check each has SKILL.md
  - Note resources/ and scripts/ presence
```

**Output**: Scope + list of skills to audit

**After Phase 0 - MANDATORY clarifying questions**:

```
Let me verify my understanding:
[2-3 sentence paraphrase of audit scope]

Clarifying questions:
1. Should I audit [N] skills found, or exclude some?
2. Priority focus - structure compliance, content quality (Signal vs Noise), or both?
3. If issues found, should I auto-fix or just report?
4. Should audit check Tier 3 resources/ organization and references?
5. What's the success criterion - all skills compliant, or report only?

Does this match what you want? If not, what should I adjust?
```

[WAIT for confirmation]

Ready to proceed? (continue/skip/back/stop)

---

### Phase 1: Structure Compliance
**Agent**: claude-manager

**Sufficient context for quality**:
```yaml
Input needed:
  - Mode: AUDIT
  - Skills to audit (names/paths from Phase 0)
  - Audit focus (from Phase 0: structure/content/both)
  - Auto-fix preference (from Phase 0)

NOT needed:
  - Full skill file contents (agent will read)
  - Generic skill theory
  - Conversation history
```

**Prompt to agent**:
```
MODE: AUDIT skills (structure compliance)

SKILLS: [list from Phase 0]
FOCUS: [structure/content/both]
AUTO_FIX: [yes/no from Phase 0]

Task: Analyze skill structure compliance.

For each skill, check:

1. **File structure present?**
   - [ ] SKILL.md exists
   - [ ] Frontmatter with description
   - [ ] resources/ directory (if referenced)
   - [ ] scripts/ directory (if referenced)

2. **Required sections in SKILL.md?**
   - [ ] Purpose section
   - [ ] When to Use section
   - [ ] Core Patterns section

4. **Tier 3 organization correct?**
   - [ ] resources/ files referenced from SKILL.md (`@resources/filename.md`)
   - [ ] No orphaned resources/ files (unreferenced)
   - [ ] ONE LEVEL DEEP: No nested @resources/ → @resources/ references
   - [ ] resources/ content is detailed (>50 lines or comprehensive)

5. **Scripts organized correctly?**
   - [ ] scripts/ files have proper shebang
   - [ ] Executable permissions set
   - [ ] Referenced from SKILL.md with usage examples

6. **References valid?**
   - [ ] All @resources/ references point to existing files
   - [ ] Cross-references to other skills valid (if present)
   - [ ] No broken references

Use skill-creator skill for structure reference.

Output format:
Per-skill report:
- Skill name
- Structure compliance score (N/M checks passed)
- Missing sections/files (list)
- Invalid references (list with details)
- Issues found (specific)
```

**After agent**:

Present structure analysis.

```
Let me verify my understanding:
[2-3 sentence paraphrase of compliance results]

Clarifying questions:
1. Found [N] skills with structure issues - should I fix these or just report?
2. Skill [X] missing [section Y] - critical or optional?
3. Some skills have broken @resources/ references - auto-fix or ask per skill?
4. Priority for fixes: [missing sections / broken references / Tier 3 organization]?
5. Should I proceed to content audit (Phase 2) or fix structure issues first?

Does this match your expectations? What should I adjust?
```

[WAIT for confirmation]

Ready to proceed? (continue/skip/back/stop)

---

### Phase 2: Content Quality Audit
**Agent**: claude-manager

**Sufficient context for quality**:
```yaml
Input needed:
  - Structure results (from Phase 1: which skills passed/failed structure)
  - User decisions (from Phase 1: auto-fix or report, priorities)
  - Skills to audit

NOT needed:
  - Full Phase 1 conversation
  - Generic examples
```

**Prompt to agent**:
```
MODE: AUDIT skills (content quality)

SKILLS: [list]
STRUCTURE RESULTS: [from Phase 1 - which skills passed/failed]
USER DECISIONS: [auto-fix or report, priorities from Phase 1]

Task: Audit skill content for Signal vs Noise and WHY over HOW violations.

⚠️ CRITICAL: FLAG INVENTED CONTENT
Flag invented metrics/incidents for removal. Recommend placeholders or deletion.
- Content should ONLY include user-provided real data

For each skill, check:

1. **Signal vs Noise violations:**
   Apply 3-question filter to content:
   - Actionable? (Can Claude act on this immediately?)
   - Impactful? (Does this prevent bugs, save time, or improve quality?)
   - Non-obvious? (Is this project-specific, not generic knowledge?)

   Violations (ANY NO = NOISE):
   - Generic explanations (frameworks Claude knows)
   - Standard syntax examples (available in docs)
   - Obvious practices (coding basics)
   - **INVENTED metrics or production incidents** (flag for removal)

2. **WHY over HOW violations:**
   Patterns must include:
   - Problem statement (what issue does this solve?)
   - Rationale (why this approach over alternatives?)
   - Impact (what happens if not followed?)

3. **Current state vs historical timeline:**
   Skills should show HOW TO USE NOW, not history.

4. **Tier 3 content in SKILL.md:**
   Check if detailed examples >50 lines should move to resources/.

Use signal-vs-noise and skill-creator skills.

Output format:
Per-skill report:
- Skill name
- Signal vs Noise violations (quote section, explain issue, suggest fix)
- WHY over HOW violations (quote section, explain issue, suggest fix)
- WHY context missing (list anti-patterns without WHY)
- Current state violations (sections with historical timeline)
- Tier 3 violations (content that should move to resources/)
- Severity (critical/moderate/minor)
```

**After agent**:

Present content audit results.

```
Let me verify my understanding:
[2-3 sentence paraphrase of violations found]

Clarifying questions:
1. Found [N] Signal vs Noise violations - should generic content be cut completely?
2. Skill [X] has patterns without WHY - add placeholders or skip?
3. Some skills have historical timeline sections - replace with current state?
4. [Skill Z] has detailed examples in SKILL.md - move to resources/?
5. Tier 3 organization needs fixing for [N] skills - proceed now or defer?

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
  - Structure analysis (Phase 1 results: missing sections, broken references)
  - Content audit (Phase 2 results: violations found per skill)
  - User decisions (priorities, auto-fix preferences)

NOT needed:
  - Full audit conversation
  - Generic refactoring theory
```

**Prompt to agent**:
```
MODE: AUDIT recommendations

STRUCTURE RESULTS: [Phase 1 - missing sections, broken references, Tier 3 issues]
CONTENT RESULTS: [Phase 2 - Signal vs Noise violations, WHY violations, etc.]
USER DECISIONS: [priorities, auto-fix preferences]

Task: Create actionable recommendations for skill improvements.

For each skill with issues:

1. **Structure fixes** (from Phase 1)
   - Missing sections to add (list with templates)
   - Broken references to fix (specific files)
   - Tier 3 organization (content to move to resources/)
   - Scripts to add/fix (if needed)

2. **Content refactoring** (from Phase 2)
   - Noise to cut (generic explanations, obvious practices)
   - WHY to add (patterns needing problem/rationale/impact)
   - Historical timeline to replace (current state focus)

3. **Priority order**
   - Critical (broken structure, missing WHY in anti-patterns)
   - High (Signal vs Noise violations, missing sections)
   - Medium (Tier 3 reorganization, clarity improvements)
   - Low (minor enhancements)

4. **Migration plan**
   - Fix structure first (sections, references, Tier 3)
   - Then content quality (cut noise, add WHY)
   - Then enhancements (clarity, examples)
   - Verification steps per skill

Use skill-creator and signal-vs-noise skills.

Output format:
Per-skill recommendations:
- Skill name
- Priority (critical/high/medium/low)
- Structure fixes (specific with file paths)
- Content refactoring (specific sections with changes)
- Tier 3 changes (content to move to resources/, new files needed)
- Migration steps (ordered 1, 2, 3...)
```

**After agent**:

Present recommendations.

```
Let me verify my understanding:
[2-3 sentence paraphrase of recommended changes]

Clarifying questions:
1. Recommendations suggest [N] critical fixes - should I do these in Phase 4?
2. Priority order: [skill A] → [skill B] → [skill C] - correct?
3. Some fixes require Tier 3 reorganization (moving content to resources/) - proceed?
4. Estimated time for all fixes: [duration] - acceptable?
5. Should I implement all recommendations or just critical + high priority?

Does this match your expectations? What should I adjust?
```

[WAIT for confirmation]

Ready to proceed with implementation? (continue/skip/back/stop)

---

### Phase 4: Implementation (Inline - Conditional)
**You do this - no agent**

**Only if user approved in Phase 3.**

Apply recommended changes per skill:

**For each skill (in priority order):**

```yaml
1. Structure fixes:
   - Add missing sections (use skill-creator templates)
   - Fix broken references (@resources/, cross-references)
   - Reorganize Tier 3 (move content >50 lines to resources/)
   - Add/fix scripts/ (proper shebang, permissions, references)

2. Content refactoring:
   - Cut noise (generic explanations, obvious practices)
   - Add WHY context:
     * Patterns: problem statement + rationale + impact
   - Replace historical timeline with current state
   - Apply Signal vs Noise 3-question filter

3. Tier 3 reorganization (if needed):
   - Move detailed examples >50 lines to resources/
   - Create resources/ files with proper names
   - Add @resources/ references to SKILL.md
   - Verify ONE LEVEL DEEP (no nested references)

4. Verification per skill:
   - Run structure checklist
   - Apply Signal vs Noise filter
   - Check WHY context present
   - Verify references valid
```

**Output**: Summary of changes per skill

```
Let me verify my understanding:
[2-3 sentence paraphrase of changes made]

Clarifying questions:
1. Made [N] changes to [M] skills - should I commit these?
2. Created [X] new resources/ files - are these organized correctly?
3. Some skills still have minor issues [list] - fix now or later?
4. Should I create pull request with changes or just local commit?
5. Verification passed for [N] skills - what about remaining [M]?

Does this match your expectations? What should I adjust?
```

[WAIT for confirmation]

Audit complete!

---

## Phase Details - MODIFY Mode

### Phase 0: Change Scope (Inline)
**You do this - no agent**

**From Universal Phase 0: Mode=MODIFY, Skill name and changes determined**

Analyze requested changes and categorize:

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

**Output**: Change scope + category breakdown + complexity

**After Phase 0 - MANDATORY clarifying questions**:

```
Let me verify my understanding:
[2-3 sentence paraphrase of changes to make]

Clarifying questions:
1. Scope: Should changes affect [specific sections] or entire skill?
2. Category: Is this primarily [category A] or [category B]?
3. Approach: Should I [approach A] or [approach B] for [specific change]?
4. Update strategy: UPDATE existing content (replace wrong) or ADD history section?
5. Verification: After changes, full quality check or just changed sections?

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
  - Skill name and path
  - Changes requested with categories (from Phase 0)
  - User confirmations/adjustments (from Phase 0 clarifying questions)

NOT needed:
  - Full skill content (agent will read)
  - Generic modification theory
  - Conversation history
```

**Prompt to agent**:
```
MODE: MODIFY skill

SKILL: [name and path]
CHANGES REQUESTED: [from Phase 0]
CATEGORIES: [pattern_update, clarification, anti_pattern, drift_fix, tier3_reorganization, script_addition]
USER ADJUSTMENTS: [from Phase 0 clarifying questions]

Task: Analyze current skill state and plan modifications.

UPDATE STRATEGY:
- Update existing content (replace wrong with correct)
- Skills show HOW TO USE NOW, not historical evolution
- Replace outdated patterns with current patterns in-place

Read skill file(s) and analyze:
1. Current state (what exists now, what sections present)
2. Requested changes mapped to sections (what needs to change where)
3. Impact (dependencies, cross-references affected)
4. Approach for each category:
   - pattern_update: Replace/enhance existing patterns
   - clarification: Improve existing content
   - anti_pattern: Add WHY context (WHAT to avoid + WHY it's wrong)
   - drift_fix: UPDATE outdated info (replace with current state)
   - tier3_reorganization: Move content to/from resources/
   - script_addition: Add utility scripts with references

Use skill-fine-tuning, signal-vs-noise, and skill-creator skills.

Output format:
**Current State:**
- [Summary of existing skill structure and content]

**Change Plan (section by section):**
1. [Section name]: [Specific changes to make]
2. [Section name]: [Specific changes to make]
...

**Tier 3 Changes (if applicable):**
- [Resources to add/modify/move]

**Scripts Changes (if applicable):**
- [Scripts to add with functionality]

**Dependencies:**
- [Cross-references to update, related skills affected]

**Implementation Steps:**
1. [Ordered steps to apply changes]
2. ...

**Verification Checklist:**
- [How to verify changes correct]
```

**After agent**:

Present change plan.

```
Let me verify my understanding:
[2-3 sentence paraphrase of change plan]

Clarifying questions:
1. Plan suggests [N] modifications - is this complete or should I add [X]?
2. Change order: [A] → [B] → [C] - correct priority?
3. Section [X] will be [modified/enhanced/replaced] - is this what you want?
4. Plan updates existing content - correct approach?
5. After changes, skill will [outcome] - matches your goal?

Does this match exactly what you want? If not, what should I adjust?
```

[WAIT for confirmation]

Ready to proceed? (continue/skip/back/stop)

---

### Phase 2: Implementation (Inline)
**You do this - no agent**

Apply modifications from Phase 1 plan:

**For each modification:**

```yaml
Pattern updates:
  - Replace outdated patterns with current state
  - Enhance existing patterns (add WHY if missing)
  - Apply Signal vs Noise filter (cut generic content)
  - Update examples to reflect current practices

Clarification improvements:
  - Improve existing content clarity
  - Replace ambiguous statements with specific guidance
  - Add WHY context where missing (problem/rationale/impact)
  - Simplify complex explanations

Drift fixes:
  - UPDATE existing content (replace wrong information)
  - Replace outdated patterns with current patterns
  - Fix incorrect information
  - Current state focus

Tier 3 reorganization:
  - Move detailed examples >50 lines to resources/
  - Create new resources/ files if needed
  - Add @resources/ references to SKILL.md
  - Verify ONE LEVEL DEEP (no nested references)

Script additions:
  - Create scripts/ directory if needed
  - Add utility scripts with proper shebang
  - Set executable permissions (chmod +x)
  - Add usage examples to SKILL.md
```

**Output**: Summary of changes made (section by section)

No clarifying questions (implementation is mechanical based on approved plan).

Ready to proceed? (continue/skip/back/stop)

---

### Phase 3: Verification (Inline)
**You do this - no agent**

Verify modifications against quality standards:

```yaml
Structure verification:
  - [ ] Modified sections structurally correct
  - [ ] Tier 3 references valid (@resources/)

Reference verification:
  - [ ] All @resources/ references still point to existing files
  - [ ] All cross-references to other skills still valid
  - [ ] No broken references introduced by changes
  - [ ] Script references accurate (if modified)

Content verification:
  - [ ] Changes match approved plan
  - [ ] Signal focused (no new noise introduced)
  - [ ] WHY context present (patterns and anti-patterns)
  - [ ] Current state focus
  - [ ] Updated existing content

Quality verification:
  - [ ] 3-question filter passed (Actionable? Impactful? Non-obvious?)
  - [ ] WHY over HOW (problem/rationale/impact for patterns)
  - [ ] Production context included (if applicable)

Tier 3 verification (if reorganized):
  - [ ] resources/ files created correctly
  - [ ] @resources/ references work
  - [ ] ONE LEVEL DEEP (no nested references)
  - [ ] Content >50 lines moved to resources/

Scripts verification (if added):
  - [ ] Proper shebang present
  - [ ] Executable permissions set
  - [ ] Referenced from SKILL.md with usage
```

**Output**: Verification results + file path

```
Let me verify my understanding:
[2-3 sentence paraphrase of changes made and verification status]

Clarifying questions:
1. Made [N] changes to [sections] - all correct?
2. Verification found [N] issues - should I fix automatically or show you?
3. Modified skill ready at [path] - should I commit or let you review?
4. Changes improve [aspect] - does this achieve your goal?
5. Updated existing content - is this the right approach?

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

- ✅ Mode (CREATE/AUDIT/MODIFY)
- ✅ Critical decisions from previous phases (extracted, not full conversation)
- ✅ User confirmations/adjustments (from clarifying questions)
- ✅ Specific task for this phase
- ✅ Expected output format

**Test question**:

> "Can claude-manager produce HIGH QUALITY output with this context alone?"
>
> If YES → sufficient
> If NO → add missing critical info (not everything)

**Example - Phase 2 context (CREATE mode):**
```yaml
✅ SUFFICIENT (50 lines):
  Extracted signal from Phase 1:
  - Core patterns: [list with WHY]
  - Tier 3 examples: [list]
  - Scripts: [list]
  User adjustments: [specific corrections]

❌ TOO MUCH (500 lines):
  Full Phase 1 conversation including all agent outputs

❌ INSUFFICIENT (10 lines):
  "Use signal from Phase 1"
  (Missing what signal was extracted)
```

---

## Key Principles

**Signal vs Noise is GATE:** 3-question filter (Actionable? Impactful? Non-obvious?) applied before any content. ANY NO = NOISE.

**WHY > HOW:** Patterns need problem/rationale/impact.

**Nothing AI knows:** Cut generic explanations, frameworks, standard practices.

**Current state focus:** Skills show HOW TO USE NOW. Update existing content.

**Production context:** Real incidents, root causes, impact statements.

**Tier 3 organization:** Detailed examples >50 lines move to resources/. SKILL.md references via `@resources/filename.md`. ONE LEVEL DEEP (no nested references).

**Clarifying Questions MANDATORY:** After Phase 0 and EVERY agent phase (paraphrase + 5 questions + confirmation).

**Sufficient Context:** Extract decisions only (50 lines vs 500 lines full output). Test question: "Can agent produce HIGH QUALITY with this?"

**Quality > Brevity:** 600 lines pure signal > 300 lines with 50% noise.
