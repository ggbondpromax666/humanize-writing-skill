# 对抗测试报告：humanize-writing-skill（盲审 B）

- 评审对象：`humanize-writing-skill` 仓库按现状（`data/ai-tells.zh.json` v1.1.0 / 192 条，`data/ai-tells.en.json` v1.0.0 / 134 条）。
- 评审方式：只读仓库产物，构造极端输入，直接运行 `scripts/scan.py` 与 `scripts/corpus_tool.py`。**所有 17 条均有复现**；未复现的猜测不在本报告内。
- 约束遵守：仓库内只新增本文件；所有测试文件写在系统临时目录 `%TEMP%\hws-review`；未运行 git；破坏性命令（`corpus_tool.py add`、改 JSON）一律在仓库的临时副本上做。
- 结论：**高 3 条 / 中 13 条 / 低 1 条**。工具在"语料库→文本"这条链路上可用，但**语言判定、英文大小写标志、规则去重、校验器**四个环节会系统性产出错误结论；`README` 承诺的 false-positive guards 在扫描器里没有实现。

## 摘要表

| # | 严重度 | 问题 | 复现输入 |
|---|---|---|---|
| A-01 | 高 | 中英混排被判成单一语言，另一语言规则整批失效（无提示） | `mixed2-zh.txt`、`ascii-with-zh.txt` |
| A-02 | 高 | 英文规则被全局强制 `re.IGNORECASE`，`[A-Z]` 正则塌缩成 `[a-z]`，正常词被当"未展开缩略语" | `english-methods.txt` |
| A-03 | 高 | 同一短语被 2–4 条规则命中，severity/fix 互相矛盾，密度与 verdict 被重复计数 | `dup.txt`、`suowei.txt` |
| A-04 | 中 | `keep` 条件与 `fix` 指令自相矛盾，按 fix 改会违反"不丢信息"红线 | `conflict.txt` |
| A-05 | 中 | 法律条文长句被判 strong 结构问题，且结构命中没有 keep 条件 | `legal-verylong.txt`、`english-legal.txt` |
| A-06 | 中 | 公文套话被大面积命中并判 `heavy`，公文 keep 条件没有在判定层生效 | `gongwen.txt` |
| A-07 | 中 | 学术方法节误报：`研究表明` 双强命中；`结构方程模型` 被当伪学术命名 | `academic.txt` |
| A-08 | 中 | 技术文档中"闭环控制/端到端加密/代码复用"等真实术语被当空壳抽象词 | `tech.txt`、`zh-clean.txt` |
| A-09 | 中 | 正常人类散文被 strong 命中（`说实话`、`的` 字堆叠、`越来越`） | `human.txt` |
| A-10 | 中 | 漏报：SKILL 点名要盯的"进行+名词/对于…来说"没有规则；`具有重要作用`、`不可否认` 也不命中 | `predicate.txt`、`slop.txt` |
| A-11 | 中 | 无最小文本长度门槛，6 字文本被判 `heavy`，与 SKILL"短于两三句不下判断"冲突 | `short.txt` |
| A-12 | 中 | 未闭合代码围栏把其后全文静默吞掉，报告 `clean` | `unclosed-fence.txt` |
| A-13 | 中 | 非 UTF-8 文件直接抛 `UnicodeDecodeError` 栈；BOM 未剥离时围栏失效、代码块被扫描 | `gbk.txt`、BOM 围栏样本 |
| A-14 | 中 | `data/` 缺失时回退 inline 表：规则 192→50，且 keep 条件全部为空 | 副本目录 `nodata` |
| A-15 | 中 | `corpus_tool.py validate` 形同虚设：零宽正则、坏 ID、缺字段、`keep:"无"` 全部通过 | 副本目录 `repo-copy` |
| A-16 | 中 | README 声称的 false-positive guards（引文/标题/讨论词/文体）在扫描器中未实现 | `discussed-word.txt` |
| A-17 | 低 | 空文件被判成 `language: en` | `empty.txt` |

---

## 0. 复现环境（先粘贴运行一次）

```powershell
# 所有测试文件写入系统临时目录，不写入仓库
$repo = 'C:\Users\Lenovo\OneDrive\文档\deepseek-harness\default-workspace\humanize-writing-skill'
$T = Join-Path $env:TEMP 'hws-review'
New-Item -ItemType Directory -Force $T | Out-Null
Set-Location $repo

Set-Content -Path "$T\legal-verylong.txt" -Encoding utf8 -Value @'
甲方应当在收到乙方书面通知后的十个工作日内按照本合同附件二约定的技术标准与验收流程对乙方交付的设备进行检验并将检验结果以书面形式通知乙方逾期未通知的视为设备符合约定标准且乙方有权拒收并要求甲方承担由此产生的全部费用包括运输费仓储费与检验费，并有权就停机造成的合理损失另行主张赔偿。
'@
Set-Content -Path "$T\english-legal.txt" -Encoding utf8 -Value @'
The Supplier shall, within ten business days after receipt of the Buyer's written notice, inspect the equipment delivered under Schedule 2 in accordance with the technical standards and acceptance procedures set out in the Contract, and shall notify the Buyer in writing of the results of such inspection, failing which the equipment shall be deemed to conform to the agreed standards and the Buyer shall be entitled to reject the same and to recover from the Supplier all costs thereby incurred.
'@
Set-Content -Path "$T\gongwen.txt" -Encoding utf8 -Value @'
关于进一步加强安全生产工作的通知

各单位要高度重视安全生产工作，切实压实主体责任，层层传导压力，进一步推进隐患排查整治，多措并举、标本兼治。
各部门要对标对表上级部署，举一反三，抓早抓小，实行清单化管理、闭环管理，确保各项任务落地见效。
下一步，各单位要持续巩固成果，形成长效机制。经检查，本阶段工作成效显著，取得阶段性成效，现将有关情况通报如下。
'@
Set-Content -Path "$T\academic.txt" -Encoding utf8 -Value @'
本研究采用问卷调查法，样本来自东部地区六所高校的在校本科生，有效问卷共 812 份。研究采用结构方程模型检验变量之间的关系，所有量表均通过信效度检验。
已有研究表明，学习投入与学业成绩显著正相关（β=0.41，p<0.01）。本研究的局限在于样本量有限，结论的外部效度有待进一步检验，未来研究可扩大样本范围。
基于上述理论框架，本研究构建了包含三个维度的分析框架，并对各变量进行了操作化定义。
'@
Set-Content -Path "$T\tech.txt" -Encoding utf8 -Value @'
该接口支持 HTTP/2 与 gRPC 两种调用方式，默认超时 30 秒，并发上限由客户端配置决定。
服务采用闭环控制策略：监控模块每 5 秒采集一次延迟指标，控制器据此调整副本数；该链路端到端加密，证书由内部 CA 签发。
稳定性保障措施包括：副本数不少于 3、跨可用区部署、滚动升级时先摘流量。代码复用集中在 common 包，新增模块请对齐现有目录结构。
该接口同时支持多种鉴权方式，返回体中的错误码定义详见下文。
'@
Set-Content -Path "$T\zh-clean.txt" -Encoding utf8 -Value @'
本方案采用微服务架构，通过服务注册发现与配置中心实现统一治理，支持灰度发布与限流熔断。网关层负责鉴权与路由，业务层按领域拆分为订单、库存、结算三个服务，数据层使用分库分表与读写分离。监控体系覆盖日志、指标、链路追踪，告警规则按服务等级分级配置。整体设计目标是保证高可用与可观测性，同时为后续的弹性扩容留出接口。
'@
Set-Content -Path "$T\human.txt" -Encoding utf8 -Value @'
那年冬天我在县城住了三个月。房东是个修钟表的，姓周，四十来岁，话不多。每天早上他把店门开一条缝，坐在柜台后面擦零件，一擦就是一上午。
我常去街口的面馆吃面，五毛钱一碗，汤是清的，上面飘着几片葱花。老板认得我，有时候多给半勺。说实话，那半年他为什么总是笑，我到现在也没问。
离开那天下了小雨，周师傅送我到车站，什么也没说，把一把旧伞塞给我，只说了句：“慢走。”他记得那个冬天的早晨的雾，还记得母亲缝的棉袄的针脚。天越来越冷，街上的铺子关得越来越早。
后来我再没回去过。
'@
Set-Content -Path "$T\slop.txt" -Encoding utf8 -Value @'
值得注意的是，在当今数字化时代，人工智能技术正在快速发展。
赋能与闭环已经成为企业转型的关键抓手，这些概念为组织变革提供了有力支撑，具有重要作用。
不可否认，AI 不是要取代人，而是要把人从重复劳动中解放出来，发挥着不可替代的作用。
综上所述，人工智能具有重要作用，其未来发展趋势不可估量。
'@
Set-Content -Path "$T\predicate.txt" -Encoding utf8 -Value @'
本次改革对流程进行了优化，对于一线员工来说，这是值得肯定的。对数据进行了清洗，对接口进行了封装。
'@
Set-Content -Path "$T\mixed2-zh.txt" -Encoding utf8 -Value @'
In today's fast-paced world, it's worth noting that AI plays a crucial role in modern workflows. Experts agree that teams must delve into the ever-evolving landscape of automation, and studies show that only time will tell which vendors survive.

正如一位国内学者所言：“人工智能正在深刻改变我们的工作方式，这一点毋庸置疑。我们必须正视技术带来的结构性挑战。”
'@
Set-Content -Path "$T\english-methods.txt" -Encoding utf8 -Value @'
We fit the model on 812 responses and evaluated it with five-fold cross-validation. The data model described in Section 2 was implemented in Python; this model predicts the outcome from three covariates. We used the network layer of the stack as a baseline in order to compare throughput, and we report results at scale. The fact that the estimates are stable represents an important check on the specification.
'@
Set-Content -Path "$T\discussed-word.txt" -Encoding utf8 -Value @'
我最近戒掉了“赋能”这个词，因为它已经把“给予支持”的意思磨没了。
很多编辑在标题里写“闭环”，其实只是想说“有始有终”。
'@
Set-Content -Path "$T\dup.txt" -Encoding utf8 -Value @'
一言以蔽之，这套方案值得一试。
毋庸置疑，这个结论已经得到验证。
由此可见，项目按期完成。
具体而言，成本下降了百分之十二。
'@
Set-Content -Path "$T\suowei.txt" -Encoding utf8 -Value @'
所谓“赋能”，不过是一种管理话术，并没有可操作的定义。
所谓生态位，只是把竞争换了个说法。
'@
Set-Content -Path "$T\conflict.txt" -Encoding utf8 -Value @'
这并非否定过去的做法，而是调整了优先级。
截至我的知识，这个问题还没有定论。
'@
Set-Content -Path "$T\short.txt" -Encoding utf8 -Value @'
值得注意的是。
'@
$f = ([string][char]96) * 3   # 三个反引号：一个故意不闭合的代码围栏
Set-Content -Path "$T\unclosed-fence.txt" -Encoding utf8 -Value ($f + "text`n下面是运行日志：`n值得注意的是，系统在启动时出现了告警。`n综上所述，根本问题在于配置错误，赋能闭环抓手都需要重新设计。`n")
New-Item -ItemType File -Force -Path "$T\empty.txt" | Out-Null

# PowerShell 5.1 的 -Encoding utf8 会写 BOM；这里统一去掉，保证 A-12/A-13 的对照可复现
Get-ChildItem "$T\*.txt" | ForEach-Object {
    $b = [System.IO.File]::ReadAllBytes($_.FullName)
    if ($b.Length -ge 3 -and $b[0] -eq 0xEF -and $b[1] -eq 0xBB -and $b[2] -eq 0xBF) {
        [System.IO.File]::WriteAllBytes($_.FullName, $b[3..($b.Length - 1)])
    }
}

# ASCII 占绝大多数、只夹一两句中文的"中文文档"
$log = '2026-10-29T12:00:00Z INFO  request_id=abc-123 status=200 latency=12ms path=/api/v1/items user=svc-checkout cache=HIT pool=db-01 '
[System.IO.File]::WriteAllText("$T\ascii-with-zh.txt", (($log * 24) -join "`n") + "`n值得注意的是，修改缓存 ttl 后必须重启服务。`n综上所述，赋能与闭环的改造留到下一阶段。`n")

# GBK（Windows 记事本 ANSI 默认保存的编码之一）
$gbk = [System.Text.Encoding]::GetEncoding(936)
[System.IO.File]::WriteAllBytes("$T\gbk.txt", $gbk.GetBytes("值得注意的是，这是一份用 GBK 编码保存的中文草稿。`r`n综上所述，结论已经很清楚。`r`n"))

# 带 UTF-8 BOM 的文件（A-13 用）
$enc = New-Object System.Text.UTF8Encoding($true)
[System.IO.File]::WriteAllText("$T\bom.txt", "他记得那个冬天的早晨的雾，还记得母亲缝的棉袄的针脚。", $enc)

Write-Output "fixtures ready in $T"
```

---

## A-01 中英混排被判成单一语言，另一语言规则整批失效（高）

**影响**：只要中文 CJK 字符占全文 `>8%`，整篇就只跑中文规则；占 `<8%`，整篇只跑英文规则。中英混排的稿子（中文引文 + 英文正文、中文说明 + 英文日志）会整批漏掉另一种语言的所有命中，报告里没有"另一种语言未检查"的提示。

**复现**

```powershell
# 英文 80% + 中文引文：被判 zh，英文 6 个 strong 全部漏掉
python "$repo\scripts\scan.py" "$T\mixed2-zh.txt"

# 同一文件强制 en：英文 strong 立刻出现
python "$repo\scripts\scan.py" "$T\mixed2-zh.txt" --lang en

# 中文文档 99% 是英文日志：被判 en，中文 2 个 strong 全部漏掉
python "$repo\scripts\scan.py" "$T\ascii-with-zh.txt"
python "$repo\scripts\scan.py" "$T\ascii-with-zh.txt" --lang zh
```

**实际输出（auto 判定）**

```text
# mixed2-zh.txt
language: zh | characters: 50 | sentences: 2
strong hits: 1 (20.0 per 1000 characters) | weak hits: 1
| 3 | strong | stock | `毋庸置疑` | 用共识替代证据 | ... |
| 3 | weak   | stock | `毋庸置疑` | 确定性副词   | ... |

# 同一文件 --lang en
language: en | words: 47 | sentences: 2
strong hits: 6 (127.66 per 1000 words) | weak hits: 3
| 1 | strong | stock | `In today's fast-paced` | world-staging opener | ... |
| 1 | strong | stock | `it's worth noting`    | paragraph opener, no referent | ... |
| 1 | strong | stock | `plays a crucial role` | importance inflation | ... |
| 1 | strong | stock | `only time will tell`  | uplift closer | ... |

# ascii-with-zh.txt（auto）
language: en | words: 606 | sentences: 1
| 1 | strong | structure | `﻿2026-10-29T12:00:00Z INFO ...` | very long sentence (480 words) | — | split at a conjunction |
# （中文两行里的 值得注意的是 / 综上所述 / 赋能 / 闭环 一条都没有）
```

**期望行为**：混排文本应同时（或按段落）跑两种规则并标出"mixed / 已检查 zh+en"；至少要在报告头注明"chosen: zh（CJK 16.4%），en 规则未运行"。

**修复建议**

1. `scripts/scan.py:240-242` 的 `guess_lang` 改成三档：`cjk_ratio < 0.02 → en`，`> 0.60 → zh`，其余返回 `mixed`；`scan.py:493` 遇到 `mixed` 时调用 `pick_rules('auto')`（该分支已存在，`scan.py:223-232`，但目前从 CLI 不可达，因为 `main` 先把它判成单一语言）。
2. `scan.py:251-287` 的 `structure_hits` 需要按行/段判语言，而不是全篇一个 `lang`。
3. 报告头输出实际的 CJK 比例与"未运行的规则集"。

---

## A-02 英文规则被全局强制 IGNORECASE，`[A-Z]` 正则塌缩成 `[a-z]`（高）

**影响**：`scan.py` 对所有英文规则无条件加 `re.IGNORECASE`，而语料库里的 `[A-Z]{2,6}`（"未展开缩略语"）设计依赖大小写。加了 IGNORECASE 后，任何两到六位的小写单词后面跟 `model/framework/method/principle` 都会命中，技术/学术写作里的正常 `the model`、`data model`、`this model` 被当成"未展开缩略语"。

**复现**

```powershell
python "$repo\scripts\scan.py" "$T\english-methods.txt"
```

**实际输出**

```text
language: en | words: 70 | sentences: 5
weak hits: 9
| 1 | weak | coined | `the model`        | unexpanded acronym + label | expanded at first use | expand at first use; ... |
| 1 | weak | coined | `The data model`   | framework name (verify origin) | proposer and source can be named | ... |
| 1 | weak | coined | `data model`       | unexpanded acronym + label | ... |
| 1 | weak | coined | `this model`       | unexpanded acronym + label | ... |
| 1 | weak | coined | `the network layer`| system metaphor (verify origin) | ... |
```

`the model` / `data model` / `this model` 都不是缩略语；`The data model` 被 `en-ct-001`（`\bthe [A-Z][A-Za-z]+ ...`）命中也是同一原因——IGNORECASE 下 `[A-Z]` 等价于 `[A-Za-z]`。

**根因**

- `scripts/scan.py:299`：`flags = rule.flags | (re.IGNORECASE if lang in ("en", "auto") else 0)`。
- `scripts/scan.py:167-174`：从 JSON 构造 `Rule` 时**没有读取** `flags` 字段，所以语料库无法声明"这条要区分大小写"。
- `data/ai-tells.en.json:72`（`en-ct-002`）与 `:71`（`en-ct-001`）的正则本身依赖大小写。

**期望行为**：`en-ct-002` 只匹配 `[A-Z]{2,6}` 全大写缩写（如 `SEM model`）；`the model` 不应命中。

**修复建议**

1. `scan.py:299`：对英文默认 **不加** IGNORECASE；只在单条规则需要时加。
2. `scan.py:167-174` 读取可选字段 `flags`（如 `"flags": "i"`），在 `Rule` 里生效；给确实需要忽略大小写的条目（如 `en-st-046` 词表）显式标记。
3. 不改代码的临时降级：把 `en-ct-001/002` 的 `[A-Z]` 改为 `(?-i:[A-Z])`。

---

## A-03 同一短语被多条规则命中，severity/fix 互相矛盾，密度被重复计数（高）

**影响**：同一个 span 被 2–4 条规则认领，报告不去重（`scan.py:307-315` 的去重键包含 `label`，所以不同 label 算不同命中）。后果：①同一句收到互相矛盾的改法；②`strong_per_1000_units` 翻倍，verdict 从 moderate 变 heavy。

**复现**

```powershell
python "$repo\scripts\scan.py" "$T\dup.txt"
python "$repo\scripts\scan.py" "$T\suowei.txt"
```

**实际输出**

```text
# dup.txt：4 行文本共 8 条命中（4 strong）
| 1 | weak   | stock | `一言以蔽之` | 口语壳替代逻辑 | ... | 删，直接给结论 |
| 1 | strong | stock | `一言以蔽之` | 同义复述       | ... | 只留更好懂的那一版 |
| 2 | strong | stock | `毋庸置疑`   | 用共识替代证据 | ... | 删；有证据就写证据 |
| 2 | weak   | stock | `毋庸置疑`   | 确定性副词     | ... | 删，或给出证明 |
| 3 | strong | stock | `由此可见`   | 假装推理已完成 | ... | 删，或补出推理 |
| 3 | strong | explanatory | `由此可见，项目按期完成` | 替读者下判断 | ... | 删，让事实自己说话 |
| 4 | weak   | stock | `具体而言` | 逻辑标签   | ... | 删，让事情自己排先后 |
| 4 | weak   | stock | `具体而言` | 伪精确化   | ... | 没更具体就删 |
strong hits: 4 (78.43 per 1000 characters)  ← 实际只有 4 个短语

# suowei.txt：2 行文本共 4 个 strong
| 1 | strong | coined | `所谓“赋能”`    | 引号新名词（需体检） | ... |
| 1 | strong | stock  | `所谓“赋能”，不过是` | 贬抑式定义 | ... |
| 2 | strong | coined | `所谓生态位`     | 引号新名词（需体检） | ... |
| 2 | strong | stock  | `所谓生态位，只是` | 贬抑式定义 | ... |
strong hits: 4 (108.11 per 1000 characters)
verdict: heavy - most strong hits are probably real
```

**互相矛盾的条目**（均为同一文件的同一文本）：

| 短语 | 规则 A | 规则 B | 矛盾点 |
|---|---|---|---|
| 一言以蔽之 | `zh-st-010` weak / "删，直接给结论" | `zh-st-046` strong / "只留更好懂的那一版" | 同一短语一条说"只在成片出现时处理"，另一条说"见一处就处理"，改法也不同 |
| 毋庸置疑 | `zh-st-003` strong | `zh-st-069` weak | severity 相反 |
| 由此可见 | `zh-st-009` strong | `zh-ex-001` strong | 两条 strong 重复计数，fix 不同 |
| 具体而言 | `zh-st-014` weak（逻辑标签） | `zh-st-047` weak（伪精确化） | 同一短语两个家族、两个改法 |
| 有研究表明 | `zh-st-030` strong | `zh-pf-016` strong | 见 A-07，"研究表明"被算两遍 |
| 闭环 | `zh-ct-006`、`zh-ct-017`、`zh-pf-010` | — | 一个词 3 条规则，见 A-08 |
| 所谓X | `zh-ct-001` strong | `zh-st-065` strong | 2 行文本 4 个 strong，密度翻倍 |

**期望行为**：同一 span 只保留一条（取最高 severity 或合并 label）；`corpus_tool.py validate` 对"字面量互相包含"的条目给出警告。

**修复建议**

1. `scan.py:307-315`：去重键改为 `(line, col, len(match), family)` 或直接按 `(line, start, end)` 合并，保留 severity 最高的条目并把 label 合并（如 `"同义复述/口语壳"`）。
2. 合并语料：`zh-st-010` 与 `zh-st-046` 合并为一条（建议 weak，fix 写成"若后句只是同义改写则删"）；`zh-st-003`/`zh-st-069`、`zh-st-014`/`zh-st-047`、`zh-st-030`/`zh-pf-016`、`zh-ct-001`/`zh-st-065` 各留一条。
3. `corpus_tool.py:110-121` 增加"字面量重叠"检查：把每条正则的最长固定子串抽出来，互为子串的报 warning。

---

## A-04 keep 条件与 fix 指令自相矛盾，照 fix 改会违反"不丢信息"红线（中）

**影响**：报告把 `keep if` 与 `suggested fix` 并排打印，但有几条规则在 keep 成立时仍要求删除——读者按 fix 执行就会删掉"保留条件明确说要留"的信息，直接违反 SKILL.md 四条红线第 2 条（不丢信息）与 README 第 99 行"最常见的失误是删掉承担逻辑的句子"。

**复现**

```powershell
python "$repo\scripts\scan.py" "$T\conflict.txt"
python "$repo\scripts\scan.py" "$T\dup.txt"   # 看 `由此可见` 那行
```

**实际输出**

```text
| 1 | strong | stock | `并非否定过去的做法，而是` | 翻案对比 | 否定部分纠正真实误解 | 直接写Y |
| 2 | strong | defensive | `截至我的知识` | 知识截止免责 | 需要时效说明就写带日期的来源 | 整句删；承认没资料后不能再用猜测填空 |
```

- `zh-st-016`（`data/ai-tells.zh.json:21`）：keep = "否定部分纠正真实误解"（即 X 是必须保留的纠正），fix = "直接写Y"（把 X 删掉）。
- `zh-ex-001`（`:73`）：keep = "后接的确实是读者无法自行推出的后果"（即这段不能删），fix = "删，让事实自己说话"。
- `zh-df-004`（`:64`）：keep = "需要时效说明就写带日期的来源"（即保留并补来源），fix = "整句删"。
- `zh-st-015`（`:20`）：keep = "X 是真实误解"（即 X 不是虚设的），fix = "删虚设的X"——fix 的前提与 keep 互斥。

**期望行为**：fix 必须写成条件式（"若 X 是真实误解：压缩 Y、保留 X 的纠正；否则删 X"），或 keep 成立时 fix 不得是删除。

**修复建议**：改 `data/ai-tells.zh.json` 上述 4 条的 `fix` 文本；在 `data/README.md` 的入库规则里加一条硬约束："fix 不得与 keep 冲突——keep 成立时 fix 只能给出非删除动作"；`corpus_tool.py validate` 无法自动检查语义，可加轻量检查：`keep` 非空且 `fix` 以"删"开头时报 warning 供人工复核。

---

## A-05 法律条文长句被判 strong 结构问题；结构命中没有 keep 条件（中）

**影响**：`structure_hits` 对中文 `≥120` 字（strong）/`≥80` 字（weak）、英文 `≥45` 词（strong）直接判结构问题。合同、法规、标准条文的单句本来就常 100+ 字 / 60+ 词，这是文体规范而不是 AI 痕迹；更严重的是结构命中 `keep` 为空，报告里 keep 列是 `—`，README 第 91 行"Every entry carries a keep-condition"和最常用的"先看 keep if 再决定改"的工作流对这类命中完全不适用。

**复现**

```powershell
python "$repo\scripts\scan.py" "$T\legal-verylong.txt"
python "$repo\scripts\scan.py" "$T\english-legal.txt"
```

**实际输出**

```text
# legal-verylong.txt（一条正常合同条款）
language: zh | characters: 138 | sentences: 1
| 1 | strong | structure | `甲方应当在收到乙方书面通知后的十个工作日内……` | 超长句（≥120 字） | — | 按语义拆成两句以上 |
| 1 | weak   | structure | `……` | 的字定语堆叠（≥4） | — | 拆成短句，还原动词 |
verdict: moderate - check every strong hit in context

# english-legal.txt（一条正常合同条款）
| 1 | strong | structure | `The Supplier shall, within ten business days after receipt o` | very long sentence (80 words) | — | split at a conjunction |
| 1 | weak   | structure | `...` | of-chain (3+) | — | reorder: actor first |
```

**期望行为**：法律/合同/标准的整句应能豁免；至少结构命中要带 keep（"合同、法规、标准条文的长句是规范形态，只检查歧义，不按 AI 痕迹处理"）。

**修复建议**

1. `scan.py:257-269`：`structure_hits` 产生的 `Hit` 加上 `keep` 文本（如 `"法律、合同、标准条文；长句是规范形态"`），与正则规则的 Hit 一致地渲染。
2. 加句式豁免：以 `第.{1,6}条`、`甲方`/`乙方`、`shall`、`hereby` 开头的行，或整行无 `。` 且以 `；`/`，` 推进的法律体，降级为 weak 或不报。
3. 或将 `>=120` 的 strong 降为 weak：`data/README.md:77` 自己写了"宁可 weak，不可乱 strong"，结构检查是少数违反该原则的地方。

---

## A-06 公文套话被大面积命中并判 heavy；公文 keep 没有在判定层生效（中）

**影响**：`zh-pf-004/005/007/008/009/010/013` 等条目自带 `keep: "公文、政策原文、讲话稿"`，但扫描器不识别文体，照样全部打印；`zh-pf-013`（成效自评）还是 strong。一份 176 字的正常通知被判 `heavy`，用户按报告去改就会把公文规范用语删掉。

**复现**

```powershell
python "$repo\scripts\scan.py" "$T\gongwen.txt"
```

**实际输出**

```text
language: zh | characters: 152 | sentences: 4
strong hits: 2 (13.16 per 1000 characters) | weak hits: 14
verdict: heavy - most strong hits are probably real
| 3 | weak | platform | `高度重视`   | 公文动员语 | 公文、讲话稿、政策原文 | 非公文写具体动作与责任人 |
| 3 | weak | platform | `层层传导压力`| 公文动员语 | 公文、讲话稿、政策原文 | ... |
| 4 | weak | platform | `对标对表`   | 公文表态语 | 公文、会议纪要 | ... |
| 4 | weak | platform | `举一反三`   | 公文方法套话 | 公文、整改报告 | ... |
| 4 | weak | platform | `清单化管理` | 管理术语堆叠 | 确有台账与销号机制 | ... |
| 5 | strong | platform | `成效显著`     | 成效自评无数据 | 紧跟可核对的指标 | 写指标与前后对比 |
| 5 | strong | platform | `取得阶段性成效`| 成效自评无数据 | 紧跟可核对的指标 | ... |
```

keep 列明确写着"公文"，但 verdict 仍把这两条 strong 算进 `heavy`。

**期望行为**：识别为公文/通报/讲话稿后，`family=platform` 且 keep 含"公文"的条目应降级或折叠；`Readme` 第 107 行承认这类误报，但工具没有给用户任何处理手段。

**修复建议**

1. `scan.py:374-397`：`compute_stats` 增加"被 keep 覆盖的命中不计入 strong 计数"的通道；或增加 `--genre auto|公文|法律|学术`，让 `pick_rules` 过滤 keep 中匹配该文体的 platform 条目。
2. 至少在报告头加一行"检测到公文体例（通知/通报/各单位要）——platform 类命中默认按文体规范处理"。
3. 若不想做文体判定：把 `zh-pf-013` 从 strong 降为 weak（它需要"紧跟可核对的指标"才能定，扫描器看不到）。

---

## A-07 学术方法节误报：`研究表明` 双强命中、`结构方程模型` 被当伪学术命名（中）

**影响**：学术论文的文献综述/方法节大量使用"研究表明"（带括号引用）、"结构方程模型"、"理论框架"、"外部效度"。工具把它们分别当"模糊归因 strong"、"伪学术命名 weak"、"框架先行 weak"，一份正常方法节被判 heavy。

**复现**

```powershell
python "$repo\scripts\scan.py" "$T\academic.txt"
```

**实际输出**

```text
language: zh | characters: 161 | sentences: 5
strong hits: 2 (12.42 per 1000 characters) | weak hits: 6
verdict: heavy
| 1 | weak   | coined | `采用结构方程模型` | 伪学术命名候选 | 查得到提出者与原始文献 | ... |
| 2 | strong | stock    | `有研究表明` | 模糊归因 | 用户给了来源 | 写出作者、年份、期刊；... |
| 2 | strong | platform | `研究表明`   | 学术模糊归因 | 有具体文献（作者、年份、期刊） | 补全出处；... |
| 2 | weak | platform | `样本量有限` / `外部效度` / `有待进一步检验` | 学术免责套话 | ... |
| 3 | weak | platform | `理论框架` / `分析框架` | 框架先行 | ... |
```

`有研究表明` 与 `研究表明` 是同一 span，被 `zh-st-030` 与 `zh-pf-016` 各算一次（见 A-03）；`采用结构方程模型` 的命中文本甚至把动词"采用"捆进了"术语"。

**期望行为**：`研究表明` 后紧跟 `（作者，年份）`、`[12]`、`β=`、`p<` 等引用/统计标记时不判"模糊归因"；`结构方程模型`、`随机森林模型` 等成熟方法名不应进"伪学术命名候选"。

**修复建议**

1. `data/ai-tells.zh.json:35`（`zh-st-030`）与 `:106`（`zh-pf-016`）合并，并加负向前瞻：`(研究表明)(?!\s*[（(][^）)]{0,30}\d{4})`，或加 `(?![^。]{0,10}(β|p\s*[<=]|n\s*=|样本))`。
2. `zh-ct-003`（`:81`）改成正则捕获整词而不是带前文：`(结构方程模型|随机森林|回归模型|…白名单)` 先排除，再匹配 `[\u4e00-\u9fa5]{2,6}(模型|框架|效应|定律|飞轮|方法论|范式)`。
3. `zh-pf-018`（`:108`）的 `外部效度`、`样本量有限` 在方法/局限节是规范表述，keep 条件已写"说清哪条结论因此不成立"，建议降为 weak（已是 weak）但报告里折叠到"局限节"分组。

---

## A-08 技术文档的真实术语被判"空壳抽象词/万能动词"；term 表输出不是名词短语（中）

**影响**：控制论里的"闭环控制"、网络里的"端到端加密"、工程里的"代码复用"、SLO 里的"高可用"都被当空壳/黑话命中；term ledger 还会把"采用闭环"这种动词短语当前缀抽出，或把整句片段当术语（`服务采用闭环`、`We fit the model`、`关键抓手`），后续"五问体检"根本没法做。

**复现**

```powershell
python "$repo\scripts\scan.py" "$T\tech.txt"
python "$repo\scripts\scan.py" "$T\zh-clean.txt"
```

**实际输出**

```text
# tech.txt
weak hits: 12
| 2 | weak | coined   | `闭环`     | 空壳抽象名词 | 有稳定定义与施动者 | 换成谁对什么做了什么 |
| 2 | weak | coined   | `闭环`     | 商业模型隐喻 | 有环节定义与数据 | 写清各环节与衔接 |
| 2 | weak | coined   | `链路`     | 商业模型隐喻 | ... |
| 2 | weak | coined   | `端到端`   | 空壳抽象名词 | ... |
| 2 | weak | platform | `端到端`   | 范围大词 | ... |
| 3 | weak | platform | `稳定性保障` | 质量空话 | 有SLA或故障数据 | ... |
| 3 | weak | coined   | `复用` / `对齐` | 万能动词 | ... | （各 2 条，共 4 条） |
| 4 | weak | platform | `支持多种` | 兼容性空话 | ... |
| 4 | weak | platform | `详见下文` | 指代式说明 | ... |

## Suspect terms
| 服务采用闭环 | 2 | 复合抽象名词 | 1 |

# zh-clean.txt（正常技术段落）
| 1 | weak | coined   | `链路`   | 商业模型隐喻 | ... |
| 1 | weak | platform | `高可用` | 技术形容词堆 | ... |
| 监控体系 | 1 | 复合抽象名词 | 1 |
```

"服务采用闭环"是把 `TERM_PATTERNS` 第二项的 `[\u4e00-\u9fa5]{2,6}` 前缀贪婪吞进来的结果（英文侧同样：`We fit the model`）。

**期望行为**：术语表只输出名词短语本身（`闭环`、`端到端`）；"闭环控制/端到端加密/代码复用/链路追踪/高可用"这类有稳定技术含义的搭配应命中 keep 或直接豁免。

**修复建议**

1. `scan.py:321-325` 的 `TERM_PATTERNS[1]`：删掉 `{2,6}` 前缀，改成 `(?:体系|闭环|飞轮|抓手|底座|生态|链路|矩阵|心智|势能|引擎)` 的纯关键词匹配（`gidx=0`），让 `clean_term` 只做去噪而不是"截前缀"。
2. `scan.py:324` 英文框架名正则同理，改成显式列表 + 边界，避免 `(?:[A-Za-z][A-Za-z\-]*\s+){1,3}` 把 `We fit the` 吞进去。
3. `data/ai-tells.zh.json:84`（`zh-ct-006`）、`:208`（`zh-ct-017`）、`:99`（`zh-pf-010`）给"闭环/链路/端到端"补技术语境 keep：命中行含 `控制|加密|协议|网络|追踪|SLA` 时降级；`zh-ct-008`/`zh-pf-048` 的 `复用/对齐` 同理（`zh-pf-048` 的 keep 已写"有具体动作与产出"，但扫描器不判）。

---

## A-09 正常人类散文被 strong 命中（中）

**影响**：一段没有人称模板、没有套话的叙事散文，被判 `moderate`，其中 `说实话` 是 strong（"装坦诚"）。第一人称叙事里的"说实话"是真实语气标记，不是防御性姿态；`的` 字堆叠与 `越来越…` 也把正常文学句法当病灶。

**复现**

```powershell
python "$repo\scripts\scan.py" "$T\human.txt"
```

**实际输出**

```text
language: zh | characters: 200 | sentences: 10
strong hits: 1 (5.0 per 1000 characters) | weak hits: 2
verdict: moderate - check every strong hit in context
| 2 | strong | defensive | `说实话` | 装坦诚 | 自曝的缺点是真信息 | 删姿态，留信息 |
| 3 | weak | structure | `”他记得那个冬天的早晨的雾，还记得母亲缝的棉袄的针脚` | 的字定语堆叠（≥4） | — | 拆成短句，还原动词 |
| 3 | weak | stock | `越来越冷，` | 线性外推 | 确为单调关系 | 给数据或范围 |
```

三个问题分别对应：`zh-df-003`（`data/ai-tells.zh.json:63`）的 keep 没覆盖"叙事语体中的真实语气"；`的` 计数不看语体（文学句法本来就多 `的`）；`zh-st-064`（`:169`）的 `越[^。！？]{0,8}越[^。！？]{0,8}[，,]` 会把"越来越冷，"这种 `越来越` 当"越X越Y"。

**期望行为**：无 AI 痕迹的散文应 cleaner，或至少 `说实话` 不判 strong。

**修复建议**

1. `zh-df-003` 降为 weak，keep 增加"第一人称叙事/转述口语中的真实语气标记"。
2. `zh-st-064` 改正则为 `越(?!来)[^。！？]{1,8}越[^。！？]{1,8}[，,]`，把 `越来越` 交给 `zh-st-057`（`:162`，已覆盖"越来越+形容词"），避免同一现象两套解释。
3. `scan.py:267-269` 的 `的` 计数加下限：整句长度 `< 30` 字或段落为叙事体时不报，或把阈值从 4 提到 5。

---

## A-10 漏报：SKILL 点名要盯的中文形态没有规则；两个高频套话不命中（中）

**影响**：`skills/humanize-zh/SKILL.md:174` 明确写"中文这边真正要盯的是：`进行+名词`、`是……的` 判断句堆叠、翻译腔的前置长定语（`对于……来说，就……而言`）"，但语料库里没有任何一条正则覆盖这三种形态。扫描器对这类文本输出 `clean`。此外 `具有重要作用`、`不可否认` 这两个典型 AI 套话也不在库中。

**复现**

```powershell
python "$repo\scripts\scan.py" "$T\predicate.txt"   # 进行+名词 / 对于…来说
python "$repo\scripts\scan.py" "$T\slop.txt"        # 具有重要作用 / 不可否认
```

**实际输出**

```text
# predicate.txt
language: zh | characters: 43 | sentences: 2
strong hits: 0 ... weak hits: 0
verdict: clean - no candidates found
No matches.

# slop.txt（刻意堆满套话）
| 1 | strong | stock | `值得注意的是` | ... |
| 2 | strong | stock | `提供了有力支撑` | ... |
| 3 | strong | stock | `发挥着不可替代的作用` | ... |
| 4 | strong | stock | `综上所述` | ... |
# 第 3 行的“不可否认”、第 4 行的“具有重要作用”一条都没有
```

**期望行为**：`进行+名词` 至少 weak 命中；`具有重要作用`、`不可否认` 应在 stock 族。

**修复建议**

1. 在 `data/ai-tells.zh.json` 新增（`corpus_tool.py add`）：
   - `(对|就|把)[^。！？]{0,8}(进行|加以)(了)?[^。！？]{0,6}(优化|改造|升级|处理|分析|调整)`，weak，keep "确为动作过程表述且不能换成动词"。
   - `对于[^。！？]{0,10}(来说|而言)`，weak，keep "确需前置话题"。
   - `具有[^。！？]{0,6}(重要|关键|巨大)的?(作用|意义|价值)`，weak，keep "后文给出具体作用对象与结果"。
   - `(不可否认|无可否认|毋庸讳言)`，weak。
2. 若暂时不加规则，把 `skills/humanize-zh/SKILL.md:174` 的表述改成"以下三种形态需人工判断，扫描器不覆盖"，避免"clean"给用户错误安全感。

---

## A-11 无最小文本长度门槛，6 字文本被判 heavy（中）

**影响**：`density_verdict` 只看 strong 命中密度，不看文本长度。`值得注意的是。`（6 个汉字）得到 `166.67 per 1000 characters`、`verdict: heavy - most strong hits are probably real`，与 `skills/humanize-zh/SKILL.md:236`"短于两三句的文本不下判断"直接冲突。

**复现**

```powershell
python "$repo\scripts\scan.py" "$T\short.txt"
```

**实际输出**

```text
language: zh | characters: 6 | sentences: 1
strong hits: 1 (166.67 per 1000 characters) | weak hits: 0
verdict: heavy - most strong hits are probably real
```

**期望行为**：文本不足（如中文 `<100` 字或 `<3` 句）时 verdict 应为 `insufficient text - no verdict`，而不是 heavy/light。

**修复建议**：`scan.py:365-397` 在 `compute_stats`/`density_verdict` 前加门槛（zh：`words < 100 or sentences < 3`；en：`words < 80 or sentences < 3`）；`scan.py:404-457` 报告头同步打印 `length check: insufficient`。

---

## A-12 未闭合代码围栏把其后全文静默吞掉，报告 clean（中）

**影响**：`strip_code` 遇到 ``` 就切换状态；如果草稿里有一个没闭合的围栏（复制粘贴代码时很常见），从围栏到文件末尾的**所有正文**都被清空，扫描器报告 `clean`，用户以为没问题。报告里没有任何告警。

**复现**

```powershell
python "$repo\scripts\scan.py" "$T\unclosed-fence.txt"
```

**实际输出**

```text
language: zh | characters: 0 | sentences: 1
strong hits: 0 | weak hits: 0
verdict: clean - no candidates found
```

文件里围栏之后有两整句明显套话（`值得注意的是`、`综上所述`、`赋能闭环抓手`），全部未被扫描。

（补充：如果文件保存为带 BOM 的 UTF-8，连第一行的围栏都匹配不到，见 A-13——那是另一种失效方向。）

**期望行为**：围栏未闭合时报告 warning（例如 `warning: unterminated code fence at line 1; lines 2-4 were skipped`），并给出被跳过的行数；或把围栏后内容按正文扫描。

**修复建议**：`scan.py:209-218` 的 `strip_code` 返回 `(text, warnings)`；遍历结束后若 `in_fence` 为真，把 `"unterminated fence at line N: text after it was not scanned"` 放进 `Report.warnings` 并在 report 渲染。另外 `strip_code` 目前只处理围栏，行内反引号、缩进代码块仍会扫描，建议一并处理。

---

## A-13 非 UTF-8 文件直接抛栈；BOM 未剥离导致代码围栏失效（中）

**影响**：Windows 上大量中文 `.txt` 是 GBK/ANSI 或带 BOM 的 UTF-8（记事本默认）。GBK 文件会抛出未捕获的 `UnicodeDecodeError`（Python 完整堆栈，exit 1），与 `scan.py:15` 声明的"Exit code is always 0 unless the file cannot be read"不一致；带 BOM 的文件除了让结构命中片段以 `\ufeff` 开头、列号偏移之外，还会让 `CODE_FENCE`（`scan.py:144`，`^\s*(```|~~~)`）匹配不到第一行——**代码围栏保护直接失效，代码块里的中文被当正文扫描**。

**复现**

```powershell
python "$repo\scripts\scan.py" "$T\gbk.txt"
python "$repo\scripts\scan.py" "$T\bom.txt" | Select-String "structure"

# BOM 使围栏失效：同一段带围栏的文本，有 BOM / 无 BOM 各扫一次
$f   = ([string][char]96) * 3
$txt = $f + "python`n# 值得注意的是：这是代码注释，不是正文`n" + $f + "`n"
[System.IO.File]::WriteAllText("$T\bom-fence.txt",   $txt, (New-Object System.Text.UTF8Encoding($true)))
[System.IO.File]::WriteAllText("$T\nobom-fence.txt", $txt, (New-Object System.Text.UTF8Encoding($false)))
python "$repo\scripts\scan.py" "$T\bom-fence.txt"   | Select-String "^language:|^\| 1"
python "$repo\scripts\scan.py" "$T\nobom-fence.txt" | Select-String "^language:|^strong hits:"
```

**实际输出**

```text
File "...\scripts\scan.py", line 488, in main
    text = sys.stdin.read() if args.path == "-" else open(args.path, encoding="utf-8").read()
File "<frozen codecs>", line 325, in decode
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xb5 in position 2: invalid start byte

| 1 | weak | structure | `﻿他记得那个冬天的早晨的雾，还记得母亲缝的棉袄的针脚` | 的字定语堆叠（≥4） | ... |
（第二行命中片段开头的不可见字符即 BOM。）

# bom-fence.txt（带 BOM）
language: zh | characters: 16 | sentences: 1
| 1 | ... | （围栏内 # 值得注意的是 被当正文命中）
# nobom-fence.txt（无 BOM）
language: zh | characters: 0 | sentences: 1
strong hits: 0 | weak hits: 0
```

**期望行为**：非 UTF-8 文件给出可读错误并建议 `--encoding gbk`；读入时统一 `utf-8-sig` 剥离 BOM，保证围栏/标题/行首锚点可用。

**修复建议**

1. `scan.py:487-491`：改为 `open(..., encoding=args.encoding or "utf-8-sig")`，并 `except UnicodeDecodeError as exc:` 输出 `cannot decode <path> as utf-8; retry with --encoding gbk`，返回 2；新增 `--encoding` 参数。
2. `scan.py:460-467` 的 argparse 增加 `--encoding`。
3. `scan.py:209-218` 的 `strip_code` 在切行前先 `text = text.lstrip("\ufeff")`（作为 `utf-8-sig` 之外的兜底）；`corpus_tool.py` 读取 `data/*.json` 同样用 `utf-8-sig`。

---

## A-14 `data/` 缺失时回退 inline 表：规则 192→50，keep 条件全部为空（中）

**影响**：`scan.py` 的设计允许"复制到没有 data/ 的地方继续用"，但 inline 表是语料库的**过期子集**（zh 50 条 vs 192 条，en 31 条 vs 134 条），并且 inline 表的 `Rule.keep` 全部为空——报告里 keep 列变成 `—`，而 keep 是这套方法防误删的唯一线索。README 第 91 行、`data/README.md:41` 的核心承诺在回退模式全部失效，但除了报告头一行 `corpus: inline fallback` 外没有醒目警告。

**复现**

```powershell
$nd = Join-Path $T 'nodata'; Remove-Item -Recurse -Force $nd -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Force "$nd\scripts" | Out-Null
Copy-Item "$repo\scripts\scan.py","$repo\scripts\corpus_tool.py" "$nd\scripts\"
python "$nd\scripts\scan.py" --stats
python "$nd\scripts\scan.py" "$T\dup.txt"
python "$nd\scripts\corpus_tool.py" stats
```

**实际输出**

```text
zh: inline fallback (data/ not found)
    strong=41 weak=9 | coined=5, defensive=8, explanatory=5, stock=32
en: inline fallback (data/ not found)
    strong=26 weak=5 | coined=3, defensive=4, explanatory=3, stock=21

| 1 | strong | stock | `一言以蔽之` | 复述前文 | — | 删；结尾给新结论或行动 |
（keep 列全部是 —；且与 data 模式结果不同：inline 只有 1 条命中，data 模式是 weak+strong 两条）

python.exe : Traceback (most recent call last):
  File "...\nodata\scripts\corpus_tool.py", line 97, in cmd_stats
FileNotFoundError: ...\nodata\data\ai-tells.zh.json
```

**期望行为**：要么禁止回退、明确报"未找到 data/，扫描器不可用"；要么 inline 表与 data/ 由同一来源生成、且保留 keep。

**修复建议**

1. `scan.py:221-237`（`pick_rules`）与 `scan.py:150-181`（`load_corpus`）：`load_corpus` 返回 `None` 时不要静默改用 inline，输出显式 warning 并在 report 头用 `WARNING: corpus missing, using stale inline fallback (keep-conditions unavailable)`。
2. 把 inline 表从 `scan.py` 删除，改为在仓库根运行 `python scripts/scan.py --stats` 的安装检查；或增加 `scripts/export_inline.py` 由 JSON 生成 inline 表，避免两套规则漂移。
3. `corpus_tool.py:36-37` 的 `read_corpus` 对 `FileNotFoundError` 给出友好错误（当前直接抛栈）。

---

## A-15 `corpus_tool.py validate` 形同虚设：零宽正则、坏 ID、缺字段、`keep:"无"` 全部通过（中）

**影响**：`validate` 是 `add` 写盘前的唯一闸门，`data/README.md:50` 说它做"正则、ID、keep 校验"。实际上它**只**检查：id 是否重复、fam/sev 枚举、keep 是否非空字符串、正则能否编译、re 是否完全重复。因此：可以塞入零宽正则（每个字符位置都命中，报告爆炸）；可以缺 `fix`/`label`/`show`；id 可写成 `bogus-id`、可与 fam 前缀不一致；`--keep "无"` 能通过"keep 必填"。

**复现**

```powershell
$C = Join-Path $T 'repo-copy'; Remove-Item -Recurse -Force $C -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Force $C | Out-Null
Copy-Item -Recurse "$repo\scripts" $C; Copy-Item -Recurse "$repo\data" $C

# 1) 零宽正则被接受，validate 通过
python "$C\scripts\corpus_tool.py" add --lang zh --re "(?:)" --label zero-width --keep x --fix y
python "$C\scripts\corpus_tool.py" validate
"可疑的句子。" | Set-Content "$C\tiny.txt" -Encoding utf8
python "$C\scripts\scan.py" "$C\tiny.txt"

# 2) keep="无" 被接受
python "$C\scripts\corpus_tool.py" add --lang zh --re "(测试占位短语)" --label placeholder --keep "无" --fix f

# 3) 改坏首条（坏 ID、ID/fam 不一致、删掉 fix/label/show）后 validate 仍 OK
@'
import json, pathlib
p = pathlib.Path(r"REPO-COPY\data\ai-tells.zh.json".replace("REPO-COPY", r"C:\Users\Lenovo\AppData\Local\Temp\hws-review\repo-copy"))
d = json.loads(p.read_text(encoding="utf-8"))
e = d["entries"][0]; e["id"] = "bogus-id"; e["fam"] = "defensive"
[e.pop(k, None) for k in ("fix", "label", "show")]
p.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
'@ | python -
python "$C\scripts\corpus_tool.py" validate
```

**实际输出**

```text
added zh-st-076 to data/ai-tells.zh.json; corpus now 193 entries
zh: OK
en: OK
language: zh | characters: 5 | sentences: 1
weak hits: 8
| 1 | weak | stock | `` | zero-width | x | y |     ← 6 个汉字报了 8 条（每个位置一条）

added zh-st-076 ...; corpus now 193 entries        ← 零宽正则通过
added zh-st-077 ...; corpus now 194 entries        ← keep="无" 通过

=== validate after schema mutations ===
zh: OK
en: OK
```

**期望行为**：`add`/`validate` 拒绝能匹配空串的正则、拒绝缺字段、拒绝不符合 `^(zh|en)-(st|df|ex|ct|pf)-\d{3}$` 的 id、拒绝 id 前缀与 fam 不一致、拒绝 `keep` 为 `无/never/none`（或要求改写）。

**修复建议**（`scripts/corpus_tool.py`）

1. `validate_payload`（:50-70）增加：
   - `pat = re.compile(e["re"])`，若 `pat.search("")` 不为 `None` 则 `problems.append(...zero-width pattern...)`（`(?:)`、`.*`、`a*` 都能被这条拦住）；
   - 必填字段 `id/re/label/keep/fix` 非空（`show` 可选）；
   - `re.fullmatch(r"(zh|en)-(st|df|ex|ct|pf)-\d{3}", eid)`，且分组 2 与 `FAM_CODE[fam]` 一致；
   - `keep.strip() in {"无", "never", "none", "n/a"}` 报错。
2. `cmd_add`（:124-160）在插入前用同一套校验（现在插入后才 validate）；`scan.py:298-305` 再保险：`re.finditer` 循环里 `if m.group(0) == "": continue`。

---

## A-16 README 声称的 false-positive guards 在扫描器中未实现（中）

**影响**：`README.md:42` 写"False-positive guards: quotations, titles, discussed-as-a-word passages, genre conventions, the writer's own sample"，`skills/humanize-zh/SKILL.md:230-236` 也列了"引文、标题、专名、法规条文……以及讨论某个词本身的段落，里面出现候选信号不算问题"。但 `scan.py` 里**没有任何一处在检测**引文、标题、讨论词或文体（`grep` 不到 keyword 逻辑，`scan()` 只有 `strip_code`）。实际后果是：一篇讨论"赋能"这个词的文章，会被当作"使用了空壳词"。

**复现**

```powershell
python "$repo\scripts\scan.py" "$T\discussed-word.txt"
```

**实际输出**

```text
| 1 | weak | coined | `赋能` | 万能动词 | 有具体对象和结果 | 换成具体动作 |
| 2 | weak | coined | `闭环` | 空壳抽象名词 | 有稳定定义与施动者 | ... |
| 2 | weak | coined | `闭环` | 商业模型隐喻 | ... |

## Suspect terms (run the five tests)
| 赋能 | 1 | 引号名词 | 1 |
| 闭环 | 2 | 引号名词 | 1 |
```

两句话都是在**批评**这两个词（"我最近戒掉了'赋能'这个词"），按 SKILL §十应豁免，实际全被列为候选术语。

**期望行为**：命中所在行若为 Markdown 标题（`#`）、引号内且后接"这个词/这种说法/这个词本身"、或处于"我戒掉了 X"句式，应标 `quoted/discussed` 并降级或跳过；至少 keep 列要提示这一点。

**修复建议**

1. `scan.py:290-318` 的 `scan()` 增加上下文判定：对每个命中检查 `line` 前缀（`^#{1,6}\s`）、前后 20 字窗口中的 `这个词|这种说法|所谓.*这个词|戒掉|不再用`，命中则 `severity="weak"` 并加 `keep="讨论用词本身，不是使用它"`。
2. 引文：成对引号 `“[^”]{1,40}”` 内的命中标记 `quoted`。
3. 若短期内不实现，`README.md:42` 应删掉这条承诺（与 `README.md:107` 的 Limits 一致），否则用户会把扫描结果当"已过 guard"。

---

## A-17 空文件被判成 `language: en`（低）

**影响**：`guess_lang("")` → `cjk = 0`，`0 > len("") * 0.08` 为 False → `en`。空文件/纯空白文件显示 `language: en`，虽然 verdict 是 clean，但对中文用户是误导，也说明语言判定没有"未知"状态。

**复现**

```powershell
python "$repo\scripts\scan.py" "$T\empty.txt"
```

**实际输出**

```text
language: en | words: 0 | sentences: 1
verdict: clean - no candidates found
corpus: data/ai-tells.en.json v1.0.0 (134 entries)
```

（`sentences: 1` 也是 `compute_stats` 里 `or 1` 的兜底值。）

**期望行为**：无文本时 `language: unknown`，不加载任何规则，并提示"no text"。

**修复建议**：`scan.py:240-242` 的 `guess_lang` 在 `text.strip() == ""` 时返回 `"unknown"`；`scan.py:493` 与 `scan.py:290` 处理该值；`compute_stats` 对空文本返回 `sentences: 0`。

---

## 附录 A：测试通过项（没有问题，供对照）

以下均实测通过，说明这些边界行为是好的：

```powershell
python "$repo\scripts\scan.py" "$T\empty.txt"                 # exit 0，clean
python "$repo\scripts\scan.py" "$T\codeonly.txt"              # 纯代码块文件：0 命中（strip_code 生效，正常）
python "$repo\scripts\scan.py" "$T\does-not-exist.txt"        # exit 1，友好错误（不抛栈）
python "$repo\scripts\scan.py"                                # exit 2，"a path is required unless --stats is used"
python "$repo\scripts\scan.py" "$repo\scripts\data"           # 目录：exit 1，cannot read（无崩溃）
Get-Content -Raw "$T\slop.txt" | python "$repo\scripts\scan.py" -   # stdin 正常
python "$repo\scripts\scan.py" "$T\slop.txt" --json           # JSON 可解析，字段完整
python "$repo\scripts\scan.py" "$T\slop.txt" --no-terms       # term 段被省略
python "$repo\scripts\scan.py" --stats                        # zh 192 / en 134，无 invalid entries
python "$repo\scripts\corpus_tool.py" validate                # 现有语料 OK
```

- **360KB 单行**（114,000 个汉字、无换行）：`scan` 0.24s 完成、不崩溃、产出 1 strong + 1 weak（`超长句`/`的字定语堆叠`）。
- **`add` 传入非法正则** `--re "("`：exit 2，文件 hash 不变（安全失败）；**重复正则**：exit 1，拒绝写入。
- **代码围栏**内的 `值得注意的是` 被正确跳过（`codeonly.txt` 0 命中）。

## 附录 B：覆盖与局限

- 本次只测了 `scripts/scan.py`、`scripts/corpus_tool.py`、`data/*.json` 与两份 `SKILL.md` 的相关声明；未评估四个 reference 文件与 ATTRIBUTION 的准确性（属其他评审线）。
- 所有结论基于本机 Python 3.13.12 / Windows；`--re ""` 在 PowerShell 下会被吞掉空参数，A-15 用 `(?:)` 等价复现；在 bash 下 `--re ""` 同样能进入 `re.compile`，结论不变。
- 报告未包含任何"未复现、仅推测"条目。
