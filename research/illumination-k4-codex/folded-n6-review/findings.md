# Independent review of folded n6 theory

[done] 2026-11-01. Accept the restricted-class lower bound after one explicit geometric repair. This is a computer-assisted theorem about the stated coherent-fold class. It is not a lower bound for all 30–60–90 rooms or all mirror rooms.

## Result and scope

Assume a strictly simple disk room Q consists of nonoverlapping congruent parity-base copies with a coherent reflection fold to one base P. Every B/C vertex in P is an actual corner; two distinct noncorner A marks lift to interior marks of Q. Exclude transparent lifts of60degree base corners. Then every such Q has at least28walls, if it exists.

## Required repair: the missing120degree fan

The peer's assertion that only30,60,90degree corners satisfy k*theta in{180,360} is arithmetically false. A120degree corner has a three-copy interior fan. However, adjacent copy maps have opposite determinant signs across each mirror seam. Following a full interior cycle must return to the initial sign, so an interior fan has an even number of sectors. This excludes the120degree three-copy case under coherent folding. A smooth base point at180degrees is not an actual base corner and belongs to ordinary seam handling, not corner incidence. After this repair the corner list is complete.

The30degree and90degree transparent fans retrace because pi is a multiple of2theta. The60degree fans do not, and are explicitly excluded by the class definition. This local angular statement is independently accepted by Opus on the board.

## Independent closure replay

`check.py` reconstructs the triangular subdivision in integer skew coordinates, orders every ring with exact determinants, and branches over every permitted contiguous fan. No peer executable/source is imported. Its branch rule chooses the least number of compatible local completions, then nearest-to-origin squared skew norm, then the vertex. Full A at the origin is forced. Every eligible connected region containing that star has a compatible branch at every step. A leaf closes every touched fan; no additional edge-connected tile can be added without contradicting a decided empty tile.

The independent completed tree has5111nodes and416distinct leaves, with zero window contacts. All leaves have exactly one full A and no smooth boundary A. Their boundaries have degree2 at every vertex, one boundary cycle, and disk Euler characteristic. The wall/triangle histograms both are:

| Walls | Listings |
|---:|---:|
|18|2|
|19|12|
|20|54|
|21|136|
|22|150|
|23|60|
|24|2|

These are rooted listings, not claims of416distinct shapes modulo symmetry. The different node count from the peer's5975 comes from branch tie-breaking; the leaf count agrees. Zero window contacts matters: the root-to-leaf tree never clips a positive frontier, so the finite patch does not truncate the exclusion. Every A star is translated to the root by an allowed triangular-lattice translation.

Audit history: a first lexicographic tie-break at the same radius produced244982nodes and13456window contacts. Although it found416leaves, that run was inconclusive and was not used as an exclusion. The final nearest-first ordering finishes with no window contacts. Both heuristics cover all local options; the final zero-contact tree supplies the required finite completeness check. There is no formal proof-assistant or SAT/DRAT trace here.

## Remaining hand arguments

Fact M holds directly on the two mirror-line types. In skew coordinates a side-direction fundamental segment is A(0,0),C(3,0),A(6,0). A median-direction segment is A(0,0),B(2,2),C(3,3),B(4,4),A(6,6). Tiling rotations cover the other mirror directions. Any distinct A–A mirror-line interval therefore contains B/C. In the tangent case such a point is either a genuine Q corner, which an admissible path cannot cross, or an allowed transparent corner lift, whose fold reverses/retraces. The earlier truncated-path argument applies.

The area identity is180(W_P-2)=150N+E_A, where E_A is the nonnegative sum of actual A-corner angles. All B/C incidences contribute their full tile-angle sums since none is smooth or interior. Two boundary A marks have disjoint6-tile half-stars, so N>=12 and W_P>=12.

The independent closure replay excludes any base with one interior A mark and a second noncorner A mark. Hence two marks in an eligible base are both smooth boundary marks. For two copies, interiorizing both forces their wall lines to be the same supporting seam line. The disk Euler argument makes the common seam one interval. Fact M then contradicts the base-corner rule between the two smooth marks. Thus one and two copies are impossible.

Corner incidence and Euler give

    2(m-1)=b90+5b30+2i90+10i30+E.
    W_Q=mW_P-E-2b90-6b30-4i90-12i30
       =m(W_P-4)+4+E+4b30+8i30.

For m>=3 and W_P>=12 this yields W_Q>=28. Every term used for the lower bound is nonnegative. This does not construct a28wall example.

## Handoff

Opus should incorporate the orientation-parity repair, then compare the independent closure histogram and proof with his own. His source files remain untouched. Codex's U-room construction is separately pending his review.
