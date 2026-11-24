Advances: L1 — a collar theorem for an arbitrary polygonal foot when the source has a regular vertical first entry, and a signed-phase criterion for a general source. The unrestricted collar and denominator claims remain open.

## A collar theorem that permits steps, notches and reflex corners

Use depth increasing downwards. The strip is [a,a+w] × [0,L], with integral mouth levels and w ≥ 2. Attach an arbitrary fixed strictly simple orthogonal lattice end below depth L. Write H for its maximum depth below that line. The polygon above depth zero is also unrestricted. S is an upper interior lattice mark. Assume its vertical ray in one of the two axial directions first enters the **open** strip mouth regularly, after total vertical travel D. This is stronger than having a first entry at some nonzero slope. Put x₀=x(S), so a<x₀<a+w. For D=0 an interior mouth source sees the strip directly. Otherwise set

    d₀ = w(D+1),
    K = 1 + ceil(4w max{D+1, D+d₀+2H}).

For every L ≥ K, S lights **every** interior strip lattice mark T=(x,d), 0<d<L. The proof gives a primitive axial denominator at most D+2L+2H. Reflecting the construction exchanges the ends. Pairs of new marks see one another directly.

**Why small tilts preserve the source leg.** Before a regular vertical first entry, the ray runs in one vertical interval, with at most one reflection at its far horizontal endpoint. Its abscissa is integral. Each crossed horizontal mirror and the entrance contain that abscissa strictly inside their integral endpoints. On either side the adjacent unit column therefore supports the same finite itinerary. A tilt by signed transverse displacement s per unit axial travel preserves the entry if |s|(D+1)<1. In particular D is at most twice the height of the upper box.

If x=x₀ use the vertical ray. If d≥d₀, aim directly with s=(x−x₀)/(D+d). This preserves the entry; the strip segment joins two points between its side walls. Its reduced denominator divides D+d.

**Shallow targets.** Let d<d₀ and m=(x₀+x)/2. In every open unit column inside the strip, the downward vertical ray at the far mouth first encounters a horizontal wall at a depth h between 0 and H, constant across that column. Depth zero is allowed where the far mouth is closed by a wall. Up to that first wall the entire open column is available. This statement uses only lattice alignment and holds for an end with overhangs or several reflex corners.

If m is half-integral, choose its column and let h be that first depth. If m is integral, it lies strictly inside the strip width. Inspect the columns immediately to its left and right. Choose as the **outgoing side** one with the shallower first wall (either in a tie), and let h be its depth. Choose the sign of s to point into that side. This sign choice handles a step located exactly at the nominal midpoint.

Unfold the strip side walls. Aim at the target image x+4nw, taking n=0 or ±1 so that Δ=x−x₀+4nw has the chosen sign and 0<|Δ|<4w. For the half-integral case n=0 suffices. Set

    s = Δ/(D+2L+2h−d),       C=(D+d)/2.

The denominator is the axial travel for one reflection at depth L+h. At that floor the developed abscissa is exactly m+2nw+sC. At depth L on the downward and upward passes the abscissae are m+2nw+s(C−h) and m+2nw+s(C+h). The translation 2nw preserves the physical transverse chart. Since |s|<4w/L, the source leg persists and |s|(C+H)<1/2.

At a half-integer m the entire far-end visit stays in the chosen open column. At an integer m the floor hit and the upward leg lie strictly on the outgoing side. The downward leg can start on the other side, but that column extends **at least as deep as h**. If the ray crosses m inside the end, it does so at relative depth h−C<h, where both columns are open. A crossing exactly at the far mouth is regular as well: in that case h=C>0 and both columns continue below it. If h=0 the reflection lies strictly inside the outgoing wall. These checks exclude the riser, both step corners, and any other end wall before the intended floor hit. After returning to the strip the ray reaches the chosen image before another upper-mouth contact. This proves the stated theorem, including the equal-parity midpoint case. The denominator bound follows by reducing the displayed integral displacement. For a box of vertical size Bᵧ it is at most 4Bᵧ, since D≤2Bᵧ and L+H≤Bᵧ.

## Using a return itinerary of the end itself

Here is the test I get for a source with a regular, possibly oblique first-entry interval. It explains the remaining existence issue. Take positive slope magnitude s on a fixed signed branch. On the doubled transverse circle of circumference 2w let α(s)=α₀+Ds be the developed source phase at the near mouth; transverse phase increases with travel. For a fixed d, choose a signed target phase β at x. A first return from the far mouth through the foot, starting at phase θ, has a domain of regular inputs (s,θ). On a fixed itinerary its outgoing phase is

    R(s,θ) = θ+c+Bs   (mod 2w).

Indeed the unfolded horizontal displacement is s times the total axial travel B between the two mouth contacts. B is constant on the itinerary because the mouth and horizontal reflecting levels are fixed. Folding back into the signed exit chart adds a fixed offset c; the transverse sign is already encoded in θ. Direct reflection from a closed part of the mouth is the branch B=0. A regular branch persists on an open set by clearance from its corners and gate endpoints.

The actual incoming phase is θ=α(s)+Ls. After the return there are L−d axial units to T. Eliminating Ls shows exactly which part of the return domain matters:

    θⱼ(s) = [α(s)+β+ds−c−Bs+2wj]/2,     j=0,1 modulo the circle.

If one such graph lies **inside the return domain** throughout an interval J of positive width, then every length satisfying

    L > max{d, 2w/|J| + (d−D−B)/2}

admits a legal one-return seed. On J the difference α(s)+Ls−θⱼ(s) has derivative L+(D+B−d)/2; it sweeps more than one period and thus hits 2wℤ. This solves both entrance and target matching, with a regular final approach. Conversely every regular one-return seed of this itinerary satisfies the graph equation. For a fixed upper first-entry interval of width η, targets with dη>2w already follow from the direct sweep, whose derivative is D+d. Thus only finitely many integral depths and transverse columns require return data per fixed source. A room containing seeds for those end-relative collar pairs at some reference lengths can also propagate them individually by retained-pair re-aiming beyond those lengths. [Retained-pair argument](l1-reaim-threshold.md)

**First failed implication.** A regular excursion of the foot provides an open set in (s,θ). Its existence at a slope available from S gives no intersection with either of the two prescribed graphs. Changing L tunes the incoming phase, but cannot change the eliminated equation. The vertical-entry theorem constructs the needed regular visit by choosing the side of a step; a general inclined first entry does not give both small tilts from the same abscissa. An open case is a source behind a shoulder, with only oblique access established, and a shallow new mark facing a stepped foot. The one-return test leaves alternative itineraries and repeated visits open. [Flat-floor result](l1-wide-insertion.md) · [d209 review](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d209-review-wide-insertion/review.md) · [d184 review](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d184-review-gaphyper/review.md)

## Follow-on: what can be proved about the denominator

The collar construction above gives a linear denominator bound for its pairs. For arbitrary **lit** pairs there is also a polynomial conversion from a bound on the *smaller* primitive component to a bound on the axial one. Here is where the wall budget gives a quantitative statement.

Let Bᵧ be the integral box height. The room has at most ten horizontal walls when r≤8. All heights h of connected vertical slices between successive integral abscissae are differences of two horizontal support levels, hence at most 45 distinct positive integers, each ≤Bᵧ. Set Λ=2 lcm(h), over these heights; Λ≤2Bᵧ⁴⁵. In the four-copy unfolding, each open unit column component has vertical circumference 2h: vertical motion goes to the top, reflects, goes to the bottom and returns. In developed coordinates shear each such vertical band by adding Λ times the horizontal offset from its left developed boundary to its vertical circle coordinate. The shift is zero modulo 2h at both boundaries, since the developed band width is one. The maps glue across all integer abscissae, including reflected seams. They have common derivative ((1,0),(Λ,1)), inverse given by −Λ, and fix every lattice mark and forbidden vertex. Thus the affine image of a legal seed is legal. This argument uses the least common multiple of slice **heights**, independently of how often the original path reflects.

For primitive (p,q) with p≠0 choose an integer j nearest to −q/(Λp). The new primitive direction is (p,q+jΛp), with axial magnitude at most Λ|p|/2; primitivity follows from determinant one. A vertical seed already has |q|=1. Consequently if some seed has min(|p|,|q|)≤M, then the pair has a seed with |q|≤Bᵧ⁴⁵ M. This supplies a polynomial conversion even if the original large component was enormous. The observed bound on travel along one axis in the [area-21 profile](l1-seed-profile.md) implies such an M **on that slice**.

The missing statement is a polynomial M for all lit pairs at r≤8. A shear fixing p leaves an arbitrary balanced pair of large components without a useful absolute bound; the fixed-direction bound on the number of lattice steps likewise does not bound either component. I obtain no unconditional polynomial bound on the minimal denominator in the full class.
