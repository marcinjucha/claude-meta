---
description: "Website - landing page/site from a brief, no generic AI look: references → impeccable → motion → verify - Usage: /website [opis | ścieżka projektu | link Figma]"
argument-hint: "[opis strony | ścieżka do projektu | link Figma]"
---

# Website — brief to shipped page

Orchestrates tools that are already installed. impeccable is the backbone. This command adds the one step none of them cover: capturing **real reference websites**. Origin: an Instagram reel listed the stack (Emil Kowalski + impeccable skills, a reference-sites skill, Figma + Playwright MCP). It named the tools only, with no method; this file is the method.

## Usage

```
/website landing dla kancelarii rodzinnej, jedna akcja: umów konsultację
/website ~/Prywatne/projects/agency-cms/apps/website      # existing project
/website https://www.figma.com/design/<fileKey>/...?node-id=1-2   # Figma as design input
```

## Phases

```
0: Input + brief gaps          (inline)
1: References                  (inline: WebSearch + Playwright MCP + script)
2: Direction + build           (/impeccable — its own gates and agents)
3: Motion                      (review-animations → animate only for gaps)
4: Verification loop           (inline Playwright + break-ui + mobile-native; impeccable's reviewer outcome)
5: Figma push                  (ONLY on request)
6: Knowledge capture           (ai-manager-agent, proposals only)
```

## Orchestrator Rules

1. **impeccable is the backbone.** Do not bring in `taste-skill:*` or `stitch-skill`. **Why:** they overlap with impeccable, and stitch-skill writes a competing DESIGN.md.
2. **Never bypass impeccable's gates.** `init`, `concept-seed` and comp approval have no skip. Comp approval is Marcin's, through impeccable's own question or decision page.
3. **Talk to Marcin in Polish. One decision per turn, recommendation first, closed question.**
4. **Deliberate deviation from the house command template: no 3-5 clarifying questions after each phase.** Marcin is asked only at real decision points: brief gaps (Phase 0), reference pick (Phase 1), comp approval (Phase 2, impeccable's), and ship (Phase 4). Decide everything else yourself and name the assumption in one line. **Why:** his working rule is "decide yourself, ask only on assumptions". A question block after every phase stalls a flow whose real decisions are already gated.
5. **Positive proof only.** A screenshot or console check counts only when you read the file or output written by THIS run. A stale screenshot from an earlier loop looks identical to a fresh one.
6. **Do not duplicate impeccable.** It asks its own questions, runs its own 1440/390 inspection into `.impeccable/review/`, and spawns `impeccable-finish-reviewer` itself. This command covers only what impeccable does not.
7. **Figma is not a preview surface.** Rendering an impeccable pick in Figma draws the same design twice, and Figma only approximates the coded page. Preview comes from (a) impeccable comps before code, (b) `/impeccable live` in the running page, and (c) Playwright screenshots in every verification loop.

## Phase 0: Input + brief gaps (inline)

**First, before the brief: is impeccable actually loaded in THIS session?** Check that `impeccable:impeccable` is in the session's available-skills list and the `impeccable:impeccable-*` agents are in the agent list. If either is missing, stop and tell Marcin to run `/plugin` → install impeccable, then resume. **Why:** on 2026-10-12 the plugin was enabled in `settings.json` and its `SKILL.md` was on disk, yet the session answered `Unknown skill: impeccable` (also for `impeccable:impeccable`). `enabledPlugins` and files on disk are no proof of loading. Collecting the brief and references first wastes both, because Phase 2 cannot start.

Also check whether image generation is available. Without it impeccable works **code-led**: its decision cards carry HTML sketches at 390×844 instead of image comps. Tell Marcin this in one line before Phase 2, so the sketches don't read as a broken run.

**Detect the input from `$ARGUMENTS`:**

| Input | Route |
|-------|-------|
| Plain description | NEW → Phases 1-4 |
| Path to existing project, "popraw / dopracuj" | POLISH → skip Phase 1; `/impeccable critique` → `audit` / `polish` on the named surface, then Phases 3-4 |
| Path to existing project, "redesign / nowy wygląd" | REDESIGN → full flow incl. Phase 1. impeccable's new-work path replaces the old visual world; it does not polish it |
| figma.com URL | FIGMA → skip Phase 1 and impeccable comps; load `/figma-design-to-code` BEFORE `get_design_context`, adapt to the project stack, then Phases 3-4 |

If the intent between POLISH and REDESIGN is unclear, that is the one question to ask.

**Brief: fill only what is missing.** Ask in one message only about the missing items, each with your proposed answer:
- cel strony (what it must achieve)
- odbiorca
- jedna akcja (the single CTA)
- stack: detect from the repo (`package.json`, framework config). Ask only when there is no repo
- czy jest gotowa treść: if not, draft copy is written during the build and must pass `human-language-check` in Phase 4

Keep the brief as 5-8 lines. It goes to impeccable verbatim in Phase 2.

## Phase 1: References (inline) — NEW and REDESIGN only

The gap this command exists for: no installed skill searches, browses or screenshots real websites.

1. **Load WebSearch** via `ToolSearch` (`select:WebSearch`). Query curated galleries (Awwwards, Godly, Land-book, SiteInspire) by **industry + page type** (e.g. "law firm landing page", "SaaS pricing page").
2. **Shortlist 3-5 TARGET sites.** Follow each gallery entry to the live site URL. ⚠️ Screenshotting the gallery page instead of the target site is the common failure: the shot shows the gallery's frame and thumbnail, not the site.
3. **Capture with Playwright MCP:** `browser_resize` 1440×900 → `browser_navigate` → dismiss the cookie banner (`browser_snapshot` to find the accept button, `browser_click`) → `browser_take_screenshot` full page. Then resize to 390×844 and repeat. Save into `<project>/.design-refs/shots/<site>-desktop.png` / `-mobile.png`. ⚠️ On a bot block, captcha or a blank render, drop the site and take the next one from the shortlist. Never keep a broken shot.
4. **Read every shot from THIS run** and extract concrete patterns per site: layout rhythm, type scale, hero construction, section order, motion (from `browser_evaluate` / observation). Write them to `<project>/.design-refs/references.md`: one short block per site, plus a closing line on "what we take" across the set.
5. **Gitignore:** if `<project>/.gitignore` lacks `.design-refs/shots/`, append it. **Why:** they are third-party screenshots. `references.md` stays tracked because it records Marcin's pick.
6. **Marcin picks.** Recommend 1-2 sites and the patterns to take, then ask one closed question.

**Why `.design-refs/` and not `.impeccable/`:** impeccable owns `.impeccable/` through its phase state (`generate-image` refuses to write under `.impeccable/mocks/` before `build-phase start`), and it never reads user references from there.

## Phase 2: Direction + build via `/impeccable`

Invoke `/impeccable` (Persuade mode for landing pages). Follow its pipeline; it carries its own instructions.

- **Hand over the finished brief** (Phase 0) plus the picked patterns as **text**, so impeccable's 2-3 questions are already answered. It still asks a compact confirmation ("skip settled facts, not the confirmation"). Answer it from the brief; don't fight it.
- **References enter as words, never as `--ref` images.** impeccable takes "the look" from its dealt world (`concept-seed`). Its catalog card images are its only `--ref` inputs, and site screenshots passed there would compete with that world. The patterns go into: (a) the brief (constraints / proof / what the surface must prove), and (b) Marcin's **steer / re-roll** on impeccable's direction page. The screenshots stay Marcin's yardstick when he judges comps.
- **Preview before code:** impeccable's 3 comps in `.impeccable/mocks/` (code-led without image generation: HTML sketches at 390×844, see Phase 0). Marcin approves one through impeccable's gate.
- **Preview in the running page:** once the dev server runs, `/impeccable live` hot-swaps element variants via HMR. Use it when Marcin wants to compare variants of a section in place, not as a mandatory step.
- Build gates (comps → spec → plates → hero → sections → motion → responsive) run as impeccable defines them. DESIGN.md is written last by its documenter.

## Phase 3: Motion

impeccable's build already has a motion gate. Review first, then add only for gaps; never rebuild.

1. `review-animations` on what impeccable built.
2. `animate` only for the gaps it names.
3. `find-animation-opportunities`: optional, only if the page feels static after step 2.

## Phase 4: Verification loop (inline)

1. **Design review: its source depends on the route.**
   - **NEW / REDESIGN:** act on the outcome of impeccable's own `impeccable-finish-reviewer` (ship / fix / rebuild / recapture). Do not spawn it a second time.
   - **FIGMA:** impeccable's new-work flow never ran, so there is no reviewer verdict. Run `/impeccable critique` on the built page and compare it against the Figma frame (`get_screenshot`).
   - **POLISH:** act on the critique / audit results from the Phase 0 route.
2. **Playwright covers only what impeccable does not:** at 1440 and 390, check `browser_console_messages` (errors), click through the CTA and interactive elements, and take fresh screenshots, reading the files from THIS run.
3. `break-ui`: worst-case data (long names, empty states, extreme copy length).
4. `mobile-native`: mobile feel at 390.
5. Fix → re-screenshot → repeat until clean.
6. **Page copy → `human-language-check`** (mandatory, global rule) on audience-facing text only, before delivery.
7. **Ship decision:** show Marcin the latest desktop + mobile shots with a recommendation, then ask one closed question.

## Phase 5: Figma push (ONLY on request)

Only when Marcin wants an editable design (manual edits, showing a client). Load `/figma-generate-design` first, then follow its workflow.

## Phase 6: Knowledge capture

**Agent**: ai-manager-agent. Pass: the brief, the picked references, the impeccable direction chosen, the fix loops that happened, and any tool failure (blocked sites, gate surprises). The agent proposes additions to this command or a project CLAUDE.md, or says explicitly "nothing worth capturing". Proposals only; never auto-update.

## Commands

`continue` · `skip` · `back` · `status` · `stop`
