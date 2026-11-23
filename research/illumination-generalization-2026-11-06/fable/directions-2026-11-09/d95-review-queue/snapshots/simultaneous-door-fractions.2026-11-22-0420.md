# Large denominators do not clear doors simultaneously

A strictly simple normalized 12-wall BBBB room can have an itinerary whose two width-one doors both have arbitrarily large reduced time denominators and arbitrarily fine individual placement grids, yet no slope clears both for the specified endpoints. R22 itself admits legal launch prefixes with arbitrarily large denominators at **all** their longitudinal stops and doors. Aiming at T couples different visits and prevents completion. Neither failure requires a door at time 1/2.

## What a fraction measures

For a fully unfolded reflection word with a specified lift of the target, the developed segment is fixed. To obtain a grid one has already allowed some image choices to vary. Even with a fixed source coordinate S and freely varying target images T+Pk, the transverse coordinate at time m/n runs through S+(m/n)(T−S)+(mP/n)ℤ in that developed chart. Modulo a chamber period one must further take the corresponding gcd. It need not have spacing 1/n. More importantly, distinct windows use the **same** endpoint image and slope. Transverse bounces alone never change the times for a fixed list of longitudinal travels; longitudinal reversals can change those times but introduce actual wall and door guards.

## DB55: every marginal passes, the two doors together fail

Use the named DB55 corridor stretch of even length L=10j+2, j≥1. The chambers are [0,5]×[0,5] and [5+L,10+L]×[0,5], joined over 2<y<3. Take S=(4,1), T=(6+L,3). They are interior and have the same coordinate parities. W=12, r=4 and n=50+L. The horizontal gcd is gcd(5,L)=1 and the vertical gcd is one. For example take j≥2, so n>64 and the reviewed normalized BBBB criterion applies. No room enumeration is involved. [Named stretch](twist-overlap.md) · [d69 §1](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d69-bbbb/README.md)

For a rightward-monotone path the longitudinal travels are 1,L,1. Both door time denominators are D=L+2, at fractions 1/D and (D−1)/D. On the positive sheets the periods are 10,2,10. Varying the middle column's full transverse periods alone moves the first seam by 2/D and the second by −2/D after reduction in its chart. The other generators are multiples of 2/D. Thus each one-dimensional projection of the endpoint-constrained placement lattice has spacing exactly 2/D. Each width-one door contains many individually admissible positions. On those same sheets the sum of the two crossing heights is always 4 modulo 10, whereas two points strictly in (2,3) have sum strictly between 4 and 6. [Placement identity](chain-criteria.md)

The miss persists on **all sheets**. Write s for transverse travel per unit horizontal travel, allowing either sign at either outer mark. A one-unit leg from height 1 can reach the mouth only when s modulo 10 belongs to the open intervals with lower ends 1,3,6,8 and width one. For height 3 the corresponding lower ends are 0,4,5,9. This follows by folding 1±s or 3±s into [0,5]. The sets are disjoint, including after allowing all physical signs; boundary equality is a lip hit. Hence no single slope works on the prescribed monotone chain for any L in this progression.

**A geometric repair on the same rooms.** Reflect from the right cap before reaching T. The left travel to its mouth is one; the backward right travel to the right mouth is now nine, including four to the cap. For 10/9<s<11/9 the two heights 1+s and 13−9s are strictly in (2,3), both on positive forward sheets. The backwards cap ordinate 3−4s is strictly between −5 and 0. The remaining match across the unit-height corridor is (L+10)s ∈ 2ℤ. Its candidate spacing 2/(L+10) is smaller than the interval width 1/9 for L>8, so rounding gives a legal path for every listed L. The same room and pair thus exhibit both effects: arbitrarily fine marginal grids can be jointly inconsistent, and a changed itinerary can repair them. This is a counterexample to the proposed sufficiency of the denominator test, not to the free-choice illumination conjecture.

## R22: no small door fraction on an arbitrarily long feasible prefix

Use the manuscript marks S=(0,0), T=(2,2). The source run has −1<x<1 between y=−1 and y=1. On each of these two horizontal end lines the portion −1<x<0 is solid and the opening is 0<x<1. At the top opening the next run is 0<x<4 for 1<y<2. These facts follow from the 15 listed cells. [Manuscript coordinates](../../illumination-publication/repository/preprints/twenty-two-wall/manuscript.tex)

Let D=2^m with m≥3. Launch downward in physical y. Use unit absolute vertical travel as time. At times j=1,3,…,D−3 reflect on the solid negative-x portions, alternating bottom and top. At time D−1 take the top opening, then travel one more unit to the target level. The final event is at the top since D−1≡3 mod 4. Every intermediate fraction j/D is in lowest terms with denominator D. In particular there is no longitudinal contact or doorway at halfway.

This is a physically feasible prefix, rather than an arbitrary list of walls. Prescribe horizontal velocity s=−4/(2D−3) per unit vertical speed. It hits the left lateral wall at time (2D−3)/4, not an integer, and crosses back through x=0 at time D−3/2. At every earlier odd event the folded x is strictly between −1 and 0. At D−1 it is strictly between 0 and 1. The beam enters the upper run legally. It misses T. All stated inequalities are strict and persist on an open slope interval around this launch.

**Why every slope aiming at T fails for this itinerary.** Let f fold the real line to [−1,1], centered so that f(x)=x on that interval, with period four. Then f(−x)=−f(x) and f(2−x)=f(x). Write z=f((D−1)s) for the required last crossing, 0<z<1. The forward horizontal sheet at this crossing is either positive or negative. In the upper run the target's transverse images are ±2 modulo 8.

* On the positive sheet, (D−1)s≡z mod 4 and z+s≡2 mod 4. Thus Ds≡2 mod 4 and z=f(2−s)=f(s). But f(s) is the first contact and must be negative.
* On the negative sheet, (D−1)s≡2−z mod 4 and z−s≡2 mod 4. Thus Ds≡0 mod 4. Events 3 and D−3 are both earlier solid-wall contacts, hence both require negative x. Yet f((D−3)s)=f(−3s)=−f(3s). Neither zero nor a lip is allowed.

This rules out all transverse reflection counts for this word of longitudinal contacts. The incompatible conditions relate **two visits**, even when every individual time denominator is arbitrarily large. The proof does not rule out a dyadic explanation on the globally folded staircase: it rules out the inference that this must appear as a physical door pinned to t=1/2 on every itinerary. D142's exclusion of a specific common-quotient midpoint construction supplies no converse for these path-level constraints. [R22 global obstruction](tokarsky-converse.md) · [d142 scope](two-image-midpoints.md)

## Status of the chain argument

| Link | Status |
|---|---|
| Two isolated rectangles admit a finite constructive path; explicit bound 6HD+5 reflections | Qualitative eight-wall result established in the project; quantitative note submitted for d157 review. |
| Keep a common open slope interval through a chain, then place a full terminal-cap reversal when the interval is wide enough | Sufficient conditions in the d157 submission. |
| Large denominators at all mandatory visits imply a common slope | False, including on a normalized BBBB room at W=12. |
| Some other longitudinal itinerary always succeeds in W≤20 BBBB rooms | Open. Neither denominator growth nor exclusion of a common midpoint quotient proves it. |

A route-selection lemma would have to control joint relations such as x_i+x_j modulo a period, or change the itinerary to remove them. Raising the individual denominators does neither in general. No discovery search or census was run.
