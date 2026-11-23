# Review of d198: exterior induction for L1 under shrink descent

Advances: L1 (referee review of the shrink-descent route's exterior-induction step).

Date: 2026-11-23. Reviewer: independent referee.
Reviewed file: [snapshot.md](snapshot.md). Bases: [PROGRAM.md](../PROGRAM.md)
(proof architecture; "Shrink-descent route (selected 2026-11-23)"), the
[d197 review](../d197-review-shrinkprimitive/review.md), and the two d197 notes
([snapshot.md](../d197-review-shrinkprimitive/snapshot.md),
[snapshot2.md](../d197-review-shrinkprimitive/snapshot2.md)).

Checks: [checks.py](checks.py), output [checks.log](checks.log). The log has
25 PASS lines and 0 FAIL in 2.2 CPU seconds. It uses only `fractions` and
`math`. It simulates only the rays the note names: the four starts of absolute
slope 1/q from S and T. The rooms are the named family, chart 3,4,2,0,1 with
horizontal gaps (n, n+1, n+2, d) and vertical gaps (1, b2, b3, h), for
n = 3..12, h ∈ {8, 12, 16}, (b2, b3) ∈ {(1, 1), (2, 3)}, d ∈ {w, w−1, w−2}, and
m = 1..6. No ray, direction, word, or room-size search was run. To rerun it,
use `python3 checks.py > checks.log`.

## Verdict

**Correct with minor gaps.** Every claim checks exactly, and the note states
its example as a method limit, not a dark pair; it doesn't advance L1 beyond
d197's open case, and the shrink route should stop.

| # | Claim | Verdict |
| --- | --- | --- |
| 1 | Eight-wall closed exterior; first-hit correspondence; at most four first phases, each in (1/q)Z mod 2h | **Correct** |
| 2 | Symbolic family: travel totals, one-visit emptiness at d = w and nonemptiness at w−1, w−2, strip bounds, corners, chart compatibility | **Correct with gaps.** The suffix bound is not stated (Low 1) |
| 3 | k-visit recurrence X_{k+1} = C_d(E_r(X_k)) and its exactness | **Correct with gaps.** C_d must also exclude a corner exit (Low 2) |
| 4 | Unbounded visits at q = 2mL | **Correct** |
| 5 | d197 corrections carried, including v2 with unfolded ΔY | **Correct.** It also fixes an imprecision in the d197 review |
| 6 | "Finite-return induction needs a denominator bound"; first open case | **Correct, not overstated.** The open case omits the horizontal gaps (Low 3) |

## Per-claim checks

### 1. Closed exterior and first-hit correspondence: correct

- With x3 < x4 < x2 < x0 < x1 and the same y order, the open room's slabs
  are (x3, x4), (x3, x0), (x2, x0), and (x2, x1), bottom to top. Clipping at
  x0 merges the top two into (x2, x0) × (y2, y1). The closed exterior is
  (x0,y4), (x0,y1), (x2,y1), (x2,y2), (x3,y2), (x3,y3), (x4,y3), (x4,y4). It
  has eight walls, six left turns and two right turns, with reflex corners
  (x2, y2) and (x4, y4). The mouth M lies inside the right wall x = x0 from
  y4 to y1 (log §1, 60 rooms × 3 widths).
- The open and closed rooms differ only on the segment M. So the two
  trajectories are the same line with the same reflections until the first
  contact with M. In the open room (x0, y0) is a reflex vertex and (x0, y1)
  is a smooth point of the top wall. The note stops on both endpoint events
  separately, which is right. Log §1 compares 1,440 named rays event by event.
- Four signed starts give at most four first phases. In an unfolding across
  integer walls, every mouth image has integer abscissa X. The height there is
  yS + (X − xS)p/q, which is in (1/q)Z. Folding by integer walls keeps the
  grid. Log §1 confirms both facts.
- The additive order of 2sp in Z/2hqZ is 2hq/gcd(2hq, 2sp) = hq/gcd(hq, sp).
  A nonempty set closed under the shift contains a full orbit. So a set of at
  most four phases can't be closed when the order exceeds four.

### 2. Symbolic family: correct with gaps

- Gaps: a = x0 − x2 = n+2 and w = x1 − x0 = n+3, so q = 2w + 2a − 4 = 4n + 6
  and gcd(1, q) = 1.
- From S = (x2+1, y0+2), a rightward start meets M after a − 1. A leftward
  start reflects at x2 after 1 and meets M after a + 1. The wall x2 spans
  y2..y1, so that contact is regular. T is symmetric. The three totals are
  2d + 2a − 2, 2d + 2a, and 2d + 2a + 2 (log §2).
- Without vertical reflection, a connection needs rise exactly 1, so it is
  upward with horizontal travel q. At d = w the smallest total is q + 2, so
  the intersection is empty. At d = w−1 the smallest total equals q. At
  d = w−2 the middle total equals q. The set formula
  (A_d + 2dr) ∩ B_T and the direct ray simulation agree in every named room
  (log §2).
- (a + 1 + 2w)/q < 2 is equivalent to 2w + 3a > 9. This holds for n ≥ 3.
- Chart compatibility holds. The marks lie in the gap (x2, x0), not in the
  cap gap, so both right-cap shrinks are admissible in d197's sense. Shrunk
  horizontal gaps keep gcd 1. Vertical gaps (1, b2, b3, h) with 4 | h are
  primitive and in the d197 parity class, and Δy = 1 is odd. The marks are
  interior and off all wall lines because h ≥ 8 (log §1).

Low 1: The bound (a + 1 + 2w)/q < 2 covers the prefix and the excursion. The
claim "requires upward motion" needs the whole path, including the suffix. A
downward start falls by up to (2a + 2 + 2d)/q. That bound is below 2 because
2w + 2a > 10 (log §2). Add it. Also note that below y0 in the exterior there
is no floor, so the bound is about staying in the mouth's height range, not
about avoiding a wall.

### 3. k-visit recurrence: correct with gaps

- A_S and E_r use only the common exterior, so they don't depend on d.
  At the mouth, the side fixes the horizontal sign and the phase fixes the
  height and vertical sign. So E_r is a deterministic partial map.
- Cutting a path with k regular visits at its mouth crossings gives
  X_k ∩ B_T ≠ ∅. Gluing pieces with matching states gives the converse.
- Log §3 runs the recurrence for 180 (room, d, k) cases with k ≤ 12. X_k
  matches the direct k-th exit phase of each start. X_k meets B_T exactly
  when that start's k-th exit reaches T before the next mouth contact.
- The phase grid (1/q)Z mod 2h holds for all k, so at most 2hq states occur
  at one slope.

Low 2: Define the domain of C_d as excursions whose far-wall contact **and**
return to M both miss the corners {0, h}. "Legal regular cap excursions"
implies this. But d197 snapshot2 says only "clears the far corners", and the
exit case does occur in the named family. In the room n = 3, h = 8, d = 5,
the start (−q, −1) leaves its second excursion exactly at (x0, y0) (log §2,
info line). A recurrence that tested only the far wall gives a wrong X_2.

Context, not an error: at the family slope 1/q, the full-width room d = w
reaches T after 4 visits for n = 3, h = 8, and after 10 visits for n = 9,
h = 8 (log §3, info line). So one-visit emptiness at d = w says nothing about
the slope as a whole. The note doesn't claim it does.

### 4. Unbounded visits: correct

- In the strip y0 < y < y1, horizontal motion reflects in [x2, x0 + d] of
  width L = a + d. Both wall segments span the strip. Each period 2L returns
  to the start abscissa and direction and contains one full cap visit.
- At q = 2mL the vertical change over q units is at most 1. Heights stay in
  [y0+1, y0+3], inside the strip since h ≥ 8.
- Upward starts with either horizontal sign first reach T at travel exactly
  q, after exactly m visits. Downward starts miss T and have made m visits by
  travel q. All contacts are regular, and the m upward exit heights are
  distinct. Log §4 checks 2,160 named rays for m = 1..6.

### 5. d197 corrections: correct

- λv integral with v primitive gives λ ∈ Z by Bezout. The horizontal edge
  lengths are g4, g3+g4, g1+g2, g1, g2+g3, whose gcd is the gap gcd. So
  normalization forces λ = 1 (log §5).
- Under sr ∈ hZ the restored far-wall height is z′ or h − z′ by the parity of
  sr/h. Both miss {0, h} together (log §5).
- ΔY = kp with k ∈ Z \ {0}, and hq | s|p| gives v2(h) ≤ v2(s) + v2(p) ≤
  v2(s) + v2(ΔY). So v2(h) > v2(s) + v2(ΔY) excludes same-exit transfer.
- The unfolded form is the right one. The d197 review wrote v2(yT − yS).
  That is exact for odd differences only. For an even difference, an image
  2c − yT changes the valuation. For example, yS = 2 and yT = 6 give
  unfolded ΔY = 2 or 4, with v2 equal to 1 or 2 (log §5). The note corrects
  the d197 review here.

### 6. Conclusion and first open case: correct, not overstated

The note claims that any truncation by a visit count depending only on the
room and marks loses genuine fixed-slope connections. Claim 4 proves that.
It says a finite argument over all slopes needs a denominator selection or a
comparison theorem across orbits. That is the honest limit. The note also says
the example is a lit pair joined by a vertical segment, so it gives no lower
bound on the best path's denominator. The note doesn't overstate.

Low 3: The first open case says "the normalized ten-wall chart". Name it
fully: chart 3,4,2,0,1 (LLLRLLLRLR), horizontal gaps (n, n+1, n+2, n+3) with
n ≥ 3. The alternatives listed match the merged d197 statement.

## Errors and fixes

There are no mathematical errors. Make these fixes:

1. (Low 1) Add the suffix bound (2a + 2 + 2d)/q < 2 to the strip argument.
2. (Low 2) Define C_d's domain to exclude a corner at the exit, not only at
   the far wall. Cite the n = 3, h = 8, d = w−1 start (−q, −1) as the case.
3. (Low 3) Name the chart and horizontal gaps in the first open case.

## Which lemma does this advance, and what is the first case still open?

It advances **L1** only as a method limit. It doesn't move the area bound.
It proves three things:

- The closed exterior gives at most four first phases per mark, with no
  closure under the cap shift.
- The fixed-slope one-visit implication from width w to w−s fails in a lit
  family.
- The number of visits needed at a fixed slope is unbounded, so exterior
  induction needs a denominator bound.

The first open case is unchanged from d197. Take chart 3,4,2,0,1 with
horizontal gaps (n, n+1, n+2, n+3), n ≥ 3, vertical gaps (1, b2, b3, 4k), and
two interior lattice marks left of x0 with odd Δy. Assume every admissible
shrink is fully lit. Must the pair be lit in the original room? A proof needs
one of these:

- (a) a cap-avoiding path in a right-cap successor
- (b) a transferable path for another horizontal gap, or for b2, b3, or b4
- (c) a changed exit compensated later, possibly at another slope

## Recommended next step for L1

**Stop the shrink-descent route now.** Its early-stop clause has fired. The
d197 review allowed one more symbolic test and said to stop if it needed a
slope-denominator bound. This note shows that exterior induction needs exactly
that bound. No reviewed result supplies (a), (b), or (c).

Report to Daniel with the three method limits above, the merged first open
case, and a proposed new L1 route. Don't run gap-by-gap subcases of (b). A
new route should not rely on per-slope transfer through a shortened gap. Both
same-exit transfer (d197) and exterior induction (d198) fail on the 2-adic
obstruction or on unbounded denominators.
