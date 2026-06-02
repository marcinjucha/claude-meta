---
description: "Convene a multi-agent council on a hard question, decision, or stubborn bug — Stage 1 fan-out of N blind agents with distinct perspectives, Stage 2 anonymized cross-review + ranking, Stage 3 Chairman synthesis. Heavyweight; for high-stakes questions, not trivia. Usage: /council <question>"
---

# Council — Multi-Agent Deliberation

Multi-phase orchestration command that models karpathy/llm-council as a Claude Code workflow. The orchestrator (you) runs three stages, spawning subagents via the **Agent tool**, then delivers the Chairman's decision.

## Usage

```
/council <question>
/council "should the Kalman gate be per-axis or combined 3-DOF Mahalanobis?"
/council "5 members, lenses: correctness, performance, failure-modes" <question>
```

**Argument**: the hard question, decision, or stubborn bug to deliberate. Optionally prefix knobs (size, lenses, "skip review", "you be the chairman", "mix models", "use agent X for the Y lens") — see Knobs below.

## When to use / when NOT

- **Use:** stubborn bug seen from one angle too long, architecture/design forks, risky trade-offs, "is this fix actually right?", any decision where independent perspectives + adversarial cross-check beat a single pass. This is what we did with the 4 verification "lenses".
- **Don't use:** trivial/mechanical tasks, single-fact lookups, or when the answer is already clear. The council costs N×(1+review)+1 agent runs — scale to the stakes.

## The Claude Code adaptation (key insight)

karpathy's council gets diversity from **different LLM vendors**. Here there is one model, so diversity comes from **distinct perspectives/roles** assigned per member (the load-bearing lever), optionally reinforced by:
- `model` override per Agent call (mix `opus`/`sonnet`/`haiku` for genuine model diversity), and/or
- **best-fit `subagent_type` per member** — match the lens to the most capable specialist agent, not one default (see Stage 0 step 4).

A council of identical agents is wasted spend — **members must differ in lens, not just be N copies**.

## Stage 0 — Frame the council (orchestrator, inline)

1. Restate the query in one sentence.
2. Choose council size: **3 default**, 4–5 for complex/high-stakes, ≤6 (diminishing returns + concurrency cap).
3. Assign each member a **distinct perspective** — either the user's (if they named angles) or derive non-overlapping lenses. Good lens sets:
   - Debugging: *measurement / data-flow / temporal / downstream-rendering* (the 4 lenses we used), or *correctness / performance / failure-modes*.
   - Design: *simplest-thing-that-works / risk-and-edge-cases / long-term-maintainability / user-impact*.
   - Decision: *proponent / skeptic / pragmatist / domain-expert*.
4. **Pick the best-fit agent per member — high-leverage, and DISCOVER don't hardcode.** Specialist subagents load their OWN skills and project context, so a well-matched agent answers with far more domain knowledge than a generic one — agent choice is part of the council's quality, not a detail. In THIS environment, enumerate what exists:
   - built-in agent types listed in the Agent tool registry (commonly `general-purpose`, `Explore`, `Plan`, plus any others),
   - project agents in `.claude/agents/` — **read each one's `description` (and `skills:` list)** to learn its specialty.
   Then map each member's lens to the agent whose description best covers it (e.g. correctness/verification, architecture/placement, implementation, testing/performance, requirements, broad search, or a domain specialist). **Maximize specialist coverage, minimize generic agents:** every member that plausibly touches the project's domain should run on a specialist — `general-purpose` is a LAST resort, used only for a lens with no specialist even loosely relevant (or when the project ships no custom agents at all). If two lenses map to the same best specialist, either give both to it (distinct prompts) or assign the second to the next-closest specialist rather than dropping to generic. When a domain has more specialists than your initial lenses, prefer shaping the lenses so each maps to a distinct specialist — the specialist's loaded skills ARE part of the council's knowledge. Prefer Stage-2 reviewers to use a different specialist `subagent_type` than the Stage-1 author of the option they review. Optionally pair a stronger `model` with the hardest lens / the Chairman.
5. State the size + the per-member (perspective → chosen agent) assignment to the user in one line, then proceed.

## Stage 1 — First opinions (parallel, FOREGROUND)

Spawn ALL members **in a single message with multiple Agent calls** so they run concurrently. Each member gets ONLY: the query + its assigned perspective + required output shape. Members are **blind to each other** (fresh subagents — natural).

- **Run foreground, not `run_in_background`.** Background agents are killed when the process exits and their state is lost (learned the hard way). Foreground parallel calls complete in one turn.
- Demand structured output (e.g. a short YAML/headed sections: claim, evidence/`file:line`, confidence, recommendation) so Stage 2 can compare like-for-like.
- Collect each final message as that member's opinion. Label them **Member A, B, C…** internally.

## Stage 2 — Anonymized cross-review

Goal: rank opinions on accuracy + insight without identity bias.

1. **Anonymize:** strip perspective names and authorship. Relabel the opinions **Option 1, 2, 3…** (shuffle so Option-number ≠ Member-letter). Never tell a reviewer which option is "theirs".
2. Spawn reviewers (reuse the same N perspectives, or a smaller neutral panel) **in parallel**. Each reviewer receives the **full anonymized set** and must:
   - rank all options best→worst on accuracy and on insight,
   - justify in 1–2 lines each, and flag any option that is wrong/unsupported.
3. Aggregate rankings (e.g. mean rank per option, plus any "flagged-wrong" notes). Surface disagreement explicitly — a split vote is signal, not noise.

## Stage 3 — Chairman synthesis

One **Chairman** produces the single final answer. The orchestrator may BE the chairman, or spawn a dedicated agent (use a stronger `model: opus` for hard calls).

Chairman input: all opinions (de-anonymized is fine now) + the aggregated rankings. Chairman must:
- weight by the panel's rankings but **not blindly follow the majority** — graft the best ideas from runners-up, discard flagged-wrong claims;
- resolve contradictions explicitly (state why one view wins);
- output **one decision + the why + concrete next action** (and, if applicable, what would change the call).

## Output to the user

```
## Council on: <query>
Members (N): <perspective A> · <perspective B> · …

### Stage 1 — opinions (summaries)
- A (<lens>): <1–3 line gist>
- B (<lens>): …

### Stage 2 — ranking
<option → mean rank, + any wrong-flags / notable disagreement>

### Stage 3 — Chairman decision
<the single answer> — Why: <…> — Next: <action>
```

Keep Stage 1/2 as scannable summaries (link to detail if asked); the Chairman decision is the headline.

## Knobs (args)

- `/council <query>` — auto-frames size + perspectives.
- Honor explicit asks: "5 members", "lenses: X, Y, Z", "skip review", "you be the chairman", "mix models", "use agent X for the Y lens" (overrides the auto-match in Stage 0 step 4).
- `--no-act` / `--decide-only`: produce the decision but don't implement it (default for code changes — confirm before editing).

## Anti-patterns

- ❌ **Background agents for the council** — they die on process exit; run foreground in parallel. (Hit this directly.)
- ❌ **Identical members** — N copies of one lens = N× cost, 1× insight. Perspectives must be distinct.
- ❌ **Skipping anonymization in Stage 2** — named authorship biases the ranking; relabel to Option N and shuffle.
- ❌ **Chairman = majority vote** — synthesize, don't tally; a minority opinion can be the correct one (flag-wrong > popularity).
- ❌ **Convening for trivia** — match council size to stakes; a 5-agent council on a one-liner is waste.
- ❌ **Letting members see each other in Stage 1** — first opinions must be independent.
- ❌ **Defaulting to `general-purpose` when a specialist exists** — specialists carry project-specific skills/context; a generic agent throws that away. Match to specialists first; generic is the last resort.

## Scaling note

For large/deterministic councils (fixed fan-out, many members, repeatable), the **Workflow tool** runs the same pattern with built-in parallelism, structured schemas, and synthesis — prefer it when the council shape is known up front and the user has opted into multi-agent orchestration. For ad-hoc, conversational councils, the foreground-parallel-Agent pattern above is simpler and is the default.
