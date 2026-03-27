# Commands

## Overview

Slash commands for managing Claude Code artifacts and utilities. All `manage-*` commands follow the same tri-modal pattern (CREATE/AUDIT/MODIFY) and delegate to `claude-manager` agent.

## Commands in This Repo

| Command | Purpose | Agent Used |
|---------|---------|------------|
| `/manage-skill` | Create, audit, or modify skills | claude-manager |
| `/manage-agent` | Create, audit, or modify agents | claude-manager |
| `/manage-claude-md` | Create, audit, or modify CLAUDE.md files | claude-manager |
| `/manage-commands` | Create, audit, or modify multi-phase commands | claude-manager |
| `/manage-git` | Generate commit messages from staged changes | none (inline) |
| `/extract-memory` | Auto-extract session learnings to memory.md | none (inline) |
| `/curate-memory` | Promote mature memory entries to CLAUDE.md files | none (inline) |
| `/solve` | Universal non-technical task executor (presentations, planning, research) | general-purpose |

## Weird Parts / Key Patterns

**Tri-modal pattern (manage-* family)**: Phase 0 always detects intent from natural language → CREATE, AUDIT, or MODIFY. Then adaptive phases follow. **Why:** users describe what they want naturally ("update the skill", "check quality", "create new agent") — the command figures out the mode, so one command handles three operations per artifact type.

**manage-* all use claude-manager; /solve uses general-purpose**: The manage-* commands are artifact-specific (need meta-skills). /solve handles arbitrary non-technical tasks (presentations, research) — doesn't need artifact knowledge.

**Clarifying questions are MANDATORY**: Every manage-* command requires paraphrase + 3-5 clarifying questions after Phase 0 AND after every agent phase. **Why:** artifact creation is high-stakes — wrong assumptions in a skill or agent propagate to all projects using claude-dev. The checkpoint pattern catches misunderstandings early.

**/manage-git is the simplest command**: No agent invocation, no phases — reads staged diff, generates commit message, shows for review. **Why:** commit messages don't need the full clarifying-questions ceremony. Prerequisites: must have staged changes first.

**/extract-memory is fully automatic**: Unlike manage-* commands, it runs without any clarifying questions or confirmations. **Why:** memory extraction is low-risk (appends to memory.md, doesn't modify artifacts) and speed matters — asking questions would make users avoid running it.

**/curate-memory is the bridge between memory and CLAUDE.md**: Reads memory.md → discovers all CLAUDE.md files → promotes mature entries to the right CLAUDE.md → removes from memory.md. **Why:** memory.md is quick capture; CLAUDE.md is permanent knowledge. Curation prevents memory.md from growing unbounded while ensuring learnings reach the right documentation.

**Sufficient context principle**: Commands must pass ALL necessary context to claude-manager. The agent has isolated context — it cannot "look up" conversation history. Inline phases (Phase 0) extract and prepare context before agent invocation.

## Cross-References

- `../agents/CLAUDE.md` — claude-manager (the agent all manage-* commands invoke)
- `../skills/CLAUDE.md` — skills loaded by claude-manager during command execution
- `../CLAUDE.md` — repo overview, tri-modal pattern explanation
