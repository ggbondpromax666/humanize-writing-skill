# 盲审报告 C：工程一致性（结构 / 对齐 / 体积）

- **审查对象**：`humanize-writing-skill`（绝对路径 `C:\Users\Lenovo\OneDrive\文档\deepseek-harness\default-workspace\humanize-writing-skill`）
- **审查日期**：2026-10-29
- **审查者**：reviewer-consistency（独立盲审，仅依据仓库产物）
- **审查范围**：整个仓库（14 个 Markdown、2 个 data JSON、2 个 Python 脚本、LICENSE / .gitignore / .gitattributes）
- **审查方式**：静态阅读 + 脚本化校验（Python 3.13.13 / PyYAML 6.0.3）+ 隔离副本中的异常输入与安装模拟
- **约束遵守**：除本文件外未修改仓库任何文件；未运行 git；所有破坏性测试均在系统临时目录的副本中进行

**结论（一句话）**：基础工程质量好于同类项目（frontmatter 合法、仓库内 32 条相对链接全部可达、8/8 references 有出处行、data 无重复 ID/正则、脚本无写死盘符、200KB 输入 0.2–0.5s），但**存在 3 个阻断级一致性问题**：语料库的 `platform` 家族（73 条，占 22.4%）在 SKILL / README / ATTRIBUTION 中均无定义（SKILL 仅列举族名）、无清单、无来源；出处声明「每个文件」漏掉 326 条规则的 data JSON 与 corpus_tool.py；以及按 README 安装命令复制技能目录后，10 条 ATTRIBUTION 出处链接全部失效。

---

## 一、问题统计

| 档位 | 数量 | 编号 |
|---|---|---|
| **阻断** | **3** | B1、B2、B3 |
| **重要** | **9** | I1–I9 |
| **次要** | **11** | M1–M11 |
| **合计** | **23** | — |

### 最严重的 3 条

1. **B1 家族体系分裂**：data 用 `stock/defensive/explanatory/coined/platform` 五族，SKILL 用 A–F / A–G 六/七类，两套分类没有任何映射；`platform`（中文 63 条 + 英文 10 条）在 README 与 ATTRIBUTION 中零出现，在 SKILL 中只作为「五族」名称被列举一次，从未被定义，也没有对应 references 文件。
2. **B2 出处声明名不副实**：`ATTRIBUTION.md:27` 标题为「文件级：**每个文件**融合了什么」，但 `data/ai-tells.zh.json`、`data/ai-tells.en.json`（全部 326 条规则的载体）和 `scripts/corpus_tool.py` 完全不在表中（`grep` 命中 0），且平台家族在 A–G 来源映射中缺行。
3. **B3 安装即断链**：按 `README.md:54-57` / `README.zh-CN.md:50-53` 的 `cp -r …skills/humanize-zh ~/.claude/skills/` 安装后，两个 SKILL.md 与 8 个 references 文件中的 10 条 `ATTRIBUTION.md` 相对链接全部指向不存在的 `~/.claude/ATTRIBUTION.md`（模拟安装实测 10 条 BROKEN）。

### 一致性维度总览

| 维度 | 结论 |
|---|---|
| skills 目录结构对称性 | ✅ 基本对称：两个技能均为 `SKILL.md + references/{stock,defensive,explanatory,coined}`，4 个文件名完全相同；工作流均为 7 步 |
| 家族/标签跨语言对齐 | ❌ 不对齐：`platform` zh=63 / en=10（差 53）；语义集也不同（见 I7 表） |
| 声明 vs 实现 | ❌ 4 处不符：四模式（I1）、分类数量（I2/I3）、出处完整性（B2）、安装可用性（B3） |
| frontmatter 合法性 | ✅ 两个 SKILL.md 均可被 YAML 解析，`name`/`description` 齐全，description 均 < 1024 字符（en 927 / zh 310，en 接近上限见 M8） |
| 相对链接有效性（仓库内） | ✅ 32/32 可达（脚本校验无 BROKEN） |
| 相对链接有效性（安装后） | ❌ 10/10 断链（B3） |
| 加载体积 | ⚠️ en SKILL ≈5.3k tokens / zh ≈5.0k tokens，均达建议上限；references 73KB 按需加载尚可（M7） |
| 可维护性 | ❌ 存在三套规则/清单来源（data JSON、scan.py 内联表、references）且两两无同步校验（I4、I8） |
| 安全/鲁棒 | ⚠️ 无写死路径 ✅；非 UTF-8 输入崩溃（I6）、corpus_tool 在损坏/缺失 JSON 上 traceback（见 I6 附注） |

---

## 二、阻断问题（3）

### B1 ｜ 家族体系分裂：`platform` 五族 vs SKILL 的 A–G 七类，73 条规则无文档、无清单、无来源

**文件:行号**
- `data/README.md:6-8`（声明两份 data 各自按 `stock / defensive / explanatory / coined / platform` 组织）、`data/README.md:38`（`fam` 枚举含 `platform`）
- `skills/humanize-zh/SKILL.md:27-38`（「六类 AI 痕迹」只有 A–F，无 platform）、`:196`（却说语料库按「五族」组织）
- `skills/humanize-en/SKILL.md:27-37`（「Seven families」只有 A–G，无 platform）、`:232`（同样说「五族」）
- `ATTRIBUTION.md:49-57`（家族来源映射只有 A–G，无 platform）
- `README.md:26-34` / `README.zh-CN.md:22-32`（家族表只有 A–G）
- `scripts/scan.py:35`（`family: str  # stock | defensive | explanatory | coined | platform`）

**证据（命令输出）**

```text
PS> python scripts/corpus_tool.py stats
zh: v1.1.0 | 192 entries (strong=76, weak=116) | coined=21, defensive=21, explanatory=12, platform=63, stock=75
en: v1.0.0 | 134 entries (strong=81, weak=53) | coined=12, defensive=18, explanatory=14, platform=10, stock=80
total: 326 entries
```

```text
PS> python -c "import pathlib; print([p.name for p in pathlib.Path('skills/humanize-zh/references').iterdir()])"
['coined-terms.md', 'defensive-forms.md', 'explanatory-forms.md', 'stock-phrases.md']
# 两个技能都只有 4 个 references 文件；没有 platform/template/formatting 的清单文件
```

```text
PS> grep -R "platform" README.md README.zh-CN.md ATTRIBUTION.md
# → 0 命中（README / ATTRIBUTION 完全没有 platform 这个词）

PS> grep -n "platform" skills/*/SKILL.md
skills/humanize-zh/SKILL.md:196: …按 stock / defensive / explanatory / coined / platform 五族组织…
skills/humanize-en/SKILL.md:232: …across stock / defensive / explanatory / coined / platform…
# 仅出现于「语料库现状（--stats）」一句；没有任何规则/章节/清单解释该族
```

- `platform` 是**中文语料库第一大族**：63/192 = **32.8%**；全库 73/326 = **22.4%**。
- 该族语义上是一个大杂烩，横跨公文、营销、教育、新闻、邮件、互联网黑话，与 A–F 的分类正交：`data/ai-tells.zh.json:92`（公文「进一步推进」）、`:106`（学术「研究表明」）、`:127`（收益承诺「月入过万」）、`:146`（课堂「本节课我们将学习」）、`:213`（营销「遥遥领先」）；`data/ai-tells.en.json:138-147` 则是 LinkedIn/email/academic/tech marketing。
- 后果：agent 调 `scan.py` 得到的报告里 `family=platform` 无法对应到 SKILL.md 的任何一节；人类维护者也拿不到该族的完整清单与改法说明。`zh` 与 `en` 的 platform 条数差 53 条，进一步说明这不是有意的「语言差异」，而是文档与数据脱节。

**修复建议（任选其一，推荐 A）**
- A. 把 `platform` 正式并入分类体系：在 SKILL.md 家族表增加 G（中文）/H（英文）「平台与文体模板」，补 `references/platform-forms.md`，ATTRIBUTION 家族映射增行，并把 data/README 的五族与 SKILL 的字母类做一张显式映射表。
- B. 取消 `platform` 族：按语义把 73 条拆入 `stock`/`defensive`/`explanatory`/`coined`，`fam` 枚举收敛为四族，同步 `scan.py:35`、`corpus_tool.py:31`、`data/README.md:38`。

---

### B2 ｜ ATTRIBUTION 的「每个文件」出处表漏掉 326 条规则的 data JSON 与 corpus_tool.py；platform 家族无来源行

**文件:行号**
- `ATTRIBUTION.md:27`（标题「## 1. 文件级：**每个文件**融合了什么」）
- `ATTRIBUTION.md:31-41`（表内只列 2 个 SKILL.md + 8 个 references + `scripts/scan.py`，共 11 行）
- `ATTRIBUTION.md:49-57`（A–G 家族来源映射，无 platform）
- `README.md:119`（「ATTRIBUTION.md has a per-file table (adapted / synthesized / original), a per-family source map」）
- `README.zh-CN.md:112`（同一承诺的中文版）

**证据（命令输出）**

```text
PS> python -c "t=open('ATTRIBUTION.md',encoding='utf-8').read(); print({k:t.count(k) for k in ['ai-tells','corpus_tool','data/','scripts/scan.py','platform']})"
{'ai-tells': 0, 'corpus_tool': 0, 'data/': 0, 'scripts/scan.py': 2, 'platform': 0}
```

```text
ATTRIBUTION.md 中被反引号列出的路径（去重）：
  .../humanize-zh/references/coined-terms.md
  .../humanize-zh/references/defensive-forms.md
  .../humanize-zh/references/explanatory-forms.md
  .../humanize-zh/references/stock-phrases.md
  .../humanize-en/references/coined-terms.md
  .../humanize-en/references/defensive-forms.md
  .../humanize-en/references/explanatory-forms.md
  .../humanize-en/references/stock-phrases.md
  skills/humanize-zh/SKILL.md
  skills/humanize-en/SKILL.md
  scripts/scan.py
# 缺：data/ai-tells.zh.json、data/ai-tells.en.json、scripts/corpus_tool.py、data/README.md
```

- data JSON 是**规则本体的唯一主数据源**：`README.md:79` 明确「`data/ai-tells.*.json` hold the rule corpus… you can extend the corpus without touching code」，`scan.py:150-181` 优先从 data 加载；`references/*.md` 只是散文清单。但 ATTRIBUTION 只给散文清单做出处，反而漏掉真正承载 326 条来自上游（blader/humanizer、anti-defensive-writing-zh、no-ai-slop 等，均为 MIT）的规则的 JSON 文件。
- `scripts/corpus_tool.py`（208 行、负责写入语料库）同样无任何出处/原创声明，而 ATTRIBUTION:41 只声明了 `scan.py`。
- platform 家族 73 条在 `ATTRIBUTION.md:49-57` 的 A–G 来源映射里没有对应行，等于 22.4% 的语料**没有任何来源归属**。对以「per-file provenance」为卖点的仓库，这是许可与可信度层面的硬伤。

**修复建议**
1. ATTRIBUTION §1 增三行：`data/ai-tells.zh.json`、`data/ai-tells.en.json`（性质=综合，主来源=四个上游清单 + Wikipedia，说明「正则与 keep 条件为本项目重写」）、`scripts/corpus_tool.py`（原创代码）。
2. ATTRIBUTION §2 增 platform 行（或随 B1 的合并方案撤销该族）。
3. 在 `scripts/` 下加一条校验（或 CI）：`git ls-files` 中的每个 skill/script/data 产物路径必须出现在 ATTRIBUTION 表格中，否则 fail。

---

### B3 ｜ 按 README 的安装命令复制后，10 条 ATTRIBUTION 出处链接全部失效

**文件:行号**
- `README.md:54-58`（安装命令：`cp -r humanize-writing-skill/skills/humanize-zh ~/.claude/skills/`，把技能文件夹单独复制走）
- `README.zh-CN.md:50-54`（同样命令）
- `skills/humanize-zh/SKILL.md:10`、`skills/humanize-en/SKILL.md:10`（`[ATTRIBUTION.md](https://github.com/ggbondpromax666/humanize-writing-skill/blob/main/ATTRIBUTION.md)`）
- 8 个 references 文件第 3 行（`[ATTRIBUTION.md](https://github.com/ggbondpromax666/humanize-writing-skill/blob/main/ATTRIBUTION.md)`，如 `skills/humanize-zh/references/defensive-forms.md:3`）

**证据（模拟安装后的链接校验）**

```text
# 模拟 README 的安装步骤（临时目录，不影响仓库）：
#   cp -r skills/humanize-zh ~/.claude/skills/ ; cp -r skills/humanize-en ~/.claude/skills/
installed tree: C:\Users\Lenovo\AppData\Local\Temp\fake_claude_8yfnss2u\.claude\skills
broken relative links after documented install: 10
  BROKEN humanize-en\references\coined-terms.md:3 -> ../../../ATTRIBUTION.md  (resolved: ...\.claude\ATTRIBUTION.md)
  BROKEN humanize-en\references\defensive-forms.md:3 -> ../../../ATTRIBUTION.md
  BROKEN humanize-en\references\explanatory-forms.md:3 -> ../../../ATTRIBUTION.md
  BROKEN humanize-en\references\stock-phrases.md:3 -> ../../../ATTRIBUTION.md
  BROKEN humanize-en\SKILL.md:10 -> ../../ATTRIBUTION.md
  BROKEN humanize-zh\references\coined-terms.md:3 -> ../../../ATTRIBUTION.md
  BROKEN humanize-zh\references\defensive-forms.md:3 -> ../../../ATTRIBUTION.md
  BROKEN humanize-zh\references\explanatory-forms.md:3 -> ../../../ATTRIBUTION.md
  BROKEN humanize-zh\references\stock-phrases.md:3 -> ../../../ATTRIBUTION.md
  BROKEN humanize-zh\SKILL.md:10 -> ../../ATTRIBUTION.md
```

- 对照：**在仓库内**这 32 条相对链接全部可达（只有安装场景才断），所以常规 link-check 不会发现，属于「文档承诺的安装路径未经验证」。
- 同一段 SKILL.md 第 10 行还写着「逐文件对照与原创声明见 ATTRIBUTION.md」，安装后这句话直接变成死链，B2 的出处问题在最终用户侧被放大。

**修复建议**
1. 把 `ATTRIBUTION.md`（或精简版 `ATTRIBUTION.md`）复制进两个技能目录，SKILL 链接改为 `ATTRIBUTION.md`（同目录）；references 改为 `../ATTRIBUTION.md`。安装命令无需改。
2. 或者修改安装文档：同时 `cp ATTRIBUTION.md` 到目标 skills 根目录，并在 README 中写明；安装后用脚本校验一次链接。
3. 加一个 CI/本地脚本：以「模拟安装后的目录树」为根重跑链接检查（本轮审查已给出可复用的检查方法）。

---

## 三、重要问题（9）

### I1 ｜ README 声称「四模式」，两份 SKILL.md 只定义了三种（「从零写 / Write from scratch」不存在）

**文件:行号**
- `README.md:66`（「The skills run in one of four modes」）、`README.md:72`（表格行 `**Write from scratch**`）
- `README.zh-CN.md:60`（「## 四种模式」）、`:66`（「**从零写**」）
- `skills/humanize-zh/SKILL.md:210-215`（§八 交付格式只有：改稿（默认）/ 诊断 / 文件模式）
- `skills/humanize-en/SKILL.md:246-251`（§8 Output 只有：Edit (default) / Audit / File mode）

**证据**

```text
grep -R "from scratch|从零" README.md README.zh-CN.md skills/*/SKILL.md
README.md:72      ← 仅 README
README.zh-CN.md:66 ← 仅 README
skills/humanize-*/SKILL.md: 0 命中
```

- `README.md:66` 还说模式是「inferred from the request」，但 SKILL.md 未写任何模式判定规则；`en SKILL.md:248-250` 三行只覆盖 edit/audit/file 三种输出。
- 影响：agent 只读 SKILL.md 时不会进入「按用户口吻从材料起草」模式；README 的对外承诺与实现不一致。

**修复建议**：在 SKILL.md §8/§八 增加第 4 种模式（触发语、输入、输出、与 Edit 的边界），或删除 README 的两处「四模式」表述并把标题改为「三种模式」。

### I2 ｜ references 的分类数量自相矛盾：中文「两族十二型」、英文「Two families, thirteen shapes」，实际都是 4 族 15 型

**文件:行号**
- `skills/humanize-zh/references/explanatory-forms.md:18`（`## 一、两族十二型`）
- `skills/humanize-en/references/explanatory-forms.md:18`（`## 1. Two families, thirteen shapes`）
- `ATTRIBUTION.md:33`（「两族十三型分类…为本项目原创」）、`ATTRIBUTION.md:52`（B 类「十三型分类」）
- 正文实际结构：zh 文件 `:20/:31/:41/:49` 四个 `### 甲/乙/丙/丁族`，正文编号 `| 1 |`…`| 15 |`（`:24-55`）；en 文件 `:20/:31/:41/:49` 四个 `### Family A–D`，同样是 15 型

**证据**

```text
zh explanatory-forms.md: family-headings=4 -> ['### 甲族｜复述型…','### 乙族｜供给过量型…','### 丙族｜元话语型…','### 丁族｜意义解释型…']; numbered types 1..15 = 15
en explanatory-forms.md: family-headings=4 -> ['### Family A — Restatement…','### Family B — Over-supply…','### Family C — Metadiscourse…','### Family D — Significance…']; numbered types 1..15 = 15
```

- 三处声明三个数：**12（中）/13（英）/13（ATTRIBUTION）**，实际 **4 族 15 型**。这不仅与实现不符，也是**中英两版对同一现象的直接冲突**。
- 连带：`ATTRIBUTION.md:33` 与 `:52` 的「十三型」表述都建立在错误计数上（README 的 B 类行本身没写数字，只列了 5 个类名）。

**修复建议**：三处统一改为「四族十五型 / Four families, fifteen shapes」；若原意是「两族」（只算复述+供给过量），则应把丙/丁族合并回去并真正删到 12/13 型——但不能标题与正文各说一套。

### I3 ｜ ATTRIBUTION 说中文固定句式「按功能重排为 10 类」，实际有 13 个编号节

**文件:行号**
- `ATTRIBUTION.md:34`（「按**功能**重排为 10 类，补保留条件与误报护栏」）
- `skills/humanize-zh/references/stock-phrases.md:21,34,47,60,75,91,105,121,135,145,155,161,167`（13 个编号节，最后一个为「## 13. 滥用排比与三项式」）
- 英文对应文件 `skills/humanize-en/references/stock-phrases.md:21…155` 为 14 个编号节

**证据**

```text
grep -n "^## " skills/humanize-zh/references/stock-phrases.md
7:## 使用说明
21:## 1. 开场垫话（强）
...
167:## 13. 滥用排比与三项式（弱）
175:## 检测输出格式（只诊断时）
# 编号节 = 13
```

**修复建议**：改为「重排为 13 类」（并顺带说明英文版为 14 类，差异来自新增 Sales language 一节）；或让 ATTRIBUTION 不写具体数字，改为「按功能重排」。

### I4 ｜ scan.py 同时维护两套规则源：内联表与 data JSON 严重漂移，且回退模式丢 keep 条件、产生重复命中

**文件:行号**
- `scripts/scan.py:47-105`（`ZH_RULES`，50 条）、`:107-142`（`EN_RULES`，31 条）
- `scripts/scan.py:146`（`DATA_DIR`）、`:150-181`（`load_corpus`，优先 data）、`:221-237`（`pick_rules`，data 缺失时回退内联表）
- 重复定义实例：`:122` 的 `in other words` 归入 `stock`，`:135` 又把同一短语归入 `explanatory`
- 数据对照：`data/ai-tells.zh.json` 192 条、`data/ai-tells.en.json` 134 条

**证据**

```text
scan.py INLINE TABLES vs DATA
  zh: inline rules=50 data entries=192 shared literal patterns=2
  en: inline rules=31 data entries=134 shared literal patterns=5
  inline rules with empty keep=50/50 (zh), 31/31 (en)

# 模拟 data/ 缺失（把 DATA_DIR 指向不存在的目录后）：
zh: rules=50 label='inline fallback (data/ not found)'
    strong=41 weak=9 | coined=5, defensive=8, explanatory=5, stock=32   ← 无 platform
en: rules=31 label='inline fallback (data/ not found)'
    strong=26 weak=5 | coined=3, defensive=4, explanatory=3, stock=21   ← 无 platform

# 同一句在回退模式下被两条规则重复报出（label 不同，去重键无法合并）：
en fallback scan hits=[('stock','strong','metadiscourse restatement','In other words'),
                       ('explanatory','strong','synonym restatement','In other words')]
```

- 漂移量：zh 48/50 的内联正则不在 data 中，en 26/31 不在 data 中；内联表与 data 是两套「平行规则集」，新增条目只进 data（见 M2），内联表永远落后。
- 回退模式违反 `README.md:91`「Every entry carries a keep-condition…the report prints it in a `keep if` column」——回退时 `keep if` 列全是 `—`，且 `--stats` 不显示 platform 族。
- ATTRIBUTION:41 说「规则表派生自本项目 `references/`」，但代码实际读 `data/`，references 只是散文；三处来源之间没有生成或校验关系。

**修复建议**：删除内联表，改为「data 缺失时明确报错并退出（exit 2）」；若必须保留单文件可移植能力，则由 `corpus_tool.py` 从 data 生成 `scan_rules.py`（构建产物），并加一致性测试：`set(data 正则) == set(内联正则)` 且两边 `keep` 非空率 100%。

### I5 ｜ keep 条件被占位化（zh 12 条 `"无"`、en 3 条 `"rarely"`），违反 data/README 的硬规则

**文件:行号**
- `data/README.md:41`（`keep` **必填**）、`:64`（「`keep` 必须写具体——写不出保留条件，说明这条规则还不成熟」）
- `skills/humanize-zh/SKILL.md:190`（「`--keep` 必填。写不出保留条件，说明这条还不成熟，先 `observe`」）
- `scripts/corpus_tool.py:61`（只检查 `keep` 非空，未拦截占位值）
- 占位条目：`data/ai-tells.zh.json` 中 `zh-st-006`、`zh-st-019`、`zh-st-025`、`zh-st-029`、`zh-st-040`、`zh-st-050`、`zh-st-051`、`zh-df-006`、`zh-df-007`、`zh-df-010`、`zh-ex-003`、`zh-df-020` 共 12 条 `"keep":"无"`；`data/ai-tells.en.json` 中 `en-st-008`、`en-st-062`、`en-pf-007` 共 3 条 `"keep":"rarely"`（如 `:144`）

**证据**

```text
zh: placeholder keeps: ('zh-st-006','无') ('zh-st-019','无') ('zh-st-025','无') ('zh-st-029','无')
    ('zh-st-040','无') ('zh-st-050','无') ('zh-st-051','无') ('zh-df-006','无') ('zh-df-007','无')
    ('zh-df-010','无') ('zh-ex-003','无') ('zh-df-020','无')
en: placeholder keeps: ('en-st-008','rarely') ('en-st-062','rarely') ('en-pf-007','rarely')
PS> python scripts/corpus_tool.py validate
zh: OK
en: OK          ← 占位值能通过校验
```

- 设计原则 #3（`README.md:99`）与 data/README 的入库纪律都指望 `keep` 防误删；占位值等于把「防误删」降级为无信息。
- `keep:"never"`（en 约 20 条）虽可解释为「任何情况下都不合法」，但它把这一列变成了常量，同样削弱了表格的信息量；与「逐条给保留条件」的叙事不符。

**修复建议**：(1) 把 12 条 `无` 改写为真实保留条件，或降级为 `observe` 暂不入库；(2) `validate_payload` 增加占位黑名单（`无/—/rarely/never/none`）与最小长度阈值，并让 `add` 拒绝；(3) 若 `never` 是有意设计，增加 `keep_type: "never"` 语义并在文档说明。

### I6 ｜ scan.py 在非 UTF-8 输入上直接 traceback 崩溃（中文 Windows 常见 GBK 文本）

**文件:行号**
- `scripts/scan.py:488`：`text = sys.stdin.read() if args.path == "-" else open(args.path, encoding="utf-8").read()`
- 只捕获了 `OSError`（`:489`），`UnicodeDecodeError` 是 `ValueError` 子类，不会被捕获

**证据**（临时副本中创建 GBK 文件后运行）

```text
PS> python scripts/scan.py gbk.txt
  File "...\scripts\scan.py", line 488, in main
    text = sys.stdin.read() if args.path == "-" else open(args.path, encoding="utf-8").read()
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xd5 in position 0: invalid continuation byte
[exit code: 1]
```

- 对照：文件不存在 → 优雅 `cannot read nope.md: [Errno 2]…` exit 1；目录 → 优雅 `Permission denied` exit 1；空文件/BOM 文件/stdin → 正常；fenced code 内的候选信号被正确跳过（实测含「值得注意的是」的代码块 hits=0）。只有编码这一条路径崩溃。
- 影响：中文场景下用户把 Word/记事本导出的 GBK `.txt` 直接喂给扫描器是高频路径。
- 同类（未单列）：`scripts/corpus_tool.py:37` 的 `json.loads` 与 `:138` 的 `read_text` 均无异常处理。临时副本实测：

```text
PS> python scripts/corpus_tool.py validate    # 把 data/ai-tells.zh.json 改成 "{not json"
json.decoder.JSONDecodeError: Expecting property name enclosed in double quotes: line 1 column 2 (char 1)
PS> python scripts/corpus_tool.py stats       # 删掉 data/ 目录
FileNotFoundError: [Errno 2] No such file or directory: ...\data\ai-tells.zh.json
```

- 对照：`scan.py` 对损坏 corpus 能降级（P8），`corpus_tool.py` 则直接 traceback；维护工具比扫描器更脆弱。

**修复建议**：读取时用 `encoding="utf-8-sig", errors="replace"`（或先按 UTF-8 尝试、失败后按 `locale.getpreferredencoding()` 回退），并捕获 `UnicodeDecodeError` 输出友好提示；stdin 同理。

### I7 ｜ `platform` 家族中英严重不对齐（63 vs 10），且两边语义集不同，README 的「同一家族表」不成立

**文件:行号**
- `data/ai-tells.zh.json:89-158, 213`（63 条：公文/营销/教学/新闻/邮件/互联网黑话/收益承诺）
- `data/ai-tells.en.json:138-147`（10 条：LinkedIn 开场、email 模板、学术自指、科技营销、增长营销）
- `README.md:26-34` / `README.zh-CN.md:22-32`（两版都声明中英覆盖同一 A–G 家族表）

**证据（家族条数表）**

| family | zh | en | delta(zh−en) | 备注 |
|---|---:|---:|---:|---|
| stock | 75 | 80 | −5 | 基本对齐 |
| defensive | 21 | 18 | +3 | 基本对齐 |
| explanatory | 12 | 14 | −2 | 基本对齐 |
| coined | 21 | 12 | +9 | en 偏少 |
| **platform** | **63** | **10** | **+53** | **严重不对齐** |
| **合计** | **192** | **134** | **+58** | zh 比 en 多 43% |

- 语义集也不同：zh 的 platform 大量是**公文套话**（`:92`「进一步推进」、`:93`「多措并举」）与**教育培训**（`:146`「本节课我们将学习」、`:148`「激发兴趣」），en 的 platform 则全是 LinkedIn/email/academic（`:138-147`）。同一 `fam` 代码在两种语言里指的不是同一类现象。
- 另外 `strong` 占比 zh 76/192=39.6% vs en 81/134=60.4%，缺少校准依据；在「单条不构成判断」的设计原则下，en 侧强信号过多会推高误报。
- 可佐证跨族重复：`show` 字符串被**其他规则**命中的情况 zh 27 处、en 11 处（含同族与跨族），例如 `zh-st-030`（stock，`:35`「有研究表明」）被 `zh-pf-016`（platform，`:106`「研究表明」）命中；`en-st-007`（stock，`:12`「worth noting」）与 `en-pf-007`（platform，`:144`「worth mentioning / it should be noted」）是同一现象的拆分。

**修复建议**：给 platform 一个明确的语义边界并写进文档；en 侧要么补齐对应规则（至少覆盖 email/公文/营销/教学四类），要么在 README 明确「platform 仅中文版有效」；同时统一 `strong` 的判定标准并在 data/README 写出校准方法。

### I8 ｜ data 与 references 是两套独立清单，无同步/无校验；已验证至少 1 条 data 规则在 references 中无对应行

**文件:行号**
- `data/ai-tells.zh.json:39`（`zh-st-034`，`"show":"据悉"`）
- `skills/humanize-zh/references/stock-phrases.md:95-103`（§6 模糊归因只有「相关人士透露／知情人士称」，无「据悉」）
- 同类：`data/ai-tells.en.json:64-65`（`en-ex-001`「This shows that」、`en-ex-002`「The key point is」）在 `references/explanatory-forms.md` 中找不到逐条对应（后者是 4 族 15 型的形态清单，不是句子级清单）

**证据**

```text
PS> python -c "import pathlib,re; t=''.join(p.read_text(encoding='utf-8') for p in pathlib.Path('skills').rglob('*.md')); print('据悉' in t)"
False          # data 有 zh-st-034「据悉」，全部 skills/*.md 中都没有
```

- 结果结构：references 是「按功能分组的长清单」，data 是「逐条正则库」，两者理论上可互补，但仓库没有任何命令/测试把二者对齐（`corpus_tool.py` 只管 data）。data 新增条目不会出现在 references，references 改动也不会回写 data。
- 佐证：`data/ai-tells.zh.json` 的 `stock` 75 条 vs references/stock-phrases.md 的 78 个表格行（粗略统计，含表头/说明行）；`en` 80 vs 76；`platform` 73 条无任何 references（B1）。数量既不是 1:1 也没有映射说明。
- 影响：维护者无法回答「某条规则到底以哪份清单为准」；SKILL.md 又反复用「完整清单见 references/…」（如 `zh SKILL.md:139`），加剧歧义。

**修复建议**：确定唯一主数据源（建议 data JSON），references 由脚本生成或至少在每条旁标 `id`；增加 `corpus_tool.py check-refs`：双向校验 data 每条 rule 能在 references 找到对应行、references 每个条目有 data id，CI 失败即拒绝合并。

### I9 ｜「两个独立技能，不是互译版本」与 ATTRIBUTION 自述的「转写自中文版 / 同中文版」冲突

**文件:行号**
- `README.md:5`（「Two independent skills, **not a translation pair**」）、`README.md:10`（「English: **same families** + sentence bloat」）
- `README.zh-CN.md:3`（「两个独立的 agent skill，**不是互译版本**」）
- `ATTRIBUTION.md:37`（en defensive：「六道判别与对称防线**转写自中文版**」）
- `ATTRIBUTION.md:38`（en explanatory：「**同中文版**，英文例句原创」）
- `ATTRIBUTION.md:40`（en coined：「**同中文版**，英文例句原创」）
- `skills/humanize-en/references/defensive-forms.md:3`（「with the six tests **rewritten from the Chinese edition**」）

**证据**

```text
ATTRIBUTION.md:37  .../humanize-en/references/defensive-forms.md | 改编 | ... | 六道判别与对称防线转写自中文版；英文例句为原创 |
ATTRIBUTION.md:38  .../humanize-en/references/explanatory-forms.md | **原创** | 同上，概念启发 | 同中文版，英文例句原创 |
ATTRIBUTION.md:40  .../humanize-en/references/coined-terms.md | **原创框架** | 同中文版 | 同中文版，英文例句原创 |
```

- 实际结构也印证「同源」：两份 explanatory 是同一 4 族 15 型骨架（I2），两份 coined 是同一 7 形态 + 5 问，workflow 7 步一一对应，references 四个文件同名同序。
- 「不是互译版本」可以作为**定位宣示**（语言病不同、G 类仅英文），但 ATTRIBUTION 的措辞是「转写自中文版」，README 的措辞又否认互译，读者/评审无法判断哪句为准。这属于**声明层内部矛盾**，不是内容错误。

**修复建议**：把 README 的说法收敛为「共享方法骨架、按语言分治的两套技能（相同分类 + 语言特有规则）」，并在 ATTRIBUTION 中明确「骨架转写自中文版，例句与语言规则独立」；或反过来，如果坚持「独立」，则 en references 需给出独立来源而非「同中文版」。

---

## 四、次要问题（11）

### M1 ｜ 版本号三处不一致，且 `add` 只更新单语种 → 两库版本必然分叉
- `skills/humanize-zh/SKILL.md:6`、`skills/humanize-en/SKILL.md:6`：`metadata.version: "1.0.0"`（两份相同）
- `data/ai-tells.zh.json:2`：`"version": "1.1.0"`；`data/ai-tells.en.json:2`：`"version": "1.0.0"`
- `scripts/corpus_tool.py:73-78`（`bump_version` 只 bump 当前写入文件）
- 证据：`python scripts/corpus_tool.py stats` 输出 `zh: v1.1.0 … en: v1.0.0`；在临时副本里执行一次 `add --lang en` 后 en 变为 `1.1.0`，zh 不变。
- **建议**：单一 `VERSION` 文件或在两文件顶部写「语料库版本 = SKILL metadata.version」并由 `add` 同步两边；`--stats` 打印前端版本。

### M2 ｜ `add` 追加到数组末尾会破坏家族分组
- `scripts/corpus_tool.py:81-91`（`insert_entry` 在 `\n  ]` 前追加）；`data/README.md:57` 只写「只插入一行」，未说明顺序副作用
- 证据：`data/ai-tells.zh.json` 的 platform 块在 `:89-158`，而新增的 `zh-pf-063` 落在 `:213`（coined 块之后）；临时副本执行 `add --lang en` 后 `en-st-081` 落在 platform 块之后（`last 4 fams=['platform','platform','platform','stock']`）。
- **建议**：按 `fam` 插入到该族末尾，或在 data/README 明说「条目按追加顺序、不保证分组」，并让 `--stats`/查看器不依赖顺序。

### M3 ｜ data/README 的 schema 与实现不一致：`note` 未文档化、示例格式与实际不符、`validate` 不校验必填字段
- `data/README.md:14-31`（schema 只列 `version/lang/entries`；示例为多行 pretty-print）
- `data/ai-tells.zh.json:4` / `data/ai-tells.en.json:4`（实际有未文档化的顶层 `note`）；实际每条为**单行 JSON**（`:6`）
- `scripts/corpus_tool.py:50-70`（`validate` 只查 id 重复 / fam / sev / keep / re，不查 `label`、`fix`、`show`、id 格式、id↔fam 一致性、`lang` 字段）
- 证据：`python scripts/corpus_tool.py validate` → `zh: OK / en: OK`，即使 `label` 为空也会通过（当前数据恰好齐全，属潜在漏洞）。
- **建议**：补 `note` 字段说明；示例改为单行条目；`validate` 增加 `label/fix` 非空、id 正则 `^(zh|en)-(st|df|ex|ct|pf)-\d{3}$`、id 前缀与 `fam` 一致、`lang` 与文件名一致的校验。

### M4 ｜ 中文 SKILL 列了 5 项判别，references 有 6 道，ATTRIBUTION 也说「六道」
- `skills/humanize-zh/SKILL.md:67`：「（删除检验／功能检验／五判据／来源检验／位置检验）」= 5 项
- `skills/humanize-zh/references/defensive-forms.md:22`「## 一、六道判别」，`:26/:31/:36/:46/:50/:53` 共 6 项，第 6 项为「信息强度分层」
- `ATTRIBUTION.md:32`（「六道判别…改编自该文件」）
- **建议**：SKILL 第 67 行补「信息强度分层」，或把「六道」改为「五道」并说明第 6 项为前提假设。

### M5 ｜ 英文技能是 English-only，却在 F 类写了中文专属的「CJK 半角标点」
- `skills/humanize-en/SKILL.md:3`（「English only」）、`:100`（「**F Residue**: … half-width punctuation in **CJK text**, emoji templates…」）
- `README.md:33` 的英文 F 行没有这一项；中文 `skills/humanize-zh/SKILL.md:154` 才有半角标点。
- **建议**：删除 en 的 CJK 项，或移到 §6.5「Chinese side differs」作为对照说明。

### M6 ｜ 两版章节编号都从「三 / 3」开始，缺「一 / 二」；交叉引用依赖未编号章节
- `skills/humanize-zh/SKILL.md:42`（`## 三、工作流`，但前面 `:18`「四条红线」、`:27`「六类 AI 痕迹」均未编号）
- `skills/humanize-en/SKILL.md:43`（`## 3. Workflow`，`:18`「Four hard limits」、`:27`「Seven families」未编号）
- 表内又用「本文件 §五 / §6」等引用（zh `:35-36`、en `:35-37`），读者需自行推断 §一/§二。
- **建议**：补编号（1/2 或 一/二），或去掉全部编号改用锚点链接。

### M7 ｜ 加载体积：两份 SKILL.md 均已到 5k tokens 量级；§4 与 references 内容重复
- 实测：`skills/humanize-en/SKILL.md` 283 行 / 20,463 字符 / 20,650 UTF-8 bytes（估算 ≈5.3k tokens）；`skills/humanize-zh/SKILL.md` 247 行 / 8,233 字符 / 18,526 bytes（≈5.0k tokens）；两份常驻合计 **39,176 bytes**。
- references 合计 **73,198 bytes**（en 35,830 / zh 37,368，按需加载）；单文件最大 `skills/humanize-zh/references/stock-phrases.md` 12,152 bytes、`skills/humanize-en/references/stock-phrases.md` 10,915 bytes。
- 重复：zh `SKILL.md:105-139`（五问/七形态/阶梯）与 `references/coined-terms.md:33-96` 基本同文；en `SKILL.md:108-144` 与 `references/coined-terms.md:33-96` 同样重复。
- **建议阈值**：`SKILL.md` 正文 ≤ 500 行 **且** ≤ 5,000 tokens（≈20KB 英文 / ≈8k CJK 字符）；单 references ≤ 15KB。当前两版 SKILL 贴上限，建议把 §4 的四张表外移到 references，预计可降到 ≈3.5–4k tokens；并把 `stock-phrases` 的 12–13 类拆成两个文件（开场/壳类 vs 收束/词类）以控制单文件体积。

### M8 ｜ 英文 description 927 字符，距 1024 上限仅 97 字符
- `skills/humanize-en/SKILL.md:3`：927 字符（Python `len(description)`；UTF-8 927 bytes）
- 触发词已很长（de-AI this / sounds like ChatGPT / cut the slop…）。再加一个触发词就可能超限，而多数 skill loader 对超长 description 会截断。
- **建议**：压缩到 ≤ 800 或把长列举改为「+ 常见同义说法」一行；加 CI 断言 `len(description) < 1024`。

### M9 ｜ `.gitattributes` 带 UTF-8 BOM；工作树里躺着 `scripts/__pycache__/*.pyc`
- `.gitattributes:1`：内容 repr 为 `'\ufeff* text=auto eol=lf\n*.py text eol=lf\n*.md text eol=lf'`，首行 `* text=auto eol=lf` 前有 BOM，部分 git/编辑器会把它当成 pattern 的一部分。
- `scripts/__pycache__/corpus_tool.cpython-313.pyc`、`scripts/__pycache__/scan.cpython-313.pyc` 存在于交付目录（`.gitignore` 已含 `__pycache__/`；因约束未运行 git，无法判定是否被跟踪）。
- **建议**：去掉 BOM 并补末尾换行；删除 pyc 并在 CI 里加「工作树不得含 __pycache__」。

### M10 ｜ 阈值文档与实现口径不一致（中文「的」层数 vs 字符计数；80/120 字未文档化；exit code 说法）
- `skills/humanize-zh/SKILL.md:172`：「一句里『的』**超过三层**…就该拆」
- `scripts/scan.py:267`：`if sent.count("的") >= 4:`（统计**字符个数**，不是层级；且以整行为单位切句，非整段）
- `scripts/scan.py:260-266`：中文 ≥80 字记 weak、≥120 字记 strong——这两个阈值在任何文档中都没有出现
- `scripts/scan.py:15` docstring：「Exit code is always 0 unless the file cannot be read」——实际无路径时 exit 2（`--stats`/无参数），argparse 错误也是 2
- 英文侧 `skills/humanize-en/SKILL.md:171-176` 的 6 项 Hard limits 中，scan.py 只自动检查句长、从句、of 链（`structure_hits`），`-ing` 链、前置修饰堆、括号嵌套不检测（文档未声称自动检测，但易被误读为「扫描器全查」）
- **建议**：统一为「的 ≥4 个」并写进 SKILL 与 README；把 80/120 写入 `data/README` 或 SKILL；修正 docstring；在 SKILL §6.5 标注「自动检查 / 人工检查」两栏。

### M11 ｜ 计数声明无单一来源：仓库中找不到「325」，实测 326；zh/en 版本与条数分叉
- `grep -R "325\|326" .` → **0 命中**（仓库任何文件都没有这两个数）
- 唯一数量表述：`skills/humanize-zh/SKILL.md:196`「中文约 190 条、英文约 130 条」、`skills/humanize-en/SKILL.md:232`「about 190 Chinese and 130 English」——与实测 192/134 在「约」的范围内可接受。
- `python scripts/corpus_tool.py stats` → `total: 326`；zh v1.1.0 比 en v1.0.0 多一条 `zh-pf-063`（`data/ai-tells.zh.json:213`，位于数组末尾，见 M2）。
- 若任务书/对外材料声称「325 entries」，则与实际差 1，**很可能是 `zh-pf-063` 追加后未同步对外数字**（325 + 1 = 326，且 zh 版本恰为 1.1.0）。
- **建议**：README 中固定「326 = zh 192 + en 134」并说明口径（是否含 platform）；加一条 CI 断言 README 数字 == `stats` 输出；对外宣传以 326 为准。

---

## 五、已验证通过项（不计入问题，供作者放心）

| # | 项目 | 证据 |
|---|---|---|
| P1 | 两个 SKILL.md frontmatter 均可被 YAML 解析，`name`/`description` 齐备，无非法键 | PyYAML 输出：`keys=['name','description','license','metadata']`，`name='humanize-zh'/'humanize-en'` |
| P2 | description 长度合规（<1024 字符） | en 927 字符 / zh 310 字符（zh UTF-8 834 bytes） |
| P3 | 仓库内 32 条相对链接全部可达 | 脚本遍历 `**/*.md`：`relative links checked: 32`，无 `BROKEN` 行 |
| P4 | 8/8 references 首部有 `> **Source** / > **出处**` 出处行 | 逐文件检查 `provenance=True`（均在第 3 行） |
| P5 | data 数据完整性：无重复 ID、无重复正则、8 个字段 100% 存在、ID 序号连续 | zh 192 条 / en 134 条，`duplicate ids=[]`、`duplicate regexes=0`、`field problems (0)`；各 fam 的 ID 区间 001..N 无空洞 |
| P6 | `corpus_tool.py` 正常路径可用：validate/stats/add/observe；`add` 会拒绝空 keep 与重复正则 | `validate` → `zh: OK / en: OK`；重复正则 → `refusing to write; validation failed` exit 1；空 keep → exit 2 |
| P7 | `scan.py` CLI 边界行为可接受：文件不存在/目录 → exit 1 且有提示；无参数 → exit 2；空文件/BOM/stdin/`--json` 正常；跳过 fenced code | 逐项实测（见 §六） |
| P8 | 损坏的 corpus 能让 scan.py 降级而非崩溃 | 临时副本写入非法正则：`--stats` 输出 `invalid entries: 1`；扫描时输出 `corpus warnings: 1`，exit 0 |
| P9 | 无写死绝对路径（换机器可用） | 脚本中仅 `pathlib.Path(__file__).resolve().parent.parent`（`corpus_tool.py:27`、`scan.py:146`），无 `C:\`/`/Users/` |
| P10 | 性能与安全：无 ReDoS 迹象 | 200,000 字符中文/英文输入分别 0.20s / 0.51s（对应语言全部规则：zh 192 / en 134） |
| P11 | LICENSE 为 MIT，并列出 4 个上游项目；README 与 ATTRIBUTION 均标注 MIT | `LICENSE:1-3,25-31`；`ATTRIBUTION.md:74-84` |
| P12 | `corpus_tool.py validate` 对当前 data 无告警；data 的 `lang` 字段与文件名一致 | `zh`/`en` 均 OK；`lang_field='zh'/'en'` |

---

## 六、复现命令（审查中实际执行）

```powershell
cd <repo-root>

# 1) 计数与家族分布（B1/I7/M1/M11）
python scripts/corpus_tool.py stats
python scripts/scan.py --stats

# 2) 当前数据校验（P5/P6）
python scripts/corpus_tool.py validate

# 3) frontmatter 合法性 + description 长度（P1/P2/M8）
python -c "import re,yaml,io; [print(p, len((d:=yaml.safe_load(re.match(r'---\n(.*?)\n---', open(p,encoding='utf-8').read(), re.S).group(1)))['description'])) for p in ('skills/humanize-zh/SKILL.md','skills/humanize-en/SKILL.md')]"

# 4) 仓库内相对链接（P3）
python -c "import pathlib,re; R=pathlib.Path('.'); bad=[(f,i,t) for f in R.rglob('*.md') for i,l in enumerate(f.read_text(encoding='utf-8').splitlines(),1) for t in re.findall(r'\]\(([^)]+)\)',l) if not re.match(r'https?:|mailto:|#',t) and not (f.parent/t.split('#')[0]).exists()]; print('broken:',bad)"

# 5) data 与 scan.py 内联表漂移（I4）；先在临时副本中把 DATA_DIR 置空再运行
python -c "import importlib.util,sys,pathlib; s=importlib.util.spec_from_file_location('s','scripts/scan.py'); m=importlib.util.module_from_spec(s); sys.modules['s']=m; s.loader.exec_module(m); m.DATA_DIR=pathlib.Path('__missing__'); print([(l, m.pick_rules(l)[1], len(m.pick_rules(l)[0])) for l in ('zh','en')])"

# 6) 非 UTF-8 输入（I6）：在临时副本中
#    [System.IO.File]::WriteAllText('gbk.txt','中文',[Text.Encoding]::GetEncoding(936))
python scripts/scan.py gbk.txt

# 7) 安装模拟（B3）：把 skills/humanize-{zh,en} 复制到临时 ~/.claude/skills/ 后重跑上面第 4 步
```

---

## 七、建议修复顺序（按投入产出）

1. **B1 + I7**：先决定 platform 是「正式家族」还是「并入其余四族」——这一项决定文件结构、ATTRIBUTION、README、data 的全部后续改动。
2. **B2 + I2 + I3 + I9**：集中修 ATTRIBUTION/README 的数字与出处（一次改完，避免二次漂移）；给「每个文件」补 data/corpus_tool/README 行。
3. **B3**：把 ATTRIBUTION 随技能打包，安装后链接自检进 CI。
4. **I1 + I5 + I4**：补第四模式 / 清理 keep 占位 / 删除或生成内联规则表；同时加 CI：`validate` + inline==data + description<1024 + 计数断言 + 安装后链接检查。
5. **I6、M1–M11**：按条目清单逐项收尾。

**门禁建议（CI 最小集）**：`corpus_tool.py validate` 通过；`scan.py --stats` 退出 0；内联表与 data 正则集合一致；README 中的条数 == `stats`；`ATTRIBUTION` 覆盖 `skills/**`、`scripts/**`、`data/*.json`；模拟安装后 0 断链；`SKILL.md` ≤ 500 行且 description < 1024。
