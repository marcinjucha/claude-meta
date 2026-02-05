## Core Principles

**Signal vs Noise:** Apply to comments, tests, documentation, skills, agents, commands.
- Komentarze: tylko non-obvious decisions, skip obvious ("set loading to true")
- Unit testy: holistyczne pokrycie najważniejszych ścieżek biznesowych/deweloperskich, pomijaj trywialne case'y
- Content quality > line count: 600 lines of signal > 300 lines with noise

**WHY over HOW:** Always explain rationale, not just implementation. Include production context.

**Agents (Thin Router) - Skills (Thick Applications):**
- Agents = operating system, infrastructure, routing only
- Skills = applications, domain knowledge, patterns
- Agents have isolated context → provide everything they need before invocation
- Skills' descriptions must precisely explain WHEN to use (not first-person "I help")
- Agenty nie powinny powielać tego, co mają w skillach

---

## Artifact Architecture (Applied Feb 2026)

**Condensed Pattern (consistent across all artifacts):**
- Anti-Patterns: Problem/Fix format, 16-40 lines max, critical markers only
- No verbose examples with full code blocks
- No generic content AI already knows (framework explanations, standard patterns)
- No historical narratives ("Critical Mistakes We Made")
- Preserve: WHY context, production incidents, project-specific patterns

**Meta-Skills Principle (embedded in skill-creator, skill-fine-tuning, command-creation, signal-vs-noise):**
- ⚠️ AVOID AI-KNOWN CONTENT: "If Claude already knows it, it's NOISE"
- Self-check: "Would Claude know this without documentation?" → YES = remove
- Focus: project-specific decisions, critical bugs, non-obvious patterns
- Skip: framework basics, architecture 101, standard syntax

**🚨 CRITICAL: NO INVENTED CONTENT**
- **NEVER fabricate metrics** without user-provided source ("40% improvement", "15 minutes saved")
- **NEVER invent production incidents** without real examples from user
- **If no data available:** Use placeholders `[User to provide: real metric]` OR delete entirely
- **Why this matters:** Invented content corrupts knowledge base, undermines trust in artifacts
- **Red flags:** Specific numbers (percentages, time savings) without attribution or "production validation"

**Results (Feb 2026 cleanup):**
- 7 skills: 5377 → 3325 lines (38% reduction)
- All artifacts follow same condensed pattern
- Token budget optimized, faster processing, maintained functionality

---

## Workflow

zawsze pytaj na koniec pracy czy nie powinienem zaktualizowac CLAUDE.md files i skills

ignoruj foldery zaczynajace sie na worktree-*
