---
name: stage-goal
description: Writes and checks the Claude Code `/goal` condition for a multi-increment BUILD STAGE in a code repo (docs/goals/STAGE.md + STAGE-wymagania.md), which the stop hook judges literally from the condition text and the transcript. Builds the ≤4000-char goal from the spec with a script and checks length, closing block, points and pointers. Trigger on "/goal", "napisz cel etapu", "cel dla stop hooka", "warunek /goal", "rozbij cel na wymagania", "goal za długi", "Goal condition is limited to 4000", "docs/goals", "-wymagania.md", "stage goal", "stop hook goal". NOT the brain vault's "blok celu" / goal checklist in CO TERAZ notes (_system/templates/goal-checklist.md, /brain-update) — this is a repo stage's /goal condition, never vault work.
---

# Stage goal — `/goal` condition for a build stage

Scope: a repo build stage run under `/goal` (course-platform, pezetpetki-hub). Not the vault's CO TERAZ goal
checklist — both are called "cel", keep them apart.

## How the condition is judged (facts)

- **The stop hook sees only the condition text and the transcript, and reads the text literally.** Origin:
  pezetpetki-hub Monitoring, 2026-11-06 — a docs-only commit demanded the one-hour proof again, „Poza zakresem”
  items and a proposal handed to Marcin blocked closing, a proof without a pasted output line did not count.
  Marcin: „musimy lepiej definiowac stop hook”.
- **`/goal` refuses a condition over 4000 characters** ("Goal condition is limited to 4000 characters (got 6980)",
  Marki, 2026-11-10). All seven multi-brand stage goals were over it as single files.
- **Unit = characters of the text after `/goal `, trailing newline stripped** (Python `len()`; reproduces 6980 on
  Marki at `c6a52ee`). `wc -c` counts bytes and overstates Polish text — never measure with it.

## Two files per stage

| File | Holds | Read by |
|------|-------|---------|
| `docs/goals/<stage>-wymagania.md` | full spec: product decisions, dependencies, marker legend, numbered points, „Poza zakresem”, pasted repo rules, increments, advisor, closing block | the working session |
| `docs/goals/<stage>.md` | `/goal` text: pointer to the spec + numbered points + „Poza zakresem” line (if it fits) + one process line + closing block | the stop hook |

**Why the points and the closing block sit in the goal and not only in the spec:** the hook judges the condition
text alone; a pointer does not make the spec part of the condition. [do potwierdzenia] whether the hook ever uses
spec content that reached the transcript — so the scope line goes in the goal whenever it fits.

**Edit the spec, then rebuild.** Points live in both files, so editing only the goal guarantees drift. A
hand-compressed goal (points too long to fit verbatim, e.g. Marki) is the one case where both files are edited by
hand; `check` reports it as compressed (WARN, not FAIL — a permanently red check stops being a gate).

## Spec content (skeleton: `resources/spec-skeleton.md`)

- **Numbered „Gotowe, gdy:” points, each verifiable from the transcript** (a pasted output line, a count, a named
  file). WHY: a point the hook cannot see satisfied reopens the stage at every check-in.
- **A point whose result is a human or process action (screenshots viewed, a language check, an inventory, a
  click-through, a guard switched off by hand) ends with its PROOF LINE in a fixed backticked form**, e.g.
  `INVENTORY: 0 bez rozstrzygnięcia (N pozycji)`, `ZRZUTY: marka A n/n, marka B n/n obejrzane`, `HLC: n/n tekstów`;
  the line must rest on tool output shown in this session (a list or table a tool printed), never on the assistant's
  claim alone. WHY: Ustawienia marki, 2026-11-12 — all proofs green, yet the hook refused closing four times with a
  new standard each round: human-language-check visible for part of 49 new strings, the inventory without per-entry
  evidence, screenshot sheets of brand B only. The points never said what the transcript must show, so the judge
  invented it. `check` warns on such a point without the form.
- **Decision markers:** `[decyzja Marcina]` = ask Marcin before that increment; `[do decyzji w decisions.md]` =
  decide yourself and record it with the rejected variants. The legend goes in the spec's intro.
- **„Poza zakresem:” as ONE line.** The script lifts it into the goal; a multi-line scope cannot be lifted.
- **Increments, each with its own review + commit, whole-stage review last.** Put the independent review with a
  different tool (e.g. `/code-review high`) and all its fixes BEFORE the long proof run. Origin: pezetpetki-hub
  Strona i blog, 2026-11-07 — four whole-stage rounds said "zero findings", `/code-review high` still found
  normal-use bugs, and three full proof runs went to SHAs that then changed. Closing order = whole-stage review to
  zero → its fixes and Boy Scout commits → code frozen → final proofs; nothing but docs after the first final proof
  (Marki, 2026-11-11: the final SHA moved four times, each move = a full new proof set).
- **Closing block „Zamknięcie (dla stop hooka):” on ONE line**, shape:
  - final SHA = last commit touching code, tests, migrations, `ops/` or the proof script; docs-only commits need
    no new proofs or review;
  - every proof on the final SHA with its pasted output line (the repo's proof list);
  - every per-SHA proof the repo needs, conditional ones named with their condition (course-platform:
    `OPS CHECK: OK` when the stage changed `ops/`). WHY: a proof the block does not name, the hook may invent or
    skip (Marki: it demanded check-ops mid-loop, unlisted);
  - all proofs in ONE message „Dowody na <SHA>”, copied from log files, each line with the SHA it ran on; the
    message opens with one line per numbered point (the increment's commit, or the point's `NAME: …` line resting on
    tool output shown in this session), then summary lines (`SUMMARY: 0 line(s) are not proofs`, `ALL ON: N passed`,
    test counts), never per-line output; point 0 (the run on the base SHA before changes), if the stage has one,
    also as summary lines. WHY: the hook reads only the transcript, compaction drops earlier pastes, and without
    SHAs it mixed point-0 and final proofs (Marki). The old wording „także linie bazowe” made the hook demand all 221
    `<GROUP> baseline '…'` lines the prove script prints (Ustawienia marki): name point 0, never „linie bazowe”.
    Tested Polish clause: `evals/stop-hook/conditions/C.md` (from „; wszystkie w jednej wiadomości” to „Nie
    blokuje”, 305 chars, +172 over the old one). „commit przyrostu” in it is load-bearing: requiring tool output for
    EVERY point made the eval judge refuse a complete close, since points proven in earlier increments have none.
    Never compress „oparta na wyjściu narzędzia pokazanym w tej sesji, nie na samym zapewnieniu”: eval 2026-11-13
    (haiku, 10 reps, `proof-line-asserted-only`), without it 0.20, with only „nie zapewnienie” 0.40, with it
    0.60–0.80. „Jeśli jest” at point 0 stays too: stages without a point 0 would get a proof demanded that cannot exist;
  - pause clause: Marcin's own message (not the assistant's) telling it to stop + the assistant's reply naming the
    missing proofs and their SHA = condition met for this session; the stage stays open, the next session sets
    `/goal` again. WHY: the hook knows only met/unmet and the assistant cannot pause a goal (Marki: „kończymy na
    dzisiaj” mid-proof → 7 re-prompts until `/goal clear`). [do potwierdzenia] that the hook honours it;
  - does NOT block: anything in „Poza zakresem”, `[do potwierdzenia]` needing external access, proposals handed to
    Marcin.

## Repo profile — read it, never copy it into this skill

Repo-specific text comes from the repo's `CLAUDE.md` "Stage process" section:
- the proof list for the closing block (e.g. course-platform: `pnpm check` count, `GIT_SHA` from the container,
  container e2e count, `SUMMARY: 0 line(s) are not proofs`, last whole-stage review round);
- Polish paste lines for the spec (review-by-likelihood rule, the two MUST rules, the „Advisor:” line);
- the **process line for the goal**: bullet labelled `Process line for the goal`, quoted „…” text, no inner
  quotation marks. The script copies it verbatim into every built goal.

**No "Stage process" section (e.g. agency-cms today):** ask Marcin for the proof list and the process line, then
propose adding them to that repo's CLAUDE.md. Never invent a proof list.

## Steps

1. Write/edit `<stage>-wymagania.md` from the skeleton; paste the repo lines from CLAUDE.md.
2. Run `human-language-check` on the spec (reader-facing Polish) — BEFORE building, so the goal inherits the
   cleaned points.
3. `build <stage>` (dry run) → read the length; then `build <stage> --write`.
4. Over the limit → nothing is written; the report lists per-point lengths. Compress the longest points in
   context (judgment, not script), write the goal by hand, keep point numbering identical to the spec.
5. `check <stage>` → no FAIL. Commit both files together.

## Script

`python3 ~/.claude/skills/stage-goal/scripts/stage_goal.py` — run from inside the repo; prints a short report.

| Command | Does |
|---------|------|
| `build <slug> [--dir docs/goals]` | dry run: assemble goal from spec + CLAUDE.md process line, report length and whether the scope line fit |
| `build <slug> --write [--force]` | write `<slug>.md`; refuses to replace a hand-compressed goal without `--force`; over limit → writes nothing, exit 1 |
| `check [<slug>\|all]` | `all` = only stages with a `-wymagania.md` sibling (legacy single-file goals listed as skipped) |

`check` FAIL: over limit · no done marker · no closing block · no pointer to the spec or no back-pointer · point
numbering differs from the spec (a point was lost). WARN: compressed points · closing or process line differs from
its source · scope line not in the goal · spec lacks advisor/scope line · a point names a human/process action
(stems in `goal-strings.json` `humanActionStems`) with no backticked `NAME: …` proof line.

Assembled goal = intro (template) + spec points verbatim + „Poza zakresem” line (only if total ≤ 4000) + process
line + spec closing line verbatim.

Polish strings (markers, intro, titles, quote characters) live in `scripts/goal-strings.json`, never in the Python
source. WHY: Polish literals in Python source have crashed or silently dropped diacritics in this setup.

## Anti-patterns

- ❌ One goal file holding the whole spec → over 4000, `/goal` refuses it.
- ❌ Editing a point only in `<stage>.md` → the spec and the goal disagree; the next build overwrites it.
- ❌ A closing block that lists only proofs → the hook blocks on out-of-scope items and docs-only commits.
- ❌ A human/process point without a proof line, or proof lines the assistant only asserts → the hook invents a
  standard per check-in and the stage never closes.
- ❌ No pause clause → a user's "stop for today" mid-proof turns into a hook loop until `/goal clear`.
- ❌ Copying the course-platform proof list into another repo's goal → wrong proofs, a stage that can never close.
