# 去 AI 味写作 Skill（中英双语）

两个独立的 agent skill，不是互译版本。中文和英文的 AI 腔**不是同一种病**，所以各管各的：清洗防御性表述、解释性表述、AI 固定句式、生造名词与结构模板，同时锁死事实、确定程度和作者声音。

```
skills/
  humanize-zh/   中文：防御填充、复述、固定句式、生造名词
  humanize-en/   英文：同四类 + 长难句（句长、从句嵌套、-ing 链、of 链）
```

## 为什么要分成两个 skill

| | 中文（humanize-zh） | 英文（humanize-en） |
|---|---|---|
| 长句 | 流水句可长，意合推进；病在长定语和多层"的" | 从句套从句会立刻失控 |
| 真正要查 | 长定语、多层"的"、翻译腔名词堆叠、`进行+名词` | 45 词以上长句、3 个以上从句、`-ing` 链、`of` 链 |
| 节奏 | 四字格与短句交替 | 定式从句长短交替；碎片句本身是 AI 腔 |
| 改法 | 拆"的"字定语，还原动词 | 拆从句，还原主谓，去名词化 |

所以英文版单独有一节"句子工艺"，中文版反过来警告两件事：**不要为了简洁把中文拆成五六个字的碎句**（那是另一种 AI 腔），也**不要为了高级叠长定语**。

## 七个痕迹家族

| 家族 | 中文 | 英文 |
|---|---|---|
| A 防御性表述 | 无依据自贬、重复免责、堆叠对冲、虚设反方、安抚 | unearned self-deprecation, repeated disclaimers, strawman rebuttals |
| B 解释性表述 | 同义复述、背景重讲、定义癖、元话语、替读者下判断 | restatement, context rebuild, metadiscourse, significance gloss |
| C 固定句式 | "不是X而是Y"、"值得注意的是"、"在当今…时代"、"为…提供有力支撑" | "not X but Y", "it's worth noting", "in today's fast-paced world" |
| D 生造名词 | 空壳抽象词、概念拼接、伪学术命名、伪机构/伪报告、自造缩略语 | empty abstractions, fake frameworks, fake institutions |
| E 结构模板 | 定义→拆项→拔高、每段同构、标题对仗 | definition → three parts → uplift, paired headings |
| F 排版残留 | 聊天壳、Markdown 残骸、半角标点、emoji 模板 | chatbot wrappers, markdown debris |
| G 长难句 | （中文侧不设此条，改查"的"字堆叠） | 45+ words, clause stacking, `-ing` chains, `of` chains |

## 本项目新增的两个检测模块

多数"去 AI 味"工具停在"删掉空话"。这个项目多做了两件最难、也最容易被漏掉的事：

### 1. AI 固定句式检测

按**功能**而非字母顺序编排的分级清单：`强` = 见一处就处理，`弱` = 成片出现才处理。每一行都带**保留条件**和**改法方向**。误报护栏：引文、标题、讨论该词本身的段落、文体规范、作者旧稿样本。

### 2. 生造名词检测

AI 最危险的痕迹不是话说得空，而是**造一个听起来专业的词，然后拿它当论证**。五问体检——**定义、溯源、边界、替换、预测**——加七种形态（空壳抽象词、概念拼接、伪学术命名、伪机构、自造缩略语、术语漂移、假专名），诊断模式下输出**名词账本**。

## 安装

就是普通的 `SKILL.md` + `references/` 结构，任何能读 `SKILL.md` 的 agent 都能用。

```bash
git clone https://github.com/ggbondpromax666/humanize-writing-skill.git
cp -r humanize-writing-skill/skills/humanize-zh ~/.claude/skills/
cp -r humanize-writing-skill/skills/humanize-en ~/.claude/skills/
```

DSH 之类支持"技能目录"的 agent：把 skills 路径指向 `humanize-writing-skill/skills/`，每个带 `SKILL.md` 的子目录就是一个技能。

只在聊天里用：把 `SKILL.md` 贴进系统提示或项目说明文件；需要完整清单时再补对应的 `references/` 文件。

## 四种模式

| 模式 | 触发 | 输出 |
|---|---|---|
| **改稿**（默认） | "润色一下""去 AI 味""精简" | 终稿 + 简短改动说明 |
| **诊断** | "这段像不像 AI 写的""查一下有没有生造词" | 只报问题，不改写：位置、原句、问题、改法 |
| **从零写** | "按我的口吻写" | 从材料长出来的稿子，不套模板 |
| **文件模式** | 指定了文件 | 只改正文；代码、路径、YAML、表格数据不动 |

生造名词的诊断会额外输出**名词账本**。

## 可选：候选扫描脚本

`scripts/scan.py` 是**候选发现器**，不是判官。它只报位置，判断交回给人或 agent。

```bash
python scripts/scan.py draft.md            # Markdown 报告
python scripts/scan.py draft.md --json     # 机器可读
python scripts/scan.py --lang zh draft.txt # 强制语言
python scripts/scan.py paper.tex          # 自动剥离 LaTeX 公式与命令
python scripts/scan.py draft.md --strict   # 表格行也计入使用
python tests/run_tests.py                  # 13 条回归测试
cat draft.txt | python scripts/scan.py -   # 标准输入
```

它查固定句式、防御填充、复述、生造词触发词，以及句子结构（句长、从句密度、"的"字堆叠），自动跳过代码块。只用标准库。

**语言按句判定，不按整篇判定。** 混排稿按句子边界切段，中文句只套中文语料、英文句只套英文语料，报告会显示切分结果（`language: mixed (zh 12 / en 8 lines)`）。

两条边界规则：真正中英混写的**一句**会**同时**跑两套语料，报告里的 `lang` 列标明命中来自哪套；判语言时**不计引号内的文字**，所以英文句里引用一句中文，仍按英文处理。

**命中不等于该改。** 每条规则都有脚本看不见的保留条件。

论文选段的完整诊断示例见 [examples/paper-zh-audit.md](examples/paper-zh-audit.md)：8 处真阳性，方法细节、样本局限、带出处引用全部未被误判。

`scripts/corpus_tool.py` 负责维护语料库（`add` / `observe` / `validate` / `stats`）。**每次用完把新发现的痕迹回写**，下次自动生效。入库纪律与字段说明见 [data/README.md](data/README.md)。

## 设计原则

1. **事实先于风格**：任何改写都不许新增事实、数字、引文或来源。
2. **信号，不是禁词表**：两级阈值，单个弱信号永远不构成修改理由。
3. **每条都给保留条件**：最常见的失误不是漏删，而是把承担逻辑的句子当 AI 味删掉。
4. **不针对检测器**：目标是让读者更清楚、更信，不是骗过 AIGC 分类器，也不输出"AI 含量"。
5. **语言分开**：中英文各一套规则，不做互译。

## 已知局限

- 无法验证你没有的来源，只会标记，不会编造。
- 不判断作者身份，也不会声称某段"一定是/不是 AI 写的"。
- 扫描脚本是启发式的：在法律、学术、公文这类"套话即规范"的文体里会有误报。

## 出处与"语料库"说明

**本项目没有 AI 语料库。** 没有抓取数据集，没有标注语料，没有语料统计。所有清单都是人工归纳的候选信号表，来源只有三类：

1. 公开观察，主要是 Wikipedia《Signs of AI writing》（它自己就强调这些迹象是*描述性而非规范性*的）；
2. 四个上游 MIT 项目里的人工清单；
3. 改真实稿件时对模型输出的直接观察。

所以本项目**不声称任何"检出率""准确率""召回率"**，词表也不是词频统计结果。单条命中从不作为判断依据。

**融合了什么、来自哪里？** 见 [ATTRIBUTION.md](ATTRIBUTION.md)：逐文件对照表（改编／综合／原创）、按家族的来源映射、原创范围，以及引用格式。每个 `references/` 文件顶部也都有一行出处说明。

## 许可与致谢

MIT。方法论融合并重写自以下项目：

- [blader/humanizer](https://github.com/blader/humanizer)（MIT）：结构性痕迹分类与证据门槛
- [op7418/Humanizer-zh](https://github.com/op7418/Humanizer-zh)（MIT）：约束优先级与中文改写边界
- [Devilyuu/anti-defensive-writing-zh](https://github.com/Devilyuu/anti-defensive-writing-zh)（MIT）：防御填充判别法与中文痕迹表
- [petergyang/no-ai-slop](https://github.com/petergyang/no-ai-slop)（MIT）：编辑/诊断双模式与最小改动原则

本项目新增：解释性表述分类、固定句式检测、生造名词检测、名词账本、中英分治、句子工艺规则。

## 盲审

这一版来自三位独立评审的盲审（他们只看得到仓库，不知道设计意图）：写作编辑 14 条、对抗测试 17 条（含 3 个高危 bug）、工程一致性 23 条。完整报告在 [`review/`](review/)。

本轮已修：中英混排语言误判、`[A-Z]` 缩略语规则被 IGNORECASE 打穿、同一片段重复命中、未闭合代码围栏吞全文、非 UTF-8 输入崩溃、短文本误判 heavy、公文依据句判据冲突、"抽象判断"误删结果句、SKILL 表格与语料库五族无映射、安装后出处链接断链、语料库与 corpus_tool 未列入出处。

仍未解决：中文 `platform` 族刻意大于英文（覆盖公文/学术/技术/营销/新闻/职场/教学/邮件等英文没有对应文体的套话）；`references/` 与 `data/` 是两套并行维护的规则，新增一条不会自动同步到另一边。