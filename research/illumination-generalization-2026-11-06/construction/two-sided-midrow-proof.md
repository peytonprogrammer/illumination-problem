# Two-sided thin combs: positive paths and an alternating-opening condition

A35 candidate, pending independent review. This extends the accepted A32 optical mechanism to a new geometry; it does not assert a universal W<=21 theorem.

## 1. Room and exact endpoint class

Start with the rectangular core [0,c] x [y_min,y_max], c>0. Attach finitely many left teeth [-w_j,0] x [l_j,l_j+u_j] and right teeth [c,c+w_j] x [l_j,l_j+u_j], with positive widths and heights. Assume ALL selected tooth bands, including those on opposite sides, have pairwise disjoint closures with positive vertical gaps. Teeth may meet the global floor or ceiling. Their union with the core is a finite strictly simple disk.

Let E consist of actual interior points strictly inside the core in x, together with every middle-row point of a tooth, including its mouth seam. Thus core points satisfy 0<x<c. An arbitrary off-middle seam point is NOT included by this E definition.

The side word is the finite list of L/R labels of teeth in increasing band order. A side block is a maximal constant run of this word. Claim: if the side word has at most TWO blocks, EVERY distinct actual pair in E illuminates. All dimensions and actual marks may be real, independent and arbitrarily small or large. No reference path or reflection bound is assumed.

There is also a necessary condition in any such two-sided comb, without the two-block restriction: an E-pair can be dark only if its two endpoints lie on middle rows of distinct teeth on the SAME side, and some opposite-side tooth lies vertically between these two selected teeth and blocks the specific central reflection described in section3.

## 2. Opposite-side tooth middle rows always connect

After ordering the pair vertically and, if necessary, reflecting the whole picture horizontally, the lower selected tooth is right and the upper selected tooth is left. Translate y so their bands are [0,u] and [H-v,H], H>u+v. Write

    S=(c+D_s,u/2), T=(-D_t,H-v/2), D_s,D_t>=0.

Zero depth means the actual interior mouth-seam point. Put A=D_s+D_t+c and

    n_s(tau)=floor(D_s*tau/u+1/2),
    n_t(tau)=floor(D_t*tau/v+1/2),
    Phi(tau)=[H-(u+v)/2+u*n_s(tau)+v*n_t(tau)]/A.

Iteration from tau0=0 is nondecreasing. It remains bounded by H/c because floor(x)<=x gives

    Phi(tau)<= [H+(D_s+D_t)*tau]/A.

On that bounded interval Phi has finitely many values, even for irrational dimensions, so the iteration stabilizes in finitely many steps at tau>0. At the FIRST stationary value the preceding iterate is strictly smaller. A floor jump there would raise Phi by at least u/A or v/A relative to that predecessor, contradicting stationarity. Hence

    r_s=D_s*tau+u/2-u*n_s in(0,u),
    r_t=D_t*tau+v/2-v*n_t in(0,v),
    r_s+r_t+c*tau=H.                                    (1)

If a depth is zero, its floor is identically0 and its residual is exactly half its tooth height. It has no jump and presents no exception to the argument.

For each nonzero-depth endpoint, floor parity selects exactly one of the legitimate endpoint images +/-u/2 or +/-v/2 modulo twice the height, just as in accepted A32. Its physical tooth arm has n_s or n_t smooth horizontal-wall reflections, all strictly outside the core and before the actual far end. A zero-depth arm is empty. Use the single straight core segment

    (c,r_s) --> (0,H-r_t).

Equation(1) matches its upward slope tau to both folded arms. The open core segment has 0<x<c and strictly ordered portal heights. It touches no mirror or added tooth. Both portals are strict, including a zero-depth actual endpoint. The upper arm is the horizontally and vertically reflected reverse of its lower-tooth arm and ends at the ACTUAL T. Thus the finite actual path avoids every actual corner. Extra teeth on either side are irrelevant: the only middle segment lies strictly inside the core. The construction has n_s+n_t reflections, with no reflection invented on either core side.

## 3. Same-side middle rows: only one opposite opening can obstruct this path

Suppose both selected teeth are right, with lower band [l_s,l_s+u] and upper band [l_t,l_t+v], l_t>l_s+u. Include zero endpoint depths as in section2. Apply the accepted A32 iteration with A=D_s+D_t+2c. Its proof still holds with zero depths: the corresponding index stays0, the residual stays at the midpoint, and its empty arm begins or ends legally at a strict seam.

The resulting central path runs from the lower portal through the point M on x=0 to the upper portal. In physical y coordinates,

    y(M)=(l_s+l_t+v+r_s-r_t)/2,
    (l_s+l_t)/2 < y(M) < (l_s+u+l_t+v)/2.                (2)

Its two open legs have 0<x<c, and its selected tooth arms are unchanged. Therefore it is an actual legal path in the two-sided comb provided y(M) is outside EVERY CLOSED band of a left tooth. At such a point x=0 is a smooth actual mirror. Closed bands are essential: at an opposite-mouth endpoint M would be a true corner and the original reflection could not be used.

If y(M) is inside a left tooth, the old mirror is absent. No reflection there is asserted and no path through that opening is inferred. If y(M) equals its endpoint, no corner continuation is accepted. These are failures of this particular path only.

Consequently ACTUAL DARKNESS implies that at least one closed left-tooth band contains this y(M). The ordinate in (2) lies strictly in (l_s,l_t+v). Because all tooth bands are globally disjoint, a left band containing it must lie vertically BETWEEN the two selected right bands. This gives an actual necessary alternating R-L-R pattern. For left selected teeth the identical argument after horizontal reflection gives an L-R-L pattern, with its only candidate mirror on x=c.

In particular if the selected same-side teeth have no opposite-side tooth between them, the A32 path is legal. It is not enough to say the room is monotone or that a missing mirror can be ignored; the explicit smooth mirror at M is the guard that makes the transfer valid.

## 4. Other endpoint placements

Two strict-core points are directly visible, since their whole segment lies in the core interior. Two middle-row points in the same tooth are directly visible within that tooth rectangle, including a mouth-seam endpoint.

Let S=(x_s,y_s) be strict-core and T=(c+D,l+u/2) a right middle-row target. If D=0, the direct segment is inside the core up to its actual interior seam target. If D>0 and y_s is within the tooth band, direct visibility again suffices. Otherwise C=c-x_s>0. Use the legitimate vertical target images

    Y_n=l+u/2+u*n, n in Z.

Their direct-line portal heights are

    z_n=y_s+C*(Y_n-y_s)/(C+D).

This progression has step u*C/(C+D)<u, hence a strict portal l<z_n<l+u exists by finite exact rounding. The core segment before the portal stays between y_s and z_n with x<c; no opposite wall or mirror is touched. Folding the remainder within the actual target tooth ends at the actual middle-row target. All tooth-wall contacts occur strictly beyond the portal and before T's far end. This works for either slope sign and every real D>0. Horizontal reflection handles a left target. Reversibility handles endpoint order.

The E placements are exhaustive: strict core/core, strict core/middle row, same tooth, opposite teeth, or distinct same-side teeth. Only the last class can be dark, and section3 forces an intervening opposite-side opening there.

## 5. Complete two-block theorem and canonical consequence

If the side word has at most two blocks, any pair of same-side teeth has no opposite-side tooth between it. Section3 supplies its smooth central mirror. All other E placements were unconditionally illuminated. This proves the claimed all-real two-block E theorem, including small depths and mouth seams.

Suppose all axial boundary coordinates are integral and EVERY tooth has height2. Every actual interior even-even A point outside the strict core lies on or beyond a tooth mouth with an even integer ordinate strictly between its band edges. There is either no such ordinate, or precisely its middle row. Actual mouth corners and points on a boundary gap are not interior and are excluded. Thus EVERY actual interior A point belongs to E.

Hence EVERY distinct actual interior A pair illuminates in EVERY integer height2-tooth two-sided comb whose side word has at most two blocks. Widths, gaps, core dimensions, area, k, diameter, tooth count and wall count are unrestricted. This includes all W<=21 members of that class, with no finite-prefix remainder. More generally a dark A pair in any globally separated integer height2 two-sided comb must use same-side teeth with an intervening opposite-side opening covering the particular A32 mirror ordinate.

This does not cover globally overlapping opposite bands, arbitrary off-middle endpoints, thicker canonical teeth, arbitrary diagonal walls or all canonical45 disks. The alternating pattern is necessary only, and no dark counterexample is claimed. The universal W<=21 objective remains OPEN. No novelty claim is made.
