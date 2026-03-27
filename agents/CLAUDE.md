# Agents

## Overview

Single meta-agent that orchestrates all artifact creation and maintenance. Unlike claude-dev (8 domain agents), claude-meta needs only one agent because all meta-operations share the same quality principles.

## Agents in This Repo

| Agent | Purpose | Model | Skills Loaded |
|-------|---------|-------|---------------|
| `claude-manager` | Creates/maintains all Claude Code artifacts (agents, skills, commands, CLAUDE.md). Enforces thin-router architecture and signal-focused content. | opus | agent-creator, skill-creator, skill-fine-tuning, claude-md, command-creation, git-commit-patterns, signal-vs-noise |

## Weird Parts / Key Patterns

**Opus model required**: claude-manager uses opus (not sonnet). **Why:** meta-operations require reasoning about artifact quality, signal vs noise filtering, and cross-artifact consistency — cheaper models produce more noise and miss subtle quality issues.

**Loads all 7 skills**: Unlike domain agents (2-4 skills each), claude-manager loads every meta-skill. **Why:** a single artifact operation often touches multiple concerns — creating a skill requires signal-vs-noise filtering, skill-creator templates, AND claude-md knowledge for cross-references. Decision tree in system prompt routes to the right skill.

**Two hardcoded critical rules**: "FACT-BASED CONTENT ONLY" and "AVOID AI-KNOWN CONTENT" are in the agent system prompt directly (lines 19-52), not in skills. **Why:** these rules must apply BEFORE any skill loads — prevents generated noise from entering artifacts during the skill-loading decision phase.

**Thin router pattern exceeded**: claude-manager's system prompt is ~84 lines body (98 with frontmatter) — significantly over the <50 line guideline. **Why justified:** the two critical rules (FACT-BASED, AVOID AI-KNOWN) at lines 19-52 must live in the system prompt, not skills. The decision tree (lines 79-87) and orchestration pattern (lines 89-98) are the routing logic; all domain knowledge comes from skills.

## Cross-References

- `../CLAUDE.md` — repo overview, self-referential system explanation
- `../skills/CLAUDE.md` — the 7 skills this agent loads
- `../commands/CLAUDE.md` — all commands invoke this agent via `subagent_type="claude-manager"`
