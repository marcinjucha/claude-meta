---
name: ai-skill-lifecycle
description: "Use when creating new skills OR maintaining/updating existing skills. Covers full skill lifecycle: creation (signal extraction, structure design, verification), maintenance (drift detection, pattern updates, anti-patterns), and advanced features (fork, scripts, dynamic injection, tool restrictions). Triggers on: 'create skill', 'update skill', 'fix skill', 'skill drift', 'add pattern'."
---

# Skill Lifecycle - Create, Maintain, Evolve

## Core Philosophy

**Content Quality > Line Count.** 500-line guideline is a target, not a hard limit. Better 600 lines of pure signal than 300 lines that omit critical information.

- Every line provides project-specific value
- No generic explanations Claude knows
- Critical mistakes documented with WHY
- Scannable structure (easy to find what you need)

**Trade-off:** Keep together if interconnected and needs context. Split to Tier 3 if modular and self-contained.

See `@../resources/signal-vs-noise-reference.md`, `@../resources/why-over-how-reference.md`.

---

## Creating New Skills

### Should You Create a Skill?

**3-question filter:**
1. **Project-specific?** (not generic framework patterns)
2. **Timeless?** (not "as of January 2025...")
3. **Helps make decisions?** (not "Framework X is a library for...")

**3/3 YES -> Create skill. 2/3 -> Consider. 1/3 -> Don't.**

### Skill vs Command vs Agent?

| Type | Purpose | When to Create |
|------|---------|----------------|
| **Skill** | Domain knowledge | Project-specific patterns, rules, decisions |
| **Command** | Workflow orchestration | Multi-phase processes with multiple agents |
| **Agent** | Specialized execution | Need specific tools, isolation, custom environment |

**Quick:** Reference patterns -> Skill. Orchestrate workflow -> Command. Execute specific task -> Agent.

*Also in ai-agent-creator -- keep decision consistent across both skills.*

### Step 1: Analyze Source Material

```yaml
Source: docs/CODE_PATTERNS.md (950 lines)

Extract to skills:
  - data-access-patterns:
      - Circular dependency bug (CRITICAL)
      - Caching strategy selection

Signal: 40% (project-specific)
Noise: 60% (generic framework patterns)
Result: Create 2 skills, keep only signal
```

**Red flags (don't extract):** Generic explanations, basic syntax, framework docs, common patterns Claude knows.

**Extract:** Critical mistakes, project decisions with WHY, architecture rules, access control rules.

### Step 2: Design Skill Structure

```yaml
SKILL.md (Tier 2): Aim for ~500 lines (quality > count)
  - Core principles (what, when, why)
  - Quick reference tables
  - Anti-patterns (critical mistakes)

Tier 3 files: Optional, self-contained detailed examples
```

**Keep in SKILL.md** if interconnected. **Split to Tier 3** if modular. Typical range: 150-600 lines.

### Step 3: Write SKILL.md

**Frontmatter fields:**
- `name` + `description` -- **CRITICAL for agent discovery.** Agents see ONLY frontmatter description during lazy loading. Without it, skill is invisible and never gets loaded. Description must contain keyword triggers.
- `disable-model-invocation: true` (manual-only skills)
- `context: fork` + `agent` (isolated subagent execution)

### Step 4: Create Supporting Files (Optional)

Move detailed examples (>50 lines), focused guides, or utility scripts to separate files.

### Step 5: Update Agent/Command References

Add to relevant agent `skills:` field and command references.

### Step 6: Verify Quality

See **Verification Checklist** at end of this skill.

---

## Maintaining Existing Skills

### What to Update (Signal vs Noise Filter)

**SIGNAL (Update immediately):**
- Pattern changed (code differs from skill)
- Production bug not documented
- Missing WHY (rule without context/rationale)
- File paths wrong (refactoring moved files)
- Numbers/thresholds changed

**NOISE (Skip update):**
- Cosmetic improvements (rewording without new information)
- Adding generic explanations (Claude knows)
- Obvious clarifications (already clear)
- Time-sensitive info (version numbers, dates)

### Pattern 1: Detecting Skill Drift

```yaml
symptoms:
  outdated_pattern:
    - Agent generates code that doesn't match current implementation
    - File paths in skill don't exist
    - Code examples don't compile

  imprecise_instructions:
    - Agent asks clarifying questions about skill content
    - Multiple valid interpretations
    - Vague "should" without clear WHEN

  missing_anti_patterns:
    - Production bug not in any skill
    - Same mistake made twice

  skill_gaps:
    - Agent can't find pattern for known solution
    - Pattern exists but in wrong skill
```

**How to detect:** Code review (implementation differs), agent confusion (asks clarification), production incident (bug not prevented), refactoring (code changed, skill not updated).

### Pattern 2: Updating Outdated Patterns

**When:** Code implementation changed, skill describes old approach.

Update: code examples, file paths, thresholds/numbers, WHY context.

**Add migration note for breaking changes:**
```markdown
## Pattern Migration
**Changed in:** [Date or Version]
**Old pattern:** [Brief description]
**New pattern:** [Brief description]
**Why changed:** [Production reason]
```

**Verify:** Copy code example to IDE, confirm it compiles against current codebase.

### Pattern 3: Clarifying Imprecise Instructions

**When:** Skill instructions vague, causing agent confusion.

**Fix:** Replace vague terms with specific criteria:

```markdown
BAD:  "Use appropriate threshold"
GOOD: "Validation threshold:
       - Small items (< Xcm): 25-30%
       - Standard (Y-Zcm): 35% (default)
       - Large (> Ncm): 35-40%"

BAD:  "Should use Service for complex logic"
GOOD: "Use Service when:
       - Combining 3+ repositories (prevents cycles)
       NOT when:
       - Thin delegation (Use Case)
       - Single repository (Repository)"
```

### Pattern 4: Adding Missing Anti-Patterns

**When:** Production bug happened, not documented in skill.

```markdown
### Mistake N: [Descriptive Name]
**Problem:** [What breaks, production impact]
**Why bad:** [Root cause]
**Fix:** [What to do instead]
**Production incident:** [When this happened]
```

### Pattern 5: Reorganizing Skill Structure

**When:** Skill grew too large (>1000 lines), hard to navigate.

**Action:**
- Multiple distinct domains -> Split into separate skills (400-600 lines each)
- Single domain -> Reorganize with standard structure
- Duplicate patterns -> Keep in one location, cross-reference

---

## Mental Model Anti-Patterns

**When:** Production bug reveals systematic thinking error (not just implementation mistake).

**Signal test:**
- Did 2+ developers make SAME mistake independently? -> Mental model error
- Does mistake "feel natural but is wrong"? -> Mental model error
- Was bug repeated after fix (thinking not updated)? -> Mental model error
- NO to all -> Regular anti-pattern

**Why mental models are signal:** Prevent systematic errors. One mental model fix = prevents N future bugs. Higher ROI than documenting single bug.

**Template:**
```markdown
### Mental Model N: [Descriptive Name]

**Incorrect mental model:** "[One sentence quote of wrong thinking]"

**Why this thinking fails:**
- [Cognitive bias / natural assumption]
- [Context that misleads]

**Correct mental model:** "[One sentence quote of correct thinking]"

**Production impact:** [How many bugs / developer efficiency]
```

**Focus:** WHY mistake happens (thinking shift), not HOW to fix (code). Skip code examples in mental model sections.

---

## Advanced Features

### 6.1 context: fork (Isolated Execution)

**When to use:** Research task, analysis task, verbose output, task has complete prompt (not just guidelines).

**When NOT to use:** Reference material, needs conversation context, just provides knowledge.

**Why fork matters:** Research skills without fork consume main context with verbose output, degrading subsequent response quality.

**Key decision:** YES if: (1) Complete task with steps, (2) Don't need conversation context, (3) Verbose output expected. NO if: Guidelines only OR needs main context OR interactive task.

```yaml
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

### 6.2 Script Integration

**When to use:** Generate visual output, process complex data, reusable analysis.

**Key pattern:**
1. Create `~/.claude/skills/my-skill/scripts/script.py`
2. Use absolute path: `python ~/.claude/skills/my-skill/scripts/script.py`
3. Script prints output file location
4. Add `allowed-tools: Bash(python *)` to frontmatter

### 6.3 Dynamic Context Injection

**When to use:** Fetch live PR/issue data, include current git status, inject file contents.

**Syntax:** `\! `command`` (backslash + exclamation + space + backtick + command + backtick)

Commands execute BEFORE skill sent to Claude. Output replaces placeholder.

```yaml
---
name: pr-analysis
context: fork
agent: Explore
---
## Pull request context
\! `gh pr diff`
\! `gh pr view --comments`

## Task
Analyze this PR for quality and breaking changes.
```

### 6.4 Tool Restrictions

**Key concept:** `allowed-tools` restricts FURTHER than user permissions (cannot grant, only limit).

```yaml
allowed-tools: Read, Grep, Glob              # Read-only
allowed-tools: Read, Bash(git *)             # Git operations only
allowed-tools: Read, Bash(gh *)              # GitHub operations only
```

### 6.5 String Substitutions

**When to use:** Skill accepts arguments (issue numbers, file paths, search patterns).

**Available:** `$ARGUMENTS` (all), `$0`/`$1` (individual), `${CLAUDE_SESSION_ID}` (session ID).

Add `argument-hint: [arg-name]` to frontmatter.

**Complete implementation guide:** See `@resources/advanced-features.md` for step-by-step details, code examples, edge cases, and troubleshooting.

---

## Decision Trees

### Should I Update Skill or Create New One?

```
Pattern is variation of existing? -> Update existing skill
Pattern is completely new domain? -> Create new skill
Existing skill too large (> 1000 lines)? -> Split into multiple skills
Pattern used by 2+ features? -> Add to skill (not CLAUDE.md)
Pattern feature-specific? -> Keep in CLAUDE.md (not skill)
```

### Which Skill Section Needs Update?

```
Pattern implementation changed? -> Update "Core Patterns" section
New anti-pattern discovered? -> Add to "Anti-Patterns" section
File moved? -> Update file paths
Numbers/thresholds changed? -> Update "Quick Reference" + relevant patterns
Need isolation? -> Add frontmatter: context: fork, agent: [type]
Need live data? -> Add dynamic injection
Need script execution? -> Add scripts/ directory
Need tool restrictions? -> Add allowed-tools
Need arguments? -> Add argument-hint + $ARGUMENTS
```

### How Much to Change?

```
Minor update (file path, number)? -> Update inline, no migration note
Pattern tweak (same approach)? -> Update pattern, mention in description
Breaking change (new approach)? -> Update pattern + "Pattern Migration" note
Complete replacement? -> Keep old in "Deprecated Patterns", add new
```

---

## Troubleshooting

**Claude doesn't see all skills:** Descriptions exceed budget -> Run `/context` to check -> Increase `SLASH_COMMAND_TOOL_CHAR_BUDGET` or shorten descriptions

**Forked skill returns nothing:** Guidelines without task -> `context: fork` needs explicit instructions ("do X, output Y"), not reference material

---

## Verification Checklist

### Structure
- [ ] Directory: `.claude/skills/skill-name/`
- [ ] SKILL.md with YAML frontmatter
- [ ] Tier 3 files self-contained (if needed)
- [ ] No nested references (one level deep only)

### Metadata
- [ ] Name: lowercase, hyphens, max 64 chars
- [ ] **Description: MUST exist** -- without it, skill is invisible to agents (lazy loading)
- [ ] Description: third-person, <1024 chars, WHEN to use with keyword triggers
- [ ] No XML tags in description
- [ ] Domain-specific name (not generic)

### Content Quality (Signal > Brevity)
- [ ] Signal-focused (only project-specific)
- [ ] No generic explanations Claude knows
- [ ] WHY included for all decisions/rules
- [ ] Anti-patterns documented (critical mistakes)
- [ ] Complete (all critical information included)
- [ ] Scannable format (tables, bullets, headers)
- [ ] Line count: Aim ~500, accept more if quality demands it

### Integration
- [ ] Added to relevant agent `skills:` field
- [ ] Referenced in commands (if applicable)
- [ ] Tested invocation

### Self-Check Questions
- [ ] Is this obvious to Claude without the skill? -> If YES, remove (noise)
- [ ] Is this project-specific? -> If NO, remove (generic)
- [ ] Would this help future me with amnesia? -> If NO, remove
- [ ] Does every section provide actionable information? -> If NO, refactor
- [ ] Did I cut content to meet line count? -> If YES, restore (quality > count)

---

## Quick Start

```bash
mkdir -p .claude/skills/my-skill-name
cp .claude/skills/ai-skill-lifecycle/resources/skill-template.md .claude/skills/my-skill-name/SKILL.md
# Edit: frontmatter, sections, verify quality
```

---

## Resources

**Shared resources** (`@../resources/`):
- `@../resources/signal-vs-noise-reference.md` - 3-question filter philosophy
- `@../resources/why-over-how-reference.md` - WHY > HOW philosophy
- `@../resources/skill-structure-reference.md` - Standard structure and best practices
- `@../resources/skill-ecosystem-reference.md` - Skill locations, sharing, permissions

**Skill-specific resources** (`@resources/`):
- `@resources/skills-guide.md` - Complete official guide to creating skills
- `@resources/skill-template.md` - Copy-paste ready templates for all skill types
- `@resources/advanced-features.md` - Complete guide: context: fork, dynamic injection, tool restrictions, scripts, string substitutions (merged from forked-execution.md)
