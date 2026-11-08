# Critique and proposal: dark pairs in fewer than 24 walls

**Bottom line.** Deduction 1 needs a repair, but the repaired bound still leaves nothing new to search. Deduction 2 is correct. Deduction 3 is valid but aims at the wrong object. Physical convex corners absorb rays even though they're regular on the unfolding. My strongest suggestion is an exact finite all-ray decider for the 45-45-90 setting. It's a certificate method, not a new darkness mechanism. It may already be standard; check Hubert–Schmoll–Troubetzkoy, "Modular fibers and illumination problems."

## Deduction 1: strict edge-to-edge bound

The Euler step is right. For a disk triangulation, N = V_b + 2V_i − 2. That gives W = N − 2I + 2 − S. Each tile has one A vertex, so A-stars use disjoint tiles.

**Gap in the right-triangle bound.** "N ≥ 3nI ⇒ W ≥ 6n−4" ignores the −S term. The third tile at a star's right vertex can belong to a smooth A half-star. Here's the repair:

- Each third tile has its own A vertex.
- That A vertex can't be a full star, because full-star tiles pair at C and four tiles would make C interior.
- Each smooth half-star has at most 2 unpaired end tiles. Its paired tiles create new right-angle fans that need their own third tiles.

So N ≥ 3nI + (n−2)S, and W ≥ (3n−2)I + (n−3)S + 2 ≥ 6n−4 for n ≥ 3. The conclusion survives.

**Case the bound misses: 30-30-120.** With n = 6 and m = 1 (or m = 4), the triangle isn't right-angled. The general bound gives only 4n−2 = 22, which is under 24. This class turns out to be empty for I ≥ 2:

- A full 12-tile A-star is a hexagram.
- Every boundary edge is BC, and each C endpoint already carries two 120° tiles (240°).
- Any tile glued across BC puts three tiles at C. An odd count breaks reflection-consistent labeling: one A lands on a B.
- So the star can't be extended edge-to-edge.
- If you allow the A↔B swap, the effective billiard is the 30-60-90 half-triangle. That triangle needs at least 32 walls.

With n ≥ 8, the bound is at least 30. **Result:** the strict method reduces to the 45-45-90 triangle, with lower bound 20. That's consistent with the need for exceptions in your restricted family.

Also confirm that Wolecki Lemma 3.1 covers generalized trajectories through interior non-A vertices. You need this once B/C exceptions are allowed.

## Deduction 2: degree-3 S₃ cover

This is correct. Riemann–Hurwitz gives 2g−2 = 3·2, so g = 4. Every 0→0 torus segment has a primitive initial piece whose midpoint is a nonzero 2-torsion point. Full ramification makes that point a cone point.

The degree bound holds if the marks lie over a G-fixed base point. Interior physical points have trivial stabilizers, so two marks need two free orbits: d ≥ 2|G|, which is 8 for D2 or 16 for D4.

## Deduction 3: orthogonal no-go

The count c = d + r₀ + 4 against at most d − 3r₀ free slots is valid under the stated assumptions. It excludes only certificates in which every blocker is a cone point.

Tokarsky's and Castro's rooms block with corners that are regular on X. A sound certificate has to mark all corner lifts as absorbers, regular or not. Under that convention the obstruction doesn't apply. It isn't a no-go for rooms.

## Proposal: exact cusp decider on the marked origami

**Assumptions.**

- The room is a 45-45-90 polyform, so its unfolding X is square-tiled.
- The marks are rational points.
- You mark three labeled sets on X: lifts of P, lifts of Q, and all corner lifts (absorbers).

**Certificate (conditional on standard origami facts).**

1. Let Γ′ ⊂ SL₂(ℤ) be the Veech group of the labeled, marked origami. Affine maps permute labeled marked configurations of a finite cover of the marked torus. So Γ′ has finite index, equal to the size of the SL₂(ℤ)-orbit of the labeled origami.
2. Any P→Q connection has a rational direction.
3. If f ∈ Γ′ has derivative M, then f maps unobstructed P→Q segments in direction θ to unobstructed ones in Mθ.
4. So illumination is decided by finitely many directions, one per cusp of Γ′.
5. In each cusp direction the surface splits into cylinders. Check exactly whether each forward trajectory from a P-lift reaches a Q-lift before an absorber.

This is an all-ray proof with no direction sampling. It allows joint blocking by many corners (your mechanism A) with no universal midpoint trap and no parity structure. Marks need not sit at tile vertices: refine the grid, and the exception count stops mattering.

**Construction mechanism.** Combine this with C, applied to tile moves rather than abstract corner straightening.

1. Start from your certified 24-wall room.
2. Enumerate local tile additions and removals that lower W by 1 to 3 while keeping the polygon simple.
3. Also enumerate rational mark positions (refined lattice, denominator 2 or 4).
4. Run the decider on each candidate.

Each candidate gets an exact verdict.

**First decisive test.** Rebuild Castro's 24-wall room as a labeled origami and compute the index of Γ′.

- The decider must return "dark" on Castro's room and "lit" on a known lit 45-45-90 room.
- If the index is computable (roughly ≤ 10⁷ orbit elements), run the single-move neighbourhood next.

**Likeliest fatal failure.**

- **Index blow-up.** Labeled marked-point orbits can be very large.
- **No sub-24 dark pair in the neighbourhood.** Room-by-room verdicts don't prove a global negative.

Without a structural reason to expect darkness in the neighbourhood, this becomes the blind search you want to avoid.

## Alternative: off-lattice marks in orthogonal rooms

This is materially different. Take vertices in ℤ² and base torus ℝ²/(2ℤ)².

- For a reflected Q-image in a given sheet, path midpoints are (P ± Q)/2 + ℤ², with signs depending on the sheet. There are four cosets.
- With absorbing corners, a dark pair needs every reachable midpoint lift in all four sheet cosets to be a corner lift. This is a two-torsion sheet-routing condition in your D2 setting.
- For marks in (½ + ℤ)², some cosets are half-integer points, where no corner can sit.

The obstruction is a coset mismatch: some sheet cosets contain no corner positions. Your mechanism B must defeat it.

I don't see a way past it without D4 symmetry, which returns you to the 45-45-90 setting. So I judge this unpromising.

## Missing lemma

You need a structural statement that predicts where dark pairs can occur, not just a way to verify them. One version would characterize dark pairs on a square-tiled room surface through cusp data of Γ′. An example: "P, Q dark ⇔ every cusp's cylinder decomposition separates P-lifts from Q-lifts by absorbers."

That would turn the decider into a constructive tool: design cusp cylinder separations with few corners, then build the polygon from them. Until someone proves that, the decider certifies candidates but doesn't generate them.
