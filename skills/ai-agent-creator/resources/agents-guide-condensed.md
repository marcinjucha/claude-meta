# Agents Guide (Condensed)

**Purpose:** Condensed version of official Claude Code agent documentation. Focus on essential concepts and patterns.

**Full documentation:** https://code.claude.com/docs/agents

---

## What Are Subagents?

Subagents are specialized AI assistants that handle specific types of tasks. Each runs in its own context with custom system prompt, tool access, and permissions.

**Key benefits:**
- **Preserve context** - Keep exploration out of main conversation
- **Enforce constraints** - Limit tools a subagent can use
- **Reuse configurations** - User-level subagents work across projects
- **Specialize behavior** - Focused system prompts for domains
- **Control costs** - Route tasks to cheaper models like Haiku

---

## Built-in Subagents

Claude Code includes these built-in agents:

| Agent | Model | Tools | Purpose |
|-------|-------|-------|---------|
| **Explore** | Haiku | Read-only | Fast codebase exploration |
| **Plan** | Inherits | Read-only | Research during plan mode |
| **General-purpose** | Inherits | All tools | Complex multi-step tasks |
| **Bash** | Inherits | Bash | Terminal commands in isolation |

---

## Create Custom Agents

### File Format

Agents are single Markdown files (not directories):

```
.claude/agents/my-agent.md
```

### Basic Structure

```markdown
---
name: my-agent
description: When to delegate to this agent
tools: Read, Grep, Glob
model: sonnet
---

# System prompt

You are a [role].

When invoked:
1. [Step 1]
2. [Step 2]
```

### Location and Priority

| Location | Scope | Priority |
|----------|-------|----------|
| `--agents` CLI flag | Current session | 1 (highest) |
| `.claude/agents/` | Project | 2 |
| `~/.claude/agents/` | User (all projects) | 3 |
| Plugin `agents/` | Where plugin enabled | 4 (lowest) |

---

## Frontmatter Configuration

### Essential Fields

```yaml
---
name: agent-name              # Lowercase + hyphens
description: When to delegate # <1024 chars, third-person
---
```

### Tool Configuration

```yaml
# Allowlist
tools: Read, Grep, Glob, Bash

# Denylist
disallowedTools: Write, Edit

# Combine (results in Read, Grep, Glob, Bash)
tools: Read, Grep, Glob, Bash, Write, Edit
disallowedTools: Write, Edit
```

### Model Selection

```yaml
model: sonnet      # Default choice
model: haiku       # Fast, cheap
model: opus        # Best capability
model: inherit     # Use parent's model
```

### Permission Modes

```yaml
permissionMode: default            # Standard prompts
permissionMode: acceptEdits        # Auto-accept file edits
permissionMode: dontAsk            # Auto-deny all
permissionMode: bypassPermissions  # Skip checks (dangerous)
permissionMode: plan               # Read-only exploration
```

### Preload Skills

```yaml
skills:
  - skill-one
  - skill-two
```

Full skill content injected at agent startup. Skills NOT inherited from parent.

---

## Working with Subagents

### Automatic Delegation

Claude delegates based on:
1. Task description in your request
2. Agent's `description` field
3. Current context

**Encourage proactive delegation:**
```yaml
description: Review code. Use proactively after code changes.
```

### Explicit Delegation

```
Use the code-reviewer subagent to review my changes
Have the test-runner subagent check the tests
```

### Foreground vs Background

**Foreground (blocking):**
- Blocks main conversation until complete
- Permission prompts passed through
- AskUserQuestion works

**Background (concurrent):**
- Runs while you continue working
- Pre-approval for all needed permissions
- Auto-denies non-approved tools
- AskUserQuestion fails
- No MCP tools

**Control:**
- Ask Claude "run this in the background"
- Press **Ctrl+B** to background running task

---

## Resume Subagents

Each invocation creates fresh context. To continue existing work:

```
Continue that code review and now analyze authorization logic
```

Claude resumes agent with full conversation history preserved.

**Transcript location:**
```
~/.claude/projects/{project}/{sessionId}/subagents/agent-{agentId}.jsonl
```

---

## Hooks for Subagents

### In Agent Frontmatter

Hooks that run while agent is active:

```yaml
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate.sh"
  PostToolUse:
    - matcher: "Edit|Write"
      hooks:
        - type: command
          command: "./scripts/format.sh"
  Stop:
    - hooks:
        - type: command
          command: "./scripts/cleanup.sh"
```

### In settings.json

Hooks that run in main session on agent lifecycle:

```json
{
  "hooks": {
    "SubagentStart": [
      {
        "matcher": "db-agent",
        "hooks": [
          { "type": "command", "command": "./scripts/setup-db.sh" }
        ]
      }
    ],
    "SubagentStop": [
      {
        "matcher": "db-agent",
        "hooks": [
          { "type": "command", "command": "./scripts/cleanup-db.sh" }
        ]
      }
    ]
  }
}
```

### Hook Exit Codes

- `0` - Success, continue
- `1` - Warning (logged, continues)
- `2` - **Block operation** (PreToolUse only)

### Hook Input (JSON via stdin)

```json
{
  "tool_name": "Bash",
  "tool_input": {
    "command": "psql -c 'SELECT * FROM users'"
  }
}
```

---

## Common Patterns

### Isolate High-Volume Operations

Run tests, fetch docs, process logs in subagent. Verbose output stays isolated:

```
Use a subagent to run the test suite and report only failures
```

### Run Parallel Research

Independent investigations in parallel:

```
Research authentication, database, and API modules in parallel using separate subagents
```

**Warning:** Each subagent returns results to main conversation. Many detailed results consume context.

### Chain Subagents

Sequential workflow:

```
Use code-reviewer to find issues, then use optimizer to fix them
```

---

## When to Use Subagents

**Use subagents when:**
- Task produces verbose output you don't need in main context
- Need specific tool restrictions or permissions
- Work is self-contained and can return summary
- Need isolation for performance

**Use main conversation when:**
- Need frequent back-and-forth or iteration
- Multiple phases share significant context
- Making quick, targeted change
- Latency matters (subagents start fresh, need time for context)

**Consider skills instead when:**
- Want reusable prompts in main conversation
- Need reference patterns, not isolated execution

---

## Agent Architecture Pattern

**Agents = Thin Routers**
- Provide infrastructure (tools, model, permissions)
- Reference skills for domain knowledge
- Keep system prompt focused on approach

**Skills = Thick Applications**
- Contain domain knowledge and patterns
- Detailed conventions and rules
- Reference documentation

**Example:**
```yaml
# ❌ WRONG - Agent contains domain knowledge
---
name: api-developer
---
You implement APIs following these patterns:
[500 lines of API patterns...]

# ✅ CORRECT - Agent references skills
---
name: api-developer
skills:
  - api-conventions
  - error-handling
---
You implement APIs following team conventions.
Refer to preloaded skills for patterns.
```

---

## Context Management

### Auto-Compaction

Subagents support automatic compaction at ~95% capacity.

**Set trigger percentage:**
```bash
export CLAUDE_AUTOCOMPACT_PCT_OVERRIDE=50  # Trigger at 50%
```

### Transcript Persistence

- **Main conversation compaction** - Subagent transcripts unaffected
- **Session persistence** - Transcripts survive session restarts
- **Automatic cleanup** - Based on `cleanupPeriodDays` (default 30)

---

## Disable Specific Agents

### In settings.json

```json
{
  "permissions": {
    "deny": ["Task(Explore)", "Task(my-custom-agent)"]
  }
}
```

### CLI Flag

```bash
claude --disallowedTools "Task(Explore)"
```

---

## CLI Pattern: Temporary Agents

Create agent for current session:

```bash
claude --agents '{
  "code-reviewer": {
    "description": "Review code for quality",
    "prompt": "You are a senior code reviewer.",
    "tools": ["Read", "Grep", "Glob", "Bash"],
    "model": "sonnet"
  }
}'
```

**JSON format:**
- `prompt` = System prompt (markdown body)
- Same fields as frontmatter
- Not saved to disk

---

## Example Agents

### Read-Only Reviewer

```yaml
---
name: code-reviewer
description: Review code. Use proactively after changes.
tools: Read, Grep, Glob, Bash
model: sonnet
skills:
  - code-quality-patterns
  - security-patterns
---

You are a senior code reviewer.

When invoked:
1. Run git diff to see changes
2. Review against preloaded patterns
3. Organize findings by priority

Provide feedback:
- Critical (must fix)
- Warnings (should fix)
- Suggestions (consider)
```

### Database Validator

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

Execute SELECT queries to answer questions.
You cannot modify data.
```

**Hook script:**
```bash
#!/bin/bash
INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

if echo "$COMMAND" | grep -iE '\b(INSERT|UPDATE|DELETE)\b' > /dev/null; then
  echo "Blocked: Only SELECT allowed" >&2
  exit 2  # Block operation
fi

exit 0
```

### Fast Log Analyzer

```yaml
---
name: log-analyzer
description: Parse and summarize log files
model: haiku
tools: Read, Bash
---

You are a log parser optimized for speed.

When invoked:
1. Read log files
2. Extract errors and warnings
3. Summarize by category

Keep analysis concise.
```

---

## Best Practices

### Design Focused Agents

Each agent excels at one specific task:
- ✅ code-reviewer (review only)
- ✅ test-runner (tests only)
- ❌ code-helper (too vague)

### Write Detailed Descriptions

Claude uses description to decide when to delegate:
- ✅ "Review code for quality and security. Use proactively after changes."
- ❌ "Helps with code"

### Limit Tool Access

Grant only necessary permissions:
- Security: Prevent accidental modifications
- Focus: Fewer tools = clearer purpose

### Check into Version Control

Project agents benefit entire team. Share with git:
```
.claude/
└── agents/
    ├── code-reviewer.md
    ├── test-runner.md
    └── doc-generator.md
```

---

## Troubleshooting

### Agent Not Triggering

1. Check description includes keywords users say
2. Verify with "What agents are available?"
3. Rephrase to match description
4. Request explicitly: "Use agent-name agent to..."

### Agent Missing Skills

Cause: Skills not in `skills:` field

Fix: Add to frontmatter (agents don't inherit from parent)

### Hook Not Blocking

Cause: Exit code not 2

Fix: Ensure script exits with code 2 on validation failure

---

## Key Concepts Summary

**Subagent basics:**
- Isolated context with custom configuration
- Preserve main conversation context
- Specialize with tools, model, permissions

**File structure:**
- Single markdown file per agent
- YAML frontmatter + system prompt
- Store in project, user, or CLI

**Tool restrictions:**
- `tools` - Allowlist
- `disallowedTools` - Denylist
- Combine for precise control

**Execution modes:**
- Foreground - Blocks, interactive
- Background - Concurrent, pre-approved
- Resume - Continue with full context

**Hooks:**
- PreToolUse - Validate before execution
- PostToolUse - Process after execution
- Stop - Cleanup on agent finish

**Architecture:**
- Agents = Thin (infrastructure)
- Skills = Thick (knowledge)
- Preload skills for immediate access

---

**Full documentation:** https://code.claude.com/docs/agents
