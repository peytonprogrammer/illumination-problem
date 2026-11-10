# Audit: the even-m staircase family

[done] Claude Opus, 2026-11-02. Codex requested this independent hand derivation on the board. The source is `illumination-k4-codex/preprint-review-codex/staircase-family-review.txt`, which uses Daniel's family definition.

Scope: hand derivation only. No code or search was run, and no manuscript was edited.

**Verdict.**
- **Validity: ACCEPT, no corrections.** For every even m ≥ 2, Q_m is a strictly simple orthogonal polygon with 12m − 2 walls, and S = (0,0) and T = (m,m) don't illuminate each other.
- m = 2 is exactly the 22-wall room of the preprint.

## 1. The base P (2m + 1 squares)

The squares are [−1,0]×[−1,0] plus one column for each j = 0, …, m − 1. Column j covers x ∈ [j, j+1] and y ∈ [−j−2, −j]. Neighboring columns overlap on one unit of height, y ∈ [−j−1, −j] at x = j. The initial square and column 0 overlap on y ∈ [−1, 0].

Traced counterclockwise, the boundary is:
- (−1,−1) → (0,−1);
- then, for j = 0, …, m − 1, (j,−j−1) → (j,−j−2) → (j+1,−j−2);
- then up the right edge x = m to (m,−m+1);
- then back along the tops: (j+1,−j) → (j+1,−j+1) → (j,−j+1) for j = m−2, …, 0;
- then the top edge from (1,0) to (−1,0), and down to (−1,−1).

| Corner type | Points | Count |
|---|---|---:|
| Reflex | (0,−1), and (j,−j−1) and (j,−j) for 1 ≤ j ≤ m−1 | 2m − 1 |
| Convex | (−1,−1), (−1,0), (j,−j−2) for 0 ≤ j ≤ m−1, (m,−m−1), (m,−m+1), and (j,−j+1) for 1 ≤ j ≤ m−1 | 2m + 3 |

The total is 4m + 2 corners, and convex minus reflex equals 4, as an orthogonal polygon requires.

**Integer points.**
- **No interior points.** For (j,y) to be interior, the left column needs y = −j and the right column needs y = −j−1. These can't both hold. The same check works at x = 0.
- **No pinches.** Each turn point has three incident squares.
- **Only a and b are smooth.** Every edge has length 1 except the top edge (−1,0)–(1,0) and the right edge (m,−m−1)–(m,−m+1). Their midpoints, a = (0,0) and b = (m,−m), are the only non-vertex integer boundary points.

## 2. The assembly Q_m

The copies are P0 = P, P1 = {(x,−y)}, and P2 = {(2m−x,−y)}.
- **P0 and P1** lie in y ≤ 0 and y ≥ 0. They meet in P ∩ {y = 0}, which is the top edge H = [−1,1]×{0}.
- **P1 and P2** lie in x ≤ m and x ≥ m. They meet in the image of P's right edge, V = {m}×[m−1, m+1].
- **P0 and P2** could meet only on y = 0. There, P0 has x ∈ [−1,1] and P2 has x ∈ [2m−1, 2m+1]. These are disjoint for every m ≥ 2.

H and V are disjoint arcs of P1's boundary, so Q_m is a disk with a strictly simple boundary.

**Seam endpoints.** The endpoints are (−1,0), (1,0), (m,m−1), and (m,m+1).
- Each one joins two convex base corners into a straight wall. For example, (m,m−1) comes from (m,−m+1) through both P1 and P2.
- Copies touch only on H and V, so every other corner incidence stays a distinct Q corner.

The counts follow:
- W = 3(4m+2) − 8 = 12m − 2;
- 3(2m+3) − 8 = 6m + 1 convex corners;
- 3(2m−1) = 6m − 3 reflex corners;
- area 6m + 3.

For m = 4, that gives 46 walls and area 27. For m = 2, it reproduces the preprint's 22 walls and area 15.

## 3. Darkness for even m

- **Folding.** The fold maps are the identity, (x,−y), and (2m−x,−y). f_P1 and f_P0 differ by the reflection across y = 0, and f_P2 and f_P1 differ by the reflection across x = m. So they agree on the seams, f(S) = a, and f(T) = b.
- **Reversal.** At (±1,0), the wall is vertical and the copy change negates the vertical component. At (m,m±1), the wall is horizontal and the copy change negates the horizontal component. In each case the folded velocity becomes −v.
- **Parity.** For even m, b = (m,−m) is even-even. The argument from the 22-wall case applies unchanged: a = (0,0) is also even-even, and every integer point of P with an odd coordinate is a vertex.
- **Truncation.**
  - f⁻¹(a) = {S, (2m,0)}. The point (2m,0) is the midpoint of P2's bottom edge, which is a smooth wall point.
  - f⁻¹(b) = {T, (m,−m)}. The point (m,−m) lies on P0's right wall.
  - So the truncation to the last visit of a in P is needed, and the preprint's argument covers it.
- **Axis-parallel paths.** S and T differ in both coordinates, so no axis-parallel path joins them.

**Odd m.** In that case, b = (m,−m) has both coordinates odd. The endpoint parity step fails, so no conclusion follows, and Codex correctly claims none.

## 4. Scope

The family uses the same mechanism as the 22-wall room: unfolding, endpoint parity, and three reflected copies.
