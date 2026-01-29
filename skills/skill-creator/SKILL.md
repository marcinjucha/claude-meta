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

### Signal vs Noise: The 3-Question Filter

Before including ANY content in a skill, ask:

1. **Actionable?** Can Claude/user act on this?
2. **Impactful?** Would lack of this cause problems?
3. **Non-obvious?** Is this insight non-trivial?

**If ANY answer is NO → It's NOISE → Cut it.**

**SIGNAL (keep):**
- Project-specific patterns with WHY explanation
- Critical crashes/bugs prevention
- Real mistakes made with fixes
- Non-obvious decisions with context

**NOISE (cut):**
- Generic patterns Claude knows (frameworks, architectures)
- HOW explanations without WHY context
- Standard syntax examples
- Architecture 101 explanations

**Example:**
- ✅ SIGNAL: "Never query same table in RLS policy → causes infinite recursion → crashed prod"
- ❌ NOISE: "Data access layer handles persistence" (Claude knows)

See `@resources/signal-vs-noise-reference.md` for extended examples (optional deep-dive).

### WHY Over HOW Principle

**Priority:** WHY explanation > HOW implementation

Code syntax (HOW) is obvious to Claude. Context (WHY) is not.

**Every pattern needs:**
- **Problem it solves** - What breaks without this pattern?
- **Why approach chosen** - What alternatives considered, why rejected?
- **Production impact** - Real incident, numbers, user complaints
- **Consequences** - What happens if violated?

**Example:**
```markdown
❌ Without WHY: "Use weak references instead of strong references"

✅ With WHY:
**Purpose:** Prevent retain cycles in subscription chains
**Why weak:** Strong capture creates cycle → memory leak (NMB per session)
**Production impact:** Lower-end devices ran out of memory after N minutes
**Alternative considered:** Manual weak capture → Why rejected: Easy to forget
```

See `@resources/why-over-how-reference.md` for complete philosophy (optional deep-dive).

### Standard Skill Structure

**Required sections (in order):**
1. **Purpose** (1-2 sentences: what problem solved)
2. **When to Use** (bulleted triggers)
3. **Core Patterns** (3-5 patterns with WHY)
4. **Anti-Patterns** (production context for each)
5. **Quick Reference** (scannable summary)

**Optional sections:** Decision Trees, Parameter Tuning, Integration, Examples

See `@resources/skill-structure-reference.md` for detailed guidelines (optional deep-dive).

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

**Frontmatter fields** (see official docs for complete reference):
- `name` + `description` (basic identification)
- `disable-model-invocation: true` (manual-only skills like /deploy)
- `context: fork` + `agent` (isolated subagent execution)

**Writing tips:**
- Signal-focused: Every line passes 3-question filter
- Quality > brevity: 600 lines of pure signal > 300 lines with 50% noise
- WHY included: Explain purpose, rationale, production impact

### Step 4: Create Supporting Files (Optional)
Move detailed examples (>50 lines), comprehensive guides, or utility scripts to separate files.

### Step 4a: Advanced Frontmatter Patterns (Optional)

**context: fork** - Use when:
- Task has complete prompt (not just guidelines)
- Agent doesn't need conversation context
- Output is verbose (research, analysis)

**Dynamic injection** - Use when:
- Need current file content, user input, or environment variables
- Pattern: `{{{ user_message }}}`, `{{{ active_file_contents }}}`

**Tool restrictions** - Use when:
- Prevent dangerous operations (Write during review)
- Force read-only access (security audits)

See official docs and `@resources/forked-execution.md` for implementation details.

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

## Skill Types (This Project)

**Type 1: Technical Patterns** - Database, code patterns with critical bugs and architecture constraints
**Type 2: Architectural Decisions** - Structure decisions with import rules and boundaries
**Type 3: Process & Philosophy** - Decision frameworks and quality criteria
**Type 4: Integration & Tools** - API patterns with critical gotchas

---

## Anti-Patterns (Common Mistakes)

### ❌ Too Much Noise (Generic Content)

**Problem:** SKILL.md is 1,200 lines but 70% is generic explanations.

**Production example:** `ui-patterns` skill was 800 lines, Claude took 12s to load it. 600 lines explained React hooks (generic), only 200 lines project-specific.

**Fix:**
1. Remove generic explanations Claude knows
2. Keep project-specific content even if longer
3. Quality matters more than line count

**Result:** Removed generic React explanation → 200 lines → 2s load time (83% faster). Claude hit rate improved 40% (more skills fit in budget).

**Key insight:** 600 lines of pure signal > 300 lines with 50% noise

### ❌ Generic Content (Not Project-Specific)

**Problem:** Skill explains React basics Claude already knows.

**Production example:** Skill with "What is a repository?" never used because Claude already knows. Wasted 300 lines of token budget.

**Fix:** Only include project-specific decisions and critical mistakes.

**Self-check:** "Would Claude know this without the skill?"
- YES → Remove it (noise)
- NO → Keep it (signal)

### ❌ First-Person Description

**Problem:** First-person descriptions confuse skill routing.

**Production example:** `database-helper` skill with "I help you debug" never auto-triggered (0% invocation rate).

**Root cause:** Description doesn't contain trigger keywords Claude looks for.

**Fix:** Changed to "Use when debugging data access, RLS policies, or caching issues" → 35% invocation rate.

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
- `@resources/forked-execution.md` - Advanced pattern: skills with `context: fork` for isolated subagent execution
- **Existing skills** - `.claude/skills/` directory for working examples

### External
- **Anthropic Best Practices** - https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
- **Skill Creation Guide** - https://support.claude.com/en/articles/12512198
- **Agent Skills Spec** - agentskills.io

---

## Quick Reference

**Decision Framework:**
- Need patterns? → Skill
- Need workflow? → Command
- Need execution? → Agent

**Signal vs Noise Filter:**
- Actionable? Impactful? Non-obvious? → If ANY NO = NOISE

**Creating Skills:**
1. Extract signal (project-specific only)
2. Design structure (self-contained, ~500-600 lines)
3. Write SKILL.md (WHY included, anti-patterns)
4. Verify (checklist above)

**Anti-Pattern Checklist:**
- [ ] No generic content (Claude knows)
- [ ] WHY included for all decisions
- [ ] Production context for anti-patterns
- [ ] Self-contained (no required resources)
- [ ] Signal-focused (3-question filter applied)

**Key Principles:**
- **Signal vs Noise** - Only project-specific content. Skip what Claude knows.
- **WHY included** - Always explain rationale for decisions and patterns.
- **Third-person** - Describe WHEN to use, not HOW you help.
- **One level deep** - SKILL.md → Tier 3 files (self-contained). No nesting.
- **Scannable** - Use tables, bullets, headers. Quick lookup, not essays.
- **Anti-patterns** - Document critical mistakes. "Here's what we tried that failed."

---

**Key Lesson:** The best skills are 150-300 lines, highly specific to the project, and document the weird parts and critical mistakes. If Claude already knows it, don't include it.
