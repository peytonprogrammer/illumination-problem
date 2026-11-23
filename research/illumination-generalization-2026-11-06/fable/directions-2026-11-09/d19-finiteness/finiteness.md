# Finiteness of dark configurations per stratum: check of the proposed argument

Date: 2026-11-10. Direction d19. Nobody has reviewed this document.

Status tags:

- **PROVED**: a complete proof or proof sketch is in this document.
- **READ**: published, and I read the statement in the arXiv TeX source today.
- **MEMORY**: published or standard, cited from memory, not re-read.
- **OPEN**: not proved and not refuted.

## 1. Verdict

The argument proves a finite decomposition of the dark locus. It doesn't prove
the stated conclusion. Three corrections are needed.

1. **Step 3 is false for homothety.** `diag(1, n) P` is a lattice room in the
   orbit of `P` for every `n`. Finiteness per closed orbit holds up to
   independent scaling of the two axes (Lemma 3).
2. **Step 4 omits one alternative.** Apisa-Wright Theorem 3.6 allows a dark pair
   of periodic points with no fold structure (type a-per below).
3. **Torus-cover families (type b) are untouched.** No cited theorem applies to
   them.

The finiteness is ineffective. The result is a short corollary of published
theorems. I didn't find it stated anywhere (Section 7).

## 2. Setting

- `Q_r = Q(1^r, -1^(r+4))`, with `r >= 1`. Its complex dimension is `2r + 2`.
  It's connected (MEMORY: genus-0 strata are connected).
- `Q_r''` is the stratum with two more labeled marked points `S != T`, neither
  a cone point. Its complex dimension is `2r + 4`.
- `(X; S, T)` in `Q_r''` is *lit* if a geodesic segment joins `S` to `T` and has
  no cone point in its interior. Zeros and poles are cone points. Otherwise the
  point is *dark*. `D_r` is the set of dark points.
- A room pair `(P; S, T)`, with `S`, `T` not corners, gives the two points
  `(DP; S+, T+)` and `(DP; S+, T-)`. The room pair is dark iff both are in
  `D_r` (d16, Section 2). Corner points need the strata with fewer marked
  points; the same argument applies there.
- `Phi` maps `(X; S, T)` to its orientation double cover. Mark the `r + 4` pole
  lifts and the 4 lifts of `S`, `T` as zeros of order 0. The image lies in
  `H = H(2^r, 0^(r+8))`, of genus `r + 1`.

## 3. The theorem that the argument yields

**Theorem A. PROVED, given the cited inputs.** Fix `r >= 1`.

1. `D_r` is closed in `Q_r''` and `GL(2, R)`-invariant.
2. `D_r = M_1 ∪ ... ∪ M_m`, a finite union of affine invariant submanifolds,
   none contained in another. Here an affine invariant submanifold of `Q_r''`
   means `Phi^(-1)` of one in `H`. `diag(1, -1)` permutes the `M_i`.
3. Every dark configuration lies in some `M_i`, and every point of every `M_i`
   is dark. This covers all flat spheres in `Q_r`, not only room doubles, and
   all rooms, not only lattice rooms.
4. Let `N_i` be the closure of the image of `M_i` in `Q_r`. Then `N_i` is a
   proper affine invariant submanifold of `Q_r`, and
   `dim M_i - dim N_i` is 0 or 1.
5. Each `M_i` has exactly one of these types.
   - **(0) Sporadic.** `dim M_i = 2`. `M_i` is a closed orbit. `X` is a Veech
     surface, arithmetic or not, and `S`, `T` are periodic points.
   - **(a-fold)** `dim M_i >= 3`, `N_i` doesn't consist of torus covers, and
     every member `(X; S, T)` has a half-translation cover `f : X -> Q` with
     `f(S) = f(T)`. `Q` is a flat sphere with at least 5 poles and
     `2 <= deg f <= r`.
   - **(a-per)** `dim M_i >= 3`, `N_i` doesn't consist of torus covers, and
     `M_i` isn't of type (a-fold). Then `dim M_i = dim N_i` and `S`, `T` are
     both `N_i`-periodic points. No fold structure is forced.
   - **(b)** `dim M_i >= 3`, and every surface in `N_i` has a torus cover as
     orientation cover. Subtypes: (b1) `N_i` is a closed orbit and one marked
     point moves; (b2) `dim N_i >= 3`, a rank-one family with moving branch
     points.
6. The dark lattice and rational configurations outside types (a-fold),
   (a-per), and (b) lie in at most `m` closed orbits. In each closed orbit the
   room configurations form finitely many orbits of `A'`, the group generated
   by the diagonal matrices and the axis swap.

**Ineffective.** `m` comes from a compactness argument on measures (EMM Theorem
2.3). The proof gives no bound on `m`, on the dimensions, or on the number of
squares of a sporadic configuration. You can't turn Theorem A into a finite
search.

**What Theorem A doesn't say.** It doesn't say that types (a-per) and (b) are
empty. So "all but finitely many dark lattice rooms have a fold structure" is
not proved.

## 4. Check of each step

### Step 1: `D_r` is closed. Correct.

- **READ.** Apisa-Wright, arXiv:1708.03411, Lemma 3.7 (label `L:OB`), states
  it: the locus with a segment from `x_1'` to `x_2'` missing `B'` and the zeros
  "is open and GL_2(R) invariant". LMW, arXiv:1407.2975, Lemma `closed sets`
  (IV) and Corollary `closed sets`, is the same statement for blocking
  cardinality at most `n`.
- **PROVED.** Triangulate `X` by saddle connections with vertex set the cone
  points and `S`, `T`. Take a lit segment with no vertex in its interior. It's
  an edge, or it crosses a fixed sequence of edges at interior points. Edges
  persist nearby. The crossing condition is open in the edge vectors, which are
  period coordinates.
- **Orientation cover. PROVED.** `(S, T)` is lit on `X` iff some lift pair is
  joined upstairs by a segment missing the zeros. A segment through a pole lift
  projects to a path that folds back at the pole. Its image is one arc that
  contains `S` and `T` and no zero. So upstairs the pole lifts can be treated
  as blockers or not; the dark set is the same. Dark on `X` means that both
  lift classes `(S_1, T_1)` and `(S_1, T_2)` are blocked by the finite set of
  pole lifts.
- **Collisions.** When `S` meets `T` or a cone point, the limit leaves `Q_r''`.
  `D_r` isn't closed in a larger space, and nothing requires it. EMM applies to
  closed subsets of the stratum itself. No boundary statement is used.

### Step 2: finite union. Correct, with one extension that isn't literal in EMM.

- **READ.** EMM, arXiv:1305.3015, Theorem 2.2: "Any closed P-invariant subset
  of H_1(alpha) is a finite union of affine invariant submanifolds." It's
  literally stated, for the unit-area locus. The proof takes the maximal
  orbit closures in the set (Theorem 2.1) and gets finiteness from Theorem 2.3,
  the Mozes-Shah analogue. Countability (label `prop:countability`; the number
  2.16 is from memory) isn't needed. No Baire argument is needed.
- **Unit area.** `D_r` is scale-invariant. Apply the theorem to its unit-area
  part and take cones.
- **Marked points. READ in LMW, not in EMM.** EMM defines `alpha` as a
  partition of `2g - 2` and doesn't mention marked points. LMW write, after
  their statement of the EMM theorem: "the results of [EMM] work for strata
  with marked points, i.e. they allow alpha_i = 0". Apisa-Wright use affine
  invariant submanifolds of `H^(*n)` throughout on the same basis. This is the
  standard reading. I didn't verify it inside the EMM proofs.
- **Quadratic differentials. PROVED, given a compactness criterion.** `Phi` is
  continuous, equivariant, finite-to-one, and linear in period coordinates.
  A saddle connection of `X` lifts to saddle connections of the same length,
  and each saddle connection upstairs projects to one. So the shortest saddle
  connections agree. By the compactness criterion for strata (MEMORY:
  Masur-Smillie, with marked points as zeros of order 0), `Phi` is proper. So
  `Phi(D_r)` is closed, and Theorem 2.2 applies to it.
- Apisa-Wright's introduction says a closed invariant subset "is an affine
  invariant submanifold". Read it as "finite union"; EMM Theorem 2.2 is the
  precise form.

### Step 3: closed orbits. Correct for orbits; wrong for "up to scaling".

- **Closed orbit. PROVED, given MEMORY inputs.** Let `P` be a lattice room and
  `S`, `T` rational with denominator `N`. The cover of the torus `R^2 / 2Z^2`
  by the orientation cover, followed by multiplication by `2N`, sends all
  marked points and zeros to 0. So `Phi(DP; S, T)` is square-tiled with all
  marked points at vertices. Its stabilizer is commensurable with `SL(2, Z)`,
  so its orbit is closed (MEMORY: Veech; Gutkin-Judge). Rational non-lattice
  points fit the same statement.
- **Counterexample to homothety finiteness. PROVED.** `diag(1, n)` maps a
  lattice room to a lattice room in the same orbit. The rooms `diag(1, n) P`
  are pairwise non-homothetic.
- **Lemma 3. PROVED, given MEMORY inputs.** Let `O` be a closed orbit in
  `Q_r''`. The room configurations in `O` form finitely many `A'`-orbits.
  *Proof.* Fix `Y_0 = (X_0; S_0, T_0)` in `O`. If `g Y_0` is a room double
  `DP`, the reflection of `DP` pulls back to an orientation-reversing affine
  involution of `X_0` with derivative `rho = g^(-1) diag(1, -1) g` in
  `PGL(2, R)`. The derivatives of affine automorphisms of `X_0` form a lattice
  `Gamma` in `PGL(2, R)` (MEMORY: Smillie, closed orbit iff lattice). A lattice
  has finitely many conjugacy classes of reflections (MEMORY). If
  `rho' = gamma rho gamma^(-1)`, then `g' = c g gamma^(-1)` with `c` in the
  centralizer of `diag(1, -1)`, which is `A'`. `gamma^(-1) Y_0` is `X_0` with
  the marking moved by an affine automorphism. The marked orbit is closed, so
  the marked stabilizer has finite index in `Gamma`, and finitely many markings
  occur. ∎
- Darkness in an orthogonal room is invariant under `A'`. So `A'`-classes are
  the right unit for counting rooms.

### Step 4: Apisa-Wright. Correct for type (a), with a missing alternative.

Let `M_i` have `N_i` not consisting of torus covers. Take a member with `X`
generic in `N_i`, so the orbit closure of `X` is `N_i`. Such members are dense
in `M_i` (PROVED: `M_i -> N_i` is open, and non-generic surfaces lie in
countably many proper submanifolds).

- **READ.** Theorem 3.6: if `x_1`, `x_2` are finitely blocked on a non-torus
  cover, "either they are both M-periodic points or zeros, where M is the orbit
  closure of (X, omega), or pi_Q(x_1) = pi_Q(x_2)".
- **READ.** Lemma 3.3: every translation covering from `(X, omega)` to a
  quadratic differential is a factor of `pi_Q`. So on the orientation cover,
  `pi_Q` factors as the double cover followed by some `f : X -> Q_min`. Then
  `pi_Q(S_1) = pi_Q(T_j)` means `f(S) = f(T)`.
- **Apply.** Both lift classes are blocked by the pole lifts (Step 1). So `S`,
  `T` are both periodic, or `f(S) = f(T)`. If `dim M_i = dim N_i + 1`, a marked
  point isn't periodic, so the fold alternative holds. If
  `dim M_i = dim N_i`, both points are periodic and nothing more is forced.
  That's type (a-per).
- **Degree bound. PROVED.** `Q_min` is a sphere with `k >= 4` poles. `k = 4`
  means the pillowcase, which makes `X` a torus-cover type. So `k >= 5`. Over
  the poles, `X` has `a` poles, `b` regular points of local degree 2, and `c`
  zeros of local degree 3, with `a + 2b + 3c = kd`. Riemann-Hurwitz gives
  `b + 2c <= 2d - 2`. So `(k - 4) d <= a - c - 4 <= r`, and `d <= r`. `d >= 2`
  because `S != T`.
- **Closure. PROVED, sketch.** Let generic members converge to a member
  `(X_0; S_0, T_0)`, with covers `f_n : X_n -> Q_n` of degree at most `r`. A
  short saddle connection of `Q_n` has a short preimage graph. Its vertices are
  cone points or regular points of valence 2. So `X_n` would have a short
  saddle connection or a thin cylinder. Hence the `Q_n` stay in a compact part
  of one stratum. The `f_n` are local isometries, so a subsequence converges
  (Arzela-Ascoli) to a cover `f_0 : X_0 -> Q_0` with `f_0(S_0) = f_0(T_0)`.
  The set of members with such a cover is closed and invariant. So it's all
  of `M_i` (type a-fold), or it misses some generic member (type a-per).
  For a lattice `X_0`, `Q_0` is a pillowcase cover other than the pillowcase.
  This has the shape of the d2 "parity factor other than `PC`". I didn't check
  that `f_0` is a parity factor in the d2 sense.
- **Item 4 of Theorem A. PROVED, given READ inputs.** If `N_i = Q_r`, Theorem
  1.4 says the periodic points are cone points (READ in d18). A generic flat
  sphere has no cover of degree at least 2 by dimension count. So both
  alternatives fail, and `N_i` is proper. `dim M_i - dim N_i = 2` is impossible
  because nearby points light each other.
- **The converse fails. READ in d18.** `f(S) = f(T)` doesn't imply dark.
  Periodic pairs need a direct check.
- **(a-per) is OPEN.** Periodic points of proper submanifolds of genus-0
  quadratic strata aren't classified. Theorem 1.4 covers only whole strata.

### Step 5: the conclusion. Not proved as stated.

Corrected form: Theorem A, item 6. The fold structure holds only for type
(a-fold).

## 5. Type (b): what is known and what isn't

- **READ.** Apisa-Wright Assumption 3.2 excludes torus covers from Section 3.
  Theorem 3.6 gives nothing here.
- **READ.** LMW Theorem 1: on a torus cover every pair is finitely blocked. So
  finite blocking gives no constraint. Earlier results of Gutkin, Monteil, and
  Hubert-Schmoll-Troubetzkoy are MEMORY, or read only as quoted in LMW.
- **READ.** LMW Theorem 2 and its general form: on one translation surface the
  dark set is a finite set plus finitely many affinely embedded surfaces. On
  each, the two projections are finite covers, related by a scalar `lambda`
  with `lambda^2` rational. HST proved this for lattice surfaces (as quoted in
  LMW).
- **(b1). PROVED, sketch, given LMW.** The fiber of a type (b1) component over
  a lattice `X_0` is a two-dimensional piece of LMW's dark set of `X_0`.
  Conversely, the orbit closure of a non-periodic pair on such a piece has
  dimension 3 and lies in a type (b) component. LMW doesn't exclude these
  pieces. A d16 half-rational family is infinite, so all but finitely many of
  its pairs lie on such pieces, for each class. Excluding two-dimensional dark
  pieces on room doubles would close d16 gap 3. This is OPEN.
- **(b2). OPEN.** No published result that I know says whether a family of
  torus covers with moving branch points can be dark at every member.
  Per-surface finiteness (LMW) is not uniform over the family.
- Wolecki Theorem 1.2 claims finitely many dark pairs per rational polygon.
  d16 reports a gap in its Lemma 2.9 in the torus-cover case. I didn't re-read
  it.

## 6. Real loci (actual rooms)

- **PROVED, sketch.** Near a room double `X_0`, the room doubles are the fixed
  set of `c = sigma* ∘ conj` in period coordinates, where `sigma` is the
  reflection. This set is `E_+ ⊕ i E_-`, with `E_±` the eigenspaces of
  `sigma*` on real cohomology. Its real dimension is `2r + 2`.
- Let `N_i` be `V_R ⊗ C` locally (EMM: defined over `R`). The room doubles in
  `N_i` near `X_0` have real dimension
  `dim(V_R ∩ E_+) + dim(V_R ∩ E_-)`. This is at least 2, the `A`-orbit, and at
  most `dim_C N_i`. Equality holds iff `V_R` is `sigma*`-invariant.
- So a "continuous dark family" is a family of flat spheres. It can meet the
  rooms in the `A`-orbit only. The fold structure of type (a-fold) still holds
  on the lattice room itself.
- A room pair needs both `(S+, T+)` and `(S+, T-)` dark. The two points can lie
  in different `M_i` of different types.
- Restricting to rooms doesn't make the finiteness effective.

## 7. Is it already known?

- Step 1 is Apisa-Wright Lemma 3.7 and LMW's closed-set lemma. Step 2 is EMM
  Theorem 2.2. Type (a) is Apisa-Wright Theorem 3.6. All READ.
- LMW run the same argument for the orbit closure of one surface. The
  per-surface results are stronger there: LMW Theorem 2, Apisa-Wright Theorems
  1.1 and 3.10, Wolecki Theorem 1.2.
- I found no statement of the stratum-wide decomposition (Theorem A, items 2
  and 6). The search was one web query plus the introductions of LMW and
  Apisa-Wright. Treat "not in the literature" as likely, not certain. The
  novelty is small: it's a direct corollary.

## 8. Citations

| Source | Used for | Status |
| --- | --- | --- |
| Eskin-Mirzakhani-Mohammadi, arXiv:1305.3015: Theorems 2.1, 2.2, 2.3, countability proposition, proof of 2.2, definitions of `H(alpha)` and affine invariant submanifold | Step 2 | READ |
| Lelievre-Monteil-Weiss, arXiv:1407.2975: Theorem 2, general theorem (form of 2-dim pieces), EMM statement and marked-point note, closed-set corollary | Steps 1, 2, type (b) | READ |
| Apisa-Wright, arXiv:1708.03411: Lemmas 3.1, 3.3, 3.7, Assumption 3.2, Remark 3.5, Theorem 3.6, definition of point markings | Steps 1, 4 | READ |
| Apisa-Wright Theorems 1.1, 1.4, 3.10; Wolecki Theorem 1.2 | Sections 4, 5, 7 | READ in d18, not re-read |
| Hubert-Schmoll-Troubetzkoy | Type (b) | Read only as quoted in LMW |
| Gutkin; Monteil (finite blocking on torus covers) | Type (b) | MEMORY |
| Masur-Smillie compactness; Veech, Gutkin-Judge, Smillie (lattice iff closed orbit); finitely many reflection classes in a lattice; connectedness of genus-0 strata | Steps 2, 3 | MEMORY |
| d16 results 2, 3 and Section 2; d2 corrected claim 4 | Sections 2, 4, 5 | Read in the project files |
