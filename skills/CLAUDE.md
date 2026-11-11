# Skills

## Overview

Global skills only: the **ai-*** meta-skills (artifact management, used by `ai-manager-agent`) plus a few domain-agnostic **working-style** skills that apply in every project. Domain skills (vps-*, copy-*, so-* …) live in `claude-dev` / the brain vault's `.claude/skills`, not here.

## AI Meta-Skills (ai-manager-agent)

All six are used by `ai-manager-agent`; `ai-agent-creator` and `ai-git-commit-patterns` are NOT preloaded (rarely needed, loaded via explicit Skill call — see `../agents/CLAUDE.md`).

| Skill | Lines | Purpose |
|-------|-------|---------|
| `ai-agent-creator` | 433 | Create/evaluate subagents. Thin router architecture, tool restrictions, frontmatter, system prompt. |
| `ai-skill-creator` | 322 | Create/evaluate/refactor skills. Signal-focused content, Tier 2/3 structure, templates. |
| `ai-skill-fine-tuning` | 461 | Update existing skills. Pattern drift, outdated content, anti-patterns, advanced features (fork, injection, hooks). |
| `ai-claude-md` | 337 | Create/maintain CLAUDE.md files. Project-specific discoveries, WHY context, signal filtering. |
| `ai-command-creation` | 345 | Create/refactor multi-phase commands. Sufficient context principle, orchestration, ask-once rule (one question message, one consent point). |
| `ai-git-commit-patterns` | 46 | Commit messages: the repo's last ~20 subjects decide the format (per-repo conventions table), subject = behaviour, body = why, never an attribution trailer. |

## Working-Style Skills (global, any project)

| Skill | Lines | Tracked | Purpose |
|-------|-------|---------|---------|
| `human-language-check` | 79 | yes | Two-pass review of reader-facing text: correctness, then de-AI/clarity. Cleans only audience text, never scaffolding. Mandated by `../CLAUDE.md` for all human-facing text. |
| `brainstorming` | 79 | yes (since 4628ba3) | Turn-by-turn variant-narrowing loop: 3 variants → one recommendation → his pick is the next base, variants push along named axes; he closes it; rejection CRITERIA recorded. |
| `stage-goal` | 115 | yes | Writes and checks the `/goal` condition for a code repo's build stage (`docs/goals/`), with a builder script and a stop-hook eval. Programming artifact, to move to claude-dev — another session owns that move. |
| `brain-conventions` | 96 | SYMLINK → brain-vault/.brain | Brain conventions + knowledge-distillation discipline. Edit at source in `brain-vault/.brain`. |

## Other Directories

| Path | What |
|------|------|
| `resources/` | 4 shared reference files (signal-vs-noise, skill-ecosystem, skill-structure, why-over-how) referenced by ai-* skills via `@../resources/`. Read on demand only, never auto-loaded (0 reads in a month, audit 2026-11-11). |
| `synced/<id>/` | 22 synced `anthropic-skills:*` copies (untracked). Not authored here — don't edit or register them. |

## Weird Parts / Key Patterns

**signal-vs-noise absorbed into shared resource**: Previously a standalone skill, now lives entirely in `resources/signal-vs-noise-reference.md`. **Why absorbed:** every skill already referenced the shared resource — the standalone skill was redundant indirection.

**ai-skill-creator vs ai-skill-fine-tuning split**: "what should this skill contain?" vs "what drifted and needs updating?" — two decision frameworks that would compete for attention in one file.

**"NEVER INVENT" and "AVOID AI-KNOWN" rules live in multiple places**: `ai-manager-agent` system prompt, individual skills, AND `signal-vs-noise-reference.md`. **Why:** defense-in-depth — the system prompt enforces them before any skill loads. Only the system-prompt copy is guaranteed to be in context: the resource file is read on demand and in practice is not read at all.

**Working-style skills encode Marcin's global rules, not a domain**: `human-language-check` and `brainstorming` are the executable form of rules in `../CLAUDE.md` (language check, lead with the point, one unit per turn). **Why global:** those rules apply in every project, so the skills must be reachable from every project.

**`summary-signal-first` retired 2026-11-11**: 0 invocations in a month; its principle lives in `../CLAUDE.md` ("The same razor on every DELIVERABLE"), and its `audit-summary.py` rejected every real coach update. Don't recreate it as a skill.

## Cross-References

- `../CLAUDE.md` -- repo overview, self-referential system, symlink rules
- `../agents/CLAUDE.md` -- ai-manager-agent frontmatter and skill preloading
- `../commands/CLAUDE.md` -- ai-* commands invoke ai-manager-agent which routes to these skills
