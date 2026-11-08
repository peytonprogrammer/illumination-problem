# R44: wide-target far folds at arbitrary real core width

Author theorem pending independent review. Original conservative deadline07:02:00Z retained. Universal canonical45W21 remains OPEN.

## Statement

Use the same finite two-sided rectangular-spine comb as R42: all vertical coordinates integral, every tooth height2, positive same-side gaps, opposite overlaps allowed, arbitrary positive REAL horizontal widths and core width c. Select actual same-side midpoint marks S=(c,s), T=(c+D,t), s<t, t-s an even integer, D>=0. The source is an actual interior seam and the target tooth has actual width w>D. Then they illuminate at W<=23 if

    E=2w-D > 6c.                                      (1)

For D0 the sharper condition w>c suffices. No input witness, commensurability, size/exception cap or finite-prefix condition is needed. This introduces a real far-wall reflection, unlike R42's direct normal target arm. It is not an assertion that widening a room preserves illumination.

## 1. Two candidates on EACH side of the mean

For the virtual target midpoint depth E=2w-D>w, use copied center gap2H, H>=2, source depth0 and target midpoint images b+2n. Set

    A=2c+E, eta=2c/A, x=EH/(2c),
    tau_n=(2H+2n)/A,
    delta_n=(2cn-EH)/A=eta*(n-x).

Under(1), eta<1/4 and x>3H>=6. Take negative-side indices ceil(x)-1,ceil(x)-2 and positive-side indices floor(x)+1,floor(x)+2. Both per-side pairs are CONSECUTIVE integers. Every n is positive. Their deltas are strictly negative or positive as named and satisfy

    0<|delta_n|<=2eta<1/2.

Hence all four virtual target portals b+2delta_n are strict, and all target horizontal reflections before its virtual mark are smooth as in R42. The opposite turn candidates occur on the prescribed sides of the nominal mean. We must retain a valid candidate on EACH side after the new far-corner guard, not merely one candidate in total.

## 2. At least one candidate on EACH side avoids the actual far corner

Put z=w-D>0. The virtual target arm crosses its actual far line at distance E-w=z from its midpoint start, exactly once. Its only possible new corner is the familiar condition

    z*tau_n is an ODD integer.                        (2)

For two consecutive n on either fixed side, their far phases differ by

    2z/A = 2(w-D)/(2c+2w-D).

This lies STRICTLY between0 and1, since the denominator exceeds the numerator by2c+D>0. Two different odd integers are at distance at least2. Thus(2) cannot hold for BOTH candidates on that side. Select a candidate avoiding(2) independently on the negative and positive sides. This guarantees two nonzero signed candidates with strict portals AND smooth actual far crossings, for every real horizontal parameter meeting(1). No number-theoretic integrality assumption on c,D,w is required.

Fold ONLY the virtual target arm at depthw by r->w-|r-w|. It maps its virtual endpoint E to actual D. Every internal horizontal contact has0<r<E and folds to a strictly positive actual depth, at mostw; equality atw would be precisely the excluded corner. Insert the actual smooth far-wall reflection at its unique crossing. The core portal r0 and its incident velocity are unchanged, all ordinary horizontal reflections map to actual finite walls, and the original actual target is reached. The same argument handles an actual seam target D0, with every internal contact still strictly beyond its mouth. It uses no repeated fold at an open mouth or fictitious internal reflector.

## 3. The sharper D0 bound

If D0, E=2w and w>c give eta=2c/(2c+2w)<1/2. One nearest STRICT index per side, ceil(x)-1 and floor(x)+1, already gives0<|delta|<=eta<1/2. Here

    delta=n-w*tau_n.

If the far phase w*tau_n were an integer, delta would be an integer; strict nonzero |delta|<1/2 excludes it. In particular it cannot be an odd integer. Both signed candidates are automatically smooth far folds. This proves the sharper condition, including noncommensurable real c,w. Reversing the pair allows either selected seam tooth to be the wider one.

## 4. Three actual end charts and full wall contradiction

Apply the construction to original source s and target copies t,-t,2G-t, using a vertical reflection when the target copy is lower. Their half-separations h,mu,G-mu are integers>=2. The actual end fold sends their nominal means to mu,h,G-h. Each supplies a physical candidate on EACH side, within distance<1/2. All turn windows lie inside(0,G), since their centers are in[2,G-2]. Core crossings of end lines are ordinary actual floor/roof reflections at0<x<c. Selected target portals and horizontal contacts fold into the original selected tooth. The new far reflection cannot coincide with a global end at its tooth corner because(2) was excluded. Existing flush-tooth end contacts remain ordinary reflections. The endpoint is original T; truncate at an earlier actual T if present.

As in the accepted R41/R42 geometric argument, actual darkness would force each integer nominal level h,mu,G-h to be an opposite tooth MIDPOINT. A nominal smooth wall or mouth endpoint has one of its clean candidates on an adjacent actual wall of length at least1. If min(s,G-t)<=2, two forced opposite midpoints violate positive same-side gaps of their height2 bands. Otherwise all three blockers and both selected teeth are distinct nonflush teeth, giving W>=24. This contradicts W<=23 and supplies a finite actual path.

## 5. Finite-aspect reduction, with its limits

Combining with R42: any unresolved seam-to-positive-depth-midrow pair in this exact comb class must have D<=2c and E<=6c. Thus its selected target width satisfies

    w <= 3c+D/2 <= 4c.

The statement bounds one transverse aspect ratio, not the number of canonical rooms, core width, height, denominators, or required reflections. Other source widths remain arbitrary. A compact normalized region is NOT automatically covered by finitely many known witnesses, and no such prefix closure is claimed. For two seam marks, the sharper result instead requires both selected widths<=c for an unresolved pair. Other endpoint placements, taller teeth and arbitrary canonical45 polygons remain OPEN.
