#!/usr/bin/env python3
"""Build and check /goal conditions for a repo build stage (stage-goal skill).

Two files per stage in <dir> (default docs/goals):
  <slug>-wymagania.md  full spec (source of truth)
  <slug>.md            the /goal text, <= limit chars

Usage (run from anywhere inside the repo):
  stage_goal.py build <slug> [--dir docs/goals] [--write] [--force]
  stage_goal.py check [<slug>|all] [--dir docs/goals]

All language-specific strings (markers, templates) live in goal-strings.json next
to this file; this source stays ASCII on purpose. Prints a short report only.
"""
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
S = json.load(open(os.path.join(HERE, "goal-strings.json"), encoding="utf-8"))
LIMIT = S["limit"]
POINT_RE = re.compile(r"^(\d+)\. ")


def repo_root():
    r = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit("not inside a git repo")
    return r.stdout.strip()


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def points_of(lines):
    """Ordered [(number, line)] of numbered point lines."""
    return [(m.group(1), l) for l in lines for m in [POINT_RE.match(l)] if m]


def first_line(lines, prefix):
    for l in lines:
        if l.startswith(prefix):
            return l
    return None


def parse_spec(text):
    lines = text.split("\n")
    title = lines[0][2:] if lines and lines[0].startswith("# ") else ""
    name = title[: -len(S["specTitleSuffix"])] if title.endswith(S["specTitleSuffix"]) else title
    return {
        "name": name,
        "points": points_of(lines),
        "scope": first_line(lines, S["scopeMarker"]),
        "closing": first_line(lines, S["closingMarker"]),
        "advisor": first_line(lines, S["advisorMarker"]) is not None,
        "done": any(m in text for m in S["doneMarkers"]),
    }


def goal_body(text):
    """Text after the /goal prefix, trailing newlines stripped (what /goal counts)."""
    i = text.find("\n" + S["goalPrefix"])
    if i >= 0:
        return text[i + 1 + len(S["goalPrefix"]):].rstrip("\n")
    if text.startswith(S["goalPrefix"]):
        return text[len(S["goalPrefix"]):].rstrip("\n")
    return None


def process_line(root):
    path = os.path.join(root, "CLAUDE.md")
    if not os.path.exists(path):
        sys.exit("no CLAUDE.md at repo root: add a '%s' paste line (see stage-goal SKILL.md)" % S["processLabel"])
    text = read(path)
    i = text.find(S["processLabel"])
    if i < 0:
        sys.exit("CLAUDE.md has no '%s' line: add it to the stage process section" % S["processLabel"])
    q_open, q_close = S["quoteOpen"], S["quoteClose"]
    m = re.search(re.escape(q_open) + "(.+?)" + re.escape(q_close), text[i:], re.S)
    if not m or not m.group(1).strip():
        sys.exit("no quoted text after '%s' in CLAUDE.md" % S["processLabel"])
    return re.sub(r"\s*\n\s*", " ", m.group(1)).strip()


def paths(root, d, slug):
    base = os.path.join(root, d)
    return os.path.join(base, slug + S["specSuffix"] + ".md"), os.path.join(base, slug + ".md")


def assemble(spec, slug, d, repo, proc):
    intro = S["intro"].format(name=spec["name"], repo=repo, slug=slug, dir=d)
    pts = "\n".join(l for _, l in spec["points"]) + "\n"
    tail = proc + "\n" + spec["closing"]
    without = intro + pts + tail
    if spec["scope"] and len(intro + pts + spec["scope"] + "\n" + tail) <= LIMIT:
        return intro + pts + spec["scope"] + "\n" + tail, True
    return without, False


def is_compressed(spec, goal_text):
    body = goal_body(goal_text) or ""
    return [l for _, l in points_of(body.split("\n"))] != [l for _, l in spec["points"]]


def cmd_build(slug, d, write, force):
    root = repo_root()
    sp, gp = paths(root, d, slug)
    if not os.path.exists(sp):
        sys.exit("no spec: %s" % sp)
    spec = parse_spec(read(sp))
    missing = [k for k in ("points", "closing") if not spec[k]]
    if not spec["name"] or missing:
        sys.exit("spec incomplete (%s): title '# <Name>%s', numbered points and the closing line are required"
                 % (", ".join(missing) or "title", S["specTitleSuffix"]))
    goal, scope_in = assemble(spec, slug, d, os.path.basename(root), process_line(root))
    n = len(goal)
    print("build %s: %d/%d chars (%s)" % (slug, n, LIMIT, "fits" if n <= LIMIT else "OVER by %d" % (n - LIMIT)))
    if spec["scope"]:
        print("  scope line: %s" % ("included" if scope_in else "OMITTED (does not fit; scope stays in the spec only)"))
    else:
        print("  scope line: none in spec")
    if n > LIMIT:
        print("  nothing written. Point lengths (compress in context, then edit the goal by hand):")
        for num, l in spec["points"]:
            print("    %s. %d" % (num, len(l)))
        return 1
    if not write:
        print("  dry run (use --write to write %s)" % os.path.relpath(gp, root))
        return 0
    if os.path.exists(gp):
        old = read(gp)
        if is_compressed(spec, old) and not force:
            print("  REFUSED: existing goal has hand-compressed points; rerun with --force to replace it")
            return 1
        new = S["goalTitle"].format(name=spec["name"]) + "\n\n" + S["goalPrefix"] + goal + "\n"
        if old == new:
            print("  unchanged")
            return 0
    new = S["goalTitle"].format(name=spec["name"]) + "\n\n" + S["goalPrefix"] + goal + "\n"
    with open(gp, "w", encoding="utf-8") as f:
        f.write(new)
    print("  written %s" % os.path.relpath(gp, root))
    return 0


def check_one(root, d, slug, proc):
    sp, gp = paths(root, d, slug)
    fails, warns = [], []
    spec_text = read(sp)
    spec = parse_spec(spec_text)
    if not os.path.exists(gp):
        return "FAIL", ["goal file missing"], [], 0
    goal_text = read(gp)
    body = goal_body(goal_text)
    if body is None:
        return "FAIL", ["no '%s' line in goal" % S["goalPrefix"].strip()], [], 0
    n = len(body)
    blines = body.split("\n")
    if n > LIMIT:
        fails.append("over limit by %d" % (n - LIMIT))
    if not any(m in body for m in S["doneMarkers"]):
        fails.append("no done marker")
    gclosing = first_line(blines, S["closingMarker"])
    if not gclosing:
        fails.append("no closing block")
    elif spec["closing"] and gclosing != spec["closing"]:
        warns.append("closing differs from spec")
    if slug + S["specSuffix"] + ".md" not in body:
        fails.append("no pointer to spec")
    if "`%s.md`" % slug not in spec_text:
        fails.append("spec has no back-pointer to goal")
    if not spec["closing"]:
        fails.append("spec has no closing block")
    if not spec["advisor"]:
        warns.append("spec has no advisor line")
    if not spec["scope"]:
        warns.append("spec has no scope line")
    gpts = points_of(blines)
    if [x for x, _ in gpts] != [x for x, _ in spec["points"]]:
        fails.append("point numbers differ: goal %s vs spec %s"
                     % (",".join(x for x, _ in gpts), ",".join(x for x, _ in spec["points"])))
    elif [l for _, l in gpts] != [l for _, l in spec["points"]]:
        diff = [x for (x, a), (_, b) in zip(gpts, spec["points"]) if a != b]
        warns.append("compressed points: %s" % ",".join(diff))
    if proc is not None and proc not in body:
        warns.append("process line differs from CLAUDE.md")
    if spec["scope"] and spec["scope"] not in body:
        warns.append("scope line not in goal")
    return ("FAIL" if fails else "WARN" if warns else "OK"), fails, warns, n


def cmd_check(target, d):
    root = repo_root()
    base = os.path.join(root, d)
    try:
        proc = process_line(root)
    except SystemExit as e:
        proc = None
        print("note: %s (process line not compared)" % e)
    suffix = S["specSuffix"] + ".md"
    if target == "all":
        slugs = sorted(f[: -len(suffix)] for f in os.listdir(base) if f.endswith(suffix))
        legacy = sorted(f for f in os.listdir(base)
                        if f.endswith(".md") and not f.endswith(suffix) and f[:-3] not in slugs)
    else:
        slugs, legacy = [target], []
        if not os.path.exists(paths(root, d, target)[0]):
            sys.exit("no spec for %s" % target)
    worst = 0
    for slug in slugs:
        status, fails, warns, n = check_one(root, d, slug, proc)
        print("%-4s %s (%d/%d)" % (status, slug, n, LIMIT))
        for m in fails:
            print("     fail: " + m)
        for m in warns:
            print("     warn: " + m)
        if status == "FAIL":
            worst = 1
    if legacy:
        print("skipped %d single-file goals without a spec: %s" % (len(legacy), ", ".join(legacy)))
    return worst


def main(argv):
    if len(argv) < 2 or argv[1] not in ("build", "check"):
        print(__doc__)
        return 2
    d = "docs/goals"
    if "--dir" in argv:
        d = argv[argv.index("--dir") + 1]
    pos = [a for i, a in enumerate(argv[2:], 2) if not a.startswith("--") and argv[i - 1] != "--dir"]
    if argv[1] == "build":
        if not pos:
            sys.exit("build needs a stage slug")
        return cmd_build(pos[0], d, "--write" in argv, "--force" in argv)
    return cmd_check(pos[0] if pos else "all", d)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
