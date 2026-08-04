# ~/.claude — Global Config + Meta-Artifact Toolchain

## Overview

This IS `~/.claude` — the live global Claude Code config, loaded into every session in every project, and itself a git repo (`.gitignore` excludes runtime dirs: `cache`, `projects`, `history.jsonl`, `plugins`, `backups`, `debug`, `shell-snapshots`, `.DS_Store`, …). It holds the **meta-artifact toolchain** natively (tools for creating, auditing, and maintaining other Claude Code artifacts) and receives the `brain-*` family by symlink from `claude-brain`.

**Domain artifacts live elsewhere:** project-specific agents/skills/commands stay in their own repos (`claude-dev` = programming/infra, `claude-marketing` = go-to-market) and are symlinked into each project's `.claude/`. Only meta-tooling + global behavior belongs here. **Why:** keeps each repo's skill-description routing budget focused on one domain.

## Structure

```
agents/      → ai-manager-agent.md (opus, tracked) + brain-manager.md (SYMLINK → claude-brain, untracked)
             + agents/CLAUDE.md
commands/    → 22 .md: 10 native (8 ai-* + council.md + commands/CLAUDE.md)
             + 12 brain-* SYMLINKS → claude-brain (5 committed as symlinks, 7 untracked)
skills/      → 7 meta skills (ai-agent-creator, ai-claude-md, ai-command-creation,
               ai-git-commit-patterns, ai-skill-creator, ai-skill-fine-tuning, ai-skill-lifecycle)
             + human-language-check (tracked) + brain-learn (UNTRACKED, this machine only)
             + brain-conventions (SYMLINK → claude-brain, untracked)
  resources/ → 4 shared reference files used across multiple skills via @../resources/
docs/        → Official Claude Code documentation (agents-doc.md, skill-doc.md)
statusline-command.sh → Status line script (model, cost, context %) — hardcoded macOS path
memory.md    → tracked session-memory buffer
```

**EDIT AT THE SOURCE, not through the symlink**: every `brain-*` command, `brain-manager.md`, and `skills/brain-conventions` is a symlink into `/Users/marcinjucha/Prywatne/projects/claude-brain/.claude/` — edit them THERE. The symlinks are created by `claude-brain/scripts/link-commands.sh` (idempotent, links `commands/*.md`). **Why:** editing via the `~/.claude` path writes through into `claude-brain` with no diff visible here — and the 7 untracked ones must never be committed in `~/.claude`, since their source of truth is `claude-brain`. The 5 that ARE committed (brain-load, brain-publish, brain-pull, brain-social, brain-update) are stored as symlink blobs holding an absolute machine-specific path — they resolve only on this machine.

## Weird Parts / Key Patterns

**Self-referential system**: `ai-manager-agent` uses the meta-skills to build/maintain artifacts — including itself and this file. When modifying ai-manager-agent or its skills, changes affect the tool doing the work.

**Two agents, one of which does all meta work**: `ai-manager-agent` (opus) performs every artifact operation (create/audit/modify agents, skills, commands, CLAUDE.md) and preloads **6** of the 7 meta skills in its frontmatter — `ai-skill-lifecycle` exists on disk but is NOT preloaded. **Why one agent with skill routing:** all meta-operations share the same quality principles (signal vs noise, WHY over HOW, no invented content), so routing by skill beats a fleet of near-identical agents. `brain-manager` is a separate router for brain/vault operations and shares none of that.

**Tri-modal command pattern**: All `ai-*` artifact commands (ai-skill, ai-agent, ai-claude-md, ai-commands) share identical phase structure: Phase 0 detects intent (CREATE/AUDIT/MODIFY), then adaptive phases follow. **Why:** consistent UX — user always gets clarifying questions → agent work → verification, regardless of artifact type.

**Three critical rules live in the agent system prompt, not skills**: `agents/ai-manager-agent.md` carries "FACT-BASED CONTENT ONLY" (no invented metrics/incidents), "AVOID AI-KNOWN CONTENT", and "SCRIPT DETERMINISTIC WORK OVER LARGE INPUTS" inline. **Why:** skills are lazily loaded — if these rules lived only in skills, ai-manager-agent could generate invented metrics before the skill enforcing the rule gets loaded.

**Artifact-file writes MUST route through ai-manager-agent, never the orchestrator inline**: The `ai-*` command family (ai-commands, ai-skill, ai-agent, ai-claude-md, ai-extract-memory) mandates that any file creation / implementation / edit to an artifact-definition file (`commands/*.md`, `skills/**/SKILL.md`, `agents/*.md`) goes through the `ai-manager-agent` subagent — the main loop must not write those files itself, even with full context. **Why:** a session running `/ai-commands` rationalized writing the command files inline ("I have context, it's procedural") and bypassed the command's explicit "must use ai-manager-agent" rule; user caught it. Rationalizations ("simpler", "full context") do NOT override an explicit MUST. Mechanical backstop: a global `~/.claude/settings.json` `PreToolUse` hook (matcher `Write|Edit`) fires a non-blocking reminder (via `hookSpecificOutput.additionalContext`) whenever an artifact-definition path is touched — non-blocking (exit 0) so the legitimate path (the subagent itself writing the files) is never blocked. CLAUDE.md files are intentionally out of scope (editable via the agent but not gated). Rule originates in the `ai-*` command bodies; enforcement hook lives in `~/.claude/settings.json`.

**Shared resources at `skills/resources/`**: 4 reference files (signal-vs-noise, skill-ecosystem, skill-structure, why-over-how) shared across the meta skills via `@../resources/` paths. **Why:** avoids duplicating foundational reference content across 7 skills.

**statusline-command.sh has hardcoded macOS path**: Line 8 reads `.effortLevel` from `/Users/marcinjucha/.claude/settings.json` via `jq` — only works on the original dev machine, not on VPS.

**`memory.md` is checked into git**: `~/.claude/memory.md` is tracked, unlike the global auto-memory index. Preference: save learnings to the *project's* `memory.md`, not to global auto-memory.

## Cross-References

- `~/.claude/agents/CLAUDE.md` — ai-manager-agent frontmatter, skill loading, thin router pattern
- `~/.claude/commands/CLAUDE.md` — command registry, tri-modal pattern, orchestration details
- `~/.claude/skills/CLAUDE.md` — skill registry, shared resources, meta-skill relationships

## Second Brain & Session Memory (global behavior)

**Brain-first awareness.** At session start, if the cwd maps to a claude-brain context (per
`/Users/marcinjucha/Prywatne/projects/claude-brain/config.json` `.paths`), treat the brain
project memory (`<vault>/<…>/_*.md`, the high shelf) as the source of truth for status and
cross-project connections; keep it current via `/brain-update` at milestones; treat the
worktree `SESSION.md` as the fine-grained, worktree-local scratchpad. The SessionStart hook
only *injects* this data (read-only) — acting on it (full orient, ticket backfill) is `/brain-load`.
If the cwd maps to NO brain context, `SESSION.md` is the only working memory.

**`[do potwierdzenia]` for unverified hypotheses.** Mark any diagnosis or conclusion not yet
confirmed by on-device testing / a passing test with a `[do potwierdzenia]` prefix in brain and
SESSION notes. Promote to plain fact only after verification. **Why:** a guessed diagnosis once
got recorded as fact and was later refuted — the prefix keeps hypotheses visibly provisional.

## Reader-facing Text — mandatory language check (global behavior)

**Whenever I write text a HUMAN reader will see — always run the `human-language-check` skill
before delivering it.** This is a MUST, not a suggestion, and it applies especially to
**website content and any copy for clients** (landing/site copy, posts, emails, ad/sales copy,
scripts, surveys, messages). The skill lives at `~/.claude/skills/human-language-check` (global,
available in every project). Run both passes (poprawność → de-AI/clarity) and honor its safety
gate: clean ONLY audience-facing text, never scaffolding (doc titles, operator instructions in
parentheses, internal notes). **Why:** unchecked text ships grammar errors and AI-tells; for
website/client copy that directly damages credibility — the check is the last gate before it
reaches a reader. Does NOT apply to code or purely internal working notes (there jargon,
abbreviations, and em-dashes are functional).
