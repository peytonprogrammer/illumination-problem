# Soundness of the independent bounded CNF encoding

[done] Encoding argument. A complete exclusion additionally requires verified contradictions for every support/marked-pair case; consult `summary.json` and per-case receipts for actual completion.

## Direction needed for exclusion

Only the following implication is needed: any eligible dark room in a support induces a satisfying assignment of its CNF. Some encodings conservatively allow extra disconnected or multiply-connected objects; that cannot invalidate UNSAT as an exclusion. Terminal geometry checks and connectivity cuts refine that relaxation without assuming illumination.

The 22-support reduction and all 31 marked pairs are established in `support-proof.md`, reconstructed in `support-check.py`. Adjacent marked cells are directly illuminated. The fixed full-A cases cover I=2 and I=3; I>=4 is excluded by W>=6+6I-2k at W<=21,k<=4.

## Local variables

Each available triangle has one Boolean x. Each lattice vertex has a corner Boolean w and three angle bits, encoding its interior angle in units of pi/4 when it is a genuine corner, and zero otherwise. B/C vertices have an exception Boolean e. Each A vertex has an occupied-cell Boolean u. The chosen I full A stars are forced selected; no other A point may have a full fan.

The final reproducibly regenerated CNFs use selector/support clauses for legal fan rows, together with redundant propagation consequences. In this encoding, at least one legal row is selected; it forces all triangle bits and outputs. A real room selects its own unique row. Conversely any selected row witnesses a legal fan. Additional support clauses express each channel literal as supported by its compatible rows and preserve that assignment.

For a room, all tile bits are its physical occupancy, w marks its genuine corners, e marks its full or smooth B/C points, and angle bits record the actual local sector size. The 528 local masks were independently verified previously; exhaustive 58-fan/256-flag checks separately validate the charge argument. No peer executable is imported by this encoder.

The redundant clauses also hold for every legal row: nonzero corner-angle bits imply w; w implies a nonzero angle and occupation; e and w are disjoint; every occupied B/C point is either an exception or a corner. At C, a corner's pi/4-unit angle is 2 or 6, so angle bit zero is false and bit one equals w.

## Global bounds and topology

Cardinality circuits enforce N<=36, W<=21, and sum(e)<=4. This is an **at-most-four** model. It contains k=0,1,2,3 as well as k=4; no earlier minimum-24 claim is assumed.

For every polygonal disk, the total exterior turning in pi/4 units is eight:

    sum_v (4*w_v - angle_units_v) = 8.

The pseudo-Boolean equality uses positive weighted corner literals and complemented angle bits; the constant is increased by the sum of the complemented weights. A real simple room satisfies it. This equation by itself is not a replacement for local manifold conditions or connectivity; those conditions are justified separately. Earlier formulas are archived history; their exact generating source was not preserved, so they are excluded from the final evidence chain.

The connected-cell bound gives P+m<=floor((W-4I+2k)/2). Therefore the number of occupied A cells outside R (full cells and their neighbors) is at most that cap minus |R-F|. This supplies a cardinality bound, a finite support radius, and the total occupied-cell bound I+cap. The initial models used the conservative W23 domains; later models materialize the tighter W21 domains. Both contain every eligible W21 room.

Occupied A-cell connectivity is encoded by reachability from one forced full cell to depth I+cap-1. A real connected room's occupied cell graph has at most I+cap vertices. Assign a reachability bit true when that cell's graph distance from the root is at most the layer number. This satisfies the predecessor and occupation clauses and every occupied cell reaches the final layer.

All 31 final regenerated cases encode exact triangle connectivity. All eight triangles of one forced full A star are initial roots. A layer bit implies that its triangle is selected and that some copy of itself or an edge-neighbor was reachable at the preceding layer. Layer zero is true exactly on the root star, and every selected triangle must be reachable at the last layer. Depth NMAX-8 suffices by the source-star collapse argument. A valid connected room assigns these bits using actual dual distances, so the encoding is necessary. Conversely the layer predecessors connect every selected triangle to the root star through selected triangles. Every final formula is byte-identical to regeneration from the frozen reviewed source in `provenance/frozen/`.

Every eligible room consequently extends to satisfying assignments of the standard cardinality/PB circuits. Exhaustive small controls test 2,304 cardinality truth cases and 192 signed-literal weighted equality cases. These controls support the implementation; the arithmetic and Boolean meanings are stated here independently of the tests.

## Static lighting clauses

For a saved certificate (U,Z), a satisfying premise U selected and Z absent forces a valid connecting path, as independently proved and replayed in `../persisted-replay/findings.md`. A dark room must therefore satisfy

    OR_{u in U} NOT x_u  OR  OR_{z in Z} x_z.

The canonical source/target certificate is moved to the case's actual marked pair by a sign/interchange grid isometry and an even-even translation. This preserves the canonical tiling, A marks and Euclidean reflections. If a required-used tile lies outside the support, its premise is impossible and the certificate can be skipped. Required-absent tiles outside the support are already absent and may be removed from the clause. Vacuous guards conflicting with the forced stars become satisfied clauses automatically.

No solver generates new optical witnesses. The path files and their independent replay receipts are fixed inputs.

## Optional connectivity refinement

If a SAT model has a component C not containing a forced marked-star triangle, pick any selected triangle t in C and let boundary(C) be all available triangles sharing an edge with C but outside it. Any connected eligible room selecting t and the forced root must cross this boundary. Hence

    NOT x_t OR OR_{u in boundary(C)} x_u

is valid. A finite component/seed/boundary receipt is stored for every such clause; `verify.py` rebuilds adjacency and validates it. All currently verified cases use zero of these optional cuts, so their proofs do not depend on this refinement.

## Proof layer and trust boundary

The solver emits DRAT on its exact frozen CNF. A separately compiled drat-trim checks the contradiction. Every successful per-case receipt records SHA-256 hashes of formula and proof. A valid nontrivial proof and a SAT/empty-proof negative control test the independent checker.

The exact reviewed source and its full geometric/static-witness inputs are frozen and hashed under `provenance/`. Codex regenerated all 31 formulas byte for byte and freshly checked the adopted peer-produced contradictions. DRAT verifies Boolean unsatisfiability; it does not prove this geometric encoding argument or the earlier exact path verifier. Those are explicit mathematical/code-review obligations. The proof is therefore computer-assisted with independently checked Boolean traces, not a fully formalized geometry theorem.

Historical enumerator node/closed-leaf counts depend on branch order and which guards are initially loaded. The new CNF procedure does not claim to reproduce those numbers. Its intended comparison is the same necessary bounded room class and no surviving dark room, supported by new contradiction proofs. This substitutes a stronger exclusion certificate for the requested duplicate historical leaf enumeration.

## Controls and limits

A fixed known dark 22-wall room is admitted at W22/k4. The same fixed room is rejected at W21. A fixed saved lit room is admitted with lighting guards disabled and rejected when guards are restored. Controls are in `controls.json`.

Even complete success at W<=21,k<=4 would establish only the bounded canonical family minimum of 22, attained by the certified room. It would not re-prove k<=3 exclusion at W22/W23, bound arbitrary k, or establish global/published priority.
