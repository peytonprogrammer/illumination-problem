# d202 review: neck phase map and the 3×4 middle-chamber family

Date: 2026-11-23. Reviewer: independent referee.

Reviewed file: `snapshot.md` in this directory, a byte-identical copy of
`.context/qclass-closure/bbbb/l1-neck-phase.md`. Context: `../PROGRAM.md` (top
section), [d201 review](../d201-review-pocket/review.md) and its snapshots,
[d200 review](../d200-review-threechamber/review.md) and
`../d163-pattern-ledger/STATUS.md`.

Code: [checks.py](checks.py), log [checks.log](checks.log). It uses the
standard library and exact `Fraction` arithmetic, and it runs in 26.7
CPU-seconds. Each ray comes from the note's formula, using at most one floor
operation or one modular inverse. The script traces that single ray. It runs
no ray, direction, word or room-size search.

## Verdict

**Correct with gaps.** Every proof step holds, and all 57,657 prescribed rays
reach their targets with no corner hit. One status claim is wrong: area 32 is
not the first open area for this word. Rooms of area 21 and 23 in the same
word aren't covered by any reviewed theorem.

## Per-part verdicts

1. **Neck map and coupled phase tests: correct with gaps.** Both closed-form
   slopes, all three explicit families and the K = 2A obstruction hold. The
   gaps are an unstated middle floor, a reused symbol and an unstated
   condition on L.
2. **All-pairs theorem for the 3×4 middle chamber: correct.** The case list is
   exhaustive (91 pairs per room), and all 56,875 traced pairs over
   1 ≤ X, Y ≤ 25 are lit.
3. **Sufficient condition for heights H₀ and H: correct with gaps.** It needs m
   to be a positive integer and the source at a lattice abscissa. Both are
   implicit.
4. **Status claims: partly wrong.** The 4×3 middle chamber and general
   displaced mouths are open, as the note says. But area 32 isn't the first
   outstanding area.

## 1. Neck map and coupled phase tests

**Neck map: correct.** In a unit neck, a phase measured from one wall advances
by Lr. A residue z in (0, 1) folds to depth z with the launch sign. A residue
in (1, 2) folds to 2 − z with the opposite sign. An integral phase at a mouth
is a mouth endpoint, which is a corner. Bounces strictly between the two
mouths are on smooth neck walls.

**Strip test: correct.** The middle travel splits into three pieces with
horizontal lengths (1 − α)/r, δ/r and (1 − β)/r. Their sum must be
(2m + 1)w, so the exit is on the rightward sheet. Substituting α = Ar − 2i and
β = Kr − 2j gives

    r = (δ + 2 + 2i + 2j) / (A + K + (2m + 1)w).

- Equivalently, the total unfolded rise from S at height 0 to T at height δ + 2
  is δ + 2 + 2i + 2j.
- The conditions 1 − α < wr and 1 − β < wr are exactly a, b ∈ (0, w).
- Side contacts in the strip are at heights strictly in (1, 1 + δ), where both
  sides are solid. Contacts at the two levels need a or b in wℤ, which the
  strict inequalities exclude.
- m ≥ 0 holds automatically, because a + δ/r > 0 > b − 2w.

**Roof test: correct.** The total vertical travel is
Ar + (δ + 2 + h − α) + (h + β) + Kr. With Ar − α = 2i and β + Kr = 2j + 2, this
gives

    r = (δ + 4 + 2i + 2j + 2h) / (A + K + (2m + 1)w),

as the note states. Roof clearance follows from 2(a + h/r) ≡ a + b (mod 2w)
with 0 < a + b < 2w, which is the d201 argument.

**Explicit families: correct.** `checks.log`, Part C:

| Family | Named rooms | Hits | Max bounces |
|---|---:|---:|---:|
| Strip, w = 2, δ even, L, R ≡ 0 (mod 4) | 64 | 64 | 80 |
| Roof, w = 2δ + 8, h = δ + 5, L ≡ 0, R ≡ 2 (mod 4) | 72 | 72 | 26 |
| Reflected stubs, K = 2A, r = 1/4 | 188 | 188 | 88 |
| Adjacent mouths, r = 2/3 | 108 | 108 | 24 |

- The roof family's predictions hold for every δ: a = 2δ + 3, b = 2δ + 7, and
  a + 4h − b = 2w. The roof contact 4δ + 13 is odd, so it isn't a multiple of
  w = 2δ + 8.
- In the reflected-stub family, 148 of the 188 rooms have e, f ≥ 3w. These are
  the rooms where the straight-stub tests fail.
- All displaced-mouth rooms have the opposite-side key
  `LLLLRRLLRRLLLLRRLLRR`. All adjacent-mouth rooms have the adjacent key
  `LLLLRRLLLRRLLLLRRLRR`.

**K = 2A obstruction: correct.** The straight stubs need er, fr < 1, so r < 1/(3w)
and wr < 1/3.

- The strip test needs 1 − α < 1/3, so α > 2/3. Then Kr ≡ 2Ar ≡ 2α (mod 2),
  and 2α ∈ (4/3, 2), which is the wrong sheet.
- The roof test needs δ + 2 − α < wr < 1/3, but δ + 2 − α > 2.
- e = f = 3w and R = 2L + 3w give K = 2A.

The note limits the claim to these two itineraries and says it isn't evidence
of darkness. That is the right scope.

**Adjacent mouths: correct.** The straight middle leg from (0, y) to (x, H)
needs x = (H − y)/r. The stub incompatibility holds for integral e, f ≥ 1:
er < 1 gives r < 1, and f/r < 1 gives r > 1. In the r = 2/3 family, 2L/3 is
even when 3 divides L, and 3R/2 is even when 4 divides R.

*Gaps (low).*

- The middle chamber's floor isn't stated. The left opening is (0, 1), so the
  word is the opposite-side key only if the floor is below 0. A floor at 0
  makes the left neck flush and changes the word. The tests themselves don't
  depend on the floor. `checks.py` uses floor −1.
- The symbol b means the aperture width in "Arbitrary chamber dimensions" and
  the exit abscissa elsewhere.
- The reflected-stub family needs R = 2A − f > 0. The note states this as a
  condition but should say that it holds for L large enough. Four of the 192
  listed parameter tuples in `checks.py` fail it and are skipped.

## 2. All-pairs theorem for the 3×4 middle chamber

**Family.** End chambers [0, 3] × [0, 3] and [P, P + 3] × [0, 3]. Middle
chamber [D₁, D₁ + 3] × [0, 4]. Unit necks at 1 < y < 2 with independent
lengths X, Y ≥ 1, so D₁ = X + 3, D₂ = Y + 3 and P = D₁ + D₂. Each room has
W = 20, the opposite-side key and 14 interior lattice points. At X = Y = 1 its
area is 32.

**Correct.** The case list is exhaustive. Each room has 91 pairs:

| Case | Pairs | Construction | Traced |
|---|---:|---|---:|
| Same chamber | 27 | direct segment | 16,875 |
| Different rows 1, 2 across chambers | 24 | direct segment in the band | 15,000 |
| Same row 1 or 2, end and middle | 16 | corridor bounce; end-pocket repair at D = 4, u = v | 9,800 + 200 |
| Same row 1 or 2, both ends | 8 | outer-wall bounce or middle pocket | 2,402 + 2,352 + 246 |
| Row 1 end to middle row 3 | 8 | pocket-base congruence | 5,000 |
| Row 2 end to middle row 3 | 8 | fast slope, m = 2/v | 5,000 |

- **Rows 1 and 2.** These cases need only the open band (0, P + 3) × (1, 2),
  which is unchanged. The residual outer pocket uses h = 2 above the band
  (spacing 1) for row 1 and h = 1 below it (spacing 3/2) for row 2. Both are
  less than the interval length min(M, 6 − M) ≥ 2. The traced residuals split
  evenly, with 49, 25 and 49 pairs at M = 2, 3, 4 for each pocket.
- **Row 1 to row 3.** With t = 1, 2a ≡ ±v + U (mod 6). Both residues fail only
  if 2v ≡ 0 (mod 6), which is impossible for v ∈ {1, 2}. The + sign was used
  for 4,150 pairs and the − sign for 850. Side contacts are at heights in
  (2, 3), on the solid flanks.
- **Row 2 to row 3.** The fast part 6mx is a multiple of 6 at every integral
  seam. The slow part 2 − x/B stays in (1, 2) before the middle entrance. The
  final unfolded height 1 + 6mv = 13 folds to 3 modulo 8.
- **Reversal.** x ↦ P + 3 − x maps the family to itself with D₁ and D₂ swapped.
  The script builds right-end constructions this way and traces them in the
  actual room.

The controls confirm that the new pocket height matters. At X = Y = 4, d201's
h = 1 entry a = 1/2 hits a corner in the h = 2 pocket, and the note's
a = 1/3 reaches the target. The fast slope with m = 1 for v = 1 (unfolded
height 7) hits a corner. With m = 3 (height 19 ≡ 3) it reaches the target.

## 3. Sufficient condition for heights H₀ and H

**Correct with gaps.** The final unfolded height measured from the middle
entrance copy is 1 + v/B + (2H₀m − 1/B)v = 1 + 2H₀vm. It folds to y modulo 2H
exactly when 2H₀vm ≡ ±y − 1 (mod 2H). An integer m exists exactly when
gcd(2H₀v, 2H) divides one of the two right-hand sides.

`checks.log`, Part B, traces the condition in six named room shapes, each with
five length pairs. All 350 rays that satisfy the condition hit their targets.

*Gaps (low).*

- The seam argument needs m·x to be an integer at every integral seam. So m
  must be a positive integer, and S must have an integral abscissa. The note
  implies both through "the same row-2 construction".
- The end chamber must satisfy F < 1 and F + H₀ > 2 so that the band and the
  source are interior. The note says "containing the same unit band".

*Observation.* The condition never holds for y = 2, because ±2 − 1 is odd.
That row is already covered by band segments. The first height where it fails
for a row above the band is H = 5 with H₀ = 3: targets at y = 4 for v = 1, 2.
So a 3 × 5 middle chamber isn't covered by this note. The note's "It is not
automatic for all rows" is accurate.

## 4. Status claims

- **Counts: correct.** STATUS.md reads 6 COVERED, 274 PARTIAL, 4,294 OPEN after
  d200 and d201.
- **4×3 middle chamber: correct.** The note proves nothing for width 4. With
  w = 4 the return period changes, and the d201 interval bounds no longer
  apply as stated. The newer unreviewed note `bbbb/l1-chamber-general.md`
  doesn't close this case either; its own text says the aligned layout isn't
  closed.
- **General displaced mouths: correct.** The note proves sufficient conditions
  and explicit families only, and the K = 2A residual is closed only by one
  reflected-stub family.
- **"First outstanding area, 32": wrong.** L2 covers area ≤ 20. The word has
  uncovered rooms of area 21 to 31. `checks.log`, Part D, confirms two named
  examples with aligned unit necks at 1 < y < 2:

  | Chambers | Necks | Area | Lattice marks |
  |---|---|---:|---:|
  | 2×3, 2×3, 2×3 | 1, 2 | 21 | 6 |
  | 3×3, 1×3, 3×3 | 1, 1 | 23 | 8 |
  | 3×3, 3×3, 3×3 (d201) | 1, 1 | 29 | 12 |

  The first two have marks in at least two chambers, and no reviewed theorem
  covers them. d201's review made the same claim. The claim holds only within
  rooms whose chambers are all at least 3 × 3.

## Errors and fixes

1. **Medium (status).** "At the first outstanding area, 32" is wrong. *Fix:*
   "The first open area is 21, for example three 2 × 3 chambers with necks 1
   and 2. Among rooms with all chambers at least 3 × 3, the first open area is
   32." The same correction applies to d201's review, under "First case still
   open".
2. **Low (neck map).** State the middle chamber floor. *Fix:* "the middle floor
   is below 0, so the left neck is strictly inset".
3. **Low (notation).** b is both an aperture width and an exit abscissa. *Fix:*
   rename the aperture width, for example to β₀.
4. **Low (reflected stubs).** *Fix:* "choose L ≥ 8 with
   2L > 8H₁j − 16H₀i − 1, so R > 0".
5. **Low (H₀, H condition).** *Fix:* "for a positive integer m and an
   integral source abscissa", and add the observation that y = 2 never
   qualifies.
6. **Scope.** The theorem covers lattice marks only. Real marks (L3) aren't
   treated.

## Which lemma does this advance, and what is the first case still open?

**L1.** The note adds a third member to the lighting tail for the three-chamber
word: the 3 × 4 middle chamber is lit for every pair of independent neck lengths. It also
gives reusable tools:

- the neck phase map;
- two exact slope formulas for displaced unit mouths;
- a row-1 pocket-base construction valid for any integral middle height;
- a gcd test for row-2 sources.

The K = 2A residual from d201's snapshot2 now has one explicit lit family,
including long stubs.

**First case still open.**

- **By area, in this word:** area 21, for example chambers 2×3, 2×3, 2×3 with
  necks of lengths 1 and 2. Area 23 has chambers 3×3, 1×3, 3×3 with length-one
  necks. The middle-width-1 case can't use any middle pocket of width 3.
- **Along the note's own direction:** the 3 × 5 middle chamber between 3 × 3
  ends. A row-2 end mark to a row-4 middle mark fails the gcd condition, and
  the row-1 construction doesn't apply to that source.
- **Displaced mouths:** the general case, including the first branch where α
  is in (1, 2).

**Smallest W ≤ 20 room not covered:** area 21 in this word, as above.

## Ledger effect

**No count change.** `LLLLRRLLRRLLLLRRLLRR` is already PARTIAL after d200 and
d201, and it can't become COVERED. Chamber widths, end heights, middle heights
other than 4, neck heights, aperture positions and real marks are all still
open.

The coordinator should add to the d200/d201 row in STATUS.md that d202 adds
the aligned 3 × 4 middle chamber for all neck lengths. It should also replace
"first open area 32" with 21 wherever it was recorded. The adjacent key
`LLLLRRLLLRRLLLLRRLRR` gains one explicit lit family, not a length region. It
stays OPEN.
