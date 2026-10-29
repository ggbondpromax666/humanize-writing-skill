#!/usr/bin/env python3
"""Regression tests for scan.py.

Stdlib only, no pytest. Each case writes a fixture to a temp dir, runs
`scan.py --json`, and asserts on the report.

    python tests/run_tests.py
"""

from __future__ import annotations

import json
import os
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
SCAN = ROOT / "scripts" / "scan.py"

CASES = []


def case(fn):
    CASES.append(fn)
    return fn


def run(name: str, text: str, *args: str, encoding: str = "utf-8") -> tuple:
    """Write a fixture, run the scanner, return (returncode, report, stderr)."""
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="hws-test-"))
    path = tmp / name
    path.write_text(text, encoding=encoding) if encoding == "utf-8" else path.write_bytes(text.encode(encoding))
    env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
    proc = subprocess.run(
        [sys.executable, str(SCAN), str(path), "--json", *args],
        capture_output=True, text=True, encoding="utf-8", errors="replace", env=env,
    )
    report = json.loads(proc.stdout) if proc.returncode == 0 and proc.stdout.strip() else {}
    return proc.returncode, report, proc.stderr


def labels(report: dict) -> list:
    return [h["label"] for h in report.get("hits", [])]


@case
def ai_chinese_is_flagged() -> str:
    rc, r, _ = run("ai.md", "在当今快速发展的时代，值得注意的是，该方案具有重要意义。"
                             "综上所述，不是方案不好，而是执行不到位。未来可期。")
    assert rc == 0
    assert r["stats"]["strong_hits"] >= 4, r["stats"]
    return f"strong={r['stats']['strong_hits']}"


@case
def clean_chinese_is_not_flagged() -> str:
    rc, r, _ = run("clean.md", "上周三我们把导出的超时从 30 秒改到了 8 秒。改动只碰了 retry 的等待逻辑，"
                              "别的没动。测试环境跑了 200 次，失败 3 次，都是同一个原因：下游偶发 502。")
    assert rc == 0
    assert r["stats"]["strong_hits"] == 0, labels(r)
    return "0 strong hits"


@case
def mixed_language_runs_both_corpora() -> str:
    rc, r, _ = run("mixed.md", "值得注意的是，这个改动很重要。It's worth noting that this plays a crucial role. "
                               "综上所述，先上线再说。In other words, we ship it.")
    assert rc == 0
    assert r["language"] == "mixed", r["language"]
    zh = any("宏大" in l or "段首" in l for l in labels(r))
    en = any("paragraph opener" in l or "metadiscourse" in l for l in labels(r))
    assert zh and en, labels(r)
    return f"language={r['language']} hits={len(r['hits'])}"


@case
def acronym_rules_need_capitals() -> str:
    rc, r, _ = run("model.md", "The data model is documented. This model works. Researchers built a model.")
    assert rc == 0
    assert not any("acronym" in l.lower() for l in labels(r)), labels(r)
    assert not any("framework name" in l.lower() for l in labels(r)), labels(r)
    return "no acronym false positive"


@case
def unclosed_fence_does_not_blank_the_document() -> str:
    rc, r, _ = run("fence.md", "正常一句话。\n```\n代码没闭合，后面的值得注意的是应该还能被扫到。")
    assert rc == 0
    assert any("段首" in l for l in labels(r)), labels(r)
    return "text after unclosed fence still scanned"


@case
def closed_fence_is_ignored() -> str:
    rc, r, _ = run("fence2.md", "正文。\n```python\n值得注意的是 = 1  # 代码里的不算\n```\n结束。")
    assert rc == 0
    assert not any("段首" in l for l in labels(r)), labels(r)
    return "code block skipped"


@case
def latex_math_is_ignored_but_prose_is_scanned() -> str:
    tex = ("\\section*{引言}\n\n\\emph{值得注意的是}，本文具有重要意义。\n\n"
           "\\begin{equation}\n 不是X，而是Y，这段在公式里应被忽略\n\\end{equation}\n\n"
           "结论：$u_t=a^2u_{xx}$ 成立。\n")
    rc, r, _ = run("paper.tex", tex)
    assert rc == 0
    hit_labels = labels(r)
    assert any("段首" in l for l in hit_labels), hit_labels
    assert not any("翻案" in l for l in hit_labels), hit_labels
    return f"hits={hit_labels}"


@case
def gbk_input_does_not_crash() -> str:
    rc, r, err = run("gbk.md", "值得注意的是，这是 GBK 编码。", encoding="gbk")
    assert rc == 0, err
    assert r["stats"]["strong_hits"] >= 1
    return "decoded gb18030"


@case
def table_rows_are_mentions_not_usage() -> str:
    text = ("| 类型 | 形态 |\n|---|---|\n"
            "| 段首壳 | 值得注意的是 |\n| 宏大开场 | 在当今……时代 |\n")
    rc, r, _ = run("table.md", text)
    assert rc == 0
    assert r["stats"]["table_hits"] >= 2, r["stats"]
    assert r["stats"]["strong_hits"] == 0, r["stats"]
    return f"table_hits={r['stats']['table_hits']} habit_strong=0"


@case
def strict_mode_counts_table_rows() -> str:
    text = "| 类型 | 形态 |\n|---|---|\n| 段首壳 | 值得注意的是 |\n"
    rc, r, _ = run("table2.md", text, "--strict")
    assert rc == 0
    assert r["stats"]["strong_hits"] >= 1, r["stats"]
    return "strict counts table rows"


@case
def short_text_is_not_judged() -> str:
    rc, r, _ = run("short.md", "值得注意的是。")
    assert rc == 0
    assert "too short" in r["stats"]["verdict"], r["stats"]["verdict"]
    return r["stats"]["verdict"]


@case
def duplicate_spans_collapse() -> str:
    rc, r, _ = run("dup.md", "值得注意的是，这个方案值得关注。")
    keys = {(h["line"], h["col"], h["text"]) for h in r["hits"]}
    assert len(keys) == len(r["hits"]), r["hits"]
    return f"{len(r['hits'])} hit(s), no duplicate span"


@case
def paper_excerpt_true_positives_without_false_ones() -> str:
    """Academic register: catch the slop, leave the scholarly parts alone."""
    text = (ROOT / "tests" / "fixtures" / "paper-zh.md").read_text(encoding="utf-8")
    rc, r, _ = run("paper.md", text)
    assert rc == 0
    got = labels(r)
    required = {"假因果开场", "段首评论壳", "拔高意义", "模糊归因", "归因未论证", "复述前文", "空展望"}
    missing = required - set(got)
    assert not missing, f"missed {missing}; got {got}"
    # Precision guards: these were real false positives before the fix.
    assert "伪学术命名候选" not in got, got
    assert "教案栏目词" not in got, got
    # Scholarly keep-conditions must not be turned into hits.
    assert "成果丰硕套话" in got  # weak platform hit is fine
    assert r["stats"]["table_hits"] == 0
    return f"strong={r['stats']['strong_hits']} labels={sorted(set(got))}"


@case
def mixed_lines_use_their_own_corpus() -> str:
    """A mixed draft must not run both rule sets over every line."""
    text = "值得注意的是，这段是中文。\nIt's worth noting that this English line is separate.\n"
    rc, r, _ = run("route.md", text)
    assert rc == 0
    assert r["language"] == "mixed", r["language"]
    assert r["stats"]["lang_lines"] == {"zh": 1, "en": 1}, r["stats"].get("lang_lines")
    got = labels(r)
    assert "段首评论壳" in got, got
    assert "paragraph opener, no referent" in got, got
    zh_hits = [h for h in r["hits"] if h["label"] == "段首评论壳"]
    assert len(zh_hits) == 1 and zh_hits[0]["line"] == 1, zh_hits
    return f"zh/en routed, hits={len(r['hits'])}"


@case
def quoted_mentions_are_not_counted_as_usage() -> str:
    """A passage that *quotes* a tell is documenting it, not using it."""
    text = "他在文章里解释过“值得注意的是”这句话为什么是套话。\n"
    rc, r, _ = run("mention.md", text)
    assert rc == 0
    assert r["stats"]["strong_hits"] == 0, r["stats"]
    assert r["stats"]["meta_hits"] >= 1, r["stats"]
    return f"meta={r['stats']['meta_hits']}, prose strong=0"


@case
def bilingual_sentence_runs_both_corpora_with_lang_tags() -> str:
    """A half-Chinese half-English sentence is checked against both corpora."""
    text = "值得注意的是，It is worth noting that this matters.\n"
    rc, r, _ = run("bilingual.md", text)
    assert rc == 0
    assert r["language"] == "mixed", r["language"]
    pairs = {(h["lang"], h["label"]) for h in r["hits"]}
    assert ("zh", "段首评论壳") in pairs, pairs
    assert ("en", "paragraph opener, no referent") in pairs, pairs
    return f"both corpora fired, pairs={sorted(pairs)}"


@case
def english_line_quoting_chinese_stays_english() -> str:
    """A quoted Chinese phrase inside an English sentence is not a Chinese line."""
    text = "We cite the Chinese phrase “值得注意的是” only as an example.\n"
    rc, r, _ = run("en-quote.md", text)
    assert rc == 0
    # The line is routed as English; the quoted Chinese phrase must not fire a
    # Chinese rule.
    assert not any("段首" in l for l in labels(r)), labels(r)
    if r["stats"].get("lang_lines"):
        assert r["stats"]["lang_lines"]["zh"] == 0, r["stats"]["lang_lines"]
    return "quoted Chinese did not switch the router"


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass
    failures = 0
    for fn in CASES:
        try:
            detail = fn()
            print(f"PASS  {fn.__name__}: {detail}")
        except AssertionError as exc:
            failures += 1
            print(f"FAIL  {fn.__name__}: {exc}")
        except Exception as exc:  # noqa: BLE001 - test harness
            failures += 1
            print(f"ERROR {fn.__name__}: {type(exc).__name__}: {exc}")
    print(f"\n{len(CASES) - failures}/{len(CASES)} passed")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
