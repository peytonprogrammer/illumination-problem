Advances: L1 — A horizontal excursion into a neighbouring template component can replace the virtual reflection when its two gate heights lie in the same unobstructed horizontal strip. The existence of such a strip and speed for every residual pair is unproved.

# Return through the non-target gate (partial)

Use the inside-column notation of [the grounded-component note, reviewed in d194](l1-grounded-component-transfer.md). The cap height b is a positive template integer (b≥1). The column has height Z=H+b, width j, and a source at horizontal distance ℓ from the target-side edge. The upper approach requires phase e−Bv at that edge. Write s for the source phase. The case at issue has H<b and both virtual contacts entering an upper opening. The following calculation is local. It gives a test at the base speed v.

**Reviewed inputs.** Each connected component of the sealed upper chamber touches the lower box through an open mouth. Otherwise that component would be disconnected from the interior of the original room. A vertical strip over such a mouth contains a grounded cell in that component. Apply directional minimality in the target's own component to obtain d194's first-entry conclusion for a target outside the closure of the grounded cells.

Let η be a uniform lower bound on the approach interval length, B_min a positive lower bound on its horizontal travel, H* the comparable upper bound on H, and b_max the largest cap height in the fixed template. Direct failure in d194 gives q₀ ≤ 2(H+b)/(Bη) ≤ 2(H*+b_max)/(B_min η), independent of the lower box. In the two-frequency test, bumps of radius ρ and K=1+⌈8/(π²ρ³)⌉ give omitted absolute Fourier mass at most 4/(π²Kρ³)<1/2, below the constant term 1. Under d194's solid-side or H≥b hypothesis, its bound on T=m+bn (H=m/n in lowest terms) therefore yields a uniform area bound A_aspect T²+V B₀(T/b)², with A_aspect/B₀=(D/u)/H and V the upper-template area. Below, A denotes horizontal excursion distance. [Independent review](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d194-review-grounded/review.md)

Take a horizontal strip in the neighbour, from the gate to a solid vertical wall a template distance A away. Assume the whole rectangle swept between those vertical lines and heights (l,r) is clear, the gate is open there, and the far wall is solid there. Choose signed phase coordinates on the gate on one fixed folding sheet, increasing or decreasing with physical height. Translate or reflect (l,r) into those coordinates. A trip to the far wall and back has horizontal travel 2A. It preserves vertical velocity and adds 2Av to signed height if it stays in that strip.

Let z be the common adjustable phase increment on the two column visits after freezing the ℓ shift as in d194. With the excursion included, the virtual endpoint equation is
```
2z = e−s−(B+2j−ℓ+2A)v     modulo 2Z.
```
Substitution into the phase at the first contact, s+(j−ℓ)v+z, gives the three successive phases
```
y−Av,    y,    y+Av,       y=(e+s−(B+ℓ)v)/2 modulo Z.
```
Here the two choices of representative modulo 2Z are the two candidate midpoint phases. The middle phase occurs at the far wall. Thus for one consistent representative the exact open-strip test is l+|Av| < y < r−|Av|. Linear interpolation along each leg proves sufficiency and necessity for this strip itinerary. Strictness supplies an open window in v. The outgoing phase includes the excursion's drift; asking for exact preservation of physical height would discard this route.

**Limitation under period shifts.** The strip calculation uses v. At v+kP a ray can leave the horizontal strip between its ends even when its predicted exit is congruent to the desired one. A sufficient replacement hypothesis is that each crossed vertical run has solid horizontal boundaries between its prescribed vertical exits, and that the period shift times each horizontal travel is a multiple of twice that run's height. Then folding preserves every signed exit by induction; intermediate horizontal reflections are legal. Split also at the far-wall turn. This applies in a fixed integral decomposition with all these travels integral after a common change of units. It gives a conditional return, dependent on the base-speed strip test and strict gate clearance.

**First open case for the inside-column row.** For the given upper approach interval J, one must find a v and a contact sheet with the clearance |Av| on both sides, or construct a different controlled return. Merely knowing that the contact y is interior supplies no such clearance. Even taking v near zero does not settle a contact approaching a strip endpoint at distance at most |Av|. D192 supplies a window for a shot from a fixed mark. Here the entrance mark itself moves as y−Av and the same v prescribes the return y+Av. Cutting at the next seam retains both conditions and can lead back to the original component. The finite number of components does not establish a decreasing induction parameter. This identifies a limit of the strip argument. Neither a dark family nor an area bound for all these placements has been proved.

Two parallel residuals remain for the wider chart: a repeated full traversal can cancel the terminal-height divisor, and a target already in a grounded cell falls outside the first-entry lemma. The inside-column return has priority here because its target approach is already available.

**What is the smallest W ≤ 20 room this result doesn't cover?** No ledger word moves. The W=10 word LLLRLLLRLR remains open for all lengths. Its ledger realization is (2,0),(4,0),(4,1),(3,1),(3,4),(0,4),(0,3),(1,3),(1,2),(2,2).
