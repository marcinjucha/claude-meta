# Agents

## Overview

Single meta-agent that orchestrates all artifact creation and maintenance, plus one symlinked brain router. Unlike claude-dev (domain agents), this repo (GitHub: `claude-meta`) needs only one meta-agent because all meta-operations share the same quality principles.

## Agents in This Repo

| Agent | Purpose | Model | Skills Loaded |
|-------|---------|-------|---------------|
| `ai-manager-agent` | Creates/maintains all Claude Code artifacts (agents, skills, commands, CLAUDE.md). Enforces thin-router architecture and signal-focused content. | opus | preloads ai-skill-creator, ai-skill-fine-tuning, ai-claude-md, ai-command-creation; on demand: ai-agent-creator, ai-git-commit-patterns |
| `brain-manager` | Worker for `/brain-meeting` phases 2/2r/4a/4b + transcript fetch (48/48 spawns, audit 2026-11 G8). | inherit | no preload (brain-conventions dropped: 4b writes no knowledge notes) |

## Weird Parts / Key Patterns

**`brain-manager.md` is a SYMLINK, untracked here**: source is `/Users/marcinjucha/Prywatne/projects/brain-vault/.brain/.claude/agents/brain-manager.md`. Edit it THERE, never through this path. **Why:** an edit via `~/.claude/agents/` writes through into the vault with no diff visible in this repo (see `../CLAUDE.md` "EDIT AT THE SOURCE").

**Opus model required**: ai-manager-agent uses opus (not sonnet). **Why:** meta-operations require reasoning about artifact quality, signal vs noise filtering, and cross-artifact consistency — cheaper models produce more noise and miss subtle quality issues.

**Preloads 4 of 6 skills**: ai-skill-creator, ai-skill-fine-tuning, ai-claude-md, ai-command-creation. **Why:** a single artifact operation often touches several of them — creating a skill requires ai-skill-creator templates AND ai-claude-md knowledge for cross-references. `ai-agent-creator` and `ai-git-commit-patterns` are NOT preloaded; the decision tree routes those cases to an explicit Skill call. **Why:** 82 spawns in a month (audit 2026-11-11), none created an agent or wrote a commit message, so the ~20 KB they add went unused on every spawn — below the ">50% of invocations" preload bar in ai-agent-creator.

**Three hardcoded critical rules**: "FACT-BASED CONTENT ONLY", "AVOID AI-KNOWN CONTENT" and "SCRIPT DETERMINISTIC WORK OVER LARGE INPUTS" are sections of the agent system prompt itself, not skills. **Why:** these rules must apply BEFORE any skill loads — prevents generated noise from entering artifacts during the skill-loading decision phase. They are also the quality filter the decision tree points to; the `@../resources/` reference files are read on demand only.

**Thin router pattern exceeded**: ai-manager-agent's file is ~107 lines with frontmatter — over the <50 line guideline. **Why justified:** the three CRITICAL sections must live in the system prompt, not skills. "Decision Tree" and "Orchestration Pattern" are the routing logic; all domain knowledge comes from skills.

## Cross-References

- `../CLAUDE.md` — repo overview, self-referential system explanation, symlink rules
- `../skills/CLAUDE.md` — the 6 meta skills this agent uses (4 preloaded)
- `../commands/CLAUDE.md` — the ai-* artifact commands invoke this agent via `subagent_type="ai-manager-agent"`
