# d236 validator: independent enumerator and lighting check

This directory holds an independent implementation of the d236 class (../README.md, section "Class") for areas 1 to 10. I didn't read ../astra/. I read only ../README.md, ../../d205-census-a21/validation/PASS.json, and ../../d205-census-a21/orbit.py (to learn the decider's method). The code in `validate.py` is my own.

## Result

- Counts by (area, W, bucket) for every area <= 10 are in `counts.tsv`. Only rows with at least one disc appear.
- Lighting covers every TOUCHING and OVERLAP disc of area <= 10, in `lighting.tsv`. The range holds 1 pair in total, and it's LIT. `dark.txt` records no dark pairs.
- No disc of area <= 10 has W > 20, so the W filter removes nothing.

Totals by bucket (discs, pairs):

| area | EMBEDDED | TOUCHING | OVERLAP |
|---|---|---|---|
| 1 | 1, 0 | 0 | 0 |
| 2 | 1, 0 | 0 | 0 |
| 3 | 2, 0 | 0 | 0 |
| 4 | 5, 0 | 0 | 0 |
| 5 | 12, 0 | 0 | 0 |
| 6 | 35, 1 | 0 | 0 |
| 7 | 107, 4 | 1, 0 | 0 |
| 8 | 363, 27 | 6, 0 | 0 |
| 9 | 1248, 122 | 47, 0 | 2, 0 |
| 10 | 4460, 628 | 270, 1 | 15, 0 |

## How to re-run

From this directory:

```
python3 validate.py 10 10 .
```

The arguments are the maximum area, the maximum area for lighting, and the output directory. The run first checks the d205 control room, then writes `counts.tsv`, `lighting.tsv`, and `dark.txt`.

CPU: the full run takes 8.1 CPU-seconds (single process). All runs in this session, including two smaller test runs and two diagnostic runs, took about 30 CPU-seconds.

## Model

A complex is a table `nb[c][d]`: the cell glued across side d of cell c, or -1 (d = E, N, W, S). The gluing rule fixes the direction, so the developing map f follows from the gluings of a connected complex. Corner q of a cell lies between sides q and q+1. Crossing glued side q from corner q reaches corner q+1 of the neighbour. A link is a connected component of the graph on (cell, corner) pairs. It's a cycle when its edge count equals its vertex count.

Final filters, applied only when counting:

- Link rule: every link is a path of 1 to 3 cells or a cycle of exactly 4.
- Connected (always true by construction) and F - E + V = 1, with E = 4F - G (G = glued side pairs) and V = number of links.
- W = links that are paths of size 1 or 3; W <= 20.
- Bucket: OVERLAP if two cells share a plane cell. Otherwise EMBEDDED if every plane-adjacent pair is glued and every lattice point touched by a cell has exactly one link. Otherwise TOUCHING.
- Marks = 4-cycle links. Pairs = C(marks, 2).

## Growth argument

Intermediate class: connected complexes in which every link is a path of at most 3 cells or a cycle of exactly 4. No Euler condition applies to intermediates.

Growth step: pick any position P adjacent across a free side of a present cell. Add a new cell at P. For each of its 4 sides, choose either no gluing or one present cell across that side whose facing side is free. At least one gluing is required. This step also covers overlaps, because P may already hold cells. The step decides every gluing between the new cell and the present cells at insertion time. A gluing between two present cells is therefore never added later: it's decided when the later of the two cells enters.

Completeness: take any valid K with F cells. Its gluing graph is connected, so order its cells c1, ..., cF by breadth-first search. Let K_i be the induced subcomplex on c1, ..., ci, with every gluing of K among those cells.

- K_i is connected, and c(i+1) is glued to at least one earlier cell. Each of its gluings to K_i uses a side that is free in K_i, because each side of K is glued at most once. So K_(i+1) is a child of K_i.
- The link graph of K_i is the induced subgraph of the link graph of K on the present (cell, corner) pairs. An induced subgraph of a path of at most 3 is a set of such paths. An induced subgraph of a 4-cycle is the 4-cycle or paths of at most 3. So K_i passes the prune.
- Paths of 4 never occur in K_i, so the prune can reject them. Links only merge as a complex grows, so a rejected intermediate has no valid extension either way.

Deduplication: the canonical key is the least neighbour table over every root cell and all 8 symmetries. Each table is numbered by breadth-first search in the transformed direction order. The key determines the complex up to translation and symmetry, because the gluings fix all positions. The growth step commutes with symmetries, so keeping one representative per key loses no class. Every valid K therefore appears at level F.

A side check: at every area through 10, the intermediate count equals discs plus annuli (for area 10: 4460 + 270 + 15 + 16 annuli = 4761). No other surface type occurs in this range.

## Lighting decider

The decider builds a 4-sheet unfolding on the abstract complex: one square per (cell, sheet). The horizontal neighbour in sheet (sx, sy) is the glued cell in room direction sx, or the same cell in sheet (-sx, sy) when that side is free. The vertical neighbour works the same way. Each square's label is the abstract link at its developing bottom-left corner, so two marks over one plane point stay distinct. Labels: mark index for a source, stop for a link of size 1 or 3, and pass for a link of size 2 (reflection is built into the sheet change).

The search runs breadth-first over the SL(2,Z) orbit with the four shear moves. States are kept up to label-preserving relabelling. Each state scan follows horizontal rays from every source square until a stop label or a return. A pair is DARK only when the orbit completes without reaching it. A state cap of 200,000 would make a pair UNDECIDED; no run reached it.

Control: the d205 control room (PASS.json `control_problem`, 15 cells, W = 22), pair (1,3)-(3,5), gives DARK with 2592 states and a complete orbit. That matches `control_c` and `control_python_states`.

## Predictions and scores

I made these predictions before the first run. I recorded them in my working notes, not in a file, and wrote them here after the run.

(a) EMBEDDED counts. Prediction: 1, 1, 2, 5, 12 for areas 1 to 5 (all polyominoes, since none can have a hole or a pinch). For area 6, 35. For area 7, 107: 108 heptominoes minus the one with a hole, whose hole also makes a pinch point. Score: exact for areas 1 to 7.

The brief lists "1, 1, 2, 5" for areas 1 to 5. That's four numbers for five areas. I read it as areas 1 to 4, and area 5 is 12.

Areas 8 to 10 give 363, 1248, and 4460. From memory, these match OEIS A000104 (polyominoes without holes). That's a guess: I didn't check OEIS. PASS.json has no per-area table for small areas, only area 20 and the aggregates `small_rows = 57` and `small_rooms = 22292`. My total through area 10 is 6234. If A000104(11) = 16094, then 22292 - 6234 = 16058 means 36 area-11 rooms have W > 20. That's plausible, but I didn't run area 11 to test it.

(b) Smallest OVERLAP disc. Prediction: area 9, a width-1 strip of 9 cells around a 1-cell hole, with its last cell over its first. Any smaller winding passes around a lattice point and makes a link of 5. There are exactly 2 classes: a seam at a ring corner (W = 10: 7 convex, 3 reflex) and a seam at a ring edge (W = 12: 8 convex, 4 reflex). Both have 0 marks. Score: exact. The enumerator finds no OVERLAP below area 9. At area 9 it finds exactly these 2 discs, with W = 10 and W = 12.

## Spec ambiguities and how I resolved them

1. F - E + V: the spec says "a glued side is one edge". I count each unglued side as one edge too, so E = 4F - G. Without that, a single square gives 5, not 1.
2. Link rule: the spec names the excluded path of 4 and the longer cycles. The spec allows only the listed shapes, so I also exclude paths of 5 or more.
3. "One link per lattice point" in EMBEDDED: I check every lattice point that is a corner of at least one cell.
4. TOUCHING is checked only when f is injective. Any disc with two cells over one plane cell is OVERLAP, whatever its gluings.
5. A ray that passes through a third mark continues. Marks are regular points, so this lights the pairs on both sides of that mark.

## Surprises

- The control range is almost empty for lighting. Through area 10, only one TOUCHING or OVERLAP disc has 2 or more marks. It's the area-10 TOUCHING disc: a 2 x 3 block plus a 4-cell hook around a 1-cell hole, with a pinch. Its one pair is LIT (20 states). The validator tests the lighting pipeline on almost nothing in this range. The d205 control is the stronger check on the decider.
- No TOUCHING disc exists below area 7. A slit needs both endpoints on the boundary, and in a hole-free shape that disconnects the cells. So every TOUCHING disc in range wraps around a hole, by a pinch (first at area 7) or a cut ring (first at area 8).
- Through area 10, the pruned intermediate class holds only discs and annuli.
