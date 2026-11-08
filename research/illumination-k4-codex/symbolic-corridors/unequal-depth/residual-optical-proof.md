# Continuous optical certificates for the finite residual rooms

Codex01a18403. Completed finite computational proof; independent acceptance required. The original finite run covered all22,538rooms with empty admissible complements. This is not yet final independent theorem acceptance.

## Actual endpoints and effective cap sheets

Work with d=g=1 and 0<s,t<=1. For a room record (a,A,b,B), actual chamber heights are (a+A)/2 and (b+B)/2. The four effective pairs are (a,b),(A,b),(a,B),(A,B). A strict successful chart on any pair gives an outer-simple auxiliary connection, which transfers to the original actual endpoints by the accepted outer-leg-transfer theorem, including cap-corner trimming.

For effective depths U=p/D,V=r/D in their least joint denominator, define

    H=U+V+ell, q=p+r+ell*D, ell=1 or 3,
    L=u+epsilon*t+4M,
    X(z)=s+(L-s)*(z+U)/H.

The normalized horizontal phases at virtual middle levels j are

    X(j)=[(q-p-jD)*s + epsilon*(p+jD)*t + (p+jD)*(u+4M)]/q.

For ell=1 use the two entry/exit guards of the accepted four-chart theorem. For ell=3 use the entry/exit guards of three-pass-circle.md and its two strict actual ledge guards at j=1,2. Every interval is unit length modulo four; split ledge intervals exclude the right-wall corner. Thus each successful chart is a conjunction of four (one-pass) or eight (three-pass) strict rational affine inequalities in the actual variables s,t.

The full phase period is q: replacing M by M+q adds 4(p+jD) at every required level. Every integer M, including negative ones, has a representative 0<=M<q with identical strict guards. Target sign epsilon and shift u are both enumerated. For each physical interval, all its translates intersecting the closed endpoint square are generated. The affine argument attains its extrema at square vertices; the integer translate bounds include those extrema and one extra period on both sides. An interval option is discarded only if at least one strict guard has nonpositive maximum on the square. This cannot remove any successful endpoint. It is unnecessary that every generated chart be feasible: empty conjunctions remove no points.

## Exact closed-complement calculation

Begin with the closed endpoint square [0,1]^2. Use homogeneous integer vertices (x,y,w), w>0, representing (x/w,y/w). Evaluate an integer affine guard (alpha,beta,gamma) by alpha*x+beta*y+gamma*w. Signs are exact. An edge crossing a guard's zero line has homogeneous coordinate c*D-d*C, where c and d are the guard values at its homogeneous endpoints; gcd normalization and a positive last coordinate give the same rational point.

Subtract an OPEN conjunction g1>0,...,gn>0 by retaining the union

    g1<=0,
    g1>=0 and g2<=0,
    ...,
    g1>=0,...,g(n-1)>=0 and gn<=0.

These closed convex pieces are exactly the complement. In particular, equality at an earlier guard is retained, including if all later guards are positive. The algorithm retains two-dimensional polygons, segments and points. Convexity permits the shortcut that a nonpositive maximum of any guard leaves the whole piece; positive minima for every guard remove the whole piece.

Every resulting piece lies in the original nonnegative square. It is inadmissible exactly when all vertices have x=0 or all have y=0. If both coordinate maxima are positive, the average of its vertices has both coordinates positive, even if the maxima occur at different vertices. Consequently, this filter removes only the excluded endpoint axes. It retains s=1, t=1, isolated admissible vertices, and segments joining opposite axes. Deduplicating identical homogeneous vertex sets preserves their convex hulls.

For each room, subtract all four cap sheets in increasing phase-period order, first one-pass and then three-pass if needed. An empty admissible complement proves every physical pair 0<s,t<=1 has at least one strict actual chart. Store every clause that changes the residual set, together with sheet and full chart parameters. These finite clauses are an exact continuous cover certificate. They can be checked later without regenerating or searching for any path.

If the run finds a nonempty complement, its rational vertex average is an exact endpoint witness for failure of these templates. Such a result would neither prove darkness nor refute the illumination theorem; it would require a different optical construction. Partial prefixes likewise do not establish all finite cases.

## How the finite proof joins the unbounded reduction

Only after all frozen room records have empty admissible complements, and after independent review of their chart geometry and continuous certificates, can this packet close the finite remainder. The earlier circle-margin proof handles all excluded large-denominator family members; the finite-support theorem handles depth pairs outside its exceptional support; and accepted equal-effective-depth transfer handles discarded equality cases. No sampled endpoint result, bounded reflection failure or denominator cutoff inferred from experiments is used in this join.

## Completed run

The original840secondaggregateeffort completed all22,538rooms without any residual cell. It applied 4522409 chart clauses; 490rooms needed at least one three-pass clause. Saved changed clauses form a finite continuous cover certificate for every room. The terminal process returned0within the original deadline. Independent replay and final acceptance remain required.
