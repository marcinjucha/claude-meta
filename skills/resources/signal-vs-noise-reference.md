---
name: signal-vs-noise
description: Signal vs Noise philosophy for filtering information and making decisions. Use when evaluating what to include in documentation, tests, code comments, or any content creation.
---

# Signal vs Noise - Decision Filter

**Purpose:** Filter information to focus on what matters. Apply to documentation, tests, code comments, feature decisions.

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

**Remember:** 100 lines of project-specific content > 50 lines of generic patterns.
