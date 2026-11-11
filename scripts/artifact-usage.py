"""Usage counts of ~/.claude agents, commands and skills from session transcripts.

Input for the audit-claude-artifacts workflow (pass the stdout as args.usage).
Transcripts live in ~/.claude/projects/**/*.jsonl (incl. subagents); Claude Code
prunes them, so the window is whatever is on disk (printed as the earliest timestamp).
Usage: python3 ~/.claude/scripts/artifact-usage.py > usage.tsv
"""
import json, re, sys, glob, os, collections
home = os.path.expanduser('~/.claude')
names = set()
for d in ['agents', 'commands']:
    for f in os.listdir(f'{home}/{d}'):
        if f.endswith('.md') and f != 'CLAUDE.md':
            names.add((d, f[:-3]))
for f in os.listdir(f'{home}/skills'):
    if os.path.isfile(f'{home}/skills/{f}/SKILL.md'):
        names.add(('skills', f))
cmd = collections.Counter(); skill = collections.Counter(); agent = collections.Counter()
skill_by_parent = collections.Counter()  # skill call made inside main session vs subagent
files = glob.glob(f'{home}/projects/**/*.jsonl', recursive=True)
first = None
cmd_re = re.compile(r'<command-name>/?([\w:.-]+)</command-name>')
for p in files:
    sub = '/subagents/' in p
    try:
        fh = open(p, encoding='utf-8', errors='replace')
    except Exception:
        continue
    for line in fh:
        if 'command-name' in line:
            for m in cmd_re.findall(line):
                cmd[m] += 1
        if '"tool_use"' not in line:
            continue
        try:
            o = json.loads(line)
        except Exception:
            continue
        ts = o.get('timestamp')
        if ts and (first is None or ts < first):
            first = ts
        content = (o.get('message') or {}).get('content')
        if not isinstance(content, list):
            continue
        for c in content:
            if c.get('type') != 'tool_use':
                continue
            inp = c.get('input') or {}
            if c.get('name') == 'Skill':
                s = str(inp.get('skill', ''))
                skill[s] += 1
                if sub: skill_by_parent[s] += 1
            elif c.get('name') in ('Agent', 'Task'):
                agent[str(inp.get('subagent_type', ''))] += 1
# frontmatter skills: lists in agents (global + vault + claude-dev)
fm = collections.Counter()
for p in glob.glob(f'{home}/agents/*.md') + glob.glob(os.path.expanduser('~/Prywatne/projects/brain-vault/.claude/agents/*.md')) + glob.glob(os.path.expanduser('~/Prywatne/projects/claude-dev/agents/*.md')):
    t = open(p, encoding='utf-8').read()
    m = re.search(r'^skills:\s*\n((?:\s+-.*\n)+)', t, re.M)
    if m:
        for s in re.findall(r'-\s*([\w:-]+)', m.group(1)):
            fm[s] += 1
    m = re.search(r'^skills:\s*\[(.*?)\]', t, re.M)
    if m:
        for s in re.split(r'[,\s]+', m.group(1)):
            if s: fm[s.strip('"\'')] += 1
print('transcripts:', len(files), 'earliest tool_use ts:', first)
rows = []
for d, n in sorted(names):
    rows.append((d, n, cmd.get(n, 0), skill.get(n, 0), skill_by_parent.get(n, 0), agent.get(n, 0), fm.get(n, 0)))
print('kind\tname\tslash_typed\tSkill_calls\t(of which in subagents)\tAgent_spawns\tfrontmatter_preloads')
for r in rows:
    print('\t'.join(map(str, r)))
