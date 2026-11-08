# Exact original-wall placement reduction for every four-band metric

Application of the accepted all-real L theorem, not a re-proof or new base theorem. No metric inequality is required. This reduces the FULL actual illumination milestone, not the restricted ST10-A five-programme class.

The accepted L theorem supplies a vertical-reflection-only path with strictly monotone physical y between distinct endpoint heights, and by transposition a horizontal-reflection-only path with strictly monotone x. Equal-coordinate cases use a direct segment. It avoids all corners of the L and matches actual endpoints with one common direction. Source: review/all-real-L-dependency-review.md and its final acceptance.

## Bottom-L actual lifting

Let Qlow=[0,w0]x[0,y1] union[0,w1]x[y1,y2]. If BOTH actual marks have height strictly less than y2, they are strictly interior to this L, including actual interior seam points at y1.

Use the accepted VERTICAL-reflection-only L path. Every vertical wall of Qlow is an original P wall: x0, xw0 for0<y<y1, xw1 fory1<y<y2. Its artificial horizontal roof y2 is never touched since height stays between the endpoint heights, both belowy2. The extra actual reflex corner(w2,y2) is on that unused roof. Other original upper corners lie above. The L's own corners, including(w1,y1), are avoided by its theorem. Therefore the whole path is genuinely legal in P; containment alone is not the justification, the reflector orientation and all extra-corner locations are.

## Top-L actual lifting

Let Qup=[0,w2]x[0,y3] union[0,w3]x[y3,H]. If BOTH actual marks have x strictly less than w2, they are strictly interior to this L. Above y3 P itself forces their x<w3; at y3 an actual interior mark also has x<w3.

Use the accepted HORIZONTAL-reflection-only L path. Its horizontal mirrors are ALL genuine P walls: floor0 on[0,w2], ledgey3 on[w3,w2], roofH on[0,w3]. The artificial right wall xw2 belowy2 is unused since x stays between the two actual endpoint abscissae, both strictly beloww2. The added original corner(w2,y2) lies on that unused right wall; (w1,y1) is outside this L. The top-L corners are avoided by the base theorem. Thus every segment and reflection is actual in P. In particular the real ledge at y3 is allowed; this path need not belong to ST10-A's no-internal-horizontal-reflection class.

## Exhaustive residual placement

If neither condition holds, one point has height>=y2 and hence x<w2 (strict actual interior convention). Since not both x<w2, the OTHER point has x>=w2 and therefore height<y2. Label that other point S=(s,u), and the upper one T=(t,v). Precisely,

 0<u<y2, w2<=s<the actual width at u,
 y2<=v<H, 0<t<the actual width at v<=w2.

The source is in band0 or1 and the target in band2 or3. At u=y1 the source belongs to band1 and must have s<w1; at v=y2 ory3 the target belongs to the narrower upper band and is strictly interior. The equality s=w2 belowy2 is retained. No endpoint moves onto an artificial boundary and no endpoint placement is discarded by a limit.

Thus any complete illumination theorem for this residual cross-placement proves the whole four-band milestone, together with the two actual L routes. Conversely an actual dark pair in this family must occur in this residual placement, because the complementary pairs are illuminated by genuine P paths.

This is a placement reduction only: the residual cross-placement is NOT yet proved illuminated in all metrics. ST10-B addresses targetband3 under B and its transpose certain right-overhang cases; neither covers the whole residual domain. The broad all-r3/r<=8 goal stays open. No bound on reflections, area, rationality, support or aspect ratios is imposed. No new search, census, engine, worker, clock reset or git change.
