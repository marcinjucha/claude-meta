# Skills

## Overview

Meta-skills loaded by the single `ai-manager-agent` agent. Each skill provides domain knowledge for one aspect of Claude Code artifact management. All 6 skills share 4 reference files at `resources/` via `@../resources/` paths.

## Skills in This Repo

| Skill | Lines | Purpose |
|-------|-------|---------|
| `ai-agent-creator` | 430 | Create/evaluate subagents. Thin router architecture, tool restrictions, frontmatter, system prompt. |
| `ai-skill-creator` | 321 | Create/evaluate/refactor skills. Signal-focused content, Tier 2/3 structure, templates. |
| `ai-skill-fine-tuning` | 472 | Update existing skills. Pattern drift, outdated content, anti-patterns, advanced features (fork, injection, hooks). |
| `ai-claude-md` | 406 | Create/maintain CLAUDE.md files. Project-specific discoveries, WHY context, signal filtering. |
| `ai-command-creation` | 653 | Create/refactor multi-phase commands. Sufficient context principle, orchestration, clarifying questions pattern. |
| `ai-git-commit-patterns` | 285 | Commit messages and organization. WHY-focused, conventional commits, ticket extraction, PR structure. |

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

**All skills serve one agent**: Unlike claude-dev (skills distributed across 8 agents), all 6 skills here load into `ai-manager-agent` exclusively. **Why:** all meta-operations share the same quality principles (signal vs noise, WHY over HOW), so one agent with a decision tree routes to the right skill.

**signal-vs-noise absorbed into shared resource**: Previously a standalone skill (132 lines), now lives entirely in `resources/signal-vs-noise-reference.md`. **Why absorbed:** all unique content (AI-known content filter, invented content rules, content philosophy) fits naturally in the shared resource. All skills already referenced the shared resource via `@../resources/signal-vs-noise-reference.md` — the standalone skill was redundant indirection.

**ai-command-creation is the largest (653 lines)**: Command orchestration is the most complex artifact type — multi-phase design, sufficient context principle, clarifying questions pattern, knowledge capture phase, section templates. **Why not split:** all sections are interconnected; the sufficient context principle references phase design which references clarifying questions. Splitting would lose that context chain.

**ai-skill-creator vs ai-skill-fine-tuning split**: Creator handles new skills (what to include, structure decisions, Tier 2/3 split). Fine-tuning handles existing skills (what to change, drift detection, advanced features). **Why two skills instead of one:** different decision frameworks — "what should this skill contain?" vs "what drifted and needs updating?" Combining them would exceed 700 lines with two distinct mental models competing for attention.

**Shared resources via `@../resources/` paths**: 4 reference files live at `skills/resources/` and are referenced by multiple skills using relative paths. **Why not duplicate into each skill:** single source of truth for foundational philosophy. Updating signal-vs-noise-reference.md once updates it for all 7 skills.

**"NEVER INVENT" and "AVOID AI-KNOWN" rules live in multiple places**: These rules appear in `ai-manager-agent` system prompt, individual skills, AND the shared `signal-vs-noise-reference.md`. **Why:** defense-in-depth — agent system prompt enforces rules immediately (before skills load), skills reinforce when loaded, shared resource provides the complete philosophy.

## Cross-References

- `../CLAUDE.md` -- repo overview, self-referential system, shared resources explanation
- `../agents/CLAUDE.md` -- ai-manager-agent loads all 7 skills, opus model rationale
- `../commands/CLAUDE.md` -- ai-* commands invoke ai-manager-agent which routes to these skills
