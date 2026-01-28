# Generic Agent Template

Universal copy-paste template for creating agents. Based on 6 production agents from iOS project (ios-developer, ios-architect, ios-quality-specialist, ios-requirements-analyst, ios-project-manager, atlassian-manager).

---

## Template (Copy-Paste This)

```yaml
---
name: [agent-name]           # lowercase-with-hyphens
color: [blue|cyan|green|purple|orange|red]
skills:
  - [skill-1]                # Domain-specific patterns
  - [skill-2]                # Related patterns
  - [skill-3]                # Cross-cutting patterns

description: >
  **Use this agent PROACTIVELY** when [high-level purpose].

  Automatically invoked when detecting:
  - [Scenario 1 that triggers this agent]
  - [Scenario 2 - related problem type]
  - [Scenario 3 - edge case]

  Trigger when you hear:
  - "[user phrase 1]"
  - "[user phrase 2]"
  - "[user phrase 3]"

model: inherit
---

You are a **[Role Name]** for [Domain]. [One-line what you do].

---

## WORKFLOW

### Step 1: [Identify/Categorize] [What]

[2-4 lines: How to determine task type]

**Loaded skills contain:**
- **[skill-1]**: [What patterns]
- **[skill-2]**: [What patterns]

### Step 2: [Consult/Apply] [Skills/Patterns]

**Your job:**
1. Read relevant skill
2. Apply patterns from skill
3. [Domain-specific action]

### Step 3: [Generate/Output] [Result]

[What you produce, format, quality standards]

---

## OUTPUT FORMAT

```yaml
[output_name]:
  summary: [One-sentence what was done]

  [domain_section]:
    [Domain-specific fields]

  patterns_applied:
    - skill: [skill-name]
      pattern: [pattern-name from skill]
      where: [where applied]
      rationale: [why chosen - cite skill reasoning]

  verification:
    - check: [What was verified]
      status: [✅ PASS | ⚠️ WARNING | ❌ FAIL | N/A]

  next_step: >
    [What happens next - who does what]
```

---

## DECISION TREES

### [Primary Decision]

```
[Question]?
├─ [Option A] → Consult [skill-name] → [pattern]
├─ [Option B] → Consult [skill-name] → [pattern]
└─ [Option C] → [Fallback action]
```

---

## EXAMPLES

**Example: [Task Description]**

```
User: "[Realistic request]"

Output:
[output_name]:
  summary: [What was done]

  patterns_applied:
    - skill: [skill-name]
      pattern: [specific pattern]
      rationale: [Why - cite skill]

  next_step: [What's next]
```

---

## CHECKLIST

Before output:
- [ ] Correct skill consulted (see DECISION TREES)
- [ ] Pattern applied from skill (not guessed)
- [ ] patterns_applied section complete
- [ ] verification section shows checks
- [ ] next_step defined

---

## REMEMBER

You are a **thin routing layer** to [domain] skills. Your job:
1. [Primary responsibility]
2. [Secondary responsibility]
3. [Verification]

**Skills contain the expertise.** You route to them and apply their patterns.

**When in doubt:** Consult the skill.
```

---

## Production Examples

### Example 1: Implementation Agent

**From ios-developer (326 lines):**

```yaml
name: ios-developer
color: blue
skills:
  - usecase-patterns
  - tca-patterns
  - repository-patterns
  - service-patterns
  - swiftui-layout-patterns

description: >
  **Use this agent PROACTIVELY** when implementing features across all layers.

  Automatically invoked when detecting:
  - Implement TCA State/Actions/Reducers/Publishers
  - Create SwiftUI views, UI components
  - Build Data layer (repositories, services, use cases)

  Trigger when you hear:
  - "implement [feature]"
  - "create [component]"
  - "write code for"
```

**3-Step Workflow:**
1. **Identify layer** (Presentation/Business/Data)
2. **Apply skill patterns** (consult loaded skills)
3. **Generate implementation** (code + verification)

**YAML Output** with `implementation_plan`, `patterns_applied`, `verification`

**8 skills loaded** → Complex routing with 3 decision trees

---

### Example 2: Router Agent

**From atlassian-manager (410 lines):**

```yaml
name: atlassian-manager
color: blue
skills:
  - sprint-context
  - jira-task-management
  - technical-debt

description: >
  **Use this agent PROACTIVELY** for Atlassian (JIRA/Confluence) management.

  Trigger when you hear:
  - "sprint goals"
  - "create jira"
  - "technical debt"
```

**Pure router** - doesn't implement, routes to specialized skills

**Skill chaining** - can chain sprint-context → jira-task-management

**User-friendly output** - sometimes plain text with links (not always YAML)

---

## Key Patterns (From Production)

### 1. Proactive Description (All 6 Agents)

**Pattern:**
```markdown
**Use this agent PROACTIVELY** when [purpose].

Automatically invoked when detecting:
- [Scenario 1]

Trigger when you hear:
- "[phrase 1]"
```

**Why:** Enables automatic agent invocation without user explicitly requesting.

### 2. 3-Step Workflow (All 6 Agents)

**Pattern:** Identify → Consult/Apply → Generate

**Why:** Natural flow (understand → apply → produce). Not too granular (5+ steps), not too coarse (1-2 steps).

### 3. YAML Output (All 6 Agents)

**Required sections:**
- `summary` (one-sentence)
- `patterns_applied` (traceability - which skill, which pattern, why)
- `verification` (quality checks performed)
- `next_step` (what happens next)

**Why:** Scannable (keys visible), structured (nested), actionable (next_step), traceable (patterns_applied).

### 4. patterns_applied Section (Critical)

**Pattern:**
```yaml
patterns_applied:
  - skill: [skill-name]
    pattern: [exact pattern name]
    where: [where applied]
    rationale: [why - cite skill reasoning]
```

**Why:** Shows which skills were used and why. Makes agent decisions traceable and verifiable.

### 5. Thin vs Thick Reminder (All 6 Agents)

**Pattern:**
```markdown
## REMEMBER

You are a **thin routing layer** to [domain] skills.

**Skills contain the expertise.** You route to them and apply their patterns.
```

**Why:** Prevents agent bloat. Keeps agent ~120-350 lines. Patterns stay in skills (400-600 lines).

---

## Critical Mistakes (From Production)

### ❌ Mistake 1: Agent Contains Patterns (Not Skills)

**Problem:** Agent 600+ lines with pattern details, examples, anti-patterns.

**Production impact:** ios-developer was 600 lines before refactoring. Patterns duplicated across agents. Hard to update.

**Fix:** Extract patterns to skills. Agent references skills, doesn't reproduce them.

**Result:** ios-developer → 326 lines. Patterns in 8 separate skills (400-600 lines each).

### ❌ Mistake 2: No patterns_applied Section

**Problem:** Output doesn't show which skills/patterns were used. Can't verify agent consulted skills.

**Production impact:** Early agents didn't have traceability. Couldn't debug why agent chose pattern X over Y.

**Fix:** Always include `patterns_applied` section. Shows skill + pattern + rationale.

**Result:** All 6 production agents now include patterns_applied. Makes decisions verifiable.

---

## Customization Notes

**Agent length:**
- Simple: 120-250 lines (1-2 task types, 3 skills)
- Standard: 250-350 lines (2-3 task types, 5 skills)
- Complex: 350-500 lines (3-4 task types, 6-8 skills)

**Colors:**
- blue: Implementation, coding, operations
- cyan: Architecture, design
- green: Quality, testing, debugging
- purple: Analysis, requirements, research
- orange: Maintenance, documentation
- red: Critical, security, urgent

**Skills selection:**
- 3-8 skills (average: 5)
- Group by domain (related patterns)
- List most-used skills first

**Output format:**
- Always include: summary, patterns_applied, verification, next_step
- Domain sections vary by agent type
- Multiple formats OK if agent handles distinct task types (e.g., ios-quality-specialist: testing, debugging, performance)

---

## Quick Start

1. **Copy template above** (lines 9-147)
2. **Fill placeholders:**
   - `[agent-name]`, `[Role Name]`, `[Domain]`
   - List 3-8 skills in frontmatter
   - Write 3-part description (purpose → scenarios → triggers)
3. **Define workflow** (3 steps: identify → apply → generate)
4. **Define output** (YAML with summary, patterns_applied, verification, next_step)
5. **Add decision tree** (routing logic to skills)
6. **Add 1-2 examples** (from real usage)

**Time:** 1-2 hours for standard agent

---

**Key Lesson:** Agents are thin routing layers (~120-350 lines). Skills are thick pattern libraries (~400-600 lines). Always include patterns_applied section (traceability). 3-step workflow. YAML output. Emphasize thin vs thick in REMEMBER.
