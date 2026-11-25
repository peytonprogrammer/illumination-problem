Advances: L1 — the proposed two-axis affine gate-box lemma is false. A fixed transition between two maximal rectangles of a six-reflex lattice room, with pinned endpoints and fixed reflection parities, has infinitely many legal rational crossing ordinates with unbounded denominators. The N-family does have a bounded rectangle description. Its reversal lower bound gives no switch lower bound.

### Where the lattice calculation changes

A maximal inscribed axis-aligned rectangle has sides on wall supports: otherwise one can enlarge it in the unsupported direction. Thus their number is at most binom(r+2,2)². An overlap alone does not specify a transition point. A chord can spend a whole segment in both rectangles. Specify an entry or exit face of the overlap, its incident sectors and unfolded copy (or fix a transverse cut inside it). Specify also which portions of each side are exposed physical mirrors. Crossing an artificial rectangle side is not a billiard reflection.

For fixed orientation parities one may write the developed target displacement (X,Y) as an affine function of the winding integers, with periods twice the respective rectangle dimensions. But the intersection ordinate on a developed vertical face x=a is S_y+(a−S_x)Y/X. A horizontal face has the reciprocal formula. Even the developed a can depend on the preceding windings. An exact test for a fully specified finite word uses these ratios, open face intervals, event order, and genuine wall incidence at every reflection. Clearing denominators of known sign gives determinant inequalities. The endpoint translation lattice is real; its linear image in the transition coordinates, as proposed in the brief, does not in general exist.

D230 works when all events have fixed travel along **one common axis** and the windings change only transverse travel: the common denominator is then fixed. A visit with no winding contributes a fixed leg in that model. Zero winding in just one rectangle does not fix the denominator of a mixed itinerary. Recording homogeneous coordinates can clear a denominator but turns the gate box into coupled inequalities. [One-axis coset test](l1-two-gate-chart.md)

### Symbolic counterexample with a genuine overlap-entry event

At successive height levels −1,0,1,2,4,5,6 take the open horizontal intervals

    (1,6), (0,7), (0,6), (2,6), (2,7), (4,7).

As usual take the interior of the union of the closed rectangles. The changes of interval endpoints give 2+1+1+1+1=6 reflexes. Both marks S=(1,1) and T=(4,4) are strictly interior and pinned. Two maximal rectangles are U=(0,6)×(0,2) and V=(2,6)×(−1,5); their side limits follow directly from the tiers. Start in U, switch to V on a rightward entry through x=2 in the overlap boundary, and finish in V. Earlier entries into the overlap are allowed while the ray remains assigned to U; switching at every overlap entry would impose a different complexity measure.

For any integer k≥0 launch upward with transverse slope p=(11+72k)/3. Switch at the last rightward crossing of x=2 before height 2. Its ordinate is

    z_k = 2 − 8/(11+72k).

Indeed from S to that crossing the transverse travel is 1+24k, making 2k full periods in U before reaching x=2 with positive sign. At height 2 the physical abscissa is 14/3, strictly inside (2,6). From the switch to T the developed transverse travel is 10+48k. Starting from x=2, this ends at the rightward copy 4+8(1+6k) of T. All hits in U below height 2 are on the true sides 0 and 6. After the switch and before height 2 the ray stays between 2 and 14/3; above height 2 both sides of V are true mirrors until T. Thus all these rays have the same rectangle sequence, switch face and even side-reflection parities. Their horizontal cycle counts are (2k,1+6k), and both vertical counts are zero. The switch really enters the overlap from its exterior, and the two marks are in their respective rectangles at the required endpoints.

The ordinates z_k are distinct rationals with denominators tending to infinity. A lattice in one real coordinate meets a bounded interval in finitely many points. Even allowing the projection of a finitely generated higher-dimensional group does not help: its subgroup of rational elements is finitely generated, so its rational differences have bounded denominators. The differences z_k−z₀ violate that condition. In particular no fixed affine winding map, nor a finite union of such transition cosets, contains these crossing data as claimed. The proposed two-axis transition dual is therefore undefined. This counterexample concerns the coordinate of an allowed vertical switch. Choosing instead to label these same rays by their crossing of y=2 recovers a one-axis description; it does not prove one works for every switch sequence.

### N-family calibration

Write b=1+B=2N+3. The proposed lower column U=(N−1,N)×(−1,b) and middle tier V=(N−1,2N+1)×(1,b) have open overlap. The upper rectangle W=(2N,3N)×(b,b+2) shares an **open gate on its boundary** with V; their interiors do not overlap. If transitions through a common open gate are allowed the three-piece witness is valid. It enters V at (N−1/2,1) and passes from V into W at (2N+1/2,b). If positive-area overlap is required, insert the maximal bridge (2N,2N+1)×(1,b+2) between V and W. Switch to the bridge at (2N,b−1) and to W at (2N+1/2,b). These contacts are regular. Assignment at the initial mark uses the sector pointing into U.

Here is the actual one-axis lattice for the (1,2) witness. Horizontal displacement X=3N/2+1 is fixed. Only the final vertical image varies. Relative to ordinate b the target images in W are ±1+4k, so the developed axial displacements are H=b±1+4k. At fixed abscissas N, 2N, 2N+1 the three developed ordinates belong to

    (b±1)(1,N+1,N+2)/X + ℤ · 4(1,N+1,N+2)/X.

These are coordinates for fixed transverse cuts in the monotone-x development, subject to the actual gate and mirror checks. For H=b+N−1=2X the coset point is (2,b−1,b+1); use +1 if N≡2 modulo 4, −1 if N≡0 modulo 4. In W the positive developed travel is N−1, the floor and roof are separated by 2, and every floor return before T is on the exposed part of that face. Thus the unbounded reversal count lies in a single rectangle with one integer winding. [Face checks](l1-two-gate-chart.md)

### Scope of the stopping result

There is a useful conditional bound: an x-monotone witness passes at most r+1 physical x-gaps. In each gap its open path lies in a single rectangular component, hence in a maximal rectangle extending that component. At a regular crossing, a short horizontal rectangle across the common open gate can be extended to a maximal rectangle if an open-area overlap chain is required. Thus at most 2r+1 visits suffice for a transverse x-monotone witness with open gates and interior marks (endpoint sectors when pinned). The same holds with the axes exchanged. The N witness meets this hypothesis. The argument supplies no monotone witness for an arbitrary joined pair.

**First open case.** I obtained neither an all-gap bound L for the specified six-reflex pair nor a family whose minimum number of maximal-rectangle switches diverges. The first missing geometric step is to control witnesses that reverse on both axes and must switch between rectangles. Even a proof of bounded switch count would require a different arithmetic membership test at mixed switches; it would not authorize d232 slice recursion on a transition lattice. Conversely, a large number of switches need not rule out a repeated multi-rectangle cycle with one unbounded counter, as in d229's template language. There is no general switch lower bound or numerical H(C) from this formulation. No searches were run.

### D233 follow-up. Can the same half-period lock work on the other axis?

Use the free chart supports and levels in the two-gate note. A left-to-right candidate from S at x=C to T at x=G can use the following four rectangular column components. Their open vertical intervals, in order, are

| x range | Chosen component |
|---|---|
| (C,D) | (y₀,y₃) |
| (D,E) | (y₂,y₃) |
| (E,F) | (y₂,y₅) |
| (F,G) | (y₃,y₅) |

The last three entries describe the component on the route through the middle; the bottom cap may be a separate component in the same column. The first two transmissions, at D and E, must both pass the interval (y₂,y₃). A valid x-monotone ray on this route has at most four maximal-rectangle visits if open-face transitions are allowed, or seven with overlap bridges. D233 confirms exactly such transverse simplicity on the N-family: its prescribed witness is monotone in x even though it makes N/2−1 vertical reversals. [D233, claims 6–8](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d233-review-two-gate-chart/review.md)

**Obstruction to copying the half-period proof.** To impose a congruence valid through *arbitrary* horizontal-wall reflections before first passage at D, translate the transverse origin to y₂. Both y₂ and y₃ are genuine mirror supports in the source-side component cut at D: the ceiling is at y₂ just left of C and at y₃ just right of C. In the target-side component cut at E, both are again mirror supports: the floor is at y₂ just left of F and at y₃ just right of F. Their reflections compose to translation by 2d, where d=y₃−y₂. Thus any modulus Q that erases both wall translations up to sign must satisfy 2d∈Qℤ on either end.

In particular d≥Q/2. For every d≥Q/2 the only residues potentially missing from the signed images of (0,d) modulo Q are 0 and Q/2. Indeed (−d,0)∪(0,d) contains a representative of every other residue. Consequently the signed gate projection has **no omitted open arc** on either end. It cannot place first and last end phases in two positively separated arcs, the step that produced N/2≤2Aₜ+Aₛ in the vertical argument. This uses the actual positions of the two shoulders and holds for all free gaps of this chart. It does not exclude exact endpoint coincidences or a stronger constraint obtained by keeping individual reflection sequences.

**A sufficient arithmetic test on the transverse route.** Set X=G−C, s₁=D−C, s₂=E−C, s₃=F−C. In lattice units let P be the lcm of the four doubled column heights in the table. Select only increasing transverse copies at each transmission and at the target. Give each gate the signed physical interval above, namely (y₂,y₃), (y₂,y₃), (y₃,y₅), of lengths dᵢ. For target images y₄+Pj the unfolded straight line has ordinate y₁+(y₄−y₁+Pj)sᵢ/X at gate i. If each ordinate lies in its gate modulo P, the copies match: translations by multiples of P are complete periods of each incident column. Between gates the column is rectangular and all intervening horizontal hits are genuine. This produces a chord.

For any ordering of the three tests let nᵢ=X/gcd(X,sᵢ). Start with q=1. Require at each gate

    dᵢ/P > gcd(q,nᵢ)/nᵢ,      then update q to lcm(q,nᵢ).

To prove sufficiency, after satisfying earlier gates keep j fixed modulo q. At the new gate the remaining j give equally spaced residues on the unit circle with the spacing on the right. The strict width test selects a residue; fixing j modulo the updated q preserves it. After three steps one has an actual compatible target image. For example, for fixed vertical data choose X=m³ and (s₁,s₂,s₃)=(1,m,m²). Testing the gates in reverse order yields spacing 1/m at each, so every m>P/min dᵢ works. This is a symbolic region in the free chart. The test can miss other witnesses, including ones using decreasing copies.

**What a two-axis lower bound must prove.** For an arbitrary witness with h horizontal-velocity reversals, split at these reversals into h+1 x-monotone pieces. Each piece crosses at most r+1 column gaps and fits in at most 2r+1 maximal rectangles with bridges at regular open crossings. At a smooth wall reversal use the same incident column rectangle on departure as on arrival. An internal subdivision level coinciding with a smooth horizontal-wall contact can be bridged by a small rectangle on its occupied side; physical corners are forbidden. The same argument applies in y. Thus for nonaxial witnesses a sufficient upper bound on visits is (2r+1)(1+min(h,v)), with v the vertical-velocity reversals. An unbounded lower bound on *minimum switches* must therefore force both h and v to grow on **every** witness. Counting both reversal types alone still does not lower-bound switches inside a rectangle. Nor does an unbounded raw switch count rule out repeated multi-rectangle templates with unbounded counters.

**First open case.** Exhibit a joined pinned family in which every witness requires unboundedly many reversals on both axes, and show that those reversals force unbounded switching, or prove bounded rectangle selection for every lit free-gap tuple. The literal rotated d233 interval-separation proof cannot do the former in this chart. The arithmetic test above proves bounded selection on a region and leaves the complementary tuples open. No uniform L or H(C) follows.
