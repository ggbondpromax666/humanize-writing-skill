# Defensive writing: identification and repair

> **Source**: adapted from [blader/humanizer](https://github.com/blader/humanizer) (§5, §9) and [no-ai-slop](https://github.com/petergyang/no-ai-slop), with the six tests rewritten from the Chinese edition. Full mapping: [ATTRIBUTION.md](../../../ATTRIBUTION.md).

Read this when "cut the defenses" is unclear.

Defensive writing is prose written **to pre-empt an objection** rather than to inform: unearned self-deprecation, repeated disclaimers, stacked hedging, strawman rebuttals, process narration, reassurance.

It buries the central claim under qualifiers, balance sentences, and disclaimers. The opposite of defensive is **not** "delete every qualifier": necessary boundaries (scope, conditions, risks, unverified items) are what let a reader use a conclusion correctly. Deleting them is distortion.

## The hedging paradox

The problem with AI text is **not** that it qualifies in-sentence. It is that it:

- piles up **meta-level disclaimers with no referent** ("for reference only", "may not be exhaustive"), while
- **avoiding in-sentence specifics** ("on two datasets", "sample from a single school").

So blanket-deleting hedges makes text *more* AI-like, turns measurements into universals, and turns guesses into assertions.

---

## 1. Six tests

Ask in order. Any test that answers "the reader loses something" means you may not delete; you may only make it precise.

### 1. Deletion test
> Delete the sentence. What does the reader lose?

A fact, scope, stance, consequence, or next step → keep and sharpen. Nothing → filler.

### 2. Function test
> Does it help the reader use the conclusion, or does it argue the other side for them and lower the piece's value?

Keep the first, cut the second. Judge by **the sentence's role in place**, not by a word list. "May" and "to some extent" are not wrong in themselves.

### 3. Five-part consequence test
Does removing it affect the reader's judgment of:
- whether the claim holds?
- how to read the evidence?
- the scope of the conclusion?
- what the method was?
- whether they can use the result?

Any yes → keep.

### 4. Source test
- **Source-tagging qualifiers** ("according to the registrar's notice", "per the venue's August page") → keep.
- **Stance-avoiding qualifiers** ("to some extent", "in a sense", three "perhaps" with no object) → cut.

### 5. Position test
State a limit **once**, where the reader needs it. In an abstract, opener, or conclusion it is high-impact; in a limitations section it is normal. Do not move every limit into a limitations section, and do not repeat one in every paragraph.

### 6. Information-strength layers
Tag each claim and match the wording:

| Layer | Wording | Example |
|---|---|---|
| Directly shown | statement | "The classroom library logged 143 loans last month." |
| Reasonable inference | "so", "suggests" | "Loans cluster at lunch, so lunch-hour access matters most." |
| Unverified | "not yet", "still" | "Whether other classes behave the same has not been tested." |
| Necessary boundary | "This paper only covers…" | "This paper covers classroom libraries only." |

**Defensive filler = a sentence belonging to no layer, expressing only "I might not be good enough."**

---

## 2. Cut list

| Type | Shape | Action |
|---|---|---|
| Unearned self-deprecation | "still has many shortcomings", "my two cents", "a modest attempt" | delete; convert real limits into specific scope |
| Repeated disclaimers | "just my opinion" at every section end; the same limit in abstract, intro, and conclusion | state once, in place |
| Strawman rebuttal | "This is not to say that X is worthless…" when nobody argued it | delete; if a real claim hides inside, state it |
| Stance vacuum | "everything has pros and cons", "it depends", "both opportunities and challenges" | name the conditions or state the judgment; otherwise delete |
| Fake balance | "on one hand it saves time, on the other it demands new skills", both vague | land both sides in evidence, or keep only the supported side |
| Stacked hedges | "could potentially to some degree have an effect" | collapse to one layer; say where the uncertainty comes from |
| Performed candor | "let me be honest", "I'll say this even if it costs me" | delete the posture; keep the disclosed weakness |
| Knowledge-cutoff disclaimers | "as of my last update", "public information is limited" | delete the whole sentence; never guess after admitting the gap |
| Process narration / self-assurance | "compiled by AI", "unverified items are flagged", "your meaning has been preserved" | delete; keep only what changes the reader's next action |
| Reassurance / direction-granting | "you're on the right track", "don't worry at all", "a great start" | delete, or "the available information does not support a judgment" |
| Self-diminish then inflate | "although this is only a preliminary exploration, it is significant" | delete the first half |
| Answering nobody | rebutting an objection no reader would raise | delete |

### Must keep

Scope statements; method and sample limitations; distinctions that carry the argument ("this is not a refund, it is a voided authorization"); evidence-backed qualifications; legal / safety / ethics notices; genuine concessions inside a request; real corrections; source tags; genuine unfinished work ("we haven't measured latency yet"); genre-required sections (limitations, "problems remaining"); date and sample ranges.

---

## 3. Repair is not only deletion

- **Positive scope**: "we do not claim these cases represent all cities" → "this paper analyzes 11 cases across four cities, 2023–2025."
- **Name the source of uncertainty**: "this may to some extent indicate…" → "the evidence supports this explanation, but it does not support estimating a population effect."
- **Condition plus claim**: "arguably effective" → "with a single class, mean submission time fell from three days to one."
- **Dated source instead of disclaimer**: "hours are subject to change" → "hours are from the venue's August notice; check the site on the day."
- **Make the constraint a capability** (fact unchanged, direction flipped): "this method runs only on a single GPU" → "this method runs on a single GPU." (Only if true, and do not hide "multi-GPU untested.")
- **State the advantage**: the other half of anti-defensive work. Say under what conditions, why, and what problem it solved.
- **No new boilerplate to replace old boilerplate**: do not follow "has limitations" with "the future is promising."

---

## 4. Symmetry check: do not make the writer more confident

The most common failure is over-cutting. These are **distortions**, not de-AI-ing:

| Do not turn | Into |
|---|---|
| "most students finished in week two" | "students finished in week two" |
| "may improve" | "improves" |
| "this may be because" | "this is because" |
| "we disagree" | "we have reservations" |
| "not measured yet, so we wait" | "results look good" |
| deleting "cross-domain effects untested" because it "looks cautious" | — |

Ask three questions after editing:

1. Did I delete a fact that affects whether the conclusion holds?
2. Did I add a claim the source does not make?
3. Did I change more than this problem required?

---

## 5. Boundary with explanatory bloat

| | Defensive | Explanatory |
|---|---|---|
| Motive | pre-empt criticism | pre-supply context |
| Shape | self-deprecation, disclaimers, hedges, fake balance | restatement, re-explaining, metadiscourse, over-definition |
| Test | does the reader lose **stance / scope / consequence**? | does the reader lose **new information**? |
| Fix | make precise, or delete | delete, or restate as fact |

They co-occur: "It's worth noting that this study may, to some extent, suggest… (for reference only)" — the front half is explanatory metadiscourse, the back half defensive hedging.

---

## 6. Audit output

Per finding: location, exact snippet (≤20 words), problem in plain language, fix direction, and one line on how the fix changes the reader's judgment.

Taxonomy names are for your reasoning only; do not show them to the user.
