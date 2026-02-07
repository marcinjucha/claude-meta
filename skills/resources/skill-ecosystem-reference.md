# Skill Ecosystem Reference

Condensed guide covering skill locations, sharing, permissions, and related resources. Extracted from official Claude Code skills documentation.

---

## Skill Locations and Priority

Where you store a skill determines who can use it and what priority it has.

### Location Hierarchy

| Location   | Path                                             | Applies to                     | Priority |
|:-----------|:-------------------------------------------------|:-------------------------------|:---------|
| Enterprise | See managed settings docs                        | All users in organization      | 1 (highest) |
| Personal   | `~/.claude/skills/<skill-name>/SKILL.md`         | All your projects              | 2 |
| Project    | `.claude/skills/<skill-name>/SKILL.md`           | This project only              | 3 |
| Plugin     | `<plugin>/skills/<skill-name>/SKILL.md`          | Where plugin enabled           | Namespaced |

### Priority Resolution

When skills share the same name across levels:

```
Priority order: enterprise > personal > project

Example:
├─ Enterprise: data-patterns (v2)
├─ Personal: data-patterns (v1)      ← Ignored (lower priority)
└─ Project: data-patterns (v1)        ← Ignored (lower priority)

Result: Enterprise version wins (v2)
```

**Plugin skills use namespacing:**
- Format: `plugin-name:skill-name`
- Cannot conflict with other levels
- Example: `/my-plugin:analyze`

**Legacy commands:**
- Files in `.claude/commands/` still work (same frontmatter support)
- If skill and command share name → skill takes precedence

### Automatic Discovery (Nested Directories)

Claude Code automatically discovers skills from nested `.claude/skills/` directories.

**Use case: Monorepos with package-specific skills**

```
monorepo/
├── .claude/skills/           # Root skills (all packages)
│   └── shared-patterns/
├── packages/
│   ├── frontend/
│   │   └── .claude/skills/   # Frontend-specific skills
│   │       └── ui-patterns/
│   └── backend/
│       └── .claude/skills/   # Backend-specific skills
│           └── api-patterns/
```

**How discovery works:**
- Working in `packages/frontend/` → Claude finds both root skills AND `frontend/.claude/skills/`
- Working in `packages/backend/` → Claude finds both root skills AND `backend/.claude/skills/`

**Priority:** Nested directory skills are treated as project-level (same as `.claude/skills/` at root).

---

## Sharing Skills

### Method 1: Project Skills (Version Control)

Commit `.claude/skills/` to git → team members get skills automatically.

```bash
# Add to version control
git add .claude/skills/my-skill/
git commit -m "Add my-skill for team"
git push
```

**Pros:** Simple, automatic for team
**Cons:** Project-specific only

### Method 2: Plugins

Package skills with other extensions in a plugin.

```
my-plugin/
├── plugin.json
└── skills/
    ├── skill-1/
    │   └── SKILL.md
    └── skill-2/
        └── SKILL.md
```

**Pros:** Distributable, can include multiple skills, works across projects
**Cons:** Requires plugin setup

See: [Plugins documentation](https://code.claude.com/docs/en/plugins)

### Method 3: Managed Settings (Enterprise)

Deploy organization-wide through managed settings.

**Pros:** Central control, all users get skills, automatic updates
**Cons:** Enterprise only

See: [Managed settings documentation](https://code.claude.com/docs/en/iam#managed-settings)

---

## Permission Control

Control which skills Claude can invoke and what tools skills can use.

### Restrict Claude's Skill Access

**Three approaches:**

#### 1. Disable All Skills

Deny the Skill tool in `/permissions`:

```
# In permission rules (deny section)
Skill
```

Claude cannot invoke any skills programmatically. User can still invoke with `/skill-name`.

#### 2. Allow/Deny Specific Skills

Use permission rules to control specific skills:

```
# Allow only specific skills (allowlist)
Skill(commit)
Skill(review-pr *)

# Deny specific skills (denylist)
Skill(deploy *)
```

**Syntax:**
- `Skill(name)` - Exact match (e.g., `Skill(commit)`)
- `Skill(name *)` - Prefix match with any arguments (e.g., `Skill(review-pr *)`)

#### 3. Hide Individual Skills

Add `disable-model-invocation: true` to skill frontmatter:

```yaml
---
name: deploy
disable-model-invocation: true
---
```

This removes skill from Claude's context entirely. Only user can invoke with `/deploy`.

**Note:** `user-invocable: false` only hides from menu, doesn't block Skill tool access. Use `disable-model-invocation: true` to block programmatic invocation.

### Tool Permissions Within Skills

Skills can grant Claude permission to use specific tools without approval:

```yaml
---
name: safe-reader
allowed-tools: Read, Grep, Glob
---
```

**How it works:**
- When skill active → Claude can use listed tools without per-use approval
- User's permission settings still govern baseline behavior for other tools
- Example: Read-only analysis skill grants Read/Grep/Glob, blocks Edit/Write

**Common patterns:**

```yaml
# Read-only analysis
allowed-tools: Read, Grep, Glob

# Web research
allowed-tools: Read, Grep, WebFetch, WebSearch

# Code changes
allowed-tools: Read, Edit, Write, Bash
```

---

## Character Budget (Skill Descriptions)

Claude loads skill descriptions into context to know what's available. If you have many skills, descriptions may exceed character budget.

**Default budget:** 15,000 characters (covers ~30-40 skills)

**Check for warnings:**

```bash
/context
```

Look for message about excluded skills.

**Solutions:**

1. **Increase budget:**
   ```bash
   export SLASH_COMMAND_TOOL_CHAR_BUDGET=30000
   ```

2. **Shorten descriptions:**
   - Focus on triggers (when to use)
   - Remove examples from descriptions
   - Keep under 100 characters per skill if possible

3. **Use `disable-model-invocation: true`:**
   - Removes description from context (skill not auto-invokable)
   - Use for manual-only skills (like `/deploy`)

---

## Related Resources

**Official Documentation:**
- **Skills Guide:** https://code.claude.com/docs/en/skills
- **Skill Creation Best Practices:** https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
- **Agent Skills Spec (Open Standard):** https://agentskills.io
- **Interactive Mode (Built-in Commands):** https://code.claude.com/docs/en/interactive-mode#built-in-commands
- **Subagents:** https://code.claude.com/docs/en/sub-agents
- **Plugins:** https://code.claude.com/docs/en/plugins
- **Hooks:** https://code.claude.com/docs/en/hooks
- **Memory (CLAUDE.md):** https://code.claude.com/docs/en/memory
- **Permissions (IAM):** https://code.claude.com/docs/en/iam

**Internal Resources (In This Skill):**
- `@resources/signal-vs-noise-reference.md` - 3-question filter for content quality
- `@resources/why-over-how-reference.md` - WHY > HOW philosophy
- `@resources/skill-structure-reference.md` - Standard skill structure
- `@resources/skills-guide.md` - Complete official guide to skills
- `@resources/skill-template.md` - Copy-paste templates

---

## Quick Reference

**Skill Priority:**
```
enterprise > personal > project
(plugins namespaced as plugin-name:skill-name)
```

**Sharing:**
```
Project → git commit .claude/skills/
Plugin → Package in plugin/skills/
Enterprise → Managed settings
```

**Permissions:**
```
Block all skills → /permissions deny: Skill
Block specific skill → /permissions deny: Skill(deploy *)
Hide from Claude → disable-model-invocation: true
Grant tools → allowed-tools: Read, Grep, Glob
```

**Nested Discovery:**
```
packages/frontend/.claude/skills/ → Auto-discovered when in frontend/
```

**Character Budget:**
```
Check: /context
Increase: export SLASH_COMMAND_TOOL_CHAR_BUDGET=30000
Reduce: Shorten descriptions, use disable-model-invocation: true
```

---

**Key Insight:** Skills are modular, shareable, and controllable. Use location hierarchy for priority, plugins for distribution, and permissions for access control.
