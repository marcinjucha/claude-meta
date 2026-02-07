---
name: agent-creator
description: >
  Use when creating custom subagents for specialized tasks. Provides decision framework,
  creation process, and best practices based on official agent documentation. Critical
  for proper agent architecture (thin routing layer vs thick skill patterns).
argument-hint: "[agent-name]"
---

# Agent Creator - Meta Skill for Creating Subagents

## Purpose

Guide the creation of high-quality custom subagents that delegate to task-specific agents with focused capabilities. Ensures consistency with agent-skill architecture (Agents as thin routers, Skills as thick domain knowledge).

## When to Use

- **Creating new agent** - Need specialized task execution with specific tools/permissions
- **Evaluating if agent needed** - Unsure whether to create agent vs skill vs command
- **Refactoring workflows** - Converting complex workflows to agent-based approach
- **Reviewing agent quality** - Verifying agent follows best practices

## ⚠️ CRITICAL: FACT-BASED EXAMPLES ONLY

**Why this rule exists:** Invented production examples in agent documentation create false assumptions about when/how to use the agent.

**What to do:**
- User provides example → Use it
- No example available → Skip or use placeholder: `[Real example needed]`

## Core Philosophy

**Agents are Thin Routers, Skills are Thick Applications**

Think of agents as operating systems and skills as applications. The agent provides routing and infrastructure (tool access, model, permissions), while skills contain domain knowledge and patterns.

**What agents should contain:**
- ✅ System prompt (how to approach tasks)
- ✅ Tool restrictions (Read-only, specific tools)
- ✅ Permission mode (auto-accept, bypass, plan)
- ✅ Model selection (sonnet, opus, haiku)
- ❌ NOT domain knowledge (that's for skills)
- ❌ NOT detailed patterns (that's for skills)

**Example:**
```yaml
# ❌ WRONG - Agent contains domain knowledge
---
name: api-developer
---
You implement API endpoints. Follow these patterns:
- Use RESTful naming conventions
- Return consistent error formats
[500 lines of API patterns...]

# ✅ CORRECT - Agent references skills
---
name: api-developer
skills:
  - api-conventions
  - error-handling-patterns
---
You implement API endpoints following team conventions.
The preloaded skills contain the patterns to follow.
```

## Decision Framework

### Should You Create an Agent?

**Ask these questions:**

1. **Does this need specific tool restrictions?**
   - ✅ YES → Read-only analysis agent (allow Read/Grep/Glob, deny Write/Edit)
   - ❌ NO → Standard tool access (use skill or command instead)

2. **Does this need isolation?**
   - ✅ YES → High-volume operations (test runs, log parsing) that fill context
   - ❌ NO → Main conversation works fine (use skill inline)

3. **Does this need specialized execution?**
   - ✅ YES → Background processing, specific model (Haiku for speed), custom permissions
   - ❌ NO → Standard execution (use skill or command)

**If 2-3 YES → Create agent**
**If 0-1 YES → Use skill or command instead**

### Agent vs Skill vs Command?

| Type | Purpose | When to Create | Example |
|------|---------|----------------|---------|
| **Agent** | Specialized execution | Need tool restrictions, isolation, or custom environment | `code-reviewer` (read-only), `db-reader` (SQL only) |
| **Skill** | Domain knowledge | Project-specific patterns, rules, decisions | `api-conventions`, `testing-patterns` |
| **Command** | Workflow orchestration | Multi-phase processes with multiple agents | `/implement-feature`, `/debug-issue` |

**Quick Decision:**
- Need **specific tools/permissions**? → Agent
- Need **reference patterns**? → Skill
- Need **orchestrate workflow**? → Command

---

## Creation Process

### Step 1: Define Agent Purpose

**Identify the specialized capability:**

```yaml
Purpose: Code reviewer that analyzes without modifying

Tool needs:
  - Read (analyze files)
  - Grep/Glob (search codebase)
  - Bash (run git commands)
  - DENY: Edit, Write (read-only)

Isolation needs:
  - YES (git diff output can be large)

Model needs:
  - Sonnet (need good analysis, not just speed)

Skills needed:
  - code-quality-patterns
  - security-patterns
```

**Red flags (don't create agent):**
- ❌ "I need to document API patterns" → Use skill instead
- ❌ "I need to orchestrate multi-step workflow" → Use command instead
- ❌ "I need standard tool access" → Use skill inline instead

**Create agent:**
- ✅ "I need read-only codebase analysis" → Agent with tool restrictions
- ✅ "I need to run tests in isolation" → Agent with context isolation
- ✅ "I need to validate SQL queries" → Agent with PreToolUse hooks

### Step 2: Choose Agent Scope

**Agent locations:**

| Location | Path | Scope | Priority |
|----------|------|-------|----------|
| CLI flag | `--agents` JSON | Current session | 1 (highest) |
| Project | `.claude/agents/` | This project | 2 |
| User | `~/.claude/agents/` | All your projects | 3 |
| Plugin | `<plugin>/agents/` | Where plugin enabled | 4 (lowest) |

**Decision guide:**
- **Project agents** - Project-specific (check into git)
- **User agents** - Personal workflow (not in git)
- **CLI agents** - Testing/automation (not saved to disk)
- **Plugin agents** - Distributable (via plugin system)

### Step 3: Write Agent File

Create `agents/your-agent-name.md` with frontmatter + body:

```markdown
---
name: agent-name
description: When Claude should delegate to this agent
tools: Read, Grep, Glob, Bash
disallowedTools: Write, Edit
model: sonnet
permissionMode: default
skills:
  - skill-one
  - skill-two
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate.sh"
---

# System prompt (how agent approaches tasks)

You are a [role]. When invoked:

1. [Step 1]
2. [Step 2]
3. [Step 3]

## Guidelines

- [Guideline 1]
- [Guideline 2]

## Output Format

[How to present results]
```

**Key frontmatter fields:**

**Non-obvious fields:**
- `permissionMode`: Controls permission prompts (acceptEdits auto-approves file edits, bypassPermissions skips all checks, plan enables read-only exploration)
- `skills`: Preloads full skill content at agent startup (not inherited from parent conversation)
- `hooks`: Lifecycle hooks scoped to this agent (PreToolUse for validation, Stop for cleanup)

**Available tools:**
Read, Write, Edit, Grep, Glob, Bash, WebFetch, WebSearch, Task, NotebookEdit, mcp tools

Restrict when needed (read-only analyst: Read, Grep, Glob only).

### Step 4: Add Supporting Files (Optional)

**When to add supporting files:**

Agents typically DON'T need supporting files. Domain knowledge belongs in skills, not agents.

**Exception: Hook scripts for validation**

```
db-reader/
├── agent.md              # Agent definition
└── scripts/
    └── validate-sql.sh   # Hook script for SQL validation
```

Agent references hook in frontmatter:
```yaml
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-sql.sh"
```

**Rule:** If you're adding reference docs to an agent, that's a skill, not an agent.

### Step 5: Test Agent

**Test invocation:**

1. **Automatic delegation:** Ask Claude to perform task that matches description
2. **Explicit delegation:** Ask Claude "Use the agent-name agent to..."
3. **Resume agent:** After completion, ask Claude to continue previous work

**Check agent transcript:**
```bash
# Agent transcripts stored here:
~/.claude/projects/{project}/{sessionId}/subagents/agent-{agentId}.jsonl

# Read transcript
tail -f ~/.claude/projects/.../subagents/agent-xyz.jsonl
```

### Step 6: Verify Quality

**Checklist:**

- [ ] Name: lowercase + hyphens, max 64 chars
- [ ] Description: third-person, describes WHEN to delegate, <1024 chars
- [ ] Body: System prompt only (no domain knowledge)
- [ ] Tool restrictions: Only what's needed for task
- [ ] Skills: Referenced (not duplicated in agent body)
- [ ] Hooks: For validation only (not domain knowledge)
- [ ] Third-person: "Use when..." not "I help..."
- [ ] Thin router: Agent provides infrastructure, skills provide knowledge

**Self-check questions:**
- [ ] Is domain knowledge in skills (not agent body)?
- [ ] Are tool restrictions justified by task requirements?
- [ ] Does description clearly indicate when to delegate?
- [ ] Is system prompt focused on approach (not patterns)?

---

## Agent Patterns

### Pattern 1: Read-Only Analyst

```yaml
---
name: code-reviewer
tools: Read, Grep, Glob, Bash
disallowedTools: Write, Edit
skills: [code-quality-patterns]
---
```

**Why read-only tools:** Production incident - agent with Write access "fixed" code during review → feedback inconsistent with committed code.

### Pattern 2: Conditional Validator (Hook)

```yaml
---
name: db-reader
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-readonly.sh"
---
```

**Hook script:** Exit code 2 blocks operation. Grep for INSERT/UPDATE/DELETE → block if found.

### Pattern 3: Fast Processor (Haiku)

```yaml
---
name: log-analyzer
model: haiku
tools: Read, Bash
---
```

**When Haiku:** Simple categorization (3x faster, 5% accuracy loss acceptable)
**When Sonnet:** Complex reasoning, code generation, multi-step analysis

---

## Advanced Patterns

### Pattern 4: Agent with Skills

**Preload skills** when agent uses skill in >50% of invocations (0s delay vs 2-5s on-demand).

```yaml
---
skills:
  - api-conventions
  - error-handling-patterns
---
```

**Skills NOT inherited** from parent conversation (must list in frontmatter).

### Pattern 5: Lifecycle Hooks

```yaml
---
hooks:
  PreToolUse:  # Validation before tool use
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate.sh"
  Stop:  # Cleanup when agent finishes
    - hooks:
        - type: command
          command: "./scripts/cleanup.sh"
---
```

### Pattern 6: Background Agent

**Background execution:** `run_in_background: true`
- ✅ Permission prompts upfront
- ❌ No AskUserQuestion (fails)
- ❌ No MCP tools

---

## Anti-Patterns (CRITICAL)

### ❌ Domain Knowledge in Agent Body
**Fix:** Move patterns to skills, reference skills in frontmatter

### ❌ Too Many Tool Restrictions
**Fix:** Allow all needed tools (Read, Grep, Glob, Bash for read-only, not just Read)

### ❌ Generic Agent Name
**Fix:** Domain-specific: `code-reviewer`, not `helper`

### ❌ First-Person Description
**Fix:** Third-person: "Review code..." not "I help you..."

### ❌ Missing WHY in Description
**Fix:** Include trigger: "Use proactively after code changes"

---

## Integration

**Agent references skills:** Full skill content injected at startup
**Command uses agent:** Command orchestrates, agents execute
**Skill forks to agent:** Skill content becomes agent task (`context: fork`)

---

## Troubleshooting

**Agent not triggering:** Check description matches user language, add "Use proactively"
**Missing skills:** Add to `skills:` frontmatter field (not inherited)
**Hook not blocking:** Exit code must be 2 (only 2 blocks operation)
**Triggers too often:** Narrow description trigger conditions

---

## Verification Checklist

### Structure
- [ ] File created: `.claude/agents/agent-name.md`
- [ ] Markdown file (not directory like skills)
- [ ] YAML frontmatter present
- [ ] System prompt in body

### Metadata
- [ ] Name: lowercase, hyphens, max 64 chars
- [ ] Description: third-person, <1024 chars, describes WHEN
- [ ] Tools: Only what's needed (or omit for inherit)
- [ ] Model: Appropriate for task (sonnet/opus/haiku)

### Content Quality
- [ ] System prompt describes APPROACH (not patterns)
- [ ] No domain knowledge in body (use skills instead)
- [ ] References skills for patterns
- [ ] Thin router (infrastructure only)
- [ ] Hook scripts separate (if any)

### Integration
- [ ] Skills listed in frontmatter (if needed)
- [ ] Hooks in separate files (if needed)
- [ ] Description enables auto-delegation

### Self-Check
- [ ] Is domain knowledge in skills? → If NO, move to skills
- [ ] Are tool restrictions justified? → If NO, remove restrictions
- [ ] Does agent duplicate skills? → If YES, remove duplication
- [ ] Is system prompt focused on approach? → If NO, refocus

---

## Quick Start Template

**Fastest way to create agent:**

```bash
# 1. Create file
touch .claude/agents/my-agent-name.md

# 2. Copy template and edit
cat > .claude/agents/my-agent-name.md << 'EOF'
---
name: my-agent-name
description: When to delegate to this agent
tools: Read, Grep, Glob
model: sonnet
skills:
  - relevant-skill
---

# System Prompt

You are a [role].

When invoked:
1. [Step 1]
2. [Step 2]
3. [Step 3]

## Guidelines
- [Guideline 1]
- [Guideline 2]
EOF

# 3. Test
# Ask Claude: "Use my-agent-name to..."
```

---

## Resources

### Internal (Agent-Specific)

- `@resources/agent-structure-reference.md` - Complete frontmatter specification, system prompt guidelines, validation checklist
- `@resources/agent-template.md` - Copy-paste ready templates for 10 common agent patterns (reviewer, validator, test runner, etc.)
- `@resources/agents-guide-condensed.md` - Condensed official documentation (built-in agents, configuration, patterns, troubleshooting)
- `@resources/agent-skill-relationship.md` - OS analogy (agents as OS, skills as apps), decision tree, auto-loading mechanism
- `@resources/refactoring-guide.md` - Thick→thin transformation process, step-by-step refactoring, production metrics

### Internal (Shared Philosophy)

- `@../resources/signal-vs-noise-reference.md` - Signal vs Noise philosophy (3-question filter, what to include/exclude in agent docs)
- `@resources/why-over-how-reference.md` - Content quality philosophy (WHY > HOW, production context for agent configuration) - **Agent-specific version** covering tool restrictions, permission modes, model selection

### Supporting Files

- `@scripts/validate-readonly.sh` - Example PreToolUse hook script for SQL validation (blocks write operations)

### External

- **Official Agent Documentation** - https://code.claude.com/docs/agents (complete reference)
- **Agent Skills Spec** - https://agentskills.io (open standard)

---

## Key Principles

**Thin routers** - Agents provide infrastructure, not knowledge

**Reference skills** - Domain knowledge lives in skills, not agents

**Tool restrictions** - Only restrict when necessary for safety/focus

**Third-person** - Describe WHEN to delegate, not HOW agent helps

**Isolation** - Use agents when context isolation benefits performance

**Proactive triggers** - Include "Use proactively" for auto-delegation

---

**Key Lesson:** The best agents are thin routing layers with focused tool access. All domain knowledge belongs in skills, not agent system prompts.
