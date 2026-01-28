# Skill Structure Reference - Standard Organization

**Purpose:** Standard sections and organization for skills. Ensures consistency and discoverability.

---

## Required Sections (All Skills)

Every skill MUST include these sections in this order:

### 1. Purpose (Required)

**What:** 1-2 sentences describing what problem this skill solves

**Important distinction:**
- **`description`** (in YAML header) - Used by agents to decide whether to load this skill. Must contain clear triggers.
- **`Purpose`** (in content) - Human-readable explanation of the problem this skill solves.

**Example:**
```markdown
---
name: skill-fine-tuning
description: Use when skills contain outdated information, imprecise patterns, or missing critical details. Fine-tune existing skills to maintain accuracy as codebase evolves. Critical for preventing skill drift and ensuring Claude has correct patterns.
---

# Skill Fine-Tuning - Maintain Pattern Accuracy

## Purpose

Keep skills accurate as codebase evolves. Update patterns when implementation changes, clarify imprecise instructions, add missing anti-patterns.
```

**Note:** The `description` field is critical for agent routing. It should include:
- **When to use** triggers (e.g., "Use when skills contain outdated information")
- **What it does** (e.g., "Fine-tune existing skills")
- **Why it matters** (e.g., "Critical for preventing skill drift")

---

### 2. When to Use (Required)

**What:** Specific triggers that indicate this skill is needed

**Format:** Bulleted list of scenarios

**Example:**
```markdown
## When to Use

- Skill references outdated pattern (code changed since skill written)
- Skill instructions imprecise (causes confusion)
- Production bug happened but not documented
- File paths wrong (refactoring moved files)
- Agent complains "skill unclear"
```

**Note:** Should answer "When does Claude invoke this skill?"

---

### 3. Core Patterns (Required)

**What:** 3-5 primary patterns with examples

**Format:**
- Pattern name (clear, descriptive)
- Purpose statement
- Code example (if applicable)
- WHY explanation (context, rationale)
- When to use (specific triggers)

**Example:**
```markdown
## Core Patterns

### Pattern 1: Resource Ownership in Component

**Purpose:** Prevent memory leaks through proper ownership

**Why component ownership:**
- Leaf component knows navigation direction
- Can cleanup conditionally
- Root can't distinguish forward vs back

**Production impact:**
- Before: NMB leak per navigation
- After: 0MB leak, stable memory

**Implementation:**
```pseudocode
struct LeafComponent {
    var resourceManager: ResourceController?

    onDisappear where isForwardNavigation:
        resourceManager.pause()  // Forward
    onDisappear:
        resourceManager.dispose()  // Back
        resourceManager = nil
}
```

---

### 4. Anti-Patterns (Required)

**What:** Common mistakes with production context

**Format:**
```markdown
### ❌ Mistake N: [Descriptive Name]

**Problem:** [What breaks, symptom]

**Why bad:** [Root cause, consequences]

**Fix:** [What to do instead]

**Production incident:** [When happened, impact]
```

**Example:**
```markdown
### ❌ Mistake 1: Resource in Root Container

**Problem:** NMB memory leak per back navigation

**Why bad:** Root container doesn't know navigation direction, always preserves resource instance. Back navigation leaks memory.

**Fix:** Move resource to leaf component with conditional cleanup based on navigation state.

**Production incident:** version X - Lower-end devices crashed after N navigations in production environment
```

---

### 5. Quick Reference (Required)

**What:** Scannable summary for quick lookups

**Format:** Concise bullet points, commands, decision trees

**Example:**
```markdown
## Quick Reference

**Detecting Drift:**
- Code differs from skill → Update pattern
- File paths wrong → Update paths
- Production bug → Add anti-pattern

**Updating Process:**
1. Identify what changed
2. Update relevant sections
3. Add migration note if breaking
4. Verify examples work

**Structure:**
- Purpose → When to Use → Patterns → Anti-Patterns → Quick Ref
- Target ~600 lines (split if larger)
- Examples must work
```

---

## Optional Sections

Include these sections when applicable:

### 6. Decision Trees (Optional)

**When to include:** Complex decisions with multiple criteria

**Format:** Tree structure or flowchart (text)

**Example:**
```markdown
## Decision Trees

### Should I Update or Create New Skill?

\`\`\`
Pattern is variation of existing? → Update existing skill
Pattern is completely new domain? → Create new skill
Existing skill > 1000 lines? → Split into multiple skills
Pattern used by 2+ features? → Add to skill
Pattern feature-specific? → Keep in local documentation
\`\`\`
```

---

### 7. Parameter Tuning Guide (Optional)

**When to include:** Pattern has configurable parameters that need tuning

**Format:** Parameter → Valid range → Default → When to adjust

**Example:**
```markdown
## Parameter Tuning Guide

**Spatial Processing Tolerance:**
- Range: Acm - Bcm
- Default: Xcm
- Small entities (< Acm spacing): A-Bcm
- Standard entities (B-Ccm spacing): Xcm
- Large entities (> Ccm spacing): C-Dcm
```

---

### 8. Integration with Other Skills (Optional)

**When to include:** Skill relates to or depends on other skills

**Format:** Bulleted list with brief explanation

**Example:**
```markdown
## Integration with Other Skills

- **documentation-maintenance** - Update documentation when skill changes
- **signal-vs-noise** - Filter updates (project-specific only)
- **testing-strategy** - Test skill patterns after updates
```

---

### 9. Real Project Example (Optional but Recommended)

**When to include:** When complex pattern needs concrete walkthrough

**Format:** Complete scenario from problem → fix → result

**Example:**
```markdown
## Real Project Example

**Scenario:** Resource lifecycle pattern changed (memory leak fix)

**Before:**
[Old pattern with problem]

**Production Incident:**
- NMB leak per navigation
- Lower-end devices crashed

**After:**
[New pattern with fix]

**Result:**
- 0MB leak
- Stable memory usage
```

---

## Tier 2 vs Tier 3 Split

**Decision criteria:**

### Keep in SKILL.md (Tier 2) when:
- Core pattern (used frequently)
- Short example (< 20 lines)
- Critical context (needs immediate visibility)
- Cross-referenced by multiple patterns

### Move to Tier 3 file when:
- Detailed walkthrough (> 50 lines)
- Self-contained topic
- Optional deep dive
- Modular content (can stand alone)

**Example:**
```
.claude/skills/component-patterns/
├── SKILL.md                      # Tier 2: Core patterns, common examples
└── resources/                    # Tier 3: Deep dives, references
    ├── data-flow-patterns.md     # Detailed data flow examples
    ├── composition-patterns.md   # Complex composition patterns
    └── testing-patterns.md       # Complete testing guide
```

---

## Line Count Guidelines

**Target:** ~500 lines for SKILL.md

**Philosophy:** Quality > Line Count

**Guidelines:**
- 500 lines is a TARGET, not a CONSTRAINT
- Completeness matters more than brevity
- 600 lines of pure signal > 300 lines with missing context
- Only move content to Tier 3 if truly modular and self-contained
- Never cut WHY context to meet line count

**When to split:**
- Skill > 1000 lines → Split into multiple skills
- Single topic > 100 lines → Consider Tier 3 file
- Unrelated patterns → Create separate skills

---

## Self-Contained Tier 3 Pattern

**Rule:** References should be ONE LEVEL DEEP

**Example:**

✅ **GOOD (One level):**
```markdown
<!-- SKILL.md -->
See @resources/data-flow-patterns.md for detailed examples

<!-- resources/data-flow-patterns.md -->
[Complete, self-contained content - no further references]
```

❌ **BAD (Too deep):**
```markdown
<!-- SKILL.md -->
See @guide.md

<!-- guide.md -->
See @examples.md

<!-- examples.md -->
See @details.md
```

---

## Resources Subdirectory Pattern

**New organizational best practice:**

```
.claude/skills/[skill-name]/
├── SKILL.md                # Main skill content
└── resources/              # Reference files
    ├── reference-1.md
    ├── reference-2.md
    └── reference-3.md
```

**Benefits:**
- Clear separation between main skill and supporting materials
- Scalable (easy to add references without cluttering root)
- Scannable (resources clearly in subdirectory)
- References use `@resources/filename.md` format

**Example:**
```markdown
<!-- SKILL.md -->
## Quick Reference

**Reference Materials:**
- @resources/signal-vs-noise-reference.md
- @resources/why-over-how-reference.md
- @resources/skill-structure-reference.md
```

---

## Content Quality Principles

### 1. Signal-Focused (CRITICAL)

**Remove generic content Claude already knows:**

❌ **Don't include:**
```markdown
## What is a Data Repository?
A data repository is a design pattern that encapsulates data access...
[Claude knows repository pattern]
```

✅ **Include only project-specific:**
```markdown
## Repository Rules (This Project)
- NEVER depend on another repository (creates cycles)
- Use Service to combine 3+ repositories
```

---

### 2. Complete WHY Context

**Always include:**
- Purpose (what problem solved)
- Why this approach (alternatives considered)
- Production impact (incidents, bugs, complaints)
- Consequences (what breaks without pattern)

**See:** `@resources/why-over-how-reference.md`

---

### 3. Production Context Mandatory

**Every anti-pattern needs:**
- When it happened (version, date approximate)
- Impact (numbers, user complaints, severity)
- How fixed (specific solution)

**Example:**
```markdown
**Production incident - version X:**
- NMB leak per back navigation
- Lower-end devices crashed after N navigations
- M user complaints in production environment
```

---

### 4. Examples Must Work

**Verify:**
- [ ] Code examples use current API
- [ ] File paths exist in codebase
- [ ] Syntax works without errors
- [ ] Dependencies correct

---

### 5. Consistent Terminology

**Pick ONE term per concept:**
- Repository (not "repo" or "data layer")
- Orchestrator (not "manager" or "coordinator" unless distinct)
- Component (not "screen" or "view" or "module" unless distinct)

---

## Anti-Patterns (Structure Mistakes)

### ❌ Too Many Sections

**Problem:** Skill has 15 different sections, hard to navigate

**Fix:** Use standard 5 required + 4 optional (max 9 sections)

---

### ❌ Missing Quick Reference

**Problem:** No scannable summary, must read entire skill

**Fix:** Always include Quick Reference section at end

---

### ❌ Generic Content (Not Signal-Focused)

**Problem:** 70% of skill is generic explanations Claude knows

**Fix:** Remove generic, keep only project-specific content

---

### ❌ Deeply Nested References

**Problem:** SKILL.md → guide.md → examples.md → details.md

**Fix:** Keep references one level deep, make Tier 3 self-contained

---

### ❌ Anti-Patterns Without Production Context

**Problem:** "Don't do X" without explaining when it happened or impact

**Fix:** Always include production incident details

---

### ❌ Examples Without WHY

**Problem:** Code examples with no explanation of purpose or rationale

**Fix:** Every example needs Purpose, WHY approach, Production impact

---

## Verification Checklist

Before finalizing skill structure:

**Required Sections:**
- [ ] Purpose (1-2 sentences)
- [ ] When to Use (bulleted triggers)
- [ ] Core Patterns (3-5 patterns with WHY)
- [ ] Anti-Patterns (production context for each)
- [ ] Quick Reference (scannable summary)

**Content Quality:**
- [ ] Signal-focused (no generic Claude-knows content)
- [ ] Complete WHY (every pattern has context)
- [ ] Production incidents (numbers, impact, when)
- [ ] Examples work (verified)
- [ ] Consistent terminology (one term per concept)

**Organization:**
- [ ] Standard section order (Purpose → When → Patterns → Anti → Quick)
- [ ] Line count reasonable (~500, accept up to 800 if needed)
- [ ] References one level deep (Tier 3 self-contained)
- [ ] Navigation easy (find any pattern in < 30 seconds)

---

## Example: Well-Structured Skill

```markdown
---
name: component-patterns
description: Component state management patterns for this project. Use when implementing features, designing state, handling events, working with data streams, or integrating components.
---

# Component Patterns - State Management

## Purpose

Component patterns for this project with architecture integration. Focuses on project-specific patterns, not framework fundamentals.

## When to Use

- Implementing new feature component
- Debugging state issues
- Integrating with data streams
- Memory leak in component
- Navigation not working

## Core Patterns

### Pattern 1: Data Stream Integration

**Purpose:** React to data changes from business layer

[Complete pattern with WHY, production context, implementation]

### Pattern 2: Navigation State

**Purpose:** Coordinate navigation with component state

[Complete pattern with WHY, production context, implementation]

[3-5 total patterns]

## Anti-Patterns (Critical Mistakes)

### ❌ Mistake 1: [Name]

**Problem:** [What breaks]
**Why bad:** [Root cause]
**Fix:** [Solution]
**Production incident:** [When, impact]

[3-5 anti-patterns with production context]

## Quick Reference

**Common Tasks:**
- Create component → [steps]
- Add data stream → [pattern]
- Debug state → [checklist]

**Critical Rules:**
- Initialize properly before use
- Handle state updates correctly
- Clean up resources on disposal

## Integration with Other Skills

- **testing-strategy** - How to test component patterns
- **clean-architecture** - Where components fit in layers

## Real Project Example

[Complete walkthrough of real feature from project]
```

---

## Remember

**Standard structure ensures:**
- Consistency across all skills
- Easy navigation (know where to look)
- Complete information (required sections force completeness)
- Signal-focused (structure guides content quality)

**Quality First:**
- Structure supports content, not constrains it
- Complete > Brief
- Signal-focused > Generic
- WHY context > HOW implementation
