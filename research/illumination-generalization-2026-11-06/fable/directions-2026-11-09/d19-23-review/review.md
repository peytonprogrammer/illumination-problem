# Review of d19 to d23

Date: 2026-11-10. One adversarial reader, one session. Nobody has reviewed this
review. No network was used, so no cited theorem was re-read at its source.

## Verdicts

| Write-up | Verdict |
| --- | --- |
| d19 finiteness | CONFIRMED WITH CORRECTION |
| d20 periodic | CONFIRMED WITH CORRECTION |
| d21 bi-pole | CONFIRMED WITH CORRECTION |
| d22 structured | CONFIRMED (the slice `z = 1`, `delta = 4` reproduced; other verdicts not re-run) |
| d23 equivariance | CONFIRMED WITH CORRECTION |

The final claim stands. It's narrower than its place in the chain suggests
(see "Most serious problem").

## d23

- **Lemma 1 is correct on room doubles, and its statement is too general.**
  Step 2 says the deck germ `tau` doesn't depend on the cover. That holds when
  the cone angle at `Z` is `p pi` with `p` prime. On a room double the angle is
  `2 pi` or `3 pi`, so it holds. At a cone angle `6 pi`, local degrees 2 and 3
  give deck groups that meet trivially, and the proof fails. Add the hypothesis
  "every cone angle of `X` is `pi`, `2 pi`, or `3 pi`".
- I checked the rest of the proof line by line: `C_f` is irreducible iff the
  monodromy is 2-transitive; `f = z^2` or `z^3` in the natural coordinate at
  `Z`; two irreducible curves with a common germ are equal. No counterexample
  exists in the stated setting, because the proof is complete there. A purely
  topological counterexample (two degree-3 maps sharing a branch point) doesn't
  apply: the flat structure fixes the germ.
- **Lemma 2 is correct.** `rho tau rho = tau^(-1)` lies in `C_f`, and
  `(rho x rho) C_f` is irreducible. The step "the reflection fixes every corner,
  each family has a 3-cycle over a pole, hence `f rho = sigma f`" holds: a
  3-cycle over a pole is a zero of `X`, so a reflex corner. The three groups are
  `A_4`, `A_5`, `S_5` in degrees 4, 5, 5, all 2-transitive (checked by hand
  from the seed tuples).
- **Route 2 proves less than item 2.** It shows that `{S, T+}` and `{S, T-}`
  aren't both family pairs. Item 2 says that no lift pair is a family pair.
  For two interior points, `R(f) = {S+, T+}` and `R(c f rho) = {S-, T-}` are
  disjoint, so the matching corollary gives no contradiction. Item 2 needs the
  shared 3-cycle, which is Lemma 2. Relabel Route 2 as a weaker statement.
- **Route 1 (`Q_min`)** is correct for non-lattice rooms, given Apisa-Wright
  Lemma 3.3 as quoted. I didn't re-read the lemma.
- **Reviewer's addition (hand argument, unreviewed).** Given Lemma 2, no room
  double lies in any of the three families, so the open item "wall-point pairs"
  closes. Reason: `sigma` fixes all six cone points of `Y`, so `Y / sigma` is an
  L-shaped room `R` and `P` is tiled by `delta` reflected copies. Each side
  `e_i` of `R` gives an involution `tau_i` on tiles, and the monodromy at a
  corner is `tau_(i+1) tau_i`. An unramified corner (the zero, or a pole with
  identity monodromy) forces both adjacent `tau` to be the identity. A corner
  with a 3-cycle needs both adjacent `tau` non-trivial. Count: the `A_4` family
  has 3 unramified corners, so at most 2 non-trivial sides and at most 1 such
  corner; it needs 2. The `A_5` family has at most 3 non-trivial sides and 2
  such corners; it needs 3. The `S_5` family has at most 1; it needs 3.

## d22

- **Bound and list: correct.** A point of `Y` with cone angle `m pi` has
  preimages of angle `k m pi` in `{pi, 2 pi, 3 pi}`. So `m <= 3`; a regular
  point and a simple zero take `k = 1` only; a pole takes `k = 1, 2, 3`.
  Order 3 over a pole is allowed, order 2 over a zero isn't, and nothing else
  occurs. `Y` has genus 0, so `Y` lies in `Q(1^z, -1^(z+4))`, and
  `r = delta z + t`. The list `z = 1, delta <= 8`; `z = 2, delta <= 4`;
  `z = 3, 4, delta = 2` is complete.
- **Lemma A: correct.** The lift must go through the orientation cover of `X`,
  not `X` itself (`X -> Y~` doesn't exist when a pole has odd local degree).
  The argument is unchanged. A converse check: 2-cycles over one pole only is
  impossible for `delta >= 6` or `z >= 2` by the index count, which matches the
  table.
- **"Lit on one square-tiled member" is valid.** The member lies in the family,
  the family is the braid orbit of the node, and one lit member shows the
  family isn't entirely dark. `y = (1, 0)` is a wall point of the base. That's
  acceptable: it's a regular point of `Y`. It excludes dark families only. It
  doesn't show that every member is lit.
- **Independent re-run (`slice.py`, 8 seconds, no shared code).** `z = 1`,
  `delta = 4`: 665 covers, 8 braid orbits, 420 P1 nodes in 5 families, 3,990 P3
  nodes in 9 families. 390 P1 nodes have a segment with `p + q <= 12` on
  `L(2,2)`, `L(3,2)`, or `L(2,3)`. The other 30 are exactly the nodes with
  2-cycles over one pole, which Lemma A proves dark. All 3,990 P3 nodes are
  lit. Every number agrees with d22.
- `counts_z2.py` reproduces the cover, P1, and P2 node counts for `z = 2, 3, 4`
  (15, 135, 680, 21, 28; 780; 15, 420, 9,420, 21, 28). I didn't re-run those
  verdicts, or degrees 5 to 8 at `z = 1`.
- **Coverage gap not named in "Not covered".** A fold or periodic pair over a
  proper sublocus of `Q_z` can be dark while the full family is lit. The base
  can be a non-arithmetic Teichmuller curve (see d20 below).

## d21

- **The darkness proof is correct** with d22's two added steps. I checked: the
  shortest sub-segment avoids `S` and `T` inside; a saddle connection can't
  cross itself (a crossing is tangential, so it forces a closed leaf or a
  fold at a pole); the arc class in the sphere minus three points is unique;
  with the tail arc, sheets 0 and 1 both land in `(0 1 2)`.
- **Correction.** "The remaining two reflections can't join five tiles" is
  valid only when the two non-wall sides are adjacent, as in the listed
  ordering. Two non-adjacent reflections join five tiles in a strip. The
  cycle-type count above covers all 30 orderings.

## d20

- **Lemma 1 (no rel) is correct.** `iota*` is `+1` on rel and `-1` on the
  tangent space of `L_r`. Rank 1 means a closed orbit.
- **Correction to Section 6.** Non-arithmetic Teichmuller curves exist in `L_r`
  for `r >= 2`: covers of an L-shaped Veech double branched over poles. A room
  tiled by reflected copies of an L-shaped Veech table is a non-lattice room
  double on one. Dark pairs there are type (0), or type a-fold with a
  3-dimensional `M`. Neither is covered by d21 or d22.
- **Case (A) identification is correct**, given Apisa-Wright Theorem 1.4 (read
  in d18 only). Lemma 2 and the bounds for cases (B) and (C) rest on READ-S
  items. The final claim doesn't use them.

## d19

- **Closedness: correct.** The pole-lift argument (a segment through a pole
  lift folds, and a sub-arc joins `S` to `T`) holds.
- **EMM passage: correct as a reduction.** Properness of `Phi` is sound. The
  marked-point extension of EMM Theorem 2.2 rests on a remark in LMW.
- **Type list: exhaustive, with one simplification.** By d20 Lemma 1 a
  torus-cover locus in `Q_r` has dimension 2. So type (b2) is empty and type
  (b) is (b1) only. d19 lists (b2) as open.

## What the chain establishes about rooms

Let `P` be a strictly simple orthogonal room with `r <= 8`, and `(S, T)` a lift
pair of two distinct non-corner points of `P`. If `(D(P); S, T)` is dark, its
orbit closure is entirely dark, and it isn't a full P1, P2, or P3 family over a
full stratum `Q(1^z, -1^(z+4))` with `z >= 1`. d23 proves this when at least one
point is interior; the reviewer's addition removes that condition. The statement
uses only: closedness of the dark set, the d21 and d22 censuses (unreviewed
code; one slice reproduced here), Lemma A, the d21 arc proof, and d23 Lemma 2.
It uses no cited theorem. The reading "what remains is type (0), type (b1), a
proper sublocus of the base stratum, or a primitive locus" does: EMM Theorem 2.2
with marked points (LMW remark), Apisa-Wright 3.3 and 3.6 (READ), Apisa-Wright
1.4 (READ in d18), Apisa 2110.07540 Theorem 1.5 and the high-rank theorem
(READ-S, summary only), and Masur-Smillie, Veech, Smillie, Lanneau (MEMORY).

## Most serious problem

The claim says nothing about the rooms where dark pairs are known to live. A
lattice room with rational points has a closed orbit, which is type (0); with
one free point it's type (b1). A room tiled by a Veech L-table sits on a
non-arithmetic closed orbit. None of these is a full family, so the theorem
doesn't constrain them. d22's "no counterexample to 22-wall minimality appears"
is not evidence for 22-wall minimality.
