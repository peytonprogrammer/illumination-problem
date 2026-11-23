# D100: independent residual check for `qclass-closure/two18`

**Verdict: CONFIRMED.** This check recomputes both rooms' residuals with independent code. It
finds the same 36 open tile pairs, and every residual pair lies inside the domain the shear
certificates cover. 100 large-K pairs drawn from inside the residual (K from 2 to 98) trace
correctly along the certificate path. This closes gaps 2 and 3 of
[d90](../d90-check-two18/README.md) (review queue item Q05).

## Re-run

```
bash run.sh > run.log 2>&1
```

The run takes about 3.1 CPU-minutes, mostly `cert2` built with UBSan. `KEEP=1` keeps `work/`
(about 25 MB of residual output); by default `run.sh` deletes it. See [run.log](run.log).

## Files

| File | Role |
|---|---|
| `cert2.cpp` | The tile-pair certifier. Lines 1–394 are d74's `cert.cpp` core verbatim: labels, singular lines, splitting, and Q update, written from d13 `theory.md`. The two-sided tile-pair driver after it is new. |
| `compare.py`, `compare_lib.py` | Compare the d100 residual with the census residual. |
| `sample_k.py` | Draws large-K pairs from the d100 residual and traces them. |
| `rooms.txt` | Copy of `two18/rooms`; `run.sh` checks that it's byte-identical. |
| `cert2_r0.log`, `cert2_r1.log` | Per-tile-pair summary: live pieces, products, and directions used. |
| `compare.log`, `sample_k.log`, `control_B8.log` | Results and the negative control. |

## Method

**Residual (task 1).** For each room, `cert2` runs over all 171 unordered tile pairs (a, b) with
directions 1 ≤ p, q ≤ 18. That bound matches the census.

- Side 0 holds every piece of int P whose closure lies in closed cell a: the open cell, its
  interior open edges, and its interior lattice corners. Its Q starts as closed cell b. Side 1
  is the same with a and b swapped.
- For each direction, both sides are split and their Q sets updated with d74's code. The two
  sides are then pruned against each other. A piece f survives only when some piece g on the
  other side satisfies two conditions: closure(g) meets ∪Q(f), and closure(f) meets ∪Q(g).
  Two copies of the same lattice point are not partners.
- Output: every live f × W, where W ∈ Q(f) meets the closure of a surviving partner.

The driver avoids d74's built-in tile mode, which prunes a piece against its own side and is
unsound for distinct tiles.

**Soundness.** Suppose (S, T) is dark, with S in closed cell a and T in closed cell b. By the
Lemma A' invariant (d13; d74 argues it), S lies in a side-0 piece f with T ∈ ∪Q(f). T lies in a
side-1 piece g with S ∈ ∪Q(g). So f and g witness each other in every prune round. Skipping a
direction is always sound; the cap of 20,000 pieces never triggered, and 0 directions were
skipped.

**What the code doesn't share with the census.** `cert2` doesn't read `cover.c`,
`build_cover.py`, `build_pairskip.py`, `export_labels.py`, or any census output. The census
residual enters only in step 2, as the object being compared.

## Results

### Tile pairs and containment (task 2)

| Quantity | Census (`two18`) | D100 |
|---|---|---|
| Open tile pairs, room 0 | 18 | 18, the same set |
| Open tile pairs, room 1 | 18 | 18, the same set |
| Polygon products | 146,308 | 165,308 (a different partition; 79,420 + 85,888) |
| Maximum displacement from the designated point | 1/17 | 1/17, exact, every vertex |
| Designated grid points | from census | derived from the d100 output; equal to the census on all 72 ends |

Containment holds in two senses:

- **In the certified domain (exact, load-bearing).** Every vertex of every d100 product lies
  in the closed cells of an audited tile pair. It's also within 1/17 of that pair's designated
  point at each end. Each end has a unique such point. The shear trees cover all pairs of the
  36 tile pairs with displacements up to 1/17 (d90 confirmed the root box ⊇ [0, 1/17]). So the
  d100 residual is inside what the certificates prove, with no gap.
- **In the census products (sampled evidence).** 300 random pairs from d100 products were
  checked. All 300 lie in the closure of some census product. Exact containment in the union
  of census products wasn't checked, because the two partitions differ.

**Negative control.** With room 0 at B = 8, the comparison fails as intended (see
`control_B8.log`). It reports an extra tile pair (11, 15) and 38 ends that reach past 1/17,
and 5 of 50 samples fall outside the census products.

### Large-K samples (task 3)

A product f × W qualifies when closure(f) contains its designated point e and W contains the
other end's designated point e′. 24,968 of 165,308 products qualify. Each sample takes random
relative-interior points X and Y, then sets S = e + λ₁(X − e) and T = e′ + λ₂(Y − e′). Convexity
keeps S in relint f and T in W. The scales λ are chosen so that K = ⌈1/(8LA)⌉ ≥ 2. Each pair is
walked to its certificate leaf and developed in the leaf's cylinder. The path is pulled back by
the shear power jK and traced with the D87 exact tracer, using d90's `check.trace_pair`.

| Quantity | Value |
|---|---|
| Pairs traced | 100, all K ≥ 2 |
| Failures | 0 |
| K | minimum 2, median 38, maximum 98; 91 pairs with K ≥ 10, 46 with K ≥ 40 |
| Room and axis tags | 00: 25, 01: 23, 10: 25, 11: 27 |
| Tile pairs hit | 32 of 36 |
| Longest pulled-back vector, ‖V‖₁ | 50,701 |
| Inside a census product closure | 100 of 100 |

## Caveats

- Soundness of `cert2` rests on Lemma A' (d13 `theory.md`) and d74's label code. d74 validated
  that code against an exact tracer and an R22 control. Its soundness argument is not a third
  derivation of the cylinder lemma.
- The tracing step reuses d90's `trace_pair`. That code was written independently of the
  author's, but it's the same tracer d90 used.
- Large-K samples reached 32 of the 36 tile pairs, because pair choice was random. The
  exact box containment covers all 36.
