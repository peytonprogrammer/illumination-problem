# Claude review: refolding gate, lattice obstruction, and reset arguments

Date: 2026-10-31. Inputs: Codex's `refolding-bound.md`, `refolding-lattice-obstruction.md`,
and `reset-findings.md` in `.context/illumination-new-mechanisms/`. No rays were traced.

## Verdict

- **Refolding gate, sections 1–4: accepted.** The data reproduces independently and the
  stabilizer and angle-sum arguments hold.
- **Lattice obstruction, steps A–E: accepted.** It's conditional only on the strict-family
  minimum of 24, which Claude confirmed separately.
- **Reset transfer lemma: accepted.** The compactness criterion is correct but gives no
  construction.
- **Consequence:** refolding any of the three known dark surfaces (the 20-wall slit, 22-wall
  contact, and 24-wall simple rooms) can't give a simple room below 24 walls.

## Independent data check

`claude_unfold.py` rebuilds each surface as room × D4. It doesn't use Codex's
`illumination_cover` or `illumination_midpoint` helpers. Vertices are glued only through
edges, so the 22-wall contact point splits correctly.

| Control | Genus | Cones | Fix(ρ) | ρ-fixed mass | W = 2 + mass/4 | Regular non-fixed | Lattice |
| --- | ---: | --- | ---: | ---: | ---: | --- | --- |
| 20 slit | 22 | 4×m2, 17×m3, 1×m5 | 26 | 64 | 18 (gate fails) | 16 = marks | 2Z² |
| 22 contact | 25 | 21×m3, 1×m7 | 32 | 80 | 22 | 16 = marks | 2Z² |
| 24 simple | 28 | 23×m3, 2×m5 | 34 | 88 | 24 | 20 ≠ marks | 2Z² |

The table matches Codex on every number. Other checks:

- On all three controls, every source and target lift lies over 0 mod 2Z².
- The m7 cone lies over (1,1).
- On the 20-wall slit, the m2 cones aren't ρ-fixed.
- Each surface has one translation automorphism, the identity. The search maps triangles to
  triangles. That's complete because a translation must map the unique m5 or m7 cone class at
  residue (1,1) to itself. So its vector is in 2Z², and it preserves the triangulation.

## Proof review notes

**Local gate.** A boundary corner with a dihedral stabilizer of order 2q has angle πm/q. The
derivative is faithful, so gcd(m, q) = 1. An m3 cone rules out orders 2 and 6. An m5 or m7
cone rules out order 4. An m2 cone fails q ∈ {1, 2, 4}. All correct.

**Corner set is Fix(ρ).** At order 8, a corner's stabilizer has even q, so it contains the
central half-turn r² = ρ. Conversely, a ρ-fixed point has a rotation in its stabilizer. Its
image can't be a flat interior point or a smooth side point, because gcd(m, q) = 1 with q ≥ 2
rules out m = q.

**Wall formula.** A corner orbit has size 8/(2q). So θ = (2π/8)·Σ m over the orbit, and the
angle sum gives W = 2 + Σ_{Fix ρ} m / 4. This is intrinsic to the surface. I also checked
R = n + 8 − 4W = 4(N − W + 2) from Euler and Σ(m−1) = 2g − 2.

**Steps A–E.**

- A: GL(2,Z) has one conjugacy class of D4 subgroups. Its invariant forms are scalar.
- B: A free 8-point orbit inside an 8-point set equals the set. So each h fixes the
  source residue 0, and its translation part is in 2Z².
- C: ρ acts on the torus as x ↦ −x. Its fixed points lie over Z², which is exactly the image of
  the square vertices. The cover is unramified over the open disk, so it's trivial, and
  developing one sheet places every corner at an integer point.
- D: A reflection y ↦ Dy + v with v ∈ 2Z² fixes x = k, y = k, x − y = 2k, or x + y = 2k.
  In each unit square, exactly one diagonal of that arrangement appears, the A–B diagonal. So
  the arrangement is the canonical tiling.
- E: An interior or smooth-boundary B/C point lifts to regular square vertices that aren't
  ρ-fixed. Those are exactly the marks, which lie over 0. A B/C point lies over a nonzero
  residue, which gives the contradiction.

The quotient would be a strict canonical simple room with W = 22, which contradicts the
minimum of 24. The solver-free n=4 bound in `../tokarsky-n/` gives a separate check on that
minimum.

**Reset transfer lemma.** A billiard path in X/H lifts to a straight segment in X. It runs
from a lift of the source, which lies in A, to a lift of the target, which lies in B. It
avoids every corner preimage, and those contain Σ, so the old darkness contradicts it. The
argument is correct. Conjugate D4 actions give similar quotients, because the D4-invariant
metric is unique up to scale.

**Compactness criterion.** Correct. A transverse finite-reflection path keeps its unfolded
itinerary under small perturbation, so U_L is open. The finite-intersection argument then
applies. It's an existence equivalence only, and it supplies no candidate family.

## Recommendation

Retire refolding of the existing surfaces. Codex's corollary N ≥ W + 6 is a cheap filter for
any sub-24 canonical room with four or more exceptions. Use it to prune the ≥4-exception
search before any ray work.
