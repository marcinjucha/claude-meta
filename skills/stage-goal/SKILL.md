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
- **A point whose result is a judgment (screenshots viewed, a language check, an inventory, a click-through, a guard
  switched off by hand) ends with a backticked proof line PRINTED BY A SCRIPT the point names BEFORE the line** — the
  script compares a deterministic item list with a subagent's per-item report; never a `NAME: n/m` the model writes,
  even with a printed list beside it. course-platform example: `python3 scripts/judgment_report.py tally HLC|ZRZUTY
  <expected> <report>` prints `HLC: n/m obejrzane, k usterek, j brakujących` (`expected strings|shots` lists the
  items, the subagent writes `<id> | ok|usterka | <note>`). No such script in the repo → write one before the stage
  or drop the proof from the goal. `check` warns on a judgment point without a proof line, and on a proof line no
  script precedes. WHY: a model-written count got a new standard from the hook each round — Ustawienia marki
  2026-11-12 (four refusals: HLC on part of 49 strings, inventory without per-entry evidence, one brand's sheets),
  Płatności i wideo marki 2026-11-13 (`ZRZUTY` without n: 3/3 counted, real 12 per brand); Funkcje marki 2026-11-14:
  `HLC: 17/17 tekstów` from a subagent was refused ~8 times („the skill's own output” — a skill has none) until
  `/goal clear`, and `ZRZUTY` passed only on a per-file subagent report.
- **A security point names the wall the stage ADDS (database / adapter / server fn) and demands a guard-off proof only
  where that refusal is the ONLY wall on its path**; a refusal the database repeats gets a recorded reason, not a
  proof. WHY: same stage — „strażniki server fn wyłączone ręcznie” for panel fns the database refuses anyway (cutting
  the fn check changes no outcome, so no proof can exist; Marcin: „nie rozumiem tego”), and a playback point already
  met by walls proven a stage earlier. Paste-ready wording: skeleton point 3.
- **Decision markers:** `[decyzja Marcina]` = ask Marcin before that increment; `[do decyzji w decisions.md]` =
  decide yourself and record it with the rejected variants. The legend goes in the spec's intro.
- **„Poza zakresem:” as ONE line.** The script lifts it into the goal; a multi-line scope cannot be lifted.
- **Increments, each with its own review + commit, whole-stage review last.** A stage is several increments, so its
  last round is REQUIRED to be `/code-review high` on the whole-stage diff (stage base..HEAD): AT MOST 3 rounds, the
  loop ends earlier after a round with zero confirmed findings OR with only narrower cases than the previous round;
  every round's prompt carries the likelihood filter (fix only what normal use hits, another brand's or buyer's data,
  data loss, wrong amounts); everything else goes to the repo's `decisions.md` as accepted classes. A change outside a stage
  gets the same loop when it exceeds ~300 changed lines or touches schema, migrations, permissions or payments,
  otherwise ONE `/code-review medium` round, no loop. WHY: Marcin 2026-11-17 — „zależy mi na tym, żeby jakość kodu była wysoka. Jak jest dużo zmian, to
  chcę mieć pełen przegląd. Jedynie nie chcę, żeby to było nadużywane”; in Raport sprzedaży five rounds added
  cache/refetch guards that an audit then removed. Origin of the whole-stage round: pezetpetki-hub Strona i blog,
  2026-11-07 — four whole-stage rounds said "zero findings", `/code-review high` still found normal-use bugs, and
  three full proof runs went to SHAs that then changed. Closing order = whole-stage review → its fixes and Boy Scout
  commits → code frozen → final proofs; nothing but docs after the first final proof (Marki, 2026-11-11: the final SHA
  moved four times, each move = a full new proof set). The round that ends the loop runs on the final SHA. [do
  potwierdzenia] open: what happens when a round-3 fix changes code (the cap allows no fourth round).
- **Closing block „Zamknięcie (dla stop hooka):” on ONE line**, shape:
  - final SHA = last commit touching code, tests, migrations, `ops/` or the proof script; docs-only commits need
    no new proofs or review;
  - every proof on the final SHA with its pasted output line (the repo's proof list);
  - every per-SHA proof the repo needs, conditional ones named with their condition (course-platform:
    `OPS CHECK: OK` when the stage changed `ops/`). WHY: a proof the block does not name, the hook may invent or
    skip (Marki: it demanded check-ops mid-loop, unlisted);
  - final review = the capped `/code-review high` loop above. It REPLACES the repo proof item „wynik ostatniej rundy
    przeglądu całego etapu („zero potwierdzonych znalezisk”)” — never add a second review item (the hook could demand
    two reviews). Clause (+321 chars over the old item; source `evals/stop-hook/conditions/E2.md`): „`/code-review
    high` baza..finalny SHA, najwyżej 3 rundy, poprawki przed zamrożeniem kodu, reszta jako przyjęte klasy w
    decisions.md: `CODE-REVIEW: <SHA>, rundy: <N>, ostatnia: 0 potwierdzonych|tylko węższe niż poprzednia|limit 3,
    przyjęte klasy: <K>` (K = wpisy ostatniej rundy w decisions.md, 0 przy zerze potwierdzonych), oparta na wyjściu
    narzędzia pokazanym w tej sesji, nie na samym zapewnieniu”. Budget it: Funkcje marki's goal had 8 chars left. The line
    rests on the review's tool output in the transcript (the forked Skill result), never typed by the model (same
    reason as the judgment-proof rule above); a capped ending with accepted findings is a valid close. The old line
    `CODE-REVIEW: 0 potwierdzonych na <SHA>` and „do zera” could never close a capped loop. `check` FAILs a closing
    line without `/code-review high`, without a `CODE-REVIEW:` line, or with the old shape. [do potwierdzenia] eval 2026-11-17
    (haiku, 10 reps per case, gold met/unmet/met): without the K gloss (E) `final-round-shown` 7/10 and 6/10 (the
    judge wanted decisions.md entries behind „przyjęte klasy: 0”), `asserted-only` 10/10 ×2, `capped-accepted`
    8/10 and 9/10; with it (E2) 8/10, 10/10, 10/10, `shown-handoff-tail` 9/10. Old item (DR) on the same excerpt:
    `final-round-shown` 10/10, `handoff-tail` 10/10, `capped-accepted` 0/10 — the new clause buys the capped close
    at the cost of a stricter judge on a complete one. E2's misses: the Marki ZRZUTY filter (fixture), and once the
    likelihood filter in the review prompt read as „a self-written narrowed filter” against `/code-review high`. E2
    was worded after seeing these cases, so the mark stays until a fresh case set or a real stage close passes it.
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
  - no pause clause: the dependable stop is `/goal clear` from outside the session, nothing in the condition. WHY:
    the real hook refused the clause (Marki, 2026-11-11: „wymienienie braków nie spełnia warunku”);
  - if the hook refuses a close the worker holds complete: ONE message with the proof state (the full „Dowody na
    <SHA>”, what the hook demands, „cel do wyczyszczenia”), then end the turn; no further reworks or reply variants.
    The person clears the goal; under the Discord bridge nobody can type, so the coordinator sends a `goal` action
    with condition „clear”. WHY: Raport sprzedaży, 2026-11-17 — five of nine refusals got a bare „Wpisz
    `/goal clear`”, the hook judged that line as the close („the assistant's last message is only `/goal
    clear`”), Claude Code cut the loop after 9 refusals (`CLAUDE_CODE_STOP_HOOK_BLOCK_CAP`) and the bridge got an
    empty report;
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

`check` FAIL: over limit · no done marker · no closing block · closing without `/code-review high`, without a
`CODE-REVIEW:` line, or with the uncapped shape (`reviewOldForms`) · no pointer to the spec or no back-pointer · point
numbering differs from the spec (a point was lost). WARN: process line with the uncapped review (`reviewOldForms`) · compressed points · closing or process line differs from
its source · scope line not in the goal · spec lacks advisor/scope line · a point names a human/process action
(stems in `goal-strings.json` `humanActionStems`) with no backticked `NAME: …` proof line · a proof line with no
script named before it in its point (`scriptRefForm`: `scripts/` or a `.py`/`.sh` name).

Assembled goal = intro (template) + spec points verbatim + „Poza zakresem” line (only if total ≤ 4000) + process
line + spec closing line verbatim.

Polish strings (markers, intro, titles, quote characters) live in `scripts/goal-strings.json`, never in the Python
source. WHY: Polish literals in Python source have crashed or silently dropped diacritics in this setup.

## Anti-patterns

- ❌ One goal file holding the whole spec → over 4000, `/goal` refuses it.
- ❌ Editing a point only in `<stage>.md` → the spec and the goal disagree; the next build overwrites it.
- ❌ A closing block that lists only proofs → the hook blocks on out-of-scope items and docs-only commits.
- ❌ A judgment point without a proof line, or a proof line the model writes instead of a script printing it → the
  hook invents a standard per check-in and the stage never closes.
- ❌ A pause clause in the closing block → the hook refuses it anyway; stopping is `/goal clear` from outside.
- ❌ Answering each refusal of a complete close with „wpisz /goal clear” → the hook judges that line as the close,
  the 9-refusal cap ends the run and the report is empty; one proof-state message, then the coordinator clears.
- ❌ A review rule „repeated until zero confirmed findings” → no cap, the loop adds guards for ever narrower cases.
- ❌ Copying the course-platform proof list into another repo's goal → wrong proofs, a stage that can never close.
