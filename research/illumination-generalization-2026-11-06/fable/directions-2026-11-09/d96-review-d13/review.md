# d96: referee review of d13 theory.md §1–4 and cover.c (review-queue item Q01)

Date: 2026-11-20. Reviewer: independent referee session. Scope: `D/d13-cylinder-cover/theory.md`
§1–4, `cover.c`, and the Q01 brief in `D/d95-review-queue/review-queue.md`.

## Verdict

| Item | Verdict |
| --- | --- |
| Lemma A' (§2), with Corollary A and Theorem B' | Sound |
| Theorem C (§3), including C(2) | Sound |
| §4 soundness of `cover.c` | Sound. Four wording nits (N1–N4); none changes a result. |

No downstream result inherits a gap from this item. The downstream runs use `cover.c` with
patches (`qclass-closure/offgrid/build_cover.py` adds reverse pruning and a direction order).
Those patches, the tile-pair restriction, and the shear certificates are outside Q01. Q02, Q05
and Q06 cover them.

## 1. Lemma A'

The proof holds as written. Checks made:

- **Segment avoids Σ.** The open strip maps into the open cylinder C. C is a component of M minus
  the singular leaves, and every point of Σ lies on a singular leaf. Σ includes the convex-corner
  lifts, which are regular points of angle 2π. The code marks them too (`MLL` for types 1 and 3).
  So the relative interior of φ∘γ_n misses Σ. The endpoints are lifts of interior points, so they
  aren't in Σ either. Local isometry makes φ∘γ_n a straight segment of M.
- **τ swap.** τ is the sheet flip e ↦ −e. It's a deck transformation of M → P with derivative −I.
  So π∘τ = π, and τ maps θ-leaves to θ-leaves and θ-cylinders to θ-cylinders. τ is a
  homeomorphism, so closure(τC) = τ(closure C). The swap is legal.
- **T on the boundary of C (v1 = 0 or h).** The extension of φ maps the closed strip onto the
  closure, so t̃ has a preimage. The segment meets the boundary line only at its endpoint, and
  t̃ is a regular unmarked point. This covers T on a boundary saddle connection.
- **Segments along a boundary saddle connection.** Can't occur. A segment from v0 in (0, h)
  touches the boundary only at its end. Segments with v1 = v0 run along a regular leaf inside C.
- **Points on the seam of the double.** The proof never works in DP. Inside M, τ fixes only the
  lifts of convex and reflex corners, and no interior point lifts to one of those. Points over walls
  (fold edges) are regular points of M, and a crossing there is a reflection. A path through a
  flat boundary point is legal by the §1 convention.
- **Axis-parallel segments.** The segment can't slide along a wall. A wall-parallel M-segment
  starting at an interior point reaches a wall line only through that wall's end corner, which is
  in Σ.
- **Existence of n.** Every n works, because s̃ ≠ t̃ for S ≠ T.

The [Standard] facts used are the following. Rational directions on square-tiled surfaces
decompose into cylinders and saddle connections. A maximal cylinder is the image of a closed
strip. Both are textbook facts.

## 2. Theorem C

- C(1) is Lemma A' applied to each (θ, D).
- C(2): if S isn't live, then Ill_Θ(S) ⊇ int P ∋ T and T ≠ S, so S lights T. The T case follows
  by symmetry, which reverses the path. T ∉ Ill_Θ(S) is the contrapositive of C(1), and S ∉
  Ill_Θ(T) follows by symmetry. The argument needs S ≠ T, which a dark pair has.
- Theorem B' and the one-cylinder remark follow directly. In a one-cylinder direction, K_D is
  P. Λ is empty exactly on singular lines of both families.

## 3. §4 against cover.c

I checked each step line by line.

- **Slots and permutation (`compute_dir`).** A square has q bottom slots of width 1/q. A leaf from
  slot j reaches height 1 at offset (j+p)/q. That offset lies in square R^k(i) with
  k = ⌊(j+p)/q⌋, then passes Uu into slot (j+p) mod q. The open slot doesn't cross an integer, so
  k is constant on it. The slot boundaries are exactly the leaves through vertices.
- **Regular leaves.** `regl_[c] = 0` iff some slot (i, 0) of cycle c has a marked lower-left
  corner. Each vertex on a cycle's left boundary chain is the lower-left corner of the next slot's
  square, at index 0. So a chain is flagged exactly when it contains a marked vertex. The
  unmarked vertices are interior lattice points and flat points, both of angle 2π. So merging
  across them gives the components of M minus the singular leaves. Both merge cases are right:
  (i, j−1)/(i, j) and (Ri[i], q−1)/(i, 0).
- **τ merge and strip indices.** I re-derived the slot index of room strip k on all four sheets.
  The derivations match lines 119 and 123: m = k − k0 on (1,1),
  m = q(a+1) − p(b+1) − k − 1 on (−1,−1), m = k − qa − p(b+1) on (1,−1), and
  m = q(a+1) + pb − k − 1 on (−1,1). `slot()` walks left along the row when m < 0, which is
  correct even through folds. Merging all room strips of both families covers every τ-pair.
- **Λ (`lambda_at`).** An off-line point takes the strip label of any closed cell containing it.
  Strips continue across interior edges on one sheet, so all such cells agree. A point on an
  integer line takes `pline`/`mline`, which is NONE when the line is singular. The line index
  range is strict, `k0−p < k < k0+q`. A lattice point is found through a cell where it's a corner.
- **K_D and subtract.** K_D ∩ (cell) is the union of the closed faces of that cell with label D. A
  face of a neighbouring cell adds nothing, because strip labels agree across interior edges.
  Runs use closed half-planes. A clip at a range end is skipped only where W already satisfies it.
  `floordiv` and the ceiling are correct for negative values. Lower-dimensional pieces are
  dropped. The density argument for (I1) is right. (I2) holds because an open face meets no other
  closed face of its cell or of any other cell.
- **Cells (§4.3).** `lin_range` with lines `lo+1 .. hi−1` selects exactly the lines with
  min < k < max. Each crossing splits a piece into a closed lo piece, a closed hi piece, and the
  segment between them, and their relative interiors partition the piece. A segment can't lie on
  a θ-line, because the slopes differ. Λ is read at the centroid of three strictly convex hull
  vertices, or at a segment's midpoint, which lies in the relative interior.
- **Pairs (§4.5).** `in_qset` uses closed polygons (`cross_sign < 0` rejects), which is
  conservative. Hulls are counter-clockwise by monotone chain.
- **Arithmetic.** Vertex denominators are at most 2B² ≤ 800, so the products in `cross_sign`
  and `clip` fit in int128 by a wide margin. Representative points stay below 3·800³ ≈ 1.5e9,
  under the 1e13 guard. Every overflow guard exits rather than rounding. Array bounds hold for
  B ≤ 20: p+q ≤ 40 < 80 and nsq·q ≤ 5,120 < 10,240.

**Nits (no effect on results):**

- N1. The `cover.c` header says the program aborts if D > 1e6. The code uses 1e9, which matches
  theory §4.6. The header comment is stale.
- N2. In §4.6, "its denominator divides 2pq" holds only for two lines of one direction. For
  directions (p, q) and (p', q'), the determinant is qp' + pq'. The bound 2B² still holds.
- N3. §4.4 says the computed live set "is exactly X'_Θ". `cover.c` stops once every live cell is
  a point (line 566), so the set is X'_{Θ'} for the processed prefix Θ' ⊆ Θ. That set is a
  superset of X'_Θ, so soundness is unaffected. The claim should name Θ'.
- N4. In §4.2, π(C) also contains points on cell edges and walls, not only strips and regular
  lines. These points lie in the closure, so the formula for K_D is unchanged.

## 4. Independent tests (COMPUTED)

Rooms: R22 (`qclass-closure/r22-control.room`), and two rooms from d74's hard list
(`qclass-closure/offgrid/fifteen-hard.rooms`): index 1 (H1, 20 walls), index 4 (H4, 18 walls). I
added index 0 (H0, 20 walls) for coverage. `harness.c` includes `cover.c` unchanged and queries
its own `lambda_at`, `subtract` and `in_qset` for single point sources. A pair is certified when
T leaves Q(S). Sampling covers generic points, interior edges, points on lines qx ± py = k with
p, q ≤ B (singular and boundary lines), and interior lattice points. Every certified pair goes to
an exhaustive search over unfolded images by increasing length with d87's `billiard.py`. A
second tracer written here (`trace2`) re-checks each found path.

| Test | Pairs | Certified | Legal path found | Not found |
| --- | --- | --- | --- | --- |
| `test.py` seed 7, B = 8, R = 24 (`test_s7_n150_B8.log`) | 600 | 580 | 580 | 0 |
| `test.py` seed 11, B = 12, R = 30 (`test_s11_n200_B12.log`) | 800 | 782 | 782 | 0 |
| `near.py` seed 3, B = 12, near R22's dark pair (`near_s3_n150_B12.log`) | 150 | 126 | 126 | 0 |
| `near.py` seed 5, B = 16 (`near_s5_n150_B16.log`) | 150 | 132 | 132 | 0 |
| **Total** | **1,700** | **1,620** | **1,620** | **0** |

- **Dark pair.** R22's dark pair (1,3)–(3,5) is uncertified in both orders for every even B from
  4 to 16.
- **Uncertified pairs.** All 18 uncertified pairs of seed 11 have S at a `cover.c` live point:
  (5,4) in H0, or (3,5) in R22. Each one is certified in the reverse order. This agrees with
  the full `cover.c` runs (`cover B 1 2000000`), which report DONE for R22 (B ≥ 8), H1 (B ≥ 8),
  H0 (B ≥ 8) and H4 (B ≥ 12).
- **Labels against an independent implementation.** `labels_cmp.py` compares `cover.c`'s
  label partition and singular-line set with d74's `geom.Direction`. d74 wrote that code from
  prose, using a room-level flow union-find. The run covers 4 rooms, 91 directions each
  (p, q ≤ 12), and 134,880 strip labels, with 0 mismatches (`labels_cmp_B12.log`).
- **Mutation control.** `mutant/` changes `cover.c` to treat some marked vertices as unmarked,
  which creates false merges. The harness then certifies the dark pair (`CERT 7 6` at B = 8).
  The unmodified code returns NOCERT. So the tests can detect a false merge.

Limits: a found path proves a pair is lit, but most random pairs are lit anyway. The decisive
evidence is the proof reading, the label agreement with d74, and the dark-pair and mutation
checks. CPU used: about 3 minutes.

## Files

`harness.c` (build: `cc -O2 -o harness harness.c`), `test.py`, `near.py`, `nocert.py`,
`labels_cmp.py`, `rooms.txt`, `mutant/`, and the logs named above. Run the Python scripts with
`python3 -B` from this directory.
