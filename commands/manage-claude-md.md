---
description: "Intelligent CLAUDE.md management - create, audit, or modify documentation based on natural language"
---

# Manage CLAUDE.md Command

Automatically detects intent (CREATE/AUDIT/MODIFY) from natural language and executes appropriate task using claude-manager agent.

**Pattern**: Minimal signal-focused documentation with WHY context and folder-specific knowledge.

---

## Agent Invocation

When you see "**Agent**: claude-manager" in a phase:
- Use Task tool with `subagent_type="claude-manager"` and the exact prompt provided
- If typing more than 3 sentences about what agent will do → invoke the agent instead

---

## Critical Rules

1. **Invoke agents** - All phases marked "Agent: claude-manager" require Task tool invocation
2. **Sufficient context** - Provide extracted decisions (50 lines), not full conversation (500 lines)
3. **Clarifying questions MANDATORY** - After Phase 0 AND after EVERY agent phase (paraphrase + 5 questions + confirmation)
4. **User checkpoints** - Offer commands ONLY after user confirms understanding
5. **Signal vs Noise filter** - 3-question filter: Project-specific? Non-obvious? Critical?
6. **WHY over HOW** - Every pattern needs WHY it exists, WHY approach chosen, WHY it matters
7. **Current state focus** - CLAUDE.md shows HOW IT WORKS NOW
8. **Cross-reference integrity** - All references valid, bidirectional when appropriate
9. **CLAUDE.md vs Skill** - Folder-specific → CLAUDE.md; Project-wide → Skill
10. **NEVER INVENT CONTENT** - claude-manager must NEVER make up metrics, production incidents, patterns, or numbers. ONLY use user-provided data.
11. **Minimal core** - Only Overview + Weird Parts required; everything else optional
12. **AVOID AI-KNOWN CONTENT** - claude-manager must NOT include generic architectural explanations or framework basics. Focus on folder-specific weird behaviors, critical bugs, non-obvious patterns with WHY context.

---

## ⚠️ AVOID AI-KNOWN CONTENT

**Core principle for CLAUDE.md:** If Claude already knows it, it's NOISE.

**Why this matters:** Generic architectural explanations (layered architecture, MVC patterns, framework basics) waste token budget. CLAUDE.md should document folder-specific weird behaviors and decisions that differ from standard approaches.

**Self-check question:**
> "Would Claude know this without CLAUDE.md?"
> - **YES** → It's noise, remove it (standard patterns, framework explanations)
> - **NO** → It's signal, keep it (folder-specific bugs, non-obvious behaviors)

**Example:**
```markdown
❌ NOISE (AI-known): "This module handles data persistence using repository pattern"
✅ SIGNAL (folder-specific): "Never query same table in RLS policy → infinite recursion (crashed prod, fixed in commit abc123)"

❌ NOISE (AI-known): "Use dependency injection for testability"
✅ SIGNAL (folder-specific): "Singleton leaks NMB per instance → use weak refs in observers (20+ crash reports, devices < 2GB RAM)"
```

**When creating CLAUDE.md, claude-manager must:**
- Skip generic module explanations → NOISE
- Document folder-specific weird behaviors + WHY → SIGNAL
- Skip framework architecture basics → NOISE
- Document critical bugs with production context → SIGNAL

---

## Minimal Core Structure

**REQUIRED:**
```markdown
# [Module/Feature Name]

## Overview
[Folder/module description]

## Weird Parts / Key Patterns
[WHY context - why exists, why chosen, why matters]
```

**OPTIONAL (only if content exists):**
- Critical Mistakes
- Quick Reference
- Cross-References
- Decision Trees
- Custom sections

**Principles:**
- Signal vs Noise
- WHY over HOW
- Avoid things AI knows
- Minimalistic approach

---

## Phase Execution Pattern

**Every phase follows this pattern:**

1. **Paraphrase** phase goal (2-3 sentences)
2. **Ask 5 clarifying questions** specific to this phase
3. **Wait for user confirmation**
4. **Execute phase** (invoke agent or perform inline work)
5. **After completion**, offer commands: `continue`, `skip`, `back`, `stop`

**Template:**
```
Let me verify my understanding of Phase N:
[2-3 sentence paraphrase]

Clarifying questions:
1. [Scope/approach question]
2. [Priorities/constraints question]
3. [Expected output question]
4. [Edge cases question]
5. [Verification criteria question]

Does this match exactly what you want? If not, what should I adjust?
```

[WAIT for user confirmation]

After user confirms:
```
[Execute phase]

Phase N complete. Ready to proceed?
Commands: continue | skip | back | stop
```

---

## Universal Phase 0: Intent Detection

**You do this - no agent**

### Step 1: Detect Intent from Natural Language

**CREATE Mode Keywords:** "create", "new", "need CLAUDE.md for [module]", "document [module]"
**AUDIT Mode Keywords:** "check", "verify", "audit", "signal vs noise", "compliance", "review"
**MODIFY Mode Keywords:** "update", "fix", "add [discovery]", "outdated [info]", "remove [obsolete]"

**Confidence levels:**
- HIGH: Single clear mode
- MEDIUM: Multiple modes possible, one more likely
- LOW: Ambiguous

### Step 2: Find Existing CLAUDE.md Files (if AUDIT/MODIFY)

```bash
Glob: "**/CLAUDE.md"
```

List found files with path and size.

### Step 3: Determine Mode and Scope

```yaml
INTENT_DETECTED:
  mode: [CREATE | AUDIT | MODIFY]
  confidence: [HIGH | MEDIUM | LOW]
  reasoning: [Why this mode was selected]

SCOPE:
  module: [Module name if CREATE/MODIFY single file]
  files: [List of CLAUDE.md files if AUDIT multiple or MODIFY]
```

### Step 4: If Confidence LOW - Ask Clarifying Questions

```
I detected intent as [MODE] with [CONFIDENCE] confidence.

Clarifying questions:
1. Mode: Should I [MODE A] or [MODE B]?
2. Scope: [Scope question]
3. Priority: [Priority question]
4. Expected outcome: [Outcome question]
5. Context: [Context question]

Does this match what you want?
```

[WAIT for confirmation]

### Step 5: Proceed to Mode-Specific Phase 0

- CREATE Mode → Phase 0: Decision Framework
- AUDIT Mode → Phase 0: Scope Selection
- MODIFY Mode → Phase 0: Change Scope

---

## CREATE Mode

**5 Phases:**
1. Phase 0: Decision Framework (inline)
2. Phase 1: Signal Extraction (claude-manager)
3. Phase 2: Structure Design (claude-manager)
4. Phase 3: File Creation (inline)
5. Phase 4: Verification (inline)

---

### CREATE Phase 0: Decision Framework (Inline)

**You do this - no agent**

#### Step 1: CLAUDE.md vs Skill Decision

```
Is this knowledge folder-specific?
├─ YES → Continue to Step 2 (CLAUDE.md)
└─ NO → Suggest /manage-skill instead

    Pattern used by 2+ unrelated modules?
    ├─ YES → Suggest /manage-skill
    └─ NO → Continue to Step 2

    Pattern reusable across project?
    ├─ YES → Suggest /manage-skill
    └─ NO → Continue to Step 2
```

**Rule**: Folder-specific → CLAUDE.md; Project-wide → Skill

**If should be skill:**
```
⚠️ DETECTED: Project-wide knowledge, not folder-specific
💡 SUGGESTION: Consider /manage-skill instead

Reasons:
- [Why project-wide]
- [Why agents need this across project]
```

#### Step 2: Apply 3-Question Filter

**Signal vs Noise filter (all 3 must be YES):**
1. **Project-specific?** (not generic architecture, frameworks Claude knows)
2. **Non-obvious?** (would cause bugs or waste time if not documented)
3. **Critical?** (production impact, frequent reference, weird behavior)

#### Step 3: Check for Existing CLAUDE.md

```bash
ls [module_path]/CLAUDE.md
```

- If exists → Switch to MODIFY mode
- If not exists → Proceed with CREATE

#### MANDATORY Clarifying Questions

```
Let me verify my understanding:
[2-3 sentence paraphrase]

Clarifying questions:
1. CLAUDE.md vs Skill: Is this folder-specific, or project-wide?
2. Source material: Where to extract content - [code/conversation/docs]?
3. Scope: Should this document [specific aspects] or broader?
4. Content availability: Critical Mistakes, Quick Reference to include, or just Overview + Weird Parts?
5. Related patterns: Existing skills to reference?

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
- Module name and path
- 3-question filter results (all YES from Phase 0)
- Source material location
- User confirmations from Phase 0

#### Prompt to Agent

```
MODE: CREATE CLAUDE.md - Signal extraction

MODULE: [name and path]

CONTEXT FROM PHASE 0:
- CLAUDE.md (not skill) because: [reason - folder-specific]
- 3-question filter: ALL YES (project-specific, non-obvious, critical)

SOURCE MATERIAL: [where to extract content from]
USER ADJUSTMENTS: [from Phase 0 clarifying questions]

Task: Extract pure signal from source material using Signal vs Noise 3-question filter.

Apply filter to EVERY piece of content:
- Project-specific? (not generic architecture, frameworks Claude knows)
- Non-obvious? (would cause bugs or waste time if not documented)
- Critical? (production impact, frequent reference, weird behavior)

ANY NO = NOISE → Cut immediately.

DO NOT include:
- Generic CLAUDE.md theory (AI knows format)
- Standard markdown (basic syntax)
- Obvious best practices

Extract categories with minimalist approach:

1. **Overview** (REQUIRED) - Folder/module description
2. **Weird Parts / Key Patterns** (REQUIRED) - WITH WHY CONTEXT (why exists, why chosen, why matters)
3. **Critical Mistakes** (OPTIONAL - only if exists) - WITH WHY CONTEXT (problem, why failed, fix, production impact with metrics)
4. **Quick Reference** (OPTIONAL - only if exists) - Frequently needed facts, file paths, key numbers
5. **Cross-References** (OPTIONAL - only if exists) - Related CLAUDE.md files and skills

⚠️ FLAG PROJECT-WIDE PATTERNS:
If pattern appears project-wide (not folder-specific):
- Pattern used in 2+ unrelated modules → Should be skill
- Pattern reusable across project → Should be skill

Use claude-md and signal-vs-noise skills for extraction patterns.

Output format:
**Overview Extracted:** [description]
**Weird Parts Extracted:** [list with WHY]
**Critical Mistakes Extracted:** [list with Problem/Why/Fix/Impact] OR "None found"
**Quick Reference Items:** [list] OR "None needed"
**Cross-References Needed:** [list] OR "None found"
**Noise Cut:** [what was excluded and why]
**Project-Wide Patterns Flagged:** [patterns that should be skills] OR "None detected"
```

#### After Agent Completes - MANDATORY Clarifying Questions

```
Let me verify my understanding of extracted signal:
[2-3 sentence paraphrase]

Clarifying questions:
1. Overview: Does description capture folder/module purpose correctly?
2. Weird Parts: Did I capture [specific pattern] correctly with WHY context?
3. Optional sections: Are Critical Mistakes/Quick Reference truly needed, or skip?
4. Cross-References: Should I reference [specific CLAUDE.md/skill], or different ones?
5. Project-wide patterns: If flagged [pattern], should that be skill instead?

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
- Extracted signal (from Phase 1: overview, weird parts, optional sections)
- User confirmations/adjustments (from Phase 1)
- Module name and path

#### Prompt to Agent

```
MODE: CREATE CLAUDE.md - Structure design
MODULE: [name and path]

EXTRACTED SIGNAL (from Phase 1):
**Overview:** [description]
**Weird Parts:** [list with WHY]
**Critical Mistakes:** [list with Problem/Why/Fix/Impact] OR "None"
**Quick Reference:** [list] OR "None"
**Cross-References:** [list] OR "None"

USER ADJUSTMENTS: [from Phase 1]

Task: Design minimal CLAUDE.md structure with only necessary sections.

MINIMAL CORE STRUCTURE:
- Always include: Overview, Weird Parts/Key Patterns
- Conditionally include (only if extracted in Phase 1): Critical Mistakes, Quick Reference, Cross-References
- Add custom sections only if user specifically requested
- Apply Signal vs Noise: Only critical project-specific patterns

Use claude-md skill for structure patterns.

Output:
1. Section breakdown (which sections to include, why)
2. Cross-reference plan (which CLAUDE.md to reference, which skills to reference)
3. Content organization (which extracted items go in which section)
4. Justification (why each optional section is included or excluded)
```

#### After Agent Completes - MANDATORY Clarifying Questions

```
Let me verify my understanding of structure design:
[2-3 sentence paraphrase]

Clarifying questions:
1. Minimal structure: Overview + Weird Parts only, or also optional sections?
2. Content allocation: Should [content item] go in [section A] or [section B]?
3. Cross-references: Should I reference [specific CLAUDE.md] in [section], or different location?
4. Optional sections: Include [Critical Mistakes/Quick Reference], or skip?
5. Custom sections: Any additional sections needed?

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

Use Write tool with:
- Minimal core structure (from Phase 2)
- Extracted content (from Phase 1)
- Only sections that have content
- Proper formatting (bold **Why**, code blocks, file paths, tables)

#### Step 2: Verify Formatting

Check:
- Bold **Why** for all WHY context
- Code blocks with language tags
- File paths with line numbers if available
- Tables in Quick Reference (if present)
- Cross-references formatted correctly

```
Phase 3 complete. CLAUDE.md created at [path] with [N] lines.
Ready to proceed?
Commands: continue | skip | back | stop
```

---

### CREATE Phase 4: Verification (Inline)

**You do this - no agent**

#### Verification Checklist

**Minimal Core:**
- [ ] Overview section present
- [ ] Weird Parts/Key Patterns section present
- [ ] No empty sections

**Signal vs Noise:**
- [ ] No generic architecture explanations
- [ ] All content passes 3-question filter
- [ ] Content is folder-specific

**Content verification - Signal vs Noise per section:**
  - [ ] Overview: No generic "what is CLAUDE.md"
  - [ ] Weird Parts: Project-specific edge cases only
  - [ ] No standard markdown formatting rules

**WHY over HOW:**
- [ ] Every pattern has WHY context
- [ ] Critical Mistakes have production impact (if present)

**Cross-References:**
- [ ] All CLAUDE.md references valid (if present)
- [ ] All skill references valid (if present)

**Current State:**
- [ ] Shows HOW IT WORKS NOW

**Optional Sections:**
- [ ] Critical Mistakes present only if content exists
- [ ] Quick Reference present only if content exists
- [ ] Cross-References present only if content exists

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

#### Determine Audit Scope

```bash
# Scope types
specific: Find CLAUDE.md at module path
all: Glob "**/CLAUDE.md"
```

List found files with path and size.

#### MANDATORY Clarifying Questions

```
Let me verify my understanding:
[2-3 sentence paraphrase]

Clarifying questions:
1. Scope: Audit [N] CLAUDE.md files found, or exclude some?
2. Priority focus: Structure, content quality, cross-references, or all?
3. Auto-fix: Fix automatically or just report?
4. Missing CLAUDE.md: Check for modules without CLAUDE.md?
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
- CLAUDE.md files to audit (paths, sizes)
- Audit focus (from Phase 0)
- User decisions (from Phase 0)

#### Prompt to Agent

```
MODE: AUDIT CLAUDE.md (structure compliance)

FILES: [list with paths, sizes]
FOCUS: [from Phase 0]
USER DECISIONS: [from Phase 0]

Task: Audit CLAUDE.md structure for minimal core compliance.

MINIMAL CORE STRUCTURE:
- REQUIRED: Overview, Weird Parts/Key Patterns
- OPTIONAL: Critical Mistakes, Quick Reference, Cross-References, custom sections

Use claude-md skill for structure patterns.

Check for each file:
- Missing REQUIRED sections (Overview, Weird Parts)
- Empty sections (heading present but no content)
- Sections without WHY context (Weird Parts must have WHY)

Output per file:
- File path
- Structure compliance: PASS/FAIL
- Missing REQUIRED sections: [list]
- Empty sections: [list]
- Missing WHY context: [list]
- Severity: critical/moderate/minor
```

#### After Agent Completes - MANDATORY Clarifying Questions

```
Let me verify my understanding of structure audit results:
[2-3 sentence paraphrase]

Clarifying questions:
1. Violations: Are [critical violations] blocking, or proceed with warnings?
2. Missing sections: Add missing REQUIRED sections?
3. Empty sections: Populate empty sections, or flag for manual review?
4. WHY context: Add WHY context where missing?
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

#### Prompt to Agent

```
MODE: AUDIT CLAUDE.md (content quality)

FILES: [list]
STRUCTURE RESULTS: [Phase 1 summary]
USER DECISIONS: [from Phase 1]

Task: Audit CLAUDE.md content for Signal vs Noise, WHY over HOW, and folder-specific knowledge.

Apply "ANY NO = NOISE" to existing CLAUDE.md content.

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

5. **CLAUDE.md vs Skill misplacement**:
   - Content not folder-specific → Should be skill
   - Pattern used in 2+ unrelated modules → Should be skill
   - Project-wide knowledge → Should be skill
   - Flag duplicate patterns across CLAUDE.md files for extraction

Output per file:
- File path
- Content quality: PASS/FAIL
- Signal vs Noise violations: [quote, issue, fix]
- WHY over HOW violations: [quote, issue, fix]
- Production context missing: [list]
- Current state violations: [sections with timeline]
- **Skill misplacement**: [content that should be skills, patterns in 2+ files]
- Severity: critical/moderate/minor
```

#### After Agent Completes - MANDATORY Clarifying Questions

```
Let me verify my understanding of content quality audit results:
[2-3 sentence paraphrase]

Clarifying questions:
1. Noise: Remove all generic content flagged, or keep some with better WHY?
2. WHY missing: Research production context for [pattern], or flag for manual addition?
3. Historical timeline: Update existing content, or preserve history?
4. Skill misplacement: Extract [pattern] to skill now with /manage-skill, or just flag?
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

#### Prompt to Agent

```
MODE: AUDIT CLAUDE.md (cross-references)

FILES: [list]
STRUCTURE RESULTS: [Phase 1 summary]
CONTENT RESULTS: [Phase 2 summary]

Task: Audit cross-references for validity and sufficiency.

Use claude-md skill for cross-reference patterns.

Check:
1. **Broken file paths** - Non-existent files, outdated line numbers
2. **Missing cross-references** - Related CLAUDE.md not linked, skills not referenced
3. **Outdated cross-references** - Section names changed, content moved

Output per file:
- File path
- Cross-reference integrity: PASS/FAIL
- Broken references: [list with paths]
- Missing references: [suggested additions]
- Outdated references: [updates]
- Severity: critical/moderate/minor
```

#### After Agent Completes - MANDATORY Clarifying Questions

```
Let me verify my understanding of cross-reference audit results:
[2-3 sentence paraphrase]

Clarifying questions:
1. Broken references: Fix all broken paths, or flag critical ones only?
2. Missing references: Add all suggested cross-references, or prioritize?
3. Outdated references: Update all, or flag for manual review?
4. Skills: If patterns should be skills, reference them or extract?
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
**Priority 1: Critical**
[List with file, violation, fix]

**Priority 2: Moderate**
[List with file, violation, fix]

**Priority 3: Minor**
[List with file, violation, fix]

**Skill Extraction Opportunities:**
[Content/patterns that should be skills → Suggest /manage-skill with name]

**Migration Plan:**
Phase 1: Fix critical ([N] files)
Phase 2: Fix moderate ([N] files)
Phase 3: Fix minor ([N] files)
Phase 4: Extract patterns to skills ([N] patterns with /manage-skill)
```

#### After Agent Completes - MANDATORY Clarifying Questions

```
Let me verify my understanding of recommendations:
[2-3 sentence paraphrase]

Clarifying questions:
1. Priority: Fix [priority 1] violations immediately, or all at once?
2. Skill extraction: Use /manage-skill to extract [patterns] now, or defer?
3. Migration plan: Does phased approach match your timeline, or adjust?
4. Scope: Handle skill extraction as part of this audit, or separate?
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

**Priority 1: Critical**
- Add missing REQUIRED sections (Overview, Weird Parts)
- Remove noise
- Add WHY context
- Fix broken cross-references

**Priority 2: Moderate**
- Update content
- Add production context
- Fix structure

**Priority 3: Minor**
- Formatting
- Polish

**Skill Extraction:**
- If user approved, use /manage-skill to create skills for project-wide patterns
- Update CLAUDE.md files to reference new skills

Track progress:
```
Fixed: [file]
- [violation 1] → [fix]
- [violation 2] → [fix]

Progress: [N/M] complete
```

#### Verify Fixes

Run verification:
- Minimal core structure
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
- Skills extracted: [N] patterns

Commands: stop | back
```

---

## MODIFY Mode

**4 Phases:**
1. Phase 0: Change Scope (inline)
2. Phase 1: Change Analysis (claude-manager)
3. Phase 2: Implementation (inline)
4. Phase 3: Verification (inline)

---

### MODIFY Phase 0: Change Scope (Inline)

**You do this - no agent**

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
[2-3 sentence paraphrase]

Clarifying questions:
1. Scope: Changes affect [specific sections] or entire CLAUDE.md?
2. Category: Primarily [category A] or [category B]?
3. Approach: [approach A] or [approach B] for [specific change]?
4. Update strategy: UPDATE existing content (replace wrong) or ADD migration note?
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
- CLAUDE.md path
- Changes requested with categories (from Phase 0)
- User confirmations (from Phase 0)

#### Prompt to Agent

```
MODE: MODIFY CLAUDE.md

FILE: [path]
CHANGES: [from Phase 0]
CATEGORIES: [add_discovery, update_outdated, remove_obsolete, restructure, cross_reference]
USER ADJUSTMENTS: [from Phase 0]

Task: Analyze current CLAUDE.md state and plan modifications.

UPDATE STRATEGY:
- Update existing content (replace wrong with correct)
- CLAUDE.md shows HOW IT WORKS NOW, not historical evolution
- Replace outdated patterns with current patterns in-place

⚠️ CHECK FOR SKILL MISPLACEMENT:
If changes add project-wide patterns (not folder-specific):
- Pattern used in 2+ unrelated modules → Should be skill
- Pattern reusable across project → Should be skill

Use claude-md, skill-fine-tuning, signal-vs-noise skills.

Read file and analyze:
1. Current state (sections, size)
2. Changes mapped to sections
3. Impact (cross-references affected)
4. Approach per category:
   - add_discovery: Add to Weird Parts/Critical Mistakes WITH WHY
   - update_outdated: Replace wrong with correct
   - remove_obsolete: Remove or archive
   - restructure: Apply minimal core structure
   - cross_reference: Remove duplicate, add reference

Output:
**Current State:** [summary]
**Change Plan (section by section):** [list]
**Cross-Reference Updates:** [list]
**Project-Wide Patterns Flagged:** [patterns that should be skills] OR "None"
**Implementation Steps:** [ordered]
**Verification Checklist:** [how to verify]
```

#### After Agent Completes - MANDATORY Clarifying Questions

```
Let me verify my understanding of change plan:
[2-3 sentence paraphrase]

Clarifying questions:
1. Scope: Changes affect [specific sections], or broader?
2. Approach: [approach A] or [approach B] for [specific change]?
3. Cross-references: Update [related CLAUDE.md] bidirectionally?
4. Project-wide patterns: If flagged [pattern], should that be skill instead?
5. Verification: After changes, verify [specific aspect]?

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

**Change patterns:**
- **add_discovery**: Add to Weird Parts/Critical Mistakes WITH WHY context + production impact
- **update_outdated**: Replace wrong with correct
- **remove_obsolete**: Remove completely or move to Deprecated section
- **restructure**: Apply minimal core structure
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
- [ ] Content is folder-specific

**Minimal Core:**
- [ ] Overview present
- [ ] Weird Parts present
- [ ] No empty sections

**Cross-References:**
- [ ] All CLAUDE.md cross-references valid
- [ ] All skill cross-references valid
- [ ] File paths and line numbers accurate
- [ ] No broken references introduced
- [ ] Bidirectional references updated (if applicable)

**Current State:**
- [ ] Shows HOW IT WORKS NOW

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
✅ Critical decisions from previous phases (extracted)
✅ User confirmations/adjustments
✅ Specific task for this phase
✅ Expected output format

**Test question:**

> "Can claude-manager produce HIGH QUALITY output with this context alone?"
>
> If YES → sufficient
> If NO → add missing critical info (not everything)

**Example:**
```yaml
✅ SUFFICIENT (50 lines):
  Extracted signal from Phase 1:
  - Overview: [description]
  - Weird Parts: [list with WHY]
  - Critical Mistakes: [list] OR "None"
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

## Success Criteria

Command `/manage-claude-md` should:

1. Detect intent from natural language (CREATE/AUDIT/MODIFY)
2. Find files dynamically using Glob
3. Invoke claude-manager for all agent phases
4. Apply Signal vs Noise filter
5. Enforce WHY over HOW
6. Apply minimal core (only Overview + Weird Parts required)
7. Make optional sections optional
8. Flag skill misplacement (project-wide → /manage-skill)
9. Audit cross-references
10. Ask clarifying questions after Phase 0 and every agent phase
11. Extract decisions (sufficient context)
12. Update existing content (replace wrong)
13. Pass verification
14. Detect pattern duplication (flag for skill extraction)

---

## Notes

- **Pattern**: Mirrors update-skill architecture
- **Agent**: claude-manager has claude-md, signal-vs-noise, skill-fine-tuning skills
- **Signal vs Noise**: 3-question filter (project-specific, non-obvious, critical)
- **Current state**: CLAUDE.md shows HOW IT WORKS NOW
- **Minimal core**: Only Overview + Weird Parts required; everything else optional
- **CLAUDE.md = folder-specific**: Project-wide knowledge → Skill
