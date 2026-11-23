# Joint band clearance at W = 10

Every row below concerns a full turn word, up to cyclic shift and reversal. The input is the saved d15 order-type certificate, which includes coincident wall levels. Reclassifying its outstanding entries by localized flush-door and wide-middle slab proofs in both orientations removes zero entries. This is an exact overlap with d15's existing coverage. The additional joint test below treats more general band sequences. Its applicability depends on the actual lengths and marks.

## A simultaneous test allowing unbounded side reflections

Fix a chain of full rectangular runs traversed monotonically along an axis between two marks. Their positive longitudinal travels are dᵢ; the transverse intervals are (lᵢ,lᵢ+uᵢ). Consecutive runs must overlap openly. Use all original lateral walls, and require interior crossings of intermediate apertures. Marks on a joint can start or finish in an incident run if the mark is physically interior. A zero-travel band is omitted. Set αᵢ=dᵢ/(2uᵢ).

**If the αᵢ are linearly independent over the rationals, every pair of transverse endpoint positions in the open runs is lit.** This holds for arbitrary positive real wall lengths, and needs no spanning hall. More precisely the following is an exact test for a monotone shot through open apertures, including when the αᵢ satisfy integer relations.

On the unit torus with one phase per run, take the subgroup H defined by m·z=0 modulo 1 for every integer vector m with m·α=0. For a candidate z, propagate a signed transverse state from the prescribed source. Start on the positive sheet, allow a signed real slope, and use the current physical coordinate and direction sign to choose its unfolded representative in each run. Advance by 2uᵢzᵢ modulo 2uᵢ, fold into the run and retain its outgoing sheet. Require all seam positions to be strictly in the physical overlaps and the last folded coordinate to equal the target. The test is whether some z in H satisfies these conditions.

**Proof.** A real slope s gives z=sα modulo 1, so necessity follows. For sufficiency, by the continuous Kronecker theorem that line is dense in H. Near an admissible z, all seam coordinates are interior to both runs and the terminal mark is interior, so choose a small neighborhood with all folding branches fixed. On these branches the exit coordinates are continuous. Starting at a sufficiently close actual phase sα, the terminal error can be made arbitrarily small. Varying the slope by t in this neighborhood moves the terminal physical coordinate by ±(Σdᵢ)t: in the developed frame it adds precisely that transverse displacement, followed by the fixed terminal sheet sign. Thus one can correct the error exactly without leaving the neighborhood. If H is the whole torus, choose seam points strictly inside the apertures and the prescribed target; select each successive phase to send the current position there on the positive sheet. This proves the independent case. The proof applies for any number of bands. It avoids the invalid step of joining two independently aimed shots. Smooth side contacts at seam endpoints can give additional paths outside this open-aperture test.

For specified real parameters this describes the exceptional set for this construction: all admissible chains in both orientations miss their endpoint windows on H (or there is no chain). For a single selected chain one may check H against finitely many linear cells: represent phases in [0,1], enumerate only the two sheet signs and the finitely many wraps within one phase period per step, and impose a basis of the integer relations. This is a mathematical criterion; identifying exact relations for unspecified real inputs is a separate issue. In particular the complement of the independent case is a countable union of resonance equations Σmᵢdᵢ/uᵢ=0. Membership in that union alone does not certify a failure. Area, a sample of lengths, or multiplying two adjacent-door clearance rates cannot close this gap.

## Per-word residuals

The table specifies an explicit unit-gap realization and a marked pair in the saved d15 residual for each word. Grid rows are listed from top to bottom, with # denoting an occupied unit cell; the origin is the lower left of the grid. Mark coordinates in the final column are doubled, so an odd index is halfway across its cell. For arbitrary lengths replace consecutive coordinate lines by increasing real coordinates independently on each axis. An odd index then ranges over the entire intervening open interval, an even one lies on the line. Together with the other masks and pairs returned by wall-slab.py this is an exact parameterization of the residual of the audited d15/slab certificates. The examples are not claimed to fail all monotone shots. Every example has rational α for any multi-run chain, so bare rational independence cannot certify it.

| Word | Order types | Outstanding placement types | Unit-gap room | Doubled marks |
|---|---:|---:|---|---|
| LLLLLRLRLR | 1 | 1 | `#.../##../###./####` | (1, 7), (7, 1) |
| LLLLRLLRLR | 5 | 7 | `#../##./###/#..` | (1, 7), (5, 3) |
| LLLRLLRLLR | 12 | 21 | `#../###/.#.` | (1, 3), (3, 1) |
| LLLLLLRLRR | 5 | 33 | `##./#../##./###` | (1, 7), (5, 1) |
| LLLRLLLRLR | 8 | 52 | `#../##./.##` | (1, 3), (3, 1) |
| LLLLLRLLRR | 11 | 67 | `#./##/#./##` | (1, 1), (3, 5) |
| LLLLLLLRRR | 5 | 99 | `##./#../#.#/###` | (1, 7), (5, 1) |
| LLLLRLLLRR | 23 | 298 | `#./##/.#/##` | (1, 1), (1, 5) |

**Ferrers is the closest whole word.** Only mask 4991 and its opposite terminal placement remain after d15. In the southwest-oriented staircase let V₁,V₂,V₃ be the three reflexes from upper left to lower right. D17's perpendicular-window lemma covers V₂ on or above the chord V₁V₃. Thus the remaining *shape* region for this comparison is V₂ strictly below the chord, and the remaining *marks* must be in the two terminal cells. For the joint construction also to fail, both horizontal and vertical travel vectors must satisfy a nonzero integer relation, since this staircase has a monotone chain in each orientation. The two relations are necessary conditions for a dark pair. D17's named grid x=(0,3,4,9,12), y=(0,3,5,9,12) with S=(1,10), T=(10,1) lies in this residual of the chord and independence tests. Its saved lighting direction is (−1,1). What is missing is a proof across the entire doubly resonant below-chord region, even for this one word. [D17 proof and example](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d17-r3/r3.md)

[Checker](wall-slab.py) · [Saved certificates and proofs](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d15-small-r/theorems.md)

## Ledger words moved and smallest word still OPEN

No new COVERED word. A smallest ten-wall word still OPEN is LLLRLLLRLR, represented by (2,0), (4,0), (4,1), (3,1), (3,4), (0,4), (0,3), (1,3), (1,2), (2,2). The live ledger controls PARTIAL status.
