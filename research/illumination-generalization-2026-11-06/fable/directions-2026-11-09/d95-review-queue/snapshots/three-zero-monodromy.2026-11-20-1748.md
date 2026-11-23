# Period ratios for two triple collisions

**Verdict for review.** At three zeros the two-divisor argument gives a dichotomy. For the two degenerations specified below, either both triples have equal absolute periods, or in each triple one primitive integral weight is the sum of the other two in absolute value. In the second case each matching contains a zero and a pole with identical image in the canonical abelian surface. This gives a parity criterion for applying the [cover recognition theorem](three-zero-recognition.md). I cannot force the two divisors or exclude the additive alternative. The proposed same-rank boundary induction has a dimension obstruction at every z.

## Hypotheses

Use the rational rank-two absolute subsystem and saturated abelian quotient A of the previous note. Use j for the Abel–Jacobi map followed by that quotient. Suppose that two degenerations can be transported to one smooth marked fiber. Each takes place over a holomorphic punctured disk in the locus and has exactly three disjoint simple zero–pole collisions on a smooth underlying sphere, at three distinct positions. The four other poles stay apart, the limiting differential is nonzero on the main sphere, and no other marked points collide. After a finite base change label all points. Assume that in each matching the three vanishing period functionals are nonzero and proportional on the **whole absolute tangent**. For example, containment of a common local hyperplane of dimension dim M−1 in their three period kernels suffices. Proportionality along a chosen one-parameter family alone is weaker. Assume that the transported arcs form the embedded alternating hexagon of the recognition theorem.

Write uᵢ and vⱼ for the doubled arcs as oriented integral cycles. The quotient sends them to aᵢP and bⱼQ, respectively, where P and Q generate the cyclic subgroups spanned by the images of the respective triples. This uses rationality and saturation of the subsystem. The signed integer vectors a,b each have gcd one; P and Q themselves need not be primitive in the entire quotient lattice.

## The monodromy computation

Near a simple zero colliding with a pole, center a coordinate x at the pole, put the zero at s, and write the differential as (x−s)H(x,t)dx²/x, with H a holomorphic unit. The period of the doubled vanishing arc is s times a holomorphic unit: substitute x=su in its integral and use the nonzero integral of √((u−1)/u) from 0 to 1. In particular all three separations in a triple have the same order e of vanishing along the disk, even if their leading coefficients differ. Each pair therefore makes e full twists. A lifted half-twist is a Dehn twist about the doubled arc, and on homology a Dehn twist adds its core times the algebraic intersection. The arcs are disjoint, so their twists commute. Up to overall convention the first local monodromy is

    Tᵤ(x) = x + 2e Σᵢ ⟨x,uᵢ⟩uᵢ.

A common deck sign, if present, is removed by another finite base change. This argument requires no choice of twisting order between the three pairs. [Margalit–Winarski, hyperelliptic braid action](https://doi.org/10.1112/blms.12456)

Let Cᵢⱼ=⟨uᵢ,vⱼ⟩. The rational kernel of j on homology is monodromy invariant, so Tᵤ descends to the quotient. Apply j to Tᵤ(vⱼ)−vⱼ. Computation upstairs gives a common nonzero scalar times (Cᵀa)ⱼP. Computation downstairs gives bⱼ times the single vector (Tᵤ−1)Q. Reversing the roles of the degenerations gives the second relation:

    Cᵀa = λ b,       Cb = μ a,

including zero scalars. In particular a and b are eigenvectors of CCᵀ and CᵀC with the same eigenvalue.

Every nonzero entry of C is ±1, and its support is a six-cycle. Changing signs of rows and columns and ordering labels cyclically reduces C to I+R or I−R, where R is a cyclic three-coordinate permutation. Indeed signs along any five edges can be prescribed by vertex signs; the cycle sign fixes the last. In either normal form the constant vector and the plane of coordinate sum zero are the two eigenspaces of CCᵀ, also of CᵀC. For I+R the eigenvalues on these spaces are 4 and 1; for I−R they are 0 and 3. Distinct eigenvalues force both weight vectors into the constant spaces or both into the sum-zero planes, in their respective sign conventions. Primitivity in the constant case gives absolute weights (1,1,1). In the plane case nonzero entries force one absolute weight to equal the sum of the other two. Exactly two entries of a primitive integer triple with signed sum zero are odd. This proves the dichotomy, including the zero-eigenvalue case.

**Recognition corollary.** If all three primitive weights in even one matching are odd, both matchings are synchronized and the degree-three cover follows by the recognition theorem (currently in review). A geometric sufficient condition is j(Z)≠j(Pole) for all three incident pairs of one matching: doubling an arc identifies the endpoint difference in A[2] with half its projected cycle modulo the integral lattice. Any even coefficient makes that difference zero. This only concerns the six singularity labels and does not assume anything about regular periodic marks.

The additive alternative satisfies the actual two matrix equations: take R(x,y,z)=(y,z,x), C=I+R, a=(1,1,−2) and b=Cᵀa=(−1,2,−1). Then Cb=a. Thus unimodularity of individual arc intersections and monodromy invariance of the two cyclic images do not themselves force unit coefficients. This is a linear example, not a claimed minimal locus.

## Explicit sphere check of the local argument

Choose distinct complex numbers c₁,c₂,c₃ and p₁,…,p₄. The differentials

    q_s = [Πᵢ (x−cᵢ−sᵢ)/(x−cᵢ)] dx² / Πⱼ(x−pⱼ)

are in Q(1³,−1⁷) when the offsets are small and nonzero, and limit to a four-pole quadratic sphere. Infinity is regular. The three doubled short-arc periods are each sᵢ times a holomorphic unit by the substitution above. Their Jacobian at zero is diagonal and nonsingular, hence they are local coordinates in these three parameters. In particular prescribing periods (t,t,2t) gives an analytic family with those **exact** ratios at every sufficiently small t≠0. The main component has positive limiting area and the orienting one-form is regular above each simple pole. Area normalization scales all three periods together. This tests the suggested local residue and area argument. It does not construct an invariant rank-two locus. Wright's cylinder deformation theorem controls deformations of equivalence classes; rank two specifies a four-dimensional complex absolute tangent and does not give two independent cylinder shears in every periodic direction, nor prescribe unit ratios. [Wright, cylinder deformations](https://arxiv.org/abs/1303.3603)

## Induction and effectivity

For any s≥1 the unmarked orientation double of Q(1^s,−1^(s+4)) has zero relative kernel. All its zeros are fixed by the negating involution J, so there is no anti-invariant purely relative direction supported on differences of zeros. A rank-h invariant locus in this sphere locus therefore has complex dimension 2h. A proper boundary component has dimension strictly below 2h. On a connected positive-area boundary its rank h′ satisfies 2h′≤dim(boundary)≤2h−1, whence h′≤h−1. Marking the collision positions in the usual boundary description does not restore rank; forgetting them only drops relative dimensions. For a disconnected limit a projection to one factor cannot increase dimension to 2h either. [Mirzakhani–Wright, connected-boundary tangent theorem](https://arxiv.org/abs/1508.01446) · [Apisa, §§1.3, 2.2 and 4–6](https://arxiv.org/pdf/2110.07540)

Thus a proper degeneration z+1 → z preserving the parent rank is unavailable throughout the proposed induction. For h≥3 one could apply a rank-at-least-two induction hypothesis **if** one constructs a boundary in the specified lower stratum with rank at least two and proves that its covering maps extend across the smoothing. For h=2 the boundary has rank one. The lower-stratum rank-at-least-two induction hypothesis says nothing about it. One needs rank-one marked boundary geometry and reconstruction, exactly the source of the three-zero problem. The full sphere locus itself illustrates rank loss; the minimal noncover case is still open.

Even a complete qualitative exclusion of every higher-rank residual locus supplies no explicit n₀(r) from d89. A single arithmetic dark seed generates a closed rank-one orbit, and an explicit lit parameter on a higher-rank line does not bound that orbit's degree. The direct synchronized-count route still gives n≤(K+32)/ε for n≥120 *if* its explicit deficit estimate is proved. Neither constant is available here. [Effectivity analysis](three-zero-divisor.md) · [Direct estimate](route-assessment.md)

**Next theorem needed.** Show that a hypothetical minimal locus admits the two clean hexagonal degenerations and that at least one matching avoids a zero–pole coincidence in A, or geometrically rule out the additive triple supported by the monodromy equations. For the recognition result, minimality of the quadratic quotient excludes the resulting further cover; BBBB/d105 alone only rules out the specified canonical pillowcase factors.
