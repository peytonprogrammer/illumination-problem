# M2: a missing mirror that no choice of tooth images can repair

For a hall with attachments on a single bank, the original no-tooth-bounce family already fails on the eight-wall U. With equal mouth widths u, equal mark depths d on the tooth centerlines, hall height c and gap g, its exact threshold is gd<cu. Tooth-side reflections repair these placements at all lengths. This fails to give a length-free theorem for arbitrary stacked rooms and arbitrary marks. [Sharp threshold and positive results](tooth-side-unfolding.md)

## A solid floor can fail even with arbitrary tooth reflections

Work symbolically in the existing single-tier, one-bank comb model. Use the common tooth width as the unit. Let the hall width A be a positive multiple of 4 in these units and its height be c. Choose two interior teeth with left lips l₁,l₂ satisfying

    0<l₁,     l₁+1<l₂,     L=l₁+l₂<2.

Put each mark at depth c/2 above its mouth and horizontal offset ε from its left side, with 0<ε<min(1/18,(2−L)/6). The teeth extend above the marks. These inequalities have nonempty interior in the placement variables (equivalently 0<l₁<1/2 and 1+l₁<l₂<2−l₁). Rational choices scale to lattice walls and lattice marks, including same-parity marks after a further dilation. No assertion of primitive normalization is needed. **No shot can descend to the solid hall floor and return to the other mark with that as its only horizontal-wall reflection.** This excludes all tooth and hall side-wall contacts in arbitrary number as possible repairs within that family. Direct horizontal travel is blocked by the gap above the hall. The same exclusion applies if another bank opens portions of the floor and the proposed turn must remain at the original floor height.

Here is the full sheet calculation. Fix the first mouth in its physical hall chart. In the reflected hall the second mouth has orientation σ=±1 and is translated by 2kA. The two endpoint images necessarily have the form

    X=l₁+2n+η,    Z=σl₂+2kA+2m+ζ,    η,ζ ∈ {−ε,+ε}.

This allows every hall winding and both tooth-image signs, even if some listed images do not give a legal itinerary. The total vertical travel is 3c, so the first and second mouth times are 1/6 and 5/6. Write their developed abscissas as l₁+e₁ and σ(l₂+e₂)+2kA; even allowing 0≤e₁,e₂≤1 will give a contradiction. Linear interpolation, with h=n+m, gives

    e₁+σe₂ = 2h+η+ζ,
    e₁ = (σl₂−l₁)/6 + h/3 + (4/3)(n+kA/4) + (5η+ζ)/6.

The last error has absolute value at most ε. Since A/4 is an integer, the winding term stays on the same 4/3-spaced grid.

* For σ=+1 the sum forces h=0 or 1. If h=0 then 0≤e₁≤2ε, but its unperturbed grid (l₂−l₁)/6+(4/3)ℤ is more than 1/6 from zero since 1<l₂−l₁<2. If h=1 then 1−2ε≤e₁≤1, but the grid (l₂−l₁+2)/6+(4/3)ℤ has distance at least 1/3 from one. Both contradict 3ε<1/6.
* For σ=−1 the difference forces h=0. The two grid points bracketing [0,1] are −L/6 and (8−L)/6. Both miss it by at least (2−L)/6 because 1<L<2. Even the perturbation ε does not reach the closed mouth.

No extra choice of side-wall images survives. In a one-bank hall a path between these marks must descend into the hall and rise again. If it uses just one horizontal reflection, that reflection can only be on the floor: a roof contact approached downward from inside a tooth passes through its open mouth or hits a lip. A legal repair therefore needs at least two horizontal-wall reflections. This is an obstruction to a path family, not proof of a dark pair. This calculation uses no room or direction enumeration.

## A two-bank obstruction including all side reflections

Consider a horizontal rectangular hall with teeth at top and bottom in an integral orthogonal room. Let S and T be interior lattice points of equal height below the hall and with congruent x-coordinates mod 2. Consider all rays which rise until a single horizontal-wall reflection on the far bank of the hall and then descend to T. Permit either initial horizontal sign and arbitrarily many reflections on actual vertical walls in any chamber, tooth or the hall.

**Necessary condition.** Some solid horizontal interval on that far bank contains a physically legal lattice site for the reflection. To prove it, unfold all vertical reflections. Their action on abscissas is x ↦ ±x+2j, j integral. The rise and fall to equal endpoint heights take the same amount of time. Thus at the far-bank contact the developed abscissa is the average of two integers of the same parity. Folding back across the vertical walls leaves it integral. A physical vertex stops the path, an open mouth carries no horizontal mirror, and a smooth vertical wall cannot reverse the vertical velocity. This proof does not prescribe the horizontal winding or the sheets of either endpoint.

**Named control and explicit repair.** Use the DB55 stretch with corridor length 1: [0,5]×[0,5] and [6,11]×[0,5] joined by [5,6]×[2,3]. View [0,11]×[2,3] as the hall. On its far bank y=3, the only available horizontal mirror is 5<x<6. Neither lip is legal. Hence the entire above shot family fails for S=(3,1), T=(7,1). This is a normalized, 12-wall BBBB room (r=4, area 51, and both axis wall-length gcds are one). [Type thresholds](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d69-bbbb/README.md)

There is nevertheless a legal path with a single horizontal reflection. It must continue into an upper tooth: the room change requires passage through 2<y<3, and the only possible higher horizontal mirror after excluding y=3 is y=5. Use that cap. The unfolded vertical travel is 8. Pass rightward through the joining corridor, then reflect in x=11 and x=6 in that order inside the right chamber; the corresponding developed target abscissa is 17. Thus the launch is (7,4), with dx/dy=7/4. The two corridor mouths are crossed at (5,15/7) and (6,19/7). The three physical reflections, in order, are

    (10,5), (11,31/7), (6,11/7).

The final reflection lies below the corridor and reaches T=(7,1). Direct substitution in the unfolded line x=3+7t/4, y=1+t for t≤4 and y=9−t for t≥4 verifies all contacts after folding. In particular the pair needs a tooth-cap reflection if exactly one horizontal-wall reflection is allowed. A path with more vertical reversals is outside the obstruction. No room or ray search was used.

**Milestone scope.** This gives the explicit-obstruction alternative for the proposed floor-bounce construction, even after allowing every tooth-side and hall-side reflection. It provides no counterexample to full illumination, and no new all-length ledger coverage. A complete theorem for this class must allow the turn to pass through a missing mirror or change the number of vertical reversals. The one- and two-bank positive sufficient conditions remain in [parallel-mouth-combs.md](parallel-mouth-combs.md).

## D164 attacker evidence

In the archived A2 and A4 runs, exceeding the factor-eight sufficient bound by 2× and 4× still left all 1,041 and 501 tested pairs covered by the tested family. In A8, seven of 1,038 pairs missed the entire tested family and all seven had other witnesses. Its overhanging B member missed 2,708 tested pairs; all 2,708 were lit by other paths. These are finite tests. Failure of the explicit shot formulas does not prove that every one-floor path fails; the all-image exclusions above use separate arguments. [D164 attack log](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d164-attack-combs/attack.log)

## What is the smallest W ≤ 20 room this result doesn't cover?

For whole-room coverage, taking the project's all-real eight-wall theorem as baseline, the first possible wall count is 10. D163's smallest OPEN example LLLRLLLRLR has coordinates (2,0), (4,0), (4,1), (3,1), (3,4), (0,4), (0,3), (1,3), (1,2), (2,2). One explicit 10-wall example outside the stacked-hall geometry is the named U2 with counterclockwise vertices (0,0), (9,0), (9,7), (5,7), (5,5), (7,5), (7,2), (2,2), (2,9), (0,9). Its cyclic turn pattern is L⁷R³ up to rotation and reversal. At x=6 and at y=3 the respective interior sections disconnect, whereas a stacked hall has connected sections normal to its banks. This particular U2 is lit by the project's separate cylinder theorem. Its presence here certifies the boundary of this result, not an OPEN classification for its entire pattern. [U2 geometry and independent review](adjacent-cylinders.md)
