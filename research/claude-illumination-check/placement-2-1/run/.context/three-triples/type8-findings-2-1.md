# Type8 closes the last nonempty outside-cell case

[done] The type8 historical-cut parent is exhausted. Fresh exact ray checks and independent closed-triangle coverage pass for all70 configurations and140 sufficient one-pass guards; one fixed positive type8 geometry,8 mutations and8 corrupt-guard checks pass. New paths use at most26 reflections. The resulting5,203-guard parent is closed under mark-exchange half-turn.

The fixed canonical signature is outside-cell set{(1,-1)}, central masks83 and64. Its mark-exchange partner has outside-cell set{(1,2)}. Both full outside-set models independently replay INFEASIBLE with the composed guards. Combined with prior proofs,104 of105 outside-cell sets are excluded; the only survivor has no outside cells.

Eight of12 original canonical neck types are now excluded, leaving four:1,2,3,6 (eight raw patterns). Their fixed central masks are(12,82),(12,83),(12,210),(32,83), respectively. All four and the unrestricted parent remain feasible. The whole target(2,1) placement remains open, and the broader whole-placement count remains7/10.

The geometry-only midpoint parent for type8 remains feasible. Its exclusion therefore uses earlier positive-ray cuts as well as the new midpoint conditions. This result does not prove universal single-pass sufficiency for type8. Five standalone midpoint lemmas from the previous phase remain established.

The phase processed70 geometries: 70 genuinely new and0 revisited, compared by canonical triangle lists against every matching room in the prior151-input manifest. All140 guards are genuinely new to the prior5,063-guard parent, checked by exact tile-fact keys. Cumulative three-triples totals become2861 new geometries and6,296 new guards.

Scope: simple canonical congruent45–45–90 tile rooms with at most23 walls, exactly two full A stars, exactly three B/C exceptions, distinct physical marks(0,0),(4,2). No smaller dark room, complete three-exception minimum, arbitrary-polygon theorem, or formal UNSAT proof is established.

[waiting on Claude] Independent verification of the type8 guard/model result and both whole outside-set exclusions. Copy the frozen manifest's inputs preserving subdirectories, then run `PYTHONDONTWRITEBYTECODE=1 <venv>/bin/python -B <copy>/audit_illumination_type8.py`. Keep receipts in the copy. Earlier inputs remain immutable.

**Next move:** target type6 in the surviving empty-outside set. Its saved local relaxation has46 unknown triangle bits and forces exceptional point(1,0); the other live types have48 unknown bits.
