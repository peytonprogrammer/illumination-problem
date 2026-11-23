# Review of d16: reduction from real pairs to rational pairs

Date: 2026-11-10. Target: `d16-real-to-rational/reduction.md`, Sections 2 to 6.1.
In scope: Propositions 1 and 2, Lemmas D, R, G, F, Theorem 1, Corollary 1.
Not reviewed: Sections 6.3 to 9, Lemma T', Proposition U, Theorem 2, the code.

Method: I read each proof line by line and re-derived each computation.
One numeric check exists, for task 3 only (`slidecheck.py`). Everything else is
a reading, not a machine check.

## Verdicts

| Statement | Verdict |
| --- | --- |
| Proposition 1 (openness) | CONFIRMED |
| Proposition 2 (twist invariance) | CONFIRMED |
| Lemma D (single points) | CONFIRMED WITH CORRECTION: one proof step is false as written; the statement is true |
| Lemma R (rational and irrational point) | CONFIRMED |
| Lemma G (generic pairs), including case B | CONFIRMED |
| Lemma F (relation families), including item 2 | CONFIRMED WITH CORRECTION: item 3 inherits the Lemma D fix |
| Theorem 1 | CONFIRMED, with "small delta" made explicit below |
| Corollary 1 | CONFIRMED. It stands. |

## The one real defect: Lemma D, first sentence of the proof

The proof says `H` fixes each horizontal tile edge pointwise "because it fixes
the end vertices and its derivative fixes the horizontal direction". That
doesn't follow. At a cone point of angle `2 pi k` there are `k` rightward
horizontal prongs, and two vertices can be joined by several horizontal edges.

Counterexample to the step (not to the lemma): take the 8-square
quaternion-group surface (squares `g` in `Q8`, right neighbour `g i`, up
neighbour `g j`). It has 4 vertices, each of angle `4 pi`. The deck
transformation `-1` fixes all 4 vertices and moves every square. Let `T` be the
horizontal multi-twist with `a = 4`. Then `H = (-1) T` is affine with
derivative `[[1, 4], [0, 1]]` and fixes every tile vertex, but fixes no
horizontal edge.

Fix, one line: `H` maps horizontal edges to horizontal edges, and there are
finitely many, so some power `H^k` maps each edge to itself. `H^k` preserves
orientation and length along the edge, so it fixes the edge pointwise. Run the
proof with `H^k`, `Vt^k`. The orbit under the subgroup is dense, so the lemma
holds as stated.

Effect on later results:

- Lemma R: none. `h^n` and `v^n` fix the lattice lines of `M` pointwise by
  construction.
- Lemma F, item 3: the power of `h x h` that "fixes every tile vertex" of the
  completion doesn't obviously fix the tile edges in the `zeta` chart. Take one
  more power. The conclusion is unchanged.
- Theorem 1, Corollary 1: none.

## Notes on the points you asked me to attack

**(a) Which surface the twists act on.** Correct. Theorem 1 works only on `M`,
one lift pair `(s, t_e)` at a time. It never applies a twist to a room pair.
Item 3 returns to the room along an explicit continuous path, where
`t_{e,delta} = k_e t_{1,delta}`, so the four pairs are again the four lift
pairs of one room pair. Proposition 2, item 4 is right that `G` doesn't act on
room pairs.

**(b) Density.**

- One coordinate rational, one irrational: Lemma D handles it by exchanging `H`
  and `Vt`. A point on a tile edge with the other coordinate irrational still
  lies in an open cylinder of the transverse direction.
- Different twist multipliers: `h` shifts by `Lh eta` in every row. The
  normalised rotation numbers are `Lh eta / c` with `c` rational, so differing
  circumferences change nothing in Kronecker's hypothesis.
- Case B of Lemma G: checked. The rotation vector is `Lh q + Lh eta alpha`
  modulo the period lattice; a multiple kills `Lh q`; the closure is the circle
  `{r alpha}`. For `r` with `1, xi, r` independent, `(s_r, t_r)` has `r1 = 2`.
  Case A (and A') uses only its own rank-2 hypothesis, so it applies. The
  sub-case `alpha_1 = 0` (one point doesn't move) is fine, because
  `det(alpha, beta) != 0` forces `beta_1 != 0`.
- The chain argument in `M x M` works with the invariant "every reached tile
  pair lies in a full cylinder pair".

**(c) Dense orbit plus open lit set.** In `M x M` the lit set is nonempty, so
the step in Theorem 1 is valid. Lemma F, item 4 is conditional ("if some pair of
`F°_0` is lit") and needs no nonemptiness. Nothing claims that a relation
family contains a lit pair.

**Lemma F, item 2.** Checked. `(a, b)` primitive makes
`xi -> (b xi, -a xi)` injective, so the solution set in `T x T` is one torus.
Fibres have size `(deg pi)^2`. I computed the translation part of `h^k x h^k`
in the `zeta` chart: it's `(A - I)(-(n/b) c0)`, which is rational. So a power
is linear on the `zeta`-torus, as the proof asserts. If `(a, b) = (1, -1)` and
`c0 = 0`, the diagonal is a whole component of `F°`; it isn't `F°_0`, because
`s != t`.

**(d) Theorem 1, item 3.** Correct. An explicit bound for "small": `|delta|`
less than `dist(x, Z)`, `dist(u, Z)/|rho|`, `dist(S, boundary)`,
`dist(T, boundary)/|rho|`, and `|S - T|/(1 + |rho|)`. Under that bound both
points are interior, distinct, and off `L`. For `x + delta` rational both
points are rational. They can lie on an interior lattice line (if `y` or `v`
is an integer) but not on a wall and not at a lattice point.

**(e) Corollary 1.** Follows. A dark pair with an irrational point gives, by
item 3, a dark pair of distinct rational interior points.

## Task 3: the known dark room

Theorem 1 is consistent with the room. Its hypothesis is "a dark pair with an
irrational point". If `(1,3), (3,5)` is the only dark pair, no such pair exists,
so Theorem 1 is vacuous there. It predicts no family through a rational pair:
Lemma F needs `z` irrational, and both points of the known pair lift into `L`,
which `F°` excludes.

Numeric check, `python3 slidecheck.py 20` (exact rationals, written from
scratch, no shared code with d16):

- The room has 15 cells; the area matches the shoelace value.
- `(1,3), (3,5)`: no lighting image with `|m|, |n| <= 20`.
- 176 slid pairs of the Theorem 1 shape (either axis, 8 values of `rho`,
  `delta = ±1/d` for `d` in 2, 3, 5, 7, 11, 50): all lit, each by an image with
  `max(|m|, |n|) <= 1`. 16 further pairs were skipped because a point left the
  interior.

This agrees with "no one-parameter family in that room". It's a finite-radius
check, not a proof of darkness.

## Residual risks

- Everything rests on the unfolding lemma, which the source cites as standard
  without proof. I didn't find a problem with it for strictly simple orthogonal
  lattice rooms.
- Corollary 1 reduces real pairs to all rational pairs. It gives no bound on
  denominators, so it doesn't by itself make the check finite.
