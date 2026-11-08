# Stronger ideas after rejecting the midpoint proposal

> Update 2026-10-31: the remaining SAME-surface contact22 refolding route has a stronger conditional lattice obstruction in `refolding-lattice-obstruction.md`, mathematically accepted by a read-only Opus challenge on supplied data. Independent code/data check is pending. The earlier quarter-turn enumeration recommendation is superseded; no ray search is authorized.

[done] Two further focused Opus consultations completed: reset-opus.md (different geometric categories) and reset-topology-opus.md (topology-changing surgery). Neither supplied a convincing new sub24 construction. Their claims are not adopted as theorems merely because the responses label them so.

## The correction

An unexplored parameter or target class is not itself a construction mechanism. The midpoint proposal lacked a structural reason for darkness. Further geometry sweeps of that kind are deferred. A new direction should identify why a hypothetical connecting ray is impossible, or transfer an existing all-ray obstruction through a precisely specified operation.

## Best conditional direction: a genuinely different mirror action

Use the known dark marked translation surface, but change its mirror quotient rather than trying to rediscover darkness. This has an explicit sufficient transfer statement.

Let X carry finite marked source and target sets A,B with no straight connecting segment in X\Sigma. Let H be a finite affine group that preserves A,B separately. Average a positive definite form over its derivatives:

    Q = sum_{h in H} (Dh)^T Dh.

This makes H an isometry group for the constant flat metric Q, while preserving the unparameterized straight lines and hence the known dark relation. If X/H develops injectively to a simple planar polygon, all interior points are regular, the boundary consists of mirror arcs, every old blocker in Sigma descends to a genuine new corner, and A,B contain distinct free H orbits, the resulting physical source and target are dark. Count its maximal straight boundary segments; a reduction is a construction rather than a new visibility search.

Every condition is essential. Quotients with holes, interior cone points, self-overlap, smooth images of old absorbing points, or mixed source/target orbits fail the gate. Taking an arbitrary surface cut is insufficient.

**The crucial distinction:** H must be a different affine-conjugacy class relative to the source/target/blocker marking. If H=F G F^-1 for an affine automorphism F preserving these markings and G is the old irreducible D4 action, the invariant metric is proportional to the conjugated original metric. The quotient is similar to the original room and has the same wall count. Ordinary stretching and moving a fundamental domain therefore provide no improvement.

The old source and target sets each have8 points. A selected free source orbit gives |H|<=8. Divisibility by8 requires the stronger assumption that ALL old source points remain interior/free. Order6 must therefore be considered; the newer local cone-angle gate excludes it for these controls because they have index3 cones. See refolding-bound.md. The earlier blanket exclusion of order6 by divisibility was too strong.

A finite affine action can be more general than an isometry of the original metric. Restricting to Isom(X) misses this possibility. Conversely, conjugating the old action by an affine automorphism only reproduces the original quotient after adapting the metric. The live target is a nonconjugate action, not an untested relabeling.

**Current evidence:** previous audits found trivial derivative-I automorphisms on the controls. A square-tiled surface with full canonical D4 and trivial translation kernel has no additional Euclidean isometries: derivatives preserve its absolute-period lattice, whose point group has at most8 elements, and the8 canonical ones already exist. Cone points force derivative-I automorphisms to preserve the square grid. Thus fixed-metric refolding is strongly constrained; changing the affine mirror structure and metric together is the only remaining version proposed here. No nonconjugate action has been found or enumerated in this turn.

The exact reset-probe.py checks the relevant algebra: D4-invariant metrics have dimension1; D2-invariant metrics dimension2; with the standard quarter-turn fixed, the only compatible integer reflections are the four canonical ones; three conjugated D4 examples average to the conjugated original metric. These are algebraic checks, not actual new affine actions on the room surface.

## A separate exact route that escapes tiling: nondegenerate compactness

This is a derived existence criterion, not an achieved construction. Fix a compact family K of polygons with at most23 walls and marked S,T. Normalize coordinates and impose closed positive clearance bounds on nonadjacent edges, edge lengths, angles, S/T distance to the boundary, and S-to-T distance. Every member of K remains a genuine simple room.

A nonsingular S-to-T path with finitely many transverse reflections persists under small perturbations: unfold its fixed finite wall word, connect the perturbed endpoint images, and use the strict corner/edge inequalities to retain the itinerary. Therefore the set of illuminated configurations with <=L reflections is open relative to K. Its complement C_L is compact, and C_{L+1} is a subset of C_L.

If C_L is nonempty for EVERY L, compactness implies a configuration in their intersection: a valid room with no finite-reflection connecting path. Equivalently, if every configuration in K is illuminated, there is a uniform finite reflection bound throughout K. This does not require rational angles or a common tiling.

A constructive version would need an analytic nested-parameter construction keeping uniform positive geometric clearance while forcing the minimum illumination reflection count to diverge. Finite capped misses do not establish this hypothesis. The known slit/contact limits fail the clearance requirement, so they do not prove a simple room exists. No such nondegenerate sequence has been found here.

## Opus suggestions rejected or narrowed

1. The proposed slit-axis flow conjugacy drops slit-tip absorption. A slit endpoint inside the room folds to a smooth point of the new axis wall. An explicit45-degree bounce at that point is valid in the half-room but terminates at the slit tip in the original. reset-probe.py checks the reflection exactly. This refutes the claimed local conjugacy; it is not itself a counterexample to the proposed global darkness equivalence. That equivalence remains unproved.
2. The assertion that every tile-compatible thickening is excluded overstates the completed result. Assemblies with four or more exceptions remain outside the proved three-exception theorem.
3. The two-folding reduction is not established at its stated generality. Its sketch assumes discreteness/finite-index properties that need hypotheses; moreover, reducing to a common refinement does not erase itinerary constraints. Endpoint saturation is not a theorem that such constraints are useless. Its claim that all folding methods are exhausted is false given the explicit remaining exception and mark hypotheses.
4. The proposed periodic-point/localization dichotomy is an unsupported conjecture. A finite affine orbit is not equivalent to being fixed by every Veech-group element. No localization theorem was verified that makes the suggested finite pentagon experiment decisive.
5. Preserving an entire wall-labeled bounce spectrum is much too strong a deformation target. The primary Bounce Theorem forces similarity except for right-angled affine cases. This theorem concerns the entire bounce spectrum, not just one dark pair, and does not rule out pair-specific preservation.

## Judgment

[done] The earlier recommendation was too optimistic. The new turn supplies sharper conditional mechanisms and rejects invalid shortcuts, but has not produced a demonstrably promising construction, a new dark room, or a sub24 example. No additional blind geometry search was run. All consultation processes finished; old artifacts, peer files, AGENTS.md and git state were left unchanged.

[waiting on Claude] Independently assess the nonconjugate-action transfer lemma and the nondegenerate compactness criterion, using the explicit hypotheses above. Arithmetic probes cannot replace those geometric checks.

**Next move:** test whether a known dark marked surface has a nonconjugate finite affine reflection action with an admissible simple polygon quotient. If only conjugate actions exist, reject this construction route rather than increasing a direction-search cap.

## Research constraint from Daniel

Daniel explicitly instructed: “avoid ray searches until you have a really promising theory.” No direction sweeps, tracing pilots, or ray-cut geometry searches are authorized as the next move. Continue mathematical derivations and exact algebraic/geometric checks. A theory should supply a credible all-ray obstruction, a plausible simple planar realization, and a concrete reason walls can be saved before further ray searches are justified. This instruction supersedes earlier search-oriented next steps.

## Theory continuation: intrinsic corner count

The newer [refolding gate](refolding-bound.md) narrows this route: the slit20 surface fails the local cone gate; every admissible refolding of the simple24 surface still has24 walls; the contact22 surface is the live target for a simple22-wall quotient. The next algebraic target is a nonconjugate quarter-turn square root of the unique half-turn, with12 fixed points and a compatible mirror. Data and derivation are checked locally; independent peer review is pending. No ray searches were run.
