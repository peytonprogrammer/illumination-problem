# A narrow folding converse needs a wall-frame hypothesis

A22 hand candidate for independent review. No fixed-room computation or discovery scan was run. This constructs a proposed43-wall genuinely octilinear dark room. It challenges ONLY necessity of folding onto an ORTHOGONAL parity base by pointwise inverse maps of whole congruent copies. It does not challenge the broader possibility of folding onto an octilinear parity base; this very candidate does that. It is above21walls and is not a counterexample to the active illumination objective.

## 1. A necessary wall-frame condition for the accepted whole-copy class

Suppose a strictly simple disk Q is assembled from whole congruent copies of a simple ORTHOGONAL base B, with disjoint interiors and pointwise agreeing inverse-copy maps wherever copies meet. The accepted shared-seam rigidity proof makes every positive contact a whole-wall reflection. The positive-contact graph is connected, since the interior of a strictly simple disk cannot connect piece clusters only through isolated boundary contacts.

Choose one copy's unordered pair F of perpendicular wall directions. A neighboring copy is its reflection across a supporting line of one of those walls. Such a reflection preserves the unordered pair F. Induction along the connected contact graph gives the SAME F for every copy, hence for every exterior wall of Q. Thus Q must itself be orthogonal up to one rigid rotation. This holds independently of the parity or marks.

In particular a dark room with both axial and diagonal walls cannot be in the precise orthogonal whole-copy class to which the accepted W>=22 shared-seam count applies. Merely saying it folds onto "a parity base" is ambiguous unless that base class is stated.

## 2. A17-wall octilinear parity base

Let P be the union of the nine unit squares with lower-left corners

    (-1,-1), (0,-1), (0,-2), (1,-2), (1,-3),
    (2,-3), (2,-4), (3,-4), (3,-5).

Its maximal boundary cycle is

    (-1,0),(1,0),(1,-1),(2,-1),(2,-2),(3,-2),
    (3,-3),(4,-3),(4,-5),(3,-5),(3,-4),(2,-4),
    (2,-3),(1,-3),(1,-2),(0,-2),(0,-1),(-1,-1).

It is an18-wall strictly simple orthogonal staircase, with no interior integer point. Its only smooth boundary integer points are a=(0,0), b=(4,-4): the top and right walls have length2, while all the remaining sixteen walls have length1. Every other integer boundary point is a listed vertex. Equivalently the nine-square chain has no four-cell integer junction, and the only two-cell half-plane boundary junctions are a,b.

Bevel the convex corner c=(2,-1), replacing the two boundary edges

    (1,-1)->(2,-1)->(2,-2)

by the single diagonal (1,-1)->(2,-2). Denote the closed resulting polygon B. Equivalently remove the attached closed triangle with vertices(1,-1),(2,-1),(2,-2) and close the remaining domain. Its new diagonal is x+y=0, a canonical A--B tiling edge. B is a strictly simple17-wall canonical45 disk of area17/2. The old neighboring270-degree vertices (1,-1),(2,-2) now have genuine225-degree interior angles; they remain corners. No integer point lies strictly on the new primitive diagonal segment. The removed triangle adds no integer point to the domain. Therefore B still has precisely a,b as its noncorner integer points, both even-even, and no interior integer point.

Every base wall reflection preserves the even-even class: this is immediate for integer axial lines, and reflection in x+y=0 is (x,y)->(-y,-x). It also preserves the full integer lattice. These are all wall directions of B.

## 3. Elementary nonillumination in the base

There is no nonconstant finite corner-avoiding billiard path in B from a to b. Unfold any proposed path into one nonconstant straight segment from a=(0,0) to an image of b. Every image is even-even by Section2. If the image is nonzero, its segment has a strictly earlier primitive integer point with at least one odd coordinate, since its coordinate gcd is at least2. If the image equals a, a nonconstant straight segment cannot join it to itself, so that case is already impossible.

Fold the earlier primitive point back by its actual finite reflection chart. It is an integer point outside the even-even class. In B every such point is a genuine corner. Thus the projected path is singular, contradiction. The argument includes boundary endpoints and ordinary smooth boundary reflections; it does not permit passing through genuine vertices.

## 4. Three reflected copies and actual interior marks

Take

    B0=B,
    B1={(x,-y):(x,y) in B},
    B2={(8-x,-y):(x,y) in B},
    Q=B0 union B1 union B2.

Their interiors are disjoint. B0 lies at y<=0, B1 at y>=0,x<=4, and B2 at y>=0,x>=4. The positive contacts are EXACTLY

    B0/B1: [-1,1]x{0},
    B1/B2: {4}x[3,5].

B0 and B2 do not meet: at y0, B2 occupies x in[7,9], while B0 has x<=1 there. The two marked full-wall seams have distinct endpoints. Gluing along these full boundary arcs gives one strictly simple polygonal disk; the bevels lie away from both seams. The inverse-copy maps

    f0(x,y)=(x,y),
    f1(x,y)=(x,-y),
    f2(x,y)=(8-x,-y)

agree pointwise on the seams. The actual marks

    S=(0,0), T=(4,4)

are strictly interior points of Q, lying in the relative interiors of those two seams. They are distinct even-even A points and satisfy f(S)=a, f(T)=b.

Every seam endpoint joins two90-degree convex base corners into one smooth physical boundary point. There are four such endpoints, with no identifications. All other copy vertices are genuine exterior vertices, including all six new225-degree corners from the bevels. Counting the3*17 corner incidences removes exactly eight incidences at the four now-smooth seam endpoints, so

    W(Q)=51-8=43.

It has actual axial exterior walls and the three actual diagonal bevel walls; hence it has no single orthogonal wall frame.

## 5. Smooth seam endpoints and the full projected endpoint fibers

A legal physical path in Q folds to a piecewise billiard path in B. Crossing a seam interior projects to an ordinary reflection at that SAME smooth base wall point. Outer reflections, including the diagonal bevel walls, project to actual base-wall reflections. A legal physical path cannot encounter any base corner image except the four smooth seam endpoints: every other base-corner image is a genuine Q corner.

At each of those four endpoints the base corner is90degrees. Folding its two physical half-rays through a180-degree smooth room half-plane gives exact reversal: the folded angular map has period pi, so the outgoing projected velocity is the negative of the incoming velocity. These are the only exceptional projected events. No new issue arises at the225-degree base corners because their images are actual forbidden room corners.

Suppose there were a finite legal actual S-to-T path. Consider its FIRST projected visit to b and its LAST projected visit to a before that visit. Such visits exist and are finite because the physical path and its fold have finitely many nonconstant line pieces. Between those selected times the projected curve contains neither a nor b.

If no exceptional reversal occurs between them, this is an ordinary corner-avoiding base path from a to b, excluded by Section3. If a first reversal occurs, its outgoing portion retraces the preceding nonsingular base path until reaching a. It cannot encounter b earlier, since that would also have been a preceding b visit, and it cannot acquire a new exceptional event before a because it is retracing a segment with none. It therefore revisits a before the selected b, contradicting the choice of last a. This handles any number of physical preimages of the marks without substituting an endpoint label.

Consequently Q has a genuine actual dark pair S,T, conditional on independent acceptance of these hand geometry and optical arguments.

## 6. Exact logical consequence and limits

By Section1, this43-wall room cannot be a pointwise whole-congruent-copy assembly of ANY orthogonal base, regardless of its parity property. It therefore refutes an UNRESTRICTED claim that every canonical45 dark room, at any wall count, belongs to that precise orthogonal class.

It does NOT refute a converse restricted to W<=21, and it does NOT refute a converse allowing octilinear parity bases: B is itself such a base. A necessity theorem with that broader conclusion would need a new wall bound for the broader base/corner class; the accepted orthogonal formula W=m(w-4)+4+2t3 cannot simply be reused for225-degree corners. None of this produces a room with fewer than22walls or proves universal22minimality.

No claim of historical novelty is made. This is a hand construction serving the requested converse-class audit, with no room/ray/direction/word/cylinder/orbit discovery computation. Independent proof review is required before counting it as established.
