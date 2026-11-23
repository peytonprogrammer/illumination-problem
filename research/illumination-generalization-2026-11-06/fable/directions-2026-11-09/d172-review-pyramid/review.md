# Review: pyramid-column note (snapshot 2026-11-22 0855)

Target: `../d95-review-queue/snapshots/pyramid-column.2026-11-22-0855.md`.
Context: d169 open-pair list, d170 tracer, d163 ledger.

**Verdict: sound with gaps.** The all-abscissa lemma and its broad-band
extension are correct. All 7 open pyramid pairs from d169 have the required
sweep form. Every constructed shot replays exactly. The gaps are wording and
scope issues. None is an error in the proof.

Checks: `checks.py`, output in `checks.log`. Result: 29 PASS, 0 FAIL,
0.4 CPU-seconds, `python3 -B`, exact `Fraction` arithmetic, 9 named rooms,
no room search, no network. `trace()` is copied verbatim from d170.

## 1. All-abscissa lemma

Chart: the middle band is [0, u], the first run is [0, w], and the final run
is [0, V] (c = 0) or [u − V, u] (c = u). L = d + b, D = a + L.

- **Choice of i.** R − c = (dz − cL − 2ubi)/L. With i nearest to
  (dz − cL)/(2ub), |R − c| ≤ ub/L. Confirmed on 4,000 random rational
  instances.
- **M and the final coordinate.** With M = (z + 2ui)/L and slope M − X/D, the
  developed coordinate is XL/D at the first joint and R + Xb/D at the second
  joint after removing 2ui. It is z at the target. The term X(1 − t/D) vanishes
  at t = D. Confirmed exactly.
- **Start copy.** X ≡ x + Ma (mod 2w), so X − Ma = x + 2wk. The start lies in
  an even copy, and the physical slope equals the developed slope.
- **Gates.** |XL/D| < w because L < D. |Xb/D| < wb/L for X ≠ 0, and it's 0
  for X = 0. So the second gate is strictly within ub/L + wb/L of c. That's at
  most u if and only if wb ≤ ud. Both gates are strict. So the ray never
  reaches the corners (w, y1), (u, y2) (c = 0), or (0, y2) (c = u).
- **Folding agreement.** On (c − u, c + u), the 2u-periodic middle fold equals
  the 2V-periodic final fold for both c = 0 and c = u. Confirmed on 3,000
  samples.
- **Zero displacement.** A gate at exactly 0, or at exactly u when c = u, lies
  on a straight side wall, not at a vertex. That's a regular reflection point.
- **Slab confinement.** Inside the slab, horizontal walls occur only at the 2
  joint levels. The gates are strictly inside the open parts of those levels.
  So the vertical velocity never changes sign. The ray stays between the
  endpoint levels, and side openings above or below play no role.
- **Broad-band extension.** The residual numerator dz − cL + 2dVj − 2ubi is
  confirmed. min(ub, dV) + wb ≤ u(d + b) holds exactly when b ≤ ud/w or
  b ≥ d(V − u)/(u − w). It holds for every b when wV ≤ u². Confirmed on
  15,000 samples.

## 2. The 7 open pairs

All 7 pairs use left-attached nested rows, so c = 0. Each run is a single
rank row, so its two side walls span the full row. Asserts in `params()`
confirm containment and the shared sides.

| Mask | Pair | Sweep (rows) | (w, u, V) at unit gaps | Sufficient region (gaps g by column, h by row, bottom up) |
|---|---|---|---|---|
| 761, 763 | (1,7)-(5,3) | 3 → 2 → 1 | (1,2,3) | g0·g2 ≤ g1(g0+g1), or g0·h1 ≤ (g0+g1)·h2 |
| 8051 | (1,1), (2,1), (3,1)-(7,5) | 0 → 1 → 2 | (2,3,4) | A·g3 ≤ g2(A+g2) with A = g0+g1, or A·h2 ≤ (A+g2)·h1 |
| 6131 | (1,7)-(7,3) | 3 → 2 → 1 | (1,3,4) | g0·g3 ≤ (g1+g2)(g0+g1+g2), or g0·h1 ≤ (g0+g1+g2)·h2 |
| 5111 | (1,7)-(7,3) | 3 → 2 → 1 | (1,2,4) | g0(g2+g3) ≤ g1(g0+g1), or g0·h1 ≤ (g0+g1)·h2 |

The first condition is wV ≤ u², and the second is w·h_T ≤ u·d. Their union
is exactly the set where the broad-band criterion holds for every b in
(0, h_T). Together with d169's 1,266 certified pairs, every pyramid room in
this region is fully lit for real interior pairs.

**Left open for LLLLRLLRLR:** the rooms of each order type that fail both
conditions of that type. One example is V1 below, which is 761 with gaps x
(3, 1, 6) and y (1, 5, 1, 2). Equal column gaps always pass, for any row gaps.

## 3. Exact replays

Each pair type gets 13 marks: the half-lattice mark and 12 random rational
marks with denominators 97 or 1009. Grid-line coordinates stay on their lines.

- **5 rooms inside the region:** A761, B8051, C6131, D5111, and E763. E763 passes
  only through the depth condition. All 91 marks (7 pair types) trace to T, with strict gates.
- **3 rooms outside the region:** V1-761, V2-8051, and V3-5111. Wherever the
  hypothesis held for the actual b, the note's shot traced to T (16 marks).
- **Violated marks in those 3 rooms:** all 49 remaining marks are still lit.
  The note's shot or another member of the same one-middle family reaches T:
  i offset by up to 4, j in [−4, 4], and X shifted by 2wk with |k| ≤ 3. This
  is a bounded replay of the construction's parameters, not a room search.
  It shows only that these named rooms are lit. Darkness is not claimed
  anywhere.
- **Mask 8052 example.** With unit column gaps and row gaps (3, 1, 4, 2), the
  sweep has c = u. Both placements, (1,5) and the upper-edge mark (1,6), trace
  to T on 13 of 13 marks each.

## 4. Ledger

- **LLLLRLLRLR should become PARTIAL** on the region in section 2, with this
  review as the reviewer. Example subfamily: equal column gaps with arbitrary
  row gaps. It isn't COVERED, because rooms that fail both conditions remain.
- **LLLRLLRLLR merits PARTIAL, and the note's reasoning is correct.** d169
  reviewed Theorem 3 and found 3 order types with empty open lists: 187,
  1278, and 16358. Each one covers every real length assignment of an order
  type, which is an infinite metric subfamily. That meets the ledger
  definition. The credit belongs to d169, not to this note. The coordinator
  hasn't recorded it in `STATUS.md` yet.

## Gaps

1. **Medium. The unresolved region is stated too loosely.** "The unresolved
   pyramid cases must violate that inequality" names only the depth
   condition. After the broad-band section, unresolved rooms must fail both
   wV ≤ u² and w·h_T ≤ u·d. The note should state the per-type union in
   section 2 as the PARTIAL region.
2. **Low. Wording: "the other 1,266 position types"** should read "position-type
   pairs".
3. **Low. Frame.** "Equal horizontal rank gaps" refers to the canonical frame
   of `cert_r3.json`. A room in another orientation must be mapped first, as
   in d169 gap 3.
4. **Low. Endpoint levels.** The lemma needs a > 0 and b > 0. A target on the
   far boundary line of its run, such as 8052 (1,6), is allowed. The statement
   should say so and not leave it to the 8052 paragraph.
5. **Low, not checked.** This review didn't verify the residual-count table
   for the other 4 words, such as 11 of 21 for LLLRLLRLLR.
6. **Observation, not a gap.** All 49 violated marks are lit by other (i, j, k).
   So the stated region isn't sharp. Joint rounding of (i, j) and allowing
   |X| < wD/L would enlarge it.
