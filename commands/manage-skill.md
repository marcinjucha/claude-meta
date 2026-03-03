---
description: "Intelligent skill management - create, audit, or modify skills based on natural language"
---

# Manage Skill - Intelligent Skill Management

Automatically detects intent from natural language and executes appropriate skill management task: CREATE new skills, AUDIT existing skills for quality, or MODIFY skills to fix issues.

## Phases (Adaptive)

**CREATE Mode:**
```
0: Intent Detection + Decision Framework    (orchestrator - inline + clarifying questions)
1: Signal Extraction                         (claude-manager)
2: Structure Design                          (claude-manager)
3: File Creation                             (orchestrator - inline)
4: Verification                              (orchestrator - inline)
```

**AUDIT Mode:**
```
0: Intent Detection + Scope                  (orchestrator - inline + clarifying questions)
1: Structure Compliance                      (claude-manager)
2: Content Quality Audit                     (claude-manager)
3: Recommendations                           (claude-manager)
4: Implementation                            (orchestrator - inline if approved)
```

**MODIFY Mode:**
```
0: Intent Detection + Change Scope           (orchestrator - inline + clarifying questions)
1: Change Analysis                           (claude-manager)
2: Implementation                            (orchestrator - inline)
3: Verification                              (orchestrator - inline)
```

---

## Orchestrator Instructions

**You are the orchestrator.** Invoke agents using the Task tool.

Use Task tool with `subagent_type="claude-manager"`, description, prompt parameters. Wait for completion, show results to user.

[IMMEDIATELY invoke Task tool with subagent_type="claude-manager" when phase requires agent]

### Critical Rules

1. **INVOKE with Task tool** - Every phase requires actual Task tool call (except Phase 0 and inline phases)
2. **Sufficient context** - Each claude-manager invocation gets ONLY critical decisions (not full conversation history)
3. **Clarifying questions MANDATORY** - After Phase 0 and EVERY agent phase, paraphrase + 3-5 questions (scale with complexity) + confirmation
4. **User checkpoints** - Get approval after confirmation before proceeding
5. **Track phase** - Remember current position and mode (CREATE/AUDIT/MODIFY)
6. **NEVER INVENT CONTENT** - claude-manager must NEVER make up metrics, production incidents, anti-patterns, or numbers. ONLY use user-provided data. Placeholder when missing: `[User to provide: real metric/incident]`
7. **AVOID AI-KNOWN CONTENT** - claude-manager must NOT include generic framework knowledge. Focus on project-specific patterns with WHY context. Example: ❌ "Repository pattern separates data access from business logic" → ✅ "Never query same table in RLS policy → infinite recursion (crashed prod)"
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
  CREATE: [skill name from request or ask]
  AUDIT: [specific skill or "all"]
  MODIFY: [skill name + changes requested]
Confidence: [HIGH / MEDIUM / LOW]
```

**Step 4: If Confidence LOW - Ask Clarifying Questions**

```
Let me verify my understanding:
[2-3 sentence paraphrase]

Clarifying questions (3-5, scale with complexity):
1. Intent: Should I [CREATE new / AUDIT existing / MODIFY existing] skill?
2. Scope: Which skill - [detected name or list options]?
3. Goal: What's the primary objective - [inferred goal]?
[4. Priority: What's most important - [structure / content / both]?]
[5. Action: Should I [specific action] or did you mean [alternative]?]

Does this match exactly what you want?
```

[WAIT for confirmation]

**Step 5: Proceed to Mode-Specific Phase 0**

- CREATE → Phase 0: Decision Framework
- AUDIT → Phase 0: Scope Selection
- MODIFY → Phase 0: Change Scope

Ready to proceed? (continue/skip/back/stop)

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

```
Let me verify my understanding:
[2-3 sentence paraphrase of decision results]

Clarifying questions (3-5, scale with complexity):
1. Source material location - where is the signal to extract?
2. Skill complexity - will this need Tier 3 resources/ (detailed examples >50 lines)?
3. Scripts needed - does this skill need utility scripts (scripts/ directory)?
[4. Related skills - should this reference other existing skills?]
[5. Target: Skill should help Claude decide [specific decision] - correct?]

Does this match exactly what you want?
```

[WAIT for user confirmation]

Ready to proceed? (continue/skip/back/stop)

---

### Phase 1: Signal Extraction
**Agent**: claude-manager

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
3. Utility scripts (scripts/ if needed): automation utilities

Output:
**Core Patterns (SKILL.md):** [list with WHY context]
**Detailed Examples (resources/):** [list examples >50 lines]
**Scripts (scripts/):** [list utility scripts]
**Noise Cut:** [what was excluded and why]
```

```
Let me verify my understanding:
[2-3 sentence paraphrase of signal extracted and categorization]

Clarifying questions (3-5, scale with complexity):
1. Extracted [N] patterns - complete or missing [specific pattern]?
2. Categorized [X] items as Tier 3 resources/ - should [item Y] be in SKILL.md instead?
3. Agent cut [noise items] as generic - do you want any included?
[4. Scripts identified: [list] - are these the right utilities?]
[5. Missing production context for [pattern Z] - add placeholder or skip?]

Does this match exactly what you want?
```

[WAIT for confirmation]

Ready to proceed? (continue/skip/back/stop)

---

### Phase 2: Structure Design
**Agent**: claude-manager

**Prompt to agent**:
```
MODE: CREATE skill - Structure design

SKILL NAME: [name]

EXTRACTED SIGNAL (from Phase 1):
Core Patterns: [patterns with WHY]
Detailed Examples: [for resources/]
Scripts: [utility scripts]
USER ADJUSTMENTS: [from Phase 1]

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

```
Let me verify my understanding:
[2-3 sentence paraphrase of skill structure]

Clarifying questions (3-5, scale with complexity):
1. SKILL.md has [N] sections - right scope?
2. resources/ includes [files] - should [content Y] be in SKILL.md instead?
3. Structure puts [pattern X] in [section] - does this make sense?
[4. scripts/ includes [script A] - needed or over-engineering?]
[5. Cross-references: SKILL.md references [files] - complete?]

Does this match exactly what you want?
```

[WAIT for confirmation]

Ready to proceed? (continue/skip/back/stop)

---

### Phase 3: File Creation (Inline)
**You do this - no agent**

Create skill files at `.claude/skills/[skill-name]/`:

```
.claude/skills/skill-name/
├── SKILL.md
├── resources/    (if Tier 3 needed)
│   └── example.md
└── scripts/      (if scripts needed)
    └── utility.sh
```

- Create SKILL.md with structure from Phase 2, frontmatter, required sections, `@resources/` references
- Create resources/ files (detailed examples, referenced FROM SKILL.md, self-contained, no nested references)
- Create scripts/ files (proper shebang, `chmod +x`, usage docs)

No clarifying questions (file creation is mechanical based on approved structure).

Ready to proceed? (continue/skip/back/stop)

---

### Phase 4: Verification (Inline)
**You do this - no agent**

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

```
Let me verify my understanding:
[2-3 sentence paraphrase of verification results]

Clarifying questions (3-5, scale with complexity):
1. Verification found [N] issues - fix automatically or show you first?
2. Missing [section/item X] - add now or optional?
3. Signal vs Noise check: [item Y] seems generic - remove or keep with WHY?
[4. Skill ready at [path] - commit or review first?]

Does this match your expectations?
```

[WAIT for confirmation]

Skill creation complete!

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

```
Let me verify my understanding:
[2-3 sentence paraphrase of audit scope]

Clarifying questions (3-5, scale with complexity):
1. Should I audit [N] skills found, or exclude some?
2. Priority focus - structure compliance, Signal vs Noise, or both?
3. If issues found, auto-fix or just report?
[4. Should audit check Tier 3 resources/ organization?]
[5. Success criterion - all compliant, or report only?]

Does this match what you want?
```

[WAIT for confirmation]

Ready to proceed? (continue/skip/back/stop)

---

### Phase 1: Structure Compliance
**Agent**: claude-manager

**Prompt to agent**:
```
MODE: AUDIT skills (structure compliance)

SKILLS: [list from Phase 0]
FOCUS: [structure/content/both]
AUTO_FIX: [yes/no]

Task: Analyze skill structure compliance.

For each skill, check:
1. File structure (SKILL.md, frontmatter, resources/ and scripts/ if referenced)
2. Required sections (Purpose, When to Use, Core Patterns)
3. Tier 3 organization (resources/ referenced via @resources/, no orphaned files, ONE LEVEL DEEP)
4. Scripts organized (proper shebang, executable, referenced from SKILL.md)
5. References valid (@resources/ exist, cross-references to other skills valid)

Output per skill: compliance score, missing sections/files, invalid references, issues (specific)
```

```
Let me verify my understanding:
[2-3 sentence paraphrase of compliance results]

Clarifying questions (3-5, scale with complexity):
1. Found [N] skills with structure issues - fix or just report?
2. Skill [X] missing [section Y] - critical or optional?
3. Broken @resources/ references - auto-fix or ask per skill?
[4. Priority: missing sections / broken references / Tier 3 organization?]
[5. Proceed to content audit or fix structure first?]

Does this match your expectations?
```

[WAIT for confirmation]

Ready to proceed? (continue/skip/back/stop)

---

### Phase 2: Content Quality Audit
**Agent**: claude-manager

**Prompt to agent**:
```
MODE: AUDIT skills (content quality)

SKILLS: [list]
STRUCTURE RESULTS: [from Phase 1]
USER DECISIONS: [auto-fix or report, priorities]

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

```
Let me verify my understanding:
[2-3 sentence paraphrase of violations found]

Clarifying questions (3-5, scale with complexity):
1. Found [N] Signal vs Noise violations - cut completely?
2. Skill [X] has patterns without WHY - add placeholders or skip?
3. Historical timeline sections found - replace with current state?
[4. [Skill Z] has detailed examples in SKILL.md - move to resources/?]
[5. Tier 3 organization fixes needed - proceed now or defer?]

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

STRUCTURE RESULTS: [Phase 1]
CONTENT RESULTS: [Phase 2]
USER DECISIONS: [priorities, preferences]

Task: Create actionable recommendations for skill improvements.

For each skill with issues:
1. Structure fixes (missing sections, broken references, Tier 3 reorganization)
2. Content refactoring (noise to cut, WHY to add, historical timeline to replace)
3. Priority: critical (broken structure, missing WHY) → high (violations) → medium (Tier 3) → low (enhancements)
4. Migration plan (structure first, then content, then verification)

Output per skill: priority, structure fixes, content refactoring, Tier 3 changes, migration steps (ordered)
```

```
Let me verify my understanding:
[2-3 sentence paraphrase of recommendations]

Clarifying questions (3-5, scale with complexity):
1. [N] critical fixes - do these in Phase 4?
2. Priority order: [skill A] → [skill B] - correct?
3. Tier 3 reorganization needed - proceed?
[4. Implement all recommendations or just critical + high priority?]

Does this match your expectations?
```

[WAIT for confirmation]

Ready to proceed with implementation? (continue/skip/back/stop)

---

### Phase 4: Implementation (Inline - Conditional)
**You do this - no agent**

**Only if user approved in Phase 3.**

Apply per skill (in priority order):

1. **Structure fixes** - add missing sections, fix broken references, reorganize Tier 3
2. **Content refactoring** - cut noise, add WHY, replace historical timeline
3. **Tier 3 reorganization** - move content >50 lines to resources/, add @resources/ references, verify ONE LEVEL DEEP
4. **Verify per skill** - structure checklist, Signal vs Noise, WHY context, references

```
Let me verify my understanding:
[2-3 sentence paraphrase of changes made]

Clarifying questions (3-5, scale with complexity):
1. Made [N] changes to [M] skills - commit these?
2. Created [X] new resources/ files - organized correctly?
3. Some skills still have minor issues [list] - fix now or later?
[4. Verification passed for [N] skills - what about remaining [M]?]

Does this match your expectations?
```

[WAIT for confirmation]

Audit complete!

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

```
Let me verify my understanding:
[2-3 sentence paraphrase of changes to make]

Clarifying questions (3-5, scale with complexity):
1. Scope: Changes affect [specific sections] or entire skill?
2. Category: Primarily [category A] or [category B]?
3. Approach: [approach A] or [approach B] for [specific change]?
[4. Update strategy: UPDATE existing (replace wrong) or ADD section?]
[5. Verification: Full quality check or just changed sections?]

Does this match exactly what you want?
```

[WAIT for confirmation]

Ready to proceed? (continue/skip/back/stop)

---

### Phase 1: Change Analysis
**Agent**: claude-manager

**Prompt to agent**:
```
MODE: MODIFY skill

SKILL: [name and path]
CHANGES REQUESTED: [from Phase 0]
CATEGORIES: [pattern_update, clarification, anti_pattern, drift_fix, tier3_reorganization, script_addition]
USER ADJUSTMENTS: [from Phase 0]

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

```
Let me verify my understanding:
[2-3 sentence paraphrase of change plan]

Clarifying questions (3-5, scale with complexity):
1. Plan suggests [N] modifications - complete or should I add [X]?
2. Change order: [A] → [B] → [C] - correct priority?
3. Section [X] will be [modified/enhanced/replaced] - is this what you want?
[4. Updates existing content - correct approach?]
[5. After changes, skill will [outcome] - matches your goal?]

Does this match exactly what you want?
```

[WAIT for confirmation]

Ready to proceed? (continue/skip/back/stop)

---

### Phase 2: Implementation (Inline)
**You do this - no agent**

Apply modifications from Phase 1 plan:

```yaml
Pattern updates: Replace outdated, enhance with WHY, apply Signal vs Noise
Drift fixes: UPDATE existing content in-place, replace with current state
Tier 3 reorganization: Move >50 lines to resources/, add @resources/ refs, verify ONE LEVEL DEEP
Script additions: Create scripts/ with shebang, chmod +x, add usage to SKILL.md
```

No clarifying questions (implementation is mechanical based on approved plan).

Ready to proceed? (continue/skip/back/stop)

---

### Phase 3: Verification (Inline)
**You do this - no agent**

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

```
Let me verify my understanding:
[2-3 sentence paraphrase of changes and verification status]

Clarifying questions (3-5, scale with complexity):
1. Made [N] changes to [sections] - all correct?
2. Verification found [N] issues - fix automatically or show you?
3. Modified skill ready at [path] - commit or review first?
[4. Changes improve [aspect] - does this achieve your goal?]

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
