# d22: structured pairs over bases with at least 5 poles, r <= 8

Date: 2026-11-10. Exact permutation and rational arithmetic only. One author;
nobody has reviewed this.

## Answer

No counterexample to 22-wall minimality appears. Three dark families exist over
`Q(1, -1^5)`; none exists over `Q(1^z, -1^{z+4})` for `z = 2, 3, 4`.

| Structure | `z`, `delta` | `r` | Tuple (d21 conventions) | Pair | Group |
| --- | --- | --- | --- | --- | --- |
| P1 (new) | 1, 4 | 6 | `(1, 1, (1 2 3), (0 1 2), (0 1)(2 3))` | `{0,1}`, `{2,3}` over pole 5 | `A_4` |
| P1 (new) | 1, 5 | 8 | `(1, (2 3 4), (1 2 3), (0 1 2), (0 1)(3 4))` | `{0,1}`, `{3,4}` over pole 5 | `A_5` |
| P2 (d21) | 1, 5 | 8 | `(1, 1, (0 1)(2 3 4), (0 1 2)(3 4), (0 4 2))` | `{0,1}` over pole 3, `{3,4}` over pole 4 | `S_5` |

The families have 30, 240, and 30 nodes over a fixed base. All three groups are
primitive, so no intermediate cover exists. No P3 (free fold) family is dark.

None of the three passes the interior filter when the cover commutes with the
reflection of the room double (see "Interior filter"). No room was built.

## The finite list

Zeros of `X` are the `delta * z` preimages of zeros of `Y` (a cover in these
strata is unramified over zeros) plus the `t` three-cycles over poles. So
`r = delta * z + t`, and `r <= 8` gives `delta * z <= 8`: `z = 1`,
`delta <= 8`; `z = 2`, `delta <= 4`; `z = 3, 4`, `delta = 2`; `z >= 5` has no
cover. Covers are `(z+4)`-tuples up to conjugation: product 1, transitive,
cycle lengths at most 3, index sum `2 delta - 2`, `t <= 8 - delta * z`.

| `z` | `delta` | covers | braid orbits | P1 nodes | P2 nodes | P3 nodes | dark |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 2 | 10 | 1 | 0 | d21 | 10 | 0 |
| 1 | 3 | 60 | 3 | 0 | d21 | 180 | 0 |
| 1 | 4 | 665 | 8 | 420 | d21 | 3,990 | P1: 1 family |
| 1 | 5 | 8,510 | 16 | 9,570 | d21 | 85,100 | P1: 1, P2: 1 |
| 1 | 6 | 75,168 | 32 | 198,780 | d21 | 1,127,520 | 0 |
| 1 | 7 | 153,440 | 13 | 1,028,220 | d21 | 3,222,240 | 0 |
| 1 | 8 | 62,100 | 14 | 850,140 | d21 | 1,738,800 | 0 |
| 2 | 2 | 15 | 1 | 0 | 15 | 15 | 0 |
| 2 | 3 | 135 | 3 | 0 | 420 | 405 | 0 |
| 2 | 4 | 680 | 4 | 780 | 9,420 | 4,080 | 0 |
| 3 | 2 | 21 | 1 | 0 | 21 | 21 | 0 |
| 4 | 2 | 28 | 1 | 0 | 28 | 28 | 0 |

Cover counts for `z = 1` equal d21's. P1 families at `z = 1`, degrees 4 to 8:
5, 11, 48, 25, 50. P3 families, degrees 2 to 8: 1, 3, 9, 16, 45, 13, 30.

## Method

- `d22.py` builds the square complex of the cover of a room double for any
  strictly simple polyomino base. Poles go in clockwise order, as in d21.
- LIT means an explicit straight segment found by an exact ray tracer
  (`Cx.visible`). DARK means `hurwitz.marked_orbit` completed its orbit.
- `z >= 2`: brute-force enumeration; every node tested on three rooms per
  stratum (`SMALL` in `d22.py`). Every node has an explicit segment
  (`p + q <= 40`). No family grouping is used.
- `z = 1`, P1: every node of every cover tested without family grouping
  (`exh`). At degrees 6, 7, 8 every node has an explicit segment on `L(2,2)`,
  `L(3,2)`, or `L(2,3)`. At degrees 4 and 5 the nodes with no segment number
  30 and 240; they equal the two dark families, and the complete decider
  returns DARK for each on four bases.
- `z = 1`, P3: exhaustive at degrees 4 and 5 (every node lit). Degrees 2, 3,
  6, 7, 8 use family grouping: sheet labels are fixed under braid moves and move by the
  monodromy group when `y` moves. Every family has a lit node on `L(2,2)` with
  `y = (1, 0)`.
- P2 at `z = 1` is a regression check only: the d21 family is DARK on `L(2,2)`,
  `L(3,2)`, `L(2,4)` in the new complex, and the tracer agrees with the
  complete decider on 564 degree-4 nodes.

## Lemma A (why the two P1 families are dark for every base)

Claim: let `S` be an order-2 ramification point over a pole `b`. A straight
segment in `X` from `S` to any point over `b` passes through a 2-cycle over a
pole `w != b`.

Proof. Lift the projected path to the orientation double cover of `Y`. Poles
become regular points, and the lift is a straight segment from the preimage of
`b` to itself, so it runs along a closed geodesic `c`. The deck involution
fixes that point and reverses `c`, so it fixes exactly one other point of `c`.
That point is regular, so it lies over a pole `w != b`. The segment in `X`
passes through a point over `w`, which must be regular: a 2-cycle.

Both P1 families have 2-cycles over one pole only. They are dark for every `Y`.

## Review of d21's hand proof

The proof holds, with two steps to add. First, a segment from `S` to `T` can't
bounce at a third pole, because only the poles under `S` and `T` carry
2-cycles. Its projection is therefore one saddle connection, and saddle
connections on a half-translation surface are simple arcs. Second, the arc
avoids the third branch pole because every point over it is a pole or zero of
`X`. Uniqueness up to isotopy then follows from the trivial pure mapping class
group of the thrice-punctured sphere. Both lifts from sheets 0 and 1 end in the
cycle `(0 1 2)`, a zero. The argument covers all 30 members by braid
invariance. The claim that no room double lies in the family assumes the
equivariance discussed below.

## Interior filter

Let `rho` be the reflection of `X = D(P)`. Interior points of `P` have two
lifts exchanged by `rho`; boundary points have one lift, fixed by `rho`.

Proved, when `f` commutes with `rho` and a reflection `rho_Y` of `Y`: a
ramified marked point `S` is interior only if `rho(S) != S`, and `rho(S)` is a
2-cycle over `rho_Y(f(S))`. A pole with a 1-cycle or 3-cycle above it is fixed
by `rho_Y`, because those points are corners of `P`.

The coordinator deduction is correct for rooms tiled by reflected copies of a
base room. `rooms` confirms it on a 2-tile and a 4-tile room built from
`L(2,2)`: each wall point is a single `rho`-fixed 2-cycle; the interior point
gives two 2-cycles exchanged by `rho`. Two corrections:

1. A pole of `Y` with only 2-cycles above it can be moved by `rho_Y` (the base
   is then not a room). The partner 2-cycle then lies over a different pole.
2. Equivariance is an assumption. A square-tiled room double can have covers
   that do not commute with `rho`. This file does not exclude them.

Under equivariance, all three families fail. In each, `rho_Y` fixes the poles
under `S` and `T`. In the d21 family each has one 2-cycle, so `S` and `T` are
wall points. In the P1 families the pole has exactly two 2-cycles, so `S`, `T`
are two wall points or the two lifts of one interior point.

## Theorem (computer-assisted, unreviewed)

Let `P` be a strictly simple orthogonal room with at most 20 walls. Let
`f: D(P) -> Y` be a half-translation cover of degree at least 2 onto a surface
with at least 5 poles, commuting with the reflection of `D(P)`. Then no pair of
distinct interior points of `P` has lifts of type P1 or P2 that form a dark
family, and no P3 family is dark at all.

Without the equivariance hypothesis the statement proved is: the only dark P1
and P2 families with `r <= 8` are the three above, and no P3 family is dark.

## Not covered

- Covers of a room double that do not commute with its reflection.
- Torus-cover families over the pillowcase (type b), primitive exotic loci,
  sporadic closed orbits.
- Pairs with one ramified and one free point, and pairs of free points in
  different fibres.
- P3 with `y` constrained to a wall or a symmetry axis of `Y`.
- Whether a wall-point room exists in the P1 families (16 and 20 walls).

## Weakest steps

- The equivariance hypothesis in the interior filter.
- P3 at `z = 1`, degrees 2, 3, 6, 7, 8 relies on family grouping (92
  families). Degrees 4 and 5, all of P1, and all of `z >= 2` do not.
- Enumeration at `z = 1` reuses d21's census; its mass check at degree 6 and
  above covers seed orderings only.
- Lemma A and the review of d21's proof are hand arguments by one author.

## Files

- `d22.py`: `z1 D`, `exh D [kinds seconds]`, `small`, `rooms`, `d21`.
- `result_*.json`, `log_*.txt`.

Compute: about 35 CPU minutes, at most 3 processes. That includes one
10-minute run that was stopped and discarded.
