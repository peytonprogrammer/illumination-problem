# A common quotient cannot block all relative lift choices by half-turns

**Theorem for review.** Let P be a strictly simple orthogonal or genuinely mixed 45° room with at most 20 walls. Write X for its translation unfolding, F for its physical corner lifts, and A,B for the complete, distinct physical interior endpoint orbits. There is no finite translation map f:X→Y such that, for **each** (x,y)∈A×B, there exists an affine involution e on Y of derivative −I with

    e f(x)=f(y),                  f⁻¹(Fix e)⊆F.

The involution may depend on both lifts, the quotient can retain arbitrarily many endpoint images, and an empty fixed set is allowed. The same quotient and the full-fiber transfer condition apply to every pair. This extends [the one-image obstruction](quotient-midpoint.md). Intersection of f(A) and f(B) is impossible under the hypothesis: the involution for a coincident pair would fix the image of a regular physical interior lift.

### Refine once and match every pair

Use the cyclic refinement u:X→Z from quotient-midpoint.md, the normalization of the image of x↦(f(Rʲx))ⱼ. Here R is the copy rotation of order l=2 or 4. The first projection gives f=vu. The cyclic shift induces r of derivative ζ=exp(2πi/l), and Z/⟨r⟩ is a sphere. Denote u(A),u(B) by A',B'. They are disjoint and individually r-invariant. We do **not** assume normalization preserves their original sizes.

For any x,y choose an admissible eⱼ for the pair Rʲx,Rʲy. Act on the product coordinatewise by these possibly different involutions. At the tuple of x this maps the smooth parametrized image germ with centered flat coordinates (ζʲt)ⱼ to the corresponding germ at y with parameter −t. All those coordinates are at regular points because x,y are regular. Thus the irreducible image curve is preserved and its normalization acquires an involution ε exchanging u(x),u(y), of derivative −I. In particular such a map exists for *every* pair in A'×B'.

Set τ=r^(l/2). It fixes u(F), because the physical half-turn fixes F pointwise. If ε fixed z, the first coordinate e₀ would fix v(z), hence every point in u⁻¹(z) would be in F. Then τ would fix z too. Two −I involutions fixing a common point agree by the local flat primitive coordinate. But τ preserves A' and B' separately. Thus ε is free.

Although the eⱼ were chosen separately, ε commutes with τ. A torus admits no free −I involution, so Z has a zero. Every zero is in u(F), since its preimages are zeros on X. The conjugate ετε⁻¹ fixes every zero just as τ does; agreement at one zero suffices. All zeros on Z have even order by the pullback order formula and the odd values of ord+1 on X. Consequently the translation involution τε is free (at a fixed point its germ in the primitive-root coordinate would be multiplication by a root of unity of odd order). The induced involution on H=Z/⟨τ⟩ is free: on a hypothetical fixed two-point fiber ε and τε cannot both swap the two points because their product is τ. On a fixed singleton fiber neither could be free. Thus H has positive odd genus. This already excludes the orthogonal case, where H is the sphere.

### Every admissible map on the refinement commutes with r

For mixed rooms H double covers the sphere Z/⟨r⟩; denote the deck involution on H by j. If genus(H)≥2, j is the unique hyperelliptic involution. If H is elliptic, a free holomorphic involution is translation by a nonzero point of order two and commutes with j(z)=c−z. Hence the map induced by ε on H commutes with j in either case. Upstairs εrε⁻¹ is therefore r or τr; its derivative is i so it equals r. The argument is the commutation proof of [free-half-turns.md](free-half-turns.md); here it does not need the branch values on the refined sphere to be real.

Let m denote the number of order-four branch values on that sphere and b₂ its number of order-two branch values. As in the one-image proof, m=2 genus(H)+2. Each free ε induces a nonidentity sphere involution whose two fixed points must both be order-two branch values: on an unbranched four-point fiber commutation with r forces the permutation to be the identity or r², contrary to freeness of ε or τε. A singleton fiber also fails. In particular b₂≥2 and

    2 genus(Z)+6 = 3m+2b₂,              genus(Z)≥5.

The map from the set of these ε to sphere involutions is injective: two lifts of the same sphere map differ by rʲ and have the same derivative only for j=0 mod 4.

### Eliminate elliptic H, including the two-by-two configuration

When H is elliptic there are only three free translations of order two. Each has at most one lift of derivative −I to Z because the two lifts differ by τ. Thus every source in A' has at most three partners, so |B'|≤3; by reversal |A'|≤3. On each set the permutation r has order dividing four, hence its square τ fixes each point (there is no four-cycle). Projection to H is injective on these τ-fixed points, including across the two sets. On H all differences between the two sets belong to H[2] minus zero. Both sets therefore occupy one coset of four points.

If either is a singleton then deg u≥8. Since genus(Z)≥5 this gives genus(X)−1≥32, whereas W≤20 gives genus(X)−1≤26 by the wall formula in quotient-midpoint.md. Otherwise the two disjoint sets must have size two each. In a coset of (ℤ/2)² a partition into two pairs has only two cross-differences (translate to {0,a} and {b,a+b}). Call the corresponding lifts ε₁,ε₂. They commute: their commutator is trivial on H and has derivative I on Z, whereas the nontrivial deck map τ has derivative −I. Their product δ is a translation involution swapping the two points within each set; this follows on H by adding a, and upstairs by injectivity on the τ-fixed points. It is free since its elliptic projection is a nonzero translation.

Now quotient Z by δ. Both endpoint sets collapse to singletons and ε₁ descends to exchange them. The descended map is free: a fixed orbit would force ε₁ or δε₁=ε₂ to have a fixed point on Z. This is exactly the single-pair quotient excluded at W≤20 by quotient-midpoint.md. This rules out the entire elliptic case.

### Eliminate higher genus H by counting branch values

Since genus(H) is odd, the remaining values are ≥3, giving m≥8 and genus(Z)≥11. Riemann–Hurwitz and genus(X)−1≤26 now force deg u≤2. If deg u=1, Z is the physical unfolding, where [the mixed-room free-involution classification](free-half-turns.md) gives at most one partner per source lift among the eight (d141 review pending).

For deg u=2 the covering is unramified: a local degree of two would divide the odd integer ordₓ+1 at some x. Hence genus(X)−1=2(genus(Z)−1), so genus(Z)≤14. Freeness makes genus(Z) odd. Thus genus(Z)∈{11,13}. From 3m+2b₂=2 genus(Z)+6 and m=2 genus(H)+2∈{8,12,…}, necessarily m=8 and b₂=2 or 4, respectively.

Every eligible sphere involution fixes two of those b₂ values. If b₂=2, there is at most one: a nonidentity Möbius involution is uniquely determined by its two fixed points. If b₂=4, it fixes two and transposes the other two. The action of the group preserving four sphere points on those points is faithful. Two realized transpositions cannot share exactly one moved point: they would generate S₃ fixing the fourth point, whereas a finite group of holomorphic Möbius maps fixing a point is cyclic (conjugate the point to infinity; a finite affine group has a common finite fixed point by orbit averaging). Hence at most two such transpositions occur. The injectivity of the lift gives at most two eligible ε on Z. Yet eight target lifts have at least four distinct u-images at degree two. One source cannot have four partners under two maps. This exhausts the cases.

**Scope.** This excludes a fixed quotient with a collection of global mark-exchanging midpoint involutions. R22 uses the lattice parity of the particular developed path and seam reversal, and makes no such assertion about global involutions. Neither d140 nor this exclusion supplies a theorem that genuine darkness must admit these witnesses. A different quotient for each relative lift choice, or a path-dependent parity obstruction, is outside this proof. No room or direction search was used.
