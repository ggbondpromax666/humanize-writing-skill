#!/usr/bin/env python3
"""Candidate scanner for AI-writing tells (Chinese + English).

This is a *candidate finder*, not a judge. It reports positions so a human or an
agent can check context. A hit is not a reason to edit: every rule in the skill
has keep-conditions, and this script cannot see them.

Usage:
    python scan.py draft.md
    python scan.py draft.md --json
    python scan.py --lang zh draft.txt
    type draft.txt | python scan.py -
    python scan.py draft.md --no-terms

Exit code is always 0 unless the file cannot be read.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field

# ---------------------------------------------------------------------------
# Rule tables
# ---------------------------------------------------------------------------

@dataclass
class Rule:
    pattern: str
    family: str          # stock | defensive | explanatory | coined
    severity: str        # strong | weak
    label: str
    fix: str
    flags: int = 0


def R(pattern, family, severity, label, fix, flags=0):
    return Rule(pattern, family, severity, label, fix, flags)


ZH_RULES = [
    # --- stock formulas -----------------------------------------------------
    R(r"在当今.{0,12}(时代|社会|背景下)", "stock", "strong", "宏大开场", "直接从问题或场景开始"),
    R(r"随着.{0,15}(的快速发展|的不断深入|的普及|的兴起)", "stock", "strong", "假因果开场", "删前半，或写带数据的事实"),
    R(r"(众所周知|毋庸置疑|不言而喻)", "stock", "strong", "用共识替代证据", "删，或给证据"),
    R(r"(值得注意的是|需要指出的是|值得一提的是)", "stock", "strong", "段首评论壳", "删壳直接陈述；要连接就加“这”"),
    R(r"(更重要的是|关键在于|问题在于|核心在于)", "stock", "strong", "重要程度未论证", "删壳或写成因果句"),
    R(r"(不难发现|不难看出|由此可见|可以看出)", "stock", "strong", "假装推理完成", "删或补出推理"),
    R(r"(综上所述|总而言之|总的来说|一言以蔽之)", "stock", "strong", "复述前文", "删；结尾给新结论或行动"),
    R(r"不是.{1,20}[，,]\s*而是", "stock", "strong", "翻案对比", "删虚设的X，直接写Y"),
    R(r"并非.{1,20}[，,]\s*而是", "stock", "strong", "翻案对比", "删虚设的X，直接写Y"),
    R(r"与其说.{1,20}不如说", "stock", "strong", "翻案对比", "直接写结论"),
    R(r"看似.{1,15}[，,]\s*实则", "stock", "strong", "翻案对比", "写清落差的证据"),
    R(r"不仅(是)?.{1,20}[，,]?\s*(更|还)(是)?", "stock", "strong", "递进拔高", "直接写后一层"),
    R(r"(具有重要意义|具有重要的.{0,6}(价值|意义)|意义深远)", "stock", "strong", "拔高意义", "换成具体对象和后果"),
    R(r"(提供了有力(支撑|保障)|奠定了坚实基础|注入新动能|开辟了新路径)", "stock", "strong", "机械拔高", "写具体产出"),
    R(r"(起到了.{0,8}作用|发挥着.{0,8}作用|扮演着.{0,8}角色)", "stock", "strong", "回避简单动词", "改成“是/有/做了”"),
    R(r"(彰显了|体现了|印证了).{0,15}(追求|理念|担当|价值)", "stock", "strong", "句尾补赞美", "删尾巴或给支撑数据"),
    R(r"(未来的?发展|前景|未来).{0,6}(可期|广阔|值得期待)", "stock", "strong", "空展望", "写具体计划或删"),
    R(r"(让我们共同|愿我们|让我们拭目以待)", "stock", "strong", "空号召", "删"),
    R(r"(有研究表明|根据相关研究|大量实践表明|有数据显示|据统计)", "stock", "strong", "模糊归因", "写出作者、年份、期刊；没有就改成作者判断"),
    R(r"(专家认为|学者普遍认为|业内(人士)?认为|国内外.{0,6}一致认为)", "stock", "strong", "匿名权威", "写名字；没有就删归因"),
    R(r"(仅供参考|仅供.{0,4}参考)", "stock", "strong", "悬空免责", "改成带日期的来源或具体范围"),
    R(r"(在一定程度上|从某种意义上(说|讲)|某种程度上)", "stock", "strong", "无对象对冲", "删壳，保留具体范围"),
    R(r"(因人而异|视情况而定|见仁见智)", "stock", "strong", "立场真空", "写出条件分支或作者的判断"),
    R(r"(各有优缺点|机遇与挑战并存|既有机遇也有挑战)", "stock", "strong", "假平衡", "写取舍条件"),
    R(r"(需要理性看待|辩证(地)?看待|客观看待)", "stock", "strong", "空指令", "删"),
    R(r"(有待进一步(研究|探讨)|仍需深入(研究|探讨))", "stock", "strong", "用展望代替结论", "写出具体待研究问题"),
    R(r"(本文将从|下文(将)?(从|分)|接下来我们(来看|看)|下面我们(来看|看))", "stock", "strong", "结构预告", "删，标题已足够"),
    R(r"(本节(介绍|说明|讨论)|本节将)", "stock", "strong", "元话语导航", "删"),
    R(r"(那么问题来了|答案(可能)?(出乎|超乎)你的意料|你以为这就完了)", "stock", "strong", "悬念替代内容", "直接给答案"),
    R(r"(首先.{0,60}其次)", "stock", "weak", "连接词连用", "改成时间/因果/场景推进"),
    R(r"(一方面.{0,60}另一方面)", "stock", "weak", "假平衡", "只写有依据的一边"),
    R(r"(与此同时|在此基础上|具体而言|进一步来说)", "stock", "weak", "逻辑标签", "删，让事情自己排先后"),

    # --- defensive ----------------------------------------------------------
    R(r"(仍有许多不足|还有很多不足|水平有限|能力有限|抛砖引玉|不足之处.{0,6}指正)", "defensive", "strong", "无对象自贬", "删；真实限制写成具体范围"),
    R(r"(以上仅为个人观点|仅代表个人观点)", "defensive", "weak", "重复免责", "全篇只留一次"),
    R(r"(说句实话|我必须诚实地说|说实话)", "defensive", "strong", "装坦诚", "删姿态，留自曝的缺点"),
    R(r"(截至我的知识|目前公开资料有限|现有资料(较少|有限))", "defensive", "strong", "知识截止免责", "整句删；需要时效就写带日期的来源"),
    R(r"(本文由\s*AI\s*(整理|生成)|未经核实处已标注|已保留原意|未改动任何事实)", "defensive", "strong", "流程自述", "删"),
    R(r"(你已经走在正确的路上|完全不用担心|这是一个很好的开始)", "defensive", "strong", "安抚与方向认证", "删或改成“现有信息不足以判断”"),
    R(r"(虽然.{0,12}(只是|仅是).{0,12}[，,].{0,12}(但|却))", "defensive", "strong", "先认不重要再拔高", "删前半"),
    R(r"(可能.{0,6}在一定程度上|也许可能|或许可能|大概可能)", "defensive", "strong", "堆叠限定", "收成一层"),

    # --- explanatory --------------------------------------------------------
    R(r"(换句话说|也就是说|简而言之|通俗(地)?讲)", "explanatory", "strong", "同义复述", "只留更好懂的那一版"),
    R(r"(更准确地说|具体来说|具体而言)", "explanatory", "weak", "伪精确化", "后句没更具体就删"),
    R(r"(正如前文所述|如前所述|前面(我们)?提到)", "explanatory", "weak", "前文回指", "长文留一次，其余删或具体指代"),
    R(r"(这意味着|这说明|由此可见).{0,20}", "explanatory", "strong", "替读者下判断", "删，让事实自己说话"),
    R(r"(所谓.{1,10}[，,].{0,30}(是指|就是))", "explanatory", "weak", "定义癖", "常识词不必定义"),

    # --- coined terms -------------------------------------------------------
    R(r"所谓[“\"「]?([^”\"」，。]{2,12})[”\"」]?", "coined", "strong", "引号新名词（需体检）", "做五问体检：定义/溯源/边界/替换/预测"),
    R(r"(称之为|被称为|业内称为|号称)[“\"「]?([^”\"」，。]{2,16})[”\"」]?", "coined", "strong", "命名无出处", "补出处或降级为描述"),
    R(r"([\u4e00-\u9fa5]{2,6})(模型|框架|效应|定律|飞轮|方法论|范式)(?![，。、）)])", "coined", "weak", "伪学术命名候选", "查提出者与原始文献"),
    R(r"(某(研究院|机构|协会|高校)|权威(机构|部门)|国际.{0,6}(协会|组织)).{0,12}(报告|数据|标准|白皮书)", "coined", "strong", "伪机构/伪报告", "删除或标〔需查证来源〕，不补来源"),
    R(r"《[^》]{2,30}(白皮书|报告|蓝皮书)》", "coined", "weak", "报告名（需核实存在）", "核对报告名与发布方"),
]

EN_RULES = [
    R(r"\b(in today's|in an?)\s+(fast-paced|ever-changing|rapidly evolving|digital|modern)\b", "stock", "strong", "world-staging opener", "open on the problem or a scene"),
    R(r"\b(it'?s|it is)\s+(worth|important)\s+(noting|to note)\b", "stock", "strong", "paragraph opener, no referent", "delete the frame, state the fact"),
    R(r"\b(notably|importantly|crucially|interestingly|indeed)\s*,", "stock", "strong", "adverb asserting significance", "delete"),
    R(r"\b(here'?s the thing|the truth is|the reality is|let me be clear)\b", "stock", "strong", "fake-insight setup", "state the point"),
    R(r"\b(what most people (get wrong|miss)|the part (everyone|nobody)|nobody tells you)\b", "stock", "strong", "faux-insight setup", "make the claim stand alone"),
    R(r"\b(isn'?t|is not|not)\s+(just\s+)?(about\s+)?\w+[,.]?\s*(it'?s|but)\b", "stock", "strong", "binary contrast", "state Y only"),
    R(r"\b(less about|more about)\b", "stock", "strong", "binary contrast", "give the trade-off"),
    R(r"\b(plays?|played)\s+(a\s+)?(crucial|vital|pivotal|key|critical)\s+role\b", "stock", "strong", "importance inflation", "say what it does"),
    R(r"\b(serves? as a testament|stands? as a testament|a testament to)\b", "stock", "strong", "testament puffery", "delete"),
    R(r"\b(mark(s|ed)? a (pivotal|turning) moment|paves? the way for|solidifies?)\b", "stock", "strong", "historical/forward inflation", "state the event"),
    R(r"\b(underscor(e|es|ing)|highlight(s|ing)?|reflect(s|ing)?)\s+(the|its)\s+(\w+\s+){0,2}(importance|significance|commitment)", "stock", "strong", "trailing significance rider", "keep the fact, cut the rider"),
    R(r"\b(experts (agree|say|believe)|many argue|it is widely believed|studies show|research suggests)\b", "stock", "strong", "vague attribution", "name the source or cut"),
    R(r"\b(industry reports?|a recent (report|study)|sources say)\b", "stock", "strong", "fake provenance", "name it or delete"),
    R(r"\b(to some extent|in some ways|generally speaking|for the most part|arguably)\b", "stock", "strong", "hedge without referent", "give the scope"),
    R(r"\b(in other words|put simply|that is to say|simply put)\b", "stock", "strong", "metadiscourse restatement", "keep the clearer version, delete the frame"),
    R(r"\b(let'?s (dive|explore|break)|without further ado)\b", "stock", "strong", "run-up", "delete"),
    R(r"\b(in conclusion|in summary|ultimately|at the end of the day|the future looks bright|only time will tell)\b", "stock", "strong", "recap/uplift closer", "end on the last concrete fact"),
    R(r"\b(what if I told you|think about it|plot twist|but here'?s the catch|sound familiar)\b", "stock", "strong", "rhetorical setup", "state it plainly"),
    R(r"\b(delve|tapestry|realm|leverage|seamless|pivotal|meticulous|intricate|multifaceted|foster|embark|unleash|harness|elevate|empower|streamline|cutting-edge|paradigm shift|game changer|transformative|holistic|synergy|ever-evolving|unprecedented|supercharge)\b", "stock", "weak", "AI-favored vocabulary", "check density; one word is not a tell"),
    R(r"\b(serves? as|functions? as|acts? as|represents?|boasts?|features?)\b", "stock", "weak", "weak verb", "is / has / the specific verb"),
    R(r"\b(highlighting|underscoring|emphasizing|reflecting|showcasing|symbolizing|ensuring|fostering|contributing to)\b", "stock", "weak", "shallow -ing rider", "keep only if the source supports it"),

    R(r"\b(just my two cents|still has (many )?limitations|for reference only)\b", "defensive", "strong", "unearned self-deprecation", "delete; convert real limits to scope"),
    R(r"\b(let me be honest|I'?ll be honest|to be frank)\b", "defensive", "strong", "performed candor", "delete posture, keep disclosure"),
    R(r"\b(as of my last (update|training)|public information is limited|information is scarce)\b", "defensive", "strong", "knowledge-cutoff disclaimer", "delete the sentence"),
    R(r"\b(compiled by AI|unverified items are (flagged|marked)|your meaning has been preserved)\b", "defensive", "strong", "process narration", "delete"),

    R(r"\b(in other words|that is to say|put simply)\b", "explanatory", "strong", "synonym restatement", "keep one version"),
    R(r"\b(this (means|shows|demonstrates) that)\b", "explanatory", "strong", "judgment on the reader's behalf", "delete; let facts carry it"),
    R(r"\b(this (article|section|piece) (will|covers)|in this section)\b", "explanatory", "strong", "metadiscourse navigation", "delete; headings suffice"),

    R(r"\b(the [A-Z][A-Za-z]+ (framework|model|effect|method|principle))\b", "coined", "weak", "framework name (verify origin)", "check proposer and source"),
    R(r"\b([A-Z]{2,6})\s+(model|framework|method)\b", "coined", "weak", "unexpanded acronym + label", "expand at first use"),
    R(r"\b(a (leading|major|top) (research institute|industry report|white paper))\b", "coined", "strong", "fake institution", "delete or mark [needs source]"),
]

CODE_FENCE = re.compile(r"^\s*(```|~~~)")


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


@dataclass
class Report:
    hits: list = field(default_factory=list)
    terms: list = field(default_factory=list)
    stats: dict = field(default_factory=dict)


def strip_code(text: str) -> str:
    """Blank out fenced code blocks so code never triggers the scanner."""
    out, in_fence = [], False
    for line in text.splitlines():
        if CODE_FENCE.match(line):
            in_fence = not in_fence
            out.append("")
            continue
        out.append("" if in_fence else line)
    return "\n".join(out)


def pick_rules(lang: str):
    if lang == "zh":
        return ZH_RULES
    if lang == "en":
        return EN_RULES
    return ZH_RULES + EN_RULES


def guess_lang(text: str) -> str:
    cjk = sum(1 for ch in text if "\u4e00" <= ch <= "\u9fff")
    return "zh" if cjk > len(text) * 0.08 else "en"


EN_SUBORDINATORS = re.compile(
    r"\b(which|that|who|whose|whom|whereas|although|though|unless|because|since|while|whereby)\b",
    re.IGNORECASE,
)


def structure_hits(lines, lang: str) -> list:
    """Sentence-level checks: length and clause density.

    English fails on subordination; Chinese fails on stacked 的-modifiers.
    """
    hits = []
    if lang == "zh":
        for i, line in enumerate(lines, 1):
            for sent in re.split(r"[。！？]", line):
                chars = len(re.findall(r"[\u4e00-\u9fa5]", sent))
                if chars >= 120:
                    hits.append(Hit(i, 1, sent.strip()[:60], "structure", "strong",
                                    "超长句（≥120 字）", "按语义拆成两句以上"))
                elif chars >= 80:
                    hits.append(Hit(i, 1, sent.strip()[:60], "structure", "weak",
                                    "长句（≥80 字）", "检查能否拆"))
                if sent.count("的") >= 4:
                    hits.append(Hit(i, 1, sent.strip()[:60], "structure", "weak",
                                    "的字定语堆叠（≥4）", "拆成短句，还原动词"))
    else:
        for i, line in enumerate(lines, 1):
            for sent in re.split(r"[.!?]", line):
                words = len(re.findall(r"[A-Za-z][A-Za-z']*", sent))
                if words >= 45:
                    hits.append(Hit(i, 1, sent.strip()[:60], "structure", "strong",
                                    f"very long sentence ({words} words)", "split at a conjunction"))
                elif words >= 30:
                    hits.append(Hit(i, 1, sent.strip()[:60], "structure", "weak",
                                    f"long sentence ({words} words)", "check whether the joint can be split"))
                subs = EN_SUBORDINATORS.findall(sent)
                if len(subs) >= 3:
                    hits.append(Hit(i, 1, sent.strip()[:60], "structure", "weak",
                                    "clause stacking (3+ subordinates)", "promote one clause to a main clause"))
                if sent.count(" of ") >= 3:
                    hits.append(Hit(i, 1, sent.strip()[:60], "structure", "weak",
                                    "of-chain (3+)", "reorder: actor first"))
    return hits


def scan(text: str, lang: str) -> Report:
    clean = strip_code(text)
    lines = clean.splitlines()
    rules = pick_rules(lang)
    rep = Report()
    for i, line in enumerate(lines, 1):
        if not line.strip():
            continue
        for rule in rules:
            flags = rule.flags | (re.IGNORECASE if lang in ("en", "auto") else 0)
            for m in re.finditer(rule.pattern, line, flags):
                rep.hits.append(Hit(
                    line=i, col=m.start() + 1, text=m.group(0)[:60],
                    family=rule.family, severity=rule.severity,
                    label=rule.label, fix=rule.fix,
                ))
    rep.hits.extend(structure_hits(lines, lang))
    # The same span can be claimed by two cross-listed rules; keep one.
    deduped, seen = [], set()
    for h in rep.hits:
        key = (h.line, h.col, h.text, h.label)
        if key in seen:
            continue
        seen.add(key)
        deduped.append(h)
    rep.hits = deduped
    rep.terms = find_terms(lines, lang)
    rep.stats = compute_stats(clean, rep.hits, lang)
    return rep


TERM_PATTERNS = [
    (r"[“\"「]([\u4e00-\u9fa5]{2,10})[”\"」]", "引号名词", 1),
    (r"[\u4e00-\u9fa5]{2,6}(?:体系|闭环|飞轮|抓手|底座|生态|链路|矩阵|心智|势能|引擎)", "复合抽象名词", 0),
    (r"(?:[A-Za-z][A-Za-z\-]*\s+){1,3}(?:framework|model|loop|flywheel|matrix)", "英文框架名", 0),
]

# Leading characters that are grammar, not part of a noun phrase.
TERM_STOP = "了的是在和与及为我们他们你们它们这那其该此把被将对于用使让以及么"
EN_STOP = {"the", "a", "an", "our", "their", "its", "this", "that", "in", "of", "grounded"}


def clean_term(raw: str) -> str:
    """Trim grammatical noise that the noun-phrase regex drags in."""
    t = raw.strip()
    # Chinese: drop anything up to and including a grammatical particle.
    for ch in "了的是在和与为把被将":
        idx = t.rfind(ch)
        if 0 <= idx < len(t) - 1:
            t = t[idx + 1:]
    while t and t[0] in TERM_STOP:
        t = t[1:]
    # English: drop leading function words.
    words = t.split()
    while words and words[0].lower() in EN_STOP:
        words = words[1:]
    return " ".join(words)


def find_terms(lines, lang: str) -> list:
    seen = {}
    for i, line in enumerate(lines, 1):
        for pat, kind, gidx in TERM_PATTERNS:
            for m in re.finditer(pat, line, re.IGNORECASE):
                term = clean_term(m.group(gidx))
                if len(term) < 2:
                    continue
                if term not in seen:
                    seen[term] = {"term": term, "line": i, "kind": kind, "count": 0}
                seen[term]["count"] += 1
    terms = list(seen.values())
    terms.sort(key=lambda t: (-t["count"], t["line"]))
    return terms[:20]


def compute_stats(text: str, hits: list, lang: str) -> dict:
    if lang == "zh":
        sentences = len(re.findall(r"[。！？；]", text)) or 1
        words = len(re.findall(r"[\u4e00-\u9fa5]", text))
        unit_label = "characters"
    else:
        sentences = len(re.findall(r"[.!?;]", text)) or 1
        words = len(re.findall(r"\b\w+\b", text))
        unit_label = "words"
    strong = sum(1 for h in hits if h.severity == "strong")
    weak = len(hits) - strong
    density = round((strong * 1000) / max(words, 1), 2)
    return {
        "sentences": sentences,
        "units": words,
        "unit_label": unit_label,
        "strong_hits": strong,
        "weak_hits": weak,
        "strong_per_1000_units": density,
        "verdict": density_verdict(density, strong, weak),
    }


def density_verdict(d: float, strong: int, weak: int) -> str:
    if strong == 0 and weak == 0:
        return "clean - no candidates found"
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
    units = rep.stats["units"]
    label = rep.stats["unit_label"]
    density = rep.stats["strong_per_1000_units"]
    out = []
    out.append(f"# Candidate scan: {path}")
    out.append(f"language: {lang} | {label}: {units} | sentences: {rep.stats['sentences']}")
    out.append(
        f"strong hits: {rep.stats['strong_hits']} ({density} per 1000 {label}) "
        f"| weak hits: {rep.stats['weak_hits']}"
    )
    out.append(f"verdict: {rep.stats['verdict']}")
    out.append("")
    out.append("A hit is a candidate, not a verdict. Check context before editing.")
    out.append("")

    if rep.hits:
        out.append("## Stock formulas, defenses, explanations")
        out.append("")
        out.append("| line | severity | family | hit | label | suggested fix |")
        out.append("|---|---|---|---|---|---|")
        for h in sorted(rep.hits, key=lambda h: (h.line, h.col)):
            snippet = h.text.replace("|", "\\|")
            out.append(
                f"| {h.line} | {h.severity} | {h.family} | `{snippet}` | {h.label} | {h.fix} |"
            )
        out.append("")
    else:
        out.append("## Stock formulas, defenses, explanations")
        out.append("")
        out.append("No matches.")
        out.append("")

    if rep.terms:
        out.append("## Suspect terms (run the five tests)")
        out.append("")
        out.append("| term | first line | kind | count |")
        out.append("|---|---|---|---|")
        for t in rep.terms:
            out.append(f"| {t['term']} | {t['line']} | {t['kind']} | {t['count']} |")
        out.append("")
        out.append("Tests: definition, provenance, boundary, substitution, prediction.")
        out.append("")

    out.append("## Next")
    out.append("")
    out.append("1. Every strong hit: keep, tighten, or delete, using the skill's keep-conditions.")
    out.append("2. Every term: ledger it. Only delete what you can prove is empty.")
    out.append("3. Never add a fact or a source to fix a finding.")
    return "\n".join(out)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Find candidate AI-writing tells (zh/en).")
    ap.add_argument("path", help="file to scan, or - for stdin")
    ap.add_argument("--lang", choices=["zh", "en", "auto"], default="auto")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--no-terms", action="store_true", help="skip term candidates")
    args = ap.parse_args(argv)

    try:
        text = sys.stdin.read() if args.path == "-" else open(args.path, encoding="utf-8").read()
    except OSError as exc:
        print(f"cannot read {args.path}: {exc}", file=sys.stderr)
        return 1

    lang = guess_lang(text) if args.lang == "auto" else args.lang
    rep = scan(text, lang)
    if args.no_terms:
        rep.terms = []

    if args.json:
        payload = {
            "path": args.path,
            "language": lang,
            "stats": rep.stats,
            "hits": [h.__dict__ for h in rep.hits],
            "terms": rep.terms,
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(render(rep, args.path, lang))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
