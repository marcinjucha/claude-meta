---
name: brainstorming
description: Iterative VARIANT-NARROWING loop run turn by turn with Marcin: each round gives 3 (max 4) genuinely different variants of ONE thing being designed (question wording, headline, survey, approach, plan) as a compact table + one recommendation + one closed question; his pick becomes the base of the next round, whose variants each push along a NAMED axis; repeats until HE says it is good enough, then records the final version + rejection CRITERIA so they don't return. Domain-agnostic. Trigger on "brainstorming", "burza mózgów", "zróbmy warianty", "daj warianty", "warianty do wariantu", "iterujmy", "zawęź to", "podaj kilka wersji", "brainstorm", "iterate on this", "give me variants", "narrow it down". DISTINCT from copy-walkthrough (walks an EXISTING multi-section artifact section by section — this generates alternatives for ONE unit), copy-write (one-pass write from a BRIEF), council (multi-agent fan-out to ONE synthesized answer; here Marcin chooses every round).
---

# Brainstorming — variant narrowing

One unit (one question, one headline, one approach) is narrowed round by round. Marcin chooses; the skill proposes and recommends. It is a loop, not a list of ideas.

## The loop

| Step | What happens | Why |
|---|---|---|
| **Round 1 — spread** | 3 (max 4) variants that differ in KIND, not in wording (open vs closed, question vs completion, pain vs curiosity). | Near-duplicates in round 1 hide the real fork; the first choice must be between directions. |
| **Marcin reacts** | Picks one, or rejects all with a reason ("za ogólny"). | His reason is the criterion for everything after. |
| **Round N — push the pick** | 3 variants OF the picked one. Each moves it along ONE named axis (narrower scope, different anchor/moment, register, sharper, safer, shorter…). Axes differ between the variants. | A named axis makes the choice legible: he picks a direction, not a random rewrite. Unnamed variants make him re-read everything to find the difference. |
| **Repeat** | Until HE says it is good enough. | The skill never declares "done". |
| **Finish** | Write final + lineage (below). | Without recorded criteria, rejected directions get re-proposed in the next review. |

**Hybrid on request, not by default:** if he says "B, ale z końcówką A", the next round's base is that hybrid, stated as a quote first.

## Turn format (every round)

```
Runda N — baza: „<quoted picked variant>" (odrzucone: <criterion>)

| | Wariant | Oś | Co daje | Minus |
|---|---|---|---|---|
| 1 | „<full text>" | <axis> | … | … |
| 2 | „<full text>" | <axis> | … | … |
| 3 | „<full text>" | <axis> | … | … |

Rekomenduję 2 — <one-line why, tied to his stated criterion>.
Bierzemy 2?

do Twojej decyzji: <at most one side remark, only if it matters>
```

- **Quote the variant text itself, in full.** Never "wariant bardziej konkretny" — he decides on words, not on descriptions of intent.
- **ONE recommendation, ONE closed question.** No "a może też…". A second idea either becomes a table row or goes to the single „do Twojej decyzji" line.
- Round 1 has no "Oś" column (variants differ in kind); from round 2 on it is mandatory.
- No preamble, no recap of the previous round beyond the one "baza" line.

## Rules that are specific to how Marcin works

- **Decide trivia yourself; ask only when assuming.** Don't ask which axis to push — pick three sensible ones. Ask a question INSTEAD of a round only when a variant would rest on an unknown fact (the audience, where the text appears, a constraint). **Why:** a question per step stalls the loop; a silent assumption poisons every later round.
- **Challenge his pick once.** If his choice is weaker on a criterion he himself stated earlier (he rejected "general", then picks the most general row), say it in one line with the criterion, then follow his decision. **Why:** his pick is a hypothesis, not an order — but arguing twice turns the loop into a debate.
- **Carry every rejection criterion forward.** Each new round must satisfy ALL criteria collected so far, not just the latest. **Why:** fixing "za ogólny" in round 3 by reintroducing what was rejected in round 1 as "za sprzedażowy" wastes a round.
- **Suggest finishing, don't declare it.** When the three variants differ only cosmetically (a word, punctuation), say „Różnice są już kosmetyczne — to wygląda na wersję końcową. Zamykamy na 2?" **Why:** past that point new rounds produce churn, not improvement; but only he knows whether it is good enough.
- **Check every variant before it enters the table, not only the winner.** (1) Plain everyday words, nothing contrived: „planujesz tak, żeby…”, not „Urlop i święta układasz pod reakcję jednej osoby”. (2) Read it in its target place, with the sentence before and after: every pronoun has a clear antecedent, „dlatego”/„bo” really follows from the previous sentence, and each word means the same as elsewhere on the surface. **Why:** Marcin, 2026-10-12, rejected both: „pamiętaj, aby używać prostego słownictwa” and „pamiętaj, aby rozumieć, do czego dana rzecz się odnosi i jakie ma znaczenie w kontekście”. A variant read in isolation from the table hides both faults, and he then picks among broken options. The full `human-language-check` still runs only on the final version (Finish, step 1).
- **Language follows the conversation.** Polish conversation → variants, table and question in Polish.
- **If the thing lives in a file, read the file before each round.** He may have edited it by hand; that edit is the new base. Don't overwrite it — if you think it is worse, say so.

## Finish

1. **Reader-facing text (copy, question for an audience, headline, message) → run `human-language-check` on the FINAL version before delivering it.** Not on every round — only the winner is delivered.
2. **Deliver the final version** as a clean quote (or write it into the target file, if there is one — the file gets ONLY the final text, no lineage).
3. **Record the lineage** — in chat if the work is ephemeral; in `<name>-decyzje.md` next to the target file if there is one. Format:

```
Wersja końcowa: „…"

Kryteria (wiążą przyszłe edycje):
⛔ <criterion> — np. „pytanie otwarte bez kotwicy momentu jest za ogólne"
⛔ <criterion>

Ścieżka: R1 C (nie A: <criterion>, nie B: <criterion>) → R2 1 (oś: moment) → R3 2 (oś: ostrzej)
```

- **Criterion, not instance.** „⛔ pytanie o przeszkodę brzmi jak obiekcja sprzedażowa" survives rewording; „⛔ nie wariant A" does not — the same idea comes back in new words and nobody recognizes it.
- The path is ONE line. It is the only history kept; everything else about the process is not recorded.

## Anti-patterns

- ❌ **Round 1 of three rewordings of the same idea** — the direction was chosen silently by me, not by him.
- ❌ **Describing variants instead of quoting them** — he can't pick words he can't see.
- ❌ **"Oto kilka opcji, wszystkie mają zalety"** — no recommendation = the work of choosing is pushed back to him.
- ❌ **Declaring "gotowe" / "idealne"** — only he closes the loop.
- ❌ **Lineage in the target file** — the copy file holds only paste-ready text; reasons go beside it.
