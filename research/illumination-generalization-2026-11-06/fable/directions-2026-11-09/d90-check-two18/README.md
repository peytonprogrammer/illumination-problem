# D90: independent check of `qclass-closure/two18`

**Verdict: CONFIRMED WITH GAPS.** Every leaf of all 144 proof trees holds over its whole box under an independently written exact cylinder model. The trees cover the stated parameter domain, and 240 concrete paths trace correctly. The gaps concern inputs this check doesn't re-derive, not the shear argument.

## Re-run

```
bash run.sh > run.log 2>&1
```

The run takes about 28 CPU-seconds. See [run.log](run.log).

## Files

| File | Role |
|---|---|
| `surface.py` | D90's own square-tiled surface model: four copies, neighbours, marked corners, line criticality by following each closed leaf, cylinders by union-find, half-turn map on cylinder labels. |
| `check.py` | Residual audit, exact leaf replay of `cert00/01/10/11.txt`, and the spot-check tracing. |
| `mutate.py` | Perturbs each witness (`j+1`, `-j`, swapped `(p,q)`) and counts rejections. |
| `run.sh` | Regenerates the census residual into `work/`, then runs both scripts. |

None of the author's `verify.py`, `shear.cpp`, `cyl.py` or `cover.c` logic is imported. The only author code `run.sh` runs is the census step (`localize.py`, `build_pairskip.py`), which produces the residual polygons. Its output is byte-identical to the author's `/tmp/e18.out`.

## Results

| Claim | README | D90 |
|---|---|---|
| Horizontal and transposed periods | (8,16), (8,12) | (8,16), (8,12), from surface row cycles |
| Residual polygon products | 146,308 | 146,308 |
| Tile pairs | 36 | 36, equal to the audit's open-pair lists |
| Maximum coordinate displacement | 1/17 | 1/17, every vertex, exact |
| Proof trees | 144 | 144 = 36 pairs × 2 axes × 2 larger endpoints |
| Illuminated boxes | 853 | 853 (192 + 270 + 195 + 196) |
| Empty boxes (phase inequality) | not stated | 30 |
| Spot checks, residual pairs | none | 200 traced, 0 failures |
| Spot checks, pairs with A ≤ 1/100 | none | 40 traced, 0 failures, K up to 171, paths up to 170,334 cell crossings |
| Mutation test | none | 2,147 of 2,552 perturbed witnesses rejected |

The residual audit also checks three more facts. Every polygon lies in its closed cell. Each designated grid point is a corner of that cell. Each designated point lies on the physical boundary, so A > 0.

The leaf check reconstructs each root box from the README: displacements in [0, 3856/65536] ⊇ [0, 1/17]. The main phase is in [1/8, max(1/4, 3856L/65536)], and the other phase is in [0, same top]. It replays every bisection at the integer midpoint and checks each `E` leaf. For each `W j p q` leaf, it computes the exact range of the transverse coordinate. It then intersects the open and closed cylinder labels over every strip and integer line in that range. It also checks that each tree's closing line `c0 c1 main 1 n` matches its own `W` count.

The spot check walks a random concrete pair to its leaf. It develops the cylinder from the sheared open lift to the sheared closed lift, then pulls the vector back by the shear power jK. It traces the physical path with the D87 tracer (`d87-review-cross-corners/billiard.py`). Each traced path ends exactly at the other endpoint without touching a corner.

## Mathematical review

- **Phase bounds.** This step is correct. K = 1 exactly when LA ≥ 1/8, so t = LA ∈ [1/8, L/17]. If K ≥ 2, then (K−1)·LA < 1/8 ≤ K·LA, so 1/8 ≤ t < 1/8 + LA < 1/4. The other phase is K·L·dy' ≤ K·L·A, since A is the largest of the four displacements.
- **Choice of K.** This step is correct. K is an integer and the same for both endpoints, so the shear power jK is an integer.
- **Affine label formula.** D90 re-derived it and got the same formula. Copy (+1, σ) has surface height σy, and the band shear moves X by −mL·(Y − band bottom). Measuring from y₀ instead of the band bottom changes X by a multiple of L. That's a multiple of every row circumference 2w, so the strip label doesn't change. With m = jK and t = KL·|y−y₀|, the shift is −σ·j·sy·t, which gives the README's term −σqjKL(y−y₀).
- **Leaf criterion.** This step is sound. The multitwist is an affine automorphism that fixes every integer-height point, so it fixes all corner lifts. It also commutes with the half-turn. A segment inside one unrolled cylinder pulls back to a straight, corner-avoiding segment.
- **One bounded phase set for all powers as A → 0.** There's no gap. The certificate uses only the cylinder decomposition of the fixed direction (p, q) on the sheared surface, which doesn't depend on K. K enters the label only through the bounded product j·t. Treating the six variables as independent covers a superset of the true region, so that's sound too. The pulled-back direction (p + jKLq, q) is unbounded, but the certificate never needs it.

## Gaps and caveats

1. **The half-turn identification is essential, and the README underplays it.** D90's first version accepted a closed lift only in the same labelled cylinder or its half-turn image, and only one fixed label for the whole box. It rejected the second leaf of tree `00 / 0 4 0`, where endpoint 0 alternates between cylinders 4 and 5 = H(4). Comparing half-turn orbits instead is sound: if s is in open ℓ and t is in the closure of ℓ or Hℓ, then t or Ht is in the closure of ℓ. With orbits, all 853 leaves pass. The README should say that labels are compared modulo the half-turn.
2. **Residual input isn't re-derived.** The residual polygons come from the census code, and D90 only audits them. The claim that every pair outside these products is already illuminated rests on that census. This check doesn't cover it, and it doesn't confirm that D74 covered these two rooms' other tile pairs.
3. **Random residual samples all have K = 1.** The residual polygons have A ≥ 1/(8L) almost everywhere, so the large-K regime comes only from the 40 synthetic pairs with A ≤ 1/100. Those pairs lie in the certificate box but not necessarily in the residual.
4. **Shared conventions.** D90 takes the box encoding (denominator 65536, split order) and the `ends` construction from the README and certificate format. These are definitions, not proof logic.
