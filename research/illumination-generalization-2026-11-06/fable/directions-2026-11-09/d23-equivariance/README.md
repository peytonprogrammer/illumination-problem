# d23: the equivariance hypothesis of d22 is automatic

Date: 2026-11-10. One author; nobody has reviewed this. Exact permutation
arithmetic only.

Status tags: **PROVED** (proof in this file), **CHECKED** (exact computation,
scope stated), **CITED-READ** (statement read in the arXiv source today),
**CITED-D22** (taken from d22, not re-verified), **OPEN**.

## Answer

The hypothesis can be deleted. For every cover in the three dark families, and
every room double, the cover commutes with the reflection. The proof is
elementary and doesn't use `Q_min`. It works for lattice and non-lattice rooms.

Notation: `P` is a strictly simple orthogonal room, `X = D(P)`, `rho` is the
reflection of `X`. For a cover `f`, `R(f)` is the set of regular points of `X`
where `f` is ramified. In each dark family `R(f)` is the family pair, 2 points.

## Lemma 1 (a shared deck germ determines the cover). PROVED

Let `f: X -> Y` and `g: X -> Y'` be half-translation covers of a compact
half-translation surface `X`, both with 2-transitive monodromy. Suppose a point
`Z` of `X` is a ramification point of both. Then `g = phi f` for a
half-translation isomorphism `phi: Y -> Y'`.

Proof.

1. `E_f = {(x, x') : f(x) = f(x')}` is an algebraic curve in `X x X`. Over the
   unbranched part of `Y` its components are the orbits of the monodromy group
   on ordered pairs of sheets. 2-transitivity gives two orbits. So
   `E_f = Delta u C_f` with `C_f` irreducible. The same holds for `g`.
2. Near `Z` the fibres of `f` are the orbits of a rotation `tau` about `Z`.
   If `Z` is regular, `f` has local degree 2 onto a pole and `tau` is the
   rotation by `pi`. If `Z` is a zero, `f` has local degree 3 onto a pole and
   `tau` is the rotation by `pi` in the cone of angle `3 pi`. Both are forced
   by `f* q_Y = q_X`. So `tau` doesn't depend on the cover.
3. The germ `{(x, tau x)}` at `(Z, Z)` lies in `C_f` and in `C_g`. Two
   irreducible curves that share infinitely many points are equal. So
   `E_f = E_g`: the two covers have the same fibres. The induced bijection
   `phi` is a homeomorphism and a local isometry off a finite set. ∎

A version with "primitive" in place of "2-transitive" needs one more step. This
file doesn't write it out, and doesn't need it.

## Lemma 2 (equivariance is automatic). PROVED

Let `f: X -> Y` have 2-transitive monodromy, and let `rho` be an
orientation-reversing isometric involution of `X` that fixes a ramification
point `Z` of `f`. Then `f rho = sigma f` for a unique orientation-reversing
isometric involution `sigma` of `Y`.

Proof. Let `c: Y -> Y^c` be the identity map onto the mirror surface. Then
`g = c f rho` is a half-translation cover with fibres `rho(fibres of f)`.
`E_g` is the image of `E_f` under `rho x rho`, so its off-diagonal part is
irreducible. `g` is ramified at `Z`, with deck germ `rho tau rho = tau^(-1)`,
which lies in `C_f`. Lemma 1 gives `g = phi f`. Put `sigma = c^(-1) phi`. Then
`sigma^2 f = f`, so `sigma^2 = 1`. ∎

On a room double, `rho` fixes every cone point, because cone points are
corners. A zero of `X` over a pole of `Y` is a ramification point of order 3.
So any cover of a room double with 2-transitive monodromy and one 3-cycle over
a pole commutes with the reflection. A ramified wall point also suffices.

## Theorem. PROVED, given CITED-D22

Let `P` be a strictly simple orthogonal room with at most 20 walls and any side
lengths. Let `f: D(P) -> Y` be a half-translation cover of degree at least 2
onto a surface with at least 5 poles.

1. If `f` belongs to one of the three dark families, then `f` commutes with
   `rho`. So `R(f) = {S, T}` is `rho`-invariant. Either `S`, `T` are two wall
   points, or they are the two lifts of one interior point.
2. So no two distinct points of `P`, at least one of them interior, have a lift
   pair that is a P1 or P2 pair of a dark family. No P3 family is dark.

The inputs: d22's census (the only dark P1 and P2 families with `r <= 8` are
the three listed; no P3 family is dark) is CITED-D22. The three groups are
`A_4`, `A_5`, `S_5` in their natural actions, each 2-transitive, and every
member has exactly two 2-cycles: CHECKED on all 300 members
(`result_groups.json`). Every member has a 3-cycle, because braid moves
preserve cycle types and each seed tuple has one.

### What the theorem doesn't say

- It classifies pairs that are dark because a whole family is dark. A lattice
  room can have a pair that is dark for a sporadic reason. The computation
  below finds such pairs on square-tiled members (not rooms).
- Two wall points remain possible in all three families. d22 left that open.

## Second proof of item 2, with no reflection (route 2). PROVED

Corollary of Lemma 1 (matching). On any `X`, two covers from the three families
have ramification sets that are equal or disjoint. So the family pairs of all
such covers of `X` form a matching on the regular points of `X`.

A dark room pair with `t` interior needs `{S, T+}` and `{S, T-}` both dark.
If both were family pairs they'd share `S`, so the covers would be equal and
`R` would contain 3 points. That contradicts `|R(f)| = 2`. This argument
covers `f`, `f rho`, and any other cover structure `X` carries.

## Route 1 through `Q_min`, and the correct uniqueness statement

- **CITED-READ.** Apisa-Wright, arXiv:1708.03411, Section 3 standing
  assumption: `(X, omega)` is not a translation cover of a torus. Lemma
  `L:minquad` (3.3 in d19's numbering): any translation covering from
  `(X, omega)` to a quadratic differential is a factor of `pi_Q`. The
  assumption is on the single surface, not on its orbit closure.
- **PROVED, given that lemma.** If `D(P)` isn't a torus cover and `Y` lies in
  `Q(1, -1^5)`, then `Y = Q_min`. Reason: a further cover `Y -> Q'` of degree
  `e >= 2` forces `(k' - 4) e <= 1`, so `Q'` is the pillowcase. The same holds
  for `c f rho`, so `rho` descends. No condition on the monodromy is needed.
- **PROVED.** The orientation cover of `D(P)` is a torus cover iff `P` is a
  lattice room after independent scaling of the axes. A path between two
  vertical walls, followed by its mirror image, is a closed loop with holonomy
  `(2 dx, 0)`. A lattice of periods forces all `dx` to be commensurable.
- So `Q_min` settles non-lattice rooms only. It says nothing on a lattice
  room, which is the case d22 flagged. Lemma 2 covers both.
- **Answer to (b).** On a surface that isn't a torus cover, a cover onto
  `Q(1, -1^5)` is unique up to automorphisms of the base. On a square-tiled
  surface the correct statement is Lemma 1: a cover with 2-transitive monodromy
  is determined by `X` plus one ramification point. Whether a square-tiled `X`
  carries two covers from the families with disjoint ramification is OPEN. It
  can't happen on a room double with `g = c f rho`.

## Mixed pairs (one ramified point over a pole, one free point)

- **PROVED, given CITED-READ.** No such dark family exists off the torus-cover
  loci. Apisa-Wright Theorem `T:cor` (3.6): finitely blocked points are both
  `M`-periodic or zeros, or have the same image under `pi_Q`. A free point
  isn't periodic. The ramified point maps to a pole of `Q_min`, and a free
  point maps to a regular point. Both alternatives fail on a generic member.
  The same theorem excludes dark families of two free points in different
  fibres of `pi_Q`.
- **OPEN.** A single mixed pair on one lattice surface can still be dark.
  Torus-cover loci (type b in d19) are untouched, as in d22.

## Computation (`d23.py`)

Scope: all 300 members of the three families over the base `L(2,2)`: 30, 240,
30 covers. Points: every regular vertex of the scale-2 complex, which is every
half-integer lattice point (82 or 102 per surface).

- LIT means an explicit segment (d22 tracer, `p + q <= 12`) or a LIT verdict
  of the complete decider. DARK means a complete orbit.
- `pair_orbit` is the rule of `hurwitz.marked_orbit` with only the two target
  points labelled. Orbits have at most 1,294 states. It agrees with
  `marked_orbit` on 402 pairs, 0 disagreements (`result_validate.json`).
- Every isometry of each surface is computed. All members have unit saddle
  connections in both axis directions, so every isometry preserves the tiling.

| Family | Surfaces | Pairs | Dark | Undecided | Reflections with a fixed curve | Moving the family pair | Interior-interior patterns | Wall-interior patterns |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P1, `A_4` | 30 | 99,630 | 42 | 0 | 30 | 0 | 0 | 0 |
| P2, `S_5` | 30 | 154,530 | 30 | 0 | 32 | 0 | 0 | 0 |
| P1, `A_5` | 240 | 1,236,240 | 240 | 38,834 | 80 | 0 | 0 | 0 |

- A pattern is `S, T, rho S, rho T` distinct with `(S, T)` and `(S, rho T)`
  not known lit. Undecided pairs count as possibly dark. So "0 patterns" rests
  on LIT verdicts only.
- For `A_5`, pairs over different pillowcase corners were decided only when a
  candidate pattern needed them. The 38,834 undecided pairs are of that kind.
  All 240 dark pairs there are family pairs.
- The 12 extra dark pairs in the `A_4` family sit on 6 members. Each is a
  same-fibre pair over the midpoint of a long wall of `L(2,2)`. This is d22's
  uncovered case "P3 with `y` on a wall". None is a mixed pair.
- No isometry of any member moves the family pair (448 isometries). No
  reflection fixes every cone point, so none of the 300 members is a room
  double. The pattern test is therefore a cross-check, not a search over rooms.

## Open

- Wall-point pairs in the three families (d22's open item). Lemma 2 shows this
  is the only way a family pair meets a room.
- Sporadic dark pairs on lattice rooms, including P3 pairs with `y` on a wall.
- Torus-cover families, exotic loci, `r > 8`: unchanged from d22.
- Lemmas 1 and 2 are hand proofs by one author.

## Files

- `d23.py`: `groups`, `validate`, `invol`, `one`, `run`.
- `result_groups.json`, `result_validate.json`, `result_invol.json`,
  `result_run_s2_*.json`, `log_run_s2_*.txt`.

Compute: about 19 CPU minutes, at most 2 processes. Network: one download of
the arXiv source of 1708.03411, deleted after reading.
