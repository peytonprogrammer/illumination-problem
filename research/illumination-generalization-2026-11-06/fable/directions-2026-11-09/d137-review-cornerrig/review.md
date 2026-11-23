# D137: review of corner-orbit-rigidity.md (snapshot 2026-11-21 23:05)

Date: 2026-11-21. Reviewer: adversarial referee.

Reviewed file: `d95-review-queue/snapshots/corner-orbit-rigidity.2026-11-21-2305.md`. It is identical to `qclass-closure/bbbb/corner-orbit-rigidity.md`. Context read: `parametric-orbits.md`, `length-periodicity.md`, the d132, d135 and d136 reviews, and `claude-illumination-check/angle-rigidity-review/findings.md` for the R22 data.

Code: [checks.py](checks.py), log [checks.log](checks.log). Run it with `python3 -B checks.py > checks.log`. It uses exact `Fraction` arithmetic and takes 62 CPU seconds. It builds four named rooms and no room families. Each ray leg is capped at 4,000 reflections, and no cap was reached. No network access was used.

## Verdict

**Sound with gaps.** The opening lemma, the equivariance argument, the Veech-orbit finiteness and the projector P are all correct. The commutant step correctly gives scalar A in mixed rooms and diagonal A in axial rooms. The replay agrees with every sign and kernel prediction it tests. The gaps concern how the rigidity conclusion is sourced and scoped, not the algebra. The most important one is scope: the test is a per-seed certificate and has no route to a W ≤ 20 statement. In the replay, every seed tested has the trivial kernel, lit or dark, so rigidity separates nothing.

## 1. The opening lemma

**The derivative identity is correct.** D(t) = det(hₜ(a), hₜ(b)). Then D′(0) = det(η(a), ρh(a)) + det(h(a), η(b)) = det(h(a), η(b − ρa)), because ρ is a fixed number along the family.

**The sign gives the side.** The chord from the source to the developed target has direction h(a) + h(b). The corner sits at h(a), and det(h(a) + h(b), h(a)) = −D. So D > 0 puts the chord to the left of the corner. One sign of t therefore puts it on the bypass side.

**Legality holds.** The two legs are compact, and away from C they have corner-free tubes. Near C, the bypass side is a flat half-disk. For a small perturbation the developed chord stays inside this union, so it is a corner-free path between the perturbed marks. Self-overlap of the developing map is harmless, because the tube is a chart along the path. The neighborhood is uniform: for all p near the seed with σ·D(p) > 0, the path exists. The note doesn't say this, but the remark in section 3 uses it.

**One-sidedness is automatic.** At a cone point every incoming germ has exactly two continuations at angle π, one on each side. They coincide exactly when the lift is regular. So the hypothesis "on one side the sector is exactly π" says only that the outgoing leg is one of the two one-sided limits. The phrasing is correct but redundant. At a regular forbidden lift, both signs of D open a path, as the note says.

**Other cases.**
- A second corner on either leg is excluded by "no other forbidden contact". Routes through two corners give inequalities, not equations, so excluding them is correct. It costs constraints: in lattice rooms, many saddle connections meet several corners.
- Simultaneous corner hits fall under the same exclusion.
- A leg along a wall line ends at the wall's far corner, so it is a two-corner route and is excluded.
- Passing a mark lift early is harmless, as the note says.
- The note forbids contact with every corner, including regular convex lifts. This matches `parametric-orbits.md`. Under a reflex-only stopping rule the constraints stay valid, because the perturbed path avoids all corners.

**Replay (checks.log, "opening-lemma replay").** For up to 12 templates per room, I moved the room by ±ε·v with ε = 1/4000 along a random integer chart direction v that has a nonzero row. I then traced the perturbed room exactly along the developed chord and asked whether T is reached at the template's own length before any corner.

| Corner type | Agreement |
| --- | --- |
| Singular corners: path legal exactly when σ·D > 0 | 58/58 (4 L-room, 20 dumbbell, 24 R22, 10 mixed) |
| Regular forbidden corners: path legal for both signs | 38/38 (20 L-room, 4 dumbbell, 0 R22, 14 mixed) |

## 2. Finiteness, equivariance and the projector

**Finiteness is correct.**
- All Σ points lie over the origin of the torus. Reflections in the allowed directions have signed-permutation linear parts and integral translations, including the 45° walls (x, y) ↦ (y − c, x + c).
- Labelled origamis of a fixed degree form finitely many SL₂(ℤ)-orbits, so the labelled Veech group has finite index.
- Primitive vectors form one SL₂(ℤ)-orbit, so right-coset representatives applied to e₁ meet every orbit of directions.
- In one rational direction there are finitely many legs.
- The termination argument is correct: the predecessor of a corner's outgoing state is the corner itself, so that state cannot lie on a cycle of regular states.

**Equivariance is correct.** For g in the labelled affine group, h(g₊a) = Dg·h(a). The image template has the same ρ and the same straight-angle side, and its row is the pairing of (Dg ⊗ g₊)(h(a) ⊗ z). Every template is the image of a template in a representative direction. So the span of the generator-invariant closure of the representative tensors equals the span of all templates. The note's "loses no constraints and adds none" is exact. The rows live at the fixed seed, so no equivariance of η is needed.

**The projector P is correct.** Physical velocities satisfy η(k₊z) = kη(z) for every room symmetry k. So pairing (k ⊗ k₊)t multiplies the pairing of t by det(k). Then P is the projector onto the det-twisted invariants, and t and P(t) give the same row. P(W) = P(ℚ² ⊗ ker h) forces η to vanish on ker h, so η = A∘h. The note is right that the orbit span must be closed before projecting.

**What wasn't checked.** The note ran no enumeration, and I didn't build the Veech group. My replay uses every non-wall-parallel primitive direction with max(|p|, |q|) ≤ N, for N = 4, 6, 8, 10. Any subset of valid rows bounds the kernel from above, so a trivial bounded kernel is already conclusive. In all four rooms the rank stops growing by N = 6, at the maximum the trivial motions allow. This is consistent with finiteness but doesn't test it, because the rank can't grow past saturation. The Veech machinery matters only when the bounded kernel stays nontrivial.

## 3. Kernel and rigidity

**Scalings: the claimed kernel matches the replay.** Commuting with diag(1, −1) and with the swap forces A = aI in mixed rooms. In axial rooms it forces A diagonal. The two axis scalings are exactly the note's axial case, so the note is consistent with them. The headline sentence mentions only the mixed case, with kernel dimension one. For axial rooms the minimal anchored kernel is two, so "kernel = uniform scaling" can never hold there.

The replay matches this. In unanchored chart coordinates (wall-line offsets plus marks), the trivial motions are two translations plus the admissible scalings.

| Room | Chart dimension | Kernel dimension | Trivial dimension | Weak-order cell (params, kernel) |
| --- | --- | --- | --- | --- |
| L-room 4×4, notch 2, S=(1,3), T=(3,1), lit | 10 | 4 | 4 | 10, 4 |
| Dumbbell U=4, L=1, S=(2,1), T=(7,3), lit | 16 | 4 | 4 | 11, 4 |
| R22 (room Q), S=(0,0), T=(2,2), dark | 26 | 4 | 4 | 14, 4 |
| Mixed V-notch (d135 room B), S=(1,2), T=(3,2), lit | 9 | 3 | 3 | not computed |

- Every row vanishes exactly on the trivial motions in every room ("max |row · trivial| = 0").
- R22 has no direct legal direction up to N = 10, which is consistent with darkness.
- The three lit seeds each have direct legal directions.

**The R22 consistency check is weak.** The only dark flat known through R22 is the trivial one. The rows vanish on it identically, since η = Ah kills ker h. So the check required by item 4 passes, but it can't fail. The R22 rank of 22 in the chart agrees with the earlier 147-witness fixed-angle result.

**Rigidity follows, given local flat structure.** Suppose the dark set near the seed is a finite union of flat germs through the seed. Then a kernel equal to the trivial span gives local rigidity. The note asserts this structure without a citation. It comes from EMM's local linearity together with the LMW marked-point convention, as reviewed in d132 and d116.

**The note under-claims.** The note confines the conclusion to the seed's weak-order cell. A lattice seed sits in a low-dimensional cell: R22 has 12 anchored cell parameters against 24 in the chart. The restriction isn't needed. Near any seed the unfolding's topology is constant in the fixed-direction chart. Its relative periods, which are developed edge vectors and mark-to-vertex vectors, are linear in chart coordinates. So the local flat structure holds in the chart, and each dark germ through the seed is two-sided there. A dark branch in an adjacent cell has the seed in its closure. It therefore lies in a germ through the seed and is covered by the same kernel test. The chart kernel is never larger than the cell kernel, so the chart test is the stronger one. For R22 it is already trivial.

**A finite-flat-free cross-check.** By the uniformity remark in section 1, the dark tangent cone at the seed lies in {v : σᵢℓᵢ(v) ≤ 0}. Regular corners contribute ℓᵢ = 0. I tested exactly, with an LP, whether this cone equals the kernel. By Gordan's theorem, it does exactly when the sign rows have a strictly positive dependence. The answer is True in all four rooms. So at R22, no nontrivial first-order dark direction leaves the seed in any cell, even one-sidedly. This uses no flat structure. The note could adopt it as a strengthened test.

## 4. Scope

**What is proved.**
- A correct necessary linear condition on two-sided dark flats at a lattice seed.
- A correct reduction of all such conditions to a finite computation, which the note doesn't bound.
- A correct saturation criterion and its projection to the symmetry component.
- Given local flat structure, kernel = trivial implies local rigidity in the fixed-direction chart. This is more than the cell statement the note claims.

**What is not proved, and what is needed for W ≤ 20 or an area bound.**
1. A dark seed with W ≤ 20 to test. The test is per seed, and none is known.
2. A reason why rigidity constrains area. In the replay, rigidity is generic: four of four seeds, three of them lit, have trivial kernel by N = 6. A rigid dark seed's dark flat is its own scaling ray. So the coefficient height H in `parametric-orbits.md` is just the seed's own size, and the argument is circular.
3. To be useful, the method needs one of the following:
   - Templates that exist uniformly in fixed relative classes over an open set of a combinatorial type, combined across directions into an incompatibility.
   - An arithmetic statement that bounds the coordinates of rigid dark rays.
   - A theorem that nonrigid dark flats always descend to a smaller lattice room, together with a separate bound for rigid ones.

   The note supplies none of these and claims none.

## Gaps

1. **High (scope).** The method has no route to W ≤ 20 or to an area bound. Rigidity is generic in every tested seed, and a rigid dark ray yields no height bound. The note disclaims this, but its "outstanding structural question" is the whole problem.
2. **Medium.** The local finite-flat structure is the load-bearing input for "kernel ⇒ rigidity", and the note asserts it without a citation. Cite EMM local linearity, LMW §2.2 and the d116/d132 marked-point review.
3. **Medium.** The finite procedure was never run, and nothing bounds the cover degree, the cusp count or the orbit sizes. For R22 the unfolding has 60 squares with labelled mark lifts, so the cusp count may be large. Bounded-direction rows already give a valid kernel bound and saturated at N = 6 here. The note should say that the Veech step is needed only when that bound stays nontrivial.
4. **Low.** The note under-claims. The cell restriction and the worry about adjacent cells are unnecessary, because the period map is linear in the full fixed-direction chart near the seed. The one-sided LP cone test is a further strengthening that doesn't need flat structure.
5. **Low.** The headline gives kernel dimension one for mixed rooms only. For axial rooms the minimum is two, from the two axis scalings. State this so that "kernel = uniform scaling" isn't applied to axial rooms.
6. **Low.** The one-sided bypass hypothesis is automatic: every germ has two π-continuations. Multi-corner routes and wall-parallel legs are excluded. Both points should be stated.
7. **Low.** The darkness convention forbids every corner. Say that the constraints remain valid under a reflex-only stopping rule.
8. **Low.** The required check that the rows hold on the actual dark flat is vacuous at R22, because the only known dark flat is trivial. No nontrivial dark flat is available to test the lemma against.
