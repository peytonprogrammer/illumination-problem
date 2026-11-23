# Type a-per dark families: what published theory settles

Date: 2026-11-10. Direction d20. Theory and literature only; no scripts.
Nobody has reviewed this document.

Status tags:

- **PROVED**: a proof or proof sketch is in this file, given the cited inputs.
- **READ**: published; the statement was read in the source in d18 or d19.
- **READ-S**: published; read today through an automated summary of the ar5iv
  page. The summary paraphrases. Nobody read the proofs.
- **MEMORY**: published or standard, cited from memory.
- **CONJ**: expected, not proved.
- **OPEN**: not proved and not refuted.

Notation follows d19. `Q_r = Q(1^r, -1^(r+4))`. `L_r` is its locus of
orientation double covers in `H(2^r)`, genus `r + 1`. `iota` is the
hyperelliptic involution. A type a-per family is `M` over `N`, with `N` a
proper affine invariant submanifold of `Q_r` that isn't a torus-cover locus,
`dim M = dim N >= 3`, and `S`, `T` regular `N`-periodic points.

## 1. Answer

- **Full stratum: no.** `Q_r` has no regular periodic point. PROVED from READ.
- **`r <= 2`: no.** Type a-per with regular points is empty. PROVED from READ
  and READ-S.
- **`r = 3, 4`: only one way left.** `N` would be a *primitive* locus of rank
  2 (or 3 when `r = 4`): its generic member covers nothing. No such locus is
  known. Published theory doesn't exclude it. OPEN.
- **`5 <= r <= 8`: two ways left.** The primitive case above, and a cover
  structure with `S`, `T` over *different* poles of the base (Section 5). Both
  OPEN.
- **The hoped-for answer is half right.** A cover structure doesn't give a
  fold. When `N` is a full locus of covers, the regular periodic points are
  ramification points over poles. A dark pair of them with `f(S) = f(T)` is
  type a-fold. A dark pair with `f(S) != f(T)` is a different structure. You
  must add it to the classification as a possibility. I found no example and
  no proof that it's empty.

## 2. Two structural facts (new here)

**Lemma 1 (no rel). PROVED.** Every affine invariant submanifold `N` of
`L_r` has `dim N = 2 rank(N)`.

*Proof.* Every zero is `iota`-fixed. So `iota*` is `+1` on the rel subspace
and `-1` on the tangent space of `L_r`. The two meet in 0. ∎

Consequences:

- Rank 1 means `dim N = 2`: a closed orbit. Rank-one loci with rel
  deformations don't exist in `Q_r`.
- Type a-per needs `dim N >= 3`, so `rank(N) >= 2` and `r >= 2`. A
  non-arithmetic Teichmuller curve with periodic `S`, `T` is type (0) in d19,
  not type a-per.

**Lemma 2 (no high-rank proper locus). PROVED from READ-S and MEMORY.** If
`N` is proper in `L_r`, then `rank(N) < (r + 3)/2`.

*Proof.* Otherwise Apisa-Wright's high-rank theorem makes `N` a stratum
component or a full quadratic double of some stratum `Q'`, with involution
`J'`. A stratum component is impossible for `r >= 2`.

- If `J' = iota`, the singularity count forces `Q' = Q_r`, so `N = L_r`.
- If `J' != iota`, every member of `Q'` has an involution with sphere
  quotient. Then `Q'` is a hyperelliptic component in Lanneau's list (MEMORY).
  Only `Q(1,1,-1,-1)` and `Q(1,1,1,1)` have doubles in some `H(2^r)`. A Klein
  four-group computation shows that `iota` swaps the zeros in pairs there:
  the sphere quotient lies in `Q(4,-1^8)` or `Q(4,4,-1^12)`. So the double
  isn't in `L_r`. ∎

Ranks that stay possible for a proper non-torus `N`, by `r`:

| `r` | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| rank of `N` | 2 | 2 | 2 to 3 | 2 to 3 | 2 to 4 | 2 to 4 | 2 to 5 |

## 3. Published results on periodic points

| Result | Statement | Status |
| --- | --- | --- |
| Eskin-Filip-Wright | `N` has infinitely many periodic points iff `N` consists of torus covers. | READ as quoted in Apisa-Wright Thm 1.2 (d18); theorem number in EFW not checked |
| Apisa, arXiv:1601.07894 | Hyperelliptic components of abelian strata: the periodic points are the Weierstrass points. | MEMORY |
| Apisa-Wright, arXiv:1708.03411, Thm 1.3 | Non-hyperelliptic components of abelian strata, genus at least 2: no periodic points. | MEMORY for content; number inferred in d18 |
| Apisa-Wright, arXiv:1708.03411, Thm 1.4 | Quadratic double of a stratum component `Q`, not `Q(-1^4)`, `Q(2,-1^2)`, `Q(2^2)`: periodic points are the `J`-fixed points, plus hyperelliptic fixed points if `Q` is hyperelliptic. Genus 0 counts as non-hyperelliptic. | READ (d18) |
| Apisa-Wright Thm 3.6, Lemmas 3.1, 3.3 | Finitely blocked implies both periodic, or same `pi_Q` image. | READ (d18, d19) |
| Apisa, arXiv:1710.05505 | Genus 2, not a torus cover: Weierstrass points, plus two golden points on the golden eigenform locus in `H(1,1)`. | READ (d18) |
| Moeller, periodic points on Veech surfaces | Non-arithmetic Veech, genus 2: Weierstrass points only. | READ as quoted in Apisa (d18) |
| Apisa-Saavedra-Zhang, regular and double `n`-gon | Periodic points classified. | READ-S that the classification exists; content (Weierstrass points only) is MEMORY |
| Apisa-Wright, High rank, arXiv:2102.06567, Thm 1.1 | `rank >= g/2 + 1` implies stratum component or full locus of holonomy double covers of a quadratic stratum. Stated without marked points. | READ-S |
| Same paper, Question 1.3 and Conjecture 1.2 | Question: is every locus of rank at least 3 a full locus of covers? Not a conjecture. Conjecture 1.2 covers rank `g/2 + 1/2`. | READ-S |
| Apisa, arXiv:2110.07540, Thm 1.5 | Genus-zero quadratic strata with at most two zeros: every orbit closure of rank at least 2 is a full locus of covers of a genus-zero stratum. The introduction says the conclusion "may hold for arbitrary genus zero strata"; the zero count enters in its Section 4 only. | READ-S |
| Same paper, Thm 1.3 | Unexceptional rational right or isosceles triangle: no two points are finitely blocked. | READ-S |
| Periodic points of primitive rank-2 loci (gothic and the other Eskin-McMullen-Mukamel-Wright loci), Prym eigenform loci | I know no result that applies to a locus inside `Q_r`. I believe these loci have positive-genus quadratic quotients and aren't in `L_r`. | MEMORY, weak |

The search found no paper titled "Reconstructing orbit closures from their
boundaries" under that query. I cite nothing from it.

## 4. Case `N = Q_r`

**PROVED from READ.** By Theorem 1.4 the `L_r`-periodic points are the
`iota`-fixed points: the lifts of zeros and poles. A point of the sphere is
periodic iff its lifts are (the lifts determine each other through `iota`).
So every `Q_r`-periodic point is a cone point. Type a-per with regular `S`,
`T` can't occur over the full stratum. This agrees with d19, Theorem A,
item 4.

## 5. Case `N` proper, rank at least 2

Let `X` be generic in `N` and `f : X -> B = Q_min` the canonical cover
(Apisa-Wright Lemma 3.3, READ). Let `N'` be the orbit closure of `B`.

### 5.1 Local types. PROVED.

`B` is a sphere. `f` is a local isometry, and `X` has cone angles `pi`,
`2 pi`, `3 pi` only. So:

- a zero of `B` is simple and unramified;
- `f` branches over poles only, with local degree `e` in `{1, 2, 3}`: pole,
  regular point, zero of `X`;
- `B` lies in `Q_z` with no marked points, `z >= 1`, and
  `r = d z + t`, `s + 2t = 2d - 2`. Here `d = deg f`, `s` counts `e = 2`
  points, and `t` counts `e = 3` points. These are d2's identities (claim 1).
  They need no parity property.

### 5.2 Three cases

- **(A) Full locus of covers.** `d >= 2` and `N' = Q_z`. Then `N` is a
  component of the full Hurwitz locus over `Q_z`, of rank `z + 1`.
- **(B) Primitive.** `d = 1`: the generic member covers nothing.
- **(C) Cover of a primitive locus.** `d >= 2` and `N'` is a proper primitive
  locus of `Q_z`.

Apisa's Theorem 1.5 (READ-S) says primitive proper loci of rank at least 2
don't exist in `Q_z` for `z <= 2`. So (B) needs `r >= 3`, and (C) needs
`z >= 3`, hence `r >= 6`. For `r <= 8`, (C) means `d = 2` and
`(z, r) = (3, 6)` or `(4, 8)`. Whether primitive loci exist for `z >= 3` is
OPEN; Apisa expects not (CONJ).

### 5.3 Periodic points of a cover locus. PROVED.

**Lemma 3.** A point `p` of `X` is `N`-periodic iff `f(p)` is a cone point
of `B` or an `N'`-periodic point.

*Proof.* `f` is canonical, so `(X, p) -> (B, f(p))` is equivariant and
finite-to-one on orbit closures. Dimensions agree. ∎

In case (A), Theorem 1.4 applies to `Q_z`. The regular `N`-periodic points
are exactly the `s` points with `e = 2` over poles. So the hoped-for
description is right: periodic points are preimages of cone points of a
smaller surface.

### 5.4 The dark pairs in case (A): fold or bi-pole

Take regular periodic `S`, `T`, with poles `b_S = f(S)`, `b_T = f(T)`.

- **`b_S = b_T`.** This is a fold structure in the d19 sense. It's type
  a-fold, not a-per.
- **`b_S != b_T` (bi-pole).** No fold: `f` is `pi_Q`, and
  `pi_Q(S) != pi_Q(T)`. Theorem 3.6 allows it, because both points are
  periodic. This is the only form of type a-per in case (A).

**Lemma 4 (bi-pole criterion). PROVED, sketch.** A bi-pole family is lit iff
some simple arc `alpha` from `b_S` to `b_T` in `B` minus the other cone
points has this property: in the graph `f^(-1)(alpha)`, a path joins `S` to
`T` through vertices of valence 2 only.

*Proof.* A straight segment is a leaf segment, so its image is a simple arc,
retraced at poles. A path through an `e = 2` point over a pole stays
straight. Conversely the pure mapping class group is transitive on simple
arcs from `b_S` to `b_T`, and it's the fundamental group of the labeled
stratum. Some member of `Q_z` has a saddle connection between two poles
(two adjacent convex corners of a room). So each arc class is straight on
some member of the same component. One lit member suffices: `M` must be dark
at every member. ∎

**Lemma 5 (small degree). PROVED.** A bi-pole family with `d <= 4` is lit.

*Proof.* Label sheets along `alpha`. Let `C_S`, `C_T` be the 2-cycles of `S`,
`T`. If they share a sheet, `alpha` lifts to a segment from `S` to `T`. For
`d <= 3` two 2-subsets always meet. For `d = 4` suppose `C_S = {1,2}`,
`C_T = {3,4}`. A full twist of `b_T` around another pole `c` is a pure braid.
It replaces `C_T` by `C_T x_c^(-1)`, where `x_c` is the monodromy at `c`.
Darkness forces every `x_c` to preserve `{3,4}`. Then the monodromy group
isn't transitive. ∎

**Consequences for `r <= 8`. PROVED given the above.** `d z <= r` and
`d >= 5` force `z = 1`. So a dark bi-pole family in case (A) has:

- base `B` in `Q(1, -1^5)`, the stratum of L-shaped room doubles;
- `5 <= d <= 8`, `r = d + t`, so `r >= 5`;
- `S`, `T` ramification points of order 2 over two different poles of `B`.

Whether such a family is dark is OPEN. It's a finite monodromy question:
does some pure Hurwitz orbit of degree 5 to 8 over five poles keep `S` and
`T` off a common valence-2 chain for every simple arc? I expect not (CONJ).
A script can decide it. I ran none.

**Room form.** By d18 Theorem C, reflections descend to `B`. A room in such
a family is a union of `d` reflected copies of an L-shaped room `R`. `S` and
`T` are tile vertices where two (on a wall) or four (inside) convex corners
of `R` meet flat. They sit at different corners of `R`. `t` counts reflex
corners of the room made of three convex corners of `R`.

### 5.5 Cases (B) and (C)

- **(B).** No cover exists, so no fold and no bi-pole. `S`, `T` would be
  periodic points of a primitive locus. Nothing published classifies them.
  OPEN.
- **(C).** By Lemma 3, regular periodic points are `e = 2` points over poles,
  or unramified preimages of regular `N'`-periodic points. A new source of
  darkness appears: two poles of `B` joined by no saddle connection on any
  member of `N'`. OPEN, and empty if primitive loci don't exist.

### 5.6 `r = 2` in full. PROVED from READ and READ-S.

`N` has rank 2. Theorem 1.5 makes it case (A) with `z = 1`, `d = 2`: double
covers of `B` in `Q(1, -1^5)` branched over two poles. The regular periodic
points are the two fixed points of the deck involution. They lie over
different poles. Every saddle connection between those poles lifts to a
segment from `S` to `T`. So the pair is lit, and type a-per is empty.

For `r = 1`, a proper `N` has dimension 2, so type a-per is empty by Lemma 1.

## 6. Rank-one non-arithmetic loci

- By Lemma 1 these are closed orbits. They give type (0), never type a-per.
  PROVED.
- `r = 1`: they exist and contain room doubles, the L-shaped Veech tables
  (McMullen, Calta; MEMORY). Periodic points are the Weierstrass points,
  which are corners (Moeller, READ as quoted). d18 Theorem L shows every pair
  lit.
- `r >= 2`: I know no non-arithmetic Teichmuller curve in `L_r`. The
  hyperelliptic Veech examples I checked from memory swap their zeros (the
  regular 14-gon lies in the hyperelliptic component of `H(2,2)`). No theorem
  excludes one. OPEN. Each `r` allows finitely many type (0) orbits by d19.
- Apisa-Saavedra-Zhang and Apisa's triangle results concern triangle
  unfoldings. Their quadratic quotients have zeros of higher order, so they
  aren't in `Q_r` (MEMORY).

## 7. Strongest statement supported

**Theorem P. PROVED, given READ and READ-S inputs.** Let `(M, N)` be a type
a-per dark family in `Q_r` with regular marked points. Then:

1. `N` is proper, `dim N = 2 rank(N)`, and
   `2 <= rank(N) < (r + 3)/2`. Item 3 then gives `r >= 3`.
2. Exactly one of the following holds.
   - (A) Every member has a half-translation cover `f : X -> B` of degree
     `d >= 5`, with `B` in `Q_z` and `d z + t = r`. `S` and `T` are
     ramification points of order 2 over two different poles of `B`. For
     `r <= 8`, `B` lies in `Q(1, -1^5)` and `r >= 5`.
   - (B) `N` is primitive of rank at least 2 in a genus-zero stratum with at
     least three zeros.
   - (C) `N` is a locus of covers of such a primitive locus, and `r >= 6`.
3. For `r <= 2` no such family exists. For `r = 3, 4` only (B) is possible.

**If Apisa's Theorem 1.5 extends to all genus-zero strata (CONJ),** then (B)
and (C) are empty. Type a-per is then empty for `r <= 4`, and for
`5 <= r <= 8` it reduces to the finite monodromy question of Section 5.4.

**Orthogonal lattice rooms with `r <= 8`.**

- d2's identities `r = delta z_N + t` and `s + 2t = 2 delta - 2` hold for the
  cover in (A). d2's bound `z_N >= 2` doesn't: it uses the parity property.
  So `z_N = 1` is allowed here, and the degree can reach 8.
- At most `s <= 2d - 2 <= 14` regular periodic points exist in case (A).
- A lattice room in a type a-per family of form (A) is tiled by 5 to 8
  copies of a lattice L-shaped room, with `S`, `T` at different tile-corner
  types. It has at least 5 reflex corners, so at least 14 walls.
- This mechanism differs from d2's single parity factor. The d2 exclusion at
  `r <= 8` doesn't cover it.

## 8. What remains open

1. The monodromy question of Section 5.4, degrees 5 to 8 over `Q(1, -1^5)`.
   Finite; needs a Hurwitz-orbit script.
2. Existence of primitive loci of rank at least 2 in genus-zero strata with
   three or more zeros, and their periodic points.
3. Dark pole pairs on such primitive loci (case C).
4. Non-arithmetic Teichmuller curves in `L_r` for `r >= 2` (type 0).
5. Reading the proofs behind the READ-S items, above all Apisa's
   Theorem 1.5 and its definition of "full locus of covers". Section 5.6
   assumes it means half-translation covers of the sphere quotient. I
   justified that through `Q_min`, but didn't check it against his text.
6. Lemma 5 for general degree.

## 9. Weakest steps

- READ-S items were read through a summarizer, not in the TeX source.
- Lemma 2 uses Lanneau's list of hyperelliptic components from memory.
- Lemma 4 and Lemma 5 use braid-group conventions that I checked by hand
  once. A second reader should recheck the twist formula
  `C_T -> C_T x_c^(-1)`.

## 10. Citations

| Source | Used for | Status |
| --- | --- | --- |
| Apisa-Wright, arXiv:1708.03411: Thms 1.2, 1.4, 3.6; Lemma 3.3 | Sections 3 to 5 | READ in d18, d19 |
| Apisa, arXiv:2110.07540: Thms 1.3, 1.5; Section 1.5 | Sections 3, 5 | READ-S |
| Apisa-Wright, arXiv:2102.06567: Thm 1.1, Conj 1.2, Question 1.3 | Lemma 2 | READ-S |
| Apisa, arXiv:1710.05505 | Section 3 | READ in d18 |
| Apisa, arXiv:1601.07894; Apisa-Wright Thm 1.3 | Section 3 | MEMORY |
| Eskin-Filip-Wright | Section 3 | READ as quoted |
| Moeller; Apisa-Saavedra-Zhang | Sections 3, 6 | READ as quoted; content MEMORY |
| Lanneau, hyperelliptic components of quadratic strata | Lemma 2 | MEMORY |
| McMullen; Calta; Eskin-McMullen-Mukamel-Wright | Sections 3, 6 | MEMORY |
| d18 Theorems C, L; d19 Theorem A; d2 claim 1 | Throughout | Read in the project files |
