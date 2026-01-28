---
name: agent-skill-architecture
description: Use when creating or refactoring agents and their skills. Explains the architectural pattern where agents are routing layers (thin wrappers) and skills contain all domain knowledge (thick patterns). Includes templates, best practices, and real production examples.
---

# Agent-Skill Architecture - Self-Contained Guide

## Purpose

Complete guide for agent-skill architecture: agents as Operating Systems (thin routing), skills as Applications (thick patterns). Includes Signal vs Noise filter, quality guidelines (WHY > HOW, quality > line count), templates, and real production examples.

## When to Use

- Creating new agent from scratch
- Refactoring existing agent (too much duplication)
- Converting agent content to skills
- Understanding agent vs skill boundary
- Applying signal-vs-noise to agent/skill content
- Need guide for creating agents in new project

## Core Philosophy

### Anthropic's OS Analogy

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

### The Problem We Solved

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

### The Golden Rule

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

## Signal vs Noise Integration

### The 3-Question Filter (For Content Quality)

**Before adding ANYTHING to agent or skill, ask:**

1. **Actionable?** Can Claude/user act on this information?
2. **Impactful?** Would lack of this cause bugs or waste time?
3. **Non-obvious?** Is this project-specific (not generic knowledge)?

**Scoring:**

- 3/3 YES → SIGNAL → Include it
- 2/3 YES → Consider (usually include if impactful + non-obvious)
- 1/3 YES → NOISE → Cut it

### Quality Guidelines

**Quality > Line Count**

The 500-line guideline is a TARGET, not a hard limit.

```
Better:
  600 lines of pure signal (every line project-specific)
Than:
  300 lines with 50% noise (generic patterns Claude knows)
```

**From production refactoring:**

- ui-component-patterns: 112 lines (focused signal)
- data-access-patterns: 355 lines (critical anti-patterns need space)
- business-logic-patterns: 444 lines (comprehensive patterns)

**All high quality** - line count varies based on domain complexity.

### WHY > HOW Focus

**SIGNAL (keep):**

```markdown
## Multi-Value Field Handler

**Real bug from implementation:** standard handler stored only last value, not collection

**Why:** Standard handler = single value, custom handler = collection handling
```

**NOISE (cut):**

```markdown
## Form Library

[Library name] is a library for managing forms...
[Generic explanation Claude already knows]
```

### Project-Specific Only

**Apply to both agents AND skills:**

**SIGNAL (keep):**

- Architecture decision (our project-specific choice)
- Custom handler bug (we hit this in production)
- Library usage rule (our project constraint)
- Circular dependency bug (crashed our production)

**NOISE (cut):**

- How framework X works (Claude knows)
- Generic routing patterns (Claude knows)
- Standard validation syntax (Claude knows)
- Basic database syntax (Claude knows)

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

## Skills with Forked Execution (context: fork)

**Special case:** Skills can run in isolated subagent context without conversation history.

### Two Approaches to Subagents + Skills

| Approach | System Prompt | Task | Skills Loaded |
|----------|--------------|------|---------------|
| **Skill with `context: fork`** | From `agent` type | SKILL.md content | CLAUDE.md only |
| **Agent with `skills` field** | Agent markdown body | Claude's delegation | Skills in frontmatter + CLAUDE.md |

**Skill with context: fork** - You write task in skill, pick agent type to execute:

```yaml
---
name: deep-research
context: fork
agent: Explore        # Picks Explore subagent (read-only tools)
---

Research $ARGUMENTS thoroughly:
1. Find files with Glob and Grep
2. Analyze code
3. Summarize findings
```

**How it works:**
1. User/Claude invokes skill (`/deep-research authentication`)
2. New isolated context created (no conversation history)
3. Skill content becomes the prompt for subagent
4. `agent` field determines execution environment (Explore = read-only tools)
5. Subagent executes, returns results to main conversation

**Agent with skills field** - You write custom agent that uses skills as reference:

```yaml
---
name: custom-analyzer
skills:
  - pattern-group-1
  - pattern-group-2
---

You are an analyzer. Use loaded skills for patterns.

## Workflow
...
```

This is for defining custom agents (see subagents docs).

### When to Use context: fork

**Use `context: fork` when:**
- Research task (explore codebase without conversation noise)
- Analysis task (focused examination)
- Skill has complete instructions (self-contained prompt)
- Don't need conversation context
- Want to use existing agent type (Explore, Plan)

**Don't use `context: fork` when:**
- Skill is reference material (guidelines, patterns)
- Needs conversation context
- Just provides knowledge (not actionable task)

**Example comparison:**

```yaml
# ❌ Wrong - Reference skill with fork
---
name: api-patterns
context: fork
---
Use these API conventions:
- Pattern A
- Pattern B

# Returns nothing (no task)

# ✅ Correct - Reference skill without fork
---
name: api-patterns
---
Use these API conventions:
- Pattern A
- Pattern B

# Agent loads this as reference when needed

# ✅ Correct - Task skill with fork
---
name: api-research
context: fork
agent: Explore
---
Research API usage for $ARGUMENTS:
1. Find relevant files
2. Analyze patterns
3. Summarize findings

# Executes research, returns summary
```

### Agent Types for Forked Skills

When using `context: fork`, specify agent type:

```yaml
agent: Explore          # Read-only: Glob, Grep, Read, WebFetch, WebSearch
agent: Plan             # Planning: All tools except Edit/Write (read-only + analysis)
agent: general-purpose  # Full access: All tools (default)
agent: custom-agent     # Custom agent from .claude/agents/
```

**Pick based on task:**
- **Explore** - Codebase research, documentation search
- **Plan** - Architecture analysis, planning
- **general-purpose** - Tasks needing write access
- **custom-agent** - Specialized behavior defined in .claude/agents/

## Agent Template

**Quick reference template** - for complete copy-paste template with production patterns, see:
👉 **@resources/agent-template-generic.md** (~340 lines, Signal-focused)

Universal template based on 6 production agents with:
- Copy-paste template (frontmatter + body)
- 2 concrete production examples (ios-developer, atlassian-manager)
- 5 key patterns (proactive description, 3-step workflow, YAML output, patterns_applied, thin vs thick)
- 2 critical mistakes (from production impact)
- Customization notes (colors, skills, length)

See **agent-template-generic.md** resource.

### Frontmatter Structure

```yaml
---
name: agent-name
color: red | blue | green | cyan | purple | orange
skills:
  - skill-1
  - skill-2
  - skill-3
description: >
  **Use this agent PROACTIVELY** when [high-level purpose].

  Automatically invoked when detecting:
  - [Scenario 1]
  - [Scenario 2]
  - [Scenario 3]

  Trigger when you hear:
  - "[phrase 1]"
  - "[phrase 2]"
  - "[phrase 3]"

model: sonnet | opus | haiku
---
```

**Description field rules:**

- Start with "Use this agent PROACTIVELY when"
- "Automatically invoked when detecting" - list scenarios
- "Trigger when you hear" - list key phrases user might say
- NO examples (too verbose, not needed)
- NO "Do NOT use for" (orchestrator knows boundaries)

### Body Structure

````markdown
You are a **[Agent Name]** for [domain]. Create [outputs] using patterns from loaded skills ([skill-1], [skill-2]).

---

## WORKFLOW

### Step 1: [Identify/Understand]

[Simple 2-3 line description]

### Step 2: [Apply Patterns]

[Reference to skills where patterns live]

### Step 3: [Output]

[What to produce]

---

## OUTPUT FORMAT

```yaml
# YAML structure expected
```
````

---

## CHECKLIST

Before output:

- [ ] [Check 1 with skill reference]
- [ ] [Check 2 with skill reference]
- [ ] [Check 3]

**Critical checks (from skills):**

- [Critical pattern 1] → [skill-name]
- [Critical pattern 2] → [skill-name]

---

[Optional: One-line closing reminder of most critical rule]

````

**Body size:** Aim for 120-150 lines (thin layer)

**What NOT to include:**
- ❌ Detailed patterns (those go in skills)
- ❌ Code examples (those go in skills)
- ❌ Anti-patterns (those go in skills)
- ❌ "YOUR EXPERTISE" sections (redundant with skills)
- ❌ "CRITICAL LESSONS" (those go in skills)
- ❌ "REFERENCE DOCUMENTATION" lists (skills auto-load)

## Skill Template

### Frontmatter Structure

```yaml
---
name: skill-name
description: Use when [specific trigger]. [What patterns it provides]. [Critical aspect that makes it essential].
---
````

**Description field rules:**

- Start with "Use when" (specific trigger)
- Explain what patterns/knowledge it contains
- Mention critical/unique aspect (why essential)
- Keep to 1-3 sentences
- Third-person ("Use when..." not "I help you...")

### Body Structure

````markdown
# Skill Name - One-Line Summary

## Purpose

[1-2 sentences: What problem does this solve?]

## When to Use

- [Trigger 1]
- [Trigger 2]
- [Trigger 3]

## Core Patterns

### Pattern 1: [Name]

**Use case:** [When to use this pattern]

```[language]
[Code example with comments]
```
````

**Why this works:**

- [Explanation 1]
- [Explanation 2]

### Pattern 2: [Name]

[Continue...]

## Anti-Patterns (Critical Mistakes)

### ❌ Mistake 1: [Name]

**Problem:** [What breaks, real example from project]

```[language]
# ❌ WRONG
[Bad code]

# ✅ CORRECT
[Good code]
```

**Why bad:** [Root cause, what happens]
**Fix:** [What to do instead]

## Quick Reference

**Commands/Checklists/Tables** - scannable format

```bash
# Common commands
command1
command2
```

**Checklist:**

- [ ] Check 1
- [ ] Check 2

## Real Project Examples

### Example 1: [Feature Name]

```[language]
// From Phase X implementation
[Actual code from project]
```

**Result:** [What this achieved]

## Integration with Other Skills

- **[skill-1]** - [How they relate]
- **[skill-2]** - [How they relate]

---

**Key Lesson:** [One sentence summary of most critical takeaway]

````

**Body size:** Aim for 400-600 lines (thick patterns)

**What MUST include:**
- ✅ Real examples from actual project
- ✅ Anti-patterns (mistakes we made, why)
- ✅ WHY explanations (not just HOW)
- ✅ Quick reference (scannable)
- ✅ Self-contained (all context needed)

## Real Example: data-specialist

### Agent File (~120 lines)

```yaml
---
name: data-specialist
skills:
  - data-structure-patterns
  - access-control-patterns
  - query-optimization-patterns
  - architecture-decisions
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

[YAML structure]

## CHECKLIST

- [ ] Structure named correctly (data-structure-patterns)
- [ ] If access control: checked access-control-patterns for cycles
- [ ] If query: checked query-optimization-patterns for indexes
````

**Notice:**

- No pattern details (in skills)
- No examples (in skills)
- Just routing + format

### Skill Files (400-600 lines each)

**data-structure-patterns.md** (432 lines)

- Structure naming conventions
- Type definition workflow
- Testing patterns
- Anti-pattern: Multiple changes for same requirement

**access-control-patterns.md** (545 lines)

- Circular dependency bug (CRITICAL)
- Delegation pattern
- Multi-context isolation
- Testing with different contexts

**query-optimization-patterns.md** (485 lines)

- Query types (simple, complex, aggregated)
- Index patterns
- Decision tree: query vs computation

### Example: Skill with Forked Execution

**Skill file: deep-research/SKILL.md** (~200 lines)

```yaml
---
name: deep-research
description: Research topic thoroughly using codebase exploration
context: fork
agent: Explore
allowed-tools: Read, Grep, Glob
---

# Deep Research - Isolated Codebase Analysis

Research $ARGUMENTS thoroughly:

1. **Find relevant files**
   ```bash
   Use Glob to find files matching topic
   Use Grep to search for keywords
   ```

2. **Analyze code**
   - Read matched files
   - Understand patterns
   - Note file locations (file:line)

3. **Summarize findings**
   - List key files with paths
   - Explain patterns found
   - Highlight relevant code sections

Output format: Markdown with file references.
```

**How this works:**

1. User invokes: `/deep-research authentication`
2. Skill content becomes prompt with "authentication" substituted for `$ARGUMENTS`
3. Isolated Explore subagent created (read-only tools)
4. Subagent executes research without conversation history
5. Returns summary to main conversation

**Why forked:**
- Research needs focus (no conversation noise)
- Complete instructions in skill (self-contained prompt)
- Read-only tools sufficient (Explore agent appropriate)

**Contrast with non-forked:**

If this was agent skill (not forked), agent would need to orchestrate research steps. With fork, skill is the complete prompt.

## Agent-Skill Boundaries

### Decision Tree: What Goes Where?

```
Is this about WHEN to invoke? → Agent description
Is this about WHAT to output? → Agent output format
Is this a WORKFLOW step? → Agent workflow section
Is this a PATTERN/TEMPLATE? → Skill
Is this an ANTI-PATTERN? → Skill
Is this a REAL EXAMPLE? → Skill
Is this a VERIFICATION step? → Skill
```

### Common Mistakes

**❌ Mistake 1: Duplicating Patterns in Agent**

```markdown
# ❌ WRONG: Agent file

## CRITICAL RULES

### Rule 1: NEVER create circular dependencies

[300 lines explaining anti-pattern]
```

**Fix:** Move to skill, reference from agent checklist

**❌ Mistake 2: Skills Reference Section in Agent**

```markdown
# ❌ WRONG: Agent file

## SKILLS REFERENCE

- data-structure-patterns - Structures, naming
- access-control-patterns - Access rules
  [Explaining what each skill does]
```

**Fix:** Delete section. Skills auto-load descriptions.

**❌ Mistake 3: "Do NOT use for" in Agent**

```markdown
# ❌ WRONG: Agent description

Do NOT use this agent for:

- Writing queries (use code-developer)
- Creating components (use code-developer)
```

**Fix:** Delete section. Orchestrator knows agent boundaries.

**❌ Mistake 4: Thin Skills**

```markdown
# ❌ WRONG: Skill with 100 lines

Just basic patterns, no anti-patterns, no examples
```

**Fix:** Skills should be 400-600 lines with:

- Multiple patterns
- Anti-patterns from real bugs
- Real project examples
- Quick reference

## Refactoring Existing Agent

### Step-by-Step Process

**From production data-specialist refactoring:**

1. **Identify Patterns to Extract**

Read agent file (300+ lines), identify:

- Sections with "Pattern 1, Pattern 2..."
- Anti-pattern sections
- Example code blocks
- Verification/testing steps

2. **Create Skills for Pattern Groups**

```
Found in agent:
- Structure patterns → data-structure-patterns skill
- Access control patterns → access-control-patterns skill
- Query patterns → query-optimization-patterns skill
```

3. **Write Skills (400-600 lines each)**

Include:

- Core patterns (templates)
- Anti-patterns (real mistakes)
- Real examples (from actual code)
- Quick reference

4. **Reduce Agent to Routing Layer**

Keep only:

- Description with triggers (30 lines)
- Workflow (3 steps, 20 lines)
- Output format (30 lines)
- Checklist with skill references (20 lines)

**Result:** 300 lines → 120 (agent) + 1400 (3 skills)

5. **Add Skills to Agent Frontmatter**

```yaml
skills:
  - data-structure-patterns
  - access-control-patterns
  - query-optimization-patterns
```

## Checklist: Creating New Agent

**Agent File:**

- [ ] Description starts with "Use this agent PROACTIVELY"
- [ ] "Automatically invoked when detecting" list
- [ ] "Trigger when you hear" phrases
- [ ] NO examples in description
- [ ] NO "Do NOT use for" section
- [ ] Skills listed in frontmatter
- [ ] Body has 3-section workflow
- [ ] Output format defined (YAML)
- [ ] Checklist references skills
- [ ] Total: 120-150 lines

**Skill Files:**

- [ ] Description: "Use when..." (1-3 sentences)
- [ ] Purpose section (problem solved)
- [ ] Core patterns (3-5 patterns with templates)
- [ ] Anti-patterns (mistakes we made, why)
- [ ] Real project examples
- [ ] Quick reference (commands/checklists)
- [ ] Self-contained (all context)
- [ ] Total: 400-600 lines per skill

**Integration:**

- [ ] Agent frontmatter lists all skills
- [ ] Agent checklist references skills
- [ ] Skills don't reference agent
- [ ] Skills self-contained (no circular deps)

## Using in New Project

### Template Repository Structure

```
new-project/.claude/
├── agents/
│   └── domain-specialist.md    # 120-150 lines
├── skills/
│   ├── pattern-group-1/
│   │   └── SKILL.md             # 400-600 lines
│   ├── pattern-group-2/
│   │   └── SKILL.md
│   └── pattern-group-3/
│       └── SKILL.md
```

### Adaptation Steps

1. **Identify Domain** (e.g., "API Integration Specialist")

2. **List Pattern Groups** (e.g., "authentication", "rate-limiting", "error-handling")

3. **Create Skills First** (easier to see what agent needs)

4. **Create Agent as Router** (reference skills)

5. **Test with Real Task** (does agent route correctly?)

### Example: New Project "E-commerce API"

**Agent:** `payment-specialist`

**Skills:**

- `stripe-integration` - Payment processing patterns
- `payment-security` - PCI compliance, tokenization
- `refund-patterns` - Refund workflows, edge cases

**Agent file (120 lines):**

```yaml
---
name: payment-specialist
skills:
  - stripe-integration
  - payment-security
  - refund-patterns
description: >
  Use when payment processing needed - Stripe integration, refunds, webhooks.

  Trigger when you hear:
  - "process payment"
  - "handle refund"
  - "stripe webhook"
---
Workflow → Output Format → Checklist
```

**Skills (400-600 lines each):** Full patterns, anti-patterns, examples

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
- Agents in system: 5-7 for monorepo (was 12)

**OS Analogy in Practice:**

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

## References (Tier 3 - Self-Contained)

**This skill includes reference files for offline use:**

- `@resources/agent-template-generic.md` - Universal agent template based on 6 production agents (~340 lines, Signal-focused)
  - Copy-paste template (frontmatter + body structure)
  - 2 concrete production examples (ios-developer, atlassian-manager)
  - 5 key patterns with WHY (proactive description, 3-step workflow, YAML output, patterns_applied, thin vs thick)
  - 2 critical mistakes (production impact: 600→326 lines, no traceability)
  - Customization notes (colors, skills selection, agent length, output format)
- `@resources/signal-vs-noise-reference.md` - Complete Signal vs Noise 3-Question Filter, examples
- `@resources/why-over-how-reference.md` - Content quality philosophy (WHY > HOW, production context)
- `@resources/skill-structure-reference.md` - Standard structure and best practices (required sections, organization)
- `@resources/skills-guide-reference.md` - Official Anthropic skills creation guide, metadata rules
- `@resources/skill-template-reference.md` - Copy-paste templates for quick skill creation
- `@resources/skill-ecosystem-reference.md` - Skill locations, sharing, permissions, and resources (where skills live, priority, distribution, access control)

**Use references for:**

- **Agent Template (Generic)** → Complete production-ready agent template based on real agents. Use when creating new agent from scratch.
- Signal vs Noise → Deep dive on 3-Question Filter, application examples
- Why over How → Philosophy of including production context and rationale in all patterns
- Skill Structure → Standard sections, organization patterns, quality guidelines
- Skills Guide → Tier 1/2/3 architecture, official metadata spec
- Templates (Skill) → Quick-start templates for new skills

**Why included:**

- Self-contained guide (no external dependencies)
- Offline reference for new projects
- Complete context for agent-skill decisions
- Consistent philosophy across all meta skills
- Production-proven patterns (not theoretical)

---

**Key Lesson:** Agents are Operating Systems (thin routing ~120 lines), skills are Applications (thick patterns ~400 lines). Quality > line count. WHY > HOW. Project-specific only.
