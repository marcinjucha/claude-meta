---
name: signal-vs-noise
description: Filter content to keep only project-specific signal. Use when deciding what to include in CLAUDE.md, documentation, code comments, or tests. Core rule: if Claude already knows it, it's noise - only document project-specific decisions with WHY context.
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

## Application

**Documentation:** Project-specific decisions with WHY. Nie tłumacz jak działa framework (Claude wie) - dokumentuj co robisz inaczej i dlaczego.

**Code Comments:** Tylko non-obvious decisions. `// Use reactive value directly, not cached - stale during reactive emission`. Pomijaj oczywiste (`// Set loading to true`).

**Tests:** Kompletne user journey z business outcome (`testUserCompletesWorkflowAndOperationSucceeds`). Pomijaj trywialne (`testButtonTapSendsAction`).

**CLAUDE.md:** Project-specific wzorce z WHY (`Resource in LeafComponent, not RootComponent - NMB leak`). Nie pisz tego, co Claude już wie (`Use reactive state for UI updates`).

---

## Quick Test

**Before writing anything, ask:**
"Is this something Claude already knows?"
- YES → Cut it
- NO → Keep it (with WHY)

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
