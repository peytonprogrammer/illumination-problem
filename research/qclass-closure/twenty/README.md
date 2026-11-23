# Why the corner-only parity class needs 22 walls

**Computer-assisted theorem.** Fix a square grid and let the room be a strictly simple orthogonal polygon with vertices on that grid. Suppose that for at least one of even-even, even-odd, odd-even and odd-odd, every grid point of that class in the closed room is a polygon corner. If the room has fewer than 22 maximal walls, every two distinct interior points can be joined by a billiard path that avoids corners. Both endpoints may have arbitrary real coordinates.

The bound is attained. In the [15-square, 22-wall room](../../illumination-publication/repository/preprints/twenty-two-wall/manuscript.pdf), the odd-odd class meets the closed room at six convex and three reflex corners. The manuscript proves that (0,0) and (2,2) are dark.

## Why this covers every area

With r reflex corners, a simple orthogonal polygon has r+4 convex corners and 2r+4 walls. Below 22 walls it has at most eight reflex corners. Now charge each unit square to its unique vertex in the chosen parity class. By hypothesis only corners receive charges. Each convex corner can account for one square, and each reflex corner for three. The room therefore has at most (r+4)+3r ≤ 36 squares. This bound follows from the geometry even when the endpoints are irrational.

| Maximal walls | Distinct rooms up to translation and square symmetry | Evidence |
| --- | ---: | --- |
| Fewer than 18 | 26,706 | [Audit](lower-audit.txt) and [saved evidence](data/below-18.tar.gz) |
| 18 | 141,887 | [Census and proof for the last two rooms](../two18/README.md) |
| 20 | 913,622 | [Audit](twenty-audit.txt) and [saved evidence](data/twenty-wall.tar.gz) |
| **All counts below 22** | **1,082,215** | |

## How a finite calculation covers irrational endpoints

For most rooms a finite collection of cylinder directions on the unfolded surface covers both endpoints throughout whole regions. The remaining regions are enclosed in products of boxes in the two endpoint coordinates. Near a grid vertex or rational reference height, the program can choose a shear according to how close the actual endpoints are to that height. This turns arbitrarily small displacements into a bounded interval of displacements on the unfolded surface. One certificate for the interval then applies to a continuum of endpoint pairs. An alternative certificate proves that a particular sequence of wall reflections works throughout a box. The earlier [exact lattice-path census](../README.md) covers distinct pairs of interior lattice points when both displacements vanish.

Of the 913,622 rooms with 20 walls, 912,728 clear the whole-room checks. The other 894 go through every unordered pair of unit tiles, including two endpoints in the same tile. Three of those rooms need the finer endpoint-box calculation. The two 24-square rooms have 9,396 and 104,769 surviving box pairs, respectively.

The [method and verification notes](method.md) explain the enclosures, shear choice and reflected-path test. For the fourfold-symmetric 12-square room alone, [the verifier](pinwheel-audit.txt) checks 181,158 pairs of endpoint boxes. This resolves the 20-wall example left open in the [earlier cylinder search](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d13-cylinder-cover/README.md).

## Reproduction and scope

Extract the 20-wall archive into a fresh directory and run `python3 audit.py /path/to/directory` from this folder. For the lower-wall archive add `--lower`. These commands reconcile each room and tile-pair record, replay terminal certificates and match remaining lattice cases to the earlier census. To regenerate the geometry, run `bash replay.sh /path/to/new-directory` or `bash replay_lower.sh /path/to/new-directory`. Use this workspace layout so the scripts can find the previous cylinder solver and lattice certificates.

A separate cell-growth implementation [checks the 20-wall counts](shape-audit.txt) at each area and each grid alignment. The independent Python replay of the terminal certificates shares the earlier cylinder theory. The whole-room continuum solver has not been independently reimplemented end to end.

A smaller orthogonal lattice room with a dark pair would have to contain an interior grid point or a smooth-wall grid point in **each** of the four parity classes. In that complementary family, regular grid points can account for additional squares in the charge count, so the 36-square bound used here no longer follows. Rooms with incommensurable wall lengths also lie outside the theorem.
