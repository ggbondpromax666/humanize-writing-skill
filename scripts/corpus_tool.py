#!/usr/bin/env python3
"""Maintain the AI-tell corpus in data/ai-tells.{zh,en}.json.

Four commands:

    python corpus_tool.py stats                  # counts by family/severity
    python corpus_tool.py validate               # regex + schema checks
    python corpus_tool.py add --lang zh --re "..." --label "..." --keep "..." --fix "..."
    python corpus_tool.py observe --lang zh --text "新发现的句式"

`add` appends one entry without rewriting the rest of the file (minimal diff),
auto-assigns the next id, and bumps the minor version. `observe` records a raw
candidate in data/observed.{lang}.md for triage later.

The corpus is a hand-built candidate list, not a scraped dataset. See
ATTRIBUTION.md.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
FILES = {"zh": DATA / "ai-tells.zh.json", "en": DATA / "ai-tells.en.json"}
PREFIX = {"zh": "zh", "en": "en"}
FAM_CODE = {"stock": "st", "defensive": "df", "explanatory": "ex", "coined": "ct", "platform": "pf"}
VALID_FAM = set(FAM_CODE)
VALID_SEV = {"strong", "weak"}


def read_corpus(lang: str) -> dict:
    return json.loads(FILES[lang].read_text(encoding="utf-8"))


def next_id(payload: dict, lang: str, fam: str) -> str:
    code = f"{PREFIX[lang]}-{FAM_CODE[fam]}-"
    nums = []
    for e in payload["entries"]:
        m = re.fullmatch(re.escape(code) + r"(\d{3})", e.get("id", ""))
        if m:
            nums.append(int(m.group(1)))
    return f"{code}{max(nums, default=0) + 1:03d}"


def validate_payload(payload: dict, lang: str) -> list:
    problems, ids, seen_re = [], set(), {}
    for e in payload.get("entries", []):
        eid = e.get("id", "?")
        if eid in ids:
            problems.append(f"{eid}: duplicate id")
        ids.add(eid)
        if e.get("fam") not in VALID_FAM:
            problems.append(f"{eid}: bad fam {e.get('fam')!r}")
        if e.get("sev") not in VALID_SEV:
            problems.append(f"{eid}: bad sev {e.get('sev')!r}")
        if not (e.get("keep") or "").strip():
            problems.append(f"{eid}: empty keep-condition")
        try:
            re.compile(e.get("re", ""))
        except re.error as exc:
            problems.append(f"{eid}: bad regex ({exc})")
        if e.get("re") in seen_re:
            problems.append(f"{eid}: duplicate regex of {seen_re[e['re']]}")
        seen_re[e.get("re")] = eid
    return problems


def bump_version(text: str) -> str:
    m = re.search(r'"version"\s*:\s*"(\d+)\.(\d+)\.(\d+)"', text)
    if not m:
        return text
    major, minor, _ = m.groups()
    return text[: m.start()] + f'"version": "{major}.{int(minor) + 1}.0"' + text[m.end():]


def insert_entry(text: str, entry: dict) -> str:
    """Append an entry just before the closing `]` without reformatting others."""
    end = text.rfind("\n  ]")
    if end == -1:
        raise ValueError("cannot find the closing entries array")
    head = text[:end].rstrip()
    tail = text[end:]
    if not head.endswith(","):
        head += ","
    line = "    " + json.dumps(entry, ensure_ascii=False, separators=(",", ":"))
    return head + "\n" + line + tail


def cmd_stats(args) -> int:
    total = 0
    for lang in ("zh", "en"):
        p = read_corpus(lang)
        fams, sevs = {}, {}
        for e in p["entries"]:
            fams[e["fam"]] = fams.get(e["fam"], 0) + 1
            sevs[e["sev"]] = sevs.get(e["sev"], 0) + 1
        total += len(p["entries"])
        fam_txt = ", ".join(f"{k}={v}" for k, v in sorted(fams.items()))
        print(f"{lang}: v{p.get('version')} | {len(p['entries'])} entries "
              f"(strong={sevs.get('strong', 0)}, weak={sevs.get('weak', 0)}) | {fam_txt}")
    print(f"total: {total} entries")
    return 0


def cmd_validate(args) -> int:
    bad = 0
    for lang in ("zh", "en"):
        problems = validate_payload(read_corpus(lang), lang)
        if problems:
            bad += len(problems)
            print(f"{lang}: {len(problems)} problem(s)")
            for p in problems:
                print(f"  - {p}")
        else:
            print(f"{lang}: OK")
    return 1 if bad else 0


def cmd_add(args) -> int:
    if args.fam not in VALID_FAM:
        print(f"bad --fam {args.fam!r}; choose from {sorted(VALID_FAM)}", file=sys.stderr)
        return 2
    try:
        re.compile(args.re)
    except re.error as exc:
        print(f"bad --re: {exc}", file=sys.stderr)
        return 2
    if not args.keep.strip():
        print("--keep is required: an entry without a keep-condition is not allowed", file=sys.stderr)
        return 2

    path = FILES[args.lang]
    text = path.read_text(encoding="utf-8")
    payload = json.loads(text)
    entry = {
        "id": next_id(payload, args.lang, args.fam),
        "re": args.re,
        "show": args.show or args.label,
        "fam": args.fam,
        "sev": args.sev,
        "label": args.label,
        "keep": args.keep,
        "fix": args.fix,
    }
    new_text = bump_version(insert_entry(text, entry))
    candidate = json.loads(new_text)
    problems = validate_payload(candidate, args.lang)
    if problems:
        print("refusing to write; validation failed:", file=sys.stderr)
        for p in problems:
            print(f"  - {p}", file=sys.stderr)
        return 1
    path.write_text(new_text, encoding="utf-8")
    print(f"added {entry['id']} to data/{path.name}; corpus now {len(candidate['entries'])} entries")
    return 0


def cmd_observe(args) -> int:
    log = DATA / f"observed.{args.lang}.md"
    log.parent.mkdir(parents=True, exist_ok=True)
    if not log.exists():
        log.write_text(
            f"# 观察记录 / Observation log ({args.lang})\n\n"
            "编辑过程中遇到、但尚未写成正则的候选信号。攒够同类再转成 corpus 条目。\n\n",
            encoding="utf-8",
        )
    stamp = args.date or "undated"
    log.open("a", encoding="utf-8").write(f"- [{stamp}] {args.text}" + (f" — {args.note}" if args.note else "") + "\n")
    print(f"logged to data/{log.name}")
    return 0


def main(argv=None) -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass
    ap = argparse.ArgumentParser(description="Maintain the AI-tell corpus.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("stats").set_defaults(func=cmd_stats)
    sub.add_parser("validate").set_defaults(func=cmd_validate)

    add = sub.add_parser("add")
    add.add_argument("--lang", choices=["zh", "en"], required=True)
    add.add_argument("--re", required=True, help="Python regex for the pattern")
    add.add_argument("--label", required=True)
    add.add_argument("--keep", required=True, help="when the hit is legitimate")
    add.add_argument("--fix", required=True)
    add.add_argument("--show", default="")
    add.add_argument("--fam", default="stock", choices=sorted(VALID_FAM))
    add.add_argument("--sev", default="weak", choices=sorted(VALID_SEV))
    add.set_defaults(func=cmd_add)

    obs = sub.add_parser("observe")
    obs.add_argument("--lang", choices=["zh", "en"], required=True)
    obs.add_argument("--text", required=True)
    obs.add_argument("--note", default="")
    obs.add_argument("--date", default="")
    obs.set_defaults(func=cmd_observe)

    args = ap.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
