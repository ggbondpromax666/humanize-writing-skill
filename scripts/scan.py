#!/usr/bin/env python3
"""Candidate scanner for AI-writing tells (Chinese + English).

A *candidate finder*, not a judge. It reports positions so a human or an agent
can check context. A hit is not a reason to edit: every entry in the corpus
carries a keep-condition, and this script cannot evaluate it.

Usage:
    python scan.py draft.md
    python scan.py draft.md --json
    python scan.py --lang zh draft.txt
    python scan.py --lang mixed draft.txt
    cat draft.txt | python scan.py -
    python scan.py --stats

The rule corpus lives in ../data/ai-tells.{zh,en}.json. Without it the script
refuses to run rather than silently using a stale built-in table.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys
from collections import Counter
from dataclasses import dataclass, field

DATA_DIR = pathlib.Path(__file__).resolve().parent.parent / "data"
CORPUS_FILES = {"zh": "ai-tells.zh.json", "en": "ai-tells.en.json"}

# Families that describe AI writing habits. "platform" covers register-bound
# formulas (public administration, academic, marketing, customer service) and is
# reported separately: many of them are correct inside their genre.
HABIT_FAMILIES = {"stock", "defensive", "explanatory", "coined"}


# ---------------------------------------------------------------------------
# Corpus loading
# ---------------------------------------------------------------------------

@dataclass
class Rule:
    pattern: str
    family: str
    severity: str
    label: str
    fix: str
    keep: str = ""
    context: str = ""
    flags: int = 0


def load_corpus(lang: str):
    """Return (rules, label, warnings). Raises FileNotFoundError if absent."""
    path = DATA_DIR / CORPUS_FILES[lang]
    payload = json.loads(path.read_text(encoding="utf-8"))
    rules, warnings = [], []
    for raw in payload.get("entries", []):
        try:
            rule = Rule(
                pattern=raw["re"],
                family=raw.get("fam", "stock"),
                severity=raw.get("sev", "weak"),
                label=raw.get("label", ""),
                fix=raw.get("fix", ""),
                keep=raw.get("keep", ""),
                flags=raw.get("flags", 0),
            )
            re.compile(rule.pattern, rule.flags)
        except (KeyError, re.error, TypeError) as exc:
            warnings.append(f"{raw.get('id', '?')}: {exc}")
            continue
        rules.append(rule)
    label = f"data/{path.name} v{payload.get('version', '?')} ({len(rules)} entries)"
    return rules, label, warnings


# ---------------------------------------------------------------------------
# Input handling
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# LaTeX prose extraction
# ---------------------------------------------------------------------------

MATH_ENV = re.compile(
    r"\\begin\{(equation\*?|align\*?|gather\*?|displaymath|math|array|cases|matrix|pmatrix|bmatrix|aligned|split)\}"
)
TEXT_CMD = re.compile(r"\\(?:textbf|textit|emph|underline|text|mathrm|mbox|textrm|textsf)\{([^{}]*)\}")


def strip_latex(text: str) -> str:
    """Keep prose, drop math and markup, preserving line numbers.

    A .tex file is prose plus markup. Scanning raw source lets `\begin{equation}`
    and friends act as noise, so math environments and commands are blanked
    while every line keeps its index.
    """
    out, in_env = [], False
    for line in text.splitlines():
        line = re.sub(r"(?<!\\)%.*$", "", line)
        if in_env:
            if r"\end{" in line:
                in_env = False
            out.append("")
            continue
        if MATH_ENV.search(line):
            in_env = True
            out.append("")
            continue
        line = re.sub(r"\$\$.*?\$\$", "", line)
        line = re.sub(r"\$[^$]*\$", "", line)
        line = re.sub(r"\\\[.*?\\\]", "", line)
        line = re.sub(r"\\\(.*?\\\)", "", line)
        line = TEXT_CMD.sub(r"\1", line)
        line = re.sub(r"\\[a-zA-Z]+\*?(\[[^\]]*\])?(\{[^{}]*\})?", "", line)
        line = re.sub(r"\\[^a-zA-Z]", " ", line)
        out.append(line)
    return "\n".join(out)


CODE_FENCE = re.compile(r"^\s*(```|~~~)")


def read_text(path: str) -> str:
    """Decode UTF-8 (with or without BOM), falling back to GB18030."""
    raw = sys.stdin.buffer.read() if path == "-" else pathlib.Path(path).read_bytes()
    for enc in ("utf-8-sig", "utf-8", "gb18030"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace")


def strip_code(text: str) -> str:
    """Blank out *closed* fenced code blocks.

    An unclosed fence is treated as ordinary text: blanking to EOF would turn a
    broken document into a clean one.
    """
    lines = text.splitlines()
    fence_idx = [i for i, line in enumerate(lines) if CODE_FENCE.match(line)]
    if len(fence_idx) % 2 == 1:
        fence_idx = fence_idx[:-1]
    openers = set(fence_idx[::2])
    closers = set(fence_idx[1::2])
    out, in_fence = [], False
    for i, line in enumerate(lines):
        if i in openers:
            in_fence = True
            out.append("")
            continue
        if i in closers:
            in_fence = False
            out.append("")
            continue
        out.append("" if in_fence else line)
    return "\n".join(out)


def guess_lang(text: str) -> str:
    """Return zh, en, or mixed.

    "mixed" matters: judging a bilingual draft as one language silently drops
    half the rules.
    """
    cjk = sum(1 for ch in text if "\u4e00" <= ch <= "\u9fff")
    latin_words = len(re.findall(r"[A-Za-z]{2,}", text))
    if cjk >= 5 and latin_words >= 8:
        return "mixed"
    if cjk >= 10 or (len(text) and cjk / len(text) > 0.08):
        return "zh"
    return "en"


# ---------------------------------------------------------------------------
# Analysis
# ---------------------------------------------------------------------------

@dataclass
class Hit:
    line: int
    col: int
    text: str
    family: str
    severity: str
    label: str
    fix: str
    keep: str = ""
    context: str = ""


@dataclass
class Report:
    hits: list = field(default_factory=list)
    terms: list = field(default_factory=list)
    stats: dict = field(default_factory=dict)
    corpus: str = ""
    warnings: list = field(default_factory=list)


def rule_flags(rule: Rule) -> int:
    """Case-insensitive matching, except for patterns that require capitals.

    Applying IGNORECASE globally collapses `[A-Z]{2,6}` into `[a-z]`, which
    turns "the model" into an "unexpanded acronym".
    """
    if "[A-Z]" in rule.pattern:
        return rule.flags
    return rule.flags | re.IGNORECASE


def line_lang(line: str) -> str:
    """Language of one line, used to route rules in a mixed document.

    A Chinese line must not be judged by English patterns and vice versa; that
    is why routing is per line rather than per document.
    """
    cjk = sum(1 for ch in line if "\u4e00" <= ch <= "\u9fff")
    latin_words = len(re.findall(r"[A-Za-z]{2,}", line))
    if cjk == 0:
        return "en" if latin_words else "zh"
    if latin_words == 0:
        return "zh"
    # A word is several characters; compare weights, not counts, so an English
    # sentence quoting six Chinese characters is still English.
    return "zh" if cjk >= latin_words * 3 else "en"


def split_segments(line: str):
    """Split a line into sentence spans, keeping delimiters.

    Routing happens per segment, so a line holding both a Chinese and an
    English sentence is judged sentence by sentence.
    """
    spans, start = [], 0
    for m in re.finditer(r"[。！？.!?]", line):
        spans.append((start, m.end()))
        start = m.end()
    if start < len(line):
        spans.append((start, len(line)))
    return spans or [(0, len(line))]


def load_rules_for(lang: str):
    """Return ({lang: rules}, label, warnings). Mixed loads both corpora."""
    langs = ["zh", "en"] if lang == "mixed" else [lang]
    rules_by_lang, labels, warnings = {}, [], []
    for code in langs:
        rules, label, warns = load_corpus(code)
        rules_by_lang[code] = rules
        labels.append(label)
        warnings.extend(f"{code}: {w}" for w in warns)
    return rules_by_lang, "; ".join(labels), warnings


EN_SUBORDINATORS = re.compile(
    r"\b(which|that|who|whose|whom|whereas|although|though|unless|because|since|while|whereby)\b",
    re.IGNORECASE,
)


def structure_hits(lines, lang: str) -> list:
    """Sentence-level checks. English fails on subordination; Chinese on stacked 的."""
    hits = []
    for i, line in enumerate(lines, 1):
            spans = split_segments(line) if lang == "mixed" else [(0, len(line))]
            for start, end in spans:
                sent = line[start:end].strip()
                if not sent:
                    continue
                code = line_lang(sent) if lang == "mixed" else lang
                if code == "zh":
                    chars = len(re.findall(r"[\u4e00-\u9fa5]", sent))
                    if chars >= 140:
                        hits.append(Hit(i, 1, sent[:60], "structure", "strong",
                                        f"超长句（{chars} 字）", "按语义拆成两句以上",
                                        "长度在承担列举或节奏时可保留"))
                    elif chars >= 80:
                        hits.append(Hit(i, 1, sent[:60], "structure", "weak",
                                        f"长句（{chars} 字）", "检查能否拆",
                                        "流水句、意合推进时可保留"))
                    if sent.count("的") >= 4:
                        hits.append(Hit(i, 1, sent[:60], "structure", "weak",
                                        "的字定语堆叠（≥4）", "拆成短句，还原动词",
                                        "公文标题、法律定义中可保留"))
                else:
                    words = len(re.findall(r"[A-Za-z][A-Za-z']*", sent))
                    if words >= 55:
                        hits.append(Hit(i, 1, sent[:60], "structure", "strong",
                                        f"very long sentence ({words} words)", "split at a conjunction",
                                        "the length enacts a list or sequence"))
                    elif words >= 30:
                        hits.append(Hit(i, 1, sent[:60], "structure", "weak",
                                        f"long sentence ({words} words)", "check whether the joint can be split",
                                        "a single genuine argument may stay long"))
                    if len(EN_SUBORDINATORS.findall(sent)) >= 3:
                        hits.append(Hit(i, 1, sent[:60], "structure", "weak",
                                        "clause stacking (3+ subordinates)", "promote one clause to a main clause",
                                        "legal or statutory text may require it"))
                    if sent.count(" of ") >= 3:
                        hits.append(Hit(i, 1, sent[:60], "structure", "weak",
                                        "of-chain (3+)", "reorder: actor first",
                                        "a formal title may need it"))
    return hits


def scan(text: str, lang: str, strict: bool = False) -> Report:
    clean = strip_code(text)
    lines = clean.splitlines()
    rules_by_lang, corpus_label, corpus_warnings = load_rules_for(lang)
    rep = Report(corpus=corpus_label, warnings=corpus_warnings)
    lang_lines = {"zh": 0, "en": 0}
    for i, line in enumerate(lines, 1):
        if not line.strip():
            continue
        ctx = "table" if line.lstrip().startswith("|") else ""
        spans = split_segments(line) if lang == "mixed" else [(0, len(line))]
        for start, end in spans:
            seg = line[start:end]
            if not seg.strip():
                continue
            code = line_lang(seg) if lang == "mixed" else lang
            lang_lines[code] += 1
            for rule in rules_by_lang[code]:
                for m in re.finditer(rule.pattern, seg, rule_flags(rule)):
                    rep.hits.append(Hit(
                        line=i, col=start + m.start() + 1, text=m.group(0)[:60],
                        family=rule.family, severity=rule.severity,
                        label=rule.label, fix=rule.fix, keep=rule.keep, context=ctx,
                    ))
    rep.hits.extend(structure_hits(lines, lang))

    # Same span from several rules: keep the strongest reading, not all of them.
    best = {}
    for h in rep.hits:
        key = (h.line, h.col, h.text)
        prev = best.get(key)
        if prev is None or (prev.severity != "strong" and h.severity == "strong"):
            best[key] = h
    rep.hits = list(best.values())

    rep.terms = find_terms(lines)
    rep.stats = compute_stats(clean, rep.hits, lang, strict)
    if lang == "mixed":
        rep.stats["lang_lines"] = lang_lines
    return rep


TERM_PATTERNS = [
    (r"[\u4e00-\u9fa5]{2,6}(?:体系|闭环|飞轮|抓手|底座|生态|链路|矩阵|心智|势能|引擎)", "复合抽象名词", 0),
    (r"(?:[A-Za-z][A-Za-z\-]*\s+){1,3}(?:framework|model|loop|flywheel|matrix)", "英文框架名", 0),
]

TERM_STOP = "了的是在和与及为我们他们你们它们这那其该此把被将对于用使让以及么"
TERM_VERBS = "采用使用实现构建打造形成进行开展推进提升"
EN_STOP = {"the", "a", "an", "our", "their", "its", "this", "that", "in", "of", "grounded"}


def clean_term(raw: str) -> str:
    """Trim grammatical noise that the noun-phrase regex drags in."""
    t = raw.strip()
    for ch in "了的是在和与为把被将":
        idx = t.rfind(ch)
        if 0 <= idx < len(t) - 1:
            t = t[idx + 1:]
    while t and t[0] in TERM_STOP:
        t = t[1:]
    if any(v in t for v in TERM_VERBS):  # a clause, not a term
        t = ""
    words = t.split()
    while words and words[0].lower() in EN_STOP:
        words = words[1:]
    return " ".join(words)


def find_terms(lines) -> list:
    seen = {}
    for i, line in enumerate(lines, 1):
        for pat, kind, gidx in TERM_PATTERNS:
            for m in re.finditer(pat, line, re.IGNORECASE):
                term = clean_term(m.group(gidx))
                if not (2 <= len(term) <= 16):
                    continue
                if term not in seen:
                    seen[term] = {"term": term, "line": i, "kind": kind, "count": 0}
                seen[term]["count"] += 1
    terms = list(seen.values())
    terms.sort(key=lambda t: (-t["count"], t["line"]))
    return terms[:20]


def compute_stats(text: str, hits: list, lang: str, strict: bool = False) -> dict:
    if lang == "zh":
        sentences = len(re.findall(r"[。！？；]", text)) or 1
        units = len(re.findall(r"[\u4e00-\u9fa5]", text))
        unit_label, min_units = "characters", 80
    else:
        sentences = len(re.findall(r"[.!?;]", text)) or 1
        units = len(re.findall(r"\b\w+\b", text))
        unit_label, min_units = "words", 40
    def counted(h):
        # Table rows usually mention a phrase rather than use it.
        return strict or h.context != "table"

    strong = sum(1 for h in hits if h.severity == "strong" and h.family in HABIT_FAMILIES and counted(h))
    weak = sum(1 for h in hits if h.severity == "weak" and h.family in HABIT_FAMILIES and counted(h))
    register = sum(1 for h in hits if h.family not in HABIT_FAMILIES or not counted(h))
    density = round((strong * 1000) / max(units, 1), 2)
    return {
        "sentences": sentences,
        "units": units,
        "unit_label": unit_label,
        "strong_hits": strong,
        "weak_hits": weak,
        "register_hits": register,
        "table_hits": sum(1 for h in hits if h.context == "table"),
        "strong_per_1000_units": density,
        "verdict": density_verdict(density, strong, weak, units, min_units),
    }


def density_verdict(d: float, strong: int, weak: int, units: int, min_units: int) -> str:
    if units < min_units:
        return "too short to judge - do not draw conclusions from a short sample"
    if strong == 0 and weak == 0:
        return "clean - no candidates from the habit families"
    if strong == 0:
        return "no strong hits; weak signals only - do not edit on these alone"
    if d >= 12:
        return "heavy - most strong hits are probably real"
    if d >= 5:
        return "moderate - check every strong hit in context"
    return "light - most hits are probably the writer's own habits"


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

def render(rep: Report, path: str, lang: str) -> str:
    st = rep.stats
    label = st["unit_label"]
    lines = st.get("lang_lines") or {}
    lang_detail = f" (zh {lines['zh']} / en {lines['en']} lines)" if lines else ""
    out = [
        f"# Candidate scan: {path}",
        f"language: {lang}{lang_detail} | {label}: {st['units']} | sentences: {st['sentences']}",
        f"habit hits: strong={st['strong_hits']} weak={st['weak_hits']} "
        f"({st['strong_per_1000_units']} per 1000 {label}) "
        f"| register/structure: {st['register_hits']} | table/example rows: {st['table_hits']} (mentions, verify before editing)",
        f"verdict: {st['verdict']}",
        f"corpus: {rep.corpus}",
    ]
    if rep.warnings:
        out.append(f"corpus warnings: {len(rep.warnings)} (run --stats to list)")
    out += ["", "A hit is a candidate, not a verdict. Check the keep-condition before editing.", ""]

    if rep.hits:
        out += [
            "## Hits",
            "",
            "| line | severity | family | hit | label | keep if | suggested fix |",
            "|---|---|---|---|---|---|---|",
        ]
        for h in sorted(rep.hits, key=lambda h: (h.line, h.col)):
            snippet = h.text.replace("|", "\\|")
            keep = (h.keep or "—").replace("|", "\\|")
            out.append(
                f"| {h.line} | {h.severity} | {h.family} | `{snippet}` | {h.label} | {keep} | {h.fix} |"
            )
        out.append("")
    else:
        out += ["## Hits", "", "No matches.", ""]

    if rep.terms:
        out += [
            "## Suspect terms (run the five tests)",
            "",
            "| term | first line | kind | count |",
            "|---|---|---|---|",
        ]
        for t in rep.terms:
            out.append(f"| {t['term']} | {t['line']} | {t['kind']} | {t['count']} |")
        out += ["", "Tests: definition, provenance, boundary, substitution, prediction.", ""]

    out += [
        "## Next",
        "",
        "1. Every strong hit: keep, tighten, or delete, using the keep-condition.",
        "2. Register hits (public administration, academic, marketing, service): check the genre first.",
        "3. Every term: ledger it. Only delete what you can prove is empty.",
        "4. Never add a fact or a source to fix a finding.",
    ]
    return "\n".join(out)


def main(argv=None) -> int:
    # Windows consoles default to GBK; force UTF-8 so Chinese labels survive.
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass
    ap = argparse.ArgumentParser(description="Find candidate AI-writing tells (zh/en).")
    ap.add_argument("path", nargs="?", help="file to scan, or - for stdin")
    ap.add_argument("--lang", choices=["zh", "en", "mixed", "auto"], default="auto")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--no-terms", action="store_true", help="skip term candidates")
    ap.add_argument("--stats", action="store_true", help="print corpus coverage and exit")
    ap.add_argument("--format", choices=["auto", "plain", "tex"], default="auto",
                    help="auto: .tex files are reduced to prose first")
    ap.add_argument("--strict", action="store_true",
                    help="count markdown table rows as usage too")
    args = ap.parse_args(argv)

    if args.stats:
        for code in ("zh", "en"):
            rules, label, warns = load_corpus(code)
            fams = Counter(r.family for r in rules)
            sevs = Counter(r.severity for r in rules)
            fam_txt = ", ".join(f"{k}={v}" for k, v in sorted(fams.items()))
            print(f"{code}: {label}")
            print(f"    strong={sevs.get('strong', 0)} weak={sevs.get('weak', 0)} | {fam_txt}")
            if warns:
                print(f"    invalid entries: {len(warns)}")
                for w in warns[:10]:
                    print(f"      - {w}")
        return 0

    if not args.path:
        print("error: a path is required unless --stats is used", file=sys.stderr)
        return 2

    try:
        text = read_text(args.path)
    except OSError as exc:
        print(f"cannot read {args.path}: {exc}", file=sys.stderr)
        return 1

    fmt = args.format
    if fmt == "auto":
        fmt = "tex" if str(args.path).lower().endswith((".tex", ".latex")) else "plain"
    if fmt == "tex":
        text = strip_latex(text)
    lang = guess_lang(text) if args.lang == "auto" else args.lang
    try:
        rep = scan(text, lang, strict=args.strict)
    except FileNotFoundError as exc:
        print(f"corpus missing: {exc}. Keep data/ next to scripts/.", file=sys.stderr)
        return 1
    if args.no_terms:
        rep.terms = []

    if args.json:
        print(json.dumps({
            "path": args.path,
            "language": lang,
            "corpus": rep.corpus,
            "corpus_warnings": rep.warnings,
            "stats": rep.stats,
            "hits": [h.__dict__ for h in rep.hits],
            "terms": rep.terms,
        }, ensure_ascii=False, indent=2))
    else:
        print(render(rep, args.path, lang))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
