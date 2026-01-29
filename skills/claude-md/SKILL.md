---
name: claude-md
description: Write and maintain CLAUDE.md documentation files. Use when creating new CLAUDE.md, updating existing documentation (adding patterns, fixing outdated info, restructuring), or removing obsolete sections. Critical for keeping documentation accurate as codebase evolves.
argument-hint: ""
---

# CLAUDE.md - Write & Maintain Documentation

## Purpose

Create and maintain focused, actionable CLAUDE.md documentation that Claude actually follows. Guide for both creating new documentation and evolving existing docs as codebase changes.

## When to Use

**Creating new CLAUDE.md:**
- New feature implemented, needs documentation
- Discovered project-specific pattern worth documenting
- Feature has non-obvious behaviors ("weird parts")
- Made critical mistakes during implementation

**Updating existing CLAUDE.md:**
- Code changed, existing documentation outdated
- Production incident reveals missing documentation
- Refactoring changed architecture, docs need update
- Skills reference wrong file paths or line numbers
- Pattern no longer used (needs deprecation)

---

## Core Philosophy

### Quality > Line Count

**Priority:** Content Quality > Line Count. Project-specific weird stuff + WHY > brevity.

Better:
  600 lines of pure signal (every line project-specific)
Than:
  300 lines with 50% noise (generic patterns Claude knows)

### The Test Question

**Before including ANY information, ask:**

> "Is this something Claude already knows?"
> - YES → Cut it
> - NO → Keep it (with WHY)

### WHY > HOW

**Every section must explain WHY:**
- WHY this pattern exists (real problem we hit)
- WHY approach chosen (alternatives considered)
- WHY it matters (production impact, user complaints)

---

## Core Patterns

### Pattern 1: Adding New Discovery

**When:** Discovered project-specific oddity or critical mistake during implementation

#### Structure for New Weird Part

```markdown
## The [Thing] ([Why It's Weird])

[Minimal description of what it is]

**Why**: [Real problem we hit, production incident, or user complaint]

[Optional: Minimal code example]
```

**Example:**
```markdown
## 15-Second Time Window (Bug Fix)

ComponentHistoryService filters history with 15-second time window.

**Why**: Server processes operations in up to 15 seconds. Without window, UI showed
"not processed" even when operation succeeded. Users reported bugs, created support
tickets. Window prevents false negatives. 95% fewer false-positive tickets after fix.

Implementation:
```language
let recentOperations = history.filter { operation in
    operation.timestamp > Date().addingTimeInterval(-15)
}
```
```

#### Structure for Critical Mistake

```markdown
### ❌ [What We Tried]

**Problem**: [What broke, production impact]

**Why it failed**: [Root cause]

**Fix**: [What we do now]
```

**Example:**
```markdown
### ❌ Resource in Root Component (Memory Leak)

**Problem**: Resource in RootComponent leaked NMB per back navigation.
Devices crashed after 3 navigations. Production issue.

**Why it failed**: Root component kept resource alive across entire flow. Back
navigation didn't destroy resource instance.

**Fix**: Moved resource to LeafComponent with conditional cleanup.
Only dispose on actual dismiss, not forward navigation. Leak fixed.
```

**Where to Add:**
- "The Weird Parts" section → non-obvious behaviors
- "Critical Mistakes We Made" section → bugs/errors fixed
- "Quick Reference" section → frequently needed facts

**Apply signal-vs-noise filter:**
- Is this project-specific? (not generic pattern Claude knows)
- Would lack of this cause bugs or waste time?
- Is this non-obvious to future developer?
→ All YES → Document it

### Pattern 2: Updating Outdated Information

**When:** Code changed, pattern no longer accurate

**Triggers:**
- File moved to different location
- Pattern replaced with better approach
- Numbers changed (thresholds, timeouts, etc.)
- Component ownership changed

**Update Process:**

1. **Identify what changed:**
   - Code location (file moved)
   - Pattern itself (new approach)
   - Parameters (thresholds adjusted)
   - Ownership (component moved to different layer)

2. **Update relevant sections:**
   - Fix file paths (❌ OLD_PATH → ✅ NEW_PATH)
   - Update pattern description
   - Update code examples
   - Update numbers/thresholds
   - Add migration note if major change

3. **Add deprecation note if needed**

**Example Update:**

```markdown
BEFORE:
## Resource Lifecycle
Resource owned by RootComponent.
File: ComponentFlow/RootComponent.ext:line 45

AFTER:
## Resource Lifecycle (Ownership Changed - version X)
Resource owned by LeafComponent, NOT RootComponent.
**Why**: Previous approach leaked NMB. Moved to leaf component for proper cleanup.
File: ComponentFlow/Leaf/LeafComponent.ext:line 23

~~Previous: RootComponent owned resource (deprecated version X)~~
```

**Verification:**
- [ ] Code example still compiles
- [ ] File paths correct
- [ ] Numbers match current implementation
- [ ] Context still accurate

### Pattern 3: Removing Obsolete Sections

**When:** Pattern no longer used, feature removed

**Triggers:**
- Pattern completely replaced
- Feature deprecated/removed
- Workaround no longer needed (bug fixed in library)

**Removal Process:**

1. **Verify obsolescence:**
   - Pattern not used anywhere in codebase
   - Feature fully removed
   - Workaround replaced with proper fix

2. **Remove or archive:**

**Option A: Full removal** (pattern never needed)
→ Delete section entirely

**Option B: Archive with deprecation** (historical context useful)
→ Move to "Deprecated Patterns" section at end
→ Add strikethrough + deprecation date

**Example Archive:**

```markdown
## Deprecated Patterns (Historical Context)

### ~~Lazy Init Guard (v1.2 - v2.1)~~ [REMOVED version X]

Previously used loaded flag to prevent double-init. Framework onAppear bug
fixed in version Y. Pattern no longer needed for version Y+ deployment target.

**Why kept here**: If bugs resurface, this shows what we tried.
```

**When to Remove vs Archive:**
- Remove: Obvious mistake, never should document
- Archive: Valid pattern at the time, might be useful context

### Pattern 4: Restructuring for Clarity

**When:** Doc grown too large, hard to navigate (> 500 lines)

**Triggers:**
- Too many sections
- Mixed concerns
- No clear structure
- Critical info buried

**Restructure Process:**

1. **Extract feature-specific docs:**

If CLAUDE.md covers multiple features:
→ Split into feature-specific CLAUDE.md files

Example:
```
Project/CLAUDE.md (overview)
Project/Module/FeatureA/CLAUDE.md (FeatureA)
Project/Module/FeatureB/CLAUDE.md (FeatureB)
```

2. **Apply standard structure:**

**Required sections (in order):**
1. `# [Feature] - Quick Orientation` (1-2 sentences)
2. `## The Weird Parts` (non-obvious behaviors)
3. `## Critical Mistakes We Made` (bugs/errors fixed)
4. `## Quick Reference` (5-10 bullet facts)

**Optional sections:**
- `## Architecture Overview` (if complex)
- `## Common Pitfalls` (preventive warnings)
- `## Deprecated Patterns` (historical context)

3. **Apply 80/20 rule:**

Keep 20% of content that provides 80% of value:
- Project-specific oddities → Keep
- Critical mistakes → Keep
- Generic patterns → Remove
- Obvious info → Remove

**Example Before (300 lines):**
```markdown
## Feature Documentation
[100 lines of generic architectural patterns]
[50 lines of generic data layer patterns]
[30 lines about 15-second window]
[120 lines of API documentation]
```

**Example After (80 lines):**
```markdown
## FeatureA - Data Processing with Progress

## The Weird Parts
### 15-Second Time Window (Bug Fix)
[30 lines - this is project-specific!]

## Quick Reference
- 15s window prevents false "not processed"
- Service combines 5 data sources (prevents cycles)
- Callback pattern for background operations
```

**Verification:**
- [ ] Each section answers: "Is this project-specific?"
- [ ] Context included (see Core Philosophy)
- [ ] Quick Reference scannable (bullets)
- [ ] Total length reasonable (< 500 lines for feature doc)

### Pattern 5: Cross-Referencing Skills

**When:** Skill covers topic better than CLAUDE.md

**Triggers:**
- CLAUDE.md duplicates skill content
- Same pattern explained in both places
- Maintenance burden (update both places)

**Cross-Reference Process:**

1. **Identify duplication:**

Check if pattern already in skill:
- Architecture patterns
- Framework-specific patterns
- Critical bug patterns

2. **Keep project-specific, reference skill for details:**

CLAUDE.md:
- Keep: How this feature uses the pattern
- Keep: Project-specific context
- Remove: Generic pattern explanation
- Add: Reference to skill for details

**Example:**

```markdown
BEFORE (CLAUDE.md):
## Data Streaming Pattern in FeatureA
ComponentX subscribes to data streams with cancellation...
[50 lines explaining data streaming pattern]

AFTER (CLAUDE.md):
## Data Streaming Pattern
ComponentX uses callback pattern for background operation completion.
**Why**: Background completion runs outside main context. Standard direct calls
don't work. See skill documentation for pattern details.
```

3. **Update skill if missing:**

If pattern not in any skill but used across features:
→ Consider adding to existing skill
→ Or create new skill if substantial

**When to Keep in CLAUDE.md vs Move to Skill:**
- Keep in CLAUDE.md: Feature-specific usage, local context
- Move to Skill: Reusable pattern, used by 2+ features

---

## What to INCLUDE

### Project-Specific Oddities
```markdown
## The 15-Second Time Window
ComponentHistoryService filters history with 15-second window.
**Why**: Server takes up to 15s to process. Without window, UI shows
"not processed" even when operation succeeded. Users complained.
```

### Real Problems You Hit
```markdown
## Resource Lifecycle (Memory Leak Fix)
Resource owned by LeafComponent, NOT RootComponent.
**Why**: Previous approach leaked NMB when navigating back.
Happened in production, caused crashes on devices.
```

### Critical Mistakes Made
```markdown
### Putting Models in Wrong Layer First
**Problem**: Had to move 8 files when second feature needed them
**Solution**: If model has potential for reuse → Core module immediately
```

---

## What to EXCLUDE

### Generic Patterns (Claude Knows)
```markdown
❌ DON'T INCLUDE:

## Architectural Pattern
Follows standard architecture pattern...

## Data Layer
Repositories handle data access...

## Clean Architecture Layers
Presentation → Business → Data → Models
```

---

## Writing Style

**Voice:** Direct, concise. Notes to future you with amnesia.

```markdown
GOOD:
Resource owned by LeafComponent. Previous approach leaked NMB.

BAD:
The resource manager is owned and managed by the LeafComponent
class. This is an important architectural decision that was made after...
```

**Format:** Bullets + Bold **Why**

```markdown
GOOD:
## Sequential Processing
After operation completes → move to next item automatically.
**Why**: Users complained about repetitive navigation (5 taps per item).
```

---

## Decision Trees

### What Section Does Update Belong In?

```
Discovered non-obvious behavior? → "The Weird Parts" (include why)
Fixed production bug? → "Critical Mistakes We Made" (include why)
Frequently needed fact? → "Quick Reference"
Architecture change? → Update existing section + migration note
Pattern no longer used? → "Deprecated Patterns" or remove
Generic pattern Claude knows? → Don't add (or remove if exists)
```

### Should I Update CLAUDE.md or Skill?

```
Pattern used by this feature only? → CLAUDE.md
Pattern used by 2+ features? → Skill (create or update)
Duplicates existing skill? → Remove from CLAUDE.md, cross-reference skill
Feature-specific context? → Keep in CLAUDE.md even if pattern in skill
```

### How Much Detail?

```
Apply signal-vs-noise:
- Project-specific oddity? → Detailed (with context)
- Generic pattern? → Remove entirely
- Critical mistake? → Detailed (problem + fix)
- Frequently referenced? → Bullet in Quick Reference
- Historical context? → Brief in Deprecated section
```

---

## Template

```markdown
# [Feature] - Quick Orientation

[1-2 sentence description]

## The Weird Parts

### [Weird Thing #1]
**Why**: [Real problem we hit]
[Minimal code example if needed]

## Critical Mistakes We Made

### [Thing We Tried That Failed]
**Problem**: [What broke]
**Fix**: [What we do now]

## Quick Reference
- [5-10 critical facts in bullet form]
```

---

## Anti-Patterns (Common Mistakes)

### ❌ Mistake 1: Adding Generic Patterns

**Problem:** CLAUDE.md filled with architectural, framework basics

```markdown
❌ DON'T ADD:
## Architectural Pattern
Standard architecture pattern implementation...

## Data Layer
Repositories handle data access and provide abstraction over...
```

**Why bad:** Claude already knows generic patterns. Just noise.

**Fix:** Only add project-specific twists or critical mistakes.

### ❌ Mistake 2: Not Explaining WHY

**Problem:** What without WHY is just code duplication

```markdown
❌ BAD:
## 15-Second Time Window
ComponentHistoryService filters history with 15-second window.

✅ GOOD:
## 15-Second Time Window (Bug Fix)
ComponentHistoryService filters history with 15-second window.
**Why**: Server processes operations in up to 15 seconds. Without window,
UI showed "not processed" even when operation succeeded. 30% of support
tickets were false alarms. Window fixed 95% of false negatives.
```

**Why bad:** Future developer doesn't understand importance, might remove.

**Fix:** ALWAYS include WHY (real problem, production incident, user complaint).

### ❌ Mistake 3: Outdated File References

**Problem:** Code moved, CLAUDE.md still references old location

```markdown
❌ OUTDATED:
Resource lifecycle in RootComponent.ext:line 45

✅ UPDATED:
Resource lifecycle in ComponentFlow/Leaf/LeafComponent.ext:line 23
(Moved from RootComponent version X - memory leak fix)
```

**Why bad:** Wastes developer time searching wrong location.

**Fix:** Update file paths when refactoring. Add migration note if major change.

### ❌ Mistake 4: No Structure (Wall of Text)

**Problem:** 500-line CLAUDE.md with no sections, hard to scan

```markdown
❌ BAD:
# FeatureA

Components are...resource is...data pattern...time window...service combines...

✅ GOOD:
# FeatureA - Quick Orientation

## The Weird Parts
### 15-Second Time Window
### Service Combines 5 Data Sources

## Critical Mistakes We Made
### ❌ Repository Cycle

## Quick Reference
- 15s window prevents false negatives
- Service pattern prevents cycles
```

**Why bad:** Can't find information quickly. Critical info buried.

**Fix:** Apply standard structure. Use headers. Keep Quick Reference scannable.

### ❌ Mistake 5: Duplicating Skill Content

**Problem:** Same pattern in CLAUDE.md and skill, maintenance burden

```markdown
❌ DUPLICATE (in CLAUDE.md):
## Data Streaming Pattern
Data streaming uses cancellation and retry logic...
[50 lines of generic streaming pattern]

✅ REFERENCE (in CLAUDE.md):
## Data Streaming Pattern
FeatureA uses callback pattern for background operation completion.
**Why**: Background completion outside main context.
See skill documentation for pattern details.
```

**Why bad:** Must update two places. Likely to drift out of sync.

**Fix:** Keep project-specific usage + WHY context. Reference skill for pattern details.

---

## Quick Reference

**Creating new CLAUDE.md:**
- Voice: Direct, concise (notes to future you with amnesia)
- Format: Bullets + Bold **Why**
- Template: Orientation → Weird Parts → Mistakes → Quick Ref
- Test: "Is this something Claude already knows?" → YES = Cut

**Adding Content:**
- New weird part → "The Weird Parts" section
- Bug fix → "Critical Mistakes We Made" section
- Frequent fact → "Quick Reference" section
- Include WHY context (see Core Philosophy)

**Updating Content:**
- Code changed → Update file paths, examples, numbers
- Pattern replaced → Update description + add migration note
- Major change → Add deprecation date to old pattern

**Removing Content:**
- Pattern obsolete → Remove or archive in "Deprecated Patterns"
- Generic pattern → Remove entirely (Claude knows)
- Duplicates skill → Remove, add cross-reference

**Structure:**
- Standard sections: Orientation → Weird Parts → Mistakes → Quick Ref
- 80/20 rule: Keep 20% content providing 80% value
- Max ~500 lines per feature (split if larger)

**Cross-Referencing:**
- Pattern in skill → Reference skill from CLAUDE.md
- Keep feature-specific context in CLAUDE.md
- Update skill if pattern missing

---

## Self-Check

Before committing CLAUDE.md:

1. **Obviousness**: Would Claude know this already? → Cut
2. **Specificity**: Is this project-specific? → Keep
3. **WHY context**: Do I explain WHY? → Required (see Core Philosophy)
4. **Actionability**: Would this help me in 6 months? → Keep
5. **Structure**: Standard sections applied? → Required
6. **Scannable**: Quick Reference in bullet form? → Required

---

## Resources

**Philosophy and Guidelines:**
- `@resources/signal-vs-noise-reference.md` - 3-question filter for deciding what to include
- `@resources/why-over-how-reference.md` - Content quality philosophy (WHY > HOW, production context)
- `@resources/skill-structure-reference.md` - Standard structure and best practices (adaptable to CLAUDE.md)

**Use references for:**
- Signal vs Noise → Filter what to document (project-specific only, not generic)
- Why over How → Include rationale for patterns (why pattern exists, why it matters)
- Structure → Consistent organization (required sections, optional sections)

**Why included:**
- Consistent philosophy across all meta skills (skills, agents, workflows, docs)
- Decision framework for documentation content (what to include, what to skip)
- Quality guidelines (completeness > brevity, WHY mandatory - see Core Philosophy)

---

## Integration with Other Skills

- **signal-vs-noise** - Filter content (project-specific only)
- **skill-fine-tuning** - Update skills when patterns change
- **skill-creator** - Create new skills for reusable patterns

---

## Real Project Example

**Scenario:** Discovered memory leak after production incident

**CLAUDE.md Before:**
```markdown
# ComponentFlow - Data Processing

Flow coordinates scan → process → store phases.
```

**CLAUDE.md After (added discovery):**
```markdown
# ComponentFlow - Data Processing

## The Weird Parts

### Resource Lifecycle (Memory Leak Fix - version X)

Resource owned by LeafComponent, NOT RootComponent.

**Why**: Previous approach leaked NMB per back navigation. Devices
crashed after 3 navigations in production. Customer complaints escalated.

Conditional cleanup based on navigation direction:
- Forward nav → `stopResource()` (preserve for return)
- Back nav → `destroyResource() + nil` (destroy completely)

File: ComponentFlow/Leaf/LeafComponent.ext:line 23
See skill documentation for full pattern.

## Critical Mistakes We Made

### ❌ Resource in Root Component

**Problem**: RootComponent owned resource → NMB leak per navigation.

**Why it failed**: Root component doesn't know navigation direction (forward vs
back). Always preserved resource. Leaked on back navigation.

**Fix**: Moved to leaf component (LeafComponent) with conditional
cleanup. Leak eliminated.
```

**Result:**
- Future developers understand resource placement rationale (leaf vs root)
- Production incident documented (prevents regression)
- Cross-referenced skill for full pattern details
- 95 lines added (signal, not noise)

---

**Key Lesson:** CLAUDE.md is living documentation. Update after every significant discovery, production incident, or refactoring. Project-specific + WHY context + Real incident = Good documentation. Good CLAUDE.md = Notes to future you with amnesia.
