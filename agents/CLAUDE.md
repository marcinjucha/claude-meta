# Agents

## Overview

Single meta-agent that orchestrates all artifact creation and maintenance. Unlike claude-dev (8 domain agents), claude-meta needs only one agent because all meta-operations share the same quality principles.

## Agents in This Repo

### Meta-Agent
| Agent | Purpose | Model | Skills Loaded |
|-------|---------|-------|---------------|
| `ai-manager-agent` | Creates/maintains all Claude Code artifacts (agents, skills, commands, CLAUDE.md). Enforces thin-router architecture and signal-focused content. | opus | preloads ai-skill-creator, ai-skill-fine-tuning, ai-claude-md, ai-command-creation; on demand: ai-agent-creator, ai-git-commit-patterns |

### VPS Infrastructure Agents
| Agent | Purpose | Model | Skills Loaded |
|-------|---------|-------|---------------|
| `vps-ops-agent` | VPS operations — Docker management, service health, deployments, infrastructure changes. Confirms destructive ops. | sonnet | vps-practices, vps-traefik-stack, vps-n8n-stack, vps-monitoring-stack, vps-glitchtip-stack, vps-email-stack, vps-strapi-stack, vps-plausible-stack, vps-cal-stack, vps-n8n-patterns, vps-postgresql-ops |
| `vps-validator-agent` | Read-only VPS validation — Docker correctness, service health, security posture, config validity. No write tools. | sonnet | (same as vps-ops-agent, minus write tools) |

## Weird Parts / Key Patterns

**Opus model required**: ai-manager-agent uses opus (not sonnet). **Why:** meta-operations require reasoning about artifact quality, signal vs noise filtering, and cross-artifact consistency — cheaper models produce more noise and miss subtle quality issues.

**Preloads 4 of 6 skills**: ai-skill-creator, ai-skill-fine-tuning, ai-claude-md, ai-command-creation. **Why:** a single artifact operation often touches several of them — creating a skill requires ai-skill-creator templates AND ai-claude-md knowledge for cross-references. `ai-agent-creator` and `ai-git-commit-patterns` are NOT preloaded; the decision tree routes those cases to an explicit Skill call. **Why:** 82 spawns in a month (audit 2026-11-11), none created an agent or wrote a commit message, so the ~20 KB they add went unused on every spawn — below the ">50% of invocations" preload bar in ai-agent-creator.

**Two hardcoded critical rules**: "FACT-BASED CONTENT ONLY" and "AVOID AI-KNOWN CONTENT" are in the agent system prompt directly (lines 19-52), not in skills. **Why:** these rules must apply BEFORE any skill loads — prevents generated noise from entering artifacts during the skill-loading decision phase.

**Thin router pattern exceeded**: ai-manager-agent's system prompt is ~84 lines body (98 with frontmatter) — significantly over the <50 line guideline. **Why justified:** the two critical rules (FACT-BASED, AVOID AI-KNOWN) at lines 19-52 must live in the system prompt, not skills. The decision tree (lines 79-87) and orchestration pattern (lines 89-98) are the routing logic; all domain knowledge comes from skills.

## Cross-References

- `../CLAUDE.md` — repo overview, self-referential system explanation
- `../skills/CLAUDE.md` — the 6 meta skills this agent uses (4 preloaded)
- `../commands/CLAUDE.md` — all commands invoke this agent via `subagent_type="ai-manager-agent"`
