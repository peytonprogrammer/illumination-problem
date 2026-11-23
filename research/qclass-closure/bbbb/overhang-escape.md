# Reaching a whole hall row through an overhanging attachment

D164 found 1,345 pairs in B and 2,028 in DB55 for which its bounded second search found no hall-walls-only shot. The bound was direction height 60 and 40 reflections. For its displayed B pair, attachment-wall necessity can be proved with no search bound. The same geometry gives a sufficient theorem for reaching *every abscissa on a row* from a child, at arbitrary real placements. [Attacker's report](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d164-attack-combs/attack.md)

**Geometry.** A parent rectangle of width v and height h opens with its full base into a rectangular hall of width A. A rectangular child above it meets its top along an open interval J of width w. Assume these bands and the traversed part of the hall have intact vertical sides. A mark in the child has abscissa x and height δ above its mouth. The target row is at depth B below the roof of the hall. All dimensions and depths are positive and the target lies in the open hall.

**Necessity in B.** The overhang has upper doorway (2,3), lower doorway (1,3), h=1, and mark (4,67/2) at δ=1/2. Any path to the hall without an attachment reflection must start downward. If it crosses the upper mouth at e, its lower crossing on the same line is 3e−8. For 2<e<3 this is strictly below 1. At e=3 the upper lip itself stops the ray. Thus *every* shot from this mark into the hall must first use an attachment wall, irrespective of its eventual direction or number of subsequent hall bounces. More generally, straight escape requires e in J and e+h(e−x)/δ in the parent's base, with smooth common-side reflections treated separately if allowed. The displayed mark is exactly at x=3+2δ, where the lip stops the limiting route. Strict failure holds for x>3+2δ inside the child, giving an open set of such marks.

**Sufficient condition for all targets on a row.** Put

    L(B) = min{ (δ+h+B) w/(2δ), (δ+h+B) v/(δ+h) }.

If L(B)>2A then every target on the row is lit. No floor is needed. The ray passes straight through the child, may bounce inside the parent, and may wind between the hall sides. The same conclusion holds for a two-bank hall as long as the target is reached before the opposite bank. The formula is uniform over child abscissas.

**Proof.** Choose the first crossing e anywhere in J. The child leg is inside a rectangle. The developed lower crossing e+h(e−x)/δ varies over an interval of length b=(δ+h)w/δ. The boundaries of the parent reflection sheets are spaced v apart. The largest continuous open piece of that interval within one sheet has length at least min(v,b/2): if two consecutive grid boundaries occur, take the interval between them; otherwise at most one interior boundary splits the interval. Fix such a piece. Its lower crossing folds strictly inside the parent base. Its horizontal velocity on exit is σ(e−x)/δ per unit of downward travel, with one fixed sign multiplier σ on the piece. The developed hall abscissa at depth B is therefore σ[e+(h+B)(e−x)/δ]+c for a constant c. Its range is open and has length at least L(B). A target abscissa has copies spaced 2A apart even on a single orientation. Choosing one in the range gives a legal shot: before hall entry all transverse contacts are in the interiors of parent sides and afterwards they are in the interiors of hall sides. All assertions exclude the artificial sheet boundaries at the parent exit. Equality in the sufficient bound is not claimed.

**A solid floor extends the result.** Write H for the hall height and B'=2H−B. Use the same construction to the reflected row at depth B'. At a floor corner the shot would stop. Two target images of the same orientation separated by 2A give floor abscissas separated in the developed hall by

    2A (δ+h+H)/(δ+h+B').

This lies strictly between A and 2A for 0<B<H. Hence both cannot be corners (corner abscissas lie in one translate of Aℤ). If L(B')>4A, the full row is lit by this family. If only L(B')>2A, the same proof lights all but finitely many abscissas on that row: over the chosen finite sheet piece only finitely many slopes hit floor corners, each giving one target abscissa. A second bank opening the floor invalidates this floor step.

**Application to the named B room.** Here A=6, H=32, v=2, h=w=1 and 0<δ<1. Both terms of L(t) decrease with δ, so L(t)>(2+t)/2 for t>0. Every child mark lights every hall mark at depth B≥22 by direct descent and every hall mark at B≤18 by the floor construction. On each intervening row at most finitely many target abscissas per child mark are left by this construction. These are pair-specific results for real marks.

For the attacker's pair choose e=379/132 and launch from the child along (−149,−66). The developed lower crossing is 3e−8=27/44 and folds at x=1 to 61/44. At hall depth 63/2 the developed abscissa is 262−66e=145/2, which folds modulo 12 to 1/2. Thus the shot reaches (1/2,1/2) with one parent-side bounce and twelve hall-side bounces, without any horizontal-wall bounce. This is a constructed direction outside the attacker's menu. It gives a simpler witness for that pair while proving rigorously that zero attachment contacts cannot work. DB55 has no parent–child overhang of this kind.

## What is the smallest W ≤ 20 room this result doesn't cover?

The ledger's ten-wall LLLRLLLRLR remains open for every length assignment and every interior pair. Its representative is (2,0), (4,0), (4,1), (3,1), (3,4), (0,4), (0,3), (1,3), (1,2), (2,2).
