# 编辑视角盲审：humanize-writing-skill

- 评审类型：写作有效性（编辑视角），只判断"这套规则拿来改稿能不能用、会不会改坏"，不做代码审查。
- 读过的材料：`README.md`、`README.zh-CN.md`、`skills/humanize-zh/SKILL.md`、`skills/humanize-en/SKILL.md`、两个 `references/` 下的 8 个 `.md`、`data/README.md`；另读了 `scripts/scan.py` 的句长段（见第 10 条），并运行仓库自带扫描器做**候选定位**（不作为判断依据）。
- 方法：自造 3 篇刻意"像 AI"的样例（中文学术摘要 242 字、中文公文通知 250 字、英文 LinkedIn 帖 164 词，全文见附录 A）→ 按 `skills/humanize-zh/SKILL.md:42-99` 的七步管线人工执行 → 记录删改点、误删点、漏检点、无法判定的保留条件 → 再回去核对 SKILL.md 与 references 是否互相打架。
- 边界：未运行 git；仓库内除本文件外未创建或修改任何文件（样例与扫描输出都在系统临时目录）。
- 结论先行：**方向对，管线可用，但不能照字面执行**。规则文本自身有 3 处会直接造成过度删改（第 1、2、10 条），中英两份在"实现强度"上明显不对称（第 10 条），入库纪律与语料库现状硬矛盾（第 3 条），另有 4 类最典型的 AI 痕迹没有归属（第 4、5、6 条与第 3 条的"三无措施句"）。以下按严重度排序。

---

## 问题清单（严重度从高到低）

### 1｜【高】"Y 若仍是抽象判断，整句删"会把结果句、局限句、承诺句一起删掉

- 位置：`skills/humanize-zh/SKILL.md:86`（对应 `skills/humanize-en/SKILL.md:89`）
- 问题：C 类处理原则把"抽象"直接当成"无信息"，但学术摘要的结果句、论文的 limitations、公文里的承诺句本身就是由抽象判断写成的，字面执行会删掉全文唯一的信息句，和红线 2「不丢信息」（`skills/humanize-zh/SKILL.md:21`）冲突。
- 证据（样例 A、B，见附录 A）：
  - A 的唯一结果句：「研究发现，安静程度、座位类型与采光条件对使用体验具有显著的正向影响，且三者之间存在协同效应。」按本规则，Y＝"显著正向影响／协同效应"属抽象判断 → 整句删 → 摘要没有结果了。
  - A 的末句：「当然，本文仍存在一定局限，样本量相对有限，未来有待进一步研究。」扫描器把"有待进一步研究"判为 strong（`zh-st-041`，`data/ai-tells.zh.json:46`），"样本量相对有限"另命中 weak 的"学术免责套话"（`zh-pf-018`，`data/ai-tells.zh.json:108`）；而 `skills/humanize-zh/references/defensive-forms.md:97` 明确"论文 limitations"是要保留的文种要求，`skills/humanize-zh/SKILL.md:205` 也要求论文保留限定 → 删掉就丢了唯一的样本局限说明。
  - B 的承诺句：「学校将以此次专项检查为契机，进一步健全长效机制。」删掉后读者少知道"学校还要改制度"，而这正是 `skills/humanize-zh/SKILL.md:25` 优先级里排在第二位的"承诺"。
- 改法：把 `skills/humanize-zh/SKILL.md:86` 整句替换为：

  > 删掉虚设的 X，直接写 Y。Y 若是评价性拔高（重要、有价值、意义重大、再上新台阶、提供有力支撑）或空壳名词，整句删；Y 若含结果、条件、范围、因果、承诺，保留，并把抽象词落到证据、对象、时间或责任人上（受红线 1、2 约束）。

  `skills/humanize-en/SKILL.md:89` 同步改为："Delete the invented X, state Y. If Y is evaluative inflation or an empty abstraction, delete the sentence. If Y carries a result, condition, scope, causal claim, or promise, keep it and attach it to evidence."

### 2｜【高】一句公文开头被三条规则判成三种结果：删 / 留 / 留

- 位置：`skills/humanize-zh/SKILL.md:83`（目的链长句＝强信号，见一处就处理）× `skills/humanize-zh/references/defensive-forms.md:47`（来源标记型限定→保留）× `data/ai-tells.zh.json:103`（`zh-pf-014`"按照……要求"，weak，keep＝公文、政策文件）
- 问题：同一条"为贯彻落实…，决定开展…"的公文依据句，在换句式一步里按强信号要删 X，在防御判别里属"来源标记"要留，在语料库里又被降级为弱信号并注明公文保留；执行者无法判断该服从哪条，实际结果取决于先读到哪个文件。
- 证据：样例 B 首段「为深入贯彻落实上级消防安全工作部署，进一步压实安全责任，切实防范各类事故发生，决定开展消防安全专项检查。」按 `SKILL.md:83` 删掉虚设 X 后只剩「决定开展消防安全专项检查」，读者失去"依据哪一级部署、为什么现在做"这一来源事实；而 `defensive-forms.md:47` 第一行就是"来源标记型限定（'据教务处通知'…）→ 保留"。
- 改法：在 `skills/humanize-zh/SKILL.md:83` 的"目的链长句"后加一句例外：

  > 若链首是公文依据或来源标记（"为贯彻落实…""根据…部署"），按 `references/defensive-forms.md:47` 保留依据，只删重复的目的套话和"切实/进一步"的堆叠。

  并在 `skills/humanize-zh/references/stock-phrases.md:14`（误报护栏第 3 条）后补一句："公文、讲话稿的目的链按 SKILL.md §七 处理，不按本节强信号删。"

### 3｜【高】语料库把公文规范语收了进来，公文样例因此被判"0 强信号、不要改"，而它真正的病没有规则

- 位置：`skills/humanize-zh/SKILL.md:192`（入库纪律 3：文体规范不入库）× `data/ai-tells.zh.json:92-104`（`zh-pf-004/005/007/008/009/011/012/014`，keep 全是"公文、政策原文、讲话稿"）× `skills/humanize-zh/SKILL.md:63-64`
- 问题：入库纪律明说"文体规范不入库——它们不是 AI 痕迹"，语料库里却有 8 条公文规范语；扫描时它们全部 weak 且 keep＝公文，于是我的公文样例得到"0 强信号、不要单独改"的结论，而它真正的问题（措施无对象、无时限、无责任人、无验收标准）没有任何规则覆盖。
- 证据：样例 B 跑仓库自带扫描器，结果是 `strong hits: 0` / `weak hits: 8` / `verdict: no strong hits; weak signals only - do not edit on these alone`；8 条命中里 5 条 keep＝公文。原句「各单位要聚焦重点部位和关键环节，建立问题台账，实行闭环管理，确保隐患整改到位、销号清零」——"重点部位"是哪些、台账几个字段、销号谁签，全篇没有，但 `data/ai-tells.zh.json:99`（`zh-pf-010`）的 keep 是"确有台账与销号机制"，这句话字面就把 keep 条件满足了。
- 改法：① 二选一：把 `skills/humanize-zh/SKILL.md:192` 第 3 条改成"文体规范可以入库，但 sev 一律 weak，keep 必须写明文体与例外条件"（与现状一致），或把这 8 条从语料库删掉；② 在 `skills/humanize-zh/SKILL.md:150`（§五 表末）后加一条可判定规则：

  > **措施句四问**：谁做、在什么对象/范围上做、什么时限前完成、以什么可核结果验收。四问缺三 → 视为填充，改成能验收的句子或删。写成"四问"而不是"是否具体"，因为后者无法判定。

### 4｜【高】无源数字/涨幅没有归口：既不在七形态里，也不在守内容清单里

- 位置：`skills/humanize-zh/SKILL.md:120`（七形态只到"伪机构／伪报告／伪标准"）× `skills/humanize-zh/references/coined-terms.md:24` 与 `:89`（处理阶梯里突然出现"伪数据"）× `skills/humanize-zh/SKILL.md:54`（第 2 步只核对改写时新增的数字）
- 问题：原稿里 AI 编的数字在"不增事实/不丢信息"两条红线保护下被原样保留，而 D 类七形态没有"无源数据"，第 2 步也只管改写时新增的数字；这是 LinkedIn 类文本最典型的 AI 迹，却成了全套规则里唯一没有归属的一类。
- 证据：样例 C「Engagement grew by 47%」「40+ engineers」；扫描器对这两处 0 命中。`coined-terms.md:89` 的处理阶梯写着"伪机构／伪报告／伪数据"，但 `:24` 的形态表里没有"伪数据"这一行——说明是漏写，不是有意排除。en 侧 `skills/humanize-en/references/coined-terms.md:24`、`:89` 同样缺。
- 改法：七形态各加第 8 条（`skills/humanize-zh/SKILL.md:123` 之后、`skills/humanize-zh/references/coined-terms.md:27` 之后）：

  > 8. **无源数据**："增长 47%""40+ 工程师""提升三倍"这类数字，原文没给出样本、时间窗、出处或计算方式。（不改数、不删数：标 `〔须补来源〕`，并在说明里列出）

  同时在 `skills/humanize-zh/SKILL.md:56` 后补："原稿数字无出处且非用户提供 → 只标注，不删不改；数字来源不明不等于数字是假的。"

### 5｜【中高】英文 platform 层过薄，LinkedIn 三类最显眼的形态没有规则；中文有对应条目，形成中英不对称

- 位置：`data/ai-tells.en.json:138-147`（en platform 共 10 条）× `data/ai-tells.zh.json:130`（`zh-pf-038` 互动引导，中文有、英文无对应）× `skills/humanize-en/SKILL.md:159`（F 类只列 emoji 模板，没有 hashtag 堆和"每句一行"断行）
- 问题：样例 C 里三处最显眼的 LinkedIn 痕迹——「What's your take? 👇」「#async #leadership #futureofwork」「每句单独成行」——扫描器 0 命中；而中文侧有"点赞收藏/关注我不迷路"的互动引导条目，10 条 vs 63 条的差距不是语言差异，是覆盖差异。
- 证据：样例 C 结尾三行（附录 A）；扫描报告 strong 5 / weak 6，无一条命中上述三形态。
- 改法：① 在 `data/ai-tells.en.json:147` 后插入两条：

  ```json
  {"id":"en-pf-011","re":"\\b(what'?s your (take|thoughts)|thoughts\\?|agree\\?|curious to hear|drop a comment)\\b","show":"What's your take?","fam":"platform","sev":"weak","label":"engagement-bait closer","keep":"a real question that changes the reply","fix":"ask a specific question, or delete"},
  {"id":"en-pf-012","re":"(#[A-Za-z0-9_]+\\s*){3,}","show":"#tag #tag #tag","fam":"platform","sev":"weak","label":"hashtag block","keep":"the platform requires it","fix":"keep at most three, or delete"}
  ```

  ② `skills/humanize-en/SKILL.md:159` 的 F 类清单末尾加 "hashtag blocks (3+), one-sentence-per-line lineation (LinkedIn)"。

### 6｜【中高】正则只覆盖单词/单数形态，两条最标准的英文翻案句实测漏检

- 位置：`data/ai-tells.en.json:20`（`en-st-015` `not X, it's Y` 只允许 X 是一个词）× `data/ai-tells.en.json:46`（`en-st-041` 只收 `the result?` 单数）× 规则原文 `skills/humanize-en/references/stock-phrases.md:58`、`:118`
- 问题：参考表把这两条列为 strong（见一处就处理），但套装里的正则遇到常见变体就不匹配，照扫描结果执行会把最标准的 AI 腔留在稿子里。
- 证据：样例 C 第 2 段「it's not about killing meetings, it's about being intentional with async communication.」——X 是"killing meetings"两个词，`en-st-015` 的 `(about\s+)?\w+[,;:]?\s*(it'?s|but)` 匹配不到（`\w+` 后紧跟的是 " meetings"）；第 4 段「The results?」是复数，`the result\?` 也不匹配。扫描器对这两段只报了 "Here's the thing" 和 "In today's fast-paced"，两条翻案句都漏了。
- 改法：`data/ai-tells.en.json:20` 的 `re` 改为：

  ```json
  "re":"\\b(isn'?t|is not|not)\\s+(just\\s+)?(about\\s+)?[^.?!,;]{1,40}?[,;:]?\\s*(it'?s|but)\\b"
  ```

  `data/ai-tells.en.json:46` 的 `the result\\?` 改为 `the results?\\?|the answer?\\?`。中文侧同样检查：`data/ai-tells.zh.json:20` 的"不是…而是"只收"而是"变体，应加"不是…，是…"（`不是[^。！？]{1,20}[，,]\s*是`）。

### 7｜【中高】D 类"一票否决"与 C 类"两级阈值"打架，最该抓的伪框架反而只算弱信号

- 位置：`skills/humanize-zh/SKILL.md:81-84`（弱信号成片出现才处理）× `skills/humanize-zh/references/coined-terms.md:35`（"任一不过就要处理"）× `data/ai-tells.zh.json:110`（`zh-pf-020`"分析框架" = weak）× `skills/humanize-zh/SKILL.md:119-120`
- 问题：同一句"基于'空间—行为—体验'三维分析框架"同时受 D 类五问和 C 类阈值管辖：五问过不了定义/溯源/边界三关就该处理，但语料库把它归到 weak platform"框架先行"，按 `SKILL.md:84` 单条不动；执行者只会走弱信号判定，于是 D 模块这个"重点模块"在真实的伪框架上失效。
- 证据：样例 A 该句在扫描结果里只出现 weak「分析框架」一条，`terms` 里只有"评价指标体系"，没有"三维分析框架"。`coined-terms.md:23` 的伪学术命名例子只写"XX 三层模型／XX 效应／XX 定律"，"N 维／X—Y—Z 框架"不在其中。
- 改法：① 在 `skills/humanize-zh/SKILL.md:84` 后加一句优先级：

  > D 类不受本节两级阈值约束：五问任一不过即处理；语料库里的 D 类候选一律标 weak，只用于提示，不构成"成片才动"的限制。

  ② 在 `skills/humanize-zh/SKILL.md:119-120` 与 `skills/humanize-zh/references/coined-terms.md:23` 的例子列各加"N 维／三层／双元／'X—Y—Z'框架（如'空间—行为—体验三维分析框架'）"。

### 8｜【中】三条 keep-condition 实际无法执行（"可能有用""确实是反直觉""确有台账"）

- 位置：`skills/humanize-zh/references/coined-terms.md:88` × `skills/humanize-zh/references/stock-phrases.md:40` × `data/ai-tells.zh.json:99`
- 问题：保留条件不可判定就等于没有保留条件；最坏的情况是保留条件被被检查的那句话本身字面满足（自证），规则在纸上存在、在实操里必然放行。
- 证据：① `coined-terms.md:88`「疑似自造、无法溯源，但可能有用 → 保留原句」——"可能有用"是万能豁免，样例 A 的"三维分析框架"被它直接放过；② `stock-phrases.md:40` 的 keep"后接的**确实是**反直觉发现"——谁判断反直觉、跟谁的直觉比，没有标准；③ `data/ai-tells.zh.json:99` 的 keep"确有台账与销号机制"，样例 B「建立问题台账，实行闭环管理…销号清零」字面含"台账"和"销号"，即便没有字段定义和签批人也算"确有"。
- 改法：三处替换为可判定条件：
  - `coined-terms.md:88` → "作者能在 30 字内给出定义，并举出一个**不属于**它的例子，且文中至少一条推论依赖它；否则按空壳处理。"
  - `stock-phrases.md:40` → "后句给出具体数字或事实，并且能写出读者原本的预期是什么（预期与结果相反才留）。"
  - `data/ai-tells.zh.json:99` → keep 改为"文中给出台账字段、销号标准、检查节点中的至少两项"。

### 9｜【中】"说明最多三条"与"名词账本必输出"冲突

- 位置：`skills/humanize-zh/SKILL.md:212`（说明最多三条）× `skills/humanize-zh/SKILL.md:137`（§4.4 名词账本"诊断模式必输出"）× `skills/humanize-zh/references/coined-terms.md:127`（"账本放在正文之后的说明里"）
- 问题：账本按定义要列全文所有可疑名词，但说明被限制在三条以内；执行者要么违反条数限制，要么砍掉账本，两种都算不按规则交付。
- 证据：样例 A 有"三维分析框架""评价指标体系"两个可疑项，样例 B 有"闭环管理""销号清零"两个；任一篇的账本表格都超过三条（附录 B 的账本逐条列出）。
- 改法：`skills/humanize-zh/SKILL.md:212` 改成"说明只写删改摘要、待核项、建议补充，最多三条；名词账本以表格另附在说明之后，不计入三条。"`skills/humanize-en/SKILL.md:248` 同步加一句 "The term ledger, when required, is appended as a table and does not count toward the three items."

### 10｜【中】中英分治：方向站得住，但中文侧的实现不成比例，且有一处自相矛盾

- 位置：`skills/humanize-zh/SKILL.md:164-165`、`:171-172`、`:174` × `skills/humanize-en/SKILL.md:169-176` × `scripts/scan.py:261-269`
- 问题：诊断方向（英文病在从属结构、中文病在长定语和"的"字堆叠）是对的，但英文给了 6 条可判定的硬限（30/45 词、3 从句、2 个 `-ing`、4 个前置修饰、3 个 `of`、括号嵌套），中文只有两个代理指标，其中"一整段只有一个句号，就该拆"还与同一节的"流水句可长（用逗号推进，意合）"直接相反；"翻译腔名词堆叠"这个中文真正的病没有任何测试。
- 证据：① 样例 A 的 `"空间—行为—体验"三维分析框架` + `评价指标体系` 是典型名词堆叠，但句长 <80 字、"的"<4，`scripts/scan.py:261-269` 的结构检查 0 命中；② `SKILL.md:172` 说"一整段只有一个句号，就该拆"，按字面就是把 :164 认可的意合长句拆掉，而实现里根本没有这条（只有句级 ≥80/≥120 字阈值）；③ 工作流层还漂移了：`SKILL.md:42` 说"时间紧就从第 1 步往后取"，`skills/humanize-en/SKILL.md:45` 却说"stopping after step 3 does not count as done"——同一套管线，两种完成标准，而 §六点五只讨论了句子层差异。
- 改法：① 删掉 `SKILL.md:172` 第二条，或改成"一句 ≥120 字且逗号 ≥8、又没有'因为/但是/于是'这类逻辑标记时才拆；公文、法规、讲话稿不拆"。② 在 `SKILL.md:174` 后补一条可判定测试："同一偏正结构里动词被名词化（'进行/加以/对…的+名词'）且'的'链 ≥2 层 → 还原动词、拆定语"。③ 统一"的"的数值：正文写"三层"、`scripts/scan.py:267` 按"≥4 个"，二者选一（建议都改成"一句内'的'≥4"）。④ 在 `SKILL.md:42` 与 `en:45` 里对齐完成标准。

### 11｜【中】结构类命中不带保留条件，"句长"这条最容易误改的规则没有刹车

- 位置：`README.md:91`（"Every entry carries a keep-condition…the report prints it in a `keep if` column"）× `skills/humanize-en/SKILL.md:171`（30 词以上就 flag）× `skills/humanize-en/references/stock-phrases.md:9`（弱信号成片才处理）
- 问题：结构命中的 keep 是空字符串，报告里显示"—"；而 30 词的 flag 门槛低于任何"成片才处理"的阈值，等于一条孤立的长句就能触发修改，且没有任何文本告诉执行者什么时候该保留。
- 证据：样例 C 第 3 段 36 词长句命中 `long sentence (36 words)`，JSON 里 `"keep": ""`，markdown 报告 keep if 列是"—"。同一份 `SKILL.md:202` 又写 "Keep a long sentence when the length enacts the content"。
- 改法：① 在 `README.md:91` 补一句"结构类命中（句长/从句/的字）的保留条件为 §6.5 的四条 counter-rules"；② 给结构命中加 keep 文本："the length enacts content (list, sequence, build), or the sentence carries one argument — see §6.5 counter-rules"；③ 把 >30 词的 weak 改成"同段 ≥2 句才处理"，>45 词才单见即改。

### 12｜【中低】"排版错误见到就改"与"作者样本优先"冲突

- 位置：`skills/humanize-zh/SKILL.md:156` × `skills/humanize-zh/SKILL.md:208` × `skills/humanize-zh/SKILL.md:25`
- 问题：F 类说半角标点、引号混用"见到就改，不算改动作者语气"；§七却说有作者旧稿时标点按样本频率；§二优先级又把"作者语气与文体规范"排在"去模板"之前——作者若一贯用半角括号，两条规则给出相反动作。
- 证据：我的样例都用全角，没触发；但这是可构造的冲突：作者旧稿写"（含 3 项）"时用半角 `(...)`，按 `:156` 要改，按 `:208` 要留，按 `:25` 应留。
- 改法：`:156` 后加"（作者样本一贯如此、且发布平台不要求全角的，按 §七 样本优先，不改）"；或把 `:156` 的"排版错误"限定为"聊天壳、Markdown 残骸、引用残片"三类，半角标点降为弱信号。

### 13｜【低】参考文件自报的型数、章节编号、家族数与交叉引用四处对不上

- 位置：`skills/humanize-zh/references/explanatory-forms.md:18`（"一、两族十二型"）× `skills/humanize-en/references/explanatory-forms.md:18`（"Two families, thirteen shapes"）× `skills/humanize-zh/SKILL.md:27`（"六类"）× `README.zh-CN.md:22`（"七个痕迹家族"）× `skills/humanize-zh/SKILL.md:176`（"见 humanize-en 的'句子工艺'一节"）
- 问题：同一批文档对同一件事给出四个不一致的说法，读者按标题建立预期后会在正文里对不上号。
- 证据：① 两份 explanatory-forms 正文实际是甲/乙/丙/丁四族、编号 1–15 共十五型，中文标题说 12 型、英文标题说 13 型，且两份互相不一致；② `skills/humanize-zh/SKILL.md` 的章节从"## 三、工作流"开始编号，前面"四条红线""六类 AI 痕迹"没有一、二，正文却用"§五""§六"交叉引用；③ `SKILL.md:176` 指向"humanize-en 的'句子工艺'一节"，而 en 文件里的实际标题是 §6.5 "Sentence craft (English-specific)"（`skills/humanize-en/SKILL.md:163`），中文名在仓库里不存在。
- 改法：① 两份 `explanatory-forms.md:18` 都改成"四族十五型"／"Four families, fifteen shapes"；② `skills/humanize-zh/SKILL.md` 给"四条红线""六类 AI 痕迹"补上"## 一、""## 二、"，或把 §三–§十 的编号全部去掉；③ `SKILL.md:176` 改成"见 `humanize-en/SKILL.md` §6.5 'Sentence craft'（:163-212）"；④ 家族数统一：要么 `SKILL.md:27` 改"七类（G 类中文侧只保留句长上限）"，要么 `README.zh-CN.md:22` 改"六个（中文侧不设 G）"。

### 14｜【低】安装路径与"每次回写语料库"断链，文档承诺的动作安装后无法执行

- 位置：`README.md:56-57`（只复制 `skills/humanize-zh`、`skills/humanize-en`）× `skills/humanize-zh/SKILL.md:184`（`python scripts/corpus_tool.py add ...`）× `skills/humanize-zh/SKILL.md:180`（"每完成一次改稿…就回写"）× `README.md:62`（只在聊天里用时只贴 SKILL.md）
- 问题：按 README 的安装方式，skills 目录里没有 `scripts/` 和 `data/`，§六点八 的命令和"每次回写"在新环境里跑不通；只在聊天里用时更完全无法回写。而 §六点八 被写成默认动作，没有"仅仓库工作副本内可用"的限定。
- 证据：仓库根目录的 `scripts/`、`data/` 不在 `skills/humanize-zh/` 下，`SKILL.md:184` 用的是相对仓库根的 `scripts/corpus_tool.py`；`README.md:62` 的聊天用法只要求贴 SKILL.md。
- 改法：① `README.md:56-57` 改成同时复制 `scripts/` 与 `data/`（或在 skills 内加指向说明）；② `SKILL.md:180` 开头加限定"在仓库工作副本内使用时"；③ 给一个不能回写时的替代动作："把新形态按 `data/README.md` 的字段格式写进交付说明，交给维护者入库。"

---

## 附：五个判断问题的直接回答

**（1）有没有规则会导致过度删改（删掉承担信息/判断的句子）？有，三处。**
第 1 条的"整句删"会误删结果句、limitations、承诺句；第 2 条会让公文依据句被"目的链强信号"删掉；第 1 条依赖的语料条目本身给的改法（`data/ai-tells.zh.json:46` 的"写出具体问题"、`stock-phrases.md:31` 的"写数据，或删"）又与"不增事实"红线冲突——执行者只能在"删整句"和"编一句"之间二选一。此外 limitations 还同时被 strong 条目 `zh-st-041`（见一处就处理）和 §五:149"没有具体下一步就删"两头夹击，文种例外只写在 `defensive-forms.md:97` 和 §七里。

**（2）有没有明显的 AI 痕迹被漏掉？有，具体形态如下。**
- 无源数字/涨幅：「Engagement grew by 47%」「40+ engineers」（第 4 条）；
- 公文"三无措施句"："聚焦重点部位和关键环节""推动各项措施落地见效"——无对象、无时限、无验收（第 3 条）；
- 伪学术框架："'空间—行为—体验'三维分析框架"这类 N 维/框架命名，只被当成弱信号的"框架先行"（第 7 条）；
- LinkedIn 互动钩、hashtag 堆、每句一行断行（第 5 条）；
- 正则覆盖不到的常见变体："not about X, it's about Y"（X 为多词）、"The results?"（复数），实测漏检（第 6 条）；
- 中文"研究发现…具有显著的正向影响""三者之间存在协同效应"这类半统计套话（改法：把这两句作为术语漂移 D6 的新例子加进 `skills/humanize-zh/references/coined-terms.md:26` 与 `skills/humanize-zh/SKILL.md:122`，规则写"没有交互项/检验结果时不得写'协同效应'，没有统计量时不得写'显著'"）。

**（3）keep-condition 是否可执行？大部分可执行，但有四类不可用。**
可执行的例子（能直接判）：`data/ai-tells.zh.json:92`"公文、政策原文、讲话稿"这种文体标签；`zh-pf-005`"写出具体是哪几招"；`zh-pf-020`"能说明每个变量从哪来"；`defensive-forms.md:47` 的"来源标记→保留"。
不可用的四类：①"可能有用"（`coined-terms.md:88`，万能豁免）；②"确实是反直觉发现"（`stock-phrases.md:40`，无可操作标准）；③"一层真实不确定性"（`stock-phrases.md:113`，谁判定"真实"）；④"读者确实缺少的背景"（`SKILL.md:74`，判据是"读者身份"但全文没有定义怎么测）。还有一类是**字面自证**：`zh-pf-010` 的 keep"确有台账与销号机制"会被"建立问题台账…销号清零"这句话本身满足。

**（4）中英规则差异是否站得住？方向站得住，执行不对称。**
"英文查从句/句长、中文查'的'字堆叠"这个诊断是对的：我的英文样例里唯一的结构命中就是 36 词长句（正是该抓的），中文样例结构层 0 命中而真正的病在名词堆叠和评价性拔高（正是该抓的没抓住）。但英文侧有 6 条数字硬限，中文侧只有 1 个"的"计数代理指标，且正文说"三层"、实现按"≥4 个"；"翻译腔名词堆叠"完全没有测试；中文侧还多了一句与"流水句可长"相反的"一段一个句号就拆"。另外工作流层的完成标准（`zh:42` vs `en:45`）也没登记进差异表。

**（5）改稿后的结果是否真的更好读？两处对照，一处变差。**

对照 1（样例 A 开头，变好）：
> 前：在当今数字化转型不断深入的背景下，高校图书馆空间改造越来越受到关注。值得注意的是，现有研究多聚焦于硬件设施与空间布局，而对使用体验的系统考察仍显不足。
> 后：现有研究多聚焦于图书馆改造的硬件设施与空间布局，对使用体验的系统考察仍显不足。

第一句"关注度"不提供任何信息（`stock-phrases.md:31` 的 keep 是"有具体数据"，原文没有），删掉后读者第一句就拿到研究缺口；"值得注意的是"删壳后语义完全不变。纯收益，没有丢信息。

对照 2（样例 C 长句，变好）：
> 前：We ran the pilot across three squads, rolling out a lightweight written update format, collecting feedback from 40+ engineers, and iterating weekly — while keeping the ritual lightweight, ensuring everyone stayed aligned, and fostering a culture of transparency.
> 后：We ran the pilot across three squads. Every week we rolled out a written update format, collected feedback from 40+ engineers, and iterated on it.

三个 `-ing` 尾巴还原成定式动词，36 词拆成 13+17 词；"ensuring everyone stayed aligned" "fostering a culture of transparency" 没有可核对内容，删掉读者不少知道任何东西。

对照 3（样例 B，照规则直译后变差）：
> 前：为深入贯彻落实上级消防安全工作部署，进一步压实安全责任，切实防范各类事故发生，决定开展消防安全专项检查。
> 按 `SKILL.md:83` 直译后：为防范事故发生，决定开展消防安全专项检查。

读者丢了"依据哪一级部署"；再按 §五:149 删掉结尾「学校将以此次专项检查为契机，进一步健全长效机制」，公文只剩要求和时限，承诺没了。所以这套规则在公文上**不能照字面走**，第 2、3 条就是现场证据；经过人工判断后保留依据与承诺的版本见附录 B。

---

## 附录 A：三篇自造样例（改前全文）

**样例 A｜中文学术摘要（242 字）**

> 在当今数字化转型不断深入的背景下，高校图书馆空间改造越来越受到关注。值得注意的是，现有研究多聚焦于硬件设施与空间布局，而对使用体验的系统考察仍显不足。本文基于"空间—行为—体验"三维分析框架，通过实地调研与问卷调查系统分析了空间使用体验，并构建了相应的评价指标体系。研究发现，安静程度、座位类型与采光条件对使用体验具有显著的正向影响，且三者之间存在协同效应。这不仅拓展了图书馆空间研究的新视角，也为高校图书馆改造实践提供了有力支撑。本研究具有重要的理论价值与实践意义。当然，本文仍存在一定局限，样本量相对有限，未来有待进一步研究。

**样例 B｜中文公文通知（250 字）**

> 关于开展 2026 年校园消防安全专项检查的通知
>
> 各学院、各部门：
>
> 为深入贯彻落实上级消防安全工作部署，进一步压实安全责任，切实防范各类事故发生，决定开展消防安全专项检查。现将有关事项通知如下：
>
> 一、提高认识，统一思想。各单位要高度重视消防安全工作。
>
> 二、聚焦重点，全面排查。各单位要聚焦重点部位和关键环节，建立问题台账，实行闭环管理，确保隐患整改到位、销号清零。
>
> 三、压实责任，狠抓落实。各单位要明确责任分工，强化督导检查，推动各项措施落地见效。
>
> 请各单位于 2026 年 11 月 30 日前将专项检查工作总结报送保卫处。学校将以此次专项检查为契机，进一步健全长效机制，推动消防安全工作再上新台阶。
>
> 特此通知。

**样例 C｜英文 LinkedIn post（164 词）**

> I'm thrilled to share that our team just wrapped a six-week pilot on async standups. 🎉
>
> In today's fast-paced world, teams are constantly being asked to do more with less — and meetings are often the first thing to go. Here's the thing: it's not about killing meetings, it's about being intentional with async communication.
>
> We ran the pilot across three squads, rolling out a lightweight written update format, collecting feedback from 40+ engineers, and iterating weekly — while keeping the ritual lightweight, ensuring everyone stayed aligned, and fostering a culture of transparency.
>
> The results? Engagement grew by 47%. That's a huge validation of the approach. Honestly, this has been a game changer for how our team ships.
>
> What I love most is that this experience underscores the importance of clarity — it's not just a communication win, it's a culture win. This is a testament to what small process changes can unlock at scale.
>
> I'm so grateful to everyone who leaned in. The possibilities are endless. What's your take? 👇
>
> #async #leadership #futureofwork

---

## 附录 B：七步管线实录（人工执行，未运行改稿脚本）

### B.1 样例 A（中文学术摘要）

| 步骤 | 动作 |
|---|---|
| 1 定主张与读者 | 主张＝三项环境因素影响使用体验（回归发现）；读者＝图情领域审稿人。结果句不能删。 |
| 2 守内容 | "某高校"匿名可接受；"显著的正向影响""协同效应"无统计量、无模型 → 不补数、不删句，标〔需核对〕；样本量未给 → 不补。 |
| 3 拆防御 | 末句 limitations：按 strong 条目 `zh-st-041` 本应处理，但 `defensive-forms.md:97`（文种要求）和 `SKILL.md:205` 要求保留 → 人工保留，只把"有待进一步研究"留作待验证层；这正是第 1 条的冲突。 |
| 4 删解释 | "本文…"自指在摘要属规范（`data/ai-tells.zh.json` 的 `zh-pf-015` keep 允许一次），保留一处。 |
| 5 换句式 | 删"在当今…背景下"；删"越来越受到关注"（无数据支撑）；删"值得注意的是"；删两处拔高句（"这不仅拓展了…新视角，也为…提供了有力支撑""本研究具有重要的理论价值与实践意义"）。 |
| 6 清名词 | "三维分析框架"五问不过（无定义/无溯源/无边界）→ 按 `coined-terms.md:88` 保留原句并标〔待核：出处与三维定义〕（此处正是第 8 条说的问题：这条 keep 实际上放行了它）；"评价指标体系"保留并标〔待核：指标清单与来源〕。 |
| 7 结构/回查 | 摘要"缺口—方法—结果—局限"结构属文种，保留；字数 242→约 190（-21%，含两处〔待核〕标注），略超 15% 阈值 → 逐段核对：删掉的只有壳与拔高，无事实、范围、承诺丢失；删改与待核项写进说明。 |

改后稿（人工版）：

> 现有研究多聚焦于图书馆改造的硬件设施与空间布局，对使用体验的系统考察仍显不足。本文基于〔待核：出处与三维定义〕"空间—行为—体验"三维分析框架，通过实地调研与问卷调查系统分析了空间使用体验，并构建了相应的评价指标体系〔待核：指标清单与来源〕。结果显示，安静程度、座位类型与采光条件对使用体验均有显著的正向影响，且三者之间存在协同效应〔需核对：原文未给出统计量与检验方法〕。样本量相对有限，未来有待进一步研究。

名词账本（诊断模式，2 条）：三维分析框架（首段，伪学术命名候选，定义/溯源/边界三问未过，标〔待核〕）；评价指标体系（首段，空壳抽象名词，定义/边界不过，标〔待核〕）。

### B.2 样例 B（中文公文通知）

| 步骤 | 动作 |
|---|---|
| 1 定主张与读者 | 可执行信息＝三项要求＋11 月 30 日前报送；读者＝各学院/部门经办人。依据、时限、报送对象不能删。 |
| 2 守内容 | 2026-11-30 未写星期，无需对日历；"上级部署"无文件名 → 不补；措施缺时限/责任人 → 缺口写进说明，不代写。 |
| 3 拆防御 | "统一思想""高度重视"的语料库 keep 都是"公文"（`zh-pf-008`/`zh-pf-007`）→ 按规则保留，但保留后这两句仍不提供可执行信息；这条落差正是第 3 条。 |
| 4 删解释 | 无解释性表述。 |
| 5 换句式 | **冲突现场**：按 `SKILL.md:83` 目的链强信号删 X 会连"依据上级部署"一起删；按 `defensive-forms.md:47` 与 `zh-pf-014` 的公文 keep 则应保留依据。最终人工取"保留依据、只删套话"。同理"狠抓落实""压实责任"也被 corpus keep＝公文 放行，规则实际能删的只有"推动各项措施落地见效""再上新台阶"这类拔高。 |
| 6 清名词 | "闭环管理""销号清零"：五问不过（无字段、无签批人），但 corpus keep"确有台账与销号机制"被字面满足 → 保留并标〔待补：台账字段、销号标准、检查节点、完成时限〕（第 8 条证据）。 |
| 7 结构/回查 | 四字对仗小标题属公文体例（`SKILL.md:147` 允许保留），不动；字数 250→约 210（-16%，略超 15% 阈值）→ 逐段核对，删掉的只是三处套话与拔高；删改与待补项写进说明。 |

改后稿（人工版，节选）：

> 各学院、各部门：
>
> 为贯彻落实上级消防安全工作部署，决定开展校园消防安全专项检查。现将有关事项通知如下：
>
> 一、提高认识，统一思想。各单位要高度重视消防安全工作。
>
> 二、聚焦重点，全面排查。各单位要聚焦重点部位和关键环节，建立问题台账，实行闭环管理，确保隐患整改到位、销号清零〔待补：重点部位清单、台账字段、销号标准、完成时限〕。
>
> 三、压实责任，狠抓落实。各单位要明确责任分工，强化督导检查〔待补：分工表与检查节点〕。
>
> 请各单位于 2026 年 11 月 30 日前将专项检查工作总结报送保卫处。学校将以此次专项检查为契机，进一步健全长效机制。
>
> 特此通知。

说明（三条）：删"推动各项措施落地见效""再上新台阶"两处拔高，保留"依据上级部署""健全长效机制"两处承担来源与承诺的句子；四字标题与"统一思想""高度重视""狠抓落实"按公文 keep 全部保留；四项待补材料（重点部位、台账字段、销号标准、验收时限）需作者提供。**这份稿子规则能干预的只有两处拔高——这正是第 3 条要说的：公文样例跑到最后，真正的"措施不可执行"没有规则管。**

### B.3 样例 C（英文 LinkedIn post）

| 步骤 | 动作 |
|---|---|
| 1 定主张与读者 | 主张＝六周 async standup 试点＋参与人数＋一个涨幅；读者＝LinkedIn 同行。 |
| 2 守内容 | "six-week""three squads""40+ engineers""47%"都在原稿里，不能删不能改；47% 与 40+ 无来源 → 标〔needs source〕，不代填。 |
| 3 拆防御 | "I'm so grateful to everyone who leaned in" 属社交致谢，不是防御 → 保留（技能里没有针对真实致谢的 keep-condition，靠 §十 判断）。 |
| 4 删解释 | "it's not about killing meetings, it's about being intentional" 是翻案句；X 是 LinkedIn 读者的真实误解（以为 async 就是砍会），按 keep-condition 可留，但需改写为陈述，不保留"Here's the thing"壳。 |
| 5 换句式 | "In today's fast-paced world" 强信号删，但保住句中的事实前提（"meetings are often the first thing to go"）；"Here's the thing"删；"-ing 链"拆（见对照 2）；"The results?""That's a huge validation""What I love most…underscores""a testament to""The possibilities are endless" 逐条处理（删或改陈述）；"game changer""at scale" 成片才处理（本文弱信号已 ≥4，按弱信号规则处理）。 |
| 6 清名词 | 无生造名词；47% 属于第 4 条的"无源数据"（本仓库目前没有归口）。 |
| 7 结构/回查 | 删掉整段评价（"What I love most…culture win"）、两处拔高、开场壳后，字数 164→约 95（-42%），逐段核对：六周、三个小组、40+ 工程师、47% 四项事实全部保留，47% 标来源；作者对"清晰"的看重改成一句陈述保留，不是整段删掉。 |

改后稿（人工版）：

> Our team just wrapped a six-week pilot on async standups.
>
> Meetings are often the first thing to go when teams are asked to do more with less. We were not trying to kill meetings; we were trying to make async communication intentional.
>
> We ran the pilot across three squads. Every week we rolled out a written update format, collected feedback from 40+ engineers, and iterated on it.
>
> Engagement grew by 47%〔needs source: sample and time window〕.
>
> The part I care about most is clarity. I'm grateful to everyone who took part. What's your take?

改动说明：删 "I'm thrilled" 壳、世界背景开场、整段评价性拔高（"huge validation / testament / possibilities are endless"）；拆 36 词长句；47% 标来源；保留作者对"清晰"的看重与结尾真实征询（不是所有被列出的形态都必须删）。

### B.4 扫描器交叉核对（仅定位，不构成判断）

| 样例 | 扫描结果（仓库 `scripts/scan.py`） | 说明 |
|---|---|---|
| A | strong 5 / weak 2，verdict heavy；命中：宏大开场、"值得注意的是"、"重要的理论价值""提供有力支撑""有待进一步研究"；terms 只有"评价指标体系" | 未命中"三维分析框架"（第 7 条） |
| B | strong 0 / weak 8，verdict "no strong hits; weak signals only - do not edit on these alone"；5 条 keep＝公文 | 公文样例在规则上"不可动"（第 3 条） |
| C | strong 5 / weak 6，verdict heavy；命中含 "In today's fast-paced""Here's the thing""underscores""a testament to""The possibilities are endless"；36 词长句为 weak 且 keep 为空 | 未命中 "not about X, it's about Y"（多词 X）、"The results?"（复数）、"What's your take?"、hashtag、47%（第 4、5、6、11 条） |
