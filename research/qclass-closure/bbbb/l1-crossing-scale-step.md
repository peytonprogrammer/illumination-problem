Advances: L1 — For the specified lattice marks and a stretched upper template, a dark placement forces an explicit bound on a/gcd(a,2d), including growing floor depth d. If mouth width divided by target-to-mouth depth tends to zero, no uniform first-hit interval in physical slope exists, even at strictly separated scales.

# A scale step at an occupied crossing

**Setting.** The lower box is [0,D] × [0,h]; S=(c,d), h=a+d, with integral D,h,c and positive integral depths. Fix a connected sealed upper lattice chamber with a marked interior lattice target and open mouths in its bottom boundary. Label the mouths actually shared with the lower box. The upper template has no openings other than those labelled mouths. Relative to the lower near side, use template coordinates x and vertical distance from the roof. Map the upper chamber, target and labelled mouths by (x,y)↦(u x,t y), with positive integral u,t. Assume the indicated gluing remains strictly simple, the shared mouths are not clipped, and every opening of the lower roof lies in [0,uR] for a fixed R≥1 with uR≤D (one may use the actual mouth span). It suffices that one upper component be the scaled template; other attached components can use any openings satisfying the same span condition. The lower sides and floor are solid. This is a structural hypothesis on a marked growth chart, not on its wall-turn word alone.

**Theorem.** Write n for the lattice area of the sealed template, m=4n, T=1+F_(3m−1) with F₀=0,F₁=1, and let W be its integral bounding width. Valid constants are

    η=1/(4T²),      P=2 lcm(1,…,W),      C=2+2R+P+η.
    a/gcd(a,2d) > 16PC²/η³  implies illumination.

Here P may instead be any common multiple of the doubled widths actually visited by the selected upper path. For st279 the visited-run period is 6; including all upper runs by their actual widths gives 30. The earlier d189 result had one free lower gap per axis and fixed d. This statement lets d vary as well, solely for the specified placements. The ratio bound is uniform in D,c,u,t, including comparable or arbitrarily separated growth. No supplied first-hit itinerary or slope window is required. The statement is for the placements specified above; arbitrary drifting marks or relative gap ratios in the template are separate questions.

### Produce the window once

Transpose d124's sealed-chamber Fibonacci portal argument so the counted steps are units of vertical travel. A backwards launch at |dx/dy|=(3−√5)/2 hits a chosen mouth by step T on the sealed surface. Stop earlier if it first hits a different shared mouth. A closed slope interval of width 1/(2T²) keeps the entire prefix, the first open unit edge and the reflection signs; take an interior subinterval J of length η. With velocity v measured forward at the seam in template units, the abscissa there is z₀=e−Bv with B the integral vertical travel, 1≤B≤T. The sign of J can be reversed to match that convention. Tracing backwards in the unit-height bands, v→v+kP preserves every unit-level contact and folding sign, since P is divisible by twice every band width. Thus in physical units the seam position is z=u(e−Bv) and the compatible forward speeds are u(v+kP)/t. This is where using the normalized slope matters. [Reviewed first-hit and stability bound](effective-chamber.md) · [Unit-band shift](l1-crossing-gate-resultants.md)

### Join through the direct or floor route

Set A=a or a+2d, respectively. On one admissible lower sheet the contact solves c+Au(v+kP)/t≡u(e−Bv) modulo 2D. Eliminating k gives exactly

    u(A+tB)v ∈ t(ue−c) + g_A ℤ,     g_A=gcd(2Dt,AuP),    v∈J.

Only the displayed positive seam sheets are used. For the floor-first route put A=a+2d. For arbitrary integers l,k let the physical horizontal speed be

    v_phys=(ue−c + 2Dl + uBkP)/(A+tB),
    v=(t/u)v_phys−kP.

The gate test is v∈J; its arithmetic index is (2Dt l−AuP k)/g_A, up to the fixed offset already displayed. The map (l,k)↦index is onto ℤ. A floor corner requires c+d v_phys=0 modulo D. This is an affine condition on the integer pair (l,k) with values in ℝ/Dℤ. Its solutions are empty or a coset of a subgroup. The subgroup is proper: incrementing l by one changes the floor coordinate by 2Dd/(A+tB), strictly between 0 and D.

If the gate interval contains two consecutive indices, at least one has a corner-free lift. Otherwise the bad coset contains both entire index fibers. Taking differences, its subgroup contains the kernel and a vector of index one, hence all of ℤ², a contradiction. This eliminates the earlier count of 2d bad seam positions and works at every d. No such exclusion is needed on direct ascent. Neither short route previously meets the roof, even if additional mouths are present elsewhere.

Write γ=gcd(a,2d) and L=a+2d. On joint failure the direct-window length u(a+tB)η is at most g_a and the floor-window length u(L+tB)η is at most 2g_L. The gcd of these moduli divides uPγ, and their lcm divides 2Dt. Multiplication gives

    D ≥ u(a+tB)(L+tB)η²/(4γPt).                         (1)

### Join by one reversal at the far wall, launching downwards

Shift the template interval by a multiple kP so its speeds v' are negative, with inf |v'| greater than Q=max(1,1+R/B,2Rt/L) and at most Q+P. Then sup |v'|≤C(1+t/L). Since 0≤z/u≤R, the shifted intercept e'=e+BkP=z/u+Bv' is negative. Set s=−t/(uv')>0. Its interval width satisfies

    δ ≥ tη/[u C²(1+t/L)²],          s uR < L.

Launch S rightward and downwards. Unfold the floor, so the virtual upward start is at height −d. Its next roof is at +h, at unfolded vertical distance L. The backwards upper leg enters the box heading toward the far wall, at z=ue'+tB/s. After reversal at x=D the exact upward roof arrival equation is

    −d+s(2D−c−ue')−tB=(2j+1)h.

Outward, the vertical travel under the opening span is <L, so a floor reflection is allowed and no roof contact there is possible. On return the roof spacing is 2h/s>uR because 2h>L. Until the open seam hit, x can encounter a vertical side only at D. The change in unfolded far-wall height between adjacent roots is 2h(D−c)/(2D−c−ue'), strictly between 0 and h. Two consecutive roots therefore suffice to avoid every far-wall corner, floor corners included. The sharp interval-length test used here is (2D−c−ue')δ>4h; the simpler Dδ>4h suffices. Failure and (1) imply

    (a+tB)(L+tB)η³ ≤ 16hγPC²(1+t/L)².

Since B≥1 and a≤L, the product on the left divided by (1+t/L)² is at least aL before its η³ factor. Finally L≥h, proving the stated ratio bound.

**Growing-depth consequences.** This covers all sequences with d=o(a) and a→∞ for a fixed upper template, since γ≤2d. At comparable depths it also covers sequences whose reduced numerator a/γ tends to infinity. More structurally, on a rational linear family on which the upper-template and gluing hypotheses hold and every positive integral placement is dark, a and 2d cannot vary independently. In a small relatively open cone about any positive rational point the ratio 2d/a is bounded above by some M. The bound just proved puts the reduced pair (a/γ,2d/γ) in a finite box of sides K and MK, where K=16PC²/η³. Rational density after clearing denominators puts the cone in finitely many lines in the (a,2d)-plane. One such proportionality must hold on the family. This argument uses darkness under scaling on the underlying geometric family, before a per-axis primitive-gcd restriction. It gives no chart-uniform bound on the second coefficient when M is unbounded.

### Why the requested physical-window induction fails

This counterexample to physical-window uniformity concerns w/b→0. An isotropic u=t stretch of a fixed labelled template keeps physical window η; the observable obstruction below does not refute the scaled-template theorem. For *every* fixed first-hit branch that must cross an open horizontal mouth of width w, its seam abscissa is e−Bv_phys on that branch, with absolute derivative B the total vertical travel. If the target is b above the seam, B≥b on every itinerary, even with cap reversals. Thus η_phys≤w/b. A union of a bounded number of such intervals has total length at most that multiple of w/b. This gives an obstruction to a uniform beam for this parameterization, independent of reflection count.

This occurs already at a single junction of two rectangles with fixed overlap of width one. For clarity one can use lower span [0,D], upper span [−2,1], lower height a+1 and upper height b+1. Take marks at (1,1) and (−1,a+1+b). For even b≥2, D=a=(b+1)²+1 gives b=o(a), or D=a=b+2 gives comparable scales. Both are lattice realizations of the same structural junction: the mouth is the overlap [0,1], of width one, the wall gcd on x is one since the edge displacements include D and D−1, and gcd(a+1,b+1)=1 in both choices. The marks are distinct, interior and same-parity. The W=8 boundary has two reflex corners. As a varying family this junction lies outside the fixed marked-template stretch hypotheses: its target depth is b and its top clearance is one. These identities illustrate the obstruction to the proposed induction, not a lighting certificate or a dark room. In either case the bound 1/b survives passage to every subsequence. For two or more independently drifting upper heights, having a finite positive limiting ratio is weaker than being one exact stretch: heights j and j+1 remain coprime, and no diverging common integral stretch can be factored out. D184's fixed-period disjoint transfer does not remove that difference at an occupied crossing.

### Extra roof openings and the first residual

Even if an extra opening lies outside [0,uR], (1) remains necessary for all depths. In particular if D=O(a), t=o(a), d fixed and the template fixed, both routes cannot fail as a→∞; the location of any additional roof openings is immaterial. This resolves the far-mouth question in that scale regime.

In the wider residual, deleting an opening to apply the far-wall proof turns that segment into a mirror. For any chosen far-wall root, before the intended seam hit the earlier roof contacts are given exactly by

    ℓ_j=((2j+1)h+d)/s,    0<ℓ_j<2D−c−z,
    x_j=D−|D−(c+ℓ_j)|.

An earlier x_j in an extra opening exits the box; a contact at a physical lip must also be excluded. Merely cutting there does not transfer the reflected path back. Even an appendage which is a rectangular arm with its whole end open illustrates the issue: at horizontal speed v with unit vertical speed, an excursion to a cap H away adds 2Hv to the unfolded horizontal phase modulo twice the arm width. Preserving the original entry coordinate and horizontal sign requires that shift to vanish modulo the doubled width. The single-root seam equation does not impose it. This isolates the additional gate obligation outside the span, without asserting that all roots fail.

**First open cases for L1 (after d192).** For the fixed template the [all-depth tail](l1-shallow-roof-return.md) bounds h/t at every source depth, including a fixed and d tending to infinity. Fixed u,t leave finitely many dark lattice placements. The open comparable-scale case has unbounded stretch, potentially high individual ratio denominators and a free source; d188’s doubly proper product remains open in general. An upper chamber changing internal shape, a mouth shrinking relative to its template, and an extra roof opening outside the near-side span beyond the resolved direct/floor regime require separate control. No all-chart census ceiling follows.

**What is the smallest W ≤ 20 room this result doesn't cover?** It gives no whole-word change. The W=10 all-length word LLLRLLLRLR remains open, with ledger realization (2,0),(4,0),(4,1),(3,1),(3,4),(0,4),(0,3),(1,3),(1,2),(2,2).
