# General geometry 02: do ordered spirals exhaust r=3?

Fable, 2026-11-08. Hand enumeration. Answer: no. Ordered spirals are one metric chart of one of eight turn types of simple orthogonal 10-gons. The ordered-spiral milestone is therefore a proper sub-milestone of all orthogonal r=3 rooms, and the project's room definition admits diagonal walls, which this file does not cover.

## 1. Counting

For a simple orthogonal polygon with r reflex corners, the convex corners number r + 4 and the walls number W = 2r + 4. So W = 10 if and only if r = 3, for orthogonal rooms. Canonical45 rooms that use diagonal walls are not orthogonal polygons; W = 2 + 6I + Q − 2J − s_N is the identity for them, and the r=3 label in the project's goal text should be checked against that definition before any all-r3 claim.

## 2. Turn types

Traverse the boundary counterclockwise. Each corner is a left turn L (convex) or a right turn R (reflex). With r = 3 there are three R's and seven L's in a cyclic word. Up to rotation and reversal the cyclic words are determined by the multiset of gaps (numbers of consecutive L's between successive R's), a composition of 7 into three parts up to dihedral symmetry:

    {0,0,7}, {0,1,6}, {0,2,5}, {0,3,4}, {1,1,5}, {1,2,4}, {1,3,3}, {2,2,3}.

The project writes gaps plus one, so the ordered spiral's {0,0,7} is turn type (1,1,8).

All eight are realizable as simple orthogonal polygons. Explicit coordinates, counterclockwise, with the reflex corners marked:

- {0,0,7}: (a,b),(a,h)R,(w,h)R,(w,c)R,(l,c),(l,0),(A,0),(A,H),(0,H),(0,b). The spiral.
- {0,1,6}: (3,0),(A,0),(A,H),(0,H),(0,1),(1,1),(1,3)R,(2,3)R,(2,1),(3,1)R. Bottom strip removed plus a stem rising at x in [1,2].
- {0,2,5}: (0,0),(1,0),(1,2)R,(2,2)R,(2,0),(4,0),(4,1)R,(5,1),(5,5),(0,5). Bottom side bite plus bottom-right corner cut.
- {0,3,4}: (0,0),(1,0),(1,2)R,(2,2)R,(2,0),(5,0),(5,4),(4,4)R,(4,5),(0,5). Bottom side bite plus top-right corner cut.
- {1,1,5}: (0,3),(1,3)R,(1,2),(2,2)R,(2,1),(3,1)R,(3,0),(A,0),(A,H),(0,H). Two-step staircase bite at a corner.
- {1,2,4}: (0,2),(1,2)R,(1,1),(2,1)R,(2,0),(4,0),(4,1)R,(5,1),(5,5),(0,5). L-bite at bottom-left plus bottom-right corner cut.
- {1,3,3}: (0,2),(1,2)R,(1,1),(2,1)R,(2,0),(5,0),(5,4),(4,4)R,(4,5),(0,5). L-bite at bottom-left plus top-right corner cut.
- {2,2,3}: (1,0),(4,0),(4,1)R,(5,1),(5,4),(4,4)R,(4,5),(0,5),(0,1),(1,1)R. Three corner cuts, one corner intact.

Each list was checked by hand for simplicity and for the turn word. Scaling by 2 and translating puts every vertex on the even lattice, so each type contains canonical45 rooms with interior even-even marks once the metrics are large enough.

## 3. Metric charts inside a turn type

A turn type fixes the combinatorics, not the inequalities among wall positions. For the spiral the chart is the removed region

    [0,a]×[0,b] ∪ [a,l]×[0,h] ∪ [l,w]×[c,h]

inside [0,A]×[0,H], which needs 0<a<w<A, 0<l<w, 0<b<h<H, 0<c<h, plus simplicity (a<l or c<b; with l<a and b<c the walls x=l and y=b cross). The signs of l−a and c−b split the turn type into three simple charts: (a<l, b<c) is the ordered spiral; (a<l, c<b); and (l<a, c<b). Transposition x↔y sends the ordered chart (a,l,w,A; b,c,h,H) to (c,b,h,H; l,a,w,A), which has l1<a1 and c1<b1 (reviewer F4, matching the accepted WJ01 swap audit). So transposition exchanges the ordered chart with (l<a, c<b) and fixes the chart (a<l, c<b). Revision 1 of this file said transposition fixes the ordered chart; that was wrong. The accepted TR04 "globally transposed" bounds use exactly this swap.

For the other seven turn types the chart count is larger because the bites and cuts sit on different sides with independent extents; it is finite for each type and can be listed when needed. No chart of any type other than {0,0,7} is covered by any accepted spiral theorem, because all accepted theorems use the spiral's four-chamber itinerary.

## 4. What this means for the milestone

- "All ordered ten-wall spirals" is: turn type {0,0,7}, chart b<c, all integer metrics. That is the stated immediate milestone, and it is consistent with the direction.
- "All ten-wall rooms" or "all r=3" needs: the chart c≤b of the spiral, seven further turn types with their charts, and the diagonal-wall rooms if the goal's definition includes them.
- A structural route that reduces a general r=3 room to a spiral would be the natural way to use the spiral milestone. File 03 examines what reductions preserve actual paths; by Corollary R of file 01 only translation coverings with matched bad sets do so without extra proof. Revision 1 of this file claimed that a covering cannot merge reflex corners because cone points map to cone points; that is false (reviewer F5): a 6π cone can map with local degree 3 to a regular point, and several 6π cones can lie over one 6π cone. File 03 revision 2 uses the reviewer's angle count instead.

Status: audit complete for orthogonal rooms (revision 2, F4 and F5 corrected); the diagonal-wall case is flagged, not resolved. The goal text is orthogonal, so diagonal rooms are outside the milestone, not silently inside it.
