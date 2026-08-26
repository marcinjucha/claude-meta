---
name: summary-signal-first
description: Use when writing or reviewing a SUMMARY / STATUS UPDATE / RECAP for a named recipient — an update for an advisor or coach, a pre-meeting summary for a partner or client, a status note, a "what matters out of this" digest. Decides what gets CUT (my process, finished work that asks nothing, stale queue items) and what leads (the recipient's decision). Trigger on "podsumowanie", "napisz podsumowanie", "update dla", "status", "zwięźle", "skróć to", "co z tego jest istotne", "przygotuj notatkę przed spotkaniem", "summary", "status update", "recap", "what matters here", "trim this down". DISTINCT from human-language-check (that is the LANGUAGE layer — grammar and AI-tells — and runs AFTER this on the surviving text) and from copy-* (sales copy written from a BRIEF; this is not persuasion, it is selection).
---

# Summary, signal first

## Purpose

A summary is not a compressed report. **Keep what the RECIPIENT needs in order to act or decide; cut
everything that documents MY process.** Length is a symptom — the work is selection, and the recipient
is the only criterion.

Origin (2026-07-29): a message to a coach cut from ~700 to ~330 words. What was load-bearing is WHAT
went — a paragraph on how a format change worked out and three things that turned out differently
than assumed. All true, none of it his business; the document existed to get three answers.

## When to Use

**Use when:** writing an update for an advisor/coach, a pre-meeting summary for a partner or client,
a status note, a digest of a long thread or document, or trimming any of those.

**Do NOT use when:**
- the text is sales copy → `copy-discovery` → `copy-write`
- the job is grammar / de-AI on already-selected text → `human-language-check` (runs after this)
- it is your own working note or operator scaffolding → nothing here applies; there, process notes
  ARE the content

## Surfaces and the entry test

Before writing a line, name the surface. The same true sentence is signal on one and noise on another.

**Entry test — two questions per paragraph:**
1. Does the recipient need this to **act or decide**?
2. Whose **burden** does this sentence describe — theirs, or mine?

| Surface | Signal = | Cut |
|---|---|---|
| **Advisor / coach** | what they can base advice on: locked decisions, what moved, the gate that was missed, the one open question | my execution (rounds of edits, tooling, reorganisations), finished work that asks nothing of them |
| **Partner / creator / client** | their product / their decisions, framed as proposal not settlement; what I need from them | operator scaffolding: revenue split, GO/NO-GO gates, hypothesis statuses, rejected variants |
| **Buyer** | what they get | sentences about us and about the process that delivers the benefit → `[[three-surfaces-operator-creator-buyer]]` |
| **Technical / self-report** | `[Marcin: podaj realny raport techniczny, wtedy dopiszemy reguły]` | — |

This last row is **deliberately empty**: no real technical report was in the source material, so there
are no verified rules to state — and an audit must not "fix" this section with invented ones.

## Patterns

### P2 — Lead with the delta, in one line
The first line after the title carries what changed since the recipient last looked. Real example:
*"Since the last update the offer got built and the validation did not."* Everything after it is
support; nothing before it is preamble.

### P3 — Cut my own process, by name
Real cut list from one advisor update: revenue split, the block-by-block offer walkthrough, eight
rounds of deck fixes, the layout audit, knowledge-note names, the Trello reorganisation. All real
work, none of it the recipient's decision.

### P4 — Cut finished work that asks nothing
DNA and copy were done and were still cut: they required nothing from the recipient. **Done ≠
reportable.** A finished item earns a line only when it changes what he decides.

### P5 — Carry inherited debt visibly, don't dress it as news
Consumer terms of sale blocked sales in July and still do. It stays in, marked *same as in July* —
re-reporting an old blocker as fresh news hides that it has not moved.

### P6 — Purge stale queue items against the recipient's own last answer
A question about a seat cap was regenerated from a July 9 queue and sent even though the recipient had
answered it on July 24 ("no seat cap") — and the paragraph then contradicted a later line of the same
document. **Before sending, check every open question against what the recipient already answered.**

### P7 — One closed question, options priced
Where a decision is wanted: state the two options you can see, then ask the closed question —
*"Which one costs less at a first launch?"* On a partner surface the asks are numbered and the most
important one is flagged as such, because the recipient reads in order.

### P8 — Numbers with provenance, ratio over count, plus your reading
*"Recorded beats live 13 to 10 overall, and 9 to 2 inside the largest segment."* And when a proportion
repeats across three samples (17/18, 25/28, 27/30) say what you read from it: *a property of the
question rather than a reading of demand.* A number without your reading hands the interpretation work
back to the recipient.

### P9 — The surface talks about its topic, never about itself
No legends, no "the table below shows", no "as I mentioned in section three". If a component needs a
legend it does not work; if it works the legend is redundant → `[[legend-signals-a-broken-component]]`.

### P10 — Proposal, not settlement; unconfirmed stays marked
Partner surface opens with *"everything below is a proposal, not a settlement"*. Anything not yet
verified keeps its `[do potwierdzenia]` marker rather than being smoothed into fact.

### P11 — Record the reason for each cut in the operator scaffolding
Every summary carries a header block (`>` quote, above the recipient-facing text) listing what was cut
and why. **Why:** a week later a cut looks like a loss unless the reason is written down — and it stops
the next pass from restoring the noise. This block is scaffolding: it never ships to the recipient.
Both templates in `resources/` carry it as part of the template.

### P12 — Boundaries
- language, grammar, AI-tells → `human-language-check`, after selection is settled
- buyer-facing copy → `copy-*`; the discriminator for what may cross from partner material to buyer
  copy is `[[three-surfaces-operator-creator-buyer]]`
- a deliverable promised at purchase that would need production first →
  `[[split-deliverable-by-production-cost]]`

## Script

```bash
python3 ~/.claude/skills/summary-signal-first/scripts/audit-summary.py <file.md> --surface advisor
```

Five detectors, surface-scoped: process leaks, document-meta/legend lines, about-us promises
(buyer only), unresolved markers, and structure (missing scaffolding block, no question anywhere).
Exit 0 clean, 1 findings, 2 could not read. It skips frontmatter and `>` blocks, so operator
scaffolding is never flagged.

**What the script cannot see** — the seven items are listed in its docstring; the load-bearing ones:
whether the lead line carries the delta, whether a cut item should have stayed, whether a number's
reading is right, and whether an open question was already answered by the recipient (P6). Silence
from the script is not a clean summary; it prints how many lines it actually read for that reason.

## Resources

- `resources/advisor-update-template.md` — advisor / coach update
- `resources/partner-summary-template.md` — partner / creator pre-meeting summary
- `@../resources/signal-vs-noise-reference.md` — the 3-question filter
