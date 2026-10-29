# Humanize Writing Skill

Bilingual agent skills that remove AI tells from prose: **defensive writing**, **explanatory bloat**, **stock AI formulas**, **coined terms**, and **template structure** — while locking down facts, certainty, and the writer's voice.

Two independent skills, not a translation pair. Chinese and English fail differently, and each skill targets its own language's failure mode.

```
skills/
  humanize-zh/   Chinese: defensive fillers, restatement, stock phrases, coined nouns
  humanize-en/   English: same families + sentence bloat (long, clause-stacked sentences)
```

## Why two skills, not one

| | Chinese (`humanize-zh`) | English (`humanize-en`) |
|---|---|---|
| Long sentences | paratactic runs are fine; the disease is stacked 的-modifiers and translationese | subordination collapses fast: relative clauses inside relative clauses |
| Real target | 长定语、多层"的"、名词堆叠 | 45+ word sentences, 3+ stacked subordinate clauses, `-ing` chains, `of` chains |
| Rhythm | 四字格 alternating with short clauses | finite clauses of varied length; fragments are their own tell |
| Fix | split 的-modifiers, restore verbs | split clauses, restore subject-verb, un-nominalize |

So the English skill has a dedicated *sentence craft* section; the Chinese skill warns against copying English habits (and against over-splitting Chinese into staccato fragments, which is its own AI tell).

## What each skill covers

| Family | Chinese | English |
|---|---|---|
| **A. Defensive writing** | 无依据自贬、重复免责、堆叠对冲、虚设反方、安抚 | unearned self-deprecation, repeated disclaimers, stacked hedges, strawman rebuttals |
| **B. Explanatory bloat** | 同义复述、背景重讲、定义癖、元话语、替读者下判断 | restatement, context rebuild, definition habit, metadiscourse, significance gloss |
| **C. Stock formulas** | "不是X而是Y"、"值得注意的是"、"在当今…时代"、"为…提供有力支撑" | "not X but Y", "it's worth noting", "in today's fast-paced world", "plays a crucial role" |
| **D. Coined terms** | 空壳抽象词、概念拼接、伪学术命名、伪机构/伪报告、自造缩略语 | empty abstractions, concept mashups, fake frameworks, fake institutions, unexpanded acronyms |
| **E. Template structure** | 定义→拆项→拔高、每段同构、标题对仗 | definition → three parts → uplift, identical paragraph shapes, paired headings |
| **F. Formatting residue** | 聊天壳、Markdown 残骸、半角标点、emoji 模板 | chatbot wrappers, markdown debris, bold decoration |
| **G. Sentence bloat** | （中文侧不设此条，改查"的"字堆叠） | 45+ words, clause stacking, `-ing` chains, `of` chains |

## The two modules this project adds

Most humanizer skills stop at "delete the filler." This one adds detection for the two failure modes that survive word-level edits:

### 1. Stock-formula detection

A tiered inventory (strong = act on one sighting, weak = act only when clustered) organised by function, not alphabet. Every row carries a keep-condition and a fix direction. False-positive guards: quotations, titles, discussed-as-a-word passages, genre conventions, the writer's own sample.

### 2. Coined-term detection

The most dangerous AI tell is inventing a term that sounds technical and then using it as the argument. Five tests — **definition, provenance, boundary, substitution, prediction** — plus a seven-shape taxonomy (empty abstraction, concept mashup, fake academic naming, fake institution, unexpanded acronym, term drift, fake proper nouns) and a **term ledger** output in audit mode.

## Install

These are plain `SKILL.md` skills with a `references/` folder. Any agent that reads `SKILL.md` can use them.

**Claude Code / Cursor / Codex / similar** — copy the folder into your skills directory:

```bash
git clone https://github.com/ggbondpromax666/humanize-writing-skill.git
cp -r humanize-writing-skill/skills/humanize-zh   ~/.claude/skills/
cp -r humanize-writing-skill/skills/humanize-en   ~/.claude/skills/
```

**DSH / agents that take a skills path** — point the skills directory at `humanize-writing-skill/skills/`. Each subfolder with a `SKILL.md` is one skill.

**Chat-only use** — paste `SKILL.md` into the system prompt or as a project instruction file; add a `references/` file when the task needs the full inventory.

## Usage

The skills run in one of four modes, inferred from the request:

| Mode | Trigger | Output |
|---|---|---|
| **Edit** (default) | "polish this", "tighten it" | final draft + short change note |
| **Audit** | "is this AI-sounding", "check for made-up terms", "audit" | findings only, no rewrite: location, quote, problem, fix |
| **Write from scratch** | "write this in my voice" | draft built from the material, no template frame |
| **File mode** | a file is named | writes only prose back; leaves code, paths, YAML, table data alone |

Audit mode for coined terms also returns the **term ledger**.

## Corpus and candidate scanner

`data/ai-tells.zh.json` and `data/ai-tells.en.json` hold the rule corpus: one regex per entry, plus a **keep-condition** (when the hit is legitimate) and a fix direction. `scripts/scan.py` loads it at runtime, so you can extend the corpus without touching code. Schema and contribution rules: [data/README.md](data/README.md).

```bash
python scripts/scan.py --stats              # entry counts by family/severity, invalid regexes
python scripts/scan.py draft.md             # markdown report
python scripts/scan.py draft.md --json      # machine-readable
python scripts/scan.py --lang zh draft.txt  # force language
python scripts/scan.py paper.tex           # auto-strips LaTeX math and markup
python scripts/scan.py draft.md --strict    # count table rows as usage too
python tests/run_tests.py                   # 13 regression tests
cat draft.txt | python scripts/scan.py -    # stdin
```

It checks stock formulas, defensive fillers, restatement, coined-term triggers, and sentence structure (length, clause stacking, 的-modifier stacks), and skips fenced code blocks. Standard library only.

**A hit is not a reason to edit.** Every entry carries a keep-condition the regex cannot evaluate; the report prints it in a `keep if` column.

A worked example of an academic excerpt (abstract + intro + methods + results) is in [examples/paper-zh-audit.md](examples/paper-zh-audit.md): 8 true positives, zero false positives on method details, sample limits, and cited sources.

`scripts/corpus_tool.py` maintains the corpus (`add` / `observe` / `validate` / `stats`). **After each session, add any tell you found that is not yet in it**, so the next invocation catches it. Admission rules and schema: [data/README.md](data/README.md).

## Design principles

1. **Facts before style.** No rewrite may add a fact, a number, a quote, or a source.
2. **Signal, not word list.** Two tiers of severity; one weak hit is never enough.
3. **Keep-conditions everywhere.** The common failure is deleting a sentence that was doing real work, not missing a tell.
4. **Not a detector bypass.** The goal is clarity and credibility for a reader, not beating AIGC classifiers. No "AI score" is produced.
5. **Language-specific.** Chinese and English are handled by separate rule sets, not mirrored translations.

## Limits

- It cannot verify a source you do not have. It will flag, not invent.
- It does not judge authorship and will not claim a text is or is not AI-written.
- The scanner is a heuristic; expect false positives in legal, academic, and public-administration prose where the "formulas" are genre conventions.

## Provenance and the "AI corpus" question

**There is no AI corpus here.** No scraped dataset, no labelled training set, no corpus statistics. Every list is a hand-built inventory of candidate signals, drawn from three places:

1. public observations, chiefly Wikipedia's ["Signs of AI writing"](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) (which is explicit that these signs are *descriptive, not prescriptive*);
2. the hand-written lists in the four upstream MIT projects;
3. direct observation of model output while editing real drafts.

So this project makes **no accuracy, recall, or "AI detection rate" claims**, and the word lists are not frequency counts. A single item is never evidence.

**What was merged, from where?** [ATTRIBUTION.md](ATTRIBUTION.md) has a per-file table (adapted / synthesized / original), a per-family source map, what counts as original here, and how to cite. Every reference file also opens with a one-line provenance note.

## License and credits

MIT. Methodology merged and rewritten from:

- [blader/humanizer](https://github.com/blader/humanizer) (MIT) — structural taxonomy, evidence thresholds
- [op7418/Humanizer-zh](https://github.com/op7418/Humanizer-zh) (MIT) — constraint priority, edit boundaries in Chinese
- [Devilyuu/anti-defensive-writing-zh](https://github.com/Devilyuu/anti-defensive-writing-zh) (MIT) — defensive-filler tests, Chinese tell inventory
- [petergyang/no-ai-slop](https://github.com/petergyang/no-ai-slop) (MIT) — edit/audit modes, minimum effective edit

New in this project: the explanatory-bloat taxonomy, stock-formula detection, coined-term detection, the term ledger, the bilingual split, and the sentence-craft rules.

## Blind review

This revision came out of a blind review by three independent reviewers who only saw the repository: a writing editor (14 findings), an adversarial tester (17, three high-severity bugs), and a consistency/engineering reviewer (23). Their full reports are in [`review/`](review/).

Fixed in this pass: mixed-language detection, case-sensitive `[A-Z]` acronym rules, duplicate-span hits, unclosed code fences, non-UTF-8 input, short-text verdicts, contradictory rules (source-tag vs purpose-chain in official documents), abstract-vs-informative "Y" in contrast formulas, family-mapping between the SKILL tables and the corpus, broken provenance links after installation, and incomplete attribution for the corpus files.

Still open: the Chinese `platform` family is intentionally larger than the English one (it covers 公文/学术/技术/营销/新闻/职场/教学/邮件 registers that have no direct English equivalent); reference tables and `data/` are maintained in parallel, so a rule added in one is not auto-mirrored in the other.