# d48: referee report on d47 (scope of the certificate-side theorem)

Referee: Opus 5.5, 2026-11-14. Memo under review: `../d47-cert-gaps/opus.md`.
Theory, plus one read-only check on two named rooms (`check_transfer.py`,
`check_transfer.log`, 0.03 CPU-s, one process). No room, ray, direction, or
word search.

Tags: **PROVED** (argued here), **CITED** (taken from the named file, not
rechecked), **GUESSED** (belief only). Notation follows d47. `rho(x, y) =
(x, -y)`. `m = [Lambda : Z^2]`. A *lift pair* is `(sigma, tau)` as in d10.

## Verdicts

| Item | Verdict | Confidence |
| --- | --- | --- |
| 1. Lemma 3.2 (odd transfer) | CORRECT WITH FIX | 85% |
| 2. Proposition 4.1 (different-class marks) | CORRECT WITH FIX | 80% |
| 2b. Residue D20 as a finite check | GAP (under-specified); spec below | 85% |
| 3. Proposition 1.1 | CORRECT | 90% |
| 3. Definition 1.2, "equivalently" clause | WRONG | 95% |
| 3. (2,4,4) bases | Reduce to pillowcase certificates (Par, Rig); no extra residue | 80% |
| 4. Section 5, "no finite bound is known" | CORRECT as stated, but a reduction was missed | 70% for the reduction |
| 5. Theorem (Section 6) | CORRECT WITH FIX (H2 redundant, H3 too broad) | 75% |
| 5. Presentation-form corollary | CORRECT | 80% |

Minor errors found along the way:

- Proposition 3.1 (line 162): "odd-index non-rectangular bases between
  `Z^2` and `(1/g) Z x (1/g') Z` exist iff `gcd(g, g') > 1`" is wrong for
  `g = g' = 2`. Goursat gives a non-product subgroup of odd order only when
  an odd prime divides `gcd(g, g')`. The 22-wall-times-3 example is
  unaffected (PROVED).
- Proposition 4.1 (line 265): "`d in {3, 4, 5}`" should be `d = 5`, because
  `n = delta d = 4 d = 20` (PROVED).
- Section 3, Residue G1-odd (lines 223 to 243): see item 3. Under d47's own
  Definition 1.2 it is empty, and its "Cut: unbounded" row is wrong under
  any definition (item 4, Lemma Z).

## 1. Lemma 3.2 (transfer across an odd cyclic inclusion)

Step by step.

1. **Corners. CORRECT.** A point of `Lambda \ Lambda'` is not fixed by any
   `p -> -p + 2v`, `v in Lambda'`, so it is a regular point of
   `P_{Lambda'}`. The corner map `Lambda'/2Lambda' -> Lambda/2Lambda` is a
   bijection when `[Lambda : Lambda']` is odd (the Lemma 1.4 argument with
   `Lambda'` for `Z^2`). Local degree at a corner over a corner is 1 (both
   have angle `pi`). PROVED.
2. **Factor. CORRECT.** `N' = Q / (Pi_N meet Pi_{Lambda'})`, the meet of two
   block systems of the monodromy of `Q -> P_Lambda`. It is a block system
   finer than `Pi_{Lambda'}`, so it is a factor of `Q -> P_{Lambda'}` in
   Theorem U's sense (restrict to one `Pi_{Lambda'}` block). It is connected
   and has genus 0 as a quotient of the sphere `DR`. Because
   `P_{Lambda'} -> P_Lambda` is unramified at `x'`, `N'_{x'}` injects into
   `N_x` with the same cycle lengths. PROVED.
3. **Par. CORRECT.** The other preimages of `x` in `P_{Lambda'}` are
   regular points of `P_{Lambda'}`, not corners. Theorem U over
   `P_{Lambda'}` never looks at them: `Q -> P_{Lambda'}` is unbranched
   there, so light paths cross them freely (the d10 Lemma 0 argument). So
   regular points of `N` over them don't matter. PROVED.
4. **Cut. CORRECT.** `phi'(sigma)` and `phi'(tau)` lie in `N'_{c_s'}`, which
   injects into `N_{c_s}`, and have the same image, so they are equal.
   Regular to regular holds by the cycle-length-preserving injection. One
   point over `w` gives exactly one point over `w'`. PROVED.
5. **Rig. CORRECT, two wording fixes.**
   - The vector: in a Smith basis, `u1`, `2 u1 + m u2`, `u1 + m u2` lie in
     `Lambda'`, are primitive in `Lambda` (`gcd(2, m) = 1`), and represent
     the three nonzero classes of `Lambda'/2Lambda'`. PROVED.
   - The segment must start at a point `s` of class `c_s`, not at 0. The
     segment `s -> s + w` is a simple saddle connection in `P_Lambda`: a
     self-intersection would need `(t - t') w / 2` or `(t + t') w / 2` in
     `Lambda` with a non-integer coefficient. Its lift to `P_{Lambda'}` ends
     at `x'`. PROVED.
   - The certificate over `P_Lambda` names some arc. Using `alpha` instead
     needs Theorem U's "one arc decides all" over `P_Lambda`. That holds
     because `alpha` is simple and misses the fourth corner. The memo
     invokes this only over `P_{Lambda'}`. PROVED.
   - Direction of liveness: the argument needs exactly "live in `N'`
     implies live in `N`". That's true: the same regular point of `Q` lies
     over both. The image of `K_{N'}` is then a connected live subgraph
     through `phi(sigma)`, so it lies in `K_N`. So `phi'(tau)` in `K_{N'}`
     would force `phi(tau)` in `K_N`. The converse isn't needed. PROVED.

**Fix to the hypothesis.** "Admissible" in d47 means `Lambda' >= Z^2 + ZS +
ZT`. That puts only the *front* lifts over corners (item 3). The lemma needs
all four lifts over corners of `P_{Lambda'}`: `S, T, rho S, rho T in
Lambda'`. Example: `Lambda = (1/3) Z^2`, `Lambda' = Z^2 + Z(1/3, 1/3)`,
`S = v0 + (1/3, 1/3)`. Then `S` is in `Lambda'` but `rho S` is not, so lift
pairs through the back lift of `S` have no certificate over `P_{Lambda'}`.
Corollary 3.3 uses `Lambda' = Lambda_r`, which is `rho`-invariant, so it is
unaffected. The "cyclic" hypothesis is removable: compose prime-order steps
through a composition series of the odd group `Lambda / Lambda'`.

**Named-room test (run).** `check_transfer.py` refines each room by 3 and
builds `P_L` as a block system on the `9 n` sheets. The base `3Z^2` (that is,
`B_R`) reproduces the d38 and d43 logs: for the 22-wall room, `B_b`, `B_c`,
`B_d` have 5, 15, 5 blocks per sheet block and separate all four lift pairs;
for the cross, only `B_d` separates. Over `Z^2 + Z(1/3, +-1/3)`:

- Each corner of `B3` has exactly one fixed `P_Lambda` block (step 1,
  asserted).
- All four lattice-mark lifts lie over the corner.
- For both rooms, every canonical `B^Lambda_x` and `R^Lambda_y` is
  `P_Lambda` itself (3 blocks) and separates nothing. So there is no Par or
  Rig certificate to transfer. The meet `N'` passes the step-3 checks.

This is consistent with Lemma 3.2 but only exercises it weakly. It also shows
that the converse fails: the 22-wall room is certified over `B_R` and not
over either sheared base. Cut over the sheared bases was not computed
(reasoned only).

## 2. Proposition 4.1 and Residue D20

- **"Par and Cut need `c_s = c_t`."** This matches d10 lines 182 and 187
  verbatim. Rig has no such clause. With `c_s != c_t` the single target is
  `t` (d10 line 177). CORRECT.
- **`z = 0`.** Correct, and there is a shorter proof than d36's colour
  argument. By Gauss-Bonnet `N` is a pillowcase. By Proposition 1.1 it is
  `P_L` with `L` between the vertex lattice and `Z^2`. With at least 3
  corner classes, `[Z^2 : L]` is odd. So over `y` there is one corner and
  `(d-1)/2` regular points. Identity at `y` forces `d = 1`, `N = B`.
  PROVED.
- **`z = 1`.** `d = 3`: the profiles are forced, `a` and `t` aren't the
  `(3)` corner by Fact L, and `<g_a, g_t>` contains a 3-cycle, so the arc
  graph is the connected path `p - r - r - p` with every vertex live.
  `d = 4` (the `V_4` argument) and `d = 5` (the parity argument) use only
  cycle types, not marks. CORRECT (PROVED here; same as d43 lines 107 to
  119).
- **`z >= 2`.** `delta z <= r <= 8`, `d <= z + 4`, `d != 6`. The `d = 6`
  exclusion (d43 lines 125 to 137) uses the seam and the `D_3` cover only.
  It doesn't use the marks. CORRECT. Two wording issues:
  - `delta` even comes from "an off-seam pole exists". At `z >= 2` that
    existence comes from the one-star *classification* (no off-seam pole
    means `K` is a cell, domino, tromino, or square, so `z <= 1`). So
    d47's claim that the one-star sub-step "is not needed" (line 286, and
    Section 7) holds only for the *disposal* of those four shapes. That
    is harmless here: without `delta` even, `(delta, z) = (3, 2)` adds
    only `n <= 15`, which is still inside Part A's area-16 range.
  - `(4, 2)` forces `n = 4 d`. With `n = 20` that gives `d = 5`, not
    `d in {3, 4, 5}`.
- **Conclusion.** A Rig certificate for a different-class lift pair forces
  `n <= 16`, or `n = 20` with `r = 8`, `(delta, d, z) = (4, 5, 2)`. PROVED,
  given the CITED d39/d43 seam steps.

**Residue D20: GAP in the specification.** "Check whether `R_y` separates"
tests only a necessary condition. Rig also needs separation in the *live*
subgraph. The check must do the following, per room and per pair.

1. Rooms: strictly simple, `W = 20`, area 20 (169,672,127 up to symmetry,
   CITED from `d9-census-w22/census_totals.md` line 94). All are normalized
   with at least 3 classes. A non-normalized one would have area
   `g g' n_R = 20` with odd `g g' = 5`, so `n_R = 4`, which can't have
   `W = 20`.
2. Pairs: interior lattice points `S`, `T` with `T - S` not in `2 Z^2`. Put
   `a = [S]`, `t = [T]`.
3. For each `y` in the two classes outside `{a, t}`: compute `R_y` (merge
   every cycle of `g_y`) and `N_y = Q / R_y`. Record `(delta, d, z)`.
4. For each of the 4 lift pairs `(sigma_i, tau_j)` and each `y`: build
   `Gamma_alpha(N_y)` for the basic arc from `a` to `t`. Use a side of the
   base square if `t` is adjacent, the diagonal if `t = c`. In both cases
   edges are sheets. Vertices are `g_a`-cycles and `g_t`-cycles of blocks.
   A vertex is live when it is a regular point of `N_y`, or a pole whose
   block contains a sheet in a 2-cycle of `g_a` (resp. `g_t`). Test whether
   `phi(tau_j)` lies in the live component of `phi(sigma_i)`.
5. The pair is certified when every lift pair is separated for at least
   one `y`. The expected count is 0.
6. Cross-check: any separation with `(delta, d, z) != (4, 5, 2)` refutes
   Proposition 4.1.

The `(4, 5, 2)` filter can prune before step 4, but run the full test at
least on a sample to validate the filter.

## 3. Proposition 1.1, Definition 1.2, and the (2,4,4) base

**Proposition 1.1: CORRECT.** I rederived it. Vertices have angles `pi` and
`3 pi`, so they map to corners (`2 pi e` can't equal `pi` or `3 pi`). The
back chart is `(x, -y) + (0, 2 y0)`, which is `rho` modulo `<2 Lambda, -1>`
because `(0, y0)` is in `Lambda`. Edge gluing forces `(h, 0)` and `(0, w)`
into `Lambda`. Normalization gives `Z^2`. PROVED.

**Definition 1.2, "Equivalently, Lambda is admissible when both marks lie
over corners": WRONG.** The front lift of `S` maps to `[S]`, the back lift to
`[rho S]`. So all four lifts lie over corners if and only if
`Lambda >= Lambda_0 + rho Lambda_0`. For `Lambda = Z^2 + Z(1/3, 1/3)` and
`S = v0 + (1/3, 1/3)`, the back lift lies over a regular point. The run
confirms it (`check_transfer.log`, back-lift demo: front over a corner and
back not for `+1/3`, reversed for `-1/3`). PROVED.

**Consequence (PROVED).** For odd `[Lambda : Lambda_r]`,
`Lambda ∩ rho Lambda = Lambda_r`. If `lambda` and `rho lambda` are in
`Lambda`, then `(2 lambda_x, 0)` and `(0, 2 lambda_y)` are in `Lambda`, so
`2 lambda` is in `Lambda_r`. Odd order then forces `lambda` into `Lambda_r`.
So for odd index, "every lift over a corner" is exactly H2. Under d47's
single-base Definition 1.2, **Residue G1-odd is empty**: a mark outside
`Lambda_r` has a lift pair that no Theorem U certificate over `P_Lambda`
can address. d47's own example is certified, if at all, over
`(1/3) Z^2`, which is rectangular and covered.

d10 Theorem U is per lift pair, so a per-lift-pair base is the native
notion. For lattice marks and odd bases this changes nothing. A lift pair
certified over a base with `ab >= 3` forces `n_R <= 13` (Par), `<= 6` (Rig),
or the cross (Cut). The d9 census then says some lift pair is lit, so the
system can't be full (PROVED from CITED bounds and census). For marks
outside `Lambda_r` it revives G1-odd for single lift pairs. That residue is
finite (item 4).

**The (2,4,4) base: decided. Theorem U certificates over it reduce to
pillowcase certificates.**

- *Classification (PROVED, sketch).* A flat orbifold that `DR` covers by a
  local isometry has holonomy containing `-1`. That rules out the torus
  and `(3,3,3)`. `(2,3,6)` would need a hexagonal `L >= Z^2` inside `Q^2`,
  which is impossible. So the bases are the `P_Lambda` and the orbifolds
  `O = P_L / J`, with `L >= Z^2` invariant under rotation by 90 degrees and
  `J` that rotation about a point of `L`. Up to translation, `J` either
  merges classes `(1,0)` and `(0,1)` into the order-2 point `m` (center of
  class `(0,0)`), or merges `(0,0)` and `(1,1)`.
- *Every map `DR -> O` factors through `P_L` (PROVED).* `DR` has holonomy
  `+-1`, which lies in the index-2 subgroup of the `Z/4` holonomy of `O`.
- *Every factor `N` of `DR -> O` yields `N'`, the component of
  `N x_O P_L` through `Q` (PROVED).* It is a factor of `Q -> P_L`, and
  `N' -> N` has degree 1 or 2.
  - Over `m`, `P_L -> O` is unramified, so `N'` over the corners `(1,0)` and
    `(0,1)` is locally `N` over `m`, split by germ side.
  - Over an order-4 point `x`, a point of `N` with local degree `e` gives
    one point of `N'` with `e' = e` when `e` is odd, and two points with
    `e' = e/2` when `e` is even. So "regular" (`e = 4`) corresponds to
    `e' = 2`.
  - Arc lifts correspond, and live maps to live.
- *Transfer (PROVED).*
  - Par over `O` at any target gives Par over `P_L` via `N'`, at the
    corresponding target or targets.
  - Rig over `O` with local degree at most 2 over the point `y` gives Rig
    over `P_L` with identity at `y'`, via `N'`. So Rig is dominated by
    `R_{y'}` (R3).
  - Theorem U's Cut proof needs two "other corners". `O` has only three
    cone points, so there is no Cut over `O` to transfer. Nothing in the
    programme defines one.
- *The trap for marks in classes `(1,0)` and `(0,1)` (PROVED).* Over `O`
  they are the same point `m`. The only light paths between them use loop
  saddle connections at `m`. Those are the images of the `P_L` saddle
  connections `(1,0) -> (0,1)`. Reading "`c_s = c_t`" on `O` makes Par
  **unsound**:
  - `N = P_L` has no regular point over `m` and separates `sigma` from
    `tau`, in every room.
  - In the 12-wall cross, `S = (1,2)` and `T = (2,1)` are interior, in
    absolute classes `(1,0)` and `(0,1)`. The segment between them passes
    `(1.5, 1.5)`, so the pair is lit (reasoned, not run).
  - The sound reading puts `c_s = c_t` on `P_L`. There these marks are
    different-class, and only Rig applies, which is Proposition 4.1 and
    Residue D20 (or Residue E when `L` has even index).
- *Tokarsky's lemma* is a Par certificate over `P_L` with `N = Q`, at
  same-class marks over an order-4 point, so it is already covered.
- *Answer.* No `(2,4,4)` certificate of Par or Rig shape certifies a pair
  that no pillowcase certificate certifies. The extra residue is empty,
  unless someone proves a new Cut-type theorem over a three-cone-point
  base. Then the only case not covered is `N` not factoring through `P_L`,
  with a single point of even local degree over an order-4 point.

## 4. Section 5 (even index)

- "Every zero-free target is a pillowcase factor": CORRECT (Gauss-Bonnet
  `p = z + 4`, then Proposition 1.1). One wording issue: d47 calls the
  resulting `P_{Lambda''}`, with `Lambda'' <= Lambda`, a "coarser base".
  It is a cover of `P_Lambda`.
- "The cross scaled by 2 has zero-free targets of unbounded delta": CORRECT
  WITH FIX. d43 line 141 gives one room with `delta = 24` at `z = 0`. That
  shows d36's bound fails there. "Unbounded" is a statement about the
  family of scalings, not about the one room.
- "No finite bound is known": true of d47, but these reductions follow.

**Odd-part reduction (PROVED).** Let `Lambda'` be the preimage of the
2-primary part of `Lambda / Z^2`. Then `[Lambda : Lambda']` is odd. Lemma
3.2 (with the fix above, composed over prime steps) moves any certificate
to `P_{Lambda'}` whenever all mark lifts are in `Lambda'`, for example for
lattice marks. So Residue E reduces to index a power of 2.

**Lemma Z (PROVED, sketch; Cut-degree bound CITED from d10 line 231).** Over
*any* base `P_Lambda`, let `n = m n_R = deg(Q -> P_Lambda)`. Each zero of `N`
has `delta` zero preimages, so `delta z <= r`.

- Par with `z >= 1`: `d = p_x + 3 z_x <= 4z + 4`, so `n <= 4r + 4r/z <= 8r`.
- Rig with `z >= 1`: `d <= p_y <= z + 4`, so `n <= 5r`.
- Cut: `deg N <= 3`. At `z >= 1` this gives `n <= 3r`. At `z = 0`, `N` is a
  degree-2 pillowcase. Cut then forces no regular point of `Q` over `x`, so
  every `Q`-point over `x` is a vertex, and `n <= (r + 4) + 3r = 4r + 4`.
- Otherwise `N = P_{Lambda''}` with `[Lambda : Lambda'']` in `{2, 4}`. That
  needs even index. Odd bases have no zero-free certificate.

This bounds the memo's "G1-odd with Cut, unbounded" row: `m n_R <= 36`.

**Witness route for Residue E (sketch).** Zero-free certificates are lattice
data.

- Par needs only `Lambda''`, `Lambda`, and the classes of `S`, `T`,
  `rho S`, `rho T`.
- Rig adds liveness of corners of `P_{Lambda''}`. A corner whose coset
  avoids `Z^2` is always live.
- A lattice coset contains a whole `2 Z^2` class. If it is not live, every
  class point is a vertex, so `n_R <= 4r + 4 <= 36`. Each cell has one
  corner in each class.
- Take `n_R > 36` and `m >= 2`. Then `m n_R > 64 >= 8r`, so every
  certificate is zero-free. All corners are live, and the system doesn't
  depend on the room.
- Take a large normalized room `R'` with a vertex at the origin, the same
  interior marks, and that lift pair lit. For example, use a big square
  with a width-1 notch ending at the origin. The same system would
  certify `R'`, which contradicts Theorem U's soundness.
- So Residue E, and per-lift-pair G1-odd, are empty for `n_R >= 37`.
- What is left:
  - `21 <= n_R <= 36` (lattice marks; `n_R <= 20` is the census).
  - `m = 2`: three lattices, mixed certificates, a finite check.
  - `m >= 4`: only rooms with a vertex-only `2 Z^2` class, such as the
    cross.
- Ratings: Lemma Z 85%; room independence 80%; the witness room existing
  for every lift pair GUESSED, 85%; the route closing E to a finite check
  60%. The open part is the `m >= 4` lattice family for the few
  non-all-live rooms. I did not pursue it.

## 5. The theorem (Section 6)

How H1 to H3 are used:

- H1 is used twice: by Lemma 3.2 and Proposition 2.1 (odd `a`, `b` give
  at least 3 classes), and to keep classes.
- H2 is used by Corollary 3.3. Under Definition 1.2 it is redundant: if it
  fails, some lift lies over a regular point and the conclusion holds
  trivially (item 3).
- H3 is broader than needed. Proposition 4.1's exception needs `r = 8`, so
  only `W = 20` matters.

The presentation-form corollary follows. For a presentation with at least 3
classes, every factor of `DP -> B` has odd index. The "rectangular part"
clause can be dropped by the same argument as H2.

**Theorem I would sign (computer-assisted).** Let `R` be a normalized,
strictly simple orthogonal lattice polygon with `W <= 20`. Let `S != T` be
interior points with rational coordinates. Let `Lambda >= Z^2 + ZS + ZT`
(origin at a vertex) with `[Lambda : Z^2]` odd. Then the four lift pairs of
`(S, T)` do not all have Par, Cut, or Rig certificates over `P_Lambda` at
every target, except possibly when all of the following hold (Residue D20):

- `W = 20`;
- `S` and `T` lie in `Lambda_r` and in different classes of
  `Lambda / 2 Lambda`;
- `n_R [Lambda_r : Z^2] = 20`.

The statement also holds when each lift pair may choose its own odd base,
provided `S` and `T` are lattice points. Status: PROVED reductions (d47
Sections 1 to 4, as corrected here) on top of CITED d10 (Theorem U, R3),
R4 as patched in d43, d36, d39 via d43, the d9 census and Part A, and d46.

## Residues

| Residue | Kind | Size | Status |
| --- | --- | --- | --- |
| D20: different-class lattice pairs, `W = 20`, area 20 | finite canonical-partition and live-graph check (spec in item 2) | at most 1.7e8 rooms times pairs; about 10 CPU-min for rooms at d46 speed, plus pairs | not run |
| G1-odd, single base (Definition 1.2) | none | empty | PROVED |
| G1-odd, per lift pair, marks outside `Lambda_r` | finite check | `m >= 3` odd; `m n_R <= 40` (Par, d36), `<= 24` (Rig), `<= 36` (Cut, Lemma Z); empty for `n_R >= 37` | bounds PROVED, check not run |
| E, even index | reduce to 2-power index, then to a finite check | `21 <= n_R <= 36`; `m = 2` (3 lattices) mixed; `m >= 4` only for rooms with a vertex-only `2 Z^2` class | reductions PROVED (sketch) or GUESSED (witness); last step open |
| (2,4,4) bases | none for Par and Rig | empty | PROVED (sketch) |
| A Cut-type theorem over three-cone-point bases | not a residue until someone proves one | — | — |
| Darkness without a certificate (U\*) | open conjecture | — | unchanged |

## What I ran and what I reasoned

- Ran `check_transfer.py`, 0.03 CPU-s. It covers the 22-wall room and the
  cross over `B_R` and `Z^2 + Z(1/3, +-1/3)`: Par and Rig canonical
  partitions, the `N'` mechanism of Lemma 3.2, and the back-lift placement.
  The `B_R` rows match `../d38-review/check_named.log` and
  `../d43-review-d39/check_cross.log`.
- Reasoned everything else: Cut over sheared bases, the (2,4,4) analysis,
  the cross counterexample to Par over `O`, Lemma Z, and the witness route.
