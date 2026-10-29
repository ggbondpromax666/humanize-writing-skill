# 出处、融合范围与引用 / Attribution, Provenance, and Citations

这个文件回答三个问题：**规则从哪来、哪些是融合的、哪些是原创**，以及**引用时怎么写**。

---

## 0. 先说清楚：没有"AI 语料库"

本项目**不使用**任何"AI 语料库"、抓取数据集或标注语料。

所有清单都是**人工归纳的候选信号表**，来源只有三类：

1. **公开文献的观察**：主要是 Wikipedia《Signs of AI writing》（WikiProject AI Cleanup 维护）。它明确说明这些迹象是 *descriptive not prescriptive*（描述性而非规范性）——是"AI 写作常见的样子"，不是"AI 写作的判定标准"。
2. **四个上游项目的人工清单**（均为 MIT）：blader/humanizer、op7418/Humanizer-zh、Devilyuu/anti-defensive-writing-zh、petergyang/no-ai-slop。
3. **对模型输出的直接观察**：句式家族、生造名词形态、中英差异，是在真实改稿中反复遇到的形态归纳。

因此：

- 本项目**没有**"AI 检出率""准确率""召回率"这类数字，也不做统计显著性声明；
- 词表**不是**从语料统计出来的高频词，而是"人写得少、模型写得多"的经验归纳；
- 单个词或单条句式**不构成判断依据**，这一点写进了每份清单的使用说明。

如果你在别处看到"AI 语料库""百万级样本训练"，那不是本项目。

---

## 1. 文件级：每个文件融合了什么

| 文件 | 性质 | 上游来源 | 具体改动 |
|---|---|---|---|
| `skills/humanize-zh/SKILL.md` | 结构原创，规则融合 | 四个上游 | 七步管线为原创；红线、优先级顺序、文体表、交付格式改编自 anti-defensive-writing-zh 与 Humanizer-zh；编辑/诊断双模式来自 no-ai-slop |
| `.../humanize-zh/references/defensive-forms.md` | 改编 | **Devilyuu/anti-defensive-writing-zh** `references/defensive-forms.md` | 六道判别、删/留分类表、改法、对称防线均改写自该文件；"中英对照"一节为原创 |
| `.../humanize-zh/references/explanatory-forms.md` | **原创** | 概念受 blader/humanizer §26（re-explaining）与 no-ai-slop（metadiscourse）启发 | 两族十三型分类、密度诊断、改法四招为本项目原创 |
| `.../humanize-zh/references/stock-phrases.md` | **综合** | anti-defensive `references/patterns-zh.md`（C/E 层）、blader/humanizer §1–§25、no-ai-slop "Words to cut / Patterns to cut" | 按**功能**重排为 10 类，补保留条件与误报护栏；具体句式是公共观察，不归任何一方独有 |
| `.../humanize-zh/references/coined-terms.md` | **原创框架** | 灵感来自 humanizer §10（生造复合词）、Humanizer-zh §10、no-ai-slop（weasel attribution） | 五问体检、七形态、处理阶梯、名词账本为原创 |
| `skills/humanize-en/SKILL.md` | 结构原创，规则融合 | 四个上游 | 同中文版骨架；§6.5 句子工艺为原创 |
| `.../humanize-en/references/defensive-forms.md` | 改编 | **blader/humanizer**（§9 qualifiers、§5 arguing with no one）+ **no-ai-slop**（editing principles） | 六道判别与对称防线转写自中文版；英文例句为原创 |
| `.../humanize-en/references/explanatory-forms.md` | **原创** | 同上，概念启发 | 同中文版，英文例句原创 |
| `.../humanize-en/references/stock-phrases.md` | **综合** | humanizer §1–§25、no-ai-slop 词表、Wikipedia | 按功能重排；补保留条件 |
| `.../humanize-en/references/coined-terms.md` | **原创框架** | 同中文版 | 同中文版，英文例句原创 |
| `scripts/scan.py` | **原创代码** | 规则表派生自本项目 `references/` | 正则、严重度阈值、结构检查、去重、JSON 输出均为原创 |

图例：**改编** = 内容主要来自单一上游并重写；**综合** = 多来源合并后重新组织；**原创** = 本项目新写。

---

## 2. 家族级：A–G 的来源映射

| 家族 | 主语料来源 | 本项目新增 |
|---|---|---|
| A 防御性表述 | anti-defensive-writing-zh（判别法、删留表）、humanizer §9 | 中英对照、边界表、输出格式 |
| B 解释性表述 | humanizer §26、no-ai-slop（interpretive metadiscourse） | 十三型分类、密度诊断、四招改法 |
| C AI 固定句式 | humanizer §1–§25、anti-defensive patterns-zh §C/§E、no-ai-slop 词表 | 功能重排、两级阈值、误报护栏 |
| D 生造名词 | humanizer §10（生造复合词）、no-ai-slop（weasel attribution） | 五问体检、七形态、处理阶梯、名词账本 |
| E 结构模板 | humanizer §19–§20、anti-defensive patterns-zh §D | 中英对照判据 |
| F 排版残留 | humanizer §19–§22、anti-defensive patterns-zh §F | 中文半角标点与 Markdown 残骸细则 |
| G 长难句 | **原创**（英文版） | 句长阈值、从句阈值、`-ing`/`of` 链检查、结构扫描 |

---

## 3. 什么算本项目原创

- 七步管线与"删掉检验"作为总闸门的组织方式；
- 解释性表述（B 类）的完整分类；
- 生造名词（D 类）的检测框架与名词账本；
- 中英分治与其差异规则（G 类）；
- `scripts/scan.py` 全部代码；
- 所有中英文对照例句（教学用，非真实材料）。

这些部分如被引用，请引本项目；上游部分请同时引上游。

---

## 4. 上游许可与版权

四份上游均为 **MIT**，允许修改与再分发，要求保留版权与许可声明。完整许可文本见各自仓库：

| 项目 | 仓库 | 许可 |
|---|---|---|
| blader/humanizer | https://github.com/blader/humanizer | MIT |
| op7418/Humanizer-zh | https://github.com/op7418/Humanizer-zh | MIT |
| Devilyuu/anti-defensive-writing-zh | https://github.com/Devilyuu/anti-defensive-writing-zh | MIT |
| petergyang/no-ai-slop | https://github.com/petergyang/no-ai-slop | MIT |

Wikipedia《Signs of AI writing》为 CC BY-SA，本项目只吸收其**观察结论**，不复制原文段落。引用时请注明：

> Wikipedia contributors, "Wikipedia:Signs of AI writing," Wikipedia.

---

## 5. 如何引用本项目 / How to cite

**中文**

> ggbondpromax666. 《去 AI 味写作 Skill（中英双语）》. 2026. https://github.com/ggbondpromax666/humanize-writing-skill

**English**

> ggbondpromax666. *Humanize Writing Skill (Bilingual)*. 2026. https://github.com/ggbondpromax666/humanize-writing-skill

若你只用了某一类规则，建议同时注明上游：

> 防御性表述判别法改编自 Devilyuu/anti-defensive-writing-zh（MIT）；解释性表述与生造名词检测来自 humanize-writing-skill（MIT）。

---

## 6. 一处诚实的说明

`stock-phrases.md` 里的具体句式（如"值得注意的是""it's worth noting"）属于**公共观察**：多个项目、多个作者都独立记录过。本项目不声称对任何单条句式拥有"发现权"，只对**分类方式、阈值、保留条件和检测流程**主张原创。这也意味着：如果某个句式你觉得来源另有其人，欢迎提 issue 补一条引用。
