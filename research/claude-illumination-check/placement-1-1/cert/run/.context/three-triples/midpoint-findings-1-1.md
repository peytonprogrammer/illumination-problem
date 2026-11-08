# Placement (1,1): exact midpoint paths and two hub families

[done] The three saved multi-event rooms all have alternative one-exception midpoint paths (16,103,4 direction tests). All37 original sample rooms now have verified one-pass witnesses.

A bounded full-parent run examines110 further configurations. Fresh audit PASS: all448 added sufficient one-pass conditions, independent triangle coverage, three fixed positive geometry controls,8 mutations and8 corrupt-guard checks pass. Maximum new path length:19 reflections. The geometry-only midpoint catalogue has588 unique patterns; its parent remains feasible. The composed full parent also remains feasible. No new placement exclusion or universal one-pass theorem.

The initial search loaded2,001 original audited cuts but omitted a later626-cut extension in `connected-search-1-1.json`. This was corrected before the hub replays. Of448 phase conditions,112 already occur in that extension, leaving336 globally new conditions. Fresh exact ray and independent coverage checks validate all514 restored conditions missing from the initial phase parent. The merged parent has2,963 unique guards and the previously audited necessary2,530-set connected-cell table. The initial110 configurations contain96 genuinely new geometries and14 revisits against every matching room in the earlier179-input certificate. Globally cumulative three-triples totals:3,163 new geometries /7,044 new guards.

[done] Exhaustive local hub reduction: the two full marked A stars, centered at physical(0,0),(2,2), meet at physical B vertex(1,1). They force four of its eight incident triangle bits. Independent cycle-connectivity and sector calculations agree that exactly seven local masks remain:175,191,239,243,247,251,255, using saved triangle ordering.

The full mask255 admits the direct zero-reflection ray in direction(1,1). A fixed positive full-hub geometry passes; its sufficient ray conditions require only triangles already forced by the two marked stars and full hub. Thus every completion of that mask is illuminated. The existing cuts already contain this condition; no extra guard was needed.

The remaining six masks form exactly two orbits under the source/target symmetry group:

- Two six-triangle masks:175,243.
- Four seven-triangle masks:191,239,247,251.

Every one of these six fixed-mask composed models freshly replays feasible. This is a complete necessary partition of the still-open(1,1) placement; it does not show that any room is dark or that only six room outlines remain.

Scope: simple canonical congruent45–45–90 tile rooms with at most23 walls, exactly two full A stars, exactly three B/C exceptions, distinct physical marks(0,0),(2,2). Whole-placement count remains8/10; only placements(1,1),(2,0) are open. No smaller dark construction, general-polygon bound or formal UNSAT proof.

[waiting on Claude] Independently check alternative paths, sufficient conditions, historical reconciliation and hub classification. Copy all manifest inputs retaining `<root>/.context/...`; run `audit_illumination_midpoint_1_1.py`, then `analyze_illumination_hub_1_1.py` with Python -B. Receipts belong in the copy. Source findings for the earlier(2,1) phases remain immutable.

[done] Peer update: Claude independently confirms the earlier(2,1) midpoint extension: all2,598 patterns and four new geometry-only cores; composed exclusions of types4,11. His newer type8/type6/mask12 checks are still pending.

**Next move:** target the seven-triangle hub family first, using the merged2,963-guard parent. It fixes more local geometry than the six-triangle family; a bounded exact-path cover should be tested before expanding the direction catalogue.
