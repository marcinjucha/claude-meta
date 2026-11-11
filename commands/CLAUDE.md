# Commands

## Overview

Slash commands for managing Claude Code artifacts and utilities. All `ai-*` artifact commands follow the same tri-modal pattern (CREATE/AUDIT/MODIFY) and delegate to `ai-manager-agent`.

## Commands in This Repo

| Command | Purpose | Agent Used |
|---------|---------|------------|
| `/ai-skill` | Create, audit, or modify skills | ai-manager-agent |
| `/ai-agent` | Create, audit, or modify agents | ai-manager-agent |
| `/ai-commands` | Create, audit, or modify multi-phase commands | ai-manager-agent |
| `/ai-git` | Generate commit messages from staged changes | none (inline) |
| `/ai-extract-memory` | Auto-extract session learnings to memory.md | none (inline) |
| `/ai-curate-memory` | Promote mature memory entries to CLAUDE.md files | none (inline) |
| `/ai-solve` | Universal non-technical task executor (presentations, planning, research) | general-purpose |
| `/website` | Professional website/landing page from a brief: real-site references → impeccable build → motion → verification | impeccable (+ its agents), inline orchestration |

Also here: `council.md`, `improve-process.md`, `website.md` (native), and 12 `brain-*` symlinks into `brain-vault/.brain` (edit at source; 4 committed as symlink blobs, 8 untracked). `/brain-social` moved out on 2026-10-11; it now lives in `brain-vault/.claude/commands`.

## Weird Parts / Key Patterns

**Tri-modal pattern (ai-* artifact family)**: Phase 0 always detects intent from natural language → CREATE, AUDIT, or MODIFY. Then adaptive phases follow. **Why:** users describe what they want naturally ("update the skill", "check quality", "create new agent") — the command figures out the mode, so one command handles three operations per artifact type.

**No `/ai-claude-md` command — it is the skill**: typing `/ai-claude-md` loads `skills/ai-claude-md/SKILL.md`, which delegates the writing to ai-manager-agent. **Why:** a skill shadows a same-named command; the old command never ran and was deleted 2026-11-11. Never name a command after an existing skill.

**ai-* artifact commands use ai-manager-agent; /ai-solve uses general-purpose**: The ai-* artifact commands are artifact-specific (need meta-skills). /ai-solve handles arbitrary non-technical tasks (presentations, research) — doesn't need artifact knowledge.

**Ask once, only about assumptions; one consent point**: ai-* artifact commands ask the user in ONE message, and only when assuming scope, location (claude-dev / brain-vault/.claude / ~/.claude / the source of a symlink) or what the change applies to; otherwise they merge phases and act. The only gate is plan → approval → ai-manager-agent writes. `ai-command-creation` teaches the same rule, so new commands inherit it. **Why:** the old per-phase paraphrase + 3-5 questions + Socratic gate + continue/skip footer ran in zero observed sessions (audit 2026-11-11), and Marcin's rule is "decide yourself, ask only about assumptions".

**/ai-git is the simplest command**: No agent invocation, no phases — reads staged diff, generates commit message, shows for review. **Why:** a commit message needs no plan or consent point. Prerequisites: must have staged changes first.

**/ai-extract-memory is fully automatic**: Unlike ai-* artifact commands, it runs without any clarifying questions or confirmations. Sole exception: inside the brain vault it targets the per-context buffer `01-Projects/<ctx>/memory.md` (the root `memory.md` no longer exists) and asks which context when the session doesn't make it clear; `/ai-curate-memory` does the same. **Why:** memory extraction is low-risk (appends to memory.md, doesn't modify artifacts) and speed matters — asking questions would make users avoid running it.

**/ai-curate-memory is the bridge between memory and CLAUDE.md**: Reads memory.md → discovers all CLAUDE.md files → promotes mature entries to the right CLAUDE.md → removes from memory.md. **Why:** memory.md is quick capture; CLAUDE.md is permanent knowledge. Curation prevents memory.md from growing unbounded while ensuring learnings reach the right documentation.

**/website has three decision points, not the house template's one**: Marcin decides at reference pick, comp approval (impeccable's own gate) and ship. References enter impeccable as text and direction-page steer, never as `--ref` images. **Why:** impeccable takes the look from its dealt world, and external screenshots passed as `--ref` would override it. It also does not re-spawn `impeccable-finish-reviewer`, because impeccable already runs it; the command acts on its outcome. Figma is not a preview surface: rendering an impeccable pick there draws the same design twice and only approximates the coded page. Preview = impeccable comps, `/impeccable live`, Playwright shots. Figma stays as an input branch (Figma URL) and an on-request push.

**Sufficient context principle**: Commands must pass ALL necessary context to ai-manager-agent. The agent has isolated context — it cannot "look up" conversation history. Inline phases (Phase 0) extract and prepare context before agent invocation.

## Cross-References

- `../agents/CLAUDE.md` — ai-manager-agent (the agent all ai-* artifact commands invoke)
- `../skills/CLAUDE.md` — skills loaded by ai-manager-agent during command execution
- `../CLAUDE.md` — repo overview, tri-modal pattern explanation
