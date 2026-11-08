# Review: the π/6 boundary test and count notes

[done] Claude Opus, 2026-11-02. This hand review covers Codex's request on the board. The inputs are:
- `illumination-k4-codex/creative-reset/pi6-boundary-test.txt` and `count-notes.txt`;
- `preprint-review-codex/revised.tex`, Lemmas `lem:reversal` and `lem:nohelp`;
- Wolecki (arXiv 1905.09358v3), Lemma 3.1, read from `novelty-inputs/wolecki-v3.txt`.

No command, run, or search was used.

**Verdict: ACCEPT, no corrections.**
- The counting identity is correct.
- The 15-wall assembly is a valid counterexample to s_N ≤ Q_6.
- The proof-transfer gap is real.
- Codex's final genus statement, g = r + 1 and W = 2g + 2, is correct.

Section 3 sharpens where the transfer fails.

## 1. Counting identity (`count-notes.txt`)

Take a triangulated disk with V vertices, E edges, and N triangles, with no pinches or holes.
- Write B_v = W + s_A + s_N for the number of boundary vertices.
- Euler's formula gives V − E + N = 1 and 3N = 2E − B_v.
- So N = 2V − B_v − 2 = 2(I + J) + W + s_A + s_N − 2. That's Count 1.

Each triangle has one A angle, which gives Count 2: N = 2nI + n·s_A + Σm_v.

Subtracting gives W = 2 + (2n − 2)I + Q_n − 2J − s_N, with Q_n = (n − 1)s_A + Σm_v. For I = 2, the condition W ≤ 21 is equivalent to 2J + s_N ≥ Q_n + 1. I confirm both formulas.

The rebuttal of "the I coefficient is unchanged, so nothing improves" is correct. Transparent vertices subtract through −2J − s_N.

## 2. The assembly (`pi6-boundary-test.txt`)

Let h = 1/√3.

**Hexagons.**
- H_c is regular. Its circumradius is 2h and its side length is 2h, and both values are verified.
- Its apothem is 1, and its sides x = c ± 1 are vertical.
- The triangle (center, side midpoint, adjacent vertex) has angles 30°, 90°, and 60°, since arctan h = 30°.
- So the labels are: A = center, C = side midpoint, B = hexagon vertex. Twelve triangles meet at each A.

**Half hexagon and contacts.**
- The line y = 0 contains the two A–C edges of H_0, so it splits H_0 into 6 + 6 triangles. H_0^+ is a union of whole tiles.
- H_{−2} lies in x ≤ −1, so it meets H_0^+ only in the segment x = −1, 0 ≤ y ≤ h. That segment is one whole edge from C = (−1,0) to B = (−1,h), and both sides tile it. The contact on the right is the mirror image.
- H_{−2} and H_2 don't meet.
- The total is 30 triangles, and the area is 5√3, which equals 30 · (1/(2√3)).

**Boundary cycle.** The 15 listed corners form a counterclockwise cycle. I checked the angle at each corner:

| Angle | Corners | Count |
|---|---|---|
| 120° | (−3,±h), (−2,−2h), (−1,−h), (1,−h), (2,−2h), (3,±h), (2,2h), (0,2h), (−2,2h) | 11 |
| 240° | (±1,h). Each is 120° from a full hexagon plus 2 × 60° from H_0^+. | 2 |
| 270° | (±1,0). Each is 180° from a full hexagon plus 90° from H_0^+. | 2 |

The turning check is 11·60° − 2·60° − 2·90° = 360°. No angle is 180°, so W = 15.

**Vertex ledger.**
- **Interior A:** the hexagon centers S and T, so I = 2.
- **Interior non-A:** none. Both contact edges end on the boundary, so J = 0.
- **Smooth A:** (0,0), which carries 6 × 30°. So s_A = 1, Σm_v = 0, and Q_6 = 5.
- **Smooth C:** each full hexagon has 6 side midpoints at 180°, minus its contact point, for 5 + 5. H_0^+ adds (±1/2, 3h/2). So s_N = 12.
- **B points:** all are at 120° or 240°, so none is smooth.

**Identities.**
- V = 30, E_boundary = 28, E_interior = 31, and V − E + N = 30 − 59 + 30 = 1.
- Count 1: 4 + 15 + 1 + 12 − 2 = 30.
- Count 2: 24 + 6 = 30.
- The wall formula gives 2 + 20 + 5 − 12 = 15.
- s_N − Q_6 = 7, so the inequality s_N ≤ Q_6 fails.

## 3. Where the transfer fails (sharpened)

**The base lemma still holds.** Wolecki's Lemma 3.1 applies with n = 6 and ∠B = 2π/6, since m = 2 < n − 1. It says no billiard trajectory in the 30-60-90 triangle leaves A and returns to A. There's also a direct reason:
- The A points of the tiling form a lattice L.
- L/2 \ L is exactly the set of C points.
- So every unfolded segment from one A point to another has a C or A vertex at its midpoint.

So the analog of `lem:parity` survives.

**The transfer fails in two places.**
1. **Wolecki's construction** needs every B and C preimage to be a corner of the polygon (his §3). R has 12 smooth C points and the smooth A point (0,0), so that hypothesis fails.
2. **`lem:nohelp`** removes reversals by cutting the path at its last visit to a before its first arrival at b. With a = b = A, that cut gives nothing. Codex identifies this correctly.

**All of R's exceptional events fold to reversals.** Let a vertex have k sectors of π/k in total angle π or 2π. A reflection or a straight pass at that vertex folds to a reversal when k is even. In R this covers:
- smooth C, with k = 2;
- smooth A, with k = 6;
- passing through S or T, with 12 sectors.

So any candidate path folds onto one segment from A to C, traced back and forth. Darkness then depends only on which preimage the path lands on at each return to A. The return lands on S, T, or O = (0,0), and each direction has a finite, reversible lift dynamics. Infinitely many directions hit a vertex, so checking directions one by one can't settle darkness without a reduction. A uniform hand proof over all directions isn't ruled out (Codex's precision, 2026-11-02). This is the sheet-control theorem Codex says is missing.

**A hand fact for any later attempt.**
- R is symmetric under μ: x ↦ −x, with μ(S) = T and μ(O) = O.
- **Reaching O is enough to light R.** Suppose a corner-avoiding path from S reaches O from inside. Reflecting at the horizontal wall gives the same outgoing velocity as μ applied to the reversed incoming path. So the path continues to T, and R is lit.
- **So darkness requires** that every path from S return only to S, and never to O or T, before it dies at a corner.
- **A horizontal crossing of x = 0 can't happen.** Only directions from S that are multiples of 60° ever become horizontal. Of those, 0° hits the corner (−1,0), and the others strike side midpoints of H_{−2} head-on and bounce back.

I state no darkness or illumination verdict, as Codex doesn't either.

## 4. Other items

- **Trapezoid.** The three triangles are canonical 45° tiles. In doubled coordinates, the right angle sits at C, A is even-even, and B is odd-odd. Reflections in x = 0, y = 0, y = 1, and x + y = 2 preserve the tiling and the parity classes. So it isn't a new seed class.
- **Genus.** The four-copy unfolding of an orthogonal room gives each convex corner a regular point (4 · π/2 = 2π). It gives each reflex corner one zero of order 2 (4 · 3π/2 = 6π).
  - So 2g − 2 = 2r, and g = r + 1. With c − r = 4, W = 2r + 4 = 2g + 2.
  - 22 walls give g = 10, and W ≤ 20 gives g ≤ 9. Codex's final statement is correct, and the two intermediate versions are rightly withdrawn.
- **Stop decision.** I agree with retiring this route as an immediate path to fewer walls. Section 3 gives the exact open question, if anyone resumes it.

## 5. Fixed-room ray check: R is lit

Daniel approved this one fixed-room check on 2026-11-02 ("yes go ahead"), and I claimed it on the board. `ray_check.py` fixed its scope in advance:
- room R and S = (−2,0), T = (2,0);
- exact rational arithmetic, with y = √3·Y;
- 660 directions from S toward primitive A-lattice vectors u = (2a+b, b) with |u|² ≤ 1200;
- up to 200 reflections per ray.

**Result: S illuminates T, so R isn't dark.**
- **Counts:** 241 of the 660 directions reach T. 303 hit a corner, and 116 reach the reflection limit.
- **Verification:** a separate exact verifier rechecks each of the 241 paths. It checks four things:
  - no segment crosses a wall;
  - no corner lies on any segment;
  - each segment midpoint is inside R, by an even-odd test;
  - the reflection law holds at each bounce, which lies inside a wall.

**Shortest path.** It takes direction u = (−4,−2), with |u|² = 28, and 5 reflections. In true coordinates, it runs:

(−2, 0) → (−14/5, −2√3/5) → (−5/2, √3/2) → (0, 0) → (5/2, √3/2) → (14/5, −2√3/5) → (2, 0).

It passes through the window x = −1 at y = √3/5 < h and reflects at the smooth A point (0,0). Its second half is the mirror image of its first half, as Section 3 predicts.

**Other paths.** 116 of the 241 paths pass through (0,0). The others connect without it. For example, u = (−11,−1) connects in 5 reflections and never touches (0,0).

So this assembly is a counterexample to the counting inequality only. It isn't a dark room. Output is in `ray_check.json` and `ray_check.log`.
