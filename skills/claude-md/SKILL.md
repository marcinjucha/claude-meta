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

## ⚠️ CRITICAL: FACT-BASED DOCUMENTATION ONLY

**Why this rule exists:** CLAUDE.md is living documentation of actual project state. Invented production context leads Claude to make decisions based on false constraints.

**What to do:**
- User describes discovery → Document it with real details
- No real data → Use placeholder: `[Real incident details needed]` or ask user
**Why**: Server processes in 15s. Without window, 95% fewer false-positive tickets.

✅ CORRECT (FACT-BASED):
## 15-Second Time Window
**Why**: [User to provide: server processing time and impact]
OR (if user provided):
## 15-Second Time Window (Bug Fix)
**Why**: Server processes in up to 15s (confirmed by user). UI showed errors when operations succeeded.
```

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
**Why**: Server processes in up to 15s. Without window, UI showed "not processed"
even when succeeded. 95% fewer false-positive tickets after fix.
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
**Problem**: Resource leaked NMB per back navigation. Devices crashed.
**Why it failed**: Root kept resource alive. Back navigation didn't destroy.
**Fix**: Moved to LeafComponent with conditional cleanup. Leak fixed.
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
BEFORE: ## Resource Lifecycle
        Resource owned by RootComponent. File: ComponentFlow/RootComponent.ext:45

AFTER:  ## Resource Lifecycle (Ownership Changed - version X)
        Resource owned by LeafComponent, NOT RootComponent.
        **Why**: Previous leaked NMB. Moved for proper cleanup.
        File: ComponentFlow/Leaf/LeafComponent.ext:23
```

**Verify:** Code compiles, file paths correct, numbers current, context accurate.

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
## Deprecated Patterns
### ~~Lazy Init Guard (v1.2 - v2.1)~~ [REMOVED version X]
Framework onAppear bug fixed in version Y. Pattern no longer needed.
**Why kept**: Shows what we tried if bugs resurface.
```

**Remove vs Archive:** Remove obvious mistakes. Archive valid-at-the-time patterns for context.

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
   - Required: Quick Orientation → The Weird Parts → Critical Mistakes → Quick Reference
   - Optional: Architecture Overview, Common Pitfalls, Deprecated Patterns

3. **Apply 80/20 rule:**
   - Keep: Project-specific oddities, critical mistakes
   - Remove: Generic patterns, obvious info

**Example:** 300 lines → 80 lines by removing generic architecture/data layer patterns, keeping only project-specific content.

**Verify:** Each section project-specific, WHY context included, Quick Reference scannable, <500 lines.

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

**Example:** Remove 50-line streaming pattern explanation, keep feature-specific usage + WHY context, reference skill for details.

3. **Update skill if missing:** Add pattern to existing skill or create new skill if substantial.

**Keep in CLAUDE.md vs Skill:**
- CLAUDE.md: Feature-specific usage, local context
- Skill: Reusable pattern, used by 2+ features

---

## Writing Style

**Voice:** Direct, concise. Notes to future you with amnesia.
**Format:** Bullets + Bold **Why**

```markdown
GOOD: Resource owned by LeafComponent. Previous approach leaked NMB.
BAD: The resource manager is owned and managed by the LeafComponent class...
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

### ❌ Mistake 1: Generic Content Instead of Project-Specific

**Problem:** CLAUDE.md filled with framework basics ("Data Layer handles persistence...")

**Why bad:** Claude knows generic patterns. Wastes space, dilutes signal.

**Fix:** Only document project-specific twists + critical mistakes.

### ❌ Mistake 2: Missing WHY Context

**Problem:** Documented WHAT without WHY. Future developer doesn't understand importance, removes pattern, regression.

**Fix:** ALWAYS include WHY (real problem, production incident, user complaint).

```markdown
❌ BAD: "ComponentHistoryService filters history with 15-second window."
✅ GOOD: "**Why**: Server processes in up to 15s. Without window, UI showed errors when operations succeeded."
```

### ❌ Mistake 3: Outdated References After Refactoring

**Problem:** Code moved to ComponentFlow/Leaf/LeafComponent.ext, docs still point to old RootComponent.ext. Wasted developer time searching.

**Fix:** Update file paths immediately after refactoring. Add migration note for major changes.

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

**Scenario:** Memory leak after production incident

**What was added:**
- **The Weird Parts**: Resource lifecycle pattern (why LeafComponent not RootComponent, conditional cleanup)
- **Critical Mistakes**: Document what failed (root component approach, why it leaked)
- **Cross-reference**: Link to skill for full pattern details

**Result:** Future developers understand rationale, production incident prevents regression, 95 lines added (pure signal).

---

**Key Lesson:** CLAUDE.md is living documentation. Update after every significant discovery, production incident, or refactoring. Project-specific + WHY context + Real incident = Good documentation. Good CLAUDE.md = Notes to future you with amnesia.
