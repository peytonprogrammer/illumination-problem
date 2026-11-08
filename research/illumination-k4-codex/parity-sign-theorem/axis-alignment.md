# Axis-cylinder alignment from a tree of lattice fans

[done] General alignment argument accepted by independent tools-disabled Opus review, with the requested genericity, crosscut and component clarifications incorporated.
[done] Structural checks on 34 frozen rooms,1440 row cores and two prescribed controls.
[waiting on Claude] Independent live copied-script replay and proof challenge.

## Statement and precise class

Use the canonical triangular tiling of the integer grid. Label even-even lattice points A, odd-odd points B, and mixed-parity points C. Split every unit square by its A–B diagonal. Each small triangle has one vertex of each type, with its right angle at C. Its A–C and B–C legs are horizontal or vertical; its A–B hypotenuse is diagonal.

Let P be a compact strictly simple polygonal disk which is a finite union of these closed triangles. Assume that no B or C lattice point lies in the interior of P. Boundary B/C points may be smooth; the theorem does not require every one of them to be a polygon vertex. The deformation family fixes all physical wall directions and moves their supporting lines, staying strictly simple near P.

**Claim.** Every horizontal and vertical cylinder core of the standard eight-copy unfolding has period parallel to its original axis throughout this fixed-direction deformation chart. In particular, its transverse period derivative vanishes identically.

It suffices to treat horizontal cylinders. Choose a core at a generic fractional height in its row strip, such as height 1/2 in the unit-square cellulation. Its physical projection has horizontal or vertical velocity. To justify genericity, note that every physical reflection is in a line x=k, y=k, x-y=2 m or x+y=2 m. A horizontal line at fractional height h is carried to a horizontal or vertical line whose transverse coordinate is congruent to+h or-h modulo 1. With h=1/2 that coordinate is never an integer. Thus the projected core avoids every lattice point, every vertex and every axis-wall glide. This genericity assertion is needed only at the undeformed base polygon. A reflection at an axis-aligned physical wall is normal incidence and reverses the physical path. A diagonal-wall reflection turns its velocity by 90 degrees.

The proof has three steps: a tree decomposition; a local prohibition of backtracking without a normal reflection; and a reflection symmetry of the unfolded core.

## 1. Cut into A-centered fans

Cut P along every B–C edge whose relative interior lies in the interior of P. Such an edge is a unit axis-aligned segment with both endpoints on the boundary, by the no-interior-B/C assumption. Its relative interior is embedded inside P. It is therefore a proper crosscut of the polygonal disk.

The crosscut interiors are mutually disjoint. A C point has only two B-C edges, which are collinear. If both edges were interior crosscuts, all four triangles incident at C would occur and C would be interior, contrary to hypothesis. Crosscuts therefore share only B endpoints. Cutting along interior-disjoint disk chords that may share a boundary endpoint keeps each subsequent chord a proper crosscut in one of the remaining disks. Cutting a disk along each such arc increases the number of components by one and preserves disk topology of all components. Consequently the adjacency multigraph of the cut pieces is connected and has one fewer edge than vertices: it is a tree. In particular it has no parallel edges.

After these cuts, triangle adjacency across an uncut A–B or A–C edge preserves the A vertex. Conversely, the included triangles around any one A vertex form one contiguous fan: at an interior A all eight triangles occur, and at a boundary A strict simplicity gives one connected angular sector. Thus each cut piece consists of exactly the included triangles around a single A point.

Translate its center A to the origin. The fan lies in the square [-1,1]^2. Its B–C outer edges lie on x=±1 or y=±1, one unit per edge, with transverse coordinate in either (0,1) or (-1,0). Its other boundary edges lie on rays from the origin: diagonal A–B edges or axis-aligned A–C edges.

A B–C edge is either a portal to another fan or an actual physical wall. If a generic axis-directed ray hits an actual B–C wall, it reflects normally. If it hits an A–C wall, it also reflects normally: genericity excludes travel along that integer-coordinate wall. In the absence of normal reflections, the only physical reflections within a fan are on its radial diagonal A–B edges.

## 2. A fan cannot immediately return a normal-free ray through the same portal

Consider a unit-speed axis-directed ray which enters a fan through a portal, and suppose it has no normal reflection before its next exit through a portal. By an axis symmetry, take the entry point and incoming velocity to be

    z(0)=(1,r),    v(0)=(-1,0),    0<|r|<1.

The sign of r specifies which of the two unit B–C edges on x=1 is the portal. Every intervening reflecting wall is radial. At a reflection in a line through the origin, z dot v is unchanged because z lies on the mirror and its tangential component of velocity is preserved. Between reflections,

    d/dt |z(t)|^2 = 2 z(t) dot v(t),
    d/dt [z(t) dot v(t)] = 1.

The first expression is continuous through each radial reflection. Thus on the entire visit to the fan,

    z(t) dot v(t) = -1+t,
    |z(t)|^2 = 1+r^2-2 t+t^2.                 (1)

The trajectory must leave the bounded fan in finite time; otherwise (1) would grow without bound. Vertex collisions and gliding are excluded by the generic axis core. At a portal exit, its axis velocity is the outward unit normal to a side x=±1 or y=±1, so z dot v=1. Equation(1) therefore forces the exit time to be exactly 2. It also gives |z(2)|^2=1+r^2, so the exit transverse coordinate has absolute value |r|.

Suppose the exit portal were the entry portal. It is the same unit edge, so its transverse coordinate has the same sign as r. Its exit point must then be exactly (1,r), and its velocity is (+1,0).

Unfold the intervening diagonal reflections about the fan center. Their linear products belong to the four-element group

    K={Id,-Id,S,-S},    S(x,y)=(y,x).

The developed straight segment starts at (1,r) with velocity(-1,0), and lasts2. Its endpoint is therefore(-1,r). If the physical exit point is(1,r), the development matrix R would have to satisfy

    R(1,r)=(-1,r).                            (2)

No matrix in K satisfies(2) when0<|r|<1. Id changes neither coordinate; -Id reverses both; S and -S exchange their absolute values. Equation(2) would instead require the axis reflection diag(-1,1), which is absent from K.

Therefore a normal-free visit to a fan cannot exit through the same B–C portal it entered. The two unit B-C edges on the same side of a fan lead to the same neighboring A center. They cannot both be portals, since their common C endpoint would then be interior. Thus a normal-free visit cannot exit on its entry side at all.

## 3. Every generic axis core has a normal reflection

The chosen horizontal core closes on the finite square-tiled unfolding, and hence its physical projection is periodic. Suppose it had no normal reflection. It cannot remain in one fan forever by(1), so its successive portal crossings form a nonempty closed walk in the fan adjacency tree.

Every nonempty closed walk in a tree has an immediate edge reversal, including cyclic adjacency of its last and first edges. That would mean that one normal-free fan visit entered and exited through the same portal, contradicting Section 2. The projected core therefore has a normal reflection.

## 4. A normal reflection forces transverse period rigidity

At a nonsingular normal wall hit, let g label the current unfolding copy and R_i be the linear reflection in that physical wall direction. The copy-switching involution

    rho:(p,h) -> (p,G h),    G=g R_i g^(-1)

is a well-defined affine symmetry of the entire standard unfolding. Indeed the gluing rule h -> h R_j commutes with left multiplication by G. It fixes the hit point because the two incident copies g and g R_i are glued there. In the developed horizontal core direction, G=diag(-1,1).

Near the hit point, rho sends the horizontal core to itself with reversed orientation. The complete core contains no singularities, so uniqueness of straight continuation makes rho preserve that whole closed curve and reverse its homology class c:

    rho_* c = -c.

The same labeled-copy action exists on every nearby fixed-wall-direction deformation, with the same derivative G. Absolute holonomy is equivariant under this action:

    hol_v(rho_*c) = G hol_v(c).

The topological class identity is preserved under the material identification of the unfolding family. Thus

    -hol_v(c) = diag(-1,1) hol_v(c),

which forces the vertical component of hol_v(c) to be zero. This is an exact period identity throughout the chart, not merely a first-order assertion. The vertical-cylinder argument exchanges the coordinates. If the physical wall reflections generate a proper subgroup of D4, the formal eight-copy surface can be disconnected. Apply the argument separately on each connected component; the normal-hit involution preserves the component containing the chosen core.

This proves the claim. Independent mathematical review accepted the crosscut topology, scattering calculation and deck-reflection argument; no numerical execution by the reviewer is claimed.

## Consequence and remaining gap

The horizontal and vertical row-annulus multitwists of the original square-tiled surface have increments which are combinations of these axis core classes. Their transverse period derivatives therefore vanish for every allowed polygon deformation. The quadratic terms in the twist-orbit corner-event rows vanish, giving the affine-in-power formula established in `twist-span-lemma.md` Section 6.

This supplies the alignment premise for every room in the stated class if the proof survives review. It does **not** prove the signed slope maps have full quotient rank, or guarantee a sufficient seed family of one-corner events. Those are still separate tasks. It also does not treat holes, interior B/C lattice points, arbitrary angles or general degenerations.

The simply connected and no-interior-B/C hypotheses are essential to this proof method: interior B/C vertices can make a B–C segment fail to be a proper crosscut, allowing cycles in the fan adjacency graph. A diagonal-walled diamond can then have axis-directed periodic paths without any normal reflection.


## Structural checks and controls

`axis-alignment.py` checks only the34 previously frozen holdout geometries. Every A fan is contiguous, every interior B-C edge is a proper crosscut, and all 34 fan graphs are trees. The 720 horizontal and720 vertical row cycles each have two normal-incidence crossings, and the appropriate left-multiplication reflection preserves each cycle while conjugating its permutation to its inverse. The same-portal obstruction is checked symbolically: the only possible scalar root in the diagonal-reflection group is r=0, excluded for a generic core.

A prescribed complete A-star square has one fan and normal-reflecting cores. A prescribed diagonal diamond has interior C points, nonproper cuts and cycles in its fan multigraph; its axis cores have no normal reflections. This is a control of the proof's hypotheses and mechanism, not a claim that its transverse periods necessarily drift.
