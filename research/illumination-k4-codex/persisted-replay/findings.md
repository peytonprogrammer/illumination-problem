# Independent replay of the persisted four-exception exclusions

[done] 2026-10-31. All 47,576 persisted witness records pass independent exact replay: 34,897 precomputed and 12,679 learned. No new paths, directions or rooms were searched. Claude-owned files and git state were not modified.

## Accepted result

The saved U/Z certificates are sound for **every slit-free canonical tile room** satisfying their requirements and containing the two marked full A stars. This is stronger than checking a path only in the room that produced it. Every learned path also passes in its saved physical room. The precomputed path records match, as multisets of exact U/Z tile sets, the separate caches consumed by the enumerator.

| Check | Result |
| --- | --- |
| Frozen inputs | 105 files, SHA-256 checked |
| Precomputed witness records | 34,897 pass across 19 files |
| Learned witness records | 12,679 pass across 19 files; six nonempty |
| Vacuous precomputed guards | 230 conflict with a forced marked star; harmless |
| Smooth lattice-vertex reflection events | 11,097 pass |
| Finished placement logs/stats | 19 consistent terminal `exit 0` receipts |
| Adjacent placement (2,0) | direct segment forced by the two stars |
| Placement coverage | all 20 placements independently reproduced |
| Search bookkeeping | 15,000 assignments/undos/late learns, 15,001 full state reconstructions, 790 guards pass |
| Corruption controls | all 12 rejected |

Counts are records/events, not distinct rooms or independent scientific discoveries. The 230 vacuous guards cannot prune any valid room with the forced marks. Their implications are true because their premises are impossible.

## Exact universal implication

`audit.py` imports no peer geometry or tracing functions. It reconstructs the canonical triangles directly. For each rational point it finds every incident closed triangle by exact half-plane containment, with no epsilon probes.

For each supplied segment, it cuts its parameter interval at the four families containing all tile edges: integer x and y, and even-integer x-y and x+y. It checks every open interval midpoint and every internal cut point. All triangles incident to these points must be used. The incident set is constant between successive cuts, so this covers the whole open segment, including vertex crossings and travel along internal triangulation edges.

For each supplied reflection it checks the reflection law exactly against the four possible mirror directions. The outgoing vector must be a positive multiple of the reflected incoming vector. It checks that the mirror splits no incident triangle interior. Every incident triangle on the incoming half-plane is required used; every triangle on the opposite half-plane is required absent. At a lattice vertex, this forces a complete smooth boundary half-plane. At an ordinary edge point, it forces the mirror edge. No genuine corner continuation is accepted.

Finally, every necessary used tile must belong to U or the two forced stars, and every necessary absent tile must belong to Z. Additional tiles outside these requirements cannot destroy the path. This establishes the requested implication over all completions; it is not a sampling of completions.

The learned builder uses floating-point normals, and the original precomputation uses fixed-epsilon probes. Neither is used as evidence here: every emitted condition was independently rebuilt with rational arithmetic. No defect was found in the saved records.

## I greater than 3 is already excluded at this threshold

Write k=J+s_N. Existing local identities give

    W = 2+6I+Q-2J-s_N,
    N = 8I+Q+s_A,       3s_A <= Q.

A finite nonempty set of full A cells has at least four external grid neighbors. If an external neighbor is occupied, its partial A fan contributes at least one unit to Q. If absent, the intervening midpoint of a full-cell side is a smooth C exception. Distinct absent cells can be charged to distinct such exceptions. Therefore

    Q >= 4-s_N,
    W >= 6+6I-2k.

At W<=21 and k<=4, I<=floor((21-6+8)/6)=3. Thus I>3 is **not an additional open branch for this threshold**. The four local missing-cell configurations are independently checked in `scope-check.py`; the extremal-neighbor and injection arguments are stated here to avoid treating a numerical table as a proof.

Also

    N <= 8I+4Q/3 = (4/3)(W-2+2J+s_N)
      <= (4/3)(21-2+8) = 36.

The peer cap NMAX=38 is consequently conservative. The existing stronger local-inventory table leaves only N<=35, but that table is unnecessary for the present bound.

For N<=38, the independently reconstructed infinite dual-tiling graph gives exactly the 20 normalized marked placements. It uses connector distance at most N-15=23. A chain between two disjoint eight-triangle stars uses at least distance-minus-one intermediate triangles, which proves the bound. A triangle centroid moves at most 2/3 in either coordinate per dual edge. Any room triangle is at most N-8 edges from the initial star; hence every vertex has coordinate magnitude at most (2(N-8)+4)/3=64/3. The search window [-24,24] contains every eligible room. No finite-window assumption was needed in the placement reconstruction.

## Search code assessment

The snapshot's local tables agree with the previous independent 528-mask audit. Active vertices are nonempty fans, so omitting the zero mask in their option lists loses no completion. Branches assign every unknown tile in the selected fan for every legal completion. A connected eligible room is reachable by this expansion from its two seeded stars. When there is no active vertex, every occupied fan has been resolved; untouched tiles are empty in that connected component. Connectivity and disk Euler characteristic are checked before accepting a room.

The pruning tests are necessary: selected tiles, completed exceptions and completed full stars cannot disappear within a branch; each unresolved occupied B/C vertex must eventually contribute a corner or an exception; a satisfied U/Z certificate proves illumination. The independent trail audit reconstructs all known/value masks, occupied counts, active vertices, wall/exception/full totals and certificate counters after each operation, including 5,271 locally invalid assignments and their rollback. Previous three-instance old/new room-set comparisons remain supplementary evidence.

Repeated node counts in distant-placement logs are not themselves a defect: the enumerator can expand disconnected seeded components before its terminal connectivity rejection. This audit makes no exclusion inference merely from repeated counts.

## What remains unverified

This audit accepts the witness layer, the finite bounds and placement coverage, and the tested search bookkeeping. It does **not** independently rerun the 53,188,384,010 reported search nodes, provide a branch-complete proof trace, or produce a formal UNSAT certificate. The completed logs and current source are frozen, but launch-time executable hashes, argv and environment were not recorded in those logs. The main code's branching/pruning argument was reviewed, not formally verified.

Accordingly, Claude's reported below22 exclusion is supported by independently validated certificates and necessary scope bounds. It remains a computer-assisted exclusion whose complete search execution has not been independently reproduced here. A fresh independent constraint-model replay using only these now-validated guards would strengthen the remaining execution evidence without discovering rays.

The global minimum, arbitrary polygon rooms, and presentations with k>=5 remain open. Integer subdivision can make k arbitrarily large without changing the physical room, so extrapolation requires a proved normalization or a geometric theorem. Historical priority is still unresolved pending the authors' replies.

## Reproduce

    python3 -B .context/illumination-k4-codex/persisted-replay/audit.py
    python3 -B .context/illumination-k4-codex/persisted-replay/mechanics.py
    python3 -B .context/illumination-k4-codex/persisted-replay/scope-check.py

All outputs stay in this Codex-owned directory. The first command took 120 seconds in this run. These commands replay supplied paths and test counting/bookkeeping only.
