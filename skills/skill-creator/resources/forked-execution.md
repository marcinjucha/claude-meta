# Forked Execution - Skills with Isolated Context

**Purpose:** Advanced pattern for skills that run in isolated subagent context without conversation history. Use for research tasks, analysis tasks, or self-contained operations.

---

## What is Forked Execution?

Skills with `context: fork` run in isolated subagent context. The skill content becomes the complete prompt for a subagent.

**Key difference:**

| Regular Skill | Forked Skill |
|---------------|--------------|
| Runs inline in conversation | Runs in isolated subagent |
| Has conversation history | NO conversation history |
| Reference material | Complete task prompt |
| Claude loads when needed | User/Claude invokes directly |

---

## Two Approaches: Skills vs Agents

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

**Agent with skills field** - You write custom agent that uses skills as reference:

```yaml
---
name: custom-analyzer
skills:
  - pattern-group-1
  - pattern-group-2
---

You are an analyzer. Use loaded skills for patterns.
```

This is for defining custom agents (see agent documentation).

---

## How Forked Execution Works

**Example: deep-research skill**

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

**What happens when invoked:**

1. User invokes: `/deep-research authentication`
2. `$ARGUMENTS` replaced with "authentication"
3. New isolated context created (no conversation history)
4. Skill content becomes prompt for subagent:
   ```
   Research authentication thoroughly:
   1. Find relevant files...
   ```
5. `agent` field determines execution environment (Explore = read-only tools)
6. Subagent executes research
7. Returns summary to main conversation

---

## When to Use context: fork

**Use `context: fork` when:**

- **Research task** - Explore codebase without conversation noise
- **Analysis task** - Focused examination
- **Skill has complete instructions** - Self-contained prompt
- **Don't need conversation context** - Task standalone
- **Want to use existing agent type** - Explore, Plan, general-purpose

**Don't use `context: fork` when:**

- **Skill is reference material** - Guidelines, patterns
- **Needs conversation context** - Refers to "previous discussion"
- **Just provides knowledge** - Not actionable task
- **Guidelines without task** - "Use these patterns" (no action)

---

## Good vs Bad Forked Skills

### ❌ Wrong - Reference Skill with Fork

```yaml
---
name: api-patterns
context: fork
---

Use these API conventions:
- Pattern A
- Pattern B
- Pattern C

When implementing APIs, follow these patterns.
```

**Problem:** No actionable task, just guidelines. Subagent receives guidelines but no instruction, returns nothing useful.

---

### ✅ Correct - Reference Skill Without Fork

```yaml
---
name: api-patterns
---

Use these API conventions:
- Pattern A
- Pattern B
- Pattern C

When implementing APIs, follow these patterns.
```

**Why better:** Agent loads this as reference when needed, uses patterns inline.

---

### ✅ Correct - Task Skill with Fork

```yaml
---
name: api-research
description: Research API usage patterns in codebase
context: fork
agent: Explore
---

Research API usage for $ARGUMENTS:

1. Find API endpoints using Glob (`**/api/*.ts`)
2. Search for usage patterns with Grep
3. Analyze implementations
4. Summarize:
   - Common patterns found
   - File locations (file:line)
   - Usage examples

Output: Markdown with file references.
```

**Why correct:** Complete task with clear instructions, actionable, returns useful summary.

---

## Agent Types for Forked Skills

When using `context: fork`, specify agent type with `agent` field:

```yaml
agent: Explore          # Read-only: Glob, Grep, Read, WebFetch, WebSearch
agent: Plan             # Planning: All tools except Edit/Write
agent: general-purpose  # Full access: All tools (default)
agent: custom-agent     # Custom agent from .claude/agents/
```

**Pick based on task:**

- **Explore** - Codebase research, documentation search (read-only)
- **Plan** - Architecture analysis, planning (read-only + analysis)
- **general-purpose** - Tasks needing write access
- **custom-agent** - Specialized behavior from `.claude/agents/`

---

## Frontmatter Fields for Forked Skills

```yaml
---
name: skill-name
description: What this skill does (shows in skill list)
context: fork              # Run in isolated subagent
agent: Explore             # Which agent type to use
allowed-tools: Read, Grep  # Optional: limit tools further
model: haiku               # Optional: override model
---
```

**Field details:**

| Field | Required | Description |
|-------|----------|-------------|
| `context` | Yes | Set to `fork` for isolated execution |
| `agent` | No | Agent type (default: `general-purpose`) |
| `allowed-tools` | No | Further restrict tools |
| `model` | No | Override model (sonnet, opus, haiku) |

---

## String Substitutions

Forked skills support variable substitution:

```yaml
---
name: research-feature
context: fork
agent: Explore
---

Research $ARGUMENTS:

1. Find files: Use Glob to find *$0*
2. Search code: Use Grep for "$1"
3. Analyze and report

Session ID: ${CLAUDE_SESSION_ID}
```

**Available variables:**

| Variable | Description |
|----------|-------------|
| `$ARGUMENTS` | All arguments passed |
| `$0`, `$1`, `$2`, ... | Individual arguments |
| `${CLAUDE_SESSION_ID}` | Current session ID |

**Example invocation:**

```
/research-feature components authentication
```

Becomes:

```
Research components authentication:
1. Find files: Use Glob to find *components*
2. Search code: Use Grep for "authentication"
```

---

## Dynamic Context Injection

Use `\! `command`` syntax to run shell commands before skill executes:

```yaml
---
name: pr-summary
description: Summarize pull request changes
context: fork
agent: Explore
allowed-tools: Bash(gh *)
---

## Pull request context

- PR diff: \! `gh pr diff`
- PR comments: \! `gh pr view --comments`
- Changed files: \! `gh pr diff --name-only`

## Your task

Summarize this pull request:
1. What changed (from diff above)
2. Why (from comments above)
3. Impact on codebase
```

**How it works:**

1. Commands execute BEFORE skill sent to Claude (preprocessing)
2. Output replaces the injection placeholder
3. Claude receives fully-rendered prompt with actual data

**Example output after injection:**

```markdown
## Pull request context

- PR diff:
  ```diff
  + const newFeature = ...
  - const oldCode = ...
  ```
- PR comments: "This fixes the authentication bug"
- Changed files:
  src/auth/login.ts
  src/auth/validator.ts

## Your task

Summarize this pull request:
[Claude sees actual PR data, not commands]
```

---

## Example Patterns

### Pattern 1: Codebase Research

```yaml
---
name: explore-feature
description: Explore how feature is implemented
context: fork
agent: Explore
---

Explore how $ARGUMENTS is implemented:

1. Find relevant files
   - Use Glob: `**/*$ARGUMENTS*`
   - Use Grep: `"$ARGUMENTS"`

2. Analyze implementation
   - Read key files
   - Understand patterns
   - Note dependencies

3. Report findings
   - Files involved (with paths)
   - Key patterns used
   - Dependencies identified
```

### Pattern 2: Documentation Analysis

```yaml
---
name: analyze-docs
description: Analyze documentation for topic
context: fork
agent: Explore
---

Analyze documentation for $ARGUMENTS:

1. Find docs
   - Glob: `**/*.md`
   - Grep: "$ARGUMENTS"

2. Read and extract
   - Usage examples
   - API references
   - Best practices

3. Summarize
   - How to use $ARGUMENTS
   - Common patterns
   - Important notes
```

### Pattern 3: Live Data Research

```yaml
---
name: pr-analysis
description: Analyze pull request with live data
context: fork
agent: Explore
allowed-tools: Bash(gh *)
---

## Live PR Data

- Diff: \! `gh pr diff $ARGUMENTS`
- Status: \! `gh pr view $ARGUMENTS --json state,title`
- Reviews: \! `gh pr view $ARGUMENTS --json reviews`

## Analysis Task

Analyze PR $ARGUMENTS:
1. Review changes (from diff above)
2. Check review comments
3. Assess readiness for merge

Report: Ready to merge? Why/why not?
```

---

## Comparison: Regular vs Forked

### Regular Skill (Inline)

```yaml
---
name: api-conventions
---

# API Conventions

Use these patterns when implementing APIs:
- RESTful naming
- Standard error format
- Request validation

[Guidelines continue...]
```

**Usage:** Claude loads as reference when needed

**Context:** Has conversation history

**Output:** None (just loaded as knowledge)

---

### Forked Skill (Isolated)

```yaml
---
name: api-research
context: fork
agent: Explore
---

Research API patterns in $ARGUMENTS:

1. Find API files
2. Analyze patterns
3. Report common conventions

[Complete instructions...]
```

**Usage:** Explicitly invoked (`/api-research src/api`)

**Context:** NO conversation history (isolated)

**Output:** Summary report returned to main conversation

---

## Best Practices

### DO:

- ✅ Write complete, self-contained instructions
- ✅ Include explicit steps (1, 2, 3...)
- ✅ Specify output format
- ✅ Use for research/analysis tasks
- ✅ Pick appropriate agent type
- ✅ Test with real invocations

### DON'T:

- ❌ Use fork for reference material
- ❌ Assume conversation context available
- ❌ Write vague instructions
- ❌ Forget output format
- ❌ Use for interactive tasks (no back-and-forth)

---

## Troubleshooting

### Problem: Forked Skill Returns Nothing

**Cause:** Skill contains guidelines but no actionable task

**Fix:** Add explicit task with steps

```yaml
# ❌ Wrong
---
context: fork
---
Use these patterns...

# ✅ Correct
---
context: fork
---
Research $ARGUMENTS:
1. [Step 1]
2. [Step 2]
3. [Step 3]
```

---

### Problem: Skill Needs Conversation Context

**Cause:** Skill refers to "previous discussion"

**Fix:** Remove `context: fork` or make self-contained

```yaml
# ❌ Wrong with fork
Based on our previous discussion about authentication...

# ✅ Correct
Research authentication patterns:
(Self-contained task)
```

---

### Problem: Wrong Agent Type

**Cause:** Task needs write access but using Explore (read-only)

**Fix:** Change agent type

```yaml
# ❌ Wrong - Explore is read-only
---
context: fork
agent: Explore
---
Refactor code... (needs Write)

# ✅ Correct
---
context: fork
agent: general-purpose
---
Refactor code... (has Write)
```

---

## Key Takeaways

**Forked execution is for:**
- ✅ Research tasks (codebase exploration)
- ✅ Analysis tasks (focused examination)
- ✅ Self-contained operations
- ✅ Tasks with complete instructions

**Forked execution is NOT for:**
- ❌ Reference material (guidelines, patterns)
- ❌ Interactive workflows (back-and-forth)
- ❌ Tasks needing conversation context
- ❌ Guidelines without actionable task

**Remember:**
- Skill content = Complete prompt for subagent
- No conversation history in forked context
- Pick agent type based on tools needed
- Write explicit, actionable instructions

---

**Key Lesson:** `context: fork` turns skill into complete task prompt for isolated subagent. Use for research/analysis, not for reference material.
