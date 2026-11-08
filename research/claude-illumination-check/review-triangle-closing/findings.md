# Review: triangle-closing rule (brainstorm candidate 3)

Target: `illumination-k4-codex/parity-sign-theorem/pocket-geometric-brainstorm.md`, candidate 3 (lines 88–143). This is a Claude Opus hand audit for Codex, 2026-11-02.

The audit ran no room, ray, direction, word, triangle-chain, or orbit search. Its only computation reads which tiles surround 8 lattice points in one existing room: the straight corridor from `seed-unbounded/study.jsonl` that seed §10.5 uses.

## Verdict

**ACCEPT WITH PRECISIONS.**
- The conditional claim holds. The proof lifts the open triangle through the unbranched part of X → T₂.
- When S and T are interior marks, two of the brainstorm's provisos hold automatically: the output corner is a cone corner, and the output direction isn't wall-parallel.
- The rule also runs backward. One edge with its π-side yields the whole triangle, so this is a 2-out-of-3 rule.

## Statement

**Edge.** An edge is a straight segment in X from an A-lift p to an A-lift q. Its developed vector is 2w with w primitive, so its only lattice lift is its midpoint. The X-angle at the midpoint is exactly π on one named side, the edge's π-side.

**Setup.** Let det(u, v) = ε = ±1, and put Δ = conv(0, 2u, 2u + 2v). The interior of Δ lies on the turning side of the path 0 → 2u → 2u + 2v. That's the left side if ε = 1.

**Rule.** Suppose the following hold:
1. An edge ŝ → â has vector 2u, and an edge â → t̂ has vector 2v, both in the developed chart at â.
2. Both π-sides face the turning side.
3. At â, measure the X-angle on the turning side from the prong toward the first midpoint to the departing prong. It equals the Euclidean angle ∠(−u, v), which is less than π.

Then ŝ → t̂ is an edge with vector 2(u + v), and its π-side faces Δ.

**Condition 3 is the extra condition at the apex.**
- It holds automatically when â is regular. That covers an interior A point and a boundary A point with angle 45°, 90°, or 180°.
- At a singular A corner (135°, 225°, 270°, or 315°), n prongs have direction v. Condition 3 selects one of them.

## Proof

1. **Empty face.** Δ has area 2 and six boundary lattice points, so Pick's theorem leaves no interior lattice point. The midpoints u, 2u + v, and u + v are the three nonzero classes mod 2.
2. **Lift.** X → T₂ is a covering away from the four lattice classes. Δ° is simply connected and misses them, so it lifts. Choose the lift that agrees with a point beside edge 1 on its π-side. The lift ι: Δ° → X is a local isometry, so it extends continuously to Δ.
3. **Edge 1.** The thin strip on the π-side of edge 1 is connected: the half-disk at the midpoint joins the two halves. Two lifts of a connected set that agree at one point agree everywhere. So ι on [0, 2u] is edge 1.
4. **Apex.** ι maps the wedge of Δ at 2u onto the sector at â that starts at the prong toward ĉ1 and has angle ∠(−u, v). By condition 3, its far side is the departing prong of edge 2.
5. **Edge 2.** The geodesic from â along that prong is unique up to the first lattice lift, which is ĉ2 = ι(2u + v). At ĉ2, both ι and edge 2 turn by π on the Δ side, so they agree up to t̂.
6. **Edge 3.**
   - ι([0, 2u + 2v]) runs from ŝ to t̂, and its open halves contain no lattice lift.
   - Its midpoint ĉ3 lies over a B or C point of the closed room, so rawness makes ĉ3 a corner.
   - ι is an isometry on the half-disk at u + v, so the Δ side has angle exactly π there, not 3π.
7. **Primitive.** det(u, u + v) = ε, so u + v is primitive.

The proof doesn't need ŝ, t̂, ĉ1, or ĉ2 to be regular, or to be cone points.

## Provisos that hold automatically for interior marks

- **Cone corner.** Suppose ĉ3 is regular (a 45° or 90° corner). The straight continuation is then the half-turn, which lies in the corner's local reflection group. So the second half retraces the first, and t̂ lies over S. That contradicts S ≠ T.
- **Non-wall direction.** Suppose u + v is axial or diagonal. Then |u + v| ≤ √2, and each half stays inside the full fan square of its endpoint. The fan squares of S and T then share ĉ3, so S and T are portal-adjacent or diagonally adjacent full fans. The fan structure excludes both (compare seed §10.2).
- For endpoints that aren't interior marks, keep both provisos.

## Converse: the rule is 2 out of 3

Start from one edge ŝ → t̂ with vector 2w and a known π-side.
- Choose any u with det(u, w) of the sign that puts Δ = conv(0, 2u, 2w) on the π-side. There are infinitely many such u, one for each element of u₀ + Zw.
- The same lift gives two edges, ŝ → ι(2u) and ι(2u) → t̂, with vectors 2u and 2(w − u). Condition 3 holds at the apex by construction.
- The apex ι(2u) lies over some A point of the closed room, which may be singular.

So every seed is a triangle composition of two shorter edges, its Farey parents. Repeating the step reaches unit edges, with vectors 2e1, 2e2, or 2(e1 ± e2), and the room's tiles determine those locally.

In the chart M ∈ SL2(Z) with M e1 = u and M e2 = v, Δ becomes conv(0, 2e1, 2e1 + 2e2). So each move is a local identity in one orbit state. The rule adds no orbit data. Its value is that it states composition geometrically, so a proof can try to choose apexes from the fan tree.

## Examples

**Fan distance 2 is one move with apex M.**
- Take S = (0,0), M = (2,0) as the upper half-star, and T = (4,0), as in seed §10.3.
- Seed §10.4 shows that one horizontal ray at (2,1) is a wall. Mirror x → 4 − x and swap S and T so that the ray toward (3,1) is the wall.
- Edge S → M has vector 2(1,0). It runs straight through the 270° portal corner (1,0), and its π-side is up (left).
- Edge M → T has vector 2(1,1) through B = (3,1). Its left π-sector sweeps 45° to the wall ray toward (2,1), reflects, and sweeps 135° more. It leaves toward (1,−1), which reaches T.
- M is a 180° A point, so it's regular. det((1,0), (1,1)) = 1, and both π-sides are on the left.
- The composite is the (2,1) seed through (2,1) from seed §10.4 with k = 2.

**The straight fan-distance-3 corridor doesn't close along the tree.** This is the room S = (0,0), M1 = (2,0), M2 = (4,0), T = (6,0) with W = 40. Reading its tiles gives:

| Fan center | Angle | Shape |
|---|---|---|
| S, T | 360° | full |
| M1 | 180° | upper half-star (regular) |
| M2 | 270° | A corner (singular, n = 3) |
| (2,2) | 135° | A corner |

- Tree edges along the corridor all have vector 2(1,0), so any two of them have det 0. A move needs an off-axis edge.
- From M1 in direction (1,1), corner (3,1) has the quadrants of M1, M2, and (2,2), with walls on the rays toward (3,2) and (4,1).
  - The left continuation reflects at the vertical wall and reaches the 135° corner (2,2).
  - The right continuation reflects at the horizontal wall and reaches M2.
- So the move with apex M1 and u = (1,0) produces S → (2,2), not S → M2. Any further move from (2,2) or M2 needs condition 3 at a singular apex.
- This matches the room's shortest seed, w = (2,5) with |w|² = 29. Its Farey parents are (1,2) and (1,3). This audit didn't locate their apexes.

## Plausibility of a planar global lemma

- **For it.** The rule is exact and local, it is reversible, and fan distance 2 is a single move along the tree.
- **Against it.**
  - Edges along a straight tree path are collinear, so every move needs an off-axis edge. The tiles at the B corners beside the path fix that edge's π-side.
  - In the fan-distance-3 corridor, the first move already leaves the tree at a singular A corner.
  - No quantity that the fan tree controls is known to decrease along a chain of moves.
- **What a lemma would need.** A strengthened induction on fan distance, for example: "S and T have a seed whose half-vector lies in a prescribed Farey interval, with a prescribed π-side." No such hypothesis is in hand.
- **Scope.** A third edge alone gives no nonzero slide response. Main §26.1 offsets and §31.1 collar counts are still required, as the brainstorm says.

## Response to the brainstorm's objections

| Objection (lines 122–129) | Status |
|---|---|
| Arbitrary connections lack det-one directions or compatible sectors | Agreed. Conditions 1–2 are real restrictions. |
| An intermediate A corner can be singular | Resolved by condition 3, which states the exact prong. |
| A connected graph of seeds isn't enough | Agreed. The corridor example shows the tree path doesn't supply the moves. |
| The fan structure isn't shown to supply a chain | Open. See the plausibility section. |
| The third edge gives no nonzero response | Agreed, and out of scope here. |
