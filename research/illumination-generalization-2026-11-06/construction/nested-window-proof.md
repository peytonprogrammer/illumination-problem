# Nested staircase windows with one globally consistent slope

Candidate extension for independent review, Codex01a18403. No independent acceptance yet. This proves a sufficient geometric class, not every staircase or the uncapped W<=21 goal. The proof uses the accepted full-window atom repeatedly, without concatenating separately chosen directions.

## Statement within the active wall range

Let 2<=m<=9, w_0>w_1>...>w_{m-1}>0, and 0=y_0<y_1<...<y_m. Define

    P = union_{j=0}^{m-1} [0,w_j] x [y_j,y_{j+1}].

This is a finite strictly simple orthogonal polygon with exactly 2m+2 maximal walls, hence at most20. Dimensions are arbitrary real numbers; canonical45 lattice members are included. Suppose, for every 1<=j<=m-2,

    w_j (y_{j+1}-y_j) >= w_{j+1} y_j.          (G_j)

Then every distinct pair of interior points illuminates by a finite corner-avoiding path with only vertical-wall reflections. No size, arithmetic, denominator, k, or reflection bound is imposed. The same conclusion holds for any isometric image, including transpose. For m=2 the inequality list is empty.

The criterion is sufficient and restrictive. For m=3 it is the already accepted condition b(d-c)>=ac. New content is a simultaneous, one-slope proof through arbitrarily many relevant narrowings, including m=4,...,9; it is not a new claim for the previously completed three-band theorem.

## Endpoint convention

Reverse the desired connection if needed so ys<=yt. If the heights are equal, their straight horizontal segment is interior. Assign a point on an internal horizontal seam to the upper band. Thus a source in band i satisfies yi<=ys<y_{i+1} and 0<s<w_i; a target in band j satisfies yj<=yt<y_{j+1} and 0<t<w_j. Both heights are strictly between0 and y_m. At a seam the narrower upper width is precisely the actual interior cross-section.

If i=j the straight segment lies in the convex band rectangle and is interior to P. Assume i<j. Put T_l=y_l-ys>0 for i+1<=l<=j. These quantities are cumulative travel heights from the ACTUAL source, not independent per-band launch parameters.

## First strict portal window

Take n=1 and C_{i+1}=2w_i. For tau in the open interval

    J_{i+1} = ((C_{i+1}-s-w_{i+1})/T_{i+1},
               (C_{i+1}-s+w_{i+1})/T_{i+1}),

the lower band fold F_{w_i}(s+tau(y-ys)) reaches the first portal with developed coordinate z=s+T_{i+1}tau-C_{i+1} strictly in (-w_{i+1},w_{i+1}). Here F_w(q)=distance(q,2w Z). The entire interval is positive because 2w_i-s-w_{i+1}>0. The new band starts with the same local absolute-value fold, so position and velocity match, including the smooth x=0 portal contact.

The invariant for later portals l is: every tau in J_l satisfies every earlier strict portal condition; its developed coordinate at yl ranges over the ENTIRE interval (-w_l,w_l); and

    J_l = ((C_l-s-w_l)/T_l, (C_l-s+w_l)/T_l)

for a fixed finite sum C_l of the prescribed even wall periods. All tau in this interval are positive.

## Induction at the next narrowing

Write g_l=y_{l+1}-y_l>0 and theta_l=(C_l-s)/T_l. Under

    U(tau)=s+(T_l+g_l)tau-C_l,

J_l maps to an open interval with center g_l theta_l and radius

    R_l=w_l(1+g_l/T_l).

Choose K_l=2k_l w_l to be a nearest even multiple of w_l to that center. Its distance from the center is at most w_l. The choice is finite and nonnegative since theta_l>0. Because ys>0, T_l=y_l-ys<y_l. Condition G_l therefore gives

    w_l g_l/T_l > w_l g_l/y_l >= w_{l+1}.

Consequently R_l>w_l+w_{l+1}. The ENTIRE open interval (K_l-w_{l+1},K_l+w_{l+1}) lies inside U(J_l), even for a rounding tie and equality in G_l. Its inverse image is exactly J_{l+1} with

    C_{l+1}=C_l+K_l,  T_{l+1}=T_l+g_l.

This smaller slope interval retains all previous strict guards. At the next portal its developed coordinate is strictly inside (-w_{l+1},w_{l+1}); the preceding fold differs by an EVEN period K_l, so both adjacent expressions again agree locally as the same absolute value. This establishes the invariant for l+1. The source band i can be any band: only the globally stated G_l with l>=i+1 are used.

## One actual target, one launch slope

After the last portal, J_j is nonempty, open, positive. The final coordinate

    Z(tau)=s+(yt-ys)tau-C_j

has image interval length

    2w_j (yt-ys)/T_j >= 2w_j.

The actual target images {t+2q w_j,-t+2q w_j} have alternating gaps2t and2(w_j-t), both strictly less than2w_j. Hence an image Y lies strictly inside that open interval, even at equality yt=yj. Choose tau=(C_j+Y-s)/(yt-ys), which is strictly inside J_j and therefore satisfies EVERY preceding portal condition with the SAME slope.

In band l>i use

    x(y)=F_{w_l}(s+tau(y-ys)-C_l),  y_l<=y<=min(y_{l+1},yt),

and use F_{w_i}(s+tau(y-ys)) in the source band. These formulas match at every portal by the even-period identities above and terminate at the actual target. At yt=yj the last band has zero length; the target is reached at the specified interior point of the seam.

## All genuine-corner and reflection guards

Physical height increases strictly. Thus there are no horizontal-wall reflections or visits to a roof or floor. Between portals, the vertical folds occur only on actual wall interiors x=0,w_l. At a narrowing, the strict bound |z|<w_{l+1} excludes the reflex corner (w_{l+1},y_{l+1}) and the convex ledge endpoint (w_l,y_{l+1}). A portal value z=0 is a smooth actual common left-wall contact, represented by the same absolute value on both sides. No splice changes the velocity illegally. Each genuine wall contact reverses only horizontal velocity, with vertical velocity fixed positive. Positive widths, a finite slope and finitely many bands imply finitely many contacts. The construction therefore gives an ordinary finite specular connection avoiding every polygon corner.

## Review boundary

No arbitrary-metric four-band or larger staircase theorem follows. Failure of any G_j is not evidence of darkness. The original canonical45 W<=21 objective includes many nonnested and diagonal-wall rooms that this argument does not address. Independent peer review is required before this candidate is counted as verified progress. Source/target seam cases and global launch-direction consistency are explicit rather than delegated to density or numerical controls.
