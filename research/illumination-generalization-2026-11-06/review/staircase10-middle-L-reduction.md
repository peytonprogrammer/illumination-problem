# ML01: middle-strip L lift and a smaller exact placement complement

Status: independent HAND positive reduction, pending reciprocal review. This directly simplifies the general all-metric staircase10 obligation. It is not a specialized metric family, a numerical example or the full illumination theorem. The only base is the already accepted all-real L theorem with orientation-controlled reflections.

## Vertical middle-strip lift

In the actual four-band room suppose, after exchanging endpoints, that

    y1 <= u < y2 <= v <= y3,
    S=(s,u), T=(t,v) are actual interior points.

There is an actual legal S-to-T ray using only genuine vertical walls. This includes u=y1, v=y2 and v=y3, with their actual strict interior width conventions.

Use the auxiliary L

    Q = [0,w1] x [0,y2] union [0,w2] x [y2,H].

Both marks are strictly interior to Q: actual source membership gives 0<s<w1; target membership gives 0<t<w2, and at v=y3 in fact t<w3. All heights are strictly between 0,H. The accepted L theorem supplies a finite ray between these actual marks with only vertical reflections and strictly increasing physical y. If the marks share a convex rectangle the direct segment has the same required properties. Thus every point of the path has y in [u,v], and all nonendpoint points have y strictly in (u,v).

For y1<y<y2 the vertical reflectors x=0 and x=w1 in Q are genuine original P walls. For y2<y<y3 the reflectors x=0 and x=w2 are genuine P walls. At y2 the L's actual step geometry equals the original geometry, so its strict portal and corner guards are exactly the original guards. The auxiliary vertical x=w1 below y1 and x=w2 above y3 can be artificial; neither can be touched because those open height ranges are outside the path. No auxiliary horizontal mirror is used at all.

Endpoint equalities need explicit treatment. If u=y1, the only path point at that height is S, whose x is strictly less than w1. Neither original corner (w1,y1) nor (w0,y1) is reached. If v=y3, the only path point there is actual T, with t<w3; neither original corner (w3,y3) nor (w2,y3) is reached. At v=y2 actual T satisfies t<w2 and is a transparent interior point, not a step corner. The other added original corners lie strictly outside the path's height range. The common left wall remains smooth at internal seam contacts. Therefore the exact entire L ray, with its one unfolded direction, signed germs, finite first-hit wall contacts and actual target identity, is legal in P. No artificial-cut reflection or retuning occurs.

## Transposed middle-strip lift

Transpose the entire room and swap endpoint order as needed. Its widths are (H,y3,y2,y1) and seam heights are (w3,w2,w1). Applying the preceding result gives an actual ray with only horizontal reflections whenever the endpoint abscissae, named left then right, satisfy

    w3 <= x_left < w2 <= x_right <= w1.

The same proof handles equality at w3 and w1, because these are actual interior endpoints, not auxiliary-boundary points. Transposition preserves first-hit/specular conditions and actual endpoint identity. Reversibility restores the originally requested S-to-T order. Internal original horizontal ledges may be used; this is a reduction of the FULL illumination target, not of ST10-A's five no-ledge programmes.

## Exact new residual after the accepted bottom/top lifts

The author's independently accepted bottom/top reductions already leave only

    0<u<y2, w2<=s<actual width at u,
    y2<=v<H, 0<t<actual width at v<=w2.

Within this domain ML01 resolves the pairs satisfying

    (u>=y1 AND v<=y3) OR (t>=w3 AND s<=w1).

Therefore, after all four justified L placement tests, the exact not-yet-covered domain is the same original residual together with

    (u<y1 OR v>y3) AND (t<w3 OR s>w1).

All boundary equalities have the displayed closed/open placement: u=y1 and v=y3 are INCLUDED by the vertical lift; t=w3 and s=w1 are INCLUDED by the horizontal lift whenever both endpoints are actual interior points. These are logical complements of sufficient placement tests, not necessary conditions for a legal ray of every other type.

For a further equivalent description within the original residual, actual membership implies s>w1 => u<y1 and v>y3 => t<w3. Distributing the conjunction therefore gives

    s>w1 OR v>y3 OR (u<y1 AND t<w3).

Thus the remaining case must involve a rightmost source tip, a topmost target tip, or the cross-placement below the first seam and left of the narrowest width. This does not claim any of those cases is dark or excludes the accepted top-window/triangle sufficient results. They may already solve parts of this residual.

## Handoff and limits

Requested reciprocal check: auxiliary walls outside the actual height interval; original corners newly introduced at the endpoint equalities; strict actual endpoint membership; transposed endpoint order; and exact residual complement. No new metric inequality, sample, search, engine, census, clock or worker is involved. The universal remaining cross-placement, all staircase10, all r3 and the broad r<=8 theorem remain OPEN. Accepted W<=8 foundations retain their prior scope.
