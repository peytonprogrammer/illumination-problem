# Research brief: the smallest unilluminable simple room

Date: 2026-10-31. Author: Claude, as research lead. Companion to `report.md`.

## Bottom line

- Inside the framework every known small dark room uses, **24 walls is optimal
  for simple polygons**, assuming our computations are correct. That framework
  is Tokarsky's lemma as generalized by Wolecki. Castro's 1997 24-gon attains
  the minimum.
- The rooms with fewer walls in the literature, a 22-gon and a 20-gon, aren't
  simple polygons: one has a boundary contact and the other a slit.
- We can find no published statement that 24 is minimal for any class of
  rooms. The result appears to be new.

## Literature: what's known

| Year | Result | Room type |
| --- | --- | --- |
| 1958 | Penrose: a room with dark regions | Curved walls |
| 1995 | Tokarsky: a 26-sided polygon with two mutually dark points, from 45-45-90 reflections | Simple |
| 1996 | Tokarsky: 20 sides, cited by Wikipedia | Has a slit, per our reconstruction of the image |
| 1997 | Castro: 24 sides | Simple; our search reproduces it |
| 2016 | Lelièvre–Monteil–Weiss: in a rational polygon, each point fails to light only finitely many points | Theory |
| 2017–21 | Apisa–Wright: finite blocking reduces to periodic points and covering constructions | Theory |
| 2019/2024 | Wolecki: finitely many dark pairs; a 22-gon; Lemma 3.1 generalizes Tokarsky's lemma | 22-gon has a boundary contact |
| — | Monteil: an unpublished 22-gon, cited by Wolecki | Unknown |

Wolecki's Lemma 3.1: for a triangle with angle π/n at A and mπ/n at B, with n
even and m < n−1, no billiard path goes from A back to A. If a polygon is
tiled by reflected copies, every image of B and C is a corner, and two
interior points fold to A, then those two points are mutually dark.

We found no 2023–2026 paper that improves the side count or proves a lower
bound. The minimum is listed as open.

## Where our work sits

1. **Zero exceptions, 45° tiling (Tokarsky–Castro rooms):** no simple room has
   fewer than 24 walls. Codex proved this, and Claude independently confirmed
   it. **Solver-free certificate (2026-10-31):** `tokarsky-n/claude_n4_bound.py 23`
   branches over every allowed local pattern from a full star at (0,0), pruning
   when walls exceed 23. It visits 7,871,705 nodes and finds 213,576 closed
   configurations. None has a second full A star, and none reaches the window
   edge. The WMAX=24 control finds two-star configurations at 24 walls. Claude's general solver
   (`tokarsky-n/claude_tokarsky_min.py 4`) reproduces Castro's 24 as the
   optimum, both with fixed marks and with the marks placed freely.
2. **One to three transparent B/C points:** these rooms aren't dark by the
   lemma, so every candidate needs an exact ray search. Every placement is
   excluded below 24.
   - Two exceptions, three stars, and two-star placements (3,0) through (2,1)
     were excluded by Codex and confirmed by Claude.
   - (2,0) and (1,1) were excluded by Claude's cut loop and independently
     verified by Codex (`.context/three-triples/three-exception-complete.md`).
3. **New: the 30-60-90 tiling, n = 6, the only other reflection tiling the
   lemma covers.** No simple room has two interior A points.
   - Any valid simple room with an interior A point has at most 24 tiles. The
     same maximum holds at radius 3, 5, and 7.
   - With two stars, every placement is INFEASIBLE, including free placement
     within radius 5.
   - Mechanism: C has room for at most 3 tiles and B can't hold exactly 3, so
     the region around an interior A is locked in place.
   - **Solver-free certificate:** `tokarsky-n/claude_n6_enumerate.py`
     branches on every allowed local pattern, starting from a full star. It
     uses only the per-vertex rules: one sector, B ∈ {1,2,4,5} tiles, and
     C ∈ {1,3}. It visits 5,975 nodes in 2 s and finds 416 closed
     configurations. The largest has 24 tiles, none contains a second full A,
     and none reaches the window edge.
   - Controls with the same code at n = 4: unseeded, growth is unbounded,
     reaching 151 tiles and the window edge 4,343 times. Seeded with stars at
     (0,0) and (4,0), it finds a closed two-star configuration.

   For n ≥ 8 the triangle doesn't tile the whole plane by reflection. That
   alone doesn't exclude a finite planar patch: Codex points out that the
   (π/8, 3π/8, π/2) triangle forms a planar full A-star, an octagon. Whether
   some finite patch has two full A-stars with every B and C image a corner is
   **open**. Our claim covers only n = 4 and n = 6.

**Claim:** among simple polygons whose darkness comes from the Tokarsky–Wolecki
lemma with the 45-45-90 or 30-60-90 triangle, 24 walls is the minimum, and
Castro's room attains it. For the 45° triangle, this covers up to three
transparent B/C points. Finite patches of triangles with n ≥ 8 remain open.

The claim rests on three conditions:

- The CP-SAT INFEASIBLE results for one to three exceptions are correct. No UNSAT
  proof file exists. The zero-exception case no longer depends on CP-SAT.
- Our room model is correct: corners count as walls, and every image of B and
  C is a corner.
- For n = 6, the exhaustive enumeration doesn't rely on CP-SAT.

## Open problems, ranked by leverage

1. **Four or more transparent exceptions at 45°.** The counting identity
   W = 2 + 6I + Q − (2J + s_N) lets exceptions lower W. The "at most three"
   restriction is our largest gap. Either find a lemma that bounds the number
   of exceptions, or extend the cut loop.
2. **Darkness without the lemma.** Lelièvre–Monteil–Weiss and Apisa–Wright tie
   finitely blocked pairs to periodic points, and for torus covers to midpoint
   constructions. A dark pair in a simple room that the lemma doesn't explain
   would need one of these mechanisms. That theory could bound the search
   space, or point to new constructions.
3. **Exact darkness is now decidable (2026-10-31).** `exact-dark/claude_origami_dark.py`
   decides darkness of any canonical room through the SL(2,Z) orbit of its unfolding,
   with no ray bound. It agrees with 2,435 of 2,435 verified-lit rooms. So the cut loop's
   only remaining incompleteness is the model's search space, not "unlit" rooms.
4. **Certificates.** Re-encode the final INFEASIBLE models as SAT with DRAT or
   LRAT proofs and check them, or formalize the lemma and the reduction in
   Lean. Either removes the trust in CP-SAT. The zero-exception case is already
   solver-free (`tokarsky-n/claude_n4_bound.py 23`).
5. **n = 6 is done.** The exhaustive enumeration is a checkable proof. A
   prose version would be the 416-case tree, which is too long to read; the
   script is the proof.
6. **Write-up.** The paper would be titled roughly "Castro's 24-gon is
   optimal among simple Tokarsky rooms," with the computer-assisted parts and
   the certificates in an appendix.

## Sources

- [Wolecki, *Illumination in Rational Billiards*, arXiv:1905.09358](https://arxiv.org/abs/1905.09358)
  ([HTML v3](https://arxiv.org/html/1905.09358v3))
- [Illumination problem, Wikipedia](https://en.wikipedia.org/wiki/Illumination_problem)
- [Illumination Problem, MathWorld](https://mathworld.wolfram.com/IlluminationProblem.html)
- [Apisa–Wright, *Marked points on translation surfaces*, arXiv:1708.03411](https://arxiv.org/pdf/1708.03411)
- [Apisa, *Billiards in right triangles and orbit closures in genus zero strata*, arXiv:2110.07540](https://arxiv.org/abs/2110.07540)
- [Lelièvre–Monteil–Weiss, as summarized in Wright, arXiv:1703.02268](https://arxiv.org/html/1703.02268)
- [Plus Magazine, *How unilluminating*](https://plus.maths.org/content/mathematical-mysteries-how-unilluminating)
- [Wolfram Demonstrations, *The 26-Sided Unilluminable Room*](https://demonstrations.wolfram.com/The26SidedUnilluminableRoom/)
