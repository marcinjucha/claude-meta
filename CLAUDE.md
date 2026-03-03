## Core Principles

**Signal vs Noise:** Apply to comments, tests, documentation, skills, agents, commands.
- Comments: only non-obvious decisions, skip obvious ("set loading to true")
- Unit tests: holistic coverage of key business/developer paths, skip trivial cases
- Content quality > line count: 600 lines of signal > 300 lines with noise
- **Sufficient > Comprehensive:** Focus on necessary signal, not exhaustive coverage

**WHY over HOW:** Always explain rationale, not just implementation. Include production context.

**Agents (Thin Router) - Skills (Thick Applications):**
- Agents = operating system, infrastructure, routing only
- Skills = applications, domain knowledge, patterns
- Agents have isolated context → provide everything they need before invocation
- **Skill loading mechanism:** Agent sees ONLY skill metadata/description before deciding which to fully load. Decision based on: (1) prompt from command, (2) skill descriptions. Therefore: descriptions must precisely describe WHEN to use, and command prompts should contain descriptive keywords that match skill descriptions (not explicit skill names - avoids tight coupling).
- Agents should not duplicate skill content, but critical rules (NEVER INVENT, AVOID AI-KNOWN) must live in command and agent system prompt - skills may not be loaded

---

## Artifact Architecture

**Condensed Pattern (consistent across all artifacts):**
- Anti-Patterns: Problem/Fix format, 16-40 lines max, critical markers only
- No verbose examples with full code blocks
- No generic content AI already knows (framework explanations, standard patterns)
- No historical narratives ("Critical Mistakes We Made")
- Preserve: WHY context, production incidents, project-specific patterns
- **Philosophy:** Sufficient signal > comprehensive coverage (focused, not exhaustive)

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

**Shared Resources:**
- Common Tier 3 resources in `skills/resources/` - meta-skills reference via `@../resources/`, skill-specific via `@resources/`

---

## Workflow

Always ask at the end of work whether CLAUDE.md files and skills should be updated.

Ignore folders starting with worktree-*
