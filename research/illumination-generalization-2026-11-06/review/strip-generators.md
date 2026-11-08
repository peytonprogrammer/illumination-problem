# Explicit strip generators for all orthogonal marked rooms

Candidate structural theorem for independent review. This is the entire ORTHOGONAL subclass of the current canonical45 W<=21 goal, including every interior A pair and arbitrary k. It provides an explicit geometric base/generator description and identifies which one-generator families the accepted neck theorem actually covers. It is not an optical equivalence under compression, and it does not settle the diagonal-wall subclass or the full goal.

## 1. Finite bounded bases with commuting even strip insertions

Translate the actual S to(0,0), and include the coordinates of EVERY vertex, S and T in each of two sorted lists of distinct x and y levels. Let these have r_x,r_y gaps. Then

    r_x,r_y<=W+1.

Each gap g is a positive integer. Write it uniquely as

    g=r+2n,  r in {1,2}, n>=0 integer,

where r has the gap's parity. In each axis replace its gaps by r, anchoring the source level at0. This gives integer base levels; their total span is at most2(W+1). A positive strictly increasing piecewise-affine coordinate map sends each old level to its base level. The product of the two axis maps is a homeomorphism of the plane and maps every horizontal or vertical edge to a straight edge of the same type. Consequently the base polygon is strictly simple with the SAME maximal-wall count and is a disk. Actual S,T remain distinct interior points.

Every level's coordinate changes by an even integer, because each gap changes by2n. Thus actual S=(0,0) and actual T remain even-even in the base room. Integer axial walls are canonical tiling boundaries, so the base is a canonical45 triangle disk as well. Internal mark alignments and shared coordinate levels are not perturbed or discarded.

Conversely increase any chosen base gap by2n. If the gap is to the source's right, translate all levels beyond it rightward; if it is to the source's left, translate all earlier levels leftward, keeping S at0. Use the analogous rule in y. These operations preserve coordinate ranks and actual A parity. All gap increments commute because the affected rank sets are fixed; rebuilding the original gap values reconstructs the EXACT original polygon AND target coordinates. There are at most2(W+1)<=44 such integer parameters; for the actual orthogonal W<=20 bound there are at most42.

There are finitely many possible coordinate-rank patterns for W vertices and two marks, and finitely many choices r in{1,2} for their gaps. Thus the bounded-grid marked bases form a FINITE list, geometrically complete for this subclass. No such list is enumerated here; no base is assumed to satisfy k<=6 or any other earlier optical hypothesis. The parameters n remain arbitrary nonnegative integers. The construction is explicit rather than an invocation of abstract semilinear decomposition.

This product map is used ONLY as a geometric classification. Its derivatives can change across transparent interior lines, so it generally bends rays. The already accepted piecewise-affine obstruction explains why it cannot be asserted to preserve illumination or darkness.

## 2. One gap opens a finite tree of parallel necks

Fix all gap parameters except one x gap and vary its increment. Its open vertical slab has no vertex or actual mark x level in its interior. Across that slab the room's vertical section is therefore a constant finite union of m disjoint nonempty intervals. No boundary vertex can change a section there. Each interval produces one horizontal rectangular neck when the gap grows.

Choose cuts strictly inside the BASE slab, retaining a fixed positive collar on each side; for base gap r one may keep collars of width r/3. All actual marks are outside the original open slab, so each lies strictly inside one resulting chamber, including marks whose x coordinate equals an endpoint level. The core width is then r/3+2n. Outside this core all chamber geometries and actual marks are FIXED as n varies, up to rigid translation of the right-hand components. Each neck mouth is a smooth relative-interior cap segment of its adjacent chamber.

Cutting the original polygon across a vertical line in this slab gives m disjoint proper polygonal arcs, each with distinct endpoints in genuine horizontal-wall interiors. One such arc, together with either of the two boundary subarcs between its endpoints, is a Jordan polygon; it separates the disk into two disks. Inductively each further disjoint proper arc splits one existing component into two. The result is m+1 disk chambers. The dual graph, with one edge for each cut interval, is connected and acyclic: each new cut replaces one node by two joined by one edge. It is therefore a TREE. The same chamber/neck tree describes every positive core length. The horizontal-gap argument follows by swapping x and y.

At a generic vertical cut each section interval has two endpoints on horizontal boundary walls. There are W/2 horizontal maximal walls in a strictly simple orthogonal polygon, and each can meet this vertical line at most once. Hence

    2m<=W/2,  m<=floor(W/4)<=5.

There are therefore at most six fixed chambers and five simultaneously stretched PARALLEL necks for a single generator. This is an exact bound in W, independent of k, support, wall lengths, endpoint coordinates and cut height. It does not bound the number of bounces or their phases.

## 3. Exact optical consequence already justified

If m=1 and S,T occupy opposite chamber nodes, the fixed-collar construction meets EVERY hypothesis of the independently accepted long-neck theorem. Thus for the fixed other gaps there is an N0 such that ALL integer n>N0 illuminate the actual pair. Any dark member of that one-parameter family must have n<=N0. The threshold depends on the other fixed geometric data, not merely on W.

If m=1 but both marks are on the same side, that opposing-mark theorem gives no conclusion. If m>=2, the unique tree route between the two marked chambers can require several necks, turns and returns. Extra branches cannot simply be capped with artificial mirrors. A closed auxiliary chamber trajectory between two selected mouths may hit a third mouth in between; the two-mouth first-transit proof does not establish legality after those other caps are removed. No multi-mouth routing theorem is assumed here.

Even a two-edge route may have both mouths on the SAME side of the middle chamber. Its physical horizontal velocity reverses in the chamber. The peer's accepted A18--A20 middle geometry has opposite supporting-line mouths and both entrance/exit horizontal velocities positive; its exact statement does not already cover this returning configuration. Its unfolding ideas may be adaptable, but that requires a separate proof of all signs, phases and actual mouth guards.

## 4. Exact controls attaining the bound and exposing the missing modes

The prescribed checker reconstructs the bounded bases and restores all original coordinates for four inputs: a rectangle, a primitive L, a U8 room and a20wall comb. It independently checks strict simplicity, actual interior A marks and the base span bound. Its exact cell decomposition at each chosen cut checks connected components, mouth incidences, absence of cycles and the m+1 count. There is no room census or ray search.

The U8 control is

    (0,0),(20,0),(20,12),(14,12),(14,4),(6,4),(6,12),(0,12),
    S=(2,10), T=(18,10).

A horizontal cut through y=7 has TWO intervals and three chambers. The middle lower chamber has both mouths facing upward; the unique route between the upper marked arms returns through that middle chamber. The room already illuminates by the accepted U8 theorem. It is a concrete geometry mode outside the literal serial/opposite-mouth hypothesis, not a dark example.

For sharpness atW20, take a spine [0,4]x[0,36] and five teeth [4,20]x[8j,8j+4], j=0,...,4. Its20vertex maximal boundary cycle and actual A marks S=(8,2),T=(8,34) are in strip-generators-check.py. The generic vertical cut x=6 has FIVE intervals, six chambers and dual degrees(5,1,1,1,1,1). Thus a five-mouth central chamber really occurs below21walls. No assumption that every generator creates at most two necks is valid.

Both these controls are used for exact structural bounds and distinctions, not all-path exclusion. No illumination verdict for the comb's marked pair is claimed from a failed or unperformed search.

## 5. What this changes in the global proof plan

The orthogonal geometry now has a concrete finite set of bounded marked bases and commuting strip parameters, rather than an unspecified collection of large shapes. A single parameter creates a tree of at most five parallel connections, with the same-side/multi-mouth modes explicit. The global octilinear geometric atlas remains the more general candidate for diagonal walls.

The unresolved implication is optical: cover these tree-routing and simultaneous-growth modes while retaining actual endpoint phases, and justify any descent to the finite bases. One-neck eventuality alone does not give a uniform bound when other strip parameters also vary. Nor do A19/A20 fixed-family residual-ray results automatically handle arbitrary moving chambers, multiple mouths, different directions of strip growth or their interactions. A finite hierarchy of geometric gap sizes does not remove arithmetic phase conditions.

Thus this is a complete structural normal form for the orthogonal subclass and a valid one-generator optical corollary, NOT a completed proof of illumination in that subclass. The full canonical45 W<=21 objective remains OPEN; no dark counterexample or universal22minimality is asserted.
