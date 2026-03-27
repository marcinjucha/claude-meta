# Skills

## Overview

Meta-skills loaded by the single `claude-manager` agent. Each skill provides domain knowledge for one aspect of Claude Code artifact management. All 7 skills share 4 reference files at `resources/` via `@../resources/` paths.

## Skills in This Repo

| Skill | Lines | Purpose |
|-------|-------|---------|
| `agent-creator` | 430 | Create/evaluate subagents. Thin router architecture, tool restrictions, frontmatter, system prompt. |
| `skill-creator` | 321 | Create/evaluate/refactor skills. Signal-focused content, Tier 2/3 structure, templates. |
| `skill-fine-tuning` | 472 | Update existing skills. Pattern drift, outdated content, anti-patterns, advanced features (fork, injection, hooks). |
| `claude-md` | 406 | Create/maintain CLAUDE.md files. Project-specific discoveries, WHY context, signal filtering. |
| `command-creation` | 653 | Create/refactor multi-phase commands. Sufficient context principle, orchestration, clarifying questions pattern. |
| `git-commit-patterns` | 285 | Commit messages and organization. WHY-focused, conventional commits, ticket extraction, PR structure. |
| `signal-vs-noise` | 132 | Content quality filter. 3-question test: actionable, impactful, non-obvious. Applied to ALL other skills' output. |

## Shared Resources

| File | Purpose |
|------|---------|
| `resources/signal-vs-noise-reference.md` | 3-question filter philosophy, detailed examples |
| `resources/skill-ecosystem-reference.md` | Skill locations, sharing, permissions, dynamic injection |
| `resources/skill-structure-reference.md` | Standard structure, required sections, organization |
| `resources/why-over-how-reference.md` | WHY > HOW philosophy, production context guidelines |

## Folder Structure

```
skills/
  skill-name/
    SKILL.md          # main content with YAML frontmatter
    resources/        # skill-specific supplementary files (optional)
  resources/          # SHARED across all 7 skills via @../resources/
```

## Weird Parts / Key Patterns

**All skills serve one agent**: Unlike claude-dev (skills distributed across 8 agents), all 7 skills here load into `claude-manager` exclusively. **Why:** all meta-operations share the same quality principles (signal vs noise, WHY over HOW), so one agent with a decision tree routes to the right skill.

**signal-vs-noise is the smallest skill (132 lines) but most widely referenced**: Every other skill references it as the quality gate for output. It is the foundational filter — all artifact content must pass its 3-question test before inclusion. **Why separate skill instead of inline in agent:** the filter philosophy is detailed enough to warrant its own reference, and keeping it as a skill allows other skills to `@../resources/signal-vs-noise-reference.md` the expanded version.

**command-creation is the largest (653 lines)**: Command orchestration is the most complex artifact type — multi-phase design, sufficient context principle, clarifying questions pattern, knowledge capture phase, section templates. **Why not split:** all sections are interconnected; the sufficient context principle references phase design which references clarifying questions. Splitting would lose that context chain.

**skill-creator vs skill-fine-tuning split**: Creator handles new skills (what to include, structure decisions, Tier 2/3 split). Fine-tuning handles existing skills (what to change, drift detection, advanced features). **Why two skills instead of one:** different decision frameworks — "what should this skill contain?" vs "what drifted and needs updating?" Combining them would exceed 700 lines with two distinct mental models competing for attention.

**Shared resources via `@../resources/` paths**: 4 reference files live at `skills/resources/` and are referenced by multiple skills using relative paths. **Why not duplicate into each skill:** single source of truth for foundational philosophy. Updating signal-vs-noise-reference.md once updates it for all 7 skills.

**Skills contain the "NEVER INVENT" and "AVOID AI-KNOWN" rules redundantly**: These rules appear in both `claude-manager` system prompt AND in individual skills. **Why:** skills are lazily loaded — the agent system prompt enforces the rules immediately, skills reinforce them when loaded for detailed work. Not a mistake, intentional defense-in-depth.

## Cross-References

- `../CLAUDE.md` -- repo overview, self-referential system, shared resources explanation
- `../agents/CLAUDE.md` -- claude-manager loads all 7 skills, opus model rationale
- `../commands/CLAUDE.md` -- manage-* commands invoke claude-manager which routes to these skills
