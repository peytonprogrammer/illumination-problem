Advances: L1 — For a crossing with one affinely stretched upper template, a wholly dark rational product forces a horizontal width proportionality or two vertical depth proportionalities. The lower side-wall period alone gives no equidistribution, even when a/gcd(a,2d) tends to infinity.

# Which ratios are actually locked at a crossing?

In the near-side fixed-template setting of the [scale-step note](l1-crossing-scale-step.md), darkness implies a/gcd(a,2d)≤16PC²/η³. Thus divergence already proves eventual lighting there, conditional on that note's proof (in d190 review). On an affine lattice ray a=a₀+pn, d=d₀+qn, gcd(a,2d) divides 2|p d₀−q a₀| when this determinant is nonzero. If it vanishes, the positive depth ratio is exactly constant. Finite positive limiting ratio, as recorded by d182, does not distinguish these cases.

## A product restriction with the actual gate modulus

Allow the upper template and target to be stretched by horizontal factor u and vertical factor t as in the scale-step note, with the mouths used by the template intact. Its horizontal placement may translate. This argument needs no near-side span bound and permits unrelated extra openings in the lower roof. Fix one normalized upper first-hit interval J, length η>0, vertical travel B>0 and signed-speed period P. The [unit-run shift](l1-crossing-gate-resultants.md) gives this data for the sealed lattice template. A shift of the upper speed by one period changes the lower normalized seam phase by

    AuP/(2Dt) mod 1,          A=a or A=L=a+2d.

Its additive order is 2Dt/gcd(2Dt,AuP). The exact gate in the normalized upper speed has window length u(A+tB)η and grid spacing g_A=gcd(2Dt,AuP). Horizontal translation affects the offset only. Direct ascent succeeds when that length exceeds g_a. Floor-first ascent succeeds when it exceeds 2g_L by the two-index floor-corner argument in the scale-step note. These shots reach the desired roof opening on their first roof encounter.

**Proposition.** Work on a rational product U × V in the full marked-gap chart. Assume the stretched-template description holds on its positive part, with D,u positive rational linear forms on U and a,d,t positive rational linear forms on V. It suffices to work on a finite-index lattice on which all relevant lengths and stretch factors are integral. If every placement there is dark, then

    D is proportional to u on U,  or
    both a and d are proportional to t on V.

This is a restriction on an entire dark product; it need not hold on an arbitrary sequence of placements for which a route fails. The argument needs unrestricted integral multiples on the geometric product before enforcing room gcd one.

**Proof.** Suppose D and u are independent on U. If the second conclusion fails, choose A from {a,L} such that A and t are independent on V. Choose two positive integral vectors x₀,x₁ in U for which D(x₀)u(x₁)≠D(x₁)u(x₀); similarly choose y₀,y₁ in V distinguishing A/t. Positivity is relatively open, and on a rational space the choices can be made by rational approximation and clearing denominators. Write D(s),u(s) for the forms at x₀+s x₁ and A(n),t(n) for their values at y₀+n y₁. Each is affine with positive intercept and slope.

Take s=kn. Consider integer polynomials

    f(n)=2D(kn)t(n),       g(n)=P u(kn)A(n).

D(kn) and u(kn) have distinct roots for every k>0, as do t(n) and A(n). Either cross equality of roots, D(kn) with A(n) or u(kn) with t(n), rules out at most one k: the horizontal root is a fixed nonzero number divided by k and the vertical root is fixed and nonzero. Thus one of k=1,2,3 gives coprime polynomials over ℚ. Their polynomial Bézout identity, with denominators cleared, gives a nonzero integer R divisible by gcd(f(n),g(n)) for every integral n. Equivalently |Res(f,g)| suffices. Hence g_A≤|R| on this diagonal, while u(kn)(A(n)+t(n)B)η tends to infinity. The relevant gate clears, including the floor-corner check when needed. This gives a lit placement on the asserted dark product. If both a and L are proportional to t, so is d=(L−a)/2. This proves the proposition.

In particular, when D/u can vary on the product and the upper-template hypothesis holds, a/gcd(a,2d) cannot diverge along a wholly dark product: a and 2d then have fixed rational ratio. The resultant depends on the forms at the chosen product vectors; the argument does not bound the primitive coefficients of a surviving proportionality in terms of the chart. No growth ray or trajectory needs to be enumerated for this proof.

## An exact obstruction to lower-period averaging

Consider the structural junction of two rectangles of equal width D with full overlap of width one. In coordinates their horizontal spans are [0,D] and [1−D,1], with roof seam at h=a+d. The upper height is two. Put the source at (D/2,d) and target at (0,h+1). Take a=2n+1, d=n for even n≥2, and any multiple of four D with D/2>3(a+2d)+1. For an affine growth ray take D=16(a+1). This is a strictly simple eight-wall lattice junction. Its horizontal wall gcd is one by the edges D and D−1, its vertical wall gcd is gcd(3n+1,2)=1, and its interior marks have the same parity. The depth quotient is 2n+1. Neither a room search nor a lighting certificate is used here.

For the direct terminal upper leg of vertical travel one, fixing the open seam coordinate and signed sheet allows speed shifts by 2D. In units of the lower circumference the direct and floor shifts are the integers a and a+2d. Both phase orbits have **order one** at every n. On a fixed speed interval the lower frequency A/(2D) also stays bounded along the affine ray. Thus neither winding through these aliases nor growth in n produces the proposed equidistribution.

There is a stronger geometric obstruction. For any single seam crossing with integral lower and upper absolute vertical travels A and b, b is odd: the target lies midway between the two upper horizontal sides. Allow all horizontal windings and both endpoint sheets. The unfolded source abscissa is ±D/2 modulo 2D and the upper target abscissa is 0 or 2 modulo 2D. If z∈(0,1) is the crossing abscissa, eliminating the shared speed gives the necessary condition

    (A+b)z ≡ ±bD/2 + A e    (mod 2D),       e∈{0,2}.

Because b is odd, the first term has distance D/2 from 2Dℤ. Therefore 3A+b≤D/2 makes the congruence impossible: its right side has distance at least D/2−2A, whereas 0<(A+b)z<A+b. In particular both short lower routes with b=1 fail, regardless of their lateral windings. This is a failure of the proposed detector. Every room in this class is lit by the reviewed [two-rectangle theorem](doorway-word-bound.md). Here the physical door stays one unit wide while the upper width grows; the fixed scaled-mouth template hypothesis does not hold.

## The doubly proper case

On a rank-one horizontal factor and a rank-one vertical factor, the first proportionality in the proposition is automatic for homogeneous positive forms. The obstruction to extracting a bounded normal factor by factor is visible in the exact phase (A/t)(u/D)P/2. Both ratios are unchanged by independent axis dilations. An exact resonance can involve arbitrarily high primitive coefficients on *both* factors. Algebraically, take (D,u)=(m,m+1) and (A,t)=(m,m+1); then Au=Dt identically on the product of these two rays, while each ray has primitive normal of height m+1. This last example tests the phase identity, not existence of a physical dark product. In a chart with fixed offsets, use the affine-polynomial argument above; fixed offsets cannot be discarded by calling the directions homogeneous.

**First open case.** A product with locked D/u and changing aperture-to-width ratio, or with both axes rank one and unbounded unknown ratio coefficients, escapes this bound. A proof must use a trajectory class sensing those coefficients separately, or show geometrically that such a product cannot be dark. No chart-wide H(C), G(C), or census ceiling follows. The product-flat application remains conditional on d132/d134.

**What is the smallest W ≤ 20 room this result doesn't cover?** There is no whole-word closure. The W=10 ledger word LLLRLLLRLR remains open as an all-length statement, with realization (2,0),(4,0),(4,1),(3,1),(3,4),(0,4),(0,3),(1,3),(1,2),(2,2).
