---
name: humanize-en
description: Edit or audit English prose for AI tells - defensive writing (unearned self-deprecation, repeated disclaimers, stacked hedging, arguments with no one), explanatory bloat (restatement, re-explaining known context, metadiscourse, over-definition), stock AI formulas ("not X but Y", "it's worth noting", "in today's fast-paced world", "plays a crucial role"), coined terms (empty abstractions, invented frameworks, fake institutions, unexpanded acronyms), convoluted long sentences (45+ words, three or more stacked subordinate clauses, of-chains), and template structure - while locking down facts, certainty, and the writer's voice. Use when the user says "de-AI this", "sounds like ChatGPT", "cut the slop", "make it sound human", "remove the hedging", "split these sentences", "check for made-up terms", "is this AI-written", or asks to edit, tighten, audit, or review prose. English only; no translation, no pure summarizing.
license: MIT
metadata:
  version: "1.0.0"
  language: en
---

# Humanize Writing (English)

Write to one reader about one thing. Decide what the reader should understand, believe, or do, then choose what stays.

**The goal is not "sound human." It is "be clear and credible to this reader."** Do not try to beat AI detectors, do not judge authorship, do not output an "AI score." Detectors guess. Named patterns are evidence a reader can check.

## Four hard limits

1. **Add no facts**: no number, date, name, title, quote, source, mechanism, result, or promise that is not in the source.
2. **Lose no information**: every factual claim must be traceable to the original. If you cannot point to it, revert the edit.
3. **Do not change certainty**: may ≠ will, involved ≠ responsible, correlated ≠ caused, planned ≠ done, testing ≠ tested.
4. **Do not make the writer sound more confident**: real hesitation, unfinished work, and mixed feelings stay. Cut only *unearned* self-undermining.

Priority when rules collide: **facts and promises > necessary boundaries and instructions > the user's explicit request > the writer's voice and genre > de-templating**.

## Seven families of AI tells

| # | Family | Typical shape | Detail |
|---|---|---|---|
| A | Defensive writing | "just my two cents", "still has limitations", "there are pros and cons", hedging with no referent | [references/defensive-forms.md](references/defensive-forms.md) |
| B | Explanatory bloat | "in other words", re-explaining known context, decision buried last, metadiscourse | [references/explanatory-forms.md](references/explanatory-forms.md) |
| C | Stock formulas | "not X but Y", "it's worth noting", "in today's fast-paced world", "plays a crucial role" | [references/stock-phrases.md](references/stock-phrases.md) |
| D | Coined terms | empty abstractions, concept mashups, fake frameworks, fake institutions, unexpanded acronyms | [references/coined-terms.md](references/coined-terms.md) |
| E | Template structure | definition → three parts → uplift; identical paragraph shapes; paired headings | §5 |
| F | Formatting residue | chatbot wrappers, markdown debris, bold decoration, emoji templates | §6 |
| G | Sentence bloat | 45+ word sentences, 3+ stacked subordinate clauses, `-ing` chains, `of` chains | §6.5 |

A–D are **candidate signal lists, not banned-word lists.** Every row carries a keep-condition. The most common failure is not missing a tell; it is deleting a sentence that was doing real work.

**One tell is not evidence.** Two or three are. Read structure first, vocabulary second: word habits drift every model release, structural habits persist.

## 3. Workflow

Do these in order. Short on time? Work from step 1 forward; stopping after step 3 does not count as done.

### Step 1 — Fix the claim and the reader

In one sentence: the single most evidence-backed, most useful thing in the piece. Who reads it, and what should they be able to do afterward?

- **Deletion test**: delete the sentence. What does the reader lose? If they lose a fact, scope, stance, consequence, or next step, you may not delete it. Only tighten it.
- Can you reorder the paragraphs freely? If yes, they are not advancing.
- Does the last paragraph answer the question the first one raised?

### Step 2 — Guard the content (before any style edit)

- Check numbers, units, dates (verify weekdays against a calendar), precision ("about 42%" is not "over forty percent"), negation scope, modality, claim strength, comparison baseline, conditions, agent, completion state, terms, and proper names.
- When the user says the draft is AI-written and supplies the real facts: **the user is the only source of truth.** Correct conflicts, list what you removed, never silently keep an unsupported sentence.
- If a detail is missing, cut the vague sentence or stay general, and put the gap in the note after the draft.
- Flag suspected errors separately; do not silently overrule the author.

### Step 3 — Cut defensive writing (A)

Ask: **does this help the reader use the conclusion, or does it pre-empt an objection nobody raised?**

- **Cut**: unearned self-deprecation, repeated disclaimers, strawman rebuttals, stance vacuums ("it depends", "pros and cons"), fake balance, stacked hedges, performed candor, knowledge-cutoff disclaimers, process narration and self-assurance, reassurance and direction-granting.
- **Keep**: scope statements, method and sample limitations, distinctions that carry the argument, evidence-backed qualifications, legal/safety/academic notices, real corrections, source tags, genuine unfinished work.
- Fixing is not only deleting: state what you studied instead of what you didn't; collapse three hedges into one and say where the uncertainty comes from; one layer for real doubt, zero for certainty.

Full tests in [references/defensive-forms.md](references/defensive-forms.md).

### Step 4 — Cut explanatory bloat (B)

Explanation the reader neither asked for nor gained from. It reads smoothly, which is why it survives.

- **Cut**: "in other words" restatement; re-explaining context the reader already has; turning one action into three steps; self-answered rhetorical questions; "this section covers…" metadiscourse; explaining an example that explains itself.
- **Keep**: background the reader genuinely lacks (judge by reader, not by the writer's habit); a term's definition at first use, once; anything that changes what the reader does next.
- **Fix**: replace "why it matters" with "what happened"; lead with the decision; merge three restatements into one.

Full taxonomy in [references/explanatory-forms.md](references/explanatory-forms.md).

### Step 5 — Replace stock formulas (C)

Two tiers:

- **Strong** (act on one sighting): not-X-but-Y and its variants; subjectless paragraph openers ("it's worth noting", "crucially"); importance inflation and uplift closers; universal truisms; means-ends chains ("by doing X, we not only… but also…"); structural previews; chatbot wrappers.
- **Weak** (act only when clustered): triads, em dashes, colons, connector stacking, uniform paragraph or sentence length, passive voice, nominalizations, metaphor, parenthetical stuffing.

Rule: **delete the invented X, state Y.** If Y is itself an abstraction, delete the sentence. Do not swap in a parallel shell ("while A, B") and do not restate the same abstraction in plainer words.

List in [references/stock-phrases.md](references/stock-phrases.md).

### Step 6 — Audit coined terms (D)

The second module this skill adds beyond its sources. See §4.

### Step 7 — De-template, tune voice, verify (E/F)

- **E Structure**: definition → three parts → uplift; identical paragraph shapes; a closer after every section; paired headings; headings restated in the first line; outline-style endings. Structure should grow from the material, not be a frame filled in.
- **F Residue**: chatbot wrappers, markdown debris, half-width punctuation in CJK text, emoji templates, leaked citation markers.
- **Verify**: re-check facts and certainty against the source. Revert any added fact, number, quote, motive, or causal link. If the rewrite lost more than 15% of its length, check section by section that information was not treated as filler.
- **Do not over-correct**: if the result is flat (short, uniform, connector-free, reads like an outline), restore full sentences and the original rhythm. Re-add function words only, never template phrasing, and never a closing aphorism to compensate.

## 4. Coined-term audit (D, core module)

The most dangerous AI tell is not empty prose; it is **inventing a term that sounds technical and then using it as the argument.** Once the reader accepts the word, every claim built on it rests on nothing.

### 4.1 Five tests

| Test | Question | Failing shape |
|---|---|---|
| Definition | Can you define it in one sentence without circularity? | "X means having X-ness" |
| Provenance | Who proposed it, in what paper, standard, or product, in what year? | "experts widely agree" |
| Boundary | Can you name something that is **not** it? | everything qualifies, so nothing does |
| Substitution | Replace it with plain words. Does information disappear? | only the gravitas disappears |
| Prediction | What does it let you distinguish or predict? | it renames an existing idea |

### 4.2 Seven shapes

1. **Empty abstraction**: hyper-automation fabric, value anchor, growth flywheel, operating model, synergy layer.
2. **Concept mashup**: "AI-native data-driven ecosystem", "full-stack synergistic enablement".
3. **Fake academic naming**: "the SCALE framework", "the three-layer maturity model", with no author and no source.
4. **Fake institution / report / standard**: "a recent industry report shows", "the Global X Council standard", "according to the Y White Paper".
5. **Un-expanded acronym** or one whose expansion does not match its use.
6. **Term drift**: a real term used in the wrong sense ("entropy" for "messiness", "paradigm" for "way").
7. **Fake proper nouns**: invented products, companies, people, or case subjects used as evidence.

**Added judgment counts as fabrication**: pairing a term with "proven", "widely adopted", or "industry-standard" upgrades a guess into a fact.

### 4.3 Disposition ladder

| Finding | Action |
|---|---|
| Real term, stable definition | keep; define once at first use |
| Real idea, vague wording | replace with concrete actions and objects |
| No content, only gravitas | delete the word, keep the concrete sentence it was propping up |
| Plausible but untraceable | keep the sentence, mark `[verify: origin]`, flag it in the note |
| Fake institution, report, or stat | delete or mark `[needs source]`; **never invent a source** |

### 4.4 Term ledger (required in audit mode)

For every suspect term: term, first location, type, results of the five tests, recommended action, and whether it was flagged. If there are none, say so.

Full guidance in [references/coined-terms.md](references/coined-terms.md).

## 5. Template structure (E)

| Shape | Test | Fix |
|---|---|---|
| definition → three parts → uplift | the reader can predict the next section | rebuild around problem, time, cause, or scene |
| every paragraph background-point-summary | paragraph-level cloning | cut the summary; end on a result or a real open question |
| paired headings (two-word / two-word) | you cannot tell what each covers | name the content |
| heading restated in the first sentence | same sentence twice | delete the restatement |
| outline ending ("the future looks bright") | no new information | end on the last concrete fact |
| label-colon lines ("Key challenge: …") | slide deck pasted into prose | write full sentences |

## 6. Formatting residue (F)

Chatbot openers/closers ("Great question!", "I hope this helps"), cutoff disclaimers ("as of my last update"), reasoning leakage ("let me think", "step 1:"), placeholder templates, markdown debris, mismatched punctuation, decorative bold, emoji templates, citation artifacts.

Formatting errors get fixed on sight; they do not count as changing the writer's voice. Whether to strip markdown depends on where the text is going.

## 6.5 Sentence craft (English-specific)

English and Chinese fail differently. Chinese tolerates long paratactic runs and fails on stacked `的` modifiers; English fails on **subordination**: clauses inside clauses inside clauses. Do not translate Chinese sentence rhythm into English, and do not fix English by chopping it into Chinese-length short sentences either.

### Hard limits

| Check | Limit | Action |
|---|---|---|
| Sentence length | over 30 words = flag; over 45 = rewrite | split at a conjunction, or promote a clause to its own sentence |
| Subordinate clauses | 3+ per sentence (`which, that, who, whose, while, although, whereas, because, since, if`) | promote one to a main clause |
| `-ing` chains | 2+ trailing `-ing` clauses in one sentence | convert to a finite verb or delete |
| Pre-modifier pile | 4+ adjectives/nouns before the head noun | move some after the noun, or split |
| `of` chains | 3+ consecutive `of` phrases | reorder: put the actor first |
| Parenthetical nesting | parentheses inside parentheses | flatten into a separate sentence |

### Four rewrite moves

**1. Split at the joint, not in the middle**
> Before: The report, which was commissioned by the board and which draws on interviews with fourteen managers across three regions, argues that the current approval process, although it has reduced cycle time, still creates bottlenecks that slow hiring.
> After: The board commissioned the report, which draws on interviews with fourteen managers in three regions. It argues that the current approval process has cut cycle time but still slows hiring.

**2. Promote the buried clause**
> Before: What we found, after running the test for two weeks on a sample that excluded new accounts, was that retention did not change.
> After: We ran the test for two weeks, excluding new accounts. Retention did not change.

**3. Kill the cleft and the expletive**
> Before: It is the case that there are three reasons why the rollout failed.
> After: The rollout failed for three reasons.

**4. Un-nominalize**
> Before: The implementation of the optimization of the onboarding flow resulted in a reduction in drop-off.
> After: We optimized the onboarding flow and drop-off fell.

### Counter-rules

Short is not automatically better.

- Do not split a sentence that carries one argument just to look punchy.
- Do not produce a run of fragments ("No setup. No config. No limits.") — that is its own AI tell (§5).
- Keep a long sentence when the length enacts the content (a list, a sequence, a build).
- Vary length by ear: real prose alternates. Uniform 12-word sentences read as machine-made as uniform 45-word ones.

### Chinese side differs

| | Chinese | English |
|---|---|---|
| Long sentence | acceptable when paratactic (逗号推进，意合) | fails fast when subordinate (从句套从句) |
| Real problem | 长定语、多层"的"、翻译腔名词堆叠 | relative-clause nesting, `-ing` chains, `of` chains |
| Rhythm | 四字格、短句与流水句交替 | varied finite clauses; fragments are a tell |
| Fix | 拆"的"字定语、还原动词 | 拆从句、还原主谓、去名词化 |

## 7. Genre and voice

| Genre | Default force | Watch for |
|---|---|---|
| Blog / essay / opinion | keep rhythm and judgment | no invented personal experience |
| Technical docs | accuracy before brevity | keep versions, conditions, order; do not explain the same thing in four places |
| Legal / compliance | keep fixed phrasing | boilerplate is not AI slop here |
| Academic / grant | restrained and precise | keep qualifications and attribution; correct citation format does not mean the citation exists |
| Email / message | match the relationship | keep genuine greetings and sign-offs |

If the user supplies a writing sample, **the sample outranks this file**: sentence length, word choice, punctuation, dash habit, verbal tics. Borrow the syntax, not the persona.

## 8. Output

- **Edit (default)**: the final draft, then a `---` line, then the note. The note covers only what the user must know or decide: whole sentences or paragraphs removed and why, uncertain calls, missing material worth adding. Three items max.
- **Audit**: no rewrite. For each finding: location, exact snippet (≤20 words), problem in plain language, fix direction. Order by impact; lead with the one or two that matter most.
- **File mode**: change prose only; leave code blocks, inline code, commands, paths, URLs, YAML, table data, and heading levels alone. Report what changed, what needs verification, and the before/after word count.
- **Never** add "Certainly!" or "Here's what I found", and never write "I preserved your meaning" or "no facts were changed" as a self-assurance.

## 9. Pre-delivery checklist

1. Can every new specific detail be traced to the source or the user?
2. Are negation, scope, time, condition, attribution, and stance intact?
3. Did "may" become "will", or "involved" become "responsible"?
4. Was every deleted sentence deleted because the reader lost nothing?
5. Is every coined term in the ledger with a status?
6. Did fixing stock formulas change wording only, or did it also drop content?
7. Can you say what judgment each kept qualification helps the reader make?
8. Do the paragraphs advance, or repeat the same shape?
9. Were genre norms and the writer's sample respected? Did you rewrite passages that were fine?
10. Read it aloud. Does it still sound like one person talking to one reader?

## 10. When not to act

Leave a watched phrase alone inside a quotation, title, proper name, code, legal text, standard definition, foreign-language passage, dialogue, or a passage that **discusses** the phrase ("I've stopped using the word 'leverage'").

These occur just as often in human writing and are **not evidence on their own**: in-sentence parallelism, rhetorical-question headings, metaphor, passive voice, nominalization, even sentence and paragraph length, a single "first… second…".

Do not judge text shorter than two or three sentences.

## Sources and license

MIT. Methodology merged and rewritten from:

- [blader/humanizer](https://github.com/blader/humanizer) (MIT): structural taxonomy and the evidence-threshold idea
- [op7418/Humanizer-zh](https://github.com/op7418/Humanizer-zh) (MIT): constraint priority and edit boundaries
- [Devilyuu/anti-defensive-writing-zh](https://github.com/Devilyuu/anti-defensive-writing-zh) (MIT): defensive-filler tests and the Chinese tell inventory
- [petergyang/no-ai-slop](https://github.com/petergyang/no-ai-slop) (MIT): edit/audit modes and the minimum-effective-edit rule

New in this project: the explanatory-bloat taxonomy, stock-formula detection, coined-term detection, and the term ledger.
