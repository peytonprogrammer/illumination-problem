# Expanded explanation and additional construction

## Result

The original 22-wall room now has a four-page illustrated elementary proof. A second room, obtained by reflecting the original lower copy across x=-1, has 30 walls and the same dark interior pair S=(0,0), T=(2,2). Its two-page note includes geometry and the darkness argument.

The mechanism is unchanged: integer-axis unfolding preserves parity, so a putative ordinary connection of the even-even base marks passes through an odd-coordinate lattice point. Every such point in the base is an actual corner. A physical reflection at a smoothed seam endpoint projects to exact reversal at a convex base corner. Taking the folded subpath from its last a to its first b makes any such reversal impossible by retracing.

## Additional room

Base square lower-left corners: (-1,-1), (0,-1), (0,-2), (1,-2), (1,-3).

Copy maps: (x,y), (x,-y), (4-x,-y), (-2-x,y).

The added seam is x=-1, -1<=y<=0. Its upper endpoint (-1,0) is a genuine concave room corner with three occupied quadrants. Its lower endpoint (-1,-1) is smooth and folds to a convex base corner with velocity reversal. The other smooth endpoint events are at (1,0), (2,1), (2,3). All remaining base-corner preimages are actual room corners.

Exact counts: 40 base-corner incidences = 17 ordinary convex + 12 ordinary concave + 3 at the concave triple junction + 8 at four smooth seam endpoints. The union has one simple boundary and 30 maximal sides.

## Verification and review

Run `python3 -B check.py` from this directory, with its inputs subdirectory present. Results and complete coordinates are in check.json, inputs/room22.json and second-example.json. No optical discovery search is involved.

PDF rendering and extracted text/metadata checks pass; see pdf-qa.json. Separate Opus review ACCEPTS all four parts (see peer-review.txt, exit 0). Incorporated explicit inverse-map parity, direct per-endpoint velocity table, copy-independent smooth billiard law, and a detailed retrace-time contradiction. The reviewer's extension census requests were already present in the supplementary PDF. Its incidental claim about finite-length reflection counts is not used. The live peer has also received a neutral verification request through the board; that executable replay remains pending. An external expert's conditional novelty comment is not proof acceptance or a priority check.


## Final proofreading

Both final PDFs pass the persistent name and geometry audit in `proofread.py/json`; all six final page renders inspected. Clarity-only edits documented in `proofread.md`. Updated outgoing files remain `proof-expanded.pdf` and `additional-example.pdf`.
