# Exact orthogonal eight-wall frontier

Independent hand classification; peer review requested. This is a finite classification of turn patterns and metric normal forms, not a finite census of rooms or a proof of their illumination. All dimensions remain arbitrary positive reals, with no k or size bound.

## 1. Four and only four turn patterns

Orient a strictly simple orthogonal polygon counterclockwise, suppressing all straight vertices so its vertices are precisely maximal-wall corners. At every corner the signed turn is +1 or -1 quarter-turn. If there are c convex and r reflex corners, then c-r=4 and c+r=W.

For W=8, r=2 and c=6. Let k be the shorter cyclic distance in edges between the two reflex vertices. Then k is exactly one of 1,2,3,4. A cyclic relabelling and, if needed, reflection of the polygon put either shorter reflex-to-reflex arc first. Once k and the first edge direction are fixed, the entire edge-direction sequence is fixed by the six + and two - turns. Therefore each k has exactly one turn-word type up to those operations.

There are C(8,2)=28 labelled positions for the two reflex vertices: eight with each of k=1,2,3 and four with k=4. The prescribed checker checks this combinatorial classification and verifies one strictly simple representative in each metric form. Neither the 28 words nor the four representatives replace the arbitrary-length argument below.

## 2. Metric normal forms

All forms are stated after an isometry, possibly including a reflection. Cyclic vertices are given; positivity of the edge lengths gives exactly the displayed inequalities, except for the explicit simplicity guard in case4. Conversely, every parameter choice satisfying these inequalities gives a strictly simple eight-wall polygon of its stated type.

### k=1: U

Use a,b,M,c>0, H_L>c and H_R>c, with A=a+M+b:

    (0,0),(A,0),(A,H_R),(a+M,H_R),
    (a+M,c),(a,c),(a,H_L),(0,H_L).

The adjacent reflex vertices are (a+M,c),(a,c). Following their outward edges and the six convex turns produces the displayed shape. The notch width M and both arm widths/heights are positive; unequal H_L,H_R are allowed. This is exactly the accepted arbitrary-real U theorem.

### k=2: staircase

Use 0<a<b<A and 0<c<d<H:

    (0,0),(A,0),(A,c),(b,c),(b,d),(a,d),(a,H),(0,H).

The reflex vertices are (b,c),(a,d), separated by two edges. The intervening convex turn makes the two horizontal step directions identical. Positivity of their lengths forces a<b<A, and positivity of the upward steps forces c<d<H. The remaining convex exterior arc closes the common left and bottom edges. This covers every metric realization of this turn word.

This class remains OPEN here. It is not an L or T under a rigid change of coordinates; a direct appeal to their illumination theorems would change the actual mirrors.

### k=3: unequal-floor T

Use 0<a<b<A and 0<u,v<C:

    (a,0),(b,0),(b,v),(A,v),(A,C),(0,C),(0,u),(a,u).

The reflex vertices (b,v),(a,u) have a three-edge short arc through the stem base. That arc forces 0<a<b<A and u,v>0. The opposite convex arc has a common horizontal roof; positivity of its two descending sides forces C>max(u,v). No equality u=v follows from the turn word.

This is exactly uneven-T-theorem.md. Its complete arbitrary-real optical proof is frozen and awaits independent review. The earlier equal-floor T theorem covers only u=v, so it would leave genuine k=3 rooms unaccounted for.

### k=4: offset corridor with a wide middle band

First write the edge-direction normal form

    (0,0),(B,0),(B,b),(A,b),(A,C),(a,C),(a,c),(0,c),

where 0<a,B<A and 0<b,c<C. The reflex vertices (B,b),(a,c) are opposite in the cyclic list. Edge positivity alone does NOT force a<B or b<c separately.

The polygon is strictly simple if and only if

    a<B OR b<c.

Indeed, if a>=B and b>=c, the nonadjacent vertical segment x=B,0<=y<=b intersects the horizontal segment y=c,0<=x<=a. Equality still gives a nonadjacent contact or repeated reflex vertex, so is also forbidden. Conversely, under the stated OR, neither this pair nor its opposite crossing pair meets, and the other nonadjacent edges have disjoint coordinate ranges. All edge lengths are positive, so the remaining boundary is strictly simple.

If b<c, keep the coordinates. If b>=c, strict simplicity requires a<B; reflect across x=y. The new parameters are

    A'=C, B'=c, a'=b, b'=a, c'=B, C'=A,

and satisfy b'<c'. Thus every case4 room has the normal form

    P=([0,B]x[0,b]) union ([0,A]x[b,c]) union ([a,A]x[c,C]),
    0<a,B<A, 0<b<c<C.

The middle band contains the horizontal projections of both outer arms. The arm ends a and B may be in either order or equal. If a>B, the two outer rectangles have separated horizontal projections and the middle band supplies a genuine corridor. Describing every case4 room as a union of two overlapping rectangles would omit these valid rooms.

This class remains OPEN here. The previously accepted three-band corridor theorem has different horizontal intervals and extra reflex corners; it does not automatically cover this normal form with arbitrary A,a,B,b,c,C.

## 3. Exact remaining scope

Among strictly simple orthogonal polygons with at most eight maximal walls: rectangles and six-wall Ls are accepted arbitrary-real foundations; k=1 U8 is also accepted. The whole k=3 class has a new frozen arbitrary-real proof awaiting review. Two eight-wall metric classes remain unresolved by those results: k=2 staircases and k=4 wide-middle offset corridors, with all their parameters unbounded.

This reduction does not address diagonal-wall polygons, larger wall counts, finite blockers, or the complete canonical45 W<=21 target. It proves no bound on k, cover degree, coordinate size, primitive directions, or reflections. No universal minimum.
