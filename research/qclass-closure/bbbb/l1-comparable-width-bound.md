Advances: L1 — In the intersection of the reviewed comparable crossing and the transverse-overlap geometry, wall-gcd normalization gives an explicit area bound for a template-aligned mouth, even when its physical width grows. The bound uses the overlap-phase lemma pending review.

# Eliminate both stretch factors from the overlap divisor

**Hypotheses.** Use a strictly simple orthogonal lattice room consisting of the lower box and the fixed marked template stretched by positive integers u,t, with the relative placement and near-side openings of d192. Write h,D for the box dimensions and impose wall gcd one on each axis. Assume all wall abscissas, up to translation, are integral combinations of D,u, and all ordinates are integral combinations of h,t. This holds for the origin-anchored template, and may fail for an independently drifting attachment offset. D192 confines dark placements to a bounded comparable region and gives finite lists of θ=d/h and κ=(D/u)/(h/t)=A/B in lowest positive terms (use the union of d191 lists over d192's depth list). The potentially enormous lists are effective in the template data.

Require also the transverse overlap of [the overlap-phase note](l1-overlap-phase.md): a full-height overlap column, legal lower-wing approach from the source and upper-wing approach to the target, with the uniform window, period P, overlap upper height β and Fourier bound K specified there. Use integral β and integer P. These are extra hypotheses: d192's first hit of a horizontal mouth does not establish an approach via the far vertical edge of an overlap. The direct transverse proof also works with a fixed upper bound E on ε=w/u in place of 1: the end mismatch derivative x+ε+B_travel is bounded below by B_travel>0, and the local left-gate bound involves x only. Equivalently use a template horizontal unit adapted to the width and track its period explicitly. Only the first formulation, in the original lattice units, is used below.

**The arithmetic.** Put h/t=m/n in lowest terms, T=m+βn and L=T/gcd(m,β). Thus gcd(L,n)=1. For any dark placement the [overlap divisor](l1-projective-crossing.md) gives L | Pqw for an integer 0<|q|≤K. The proof is directly from the gate equation; multiplying

    Pp(D−c−w)/(2u(m/n)) + Pqw/[2u(m/n+β)] ∈ ℤ

by 2umT and reducing modulo T eliminates the arbitrary lattice source c. Meanwhile normalization implies gcd(h,t)=gcd(D,u)=1: a common divisor would divide every wall displacement on that axis. Thus h=m, t=n, and

    g=gcd(Am,Bn),       D=Am/g,       u=Bn/g.

Suppose one usable column has width rw=iD+ju with fixed integers r>0,i,j. Multiplying the divisibility by rg and reducing m≡−βn modulo L gives

    L | Pq(iAm+jBn),          hence L | Pq(jB−iAβ).                (1)

This second reduction uses gcd(L,n)=1. The factor g need not be invertible; only multiplication by g was used. No source-denominator or small-aperture assumption enters (1).

**Explicit bound.** If Δ=jB−iAβ≠0, put S=KP|Δ|. Then h=m≤βS, t=n≤S, D≤AβS and u≤BS. With upper-template area V and no other occupied pieces, the resulting physical area is bounded by

    Dh+Vut ≤ (Aβ²+VB) S².

For multiple fixed aspect or gate choices use the corresponding finite maximum, with uniform upper-approach constants; for each aspect at least one usable gate with nonzero Δ is required. For a single template-width mouth w=ju, j>0, the determinant is jB, so (1) applies however large u becomes. For a positive complementary width w=D−ku, k≥0, it is −kB−Aβ and also cannot vanish. In particular the width min(D,r₁u)−max(0,l u) of a nonempty intersection of horizontal spans always has one of these forms when l,r₁ are fixed integers. This proves the size bound **if that overlap has the indicated solid column and wing access**.

**Two routes and the exceptional width.** If two usable columns for the same marks share β and their width rows (i₁,j₁),(i₂,j₂) are linearly independent, they cannot both have zero determinant in (1); both would be parallel to (B,Aβ). For different β use the actual determinant for each column. One suitable route suffices. If Δ=0, the given width is proportional in template units to m/n+β, so the gate divisor can be absorbed by the mouth itself. An artificial subdivision is not a second usable route: the end of the new column must have an actual approach to the target with the required phase control.

**Source already inside the overlap.** There is a direct alternative for this placement. Let ℓ be the normalized horizontal distance from S to the target-side edge of the column. Until that edge only smooth floor and roof reflections are needed. Using the upper return σ=v+kP, the tall-circle match is (ℓ+B_travel)v ≡ e−y_S−ℓkP modulo 2(H+β), with v∈J; the initial tall phase can be chosen y_S. For rational lengths and ℓ>0 the grid spacing is the rational gcd of 2(H+β) and ℓP, hence at most ℓP. Thus (ℓ+B_travel)η>ℓP suffices. In particular a sufficiently thin column ε<B_travel η/P covers all its interior source positions, since ℓ≤ε, provided the target-side approach is valid. A successful match arrives strictly inside the side portal; there is no test at the internal horizontal seam.

**First case still open.** With an anchored scaled mouth, the first missing geometric assertion is that every residual source and target have a usable transverse approach (or an equally strong second congruence). A source inside a wide column that misses the last test, or an upper wing whose first side hit lies in another vertical component, still needs an argument. With an independent horizontal offset normalization may give only gcd(D,u,w)=1. Then u can contain factors of L, even for κ=1, and the symbolic arithmetic obstruction in l1-projective-crossing.md applies. If the upper chamber changes shape, one needs uniform K and control of the prime factors shared with P; d182 scale ordering supplies neither. The displayed area bound is for the stated intersection, not for all W≤20 charts. No search or census was run.

**What is the smallest W ≤ 20 room this result doesn't cover?** The W=10 word LLLRLLLRLR remains open as an all-length statement, with ledger realization (2,0),(4,0),(4,1),(3,1),(3,4),(0,4),(0,3),(1,3),(1,2),(2,2).
