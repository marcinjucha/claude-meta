#!/usr/bin/env python3
"""skill-ab: A/B eval of ONE model decision made by a skill or command.

Each call is a tool-free `claude -p` with the inputs inlined and a JSON schema for the answer; a
deterministic grader compares the answer with a hand-labelled gold set, and a fixed rule decides
whether the candidate variant may replace the baseline. Out of scope: commands whose quality comes
from multi-turn tool use or written output (use skill-creator's old-vs-new workflow for those).

  skill-ab.py run <suite_dir> [--variants A,B] [--reps N] [--cases id,...] [--model M] [--no-escalate]
  skill-ab.py report <run_dir> --suite <suite_dir>     re-grade stored answers, no model calls
  skill-ab.py candidates <run_dir> --suite <suite_dir> write candidates.md for gold labelling
  skill-ab.py calibrate <suite_dir> [--model M]        A/A + negative-control check of the eval itself

Exit codes: 0 verdict printed, 1 calibration failed, 2 precondition failed, 3 too many failed calls.
"""
import argparse
import concurrent.futures as cf
import datetime
import hashlib
import json
import os
import random
import re
import shutil
import statistics
import subprocess
import sys
import tempfile
from pathlib import Path

CLAUDE = os.environ.get("CLAUDE_BIN", "claude")
CACHE = Path(os.environ.get("SKILL_AB_CACHE", Path.home() / ".cache" / "skill-ab"))
SCHEMA = json.dumps({"type": "object", "properties": {
    "selected": {"type": "array", "items": {"type": "string"}}, "why": {"type": "string"}},
    "required": ["selected"]})
WIKILINK = re.compile(r"\[\[([^\]|#]+)")
WORKERS = int(os.environ.get("SKILL_AB_WORKERS", "4"))


class Precondition(Exception):
    pass


# ---------- suite and inputs ----------

def load_suite(suite_dir):
    suite_dir = Path(suite_dir).resolve()
    s = json.loads((suite_dir / "suite.json").read_text(encoding="utf-8"))
    s["_dir"] = suite_dir
    return s


def subst(v, s):
    return v.replace("{pool_dir}", s["pool_dir"]).replace("{suite_dir}", str(s["_dir"]))


def resolve_one(spec, s):
    if "file" in spec:
        p = Path(subst(spec["file"], s))
        if not p.exists():
            raise Precondition(f"input file missing: {p}")
        text = p.read_text(encoding="utf-8")
        if "between" in spec:
            start, end = spec["between"]
            i = next((k for k, ln in enumerate(text.split("\n")) if ln.startswith(start)), None)
            j = None if i is None else next((k for k, ln in enumerate(text.split("\n")) if k > i and ln.startswith(end)), None)
            if i is None or j is None or j <= i:
                raise Precondition(f"slice markers not found in {p}: {spec['between']}")
            text = "\n".join(text.split("\n")[i:j])
        return text
    if "cmd" in spec:
        cmd = [subst(c, s) for c in spec["cmd"]]
        outs = []
        for _ in range(2):
            r = subprocess.run(cmd, capture_output=True, text=True, cwd=s["_dir"])
            if r.returncode != 0:
                raise Precondition(f"generator failed ({r.returncode}): {' '.join(cmd)}\n{r.stderr}")
            outs.append(r.stdout)
        if outs[0] != outs[1]:
            raise Precondition(f"generator is not deterministic: {' '.join(cmd)}")
        return outs[0]
    raise Precondition(f"input spec needs 'file' or 'cmd': {spec}")


def resolve_inputs(s, variants, alias=None):
    """Returns {variant: {input_name: text}}. alias maps a synthetic variant to a real one (A2 -> A)."""
    alias = alias or {}
    out = {v: {} for v in variants}
    for name, spec in s["inputs"].items():
        per_variant = not ("file" in spec or "cmd" in spec)
        cache = {}
        for v in variants:
            real = alias.get(v, v)
            if per_variant and real not in spec:
                raise Precondition(f"input '{name}' has no variant '{real}'")
            key = real if per_variant else "*"
            if key not in cache:
                cache[key] = resolve_one(spec[real] if per_variant else spec, s)
            out[v][name] = cache[key]
    return out


def pool_ids(s):
    excl = set(s.get("pool_exclude", []))
    return {p.stem for p in Path(s["pool_dir"]).glob("*.md") if p.name not in excl}


def pool_sha(s):
    return hashlib.sha256("\n".join(sorted(pool_ids(s))).encode()).hexdigest()[:12]


def gold_sha(s):
    gold = [(c["id"], sorted(c.get("must") or []), sorted(c.get("ok") or [])) for c in s["cases"]
            if c.get("must") is not None]
    return hashlib.sha256(json.dumps(gold).encode()).hexdigest()[:12]


def check_preconditions(s, inputs):
    pool = pool_ids(s)
    errs = []
    for c in s["cases"]:
        for nid in (c.get("must") or []) + (c.get("ok") or []):
            if nid not in pool:
                errs.append(f"case {c['id']}: gold id not in pool: {nid}")
    cover = s.get("coverage_input")
    if cover:
        for v, ins in inputs.items():
            missing = sorted(pool - set(WIKILINK.findall(ins[cover])))
            if missing:
                errs.append(f"variant {v}: {len(missing)} pool notes not linked in '{cover}': {', '.join(missing)}")
    if errs:
        raise Precondition("\n".join(errs))
    cur = pool_sha(s)
    for c in s["cases"]:
        if c.get("must") is not None and c.get("pool_sha") and c["pool_sha"] != cur:
            print(f"WARNING case {c['id']}: gold labelled against pool {c['pool_sha']}, pool is now {cur}")


# ---------- model calls ----------

def call(prompt, system, model):
    d = tempfile.mkdtemp(prefix="skill-ab-")
    try:
        cmd = [CLAUDE, "-p", "--setting-sources", "", "--tools", "", "--system-prompt", system,
               "--json-schema", SCHEMA, "--model", model, "--max-turns", "3",
               "--output-format", "json", "--no-session-persistence"]
        r = subprocess.run(cmd, input=prompt, capture_output=True, text=True, cwd=d, timeout=300)
    except subprocess.TimeoutExpired:
        return {"status": "error", "reason": "timeout"}
    finally:
        shutil.rmtree(d, ignore_errors=True)
    if r.returncode != 0:
        return {"status": "error", "reason": f"exit {r.returncode}: {r.stderr[:300]}"}
    try:
        out = json.loads(r.stdout)
    except json.JSONDecodeError:
        return {"status": "error", "reason": "unparseable stdout"}
    sel = (out.get("structured_output") or {}).get("selected")
    if out.get("is_error") or not isinstance(sel, list):
        return {"status": "error", "reason": "no structured_output.selected", "cli": out}
    return {"status": "ok", "cli": out}


def call_with_retry(prompt, system, model):
    res = call(prompt, system, model)
    attempts = 1
    if res["status"] != "ok":
        res = call(prompt, system, model)
        attempts = 2
    res["attempts"] = attempts
    return res


def input_tokens(cli):
    u = cli.get("usage") or {}
    return u.get("input_tokens", 0) + u.get("cache_creation_input_tokens", 0) + u.get("cache_read_input_tokens", 0)


def run_calls(s, inputs, cases, variants, reps, model, run_dir, rep_offset=0):
    system = (s["_dir"] / s["system"]).read_text(encoding="utf-8")
    jobs = []
    for c in cases:
        for r in range(rep_offset, rep_offset + reps):
            for v in variants:  # interleaved A,B,A,B so cache warmth is shared
                fields = dict(inputs[v], problem=c["problem"])
                jobs.append((c["id"], v, r, s["template"].format(**fields)))
    raw = run_dir / "raw"
    raw.mkdir(parents=True, exist_ok=True)

    def work(job):
        cid, v, r, prompt = job
        res = call_with_retry(prompt, system, model)
        res.update(case=cid, variant=v, rep=r, prompt_chars=len(prompt) + len(system))
        (raw / f"{cid}__{v}__{r}.json").write_text(json.dumps(res, ensure_ascii=False), encoding="utf-8")
        return res

    with cf.ThreadPoolExecutor(max_workers=WORKERS) as ex:
        return list(ex.map(work, jobs))


def smoke(s, model):
    system = (s["_dir"] / s["system"]).read_text(encoding="utf-8")
    res = call_with_retry("smoke: return an empty selection.", system, model)
    if res["status"] != "ok":
        raise Precondition(f"smoke call failed: {res.get('reason')}")
    ceiling = s.get("decision", {}).get("smoke_max_input_tokens", 8000)
    tok = input_tokens(res["cli"])
    if tok > ceiling:
        raise Precondition(f"smoke call used {tok} input tokens (ceiling {ceiling}): settings, CLAUDE.md or MCP leaked in")
    return res


# ---------- grading ----------

def norm(i):
    i = i.strip().removeprefix("[[").removesuffix("]]")
    return re.split(r"[|#]", i)[0].strip().removesuffix(".md").split("/")[-1]


def load_results(run_dir):
    return [json.loads(p.read_text(encoding="utf-8")) for p in sorted((Path(run_dir) / "raw").glob("*.json"))]


def grade(s, results, baseline, candidate):
    pool = pool_ids(s)
    sizes = {p.stem: len(p.read_text(encoding="utf-8")) for p in Path(s["pool_dir"]).glob("*.md")}
    cases = {c["id"]: c for c in s["cases"]}
    ok = [r for r in results if r["status"] == "ok"]
    ratios = [r["prompt_chars"] / max(1, input_tokens(r["cli"])) for r in ok]
    cpt = statistics.median(ratios) if ratios else 3.5
    rows = []
    for r in ok:
        c = cases.get(r["case"])
        if c is None:
            continue
        sel = {norm(x) for x in r["cli"]["structured_output"]["selected"]}
        must = set(c["must"]) if c.get("must") is not None else None
        okset = set(c.get("ok") or [])
        tsel = input_tokens(r["cli"]) + (r["cli"].get("usage") or {}).get("output_tokens", 0)
        tload = sum(sizes.get(i, 0) for i in sel & pool) / cpt
        rows.append(dict(case=r["case"], variant=r["variant"], rep=r["rep"], sel=sorted(sel),
                         recall=(len(sel & must) / len(must)) if must else None,
                         noise=len(sel - (must or set()) - okset) if must is not None else None,
                         invalid=sorted(sel - pool), unjudged=sorted((sel & pool) - (must or set()) - okset),
                         size=len(sel), cap=len(sel) > c.get("max_selected", 10 ** 6),
                         tokens=tsel + tload, cost=r["cli"].get("total_cost_usd", 0.0)))
    errors = {v: sum(1 for r in results if r["variant"] == v and r["status"] != "ok") for v in (baseline, candidate)}
    calls = {v: sum(1 for r in results if r["variant"] == v) for v in (baseline, candidate)}
    return rows, errors, calls


def mean(xs):
    xs = [x for x in xs if x is not None]
    return statistics.mean(xs) if xs else None


def sd(xs):
    xs = [x for x in xs if x is not None]
    return statistics.stdev(xs) if len(xs) > 1 else 0.0


def hits(rows, cases):
    """hits[case][variant][note] = (k, n) for every must note."""
    h = {}
    for c in cases:
        if not c.get("must"):
            continue
        for v in {r["variant"] for r in rows}:
            rs = [r for r in rows if r["case"] == c["id"] and r["variant"] == v]
            h.setdefault(c["id"], {})[v] = {m: (sum(m in r["sel"] for r in rs), len(rs)) for m in c["must"]}
    return h


def aggregates(rows, cases, v):
    """Every metric is averaged per case first, so a case that lost reps to errors keeps its weight."""
    def per_case(key, only_graded=False):
        cs = [c for c in cases if c.get("must")] if only_graded else cases
        return [mean([r[key] for r in rows if r["case"] == c["id"] and r["variant"] == v]) for c in cs]
    vr = [r for r in rows if r["variant"] == v]
    R, N, T = per_case("recall", True), per_case("noise"), per_case("tokens")
    return dict(R=mean(R), R_sd=sd(R), N=mean(N), N_sd=sd(N),
                I=sum(len(r["invalid"]) for r in vr), C=sum(r["cap"] for r in vr),
                T=mean(T), T_sd=sd(T),
                cost=sum(r["cost"] for r in vr), n=len(vr))


def lost_notes(h, baseline, candidate, d):
    """A note is judged on pooled counts once both variants have lost_confirm_n answers; below that a
    note B never picked is an unresolved candidate, which blocks ADOPT."""
    cand, confirmed = [], []
    for cid, per in h.items():
        if baseline not in per or candidate not in per:
            continue
        for note, (ka, na) in per[baseline].items():
            kb, nb = per[candidate][note]
            if na == 0 or nb == 0:
                continue
            if min(na, nb) >= d.get("lost_confirm_n", 6):
                if ka / na >= d.get("lost_a_rate", 0.6) and kb <= nb * d.get("lost_b_rate", 0.125):
                    confirmed.append((cid, note, ka, na, kb, nb))
            elif ka / na >= 2 / 3 and kb == 0:
                cand.append((cid, note, ka, na, kb, nb))
    return cand, confirmed


def borderline_cases(rows, cases, h, baseline, candidate, d):
    out = set()
    cand, _ = lost_notes(h, baseline, candidate, d)
    out |= {c[0] for c in cand}
    for c in cases:
        if not c.get("must"):
            continue
        ra = mean([r["recall"] for r in rows if r["case"] == c["id"] and r["variant"] == baseline])
        rb = mean([r["recall"] for r in rows if r["case"] == c["id"] and r["variant"] == candidate])
        if ra is not None and rb is not None and abs(ra - rb) >= 0.34:
            out.add(c["id"])
    return out


def paired(rows, baseline, candidate):
    """Keep only cases answered by both variants, so A and B are averaged over the same cases."""
    both = {r["case"] for r in rows if r["variant"] == baseline} & {r["case"] for r in rows if r["variant"] == candidate}
    return [r for r in rows if r["case"] in both]


def verdict(s, rows, baseline, candidate):
    d = s.get("decision", {})
    cases = s["cases"]
    rows = paired(rows, baseline, candidate)
    h = hits(rows, cases)
    A, B = aggregates(rows, cases, baseline), aggregates(rows, cases, candidate)
    cand, confirmed = lost_notes(h, baseline, candidate, d)
    tol, rej = d.get("recall_tolerance", 0.05), d.get("recall_reject", 0.10)
    save = d.get("min_token_saving", 0.15)
    checks = {}
    if A["R"] is None or B["R"] is None:
        return "UNGRADED (no labelled cases)", checks, A, B, cand, confirmed
    off = [c for c in cases if c.get("must") == []]
    off_ok = all(all(not r["cap"] for r in rows if r["case"] == c["id"] and r["variant"] == candidate) for c in off)
    checks["no confirmed lost note"] = not confirmed
    checks["no unresolved lost-note candidate"] = not cand
    checks[f"recall B >= A - {tol}"] = B["R"] >= A["R"] - tol
    checks[f"noise B <= A + {d.get('noise_tolerance', 1.0)}"] = B["N"] <= A["N"] + d.get("noise_tolerance", 1.0)
    checks["invalid and cap violations B <= A"] = B["I"] <= A["I"] and B["C"] <= A["C"]
    checks["off-domain cases within cap"] = off_ok
    checks[f"tokens B <= (1 - {save}) * A"] = B["T"] <= (1 - save) * A["T"]
    if all(checks.values()):
        v = f"ADOPT {candidate}"
    elif confirmed or B["R"] < A["R"] - rej or (not checks[f"tokens B <= (1 - {save}) * A"] and B["R"] <= A["R"] + tol):
        v = f"REJECT {candidate}"
    else:
        v = "INCONCLUSIVE"
    return v, checks, A, B, cand, confirmed


# ---------- report ----------

def fmt(x, nd=3):
    return "-" if x is None else (f"{x:.{nd}f}" if isinstance(x, float) else str(x))


def hook_lines(text):
    out = {}
    for ln in text.split("\n"):
        m = re.match(r"^- \[\[([^\]|#]+)", ln)
        if m:
            out[m.group(1)] = ln[:200]
    return out


def write_report(s, run_dir, baseline, candidate, meta):
    results = load_results(run_dir)
    rows, errors, calls = grade(s, results, baseline, candidate)
    v, checks, A, B, cand, confirmed = verdict(s, rows, baseline, candidate)
    if over_error_budget(s, errors, calls):
        v = f"INVALID: too many failed calls {errors} of {calls}"
    L = []
    banners = calibration_banners(s, meta, baseline)
    ran = meta.get("cases")
    if ran is not None and len(ran) < len(s["cases"]):
        banners.append(f"partial run: {len(ran)} of {len(s['cases'])} cases")
    L += [f"!! {b}" for b in banners]
    shown = v if not (banners and v.startswith("ADOPT")) else f"{v}, NOT TRUSTWORTHY: {'; '.join(banners)}"
    L.append(f"VERDICT: {shown}")
    L.append(f"suite={s['name']} model={meta.get('model')} gold={gold_sha(s)} pool={pool_sha(s)} cli={meta.get('cli')}")
    for k, ok in checks.items():
        L.append(f"  [{'x' if ok else ' '}] {k}")
    L.append("")
    L.append(f"{'':10} {'recall':>14} {'noise':>12} {'invalid':>8} {'cap':>4} {'tokens':>16} {'calls':>6} {'errors':>6}")
    for name, a in ((baseline, A), (candidate, B)):
        L.append(f"{name:10} {fmt(a['R']):>7}±{fmt(a['R_sd'],2):<6} {fmt(a['N'],2):>6}±{fmt(a['N_sd'],2):<5} "
                 f"{a['I']:>8} {a['C']:>4} {fmt(a['T'],0):>9}±{fmt(a['T_sd'],0):<6} {calls[name]:>6} {errors[name]:>6}")
    L.append(f"cost usd: {fmt(A['cost'] + B['cost'], 3)}")
    L.append("\nper case (mean recall / noise / size):")
    for c in s["cases"]:
        def m(v_, k):
            return fmt(mean([r[k] for r in rows if r["case"] == c["id"] and r["variant"] == v_]), 2)
        tag = ",".join(c.get("tags", []))
        L.append(f"  {c['id']:40} {baseline}: {m(baseline,'recall')}/{m(baseline,'noise')}/{m(baseline,'size')}"
                 f"   {candidate}: {m(candidate,'recall')}/{m(candidate,'noise')}/{m(candidate,'size')}  {tag}")
    hooks = {}
    for name in (baseline, candidate):
        p = Path(run_dir) / "inputs" / f"{s.get('coverage_input', 'moc')}-{name}.txt"
        hooks[name] = hook_lines(p.read_text(encoding="utf-8")) if p.exists() else {}
    for title, items in (("CONFIRMED LOST NOTES", confirmed), ("lost-note candidates (stage 1)", cand)):
        if items:
            L.append(f"\n{title}:")
            for cid, note, ka, na, kb, nb in items:
                L.append(f"  {cid}: {note}  {baseline} {ka}/{na}  {candidate} {kb}/{nb}")
                L.append(f"    {baseline}: {hooks[baseline].get(note, '?')}")
                L.append(f"    {candidate}: {hooks[candidate].get(note, '?')}")
    unj = sorted({(r["case"], n) for r in rows for n in r["unjudged"]})
    inv = sorted({(r["case"], n) for r in rows for n in r["invalid"]})
    if unj:
        L.append("\nunjudged picks (triage into gold between runs):")
        L += [f"  {c}: {n}" for c, n in unj]
    if inv:
        L.append("\ninvalid ids:")
        L += [f"  {c}: {n}" for c, n in inv]
    text = "\n".join(L) + "\n"
    (Path(run_dir) / "report.txt").write_text(text, encoding="utf-8")
    (Path(run_dir) / "results.json").write_text(json.dumps(
        dict(verdict=v, checks=checks, A=A, B=B, rows=rows, lost_candidates=cand, lost_confirmed=confirmed,
             errors=errors, meta=meta, gold=gold_sha(s)), ensure_ascii=False, indent=1), encoding="utf-8")
    return v, text, errors, calls


def over_error_budget(s, errors, calls):
    maxerr = s.get("decision", {}).get("max_error_rate", 0.10)
    return any(calls[x] and errors[x] / calls[x] > maxerr for x in calls)


def setup_sha(s):
    """What the model is asked: system prompt, template, pool and every case's question and cap."""
    system = (s["_dir"] / s["system"]).read_text(encoding="utf-8")
    qs = [(c["id"], c["problem"], c.get("max_selected")) for c in s["cases"]]
    return hashlib.sha256(json.dumps([system, s["template"], pool_sha(s), qs]).encode()).hexdigest()[:12]


def calibration_key(s, meta, base):
    """Gold, model, the setup the run was made with and the baseline's inputs: change any and the
    stored calibration no longer applies."""
    ins = sorted((k, v) for k, v in meta.get("input_sha", {}).items() if k.endswith(f"-{base}"))
    fp = hashlib.sha256(json.dumps([meta.get("setup_sha"), ins]).encode()).hexdigest()[:12]
    return f"{gold_sha(s)}:{meta.get('model')}:{fp}"


def calibration_banners(s, meta, base):
    p = CACHE / s["name"] / "calibration.json"
    key = calibration_key(s, meta, base)
    if not p.exists():
        return ["no calibration for these inputs, gold and model (run: skill-ab.py calibrate)"]
    cal = json.loads(p.read_text(encoding="utf-8")).get(key)
    if not cal:
        return ["no calibration for these inputs, gold and model (run: skill-ab.py calibrate)"]
    if not cal.get("passed"):
        return [f"calibration failed: {cal.get('why')}"]
    return []


# ---------- commands ----------

def new_run_dir(s):
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    for k in range(100):
        d = CACHE / s["name"] / (stamp if k == 0 else f"{stamp}-{k}")
        try:
            d.mkdir(parents=True, exist_ok=False)
            return d
        except FileExistsError:
            continue
    raise Precondition("could not create a fresh run dir")


def cli_version():
    try:
        return subprocess.run([CLAUDE, "--version"], capture_output=True, text=True, timeout=30).stdout.strip()
    except Exception:
        return "?"


def execute(s, variants, reps, model, case_ids, escalate, alias=None):
    cases = [c for c in s["cases"] if not case_ids or c["id"] in case_ids]
    inputs = resolve_inputs(s, variants, alias)
    check_preconditions(s, inputs)
    smoke(s, model)
    run_dir = new_run_dir(s)
    (run_dir / "inputs").mkdir()
    shas = {}
    for v, ins in inputs.items():
        for name, text in ins.items():
            (run_dir / "inputs" / f"{name}-{v}.txt").write_text(text, encoding="utf-8")
            shas[f"{name}-{v}"] = hashlib.sha256(text.encode()).hexdigest()[:12]
    meta = dict(model=model, cli=cli_version(), variants=variants, reps=reps, input_sha=shas, alias=alias or {},
                setup_sha=setup_sha(s), cases=[c["id"] for c in cases])
    (run_dir / "meta.json").write_text(json.dumps(meta, indent=1), encoding="utf-8")
    print(f"run dir: {run_dir}")
    results = run_calls(s, inputs, cases, variants, reps, model, run_dir)
    base, cand = variants[0], variants[1]
    if escalate:
        rows, _, _ = grade(s, results, base, cand)
        border = borderline_cases(rows, cases, hits(rows, cases), base, cand, s.get("decision", {}))
        if border:
            print(f"escalating {len(border)} borderline cases: {', '.join(sorted(border))}")
            more = s.get("escalate_reps", 5)
            run_calls(s, inputs, [c for c in cases if c["id"] in border], [base, cand], more, model, run_dir, rep_offset=reps)
            meta["escalated"] = sorted(border)
    (run_dir / "meta.json").write_text(json.dumps(meta, indent=1), encoding="utf-8")
    return run_dir, meta


def finish(s, run_dir, meta, base, cand):
    v, text, errors, calls = write_report(s, run_dir, base, cand, meta)
    print(text)
    return (3 if v.startswith("INVALID") else 0), v


def cmd_run(a):
    s = load_suite(a.suite)
    variants = a.variants.split(",") if a.variants else s.get("default_variants", ["A", "B"])
    if len(variants) != 2:
        raise Precondition(f"--variants takes exactly two, baseline first: {variants}")
    model = a.model or s.get("model", "opus")
    reps = a.reps or s.get("reps", 3)
    case_ids = set(a.cases.split(",")) if a.cases else None
    run_dir, meta = execute(s, variants, reps, model, case_ids, not a.no_escalate)
    return finish(s, run_dir, meta, variants[0], variants[1])[0]


def cmd_report(a):
    s = load_suite(a.suite)
    meta = json.loads((Path(a.run_dir) / "meta.json").read_text())
    v = meta["variants"]
    return finish(s, Path(a.run_dir), meta, v[0], v[1])[0]


def cmd_candidates(a):
    s = load_suite(a.suite)
    results = [r for r in load_results(a.run_dir) if r["status"] == "ok"]
    pool = Path(s["pool_dir"])
    bodies = {p.stem: p.read_text(encoding="utf-8").lower() for p in pool.glob("*.md") if p.name not in s.get("pool_exclude", [])}
    L = []
    for c in s["cases"]:
        picked = {norm(x) for r in results if r["case"] == c["id"] for x in r["cli"]["structured_output"]["selected"]}
        grep = {n for n, b in bodies.items() if any(t.lower() in b for t in c.get("grep_terms", []))}
        allc = sorted((picked | grep) & set(bodies))
        random.Random(c["id"]).shuffle(allc)
        L.append(f"## {c['id']}\n{c['problem']}\n")
        L += [f"- {n}" for n in allc]
        L.append("")
    out = Path(a.run_dir) / "candidates.md"
    out.write_text("\n".join(L), encoding="utf-8")
    print(out)
    return 0


def cmd_calibrate(a):
    s = load_suite(a.suite)
    model = a.model or s.get("model", "opus")
    base = s.get("default_variants", ["A", "B"])[0]
    ctrl = s.get("control_variant", "CTRL")
    case_ids = set(s.get("calibration_cases") or [c["id"] for c in s["cases"] if c.get("must")])
    d = s.get("decision", {})
    twin = f"{base}2"
    run_dir, meta = execute(s, [base, twin, ctrl], s.get("reps", 3), model, case_ids, False, alias={twin: base})
    results = load_results(run_dir)
    cases = [c for c in s["cases"] if c["id"] in case_ids]
    sub = dict(s, cases=cases)
    rows_aa, _, _ = grade(sub, results, base, twin)
    errors = {v: sum(1 for r in results if r["variant"] == v and r["status"] != "ok") for v in (base, twin, ctrl)}
    calls = {v: sum(1 for r in results if r["variant"] == v) for v in (base, twin, ctrl)}
    va, checks_aa, A, A2, _, _ = verdict(sub, rows_aa, base, twin)
    rows_ctrl = paired(rows_aa, base, ctrl)
    A_c, C = aggregates(rows_ctrl, cases, base), aggregates(rows_ctrl, cases, ctrl)
    graded = None not in (A["R"], A2["R"], A_c["R"], C["R"])
    sampling = ("tokens", "no unresolved lost-note candidate", "invalid and cap")
    quality = [k for k in checks_aa if not k.startswith(sampling)]
    aa_ok = graded and all(checks_aa[k] for k in quality) and abs(A["R"] - A2["R"]) <= d.get("recall_tolerance", 0.05)
    disc_ok = graded and C["R"] <= A_c["R"] - d.get("ctrl_min_drop", 0.15)
    why = []
    if over_error_budget(s, errors, calls):
        aa_ok = False
        why.append(f"too many failed calls {errors} of {calls}")
    elif not graded:
        why.append("no graded answers for one of the variants")
    elif not aa_ok:
        why.append(f"A/A gap {fmt(abs(A['R'] - A2['R']))} or a quality check failed on identical inputs")
    if not disc_ok:
        why.append(f"control not caught: recall {fmt(C['R'])} vs {fmt(A_c['R'])}")
    rec = dict(passed=aa_ok and disc_ok, why="; ".join(why), A=A["R"], A2=A2["R"], CTRL=C["R"], run=str(run_dir))
    p = CACHE / s["name"] / "calibration.json"
    allcal = json.loads(p.read_text()) if p.exists() else {}
    allcal[calibration_key(s, meta, base)] = rec
    p.write_text(json.dumps(allcal, indent=1))
    print(json.dumps(rec, indent=1))
    return 0 if rec["passed"] else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    r = sp.add_parser("run")
    r.add_argument("suite")
    r.add_argument("--variants")
    r.add_argument("--reps", type=int)
    r.add_argument("--cases")
    r.add_argument("--model")
    r.add_argument("--no-escalate", action="store_true")
    for name in ("report", "candidates"):
        p = sp.add_parser(name)
        p.add_argument("run_dir")
        p.add_argument("--suite", required=True)
    c = sp.add_parser("calibrate")
    c.add_argument("suite")
    c.add_argument("--model")
    a = ap.parse_args()
    try:
        return {"run": cmd_run, "report": cmd_report, "candidates": cmd_candidates, "calibrate": cmd_calibrate}[a.cmd](a)
    except Precondition as e:
        print(f"PRECONDITION FAILED:\n{e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
