Advances: L1 — Conditional on the marked finite-flat theorem, a dark lattice room has a bounded witness in the same chart, with a precise one-axis formula for the required cutoff. The formula also covers isolated dark rooms. Its inputs have no known numerical bounds.

# Assembling the four growth cases

Fix a full real marked orthogonal order chart C, including ties and wall incidences. Impose endpoint parities on its lattice subset after deriving the product splitting. Use the wall gcd separately on each axis. Each axis has at most 11 positive gaps when the two marks are included and at most 9 gaps between wall levels. Let A send the fine gaps to the consecutive wall gaps by summing entries. In particular the largest wall gap also bounds each fine gap. Here a chart specifies order and incidences, without freezing numerical lengths. Freezing a gap to an arbitrarily prescribed value can itself force the required bound arbitrarily high.

**Bounded-witness theorem.** Assume the full-chart dark set is the finite union of product flats (the d132/d134 argument and classifying-map completion submitted to d186). Write one such flat as U × V within the strictly positive gaps. For an axis factor U define
     
    m(U) = min ||Az||∞ over z ∈ U ∩ ℤᵏ, z>0,
           with the specified axis mark parity and gcd(Az)=1.

Set m to infinity if empty, and use the corresponding vertical map for V. Discard products with either entry infinite. Then a valid uniform wall-gap cutoff on C is

    G(C) = max over retained products of max(m(U), m(V)),

with zero for an empty list. More precisely a representative of each product has area at most kₓ kᵧ m(U)m(V), where kₓ,kᵧ count wall gaps. In particular **81 G(C)²** suffices at W ≤ 20. This is a bound for finding a counterexample if one exists. It says nothing about the largest area of counterexamples if there are any. An implication restricted to unbounded dark sequences would miss a chart with just one large normalized integral counterexample. Isolation here concerns the arithmetic restriction: every real marked dark room has a two-parameter orbit of axis scalings.

**Proof and order of reduction.** Separate positive rescalings in x and y preserve all billiard paths and the chart. They fix each of the finitely many maximal dark flats, since their group is connected. Subtract (x,y) from (2x,y) on the resulting linear flat to split it into independent axis factors. Choose minimizers in the displayed formula separately and concatenate them. All incidences, wall gcds, endpoint parities and darkness survive. Bounding area by the enclosing rectangle gives the claimed estimate. For an unbounded sequence choose a subsequence on one flat. Replace first the entire axis containing a fastest gap by its minimizer; then replace the other axis. Neither replacement changes any coordinate on the axis already finished. If both axes contain fastest gaps either order works. This proves descent in two replacements regardless of how many relative growth scales occur. It need not be physical shortening of a particular corridor.

A fastest-*scale*-first replacement on the same axis does not follow: the elementary model x₃=x₁+x₂ with (x₁,x₂,x₃)=(j²,j,j²+j) forbids bounding both fast coordinates while retaining the slower coordinate. This is a model of the inference gap, not a proposed dark room. Replacing the whole axis keeps the exact linear relations. Within one sequence, bounded integral coordinates can be made constant by subselection. Across sequences their constant values can drift without bound. The minimizations take place on the full factors before such constants are fixed. If fixed-gap values are part of the problem itself, they must be retained as constraints and the cutoff may depend on them. [Growth charts](l1-growth-modes.md) · [Axis splitting and normalized feasibility](primitive-dark-flats.md) · [Row-4 hypotheses and review status](l1-crossing-gap-transfer.md)

## What can be computed

Given a **complete list of the rational spans of integral gap vectors** in the factors, compute a saturated ℤ-basis of each rational span intersected with ℤᵏ (Smith or Hermite form), then impose mark parity on that lattice. D133 decides each one-axis feasibility problem using Smith form and positivity. For a feasible factor its minimum is computable by increasing the upper bound on each component of Az and testing the resulting finite box. This is an algorithm given the list; it was not run. The census ceiling conditional on these data is at most

    max over charts and retained products of kₓ kᵧ m(U)m(V).

The first unknown is the least primitive positive representative on the transverse axis of an unspecified dark product. Even a positive rank-one kernel spanned by (1,M) has primitive wall height M for the identity wall-gap map. This models why counting dimensions and walls gives no coefficient bound. It does not show that any room realizes this kernel as a dark factor.

D182 transfers a known seed along an integral ray. D184 can decide universality in its fixed-transverse, Presburger-domain setting by recursion on exceptional slices. Its bound uses the actual seed and crossed heights. A variable wall-gcd condition needs the separate feasibility treatment. The single-mouth row-4 estimate bounds two lengths with the end depths, door position and upper width held fixed. None supplies the missing transverse minimum uniformly. A complete effective list of factor spans would suffice; so would a uniform bound on m for every feasible axis factor, without such a list. A lower clearance for one known seed alone does not bound where an entirely different dark factor can first meet the lattice. No numerical extension of L2 follows. [Parallel and disjoint cuts](l1-gap-hyperplanes.md) · [Single-mouth bound](l1-cross-cap-budget.md)

## L3 follow-on: real marks, integral walls

The product proof works for real marked gaps without requiring either mark to be rational. Keep integrality on the walls: minimize ||Az||∞ over positive real z in U with Az integral and primitive, dropping the lattice-mark and endpoint-parity restrictions. The attainable norms are positive integers, so a minimum is attained whenever feasible, even if the mark fiber is open. Take the two minimizing real lifts independently. This gives the same area formula for an interior real dark witness on a normalized lattice room. It gives neither a denominator bound for those witnesses nor a real-pair certificate from an L2 lattice-pair check.

Here the rational span of *integral marked* vectors can lose the entire relevant real fiber. An effective substitute is a complete factor list with effective real-algebraic linear equations: project each positive axis factor onto wall-gap coordinates, retain strict inequalities, and test membership for candidate primitive wall vectors. A uniform bound on the first feasible primitive vector (or a feasibility oracle that can also certify emptiness) is still needed to terminate on empty factors. D89/d80 alternatively give bounded denominators for normalized areas ≥120 under their reviewed hypotheses; the denominator has no explicit value, and that route does not cover smaller areas. [Denominator theorem](dark-locus.md)

**First open case.** Even with the other axis frozen after descent, its chosen primitive wall gaps have no known chart-uniform numerical bound. Bounding the first positive primitive transverse representative on an occupied-cross dark flat would make the remaining fixed-axis descent applicable on a bounded list, within its stated domain. No searches or census extension were performed.

**What is the smallest W ≤ 20 room this result doesn't cover?** The bounded-witness theorem does not establish illumination for the W=10 ledger word LLLRLLLRLR, realized by (2,0),(4,0),(4,1),(3,1),(3,4),(0,4),(0,3),(1,3),(1,2),(2,2). No ledger status changes.
