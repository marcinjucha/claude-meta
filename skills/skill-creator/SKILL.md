---
name: skill-creator
description: Use when creating new Agent Skills for this project. Provides decision framework (signal vs noise), creation process, templates, and verification checklist.
---

# Skill Creator - Meta Skill for Creating Skills

## Purpose

Guide the creation of high-quality Agent Skills that are concise, signal-focused, and project-specific. Ensures consistency with agent-skill architecture (Skills for domain knowledge, Commands for workflows, Agents for specialized tasks).

## When to Use

- **Creating new skill** - Have domain knowledge to extract from docs or codebase
- **Evaluating if skill needed** - Unsure whether to create skill vs command vs agent
- **Refactoring existing docs** - Converting documentation to skill format
- **Reviewing skill quality** - Verifying skill follows best practices

## Core Philosophy

**Content Quality > Line Count**

The 500-line guideline is a target, not a hard limit. If high-quality, signal-focused content requires more space, use it. Better to have 600 lines of pure signal than 300 lines that omit critical information.

**What matters:**
- ✅ Every line provides project-specific value
- ✅ No generic explanations Claude knows
- ✅ Critical mistakes documented with WHY
- ✅ Scannable structure (easy to find what you need)
- ❌ NOT arbitrary line count compliance

**Trade-off:** More comprehensive content (600 lines) vs splitting to Tier 3 files (300 + 300)
- **Keep together** if content is interconnected and needs context
- **Split to Tier 3** if content is modular and self-contained

**See:** `@resources/signal-vs-noise-reference.md` for the complete 3-question filter and application examples.

## Decision Framework

### Should You Create a Skill?

**Ask these 3 questions (Signal vs Noise):**

1. **Is this project-specific?**
   - ✅ YES → Data access patterns with critical anti-pattern
   - ❌ NO → Generic framework patterns (Claude knows)

2. **Is this timeless?**
   - ✅ YES → Architecture decisions (module structure)
   - ❌ NO → "As of January 2025..." (outdated quickly)

3. **Does this help make decisions?**
   - ✅ YES → When to use Pattern A vs Pattern B (decision table)
   - ❌ NO → "Framework X is a library for..." (noise)

**If 3/3 YES → Create skill**
**If 2/3 YES → Consider creating skill**
**If 1/3 YES → Don't create skill**

### Skill vs Command vs Agent?

| Type | Purpose | When to Create | Example |
|------|---------|----------------|---------|
| **Skill** | Domain knowledge | Project-specific patterns, rules, decisions | `data-patterns`, `ui-patterns` |
| **Command** | Workflow orchestration | Multi-phase processes with multiple agents | `/implement-feature`, `/debug` |
| **Agent** | Specialized task execution | Need specific tools, loaded by commands | `plan-analyzer`, `docs-updater` |

**Quick Decision:**
- Need to **reference patterns**? → Skill
- Need to **orchestrate workflow**? → Command
- Need to **execute specific task**? → Agent

---

## Creation Process

### Step 1: Analyze Source Material

**Identify what to extract:**

```yaml
Source: docs/CODE_PATTERNS.md (950 lines)

Extract to skills:
  - data-access-patterns:
      - Circular dependency bug (CRITICAL)
      - Caching strategy selection
      - Query optimization patterns
      - Schema migration workflow

  - ui-component-patterns:
      - Component composition patterns
      - State management patterns
      - Validation rules (project-specific)
      - Type safety enforcement

Signal: 40% (project-specific)
Noise: 60% (generic framework patterns)

Result: Create 2 skills, keep only signal
```

**Red flags (don't extract):**
- ❌ Generic explanations ("What is a design pattern?")
- ❌ Basic syntax ("How to use framework X")
- ❌ Framework docs ("Library Y API reference")
- ❌ Common patterns Claude knows ("State management basics")

**Extract (project-specific):**
- ✅ Critical mistakes we made ("Circular dependency crash")
- ✅ Project decisions ("Why we use Pattern A not Pattern B")
- ✅ Architecture rules ("Layer A vs Layer B separation")
- ✅ Access control rules ("Never context from user input")

### Step 2: Design Skill Structure

**Decide Tier 2 vs Tier 3 split:**

```yaml
SKILL.md (Tier 2): Aim for ~500 lines (quality > count)
  - Core principles (what, when, why)
  - Quick reference tables
  - Anti-patterns (critical mistakes)
  - Complete if interconnected, reference Tier 3 if modular

Tier 3 files: Optional detailed examples
  - rls-policies.md - Full RLS policy examples
  - client-selection.md - Server vs browser client guide
  - testing-rls.md - RLS testing commands
```

**Decision guide:**
- **Keep in SKILL.md** if interconnected (needs context from other sections)
- **Split to Tier 3** if modular (self-contained, can be read independently)
- **Quality first:** Better 600 lines of signal than 300 incomplete
- **Typical range:** 150-600 lines depending on domain complexity

### Step 3: Write SKILL.md

**Frontmatter fields (all optional except name/description recommended):**

```yaml
---
name: skill-name                    # Lowercase + hyphens, max 64 chars
description: >                      # WHEN to use (3rd person, <1024 chars)
  Use when [trigger]. Provides [what]. Critical for [why essential].

argument-hint: [filename]           # Autocomplete hint (e.g., "[issue-number]")
disable-model-invocation: false     # true = only user can invoke (like /deploy)
user-invocable: true                # false = hide from menu (background knowledge)
allowed-tools: Read, Grep, Glob     # Tools Claude can use without permission
model: sonnet                       # sonnet | opus | haiku
context: fork                       # Run in isolated subagent context
agent: Explore                      # Which subagent (if context: fork)
hooks:                              # Skill-scoped hooks (see Hooks docs)
  pre-tool: hook-script.sh
---
```

**Field usage guide:**

**Basic fields (always include):**
- `name` - Used for `/skill-name` command
- `description` - Claude uses this to decide when to invoke automatically

**Control invocation:**
- `disable-model-invocation: true` - Prevent Claude from auto-invoking (use for workflows with side effects like /deploy, /commit)
- `user-invocable: false` - Hide from menu (use for background knowledge skills)

**String substitutions (use in skill body):**
- `$ARGUMENTS` - All arguments passed (if not present, appended as "ARGUMENTS: <value>")
- `$ARGUMENTS[0]` or `$0` - First argument
- `$ARGUMENTS[1]` or `$1` - Second argument
- `${CLAUDE_SESSION_ID}` - Current session ID (for logging, session-specific files)

**Example with arguments:**
```markdown
---
name: fix-issue
argument-hint: [issue-number]
---
Fix GitHub issue $ARGUMENTS following coding standards.
```
Running `/fix-issue 123` → Claude sees "Fix GitHub issue 123..."

**Advanced execution:**
- `context: fork` - Run skill in isolated subagent (no conversation history)
- `agent: Explore` - Which subagent type (Explore, Plan, general-purpose, or custom)
- `allowed-tools` - Tools Claude can use without approval when skill active

**Use this structure:**

```markdown
---
name: skill-name
description: When to use (third-person, <1024 chars)
---

# Skill Name - One-Line Description

## Purpose
[1-2 sentences: What problem does this solve?]

## When to Use
- Trigger 1
- Trigger 2
- Trigger 3

## Core Principles (or Patterns)

### Principle 1: Name
**What:** [Brief explanation]
**Why:** [Real problem we hit]
**Example:** [Minimal code if needed]

### Principle 2: Name
[Continue...]

## Quick Reference
[Tables, checklists, commands - scannable format]

## Anti-Patterns (Critical Mistakes We Made)

### ❌ Mistake 1
**Problem:** [What broke]
**Why it failed:** [Root cause]
**Fix:** [What we do now]

## References
- @tier3-file-1.md - Description
- @tier3-file-2.md - Description
```

**Writing tips:**
- **Signal-focused** - Only project-specific, skip generic (most important)
- **Quality > brevity** - Include everything critical, even if longer
- **WHY included** - Always explain WHY decisions made (critical for context)
- **Scannable** - Use tables, bullets, headers for quick reference
- **Third-person** - "Use when..." not "I can help..."
- **Complete** - Better comprehensive than artificially short

### Step 4: Create Supporting Files (Optional)

**When to create supporting files:**
- Detailed code examples (>50 lines)
- Multiple related patterns (5+ examples)
- Deep-dive guides (comprehensive explanation)
- Scripts that Claude can execute (Python, bash, etc.)
- Templates for Claude to fill in

**Supporting file structure:**

```
my-skill/
├── SKILL.md              # Main skill (required, aim <500 lines)
├── reference.md          # Detailed reference docs (loaded when needed)
├── examples.md           # Usage examples collection
├── template.md           # Template for Claude to fill in
└── scripts/
    ├── helper.py         # Utility script Claude can execute
    └── visualize.sh      # Script for generating output
```

**Reference supporting files from SKILL.md:**

```markdown
## Additional Resources

- For complete API details, see [reference.md](reference.md)
- For usage examples, see [examples.md](examples.md)
- Script for visualization: [scripts/visualize.py](scripts/visualize.py)
```

**Keep SKILL.md under 500 lines** - move detailed examples to supporting files.

**Example: Script integration**

Skills can bundle scripts in any language. This codebase-visualizer example includes a Python script that generates interactive HTML:

```
codebase-visualizer/
├── SKILL.md              # Instructions (200 lines)
└── scripts/
    └── visualize.py      # Python script (130 lines)
```

SKILL.md instructs Claude to run the script:
````markdown
---
name: codebase-visualizer
allowed-tools: Bash(python *)
---

Generate interactive HTML tree view of project structure.

## Usage

Run from project root:

```bash
python ~/.claude/skills/codebase-visualizer/scripts/visualize.py .
```

Creates `codebase-map.html` with:
- Collapsible directory tree
- File sizes
- Color-coded file types
- Bar chart breakdown
````

The script generates visual output that opens in browser. Pattern works for any visual output: dependency graphs, test coverage, database schema, etc.

**Keep Tier 3 self-contained** - no nested references.

### Step 4a: Advanced Execution Patterns (Optional)

**Use these patterns for specialized skill behavior:**

#### Pattern 1: Run in Isolated Subagent (context: fork)

Add `context: fork` when skill needs isolated execution without conversation history.

```yaml
---
name: deep-research
context: fork
agent: Explore
allowed-tools: Read, Grep, Glob
---

Research $ARGUMENTS thoroughly:
1. Find relevant files
2. Analyze code
3. Summarize with specific file references
```

**How it works:**
1. Skill content becomes the prompt for subagent
2. Subagent has no conversation history (isolated context)
3. `agent` field picks subagent type (Explore, Plan, general-purpose, or custom from `.claude/agents/`)
4. Results returned to main conversation

**When to use:**
- Research tasks (explore codebase without history noise)
- Analysis tasks (focus on specific task, no conversation context)
- Tasks with explicit instructions (skill content is complete prompt)

**When NOT to use:**
- Skills with guidelines only (no actionable task → subagent returns nothing)
- Skills that need conversation context

#### Pattern 2: Dynamic Context Injection

Use the **dynamic injection syntax** to inject live data before Claude sees the skill.

**Syntax format:** exclamation mark, then backtick, then command, then backtick

```yaml
---
name: pr-summary
context: fork
agent: Explore
allowed-tools: Bash(gh *)
---

## Pull request context
- PR diff: !(backtick)gh pr diff(backtick)
- PR comments: !(backtick)gh pr view --comments(backtick)
- Changed files: !(backtick)gh pr diff --name-only(backtick)

## Your task
Summarize this pull request...
```

**Note:** In your actual skill file, replace the word (backtick) with the backtick character.

**How it works:**
1. Commands execute BEFORE skill sent to Claude (preprocessing)
2. Output replaces the injection placeholder with actual command output
3. Claude receives fully-rendered prompt with actual data

**This is NOT something Claude executes** - it's preprocessing that runs before Claude sees the skill.

**When to use:**
- Fetch live PR/issue data
- Include current system state
- Inject file contents or command output

#### Pattern 3: Tool Restrictions

Use `allowed-tools` to grant Claude permission for specific tools when skill active.

```yaml
---
name: safe-reader
allowed-tools: Read, Grep, Glob
---

Read and analyze files without making changes.
```

Claude can use Read, Grep, Glob without approval when this skill active. Other tools still require permission (based on user's permission settings).

**When to use:**
- Read-only analysis (allow Read/Grep/Glob, block Edit/Write)
- Specific tool workflows (allow only tools needed)
- Reduce permission prompts for trusted skills

### Step 5: Update Agent/Command References

**If skill should be loaded by agents:**

```yaml
# .claude/agents/server-action-developer.md
---
name: server-action-developer
skills:
  - code-patterns        # NEW
  - supabase-patterns    # NEW
---
```

**If skill should be referenced in commands:**

```markdown
# .claude/commands/implement-phase.md

## Reference Documentation

**Skills (loaded automatically via agent skills: field):**
- `data-access-patterns` - Data layer patterns (access rules, optimization)
- `code-patterns` - Application patterns (Server Actions, types)
```

### Step 6: Verify Quality

**Run through checklist:**

- [ ] Name: lowercase + hyphens, max 64 chars
- [ ] Description: third-person, describes WHEN to use, <1024 chars
- [ ] Body: <500 lines (ideally 150-300)
- [ ] References: One level deep only
- [ ] Signal: Only project-specific (no generic explanations)
- [ ] Third-person: "Use when..." not "I help..."
- [ ] WHY included: Explains rationale for decisions
- [ ] Anti-patterns: Documents critical mistakes made
- [ ] Scannable: Tables, bullets, headers for quick lookup
- [ ] Self-check: Would this help future me with amnesia?

**Token budget check:**
```bash
wc -l .claude/skills/skill-name/SKILL.md
# Should be: <500 lines (ideally 150-300)
```

---

## Advanced Pattern: Document Mental Models, Not Just Mistakes

**Meta-principle for skill creation:**

When documenting anti-patterns, reveal the **WHY behind the mistake** - the systematic mental model that caused it. This prevents the mistake from recurring, not just documents it happened.

### Why Mental Models Matter (Signal vs Noise)

**SIGNAL (High Value):**
- **Why mistakes happen** - cognitive bias, incorrect assumptions
- **Systematic patterns** - same error by multiple developers independently
- **Mental model shift** - what thinking needs to change

**NOISE (Low Value):**
- **What mistake looks like** - code example alone
- **How to fix** - mechanical steps without understanding
- **One-off bugs** - unique circumstances, not repeatable pattern

**Production validation:**
- 6 mental model anti-patterns in `tca-error-patterns`
- Prevented 8/10 future test failures (same mental model)
- ROI: One mental model = prevents N future bugs

### Signal Test: When to Document Mental Models

**Ask: "Is this a systematic thinking error?"**

**YES → Document mental model:**
- ✅ Same mistake by 2+ developers independently
- ✅ "Feels natural but is wrong" pattern
- ✅ Tests fail on first attempt consistently
- ✅ Mistake repeated after fix (mental model not updated)

**NO → Regular anti-pattern:**
- ❌ One-off bug with unique context
- ❌ Obvious mistake (typo, copy-paste error)
- ❌ Framework limitation, not thinking error

**Example:** LoginStore tests
- Symptom: 3 developers made same mistake (manual `.send()` after automatic action)
- Root cause: NOT "didn't read docs"
- Root cause: **"Synchronous thinking in async world"** = mental model error

### Structure Template: Mental Model Anti-Patterns

**Focus on WHY, minimize HOW:**

```markdown
### ❌ Mental Model N: [Descriptive Name]

**Incorrect mental model:**
"[Quote the incorrect thinking - one sentence]"

**Why this thinking fails:**
- [Cognitive bias / natural assumption that misleads]
- [Context that makes wrong approach feel right]
- [What developers expect vs what actually happens]

**Correct mental model:**
"[Quote the correct thinking - one sentence]"

**Why this matters:**
[Production impact / prevented bugs / developer efficiency]

**Decision trigger:**
[One question to ask before action]
```

**Anti-pattern:** Don't include code examples in mental model section
- Code = HOW to fix
- Mental model = WHY mistake happens
- Keep focused on thinking shift, not mechanical fix

### Integration: When Creating Skills

**Include mental model section IF:**
1. Skill involves testing (tests reveal thinking patterns)
2. Multiple production bugs from same root cause
3. Pattern violation "feels natural" (counter-intuitive correct approach)
4. New team members consistently make same mistake

**Skip mental model section IF:**
- Skill is purely informational (no decisions/actions)
- Mistakes are one-off, context-specific
- Pattern is obvious once explained (no thinking shift needed)

**Example skills with mental models:**
- `tca-error-patterns` - 6 TCA testing mental models (high ROI)
- Future: Any skill where "natural thinking" leads to systematic bugs

---

## Templates

### Basic SKILL.md Template

See `@skill-template.md` for copy-paste ready template.

**Minimal viable skill:**

```yaml
---
name: my-skill-name
description: Use when [specific trigger]. Provides [what it provides].
---

# Skill Name - Purpose

## When to Use
- Trigger 1
- Trigger 2

## Core Pattern
**What:** [Brief explanation]
**Why:** [Problem it solves]

## Quick Reference
- Key fact 1
- Key fact 2

## Anti-Patterns
### ❌ Common Mistake
**Fix:** [What to do instead]
```

**Expand as needed** - start minimal, add sections as patterns emerge.

---

## Skill Types (This Project)

### Type 1: Technical Patterns (Database, Code)

**Examples:** `data-access-patterns`, `ui-component-patterns`

**Focus:**
- Technical decisions with rationale
- Critical bugs we hit (with fixes)
- Architecture constraints
- Quick reference commands/tables

**Structure:**
```markdown
## Pattern Name
**Rule:** [What to do/avoid]
**Why:** [Real problem we hit]
**Example:** [Minimal code]
```

### Type 2: Architectural Decisions (Structure, Organization)

**Examples:** `architecture-decisions`, `design-system`

**Focus:**
- Why architecture chosen
- Import rules and boundaries
- Change impact mapping
- Module placement rules

**Structure:**
```markdown
## Decision: [Name]
**Context:** [What problem we were solving]
**Decision:** [What we chose]
**Consequences:** [Trade-offs, constraints]
```

### Type 3: Process & Philosophy (Workflows, Principles)

**Examples:** `signal-vs-noise`, `claude-md-guidelines`

**Focus:**
- Decision frameworks (3-question filter)
- Writing guidelines (what to include/exclude)
- Quality criteria (when something is good enough)

**Structure:**
```markdown
## The [Framework/Filter/Process]

**Purpose:** [What it helps decide]

**Questions:**
1. Question 1?
2. Question 2?
3. Question 3?

**Examples:**
- ✅ Good example
- ❌ Bad example
```

### Type 4: Integration & Tools (APIs, Services)

**Examples:** `notion-integration`

**Focus:**
- API patterns (MCP tool calls)
- Configuration (resource IDs, status values)
- Error handling (graceful fallbacks)
- Critical gotchas (case-sensitive values)

**Structure:**
```markdown
## Tool Pattern: [Name]

**Purpose:** [When to use]
**Critical:** [Gotcha that caused bugs]

**Example:**
```typescript
// Correct usage
```

**Common mistakes:**
- ❌ Wrong approach → ✅ Correct approach
```

---

## Anti-Patterns (Common Mistakes)

### ❌ Too Much Noise (Generic Content)

**Problem:** SKILL.md is 1,200 lines but 70% is generic explanations.

**Fix:**
1. Remove generic explanations Claude knows
2. Keep project-specific content even if longer
3. Quality matters more than line count

**Example:**
```markdown
❌ Before (noise - 300 lines):
## What is a Server Action?
Server Actions are functions that run on the server...
[300 words explaining React Server Components basics]

✅ After (signal - 50 lines):
## Server Action Pattern
Return type: { success: boolean, data?: T, error?: string }
**Why:** Type-safe error handling, no thrown exceptions
**We hit this:** Throwing errors in actions crashed Next.js middleware

[Project-specific examples with actual code]
```

**Key insight:** 600 lines of pure signal > 300 lines with 50% noise

### ❌ Generic Content (Not Project-Specific)

**Problem:** Skill explains React basics Claude already knows.

**Fix:** Only include project-specific decisions and critical mistakes.

**Self-check:** "Would Claude know this without the skill?"
- YES → Remove it (noise)
- NO → Keep it (signal)

### ❌ First-Person Description

**Problem:** `description: "I help you debug Supabase issues"`

**Fix:** `description: "Use when debugging data access patterns or caching issues."`

**Rule:** Third-person, describes WHEN not HOW.

### ❌ Missing WHY

**Problem:** States rules without explaining rationale.

```markdown
❌ Without WHY:
## RLS Policy Rule
Never query same table in RLS policy.

✅ With WHY:
## RLS Policy Rule
Never query same table in RLS policy.
**Why:** Causes infinite recursion, crashes PostgreSQL with stack overflow.
**We hit this:** survey_links table RLS checking survey_links.active crashed prod.
```

### ❌ Nested References (Too Deep)

**Problem:** SKILL.md → guide.md → examples.md → details.md

**Fix:** Keep references one level deep. Make Tier 3 files self-contained.

```markdown
✅ Correct:
SKILL.md references:
  - @rls-policies.md (self-contained examples)
  - @client-selection.md (self-contained guide)

❌ Wrong:
SKILL.md references:
  - @guide.md which references @examples.md which references @details.md
```

### ❌ Windows Paths

**Problem:** Examples use `C:\Users\...` in cross-platform project.

**Fix:** Use Unix paths (`~/`, `/path/to/`) or relative paths.

### ❌ Time-Sensitive Information

**Problem:** "As of January 2025, Supabase version 2.5..."

**Fix:** "Check Supabase version in package.json"

### ❌ Generic Skill Names

**Problem:** `patterns`, `helper`, `utils`

**Fix:** Domain-specific: `data-access-patterns`, `ui-component-patterns`, `design-system`

---

## Troubleshooting

### Skill Not Triggering

**Problem:** Claude doesn't use skill when expected.

**Fixes:**
1. Check description includes keywords users naturally say
2. Verify skill appears in "What skills are available?"
3. Try rephrasing request to match description
4. Invoke directly with `/skill-name` to test

**Example:**
```yaml
# ❌ Too vague
description: "Helps with data patterns"

# ✅ Specific triggers
description: "Use when creating data schemas, debugging RLS policies, or optimizing queries. Critical for preventing circular dependency bugs in access control."
```

### Skill Triggers Too Often

**Problem:** Claude uses skill when you don't want it.

**Fixes:**
1. Make description more specific (narrow the trigger conditions)
2. Add `disable-model-invocation: true` if should only be manual

### Claude Doesn't See All Skills

**Problem:** Some skills not available to Claude.

**Cause:** Skill descriptions exceed character budget (default 15,000 characters).

**Fix:**
1. Run `/context` to check for warning about excluded skills
2. Increase limit: Set `SLASH_COMMAND_TOOL_CHAR_BUDGET` environment variable
3. Or shorten skill descriptions (focus on triggers, remove examples)

### Skill with context: fork Returns Nothing

**Problem:** Forked skill returns empty or useless output.

**Cause:** Skill contains guidelines but no actionable task.

**Fix:**
- `context: fork` requires explicit instructions (task)
- Don't fork skills with just reference material ("use these patterns")
- Only fork skills with complete prompts ("do X, then Y, output Z")

```yaml
# ❌ Won't work with fork
---
context: fork
---
Use these API conventions:
- Pattern 1
- Pattern 2

# ✅ Works with fork
---
context: fork
---
Research $ARGUMENTS:
1. Find files with Glob
2. Analyze with Read
3. Summarize findings
```

---

## Verification Checklist

Before finalizing skill, verify:

### Structure
- [ ] Directory created: `.claude/skills/skill-name/`
- [ ] SKILL.md exists with YAML frontmatter
- [ ] Tier 3 files (if needed) are self-contained
- [ ] No nested references (one level deep only)

### Metadata
- [ ] Name: lowercase, hyphens, max 64 chars
- [ ] Description: third-person, <1024 chars, describes WHEN
- [ ] No XML tags in description
- [ ] Domain-specific name (not generic)

### Content Quality (Priority: Signal > Brevity)
- [ ] Signal-focused (only project-specific) - MOST IMPORTANT
- [ ] No generic explanations Claude knows - CRITICAL
- [ ] WHY included for all decisions/rules - ESSENTIAL
- [ ] Anti-patterns documented (critical mistakes)
- [ ] Complete (includes all critical information)
- [ ] Scannable format (tables, bullets, headers)
- [ ] Line count: Aim ~500, accept more if quality demands it

### Integration
- [ ] Added to relevant agent `skills:` field (if applicable)
- [ ] Referenced in commands (if applicable)
- [ ] Tested: Claude can invoke it correctly

### Self-Check Questions (Quality Filter)
- [ ] Is this obvious to Claude without the skill? → If YES, remove (noise)
- [ ] Is this project-specific? → If NO, remove (generic)
- [ ] Would this help future me with amnesia? → If NO, remove (not useful)
- [ ] Does every section provide actionable information? → If NO, refactor
- [ ] Did I cut content to meet line count? → If YES, restore it (quality > count)
- [ ] Is every line signal (no filler)? → If NO, remove filler (not to reduce length)

---

## Quick Start Template

**Fastest way to create a skill:**

```bash
# 1. Create directory
mkdir -p .claude/skills/my-skill-name

# 2. Copy template
cp .claude/skills/skill-creator/skill-template.md \
   .claude/skills/my-skill-name/SKILL.md

# 3. Edit SKILL.md
# - Update YAML frontmatter (name, description)
# - Fill in sections with project-specific content
# - Remove unused sections
# - Keep <500 lines

# 4. Verify line count
wc -l .claude/skills/my-skill-name/SKILL.md

# 5. Test invocation
# Ask Claude: "Use @my-skill-name to help with..."
```

---

## Examples from This Project

### High-Quality Skills (Follow These)

**data-access-patterns (132 lines)**
- ✅ Project-specific (circular dependency bug)
- ✅ WHY included (explains why patterns exist)
- ✅ Critical mistakes documented
- ✅ Quick reference tables (server vs browser client)
- ✅ Concise (<500 lines)

**signal-vs-noise (112 lines)**
- ✅ Decision framework (3 questions)
- ✅ Examples show good vs bad
- ✅ Actionable (helps decide what to include)
- ✅ Philosophy skill (no code, pure decision-making)

**claude-md-guidelines (127 lines)**
- ✅ Writing guidelines (what to include/exclude)
- ✅ Self-check questions
- ✅ Examples of good vs bad docs
- ✅ Meta-documentation (how to document)

### Advanced Pattern Examples

**Skill with context: fork (research task):**
```yaml
---
name: deep-research
description: Research topic thoroughly using codebase exploration
context: fork
agent: Explore
---

Research $ARGUMENTS thoroughly:
1. Find relevant files using Glob and Grep
2. Read and analyze the code
3. Summarize findings with specific file references
```
When invoked: Creates isolated subagent, executes research, returns summary.

**Skill with dynamic context injection (PR analysis):**
```yaml
---
name: pr-summary
description: Summarize pull request changes
context: fork
agent: Explore
allowed-tools: Bash(gh *)
---

## Pull request context
- PR diff: !(backtick)gh pr diff(backtick)
- PR comments: !(backtick)gh pr view --comments(backtick)

## Your task
Summarize this pull request...
```
Note: Replace (backtick) with the backtick character. Commands execute first, output injected, then Claude sees fully-rendered prompt.

**Skill with script integration (visual output):**
```yaml
---
name: codebase-visualizer
description: Generate interactive tree visualization
allowed-tools: Bash(python *)
---

Run visualization script:
```bash
python ~/.claude/skills/codebase-visualizer/scripts/visualize.py .
```

Creates `codebase-map.html` with interactive directory tree.
```
Script generates HTML, opens in browser. Pattern for any visual output.

### Skills to Reference

- **data-access-patterns** - Technical pattern skill (data layer, access control)
- **code-patterns** - Application pattern skill (React, TypeScript)
- **architecture-decisions** - Architectural skill (structure, rules)
- **notion-integration** - Integration skill (API, MCP tools)
- **design-system** - Design skill (UI, accessibility)
- **signal-vs-noise** - Philosophy skill (decision framework)
- **claude-md-guidelines** - Process skill (documentation guidelines)

---

## Resources

### Internal (Tier 3 Resources)
- `@resources/signal-vs-noise-reference.md` - Signal vs Noise philosophy (3-question filter, what to include/exclude)
- `@resources/why-over-how-reference.md` - Content quality philosophy (WHY > HOW, production context)
- `@resources/skill-structure-reference.md` - Standard structure and best practices (required sections, organization)
- `@resources/skills-guide.md` - Complete official guide to creating skills (moved from .claude/)
- `@resources/skill-template.md` - Copy-paste ready templates for all skill types
- `@resources/skill-ecosystem-reference.md` - Skill locations, sharing, permissions, and resources (where to put skills, how to distribute, access control)
- **Existing skills** - `.claude/skills/` directory for working examples

### External
- **Anthropic Best Practices** - https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
- **Skill Creation Guide** - https://support.claude.com/en/articles/12512198
- **Agent Skills Spec** - agentskills.io

---

## Key Principles

**Concise is key** - Context window is a public good. Every token counts.

**Signal vs Noise** - Only project-specific content. Skip what Claude knows.

**Third-person** - Describe WHEN to use, not HOW you help.

**WHY included** - Always explain rationale for decisions and patterns.

**One level deep** - SKILL.md → Tier 3 files (self-contained). No nesting.

**Scannable** - Use tables, bullets, headers. Quick lookup, not essays.

**Anti-patterns** - Document critical mistakes. "Here's what we tried that failed."

---

**Key Lesson:** The best skills are 150-300 lines, highly specific to the project, and document the weird parts and critical mistakes. If Claude already knows it, don't include it.
