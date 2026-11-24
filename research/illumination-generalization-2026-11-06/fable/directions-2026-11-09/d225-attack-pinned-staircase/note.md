# D225: two-scale blow-up at the pins of the x = 1 staircase pair

Date: 2026-11-23. Advances **L1** (pinned-pair route in `../PROGRAM.md`).
Checks: [checks.py](checks.py), output [checks.log](checks.log): 45 PASS,
0 FAIL, under 1 CPU-second at `nice -n 10`.

## Result

The strip near b = c and the band 2a+2b ≤ c with α ≥ 1/4 are **closed** for
every real gain pair with x + y > 8. Both pin lines are closed from much
lower: x = y for all x > 0, and y = 2x+2 for all x > 1/3. In the closed
sector 1/4 ≤ α ≤ 2/3 the only lattice rooms without a certificate here are
(x, y) = (0, 0) (area 18, census), (0, 2) (area 24) and (0, 3) (area 27).

The mechanism is a one-unit micro move. A floor bounce under S, or a roof
bounce over T, shifts every interface crossing by a fixed number of axial
lattice units. That moves the chord off the pinned corner while keeping it
inside the same macro window. The same tool also closes α > 2/3, so with
d215 the pair is lit outside an explicit compact set that stays away from the
face at infinity (Theorem B).

## Setup

The room is d213's offset staircase. Tiers x ∈ [0,3], [1,4], [3,6], [4,7]
have heights 2, 1+x, 1+y, 2, for real x, y ≥ 0. The pair is S = (1, 1) and
T = (5, top − 1). The interfaces sit at axial heights 2, 3+x and 4+x+y. Their
open gates are (1,3), (3,4) and (4,6).

Put D = 4+x+y and α = (2+x)/D. With barycentric (a, b, c) ∝ (1, x, y), α =
(2a+b)/(4a+b+c). The translations are exact linear identities (checks §2):

| Ratio condition | Gain condition |
| --- | --- |
| α = 1/2 | x = y (b = c) |
| α = 1/3 | y = 2x+2 (2a+2b = c) |
| α = 1/4 | y = 3x+4 |
| α = 2/3 | x = 2y+2 |

So the band is 1/4 ≤ α ≤ 1/3, and the strip is a neighborhood of α = 1/2.

## Lemma M (the chord family)

Fix h0, h3 ∈ {1, 3} and an integer k > 0. Put D' = h0+h3+2+x+y,
σ = k/D' and α' = (h0+1+x)/D'. Launch from S to the right with horizontal
speed σ per axial unit. Go down first if h0 = 3, which bounces once on the
floor. Bounce once on the roof of the top tier if h3 = 3. Otherwise go up.

**Lemma M.** Suppose h0σ < 2 and h3σ < 1. Let r = kα' mod 6. The ray reaches
T legally in exactly these cases:

- Case A: r ∈ (2, 3) and k ≡ 0 or 4 (mod 6).
- Case B: r ∈ (3, 4) and k ≡ 0 or 2 (mod 6).

*Proof.* In the bottom tier the ray meets the floor at 1+σ (if h0 = 3) and
the first interface at 1+h0σ ∈ (1, 3). Each tier has width 3, so inside a tier
the abscissa is the fold of an unfolded offset by tri(v), the triangle wave
of period 6 on [0, 3].

The unfolded offset from x = 1 at the middle interface is v = σ(h0+1+x) = kα'.
The physical crossing is 1 + tri(v). It lies in the gate (3, 4) exactly when
r ∈ (2,3) ∪ (3,4). In case A the ray moves right; in case B it moves left.
At r = 3 it hits the corner (4, 3+x), and at r ∈ {2, 4} the corner (3, 3+x).

In tier 2, measure from the wall x = 3. Let w = r − 2 + σ(1+y) in case A, or
w = r − 4 + σ(1+y) in case B. The crossing is 3 + tri(w). The final leg has
horizontal length h3σ < 1 and no side reflection. So it ends at 5 exactly
when w + h3σ ≡ 2 (moving right) or 4 (moving left) mod 6. The intervals
needed, w mod 6 ∈ (1,3) or (3,5), then hold automatically.

Now w + h3σ = k − 6m − 2 in case A, and k − 6m − 4 in case B, where
v = 6m + r. That gives the residue conditions. Every reflection inside a tier
happens strictly between interface heights, because all entry and exit
abscissae are strictly inside the gates. The roof bounce point 5 ∓ σ lies in
(4, 7). ∎

The d215 constructions are special cases. The (6, D) ray is h0 = h3 = 1 with
k = 6 in case A. Its mirror region is k = 6 in case B. The x^(3/2) ray is
case A with k ≡ 0, 4 and kα ∈ (2, 3). The exact traces in §6 of the checks
confirm the predicted three crossings at every legal point.

## Step 1: what pins what

- **The marks.** In the two-gain slice every mark coordinate is frozen, so
  the mark fiber is a point. In the full refined chart only one coordinate is
  pinned: S_x = 1 lies on the supporting line of the tier-1 left wall. That
  line meets the tier-0 roof at the reflex corner (1, 2), directly above S.
  T_x = 5, S_y and T_y are private levels.
- **The chord pins.** Darkness of the monotone family (h0 = h3 = 1) on the
  uncovered set comes from two supporting-line intersections on the middle
  interface: (4, 3+x), where the tier-1 right wall x = 4 ends, and (3, 3+x),
  where the tier-1 roof ends at the tier-2 left wall x = 3.
- **No other pins.** The top gate is never approached. The last crossing is
  5 ∓ h3σ, with h3σ < 1.

The pin set of the monotone family inside [1/4, 2/3] is exactly
{1/3, 1/2} (checks §1–2):

- At α = 1/2 every k fails, because kα mod 6 depends on k mod 12. The k = 6
  chord hits (4, 3+x), and the k = 4 chord hits (3, 3+x).
- At α = 1/3 every k fails, because kα mod 6 depends on k mod 18. The k = 6
  and k = 12 chords both hit (3, 3+x).
- At α = 1/4 the monotone k = 10 chord works, so it isn't a pin.

The exact traces at P1 = (10, 10) and P2 = (10, 22) reproduce all four
corner hits.

## Step 2: macro chord and crossing types

**Macro limit.** Normalize the axial coordinate by D' and let x, y → ∞ with
α → α*. This approaches the face a = 0. The end tiers collapse to the levels
0 and 1, and the middle interface sits at level α*. The developed chord is
the segment from (1, 0) to (1+k, 1), so the middle crossing is at 1 + kα*.

For each k, the set of good α is a finite union of open intervals of length
1/k. These are the **macro windows**:

| k | Case | Window |
| ---: | --- | --- |
| 4 | A | (1/2, 3/4) |
| 6 | A | (1/3, 1/2) |
| 6 | B | (1/2, 2/3) |
| 10 | A | (1/5, 3/10) |
| 12 | B | (1/4, 1/3) |

A pin is a common endpoint of windows where the macro slack is zero. The
macro chord also starts on the corner (1, 2), because S collapses onto it.

**Micro coordinate.** Near a pin corner c, set μ = (crossing − c)/σ. This is
the offset in axial lattice units. At the 1/2 pin with k = 6 it equals
μ = (x − y + h0 − h3)/2 (checks §3).

**Crossing types.** Each pin corner has one of these local types:

| Type | Corner | Left side of c | Right side of c | Lit when |
| --- | --- | --- | --- | --- |
| P0 | End of a side wall parallel to the axis, k ≡ 0 | Passes the gate (case A) | Reflects off the wall below c, then passes (case B) | μ ≠ 0 |
| P+ | Same corner, k ≡ 4 | Passes | Downstream residue fails | μ < 0 |
| P− | Same corner, k ≡ 2 | Downstream residue fails | Reflects, then passes | μ > 0 |
| R | End of the lower tier's roof, perpendicular to the axis | Hits the roof, so monotonicity breaks | Passes the gate | μ > 0 |
| S | Mark on the supporting line of the next tier's side wall | Never reached, since σ > 0 | Passes | Always, but budget h0σ < gate width |

Here (4, 3+x) is P0 for k = 6, P+ for k = 4 and P− for k = 2. (3, 3+x) is
type R. (1, 2) is type S.

**Micro moves.** A floor bounce under S adds 2 to the axial path below every
interface. It shifts every interface crossing by **+2(1 − α_i)** micro units.
A roof bounce over T shifts every crossing by **−2α_i** units. The checks
(§3) verify both exactly. Meanwhile α' − α = O(1/D), so the macro window is
kept.

## Step 3: theorem for the strip and the band

**Theorem A.** Let x, y ≥ 0 be real with 1/4 ≤ α ≤ 2/3, that is,
y ≤ 3x+4 and x ≤ 2y+2. If x + y > 8, then the x = 1 pair is lit. These
certificates apply:

| Region | Certificate | Own threshold |
| --- | --- | --- |
| 1/4 ≤ α < 3/10 | k = 10, monotone, case A | D > 10 |
| 1/4 < α < 1/3 | k = 12, monotone, case B | D > 12 |
| α = 1/3 (y = 2x+2) | k = 6, floor bounce, case A | x > 1/3 |
| α ∈ (1/3, 1/2) ∪ (1/2, 2/3) | k = 6, monotone | D > 6 |
| α = 1/2 (x = y) | k = 4, floor bounce, case A | x > 0 |
| α = 2/3 | k = 4, monotone, case A | D > 4 |

*Proof.* The open windows and the two pin points cover [1/4, 2/3] (checks
§2). Each monotone line follows from Lemma M, since σ = k/D < 1 when D > k.

For the pin lines, take h0 = 3 and h3 = 1, so D' = 6+x+y.

- **x = y.** Here α' = 1/2 + 1/(6+2x) ∈ (1/2, 3/4). With k = 4 we get
  r = 4α' ∈ (2, 3), and k ≡ 4, so this is case A. The budget
  σ = 4/(6+2x) < 2/3 holds exactly when x > 0. The middle crossing is
  3 + 2/(3+x). This is the type-R corner (3, 3+x) cleared on its passing
  side by μ = +2(1 − 1/2) = 1 unit.
- **y = 2x+2.** Here α' = (4+x)/(8+3x) ∈ (1/3, 1/2) for x > 0. With k = 6,
  r = 6α' ∈ (2, 3), and k ≡ 0, so this is case A. The budget σ = 6/(8+3x)
  < 2/3 holds exactly when x > 1/3. The crossing is 8/(8+3x) to the right of
  the type-R corner (3, 3+x), which is μ = +4/3 units. ∎

Both bounce certificates are open conditions, so each covers a full
neighborhood of its pin line, not only the line.

- The floor k = 4 chord lights the set where α' ∈ (1/2, 3/4) and x + y > 0.
  That is {y < x+2, x < 3y+2}, which is a uniform strip around b = c.
- The floor k = 6 chord lights {y < 2x+6, x < 2y, y ≠ x+2, x+y > 3}.

**Clearance and the macro slack window.** At a pin the macro slack of d214
claim 1 is zero. The micro move restores an absolute clearance σ|μ| of order
1/D'. For example, the clearance is 2/(3+x) on x = y and 8/(8+3x) on
y = 2x+2. This is the same order as d214's Farey window bound 2/(bH). The
legality is exact; no clearance estimate is used.

**Small rooms.** Inside the sector with x + y ≤ 8, each lattice point was
tested against the six rules of Lemma M (inequalities only, no traces). Every
point is covered except (0, 0), (0, 2) and (0, 3), with areas 18, 24 and 27.

- (0, 0) is in the census.
- At (0, 2) the floor bounce lands on the pin α' = 1/2 again.
- At (0, 3) the floor k = 6 chord has σ = 2/3, which exhausts the type-S
  budget and hits the corner (3, 2).

## Theorem B: the rest of the triangle

**Theorem B.** The x = 1 pair is lit for every real x, y ≥ 0 outside the
compact set

    K0 = {x + y ≤ 8}  ∪  {x < 1, y ≤ 18 + 5x}.

Since a = 1/(1+x+y) ≥ 1/25 on K0, the whole neighborhood a < 1/25 of the face
at infinity is closed for this pair. This part is proved by reading
plus inequality checks (§4). No point outside the strip was traced.

*Proof.* Let β = 1 − α.

- **α < 1/4 and x ≥ 1.** Use d215's case-A construction.
- **x < 1 and y > 18+5x.** This forces α' = (4+x)/(6+x+y) < 1/6. Take the
  floor bounce with k ≡ 0 or 4 in the interval (2/α', min(3, (8+2x)/3)/α').
  Its length is at least 2/(3α') > 4. The maximum gap of the residues {0, 4}
  mod 6 is 4, so such a k exists. Then σ = kα'/(4+x) < 2/3, which gives case A.
- **1/4 ≤ α ≤ 2/3.** Use Theorem A.
- **2/3 < α < 3/4.** Use k = 4, monotone, case A.
- **α = 3/4 (x = 3y+4).** Use a roof bounce with k = 4. Here
  α'' = (6+3y)/(10+4y) ∈ (1/2, 3/4), which is case A. The roof leg needs
  3σ < 1, which holds exactly when y > 1/2. This is the type-P+ pin at
  (4, 3+x), shifted to its passing side by −2α* = −3/2 units.
- **3/4 < α < 5/6.** Use k = 12, case B.
- **4/5 ≤ α < 9/10.** Use k = 10, case A.
- **α > 5/6 (β < 1/6).** Use k ≡ 4 (mod 6) with kβ ∈ (1, 2). Such a k exists,
  since the interval (1/β, 2/β) is longer than 6. Then
  kα ≡ 4 − kβ ∈ (2, 3), which is case A, and σ = kβ/(2+y) < 1.

With D > 12, every condition above holds. ∎

The lattice residual of K0 outside the sector was not enumerated; doing so
would be a sweep. It is a finite list of rooms with x + y ≤ 8 or with
x = 0 and y ≤ 18.

## Step 4: general principle

**Pin blow-up lemma.** Consider a chart whose tiers stack along one axis.
Each interface has a single open gate, and the marks sit in the two end
tiers. Mark S is at axial distance d0 from the wall beneath it, and T is at
axial distance d3 from the wall above it. Assume both walls span the
end-tier gate columns. Let the developed chords be indexed by an integer
winding k, and let a residue test such as Lemma M's decide their legality.

Let α* be a pin of winding k. Let I be the set of interfaces whose crossings
hit corners there. Suppose each such corner has crossing type P0, P+, P− or R,
with legal sign s_i. Suppose also that for some e0, e3 ∈ {0, 1}, for every
i ∈ I:

    sign( 2 e0 d0 (1 − α_i*) − 2 e3 d3 α_i* ) = s_i,  or nonzero for P0.

Then the pin line, together with an open neighborhood of it, is lit by the
bounced winding-k chord. This holds whenever the end-tier budgets are met:

    (h0 σ, h3 σ) < (end-gate clearances),  with σ = k / D',  h0 = d0(1+2e0),  h3 = d3(1+2e3).

That gives the explicit threshold D' > k · max(h0/g0, h3/g3), where g0 and
g3 are the end-gate clearances. Here g0 = 2 (gate (1, 3) from x = 1) and
g3 = 1 (gate (4, 6) from x = 5). Away from pins the macro window gives an
open set. So in such a chart only the pin lines need the micro move.

The proof is Lemma M's computation with general tier widths. The bounce
changes only the axial lengths below or above each interface, so it changes
the residue test of no k.

**Covered crossing types.**

- P0: two-sided side-wall corner.
- P+ and P−: side-wall corner whose residue selects one side.
- R: roof corner, one-sided.
- S: mark on the supporting line of the next side wall. This type only
  limits the budget.

**Not covered.**

1. The bounce shift 2e0d0 − 2(e0d0 + e3d3)α is decreasing in α. So two
   simultaneous pins at α_1 < α_2 that need signs (−, +) can't be fixed by
   end bounces.
2. A pin corner with no legal side, such as a corner where both neighbors
   block or reverse the axial motion.
3. A budget overrun: a pin reached only in rooms too short for h0σ < g0. The
   rooms (0, 2) and (0, 3) fail in this way.
4. Charts whose interfaces have several gate components, or whose marks
   aren't in end tiers. For these the crossing type also has to record the
   component, and the end-bounce move may not exist.

No pinned dark sub-family with all gaps unbounded appears in this chart. Every
pin line here is lit from x > 1/3 on.

## What remains

- **This pair.** The lattice rooms (0, 2) and (0, 3), with areas 24 and 27,
  need an exact certificate. Finding one would be a direction search, which
  this note's budget excludes. The finite lattice residual of K0 outside the
  sector also remains. So does a compact real residual inside K0. The face at
  infinity is fully closed.
- **L1 in general.** Two steps remain:
  - Show that in every nondegenerate chart with r ≤ 8, each pin of the
    descent chord is of type P0, P±, R or S.
  - Handle the (−, +) sign pattern, budget overruns and multi-gate
    interfaces. For those, the end-bounce move must be replaced by an
    interior bounce or another micro move.

  The pin blow-up lemma is proved here only for stacked single-gate charts.
- No census changes.
