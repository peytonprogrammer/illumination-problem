# d166 review: parallel dents and the first missed doorway

Target: `../d95-review-queue/snapshots/parallel-dent-frontier.2026-11-22-0758.md`.
Checks: [checks.py](checks.py), output in [checks.log](checks.log). Sections 1–4 come from
`python3 -B checks.py` (460 CPU-seconds). Section 5 comes from `python3 -B checks.py --extra`
(25 CPU-seconds), appended to the log. The run uses named and explicit rooms only. The only
enumerations are over marks, levels and ray directions inside fixed rooms. The ray tracer
`trace()` is copied verbatim from d164 `attack.py`.

## Verdict

**Sound with gaps.** The bookkeeping, the joint criterion, its all-abscissa corollary, both
worked examples and the bank decomposition all check. The criterion agrees with an
independent exact tracer on 581 of 581 pairs. The note is a local tool plus one
obstruction example. It moves no ledger word to COVERED or PARTIAL.

## 1. Ledger bookkeeping

All claims match `ledger.json`, using my own turn-word, dent and section code:

- Target 1 has 1,020 OPEN words with all dents parallel: 935 dented and 85 undented. By W:
  7, 20, 44, 115, 246, 588.
- 296 dented words have no strip parallel to the dents that spans the bounding box in their
  ledger realization. 18 of them have no spanning strip in either direction.
- Two such words occur at W = 12: LLLRLLLRLLRR and LLLRLLRLLLRR (room 1843's word).
  LLLRLLLRLLRR comes first in ledger order, and its coordinates match the note exactly.
- LLLRLLLRLR is one of the 7 OPEN words at W = 10, all in target 1. Its polygon matches.
  "A smallest" is correct. It isn't first in ledger order (LLLLLLRLRR is), but ledger.md
  lists it first.
- S10 (LLLRLRLLLRLR, W = 12, 10 cells) is OPEN and in target 1. Its runs are (2,4), (1,4),
  (0,3), (0,2), as stated.

## 2. The joint criterion

**Derivation: correct.** In the connected-section orientation each band is a rectangle
whose vertical sides are walls over the band's full open height. So the reflection group of
each band acts on abscissas as x ↦ ±x + 2ku. The developed segment from s′ at depth a to t′
at height b crosses the joint at (b s′ + a t′)/D. Substituting s′ = l ± ξ + 2ku and
t′ = m ± η + 2jv gives ω ± p ± q + (2bu/D)k + (2av/D)j. The converse fold works because the
crossing lies in the physical copy of both bands. The folded legs touch only vertical sides
at heights strictly between the mark and the joint, so they meet no corner. The note doesn't
state the full-height-wall fact, which carries the converse (gap 5).

**Staggered versus flush.** At a staggered lip the mouth endpoint is a vertex, so the open
test is exact. At a flush lip, a crossing at the endpoint is a legal side reflection, as
the note says. In practice it never mattered: across 4 flush joints and 432,964 placements,
no pair failed the open test but had a flush-endpoint crossing. The exact tracer also found
no pair lit only through a flush point (gap 6).

**All-abscissa corollary: correct.** The four candidates are symmetric under σ: x ↦ 2ω − x,
whose fixed residues are ω and ω + g/2.

- Both residues in J: the closed complement arc avoids both fixed points, so it misses its
  σ-image. One of ω ± (p+q) clears.
- A residue outside the closure of J: p, q → 0, or p → g/2 and q → 0, gives an open
  failing set. The bound bu/D ≥ g/2 holds because 2bu/D is a positive multiple of g.
- Boundary: failure ⇔ ω+p+q and ω+p−q both lie in H. This forces p, q onto the
  quarter grid, so 16 residue pairs suffice.

Check 2c tests the classification at 188 level pairs over 6 joints. It evaluates the
open criterion on a grid of step g/24, which contains the quarter grid. The checks pass
as follows:

- all-clear: 164 of 164 levels have no failures
- open-fail: 5 of 5 levels have failures
- boundary: 19 of 19 levels have failure sets equal to the 16-pair prediction

A boundary case with real failures: J2 has lower run (0,2) and upper run (1,4). At a = b = 1,
g = 1 = |I|, which is the punctured circle. Exactly one placement fails, S = (1,1) and
T = (3,3). The tracer confirms 0 monotone shots, and a perturbation of 1/100 clears.
Rectangles and the L can't fail at all. In the L, ω is the flush endpoint, and g < 2 keeps
ω + g/2 in J. A failure would need g > |I|, which contradicts k₂ ≥ 2.

**Note's examples: correct.** In the S-tetromino, the residues are 1/8, 1/2 and 7/8, and
the tracer finds 0 monotone shots. The floor bounce at (5/8,0) reaches T exactly. In S10,
ω = 1/2, p = q = 1/8 and g = 3, and the criterion fails. The full-room tracer finds 0
monotone shots with |n| ≤ 30. The cap path with direction (−1,4) reflects once at (5/8,4)
and ends at T. Both extreme section pairs of S10 are (2,4) and (0,2), which are disjoint,
so no spine spans the room.

## 3. Exact tests

The test uses 6 two-band joints. Three are staggered: the S-tetromino, J2 and a T-nested
joint with v = 17/12. One more is staggered with u = 7/5. Two are flush: an L and a
flush-right joint with v = 99/70. Marks are half-lattice points plus random rationals, with
denominators 79–97, 581 pairs in total.

The tracer is independent of the bands. It aims at every image ±T.x + 2λn, where λ is the
gcd of the wall abscissas and |Δx| ≤ 12 (8 for λ < 1/20). It traces each image physically
and accepts only vertical-wall contacts that end exactly at T.

| Comparison | Disagreements |
| --- | --- |
| Open criterion, bounded to the same Δx, vs tracer | 0 / 581 |
| With flush endpoints added, vs tracer | 0 / 581 |
| Exact residue criterion vs bounded | 10 / 581 |

All 10 have a shortest witness with |Δx| between 14.4 and 358.6. Section 5 builds each witness
by Bezout and traces it physically, and each reaches T monotonically. Exact criterion and
physics agree on all 581 pairs, with 577 lit and 4 failing.

## 4. Other claims and target 1

- **Advance on target 1: none at word level.** No word changes status. The criterion
  decides one joint for one pair of levels. It says nothing about non-monotone routes, other
  joints or other levels. S10 is one repaired pair, not a proof for S10.
- **Bank decomposition: correct.** Checked on 14 named realizations. Band counts are
  ≤ W/2 − 1, consecutive runs overlap, and greedy groups are ≤ ⌈(r+1)/2⌉: S10 2,
  cov279 2, cov2929 2, LLLRLLLRLLRR 2, others 1. The exchange argument for greedy
  optimality is sound. The note correctly says the chain doesn't transfer shots.
- **Passage argument: correct as a reduction,** with d131's scope. Four bands give at most
  4(k+1) passages for k reversals. d131 notes the forced count exceeds 4 only from
  m ≈ 1.1 × 10⁸, so this is asymptotic. It is for one orientation, which the note says.
- **d164 figures match attack.md:** 4,646 DB55 placements and 127 for room E.

## Gaps

1. **High: no word-level progress.** The note proves no target-1 word COVERED or PARTIAL.
   It should say that the criterion is a local lemma and that the S10 repair covers one
   pair.
2. **Medium: 296 is a one-realization count.** It's a lower bound on words with some
   hall-less length assignment. A hall theorem gives at most PARTIAL to the other 639 unless
   every length assignment of the word has a hall. Histograms do. Most two-bank words
   likely don't. Also, "the first" is one of two W = 12 words; the other is room 1843's.
3. **Medium: missing or broken citations.** `local-thickness.md` (the "reviewed flush-joint
   criterion") exists nowhere in the tree. `passage-complexity.md` exists only as a dated
   snapshot. The two `../../illumination-generalization-…` links resolve to nonexistent
   paths. My L analysis independently supports the flush claim.
4. **Medium: the corollary is per level pair.** "Every pair clears" fixes a and b. It is
   not a room-wide statement. The S-tetromino has open failing sets at some levels and
   none at others. The note should say so wherever it uses the corollary for a room.
5. **Low: the converse needs full-height side walls.** State that each band side is a wall
   over the band's whole open height, which holds in the connected-section orientation.
6. **Low: the flush caveat is conservative.** Flush endpoints changed no answer in 432,964
   placements. Either prove that the open test is exact at flush lips too, or keep the
   caveat as one-sided.
7. **Low: "nested rectangular attachments."** The height set at a given distance from a
   spine is a union of bands and can be disconnected, like comb teeth. "Unions of
   rectangles" is the accurate phrase.
