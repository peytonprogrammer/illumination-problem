# D211: review of the general collar theorem, the shoulder extension, and the shear

Date: 2026-11-23. Reviewer: independent referee.
Reviewed file: [snapshot.md](snapshot.md).
Checks: [checks.py](checks.py). The full run takes 15.7 CPU-seconds, single
process, under `nice -n 10`. It reports 0 failures and 0 travel mismatches.

To rerun it, use `nice -n 10 python3 -B checks.py`. To run one part, pass
any of `ineq A wrong ties B C`.

The tracer in `checks.py` is new. It works in integer coordinates scaled by
|q| horizontally and |p| vertically, so every step moves one unit on each
axis. At a lattice point it counts the four incident cells. Four cells means
an interior point. Two cells sharing an edge means a straight wall, so the ray
reflects. Anything else is a corner, so the trace stops. Every room is checked
for connectivity, no holes, and no diagonal pinch before it's traced.

Rooms used: nine hand-made feet for (A), one hand-made shoulder room for (B),
and a21 ranks 11 and 18 from `seed-profile-a21/paths.json` for (C). No search
over rooms, directions, or words was run. Every traced direction is the one the
note's construction prescribes, or a stated control.

## Verdicts

| # | Claim | Verdict |
| --- | --- | --- |
| A | Collar theorem, regular vertical first entry, arbitrary foot | CORRECT, with presentation gaps |
| B | Rectangular-shoulder extension and the signed-phase criterion | CORRECT, with presentation gaps |
| C | Shear conversion with Λ = 2 lcm(slice heights) | CORRECT. The B_y^45 bound is true but weak |
| | **Overall** | **CORRECT WITH GAPS** |

No counterexample was found. Every gap is a missing sentence, a loose
constant, or a scope remark.

## Claim A: the collar theorem

### The inequalities hold

- **Source leg.** Regular vertical entry means every lattice point on the
  vertical ray before entry has four room cells, and the one reflection is at
  a straight horizontal wall. So both unit columns beside x₀ are open over the
  whole leg. A tilt that moves the ray less than one unit stays in them. The
  condition |s|(D+1) < 1 is sufficient. |s|D < 1 would already do.
- **|s| < 4w/L.** The denominator D+2L+2h−d exceeds L because d < L, and
  |Δ| < 4w.
- **|s|(C+H) < 1/2.** With d < d₀ you get C+H < (D+d₀+2H)/2. Then
  L ≥ 4w(D+d₀+2H) gives the bound. The extra 1 in K is slack.
- **Deep targets.** For d ≥ d₀ you get |x−x₀|(D+1)/(D+d) ≤ (w−2)(D+1)/(D+d₀) < 1.

`checks.py ineq` checks the worst case (h = 0, d = d₀−1, largest |Δ|) exactly
for 1,440 parameter cases with w ≤ 8, D ≤ 12, H ≤ 9, and L ∈ {K, K+1}. All
pass. The largest values are |s|(C+H) = 0.243 and |s|(D+1) = 0.055, so K has a
factor of about 2 to spare even inside the proof.

### The column claim and the outgoing side hold

- **First-wall depth.** In a polyomino, two vertically adjacent room cells
  share an open edge. So column c is open from the far mouth down to the first
  missing cell, and h is constant across the column. Overhangs below a closed
  cell don't matter, because the ray never passes that first wall.
- **Columns stay inside the strip.** If m is half-integral, its column is
  [m−½, m+½]. If m is integral, a < m < a+w gives [m−1, m+1]. Both lie inside
  [a, a+w].
- **Integral midpoint.** The floor hit is at m+sC with 0 < |sC| < ½ on the
  outgoing side, so it's inside a unit wall edge. The ascent moves farther
  into the outgoing side. The descent may start on the deeper side. It crosses
  x = m at relative depth h−C < h, where both cells are open, so the crossing
  is through an open edge. If h = C, the crossing point (m, L) has four room
  cells, because h ≥ 1 on both sides. If h = 0, the reflection is at depth L
  strictly inside the outgoing wall.
- **Far-mouth crossings.** Both crossings are within ½ of m and nonzero offset
  from it, so they avoid every lattice point except (m, L) in the h = C case.

### Traces

The feet are built with a = 3 and an irregular three-row upper chamber. Its
top row is offset, so some up-going vertical rays hit a reflex corner and are
correctly excluded as irregular. Sources use both vertical directions, with
D ∈ {1, 2, 4, 5}.

| Foot | Shape | Strip-column first depths for w = 2, 3, 4, 5 |
| --- | --- | --- |
| stepped | staircase, every column a different depth | [2,3], [2,3,4], [2,3,4,5], [2,…,6] |
| overhang | left mouth columns closed, room continues under them, extra reflex step | [0,5], [0,4,5], [0,0,4,5], [0,0,4,4,5] |
| notch | two floor notches of depths 2 and 1 | [4,2], [4,2,3], [4,2,4,3], [4,2,4,4,3] |

At L = K and L = K+1, `checks.py A` traces every pair of regular vertical
source and interior strip mark. That's 170,950 traces: 53,362 vertical,
114,366 deep, 2,352 half-integral, and 870 integral-midpoint. All reach the
target. In every trace the axial travel at arrival equals the predicted
D+2L+2h−d or D+d, so each trace follows the constructed itinerary and doesn't
land on the target by accident.

**Controls show the tests can fail.**

- **Wrong side.** Aim into the deeper column at an unequal integral midpoint
  and the construction fails 1 of 7 to 6 of 9 shallow targets per source. For
  example, in the stepped foot with w = 4, S = (4,−1), and L = 337, target
  (6,1) on the deeper side hits the corner (5,340). In the overhang foot, a
  deeper-side seed from (4,−1) to (6,2) hits (4,−2) in the upper chamber. The
  outgoing-side rule is necessary, not decoration.
- **Ties.** At 72 equal-depth integral midpoints, both tie choices succeed.
- **Below K.** On a sampled grid of L < K, the constructed shallow seeds do
  fail for some sources. The largest failing L is 77, for the stepped foot
  with w = 5, S = (5,−2), D = 2, where K = 621. Every other source has its last
  failure at L ≤ 74, and 52 of the 66 source and direction cases never fail on
  the grid. K is
  sufficient and about 8 to 30 times larger than the observed need.

### Gaps

1. **Medium (scope of the tests and of the novelty).** For w = 2 the only
   interior abscissa is a+1, so x = x₀ always and the theorem reduces to the
   vertical ray. For w = 3, x ≠ x₀ forces |x−x₀| = 1, so m is always
   half-integral. The integral-midpoint step, which the note calls the key
   step, first occurs at w = 4. This review therefore added w = 4 and 5. The
   note should say that the outgoing-side argument matters only for w ≥ 4.
2. **Low.** Define "regular vertical first entry" explicitly: every lattice
   point on the vertical ray before depth 0 has four room cells, except one
   straight horizontal wall point where it reflects, and (x₀, 0) has four room
   cells. The source-leg paragraph uses exactly this.
3. **Low (loose constant).** The note bounds the denominator by 4B_y using
   D ≤ 2B_y and L+H ≤ B_y. The upper box, the strip, and the foot stack
   vertically, so D ≤ 2U with U+L+H ≤ B_y. That gives D+2L+2H ≤ 2B_y, and the
   construction gives at most 2B_y−1.
4. **Low.** Both x and x₀ lie in {a+1, …, a+w−1}, so |x−x₀| ≤ w−2 and
   d₀ = (w−2)(D+1) suffices for the deep case. This tightens K slightly and
   changes no argument.

**Surviving statement.** As stated in the note, with the denominator bound
improved to 2B_y−1 and the remark that w ≤ 3 never uses the integral-midpoint
case.

## Claim B: the rectangular shoulder and the phase criterion

### The argument holds

- **Oblique entry.** For s in J(t) = (b/t, b/(t−A)), the selected visit has
  0 < e(s) < As, and the previous visit is at e−2As < 0. The abscissa
  increases from −b, so the ray never reaches the rectangle's left wall. It
  stays left of w, which is at most the right wall. Earlier bottom visits are
  at x < 0 on the rectangle floor. The only corners near them are (0,0) and
  the rectangle corners, and the ray avoids both.
- **Deep targets.** The phase e(s)+ds = (t₀+d)s−b sweeps more than 2w over J₀
  once d ≥ d₁. Either target image, x or −x modulo 2w, works.
- **Shallow targets.** sup J ≤ U and e(s) < As give
  0 < e(s)+s(d+2H) < s(A+d₁+2H) ≤ 1. The left side of the matching equation
  has derivative t+2L+2h−d > d₁+4w/|J| on J, so it sweeps more than 4w.
- **Folding.** The developed floor coordinate is σm+2wn+δ with
  δ = (e+sd)/2 ∈ (0, ½). It folds to m+σδ, so σ = −1 reaches the left side from
  a rightward entry. The visit stays within δ+hs < ½ of m. The integral-m
  descent and ascent arguments are the same as in (A), with δ in place of sC.
- **Constants.** t₀ = O(B²), 1/|J₀| = O(B⁴), d₁ = O(B⁵), t = O(B⁶),
  1/|J| = O(B¹²), and the length cutoff is O(B¹³). These all check. Because
  2w/|J| ≥ t, every seed denominator t+2L+2H is at most 3L+2H, which is
  linear in the enlarged box.
- **Phase criterion.** The elimination gives
  2θ ≡ α+β+(d−B)s−c (mod 2w). The derivative of α(s)+Ls−θⱼ(s) is
  L+(D+B−d)/2, and the length condition follows. The converse is a
  restatement. The criterion is a correct reformulation. It proves nothing
  new by itself, and the note doesn't claim that it does.

### Traces on one shoulder room

The room has a rectangle [−3, w+1] × [−A, 0] above the strip [0, w], and a
stepped foot with column depths 1 (left of the strip and column 0), 3
(column 1), and 2 (column 2 and beyond). So i = 2 gives an integral midpoint
m = 1 at a step, and the rule picks σ = −1.

| w | A | Source | d₁ | J | L_min | Traced at L_min and L_min+1 | Failures |
| --- | --- | --- | ---: | --- | ---: | --- | ---: |
| 3 | 2 | (0,−1), b = 0 | 9 | (0, 1/38) | 238 | all 474 + 476 pairs | 0 |
| 4 | 3 | (0,−2), b = 0 | 13 | (0, 1/48) | 398 | all 1,191 + 1,194 pairs | 0 |
| 3 | 2 | (−1,−1), b = 1 | 46 | (1/61, 1/59) | 10,844 | all 90 shallow, 538 sampled deep, each L | 0 |

For b = 1 the deep targets are sampled (every 97th depth, the first 120 above
d₁, and the last 40). Each is a direct sweep, and a full pass would exceed the
CPU budget.

Below L_min, the shallow equation often has no solution in J. That's the
expected way to fail. Every seed it does produce is legal.

The 6 × 2 shoulder with b = 1 needs L ≥ 10,844. That confirms the note's own
warning that these constants give no census-scale guarantee.

### Gaps

1. **Low.** "Sources strictly over the opening have vertical entry as above"
   should say these are covered by Claim A with D = z. Sources at x = w or
   right of the strip follow by reflection. Say so in one line.
2. **Low.** The oblique entries satisfy 0 < e(s) < As, strictly. The note
   writes ≤ in one place.
3. **Low.** In the phase criterion, state that the source leg is regular for
   every s in J, and that the transverse phase convention (phase increases
   with travel) is the one that makes the slope of R in θ equal to +1 on every
   itinerary, including after reflections off vertical foot walls.

**Surviving statement.** As stated in the note.

## Claim C: the shear

### The map is an affine automorphism

For a polyomino, every vertex has an integral abscissa. The vertical slices
over (k, k+1) are the maximal runs of cells in column k. In the four-copy
translation surface, each run of height h gives a vertical cylinder of
circumference 2h. On each unit band, the map v ↦ v + Λu is well defined on the
circle ℝ/2hℤ because Λ ≡ 0 mod 2h. Here u ∈ [0,1] is the offset from the band's
left boundary in the developed chart. At u = 0 the shift is 0, and at u = 1
it's Λ ≡ 0. So every point on every integral vertical line is fixed, from
both sides.

- **Reflected seams.** A seam across a vertical wall joins a band in one copy
  to a band in the x-reflected copy. In the developed chart this is still
  "right boundary of the left band, left boundary of the right band", so the
  argument above applies. Wide cylinders, where several unit columns have the
  same run, are handled the same way.
- **Fixed points.** All lattice marks and all vertices, convex ones included,
  lie on integral vertical lines, so the map fixes each of their four copies.
  Convex corners are regular points of the surface, but they're still fixed,
  and that's what legality needs.
- **Legality.** The map is a homeomorphism with constant derivative
  ((1,0),(Λ,1)), and it permutes, in fact fixes, the forbidden set. So it maps
  a legal segment from a copy of S to a copy of T onto a legal segment between
  the same copies. Primitivity and the nearest-j bound |q′| ≤ Λ|p|/2 both
  check.

### Traces on the named rooms

| Room | Seed | Slice heights | Λ | Sheared directions traced | Result |
| --- | --- | --- | ---: | --- | --- |
| rank 11 | (1,1)→(3,6), (−24,5) | 1, 2, 3, 5 | 60 | j = ±1, ±2, +3, up to (−24,−4315) | all reach T |
| rank 18 | (2,1)→(5,6), (23,−5) | 1, 2, 3, 4 | 24 | j = ±1, ±2, +3, up to (23,1651) | all reach T |

Every sheared trace has the same transverse travel as the stored seed: 24 for
rank 11 and 69 for rank 18. That matches the image segment M·v, which keeps
the horizontal component.

**Control.** If you use Λ/2 = lcm(h) instead, rank 18 gives (23,271) and
(23,−281), and both hit a corner. There 12 ≢ 0 mod 2·4 for the height-4 slice. For
rank 11, Λ/2 = 30 still reaches T. 30 is 0 mod 2h for every height except
h = 2, and this seed doesn't need that cylinder to agree. The factor 2 in Λ is
needed in general.

### On "polynomial"

- **Formally correct.** With r ≤ 8 there are at most 10 horizontal edges, so
  at most 10 support levels and 45 possible heights. Then
  Λ/2 = lcm(h) ≤ B_y^45. For a fixed reflex budget this is a polynomial, but
  its degree is C(r+2, 2), which grows with r.
- **Weak in practice.** The heights are at most B_y, so lcm(h) also divides
  lcm(1, …, B_y) ≈ e^{B_y}. That bound is smaller than B_y^45 for every
  B_y below about 230, which covers every census room. For the two named
  rooms, B_y = 7. The note's bound gives 7^45 ≈ 10^38, while lcm(1,…,7) = 420,
  and the actual values of Λ/2 are 30 and 12.
- **Conditional.** The conversion needs a seed with min(|p|,|q|) ≤ M. The note
  says plainly that no polynomial M is known for all lit pairs. The a21
  profile gives an M on that slice only. That's an observation, not a theorem.

### Gaps

1. **Low.** State that each band's offset is measured in the translation
   chart. In an x-reflected copy, the developed left boundary is the physical
   right side.
2. **Low.** Add lcm(h) | lcm(1, …, B_y) next to B_y^45. It's the useful bound
   at census scale.
3. **Low.** "Polynomial" should read "polynomial of degree C(r+2,2) for fixed
   r", so readers don't take it as uniform in r.

**Surviving statement.** As stated in the note, with the bound written as
|q| ≤ min(B_y^45, lcm(1,…,B_y))·M for r ≤ 8.

## Overclaim and scope

The note is careful. Its first line says the unrestricted collar and the
denominator claims remain open, and its last paragraph says the same. The
remaining scope issues are:

- **Novelty of (A).** The integral-midpoint case only appears for w ≥ 4. For
  w = 2 the theorem is the vertical ray, and for w = 3 it's the half-integral
  case only.
- **Size of the constants.** The (A) threshold K is linear in w(D+wD+H) and
  conservative by a factor of about 8 to 30 on these rooms. The (B) threshold
  is O(B¹³) and gives L_min = 10,844 for a 6 × 2 shoulder.
- **Phase criterion.** It's a correct criterion. The open case it names (an
  irregular upper chamber with oblique entry near an interior partial-mouth
  endpoint, facing a stepped foot) stays open.
- **Links.** The relative links to the d209 and d184 reviews resolve from
  `qclass-closure/bbbb/`.

## What this review settles

- (A) holds on 170,950 exact traces over three feet with steps, an overhang,
  notches, and several reflex corners, for w = 2 to 5 and D = 1 to 5.
- The outgoing-side rule is necessary: aiming at the deeper side fails on all
  three feet.
- (B) holds on one shoulder room, for b = 0 and b = 1 and both midpoint
  parities, including σ = −1 at a step.
- (C) is a valid multi-twist. Sheared seeds with axial components up to 4,315
  trace legally to the same target. Halving Λ breaks it on rank 18.
