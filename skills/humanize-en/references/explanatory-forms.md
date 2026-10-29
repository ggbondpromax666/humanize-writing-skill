# Explanatory bloat: identification and repair

> **Source**: original to this project, informed by [humanizer](https://github.com/blader/humanizer) §26 and [no-ai-slop](https://github.com/petergyang/no-ai-slop). See [ATTRIBUTION.md](../../../ATTRIBUTION.md).

Read this when "cut the explanation" is unclear.

Explanatory bloat is prose the reader **did not ask for and does not gain from**. It reads smoothly and logically, which is why it survives every sentence-level cleanup. It is also the most stable structural signature of AI text: a model writes for the widest possible reader, so it assumes the reader knows nothing.

**Core test: does the reader already have this information?**

- Yes → explaining it adds nothing. Cut.
- No → keep it, but explain once, where the reader needs it.

Explanation is not the problem. Onboarding docs, teaching material, and science writing need it. The problems are **re-explaining to a reader who already knows** and **using explanation in place of argument**.

---

## 1. Two families, thirteen shapes

### Family A — Restatement (the reader already read it)

| # | Shape | Test | Fix |
|---|---|---|---|
| 1 | **Synonym restatement**: "in other words", "put simply", "that is to say", followed by the same content | do the two sentences carry the same information? | keep the clearer version, delete the frame |
| 2 | **False precision**: "more precisely", "specifically", with no added precision | is the second version more specific (number, scope, condition)? | if not, delete |
| 3 | **Back-reference**: "as mentioned earlier", "as we saw above" | long document, one use allowed | delete the rest, or point specifically ("the three conditions in §2") |
| 4 | **Conclusion–explanation–conclusion**: claim, then explanation, then the claim again | is it the same sentence three times? | keep one, unless the middle contains real argument |

**A disguised variant**: restating the same idea as a rhetorical triad plus uplift ("In the moment it tested composure; afterward it offered a chance for reflection"). That is not explanation; it is the same abstraction promoted one level. Delete the sentence.

### Family B — Over-supply (the reader does not need it)

| # | Shape | Test | Fix |
|---|---|---|---|
| 5 | **Context rebuild**: re-narrating background in a reply or a doc for participants | is the reader a participant? | lead with the decision; keep one fact they lack |
| 6 | **Definition habit**: defining common words ("efficiency means getting more output from less input") | does the reader need it? | delete; keep one definition for a technical term at first use |
| 7 | **Causal padding**: one cause told three times ("this is because… which in turn leads to… so therefore…") | is the chain really three links? | compress to one sentence |
| 8 | **Step inflation**: one action split into three steps | does each step carry independent information? | merge |
| 9 | **Parenthetical stuffing**: three "(including…)", "(i.e.,…)", "(such as…)" in one paragraph | is each necessary? | expand the term's first use, cut the rest |

### Family C — Metadiscourse (writing about the document)

| # | Shape | Test | Fix |
|---|---|---|---|
| 10 | **Navigation preview**: "this article covers three things", "in this section we will…" | do the headings already say it? | delete |
| 11 | **Self-answered question**: "So what's the problem? The problem is…" | speaking-script context only | merge into a statement |
| 12 | **Process narration**: "here's a quick example to illustrate", "I went and checked the docs" | does it change what the reader does? | delete; method notes belong in a method section |

### Family D — Significance explanation (the most AI-like)

| # | Shape | Test | Fix |
|---|---|---|---|
| 13 | **Judgment on the reader's behalf**: "this means… is of great value", "this clearly demonstrates…" | do the facts already let the reader judge? | delete; let facts carry it |
| 14 | **Explaining the example**: giving an example, then "what this shows is…" | is the example self-evident? | delete the gloss unless the example is ambiguous |
| 15 | **Section-end uplift**: a fact, then "this provides a foundation for…" | does the closer add information? | end on the concrete result |

> Family D vs. defensive writing: D explains **significance** (how much this matters); defensive explains **stance** (I might be wrong).

---

## 2. Keep conditions (six)

1. The reader genuinely lacks the background — judge by **who the reader is**, not by the writer's habit.
2. A technical term at first use: one sentence of definition; not again.
3. **Mechanism explanation** ("why this happens") that the reader needs in order to act — as opposed to significance explanation ("how much this matters").
4. Operational detail that changes the reader's next step.
5. Failure-mode warnings: where intuition leads people wrong.
6. Genre: teaching material, onboarding, FAQ, and science writing are explanatory by design.

Mnemonic: **keep mechanism, cut significance; keep what the reader lacks, cut what they have.**

---

## 3. Four repair moves

**1. Keep the content, delete the frame**
> Before: In other words, what we're really doing is using a lower cost to accomplish the same thing.
> After: We accomplished the same thing at a lower cost.

**2. Lead with the decision**
> Before: Due to a combination of historical factors, organizational restructuring, and staffing changes, we ultimately arrived at the decision to pause the project.
> After: We paused the project. The lead engineer left, and the person who took over does not know the system.

**3. Replace significance with consequence**
> Before: This adjustment is significant, marking a shift in how the organization manages work.
> After: After the change, approval went from three levels to one and took one day instead of five.

**4. Merge repeated explanations**
> Before: "Low-code" means building with little code. That is, you don't write much code. Put simply, the amount of code you write is smaller.
> After: Low-code means building by dragging components instead of writing the interface by hand.

---

## 4. Density diagnosis (audit mode)

- **Restatement ratio**: restatement sentences ÷ total sentences. Above 10% = the text is talking to itself.
- **Metadiscourse count**: navigation, preview, process narration. Above two per thousand words needs work.
- **Uplift closers**: share of paragraphs ending in a significance sentence. Above 50% = every paragraph is reaching.
- **Example gloss ratio**: explanation sentences after an example ÷ sentences of the example. Above 1 = the gloss is longer than the example.

These are not hard thresholds; they give "this feels wordy" something checkable.

---

## 5. Overlap with stock formulas

These are both explanatory and formulaic. Handle them as explanatory first (ask whether the reader already has the information), then as formulaic:

- in other words / that is to say / put simply / specifically
- it's worth noting / it's important to note
- this article will / below we look at
- this means / this shows / it follows that

Two gates, in order: **does the reader need this information → can the frame be deleted.** Only delete when both pass.

---

## 6. Audit output

Per finding: location, exact snippet, family, why the reader already has (or does not need) the information, fix direction.

```
Para 4, sentence 2 | "In other words, the mechanism is about making information flow more smoothly."
Family: A-1 synonym restatement
Reason: the previous sentence already says feedback returns directly to the backlog
Fix: delete the whole sentence
```
