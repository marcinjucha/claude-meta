---
name: skill-fine-tuning
description: Maintain and update existing Agent Skills. Use when: skill references outdated pattern or wrong file paths after refactoring, skill instructions cause agent confusion, production bug reveals missing documentation, or skill needs advanced features (context: fork, dynamic injection, tool restrictions, arguments).
---

# Skill Fine-Tuning

## Decision Framework: What to Update

Before updating a skill, apply Signal vs Noise filter:

**SIGNAL (Update immediately):**
- Pattern changed (code implementation differs from skill)
- Production bug not documented (happened, not in anti-patterns)
- Missing WHY (rule stated without context/rationale)
- File paths wrong (refactoring moved files)
- Numbers/thresholds changed (configuration adjusted)

**NOISE (Skip update):**
- Cosmetic improvements (rewording without new information)
- Adding generic explanations (Claude knows)
- Obvious clarifications (already clear to reader)
- Time-sensitive info (version numbers, dates)

**See:** `@../resources/signal-vs-noise-reference.md` for complete 3-question filter and detailed examples.


## Core Patterns

### Pattern 1: Detecting Skill Drift

**Signs skill needs update:**

```yaml
symptoms:
  outdated_pattern:
    - Agent generates code that doesn't match current implementation
    - File paths in skill don't exist
    - Code examples don't compile
    - Thresholds/numbers wrong (configuration changed)

  imprecise_instructions:
    - Agent asks clarifying questions about skill content
    - Multiple valid interpretations
    - Missing decision criteria
    - Vague "should" without clear WHEN

  missing_anti_patterns:
    - Production bug not in any skill
    - Same mistake made twice (no documentation first time)
    - Common pitfall not warned against

  skill_gaps:
    - Agent can't find pattern for known solution
    - Pattern exists but in wrong skill (hard to find)
    - Integration between skills missing
```

**How to detect:**
1. **Code review:** Implementation differs from skill pattern
2. **Agent confusion:** Claude asks for clarification despite skill existing
3. **Production incident:** Bug happens, skill didn't prevent it
4. **Refactoring:** Code changed, skill not updated

### Pattern 2: Updating Outdated Patterns

**When:** Code implementation changed, skill still describes old approach

**What to update:**
- Code examples (match current implementation)
- File paths (if moved during refactoring)
- Thresholds/numbers (if configuration changed)
- WHY context (if rationale changed)

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

**When:** Skill instructions vague, causing agent confusion

**Production impact:** Vague "use appropriate threshold" → developers chose different values → inconsistent behavior → bug reports.

**Fix:** Replace vague terms with specific criteria:

```markdown
❌ VAGUE: "Use appropriate threshold"
✅ SPECIFIC:
"Validation threshold:
- Small items (< Xcm): 25-30%
- Standard (Y-Zcm): 35% (default)
- Large (> Ncm): 35-40%"

❌ VAGUE: "Should use Service for complex logic"
✅ SPECIFIC:
"Use Service when:
- Combining 3+ repositories (prevents cycles)
- OR complex algorithm
NOT when:
- Thin delegation (Use Case)
- Single repository (Repository)"
```

**Make scannable with triggers:**
```markdown
## When to Use
- API returns nil → Check auth state
- Data jittery → Apply deduplication
- Multiple results → Use ranking
```

### Pattern 4: Adding Missing Anti-Patterns

**When:** Production bug happened, not documented in skill

**Structure:**
```markdown
### ❌ Mistake N: [Descriptive Name]
**Problem:** [What breaks, production impact]
**Why bad:** [Root cause]
**Fix:** [What to do instead]
**Production incident:** [When this happened]
```

**Add to:**
- Common mistake → "Anti-Patterns (Critical Mistakes)" section
- Subtle issue → Note in relevant "Pattern" section
- Blocking issue → "When to Use" triggers

### Pattern 5: Reorganizing Skill Structure

**When:** Skill grew too large (>1000 lines), hard to navigate

**Why 1000 lines threshold:**

Skills >1000 lines are harder to navigate and take longer to find patterns.

**Note:** Content quality > line count. After split, each skill should be 400-600 lines of pure signal, not reduced for brevity.

**Action:**
- Multiple distinct domains → Split into separate skills (400-600 lines each)
- Single domain → Reorganize with standard structure
- Duplicate patterns → Keep in one location, cross-reference from others

### Pattern 6: Adding Advanced Features (Frontmatter, Scripts, Execution)

**When:** Skill needs isolation, script execution, tool restrictions, or dynamic context

#### 6.1 Adding context: fork (Isolated Execution)

**When to use:**
- Research task (codebase exploration) → fork
- Analysis task (focused examination) → fork
- Verbose output (keeps main context clean) → fork
- Task has complete prompt (not just guidelines) → fork

**When NOT to use:**
- Skill is reference material (guidelines, patterns)
- Needs conversation context
- Just provides knowledge (not actionable task)

**Why fork matters:**
Research skills without fork can consume significant main context with verbose output, degrading subsequent response quality. Forked research skills isolate output, keeping main context clean.

**Key decision:**
- YES if: (1) Complete task with steps, (2) Don't need conversation context, (3) Verbose output expected
- NO if: Guidelines only OR needs main context OR interactive task

**Minimal example:**
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

#### 6.2 Adding Script Integration

**When to use:**
- Generate visual output (charts, graphs, HTML reports)
- Process data with complex logic (easier in Python than bash)
- Reusable analysis that's separate from skill prompt

**Key pattern:**
1. Create `~/.claude/skills/my-skill/scripts/script.py`
2. Use absolute path in skill: `python ~/.claude/skills/my-skill/scripts/script.py`
3. Script prints output file location for Claude to find
4. Add `allowed-tools: Bash(python *)` to frontmatter

**Minimal example:**
```markdown
---
name: visualizer
allowed-tools: Bash(python *)
---
Generate visualization:

```bash
python ~/.claude/skills/visualizer/scripts/visualize.py .
```

Creates `output.html` with interactive visualization.
```

#### 6.3 Adding Dynamic Context Injection

**When to use:**
- Fetch live PR/issue data (changes frequently)
- Include current git status before analysis
- Inject file contents for context
- Any data that must be fresh at invocation time

**Syntax:** `\! `command`` (backslash + exclamation + space + backtick + command + backtick)

**How it works:**
Commands execute BEFORE skill sent to Claude → output replaces placeholder → Claude sees fully-rendered prompt with actual data.

**Minimal example:**
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

#### 6.4 Adding Tool Restrictions

**When to use:**
- Skill should be read-only (prevent accidental writes)
- Limit to specific bash commands (e.g., only git, only gh)
- Safety constraint for forked execution

**Key concept:**
`allowed-tools` restricts FURTHER than user permissions (cannot grant new permissions, only limit existing ones).

**Common patterns:**
```yaml
allowed-tools: Read, Grep, Glob              # Read-only
allowed-tools: Read, Bash(git *)             # Git operations only
allowed-tools: Read, Bash(gh *)              # GitHub operations only
allowed-tools: Read, Edit, Write, Bash       # Full access (default)
```

**Document restriction in skill:**
```markdown
## Tool Access
This skill limits Claude to read-only operations: Read, Grep, Glob
```

#### 6.5 Adding String Substitutions

**When to use:**
- Skill accepts arguments (issue numbers, file paths, search patterns)
- Need session-specific identifiers

**Available substitutions:**
- `$ARGUMENTS` - All arguments as string
- `$0` or `$ARGUMENTS[0]` - First argument
- `$1` or `$ARGUMENTS[1]` - Second argument
- `${CLAUDE_SESSION_ID}` - Current session ID

**Minimal example:**
```yaml
---
name: fix-issue
argument-hint: [issue-number]
---
Fix GitHub issue $ARGUMENTS:

```bash
gh issue view $ARGUMENTS
git checkout -b fix-$ARGUMENTS
```

Reference issue in commit message.
```

**Complete implementation guide:** See `@resources/advanced-features.md` for:
- Step-by-step implementation details
- Complete code examples with error handling
- Edge cases and troubleshooting
- Advanced patterns combining multiple features

### Pattern 7: Adding Mental Model Anti-Patterns (After Systematic Bugs)

**When:** Production bug reveals systematic thinking error, not just implementation mistake

**Signal test: "Is this a mental model error?"**

```
Ask:
├─ Did 2+ developers make SAME mistake independently?
│   └─ YES → Mental model error
├─ Does mistake "feel natural but is wrong"?
│   └─ YES → Mental model error
├─ Was bug repeated after fix (thinking not updated)?
│   └─ YES → Mental model error
└─ NO to all → Regular anti-pattern (not mental model)
```

**Why mental models are signal:**
- Prevent systematic errors (not one-off bugs)
- One mental model fix = prevents N future bugs
- Reveals WHY mistake happens (cognitive bias, incorrect assumption)
- Higher ROI than documenting single bug

**Process:**

```markdown
Step 1: Identify Mental Model Error

After production bug, ask:
- What incorrect thinking led to this?
- Why did developer assume X when Y is correct?
- What natural intuition failed here?

Example: Framework tests (3 developers same mistake)
- Symptom: Manual action after automatic action
- Incorrect thinking: "I sent action → I handle it"
- Correct thinking: "Framework sent action → I receive it"
- Mental model: **Synchronous thinking in async world**

Step 2: Document WHY, Not WHAT

Focus on thinking shift, not mechanical fix:

\`\`\`markdown
### ❌ Mental Model N: [Descriptive Name]

**Incorrect mental model:**
"[One sentence quote of wrong thinking]"

**Why this thinking fails:**
- [Cognitive bias / natural assumption]
- [Context that misleads]

**Correct mental model:**
"[One sentence quote of correct thinking]"

**Production impact:**
[How many bugs / developer efficiency]
\`\`\`

Step 3: Skip Code Examples

Mental model section = WHY (thinking)
Regular anti-pattern = WHAT + HOW (code)

Keep mental models focused on cognitive shift.

Step 4: Add to Appropriate Section

Options:
1. New section: "Anti-Patterns: Common Mental Models That Fail"
   - Use when 3+ mental model errors identified
   - Example: `error-patterns` (6 mental models)

2. Within existing anti-pattern:
   - Add "Why this thinking fails" subsection
   - Explain cognitive bias behind mistake

3. Cross-reference:
   - If mental model documented in another skill
   - Link from regular anti-pattern
```

**Example: Before vs After**

**BEFORE (regular anti-pattern):**
```markdown
### ❌ Mistake: Stub Between Actions

**Problem:** Test stub set after action sent
**Fix:** Set stub before action
```

**AFTER (mental model added):**
```markdown
### ❌ Mental Model: Reactive Setup Instead of Proactive

**Incorrect mental model:**
"Action executes → I quickly stub result"

**Why this thinking fails:**
- Reactive mindset: "I respond to what happens"
- Framework actions execute immediately - no time for reactive setup
- Async world requires proactive thinking

**Correct mental model:**
"Prepare ALL stubs BEFORE flow starts"

**Production impact:**
- 3 developers made same mistake independently
- Would prevent if mental model documented
```

## Decision Trees

### Should I Update Skill or Create New One?

```
Pattern is variation of existing? → Update existing skill
Pattern is completely new domain? → Create new skill
Existing skill too large (> 1000 lines)? → Split into multiple skills
Pattern used by 2+ features? → Add to skill (not CLAUDE.md)
Pattern feature-specific? → Keep in CLAUDE.md (not skill)
```

### Which Skill Section Needs Update?

```
Pattern implementation changed? → Update "Core Patterns" section
New anti-pattern discovered? → Add to "Anti-Patterns" section
File moved? → Update "Real Project Example" file paths
Numbers/thresholds changed? → Update "Quick Reference" + relevant patterns
Integration changed? → Update "Integration with Other Skills"
Need isolation? → Add frontmatter: context: fork, agent: [type]
Need live data? → Add dynamic injection (exclamation + backtick syntax)
Need script execution? → Add scripts/ directory + reference in SKILL.md
Need tool restrictions? → Add frontmatter: allowed-tools: [list]
Need arguments? → Add frontmatter: argument-hint, use $ARGUMENTS in body
```

### Should I Add Advanced Features?

```
Skill runs research/analysis without conversation context? → Add context: fork
Skill needs live PR/git data? → Add dynamic injection (! + backtick + command)
Skill generates visual output? → Add script integration (scripts/ dir)
Skill should limit tool access? → Add allowed-tools
Skill takes arguments? → Add argument-hint + $ARGUMENTS
Skill only for manual use? → Add disable-model-invocation: true
Skill is background knowledge? → Add user-invocable: false
```

### How Much to Change?

```
Minor update (file path, number)? → Update inline, no migration note
Pattern tweak (same approach)? → Update pattern, mention in description
Breaking change (new approach)? → Update pattern + add "Pattern Migration" note
Complete replacement? → Keep old in "Deprecated Patterns", add new
```

## Resources

**Shared resources** (`@../resources/`):
- `@../resources/signal-vs-noise-reference.md` - 3-question filter for deciding what to update
- `@../resources/why-over-how-reference.md` - WHY > HOW philosophy

**Skill-specific resources** (`@resources/`):
- `@resources/advanced-features.md` - Complete guide: context: fork, dynamic injection, tool restrictions
