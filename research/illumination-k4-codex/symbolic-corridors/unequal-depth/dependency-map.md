# Dependency map for the full corridor endpoint theorem

This is a live status map. Frozen proofs and their acceptance receipts remain unchanged. Root paths are relative to symbolic-corridors/ unless otherwise stated.

| Implication | Proof source | Independent status |
|---|---|---|
| Axis scaling and the common-core horizontal reduction | prior accepted arbitrary-endpoint/common-core packets | Accepted |
| Equal original depths, arbitrary horizontal endpoints | equal-depth/ frozen proof plus equal-depth-independent/ | Accepted; q4 portal prose correction is in the supplemental erratum |
| Any strict cap chart transfers to actual S,T, including cap corners | unequal-depth/cap-corner-removal and outer-leg-transfer packets | Accepted |
| Any effective-depth equality closes a room | unequal-depth/outer-leg-transfer.md | Accepted |
| Outside ten lines plus eleven points, every endpoint pair has a one-pass chart | unequal-depth/finite-support-theorem.md WITH finite-support-irrational-clarification.md; lattice/margin/finite certificates | Accepted in unequal-depth-independent/finite-support-audit/ |
| Four critical-line corners have only90affine families and288isolated points | unequal-depth/critical-rectangles.py/json | Accepted in unequal-depth-independent/critical-rectangles-acceptance.json |
| Three-pass strict phase inequalities give an actual outer-simple path | unequal-depth/three-pass-circle.md/py/json | Accepted in unequal-depth-independent/three-pass-acceptance.json |
| Every nonequality affine family has a full closed-square joint circle margin | unequal-depth/family-joint-margin.md/py/json | Accepted in unequal-depth-independent/family-joint-margin-acceptance.json |
| Circle margin guarantees finite rational orbit hit above explicit Q<=64 | unequal-depth/family-joint-margin.md, using accepted component-spacing lemma | Accepted in unequal-depth-independent/family-joint-margin-acceptance.json |
| All remaining rational family members and exceptional-point rectangles are in finite list | unequal-depth/residual-rooms.md/py/json | Accepted in unequal-depth-independent/residual-rooms-acceptance.json |
| Every room on that list has a continuous endpoint cover by strict physical charts | unequal-depth/residual-optical-proof.md/py/json | Accepted in unequal-depth-independent/residual-optical-audit/acceptance.json; parent replay also passes |
| Full quantified conclusion | unequal-depth/full-join.md | FINAL INDEPENDENT ACCEPT in ../unequal-depth-independent/whole-result-acceptance.json |

Independent receipts pin local artifact hashes relative to their own directory. The finite-support receipt's source_roots metadata describes nested effort peer-input hashes; see its receipt-root-clarification.md. There is no missing parent effort.json dependency.

The old rational shear sufficient criteria are accepted auxiliary results. The finite-support/rectangle/joint-margin proof route can close the theorem without assuming those criteria exhaust the rational residual. The original generic reduction is not silently upgraded by these auxiliary acceptances.

All listed proof implications now have explicit independent acceptance. See completion.md for the final statement and review boundaries.
