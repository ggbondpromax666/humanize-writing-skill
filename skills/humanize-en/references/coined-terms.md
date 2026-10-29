# Coined-term audit (English)

> **Source**: original framework; inspired by [humanizer](https://github.com/blader/humanizer) §10, [Humanizer-zh](https://github.com/op7418/Humanizer-zh) §10, and [no-ai-slop](https://github.com/petergyang/no-ai-slop) (weasel attribution). See [ATTRIBUTION.md](https://github.com/ggbondpromax666/humanize-writing-skill/blob/main/ATTRIBUTION.md).

The most dangerous AI tell is not empty prose. It is **inventing a term that sounds technical and then using it as the argument.** Once the reader accepts the word, every claim built on it rests on nothing.

This class is worse than the others because:

- it reads the **most** expert-like and is hardest for a non-specialist to catch;
- it **propagates**: one fabricated concept can contaminate a whole team's documents;
- it usually arrives with **fake provenance** ("a recent industry report", "widely adopted"), dressing fabrication as citation.

**Rule: never invent a source for the writer, and never delete a term the writer genuinely owns.** When unsure, flag it and let the author decide.

---

## 1. Seven shapes

| # | Shape | Examples | Signature | Default |
|---|---|---|---|---|
| 1 | **Empty abstraction** | value anchor, growth flywheel, operating model, synergy layer, hyper-automation fabric | no agent, no object, no measurable result | replace with who did what; if impossible, delete |
| 2 | **Concept mashup** | AI-native data-driven ecosystem, full-stack synergistic enablement | two buzzwords welded; each survives alone, the compound is emptier | split; keep the half with evidence |
| 3 | **Fake academic naming** | "the SCALE framework", "the three-layer maturity model", "the X effect" | academic shape, no author, no citation, no validation | untraceable → flag, do not rewrite |
| 4 | **Fake institution / report / standard** | "a recent industry report shows", "the Global X Council standard", "the Y White Paper" | vague institution; suspiciously tidy report title | delete or mark `[needs source]`; never supply one |
| 5 | **Un-expanded acronym** | "our 3E model", no expansion at first use | reader cannot decode it | expand at first use; if it cannot be expanded, it is empty |
| 6 | **Term drift** | "entropy" for "messiness", "paradigm" for "approach", "algorithm" for "method" | real term, wrong sense | restore the real sense, or use a plain word |
| 7 | **Fake proper nouns** | invented products, companies, people, case subjects | used as evidence or endorsement | delete; ask the author for a real case |

**Added judgment counts as fabrication.** Pairing a term with "proven", "widely adopted", or "industry-standard" upgrades a guess into a fact.

---

## 2. Five tests

Ask in order. Failing any one requires action.

### 1. Definition
> Can you define it in one sentence **without circularity**?

- Pass: "'Closed loop' means feedback goes back into the next planning round."
- Fail: "'Closed loop' means the process is closed-loop."

### 2. Provenance
> Who proposed it, in what paper, standard, product, and year?

- Pass: "'Double diamond' was published by the UK Design Council in 2005."
- Fail: "the double diamond that has emerged in recent years" — no "who".

### 3. Boundary
> Can you name something that is **not** it?

- Pass: "This method needs historical data; new products with no data do not qualify."
- Fail: "It is a new paradigm." Everything qualifies, so nothing does.

### 4. Substitution
> Replace it with plain words. Does information disappear?

- Only gravitas disappears → it has no content.
- Discriminating power disappears (it separated two cases) → it is a real concept; keep it.

### 5. Prediction
> What does it let you distinguish or predict?

- Pass: "'Funnel conversion rate' separates a traffic problem from a landing-page problem."
- Fail: "'Growth flywheel' shows the business is spinning." It distinguishes nothing.

---

## 3. Three origins, three treatments

| Origin | Test | Treatment |
|---|---|---|
| **Established term** | textbook, standard, common industry usage, stable definition | keep; define once at first use; do not delete just because it sounds like an AI word |
| **Author-coined but useful** | the author can state definition, boundary, and why a new word is needed | keep; require a one-sentence definition at first use and consistent use after |
| **Model-fabricated** | untraceable, circular definition, no boundary, fake provenance | disposition ladder below |

**Edge case**: author-coined but the author cannot define it → treat as empty abstraction, and note "this term needs a definition."

---

## 4. Disposition ladder

| Finding | Action | Mark |
|---|---|---|
| Real term with definition | keep; add a definition or expansion at first use | none |
| Real idea, vague wording | replace with concrete actions and objects | none |
| No content, only gravitas | delete the word, keep the concrete sentence | none |
| Plausible but untraceable | keep the sentence | `[verify: origin]` |
| Fake institution, report, or statistic | delete, or downgrade to "the author argues" | `[needs source]` |
| Fabricated proper noun or case | delete | list removals in the note |

**Three things not to do**:

1. Do not replace it with a sibling coinage (delete "leverage", do not add "value-add").
2. Do not flatten a real technical term into plain speech and cost expert readers their precision.
3. Do not go find a "looks about right" source to attach.

---

## 5. Verification

### Offline
1. How many times does the term appear? Is its sense stable? (Inconsistent = drift.)
2. Is there a definition, expansion, or citation at first use?
3. Is it immediately followed by "studies show" or "data suggests"? (High-risk slot.)
4. Replace it with plain words and reread: does the argument collapse? If so, the argument was resting on the word.

### Online (when search is available)
1. Search the exact term in quotes; look for independent sources, not reprints of the same draft.
2. Search "proposer + year + original paper" to confirm it is not second-hand.
3. Search the institution and report name; watch for same-name institutions and misattribution.
4. Check a field review or textbook, not a single encyclopedia page.

**Not finding it does not prove fabrication.** It may be internal, new, or non-English. Flag it; do not delete on absence alone.

---

## 6. Term ledger (required in audit mode)

```
| # | Term | First location | Type | Definition | Provenance | Boundary | Verdict | Action |
|---|------|---------------|------|------------|------------|----------|---------|--------|
| 1 | growth flywheel | para 1 | empty abstraction | none | none | none | empty | delete; state what grew |
| 2 | double diamond | para 2 | real term | yes | UK Design Council, 2005 | yes | keep | cite at first use |
| 3 | "recent industry report" | para 4 | fake institution | — | not found | — | fabricated | delete; mark [needs source] |
```

If there are no suspect terms, say "none found." The ledger belongs in the note after the draft, not in the prose.

---

## 7. Common false positives (leave these alone)

- **Standard terms**: GDP, ISO 9001, SLA, conversion rate, p-value.
- **Stable academic concepts**: opportunity cost, significance level, inter-rater reliability.
- **Real proper nouns**: products, companies, people, even when abbreviated.
- **The organization's internal vocabulary**: fine if the author can explain it and defines it once.
- **Quoted policy language**: leave it verbatim.

The test is not "does it sound like an AI word" but **definition, provenance, boundary**.

---

## 8. Before / after

**1 — Empty abstraction**

> Before: We built a **full-stack, AI-native enablement fabric** that delivers **end-to-end value across the entire lifecycle**.
>
> After: A request is routed to the on-call engineer automatically; the result is logged and reviewed at the next morning standup. Mean handling time fell from 26 hours to 9 hours in the first quarter.

Three words deleted, actions and numbers added (**numbers must come from the material**; if they do not exist, do not invent them).

**2 — Fake framework**

> Before: Grounded in the **SCALE three-layer maturity model**, we restructured onboarding.
>
> After: Onboarding runs in three steps: why the change matters, one supervised attempt, then a review of what broke. We assembled that sequence ourselves; it is not a published model.

If the author does have a source, cite it. If not, do not borrow academic clothing.

**3 — Term drift**

> Before: The proposal has high **entropy** and needs to be de-entropied.
>
> After: The proposal touches too many teams. Interfaces are undefined, so one change requires coordinating five people.

**4 — Fake institution**

> Before: **A leading research institute's 2026 AI in Education White Paper** found that 83% of teachers already use AI in class.
>
> After: (Delete. In the note: "This figure has no source. If you have one, send it and I'll restore it.")

---

## 9. One-line test

**If a term can be replaced by a concrete sentence without losing information, it should not stand alone.**
