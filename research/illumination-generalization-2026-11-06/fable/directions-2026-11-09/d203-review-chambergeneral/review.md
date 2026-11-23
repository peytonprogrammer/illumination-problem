# d203 review: arithmetic matching for aligned rectangular chambers

Date: 2026-11-23. Reviewer: independent referee.

Reviewed file: `snapshot.md` in this directory. Context: `../PROGRAM.md` (top
section), [d201 review](../d201-review-pocket/review.md),
[d202 review](../d202-review-neckphase/review.md),
`../d163-pattern-ledger/STATUS.md` and `ledger.json`.

Code: [checks.py](checks.py), log [checks.log](checks.log). It uses the
standard library and exact integer arithmetic. The tracer scales coordinates
by DX·DY, so every bounce point is an integer, and a vertex hit is a failure.
The full run takes about 280 CPU-seconds; Part E's J fallback uses most of it.
Every ray comes from a construction in the note: a closed-form slope, one
modular solve, or a solution of the note's group-ring test. The script runs no
ray, direction, word or room-size search.

## Verdict

**Correct with gaps.** Every theorem in the note holds. All 55,000-plus
prescribed rays reach their targets with no corner hit. The gaps are an
understated end-pocket condition (L ≡ 2 mod 3 needs no separate route), a few
implicit hypotheses and one status-level imprecision. None of them breaks a
proof.

## Per-part verdicts

1. **Arithmetic test J: correct.** The group, the expressions Eⱼ, the gate
   bounds Lᵢ, Uᵢ and the identity coefficient are right. J > 0 is an exact
   criterion for the prescribed strip transit.
2. **Dimension-only consequences: correct.** This covers the opposite-side
   theorem, the same-side theorem for opposite-parity pairs, and the
   exceptional set for odd P, including the 4, 6, 4+156k example.
3. **Narrow chambers: correct with gaps.** The width-2 family, the end-pocket
   test and the width-1 corollary hold. The L ≡ 2 (mod 3) branch is
   unnecessary, because the end-pocket test with n = 1 works. The height ≥ 5
   discussion is accurate but too cautious.
4. **Mixed construction: correct.** The 368 roots it prescribes on 8 named
   rooms all reach their targets.
5. **Complement statement: correct, not overstated.** It is a per-pair
   definition of the residual. The note correctly claims neither emptiness nor
   darkness.
6. **Ledger follow-on: correct.** The two OPEN words match ledger.json and
   STATUS.md. The list is exhaustive for the stated shape model.

## 1. Arithmetic test

- **Phase bookkeeping.** In strip (f, f+B), a point at x with sign ε has
  oriented phase ε(x − f) mod 2B, and the phase grows by v per unit of
  longitudinal travel. Over piece j the condition is
  ε_j(x_j − f) − ε_{j−1}(x_{j−1} − f) ≡ d_j v (mod 2B_j). Scaling by D gives
  Eⱼ ≡ dⱼ n (mod 2BⱼD), as stated. The sign is the same on both sides of a
  gate, and it continues through a prescribed roof bounce. Both are right.
- **Dv is an integer.** The local map between physical and unfolded
  coordinates is ±U + c with c an integer. c starts integral at a lattice mark
  and stays integral, because each wall reflection sends c to 2·wall − c. So
  the unfolded endpoint is an integer, and n = Dv is an integer. Each gate
  coordinate times D is then an integer.
- **Gates.** A strict gate a < z/D < b gives Da + 1 ≤ z ≤ Db − 1, which is the
  note's Lᵢ and Uᵢ.
- **Converse.** A common n can be made positive by adding
  lcm(2BⱼD / gcd(dⱼ, 2BⱼD)). Transverse reflections inside a piece can't land
  on a gate line, because the gate point is strictly inside the strip. So no
  corner is hit.
- **Checks (Part G).** On 12 itineraries, the group-ring coefficient (a lex-min
  coset normal form in G) equals a direct CRT enumeration. These itineraries
  cover horizontal ones in the area-21 room, neck bounces, chamber
  excursions, pocket stubs and opposite labels. All 22 solutions traced reach
  T, with total longitudinal travel D and every gate crossing at zᵢ/D.

*Gap (low).* The proof needs integral mark coordinates. The note says "all
data are integral" but doesn't name the marks. That's lemma L3's territory.

*Gap (low).* The specialized gcd lift (item 3) also needs the source chamber
height in M and an integral source abscissa. d202's review raised the same
point.

## 2. Dimension-only consequences

- **Opposite side.** The fold arithmetic checks out. Mma is a multiple of 2u,
  the band adds Mm + η modulo 2P, and Mmb is a multiple of 2v. With gcd = 1,
  g = 2, so |d| ≤ 1 and |aη|, |bη| < 1.
- **Same side, opposite parity.** Δ = 2K + d with K even is right, so
  Mm ≡ K (mod 2P) is solvable. The unit cell beside z is entirely neck wall or
  entirely aperture, because every boundary is an integer. The roof contact and
  the return stay in that cell, and the target sheet is right.
- **Exceptional set.** For odd P, each choice of lift has exactly one root of
  the right parity, and no root is 0 or P. The bound x_S ≡ z₊ + z₋,
  x_T ≡ z₊ − z₋ (mod P) holds.
- **The 4, 6, 4+156k example.** For k = 1..6 (Part F), P is odd and coprime,
  and the roots fold to the seams 12 and 4. A control ray at z = 12 hits the
  corner (12, 1), as predicted. At k = 1, zero drift misses exactly 4 ordered
  abscissa pairs, all inside the 64-pair bound.
- **Grid (Part E).** The grid has 789 coprime rooms: widths 1–4, necks 1–3 and
  three height sets. The traced rays were 25,774 opposite-side, 12,084
  same-side odd and 8,972 zero-drift, with 0 failures. The 1,218 zero-drift
  exceptions all have both roots at seams, and all lie inside the 64-pair
  bound. *Beyond the note:* each of these 1,218 pairs has a positive J for
  some itinerary of at most 5 pieces, and its traced ray reaches T.

## 3. Narrow chambers

- **Width two (Part D).** P is odd, x and y are even, and z = x + 1 + L₂/2 is
  even and inside (x+1, y−1). All of this checks. On 96 rooms
  (L₁ ∈ {1,…,11} odd, L₂ ∈ {2, 6, 10, 14}, four height patterns), all 3,504
  cross-chamber pairs reach their targets.
- **End-pocket test.** The phase −e + 2bc and the floor-corner argument
  (only e = v needs the separate check) are right. So is the solvability gcd.
- **Width-one corollary (Part C).** The odd-B slope 3 + 1/B and the
  equal-offset routes work for every pair, for L = 1..30.
- **Understated condition (low).** The note tests 2 − P ≡ ±1 (mod 6) at n = 0
  only. Its own solvability criterion, gcd(4P, 6) = 2 dividing 2 − P ∓ 1,
  always holds. For L ≡ 2 (mod 3), n = 1 (c = 5P/2) gives 2 − 5P ≡ 1
  (mod 6), and the traced ray reaches T for L = 2, 5, …, 29. The
  outer-wall-plus-neck route is also correct, but it isn't needed.
- **Height 5.** The arithmetic is right: the right-hand side is 3 or −5, which
  is odd, and the gcd is 2. But the note's own coprime theorems decide the d202
  gap in the named room 3×3, 3×5, 3×3 with necks 1 and 1 (P = 11). All four
  pairs from an end at row 1 to the middle at row 3 reach their targets
  (Part H): two by the same-side odd construction, two by zero drift.

## 4. Mixed construction

The entry and return positions (1 − u)/r and w − (1 − v)/r are right. So is
the odd-multiple equation and the roof-corner exclusion by the doubled-phase
identity. On each fold piece, (A/r + B)/w is monotone, so checking the
endpoints suffices.

The script implemented the piecewise folds, including optional outer-wall
images. It tested 4 rooms and their vertical flips, which cover the
lower-pocket branch. All 368 roots with an odd multiplier of at most 41 reach T
(Part I).

## 5. Complement statement

This is a definition of the residual (all applicable tests vanish), not a
classification, and the note says so. The R22 remark is limited correctly, and
the note claims no darkness. *Gap (low).* "Every applicable test" is finite
only once the itinerary list is fixed. State that this is the list in items 1
and 2 plus the two mixed branches.

## 6. Ledger follow-on

Each strictly inset neck has 4 reflex corners, and W = 4 + 2R ≤ 20 allows at
most 8. So there are at most two necks, and the chambers form a path of three.
F = RRLLLLRR is right. The canonical forms of F L^j F L^(4−j) (Part J) are:

| j | Canonical word | Status |
|---|---|---|
| 0 (same side) | LLLLRRLLLLRRLLLLRRRR | OPEN |
| 1 (adjacent) | LLLLRRLLLRRLLLLRRLRR | OPEN |
| 2 (opposite) | LLLLRRLLRRLLLLRRLLRR | OPEN in ledger.json, PARTIAL in STATUS.md since d200 and d201 |

The one-neck word LLLLRRLLLLRR is PARTIAL (d77, d108, d111, d112), and LLLL is
COVERED. The exhaustiveness claim holds for this shape model.

## Errors and fixes

1. **Low (width-one corollary).** *Fix:* "The end-pocket test covers all
   L ≥ 1: take n = 0 for L ≡ 0, 1 (mod 3) and n = 1 for L ≡ 2." Keep the
   outer-wall route as an alternative.
2. **Low (height ≥ 5).** *Fix:* add "When gcd(P, 3) = 1, the coprime theorems
   light the d202 gap pairs, for example with necks 1 and 1."
3. **Low (hypotheses).** State that the marks are lattice points for J, and
   that the source chamber is included in M for the gcd lift.
4. **Low (complement).** Name the finite itinerary list that "every applicable
   test" ranges over.

## Which lemma does this advance, and what is the first case still open?

**L1** (lighting tail), for the opposite-side three-chamber word with aligned
unit necks. The note gives an exact per-itinerary test, a dimension-level
theorem that lights all coprime rooms except a finite abscissa residue, and the
two narrow families.

**First case still open.**

- **Aligned, unit necks.** The note proves no dimension-only theorem when
  gcd(P, lcm wᵢ) > 1. An example is chambers 3×3, 1×3, 2×3 with necks 1 and 2
  (area 21, gcd 3).
  - Its 4 same-row pairs aren't covered by any stated theorem.
  - Part K evaluated J on them: all 4 have J > 0 through a neck bounce, and
    the traced rays reach T.
  - Part K didn't check the room's cross-row pairs, so this review doesn't
    claim the whole room is lit.
  - The general non-coprime case is open as a theorem.
- **Same word, outside the note.** Displaced or non-unit necks of area 21 and
  up, chamber heights other than the aligned band, and real marks (L3).
- **Smallest W ≤ 20 room not covered by a reviewed theorem.** Area 21 remains
  open in this word through rooms like the one above. This review didn't
  enumerate rooms by area.

## Area-21 and area-23 rooms

**Both are fully lit for lattice marks.**

- **Area 21** (three 2×3 chambers, necks 1 and 2): all 15 pairs (Part B).
  The pairs are 3 axis segments within a chamber, 6 opposite-side, 4
  same-side odd and 2 zero-drift at z = 6.
- **Area 23** (3×3, 1×3, 3×3, necks 1 and 1): all 28 pairs (Part C, L = 1).
  - The traced constructions are the end-pocket, odd-B and cross-row direct
    rays.
  - Same-chamber pairs use a direct segment (4 rays) or a vertical axis
    segment (8 pairs).

Real marks (L3) aren't treated.

## Ledger effect

**No count change.** The opposite-side word stays PARTIAL, with a larger lit
region:

- every coprime aligned room, apart from the finite zero-drift residue;
- the width-2 and width-1 families;
- the area-21 and area-23 rooms.

The adjacent and same-side words stay OPEN, because the note proves nothing
for them. The coordinator should add these results to the d200/d201 row in
STATUS.md. The coordinator should also record that 21 is still the first open
area. Its example is the non-coprime room above, no longer the three 2×3
chambers.
