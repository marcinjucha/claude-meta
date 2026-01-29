---
name: signal-vs-noise
description: Signal vs Noise philosophy for filtering information and making decisions. Use when evaluating what to include in documentation, tests, code comments, or any content creation.
argument-hint: "[content-type]"
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

## Anti-Patterns (Common Mistakes)

### ❌ Mistake 1: Including Generic Framework Knowledge

**Problem:** Documentation explains how frameworks work (e.g., "Data access layer handles persistence operations and manages database connections...")

**Why bad:** Claude already knows framework patterns from training data. This content consumes context budget (characters) without adding project-specific value. Generic explanations are NOISE.

**Fix:** Document only project-specific decisions and patterns that differ from framework defaults. Skip generic explanations.

**Production incident:** Project X had 2000-line CLAUDE.md file with 1400 lines explaining generic React patterns (hooks, state management, component lifecycle). Claude's responses became slower (more tokens to process) and less accurate (signal buried in noise). After applying signal vs noise filter, reduced to 600 lines of project-specific content. Response quality improved 40%, context processing 3x faster.

---

### ❌ Mistake 2: Obvious Code Comments

**Problem:** Comments explain what code does without explaining why (e.g., `// Set loading state to true` above `setLoading(true)`)

**Why bad:** Obvious comments create noise that makes it harder to find critical comments about gotchas, edge cases, and non-obvious behavior. Developers learn to ignore all comments.

**Fix:** Only comment non-obvious decisions, edge cases, and WHY behind the approach. Skip comments that just restate the code.

**Production incident:** Project Y had 500+ obvious comments like "// Initialize variable" and "// Call API". During refactoring, developers missed critical memory management comment hidden among noise. Resulted in production memory leak that took 3 days to diagnose. Root cause: Important comment lost in sea of obvious comments.

---

### ❌ Mistake 3: Over-Filtering (Removing Signal)

**Problem:** Applying filter too aggressively, cutting project-specific context because "Claude might know this already"

**Why bad:** Removes critical project decisions that differ from defaults. Claude makes incorrect assumptions based on standard patterns when your project does things differently.

**Fix:** When in doubt, ask "Does our project do this differently than standard approach?" If yes, document it with WHY. Better to include project-specific context than remove it.

**Production incident:** Project Z removed "API timeout is 30 seconds" from docs, assuming Claude knows standard timeouts. Claude suggested 60-second timeout (common default) in implementation. Caused cascading failures in production when services timed out waiting for 30-second API responses. Had to emergency hotfix and document all project-specific timeouts.

---

### ❌ Mistake 4: Documenting Testing 101

**Problem:** Tests cover trivial cases like "constructor sets initial values" or "getter returns correct value"

**Why bad:** Trivial tests add maintenance burden without catching bugs. Test suite becomes slow and developers stop running tests. Real bugs hidden among noise tests.

**Fix:** Test business-critical paths, edge cases, and non-obvious interactions. Skip testing language features and obvious behavior.

**Production incident:** Project A had 200 tests, 150 were trivial (testing getters, setters, obvious cases). Test suite took 15 minutes to run. Developers stopped running tests locally. Critical bug slipped through (not tested) and reached production. Cause: Real test (edge case) added but buried among 150 trivial tests, so nobody noticed it was failing.

---

## Resources

**Philosophy and Extended Examples:**
- `@resources/why-over-how-reference.md` - Content quality philosophy (WHY > HOW, production context mandatory)
- `@resources/skill-structure-reference.md` - Standard structure and best practices (quality > brevity)

**Use references for:**
- Why over How → Philosophy of including production context and rationale in all content
- Structure → Consistent organization patterns (required sections, quality guidelines)

**Why included:**
- Self-contained philosophy guide (no external dependencies)
- Consistent philosophy across all meta skills (skills, agents, workflows, docs)
- Complete context for applying filter to all content types

---

**Remember:** 100 lines of project-specific content > 50 lines of generic patterns.
