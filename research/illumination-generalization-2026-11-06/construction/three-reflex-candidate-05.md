# TR05 candidate: rotated-U transfer for upper-cap sources

Published before prescribed checks. Independent review pending.

Let 0<a<w<A, 0<l<w, 0<b<h<H, 0<c<h, and a<l OR c<b.
Let P have boundary

    (a,b),(a,h),(w,h),(w,c),(l,c),(l,0),(A,0),(A,H),(0,H),(0,b).

For EVERY actual source S=(s,u) with a<=s<=w and h<u<H,
and EVERY target T=(t,v) with l<t<A and 0<v<c, there is a finite,
corner-avoiding actual specular S-to-T path in P. No aspect-ratio or
reflection bound is assumed. Endpoints are arbitrary real points.

Use the specific accepted U construction in Q_B=C_U union C_R union C_B,
under isometry (x',y')=(H-y,A-x). The missing implication is that its
reflections avoid Q_B's artificial y=h segment 0<x<a and the added
original corner (a,h). The success criterion is strict source-arm contact
x>s>=a, including s=a, s=w and t=w; exact actual target attainment follows
from the accepted construction under the same isometry.

Strongest objection: the bare eight-wall theorem gives no control over the
artificial wall. We must use the direction-specific U/L formulas, not
illumination monotonicity or a limiting endpoint argument.

Combined with accepted TR04 partial coverage, the only pairs not covered
at arbitrary metrics are a point in (0,a)x(b,H) and a point in
(l,A)x(0,c). This is an endpoint reduction within the stated normal form;
it does not close that residual, the whole turn type, all W10, or r<=8.

No discovery search is needed for the hand proof or prescribed replay.
