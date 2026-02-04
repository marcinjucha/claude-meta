---
description: "Intelligent CLAUDE.md management - create, audit, or modify documentation based on natural language"
---

# Manage CLAUDE.md Command

Intelligent CLAUDE.md documentation management - automatically detects intent (CREATE/AUDIT/MODIFY) from natural language and executes appropriate task using claude-manager agent.

**Pattern**: Signal-focused documentation with mandatory WHY context, hierarchical structure, and cross-reference integrity.

---

## ⚠️ CRITICAL: YOU MUST INVOKE AGENTS

**This is NOT a research task. You MUST invoke the claude-manager agent for all agent phases.**

When you see "**Agent**: claude-manager" in a phase:
- ✅ DO: Use Task tool with `subagent_type="claude-manager"` and the exact prompt provided
- ❌ DON'T: Describe what the agent would do, summarize expected output, or skip invocation

**Test**: If you're typing more than 3 sentences about what an agent phase will do → YOU'RE DOING IT WRONG. Invoke the agent instead.

---

## Critical Rules

1. **YOU MUST INVOKE AGENTS** - All phases marked "Agent: claude-manager" require Task tool invocation
2. **Sufficient context principle** - Provide extracted decisions (50 lines), not full conversation (500 lines)
3. **Clarifying questions MANDATORY** - After Phase 0 AND after EVERY agent phase (paraphrase + 5 questions + confirmation)
4. **User checkpoints** - Offer commands ONLY after user confirms understanding (never before)
5. **Signal vs Noise is GATE** - 3-question filter before any content (Project-specific? Non-obvious? Critical?)
6. **WHY > HOW** - Every pattern needs WHY it exists, WHY approach chosen, WHY it matters (production impact)
7. **Current state focus** - CLAUDE.md shows HOW IT WORKS NOW (update existing content, don't add "Changed in [date]")
8. **Cross-reference integrity** - All references valid, bidirectional when appropriate
9. **CLAUDE.md vs Skill distinction** - Pattern in 2+ unrelated modules → Extract to skill, reference from CLAUDE.md
10. **NEVER INVENT CONTENT** - claude-manager must NEVER make up metrics, production incidents, anti-patterns, or numbers. ONLY use user-provided data.

---

## Phase Execution Pattern

**When executing any phase, you MUST follow this pattern:**

1. **Paraphrase** phase goal (2-3 sentences showing you understand)
2. **Ask 5 clarifying questions** specific to this phase
3. **Wait for user confirmation** (never proceed without explicit approval)
4. **Execute phase** (invoke agent or perform inline work)
5. **After completion**, offer commands: `continue`, `skip`, `back`, `stop`

**Template:**
```
Let me verify my understanding of Phase N:
[2-3 sentence paraphrase of what this phase will accomplish]

Clarifying questions:
1. [Specific question about scope/approach]
2. [Specific question about priorities/constraints]
3. [Specific question about expected output]
4. [Specific question about edge cases]
5. [Specific question about verification criteria]

Does this match exactly what you want? If not, what should I adjust?
```

[WAIT for user confirmation - DO NOT proceed without it]

After user confirms:
```
[Execute phase - invoke agent or perform inline work]

Phase N complete. Ready to proceed?
Commands: continue | skip | back | stop
```

---

## Universal Phase 0: Intent Detection

**You do this - no agent**

### Step 1: Detect Intent from Natural Language

Analyze user's message for keywords:

**CREATE Mode Keywords:**
- "create", "new", "need CLAUDE.md for [module]", "document [module]", "write CLAUDE.md"

**AUDIT Mode Keywords:**
- "check", "verify", "audit", "signal vs noise", "compliance", "review", "validate"

**MODIFY Mode Keywords:**
- "update", "fix", "add [discovery]", "outdated [info]", "remove [obsolete]", "change"

**Confidence levels:**
- HIGH: Single clear mode indicated by primary keywords
- MEDIUM: Multiple modes possible, but one more likely
- LOW: Ambiguous, multiple interpretations possible

### Step 2: Find Existing CLAUDE.md Files (if AUDIT/MODIFY)

For AUDIT or MODIFY modes, use Glob to find all CLAUDE.md files:

```bash
# Find all CLAUDE.md files
Glob: "**/CLAUDE.md"
```

List found files with detected level (based on path depth and naming).

### Step 3: Determine Mode, Level, and Scope

**Output format:**
```yaml
INTENT_DETECTED:
  mode: [CREATE | AUDIT | MODIFY]
  confidence: [HIGH | MEDIUM | LOW]
  reasoning: [Why this mode was selected]

SCOPE:
  module: [Module name if CREATE/MODIFY single file]
  level: [root | domain | subdomain | BUS | kit | test]
  files: [List of CLAUDE.md files if AUDIT multiple or MODIFY]
```

### Step 4: If Confidence LOW - Ask Clarifying Questions

If confidence is MEDIUM or LOW:

```
I detected intent as [MODE] with [CONFIDENCE] confidence.

Clarifying questions to confirm:
1. Mode: Should I [MODE A] or [MODE B]?
2. Scope: [Scope question based on detected mode]
3. Level: [Level question if applicable]
4. Priority: [Priority question based on mode]
5. Expected outcome: [Outcome question]

Does this match what you want?
```

[WAIT for confirmation]

### Step 5: Proceed to Mode-Specific Phase 0

Based on confirmed mode, proceed to:
- CREATE Mode → Phase 0: Level & Decision Framework
- AUDIT Mode → Phase 0: Scope Selection
- MODIFY Mode → Phase 0: Change Scope

---

## CREATE Mode

**Purpose**: Create new CLAUDE.md file for module with signal-focused content and WHY context.

**5 Phases:**
1. Phase 0: Level & Decision Framework (inline)
2. Phase 1: Signal Extraction (claude-manager)
3. Phase 2: Structure Design (claude-manager)
4. Phase 3: File Creation (inline)
5. Phase 4: Verification (inline)

---

### CREATE Phase 0: Level & Decision Framework (Inline)

**You do this - no agent**

**From Universal Phase 0: Mode=CREATE, Module name determined**

#### Step 1: CLAUDE.md vs Skill Decision

Apply decision framework:

```
Is this specific to folder and subfolders?
├─ YES → Continue to Step 2 (CLAUDE.md)
└─ NO → Should this be a skill instead?

    Pattern used by 2+ unrelated modules?
    ├─ YES → Create skill, not CLAUDE.md
    └─ NO → Continue to Step 2

    Pattern reusable across Domains/Subdomains?
    ├─ YES → Create skill, not CLAUDE.md
    └─ NO → Continue to Step 2
```

**Rule**: If pattern appears in 2+ unrelated CLAUDE.md files → Extract to skill, reference from CLAUDE.md

#### Step 2: Determine CLAUDE.md Level

Detect level from module path:
- **root**: `/CLAUDE.md` (project-wide architecture guide)
- **domain**: `[Domain]/CLAUDE.md` (high-level business capability)
- **subdomain**: `[Domain]/[Subdomain]/CLAUDE.md` (feature grouping)
- **BUS**: `[Domain]/[Subdomain]/[BUS]/CLAUDE.md` (single workflow)
- **kit**: `[Kit]/CLAUDE.md` (utility module)
- **test**: `[Kit]/[TestFolder]/CLAUDE.md` (test infrastructure)

#### Step 3: Apply 3-Question Filter

**Signal vs Noise filter (all 3 must be YES):**
1. **Project-specific?** (not generic architecture, frameworks Claude knows)
2. **Non-obvious?** (would cause bugs or waste time if not documented)
3. **Critical?** (production impact, frequent reference, weird behavior)

→ All YES → Create CLAUDE.md
→ Any NO → Reconsider or should be skill

#### Step 4: Check for Existing CLAUDE.md

```bash
# Check if file exists
ls [module_path]/CLAUDE.md
```

- If exists → Switch to MODIFY mode
- If not exists → Proceed with CREATE

#### MANDATORY Clarifying Questions

```
Let me verify my understanding:
[2-3 sentence paraphrase of CLAUDE.md vs skill decision + level]

Clarifying questions:
1. CLAUDE.md vs Skill: Is this pattern specific to [Module] folder/subfolders, or reusable across project?
2. Level: If CLAUDE.md, which level - [detected level]?
3. Source material: Where is content to extract - [code/conversation/docs]?
4. Scope: Should this document [specific aspects] or broader?
5. Related patterns: Are there existing skills covering similar patterns that should be referenced?

Does this match exactly what you want? If not, what should I adjust?
```

[WAIT for confirmation]

```
Phase 0 complete. Ready to proceed?
Commands: continue | skip | back | stop
```

---

### CREATE Phase 1: Signal Extraction

**Agent**: claude-manager

#### Sufficient Context for Quality

**Input needed:**
- Mode: CREATE
- CLAUDE.md level (detected from path)
- Module name and path
- Decision framework results (3 YES from Phase 0)
- Source material location
- User confirmations from Phase 0

**NOT needed:**
- Full conversation history
- Generic documentation theory
- Full Phase 0 conversation

#### Prompt to Agent

```
MODE: CREATE CLAUDE.md - Signal extraction

⚠️ CRITICAL: NEVER INVENT OR HALLUCINATE CONTENT
- DO NOT make up metrics, numbers, or production incidents
- DO NOT invent anti-patterns without user-provided examples
- ONLY extract what user actually provided
- If no production data exists, use placeholder: [User to provide real metric/incident]

LEVEL: [root/domain/subdomain/BUS/kit/test]
MODULE: [name and path]

CONTEXT FROM PHASE 0:
- CLAUDE.md (not skill) because: [reason]
- Level: [level] because: [reason]
- 3-question filter: ALL YES (project-specific, non-obvious, critical)

SOURCE MATERIAL: [where to extract content from]
USER ADJUSTMENTS: [from Phase 0 clarifying questions]

Task: Extract pure signal from source material using Signal vs Noise 3-question filter.

Apply filter to EVERY piece of content:
- Project-specific? (not generic architecture, frameworks Claude knows)
- Non-obvious? (would cause bugs or waste time if not documented)
- Critical? (production impact, frequent reference, weird behavior)

Extract categories (adapt to level):
1. **Weird Parts / Key Patterns** - WITH WHY CONTEXT (why exists, why chosen, why matters)
2. **Critical Mistakes** - WITH WHY CONTEXT (problem, why failed, fix, production impact with metrics)
3. **Quick Reference** - Frequently needed facts, file paths, key numbers
4. **Cross-References** - Related CLAUDE.md files and skills to reference

Use claude-md and signal-vs-noise skills for extraction patterns.

Output format:
**Weird Parts Extracted:** [list with WHY]
**Critical Mistakes Extracted:** [list with Problem/Why/Fix/Impact]
**Quick Reference Items:** [list]
**Cross-References Needed:** [list]
**Noise Cut:** [what was excluded and why]
```

#### After Agent Completes - MANDATORY Clarifying Questions

```
Let me verify my understanding of extracted signal:
[2-3 sentence paraphrase]

Clarifying questions:
1. Weird Parts: Did I capture [specific pattern] correctly, or should I adjust?
2. Critical Mistakes: Is production impact context sufficient, or need more details?
3. Quick Reference: Are file paths complete, or missing key references?
4. Cross-References: Should I reference [specific CLAUDE.md/skill], or different ones?
5. Noise Cut: Did I correctly exclude [generic content], or should it be included?

Does this match exactly what you want? If not, what should I adjust?
```

[WAIT for confirmation]

```
Phase 1 complete. Ready to proceed?
Commands: continue | skip | back | stop
```

---

### CREATE Phase 2: Structure Design

**Agent**: claude-manager

#### Sufficient Context for Quality

**Input needed:**
- Extracted signal (from Phase 1: weird parts, mistakes, quick ref, cross-refs)
- User confirmations/adjustments (from Phase 1)
- CLAUDE.md level (determines required sections)
- Module name and path

**NOT needed:**
- Full Phase 1 conversation
- Generic CLAUDE.md examples

#### Prompt to Agent

```
MODE: CREATE CLAUDE.md - Structure design
LEVEL: [root/domain/subdomain/BUS/kit/test]
MODULE: [name and path]

EXTRACTED SIGNAL (from Phase 1):
**Weird Parts:** [list with WHY]
**Critical Mistakes:** [list with Problem/Why/Fix/Impact]
**Quick Reference:** [list]
**Cross-References:** [list]

USER ADJUSTMENTS: [from Phase 1]

Task: Design CLAUDE.md structure using standard sections for detected level.

Use claude-md skill for level-appropriate structure templates and section requirements.

Output:
1. Section breakdown (which sections, content allocation per section)
2. Cross-reference plan (which CLAUDE.md to reference, which skills to reference)
3. Content organization (which extracted items go in which section)
```

#### After Agent Completes - MANDATORY Clarifying Questions

```
Let me verify my understanding of structure design:
[2-3 sentence paraphrase]

Clarifying questions:
1. Sections: Are all required sections for [level] present, or missing any?
2. Content allocation: Should [content item] go in [section A] or [section B]?
3. Cross-references: Should I reference [specific CLAUDE.md] in [section], or different location?
4. Decision trees: Should I include decision trees for [pattern], or skip?
5. Level compliance: Does structure match [level] requirements, or need adjustments?

Does this match exactly what you want? If not, what should I adjust?
```

[WAIT for confirmation]

```
Phase 2 complete. Ready to proceed?
Commands: continue | skip | back | stop
```

---

### CREATE Phase 3: File Creation (Inline)

**You do this - no agent**

#### Step 1: Create CLAUDE.md File

Use Write tool to create file at module path with:
- Standard sections for level (from Phase 2 approved structure)
- Extracted content (from Phase 1)
- Cross-references (from Phase 1)
- Proper formatting (bold **Why**, code blocks, file paths, tables)

#### Step 2: Verify Formatting

Check:
- Bold **Why**: for all WHY context
- Code blocks with language tags
- File paths with line numbers if available
- Tables in Quick Reference
- Cross-references with level indicators

```
Phase 3 complete. CLAUDE.md created at [path] with [N] lines.
Ready to proceed?
Commands: continue | skip | back | stop
```

---

### CREATE Phase 4: Verification (Inline)

**You do this - no agent**

#### Verification Checklist

**Structure Compliance:**
- [ ] All required sections for level present
- [ ] Sections in standard order
- [ ] No level-inappropriate sections

**Signal vs Noise:**
- [ ] No generic architecture explanations
- [ ] All content passes 3-question filter

**WHY over HOW:**
- [ ] Every pattern has WHY context
- [ ] Critical Mistakes have production impact

**Cross-Reference Integrity:**
- [ ] All CLAUDE.md references valid
- [ ] All skill references valid
- [ ] Level indicators present

**Current State Focus:**
- [ ] Shows HOW IT WORKS NOW
- [ ] No "Changed in [date]" sections

**Output:**
```
✅ PASSED: [checks that passed]
⚠️ WARNINGS: [potential issues]
❌ FAILED: [checks that failed]
```

```
Phase 4 complete. Verification [PASSED/FAILED].
CREATE mode complete.

Commands: stop | back
```

---

## AUDIT Mode

**Purpose**: Audit existing CLAUDE.md files for structure compliance, content quality (Signal vs Noise), and cross-reference integrity.

**6 Phases:**
1. Phase 0: Scope Selection (inline)
2. Phase 1: Structure Compliance (claude-manager)
3. Phase 2: Content Quality Audit (claude-manager)
4. Phase 3: Cross-Reference Audit (claude-manager)
5. Phase 4: Recommendations (claude-manager)
6. Phase 5: Implementation (inline, if approved)

---

### AUDIT Phase 0: Scope Selection (Inline)

**You do this - no agent**

**From Universal Phase 0: Mode=AUDIT, Scope determined**

#### Determine Audit Scope

Use Glob to find CLAUDE.md files based on scope:

```bash
# Scope types
specific: Find CLAUDE.md at module path
level: Glob pattern for level (e.g., "**/*Subdomain/CLAUDE.md" for subdomain level)
all: Glob "**/CLAUDE.md"
```

List found files with level (detected from path) and size.

#### MANDATORY Clarifying Questions

```
Let me verify my understanding:
[2-3 sentence paraphrase of audit scope]

Clarifying questions:
1. Scope: Should I audit [N] CLAUDE.md files found, or exclude some?
2. Priority focus: Structure compliance, content quality (Signal vs Noise), cross-references, or all?
3. Auto-fix: If issues found, should I fix automatically or just report?
4. Missing CLAUDE.md: Should audit check for modules without CLAUDE.md?
5. Success criterion: All files compliant, or report only?

Does this match exactly what you want? If not, what should I adjust?
```

[WAIT for confirmation]

```
Phase 0 complete. Audit scope: [N] files.
Ready to proceed?
Commands: continue | skip | back | stop
```

---

### AUDIT Phase 1: Structure Compliance

**Agent**: claude-manager

#### Sufficient Context for Quality

**Input needed:**
- CLAUDE.md files to audit (paths, detected levels, sizes)
- Audit focus (from Phase 0: structure/content/cross-refs/all)
- User decisions (from Phase 0)

**NOT needed:**
- Full Phase 0 conversation

#### Prompt to Agent

```
MODE: AUDIT CLAUDE.md (structure compliance)

FILES: [list with paths, levels, sizes]
FOCUS: [from Phase 0]
USER DECISIONS: [from Phase 0]

Task: Audit CLAUDE.md structure for level-appropriate required sections and standard order.

Use claude-md skill for level-specific section requirements.

Check for each file:
- Missing required sections
- Level-inappropriate sections
- Non-standard section order
- Empty sections (heading present but no content)

Output per file:
- File path and level
- Structure compliance: PASS/FAIL
- Missing sections: [list]
- Level-inappropriate sections: [list]
- Order violations: [list]
- Empty sections: [list]
- Severity: critical/moderate/minor
```

#### After Agent Completes - MANDATORY Clarifying Questions

```
Let me verify my understanding of structure audit results:
[2-3 sentence paraphrase]

Clarifying questions:
1. Violations: Are [critical violations] blocking, or can proceed with warnings?
2. Missing sections: Should I add all missing sections, or prioritize some?
3. Order: Should I reorder sections to standard, or leave as-is with warning?
4. Empty sections: Should I populate empty sections, or flag for manual review?
5. Next phase: Proceed to content quality audit, or fix structure first?

Does this match exactly what you want? If not, what should I adjust?
```

[WAIT for confirmation]

```
Phase 1 complete. Structure audit: [N passed], [N failed].
Ready to proceed?
Commands: continue | skip | back | stop
```

---

### AUDIT Phase 2: Content Quality Audit

**Agent**: claude-manager

#### Sufficient Context for Quality

**Input needed:**
- Structure results (Phase 1: which files passed/failed)
- User decisions (from Phase 1)
- CLAUDE.md files to audit

**NOT needed:**
- Full Phase 1 conversation
- Generic examples

#### Prompt to Agent

```
MODE: AUDIT CLAUDE.md (content quality)

⚠️ CRITICAL: FLAG INVENTED CONTENT
Flag invented metrics/incidents for removal. Recommend placeholders or deletion.

FILES: [list]
STRUCTURE RESULTS: [Phase 1 summary]
USER DECISIONS: [from Phase 1]

Task: Audit CLAUDE.md content for Signal vs Noise, WHY over HOW, and production context.

Use signal-vs-noise and claude-md skills for quality standards.

Check violations:

1. **Signal vs Noise** - Apply 3-question filter (Project-specific? Non-obvious? Critical?)
   - Generic architectural explanations (Claude knows) = NOISE
   - Standard framework patterns (Claude knows) = NOISE
   - HOW without WHY = NOISE

2. **WHY over HOW** - Patterns must include:
   - WHY pattern exists (real problem)
   - WHY approach chosen (alternatives)
   - WHY it matters (production impact)

3. **Production context** - Critical Mistakes must explain:
   - Problem (what broke)
   - Why it failed (root cause)
   - Fix (what we do now)
   - Production impact (metrics if available)

4. **Current state vs historical timeline**:
   - CLAUDE.md shows HOW IT WORKS NOW, not history
   - Flag "Changed in [date]" notes
   - Flag "Previously X, now Y" sections

5. **CLAUDE.md vs Skill misplacement**:
   - Pattern in 2+ unrelated CLAUDE.md files → Should be skill
   - Flag duplicate patterns for extraction

Output per file:
- File path and level
- Content quality: PASS/FAIL
- Signal vs Noise violations: [quote, issue, fix]
- WHY over HOW violations: [quote, issue, fix]
- Production context missing: [list]
- Current state violations: [sections with timeline]
- Skill misplacement: [patterns in 2+ files]
- Severity: critical/moderate/minor
```

#### After Agent Completes - MANDATORY Clarifying Questions

```
Let me verify my understanding of content quality audit results:
[2-3 sentence paraphrase]

Clarifying questions:
1. Noise: Should I remove all generic content flagged, or keep some with better WHY?
2. WHY missing: Should I research production context for [pattern], or flag for manual addition?
3. Historical timeline: Should I update existing content, or preserve history?
4. Skill extraction: Should I extract [pattern] to skill now, or just flag for later?
5. Next phase: Proceed to cross-reference audit, or fix content first?

Does this match exactly what you want? If not, what should I adjust?
```

[WAIT for confirmation]

```
Phase 2 complete. Content quality audit: [N passed], [N failed].
Ready to proceed?
Commands: continue | skip | back | stop
```

---

### AUDIT Phase 3: Cross-Reference Audit

**Agent**: claude-manager

#### Sufficient Context for Quality

**Input needed:**
- Structure results (Phase 1 summary)
- Content results (Phase 2 summary)
- CLAUDE.md files to audit

**NOT needed:**
- Full Phase 1-2 conversation

#### Prompt to Agent

```
MODE: AUDIT CLAUDE.md (cross-references)

FILES: [list]
STRUCTURE RESULTS: [Phase 1 summary]
CONTENT RESULTS: [Phase 2 summary]

Task: Audit cross-references for validity and completeness.

Use claude-md skill for cross-reference patterns.

Check:
1. **Broken file paths** - Non-existent files, outdated line numbers
2. **Missing cross-references** - Related CLAUDE.md not linked, skills not referenced
3. **Wrong reference direction** - BUS referencing down instead of up
4. **Outdated cross-references** - Section names changed, content moved
5. **Missing level indicators** - Cross-references should include level

Output per file:
- File path and level
- Cross-reference integrity: PASS/FAIL
- Broken references: [list with paths]
- Missing references: [suggested additions]
- Wrong direction: [corrections]
- Outdated references: [updates]
- Missing level indicators: [list]
- Severity: critical/moderate/minor
```

#### After Agent Completes - MANDATORY Clarifying Questions

```
Let me verify my understanding of cross-reference audit results:
[2-3 sentence paraphrase]

Clarifying questions:
1. Broken references: Should I fix all broken paths, or flag critical ones only?
2. Missing references: Should I add all suggested cross-references, or prioritize?
3. Wrong direction: Should I reverse reference direction, or remove?
4. Level indicators: Should I add level indicators to all cross-references?
5. Next phase: Proceed to recommendations, or fix cross-references first?

Does this match exactly what you want? If not, what should I adjust?
```

[WAIT for confirmation]

```
Phase 3 complete. Cross-reference audit: [N passed], [N failed].
Ready to proceed?
Commands: continue | skip | back | stop
```

---

### AUDIT Phase 4: Recommendations

**Agent**: claude-manager

#### Sufficient Context for Quality

**Input needed:**
- Structure results (Phase 1 summary)
- Content results (Phase 2 summary)
- Cross-reference results (Phase 3 summary)
- User priorities (from previous phases)

**NOT needed:**
- Full Phase 1-3 conversations
- Detailed violation quotes

#### Prompt to Agent

```
MODE: AUDIT CLAUDE.md (recommendations)

AUDIT RESULTS SUMMARY:
- Structure (Phase 1): [N passed, N failed, critical violations]
- Content Quality (Phase 2): [N passed, N failed, critical violations]
- Cross-References (Phase 3): [N passed, N failed, critical violations]

USER PRIORITIES: [from Phase 0]

Task: Generate prioritized recommendations for fixing violations.

Output:
**Priority 1: Critical** (blocks usage)
[List with file, violation, fix]

**Priority 2: Moderate** (reduces quality)
[List with file, violation, fix]

**Priority 3: Minor** (polish)
[List with file, violation, fix]

**Skill Extraction Opportunities:**
[Patterns in 2+ files → Create skill: [name]]

**Migration Plan:**
Phase 1: Fix critical ([N] files)
Phase 2: Fix moderate ([N] files)
Phase 3: Fix minor ([N] files)
Phase 4: Extract patterns to skills ([N] patterns)
```

#### After Agent Completes - MANDATORY Clarifying Questions

```
Let me verify my understanding of recommendations:
[2-3 sentence paraphrase]

Clarifying questions:
1. Priority: Should I fix [priority 1] violations immediately, or all at once?
2. Skill extraction: Should I extract [patterns] to skills now, or defer?
3. Migration plan: Does phased approach match your timeline, or adjust?
4. Effort: Does estimated effort seem reasonable, or need breakdown?
5. Next phase: Proceed to implementation, or review recommendations?

Does this match exactly what you want? If not, what should I adjust?
```

[WAIT for confirmation]

```
Phase 4 complete. Recommendations: [N] critical, [N] moderate, [N] minor.
Ready to proceed?
Commands: continue | skip | back | stop
```

---

### AUDIT Phase 5: Implementation (Inline)

**You do this - no agent**

**Only proceed if user approved fixes**

#### Apply Fixes Based on Priority

Work through recommendations from Phase 4 in priority order:

**Priority 1: Critical**
- Add missing sections
- Remove noise
- Add WHY context
- Fix broken cross-references

**Priority 2: Moderate**
- Update content
- Add production context
- Fix structure

**Priority 3: Minor**
- Formatting
- Order
- Polish

Track progress after each file:
```
Fixed: [file]
- [violation 1] → [fix]
- [violation 2] → [fix]

Progress: [N/M] complete
```

#### Verify Fixes

Run verification:
- Structure compliance
- Signal vs Noise
- WHY over HOW
- Cross-references
- Current state

```
Phase 5 complete. Fixed [N] files.
Verification: [PASSED/FAILED]

AUDIT mode complete. Summary:
- Structure: [N] files fixed
- Content: [N] files fixed
- Cross-references: [N] files fixed

Commands: stop | back
```

---

## MODIFY Mode

**Purpose**: Modify existing CLAUDE.md based on discovered changes.

**4 Phases:**
1. Phase 0: Change Scope (inline)
2. Phase 1: Change Analysis (claude-manager)
3. Phase 2: Implementation (inline)
4. Phase 3: Verification (inline)

---

### MODIFY Phase 0: Change Scope (Inline)

**You do this - no agent**

**From Universal Phase 0: Mode=MODIFY, Module and changes determined**

#### Categorize Changes

**Change categories:**
- **add_discovery**: Add new weird part or critical mistake
- **update_outdated**: Update file paths, patterns, numbers
- **remove_obsolete**: Remove pattern no longer used
- **restructure**: Reorganize for clarity
- **cross_reference**: Add references to skills or other CLAUDE.md

#### MANDATORY Clarifying Questions

```
Let me verify my understanding:
[2-3 sentence paraphrase of changes]

Clarifying questions:
1. Scope: Should changes affect [specific sections] or entire CLAUDE.md?
2. Category: Is this primarily [category A] or [category B]?
3. Approach: Should I [approach A] or [approach B] for [specific change]?
4. CRITICAL: Should I UPDATE existing content (replace wrong) or ADD migration note?
5. Verification: After changes, full quality check or just changed sections?

Does this match exactly what you want? If not, what should I adjust?
```

[WAIT for confirmation]

```
Phase 0 complete. Change scope: [categories].
Ready to proceed?
Commands: continue | skip | back | stop
```

---

### MODIFY Phase 1: Change Analysis

**Agent**: claude-manager

#### Sufficient Context for Quality

**Input needed:**
- CLAUDE.md path and level
- Changes requested with categories (from Phase 0)
- User confirmations (from Phase 0)

**NOT needed:**
- Full CLAUDE.md content (agent will read)
- Generic modification theory

#### Prompt to Agent

```
MODE: MODIFY CLAUDE.md

FILE: [path and level]
CHANGES: [from Phase 0]
CATEGORIES: [add_discovery, update_outdated, remove_obsolete, restructure, cross_reference]
USER ADJUSTMENTS: [from Phase 0]

Task: Analyze current CLAUDE.md state and plan modifications.

CRITICAL INSTRUCTION:
- UPDATE existing content (replace wrong with correct)
- DO NOT add "Changed in [date]" or "Previously X, now Y" sections
- DO NOT add "Was" or "Migration" sections
- CLAUDE.md shows HOW IT WORKS NOW, not historical evolution
- Replace outdated patterns with current patterns in-place

Use claude-md, skill-fine-tuning, signal-vs-noise skills.

Read file and analyze:
1. Current state (sections, level, size)
2. Changes mapped to sections
3. Impact (cross-references affected)
4. Approach per category:
   - add_discovery: Add to Weird Parts/Critical Mistakes WITH WHY
   - update_outdated: Replace wrong with correct
   - remove_obsolete: Remove or archive
   - restructure: Apply standard structure
   - cross_reference: Remove duplicate, add reference

Output:
**Current State:** [summary]
**Change Plan (section by section):** [list]
**Cross-Reference Updates:** [list]
**Dependencies:** [list]
**Implementation Steps:** [ordered]
**Verification Checklist:** [how to verify]
```

#### After Agent Completes - MANDATORY Clarifying Questions

```
Let me verify my understanding of change plan:
[2-3 sentence paraphrase]

Clarifying questions:
1. Scope: Will changes affect [specific sections], or broader?
2. Approach: Should I [approach A] or [approach B] for [specific change]?
3. Cross-references: Should I update [related CLAUDE.md] bidirectionally?
4. Verification: After changes, should I verify [specific aspect]?
5. Risk: Any concerns about [potential issue]?

Does this match exactly what you want? If not, what should I adjust?
```

[WAIT for confirmation]

```
Phase 1 complete. Change plan approved.
Ready to proceed?
Commands: continue | skip | back | stop
```

---

### MODIFY Phase 2: Implementation (Inline)

**You do this - no agent**

#### Apply Changes

Follow change plan from Phase 1:

**Change patterns:**
- **add_discovery**: Add to Weird Parts/Critical Mistakes WITH WHY context + production impact
- **update_outdated**: Replace wrong with correct (NO "Changed in [date]" notes)
- **remove_obsolete**: Remove completely or move to Deprecated section
- **restructure**: Apply standard structure for level
- **cross_reference**: Remove duplicate, add skill/CLAUDE.md reference

Track changes:
```
Applied: [change]
- Section: [name]
- Change: [what]
- Reason: [why]
```

Update bidirectional cross-references if needed.

```
Phase 2 complete. Applied [N] changes.
Ready to proceed?
Commands: continue | skip | back | stop
```

---

### MODIFY Phase 3: Verification (Inline)

**You do this - no agent**

#### Verification Checklist

**Change Verification:**
- [ ] All requested changes applied
- [ ] No unintended changes
- [ ] Change plan followed

**Signal vs Noise:**
- [ ] No new generic content
- [ ] All new content passes 3-question filter
- [ ] WHY context present

**Structure Compliance:**
- [ ] Level-appropriate sections maintained
- [ ] Standard order preserved

**Cross-Reference Integrity:**
- [ ] All CLAUDE.md cross-references still valid
- [ ] All skill cross-references still valid
- [ ] File paths and line numbers accurate
- [ ] No broken references introduced by changes
- [ ] Bidirectional references updated (if applicable)

**Current State Focus:**
- [ ] Shows HOW IT WORKS NOW
- [ ] No "Changed in [date]" added

**Output:**
```
✅ PASSED: [checks]
⚠️ WARNINGS: [issues]
❌ FAILED: [failures]
```

```
Phase 3 complete. Verification [PASSED/FAILED].
MODIFY mode complete.

Commands: stop | back
```

---

## Sufficient Context Principle

**For each claude-manager invocation, provide:**

✅ Mode (CREATE/AUDIT/MODIFY)
✅ CLAUDE.md level (affects structure)
✅ Critical decisions from previous phases (extracted)
✅ User confirmations/adjustments
✅ Specific task for this phase
✅ Expected output format

**Do NOT provide:**

❌ Full previous outputs (extract decisions only)
❌ Entire conversation history (conclusions only)
❌ Generic documentation theory (claude-manager has claude-md skill)
❌ Full CLAUDE.md content (agent will read file)

**Test question:**

> "Can claude-manager produce HIGH QUALITY output with this context alone?"
>
> If YES → sufficient
> If NO → add missing critical info (not everything)

**Example:**
```yaml
✅ SUFFICIENT (50 lines):
  Extracted signal from Phase 1:
  - Weird Parts: [list with WHY]
  - Critical Mistakes: [list with Problem/Why/Fix/Impact]
  CLAUDE.md level: BUS
  User adjustments: [specific corrections]

❌ TOO MUCH (500 lines):
  Full Phase 1 conversation including all agent outputs

❌ INSUFFICIENT (10 lines):
  "Use signal from Phase 1"
```

---

## Commands

- `continue` - Proceed to next phase
- `skip` - Skip current phase (with confirmation)
- `back` - Return to previous phase
- `status` - Show progress (current mode, phase, completion)
- `stop` - Exit command (with confirmation if work in progress)

---

## Anti-Patterns to Prevent

### ❌ Not Invoking claude-manager

**Problem**: Describing what agent will do instead of invoking.

**Fix**: When phase says "Agent: claude-manager", use Task tool with exact prompt.

### ❌ Too Much Context

**Problem**: Passing full conversation (500+ lines) to agent.

**Fix**: Extract decisions only (50 lines). Use "Sufficient Context" sections.

### ❌ No Clarifying Questions After Phase 0

**Problem**: Proceeding without user confirmation of understanding.

**Fix**: MANDATORY clarifying questions after Phase 0 AND after every agent phase.

### ❌ Offering Commands Before Confirmation

**Problem**: Showing commands before user confirms understanding.

**Fix**: Wait for user to confirm clarifying questions, THEN offer commands.


---

## Success Criteria

Command `/manage-claude-md` should:

1. **Detect intent** from natural language (CREATE/AUDIT/MODIFY)
2. **Find files dynamically** using Glob (not hardcoded list)
3. **Invoke claude-manager** for all agent phases (not describe)
4. **Apply Signal vs Noise filter** (cut generic content)
5. **Enforce WHY over HOW** (patterns need WHY, mistakes need production impact)
6. **Validate structure** (level-appropriate sections via claude-md skill)
7. **Audit cross-references** (valid paths, missing links, wrong direction)
8. **Ask clarifying questions** after Phase 0 and every agent phase
9. **Extract decisions** (sufficient context, not full conversation)
10. **Update existing content** (replace wrong, don't add "Changed in [date]")
11. **Pass verification** (structure + content + cross-references)
12. **Detect pattern duplication** (flag patterns in 2+ files for skill extraction)

---

## Notes

- **Pattern**: Mirrors update-skill architecture (proven pattern)
- **Agent**: claude-manager has claude-md, signal-vs-noise, skill-fine-tuning skills
- **Signal vs Noise**: 3-question filter (project-specific, non-obvious, critical)
- **Quality > Brevity**: 600 lines pure signal > 300 with noise
- **Current state**: CLAUDE.md shows HOW IT WORKS NOW, not historical evolution
- **UPDATE not ADD**: MODIFY replaces wrong content, doesn't add timeline sections
- **Dynamic discovery**: Use Glob to find CLAUDE.md files, don't hardcode list
- **Skills know structure**: claude-md skill has level-specific templates, don't duplicate here
