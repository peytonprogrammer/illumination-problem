# Fable reconciliation of reviewer findings F1–F10

Fable, 2026-11-08. Responds to `review/general-spiral-completeness-fable-findings.md` (F1–F6) and `review/general-spiral-completeness-fable-return-findings.md` (F7–F10). Revision 2 of files 01, 02, 03 incorporates these. Revision 1 statements that were false are listed inside each file under "retired" with the finding number, so provenance is kept.

| Finding | Disposition | Where fixed |
| --- | --- | --- |
| F1 ramified start has k prongs | Accepted. Lemma L now requires an unramified starting lift; all applications start at a lift of an interior room point, which is regular. | 01 §2 |
| F2 sheet symmetries are affine, not translations | Accepted. 01 §1 now says so and uses only that they preserve straight segments and the bad set, with direction sign flips. | 01 §1 |
| F3 coverings need not be symmetry quotients; coordinate-mod-lattice cover always exists | Accepted. The claim "quotients exist only with common period structure" is retired. Proposition 2 (03 §2) analyses the mod-Λ covers for every admissible Λ and proves they are vacuous for rooms with corners in all three parity classes. | 03 top, 03 §2 |
| F4 transposition does not fix the ordered chart | Accepted. 02 §3 now lists the three simple charts of the turn type and states that transposition exchanges (a<l,b<c) with (l<a,c<b) and fixes (a<l,c<b). | 02 §3 |
| F5 cone points can merge or map to regular points | Accepted. The sentence in 02 §4 is retired. 03 §1 classifies fold maps (equivariant coverings) by room angles only; 03 §4 uses the reviewer's genus/cone count for general coverings and states the degree-3 genus-2 case as a per-room block-system test, with the factorization claim flagged for citation. | 02 §4, 03 §1, §4 |
| F6 orbifold is a different category | Accepted. The de Winter–Tokarsky instance now uses the torus R²/(2Z)² with four marked points, a translation surface, and the mod-(2Z)² translation covering. Self-darkness of [0,0] is proved by the midpoint argument on the torus. | 01 §5 |
| F7 Lemma C necessity unproved; perturbation invalid; finite segment need not extend to a clean leaf | Accepted. Lemma C is retired as an equivalence. Rationality of a native path's direction is taken from the integer displacement, as the reviewer states. Replaced by Lemma M (03 §3), which keeps the chosen target lift and makes no leaf or cylinder claim. | 03 top, 03 §3 |
| F8 cylinder quantifiers and the "≤ 6" bound | Accepted. Lemma G is withdrawn; no cylinder count is used. | 03 top |
| F9 L-rooms are covered; degree 2 impossible | Accepted. Proposition 1 now proves deg = 3 only and records that L-fold subfamilies inherit accepted L-room paths up to the unproved sheet-selection step. | 03 §1 |
| F10 keep classification conditional; distinguish torus mark sets | Accepted. Proposition 1 is stated for fold maps (equivariant coverings) only. Non-equivariant coverings are handled by the F5 count plus the block-system test. One-mark and four-mark tori are both covered by Proposition 2. | 03 §1, §2, §4 |

Net mathematical content after corrections:
- Lemma L (unramified start), Corollary R, Theorem E, torus self-darkness, trivial-fold class: proved, translation-surface category only.
- Proposition 1: fold maps of a spiral go to rectangles or, in degree 3 on 4-parameter subfamilies, L-rooms.
- Proposition 2: torus coverings of a spiral unfolding transfer nothing for even-even pairs when corners occupy all three parity classes.
- Lemma M: with the target lift kept, the covering formulation is the vertex walk σ_θ, a partial injection on 4I A-lifts; the orbit of S~ is a chain that reaches T~, ends at a corner, or cycles to S~. The author's return relation inherits this trichotomy.

No nonemptiness result. No new family, search, worker, engine, census, clock, or git action. Full goal open.
