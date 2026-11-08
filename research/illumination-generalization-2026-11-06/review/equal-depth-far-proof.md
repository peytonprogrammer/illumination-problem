# R43: equal-depth far-fold reduction to three minimal configurations

Author theorem pending independent review. Original deadline06:59:00Z is retained. Universal canonical45W21 remains OPEN.

## Theorem

In a finite strictly simple INTEGER two-sided rectangular-spine comb with core width1 and height2 teeth of arbitrary independent integer widths, consider actual interior A marks in different teeth on the same side at a COMMON integer depth D>=0. Assume W<=23. The pair illuminates if D>=3, or if at least one selected tooth has width>=D+2.

Equivalently, the only equal-depth configurations not covered here are D0,1,2 with BOTH selected widths exactly D+1. No bound on room height, size, exceptions, support or other tooth widths is used. Opposite-side bands may overlap, while same-side bands have positive gaps. This result concerns the actual pair, not illumination of an artificially extended room.

## 1. Explicit virtual far arm and the accepted phase data

If necessary exchange endpoints by reversibility so the selected width to be used is that of the target tooth, call it w>D. Set z=w-D>=1 and virtual target depth

    E=2w-D=D+2z.

Actual endpoint heights are unchanged. The generic virtual depth pair(D,E) has unequal same-parity nonnegative integers. It avoids the three exceptional R41 pairs EXACTLY when it is not one of(D,z)=(0,1),(1,1),(2,1). This follows directly from E=D+2z. Thus it is generic under the theorem's hypothesis, using either selected width.

Use R41's explicit STRICT residue table and its transports, rather than importing an existential path in a larger room. In every one of the three selected end charts, and at every corresponding integer half-separation H>=2, it gives two finite matching slopes whose strict actual-mouth residuals have turn displacements +/-epsilon, with0<epsilon<1. Each virtual selected prefix travels only from its own midpoint depth toward its mouth, with ordinary horizontal-wall contacts, positive horizontal progress, and legitimate midpoint-image parity. Its core legs use only the original width-one open core.

The source arm at depthD is already contained in its original actual tooth because its width exceedsD. The target arm at depthE extends beyond the actual far wall. Only THIS explicitly described arm will be folded, with the guards proved next. No extension or deletion of any other boundary is assumed.

## 2. Nonzero displacement excludes EVERY possible far corner

Order the two copied selected bands vertically for matching. If the depthD arm is lower and depthE arm upper, their common-slope turn displacement is

    delta=(D-E)*tau/2-(n_D-n_E)
         =-z*tau-(n_D-n_E).

If their order is reversed, delta has the opposite sign. In either order, if z*tau were an integer then delta would be an integer. Strict portals force |delta|<1, so that would give delta0. R41 uses NONZERO displacements. Hence

    z*tau is NOT an integer                           (1)

for BOTH independently constructed signed candidates, including all reflected end charts and transported periods.

The virtual arm starts on its midrow at depthE and proceeds horizontally toward0. It crosses depth w exactly ONCE. The unfolded horizontal distance from its start to that crossing is E-w=z. Starting a height2 strip on its midpoint, a simultaneous horizontal-wall contact at that crossing occurs exactly when z*tau is an ODD integer, independent of its initial vertical sign. Condition(1) excludes that and all stronger integer coincidences. The new far-wall reflection is therefore smooth; no actual corner continuation is needed.

## 3. Fold the entire virtual target arm into the actual target tooth

Use the physical horizontal fold of depth r,

    r -> w-|r-w|,    0<=r<=E.

It fixes the part0<=r<=w and reflects the partw<r<=E. It maps the virtual starting mark E to the ORIGINAL actual depthD. Every virtual horizontal contact has0<r<E. Its physical depth is positive and at mostw, strictly beloww except for the excluded simultaneous far corner. If D0, strict r<E still gives positive physical depth after folding, so an interior contact never becomes an artificial mouth mirror.

At the unique crossing of r=w insert the actual vertical far-wall reflection. It is smooth by(1). All existing horizontal contacts fold to actual horizontal selected-tooth wall interiors. Horizontal and vertical coordinate reflections commute, so every incident velocity obeys the ordinary axial reflection law. The strict target mouth portal r0 is fixed by this horizontal fold. Its matched incoming core velocity is unchanged at that portal. Reversing the folded prefix therefore completes the core path at ORIGINAL actual T; when the copied target is the lower virtual endpoint, the same statement holds after ordering/reversal. The selected other arm and all open core legs are untouched.

Thus every R41 signed candidate has a fully guarded physical realization whenever its opposite turn is a smooth actual wall. This is an explicit prefix conversion, not optical monotonicity of a wider tooth. Any earlier actual T can be taken as first arrival.

## 4. Global ends and the complete wall contradiction

Now fold the entire converted trace at the original physical core ends as in R41. The three nominal opposite levels are h,mu,G-h, all integers in[2,G-2]. Their candidate shifts remain nonzero and on both sides with absolute size<1. Strict portals map to the selected actual mouth interiors. The new actual far reflection stays inside its copied tooth band, away from its horizontal endpoints by(1), so cannot become a far corner at a global end. Existing horizontal contacts of a flush tooth on an end line remain ordinary reflections. All open core end-line crossings occur at strict0<x<1. The final copied target mark maps to original actual T.

Consequently the accepted R41 darkness argument applies to these PHYSICAL converted candidates: a nominal smooth-wall level or a mouth endpoint has at least one smooth candidate. Actual darkness would force all three nominal levels to opposite tooth MIDPOINTS. If min(s,G-t)<=2, two required height2 midpoint bands would touch or overlap. Otherwise both selected teeth and the three distinct opposite midpoint teeth are nonflush, forcing W>=24. Neither possibility is compatible with W<=23 and the stipulated gaps.

This proves the theorem for EVERY stated integer D,w and every other allowed metric parameter. It closes equal-depth D>=3 without the vertical-pattern cutoff of A51, and lowD cases whenever one selected far clearance is at least2. It leaves exactly three minimal selected-width configurations, not three rooms. Their opposite tooth widths and vertical geometry remain unbounded and are not settled here. Unequal actual depths are handled by separate R41/A52 work, not duplicated in this theorem. General taller/diagonal/chamber geometry and the native universal goal remain OPEN.
