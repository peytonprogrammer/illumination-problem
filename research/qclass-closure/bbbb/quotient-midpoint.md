# Wall cost of a quotient that blocks every lift pair by one half-turn

**Theorem for review.** Let X be the translation unfolding of a bounded strictly simple polygon with genuine turns, with wall directions among multiples of π/4. Let F be all physical corner lifts and A,B the complete lift sets of two distinct interior marks. Suppose f:X→Y is a finite translation covering of compact connected translation surfaces, f(A)={a}, f(B)={b}, and Y has an affine involution e with derivative −I interchanging a,b. Require the full-fiber midpoint rule f⁻¹(Fix e)⊆F. In the orthogonal case such a quotient cannot exist at any wall count. In the genuinely mixed case it requires **at least 24 walls**. In particular the list of degrees and fold types with all three properties at W≤20 is empty, for every reflex count and every torus base T. No search was used.

The transfer rule means every preimage of each proposed fixed-point blocker is forbidden. If one instead asks only about selected geodesic itineraries or only about fixed points independently known to be reachable as midpoints, that is a weaker hypothesis. The proof below uses the full-fiber rule. The endpoints are regular, so a=b is already excluded by this rule.

## 1. Recover the rotation symmetry without assuming it descends

Let R be the physical copy rotation, of order l=4 for mixed rooms or l=2 in the orthogonal case. Its derivative is the corresponding primitive root of unity ζ. The cyclic quotient X/⟨R⟩ is the two-copy sphere double. The central half-turn R^(l/2) fixes every corner lift: its linear part belongs to the subgroup of the incident wall reflections at every genuine corner. Consider the holomorphic map

    Φ(x)=( f(x), f(Rx), …, f(R^(l−1)x) )  into Y^l.

Normalize its irreducible image curve to obtain X —u→ Z —v→ Y, with v the first projection and f=vu. Give Z the form pulled back by v. Its pullback to X is the original form, so these are translation maps. The cyclic coordinate shift gives an automorphism r of Z with uR=ru and derivative ζ; its order is l. The map X/⟨R⟩→Z/⟨r⟩ is surjective, so Z/⟨r⟩ is a sphere by Riemann–Hurwitz.

**Normalization does not separate the selected lifts.** At every point of A, all the factors of Φ are at the same regular a, since R permutes A. Regularity downstairs follows from regularity upstairs by the local order formula. In flat coordinates centered at a the image germ is exactly the smooth disk (t,ζt,…,ζ^(l−1)t), independent of the chosen lift. Thus all of A maps to one point α on the normalization, even if another image branch passes through the same tuple. The same is true of B at β. In particular deg u≥|A|, which is eight for a mixed room. The new rotation fixes α and β separately.

Acting by e in all coordinates sends that disk at (a,…,a) to the very same disk germ at (b,…,b), with parameter −t. Two irreducible image curves sharing an open analytic germ agree. Hence the coordinatewise map preserves the image and lifts to an involution ε of Z exchanging α,β, with derivative −I. It commutes with r because the coordinatewise map commutes with cyclic shift. This is the descent step in the *refined* quotient; no invariance of the original sheet blocks under R was assumed.

## 2. Two involutions on the refinement must be free

Put τ=r^(l/2). If ε fixed z, every point x above z under u would project under f to a fixed point of e. By the transfer rule x would be a physical corner lift. Thus τz=z as well. Two holomorphic −I involutions fixing the same point of a translation surface coincide. Indeed at a point of order k take a local coordinate w with centered flat primitive w^(k+1); each involution acts by w↦λw, λ^(k+1)=−1, λ²=1, leaving only λ=−1. But τ fixes α,β separately, whereas ε exchanges them. This contradiction proves ε is free.

The commuting product δ=τε is a nonidentity translation involution. It too is free. The upstairs zero orders are even (orthogonal orders 0 or 2; mixed orders 0,2,4,6). The local pullback formula k_X+1=e_x(k_Z+1) gives even orders on Z. At a fixed point of δ we would have λ^(k_Z+1)=1 and λ²=1, hence λ=1. That would make δ the identity on an open disk and hence everywhere.

On H=Z/⟨τ⟩ the common action induced by ε and δ is a free involution. Over a singleton τ-fiber a fixed base point would force ε to fix it. Over a two-point fiber ε and δ would both have to swap the points, whereas their product τ also swaps them. In particular genus(H)≥1. For an orthogonal room H=Z/⟨r⟩ is the sphere from step 1. This proves the orthogonal exclusion.

## 3. Cost in the mixed case

Now l=4. On the sphere Z/⟨r⟩ let m count branch values with stabilizer of order four, and let b₂ count those with stabilizer of order two. The intermediate double cover H→Z/⟨r⟩ branches precisely at the m values of the first kind (inertia maps nontrivially to ⟨r⟩/⟨τ⟩ there). Thus m=2 genus(H)+2≥4.

The involution ε induces a *nonidentity* Möbius involution on this sphere. If it induced the identity it would be a deck transformation of the cyclic quotient, and its derivative would make it τ, already excluded. There are two fixed sphere points. Neither can have a singleton fiber, since ε is free. On an unbranched fiber ε commutes with the regular cyclic action of order four. Its permutation must be a shift of order dividing two: either it fixes points, or it is the shift by two, in which case δ fixes points. Both are impossible. Each fixed sphere point therefore has stabilizer of order two, giving b₂≥2.

Riemann–Hurwitz for the cyclic cover now gives

    2 genus(Z) − 2 = −8 + 3m + 2b₂ ≥ 8.

Hence genus(Z)≥5. Applying Riemann–Hurwitz to u gives genus(X)−1≥8(5−1)=32. On the other hand, if the W corner angles are aᵢπ/4, each corner has gcd(4,aᵢ) lifts, with total zero order aᵢ−gcd(4,aᵢ). Since Σaᵢ=4(W−2),

    genus(X)−1 = [4(W−2)−Σ gcd(4,aᵢ)]/2 ≤ (3W−8)/2.

It follows that W≥24. At W≤20 the upper bound is genus(X)≤27, six below the required 33. This is a necessary wall count; existence at 24 is not asserted. It uses no degree or cusp estimate, and the first map of a proposed X→Y→T already suffices.

## Controls and the actual converse

- The d72 cov446 pair (W=18) is directly visible while no choice of lifts shares an open corner-cut cylinder in any primitive direction. Accordingly cylinder separation in that sense cannot force the proposed blocks. [Saved complete orbit](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d72-cylinder-test/README.md)
- In R22 the certified staircase fold has degree three. A translation map collapsing four distinct regular lifts of one interior mark to a single point has degree at least four. More concretely the staircase marks are distinct smooth-wall points, each with two lifts on the staircase unfolding. The fold uses an intermediate odd-coordinate vertex along a developed path and a separate proof for reversed paths at seams. Its five size-three blocks in the 15-sheet pillowcase action do not give the complete lift collapse in this question. [R22 manuscript](../../illumination-publication/repository/preprints/twenty-two-wall/manuscript.tex) · [D93 sheet blocks](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d93-review-blocks/review.md)
- D140 supplies examples where separation coexists with primitive monodromy and a half-turn. It does not classify every example of separation in a primitive action. Nor does every-direction geometric separation say that two specified sheets never occur in the same raw primitive-word cycle: a forbidden site can cut the corresponding leaf. [Half-turn fibers](half-turn-fibers.md)

For actual all-lift darkness, the implication “dark implies this quotient” at W≤20 is therefore equivalent to nonexistence of such a dark pair in that range. We have proved the nonexistence of the *quotient*, not the nonexistence of the pair. R22 is an example of a different quotient mechanism outside the range, not a counterexample to the W≤20 implication. The feature to retain from it is that different relative lift choices can retain different images and meet different blockers. Replacing that family by a single matched pair loses exactly the information used by the staircase argument.
