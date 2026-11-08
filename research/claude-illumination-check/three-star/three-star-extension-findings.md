# Three-exception rooms with three full A stars

[done] All five necessary arrangements and all ten nonadjacent marked pairs are excluded below24 walls in the simple canonical45-degree family. Three arrangements are geometrically impossible. The straight arrangement and the L arrangement yield1 and22 distinct configurations, respectively; each has an exact illuminating path, and adding their positive-ray guards exhausts both cases. No smaller dark room was found.

Fresh CP-SAT replays and a separate one-hot fan/SCIP relaxation both exclude all ten cases. The independent model uses fan-angle traversal instead of the search model's angular slots and omits explicit Euler/connectivity requirements, making it a necessary relaxation. A fixed24-wall three-exception room is accepted by both models. Five full/clipped guard comparisons and24 unconstrained tile mutations preserve the checked paths. The bound enumeration also agrees with an independent66-pattern enumeration rooted at the middle vertex of a connected distance-two overlap graph.

## Complete finite reduction

Let I be the number of full A stars, P the number of partial A cells, k=J+s_N the number of B/C exceptions, E=2J+s_N their credit, Q the partial A charge, and m the number of absent external neighbors of full cells. Existing identities give W=2+6I+Q-E and E+m<=2k. The connected cell graph gives Q>=2P-2I-2+m.

For I=3, k<=3 and W<=23, Q<=3+E. Therefore 2(P+m)<=Q+8+m<=11+E+m<=17, so P+m<=8. The external full-star neighborhood has b<=8 cells, and at most8-b cells can lie outside it. The full-star distance-two overlap graph is connected: a disconnected three-star pattern has at least ten external neighbors. A connected three-point graph has a vertex adjacent to both others, so independently enumerating both neighbors within radius2 suffices. The five resulting unmarked arrangements have external neighbor counts8,8,8,8,7. Their complete supports contain11,11,11,11,21 A cells.

All nonadjacent choices of two marks among the three full stars are tested (3+2+3+1+1=10 raw cases). Adjacent marked full stars illuminate directly and cannot be dark pairs. Exactly three exceptions are searched here; earlier results cover at most two. Four or more full stars already have W>=6+6I-2k>=24 when k<=3.

## Model isolation and reproduction

Claude's two-exception inputs remain unchanged. `illumination_three_star_model.py` is a frozen copy of the earlier builder; a source comparison checks that the sole logic change permits exception budget3. Ray guards and the independent physical verifier are reused without modification.

Run with the existing read-only environment, after registering any output paths on the coordination board:

```sh
PYTHONDONTWRITEBYTECODE=1 .context/illumination-venv/bin/python -B .context/search_illumination_three_star.py --seconds 40
PYTHONDONTWRITEBYTECODE=1 .context/illumination-venv/bin/python -B .context/audit_illumination_three_star_extension.py
```

Search writes `three-star-geometry-*.json`, `three-star-case-*.json`, `three-star-control24.json`, and `three-star-extension-summary.json`. Audit writes `three-star-extension-audit.json`. For independent verification, copy the exact input paths in `three-star-proof-inputs.json` into a separate claimed directory before running, so the source receipts stay unchanged.

## Remaining scope

The two-full-star branch with three exceptions remains unsearched. At I=2 the same inequalities give P+m<=10, hence mark distance<=5 and ten normalized nonadjacent placements. All such rooms have at most36 triangles. These are necessary bounds, not a geometric or illumination exclusion. No full three-exception minimum or general-polygon bound is established by this phase.

**Next move:** test the complete two-star, three-exception supports.
