Advances: L1 — a collar theorem for an arbitrary polygonal foot when the source has a regular vertical first entry, an oblique-entry extension for rectangular upper chambers, and a signed-phase criterion for a general source. The unrestricted collar and denominator claims remain open.

## A collar theorem that permits steps, notches and reflex corners

Use depth increasing downwards. The strip is [a,a+w] × [0,L], with integral mouth levels and w ≥ 2. Attach an arbitrary fixed strictly simple orthogonal lattice end below depth L. Write H for its maximum depth below that line. The polygon above depth zero is also unrestricted. S is an upper interior lattice mark. Assume its vertical ray in one of the two axial directions first enters the **open** strip mouth regularly, after total vertical travel D. Regular vertical first entry means that the mouth point (x₀,0) has four incident room cells and so does each intermediate lattice point, except for at most one ordinary reflection in the relative interior of a horizontal wall (two adjacent cells). The ray meets no corner before entry. Put x₀=x(S), so a<x₀<a+w. For D=0 an interior mouth source sees the strip directly. Otherwise set

    d₀ = (w−2)(D+1),
    K = 1 + ceil(4w max{D+1, D+d₀+2H}).

For every L ≥ K, S lights **every** interior strip lattice mark T=(x,d), 0<d<L. The proof gives a primitive axial denominator at most D+2L+2H. Reflecting the construction exchanges the ends. Pairs of new marks see one another directly.

**Why small tilts preserve the source leg.** Before a regular vertical first entry, the ray runs in one vertical interval, with at most one reflection at its far horizontal endpoint. Its abscissa is integral. Each crossed horizontal mirror and the entrance contain that abscissa strictly inside their integral endpoints. On either side the adjacent unit column therefore supports the same finite itinerary. A tilt by signed transverse displacement s per unit axial travel preserves the entry if |s|(D+1)<1. In particular D is at most twice the height of the upper box.

The two interior lattice abscissae differ by at most w−2. If x=x₀ use the vertical ray. If d≥d₀, aim directly with s=(x−x₀)/(D+d). This preserves the entry; the strip segment joins two points between its side walls. Its reduced denominator divides D+d.

**Shallow targets.** Let d<d₀ and m=(x₀+x)/2. In every open unit column inside the strip, the downward vertical ray at the far mouth first encounters a horizontal wall at a depth h between 0 and H, constant across that column. Depth zero is allowed where the far mouth is closed by a wall. Up to that first wall the entire open column is available. This statement uses only lattice alignment and holds for an end with overhangs or several reflex corners.

If m is half-integral, choose its column and let h be that first depth. For distinct abscissae the integral-midpoint case arises only at w≥4. If m is integral, it lies strictly inside the strip width. Inspect the columns immediately to its left and right. Choose as the **outgoing side** one with the shallower first wall (either in a tie), and let h be its depth. Choose the sign of s to point into that side. This sign choice handles a step located exactly at the nominal midpoint.

Unfold the strip side walls. Aim at the target image x+4nw, taking n=0 or ±1 so that Δ=x−x₀+4nw has the chosen sign and 0<|Δ|<4w. For the half-integral case n=0 suffices. Set

    s = Δ/(D+2L+2h−d),       C=(D+d)/2.

The denominator is the axial travel for one reflection at depth L+h. At that floor the developed abscissa is exactly m+2nw+sC. At depth L on the downward and upward passes the abscissae are m+2nw+s(C−h) and m+2nw+s(C+h). The translation 2nw preserves the physical transverse chart. Since |s|<4w/L, the source leg persists and |s|(C+H)<1/2.

At a half-integer m the entire far-end visit stays in the chosen open column. At an integer m the floor hit and the upward leg lie strictly on the outgoing side. The downward leg can start on the other side, but that column extends **at least as deep as h**. If the ray crosses m inside the end, it does so at relative depth h−C<h, where both columns are open. A crossing exactly at the far mouth is regular as well: in that case h=C>0 and both columns continue below it. If h=0 the reflection lies strictly inside the outgoing wall. These checks exclude the riser, both step corners, and any other end wall before the intended floor hit. After returning to the strip the ray reaches the chosen image before another upper-mouth contact. This proves the stated theorem, including the equal-parity midpoint case. The denominator bound follows by reducing the displayed integral displacement. Let U be the upper height. Since U+L+H≤Bᵧ, D≤2U and d≥1, the shallow denominator divides D+2L+2h−d≤2Bᵧ−1. The direct denominator D+d also satisfies this bound since d≤L−1. In d211’s tests of the original sufficient cutoff, the largest sampled failing length of the prescribed shallow seeds was 77; the cutoff was roughly 8–30 times the observed need. This comparison is confined to the tested geometries and lengths. [d211 review](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d211-review-general-collar/review.md)

## A source behind a rectangular shoulder: both parities, arbitrary foot

The vertical-access restriction can be removed when the upper chamber is a rectangle whose bottom opens along the full strip mouth. The foot is still an arbitrary strictly simple orthogonal lattice polygon. This conclusion concerns **upper-source to strip-target** pairs. Reverse the configuration for the corresponding result from the other end when its hypothesis holds.

Translate the strip to [0,w]. Sources strictly over the opening satisfy the vertical-entry hypothesis with D=z, their height above the bottom. By reflection, take the remaining source at x=−b, b≥0, at height z>0 above the bottom of a rectangle of height A. The case b=0 includes a source vertically aligned with a mouth corner. Launch right and down with transverse-to-axial ratio s>0. Before entry the bottom visits occur at axial travels tₙ=z+2An. For b>0 choose n≥1 with t=tₙ sufficiently large and use

    J(t)=(b/t, b/(t−A)),     e(s)=ts−b.

At the selected visit 0<e(s)<As; at every earlier bottom visit x≤e(s)−2As<0. For As<w the selected visit is the first entry. The abscissa increases throughout inside the rectangle, so all preceding reflections are regular. For b=0 take t=z and e(s)=zs on any positive open slope interval with zs<w. These constructions give oblique first entries arbitrarily near the mouth edge with 0<e(s)<As. They use only the fixed upper chamber.

**A finite threshold.** For b>0 take as the coarse interval J₀ the first J(tₙ), n≥1, with tₙ>A+Ab/w. For b=0 take J₀=(0,w/(2A)). Set d₁=⌊2w/|J₀|⌋+1. Every target at depth d≥d₁ is lit by the direct sweep: the phase e(s)+ds varies over more than 2w on J₀. For the remaining depths put U=min(w/A,1/(A+d₁+2H)). For b>0 take the first n≥1 with tₙ>A+b/U and set J=J(tₙ); for b=0 set J=(0,U/2). Then sup J≤U and 0<e(s)+s(d+2H)<1 on J for all d<d₁. A sufficient strip length for every upper-to-strip pair from this source is

    L ≥ 1 + ceil(d₁ + 2w/|J|).

**Return through the foot.** For transverse target coordinate i in {1,…,w−1}, put m=i/2. For half-integral m take its column, its first floor depth h, and sign σ=+1. For integral m take the shallower adjacent first floor as before, and select σ=+1 when that column is on the right, −1 when it is on the left. Solve

    e(s)+(2L+2h−d)s = σ i + 4wn,       n integral, s in J.

The left side varies over more than 4w under the length bound. This yields both signs of the *target image* as choices even though only a rightward first entry was constructed. At the intended floor the developed coordinate is σm+2wn+(e(s)+ds)/2. Folding into the physical column puts the hit at m+σ(e(s)+ds)/2. The near and far abscissae of the foot visit differ from this hit by at most hs, so the visit stays within distance 1/2 of m. In the integer case the floor hit lies strictly on the chosen shallower side. Any crossing of m on descent occurs strictly before the shallow floor because (e(s)+ds)/2>0; the deeper neighbor is open there. On ascent the ray moves farther into the shallower side. The half-integer case stays in one open column. The selected target therefore has a regular approach for every L above the threshold, including when the midpoint faces a step. In particular choosing the sign of the physical launch is unnecessary in this case.

The constants are polynomial for this class. For a base box with both dimensions ≤B, t for J₀ is O(B²), since consecutive visits are spaced by 2A. Its reciprocal width is t(t−A)/(bA)=O(B⁴) for b≥1. Thus d₁=O(B⁵), t for J is O(B⁶), and 1/|J|=O(B¹²); the displayed length cutoff is O(B¹³). The b=0 formulas are smaller. These coarse exponents give no census-scale numerical guarantee. For each constructed shallow seed, s=(σi+4wn+b)/(t+2L+2h−d), so its primitive axial denominator is bounded by t+2L+2H. For deep targets use the analogous direct denominator t₀+d from J₀. This proves a polynomial denominator bound in the enlarged box for these pairs.

## Using a return itinerary of the end itself

Here is the test I get for a source with a regular, possibly oblique first-entry interval. It explains the remaining existence issue. Take positive slope magnitude s on a fixed signed branch. On the doubled transverse circle of circumference 2w let α(s)=α₀+Ds be the developed source phase at the near mouth; transverse phase increases with travel. For a fixed d, choose a signed target phase β at x. A first return from the far mouth through the foot, starting at phase θ, has a domain of regular inputs (s,θ). On a fixed itinerary its outgoing phase is

    R(s,θ) = θ+c+Bs   (mod 2w).

Indeed the unfolded horizontal displacement is s times the total axial travel B between the two mouth contacts. B is constant on the itinerary because the mouth and horizontal reflecting levels are fixed. Folding back into the signed exit chart adds a fixed offset c; the transverse sign is already encoded in θ. Direct reflection from a closed part of the mouth is the branch B=0. A regular branch persists on an open set by clearance from its corners and gate endpoints.

The actual incoming phase is θ=α(s)+Ls. After the return there are L−d axial units to T. Eliminating Ls shows exactly which part of the return domain matters:

    θⱼ(s) = [α(s)+β+ds−c−Bs+2wj]/2,     j=0,1 modulo the circle.

If the source leg is regular throughout an interval J of positive width and one such graph lies **inside the return domain** there, then every length satisfying

    L > max{d, 2w/|J| + (d−D−B)/2}

admits a legal one-return seed. On J the difference α(s)+Ls−θⱼ(s) has derivative L+(D+B−d)/2; it sweeps more than one period and thus hits 2wℤ. This solves both entrance and target matching, with a regular final approach. Conversely every regular one-return seed of this itinerary satisfies the graph equation. For a fixed upper first-entry interval of width η, targets with dη>2w already follow from the direct sweep, whose derivative is D+d. Thus only finitely many integral depths and transverse columns require return data per fixed source. A room containing seeds for those end-relative collar pairs at some reference lengths can also propagate them individually by retained-pair re-aiming beyond those lengths. [Retained-pair argument](l1-reaim-threshold.md)

**First failed implication.** A regular excursion of the foot provides an open set in (s,θ). Its existence at a slope available from S gives no intersection with either of the two prescribed graphs. Changing L tunes the incoming phase, but cannot change the eliminated equation. The vertical-entry theorem constructs the needed regular visit by choosing the side of a step; a general inclined first entry does not give both small tilts from the same abscissa. The rectangular shoulder above supplies entry next to an outer side of the strip. An open case is an irregular upper chamber whose available oblique first entries approach an interior endpoint of a partial mouth, with a shallow new mark facing a stepped foot. For an entry phase tending to an interior coordinate b′, the two nominal midpoints (b′+i)/2 and (b′−i)/2 can fold to different physical columns. The sign choice above then ceases to select either side of the same step. The one-return test leaves alternative itineraries and repeated visits open. [Flat-floor result](l1-wide-insertion.md) · [d209 review](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d209-review-wide-insertion/review.md) · [d184 review](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d184-review-gaphyper/review.md)

## Follow-on: what can be proved about the denominator

The collar construction above gives a linear denominator bound for its pairs. For arbitrary **lit** pairs there is also a polynomial conversion from a bound on the *smaller* primitive component to a bound on the axial one. Here is where the wall budget gives a quantitative statement.

Let Bᵧ be the integral box height. The room has at most ten horizontal walls when r≤8. All heights h of connected vertical slices between successive integral abscissae are differences of two horizontal support levels, hence at most 45 distinct positive integers, each ≤Bᵧ. Set Λ=2 lcm(h), over these heights; Λ≤2Bᵧ⁴⁵. In the four-copy unfolding, each open unit column component has vertical circumference 2h: vertical motion goes to the top, reflects, goes to the bottom and returns. In developed coordinates shear each such vertical band by adding Λ times the horizontal offset from its left developed boundary to its vertical circle coordinate. The shift is zero modulo 2h at both boundaries, since the developed band width is one (the developed left boundary in an x-reflected copy is its physical right side). The maps glue across all integer abscissae, including reflected seams. They have common derivative ((1,0),(Λ,1)), inverse given by −Λ, and fix every lattice mark and forbidden vertex. Thus the affine image of a legal seed is legal. This argument uses the least common multiple of slice **heights**, independently of how often the original path reflects.

For primitive (p,q) with p≠0 choose an integer j nearest to −q/(Λp). The new primitive direction is (p,q+jΛp), with axial magnitude at most Λ|p|/2; primitivity follows from determinant one. A vertical seed already has |q|=1. Consequently if some seed has min(|p|,|q|)≤M, then the pair has a seed with |q|≤Bᵧ⁴⁵ M. For fixed r the power bound has degree binom(r+2,2), reaching 45 at r=8, which is impractical at census scale. Since lcm(h) divides lcm(1,…,Bᵧ), the multiplier can be replaced by min(Bᵧ⁴⁵, lcm(1,…,Bᵧ)). The observed bound on travel along one axis in the [area-21 profile](l1-seed-profile.md) implies such an M **on that slice**.

The missing statement is a polynomial M for all lit pairs at r≤8. A shear fixing p leaves an arbitrary balanced pair of large components without a useful absolute bound; the fixed-direction bound on the number of lattice steps likewise does not bound either component. I obtain no unconditional polynomial bound on the minimal denominator in the full class.
