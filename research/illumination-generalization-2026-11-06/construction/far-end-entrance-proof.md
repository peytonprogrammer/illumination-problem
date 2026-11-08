# An actual far-end entrance theorem for a comb

A34 candidate. Arbitrary real dimensions, actual distinct interior endpoints, no supplied path or finite-prefix hypothesis. Independent acceptance is required.

## Geometry and statement

Use the finite strictly simple rectangular-spine comb of A32. Its spine is [0,c] x [y_min,y_max], c>0. The selected right tooth is [c,c+w] x [l,l+u], w,u>0; other teeth are arbitrary disjoint bands. Put T=(c+D,l+b), 0<D<w, 0<b<u. Let S=(x_s,y_s) be an actual spine/seam interior point, 0<x_s<=c. If y_s is in [l,l+u], direct visibility settles the pair.

Otherwise there are two protected entrance charts:

1. If x_s<c, direct spine travel has positive horizontal distance C=c-x_s.
2. For every x_s<=c, an actual reflection at x=0 has positive unfolded spine distance C=c+x_s.

Claim: either chart gives a finite actual S-to-T specular path whenever

    2w-D >= C.                                             (1)

All polygon corners are avoided before the first actual T. The path may use horizontal tooth walls, one far tooth wall and, only in chart2, the actual left spine wall. It uses no artificial horizontal cap or mirror at a tooth mouth.

## Strict portal selection

Set L=2w-D. Use the horizontally reflected target image at abscissa c+L, and the two legitimate local vertical image progressions

    Y_(sigma,n)=l+sigma*b+2u*n, sigma in {+1,-1}, n in Z.

For direct chart1 use source image (x_s,y_s); for chart2 use (-x_s,y_s), followed by its actual x=0 reflection. In either chart the line has ordinate at its first entrance x=c equal to

    z_(sigma,n)=y_s + C*(Y_(sigma,n)-y_s)/(C+L).              (2)

For fixed sigma these portal heights form a two-sided arithmetic progression with step h=2u*C/(C+L). If L>C, then 0<h<u, so there is an integer n with l<z<l+u. This is finite exact rounding on a real interval of length u/h>1.

If L=C, then h=u. If the plus progression has no strict representative, all its representatives are mouth endpoints. The minus progression differs by -2Cb/(C+L)=-b, with 0<b<u. It therefore has a strict representative. This treats equality in (1), without a generic-position assumption.

Choose one such sigma,n. The portal is strictly within the actual mouth. Because y_s is outside the tooth band, the slope is nonzero. Either vertical sign and any integer n are valid; no sign or winding positivity is assumed in this finite tooth rectangle.

## Actual spine and tooth guards

In chart1, the segment before the portal has x<c and y between y_s and z, hence lies strictly in the spine. Its source is interior. No other tooth or mouth corner is met.

In chart2, the actual path first moves left from S and then right from x=0 to the portal. Its contact ordinate at x=0 is y_s+x_s*(z-y_s)/C. Since 0<x_s<C, this lies strictly between y_s and z. Both are strictly between the global spine ends. Thus the left contact is a smooth actual mirror point and both open spine legs have x<c. The initial leftward leg is legal even when S lies on another mouth seam x=c.

After the strict entrance, fold the unfolded horizontal coordinate once at c+w. Since w<L<2w, the physical coordinate moves from c to c+w and then to c+D; it never returns to c. Fold the vertical coordinate by the period2u triangular map. Every horizontal tooth-wall contact has x>c and, except possibly the far-wall crossing, x<c+w. These contacts are smooth actual mirrors. There are finitely many because the unfolded segment has finite length and u>0. The terminal image Y_(sigma,n) folds to the actual ordinate l+b, so its horizontal and vertical folds reach the actual T.

The only potential corner after the strict entrance is a simultaneous horizontal/far-wall contact at (c+w,l) or (c+w,l+u). The following argument eliminates it from the actual first-target path.

## Far-corner purification without continuing a legal ray through it

Parameterize unfolded travel by its horizontal progress q from the source image. The portal is at q=C, the far wall at q_f=C+w, and the final image at q_T=C+2w-D. Suppose the far crossing has vertical coordinate l+j*u for an integer j. The combined horizontal and vertical folds then reverse both velocity components. The folded trace after q_f is exactly the reverse of its trace before q_f, over the corresponding equal times. In particular the final T also occurs at

    q_early=2q_f-q_T=C+D.

Since 0<D<w, one has C<q_early<q_f. This earlier T lies strictly in the tooth, before the potential corner. Truncate there. All prior contacts have already been proved smooth. This reasoning uses the formula for an auxiliary folded trace solely to identify the earlier legal target arrival; it does not allow a physical billiard path through a corner.

If the far crossing is smooth, all contacts to the final T are legal. If T was met even earlier, truncate at that first arrival. Thus in all cases there is a finite actual corner-avoiding path.

## Whole-class consequences and a necessary condition for darkness

If the selected tooth has w>=c, every S strictly inside the spine with x_s<c illuminates EVERY actual interior T in that tooth: C=c-x_s<c<=w<2w-D. This is independent of the tooth height, gap, actual offsets, number of teeth or wall count. No small-depth remainder survives for these placements.

If w>=2c, the same conclusion includes EVERY actual spine/mouth-seam S, using chart2: C=c+x_s<=2c<=w<2w-D. Spine/spine pairs are already covered by direct visibility or one smooth left-wall reflection as in A32.

More sharply, if an actual dark pair has S strictly inside the spine and T in a different-height tooth, this construction forces

    c-x_s > 2w-D.

In particular w<c-x_s<c. For a seam S at x_s=c, darkness forces 2c>2w-D. These are necessary conditions only. They do not establish darkness when violated, all comb illumination, a finite wall-count reduction, or the universal W<=21 theorem.

The midpoint theorem and this entrance theorem remove different residual placements. All tooth/tooth off-middle pairs and narrow-tooth spine pairs outside (1) remain open in the general comb class. No novelty claim is made.
