# Agent-Skill Relationship

**Purpose:** Understand the fundamental relationship between agents and skills using the OS-Application analogy. Includes decision tree for what goes where and how auto-loading works.

---

## The OS Analogy

**Think of it like a computer system:**

```
Agent = Operating System
├─ Routes requests to applications
├─ Provides consistent interface (workflow, output format)
├─ Manages execution (orchestration)
└─ Lightweight, stable core

Skill = Application
├─ Domain-specific functionality
├─ Self-contained patterns and knowledge
├─ Can be added/updated independently
└─ Feature-rich, specialized
```

**Why this works:**

- OS doesn't contain apps (agent doesn't contain patterns)
- OS routes to apps (agent routes to skills)
- Apps are self-contained (skills are self-contained)
- Add new apps without OS change (add skills without agent change)
- OS provides interface (agent provides workflow + output)

---

## The Golden Rule

```
Agent = Operating System (thin routing layer)
├─ When to invoke (description with triggers)
├─ How to execute (workflow steps)
├─ What to output (format specification)
└─ Quality checks (checklist)

Skill = Application (thick pattern library)
├─ What patterns to use (templates, examples)
├─ What to avoid (anti-patterns)
├─ Why it works (explanations)
└─ How to verify (testing, commands)
```

**Agent responsibilities:**

- ✅ Description with triggers (when to invoke)
- ✅ Workflow (3-5 steps)
- ✅ Output format (YAML/JSON structure)
- ✅ Checklist (with skill references)
- ❌ NOT patterns/templates
- ❌ NOT anti-patterns/examples
- ❌ NOT detailed how-to

**Skill responsibilities:**

- ✅ Domain patterns (templates, examples)
- ✅ Anti-patterns (what NOT to do, why)
- ✅ Real project examples (from actual code)
- ✅ Quick reference (commands, checklists)
- ✅ Self-contained (all context needed)
- ❌ NOT workflow steps
- ❌ NOT output formats

---

## How Skills Auto-Load

**Key insight:** Agent lists skills in frontmatter, Claude auto-loads skill descriptions, then loads full skill content when needed.

```yaml
# Agent frontmatter
skills:
  - pattern-group-1 # Claude sees description
  - pattern-group-2 # Claude sees description
  - pattern-group-3 # Claude sees description
```

**What happens:**

1. Agent invoked with task
2. Claude reads agent file
3. Claude sees skill names in frontmatter
4. Claude loads ALL skill descriptions (from `description:` field)
5. Claude decides which skill to consult based on task
6. Claude loads full skill content (SKILL.md body)

**Why this works:**

- Agent doesn't need to explain skills (descriptions already loaded)
- Agent doesn't need "Consult X skill for Y" (Claude figures it out)
- Skills self-document via description field

**Example:**

```yaml
---
name: api-developer
skills:
  - api-conventions        # Description: "Use when designing API endpoints..."
  - error-handling-patterns # Description: "Use when handling errors..."
  - testing-strategy       # Description: "Use when writing tests..."
---

You implement API endpoints following team conventions.

When invoked:
1. Design endpoint (consult api-conventions)
2. Add error handling (consult error-handling-patterns)
3. Write tests (consult testing-strategy)
```

Claude sees all 3 skill descriptions in context, decides which to load based on current step.

---

## Decision Tree: What Goes Where?

**Use this to decide if content belongs in agent or skill:**

```
Is this about WHEN to invoke? → Agent description
Is this about WHAT to output? → Agent output format
Is this a WORKFLOW step? → Agent workflow section
Is this a PATTERN/TEMPLATE? → Skill
Is this an ANTI-PATTERN? → Skill
Is this a REAL EXAMPLE? → Skill
Is this a VERIFICATION step? → Skill
Is this WHY explanation? → Skill
Is this HOW-TO guide? → Skill
```

**Quick test:**

- **"When to use this agent?"** → Agent description
- **"What steps to follow?"** → Agent workflow
- **"How to format output?"** → Agent output format
- **"What pattern to use?"** → Skill
- **"Why this approach?"** → Skill
- **"What NOT to do?"** → Skill

---

## Common Mistakes

### ❌ Mistake 1: Duplicating Patterns in Agent

```markdown
# ❌ WRONG: Agent file

## CRITICAL RULES

### Rule 1: NEVER create circular dependencies

[300 lines explaining anti-pattern]
```

**Fix:** Move to skill, reference from agent checklist

```markdown
# ✅ CORRECT: Agent file

## CHECKLIST

- [ ] No circular dependencies (see access-control-patterns skill)
```

---

### ❌ Mistake 2: Skills Reference Section in Agent

```markdown
# ❌ WRONG: Agent file

## SKILLS REFERENCE

- data-structure-patterns - Structures, naming
- access-control-patterns - Access rules
  [Explaining what each skill does]
```

**Fix:** Delete section. Skills auto-load descriptions.

```markdown
# ✅ CORRECT: Agent file

# (No skills reference section - frontmatter is enough)

---
skills:
  - data-structure-patterns
  - access-control-patterns
---
```

---

### ❌ Mistake 3: "Do NOT use for" in Agent

```markdown
# ❌ WRONG: Agent description

Do NOT use this agent for:

- Writing queries (use code-developer)
- Creating components (use code-developer)
```

**Fix:** Delete section. Orchestrator knows agent boundaries from positive descriptions.

```markdown
# ✅ CORRECT: Agent description

description: >
  Use when data layer changes needed - schemas, access control, query optimization.

  Trigger when you hear:
  - "create data schema"
  - "add access rule"
```

---

### ❌ Mistake 4: Thin Skills

```markdown
# ❌ WRONG: Skill with 100 lines

Just basic patterns, no anti-patterns, no examples
```

**Fix:** Skills should be 400-600 lines with:

- Multiple patterns
- Anti-patterns from real bugs
- Real project examples
- Quick reference

---

## OS Analogy in Practice

**Example: data-specialist agent**

```
data-specialist (OS)
├─ loads → data-structure-patterns (app)
├─ loads → access-control-patterns (app)
└─ loads → query-optimization-patterns (app)

User: "Create data schema"
├─ OS (agent) receives request
├─ OS routes to data-structure-patterns (app)
└─ App provides pattern/template
```

**What happens:**

1. User requests: "Create data schema for user profiles"
2. data-specialist agent invoked (OS starts)
3. Agent workflow Step 1: Identify change type → Structure change
4. Agent workflow Step 2: Consult data-structure-patterns skill (load app)
5. Skill provides: Structure naming, type definition, testing pattern
6. Agent workflow Step 3: Create implementation using skill patterns
7. Agent returns: YAML output with patterns_applied field referencing skill

**Why OS analogy works:**

- OS (agent) stable - rarely changes
- Apps (skills) updatable - patterns evolve
- OS routes efficiently - agent knows which skill for which task
- Apps self-contained - skills don't need agent to explain them
- Add apps without OS change - add skills without modifying agent

---

## Practical Size Guidelines

**From production refactoring:**

| Component | Target Size | Why |
|-----------|-------------|-----|
| Agent | 120-150 lines | Thin routing layer |
| Skill | 400-600 lines | Thick pattern library |
| Skills per agent | 3-4 optimal | Like bundled apps |
| Agents in system | 5-7 for monorepo | Specialized roles |

**Example: data-specialist transformation**

Before refactoring:
- data-specialist agent: 300 lines
- All patterns embedded in agent

After refactoring:
- data-specialist agent: 120 lines
- data-structure-patterns skill: 432 lines
- access-control-patterns skill: 545 lines
- query-optimization-patterns skill: 485 lines

**Result:** 300 lines → 120 (agent) + 1462 (3 skills) = more content, better organized

---

## Key Insights

**From Production Refactoring:**

1. **Agent descriptions auto-propagate** - Orchestrator sees them without agent explaining
2. **Skills self-document** - Description field makes them discoverable
3. **Thin agents scale better** - Adding new patterns = add skill, not modify agent
4. **Pattern reuse** - Same skill used by multiple agents (like shared libraries)
5. **Maintenance simplified** - Update pattern once (skill), all agents benefit
6. **OS analogy holds** - Agents are stable OS, skills are updatable apps

**Critical Numbers:**

- Agent: 120-150 lines (thin OS)
- Skill: 400-600 lines (thick app)
- Skills per agent: 3-4 optimal (like bundled apps)
- Agents in system: 5-7 for monorepo (was 12 before consolidation)

---

**Key Lesson:** Think of agents as Operating Systems and skills as Applications. OS doesn't contain apps, OS routes to apps. Agent doesn't contain patterns, agent routes to skills.
