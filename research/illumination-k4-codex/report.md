# Joint illumination part B: local inventories and geometric supports

[done] Local-inventory classification through k=12 and complete k=4 support eligibility reduction. Independent peer review is requested. The general minimum and darkness of the surviving families remain open. No ray tracing, ray cuts, orbit runs, or new darkness verdicts.

**Theoretical correction for part A:** k is not invariant under integer dilation and subdivision. The known dark 24-wall room has presentations with k=0,53,98,187 at scales 1,2,3,4. A useful finite reduction needs a primitive presentation or a bound up to similarity. See scaling-obstruction.md; the count tables remain valid presentation-specific results.

## Local-inventory feasibility table

A cell is the exact tuple (I,J,s_N,Q,N), with W determined by the wall identity. Every feasible cell has an integer inventory witness in table.json. Feasible here means that counts of legal local fans can match; it does not assert a compatible planar embedding or a dark pair.

| k | Arithmetic candidates | Inventory feasible | Inventory infeasible | Surviving I | Largest N |
| --- | ---: | ---: | ---: | --- | ---: |
| 4 | 305 | 191 | 114 | 2, 3 | 37 |
| 5 | 469 | 338 | 131 | 2, 3 | 40 |
| 6 | 712 | 555 | 157 | 2, 3, 4 | 43 |
| 7 | 1033 | 837 | 196 | 2, 3, 4 | 46 |
| 8 | 1435 | 1206 | 229 | 2, 3, 4 | 49 |
| 9 | 1913 | 1643 | 270 | 2, 3, 4, 5 | 52 |
| 10 | 2482 | 2160 | 322 | 2, 3, 4, 5 | 54 |
| 11 | 3155 | 2794 | 361 | 2, 3, 4, 5 | 57 |
| 12 | 3940 | 3501 | 439 | 2, 3, 4, 5, 6 | 60 |

All 15,444 verdicts agree with the independent, solver-free integer-angle dynamic program in inventory-dp-audit.py. There are no UNKNOWN cells. The table covers exactly k=4,...,12; no finite upper bound on k for dark rooms is claimed.

### Four-exception detail

| I | J | s_N | Feasible tuples | Q range | N range |
| --- | --- | --- | ---: | --- | --- |
| 2 | 0 | 4 | 25 | 4–13 | 20–32 |
| 2 | 1 | 3 | 30 | 3–14 | 19–33 |
| 2 | 2 | 2 | 34 | 4–15 | 20–35 |
| 2 | 3 | 1 | 38 | 5–16 | 21–36 |
| 2 | 4 | 0 | 42 | 6–17 | 22–37 |
| 3 | 0 | 4 | 0 | — | — |
| 3 | 1 | 3 | 2 | 7–8 | 31–32 |
| 3 | 2 | 2 | 5 | 6–9 | 30–34 |
| 3 | 3 | 1 | 7 | 6–10 | 30–35 |
| 3 | 4 | 0 | 8 | 7–11 | 31–36 |

Ranges are marginal summaries; combinations inside a range need not be feasible. Use the individual JSON cells for precise membership.

## Constraints and independent verification

The finite inventory contains 11 A fan types, 11 B types, and 5 C types, after identifying orientations with the same tile incidence and boundary-edge color data. Each used vertex has one contiguous sector or a full interior star. A/B boundary fan sizes are 1,...,7 in pi/4 units; C sizes are 1,2,3 in pi/2 units. Full stars contribute 8,8,4 incident triangles respectively. Smooth A/B size 4 and smooth C size 2 do not count as walls. Interior or smooth B/C points count as transparent exceptions.

The model enforces each color of vertex having exactly N triangle incidences, Euler for a disk, boundary-stub matching at both ends of each AB/AC/BC edge, and N minus each boundary-edge count being a nonnegative even integer. It also imposes the established identities W=2+6I+Q-2J-s_N, N=8I+Q+s_A, 3s_A<=Q, R=4(N-W+2), N>=W+6, and the existing external-full-neighbor bounds. At I<=4 it uses the exact audited boundary minima 6,7,8; at larger I it uses only the weaker universal minimum 4. This remains a necessary superset of embedded rooms.

The independent dynamic program imports neither OR-Tools nor geometry helpers. It builds all possible nonsmooth acute fan inventories by exact integer-angle recurrence, tracks boundary stub counts as bitsets, enumerates the B/C split of interior and smooth exceptions, and solves the three boundary-edge balance conditions algebraically. It verifies both positive and negative cells. Every extracted CP-SAT positive witness is also checked by direct integer equalities.

Two physical controls pass: the saved k=3 simple room (I=2,J=2,s_N=1,Q=13,N=29,W=22) and a 4-by-6 rectangle (I=2,J=13,s_N=10,Q=26,N=48,W=4). Each control is classified using both independent fan-angle helpers and accepted with its inventory fixed. An initial diagnostic run accidentally omitted full-star rows and is invalid; it was replaced before posting any exclusions. The final source asserts that every vertex type includes its full-star row. Historical diagnostic lines remain in run.log; table.json and dp-audit.json identify the final checked run.

## Why geometry alone cannot bound k

For a canonical rectangle [0,2a] by [0,2b] with a,b>=2 and (a-1)(b-1)>=2, exact counts give

    I=(a-1)(b-1), J=3ab-a-b, s_N=2a+2b,
    k=3ab+a+b, Q=6a+6b-4, N=8ab, W=4.

Thus simple eligible geometry with two interior A points has unbounded exceptions. Convexity supplies a direct segment between the marked points, so these examples are illuminated without any ray search. Claude part A must be a darkness-specific theorem, not a wall-budget-only bound.

## k=4 geometric reduction

The connected A-cell graph and fan-degree lemma extend as

    Q >= 2P-2I-2+m, E+m<=2k,
    P+m <= floor((23-4I+2k)/2),

where P is the number of partial A cells and m counts absent external neighbors of full cells. For I=2,k=4 this gives P+m<=11. The established connecting-path argument gives marked-cell Manhattan distance <=6. Nonadjacent normalized placements give 14 complete supports.

For I=3,k=4 it gives P+m<=9, hence at most 9 external full-cell neighbors. If the full cells have disconnected distance-two overlap components, they require at least 4+6=10 external neighbors. Therefore they form an overlap-connected triple and lie within distance four of a full root. All 138 rooted patterns reduce under grid isometries to eight shapes with at most nine external neighbors. Every other occupied cell lies within distance 9-b of the full cells and their required external neighborhood. branch-support.json lists the complete supports and nonadjacent mark pairs. Adjacent marks are omitted by the direct-segment theorem.

geometry_model.py is an owned copy of the frozen three-exception builder. It permits arbitrary nonnegative budgets and caches translated local tables. Frozen originals and Claude files are unchanged. The first pass adds the k=4 inventory table as a redundant filter and checks room witnesses independently. Its four unresolved geometric supports were subsequently closed by complete fixed-cell partitions. The historical UNKNOWN results remain inconclusive; geometry-summary.json composes the later receipts. A feasible support establishes geometry only; it is not an unlit candidate.

## Complete k=4 geometric support classification

The composite receipt is geometry-summary.json: all 22 supports are classified, with 10 geometry-feasible and 12 geometry-infeasible. It rechecks 48 physical positive rooms, 225 complete fixed-outside-cell negative leaves, and the 66 fixed-tuple three-star queries. These geometric negatives still need Claude’s independent model/coverage review. They are not formal UNSAT certificates.

| I | Full-cell placement or shape | Geometry | Evidence |
| --- | --- | --- | --- |
| 2 | I2_1_1: [[0, 0], [1, 1]] | GEOMETRY_FEASIBLE | checked witness (J,s_N,Q,N,W)=(2,2,15,32,23) |
| 2 | I2_2_0: [[0, 0], [2, 0]] | GEOMETRY_FEASIBLE | checked witness (J,s_N,Q,N,W)=(0,4,8,25,18) |
| 2 | I2_2_1: [[0, 0], [2, 1]] | GEOMETRY_FEASIBLE | checked witness (J,s_N,Q,N,W)=(0,4,7,23,17) |
| 2 | I2_3_0: [[0, 0], [3, 0]] | GEOMETRY_FEASIBLE | checked witness (J,s_N,Q,N,W)=(1,3,14,32,23) |
| 2 | I2_2_2: [[0, 0], [2, 2]] | GEOMETRY_FEASIBLE | checked witness (J,s_N,Q,N,W)=(0,4,13,30,23) |
| 2 | I2_3_1: [[0, 0], [3, 1]] | GEOMETRY_FEASIBLE | checked witness (J,s_N,Q,N,W)=(0,4,13,30,23) |
| 2 | I2_4_0: [[0, 0], [4, 0]] | GEOMETRY_INFEASIBLE | complete fixed-outside-cell partition, 171 complete cases |
| 2 | I2_3_2: [[0, 0], [3, 2]] | GEOMETRY_FEASIBLE | checked witness (J,s_N,Q,N,W)=(0,4,13,30,23) |
| 2 | I2_4_1: [[0, 0], [4, 1]] | GEOMETRY_INFEASIBLE | complete fixed-outside-cell partition, 49 complete cases |
| 2 | I2_5_0: [[0, 0], [5, 0]] | GEOMETRY_INFEASIBLE | cell-path wall bound, W≥24 |
| 2 | I2_3_3: [[0, 0], [3, 3]] | GEOMETRY_INFEASIBLE | complete fixed-outside-cell partition, 2 complete cases |
| 2 | I2_4_2: [[0, 0], [4, 2]] | GEOMETRY_INFEASIBLE | complete fixed-outside-cell partition, 3 complete cases |
| 2 | I2_5_1: [[0, 0], [5, 1]] | GEOMETRY_INFEASIBLE | cell-path wall bound, W≥25 |
| 2 | I2_6_0: [[0, 0], [6, 0]] | GEOMETRY_INFEASIBLE | cell-path wall bound, W≥27 |
| 3 | I3_0: [[-3, -1], [-2, 0], [0, 0]] | GEOMETRY_INFEASIBLE | whole-support first-pass model |
| 3 | I3_1: [[-3, 0], [-2, 0], [0, 0]] | GEOMETRY_INFEASIBLE | whole-support first-pass model |
| 3 | I3_2: [[-2, -2], [-1, -1], [0, 0]] | GEOMETRY_INFEASIBLE | whole-support first-pass model |
| 3 | I3_3: [[-2, -1], [-2, 0], [0, 0]] | GEOMETRY_INFEASIBLE | whole-support first-pass model |
| 3 | I3_4: [[-2, -1], [-1, -1], [0, 0]] | GEOMETRY_FEASIBLE | checked witness (J,s_N,Q,N,W)=(2,2,9,33,23) |
| 3 | I3_5: [[-2, 0], [-1, -1], [0, 0]] | GEOMETRY_INFEASIBLE | whole-support first-pass model |
| 3 | I3_6: [[-2, 0], [-1, 0], [0, 0]] | GEOMETRY_FEASIBLE | checked witness (J,s_N,Q,N,W)=(4,0,11,35,23) |
| 3 | I3_7: [[-1, -1], [-1, 0], [0, 0]] | GEOMETRY_FEASIBLE | checked witness (J,s_N,Q,N,W)=(3,1,10,34,23) |

For I=2, the three direct cell-path bounds exclude (5,0),(5,1),(6,0). Complete partitions of size 2,3,49,171 exclude (3,3),(4,2),(4,1),(4,0). The seven surviving placements are (1,1),(2,0),(2,1),(3,0),(2,2),(3,1),(3,2).

For I=3, only shapes I3_4, I3_6, I3_7 are geometrically eligible. The collinear I3_6 chain is directly illuminated: the three full square cells form the rectangle [-5,1] by [-1,1], and the only nonadjacent marked pair (-4,0),(0,0) lies on an interior segment of that rectangle. This is a direct convexity proof, not a trajectory search. Two three-star shapes remain, with two and one nonadjacent marked-pair cases respectively. Altogether nine potential-dark shape families / ten marked-family cases remain at exactly k=4. No darkness conclusion is drawn for them.

### Three-star tuple projection

All 22 locally eligible I=3,k=4 tuples were queried on each of the three geometrically eligible shapes. There are no UNKNOWN queries. Shapes I3_4/I3_6/I3_7 admit 8/13/17 tuples respectively; the union admits 19 of the 22 local-inventory tuples. Every positive query includes a checked physical room in three-star-cells.json. Five excluded full-star shapes contribute no tuples. The complete two-star tuple-to-embedding projection is not performed; table.json gives its local-inventory relaxation plus seven geometric sample witnesses.

### Complete outside-cell coverage argument

Every true occupied-cell graph supplies a simple full-to-full cell path. Its partial cell charges imply Q+m>=b+path_cost, with each visited partial cell costing at least 2 (3 for a straight passage), minus one when it is already a required external neighbor. At k=4,I=2, Q+m<=17. Thus every true path is among those enumerated under the positive charge cap 17-b. Its outside-cell set S uses at most three cells. Every actual outside set T contains one such S. Adding all required neighbors to the real connected cell graph preserves connectedness, because each added neighbor is adjacent to a full cell. Hence required∪T is connected and T can be grown from S by adding neighboring cells until at most three outside cells are used. geometry-partitions.py enumerates precisely these possible connected extensions, fixes every chosen outside cell occupied, and solves the unchanged local-fan/Euler/connectivity model on required∪T. Each reported geometric exclusion has every such case INFEASIBLE. A failed compact path support alone was never used as an exclusion.

The positive-only compact-support attempt and the broad flow refinement did not settle the four hard supports. They are historical diagnostics. The complete fixed-cell partition is the successful receipt used in the final composition.

## Previously requested final-case verification

The (2,0) and (1,1) independent checks were completed before this turn. Fresh reconciliation confirms the final own-model PASS receipts: 699/2,530 raw cases, 190/657 complete symmetry groups, and 5,710/4,671 checked guards, respectively. Every final group is INFEASIBLE and physical positive controls were accepted. All 328 frozen input hashes still match. See peer-verification-receipts.json and ../three-triples/three-exception-complete.md. This turn reread and hash-checked the saved receipts; it did not repeat ray discovery or claim a new path audit.

## Reproduce

    .context/illumination-venv/bin/python -B .context/illumination-k4-codex/local-inventory.py --max-k 12
    python3 -B .context/illumination-k4-codex/inventory-dp-audit.py
    .context/illumination-venv/bin/python -B .context/illumination-k4-codex/branch-support.py
    .context/illumination-venv/bin/python -B .context/illumination-k4-codex/geometry-first-pass.py

Run peer reproductions in a separate copy preserving the .context layout. Reruns write only the Codex-owned result paths. No ray/orbit code is invoked.

**Next move:** independently review the geometric negatives and define the primitive normalization for part A; use the nine k=4 surviving shape families as concrete theory targets.
