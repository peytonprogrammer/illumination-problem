# Review: d15 Theorem 3 (r = 3, W = 10)

Date: 2026-11-22. Target: `../d15-small-r/theorems.md`, section "Partial
theorems for r = 3 and r = 4", with `lemmas.py`, `types_r3.txt`, and
`cert_r3.json`. Prior review: `../d15-review/review.md` (r <= 2 only).

**Verdict: sound with gaps.** Every one of the 13,030 certificates names a
lemma instance whose hypotheses hold, and every traced certificate path is
legal. The gaps are statement and scope issues, not errors in a certificate.
Theorem 3 closes no W = 10 word. The 578 open pairs below are the exact work
list.

Checks: `checks.py`, output in `checks.log`. Result: 23 PASS, 0 FAIL, 35
CPU-seconds, `python3 -B`, no network, no search over rooms or directions.

## 1. What Theorem 3 states

- **Statement.** Let P have 3 reflex corners and let S, T be distinct real
  interior points. If the pair of position types of S and T isn't in the
  `uncovered` list of the order type of P in `cert_r3.json`, the pair is lit.
- **Order type.** The set of grid cells of P on the rank grid of its vertex
  coordinates, up to the 8 symmetries of the square. There are 70 at r = 3.
- **Position type.** Doubled rank coordinates (X, Y). Even means on a grid
  line, odd means strictly between two neighboring grid lines.
- **"Certified" means this.** The hypotheses compare each point only with grid
  objects: cells in P, unit edges in the boundary, and the side of a grid line
  a point lies on. So one certificate covers every real realization of the
  order type, with any real edge lengths, and every pair of real interior
  points of the two position types. Parity and integrality play no role. The
  claim covers interior points only, not boundary points.
- **Counts, reproduced.** 13,608 position-type pairs, 13,030 certified, 578
  open. The re-run of `certify_type` matches `cert_r3.json` type by type, both
  counts and open lists.
- **Certificates by lemma.** A 10,285. A2 68. B 2,043. B2 250. C par 148.
  C perp 33. C same 200. D 3.
- **Fully certified types.** `.#./###/##.`, `.#./##./###/.##`, and
  `##../####/.###/.##.`. Each uses Lemma D for exactly 1 pair. All 3 have the
  word LLLRLLRLLR.
- **Type list.** An independent enumeration by lexicographically rooted closed
  walks on {0..4}^2 finds 2,400 simple walks and the same 70 types. Each type
  has exactly 1 boundary word.

## 2. Lemmas used at r = 3

Lemmas A, A2, B, B2, and C are the lemmas that the r <= 2 review confirmed.
At r = 3 they occur in new configurations, for example 250 B2 and 200 C same
certificates. `lemmas.py` tests the hypotheses on cell hulls and whole hub
sides in general, so nothing in that review depends on r <= 2. The
cross-check in section 4 confirms each r = 3 certificate against the review
code `rv.py`.

The one new lemma is **Lemma D** (two corridors at one corner). It's used
for 3 pairs. Each is the last pair of a fully certified type. This review
read the proof and the code.

- **Case c <= e.** Lemma B' applies with viewer T and corridor 1. The bounding
  box [-w, a] x [-c, 0] lies in the block and corridor 2, because a <= e2 and
  c < h. The condition d - s2 <= t2 - d of B' is c <= e. The weak form of B'
  (c = e, at least one sign) was confirmed in the r <= 2 review.
- **Case b <= a.** This is the mirror case, with viewer S and corridor 2. The
  box [-b, 0] x [-h, e] lies in the block and corridor 1.
- **Case c > e and b > a.** Then ae < bc. The segment TS crosses x = 0 at
  height -c + a(c + e)/(a + b), which lies in (-c, 0). It crosses y = 0 at
  x = a - (a + b)c/(c + e), which lies in (-b, 0). Both crossings are door
  points with P on both sides. The three pieces lie in corridor 2, the block,
  and corridor 1. Every point is interior.
- **Code.** `_lemma_D_canon` checks both side walls of corridor 1 on every row
  from the door to S, and both walls of corridor 2 on every column from V to
  T's cell. It checks the block, and the strict inequalities 0 < b < w,
  0 < c < h, e > 0, and a > 0. T on the far end of corridor 2 is allowed, as
  the lemma allows. These tests imply hypotheses 1 to 4 for every real point
  of the types.
- **Exact test.** 24 D certificates in 12 lattice rooms trace legal, along with
  176 degenerate D instances. The degenerate cases are S + T = 2V (12 pairs),
  one coordinate mirrored in V (76), the weak B' case c = e, and the direct
  case.

The `theorems.md` section "Weakest step" notes that no test checked Lemma D at
the level of hypotheses. This review closes that.

## 3. The 8 W = 10 words

Each ledger realization has the stated word. Its order type is in the list.

| Word | Ledger subfamily | Types (fully certified) | Pairs | Certified | Open | Open by link distance k | Ledger room type, open |
| --- | --- | --- | --- | --- | --- | --- | --- |
| LLLLLLLRRR | spiral | 5 (0) | 891 | 792 | 99 | k2 28, k3 52, k4 19 | 12703, 9 |
| LLLLLLRLRR | stacked hall | 5 (0) | 1,075 | 1,042 | 33 | k2 14, k3 19 | 6623, 7 |
| LLLLLRLLRR | stacked hall | 11 (0) | 2,100 | 2,033 | 67 | k2 34, k3 33 | 5503, 5 |
| LLLLLRLRLR | Ferrers staircase | 1 (0) | 322 | 321 | 1 | k2 1 | 4991, 1 |
| LLLLRLLLRR | two-bank | 23 (0) | 4,028 | 3,730 | 298 | k1 15, k2 118, k3 139, k4 26 | 8115, 20 |
| LLLLRLLRLR | pyramid | 5 (0) | 1,273 | 1,266 | 7 | k2 7 | 8051, 3 |
| LLLRLLLRLR | staircase band | 8 (0) | 1,539 | 1,487 | 52 | k2 29, k3 20, k4 3 | 5112, 3 |
| LLLRLLRLLR | orthoconvex 3-4 corners | 12 (3) | 2,380 | 2,359 | 21 | k2 15, k3 6 | 8052, 3 |
| Total | | 70 (3) | 13,608 | 13,030 | 578 | k1 15, k2 246, k3 269, k4 48 | |

A word can have several order types, because different length orders give
different rank grids. A word is closed only when every one of its types is
closed. `checks.log`, section 3, lists every open pair by type, in the
canonical frame of `cert_r3.json`.

All 15 open pairs with k = 1, the collinear pairs separated by a vertex, are in
the two-bank word LLLLRLLLRR.

### Small open lists, verbatim

- **LLLLLRLRLR, Ferrers.** Mask 4991 `#.../##../###./####`: (1,7)-(7,1).
- **LLLLRLLRLR, pyramid.**
  - Mask 761 `#../##./###/#..` and mask 763 `#../##./###/##.`: (1,7)-(5,3).
  - Mask 8051 `#.../####/###./##..`: (1,1)-(7,5), (2,1)-(7,5), (3,1)-(7,5).
  - Mask 6131 `#.../###./####/##..` and mask 5111 `#.../##../####/###.`:
    (1,7)-(7,3).
- **LLLRLLRLLR, 3-4 corners.**
  - Masks 122, 1010, 986, 1238, 8132, and 8052: 3 pairs each. In each, one
    position type is fixed and the other runs over 3 consecutive types.
  - Masks 1275, 12023, and 9207: 1 pair each.
  - Masks 187, 1278, and 16358: none. These are the 3 fully certified types.

## 4. Re-run and exact traces

- **Cross-check on unit-gap rooms, all 70 types.** For every certified pair,
  `rv.py` finds every instance of the certificate's lemma from the geometry.
  The author's certificate must name one of them, with the same lemma, door,
  flat end, and roles. That instance is then traced exactly. Result: 13,030 of
  13,030 confirmed, 13,033 traces legal, 0 problems.
- **Open pairs.** For all 578 open pairs, `rv.py` also finds no instance of A,
  A2, B, B2, C, or D. So the gap isn't an artifact of the search order in
  `lemmas.py`. 4 open pairs have a Lemma B' instance in the unit room. B' is
  metric, so it isn't a certificate.
- **Lattice realizations, 4 per word, 32 rooms.** Each word gets the ledger
  room plus 3 rooms with gap vectors such as x (2, 7, 3, 1) and y (4, 3, 1, 2).
  Where a word has several types, the 3 rooms are its types with the most
  open pairs. Every certified pair is traced with two point choices:
  half-cell points, and generic rationals 1/3, 2/5 against 3/7, 5/11. Result:
  11,638 traces legal, 0 problems, 0 over the reflection cap.
- **Lemma D rooms.** The 3 fully certified types get 4 lattice rooms each.
  Result: 5,480 certificate traces and 176 degenerate D traces legal.
- **Irrational rooms.** One room per word uses gaps 1, sqrt 2, 2 - sqrt 2 / 2,
  and 1 + sqrt 2. Result: 1,905 traces legal, all in exact Q(sqrt 2)
  arithmetic.
- **C same degeneracy.** No C same certificate uses one corridor as both arms
  (0 of 200). So the correction from the r <= 2 review doesn't affect r = 3.

## 5. The d168 claim for LLLLLRLRLR

**Confirmed exactly.** The word has 1 order type, mask 4991
`#.../##../###./####`. A staircase has strictly monotone step coordinates,
so no coincident type exists. Its only open pair is (1,7)-(7,1).

- (1,7) is the only position type with a point strictly inside the top cell
  (0,3). (7,1) is the only one strictly inside the bottom-right cell (3,0).
  The other sides of those cells are walls, and points on the inner grid lines
  have other position types, which are certified.
- The other 321 pairs are certified: A 281, B 32, C perp 8. All 321 trace
  legal in 4 lattice rooms and 1 irrational room.
- So in every Ferrers room with W = 10, every two distinct real interior points
  are lit for all real lengths. The one exception is a point in the open top
  cell paired with a point in the open bottom-right cell. Its d168 framing is
  "[v, W] x [0, h]". The ledger room shows the same shape in a reflected
  frame.
- That doesn't close the word for lattice rooms. d168 found that the terminal
  strip note covers only a thin region of that pair.

## 6. Work list for closing W = 10

Proven for all real lengths and all real interior pairs: every certified pair
above, and the 3 types masks 187, 1278, and 16358 completely. Left open: the
578 pairs in section 3, by word.

1. **LLLLLRLRLR (Ferrers): 1 pair.** Top cell against bottom-right cell, k = 2.
   This is the 4-step staircase example in `theorems.md`. The region between
   the doors is an L shape.
2. **LLLLRLLRLR (pyramid): 7 pairs in 5 types,** listed in section 3.
3. **LLLRLLRLLR (3-4 corners): 21 pairs in 9 types.**
4. **LLLLLLRLRR (stacked hall): 33 pairs in 5 types.**
5. **LLLRLLLRLR (staircase band): 52 pairs in 8 types.**
6. **LLLLLRLLRR (stacked hall): 67 pairs in 11 types.**
7. **LLLLLLLRRR (spiral): 99 pairs in 5 types.** The ledger lists it as
   PARTIAL by d84, for U2 and its stretches.
8. **LLLLRLLLRR (two-bank): 298 pairs in 23 types.** These include all 15
   collinear k = 1 pairs.

## Gaps

1. **Medium. "3 of 70 types fully certified" doesn't mean that a word is
   closed.** All 3 types belong to LLLRLLRLLR. That word has 9 more types with
   21 open pairs. The Results section should say that Theorem 3 closes no
   W = 10 word.
2. **Medium, closed by this review. Lemma D was unchecked at the level of
   hypotheses.** `theorems.md` says so under "Weakest step", and only the
   shooting test C9 supported it. Section 2 checks the proof and the code by
   hand, and the exact traces confirm them. The 3 fully certified types
   depend on it.
3. **Low. Frame of the table.** Theorem 3 says "the order type of P in
   `cert_r3.json`". The lists are in one canonical frame. The statement should
   say that you first map P by one of the 8 symmetries and transform the
   position types the same way. d168 applies the table correctly to the
   reflected ledger room.
4. **Low, inherited. Setting.** The Setting says integer vertex coordinates,
   but Theorem 3 claims real lengths. The correction is the one from the r <= 2
   review: real coordinates. No proof uses integrality.
5. **Low, inherited. Lemma C same form** needs "two different corridors". It
   has no effect at r = 3: 0 of 200 certificates.
6. **Low. Interior points only.** Theorem 3 says nothing about boundary points,
   including the d10 boundary dark pair at W = 10.
