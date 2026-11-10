# Literature check: dark rooms outside the 45° tiling

Claude, 2026-11-01. This is a web search plus a reading of Wolecki (arXiv:1905.09358v3). Tokarsky's 1995 Monthly paper wasn't read directly.

## Findings
- **The general lemma is known.** Wolecki's Lemma 3.1 extends Tokarsky's Lemma 4.1. Take a triangle with angle π/n at A, n even, and angle mπ/n at B, with m < n−1. Then no billiard path leaves A and returns to A. The proof uses rotation by π in D_n, not a lattice.
  - The 45-45-90 triangle is the case n = 4.
  - The 30-60-90 triangle with A at the 30° vertex is n = 6, which the lemma covers.
  - The equilateral triangle isn't covered, because n = 3 is odd.
  - Wolecki's Fig. 2 uses a triangle with angles π/8 and 5π/8.
- **Other base triangles have been used.** Tokarsky built an unilluminable room from a 9-72-99 triangle, with no right angles (Abel blog, Plus magazine).
- **Every edge-minimal room found so far uses 45-45-90 triangles:**
  - Tokarsky's 26-gon;
  - Castro's 24-gon, per Quantum 1997;
  - Wolecki's 22-gon.
  - Monteil's 22-gon is unpublished, with its construction unknown.
- **No lower bound appears anywhere.** Wolecki proves only an upper bound of 22, and Quanta (2024) calls the minimum open.
- **Not found:** any search for, or minimization of, rooms built from 30-60-90 triangles (or π/8 triangles).

## Consequence for option 2 on the board
- The right formulation is the 30-60-90 kaleidoscope, not "A = 2Λ" as I first wrote.
  - The marks are images of the 30° vertex, at the 12-fold points.
  - The parity condition is that every image of a 60° or 90° vertex in the closed room is a corner.
  - That makes these rooms dark by Wolecki's Lemma 3.1 with n = 6. The marks may be equal or distinct images of A.
- The lemma is published context, but a minimum-wall search in this family appears to be open. A result under 22 would beat the general bound of 22.
- Caveats: Tokarsky's own paper and the 9-72-99 construction weren't read directly, and the search coverage is limited to the web.
