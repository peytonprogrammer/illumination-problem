Advances: L1 — A lower box with a source at fixed floor depth lights an independently stretched upper lattice chamber once the source-to-roof depth exceeds an explicit threshold independent of either upper stretch and of the lower width. A uniform first-hit interval in physical slope is impossible even at strictly separated scales.

# A scale step at an occupied crossing

**Setting.** The lower box is [0,D] × [0,h]; S=(c,d), h=a+d, with 0<c<D and positive lattice depths. Fix a connected sealed upper lattice chamber with a marked interior lattice target and open mouths in its bottom boundary. Label the mouths actually shared with the lower box. Relative to the lower near side, use template coordinates x and vertical distance from the roof. Map the upper chamber, target and labelled mouths by (x,y)↦(u x,t y), with positive integral u,t. Assume the indicated gluing remains strictly simple, the shared mouths are not clipped, and every opening of the lower roof lies in [0,uR] for a fixed R≥1. It suffices that one upper component be the scaled template; other attached components can use any openings satisfying the same span condition. The lower sides and floor are solid. This is a structural hypothesis on a marked growth chart, not on its wall-turn word alone.

**Theorem.** Write n for the lattice area of the sealed template, m=4n, T=1+F_(3m−1) with F₀=0,F₁=1, and let W be its integral bounding width. Valid constants are

    η=1/(4T²),      P=2 lcm(1,…,W),      C=2+2R+P+η.
    a > max{d, 2dP(2d+1)/η, 32dPC²/η³}  implies illumination.

The threshold is uniform in D,c,u,t, including comparable or arbitrarily separated growth. No supplied first-hit itinerary or slope window is required. The statement is for the placements specified above; arbitrary drifting marks or relative gap ratios in the template are separate questions.

### Produce the window once

Transpose d124's sealed-chamber Fibonacci portal argument so the counted steps are units of vertical travel. A backwards launch at |dx/dy|=(3−√5)/2 hits a chosen mouth by step T on the sealed surface. Stop earlier if it first hits a different shared mouth. A closed slope interval of width 1/(2T²) keeps the entire prefix, the first open unit edge and the reflection signs; take an interior subinterval J of length η. With velocity v measured forward at the seam in template units, the abscissa there is z₀=e−Bv with B the integral vertical travel, 1≤B≤T. The sign of J can be reversed to match that convention. Tracing backwards in the unit-height bands, v→v+kP preserves every unit-level contact and folding sign, since P is divisible by twice every band width. Thus in physical units the seam position is z=u(e−Bv) and the compatible forward speeds are u(v+kP)/t. This is where using the normalized slope matters. [Reviewed first-hit and stability bound](effective-chamber.md) · [Unit-band shift](l1-crossing-gate-resultants.md)

### Join through the direct or floor route

Set A=a or a+2d, respectively. On one admissible lower sheet the contact solves c+Au(v+kP)/t≡u(e−Bv) modulo 2D. Eliminating k gives exactly

    u(A+tB)v ∈ t(ue−c) + g_A ℤ,     g_A=gcd(2Dt,AuP),    v∈J.

For floor-first travel the additional excluded event is a floor-corner hit. At fixed v, change k by 2Dt/g_A. The floor coordinate changes by 2DduP/g_A. If g_A>2duP, two consecutive choices cannot both hit a corner. Otherwise a bad physical speed is (jD−c)/d, so the seam coordinate modulo 2D is determined by j modulo 2d. At most 2d distinct seam positions are bad, and z is injective in J. Once aη>2dP(2d+1), the small-g case gives enough strict gate solutions to avoid them. Neither lower route previously hits the roof. This part holds with additional roof openings at arbitrary locations.

Consequently failure of both gives u(A+tB)η≤g_A for each A. Their gcd divides 2duP, and their lcm divides 2Dt. Therefore

    D ≥ u(a+tB)²η²/(4dPt).                              (1)

### Join by one reversal at the far wall

Shift the template interval by an integer multiple kP so its speeds v' are negative, with min |v'| greater than Q=max(1,1+R/B,2Rt/a) and at most Q+P. Then max |v'|≤C(1+t/a). Since 0≤z/u≤R, the shifted intercept e'=e+BkP=z/u+Bv' is negative. Set s=−t/(uv')>0. Its interval width satisfies

    δ ≥ tη/[u C²(1+t/a)²],          s uR < a.

The backwards upper leg now enters the box heading toward its far wall, at z=ue'+tB/s. Launch S rightward and up. After the reversal at x=D the exact seam equation is

    d+s(2D−c−ue')−tB=(2j+1)h.

Outward, the rise under the opening span is <a, since a rightward launch from c>0 travels at most uR before leaving that span. On return the horizontal spacing 2h/s of successive roof contacts exceeds uR, so only the last can fall in the span. Two consecutive roots of the seam equation cannot both hit a far-wall corner: the change of unfolded cap height is 2h(D−c)/(2D−c−ue'), strictly between 0 and h. Thus failure requires Dδ≤4h. Combine this with (1), cancel u/t and use a+tB≥a+t to get

    a²η³ ≤ 16dPC²(a+d).

For a≥d this is precisely the last stated bound on failure. No separation of scales or approximation by a weighted growth ray entered the proof. The freedom to shift the upper interval by an amount depending on t/a is essential to this uniform estimate.

### Why the requested physical-window induction fails

For *every* fixed first-hit branch that must cross an open horizontal mouth of width w, its seam abscissa is e−Bv_phys on that branch, with absolute derivative B the total vertical travel. If the target is b above the seam, B≥b on every itinerary, even with cap reversals. Thus η_phys≤w/b. A union of a bounded number of such intervals has total length at most that multiple of w/b. This gives an obstruction to a uniform beam for this parameterization, independent of reflection count.

This occurs already at a single junction of two rectangles with fixed overlap of width one. For clarity one can use lower span [0,D], upper span [−2,1], lower height a+1 and upper height b+1. Take marks at (1,1) and (−1,a+1+b). For even b≥2, D=a=(b+1)²+1 gives b=o(a), or D=a=b+2 gives comparable scales. Both are lattice realizations of the same structural junction: the horizontal overlap endpoints are offset by one, the wall gcd on x is one since the edge displacements include D and D−1, and gcd(a+1,b+1)=1 in both choices. The marks are distinct, interior and same-parity. The W=8 boundary has two reflex corners. These identities illustrate the obstruction to the proposed induction, not a lighting certificate or a dark room. In either case the bound 1/b survives passage to every subsequence. For two or more independently drifting upper heights, having a finite positive limiting ratio is weaker than being one exact stretch: heights j and j+1 remain coprime, and no diverging common integral stretch can be factored out. D184's fixed-period disjoint transfer does not remove that difference at an occupied crossing.

### Extra roof openings and the first residual

Even if an extra opening lies outside [0,uR], (1) remains necessary once the small-g threshold is passed. In particular if D=O(a), t=o(a), d fixed and the template fixed, both routes cannot fail as a→∞; the location of any additional roof openings is immaterial. This resolves the far-mouth question in that scale regime.

In the wider residual, deleting an opening to apply the far-wall proof turns that segment into a mirror. For any chosen far-wall root, before the intended seam hit the earlier roof contacts are given exactly by

    ℓ_j=((2j+1)h−d)/s,    0<ℓ_j<2D−c−z,
    x_j=D−|D−(c+ℓ_j)|.

An earlier x_j in an extra opening exits the box; a contact at a physical lip must also be excluded. Merely cutting there does not transfer the reflected path back. Even an appendage which is a rectangular arm with its whole end open illustrates the issue: at horizontal speed v with unit vertical speed, an excursion to a cap H away adds 2Hv to the unfolded horizontal phase modulo twice the arm width. Preserving the original entry coordinate and horizontal sign requires that shift to vanish modulo the doubled width. The single-root seam equation does not impose it. This isolates the additional gate obligation outside the span, without asserting that all roots fail.

**First open case for L1.** The upper approach must use two growing depths with an uncontrolled relative shape (or a mouth that shrinks relative to the upper template), and (1) no longer discharges the route using available constants. Applying the area-only bound to the moving template gives pointwise constants, not a uniform K(C). Strict growth-class order supplies no lower bound on the physical J, and comparable growth supplies no common scale for arbitrary integral depths. No census ceiling follows.

**What is the smallest W ≤ 20 room this result doesn't cover?** It gives no whole-word change. The W=10 all-length word LLLRLLLRLR remains open, with ledger realization (2,0),(4,0),(4,1),(3,1),(3,4),(0,4),(0,3),(1,3),(1,2),(2,2).
