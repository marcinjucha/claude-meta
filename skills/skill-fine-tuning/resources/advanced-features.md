# Advanced Features: Complete Implementation Guide

This resource provides detailed implementation steps, complete examples, and edge cases for advanced skill features (frontmatter, scripts, execution modes, tool restrictions, string substitutions).

**Use this resource when:** You need step-by-step implementation details or troubleshooting guidance for advanced features.

**SKILL.md contains:** Decision criteria (WHEN to use), key concepts, and brief examples.

---

## 1. context: fork (Isolated Execution)

### Complete Implementation Steps

**Step 1: Verify Skill Has Complete Prompt**

Fork requires a complete, self-contained task. It won't work with reference material or guidelines.

```yaml
# ❌ Won't work with fork (no task)
---
name: api-patterns
context: fork  # WRONG - just guidelines
---
Use these API patterns:
- Pattern 1
- Pattern 2

# ✅ Works with fork (complete task)
---
name: deep-research
context: fork
agent: Explore
---
Research $ARGUMENTS:
1. Find files with Glob
2. Analyze code
3. Summarize findings
```

**Step 2: Pick Subagent Type**

```yaml
agent: Explore          # Read-only codebase exploration (Read, Grep, Glob, WebFetch)
agent: Plan             # Planning/architecture analysis (Read, Grep, Glob, WebFetch)
agent: general-purpose  # Default (all tools available)
agent: custom-agent     # From .claude/agents/ directory
```

**Agent Capabilities:**
- **Explore**: Read, Grep, Glob, WebFetch, WebSearch - perfect for research
- **Plan**: Read, Grep, Glob, WebFetch, WebSearch - perfect for analysis
- **general-purpose**: All standard tools - use for tasks requiring Write/Edit
- **custom-agent**: Your own agent definition with custom tools/instructions

**Step 3: Update Frontmatter**

```yaml
---
name: existing-skill
context: fork           # NEW - enable isolated execution
agent: Explore          # NEW - specify subagent
allowed-tools: Read, Grep, Glob  # Optional - restrict further
---
```

**Step 4: Test Invocation**

Verify skill returns useful results:
- ✅ Research outputs are detailed and specific
- ✅ No "I don't have conversation context" messages
- ✅ Agent completes task without asking clarifying questions
- ❌ If confused or returns nothing, skill may lack complete instructions

### Edge Cases

**Case 1: Skill needs conversation context**
```yaml
# DON'T use fork if skill needs to reference earlier conversation
---
name: continue-work
context: fork  # WRONG - loses conversation history
---
Continue the implementation we discussed.
```

**Case 2: Skill with dynamic injection needs conversation**
```yaml
# If using \! `command` injection, fork is OK (commands run before isolation)
---
name: pr-analysis
context: fork
agent: Explore
---
Analyze this PR:
\! `gh pr diff`

Task: Review changes above.  # Fork is fine - diff already injected
```

**Case 3: Guidelines vs Task distinction**
```markdown
# GUIDELINE (no fork):
"When implementing APIs, follow these patterns..."

# TASK (use fork):
"Research API patterns in codebase. Find all controllers. Summarize common patterns."
```

### Troubleshooting

**Problem:** Skill returns empty or generic response

**Solution:** Skill likely doesn't have complete task. Add:
1. Explicit instructions (numbered steps)
2. Expected output format
3. Success criteria

**Problem:** Agent asks clarifying questions

**Solution:** Fork prevents conversation. Either:
1. Remove fork and allow interactive mode
2. Add all needed context to skill prompt

---

## 2. Script Integration

### Complete Implementation Steps

**Step 1: Create scripts/ Directory**

```bash
mkdir -p ~/.claude/skills/my-skill/scripts
```

**Step 2: Add Script with Proper Structure**

```python
# scripts/visualize.py
#!/usr/bin/env python3
"""Generate visualization from project data.

Usage:
    python visualize.py [target-directory]

Output:
    Creates output.html in current directory
"""

import sys
from pathlib import Path

def generate(target):
    """Generate visualization HTML."""
    # Read project data
    data = collect_data(target)

    # Generate HTML
    html = f"""
    <!DOCTYPE html>
    <html>
    <head><title>Project Visualization</title></head>
    <body>
        {render_data(data)}
    </body>
    </html>
    """

    # Write output
    output = Path('output.html')
    output.write_text(html)
    print(f'Generated {output.absolute()}')
    return output

if __name__ == '__main__':
    target = Path(sys.argv[1] if len(sys.argv) > 1 else '.')
    generate(target)
```

**Step 3: Make Script Executable**

```bash
chmod +x ~/.claude/skills/my-skill/scripts/visualize.py
```

**Step 4: Update SKILL.md to Reference Script**

```markdown
---
name: my-skill
allowed-tools: Bash(python *)
---

# My Skill

Generate visualization:

```bash
python ~/.claude/skills/my-skill/scripts/visualize.py .
```

Creates `output.html` with interactive visualization.

**Output:** `output.html` (open in browser)
```

**Step 5: Test Script Execution**

```bash
cd /path/to/test/project
python ~/.claude/skills/my-skill/scripts/visualize.py .
# Verify output.html created
```

### Script Best Practices

**1. Use absolute paths for skill scripts:**
```bash
# ✅ Good - works from any directory
python ~/.claude/skills/my-skill/scripts/visualize.py .

# ❌ Bad - only works from skill directory
python scripts/visualize.py .
```

**2. Accept target directory as argument:**
```python
# ✅ Good - flexible
target = Path(sys.argv[1] if len(sys.argv) > 1 else '.')

# ❌ Bad - hardcoded
target = Path('.')
```

**3. Print output file paths:**
```python
# ✅ Good - Claude knows where to find output
print(f'Generated {output.absolute()}')

# ❌ Bad - silent
output.write_text(html)
```

**4. Include docstring with usage:**
```python
"""Generate visualization from project data.

Usage:
    python visualize.py [target-directory]

Output:
    Creates output.html in current directory
"""
```

### Common Script Patterns

**Pattern 1: Data Collection + Visualization**
```python
def collect_data(target: Path) -> dict:
    """Scan codebase and collect metrics."""
    pass

def render_data(data: dict) -> str:
    """Generate HTML/SVG from data."""
    pass

def generate(target: Path) -> Path:
    """Main entry point."""
    data = collect_data(target)
    html = render_data(data)
    output = Path('output.html')
    output.write_text(html)
    return output
```

**Pattern 2: Report Generation**
```python
def analyze(target: Path) -> list:
    """Analyze project and return findings."""
    pass

def generate_report(findings: list) -> str:
    """Generate markdown report."""
    pass

def main(target: Path):
    findings = analyze(target)
    report = generate_report(findings)
    output = Path('report.md')
    output.write_text(report)
    print(f'Report: {output.absolute()}')
```

---

## 3. Dynamic Context Injection

### Complete Implementation

**Syntax:** Place `\! ` before backtick-wrapped command: `\! `command``

```yaml
---
name: pr-analysis
context: fork
agent: Explore
allowed-tools: Bash(gh *)
---

## Pull request context
- Diff: \! `gh pr diff`
- Comments: \! `gh pr view --comments`
- Files: \! `gh pr diff --name-only`

## Task
Analyze this PR for:
1. Code quality
2. Test coverage
3. Breaking changes
```

### How It Works

**Preprocessing (before Claude sees prompt):**
1. CLI finds all `\! `command`` patterns
2. Executes each command
3. Replaces pattern with command output
4. Sends fully-rendered prompt to Claude

**Example transformation:**
```markdown
# BEFORE (what you write):
Files changed: \! `gh pr diff --name-only`

# AFTER (what Claude sees):
Files changed:
src/api/controller.ts
src/api/service.ts
tests/api.test.ts
```

### Common Injection Commands

**GitHub PR data:**
```markdown
\! `gh pr diff`                    # Full diff
\! `gh pr view --comments`         # All comments
\! `gh pr diff --name-only`        # Changed files
\! `gh pr view --json checks`      # CI status
```

**Git status:**
```markdown
\! `git status --short`            # Short status
\! `git diff --staged`             # Staged changes
\! `git log -10 --oneline`         # Recent commits
```

**File contents:**
```markdown
\! `cat README.md`                 # Inject file
\! `head -20 src/main.ts`          # First 20 lines
```

**System state:**
```markdown
\! `date`                          # Current date
\! `pwd`                           # Current directory
\! `ls -la`                        # Directory listing
```

### Edge Cases

**Case 1: Command fails**
```markdown
# If command exits non-zero, output includes error
\! `gh pr diff`  # If not in PR context, shows error message
```

**Case 2: Command produces huge output**
```markdown
# Be careful with unbounded commands
\! `gh pr diff`  # Could be thousands of lines

# Better: limit output
\! `gh pr diff | head -100`
```

**Case 3: Command needs quotes**
```markdown
# Use single quotes inside command
\! `git log --format="%h %s" -10`
```

### When to Use

**YES - inject live data:**
- PR/issue details that change
- Git status before analysis
- Current file contents for context
- System state needed for decision

**NO - don't inject:**
- Static guidelines (put directly in skill)
- Large reference docs (use @resources/)
- Data that doesn't change (hardcode it)

---

## 4. Tool Restrictions

### Complete Implementation

**Step 1: Identify Tools Needed**

```markdown
Read-only analysis → Read, Grep, Glob
Data exploration → Read, Grep, Glob, WebFetch
Write operations → Read, Edit, Write, Bash
Git operations → Read, Grep, Bash(git *)
GitHub operations → Read, Bash(gh *)
```

**Step 2: Update Frontmatter**

```yaml
---
name: safe-reader
allowed-tools: Read, Grep, Glob
---
```

**Step 3: Document Restriction in Skill**

```markdown
## Tool Access

This skill limits Claude to read-only operations:
- Read - File reading
- Grep - Content search
- Glob - File finding

No write or bash access to prevent accidental modifications.
```

### Tool Restriction Patterns

**Pattern 1: Read-only research**
```yaml
---
name: codebase-explorer
allowed-tools: Read, Grep, Glob, WebFetch
---
```

**Pattern 2: Safe bash (specific commands)**
```yaml
---
name: git-analyzer
allowed-tools: Read, Grep, Bash(git *)
---
```

**Pattern 3: GitHub operations**
```yaml
---
name: pr-helper
allowed-tools: Read, Grep, Bash(gh *)
---
```

**Pattern 4: Full access (default)**
```yaml
---
name: implementation-helper
# No allowed-tools = all tools available
---
```

### Bash Command Restrictions

**Syntax:** `Bash(pattern)` where pattern is glob-style

```yaml
allowed-tools: Bash(git *)        # Only git commands
allowed-tools: Bash(gh *)         # Only gh commands
allowed-tools: Bash(python *)     # Only python commands
allowed-tools: Bash(npm *, yarn *) # Multiple patterns
```

**Examples:**
```yaml
# Allow git and gh
allowed-tools: Read, Grep, Bash(git *), Bash(gh *)

# Allow python scripts only
allowed-tools: Read, Bash(python *)

# Allow safe read-only bash
allowed-tools: Read, Bash(ls *), Bash(cat *)
```

### How Restrictions Work

**User permissions ALWAYS apply:**
- If user has auto-approval for Read → skill gets auto-approval
- If user requires approval for Bash → skill requires approval
- Skill cannot GRANT permissions, only RESTRICT further

**Example:**
```yaml
# User has auto-approval for all tools
# Skill restricts to read-only
---
name: research
allowed-tools: Read, Grep, Glob
---
# Result: Claude can use Read, Grep, Glob without asking
#         Claude CANNOT use Edit, Write, Bash (even though user allows it)
```

---

## 5. String Substitutions

### Available Substitutions

**Arguments:**
- `$ARGUMENTS` - All arguments as single string
- `$ARGUMENTS[0]` or `$0` - First argument
- `$ARGUMENTS[1]` or `$1` - Second argument
- `$ARGUMENTS[n]` or `$n` - Nth argument

**Session info:**
- `${CLAUDE_SESSION_ID}` - Current session ID

### Complete Implementation

**Step 1: Add argument-hint to Frontmatter**

```yaml
---
name: fix-issue
argument-hint: [issue-number]
---
```

**Step 2: Use Substitution in Skill Content**

```markdown
---
name: fix-issue
argument-hint: [issue-number]
---

# Fix GitHub Issue

Fix GitHub issue $ARGUMENTS following standards:

1. Fetch issue details:
   ```bash
   gh issue view $ARGUMENTS
   ```

2. Create branch:
   ```bash
   git checkout -b fix-$ARGUMENTS
   ```

3. Implement fix following project patterns

4. Reference issue in commit:
   ```
   Fix issue $ARGUMENTS
   ```
```

**Step 3: Test with Arguments**

```bash
# User types:
/fix-issue 123

# Claude sees:
Fix GitHub issue 123 following standards:
1. Fetch issue details: gh issue view 123
2. Create branch: git checkout -b fix-123
```

### Multiple Arguments

```yaml
---
name: compare-branches
argument-hint: [base-branch] [compare-branch]
---

Compare branches $0 and $1:

```bash
git diff $0..$1
```
```

**Usage:**
```bash
/compare-branches main feature-x
# Expands to: Compare branches main and feature-x: git diff main..feature-x
```

### Edge Cases

**Case 1: No arguments provided**
```markdown
# In skill:
Fix issue $ARGUMENTS

# User types: /fix-issue
# Claude sees: Fix issue
# (empty string - might be confusing)

# Better: provide default or check
Fix issue ${ARGUMENTS:-unspecified}
# OR add instructions:
# If no issue number provided, list open issues first.
```

**Case 2: Arguments with spaces**
```bash
# User types: /search-code "error handling"
# $ARGUMENTS = "error handling"
# Quotes preserved in substitution
```

**Case 3: Session ID for temp files**
```markdown
# Create session-specific temp file
```bash
echo "Data" > /tmp/output-${CLAUDE_SESSION_ID}.txt
```
```

### Common Patterns

**Pattern 1: Issue/PR operations**
```yaml
---
name: review-pr
argument-hint: [pr-number]
---
Review PR $ARGUMENTS:
\! `gh pr view $ARGUMENTS`
\! `gh pr diff $ARGUMENTS`
```

**Pattern 2: File operations**
```yaml
---
name: analyze-file
argument-hint: [file-path]
---
Analyze file: $ARGUMENTS

```bash
wc -l $ARGUMENTS
head -50 $ARGUMENTS
```
```

**Pattern 3: Search operations**
```yaml
---
name: find-pattern
argument-hint: [search-pattern]
---
Search codebase for: $ARGUMENTS

Use Grep tool with pattern: $ARGUMENTS
```

---

## Complete Example: Advanced Skill

Here's a skill using all advanced features:

```yaml
---
name: pr-review
description: Deep analysis of pull request with automated checks
argument-hint: [pr-number]
context: fork
agent: Explore
allowed-tools: Read, Grep, Glob, Bash(gh *)
---

# Pull Request Review: $ARGUMENTS

## Context (injected at runtime)

### PR Details
\! `gh pr view $ARGUMENTS`

### Changed Files
\! `gh pr diff $ARGUMENTS --name-only`

### Full Diff
\! `gh pr diff $ARGUMENTS`

## Analysis Tasks

1. **Code Quality**
   - Review changed files for patterns
   - Check test coverage
   - Verify naming conventions

2. **Breaking Changes**
   - Identify API changes
   - Check backwards compatibility

3. **Security**
   - Look for credential leaks
   - Check input validation

4. **Output**

   Generate review report:

   ```bash
   python ~/.claude/skills/pr-review/scripts/generate-report.py $ARGUMENTS
   ```

## Tool Restrictions

This skill uses read-only tools plus gh CLI:
- Read, Grep, Glob for code analysis
- Bash(gh *) for GitHub operations only

No file modifications to prevent accidental commits.
```

**Features used:**
- ✅ `argument-hint` - shows user what to pass
- ✅ `$ARGUMENTS` - substitutes PR number
- ✅ `context: fork` - isolated execution
- ✅ `agent: Explore` - read-only subagent
- ✅ `allowed-tools` - restricted to safe operations
- ✅ `\! `command`` - dynamic PR data injection
- ✅ Script integration - external report generation

---

## Troubleshooting Guide

### Problem: Fork returns nothing

**Cause:** Skill has guidelines, not task

**Solution:** Add explicit instructions with steps

### Problem: Dynamic injection shows error

**Cause:** Command failed (wrong directory, auth issue)

**Solution:** Test command manually first, ensure it works in expected context

### Problem: Tool restrictions ignored

**Cause:** User permission settings override

**Solution:** Skills can only restrict, not grant. Check user's permission settings.

### Problem: Arguments not substituting

**Cause:** Wrong syntax or missing argument-hint

**Solution:** Use `$ARGUMENTS`, `$0`, `$1` (not `${0}`), add `argument-hint` to frontmatter

### Problem: Script not found

**Cause:** Relative path used

**Solution:** Use absolute path: `~/.claude/skills/my-skill/scripts/script.py`

---

**Last Updated:** 2026-01-28
**Related:** See SKILL.md Pattern 6 for decision criteria and when to use each feature.
