# D205 · exact area 21, W ≤ 20, all interior lattice pairs

The unit of enumeration is a strictly simple orthogonal lattice room modulo translation and the eight square-lattice symmetries. The unit of illumination is an unordered pair of distinct interior lattice points within that representative. Pair counts retain symmetries within a representative. No axis rescaling or parity-class exclusion is used.

## Implementation

The Redelmeier ordering, split depth 11 and dihedral key order come from d9. The copied enumerator maintains the d9 vertex masks on cell insertion and removal. A new square contributes +1 face, four minus the number of shared sides new edges, and one new vertex per previously empty vertex mask. Hence the Euler characteristic increment is new vertices − 3 + shared sides. For a connected nonpinched cell union, characteristic one is the no-hole test. Corner-mask, pinch-mask and full-mask changes update the number of maximal walls, pinches and marks. Only the final shape is filtered. The canonical key orders width, height and normalized row masks. For width less than height, swapping axes is lexicographically worse; for a square box the transposed candidates are explicitly checked. All integer masks fit for the authorized limit. Rooms with fewer than two marks are counted and require no shooting.

For an eligible room, the enumerator calls the shooter in process. The shooter reconstructs interior marks independently by intersecting adjacent row masks and adjacent columns. It checks its number of marks against the producer. D9's four-sheet direction traversal supplies hits, with the original independent plane replay performed immediately on every hit. A failed replay aborts a shard. Only survivors need per-pair disk storage. The independent producer count Σ binomial(number of marks,2) must match the two parity subtotals for each wall bucket of every shard.

The supervisor launches at most seven fused workers at nice 10. It reaps a worker before starting any survivor subprocess. It saves each surviving pair and the normalized cells as orbitc input; a DARK decision requires full orbit exhaustion and independent reproduction using orbit.py. A cap, crash or mismatch does not count as dark. The area-21 manifest fingerprints the worker and sources. Each atomic completion record includes CPU seconds, peak RSS (bytes on Darwin), pair and room totals, and the counts-file checksum. In-memory LIT witnesses can be reproduced from the shard and source fingerprints. The two orbit implementations and plane verifier are unmodified copies from d9.

## Validation and outputs

- [validation/PASS.json](validation/PASS.json) records exact area-20 counts, the through-area-11 Part A table comparison and the separate W=22 control. The area-20 run counted candidate pairs combinatorially without testing their illumination.
- [a21/manifest.json](a21/manifest.json) defines the 84 production shards. Each shard has a counts file, a survivor file and a completion JSON. [a21/batch.log](a21/batch.log) records completion order.
- report.py reconciles the sealed records before producing a21/totals.json. The forecast uses measured CPU at exact areas 20 (counts) and 21 (counts and shots), with fixed-node and pair-count growth as separate predictors. Area 22 is forecast only.
