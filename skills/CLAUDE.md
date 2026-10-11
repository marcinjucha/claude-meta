# Skills

## Overview

Global skills only: the **ai-*** meta-skills (artifact management, used by `ai-manager-agent`) plus a few domain-agnostic **working-style** skills that apply in every project. Domain skills (vps-*, copy-*, so-* …) live in `claude-dev` / `claude-marketing`, not here.

## AI Meta-Skills (ai-manager-agent)

| Skill | Lines | Purpose |
|-------|-------|---------|
| `ai-agent-creator` | 433 | Create/evaluate subagents. Thin router architecture, tool restrictions, frontmatter, system prompt. |
| `ai-skill-creator` | 321 | Create/evaluate/refactor skills. Signal-focused content, Tier 2/3 structure, templates. |
| `ai-skill-fine-tuning` | 472 | Update existing skills. Pattern drift, outdated content, anti-patterns, advanced features (fork, injection, hooks). |
| `ai-claude-md` | 333 | Create/maintain CLAUDE.md files. Project-specific discoveries, WHY context, signal filtering. |
| `ai-command-creation` | 555 | Create/refactor multi-phase commands. Sufficient context principle, orchestration, clarifying questions pattern. |
| `ai-git-commit-patterns` | 283 | Commit messages and organization. WHY-focused, conventional commits, ticket extraction, PR structure. |
| `ai-skill-lifecycle` | 417 | Full skill lifecycle (create + maintain + advanced features) in one skill. **NOT preloaded** by `ai-manager-agent`. |

## Working-Style Skills (global, any project)

| Skill | Lines | Tracked | Purpose |
|-------|-------|---------|---------|
| `human-language-check` | 79 | yes | Two-pass review of reader-facing text: correctness, then de-AI/clarity. Cleans only audience text, never scaffolding. Mandated by `../CLAUDE.md` for all human-facing text. |
| `summary-signal-first` | 124 | yes | Summary/status/recap for a named recipient: decides what gets cut and what leads (the recipient's decision). Runs BEFORE `human-language-check`. |
| `brainstorming` | 78 | no (new) | Turn-by-turn variant-narrowing loop: 3 variants → one recommendation → his pick is the next base, variants push along named axes; he closes it; rejection CRITERIA recorded. |
| `brain-conventions` | 91 | SYMLINK → brain-vault/.brain | Brain conventions + knowledge-distillation discipline. Edit at source in `brain-vault/.brain`. |

## Other Directories

| Path | What |
|------|------|
| `resources/` | 4 shared reference files (signal-vs-noise, skill-ecosystem, skill-structure, why-over-how) used by ai-* skills via `@../resources/`. |
| `synced/<id>/` | 22 synced `anthropic-skills:*` copies (untracked). Not authored here — don't edit or register them. |

## Weird Parts / Key Patterns

**`ai-manager-agent` preloads 6 of 7 ai-* skills**: `ai-skill-lifecycle` is on disk but not in the agent's `skills:` frontmatter, so it only loads on demand.

**signal-vs-noise absorbed into shared resource**: Previously a standalone skill, now lives entirely in `resources/signal-vs-noise-reference.md`. **Why absorbed:** every skill already referenced the shared resource — the standalone skill was redundant indirection.

**ai-command-creation is the largest**: **Why not split:** sufficient context principle → phase design → clarifying questions form one chain; splitting would lose it.

**ai-skill-creator vs ai-skill-fine-tuning split**: "what should this skill contain?" vs "what drifted and needs updating?" — two decision frameworks that would compete for attention in one file.

**"NEVER INVENT" and "AVOID AI-KNOWN" rules live in multiple places**: `ai-manager-agent` system prompt, individual skills, AND `signal-vs-noise-reference.md`. **Why:** defense-in-depth — the system prompt enforces them before any skill loads.

**Working-style skills encode Marcin's global rules, not a domain**: `human-language-check`, `summary-signal-first` and `brainstorming` are the executable form of rules in `../CLAUDE.md` (language check, lead with the point, one unit per turn). **Why global:** those rules apply in every project, so the skills must be reachable from every project.

## Cross-References

- `../CLAUDE.md` -- repo overview, self-referential system, symlink rules
- `../agents/CLAUDE.md` -- ai-manager-agent frontmatter and skill preloading
- `../commands/CLAUDE.md` -- ai-* commands invoke ai-manager-agent which routes to these skills
