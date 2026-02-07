# Agent Structure Reference

**Purpose:** Detailed specification of agent file structure, frontmatter fields, and system prompt guidelines.

---

## File Structure

### Agent File Format

Agents are single Markdown files (not directories like skills):

```
.claude/agents/
├── code-reviewer.md        # Single file per agent
├── db-reader.md
└── test-runner.md
```

**Not like skills:**
```
.claude/skills/
└── my-skill/               # Directory
    ├── SKILL.md            # Main file
    └── resources/          # Supporting files
```

---

## Frontmatter Fields

### Required Fields

**None required, but `description` strongly recommended.**

### All Available Fields

```yaml
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
```

---

### Field Specifications

#### `name` (optional)

- **Type:** String
- **Default:** Filename without extension
- **Format:** Lowercase letters, numbers, hyphens only
- **Max length:** 64 characters
- **Purpose:** Agent identifier for delegation

**Examples:**
```yaml
✅ GOOD:
name: code-reviewer
name: db-reader
name: test-runner-fast

❌ BAD:
name: Code Reviewer        # Spaces not allowed
name: db_reader            # Underscores not allowed
name: TestRunner           # CamelCase not allowed
```

---

#### `description` (recommended)

- **Type:** String
- **Max length:** 1024 characters
- **Format:** Third-person, describes WHEN to delegate
- **Purpose:** Claude uses this to decide when to delegate

**Best practices:**
- Third-person (not first-person "I help you")
- Describes trigger conditions ("Use when...", "Use after...")
- Include "Use proactively" for automatic delegation
- Specific enough to avoid false triggers

**Examples:**
```yaml
✅ GOOD:
description: Review code for quality and security. Use proactively after code changes.

description: Execute read-only database queries. Use for data analysis and reporting.

description: Run test suite and report failures. Use proactively before commits.

❌ BAD:
description: I help you review code        # First-person
description: Code reviewer                  # Too vague
description: Reviews code                   # Missing trigger
```

---

#### `tools` (optional)

- **Type:** String array or comma-separated string
- **Default:** Inherits all tools from parent
- **Purpose:** Allowlist of tools agent can use

**Available tools:**
- `Read` - Read files
- `Write` - Create files
- `Edit` - Modify files
- `Grep` - Search content
- `Glob` - Find files by pattern
- `Bash` - Execute commands
- `Task` - Launch subagents
- `WebFetch` - Fetch URLs
- `WebSearch` - Search web
- MCP tools (if configured)

**Format options:**
```yaml
# Array format
tools:
  - Read
  - Grep
  - Glob
  - Bash

# Comma-separated
tools: Read, Grep, Glob, Bash
```

**Common patterns:**
```yaml
# Read-only analysis
tools: Read, Grep, Glob, Bash

# Test runner
tools: Read, Bash

# Code modifier
tools: Read, Write, Edit, Bash

# Research only
tools: Read, Grep, Glob
```

---

#### `disallowedTools` (optional)

- **Type:** String array or comma-separated string
- **Default:** None
- **Purpose:** Denylist (removed from inherited or specified tools)

**When to use:**
- Want most tools BUT exclude specific ones
- More maintainable than long allowlist

**Examples:**
```yaml
# Allow all except Write/Edit (read-only)
disallowedTools: Write, Edit

# Allow all except Task (no subagents)
disallowedTools: Task

# Combine with tools
tools: Read, Grep, Glob, Bash, Write, Edit
disallowedTools: Write, Edit  # Results in: Read, Grep, Glob, Bash
```

---

#### `model` (optional)

- **Type:** String enum
- **Default:** `inherit`
- **Options:** `sonnet`, `opus`, `haiku`, `inherit`
- **Purpose:** Which model executes the agent

**Model characteristics:**

| Model | Speed | Cost | Capability | Use When |
|-------|-------|------|------------|----------|
| `haiku` | Fast | Low | Good | Pattern matching, parsing, simple analysis |
| `sonnet` | Medium | Medium | Excellent | Most tasks, default choice |
| `opus` | Slow | High | Best | Complex reasoning, critical decisions |
| `inherit` | - | - | - | Use parent conversation's model |

**Examples:**
```yaml
# Fast log parsing
model: haiku

# Code review (needs good analysis)
model: sonnet

# Critical security audit
model: opus

# Match parent conversation
model: inherit
```

**Decision guide:**
- **Haiku** - Speed > accuracy (logs, parsing, simple patterns)
- **Sonnet** - Balanced (most agents should use this)
- **Opus** - Accuracy critical (security, architecture, complex reasoning)
- **Inherit** - Follow parent's choice (default)

---

#### `permissionMode` (optional)

- **Type:** String enum
- **Default:** `default`
- **Options:** `default`, `acceptEdits`, `dontAsk`, `bypassPermissions`, `plan`
- **Purpose:** How agent handles permission prompts

**Mode behaviors:**

| Mode | File Edits | Commands | Network | Effect |
|------|-----------|----------|---------|--------|
| `default` | Prompt | Prompt | Prompt | Standard permission checking |
| `acceptEdits` | Auto-accept | Prompt | Prompt | Auto-approve file edits only |
| `dontAsk` | Auto-deny | Auto-deny | Auto-deny | Auto-deny all (allowed tools work) |
| `bypassPermissions` | Skip check | Skip check | Skip check | Skip ALL checks (dangerous) |
| `plan` | Auto-deny | Auto-deny | Auto-deny | Read-only exploration mode |

**When to use each:**

```yaml
# Test runner (creates temp files)
permissionMode: acceptEdits  # Auto-approve test fixtures

# Code reviewer (read-only analysis)
permissionMode: plan  # Deny all modifications

# CI/CD automation (trusted environment)
permissionMode: bypassPermissions  # Skip checks (use carefully)

# Standard analysis (normal prompts)
permissionMode: default  # Prompt as needed
```

**Warning:**
```yaml
# ⚠️ DANGEROUS - bypasses ALL security checks
permissionMode: bypassPermissions

# Use only in:
# - Trusted CI/CD environments
# - Automation scripts
# - NOT for user-facing agents
```

---

#### `skills` (optional)

- **Type:** String array
- **Default:** None
- **Purpose:** Skills to preload into agent context at startup

**How it works:**
1. Agent starts
2. Full skill content injected into context
3. Agent has immediate access to patterns

**Important notes:**
- Full skill content loaded (not just description)
- Skills NOT inherited from parent conversation
- Preloading is one-time cost at startup
- Only preload what's needed 80% of time

**Examples:**
```yaml
# API developer
skills:
  - api-conventions
  - error-handling-patterns
  - testing-strategy

# Code reviewer
skills:
  - code-quality-patterns
  - security-checklist

# Don't overload
skills:
  - pattern-1
  - pattern-2
  - pattern-3
  # ❌ Too many (agent context bloated)
```

**Decision guide:**
- Preload if: Needed in 80%+ of agent tasks
- Don't preload if: Only needed occasionally (agent can load on-demand)

---

#### `hooks` (optional)

- **Type:** Object with hook configurations
- **Default:** None
- **Purpose:** Lifecycle hooks scoped to this agent

**Available events:**

| Event | Matcher | When Fires |
|-------|---------|------------|
| `PreToolUse` | Tool name | Before agent uses tool |
| `PostToolUse` | Tool name | After agent uses tool |
| `Stop` | None | When agent finishes |

**Hook structure:**
```yaml
hooks:
  PreToolUse:
    - matcher: "Bash"         # Which tool
      hooks:
        - type: command       # Run shell command
          command: "./scripts/validate.sh"

  PostToolUse:
    - matcher: "Edit|Write"   # Regex matcher
      hooks:
        - type: command
          command: "./scripts/format.sh"

  Stop:
    - hooks:
        - type: command
          command: "./scripts/cleanup.sh"
```

**Exit codes:**
- `0` - Success, continue
- `1` - Warning (logged, continues)
- `2` - **Block operation** (PreToolUse only)

**Hook input format (JSON via stdin):**
```json
{
  "tool_name": "Bash",
  "tool_input": {
    "command": "psql -c 'SELECT * FROM users'"
  }
}
```

**Example validation script:**
```bash
#!/bin/bash
# scripts/validate-readonly.sh

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

# Block write operations
if echo "$COMMAND" | grep -iE '\b(DELETE|UPDATE|INSERT)\b' > /dev/null; then
  echo "Blocked: Write operation not allowed" >&2
  exit 2  # Block the operation
fi

exit 0  # Allow
```

---

## System Prompt Guidelines

### Purpose of System Prompt

The system prompt (markdown body after frontmatter) defines:

1. **Agent role** - What the agent is
2. **Task approach** - How agent should work
3. **Output format** - How to present results

**What system prompt is NOT:**
- ❌ Domain knowledge (use skills instead)
- ❌ Detailed patterns (use skills instead)
- ❌ Reference documentation (use skills instead)

---

### System Prompt Structure

```markdown
---
[frontmatter]
---

# [Agent Name] ([Key Characteristic])

**Purpose:** [One sentence - what problem agent solves]

You are a [role].

When invoked:
1. [Step 1]
2. [Step 2]
3. [Step 3]

## Guidelines

- [Guideline 1]
- [Guideline 2]
- [Guideline 3]

## Output Format

[How to present results]
```

---

### Good vs Bad System Prompts

**❌ BAD - Contains domain knowledge:**
```markdown
---
name: api-developer
---

You implement API endpoints.

## REST Conventions
- Use GET for retrieval
- Use POST for creation
- Use PUT for updates
[300 lines of REST patterns...]
```

**✅ GOOD - References skills:**
```markdown
---
name: api-developer
skills:
  - api-conventions
---

You implement API endpoints following team conventions.

When invoked:
1. Review preloaded api-conventions skill
2. Design endpoint following patterns
3. Implement with error handling
4. Add tests per testing-strategy skill

Present implementation with rationale for design choices.
```

---

### System Prompt Best Practices

**DO:**
- ✅ Describe agent role
- ✅ List execution steps
- ✅ Reference preloaded skills
- ✅ Define output format
- ✅ Keep under 200 lines

**DON'T:**
- ❌ Include domain patterns (use skills)
- ❌ Duplicate skill content
- ❌ Explain what Claude knows
- ❌ List all possible scenarios

---

### Length Guidelines

**System prompt length:**
- **Target:** 50-150 lines
- **Maximum:** 200 lines
- **If longer:** Move content to skills

**Note:** Content quality > line count. Complete approach within limits > incomplete guidance for brevity.

**Comparison:**
```
Agent system prompt: 50-150 lines (approach)
Skill content: 200-600 lines (patterns)
```

---

## Complete Agent Template

```markdown
---
name: agent-name
description: When to delegate to this agent. Use proactively when [trigger].
tools: Read, Grep, Glob, Bash
disallowedTools: Write, Edit
model: sonnet
permissionMode: default
skills:
  - relevant-skill-1
  - relevant-skill-2
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate.sh"
---

# [Agent Name] ([Key Characteristic])

**Purpose:** [One sentence problem statement]

You are a [role description].

When invoked:
1. [Step 1 - what to do first]
2. [Step 2 - what to do next]
3. [Step 3 - how to finish]

## Guidelines

- [Guideline 1 - how to approach the task]
- [Guideline 2 - what to prioritize]
- [Guideline 3 - what to avoid]

## Preloaded Skills

- `relevant-skill-1` - [What patterns it contains]
- `relevant-skill-2` - [What patterns it contains]

## Output Format

[How to structure the results]

Example:
```
[Expected output format]
```
```

---

## Validation Checklist

**Before finalizing agent:**

### Frontmatter
- [ ] `name` - Lowercase + hyphens, max 64 chars
- [ ] `description` - Third-person, describes WHEN, <1024 chars
- [ ] `tools` - Only necessary tools (or omit for inherit)
- [ ] `model` - Appropriate choice (haiku/sonnet/opus/inherit)
- [ ] `skills` - Only preload what's needed 80% of time

### System Prompt
- [ ] Role clearly defined
- [ ] Execution steps listed (3-5 steps)
- [ ] References preloaded skills (not duplicate content)
- [ ] Output format specified
- [ ] Under 200 lines (move content to skills if longer)

### Architecture
- [ ] Agent is thin router (not thick knowledge)
- [ ] Domain knowledge in skills (not agent body)
- [ ] Tool restrictions justified (security/safety)
- [ ] Permission mode appropriate for task

---

## Quick Reference

### Tool Restriction Patterns

```yaml
# Read-only analysis
tools: Read, Grep, Glob, Bash
disallowedTools: Write, Edit

# Test runner (needs temp files)
tools: Read, Bash
permissionMode: acceptEdits

# Code modifier
tools: Read, Write, Edit, Bash

# Pure research
tools: Read, Grep, Glob
permissionMode: plan
```

### Model Selection Patterns

```yaml
# Fast parsing/analysis
model: haiku

# Standard tasks
model: sonnet

# Critical decisions
model: opus

# Follow parent
model: inherit
```

### Skill Preloading Patterns

```yaml
# Domain-specific agent
skills:
  - domain-conventions
  - domain-patterns

# Multi-domain agent
skills:
  - api-conventions
  - error-handling
  - testing-strategy

# No preload (on-demand)
skills: []
```

---

**Key Principle:** Agent file defines infrastructure (tools, model, permissions). Skills contain knowledge (patterns, conventions, decisions).
