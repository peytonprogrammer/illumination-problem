# Published 34-wall orthogonal room: darkness and local rigidity

[done] Exact geometry and all-direction darkness verified for O'Rourke's public orthogonal Tokarsky figure.

[done] Local rigidity certified by 86 exact one-sided corner events. Independently replayed all 179 events of Opus's separate certificate.

[waiting on Claude] Independent peer review of the smaller 86-event certificate and normalized-slice proof.

## Provenance

The selected figure is Joseph O'Rourke's public Fig9.14, linked from his [book page](https://www.science.smith.edu/~jorourke/AGVT/) as an orthogonal Tokarsky polygon. The cached vector source is `inputs/orourke-orthogonal.pdf`; the earlier exact vector-to-grid reconstruction is frozen in `inputs/novelty-geometry-check.json`. File hashes are in `manifest.json`.

The34 segments form a single degree-two Jordan boundary on the integer grid. We independently traversed this graph, filled exactly the unit cells whose centers lie inside, and rebuilt the canonical triangles. The two marked centers were read against the visible dotted grid: (2,0) and (6,0). In the displayed source these are the dark y mark and illuminated-source x mark respectively; reversing the pair preserves the connection question. The figure's absolute unit, translation and orientation are normalization choices.

This verifies the specific published public figure. We have not recovered an original1995 coordinate table or established that this exact34-wall geometry appears unchanged in Tokarsky's1995 paper. Abel's indexed blog discusses the folded-square obstruction, but its live page could not be retrieved with a valid TLS connection in this check. A fresh fetch of the author-hosted figure also failed locally; the cached vector file and independently checked boundary remain available. Do not convert those gaps into an original-source or priority claim.

## Exact geometry

- 34 maximal straight walls,19 whole unit squares,38 canonical triangles.
- One strictly simple boundary; no slits, holes or point contacts.
- Exactly two interior A points, the two marks.
- Two smooth boundary A points; no transparent B/C vertices.
- 27 occupied non-A lattice vertices independently classified as actual corners.

`reconstruct.py/json/log` and `room.json` contain the full vertices, cells, marks and geometric receipt. The rigidity chart has 40 parameters: two anchor coordinates, 34 positive edge lengths and four mark coordinates. Two closure equations leave dimension 38. The verified event rows have rank 34 on this subspace; their common kernel is exactly the four translation and independent axis-scaling directions.

## Darkness proof

Suppose a positive-length finite billiard path joined the two marks, stopping at every actual corner. Reflect across its encountered horizontal/vertical integer wall lines. The path unfolds to a nonzero straight displacement between even-even integer points: reflections preserve both coordinate parities.

Write the displacement k(p,q) with p,q coprime. At least one of p,q is odd, so k is even and k>=2. The first primitive lattice point on the segment occurs at displacement(p,q), strictly before the endpoint. Folding it back preserves its non-even-even parity. Every occupied lattice point of that parity is an actual corner of this reconstructed room, as independently checked. The proposed path would stop there before reaching the other mark, a contradiction.

This proves darkness for all directions and all finite reflection counts. Rationality is a consequence of the unfolded endpoints; no direction sampling is used.

## Finite certificate and the unfinished larger orbit

`parity-certificate.json` records the six invertible2x2 parity-basis matrices over F2 and the three absorbing nonzero residues. `parity-check.py` checks all six states,12 elementary-generator transitions, both mark parities, and the physical corner premise. Missing blockers, missing basis states and a wrong room digest are rejected by corruption controls. `parity-check.json` is PASS.

The parity quotient identifies the source and target residue. Its proof explicitly requires a nonzero physical unfolded displacement; it is not an assertion that source and target are the same physical point or that a zero-length path is forbidden by a blocker.

An attempted expansion of the full76-square physical shear orbit reached its resource guard after25,015 processed states,50,002 known states and24,987 pending. That run is INCONCLUSIVE and does not support the conclusion. The separate complete parity argument and finite quotient certificate do support it. No partial physical-orbit output is described as a closed certificate.

## Local rigidity theorem

In a sufficiently small neighborhood of this marked room, among strictly simple orthogonal polygons with the same cyclic edge directions, the marked pair remains dark exactly on its positive axis-affine orbit: translations and independent positive horizontal and vertical scalings. Both marks may move in the parameter chart. This is a local statement; no explicit neighborhood radius has been computed.

The certificate has 86 signed one-corner events. `certificate-check.py` reconstructs their fixed reflection words, verifies that each limiting segment meets only one unfolded corner image, checks that the corner is reflex, and recovers all 3,440 derivative coordinates by exact quadratic finite differences. On the closure subspace, the rows have rank 34 and annihilate exactly the four axis-affine symmetry directions. All 86 strictly positive rational coefficients in `positive-span.json` give an exact zero dependence modulo closure. Four corrupted certificates are rejected. This checker uses neither an LP solver nor a direction scan.

For each event, the established one-sided corner lemma gives a signed quadratic determinant f_i, zero at the base room, such that f_i < 0 yields a valid connecting reflection word nearby. All other wall-contact and endpoint conditions are strict at that event, hence persist in some neighborhood. A dark nearby room must therefore satisfy every f_i >= 0.

Normalize a nearby room by translation and positive axis scalings so its first vertex and its first two positive edge lengths equal the base values. The first two edges have different orthogonal directions, so this defines a local slice transverse to the four symmetries. The two closure equations leave this slice dimension 34. Let g_i be the restrictions of the signed derivatives to that slice. Their common kernel is zero, and a strictly positive weighted sum of the g_i is zero. Consequently, for each nonzero slice displacement v, at least one g_i(v) is negative: otherwise positivity of the dependence would force all g_i(v) to vanish.

The continuous function min_i g_i(v) is strictly negative on the compact unit sphere in the slice. It has a uniform negative upper bound -c, for some c > 0. The finite quadratic remainders satisfy |f_i(theta+v)-g_i(v)| <= C ||v||^2. For sufficiently small nonzero v, one event therefore has f_i(theta+v) < 0 and lights the pair. Shrink the neighborhood further to preserve all finite strict contact conditions, positive edge lengths, strict simplicity and interior marks. This excludes every nonzero normalized deformation. Conversely, positive axis-affine maps preserve orthogonal billiard paths and corners, so the certified base darkness persists on that orbit.

## Why the two extra events matter

The initial radius-12 calculation gives 84 events and rank 34, but rank alone does not establish rigidity. `cone-witness.json` supplies an exact non-affine displacement satisfying all 84 linear event inequalities (81 tangent and three strict). This proves that those rows do not positively span; it does not prove the displacement integrates to dark rooms.

A bounded, counterexample-guided extension on this single certified room retained only events that cut off an exact surviving cone vector. Directions (9,-13) and (-15,11), each on side -1, supply the two missing inequalities. The calculation stopped immediately at 86 events and maximum radius 15, after 315 additional side evaluations. The radius ceiling was 24. `adaptive-cone-history.json` and `rigidity-extended.json` preserve the construction history, including numerical infeasibility receipts that were never treated as exact exclusions. Exact rational verification supplies the final positive-span conclusion.

`validate.py` separately checks 86 event-specific descending deformations and 341 additional non-tangent predictions by exact fixed-word replay. All 427 predictions agree; three tangent predictions are skipped. The additional predictions comprise 184 valid connecting words and 157 invalid prescribed words. Invalidity of one word is never evidence of darkness.

## Independent comparison with Opus

The frozen peer room is byte-identical to `room.json`. `peer-replay.py` independently reconstructs all 179 supplied signed events from 175 fixed directions and 350 one-sided limits. The other 171 limits stop at a second corner. It verifies rank 34, the exact four-dimensional axis-affine kernel and all 179 strictly positive dependence coefficients.

The peer chart traverses the same boundary in reverse order. Positive edge coordinates are therefore reversed, and gradients are compared modulo the two closure equations. The checker verifies the closure span and symmetry spans before matching event gradients, corners, directions and unfolded targets. No peer executable source is imported. `peer-replay.json` is PASS.

## Reproduction and scope

Run these fixed-certificate checks from the workspace root:

```sh
.context/illumination-venv/bin/python -B .context/illumination-k4-codex/historical-rigidity34/certificate-check.py
.context/illumination-venv/bin/python -B .context/illumination-k4-codex/historical-rigidity34/validate.py
.context/illumination-venv/bin/python -B .context/illumination-k4-codex/historical-rigidity34/peer-replay.py
```

The construction uses OR-Tools GLOP to propose coefficients; the accepted dependence is reconstructed and verified with exact fractions. The certificate checker itself needs no LP. `rigidity-input-lock.json` hashes the source, dependencies, fixed inputs and receipts. Frozen peer/provenance snapshots retain their original manifest hashes; hashes of revised Codex-owned reports are refreshed.

The independently checked 22-, 24- and 34-wall examples now support the local-rigidity mechanism on three fixed rooms. They do not classify all dark rooms, exclude degeneration limits, establish a global wall minimum, or settle historical novelty. The larger physical orbit remains inconclusive as recorded above.

Next move: peer-review the 86-event certificate, then focus the global argument on uniform control of degeneration limits, in coordination with Opus's separating-pinch work.
