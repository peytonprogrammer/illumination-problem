# Review: attainment of the restricted bound by the 22-wall room

[done] Claude Opus, 2026-11-02. Daniel approved this check ("go ahead"), and Codex requested it on the board. The inputs are:
- `illumination-k4-codex/restricted-theorem-note/attainment-check.txt`;
- `preprint-review-codex/revised.tex`, the construction and `thm:main`;
- `preprint-review-codex/geometry-check.json`, read only.

No command, run, or search was used. I rebuilt the room from its five squares and counted by hand.

**Verdict: ACCEPT, no corrections.** The 22-wall room Q is in the exact class of the restricted theorem, with k = 4. Every number in Codex's ledger matches my count.

So the bound is attained. Among strictly simple canonical 45° lattice disks with k ≤ 6, the fewest walls for a dark pair of distinct interior A marks is 22. The same holds for k ≤ 4 and k ≤ 5. For k ≤ 3, the theorem still gives at least 22 walls, but this room doesn't show that 22 is reached.

This review doesn't re-prove darkness. Darkness rests on the preprint proof, which I accepted in `review-preprint-v02/findings.md`.

## 1. The room

P has the unit squares with lower-left corners (−1,−1), (0,−1), (0,−2), (1,−2), and (1,−3). Q is the union of three pieces:
- P itself;
- its mirror image P₁ = {(x, −y)};
- its half-turn image P₂ = {(4 − x, −y)}, a rotation by 180° about (2,0).

Each row of Q, by the x values of its squares' lower-left corners:

| Row (lower y) | Squares at x |
|---|---|
| 2 | 1, 2 |
| 1 | 0, 1, 2, 3 |
| 0 | −1, 0, 3, 4 |
| −1 | −1, 0 |
| −2 | 0, 1 |
| −3 | 1 |

That's 15 squares and 30 triangles, so N = 30.

**Pieces and seams.**
- P lies in y ≤ 0, P₁ in y ≥ 0 with x ≤ 2, and P₂ in x ≥ 2 with y ≥ 0. So their interiors are disjoint.
- P ∩ P₁ is the segment from (−1,0) to (1,0).
- P₁ ∩ P₂ is the segment from (2,1) to (2,3).
- P ∩ P₂ is empty, because (2,0) isn't in P.

## 2. Class membership

**Canonical tiling.** Each unit square has exactly one even-even corner and one odd-odd corner, and they're diagonal. So each square splits into two canonical triangles. The union is unchanged whichever way you think of the split.

**Disk and strict simplicity.**
- **Connected.** Each piece is a chain of edge-adjacent squares. P meets P₁ along the edge between the squares at (−1,−1) and (−1,0). P₁ meets P₂ along x = 2.
- **No holes.** The two empty squares at row 0, x = 1 and x = 2, open downward. They reach the outside through the empty squares at row −1, x = 1, 2, and 3.
- **No pinches.** No grid point has exactly two diagonally opposite squares filled. I checked all 30 integer points of Q.

**Boundary cycle.** I traced it counterclockwise from (−1,−1):

(−1,−1) → (−1,1) → (0,1) → (0,2) → (1,2) → (1,3) → (3,3) → (3,2) → (4,2) → (4,1) → (5,1) → (5,0) → (3,0) → (3,1) → (1,1) → (1,−1) → (2,−1) → (2,−3) → (1,−3) → (1,−2) → (0,−2) → (0,−1) → (−1,−1).

| Corner type | Corners | Count |
|---|---|---|
| Convex | (−1,−1), (−1,1), (0,2), (1,3), (3,3), (4,2), (5,1), (5,0), (3,0), (2,−1), (2,−3), (1,−3), (0,−2) | 13 |
| Reflex | (0,1), (1,2), (3,2), (4,1), (3,1), (1,1), (1,−1), (1,−2), (0,−1) | 9 |

So W = 22, and c − r = 4.
- **Wall lengths.** Six walls have length 2, and the other 16 have length 1. The boundary length is 28.
- **Matches the JSON.** These counts match `geometry-check.json`: 15 squares, 22 vertices, 13 convex, 9 reflex, and 1 boundary component.

**Marks.** S = (0,0) and T = (2,2) each have all four neighboring squares in Q. Both are even-even, so both are interior A points.

## 3. Integer-point ledger

Q has 30 integer points: 2 interior and 28 on the boundary.

**Interior.** Only (0,0) and (2,2) have all four squares filled. So I = 2 and J = 0.

**Smooth boundary points.** The 28 boundary points are the 22 corners plus one point in the middle of each length-2 wall:

| Wall | Point | Type |
|---|---|---|
| x = −1, y from −1 to 1 | (−1,0) | C |
| x = 1, y from −1 to 1 | (1,0) | C |
| y = 1, x from 1 to 3 | (2,1) | C |
| y = 3, x from 1 to 3 | (2,3) | C |
| y = 0, x from 3 to 5 | (4,0) | A |
| x = 2, y from −3 to −1 | (2,−2) | A |

So s_A = 2, s_N = 4, and no smooth point is a B point. That gives k = J + s_N = 4.

The four C points are the seam endpoints E₁ to E₄ of the preprint. The two A points are copies of the base marks: b = (2,−2), and (4,0) is the half-turn image of a = (0,0).

**A corners.** The even-even corners are (0,2), (4,2), and (0,−2). All three are convex with 2 triangles each, so Σm = 6. The other corners are B or C points.

## 4. Identities

- **Charge.** Q = 3s_A + Σm = 6 + 6 = 12.
- **Wall formula.** W = 2 + 6I + Q − 2J − s_N = 2 + 12 + 12 − 0 − 4 = 22.
- **A count.** N = 8I + Q + s_A = 16 + 12 + 2 = 30.
- **Euler count.** N = 2(I + J) + W + s_A + s_N − 2 = 4 + 22 + 2 + 4 − 2 = 30.
- **Euler check.** V = 30, E = V + N − 1 = 59, and 3N = 2E − 28 = 90.

## 5. Wording

**Supported:** "22 is the minimum number of maximal walls among strictly simple canonical 45° lattice disks with k ≤ 6 that contain a dark pair of distinct interior A marks."
- That statement rests on two parts: the certified exclusion for W ≤ 21 with k ≤ 6, and this room's membership.
- It doesn't establish a universal minimum or historical novelty. See `../restricted-novelty/findings.md`.

**Optional precision:** the room has k = 4. So the same minimum holds for any budget from k ≤ 4 to k ≤ 6.
