---
name: ai-claude-md
description: Create and maintain CLAUDE.md files with project-specific signal. Use when: creating new CLAUDE.md for a feature, updating outdated patterns after refactoring, removing obsolete sections, or deciding what belongs in CLAUDE.md vs a skill.
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

**Note:** Fact-based and signal-only rules enforced by ai-manager-agent system prompt.

## Core Philosophy

- **Quality > Line Count** — 600 lines of pure signal beats 300 lines with 50% noise
- **Self-check** — "Would Claude know this without CLAUDE.md?" YES = noise, NO = signal
- **WHY > HOW** — every section must explain WHY (real problem, alternatives considered, production impact)

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
**Why**: Server processes in up to 15s. Without window, UI showed errors when operations succeeded.
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

- `@../resources/signal-vs-noise-reference.md` - 3-question filter for content decisions
- `@../resources/why-over-how-reference.md` - WHY > HOW philosophy
- `@../resources/skill-structure-reference.md` - Structure best practices

**Related skills:** ai-skill-fine-tuning (update skills when patterns change), ai-skill-creator (create new skills for reusable patterns)

