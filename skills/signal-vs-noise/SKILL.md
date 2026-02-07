---
name: signal-vs-noise
description: Signal vs Noise philosophy for filtering information and making decisions. Use when evaluating what to include in documentation, tests, code comments, or any content creation.
argument-hint: "[content-type]"
---

# Signal vs Noise - Decision Filter

**Purpose:** Filter information to focus on what matters. Apply to documentation, tests, code comments, feature decisions.

## ⚠️ CRITICAL: AVOID AI-KNOWN CONTENT

**Core principle for signal vs noise:** If Claude already knows it, it's NOISE.

**Why this matters:** Generic explanations (framework basics, standard patterns, architecture 101) waste token budget and dilute project-specific insights. Always prioritize project-specific content over generic knowledge.

**Self-check question:**
> "Would Claude know this without documentation?"
> - **YES** → It's noise, remove it (React hooks basics, standard design patterns)
> - **NO** → It's signal, keep it (project-specific bugs, non-obvious decisions)

**Example:**
```markdown
❌ NOISE (AI-known): "Repository pattern separates data access from business logic"
✅ SIGNAL (project-specific): "Never query same table in RLS policy → infinite recursion (crashed prod)"

❌ NOISE (AI-known): "Use meaningful variable names"
✅ SIGNAL (project-specific): "Use weak ref in subscription hooks → prevents NMB leak (production incident)"
```

**When filtering content:**
- Generic knowledge → NOISE (remove)
- Project-specific application → SIGNAL (keep)
- Framework explanations → NOISE (remove)
- Critical project bugs → SIGNAL (keep)
- Standard syntax → NOISE (remove)
- Non-obvious project patterns → SIGNAL (keep)

## ⚠️ CRITICAL: SIGNAL MUST BE REAL, NOT INVENTED

**ABSOLUTE RULE:**

- ❌ **NEVER invent metrics, numbers, or incidents** to demonstrate signal vs noise
- ❌ **Production impact examples MUST be real** (user-provided only)
- ❌ **Don't make up "before/after" statistics** to show improvements

**Signal vs Noise applies to REAL data:**

- ✅ **Real project-specific patterns** (not invented examples)
- ✅ **Real incidents** user described (not hypothetical scenarios)
- ✅ **Actual numbers** user provided (not made-up metrics)

**RED FLAGS - NEVER invent:**
- ❌ Metrics/percentages without source ("30% faster", "50% reduction")
- ❌ Production incidents without user verification
- ❌ Team statistics or timing data
- ❌ Anti-patterns without real examples

**GREEN LIGHT - ONLY include:**
- ✅ User-provided data and incidents
- ✅ Real patterns from codebase
- ✅ Placeholder when missing: `[User to provide: real metric]`

**Quick test:** Can you verify with user/codebase? NO → Use placeholder or skip.

**If no real data available:**

- Ask user: "Do you have real metrics/incidents for this?"
- Use placeholder: `[User to provide real example]`
- Focus on the principle without fake examples

---

## The 3-Question Filter

**Before including ANY information, ask:**

1. **Actionable?** Can Claude/user act on this?
2. **Impactful?** Would lack of this cause problems?
3. **Non-Obvious?** Is this insight non-trivial?

**If ANY answer is NO → It's NOISE → Cut it.**

---

## SIGNAL (Keep)

- Project-specific weird stuff + WHY explanation
- Critical crashes/bugs prevention
- Non-obvious patterns with context
- Real mistakes made + fix
- Impact numbers (NMB memory leak, X% error rate, $Y/week cost)

## NOISE (Cut)

- Generic patterns Claude already knows (frameworks, architectures)
- HOW explanations without WHY
- Standard syntax examples
- Architecture 101 explanations
- Obvious comments ("Set loading to true")

---

## Application: Documentation

**SIGNAL:**
```markdown
## Resource Lifecycle (Memory Leak Fix)
Resource owned by LeafComponent, NOT RootComponent.
**Why**: Previous approach leaked NMB per navigation. Devices crashed.
```

**NOISE:**
```markdown
## Data Access Pattern
Data access layer handles persistence. It can use different strategies...
[Claude already knows this]
```

---

## Application: Code Comments

**SIGNAL:**
```
// Critical: Use reactive value directly, not cached property
// Cached property may be stale during reactive emission
guard let contextId = newContextId else { return }
```

**NOISE:**
```
// Set loading state to true
state.isLoading = true
```

---

## Application: Tests

**SIGNAL:** Complete user journey with business outcome
```
func testUserCompletesWorkflowAndOperationSucceeds()
```

**NOISE:** Trivial verification
```
func testButtonTapSendsAction()
```

---

## Application: CLAUDE.md Files

**SIGNAL:** Project-specific decisions with WHY
- "N-second timeout window prevents false negatives (X% fewer tickets)"
- "Resource in LeafComponent, not RootComponent (NMB leak fixed)"

**NOISE:** Generic patterns
- "Use reactive state for UI updates" (Claude knows)
- "Architecture has N layers" (Claude knows)

---

## Quick Test

**Before writing anything, ask:**
"Is this something Claude already knows?"
- YES → Cut it
- NO → Keep it (with WHY)

---

## Anti-Patterns (Common Mistakes)

### ❌ Mistake 1: Including Generic Framework Knowledge

**Problem:** Documentation explains how frameworks work instead of documenting project-specific decisions.

**Why bad:** Claude already knows framework patterns. Generic explanations waste token budget and dilute project-specific insights.

**Fix:** Document only project-specific decisions and patterns that differ from framework defaults.

---

### ❌ Mistake 2: Over-Filtering (Removing Signal)

**Problem:** Applying filter too aggressively, cutting project-specific context because "Claude might know this already."

**Why bad:** Removes critical project decisions that differ from defaults. Claude makes incorrect assumptions based on standard patterns when your project does things differently.

**Fix:** When in doubt, ask "Does our project do this differently than standard approach?" If yes, document it with WHY. Better to include project-specific context than remove it.

---

## Resources

**Shared resources** (`@../resources/`) - Common across meta-skills:
- `@../resources/why-over-how-reference.md` - Content quality philosophy (WHY > HOW, production context mandatory)
- `@../resources/skill-structure-reference.md` - Standard structure and best practices (quality > brevity)

**Use references for:**
- Why over How → Philosophy of including production context and rationale in all content
- Structure → Consistent organization patterns (required sections, quality guidelines)

**Why included:**
- Self-contained philosophy guide (no external dependencies)
- Consistent philosophy across all meta skills (skills, agents, workflows, docs)
- Complete context for applying filter to all content types

---

## Content Philosophy

**Sufficient > Comprehensive:**
- Focus on necessary signal, not exhaustive coverage
- 600 lines of focused signal > 300 lines missing critical info
- Include what's needed, skip what's known
- Sufficient patterns > comprehensive documentation

**Remember:** 100 lines of project-specific content > 50 lines of generic patterns.
