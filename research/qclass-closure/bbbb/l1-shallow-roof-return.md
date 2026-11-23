Advances: L1 — For the d190 scaled upper template and near-side mouth span, all cross placements with sufficiently large h/t are lit, uniformly in the source depth ratio. A roof–floor return covers the previously escaping shallow-source regime.

# A source close to the roof

Use exactly the crossing geometry and admissible lattice placements of [d190](l1-crossing-scale-step.md). In template units put H=h/t, A=a/t, X=D/u, c₀=c/u, so 0<A<H and 0<c₀<X. The lower box is [0,X] × [0,H] and S is A below its roof. Its roof openings lie in [0,R]. In the unchanged upper template a positive-sheet backward approach from T gives the seam position z=e−Bv in (0,R) for v in an open interval J of length η; the same z works at speed v+kP for every integer k. As in d190 the template has only its labelled openings, B≥1, and P is an integer common period. The physical unit and mark hypotheses guarantee the integer gcds used below. Constants are those of this particular template and span.

**Why the one-slab suggestion helps.** At fixed a,D and fixed upper dimensions the floor-first travel is 2h−a. Its physical gate spacing is at most 2Dt, so the two-index floor test eventually lights every member, without first finding a lit seed for d182. This bound alone depends on D. The next argument also handles widths growing along with the floor gap.

## A bounded winding period on failure

Assume H≥1. Write C=2+2R+P+η and Q=ceil(64C²/η²). Suppose the floor-first and downward far-wall routes of d190 both fail. Let

    g=gcd(2Dt,(2h−a)uP),         q=2Dt/g.

The floor test gives u(2h−a+tB)η≤2g. The far-wall window gives X≤4HC²(1+1/(2H−A))²/η≤16HC²/η. It follows that

    X ≥ (2H−A+B)η/4 ≥ Hη/4,      q ≤ 4X/[(2H−A+B)η] ≤ Q.
    (2H−A)qP ∈ 2Xℤ.                                             (1)

The period identity in (1) holds at every placement by the definition of q. Failure of both routes supplies the displayed bounds, in particular q≤Q, for using that period on a different route.

## The roof–floor route

Launch upwards. Specify a reflection on solid roof, one on the floor, and a final upward arrival in the open mouth. Side-wall windings are unrestricted. The vertical travels to the two roof visits are A and L=2H+A. Use upper speeds v+qjP for integer j. On the positive seam sheet, (1) reduces the exact terminal equation to

    c₀+(L+B)v+2AqPj ≡ e modulo 2X.                              (2)

The first roof abscissa before folding is r=c₀+A(v+qjP). If r is farther than R from Xℤ, it folds to a solid roof point away from both upper corners. There is then no intervening floor corner: the unfolded floor abscissa is the average of r and the final roof abscissa z+2Xl. A floor corner would imply r≡−z modulo 2X, impossible because z∈(0,R). These are all horizontal-level contacts before the final gate.

Take v₀ in the middle half of J and first solve (2) over the reals with its multiple of 2X chosen zero. The real choice j*=[e−c₀−(L+B)v₀]/(2AqP) would put the first roof at

    r*=[e+c₀−(2H−A+B)v₀]/2.

As v₀ varies over the middle half, r* spans an interval of length (2H−A+B)η/4≥Hη/4. Since X≥Hη/4, this interval contains a point at distance at least Hη/16 from Xℤ. Indeed an interval lying entirely closer to the grid would fit in one component of length Hη/8. Choose v₀ there. Round j* to a nearest integer j and set

    v=v₀−2AqP(j−j*)/(L+B).

This satisfies (2). The speed correction is at most AqP/(L+B). The first roof moves by at most AqP/2, since its change equals AqP(j−j*)[1−2A/(L+B)] and 0<2A<L+B.

In particular define

    ε=min(1/2, η/(32QP)),       H₁=max(1,64(R+1)/η).

If A/H≤ε and H>H₁, the speed correction is below η/4 and the first roof still clears Xℤ by more than R. The final seam is therefore strictly open and the path reaches T. Either a d190 route worked or the constructed route does. The proof is uniform in c₀ and X. It handles fixed a with d→∞ for a fixed upper chamber, and more generally any d190 sequence with a/h→0 and h/t→∞. Negative winding indices are allowed by the signed-period construction.

## All source depths, and the comparable-scale follow-on

Let K₀=16PC²/η³. By d190 a dark pair must have p=a/gcd(a,2d)≤K₀. For H>H₁, the argument above also forces a/h>ε. Hence the coprime positive integers p and b=2d/gcd(a,2d) obey

    p≤K₀,             b≤2K₀/ε,             θ=d/h=b/(2p+b).

This bounds the very denominator at which d191's corner threshold had diverged. Let H₂(θ) denote 1 plus the maximum of 1 and the right-hand threshold for Y=h/t obtained by dividing the explicit maximum in d191 equation (1) by κ₋. A valid all-depth tail starts above

    H*=max( H₁, max H₂(b/(2p+b)) over 1≤p≤ceil(K₀), 1≤b≤ceil(2K₀/ε) ).

The finite maximum is a formula in template data; it requires no room or trajectory enumeration. Use reduced θ in computing H₂. For H>H* the preceding roof–floor argument covers the shallow placements and the reviewed fixed-ratio theorem covers each remaining candidate. This removes the fixed-ratio hypothesis from the large relative height statement. [D191 theorem and threshold](l1-fixed-ratio-corner.md)

**Fixed-stretch finiteness corollary (d192).** For fixed template, u,t and the stated lattice placements, a dark placement has h≤tH* and D≤uκ_max H*, using the uniform dark-aspect bound 4C²(1+P/(Bη))²/η. There are finitely many possible lower boxes and source marks. In particular a=t=1 requires only the shallow estimate: darkness forces d+1≤max(H₁,1/ε). At the st279 review constants the reduced-depth list reaches denominators near 10³⁷. Finiteness does not make this a practical census.

**What is left on the comparable product.** Failure of the direct route also forces u(a+tB)η≤auP, hence A≥Bη/P. Consequently for any surviving dark placement, H≤H* and a/h≥Bη/(PH*)>0. D190 again bounds the list of reduced depth ratios, now even inside the residual box. D191 gives a finite list of coupled aspects κ=X/H for those ratios; its upper bound remains valid at H<1 using t/a≤P/(Bη). Neither result bounds the individual reduced denominators of X and H when both lie in bounded positive intervals. The first open case is this comparable-scale product with a freely placed source and possibly high-denominator axis ratios. Changing the upper template internally, shrinking its labelled aperture relative to the template, or putting other mouths outside the prescribed span is outside the all-depth theorem. No absolute area cutoff for L1 follows.

**What is the smallest W ≤ 20 room this result doesn't cover?** No all-length ledger status changes. The W=10 word LLLRLLLRLR remains open as a whole word, with realization (2,0),(4,0),(4,1),(3,1),(3,4),(0,4),(0,3),(1,3),(1,2),(2,2). No discovery search was run.
