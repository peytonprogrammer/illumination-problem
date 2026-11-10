# Every real T room illuminates every distinct interior pair

Exact corollary of the independently accepted arbitrary-real L theorem. Independent review requested. No bound on k, size, endpoint arithmetic, reflection count or aspect ratio is imposed.

## Statement

For any real parameters 0<a<b<A and 0<c<C, let

    P=([0,A]x[c,C]) union ([a,b]x[0,c]).

This is the strictly simple eight-wall orthogonal T room with cyclic vertices

    (a,0),(b,0),(b,c),(A,c),(A,C),(0,C),(0,c),(a,c).

Every pair of distinct interior points S,T has a finite ordinary specular connection avoiding every actual polygon corner. In particular, every canonical45 T room in this class illuminates all interior A pairs without any exception-count restriction.

## Accepted input

The arbitrary-real L theorem proves that every two distinct interior points in an L room admit a finite corner-free path using only horizontal-wall reflections, and also a path using only vertical-wall reflections. Rigid motions preserve those assertions with the corresponding wall orientations. The full source and independent reconstruction are pinned in all-real-L-dependency-acceptance.json. It does not need commensurable dimensions or rational endpoints.

## Exhaustive placement split

Write the horizontal bar R=[0,A]x[c,C] and the full stem column V=[a,b]x[0,C]. Both are convex rectangles contained in P. If both marks belong to either R or V, the direct segment stays in the polygon interior. Possible segments along an internal rectangle boundary remain interior to P: points of R on y=c can be interior marks only over the open stem; points of V on x=a or x=b can be interior marks only above c. Actual outside edges and the two reflex vertices cannot be interior marks.

Otherwise, after exchanging labels if necessary, S is strictly in the low stem:

    a<x_s<b, 0<y_s<c,

and T is high in the bar outside that column:

    c<y_t<C, and either 0<x_t<a or b<x_t<A.

The equality lines x=a,x=b and y=c have already been handled by the shared-convex-rectangle case or are actual boundary points excluded by the hypotheses. This split loses no interior mark placements.

## Left-hand bar target

Suppose x_t<a. Use the six-wall L subroom

    Q_left=([0,b]x[c,C]) union ([a,b]x[0,c]).

It is an ordinary L room after a half-turn, with positive dimensions satisfying all hypotheses of the accepted input. Both S and T are strictly interior to Q_left. Choose its connecting path with ONLY HORIZONTAL wall reflections.

Every horizontal wall of Q_left is a subset of an actual horizontal wall of P: its roof lies on y=C, its lower stem floor lies on y=0, and its exposed bar floor lies on y=c over [0,a]. A reflection on one of those smooth L wall portions is therefore an ordinary reflection in P with the same incident and outgoing velocities. The only added boundary portion is the vertical cut x=b, c<y<C. The selected path never contacts it, because it has no vertical-wall reflections and is corner-free.

One additional corner guard is essential: (b,c) is SMOOTH on the vertical boundary of Q_left but is a genuine reflex corner of P. The selected path avoids it too, since every contact at (b,c) would be a vertical-wall contact in Q_left. Thus it cannot become a newly forbidden actual corner when the rest of the T bar is restored. All other actual corners of P lying in Q_left are already L corners or lie on that same avoided vertical boundary.

Consequently the entire L path is also a valid finite corner-free path in the actual P, connecting the same physical S and T. This is not a claim of illumination monotonicity under arbitrary mirror deletion; the path transfers because it avoids every artificial mirror and every newly genuine corner.

## Right-hand bar target

For x_t>b, use

    Q_right=([a,A]x[c,C]) union ([a,b]x[0,c]).

Choose the horizontal-reflection-only L path. Its artificial boundary is the vertical cut x=a, c<y<C, which it avoids. The point (a,c), smooth on Q_right's vertical boundary but reflex in P, is avoided by the same orientation argument. Every horizontal reflection again occurs on an actual horizontal P wall. The actual endpoints and specular velocities therefore transfer unchanged. Reversing either construction handles the opposite source order.

These cases and direct visibility exhaust all distinct interior pairs, proving the theorem.

## Exact fixed control

For the T room a=4,b=5,A=10,c=1,C=3, take S=(9/2,1/2), T=(1/2,2). A prescribed connection has nine horizontal-wall reflections

    P_j=((311-32j)/78, 3) for j even,
    P_j=((311-32j)/78, 1) for j odd,
    j=0,...,8,

in order between S and T. These contacts come from the accepted L formula after the coordinate change (x'',y'')=(3-y,5-x). The physical x coordinate decreases throughout; every contact has x in (0,4), so each is on a genuine bar roof or exposed floor. The first leg crosses y=1 at x=343/78 in (4,5), strictly inside the stem portal. It crosses x=4 at y=47/16>1, safely above the actual reflex corner. The last leg reaches the specified T.

The exact checker verifies all segment-wall intersections, true reflections and corners for this fixed control. It is not a direction search, a reflection bound, or a replacement for the arbitrary-real proof.

## Scope and review targets

This is a cap-free T-shape theorem, not a classification of all eight-wall polygons. The U class is separately covered by the recovered all-real U theorem. Staircase and offset eight-wall shapes, and all other unbounded W<=21 cases, retain their existing status.

Review the exhaustive mark placement, both L embeddings, avoidance of artificial vertical mirrors, the smooth-in-L/reflex-in-P endpoint of each artificial cut, genuine horizontal wall contacts, and use of the previously accepted two-orientation L theorem. No change to the optical model or actual marked pair is allowed.
