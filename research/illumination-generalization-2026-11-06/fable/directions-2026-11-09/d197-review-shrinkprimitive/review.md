# Review of d197: shrink descent on the primitive (n,n+1,n+2,n+3) family

Advances: L1 (referee review of the shrink-descent route's first test).

Date: 2026-11-23. Reviewer: independent referee.
Reviewed file: [snapshot.md](snapshot.md). Bases: [PROGRAM.md](../PROGRAM.md)
(L1–L4, shrink-descent stopping rule), the proposal
`qclass-closure/bbbb/l1-route-shrink-descent.md`,
[d196 review](../d196-review-crossreduction/review.md), and the d152 entry in
[RESULTS.md](../d70-writeup/RESULTS.md) §11.

Follow-up reviewed in the section "Follow-up: snapshot2.md" below:
[snapshot2.md](snapshot2.md), a copy of `qclass-closure/bbbb/l1-shrink-dark-transfer.md`.

Checks: [checks.py](checks.py), output [checks.log](checks.log). The log has
28 PASS lines and 0 FAIL in 0.25 CPU seconds. It contains exact `Fraction` and
`sympy` identities, arithmetic over n = 3..50, and six named realizations of
the chart. No ray, direction, word, room-size, or illumination search was run.
To rerun it, use `uv run --no-project --with sympy python checks.py`.

## Verdict

**Correct with minor gaps.** Every computation is exact and every claim is
stated as a failure of a transfer rule, not of illumination. The note meets the
stopping rule's alternative deliverable: it names the first implication that
fails.

| # | Claim | Verdict |
| --- | --- | --- |
| 1 | Admissible horizontal moves exist | **Correct.** Add that normalization forces the primitive representative (Low 1) |
| 2 | v − s·e_j leaves the line; vertical analog | **Correct** |
| 3 | Affine side test; averaging identity; no common sign list | **Correct** |
| 4 | Terminal-rectangle criterion s·r ∈ hZ; corner miss | **Correct.** One step in the corner argument should be stated (Low 2) |
| 5 | Parity obstruction for 4 \| h, odd Δy, s ∈ {1,2} | **Correct.** It is a special case of a 2-adic statement, and the step bound causes it (Medium 1) |
| 6 | First open case; no overstatement | **Correct with gaps.** Two different first-open-case statements; the final one omits alternatives (Medium 2) |

## Per-claim checks

### 1. Admissible horizontal moves

- Two marks have two x-coordinates, so at most two of the four open wall gaps
  contain one. A mark-free gap exists.
- Every gap is at least n ≥ 3 > s, so all gaps stay positive (log §1).
- With no mark line inside the gap, the coordinate order is unchanged. For
  orthogonal polygons with distinct coordinates, simplicity and cell occupancy
  depend only on that order (d196 review §e). Marks move by an integer, so they
  stay interior lattice points.
- Deleting any one index of 0..3 leaves two consecutive indices. So the three
  unchanged gaps contain n+i and n+i+1, and their gcd is 1 (log §1, n = 3..50).

Low 1: RESULTS defines normalized as "horizontal edge lengths have gcd 1". The
horizontal edges link all five x-lines, so this gcd equals the gcd of the wall
gaps. A normalized room on span(v) is therefore realized at v itself, not at
λv. The note says "take a positive integral marked realization projecting to
v". It should say that normalization forces this choice.

### 2. Leaving the line

If v − s·e_j = λv, any unchanged positive coordinate gives λ = 1 and then
s = 0 (log §2, symbolic, and n = 3..50 for s = 1, 2). The vertical claim is the
same calculation for any primitive positive b with a positive-gap shrink.
Collapses change the chart, as the note says. The conditional positive result
for rank ≥ 2 vertical factors is stated correctly as conditional.

### 3. Affine side test and averaging

- Each reflection in a vertical line x = c + αt is x ↦ 2(c + αt) − x, which is
  affine in t. Compositions stay affine. The determinant is x₁y₂ − y₁x₂ with all
  y fixed, so it is affine in t. This holds even when S moves (log §3).
- For F(t) = F(0) + tB with opposite signs, a strict sign on [0, s] holds if
  and only if |F(0)| > s|B|. Integrality gives |F(0)| ≥ 1 and nothing about B.
- Σ_j (v_j/L)(v − e_j) = (1 − 1/L)v holds symbolically. The two-unit version
  gives (1 − 2/L)v (log §3). When marks lie on wall lines, the determinants are
  homogeneous linear in the gaps. So signs common to all four shrinks hold at
  v. This is convexity of the open cone of a fixed itinerary.
- The quantifier remark is right. The premise gives one itinerary per
  successor, so it gives no common sign list.

### 4. Terminal-rectangle transfer

The chart 3,4,2,0,1 has x3 < x4 < x2 < x0 < x1 and the same order in y. The
rightmost column (x0, x1) × (y0, y1) is bounded by the bottom wall y0 (x0..x1),
the right wall x1, and the top wall y1 (x2..x1). The only wall on x = x0 runs
from y4 to y0. So the left side opens into the top slab, (x0, y0) is a reflex
corner, and (x0, y1) is a smooth point of the top wall. Its width is
g4 = n + 3 and its height is h = b4 (log §6).

An excursion enters at x0, reaches x1 once, and leaves at x0. The unfolded
height changes by 2(w − s)r in the short room and 2wr in the restored room.
Phase mod 2h fixes folded height and vertical direction away from {0, h}. So
the exit state is unchanged if and only if 2sr ∈ 2hZ, that is s·r ∈ hZ. The
log confirms this on 13,920 exact named cases. All excursions share |r|, so
one condition covers the path.

Low 2: The far-wall heights differ by s·r ∈ hZ, not 2hZ. When s·r is an odd
multiple of h, the folded height is h − z′ instead of z′. The corner set
{0, h} is symmetric under z′ ↦ h − z′, so the corner-miss argument holds
(log §4). State this step.

### 5. Parity obstruction

- Reflection in an integer line, x ↦ 2c − x, preserves x mod 2. So every
  unfolded image of T is congruent to T mod 2, and Δy is odd (log §5).
- A legal connecting path has rational direction (p, q) in lowest terms. The
  integral displacement is k(q, p) with k an integer, so p is odd.
- The criterion needs q | s and h | (s/q)p. For s ∈ {1, 2}, (s/q)p has 2-adic
  valuation at most 1, so 4 | h excludes it. Checked for h = 4..100 (log §5).
- A horizontal path has Δy = 0, so it can't join the marks.
- The realization class is consistent with LLLRLLLRLR. The y-gap vector is
  (y4−y3, y2−y4, y0−y2, y1−y0), so h is the fourth entry. (1, b2, b3, 4k) is
  primitive because of the leading 1. Interior marks with odd Δy exist left of
  x0, for example (x0−1, y0+1) and (x0−1, y0+2), because g3 = n + 2 ≥ 5 and
  h ≥ 4 (log §6, six named realizations).

Medium 1: State the obstruction in its general form. Same-exit transfer
through the cap is impossible whenever v2(h) > v2(s) + v2(yT − yS). The log
checks the odd-Δy case for h ≤ 64 and s ≤ 8. So the cause is the step bound
s ≤ 2, not 4 | h. For example, s = 4 with h = 4 transfers every q = 1 path. A
step set commensurate with h does not repair it uniformly either. s = hq works
only for slope denominator q, and q is not bounded for successor paths. That
repair needs a slope-period bound, which is the H(C)-type estimate the
stopping rule says to stop on.

Context, not an error: the example pair above is joined by a vertical segment
in every room. The obstruction concerns cap-using paths only. It matters for
pairs whose successor paths all enter the cap, as the note says.

### 6. First open case and overstatement

No claim overstates. The note says "It is not a failure of illumination" and
"no dark instance or counterexample to descent is established". The d152
summary matches RESULTS §11: the uniform tail fails at W = 22, and one-way
descent is not contradicted.

Medium 2: The note states the first open case twice. "Initial transfer test"
says "uniform geometric transfer or exclusion of this primitive marked
product". The last section asks only "a path avoiding that cap, or a different
admissible gap". The final question omits two alternatives that the note
itself names: a changed exit state compensated later, and vertical-axis
shrinks. In the class (1, b2, b3, 4k), every b1 shrink is a collapse and
leaves the chart. Replace both statements with the single statement below.

## Follow-up: snapshot2.md (dark transfer at one cap visit)

**Verdict: correct.** Both items hold as stated, and the note claims no more
than it proves. Log §7 holds the arithmetic.

### (a) Single-excursion obstruction: correct

- **Exit phase θ + 2dr.** The note orients the vertical unfolding so the phase
  increases along travel, and r = |p|/q is the absolute slope. Then a regular
  excursion of width d adds unfolded vertical travel 2dr, so the exit phase is
  θ + 2dr mod 2h. With the horizontal direction fixed (right on entry, left on
  exit) and |slope| fixed, the phase determines position and velocity.
- **Disjointness.** Over the same entry θ, the exits differ by 2sr. So they
  coincide if and only if 2sr ∈ 2hZ. The cap is deterministic, so each graph
  is a partial function, and the graphs are disjoint otherwise. A corner hit in
  the long cap removes θ from the long domain, which only strengthens this.
- **Parity step.** 2sr ∈ 2hZ is equivalent to hq | s|p| (log §7). An S-to-T
  path has odd unfolded Δy = k·p, so p is odd (log §5). With 4 | h, hq | s|p|
  needs 4 | s|p|, which is impossible for s ≤ 2. Same correction as Medium 1:
  the general condition is v2(h) > v2(s) + v2(Δy).

### (b) One-visit gluing criterion: correct, both directions

- **Necessity.** Cut a one-visit path at its entry and exit crossings of the
  mouth. The first piece lies in the common exterior and ends at a regular
  entry, so its phase is in A_S(r). The excursion is legal at width d, so the
  phase is in A_d. The exit phase θ + 2dr starts the last piece, which reaches
  T with no further entry, so it is in B_T(r).
- **Sufficiency.** Pick θ ∈ A_d with θ + 2dr ∈ B_T. Glue the exterior piece,
  the width-d excursion, and the exterior piece to T. Position and velocity
  match at both crossings, and each piece is legal. The result is a legal
  one-visit path.
- **Width independence.** A_S and B_T use only the common exterior, so they
  don't depend on d. Only the restriction A_d does, through corner clearance.
- **Consequences.** Darkness of P empties the d = w intersection. It says
  nothing about d = w − s. Reproducing a short exit at width w needs the entry
  θ − 2sr (log §7), and nothing puts that entry in A_w.
- **Additive order.** The smallest m ≥ 1 with m·2s|p|/q ∈ 2hZ satisfies
  m·s|p| ∈ hqZ, so m = hq/gcd(hq, s|p|). The log checks this on 2,112 exact
  cases. With p odd and 4 | h, v2(gcd) = v2(s), so v2(m) ≥ v2(h) − v2(s).
  That is at least 2 for s = 1 and at least 1 for s = 2, as claimed.

Low 3 (wording): "an odd integer multiple of a unit lattice spacing" means Δy
is odd. Write that instead. Also, the parity step uses the whole S-to-T path,
not only the excursion. Say that p is fixed for the path because |slope| is
invariant.

The first open case in snapshot2 is a regular one-visit path in P_s with no
replacement entry in P. It refines alternative (a)/(c) of the merged statement
above, at one visit and fixed slope. Inclusion of the endpoint sets stays
open, as the note says. The cap-avoidance test recommended below is the
companion question: is A_w closed under the shift −2sr on the entries that
actually reach T?

## Errors and fixes

There are no mathematical errors. Make these fixes:

1. (Medium 1) Add the 2-adic form: no same-exit cap transfer when
   v2(h) > v2(s) + v2(Δy). Say that the bound s ≤ 2 causes it. Say that a
   period-commensurate repair needs a bound on slope denominators.
2. (Medium 2) Merge the two first-open-case statements into the one below.
   List all alternatives.
3. (Low 1) State that normalization forces the realization at v.
4. (Low 2) In the corner-miss step, note that an odd multiple of h maps the
   folded height z′ to h − z′, and that {0, h} is symmetric.
5. (Low 3, snapshot2) Say "Δy is odd" directly, and note that p is fixed
   for the whole path because |slope| is invariant.

## Which lemma does this advance, and what is the first case still open?

It advances **L1** (area bound via one-way descent). It is a method limit, not
progress on the bound. It proves that two transfer mechanisms fail. Darkness
can't stay on the same rank-one product, and same-exit cap transfer can't work
with s ∈ {1, 2} when v2(h) ≥ 2 and Δy is odd.

First open case: take the chart 3,4,2,0,1 with horizontal gaps
(n, n+1, n+2, n+3), n ≥ 3, vertical gaps (1, b2, b3, 4k), and two interior
lattice marks left of x0 with odd Δy. Assume every admissible successor is
fully lit. Does the pair have a legal path in the original room? A proof needs
one of three things:

- (a) a cap-avoiding path in a right-cap successor
- (b) a transferable path for another horizontal gap, or for vertical gap b2,
  b3, or b4
- (c) a transfer that changes an exit state and compensates later

No reviewed result supplies any of them.

## Recommended next step for L1 under this route

The note meets the stopping rule's "first precise implication that fails" a
day before 2026-11-25 20:00 HST. The early-stop clause also applies in
substance. The same-line fallback is blocked, and the only uniform cap repair
needs a slope-period bound.

Recommendation: report the method limit to Daniel now, with the merged
first-open-case statement and the 2-adic obstruction. Allow at most one more
symbolic test before the deadline: a cap-avoidance lemma for (a). Model the
cap of width w′ as a mirror at x = x0 that shifts the phase by 2w′r mod 2h.
Then ask whether a fully lit right-cap successor must join the pair without
entering the cap. If that lemma needs a bound on slope denominators, stop the
route under its own clause. Don't run further gap-by-gap subcases (b).
