# d164 attack: limits of the stacked-hall theorem

Target: the "Parallel mouths on one side of a hall" theorem and its two-sided step in `qclass-closure/bbbb/parallel-mouth-combs.md`.
Script: [attack.py](attack.py). Output: [attack.log](attack.log). The run takes 177 CPU seconds.

## Result

No dark pair. The note's shot family first fails in **A8**, at 8× the bound. Every failing pair in all 10 rooms is lit by the per-pair search.

- In A8, AT and E, a hall-walls-only path lights every failing pair. These paths use several floor and roof bounces or a straight chord.
- In B (overhang) and DB55, some failing pairs need a bounce on attachment walls: 1,345 pairs in B and 2,028 in DB55.

## Method

- **Pairs.** Each room uses every lattice and half-lattice interior mark. A pair is tested when at least one mark lies outside the open hall strip 0<y<c. Pairs inside the open hall are convex chords and aren't traced.
- **Shot family.** The family is the note's direct chord, plus the floor turn with the sign rule and both travel candidates E and E+2A. The chosen candidate is reported separately from the other one. Two-sided rooms add the mirrored roof turn and the direct traversal with no turn.
- **Lit search.** A pair fails when every shot in its family fails. Each failing pair gets a search inside its own room only. The search tries all 8,812 primitive directions with max(|p|,|q|)≤60, plus the 4 axis directions, with at most 40 reflections.
- **Mechanism.** Each lit path's reflections are tagged by wall: floor, roof, hall side, attachment side or horizontal, and bank. A second search then forbids attachment-wall bounces, which shows whether those bounces are needed.
- **Exactness.** Arithmetic is exact integer stepping on doubled coordinates. The ray stops at every vertex. On 3,000 shots in A2 and DB55, the stepper agreed with the d162 Fraction tracer every time. On A4 the search recovered all 258 family-lit pairs within bounds.

## Rooms

| Room | Hypothesis edge | W | Max 8Ah/(cu) | Pairs | Chosen fails | Family fails | Lit by search |
|---|---|---|---|---|---|---|---|
| A2 | 2× bound, A=5, c=10, tooth [1,3]×[10,11] | 8 | 2 | 1,041 | 0 | 0 | – |
| A4 | 4× bound, c=5, tooth [1,3]×[5,6] | 8 | 4 | 501 | 0 | 0 | – |
| A8 | 8× bound, c=5, tooth [1,3]×[5,7] | 8 | 8 | 1,038 | 7 | 7 | 7/7 |
| AT | narrow tall arm [1,2]×[3,9], c=3 | 8 | 80 | 606 | 160 | 68 | 68/68 |
| B | overhang: [1,3]×[32,33] with child [2,5]×[33,34], A=6 | 12 | 1 | 8,382 | 2,743 | 2,708 | 2,708/2,708 |
| C | child [2,4] flush with parent [1,4], A=5, c=40 | 10 | 1 | 11,496 | 0 | 0 | – |
| D1 | roof [1,3]×[20,21] over floor [1,3]×[−1,0], A=5 | 12 | 1 each bank | 4,278 | – | 2 | 2/2 |
| D2 | roof [1,3]×[24,25], floor [3,5]×[−1,0], A=6 | 12 | 1 each bank | 6,270 | – | 0 | – |
| DB55 | hall [0,13]×[2,3], banks of depth 2 on both sides | 12 | 208/5 | 13,896 | – | 4,646 | 4,646/4,646 |
| E | 8 nested unit-height levels, zigzag flush, A=c=9 | 20 | 64 | 45,120 | 133 | 127 | 127/127 |

## Findings

1. **The constant 8 is loose by about 8.** A2 and A4 pass every pair at 2× and 4×. In A4 the second candidate fails 151 times, but the chosen shot never fails. A8 is the first failure. Its 7 failing pairs all involve the arm's top marks, such as (3/2,13/2), and all are lit. Each has a hall-walls-only path, using a straight chord or 1–5 floor and roof bounces.
2. **Narrow tall arm (AT).** 68 pairs fail the family. Of these, 25 are lit by a straight chord. The other 43 have hall-walls-only paths, each with at least 2 floor and roof bounces. The note's single floor bounce is the limit, not the hall.
3. **Overhang (B) breaks the construction with the metric satisfied.** Marks in the child above the gap 3<x<5 get the sign rule's far-end direction, toward x=5. Their descent must pass through the parent interval [1,3], so the leg is blocked. Every pair is still lit, and 1,345 pairs need child-wall bounces. Example: (1/2,1/2)–(4,67/2), direction (3,−2), with 2 child-ceiling and 2 child-side bounces before the hall.
4. **Flush child (C) is safe.** All 11,496 pairs pass at equality. This supports adding flush children to the hypotheses, as d162 recommended.
5. **Two-sided.** D1 and D2 both violate the two-sided step: 16Ah=2cu, and their mouths lie outside [A/4,A/3].
   - D2 passes every pair.
   - D1 fails only (3/2,−1/2)–(5/2,−1/2) and its roof mirror. These are same-height pairs in one tooth: both turn contacts land in the opposite open mouth. A straight chord lights them.
   - DB55 fails 4,646 pairs. Of these, 1,079 are lit by straight chords inside a chamber, and 2,028 need bank-wall bounces. Example: (1/2,−3/2)–(17/2,−3/2) with reflections bank side, roof, bank side, bank floor.
6. **Deepest nesting (E, W=20).** Eight levels at 64× the bound fail only 127 of 45,120 pairs. All are lit by hall-walls-only paths. An 8-level member at the bound needs c≥576, too tall to enumerate here. d162 M4 covers 3 levels at the bound.

## What this means for the theorem

- **Bound.** The one-floor-bounce family survives up to 4× the bound in these rooms. Its failures come from the bound before any darkness appears.
- **Missing mechanisms.** Two repairs are visible.
  - **Several floor and roof bounces.** Use more travel candidates and more turns. This lights every failure in rooms that satisfy nesting.
  - **Attachment-wall bounces.** These are needed once nesting fails (B), or when banks are open on both sides (DB55).
- **Limits.** The search bounds don't prove darkness, but no candidate appeared. Nothing here moves the W≤20 estimate.
