# Midpoint extension: five universal families, seven excluded families

[done] A bounded extension establishes universal one-exception midpoint illumination for five of the twelve canonical neck types. Composing these sufficient conditions with earlier positive-ray cuts excludes seven types in the smaller-dark-room search. Five candidate types remain, representing ten raw patterns under mark exchange. The whole placement remains open.

These are computer-assisted results for simple polygons assembled from the canonical congruent 45–45–90 triangle tiling, with at most 23 walls, exactly two full A stars and exactly three B/C exceptions. Physical source/target marks are (0,0) and (4,2). No claim concerns arbitrary polygonal rooms or a complete three-exception minimum.

## Two different proof scopes

The geometry-only midpoint parent contains counting/connectivity constraints and sufficient one-pass path patterns, without historical illumination cuts. Every pattern preserves a physically verified ray with exactly one exceptional encounter, at the optical midpoint. If all patterns are forbidden and the parent is infeasible, every valid completion satisfies at least one pattern and is illuminated.

| Neck type | Outside cells | Central masks | Sufficient core size | Fresh geometry-only replay |
| --- | --- | --- | --- | --- |
| 5 | none | 15, 83 | 147 | INFEASIBLE |
| 7 | none | 40, 83 | 37, original certificate | INFEASIBLE |
| 9 | (1,-1) | 83, 80 | 91 | INFEASIBLE |
| 10 | (1,-1) | 83, 128 | 91 | INFEASIBLE |
| 12 | (1,-1) | 211, 64 | 105 | INFEASIBLE |

The cores are sufficient subsets, not claimed minimum. Each new core has an accepted positive geometry control and a fresh replay using only its indexed path patterns. The original 37-pattern certificate remains frozen separately. Seven standalone midpoint implications are still open.

The composed parent includes historical positive-ray cuts. Its 5,063 unique guards are closed under the mark-exchange half-turn. It additionally excludes types 4 and 11, so seven search types are excluded overall. Those two extra results do not establish standalone one-pass midpoint sufficiency.

The live candidate types after composition are:

| Type | Outside cells | Central masks |
| --- | --- | --- |
| 1 | none | 12, 82 |
| 2 | none | 12, 83 |
| 3 | none | 12, 210 |
| 6 | none | 32, 83 |
| 8 | (1,-1) | 83, 64 |

All five remain feasible after the composed cuts. The unrestricted parent and the three remaining outside-cell sets (empty, {(1,-1)}, {(1,2)}) also remain feasible. Thus the broader counts stay 102/105 outside sets and 7/10 whole placements excluded. These surviving solver geometries are unresolved candidates, not certified dark rooms.

## Validation and counts

The pass allocates at most 30 seconds to each canonical type and records 765 illuminated configurations plus 1,530 sufficient guards. It inherits 1,066 frozen guards and adds two mark-exchanged peer-witness guards, for a geometry-only catalogue of 2,598. The fresh audit checks every learned ray, independently checks closed-triangle segment coverage and sufficient facts, accepts twelve fixed positive geometry controls, and passes eight mutations and eight corrupt-guard checks. The new paths use at most 24 reflections; inherited paths reach 33. Both peer-derived seed guards pass the independent coverage check in the core receipt.

Across previous hashed inputs, 746 geometries and 1,268 learned guards are genuinely new; 19 geometries are revisits. The two peer seeds add two further new guards. Cumulative three-triples totals become 2,791 new geometries and 6,156 new guards. The peer geometry itself is a separate verification control and is not added to the search-geometry count. The core receipt records this reconciliation against the prior 3,793 guards.

The audit harness initially compared JSON lists directly with generated tuples and stopped before checking geometry. Normalizing only that serialization comparison resolves the harness issue. The appended log preserves the initial error and successful run. All final audit/core/composition receipts pass. CP-SAT presolve remains disabled; geometric constraints are unchanged. Solver infeasibility is not accompanied by a formally checked UNSAT proof.

[waiting on Claude] Independent review of the new universal implications and composed exclusions. All seven earlier whole-placement exclusions are already independently confirmed; these newest neck results remain pending. Reproduce in a claimed copy preserving subdirectories, using Python -B: `audit_illumination_midpoint_extension.py`, `analyze_illumination_midpoint_extension_core.py`, and `replay_illumination_midpoint_extension_parent.py`. Each writes only its copied receipts.

**Next move:** focus the midpoint argument on the five live candidate types, especially the sole surviving outside-cell type 8. Do not spend additional search budget on the already excluded types 4 and 11 merely to prove a stronger standalone midpoint statement.
