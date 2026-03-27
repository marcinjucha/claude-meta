# claude-meta — Meta-Artifact Repository

## Overview

This repo stores **meta-level** Claude Code artifacts — tools for creating, auditing, and maintaining other Claude Code artifacts. Symlinked into `.claude/` alongside `claude-dev` artifacts via shared `hooks/simlink.sh`.

**Why separate from claude-dev:** claude-dev holds domain artifacts (project-specific agents, skills, commands). claude-meta holds the tooling that builds and maintains those artifacts. Separation prevents circular dependencies and allows meta-tooling to evolve independently.

## Structure

```
agents/      → Single meta-agent (claude-manager) that orchestrates all artifact work
commands/    → 8 slash commands: manage-* family + memory + solve + git
skills/      → 7 meta-skills loaded by claude-manager (creator, auditor, fine-tuner patterns)
  resources/ → 4 shared reference files used across multiple skills via @../resources/
docs/        → Official Claude Code documentation (agents-doc.md, skill-doc.md)
statusline-command.sh → Status line script (model, cost, context %) — hardcoded macOS path
```

## Weird Parts / Key Patterns

**Self-referential system**: claude-manager (the only agent) uses meta-skills to build/maintain artifacts — including itself. When modifying claude-manager or its skills, changes affect the tool doing the work.

**Single agent, 7 skills**: Unlike claude-dev (8 specialized agents), claude-meta has exactly one agent (`claude-manager`, opus model) that loads all 7 skills. **Why:** all meta-operations (create/audit/modify agents, skills, commands, CLAUDE.md) share the same quality principles (signal vs noise, WHY over HOW, no invented content), so one agent with skill-based routing is sufficient.

**Tri-modal command pattern**: All `manage-*` commands (skill, agent, claude-md, commands) share identical phase structure: Phase 0 detects intent (CREATE/AUDIT/MODIFY), then adaptive phases follow. **Why:** consistent UX — user always gets clarifying questions → agent work → verification, regardless of artifact type.

**Two critical rules live in agent system prompt, not skills**: "NEVER INVENT CONTENT" and "AVOID AI-KNOWN CONTENT" are in `claude-manager.md` directly. **Why:** skills are lazily loaded — if these rules were only in skills, claude-manager could generate invented metrics before the skill enforcing the rule gets loaded.

**Shared resources at `skills/resources/`**: 4 reference files (signal-vs-noise, skill-ecosystem, skill-structure, why-over-how) shared across multiple skills via `@../resources/` paths. **Why:** avoids duplicating foundational reference content across 7 skills.

**statusline-command.sh has hardcoded macOS path**: Line 8 reads from `/Users/marcinjucha/.claude/settings.json` — only works on the original dev machine, not on VPS.

**memory.md is project-scoped**: Unlike auto-memory (global), `memory.md` is checked into git. Preference: save project learnings here, not global auto-memory.

## Cross-References

- `agents/CLAUDE.md` — claude-manager frontmatter, skill loading, thin router pattern
- `commands/CLAUDE.md` — command registry, tri-modal pattern, orchestration details
- `skills/CLAUDE.md` — skill registry, shared resources, meta-skill relationships
