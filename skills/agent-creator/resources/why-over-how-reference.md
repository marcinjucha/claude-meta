# Why Over How - Content Quality Philosophy

**Purpose:** Ensure agent documentation includes context and rationale, not just implementation details. Every agent decision needs WHY.

---

## Core Principle

**Priority:** WHY explanation > HOW implementation

Agent configuration syntax (HOW) is obvious to Claude. Context (WHY) is not.

**Without WHY:** Future developers don't understand importance → might change agent config → reintroduce bugs

**With WHY:** Agent becomes maintainable → developers understand consequences → configuration persists

---

## What is WHY for Agents?

**WHY includes:**

1. **Problem it solves** - What breaks without this agent configuration?
2. **Why approach chosen** - What alternatives were considered? Why rejected?
3. **Production impact** - Real incident, user complaint, measured numbers
4. **Consequences** - What happens if misconfigured? (crash, security issue, wrong data)

**WHY does NOT include:**

- Generic explanations (Claude knows)
- Syntax details (obvious)
- Architecture 101 (Claude knows)
- Time-sensitive info (version numbers, dates)

---

## Philosophy: Quality > Line Count

**Wrong approach:** Cut content to meet line count target

**Right approach:** Keep all critical WHY context, even if longer

**Example:**
- Complete WHY context for tool restrictions > brief config without explanation
- Signal-focused content matters more than brevity
- Line count is a guideline, not a constraint

---

## Agent Configuration Examples

### Example 1: Read-Only Tool Restrictions

**❌ Without WHY (HOW only):**
```yaml
---
name: code-reviewer
tools: Read, Grep, Glob, Bash
---
```

**What's missing:** Why these tools? Why not Write/Edit? What breaks if unrestricted?

---

**✅ With WHY (Context + Impact):**
```yaml
---
name: code-reviewer
description: Review code for quality and security. Use proactively after code changes.
tools: Read, Grep, Glob, Bash
disallowedTools: Write, Edit
model: sonnet
---

# Code Reviewer (Read-Only Analysis)

**Purpose:** Analyze code without risk of modifications during review

**Why read-only tools:**
- Review agent should NEVER modify code (safety requirement)
- Past incident: Agent with Write access accidentally fixed code during review
- Result: Review feedback inconsistent with actual committed code
- Solution: Explicit tool restrictions enforce read-only

**Why Bash included:**
- Need to run git diff (see what changed)
- Need to run linters (check code quality)
- Bash is read-only when used for these commands

**Why NOT Write/Edit:**
- Write/Edit tempts agent to "fix while reviewing"
- Reviews should document issues, not fix them
- Fixes should go through normal development workflow (with tests)

**Production impact - version X:**
- Before restrictions: Agent "helpfully" fixed issues during review
- Problem: Fixes not tested, caused regressions (2 production bugs)
- After restrictions: Agent reviews only, developer fixes with tests
- Result: 0 regressions from reviews

**Alternative considered:** Allow Write but prompt "Are you sure?"
**Why rejected:** Prompts add friction, don't prevent mistakes (user fatigue)
```

---

### Example 2: Permission Mode Selection

**❌ Without WHY (HOW only):**
```yaml
---
name: test-runner
permissionMode: acceptEdits
---
```

**What's missing:** Why acceptEdits? What happens with default? Why not bypass?

---

**✅ With WHY (Context + Impact):**
```yaml
---
name: test-runner
description: Run test suite and report failures
model: haiku
permissionMode: acceptEdits
---

# Test Runner (Auto-Accept Test Edits)

**Purpose:** Run tests quickly without permission prompts

**Why acceptEdits mode:**
- Tests may create temporary files (test fixtures, snapshots)
- Default mode prompts for each file → N prompts per test run
- acceptEdits auto-approves → no prompts, faster execution

**Why NOT bypassPermissions:**
- bypassPermissions skips ALL checks (too broad)
- acceptEdits only auto-approves edits (safer)
- Tests shouldn't need network/exec permissions

**Why NOT default:**
- Default mode prompts for every temporary file
- User experience: N interruptions during test run
- Feedback: "Too many prompts, can't use test runner"

**Production usage - feedback:**
- Before acceptEdits: Users abandoned test runner (too many prompts)
- After acceptEdits: Smooth experience, high adoption
- Safety: Still blocks network/exec (only edits auto-approved)

**Alternative considered:** Pre-approve specific paths only
**Why rejected:** Test framework creates unpredictable temp paths
```

---

### Example 3: Model Selection

**❌ Without WHY (HOW only):**
```yaml
---
name: log-analyzer
model: haiku
---
```

**What's missing:** Why Haiku? When is Sonnet better? Cost/speed trade-off?

---

**✅ With WHY (Context + Impact):**
```yaml
---
name: log-analyzer
description: Parse and summarize log files
model: haiku
tools: Read, Bash
---

# Log Analyzer (Haiku for Speed)

**Purpose:** Quick log analysis with minimal cost

**Why Haiku:**
- Log analysis is pattern matching (doesn't need deep reasoning)
- Haiku: 3-5s analysis, $0.XX per run
- Sonnet: 8-12s analysis, $0.YY per run (3× cost)
- Speed matters: Developers run this 10-20× per day

**When to use Sonnet instead:**
- Complex error correlation (multi-log synthesis)
- Root cause analysis (deep reasoning)
- Security incident investigation (need accuracy > speed)

**Performance testing:**
- Tested both models on 100 log files
- Haiku: 95% accuracy, 4s average
- Sonnet: 97% accuracy, 10s average
- Decision: 2% accuracy gain not worth 2.5× time + 3× cost

**Production metrics - month X:**
- Daily runs: N
- Haiku total cost: $X
- If Sonnet: $Y (3× higher)
- Accuracy issues: 0 (Haiku sufficient)

**Alternative considered:** Sonnet for all analysis
**Why rejected:** Cost and speed matter for high-frequency tool
```

---

### Example 4: Skill Preloading

**❌ Without WHY (HOW only):**
```yaml
---
name: api-developer
skills:
  - api-conventions
  - error-handling
---
```

**What's missing:** Why preload? Why these skills? Alternative?

---

**✅ With WHY (Context + Impact):**
```yaml
---
name: api-developer
description: Implement API endpoints following team conventions
skills:
  - api-conventions
  - error-handling-patterns
  - testing-strategy
model: sonnet
---

# API Developer (Preloaded Conventions)

**Purpose:** Implement APIs with immediate access to team patterns

**Why preload skills:**
- API patterns are 80% of implementation decisions
- Without preload: Agent must discover and load skills mid-task
- With preload: Patterns available from first action
- Performance: 2-3 fewer tool calls per implementation

**Why these specific skills:**
- api-conventions: REST patterns, naming, request/response structure
- error-handling-patterns: Standard error responses, validation
- testing-strategy: Test coverage requirements for APIs

**Why NOT preload more:**
- Database patterns: Only needed for data layer (not API layer)
- UI patterns: Not relevant for backend APIs
- Rule: Preload only what's needed 80% of the time

**Alternative considered:** Load skills on-demand during task
**Why rejected:**
- Agent must discover which skills exist (adds latency)
- Multiple skill loads interrupt workflow
- Preloading is one-time cost at agent start

**Production measurement:**
- Without preload: 5-8 tool calls for skill discovery
- With preload: 0 skill discovery calls (immediate access)
- Time saved: 3-5s per API implementation
- Developer feedback: "Much faster with preloaded patterns"
```

---

## When to Include WHY for Agents

**Always include WHY for:**

1. **Tool restrictions** - Why these tools? Why deny others?
2. **Permission modes** - Why this mode? What breaks with default?
3. **Model selection** - Why this model? Cost/speed trade-off?
4. **Skill preloading** - Why these skills? Why not others?
5. **Hook configuration** - Why this validation? What does it prevent?

**Example triggers:**
- "Why read-only tools for reviewer?"
- "Why acceptEdits for test runner?"
- "Why Haiku instead of Sonnet?"
- "Why preload api-conventions skill?"
- "Why validate SQL in hook?"

---

## Structure Template for Agent WHY

**Standard WHY structure for agent configuration:**

```yaml
---
name: [agent-name]
description: [When to delegate]
tools: [Tool list]
model: [model choice]
skills: [Preloaded skills]
---

# [Agent Name] ([Key Characteristic])

**Purpose:** [One sentence - what problem does agent solve?]

**Why [configuration choice]:**
- [Reason 1 - technical constraint]
- [Reason 2 - safety requirement]
- [Reason 3 - production requirement]

**Why NOT [alternative]:**
- [Why alternative A fails]
- [Why alternative B inadequate]

**Production impact:**
- Before configuration: [Symptom, numbers, user complaints]
- After configuration: [Improvement, metrics]
- Root cause: [Technical explanation]

**Alternative considered:** [Other approach]
**Why rejected:** [Reason]
```

---

## Anti-Pattern: Missing WHY in Agent Config

**Common mistake:** Agent configured without context

**Example:**
```yaml
❌ BAD (no WHY):
---
name: db-reader
tools: Bash
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate.sh"
---

✅ GOOD (includes WHY):
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

# Database Reader (SQL Validation Hook)

**Purpose:** Prevent write operations to production database

**Why validation hook:**
- Agent has Bash access (needed for running psql/mysql)
- Bash allows both SELECT and DELETE (risky)
- Can't restrict Bash to "read-only commands only"
- Solution: Hook validates SQL before execution

**Why PreToolUse (not PostToolUse):**
- PreToolUse blocks before execution → prevents damage
- PostToolUse runs after execution → damage already done
- Exit code 2 blocks the operation entirely

**Production incident - version X:**
- Agent accidentally ran DELETE during analysis
- Lost N rows of production data
- Root cause: No validation, agent "cleaned up" what it thought was test data
- Fix: Added validation hook to block write operations

**Hook validation logic:**
```bash
# Block: INSERT, UPDATE, DELETE, DROP, CREATE, ALTER
if contains_write_operation(command); then
  echo "Blocked: Only SELECT queries allowed" >&2
  exit 2  # Blocks the operation
fi
```

**Alternative considered:** Separate read-only DB user
**Why rejected:** Not available in all environments (legacy systems)
```

---

## Quick Checklist for Agent WHY

**Before finalizing agent, verify:**

- [ ] Tool restrictions include **Why these tools** (reason for allowlist/denylist)
- [ ] Permission mode includes **Why this mode** (what breaks with default)
- [ ] Model choice includes **Why this model** (cost/speed trade-off)
- [ ] Skill preloading includes **Why these skills** (what's needed 80% of time)
- [ ] Hooks include **Why validation needed** (what incident does it prevent)
- [ ] Production impact documented **with numbers** (cost, time, error rate)
- [ ] Alternatives documented with **Why rejected** (show thinking)

---

## Remember

**Signal = WHY-focused content for agents**
- Claude knows HOW to configure agents
- Claude doesn't know WHY your project chose specific configuration
- Production context is ALWAYS valuable (incidents, bugs, cost)
- Complete WHY context > brevity

**Quality First:**
- Complete agent explanation > brief config without context
- Better to include full WHY than cut for line count
- Every "Why not?" is valuable (shows alternatives considered)

**Future-proof:**
- Agent with WHY survives refactoring (devs understand importance)
- Agent without WHY gets misconfigured (seems arbitrary)
- Production context prevents regression (nobody wants to reintroduce bug)
