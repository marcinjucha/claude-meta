export const meta = {
  name: 'audit-claude-artifacts',
  description: 'Read-only audit of ~/.claude agents, commands, skills and the brain-* family, with adversarial verification of every finding',
  whenToUse: 'Quarterly audit of the artifact ecosystem. First run: python3 ~/.claude/scripts/artifact-usage.py > usage.tsv, then pass args {usage: <tsv text>, groups?: [keys]}.',
  phases: [
    { title: 'Audit', detail: 'one auditor per artifact group' },
    { title: 'Verify', detail: 'one skeptic per group re-checks every finding from scratch' },
  ],
}

// args.usage  — stdout of ~/.claude/scripts/artifact-usage.py (required: the audit judges by real use)
// args.groups — optional subset of GROUPS keys; default = all (8 groups → 16 agents)
// Output goes into a walkthrough file (01-Projects/brain/audyt-claude-<rrrr-mm>.md) reviewed one item per turn.

const USAGE = args && args.usage
if (!USAGE) throw new Error('args.usage missing: run python3 ~/.claude/scripts/artifact-usage.py and pass its output')

const BRAIN = '/Users/marcinjucha/Prywatne/projects/brain-vault/.brain/.claude'

const COMMON = `
You are auditing Claude Code artifacts of Marcin: the native ~/.claude meta toolchain and the brain-* family
(SOURCE in ${BRAIN}/; ~/.claude/commands/brain-*.md, agents/brain-manager.md and skills/brain-conventions are symlinks to it).
STRICTLY READ-ONLY: no edits anywhere (also not through symlinks), scratch files only under /tmp; never run
~/.claude/evals/skill-ab.py run/calibrate (costs money); sync-knowledge.py only with --check; never git checkout/commit.
Shell traps: grep is ugrep and can print NOTHING on Polish or single-line text even when matches exist — search/count
with python3 (open().read().count(), re.finditer). Silence is not absence. zsh: quote globs.
Out of scope: third-party skills (gitignored emilkowalski skills, taste-skill plugin, skills/synced/) — never propose edits.

Usage counts from session transcripts (window = earliest timestamp on the first line), already computed — do not recount:
${USAGE}
Column notes: slash_typed counts <command-name> tags, which also appear when an agent PRELOADS a skill via frontmatter —
a load count, not proof a human typed it. Skill_calls = explicit Skill tool calls. Agent_spawns = Agent/Task calls.
Transcripts for real cases: ~/.claude/projects/**/*.jsonl (incl. */subagents/*.jsonl). Lessons about the system:
brain-vault/01-Projects/brain/memory.md. The previous audit and its decisions: brain-vault/01-Projects/brain/audyt-claude-*.md —
do not re-propose what a previous audit already decided against, unless new evidence appears.

Judge per artifact: state (healthy / needs-work / stale / unused) and concrete proposals. Look for: facts no longer true
(paths, counts, file lists, moved/merged repos); contradictions between artifacts, engine scripts or CLAUDE.md files; dead
references; steps the model routinely skips or overrides in real transcripts (the instruction does not change behaviour →
noise or wrong); real failures a missing or unclear rule caused; context cost of long text that repeats what another loaded
file carries or what the model already knows; description problems for artifacts the model picks from description;
artifacts with 0 use — does anything call them, should they stay, be fixed or be archived.

LIKELIHOOD FILTER (Marcin's rule): report only what normal use triggers, or what causes data loss / exposure of another
person's data. DO NOT REPORT: documentation drift that changes no behaviour, style or wording polish, theoretical edge
cases, rare two-session races, features nobody asked for.

EVIDENCE RULE (the audit separates proven improvements from guesses): every finding carries
- evidence: exact file path + verbatim quote (or command + output) proving the problem exists NOW;
- failing_case: a REAL case (transcript path + quote, buffer entry, commit) where the current text failed or cost
  something, or null → then hypothesis=true; keep it but do not dress it up;
- eval_type: 1 = a discrete model decision measurable with skill-ab.py against a human gold set (name the decision and
  where cases come from); 2 = generated text (assertions / calibrated judge); 3 = multi-step tool work; 0 = factual fix.
Write claim/proposal fields in Polish, plain and concise; quotes verbatim in their original language.`

const FINDINGS = {
  type: 'object',
  properties: {
    artifacts: { type: 'array', items: { type: 'object', properties: {
      path: { type: 'string' }, state: { type: 'string', enum: ['healthy', 'needs-work', 'stale', 'unused'] },
      summary: { type: 'string' } }, required: ['path', 'state', 'summary'] } },
    findings: { type: 'array', items: { type: 'object', properties: {
      id: { type: 'string' }, path: { type: 'string' }, location: { type: 'string' },
      kind: { type: 'string', enum: ['stale-fact', 'contradiction', 'dead-reference', 'noise', 'missing-rule', 'duplication', 'description', 'unused', 'other'] },
      claim: { type: 'string' }, evidence: { type: 'string' }, failing_case: { type: ['string', 'null'] },
      hypothesis: { type: 'boolean' }, likelihood: { type: 'string', enum: ['normal-use', 'data-loss', 'rare'] },
      proposal: { type: 'string' }, eval_type: { type: 'integer', enum: [0, 1, 2, 3] } },
      required: ['id', 'path', 'location', 'kind', 'claim', 'evidence', 'failing_case', 'hypothesis', 'likelihood', 'proposal', 'eval_type'] } },
  },
  required: ['artifacts', 'findings'],
}

const VERDICTS = {
  type: 'object',
  properties: { verdicts: { type: 'array', items: { type: 'object', properties: {
    id: { type: 'string' }, verdict: { type: 'string', enum: ['confirmed', 'refuted', 'partly'] },
    evidence_found: { type: 'string' }, failing_case_real: { type: 'boolean' },
    likelihood_ok: { type: 'boolean' }, note: { type: 'string' } },
    required: ['id', 'verdict', 'evidence_found', 'failing_case_real', 'likelihood_ok', 'note'] } } },
  required: ['verdicts'],
}

const ALL_GROUPS = [
  { key: 'meta-core', scope: `the meta toolchain core: ~/.claude/agents/ai-manager-agent.md, ~/.claude/agents/CLAUDE.md, ~/.claude/skills/CLAUDE.md, every ~/.claude/skills/ai-*/ skill (SKILL.md + all files) and ~/.claude/skills/resources/. Compare against official docs in ~/.claude/docs/ where an artifact states how Claude Code works.` },
  { key: 'ai-commands', scope: `the ai-* artifact commands in ~/.claude/commands/ (ai-agent, ai-skill, ai-commands, ai-curate-memory, ai-extract-memory, ai-git and any other ai-*.md) plus ~/.claude/commands/CLAUDE.md. Check duplication with the skills ai-manager-agent preloads, consistency of the 'artifact writes go through ai-manager-agent' rule, and the brain-vault per-context memory buffer behaviour (brain-vault CLAUDE.md) for the memory commands.` },
  { key: 'other-native', scope: `every other native command and skill in ~/.claude (commands that are not ai-* and not brain-*, e.g. council, improve-process, website; tracked skills that are not ai-*, brain-* or third-party, e.g. human-language-check, brainstorming). For description-routed skills eval_type 1 is realistic — name the concrete decision a skill-ab suite would measure.` },
  { key: 'registry', scope: `registry consistency: ~/.claude/CLAUDE.md Structure section vs what is on disk (counts, lists, symlinks, tracked vs untracked: git -C ~/.claude ls-files), and ~/.claude/settings.json hooks vs what CLAUDE.md says about them. Report only drift that misleads a session into a wrong action.` },
  { key: 'brain-session', scope: `${BRAIN}/commands/{brain-load,brain-update,brain-finish}.md — the most used flow. Check transcripts for steps skipped or done differently than written, and for repeated corrections from Marcin. Engine docs: brain-vault/.brain/CLAUDE.md, .brain/docs/, .brain/scripts/.` },
  { key: 'brain-knowledge', scope: `${BRAIN}/commands/{brain-extract-knowledge,brain-knowledge,brain-knowledge-init,brain-knowledge-migrate}.md, ${BRAIN}/skills/brain-conventions/ and ${BRAIN}/agents/brain-manager.md. Contract: brain-vault/_system/knowledge-system.md. Evals that already settled a decision live in brain-vault/.brain/evals/ — do not re-litigate them without new evidence.` },
  { key: 'brain-meeting', scope: `${BRAIN}/commands/brain-meeting.md and any file it delegates agent text to — judge whether its size is earned: which parts transcripts show the model following vs skipping, and real failures.` },
  { key: 'brain-rest', scope: `every remaining command in ${BRAIN}/commands/ not covered by brain-session, brain-knowledge or brain-meeting (e.g. brain-sync, brain-publish), plus brain-vault/.claude/commands/ (go-to-market commands loaded only in the vault). For each with 0 use: does anything call it, is it broken by later changes, stay / fix / archive.` },
]

const wanted = args.groups && args.groups.length ? new Set(args.groups) : null
const GROUPS = wanted ? ALL_GROUPS.filter(g => wanted.has(g.key)) : ALL_GROUPS
if (wanted) log(`groups: ${GROUPS.map(g => g.key).join(', ')} (skipped ${ALL_GROUPS.length - GROUPS.length})`)

const results = await pipeline(
  GROUPS,
  g => agent(`${COMMON}\n\nYOUR SCOPE: ${g.scope}\n\nRead every file in scope fully. Return artifacts[] (one row per artifact in scope) and findings[] (ids prefixed '${g.key}-').`,
    { label: `audit:${g.key}`, phase: 'Audit', schema: FINDINGS }),
  (audit, g) => {
    if (!audit) return null
    if (!audit.findings.length) return { group: g.key, audit, verdicts: [] }
    const bare = audit.findings.map(f => `- ${f.id} | ${f.path} @ ${f.location} | claim: ${f.claim} | stated failing_case: ${f.failing_case ?? 'none'}`).join('\n')
    return agent(`Adversarial verifier for an audit of Claude Code artifacts (~/.claude and brain source ${BRAIN}). STRICTLY READ-ONLY (no edits, no skill-ab.py run/calibrate). grep can silently print nothing here — search/count with python3; silence is not absence.
For EACH claim below: open the file yourself, locate the evidence independently, and try to REFUTE it. Default to 'refuted' without positive proof; 'partly' = core true but overstated or the proposal targets the wrong spot.
failing_case_real: does the stated case exist and show what is claimed (open it)? likelihood_ok: would normal use trigger it (rare / theoretical / doc-only = false; data loss or exposure of another person's data = true)?
Write evidence_found and note in Polish, concise, quotes verbatim.

Claims:
${bare}`, { label: `verify:${g.key}`, phase: 'Verify', schema: VERDICTS })
      .then(v => ({ group: g.key, audit, verdicts: v ? v.verdicts : null }))
  },
)
return results.filter(Boolean)
