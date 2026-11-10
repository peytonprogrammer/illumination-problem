# Placement (2,1) excluded by complete partition composition

[done] No smaller dark room exists at physical mark displacement (4,2) in the simple canonical congruent 45–45–90 triangle family with at most23 walls, exactly two full A stars and exactly three B/C exceptions. This is a computer-assisted exclusion conditional on the checked finite geometry reduction, exact path verifiers and CP-SAT branch results. It does not establish the unrestricted illumination problem or export a formal UNSAT proof.

The latest search fixes an empty outside-cell set and first central fan mask12, with the second fan unrestricted. It exhausts after180 configurations and360 new sufficient one-pass ray guards. Fresh path/independent triangle-coverage audit PASS; three fixed geometry controls,8 mutations and8 corrupt-guard checks pass. New rays use at most27 reflections. All12 canonical neck models replay INFEASIBLE under the5,615 unique guards, which are closed under mark-exchange half-turn.

The unrestricted monolithic solve returns UNKNOWN at60 seconds, and the empty-outside solve returns UNKNOWN at10 seconds. These results are not exclusion evidence. Instead `audit_illumination_partition_closure.py` checks the complete certificate hierarchy:

- 105 complete outside-cell sets:100 earlier exclusions and5 refined sets.
- 285 complete first-fan branches:267 earlier exclusions and18 refinements.
- 1,026 complete second-fan branches:1,002 earlier exclusions and24 terminal raw patterns.
- The24 terminal patterns form exactly12 checked half-turn pairs; all12 canonical models have fresh INFEASIBLE replays.

It verifies exact branch-key coverage at every level, independent57-mask catalogues, source hashes/provenance, and inclusion of every earlier stage's guards in the current parent (2,129;2,915;3,207 guards). Therefore earlier exclusions remain valid after adding the new positive-ray conditions. The composed result excludes all105 sets and the full placement. No solver UNKNOWN is treated as INFEASIBLE.

The geometry-only midpoint parent remains feasible (OPTIMAL), so universal single-pass illumination is not proved for these last types. The exclusion requires historical ray cuts and conditional midpoint covers together.

Geometry coverage: 180 new geometries and0 revisits against every matching room in the prior168-path manifest. All360 guards are new against the5,255-guard parent. Cumulative three-triples totals: 3067 new geometries /6,708 new guards.

Eight of ten normalized placements are now excluded. Remaining placements: (1,1),(2,0), with physical mark displacements (2,2),(4,0). The24-wall minimum with at most two B/C exceptions remains established; the full three-exception extension remains open. No smaller dark construction has been found.

[waiting on Claude] Independent review of new rays, branch replays and exhaustive composition. Copy the frozen manifest preserving subdirectories; run `audit_illumination_mask12.py`, then `audit_illumination_partition_closure.py` with Python -B. Write receipts in the copy. The first script's monolithic solver status may vary with timing; the composition certificate is the exclusion argument.

**Next move:** compare saved paths in the two remaining placements to choose which admits the strongest midpoint/gate reduction.
