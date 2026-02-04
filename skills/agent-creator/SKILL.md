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

**Purpose:** Analyze codebase without modifications

```yaml
---
name: code-reviewer
description: Review code for quality and best practices. Use after code changes.
tools: Read, Grep, Glob, Bash
model: sonnet
skills:
  - code-quality-patterns
  - security-patterns
---

You are a senior code reviewer.

When invoked:
1. Run git diff to see changes
2. Focus on modified files
3. Apply patterns from preloaded skills

Provide feedback organized by priority:
- Critical issues (must fix)
- Warnings (should fix)
- Suggestions (consider)
```

**Why read-only tools:**

Production incident: Review agent with Write access accidentally "fixed" code during review → review feedback inconsistent with committed code → confusion in PR discussion thread.

Fix: Explicit tool restrictions (`tools: Read, Grep, Glob, Bash`) enforce read-only → agent cannot modify files → consistent review process → feedback matches actual code state.

**Key points:**
- ✅ Tool restrictions enforce read-only
- ✅ Skills contain patterns (not agent body)
- ✅ System prompt describes approach

### Pattern 2: Conditional Validator

**Purpose:** Allow tool but validate usage

```yaml
---
name: db-reader
description: Execute read-only database queries. Use for data analysis.
tools: Bash
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-readonly.sh"
---

You are a database analyst with read-only access.

Execute SELECT queries to answer questions.
You cannot modify data (INSERT, UPDATE, DELETE).
```

**Hook script (scripts/validate-readonly.sh):**
```bash
#!/bin/bash
INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

# Block write operations
if echo "$COMMAND" | grep -iE '\b(INSERT|UPDATE|DELETE|DROP|CREATE|ALTER)\b' > /dev/null; then
  echo "Blocked: Only SELECT queries allowed" >&2
  exit 2  # Exit code 2 blocks the operation
fi

exit 0
```

**Key points:**
- ✅ Hook validates before execution
- ✅ Exit code 2 blocks operation
- ✅ Error message via stderr

### Pattern 3: Parallel Researcher

**Purpose:** Independent research in isolation

```yaml
---
name: deep-researcher
description: Thorough codebase research with detailed analysis
model: sonnet
permissionMode: plan
skills:
  - research-guidelines
---

You are a thorough researcher.

When invoked:
1. Explore codebase systematically
2. Document findings with file references
3. Summarize patterns and insights

Present findings in structured format.
```

**Key points:**
- ✅ Plan mode for read-only
- ✅ Model specified for capability
- ✅ Skills provide research methodology

### Pattern 4: Fast Processor

**Purpose:** Quick operations with Haiku

```yaml
---
name: log-analyzer
description: Parse and summarize log files. Use for log analysis.
model: haiku
tools: Read, Bash
---

You are a log analyzer.

When invoked:
1. Read log files
2. Extract errors and warnings
3. Summarize by category

Keep analysis concise.
```

**Why Haiku for simple tasks:**

Production metrics:
- Haiku: ~2-3s response time, 90% accuracy for log categorization
- Sonnet: ~8-10s response time, 95% accuracy for same task
- Trade-off: 3x faster, 5% accuracy loss acceptable for simple categorization

When NOT to use Haiku:
- Complex reasoning (use Sonnet) - code architecture analysis, multi-step debugging
- Code generation (use Sonnet) - implementation quality matters more than speed
- Multi-step analysis (use Sonnet) - requires maintaining complex context

**Key points:**
- ✅ Haiku for speed + cost
- ✅ Limited tools for focused task
- ✅ Concise system prompt

---

## Advanced Patterns

### Pattern: Agent with Skills

**Agent preloads skill content at startup:**

```yaml
---
name: api-developer
description: Implement API endpoints following team conventions
skills:
  - api-conventions
  - error-handling-patterns
  - testing-strategy
---

You implement API endpoints.

Follow conventions from preloaded skills:
- api-conventions (patterns and rules)
- error-handling-patterns (error handling)
- testing-strategy (test coverage)

When implementing:
1. Design endpoint following conventions
2. Implement with error handling
3. Add tests per strategy
```

**Why preload skills:**

Performance impact:
- Preloaded: Skills available immediately in agent context (0s delay)
- On-demand: Agent must invoke Skill tool → additional API call → 2-5s delay per skill access

When to preload:
- Agent uses skill in >50% of invocations → preload (example: code-reviewer uses style-guide in 80% of reviews)
- Agent uses skill rarely (<20%) → let agent load on-demand (example: db-reader rarely needs migration-patterns)

**How it works:**
1. Agent starts with skills injected into context
2. Full skill content available (not just description)
3. Agent references skill knowledge in system prompt
4. Skills are NOT inherited from parent conversation

**When to use:**
- Agent needs domain knowledge to operate
- Domain knowledge reusable across agents
- Knowledge changes independently of agent logic

### Pattern: Lifecycle Hooks

**Agent with setup/cleanup:**

```yaml
---
name: integration-tester
description: Run integration tests with environment setup
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-test-command.sh"
  Stop:
    - hooks:
        - type: command
          command: "./scripts/cleanup-test-env.sh"
---

You run integration tests.

Environment is set up automatically.
Run tests and report results.
Environment is cleaned up on completion.
```

**Hook events:**

| Event | Matcher | When it fires |
|-------|---------|---------------|
| `PreToolUse` | Tool name | Before agent uses tool |
| `PostToolUse` | Tool name | After agent uses tool |
| `Stop` | (none) | When agent finishes |

### Pattern: Background Agent

**Agent runs concurrently:**

```yaml
---
name: test-runner
description: Run test suite in background
model: haiku
permissionMode: acceptEdits
---

You run the test suite.

1. Run all tests
2. Collect failures
3. Report summary with file:line references

Continue even if some tests fail.
```

**Invocation:**
- User: "Run tests in the background"
- Claude: Launches agent with `run_in_background: true`
- Agent executes concurrently
- Results returned when complete

**Key points:**
- ✅ Permission prompts upfront (before background)
- ✅ Auto-deny any non-approved tools
- ✅ No AskUserQuestion (fails if attempted)
- ✅ No MCP tools in background

---

## Anti-Patterns (Common Mistakes)

### ❌ Domain Knowledge in Agent Body

**Problem:** Agent contains 500 lines of API patterns

```yaml
# ❌ WRONG
---
name: api-developer
---
You implement API endpoints. Follow these patterns:

## REST Conventions
[300 lines of REST patterns...]

## Error Handling
[200 lines of error patterns...]
```

**Fix:** Move domain knowledge to skills

```yaml
# ✅ CORRECT
---
name: api-developer
skills:
  - api-conventions
  - error-handling-patterns
---
You implement API endpoints following team conventions.
Refer to preloaded skills for patterns.
```

### ❌ Agent Duplicates Existing Skills

**Problem:** Agent reimplements patterns already in skills

**Fix:** Reference skills instead of duplicating content

### ❌ Too Many Tool Restrictions

**Problem:** Agent restricts tools unnecessarily

```yaml
# ❌ WRONG - Read-only but denies Grep/Glob
---
name: code-reviewer
tools: Read
---
```

**Fix:** Allow all needed tools for read-only analysis

```yaml
# ✅ CORRECT
---
name: code-reviewer
tools: Read, Grep, Glob, Bash
disallowedTools: Write, Edit
---
```

### ❌ Generic Agent Name

**Problem:** `helper`, `processor`, `analyzer`

**Fix:** Domain-specific: `code-reviewer`, `db-reader`, `test-runner`

### ❌ First-Person Description

**Problem:** `description: "I help you review code"`

**Fix:** `description: "Review code for quality and best practices. Use after code changes."`

### ❌ Missing WHY in Description

**Problem:** `description: "Code reviewer"`

**Fix:** `description: "Review code for quality and security. Use proactively after code changes or before merging."`

### ❌ Agent Contains Hook Scripts

**Problem:** Agent body includes bash script code

**Fix:** Hook scripts in separate files, referenced via hooks frontmatter

---

## CLI Pattern: Temporary Agents

**Create agent for current session only:**

```bash
claude --agents '{
  "code-reviewer": {
    "description": "Review code for quality and best practices",
    "prompt": "You are a senior code reviewer. Focus on security and performance.",
    "tools": ["Read", "Grep", "Glob", "Bash"],
    "model": "sonnet"
  }
}'
```

**JSON format:**
- `prompt` = System prompt (equivalent to markdown body)
- Same fields as frontmatter
- Not saved to disk (session only)

**When to use:**
- Quick testing
- Automation scripts
- CI/CD pipelines
- One-off tasks

---

## Integration with Skills and Commands

### Agent References Skills

**Agent loads skills at startup:**

```yaml
---
name: api-developer
skills:
  - api-conventions
  - error-handling-patterns
---
```

**Full skill content injected when agent starts.**

### Command Uses Agent

**Command delegates to agent:**

```markdown
# .claude/commands/implement-api.md

Phase 1: Use api-developer agent to implement endpoint
Phase 2: Use test-runner agent to validate
Phase 3: Use code-reviewer agent to review
```

**Command orchestrates, agents execute.**

### Skill Forks to Agent

**Skill runs in agent context:**

```yaml
# .claude/skills/deep-research/SKILL.md
---
name: deep-research
context: fork
agent: Explore
---

Research $ARGUMENTS thoroughly:
1. Find files
2. Analyze code
3. Summarize findings
```

**Skill content becomes agent task.**

---

## Troubleshooting

### Agent Not Triggering

**Problem:** Claude doesn't delegate to agent

**Fixes:**
1. Check description matches user's natural language
2. Verify description includes "Use proactively" if should auto-trigger
3. Ask Claude "What agents are available?"
4. Request explicitly: "Use the agent-name agent to..."

### Agent Missing Skills

**Problem:** Agent doesn't have access to skill content

**Cause:** Skills not listed in agent's `skills:` field

**Fix:** Add skills to frontmatter (agents don't inherit from parent)

### Hook Not Blocking

**Problem:** PreToolUse hook doesn't block operation

**Cause:** Exit code not 2 (only exit code 2 blocks)

**Fix:** Ensure hook script `exit 2` on validation failure

### Agent Triggers Too Often

**Problem:** Claude delegates when you don't want it

**Fix:** Make description more specific (narrow trigger conditions)

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

## Examples from Documentation

### Built-in Agents

**Explore** - Fast codebase research
- Model: Haiku (speed)
- Tools: Read-only (no Write/Edit)
- Purpose: File discovery, code search

**Plan** - Research for planning
- Model: Inherits from main
- Tools: Read-only
- Purpose: Gather context before plan

**General-purpose** - Complex multi-step
- Model: Inherits from main
- Tools: All tools
- Purpose: Research + action

### Custom Agent Examples

**Code Reviewer** (from docs)
```yaml
---
name: code-reviewer
description: Expert code review. Use proactively after code changes.
tools: Read, Grep, Glob, Bash
model: inherit
---

You are a senior code reviewer.

When invoked:
1. Run git diff
2. Focus on modified files
3. Begin review

Review checklist:
- Code clarity
- No duplicated code
- Error handling
- Security issues

Provide feedback by priority.
```

**Database Query Validator** (from docs)
```yaml
---
name: db-reader
description: Execute read-only database queries
tools: Bash
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-readonly.sh"
---

You are a database analyst with read-only access.
Execute SELECT queries. Cannot modify data.
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

- `@resources/signal-vs-noise-reference.md` - Signal vs Noise philosophy (3-question filter, what to include/exclude in agent docs)
- `@resources/why-over-how-reference.md` - Content quality philosophy (WHY > HOW, production context for agent configuration)

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
