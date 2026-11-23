# Why does the Apisa-Wright argument fail for square-tiled rooms, and does any of it survive at r <= 8?

Read-only, no searches, under 1,200 words, PROVED / CITED / GUESSED. Do
mathematics. Paths are under
`.context/illumination-generalization-2026-11-06/fable/directions-2026-11-09/`.

## The core problem
Square-lattice orthogonal room P with W <= 20 (r <= 8). Its unfolding M is
a square-tiled surface (torus cover); DP is a pillowcase cover in
Q(1^r, -1^(r+4)). Proved: no fold (parity factor, any base) separates two
interior same-class lattice points when r <= 8 (`d2-review/review.md`
plus the k <= 6 theorem). So the 22-wall minimum on the square grid is
equivalent to: no room with r <= 8 has a dark pair without a fold.
Every known dark pair comes from a fold.

## What Apisa-Wright prove off torus covers
Read `d32-fold-minimum/literature.md` (exact quotes of Thms 1.1, 1.3,
1.4, 3.6, 3.10, Lemma 3.8). Thm 3.6: finitely blocked x1, x2 on (X, w)
are both M-periodic (or zeros) or have the same image under the minimal
half-translation quotient. It excludes torus covers, where every pair is
finitely blocked and every point with rational coordinates is periodic.

## Questions
1. Locate precisely where the proof of Thm 3.6 (and Thm 1.3) uses "not a
   torus cover": is it (a) the existence of infinitely many non-periodic
   points, (b) the orbit-closure classification of marked points
   (rel/rank), (c) the finite-blocking-to-cover step, or something else?
2. Darkness is stronger than finite blocking: the blocking set must be the
   set of corner preimages, and the room's Klein-four symmetry acts. On a
   square-tiled surface every marked configuration has a closed SL(2,Z)
   orbit, so orbit closures carry no information. Replace "orbit closure"
   by a finite object: the Veech group Gamma of (M; corners) acting on
   pairs of lattice points, or the pure-braid orbit of the pair in the
   pillowcase cover. State an analogue of Thm 3.6 for this finite action
   ("dark implies a block system / cover collapsing the pair") and
   identify the exact step whose analogue is unproved.
3. Does anything survive with the hypothesis r <= 8 (few zeros: at most
   8 cone points of angle 3 pi, r + 4 poles)? For example: a counting or
   cylinder argument that, for small r, the Gamma-orbit of a pair must
   contain a configuration where both points lie on the boundary of one
   cylinder (lit), unless the orbit respects a block system. Test any
   proposed lemma against the known dark pairs: the 22-wall room (r = 9,
   fold of degree 3 over the 5-cell staircase) and P6 (r = 12) in
   `d30-rigidity-proof/rigidity.md`.
4. Verdict: does a torus-cover analogue of Apisa-Wright look provable for
   r <= 8, and what is the first lemma to try?

End with a probability.
