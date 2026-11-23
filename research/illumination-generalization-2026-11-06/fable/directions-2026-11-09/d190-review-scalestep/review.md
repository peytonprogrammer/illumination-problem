# d190 review: a scale step at an occupied crossing

**Verdict: PASS WITH CORRECTIONS.** Confidence: high (about 85%) that the
positive theorem is correct as scoped. The corrections concern how the
negative claim is labeled and what the open-case list includes. No proof step
fails.

Date: 2026-11-22. Reviewer: independent referee. Reviewed file:
[snapshot.md](snapshot.md), sha256 `835be639…25552dc`. It's byte-identical to
`qclass-closure/bbbb/l1-crossing-scale-step.md`. Reviewed bases:
`l1-crossing-gate-resultants.md` ([d189](../d189-review-gateresultants/review.md)),
`l1-mixed-seed-normals.md` ([d188](../d188-review-mixedseed/review.md)),
`l1-growth-modes.md` ([d182](../d182-review-growthmodes/review.md)) and
`effective-chamber.md` (d124), which supplies the Fibonacci first hit.

Checks: [checks.py](checks.py), output [checks.log](checks.log). The run takes
0.17 CPU seconds with exact `Fraction` arithmetic. `trace()` is copied verbatim
from d189. The log has 48 PASS lines, several INFO lines and 0 failures.

What the script covers:

- The theorem's identities and inequalities, on fixed grids of small integers
  and rationals. This is arithmetic only, with no rooms.
- The st279 run widths (3, 3, 5), for P = 6 and P = 30.
- The note's two-rectangle junction at b = 2, 4, 6, 8 and 10, with both choices
  of D = a.
- The W=10 ledger realization of LLLRLLLRLR.

The only traced paths are the junction's straight upper branch at the
closed-form speeds 3/(2b) and 1/b. No room, ray, direction, slope, word or
room-size search was run.

## Bottom line

The positive theorem is correct, including every constant. For a fixed sealed
template stretched by (u,t), it gives one ratio bound on darkness:

    a/gcd(a,2d) ≤ K = 16PC²/η³

The bound is uniform in D, c, u and t, and the floor depth d may grow. Two
steps carry the improvement over d189:

- A coset lemma replaces d189's count of 2d bad floor positions, so no
  threshold in d remains.
- Normalized template slope makes u and t cancel exactly in the final
  inequality.

The negative claim is correct in the body: η_phys ≤ w/b. The Advances line
states it more broadly than the argument supports (Medium 1). The appendage
discussion is correctly labeled as an obstruction to the method.

| Claim | Verdict |
| --- | --- |
| Transposed d124 first hit: B ≤ T = 1+F_(3m−1), stability width 1/(2T²), η = 1/(4T²) | **Correct.** The log confirms that no p/q with q ≤ 90 lies in α ± 1/(4·90²) |
| Stretch equivariance: physical speed u(v+kP)/t, seam z = u(e−Bv) | **Correct.** Diagonal scaling commutes with orthogonal reflection |
| P = 2 lcm(1,…,W), or the visited doubled widths; st279 gives 6 and 30 | **Correct.** This resolves d189 Low 1 |
| Gate u(A+tB)v ∈ t(ue−c) + g_A ℤ, g_A = gcd(2Dt, AuP); explicit v_phys; onto index | **Correct.** Exact on 6912 grid lifts |
| Floor coset lemma: two consecutive indices give a corner-free lift | **Correct.** The step 2Dd/(A+tB) lies in (0,D). It holds on 60 enumerated index pairs |
| (1) D ≥ u(a+tB)(L+tB)η²/(4γPt) | **Correct.** gcd \| uPγ and lcm \| 2Dt on 864 tuples |
| Far-wall shift: Q, sup\|v′\| ≤ C(1+t/L), e′ < 0, s·uR < L, δ bound | **Correct.** Holds on 2592 grid cases |
| Downward launch: arrival −d + s(2D−c−ue′) − tB = (2j+1)h; corner step in (0,h) | **Correct.** This route differs from d189's upward launch, and both are valid |
| Final: aLη³ ≤ 16hγPC², so a/γ ≤ K | **Correct.** u and t cancel; L ≥ h and a ≤ L are used correctly |
| Growing depth: d = o(a) covered; a dark rational linear family forces one ratio a:2d | **Correct** |
| (b) η_phys ≤ w/b for every first-hit branch | **Correct** |
| (b) "A uniform first-hit interval in physical slope is impossible even at strictly separated scales" | **Overstated** (Medium 1) |
| (b) Junction example: W=8, two reflex corners, gcds, coprimality, parity | **Correct** at all 10 named rooms |
| (c) Outside-span openings: (1) still necessary; regime D = O(a), t = o(a), d fixed resolved | **Correct** |
| (c) Arm phase 2Hv mod 2w; labeled an obstruction to the method, not darkness | **Correct and correctly labeled** |
| (d) First open cases | **Correct but incomplete** (Low 2) |
| d189 Medium 1 (growing d; two gaps per axis) | **Addressed.** Growing d is proved up to bounded a/γ. The d188 two-gap product is listed as open |
| LLLRLLLRLR realization | **Correct.** Strictly simple, 10 walls, area 8 |

## 1. The upper window

**First hit.** The note swaps the roles of x and y in d124's argument. The
backward ray from the template target has |dx/dy| = α = (3−√5)/2 = 1/φ². It
crosses a horizontal unit edge of a chosen mouth within vertical travel
T = 1+F_(3m−1), where m = 4n. Stopping at an earlier shared mouth is harmless,
because d124's stability preserves the whole cutting word through step T. The
quadratic estimate |α − p/q| > 1/(3q²) gives the closed interval
α ± 1/(4T²), of width 1/(2T²). An interior J of length η = 1/(4T²) fits. The
log checks the Diophantine step exactly at T = 90, the value for n = 1.

The hit is on a unit edge at a nonintegral abscissa, so it's interior to the
mouth. B and e are integers because the target and the walls are lattice.

**Stretch.** A diagonal map (x,y) ↦ (ux,ty) sends orthogonal billiard paths to
orthogonal billiard paths. A template velocity (v,1) becomes (uv,t), so the
physical horizontal speed per unit physical rise is uv/t. The seam point is
u(e−Bv), and the physical rise is tB. The unit-band shift v → v+kP is the
d189 lemma applied in template units. A shift of P is divisible by twice every
run width W' ≤ W. "P may instead be the visited doubled widths" matches d189
Low 1, with st279 at 6 for the visited run and 30 for all runs.

**One unstated hypothesis (Low 3).** The sealed-chamber first hit is physical
only if the template component has no openings other than the labelled shared
mouths. "Sealed" and "label the mouths actually shared" suggest that, but the
note never says that every opening of the template is a shared mouth.

## 2. The short routes and (1)

**Gate.** From c + A·v_phys = u(e−Bv) + 2Dl and v_phys = u(v+kP)/t:

    u(A+tB)v = t(ue−c) + 2Dt·l − AuP·k.

As (l,k) ranges over ℤ², the right side ranges over t(ue−c) + g_A ℤ with
g_A = gcd(2Dt, AuP). The explicit v_phys formula and the index map are exact.
The log confirms the identity on 6912 lifts and finds an index ±1 by Bezout on
all 576 tuples. Each index fixes v, and so the seam point. Different lifts in
one fibre change k and the lower path, never the upper path.

**Coset lemma.** The floor-corner set is {(l,k) : c + d·v_phys ∈ Dℤ}. It's
affine in (l,k), so it's empty or a coset of a subgroup H. The step in l is
2Dd/(A+tB), and it lies in (0,D) because A+tB > 2d. So (1,0) ∉ H, and H is
proper. If both fibres over indices i and i+1 were all bad, H would contain the
kernel K and a vector of index 1. Since the index map is onto with kernel K,
that gives H = ℤ², a contradiction. The argument is complete. It removes
d189's floor threshold aη > 2dP(2d+1), which was the only source of a
d-dependent hypothesis. The log enumerates 60 consecutive index pairs on six
small tuples, with lifts in |l|, |k| ≤ 40, and finds no all-corner pair.

**Failure windows.** The direct route fails when its window u(a+tB)η contains
no point of the progression, so u(a+tB)η ≤ g_a. The floor route fails when the
window holds fewer than two consecutive points, so u(L+tB)η ≤ 2g_L. Both are
the right failure conditions for an open or closed J.

**(1).** gcd(g_a, g_L) divides gcd(auP, LuP) = uP·gcd(a, a+2d) = uPγ. The lcm
divides 2Dt. So g_a·g_L ≤ 2uPγDt, and

    u²(a+tB)(L+tB)η² ≤ 2 g_a g_L ≤ 4uPγDt.

That's (1). The log checks the divisibility on 864 tuples.

## 3. The far-wall route and the final bound

**Shift.** J has length η < P, so some J′ = J + kP has inf|v′| in (Q, Q+P].
Then sup|v′| ≤ Q + P + η. Since B ≥ 1, Q ≤ 1 + R + 2Rt/L, and
C(1+t/L) ≥ 1 + R + P + η + 2Rt/L. So sup|v′| ≤ C(1+t/L). The intercept is
e′ = z/u + Bv′ < R − B − R < 0. With s = t/(u|v′|), the bound
s·uR < tR/Q ≤ L/2 holds. The width of the s interval is at least
t·η/(u·sup|v′|²), which gives the stated δ. The "1" inside Q is never used,
which is harmless.

**Route.** The note launches downward, unlike d189, which launched upward.
After unfolding the floor, the virtual start is at −d and the first roof level
is at +h, a distance L above it. The arrival equation is exact:

    −d + s(2D−c−ue′) − tB = (2j+1)h.

Here 2D − c − z is the horizontal travel and z = ue′ + tB/s. The guards hold:

- **Outward leg.** Any point with x ≤ uR has risen less than s·uR < L from
  −d. So it's below h, and no roof contact in [0,uR] is possible.
- **Return leg.** Roof contacts are 2h/s > uR apart, because 2h > L > s·uR.
  So only the final contact lies in [0,uR].
- **Corners.** The only reachable side is x = D. Its unfolded height changes
  by 2h(D−c)/(2D−c−ue′) between adjacent roots. That's in (0,h) because
  ue′ < 0 < c.
- **Two roots.** (2D−c−ue′)δ > 4h gives two consecutive roots, and
  2D−c−ue′ > D.

The log checks these on 2592 and 72 grid cases.

**Final step.** On failure, D ≤ 4h/δ ≤ 4huC²(1+t/L)²/(tη). Combining this with
(1) cancels u and t:

    (a+tB)(L+tB)η³ ≤ 16hγPC²(1+t/L)².

For B ≥ 1 and a ≤ L, (a+tB)(L+tB)/(1+t/L)² ≥ (a+t)L²/(L+t) ≥ aL. With L ≥ h
this gives a/γ ≤ 16PC²/η³. The theorem's strict inequality then forces
lighting. The constants depend only on n, W and R, as stated.

**Growing depth.** γ ≤ 2d, so d = o(a) gives a/γ → ∞. The cone argument is
correct. Suppose every integral point of a rational linear family is dark. In
a small cone the bound puts (a, 2d)/γ in a finite box. So the image of the
family in the (a,2d)-plane meets only finitely many rays through the origin.
A rank-2 image would meet infinitely many, so a:2d is fixed on the family. The
log confirms the converse: on a:2d = p:q, a/γ is constant, so those families
escape the theorem.

## 4. The negative claim (item b)

**The argument is correct.** Fix a first-hit branch through a mouth of width
w. On that branch the seam abscissa is affine in v_phys with slope B, the
total vertical travel. If the target is b above the seam, then B ≥ b. So the
branch's slope interval has length at most w/b. A union of N branches has
total length at most Nw/b.

**The example is correct.** At b = 2, 4, 6, 8 and 10, both choices
D = a = (b+1)²+1 and D = a = b+2 give strictly simple rooms. Each has W = 8,
two reflex corners, wall gcds (1,1) and gcd(a+1, b+1) = 1. The marks are
interior and of the same parity. The straight upper branch has the window
(1/b, 2/b), of length exactly w/b with w = 1. The log traces 3/(2b) through the
seam at x = 1/2. At 1/b the path hits the reflex corner (0, a+1).

**What it refutes.** It refutes a scale-uniform first-hit interval in physical
slope when the mouth width stays bounded while the target height above the
seam grows. That's w/b → 0. It doesn't refute more, and the body says it's not
a dark room or a lighting certificate.

**Medium 1: the Advances line overstates the claim.** "A uniform first-hit
interval in physical slope is impossible even at strictly separated scales"
is false as written. In the note's own theorem with u = t, the physical speeds
are v + kP. The physical window is (u/t)η = η at every scale, even with
t = o(a), which separates the scales. The log records this contrast. The
junction escapes the theorem because its target sits at relative height
b/(b+1). That's a drifting mark, not an exact stretch of one template. State
the condition w/b → 0, or equivalently a mouth that shrinks relative to the
target depth, in the Advances line and the section's first paragraph. Also
say that the junction lies outside the theorem's hypotheses.

The remark about heights j and j+1 is correct. A finite limiting ratio doesn't
give a common integral stretch.

## 5. Outside-span openings (item c)

- **(1) survives.** Neither short route touches the roof before the seam. So
  (1) holds wherever extra openings lie.
- **Regime D = O(a), t = o(a), d fixed.** γ ≤ 2d and u ≥ 1 make the right side
  of (1) at least a²η²/(8dPt). That's ω(a), so both short routes can't fail.
  "Resolves the far-mouth question in that scale regime" is correct, with the
  template fixed.
- **Roof contacts.** The formulas ℓ_j = ((2j+1)h+d)/s and
  x_j = D − |D − (c+ℓ_j)| are exact for one lateral reflection (30 cases in
  the log).
- **Arm phase.** An excursion of height H in an open-ended arm of width w adds
  2Hv to the unfolded phase. The path returns to the same entry coordinate and
  sign exactly when 2Hv ∈ 2wℤ (90 cases in the log).

The note says this "isolates the additional gate obligation … without
asserting that all roots fail". That's the correct label: an obstruction to
the method, not a darkness claim.

## 6. First open cases and the d189 correction (item d)

**d189 Medium 1 is addressed.**

- **Growing d.** The theorem proves it outside the bounded set of a/γ, and
  the residual a/γ ≤ K is named.
- **Two gaps per axis.** d188's product with two gaps per axis at an occupied
  crossing is listed as open. That's right. The theorem frees a, d, D, c, u
  and t, but only through one exact stretch of a fixed template. A d188
  product can vary the template's internal gaps independently.

The note's three listed cases are correct:

1. Growing d with a/γ bounded, such as a fixed ratio a = 2d.
2. The d188 two-gap product.
3. Two independently growing upper depths, or a mouth that shrinks relative
   to the template.

**Low 2: the list is incomplete.** It omits the outside-span opening beyond
the regime D = O(a), t = o(a), fixed d. The note's own section 5 calls this
the first residual, and d189 listed it. Add it to the "First open cases"
paragraph. The scope hypotheses are also real open directions: solid lower
sides, unclipped mouths and a template with fixed marks. They're stated in the
Setting, which is enough.

## 7. Mandatory corrections

### High

None.

### Medium

1. **Qualify the negative claim.** Rewrite the Advances line and the opening of
   "Why the requested physical-window induction fails". The impossibility holds
   when w/b → 0: a fixed-width mouth with growing target depth, or a drifting
   mark. Under the note's own exact stretch with u/t bounded below, a uniform
   physical window exists, of width (u/t)η ≥ η·inf(u/t). State that the
   junction example lies outside the theorem's hypotheses.

### Low

1. **Symbol clashes.** T names both the target and the Fibonacci bound. W
   names both the template width and the room wall count (W = 8, W ≤ 20).
   Rename the template width, for example W_tmpl, and the bound, for example
   T_F.
2. **Open-case list.** Add the outside-span roof opening beyond the resolved
   regime to "First open cases for L1", as in section 6.
3. **Template openings.** State that the template component meets the rest of
   the room only through its labelled shared mouths. Otherwise the
   sealed-chamber first hit can cross an unshared opening.
4. **Junction wording.** "The horizontal overlap endpoints are offset by one"
   is unclear. Say "the mouth is the overlap [0,1], of width one".
5. **Unused term.** The 1 in Q = max(1, 1+R/B, 2Rt/L) is never used. This
   change is optional.

## 8. Scope

The theorem covers this setup:

- a solid-sided lower rectangle [0,D] × [0,h], with source depth d and height
  a above the source, both free;
- a fixed sealed lattice template with a lattice target, stretched by integer
  (u,t);
- unclipped shared mouths, with every roof opening in [0,uR] and uR ≤ D;
- strict simplicity of the glued room.

For these placements, darkness forces a/gcd(a,2d) ≤ 16PC²/η³. The bound is
uniform in D, c, u and t. It's a necessary condition for darkness, not a
census. No chart-wide K(C), G(C) or H(C) follows, and the note says so.

## 9. What it advances

**L1 (area bound), occupied-crossing row.** The note removes two hypotheses
from d189:

- **Fixed source depth.** It's replaced by unbounded a/gcd(a,2d).
- **Fixed upper chamber.** It's replaced by an arbitrary exact stretch (u,t),
  with comparable or separated scales.

It replaces d189's two-part box with one ratio bound and no condition on D. It
also proves a structural fact that later chart arguments can use: any dark
rational linear family of these placements has a fixed ratio a:2d. That cuts
one dimension from the d188 product at this crossing. It doesn't supply the
fixed-period transfer, so H(C) isn't bounded. No ledger word changes status.
The advance is real, but it removes hypotheses inside one geometry class. I
see no basis to move the W ≤ 20 estimate.

## 10. First open case

The smallest open case inside this geometry is growing depth in a fixed ratio,
for example a = 2d, where a/gcd(a,2d) = 1 for every d. Every bound in the note
stays finite there, and no route is certified. Three cases have equal
standing:

- d188's two-gap product, where the template's internal shape varies;
- two independently growing upper depths, or a shrinking mouth;
- an extra roof opening outside [0,uR] beyond the regime D = O(a), t = o(a),
  fixed d.

LLLRLLLRLR (W = 10) remains open as an all-length statement. Its ledger
realization is correct: strictly simple, 10 walls, area 8.
