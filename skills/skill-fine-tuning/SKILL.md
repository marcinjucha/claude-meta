---
name: skill-fine-tuning
description: Use when skills contain outdated information, imprecise patterns, or missing critical details. Fine-tune existing skills to maintain accuracy as codebase evolves. Critical for preventing skill drift and ensuring Claude has correct patterns.
---

# Skill Fine-Tuning - Maintain Pattern Accuracy

## Purpose

Keep skills accurate as codebase evolves. Update patterns when implementation changes, clarify imprecise instructions, add missing anti-patterns. Prevent skill drift.

## When to Use

- Skill references outdated pattern (code changed since skill written)
- Skill instructions imprecise (causes confusion or wrong implementation)
- Skill missing critical anti-pattern (production bug not documented)
- Skill file paths wrong (refactoring moved files)
- Skill examples no longer compile
- Agent complains "skill unclear" or "pattern doesn't work"
- Production incident reveals skill gap

## Decision Framework: What to Update

Before updating a skill, apply Signal vs Noise filter:

**SIGNAL (Update immediately):**
- Pattern changed (code implementation differs from skill)
- Production bug not documented (happened, not in anti-patterns)
- Missing WHY (rule stated without context/rationale)
- File paths wrong (refactoring moved files)
- Numbers/thresholds changed (configuration adjusted)

**NOISE (Skip update):**
- Cosmetic improvements (rewording without new information)
- Adding generic explanations (Claude knows)
- Obvious clarifications (already clear to reader)
- Time-sensitive info (version numbers, dates)

**See:** `@resources/signal-vs-noise-reference.md` for complete 3-question filter and detailed examples.

## Content Quality: Why over How

**Priority:** WHY explanation > HOW implementation

When updating patterns, ALWAYS include:
- **Why pattern exists** (problem it solves)
- **Why approach chosen** (alternatives considered)
- **Why it matters** (production impact)

**Example transformation:**

❌ **Without WHY (HOW only):**
```markdown
## Pattern: Resource in Feature

Resource owned by LeafComponent:
```
ComponentA {
    var resource: Resource?
}
```
```

✅ **With WHY (Context + Impact):**
```markdown
## Pattern: Resource in Feature (Not Root)

**Why feature ownership:**
- Leaf node knows navigation direction (forward vs back)
- Conditional cleanup prevents memory leak
- Root component can't distinguish navigation context

**Production impact:**
- Before: NMB leak per navigation → crashes on devices
- After: 0MB leak, stable memory

**Implementation:**
```
LeafComponent {
    var resource: Resource?

    case .onDisappear where !isNavigatingBack:
        resource?.pause()  // Forward navigation
    case .onDisappear:
        resource?.cleanup()  // Back navigation
        resource = nil
}
```
```

**See:** `@resources/why-over-how-reference.md` for philosophy and more examples.

## Core Patterns

### Pattern 1: Detecting Skill Drift

**Signs skill needs update:**

```yaml
symptoms:
  outdated_pattern:
    - Agent generates code that doesn't match current implementation
    - File paths in skill don't exist
    - Code examples don't compile
    - Thresholds/numbers wrong (configuration changed)

  imprecise_instructions:
    - Agent asks clarifying questions about skill content
    - Multiple valid interpretations
    - Missing decision criteria
    - Vague "should" without clear WHEN

  missing_anti_patterns:
    - Production bug not in any skill
    - Same mistake made twice (no documentation first time)
    - Common pitfall not warned against

  skill_gaps:
    - Agent can't find pattern for known solution
    - Pattern exists but in wrong skill (hard to find)
    - Integration between skills missing
```

**How to detect:**
1. **Code review:** Implementation differs from skill pattern
2. **Agent confusion:** Claude asks for clarification despite skill existing
3. **Production incident:** Bug happens, skill didn't prevent it
4. **Refactoring:** Code changed, skill not updated

### Pattern 2: Updating Outdated Patterns

**When:** Code implementation changed, skill still describes old approach

```markdown
## Update Process

Step 1: Identify What Changed

Check:
- [ ] Code location (files moved)
- [ ] Pattern itself (new approach)
- [ ] Parameters (thresholds, timeouts adjusted)
- [ ] Dependencies (new dependencies added/removed)
- [ ] Integration (how components interact changed)

Step 2: Update Skill Sections

For each outdated section:

A. Core Patterns
   - Update code examples to match current implementation
   - Update explanations if approach changed
   - Keep WHY if still valid, update if not

B. Anti-Patterns
   - Update "wrong" examples if pattern changed
   - Add new anti-pattern if discovered
   - Update "fix" if approach changed

C. Quick Reference
   - Update commands if syntax changed
   - Update thresholds/numbers to current values
   - Update file paths if moved

D. Real Project Example
   - Verify example still accurate
   - Update file paths
   - Update code snippets if implementation changed

Step 3: Add Migration Note (if major change)

For breaking changes, add note:

## Pattern Migration

**Changed in:** [Date or Version]
**Old pattern:** [Brief description]
**New pattern:** [Brief description]
**Why changed:** [Production reason]

Example:
## Pattern Migration

**Changed in:** Version X (Date)
**Old pattern:** Resource owned by root component
**New pattern:** Resource owned by leaf feature with conditional cleanup
**Why changed:** NMB memory leak in production (root didn't know navigation direction)

Step 4: Verify Examples Compile

- [ ] Copy code example to IDE
- [ ] Verify compiles without errors
- [ ] Check file paths exist
- [ ] Test against current codebase
```

**Example Update:**

**BEFORE (resource-lifecycle-patterns skill):**
```markdown
## Pattern 1: Resource Ownership

Resource owned by RootComponent:

\`\`\`
Component RootComponent {
    state {
        resource: Resource?
    }
}
\`\`\`
```

**AFTER (updated):**
```markdown
## Pattern 1: Resource Ownership in Feature (Not Root)

**Purpose:** Prevent memory leaks through proper ownership

Resource owned by LeafComponent (leaf node), NOT root:

\`\`\`
Component LeafComponent {  // ← Leaf feature, not root
    state {
        resource: Resource?
    }
}
\`\`\`

**Why feature ownership:**
- Leaf node knows navigation direction (forward vs back)
- Can cleanup conditionally based on navigation context
- Prevents memory leak (root preserved resource on all navigation)

**Production incident - Before fix:**
- Resource in root → leaked NMB per back navigation
- Devices crashed after multiple navigations

## Pattern Migration

**Changed in:** Version X (Date)
**Old pattern:** Resource in RootComponent (root)
**New pattern:** Resource in LeafComponent (leaf) + conditional cleanup
**Why changed:** Memory leak eliminated
```

### Pattern 3: Clarifying Imprecise Instructions

**When:** Skill instructions vague, causing agent confusion

```markdown
## Clarification Process

Step 1: Identify Imprecision

Look for:
- "Should" without WHEN (should do X - but when?)
- Multiple interpretations (could mean A or B)
- Missing decision criteria (when to use pattern A vs B?)
- Vague terms ("appropriate", "reasonable", "good" - what values?)

Step 2: Add Decision Criteria

Transform vague → specific:

BEFORE (vague):
"Use appropriate threshold for validation"

AFTER (specific):
"Validation threshold:
- Small items (< Xcm): 25-30%
- Standard items (Y-Zcm): 35% (default)
- Large items (> Ncm): 35-40%"

BEFORE (missing WHEN):
"Should use Service for complex logic"

AFTER (decision tree):
"Use Service when:
- Combining 3+ repositories (prevents cycles)
- OR complex algorithm (multi-criteria, computations)
NOT when:
- Just thin delegation (that's Use Case)
- Single repository access (that's Repository)"

Step 3: Add Examples for Each Case

For each decision branch, show example:

\`\`\`markdown
**Example 1: Service (Multi-Repo)**
DataCombinerService combines repoA + repoB + repoC
→ Service (prevents cycle)

**Example 2: Use Case (Thin Delegation)**
DataListUseCase exposes publisher from DataService
→ Use Case (just delegates)
\`\`\`

Step 4: Add "When to Use" Triggers

Make it scannable:

\`\`\`markdown
## When to Use

- API call returns nil → Check configuration, auth state
- Data positions jittery → Apply deduplication + averaging
- Multiple results detected → Use ranking algorithm
- Calculation returns NaN → Normalize input values
\`\`\`
```

**Example Clarification:**

**BEFORE (imprecise):**
```markdown
## Spatial Deduplication

Use spatial tolerance to deduplicate items.
Tolerance should be appropriate for item size.
```

**AFTER (precise):**
```markdown
## Spatial Deduplication (Xcm Tolerance)

**Purpose:** Prevent same physical item from creating multiple detections

**Default tolerance:** Xcm

**When to adjust:**
- Small products (< Ycm spacing): Y1-Y2cm tolerance
- Standard products (Z1-Z2cm spacing): Xcm tolerance (default)
- Large products (> Ncm spacing): N1-N2cm tolerance

**Why Xcm:**
- System has ±Ycm noise per frame
- Xcm compensates for noise + allows slight movement
- Below Ycm: Same item detected 2-3 times (too strict)
- Above Ncm: Different items merged as one (too loose)

**Production validation:**
- Without: NNN item entries from N physical items
- With Xcm: N unique entries (correct!)
```

### Pattern 4: Adding Missing Anti-Patterns

**When:** Production bug happened, not documented in skill

```markdown
## Process

Step 1: Analyze Production Incident

Gather:
- What went wrong (symptom)
- Root cause (why it happened)
- How it was fixed
- Impact (users affected, severity)

Step 2: Create Anti-Pattern Entry

Structure:
### ❌ Mistake N: [Descriptive Name]

**Problem:** [What breaks, production impact]

\`\`\`
// ❌ WRONG
[Bad code that caused issue]

// ✅ CORRECT
[Fixed code]
\`\`\`

**Why bad:** [Root cause, what happens]

**Fix:** [What to do instead]

**Production incident:** [Brief description of when this happened]

Step 3: Add to Skill

Location in skill:
- If common mistake → "Anti-Patterns (Critical Mistakes)" section
- If subtle → Add note in relevant "Pattern" section
- If blocking → Add to "When to Use" triggers

Step 4: Cross-Reference from Related Skills

If multiple skills relate:
→ Add cross-reference in "Integration with Other Skills"
```

**Example Addition:**

**Skill:** spatial-patterns

**Production Incident:** Same item appeared NNN times (no deduplication)

**Added Anti-Pattern:**
```markdown
## Anti-Patterns (Critical Mistakes)

### ❌ Mistake 1: No Spatial Deduplication

**Problem:** Hundreds of duplicate items from same physical item.
UI laggy, algorithm fails.

\`\`\`
// ❌ WRONG - Every detection is unique
function ingest(detection) {
    const entry = {
        id: generateUUID(),
        groupID: detection.data,
        locations: [detection.location]
    }
    entries[generateUUID()] = entry  // ❌ New entry every frame!
}
\`\`\`

**Why bad:** System captures N-M FPS after throttling. Same item detected
every frame = NNN entries from N items in 60 seconds. UI laggy, algorithm
fails (too many points).

**Fix:**
\`\`\`
// ✅ CORRECT - Check proximity first
if (existing = findExisting(detection.data, detection.location)) {
    existing.locations.push(detection.location)  // Update existing
} else {
    add(newEntry)  // Add only if truly new
}
\`\`\`

**Production incident:** Version X - users reported "hundreds of items"
when scanning. NNN entries → N unique after fix.
```

### Pattern 5: Reorganizing Skill Structure

**When:** Skill grew too large, hard to navigate

```markdown
## Reorganization Triggers

- Skill > 1000 lines (hard to scan)
- Multiple unrelated patterns (should split)
- Can't find pattern quickly (poor organization)
- Duplicate patterns (need deduplication)

## Process

Step 1: Identify Separation Opportunities

Check if skill covers multiple distinct domains:
- YES → Split into separate skills
- NO → Reorganize sections

Example:
domain-specialist (977 lines) covers:
- API patterns → api-patterns
- Spatial tracking → spatial-patterns
- Data processing → data-patterns
- Validation → validation-patterns
- Resource lifecycle → resource-lifecycle-patterns

→ Split into 5 focused skills (400-600 lines each)

Step 2: Apply Standard Structure

Required sections (in order):
1. Purpose (1-2 sentences)
2. When to Use (triggers)
3. Core Patterns (3-5 patterns with examples)
4. Anti-Patterns (Critical Mistakes)
5. Quick Reference (commands/checklists)
6. Integration with Other Skills
7. Real Project Example

Optional sections:
- Decision Trees (if complex decisions)
- Parameter Tuning Guide (if many parameters)

Step 3: Deduplicate Content

If pattern appears in multiple places:
→ Keep in one authoritative location
→ Cross-reference from other locations

Step 4: Verify Navigation

- [ ] Can find any pattern in < 30 seconds
- [ ] Section headers descriptive
- [ ] Quick Reference at end (scannable)
- [ ] Examples near patterns (not separated)
```

### Pattern 6: Adding Advanced Features (Frontmatter, Scripts, Execution)

**When:** Skill needs isolation, script execution, tool restrictions, or dynamic context

#### Adding context: fork (Isolated Execution)

**Trigger:** Skill should run in isolation without conversation history

```markdown
## Decision: Should I add context: fork?

YES if:
- Research task (codebase exploration)
- Analysis task (focused examination)
- Skill has complete prompt (not just guidelines)
- Don't need conversation context

NO if:
- Skill is reference material (guidelines, patterns)
- Needs conversation context
- Just provides knowledge (not actionable task)

## Process

Step 1: Verify Skill Has Complete Prompt

\`\`\`yaml
# ❌ Won't work with fork (no task)
---
name: api-patterns
context: fork  # WRONG - just guidelines
---
Use these API patterns:
- Pattern 1
- Pattern 2

# ✅ Works with fork (complete task)
---
name: deep-research
context: fork
agent: Explore
---
Research $ARGUMENTS:
1. Find files with Glob
2. Analyze code
3. Summarize findings
\`\`\`

Step 2: Pick Subagent Type

\`\`\`yaml
agent: Explore          # Read-only codebase exploration
agent: Plan             # Planning/architecture analysis
agent: general-purpose  # Default (all tools)
agent: custom-agent     # From .claude/agents/
\`\`\`

Step 3: Update Frontmatter

\`\`\`yaml
---
name: existing-skill
context: fork           # NEW
agent: Explore          # NEW
allowed-tools: Read, Grep, Glob  # Optional
---
\`\`\`

Step 4: Test Invocation

Verify skill returns useful results (not empty or confused).
```

#### Adding Script Integration

**Trigger:** Skill needs to generate visual output, process data, or execute complex operations

```markdown
## Process

Step 1: Create scripts/ Directory

\`\`\`bash
mkdir -p .claude/skills/my-skill/scripts
\`\`\`

Step 2: Add Script

\`\`\`python
# scripts/visualize.py
#!/usr/bin/env python3
"""Generate visualization from project data."""

import sys
from pathlib import Path

def generate(target):
    # Script logic...
    output = Path('output.html')
    output.write_text(html)
    print(f'Generated {output.absolute()}')

if __name__ == '__main__':
    target = Path(sys.argv[1] if len(sys.argv) > 1 else '.')
    generate(target)
\`\`\`

Step 3: Update SKILL.md to Reference Script

\`\`\`markdown
---
name: my-skill
allowed-tools: Bash(python *)
---

# My Skill

Generate visualization:

\`\`\`bash
python ~/.claude/skills/my-skill/scripts/visualize.py .
\`\`\`

Creates `output.html` with interactive visualization.
\`\`\`

Step 4: Test Script Execution

Run script manually to verify it works.
```

#### Adding Dynamic Context Injection

**Trigger:** Skill needs live data (PR info, git status, file contents)

```markdown
## Pattern

Use the dynamic injection syntax (exclamation + backtick + command + backtick) to inject command output before Claude sees skill.

**Syntax:** Place exclamation mark before backtick-wrapped command

\`\`\`yaml
---
name: pr-analysis
context: fork
agent: Explore
allowed-tools: Bash(gh *)
---

## Pull request context
- Diff: !(backtick)gh pr diff(backtick)
- Comments: !(backtick)gh pr view --comments(backtick)
- Files: !(backtick)gh pr diff --name-only(backtick)

## Task
Analyze this PR...
\`\`\`

**Note:** In your actual skill file, replace the word (backtick) with the backtick character.

**How it works:**
1. Commands execute BEFORE skill sent to Claude (preprocessing)
2. Output replaces the injection placeholder with actual command output
3. Claude sees fully-rendered prompt with actual data

**When to use:**
- Fetch PR/issue data
- Include git status
- Inject file contents
- Current system state
```

#### Adding Tool Restrictions

**Trigger:** Skill should limit which tools Claude can use

```markdown
## Process

Step 1: Identify Tools Needed

\`\`\`
Read-only analysis → Read, Grep, Glob
Data exploration → Read, Grep, Glob, WebFetch
Write operations → Read, Edit, Write, Bash
\`\`\`

Step 2: Update Frontmatter

\`\`\`yaml
---
name: safe-reader
allowed-tools: Read, Grep, Glob
---
\`\`\`

Claude can use listed tools without approval when this skill active.
User's permission settings still govern other tools.

Step 3: Document Restriction

\`\`\`markdown
## Tool Access

This skill limits Claude to read-only operations:
- Read - File reading
- Grep - Content search
- Glob - File finding
\`\`\`
```

#### Adding String Substitutions

**Trigger:** Skill needs arguments or session-specific values

```markdown
## Available Substitutions

- \`$ARGUMENTS\` - All arguments passed
- \`$ARGUMENTS[0]\` or \`$0\` - First argument
- \`$ARGUMENTS[1]\` or \`$1\` - Second argument
- \`${CLAUDE_SESSION_ID}\` - Current session ID

## Example Update

\`\`\`yaml
# BEFORE (no arguments)
---
name: fix-issue
---
Fix GitHub issue following standards.

# AFTER (with arguments)
---
name: fix-issue
argument-hint: [issue-number]
---
Fix GitHub issue $ARGUMENTS following standards.

# Usage: /fix-issue 123
# Claude sees: "Fix GitHub issue 123 following standards."
\`\`\`
```

### Pattern 7: Adding Mental Model Anti-Patterns (After Systematic Bugs)

**When:** Production bug reveals systematic thinking error, not just implementation mistake

**Signal test: "Is this a mental model error?"**

```
Ask:
├─ Did 2+ developers make SAME mistake independently?
│   └─ YES → Mental model error
├─ Does mistake "feel natural but is wrong"?
│   └─ YES → Mental model error
├─ Was bug repeated after fix (thinking not updated)?
│   └─ YES → Mental model error
└─ NO to all → Regular anti-pattern (not mental model)
```

**Why mental models are signal:**
- Prevent systematic errors (not one-off bugs)
- One mental model fix = prevents N future bugs
- Reveals WHY mistake happens (cognitive bias, incorrect assumption)
- Higher ROI than documenting single bug

**Process:**

```markdown
Step 1: Identify Mental Model Error

After production bug, ask:
- What incorrect thinking led to this?
- Why did developer assume X when Y is correct?
- What natural intuition failed here?

Example: Framework tests (3 developers same mistake)
- Symptom: Manual action after automatic action
- Incorrect thinking: "I sent action → I handle it"
- Correct thinking: "Framework sent action → I receive it"
- Mental model: **Synchronous thinking in async world**

Step 2: Document WHY, Not WHAT

Focus on thinking shift, not mechanical fix:

\`\`\`markdown
### ❌ Mental Model N: [Descriptive Name]

**Incorrect mental model:**
"[One sentence quote of wrong thinking]"

**Why this thinking fails:**
- [Cognitive bias / natural assumption]
- [Context that misleads]

**Correct mental model:**
"[One sentence quote of correct thinking]"

**Production impact:**
[How many bugs / developer efficiency]
\`\`\`

Step 3: Skip Code Examples

Mental model section = WHY (thinking)
Regular anti-pattern = WHAT + HOW (code)

Keep mental models focused on cognitive shift.

Step 4: Add to Appropriate Section

Options:
1. New section: "Anti-Patterns: Common Mental Models That Fail"
   - Use when 3+ mental model errors identified
   - Example: `error-patterns` (6 mental models)

2. Within existing anti-pattern:
   - Add "Why this thinking fails" subsection
   - Explain cognitive bias behind mistake

3. Cross-reference:
   - If mental model documented in another skill
   - Link from regular anti-pattern
```

**Production validation:**
- `error-patterns`: 6 mental models added after framework bugs
- ROI: Prevented 8/10 future test failures (same mental models)
- New developers: 1st attempt pass rate (was 3-5 iterations before)

**Example: Before vs After**

**BEFORE (regular anti-pattern):**
```markdown
### ❌ Mistake: Stub Between Actions

**Problem:** Test stub set after action sent
**Fix:** Set stub before action
```

**AFTER (mental model added):**
```markdown
### ❌ Mental Model: Reactive Setup Instead of Proactive

**Incorrect mental model:**
"Action executes → I quickly stub result"

**Why this thinking fails:**
- Reactive mindset: "I respond to what happens"
- Framework actions execute immediately - no time for reactive setup
- Async world requires proactive thinking

**Correct mental model:**
"Prepare ALL stubs BEFORE flow starts"

**Production impact:**
- 3 developers made same mistake independently
- Would prevent if mental model documented
```

## Decision Trees

### Should I Update Skill or Create New One?

```
Pattern is variation of existing? → Update existing skill
Pattern is completely new domain? → Create new skill
Existing skill too large (> 1000 lines)? → Split into multiple skills
Pattern used by 2+ features? → Add to skill (not CLAUDE.md)
Pattern feature-specific? → Keep in CLAUDE.md (not skill)
```

### Which Skill Section Needs Update?

```
Pattern implementation changed? → Update "Core Patterns" section
New anti-pattern discovered? → Add to "Anti-Patterns" section
File moved? → Update "Real Project Example" file paths
Numbers/thresholds changed? → Update "Quick Reference" + relevant patterns
Integration changed? → Update "Integration with Other Skills"
Need isolation? → Add frontmatter: context: fork, agent: [type]
Need live data? → Add dynamic injection (exclamation + backtick syntax)
Need script execution? → Add scripts/ directory + reference in SKILL.md
Need tool restrictions? → Add frontmatter: allowed-tools: [list]
Need arguments? → Add frontmatter: argument-hint, use $ARGUMENTS in body
```

### Should I Add Advanced Features?

```
Skill runs research/analysis without conversation context? → Add context: fork
Skill needs live PR/git data? → Add dynamic injection (! + backtick + command)
Skill generates visual output? → Add script integration (scripts/ dir)
Skill should limit tool access? → Add allowed-tools
Skill takes arguments? → Add argument-hint + $ARGUMENTS
Skill only for manual use? → Add disable-model-invocation: true
Skill is background knowledge? → Add user-invocable: false
```

### How Much to Change?

```
Minor update (file path, number)? → Update inline, no migration note
Pattern tweak (same approach)? → Update pattern, mention in description
Breaking change (new approach)? → Update pattern + add "Pattern Migration" note
Complete replacement? → Keep old in "Deprecated Patterns", add new
```

## Anti-Patterns (Common Mistakes)

### ❌ Mistake 1: Not Updating After Refactoring

**Problem:** Code refactored, skill references old structure

```markdown
❌ BAD (skill not updated):
File: ComponentA/RootComponent.swift:line 45

[File moved to ComponentA/SubComponent/LeafComponent.swift 2 months ago]

✅ GOOD (skill updated):
File: ComponentA/SubComponent/LeafComponent.swift:line 23
(Moved from RootComponent.swift version X - memory leak fix)
```

**Why bad:** Wastes developer time searching wrong location. Erodes trust in skills.

**Fix:** Update skills immediately after refactoring. Add migration note.

### ❌ Mistake 2: Vague Instructions

**Problem:** Skill says "use appropriate value" without defining "appropriate"

```markdown
❌ VAGUE:
"Use appropriate threshold for validation"

✅ SPECIFIC:
"Validation threshold:
- Small items (< Xcm): 25-30%
- Standard (Y-Zcm): 35% (default)
- Large (> Ncm): 35-40%"
```

**Why bad:** Agent must guess, might guess wrong. No decision criteria.

**Fix:** Replace vague terms with specific values/decision trees.

### ❌ Mistake 3: Missing Production Context

**Problem:** Pattern added without WHY or real incident

```markdown
❌ NO CONTEXT:
## Pattern: Use Xcm deduplication tolerance

✅ WITH CONTEXT:
## Pattern: Xcm Deduplication Tolerance

**Production incident:** Version X - users reported "hundreds of items"
when scanning. NNN entries from N physical items.

**Root cause:** No deduplication. System ±Ycm noise + N-M FPS capture
= same item detected every frame.

**Fix:** Xcm tolerance filters noise. NNN entries → N unique.
```

**Why bad:** Future developer doesn't understand importance, might remove or change.

**Fix:** ALWAYS include production context (incident, bug report, user complaint).

### ❌ Mistake 4: Outdated Examples

**Problem:** Code example doesn't compile with current codebase

```markdown
❌ OUTDATED (doesn't compile):
\`\`\`
const resource = OldResourceClass()  // OldResourceClass removed version X
\`\`\`

✅ UPDATED (compiles):
\`\`\`
const resource = NewResourceClass()  // Renamed in version X
\`\`\`
```

**Why bad:** Breaks trust. Agent generates code that doesn't compile.

**Fix:** Verify examples compile after every major refactoring.

### ❌ Mistake 5: Wrong context: fork Usage

**Problem:** Added `context: fork` to reference skill (guidelines only), returns nothing useful

```markdown
❌ WRONG (fork with guidelines):
---
name: api-patterns
context: fork
---
Use these API patterns:
- Pattern A
- Pattern B

Result: Subagent receives guidelines but no task → returns nothing

✅ CORRECT (fork with complete task):
---
name: api-research
context: fork
agent: Explore
---
Research API usage for $ARGUMENTS:
1. Find files
2. Analyze patterns
3. Summarize findings

Result: Subagent executes research → returns summary
```

**Why bad:** `context: fork` requires explicit instructions (complete prompt). Guidelines alone don't work.

**Fix:** Only use `context: fork` for skills with actionable tasks, not reference material.

### ❌ Mistake 6: Skill Bloat

**Problem:** Skill covers too many unrelated patterns (> 1000 lines)

```markdown
❌ TOO LARGE:
domain-specialist (977 lines):
- API patterns
- Spatial tracking
- Data processing
- Validation
- Resource lifecycle

✅ SPLIT:
api-patterns (520 lines)
spatial-patterns (550 lines)
data-patterns (700 lines)
validation-patterns (650 lines)
resource-lifecycle-patterns (500 lines)
```

**Why bad:** Hard to navigate. Can't find pattern quickly. Agent loads unnecessary content.

**Fix:** Split into focused skills (400-600 lines each) when > 1000 lines.

## Quick Reference

**Detecting Drift:**
- Code differs from skill → Update pattern
- File paths wrong → Update paths
- Agent confused → Clarify instructions
- Production bug → Add anti-pattern

**Updating Process:**
1. Identify what changed (code, pattern, numbers, location)
2. Update relevant sections (patterns, anti-patterns, examples, quick ref)
3. Add migration note if breaking change
4. Verify examples compile

**When to Update:**
- Immediately after refactoring (file moves, pattern changes)
- After production incident (add anti-pattern)
- After threshold tuning (update numbers)
- When agent confused (clarify instructions)

**Structure:**
- Standard sections: Purpose → When to Use → Patterns → Anti-Patterns → Quick Ref
- Max ~600 lines per skill (split if larger)
- Examples must compile

**Reference Materials:**
- `@resources/signal-vs-noise-reference.md` - 3-question filter for deciding what to update
- `@resources/why-over-how-reference.md` - Content quality philosophy (WHY > HOW)
- `@resources/skill-structure-reference.md` - Standard structure and best practices
- `@resources/skill-ecosystem-reference.md` - Skill locations, sharing, and permissions (where skills live, how to distribute)

## Integration with Other Skills

- **claude-md-maintenance** - Update CLAUDE.md when skill changes
- **signal-vs-noise** - Filter updates (project-specific only)
- **agent-skill-architecture** - Follow OS/Application architecture when updating

## Real Project Example

**Scenario:** Resource lifecycle pattern changed (memory leak fix)

**Skill Before (resource-lifecycle-patterns):**
```markdown
## Pattern 1: Resource Ownership

Resource owned by root component:
\`\`\`
Component RootComponent {
    state {
        resource: Resource?
    }
}
\`\`\`
```

**Production Incident:**
- NMB memory leak per back navigation
- Devices crashed after multiple navigations
- Root cause: Root component didn't know navigation direction, always preserved resource

**Skill After (updated):**
```markdown
## Pattern 1: Resource Ownership in Feature (Not Root)

**Purpose:** Prevent memory leaks through proper ownership

Resource owned by LeafComponent (leaf node), NOT root:

\`\`\`
Component LeafComponent {  // ← Leaf feature, not root
    state {
        resource: Resource?
    }

    onDisappear() {
        if (!isNavigatingBack) {
            // Forward navigation - preserve resource
            resource.pause()
            return
        }

        // Back navigation - destroy resource
        resource.cleanup()
        resource = null
        cancelOperations()
    }
}
\`\`\`

**Why feature ownership:**
- Leaf node knows navigation direction (navigation context awareness)
- Conditional cleanup prevents leak
- Root component can't distinguish forward vs back

**Production incident - Version X:**
- Before: Resource in root → NMB leak per back navigation
- After: Resource in leaf → 0MB leak, stable memory

## Pattern Migration

**Changed in:** Version X (Date)
**Old pattern:** Resource in RootComponent (root component)
**New pattern:** Resource in LeafComponent (leaf feature) with conditional cleanup
**Why changed:** Memory leak eliminated (root didn't know navigation direction)
**Migration:** Move resource state from root to leaf + add navigation context conditional

## Anti-Patterns (Critical Mistakes)

### ❌ Mistake 1: Resource in Root Component

**Problem:** NMB memory leak per back navigation

[Full anti-pattern entry...]
```

**Result:**
- Skill updated with current pattern
- Production incident documented
- Migration path clear
- Anti-pattern prevents regression
- Future developers understand WHY feature ownership

---

**Key Lesson:** Skills drift without maintenance. Update immediately after refactoring, production incidents, or pattern changes. Always add WHY (production context). Verify examples compile.
