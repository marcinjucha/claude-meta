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

## Answers to Marcin: lead with the point, no walls of text (global behavior)

**Write the smallest thing that carries the decision.** Conclusion or recommendation FIRST, then only
the reasoning that changes what he does next. Cut: preambles, recaps of what he just said, restating
what a subagent already returned, listing options I am not recommending, and closing summaries of a
message he can still see. Prefer a few lines over a section-per-thought; add structure (tables,
headers, bullets) only when the content is genuinely parallel — never as decoration. When something
long IS the deliverable (a draft, a script, a diff), that artifact can be long; the message around it
stays short. **Why:** a wall of text is noise he has to parse to find the one line that matters, and
a long answer reads as thorough while actually shifting the work of finding the point onto him. Same
discipline as `human-language-check`, turned on my own output instead of reader-facing copy. Applies
to EVERY response, including reports from multi-phase commands and relays of subagent results.

**The same razor on every DELIVERABLE, not just chat: keep what the RECIPIENT needs in order to act
or decide; cut everything that documents MY process.** Origin (2026-07-29): a message to a coach cut
from ~700 to ~330 words — „teraz mi się podoba, zawsze pisz zwięźle, usuwaj cały noise". What was
load-bearing is WHAT went: a paragraph on how a format change worked out and three things that turned
out differently than I assumed — all true, none of it the recipient's business, and the document
existed to get three answers. Test per paragraph: „does the recipient need this to answer or decide?"
When cutting, record the REASON in operator scaffolding (file header) so a week later the cut doesn't
look like a loss. This is the parent rule whose instances are „notatki: czyść, nie dodawaj"
(2026-06-21) and „shared running doc = essence only, one language" (2026-07-21).

## Reviewing work WITH Marcin: one unit per turn, and show the framework's labels (global behavior)

**Walk a long artifact BLOCK BY BLOCK in conversation — one block per message, ONE recommendation,
closed question.** Format that carried a 13-block script without stalling: quote the block → one line
on what it does and what it deliberately lacks → AT MOST one proposed change → „bierzemy?". Second
variants, side remarks and meta-analysis either drop or go as a separate line marked „do Twojej
decyzji". **Why:** Marcin's own words — „bo ja się gubię i nie wiem, na czym się skupić". The same 27
findings delivered in bulk are unprocessable in chat; delivered per block they pass without friction.

**For a BATCH of corrections, build a walkthrough FILE to arbitrate item by item** — each item with
its WHY and its SOURCE, and mark CITATION-of-canon separately from MY-READING-of-canon. **Why:** a
silent batch rewrite hides which edits rest on doctrine and which rest on my inference, so the weakest
edits ship with the same authority as the strongest. The reading-of-canon ones are exactly what he
wants to decide.

**When applying ANY named framework, render it EXPLICITLY LABELLED with concrete steps** (Mean/Know/
So-what, Value Equation, Grand Slam steps, awareness stages, launch phases…) — walk the work through
each labelled step instead of folding the conclusion in silently. **Why:** the visible structure
teaches him to apply the framework himself; a silently applied framework gives the answer but not the
method.

## Pliki z copy: sam gotowy tekst, uzasadnienia OSOBNO (global behavior)

**Plik z copy zawiera WYŁĄCZNIE tekst do wklejenia.** Nagłówek powierzchni i pod nim treść. ZERO
bramek, cytatów doktryny, „powodów wycięcia", tabelek „linijka → robota" i notatek o proweniencji
wplecionych między akapity. Plik ma się czytać jak dokument, nie jak protokół z audytu — bo Marcin
wchodzi do niego RĘCZNIE, przepisuje zdanie po swojemu i zamyka, a każde zdanie operatorskie obok
copy jest wtedy przeszkodą, nie pomocą. **Why:** artefakt i uzasadnienie artefaktu to dwa różne
dokumenty dla dwóch różnych odbiorców; sklejone w jeden plik obniżają jakość obu — copy tonie
w scaffoldingu, a uzasadnienia nikt nie czyta, bo są porozrzucane.

**Uzasadnienia idą do pliku obok** (`<nazwa>-decyzje.md`) i TYLKO te, które coś kosztują w przyszłości:
dlaczego coś NIE wraca · na czym stoi warunek, którego złamanie unieważnia powierzchnię · co jest
świadomie różne między powierzchniami, żeby następny przegląd nie zgłosił tego jako błędu. Reszty NIE
przenosisz do drugiego pliku — przestajesz ją pisać.

**Historia zmian to NIE uzasadnienie — domyślnie nie powstaje.** „Wycięliśmy linijkę X", „wcześniejsza
wersja brzmiała Y", „rozważone i odrzucone warianty", tabelki „linijka → robota" — to kronika procesu
i jest szumem w obu plikach. `-decyzje.md` niesie wyłącznie to, co WIĄŻE PRZYSZŁE edycje, i to
sformułowane jako reguła, nie jako opowieść: zakaz zostaje zakazem („⛔ cena nie wchodzi na powierzchnię
przypiętą, bo jest jedynym ruchomym parametrem"), bez historii tego, kto i kiedy ją stamtąd wyjął.
**Próg na notatkę o zmianie: tylko ZNACZĄCA zmiana** — taka, która unieważnia wcześniejsze
rozstrzygnięcie albo zmienia architekturę powierzchni (np. kanał → grupy). Wtedy notatka ma wartość.
Każda inna zmiana ma zostać po prostu WYKONANA. **Why:** przy pracy blok po bloku zmian są dziesiątki
na sesję; zapisywanie każdej zamienia dokument decyzyjny w log, w którym te dwie albo trzy naprawdę
wiążące rzeczy przestają być widoczne.

**Wersja w pliku jest ŹRÓDŁEM PRAWDY, także gdy Marcin zmienił ją ręcznie.** Przed każdą edycją czytaj
plik od nowa; nigdy nie nadpisuj jego zmian wersją sprzed nich. Jeśli uznasz jego zmianę za błąd —
POWIEDZ to, nie poprawiaj po cichu. **Why:** pracujemy na tym samym pliku naprzemiennie, więc cicha
nadpisana edycja wygląda identycznie jak jej brak.

**Robota idzie do PLIKU, nie do czatu.** W czacie zostaje to, co wymaga jego decyzji, oraz blok, który
akurat przechodzimy blok po bloku (reguła wyżej) — poza tym wystarczy werdykt („wyciąłem drugą
linijkę, powód w `-decyzje`"). **Why:** ten sam tekst w dwóch miejscach rozjeżdża się natychmiast,
a czat nie jest powierzchnią, którą da się edytować.

**Test przed zapisaniem czegokolwiek do pliku z copy:** czy to jest tekst, który zobaczy CZYTELNIK?
Nie → to nie jest miejsce na to. Origin (2026-09-21): plik z trzema powierzchniami kanału WhatsApp
Kacpra urósł do postaci, w której między akapitami copy siedziały bramki, warunki i powody wycięcia —
„nie chcę, aby one mi zaśmiecały całość".
