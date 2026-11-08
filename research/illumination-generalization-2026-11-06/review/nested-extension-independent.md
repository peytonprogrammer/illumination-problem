# Independent review of the nested-band and bounding-triangle lemmas

Verdict: ACCEPT both exact sufficient-class statements in the frozen peer packet. These do not imply the uncapped W<=21 theorem. This is independent mathematical hand review plus a separately written exact finite checker, not formal verification.

## One slope through all bands

I independently derive the invariant in nested-window-proof.md. At portal l, the surviving open interval consists of slopes for which the local developed abscissa is in (-w_l,w_l), with center (C_l-s)/T_l and radius w_l/T_l. The first interval is strictly positive because s<w_i and w_{i+1}<w_i. It starts in the actual source band even when ys=y_i.

The map to the next portal multiplies interval radius by 1+g_l/T_l and shifts its center to g_l(C_l-s)/T_l. Choosing an even multiple K_l of w_l within distance w_l of this center makes the new full exit window fit whenever w_l*g_l/T_l>w_{l+1}. Since ys>0, T_l<y_l, so the global non-strict premise G_l supplies this strict inequality, including equality cases in G_l. Its inverse image is a STRICT subinterval of the preceding interval. Thus the construction does not concatenate independent launch choices or lose an earlier guard. The integer k_l is finite and may be zero; this causes no degeneracy.

At the final portal, the target image interval has length at least 2w_j. For 0<t<w_j the two genuine image progressions have largest consecutive gap strictly less than 2w_j. Therefore an actual target image lies in its open interior even at yt=y_j. The chosen single slope belongs to every preceding interval.

For each band, physical x is F_{w_l}(s+tau(y-ys)-C_l). At its next portal the previous expression differs by the EVEN period K_l and has absolute value less than the next width. On both sides it is locally the same absolute value; x=0 is a genuine smooth left-wall reflection. At nonzero portal x neither expression reflects. Both endpoints of every ledge are excluded by the strict smaller-width guard. Height increases, so no floor/roof reflection or horizontal ledge contact is possible. Every other fold is on a true vertical wall interior. Finite band count, finite slope and positive widths imply finite contacts.

Source/target order can be reversed. Equal-height marks connect horizontally in the actual interior cross-section. A mark on a seam belongs to the upper band with strict x below its narrower width; same-band segments stay interior. The polygon has exactly 2m+2 corners because all width and height changes are strict. Consequently all claims for 2<=m<=9, arbitrary real dimensions, all distinct actual interior marks, and isometric images are accepted.

## Bounding triangle and ordinary axis reflections

The premise w_j/A+y_j/H>=1 is necessary and sufficient for closed triangle containment: in each band the triangle's maximum width occurs at its lower edge. Points with x,y>0 and x/A+y/H<1 are strictly interior even if a reflex corner is on the triangle side.

For S=(s,u), T=(t,v), the developed segment S to -T has axis crossing times s/(s+t) and u/(u+v). When equal, sv=tu and the direct physical segment is componentwise below one of its endpoints; it avoids the origin. Otherwise the two contact coordinates are |sv-tu|/(u+v) and |sv-tu|/(s+t), strictly between zero and their respective outer dimensions. They are on actual smooth walls. Before the first contact coordinates decrease from S; after the second they increase toward T. The down-set property puts those open legs strictly inside. The middle leg lies strictly inside the bounding triangle because BOTH intercepts are strictly smaller than A,H. Folding reverses exactly the relevant component at each of two separate times. All corners, other walls, artificial seams and actual target arrival are accounted for.

## Reproducible controls and limits

resumed-exact-check.py independently constructs four fixed paths, including four and nine bands, source and target seams, and exact G equality. It checks 645 genuine vertical reflections with exact rational open-leg/all-wall and velocity guards. Three fixed triangle-class paths include seam and collinear cases and four genuine axis reflections in total. These controls corroborate the hand proof; they do not prove arbitrary-real quantifiers by sampling. No peer construction script was executed, no discovery restarted, and no peer output was modified.

Uncovered: arbitrary-metric four-or-more-band stairs, other orthogonal shapes with >=10 walls, diagonal-wall rooms, the full uncapped canonical45 target, and universal minimality.
