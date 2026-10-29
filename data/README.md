# AI 痕迹语料库 / AI-tell corpus

两份结构化数据文件，`scripts/scan.py` 从这里加载规则：

```
data/ai-tells.zh.json    中文（stock / defensive / explanatory / coined / platform）
data/ai-tells.en.json    英文（同上）
```

**它仍然不是"AI 语料库"。** 这里没有从模型输出里抓取的大规模文本，也没有统计标注。它是**人工维护的候选信号库**：每条是一段正则 + 一个保留条件。见 [ATTRIBUTION.md](../ATTRIBUTION.md)。

## 结构

```json
{
  "version": "1.0.0",
  "lang": "zh",
  "entries": [
    {
      "id": "zh-st-001",
      "re": "在当今.{0,12}(时代|社会|背景下|大环境中)",
      "show": "在当今……的时代",
      "fam": "stock",
      "sev": "strong",
      "label": "宏大开场",
      "keep": "背景本身是论证对象",
      "fix": "直接从问题、场景或判断开始"
    }
  ]
}
```

| 字段 | 必填 | 说明 |
|---|---|---|
| `id` | 是 | 稳定 ID，格式 `语言-家族-序号`。不要复用已删除的 ID |
| `re` | 是 | Python 正则。加载时会编译校验，写错会跳过并在 `--stats` 里报告 |
| `show` | 否 | 人类可读形态，用于文档与评审 |
| `fam` | 是 | `stock`｜`defensive`｜`explanatory`｜`coined`｜`platform` |
| `sev` | 是 | `strong`（见一处就处理）｜`weak`（成片出现才处理） |
| `label` | 是 | 问题类型名，用于报告 |
| `keep` | **是** | **保留条件**。没有这一条，就不该进库——它是防止误删的唯一线索 |
| `fix` | 是 | 改法方向，一句话 |

## 怎么扩充

**推荐用工具，不要手改 JSON：**

```bash
python scripts/corpus_tool.py stats                 # 条数、家族分布
python scripts/corpus_tool.py validate              # 正则、ID、keep 校验
python scripts/corpus_tool.py add --lang zh --fam stock --sev weak \
    --re "(不是.{1,20}[，,]\\s*而是)" --label "翻案对比" \
    --keep "X 是真实误解，读者会因此做不同的事" --fix "删虚设的X，直接写Y"
python scripts/corpus_tool.py observe --lang zh --text "新看到的句式" --note "为什么可疑"
```

`add` 会：自动分配下一个 ID → 只插入一行（其余格式不动）→ 递增 minor 版本 → 写前先 validate，失败就拒绝写入。
`observe` 把拿不准的形态记到 `data/observed.zh.md`，攒够同类再转成条目。

手改的话，按下面来：

1. 挑一个家族，复制一条现有条目。
2. 写正则时优先**功能形态**，不要堆词表：`(值得注意的是|需要指出的是)` 比单列十个词更稳。
3. `keep` 必须写具体——写不出保留条件，说明这条规则还不成熟。
4. 新增后自检：

```bash
python scripts/corpus_tool.py validate
python scripts/scan.py test.md          # 命中是否合理
```

5. 同一条信号不要在中英两份里重复定义不同的正则；保持语义对齐、正则按语言各写。

## 两条硬约束

- **强信号不准随便加**：`strong` 意味着"见一处就能改"。加之前先想清楚它在哪些文体里是规范（公文、法律、期刊）。
- **正则不准过宽**：`(是)` 这种级别会命中一切。宁可漏，不可滥；宁可 `weak`，不可乱 `strong`。

## 版本

`add` 会自动递增 minor 版本。手改时请自行递增，并在提交信息里写清新增/删除的条目数。扫描报告会打印当前版本。
