# Agent Refactoring Guide - Thick to Thin Transformation

**Purpose:** Step-by-step process for refactoring thick agents (300+ lines with embedded patterns) into thin agents (120-150 lines) + separate skills (400-600 lines each).

---

## The Problem We Solved

**Before refactoring:**

- 12 specialized agents (feature-developer-A, feature-developer-B, data-developer, etc.)
- Each agent 300-600 lines
- Heavy duplication of patterns between agents
- Hard to update patterns (must update multiple agents)
- Mixed routing logic with domain knowledge
- **Like:** 12 operating systems, each with apps baked in

**After refactoring:**

- 5 consolidated agents (code-developer, data-specialist, analysis-agent, etc.)
- Each agent ~120-150 lines
- Domain knowledge extracted to skills
- Patterns updated once, used by all agents
- Clear separation: agents route, skills provide patterns
- **Like:** 5 operating systems, with installable applications

---

## Step-by-Step Refactoring Process

**From production data-specialist refactoring:**

### Step 1: Identify Patterns to Extract

Read agent file (300+ lines), identify sections that are patterns, not routing:

**What to extract:**
- Sections with "Pattern 1, Pattern 2..."
- Anti-pattern sections
- Example code blocks
- Verification/testing steps
- WHY explanations
- Real project examples

**What to keep in agent:**
- Description with triggers
- Workflow steps (3-5 steps)
- Output format
- Checklist (will reference skills)

**Example from data-specialist:**

```markdown
# Original agent (300 lines)

## Structure Patterns
[100 lines of structure patterns]

## Access Control Patterns
[120 lines of access patterns + circular dependency bug]

## Query Optimization
[80 lines of query patterns]
```

**Decision:**
```
Structure patterns → data-structure-patterns skill
Access control patterns → access-control-patterns skill
Query patterns → query-optimization-patterns skill
```

---

### Step 2: Create Skills for Pattern Groups

**Group related patterns together:**

Found in agent:
- Structure patterns → `data-structure-patterns` skill
- Access control patterns → `access-control-patterns` skill
- Query patterns → `query-optimization-patterns` skill

**Naming convention:**
- `[domain]-[aspect]-patterns` (e.g., `data-structure-patterns`)
- `[domain]-[aspect]` (e.g., `api-conventions`)
- Keep names descriptive and consistent

---

### Step 3: Write Skills (400-600 lines each)

**Include in each skill:**

1. **Purpose** (1-2 sentences)
2. **When to Use** (3-5 trigger scenarios)
3. **Core Patterns** (3-5 patterns with templates)
4. **Anti-Patterns** (real mistakes from production)
5. **Real Examples** (from actual project code)
6. **Quick Reference** (commands, checklists)

**Example: data-structure-patterns skill (432 lines)**

```markdown
---
name: data-structure-patterns
description: Use when creating or modifying data structures. Provides structure naming, type definitions, and testing patterns.
---

# Data Structure Patterns

## Purpose
[Problem this solves]

## When to Use
- Creating new data schema
- Modifying existing structure
- Adding validation rules

## Core Patterns

### Pattern 1: Structure Naming
[Template + example]

### Pattern 2: Type Definition
[Template + example]

### Pattern 3: Testing Pattern
[Template + example]

## Anti-Patterns

### ❌ Multiple Changes for Same Requirement
**Problem:** [Real bug from production]
**Why it failed:** [Root cause]
**Fix:** [What to do instead]

## Quick Reference
[Commands, checklists]

## Real Project Examples
[Actual code from project]
```

---

### Step 4: Reduce Agent to Routing Layer

**Keep ONLY:**

1. **Description with triggers** (~30 lines)
2. **Workflow** (3 steps, ~20 lines)
3. **Output format** (~30 lines)
4. **Checklist with skill references** (~20 lines)

**Total: 100-120 lines**

**Example: data-specialist agent (reduced to 120 lines)**

```yaml
---
name: data-specialist
skills:
  - data-structure-patterns
  - access-control-patterns
  - query-optimization-patterns
description: >
  **Use this agent PROACTIVELY** when data layer changes are needed.

  Automatically invoked when detecting:
  - Need to create or modify data structures
  - Adding access control rules
  - Implementing data transformations

  Trigger when you hear:
  - "create data schema"
  - "add access rule"
  - "performance issue"
---

You are a **Data Specialist**. Design data layer using patterns from loaded skills.

## WORKFLOW

### Step 1: Identify Change Type

Structure change? → data-structure-patterns skill
Access control? → access-control-patterns skill
Query optimization? → query-optimization-patterns skill

### Step 2: Apply Skill Pattern

Consult loaded skill for exact pattern.

### Step 3: Create Implementation + Output

Use skill patterns to create solution.

## OUTPUT FORMAT

```yaml
# YAML structure
```

## CHECKLIST

- [ ] Structure named correctly (data-structure-patterns)
- [ ] If access control: checked access-control-patterns for cycles
- [ ] If query: checked query-optimization-patterns for indexes
```

**Notice:**
- No pattern details (in skills)
- No examples (in skills)
- Just routing + format

---

### Step 5: Add Skills to Agent Frontmatter

```yaml
skills:
  - data-structure-patterns
  - access-control-patterns
  - query-optimization-patterns
```

**Claude will:**
1. See skill names
2. Load skill descriptions
3. Decide which to consult based on task
4. Load full skill content when needed

---

### Step 6: Test Refactored Agent

**Verify:**

1. **Agent invokes correctly** - Description triggers match use cases
2. **Skills load automatically** - Claude finds right skill for task
3. **Output format works** - YAML structure as expected
4. **Checklist references skills** - No broken references

**Test cases:**

```
User: "Create data schema for user profiles"
Expected: Agent routes to data-structure-patterns skill

User: "Add access control for admin-only data"
Expected: Agent routes to access-control-patterns skill

User: "Optimize slow query"
Expected: Agent routes to query-optimization-patterns skill
```

---

## Production Metrics

**From data-specialist refactoring:**

### Before Refactoring

```
data-specialist agent: 300 lines
├─ Structure patterns: ~100 lines
├─ Access patterns: ~120 lines
└─ Query patterns: ~80 lines

Problems:
- All patterns in one file (hard to maintain)
- No clear separation (routing mixed with patterns)
- Duplication with other agents (patterns repeated)
```

### After Refactoring

```
data-specialist agent: 120 lines
├─ Description + triggers: 30 lines
├─ Workflow (3 steps): 20 lines
├─ Output format: 30 lines
└─ Checklist: 20 lines

Skills:
├─ data-structure-patterns: 432 lines
├─ access-control-patterns: 545 lines
└─ query-optimization-patterns: 485 lines

Total: 120 (agent) + 1462 (skills) = 1582 lines
```

**Result:** 300 lines → 1582 lines (more content, better organized)

---

## Benefits Measured

**From production refactoring (6 agents → 5 agents):**

1. **Maintenance** - Update pattern once (skill), all agents benefit
   - Before: Update pattern in 3 agents (3× work)
   - After: Update pattern in 1 skill (1× work)

2. **Reusability** - Same skill used by multiple agents
   - Example: `testing-strategy` skill used by 3 agents

3. **Clarity** - Clear separation (routing vs patterns)
   - Agent: ~120 lines (easy to understand workflow)
   - Skills: ~400-600 lines (sufficient patterns, focused not exhaustive)

4. **Scalability** - Add patterns without modifying agents
   - Before: Modify agent to add pattern (risk breaking workflow)
   - After: Add new skill or extend existing skill (agent unchanged)

---

## Common Refactoring Patterns

### Pattern 1: Extract Anti-Patterns First

**Why:** Anti-patterns often reveal natural skill boundaries

**Example:**

```markdown
# Agent has 3 anti-pattern sections
Anti-pattern: Circular dependency → access-control-patterns skill
Anti-pattern: N+1 queries → query-optimization-patterns skill
Anti-pattern: Missing validation → validation-patterns skill
```

### Pattern 2: Group by Domain, Not by Type

**❌ Wrong grouping:**
```
- all-patterns skill (500 lines of mixed patterns)
- all-anti-patterns skill (400 lines of mixed anti-patterns)
```

**✅ Correct grouping:**
```
- data-structure-patterns skill (patterns + anti-patterns + examples)
- access-control-patterns skill (patterns + anti-patterns + examples)
- query-optimization-patterns skill (patterns + anti-patterns + examples)
```

### Pattern 3: Keep Skills Self-Contained

**Each skill should be usable independently:**

```markdown
# ✅ Good skill (self-contained)
- Purpose (what problem it solves)
- Core patterns (templates)
- Anti-patterns (mistakes)
- Examples (real code)
- Quick reference

# ❌ Bad skill (depends on other skills)
- "See other-skill for setup"
- "Refer to another-skill for examples"
```

---

## Refactoring Checklist

### Before Refactoring

- [ ] Agent has 200+ lines
- [ ] Agent contains pattern sections
- [ ] Agent has anti-pattern sections
- [ ] Agent has example code blocks
- [ ] Patterns duplicated in other agents
- [ ] Difficult to update patterns

### During Refactoring

- [ ] Identified pattern groups (3-4 groups)
- [ ] Created skills (400-600 lines each)
- [ ] Extracted patterns from agent to skills
- [ ] Extracted anti-patterns from agent to skills
- [ ] Extracted examples from agent to skills
- [ ] Reduced agent to routing layer (120-150 lines)
- [ ] Added skills to agent frontmatter
- [ ] Updated checklist to reference skills

### After Refactoring

- [ ] Agent: 120-150 lines
- [ ] Skills: 400-600 lines each
- [ ] Agent workflow clear (3-5 steps)
- [ ] Skills self-contained
- [ ] No duplication between skills
- [ ] Tested with real tasks
- [ ] Agent routes correctly
- [ ] Skills load automatically

---

## When NOT to Refactor

**Don't refactor if:**

1. **Agent is already thin** (<150 lines)
2. **No pattern duplication** (patterns unique to this agent)
3. **Small domain** (not enough content for separate skills)
4. **Patterns tightly coupled** (can't separate cleanly)

**Example: Keep as single agent**

```yaml
---
name: simple-formatter
---

You format code.

1. Read file
2. Apply formatting rules
3. Write formatted file

(No skills needed - too simple)
```

---

## Refactoring Benefits

**Improvements from thick-to-thin transformation:**

- **Consolidation:** Multiple specialized agents → Fewer general-purpose agents
- **Size reduction:** Large agent files → Smaller routing layers
- **Knowledge extraction:** Patterns embedded in agents → Separate skills
- **Reusability:** Duplicate patterns → Single skill used by multiple agents
- **Maintenance:** Update pattern once in skill, all agents benefit
- **Clarity:** Mixed routing and patterns → Clear separation of concerns

---

**Key Lesson:** Thick agents (300+ lines) should be refactored into thin agents (120-150 lines) + separate skills (400-600 lines). Update pattern once (skill), all agents benefit.
