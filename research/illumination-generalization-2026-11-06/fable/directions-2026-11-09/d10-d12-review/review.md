# Second-reader review of `d10-mechanisms/theory.md` and `d12-lit-side/notes.md`

Date: 2026-11-09. Reviewer: Fable subagent, adversarial second reader.
Scope: every named statement in the two write-ups, checked by hand and by exact
permutation arithmetic on the saved census, n <= 10. No room search was run.

## Result

No named statement is false. One proof has a real gap, and four statements need a
corrected wording or a corrected dependency list.

- **Gap, now closed:** Proposition R4, step 3, assumes that the degree-3 fold target
  is the planar L-tromino. That is wrong when the two `[2,1]` classes are adjacent.
  The target is then a 3-cell disc with an interior cone point, and a strictly simple
  room (the Z-hexomino) folds onto it. A patch in this file closes the case. The patch
  has one author and no second reader.
- **Wording that changes truth:** Proposition R1 needs "gcd 1 of the edge lengths in
  each direction". `theory.md` never defines "normalized". The coordinator log
  paraphrases it as a statement about parity classes of corners. Under that reading
  R1 is false.
- **Dependency list:** D1 does not use R1 or R4. It is Theorem U over `B` plus the
  first sentences of R3, parts 1 and 2. D1 is fully proved for rooms, given the
  standing dictionary D0.
- **Missing definition step:** the notes never show that `M_t` is a group or that it
  is the same group in every state. Both are true, and the argument is three lines.
- **Computation:** every count that this review recomputed equals the authors' count.
  The recomputation covers all 3,882 census orbits with q >= 2 and all 12,864 pairs.

## Verdict table

Verdicts: CONFIRMED, CONFIRMED WITH CORRECTION, GAP, FALSE. D2 and D3 are
conjectures, so they get a status and no verdict.

### `d10-mechanisms/theory.md`

| Statement | Verdict | Reason |
| --- | --- | --- |
| Fact L, Lemma 1, Lemma 2 | CONFIRMED | Proofs are complete. |
| Lemma 0 (change of base) | CONFIRMED | Proof is a sketch that rests on D0. Only relative certificates use it. |
| Theorem U | CONFIRMED | Par, Rig, and Cut proofs hold. 0 of 12,425 LIT pairs carry a full certificate in an independent implementation. |
| Proposition R1 | CONFIRMED WITH CORRECTION | True for gcd 1 per axis. False if "normalized" means "corners occupy three parity classes". |
| Proposition R2 | CONFIRMED | Needs one interior point only. No normalization. |
| Proposition R3 (support) | CONFIRMED | All three parts hold. |
| Proposition R4 | CONFIRMED WITH CORRECTION | Step 3 is wrong in the adjacent case. The patch below closes it. The statement survives. |
| Lemma F (fold onto a polygon) | CONFIRMED | Needs an embedded target, as stated. |
| Proposition R5 | CONFIRMED | Holds under its explicit hypothesis. Uses R1, so it needs gcd 1 per axis. |
| Proposition R6 and corollary | CONFIRMED | Case check redone in full. Uses strict simplicity. No normalization in R6. |
| D1 | CONFIRMED WITH CORRECTION | Proved for rooms given D0. The cited dependencies are wrong. |
| D2 | Open conjecture | The corner-by-corner gloss is false, as already known. Not re-derived here. |
| D3 | Open conjecture | Exactly two open cases. See "Open cases of D3". |
| Proposition (same-fibre is D2 and D3) | CONFIRMED | Both directions hold. |

### `d12-lit-side/notes.md`

| Statement | Verdict | Reason |
| --- | --- | --- |
| Lemma 1 (tree of an arc) | CONFIRMED | Proof holds. 0 failures over every state and arc of every orbit. |
| Lemma F (faces, Face certificate) | CONFIRMED | Index computation holds. 466,494 pinches all give a 4-cycle of `h_x`. |
| Counterexample at n = 8 | CONFIRMED WITH CORRECTION | One step needs Lemma 1, not the cycle count alone. The conclusion holds. |
| Lemma T | CONFIRMED | 2,400,774 twist cases lie in `M_t`. 30,237 literal braid words on arcs b, c, d return the tuple. |
| Corollary T1 | CONFIRMED | 364,272 pinch transpositions lie in `M_t`. |
| Corollary T2 | CONFIRMED | Follows from T1 and Jordan's theorem. The theorem number in the citation was not re-read. |
| Lemma C | CONFIRMED | Proof holds given D0. No DARK pair has a cylinder witness, n <= 10. |
| Lemma G | CONFIRMED | Proof is complete. |
| Proposition N | CONFIRMED | Proof holds given D0. Not tested by computation, here or in the notes. |
| Proposition R | CONFIRMED WITH CORRECTION | Add the proof that `M_t` is a group and is state independent. Vacuous at q = 2. |

## The single most serious problem

**The room-side arguments treat fold targets as planar polygons, and they are not.**

- R4, step 3, says "`P` folds onto the planar tromino `K`". The degree-3 cover with
  types `[2,1]`, `[2,1]`, `[1^3]`, `[3]` has two forms. If the two `[2,1]` corners are
  diagonal, it is the double of the L-tromino. If they are adjacent, it is the double
  of a disc `K2` with an interior cone point of angle pi.
- `K2` is a real fold target. The Z-hexomino `H` is strictly simple, has gcd 1 per
  axis, and folds onto `K2`. For the wall pair `(2,0)`, `(0,2)` of `H`, Cut holds at
  the adjacent class `b`, and the pair is LIT.
- R4 survives because it is stated for interior marks, and `H` has one interior
  point. The written proof does not show that. The patch does.
- The same assumption is the open case of R5 and of D3. So every "PROVED" row for
  rooms in section 3.8 of `theory.md` rests on either R1 or a planar-target step.

If you build on the room side, do not reuse "the target is an embedded polygon"
without proof. The smallest counterexample has degree 3 and a 6-cell room.

For the lit side, the lemmas that `d14-lemma-h` uses are sound: Lemma 1, Lemma F,
Lemma T, T1, T2, and Proposition R all hold and reproduce exactly. The caveat there
is evidence, not proof: Lemma H is vacuous at q = 2, and 1,242 of the 2,885 supporting
orbits have q = 2.

## Corrected statements in full

### Proposition R1, corrected

**Definition.** A simple orthogonal lattice polygon is *normalized* when two conditions
hold. The greatest common divisor of its horizontal edge lengths is 1. The greatest
common divisor of its vertical edge lengths is 1.

**Proposition R1.** Let `P` be a normalized simple orthogonal lattice polygon. Then
`B` is the only pillowcase factor of `DP`.

The proof in `theory.md` is correct for this definition. Two remarks:

- The lift `D` exists because a regular point of `DP` over a pole of `P'` maps by the
  local quotient by `-1`. So the face maps to the orbifold `P'` as a local isometry.
- A zero of `DP` maps to a pole of `P'` because a pillowcase has no zero. Fact L alone
  allows a zero to map to a zero.

**The weaker hypothesis fails.** Normalized implies that the corners occupy at least
three parity classes. The converse is false, and R1 is false under the weaker
hypothesis. Example, checked by `room_r1.py`: the L-tromino stretched by 3 along x.

- Cells: `(i,0)` for i = 0..5 and `(i,1)` for i = 0..2. Vertices: `(0,0)`, `(6,0)`,
  `(6,1)`, `(3,1)`, `(3,2)`, `(0,2)`. The corners occupy all four parity classes.
- Tuple, cells sorted: `[[0,1,4,5,2,3,7,6,8],[2,3,0,1,6,5,4,8,7],[3,2,1,0,6,4,5,8,7],[1,0,5,4,3,2,7,6,8]]`.
- Block system `(0,0,1,1,2,2,2,1,0)` gives a factor of degree 3 with types `[2,1]` at
  every corner. That factor is a pillowcase other than `B`.

The coordinator log says "G1 needs two classes with no corner, which the normalization
forbids". That sentence describes the weaker property. Section 1 (ii) of `theory.md`
already notes that the parity argument fails for odd index. State the definition
above wherever R1, R4, R5, or section 3.8 is cited.

### Proposition R4, corrected proof

The statement is unchanged:

**Proposition R4.** Let `P` be a strictly simple normalized orthogonal lattice room.
Let `S != T` be interior lattice points of class `a`. Suppose Cut(x) holds for a lift
pair of `(S, T)` and class `x` has a transparent point. Then `x` is the class diagonal
to `a`, `P` is the 12-wall cross, and the pair is LIT.

Steps 1, 2, 4, and 5 of the written proof hold. Replace step 3 by the following.

**Step 3a.** The factor `N` has types `[2,1]` at `a`, `[2,1]` at `x`, `[3]` at `y`,
and `[1^3]` at `w`. A product-one triple of two transpositions and a 3-cycle in `S_3`
is unique up to conjugation. So `N` is determined by which corner is `x`. The deck
group is trivial, so the reflection of `N` is unique.

**Step 3b, `x` diagonal to `a`.** `N` is the double of the planar L-tromino. Continue
with steps 4 and 5 as written.

**Step 3c, `x` adjacent to `a`.** Name the corners so that `x = b`, `w = c`, `y = d`.
Then `N` is the double of the disc `K2` given by

    kappa_ab = id,  kappa_bc = kappa_cd = (1 2),  kappa_da = (2 3),
    g_a = (2 3),  g_b = (1 2),  g_c = id,  g_d = (1 2 3).

Cells 1 and 2 share both edges at their `c`-corner. That corner is an interior cone
point of angle pi.

- A point of `P` over the cone point is interior to `P`, because a fold maps walls to
  the boundary of the target. It has four cells and maps with local degree 2.
- So each component of the preimage of the interior of `K2` is the branched double
  cover of `K2`. That cover is the Z-hexomino `H` with cells `(-1,1)`, `(0,1)`,
  `(1,1)`, `(0,0)`, `(1,0)`, `(2,0)`, up to a lattice isometry that keeps classes.
  Its centre `(1,1)` has class `c`.
- `P` is a union of whole copies of `H` with disjoint interiors. Two neighbouring
  copies are mirror images in a side line. In a strictly simple room, an edge with a
  cell on both sides is not a wall.
- `H` has cells on both sides of the side lines `y = 1`, `x = 0`, and `x = 2`. A mirror
  copy in one of those lines overlaps `H`. So every edge of `H` on those lines is a
  wall of `P`, and no cell of `P` lies across it.
- The other side lines are `y = 0`, `y = 2`, `x = -1`, and `x = 3`. The rotation of
  `H` about `(1,1)` keeps classes and swaps `y = 0` with `y = 2` and `x = 3` with
  `x = -1`. So two cases remain.
- **Mirror in `y = 0`.** The corner `(0,0)` has class `a` and is a pole of `N`. Its
  star holds the cells `(0,0)` and `(0,-1)`. The cells `(-1,0)` and `(-1,-1)` lie
  across the line `x = 0` from a copy, so they are not in `P`. So `(0,0)` is a smooth
  wall point of class `a` over a pole. Cut forbids that.
- **Mirror in `x = 3`.** The corner `(3,0)` has class `b` and is a pole of `N`. Its
  star holds `(2,0)` and `(3,0)`. A third cell `(2,-1)` or `(3,-1)` needs a mirror in
  `y = 0` of `H` or of its copy, which the previous case excludes. So `(3,0)` is a
  smooth wall point of class `b = x` over a pole. Cut forbids that.
- So `P = H`. `H` has one interior lattice point, of class `c`. It has no interior
  pair of class `a`. The adjacent case does not occur under the hypotheses.

The same check of third and fourth cells is needed in step 4 of the written proof.
There a short-side mirror puts a second cell at a convex corner of class `a` or `x`.
A third cell would lie across a side line that the tromino straddles. So the point is
smooth, as the written proof says.

`room_r4.py` confirms the objects on fixed polygons:

- `H` has a kappa-invariant factor of degree 3 with types `[2,1]`, `[2,1]`, `[1^3]`,
  `[3]`. No regular point of class `a` or `b` lies over a pole of it.
- `H` with its mirror in `y = 0` has regular points over poles: one of class `a`, one
  of class `b`.
- For `H` and the wall marks `(2,0)`, `(0,2)`, the certificates at b, c, d are Cut,
  none, Par. The decider says LIT.
- For the 12-wall cross with `S = (1,2)`, `T = (3,2)`, all four lift pairs have none,
  Cut, Par at b, c, d, and the decider says LIT.

Scope note. R4 is false for smooth wall marks if you keep the conclusion "`x` is
diagonal to `a`". The pair on `H` above is the example.

### D1, corrected

**D1.** Let `P` be a strictly simple orthogonal lattice room, and let `S != T` be
interior lattice points of class `a`. Suppose one of two conditions holds for each
class `x` in `{b, c, d}` and each of the four lift pairs. Either `B_x` separates the
lift pair, or Rig(x) holds for `DP / R_y` with some `y` outside `{a, x}`. Then no
billiard path joins `S` to `T`.

Proof. Fix a lift pair. Take `P' = B` in Theorem U, so the targets are `b`, `c`, `d`.
If `B_x` separates, then `DP / B_x` satisfies Par(x) by the first sentence of R3,
part 1. Otherwise `DP / R_y` satisfies Rig(x), because it has identity monodromy at
`y`. Theorem U makes the lift pair DARK. A billiard path from `S` to `T` unfolds to a
straight segment between two lifts with regular interior. By D0 that segment is a
chain in some state.

Changes against `theory.md`:

- The proof does not use R1 or R4, and it does not need normalization.
- R1 and R4 serve a different claim: that D2 is the room form of U\*. R1 removes the
  relative certificates. R4 removes Cut.
- The proof uses Theorem U only with `P' = B`. Lemma 0 is not used.
- The only unproved input is D0, the project's standing dictionary.

### Proposition R, with the missing step

**Definition.** Give each regular a-point of a base state an ID. A braid move carries
the IDs along. Let `M` be the set of permutations `pi` of the IDs such that `(t, pi L)`
lies in the pure-braid orbit of `(t, L)`, up to simultaneous conjugation.

**Lemma (well defined).** `M` is a subgroup of the symmetric group on the IDs. It does
not depend on the state `(t, L)` chosen in the marked orbit.

Proof. Renaming IDs commutes with every braid move and with conjugation. If `pi` and
`rho` lie in `M`, apply `rho` to the path from `(t, L)` to `(t, pi L)`. That gives a
path from `(t, rho L)` to `(t, rho pi L)`, so `rho pi` lies in `M`. A finite set closed
under products is a group. If `(t', L') = beta (t, L)`, then `(t', pi L') = beta (t,
pi L)`. So `pi` works at `t'` exactly when it works at `t`.

**Proposition R.** If `M` is 2-homogeneous on the IDs and one pair is LIT, then every
pair of the orbit is LIT.

The proof in the notes holds once `M` is defined this way. Edge cases:

- q = 0 and q = 1: no pair exists. The census data starts at q = 2.
- q = 2: there is one pair, and every subgroup of `S_2` is 2-homogeneous. The
  proposition says nothing.
- q = 3: 2-homogeneous equals transitive.

### Counterexample at n = 8, corrected step

Replace "The cycle counts 3 + 4 + 3 = 8 + 2 show that `(h_b^-1, g_c, g_d)` is one
genus-0 component" by:

By Lemma 1 the graph of the arc a-b is a tree. It has 3 Gamma-components (the chain
component, the 3-cycle, the fixed sheet) and 3 annuli. So it has one T-component, and
`<g_c, g_d>` is transitive. The count 3 + 4 + 3 = 8 + 2 then gives genus 0.

The cycle count alone also allows two components of total genus 1. The list of three
multigraphs with degrees 3, 3, 2 is complete, and their face types are right.

### Theorem U, one remark (no correction)

In the Cut proof, the case "`C` is a cycle" never occurs. `T` is connected and
disjoint from `C`, so `T` lies in one of the two discs bounded by `C`. An annulus that
borders `C` on the other side has its far end on `T`. That is impossible. The written
argument for the cycle case is also correct, so the proof stands as written.

## Counterexamples and explicit objects

This review found no counterexample to any named statement. It found three explicit
objects that mark where a proof or a wording breaks.

| Object | Data | What it shows |
| --- | --- | --- |
| `K2`, degree 3 | `[[0,2,1],[1,0,2],[0,1,2],[2,0,1]]`, types `[2,1]`, `[2,1]`, `[1^3]`, `[3]` | The Cut target in the adjacent case. Not a planar polygon. |
| Z-hexomino `H`, degree 6 | `[[2,1,0,5,4,3],[0,3,4,1,2,5],[0,4,3,2,1,5],[2,0,1,4,5,3]]`, block system `(0,1,2,2,1,0)` | A strictly simple normalized room that folds onto `K2`. R4, step 3, fails here. |
| Stretched L-tromino, degree 9 | Tuple under "Proposition R1, corrected" | R1 fails when "normalized" means three parity classes. |

The known counterexample to the per-corner converse reproduces:
`[[1,2,0,4,3,6,5,7],[0,1,2,3,4,5,7,6],[5,6,3,2,7,0,1,4],[6,7,4,1,5,2,0,3]]`, `|G|` =
40,320, primitive, plain orbit 9, x-lit at (b, c, d) = (0, 1, 1), no certificate over
`B` at any corner.

## Line-by-line notes on `theory.md`

### Section 0

- **Fact L.** Correct. A sheet count around the point gives `len(q) = e len(p)`.
- **Lemma 1.** Correct. Regular points map to live points by the definition of live.
- **Lemma 2.** Correct. The Cut proof uses only the path case. See the remark above.
- **Lemma 0.** The proof is two sentences and appeals to D0. It is used for G1 and G7
  only. In the census that is 12 DARK pairs. For normalized rooms it is not used.

### Section 2, Theorem U

Restatement. Fix a pillowcase factor `P'` of `Q` with `sigma`, `tau` over corners
`c_s`, `c_t` of `P'`. Targets: the three other corners if `c_s = c_t`, else `c_t`. If
every target `x` has a factor `N` between `Q` and `P'` with Par(x), Rig(x), or Cut(x),
the pair is DARK.

- **Reduction.** A light path projects to a path that runs along one saddle connection
  from `c_s` to a corner `x`. If `c_s != c_t`, the path ends over `c_t`, so `x = c_t`.
- **Par.** Correct. Zeros are never live, so live vertices over `x` are poles and
  leaves. Par is defined only for `c_s = c_t`.
- **Rig.** Correct. In the sphere minus three points, a simple arc between two of them
  is unique up to isotopy. The isotopy lifts to `N` and fixes each fibre pointwise.
- **Cut.** Correct. See the remark on the cycle case. The bound `deg(N -> P') <= 3`
  follows from the single cycle at one corner.
- **Marked points and cone points.** The proof keeps them apart correctly. Liveness is
  a property of a point of `N`, defined through the regular points of `Q` above it.

### Section 1 and 3, rooms

- **R1.** See the corrected statement.
- **R2.** Correct. The adjacent case uses the two mid-side points of the block around
  `S`. The diagonal case uses its four corners and connectedness of `P`.
- **R3.** Correct. Part 1 uses Fact L for blocks made of 3-cycle cells. Part 2 applies
  Lemma 1 to `DP / R_y -> N`. Part 3 holds because each kappa normalizes `G`.
- **R4, step 1.** Correct. The type `[3]`, `[3]`, `[1^3]`, `[1^3]` is excluded because
  `a` needs a regular point of `N`.
- **R4, step 2.** Correct. The orbit of intersecting pairs has size 3, 6, or 9. Size 9
  gives branching 6 + 4 + 4 = 14 on 9 sheets, so genus -1. Size 6 forces the two
  kernels to agree, by Goursat's lemma, and gives the regular `S_3` cover.
- **R4, step 3.** Gap. See the corrected proof.
- **R4, steps 4 and 5.** Correct. With 1, 2, or 3 copies there are 0, 1, or 2 interior
  points, and the 2 points with 3 copies have different classes.
- **Lemma F and R5.** Correct. Each cell of the target has walls on both edges at its
  `y`-corner, so all cells share the opposite corner. The tromino case uses Lemma F at
  the convex corner `(1,2)`.
- **R6.** Correct. Steps that the write-up leaves out, all checked:
  - A block system of block size 2 always comes from a deck involution.
  - The centre `O` is a lattice point and is interior to `P`. This uses strict
    simplicity.
  - A mirror axis meets the boundary in exactly two points.
  - `O +- (1,0)` and `O +- (0,1)` have 2 or 4 cells by mirror symmetry.
  - Cases `{h, v}`, `{o, h}`, `{o, v}` end with `P` equal to the 2 x 2 block. A class
    `w` diagonal to `O` has no transparent fixed point.
- **Corollary.** Correct. A separating `B_x` with 2 blocks is a pillowcase, which R1
  excludes. Each zero of the factor has `delta` zeros above it.

### Room properties assumed without proof

| Property | Where it is used | Status |
| --- | --- | --- |
| Normalization means gcd 1 per axis | R1, hence R4 step 1, R5, corollary of R6, section 3.8 | Used in the proof of R1, never stated as the definition. |
| Corners occupy three parity classes | Coordinator log, section 1 (ii) | Weaker than normalization. Not enough for R1. |
| Fold target is a planar polygon | R4 step 3, R5 | False in general. R5 states it as a hypothesis. R4 assumes it. |
| Copies of the target in `P` are whole | R4 step 4, Lemma F | True for a target with no interior cone point. For `K2` the copy is the double cover `H`. |
| A convex corner that gains a cell becomes smooth | R4 step 4 | True, but the proof must exclude a third cell. See the patch. |
| Strict simplicity | R4 step 4, R6 | Stated in section 3. Used where the write-up says "embedded". |
| A class with only convex corners (class A) | R2 | Proved. Needs one interior point. |
| Dictionary D0 | Theorem U for rooms, D1, Lemma C, Proposition N | Standing model. Not re-proved in either write-up. |

## Is D1 fully proved for rooms?

Yes, given D0. The proof is Theorem U with `P' = B`, applied to each of the four lift
pairs, plus the first sentences of R3 parts 1 and 2. It needs no normalization, no
R1, no R4, and no Lemma 0. See "D1, corrected".

## Open cases of D3

D3 says: if `b`, `c`, `d` are certified, then `B_min = B_b v B_c v B_d` separates all
four lift pairs. Let `X` be the set of classes in `{b, c, d}` with a transparent point.
For a class outside `X`, `B_x` is the discrete partition.

D3 holds in these cases:

- Every class is certified by Par for every lift pair, and the `B_x` with `x` in `X`
  are pairwise comparable. This includes `X` empty and all `B_x` equal.

D3 is open in exactly these two cases:

- **O1, two parity factors.** Every class is certified by Par for every lift pair.
  Two classes of `X` have incomparable `B_x`. The join does not separate some lift
  pair. Proved constraints: the two are not both of block size 2 (R6). One has block
  size at least 3 and at least 3 blocks. So n >= 9 and r >= 3.
- **O2, rigid route.** For some class `x` and some lift pair, `B_x` does not separate,
  and Rig(x) holds for `DP / R_y` with `y` outside `{a, x}`. Then `R_y` is neither
  discrete (R2) nor the one-block system. `P / R_y` is not an embedded lattice
  polygon (R5). So it overlaps itself or has an interior cone point.

A fully certified room of type O2 refutes D3 at once. `B_min` is coarser than `B_x`,
so it does not separate that lift pair. `K2` shows that interior cone points occur for
fold targets of strictly simple rooms. So O2 is not an empty class of targets.

## Line-by-line notes on `notes.md`

- **Conventions.** `M_t` is defined in one sentence. See "Proposition R, with the
  missing step". The pure braid group is used throughout the proved statements. The
  full braid group appears only in the Klein symmetry data, which this review did not
  check.
- **Lemma 1.** Correct. Every preimage circle separates the sphere `Q`, so the dual
  graph is a tree.
- **Lemma F.** Correct with `h_x(i) = g_x(g_a(i))`. For `x = d` the arc-adapted product
  is `g_d g_a`, and the cycle runs in the opposite direction. The cycle type is the
  same. The Face certificate follows. Its counts from `face.py` were not recomputed.
- **Tree criterion.** It is a restatement of Lemma 1, as the notes say. It decides
  classes, not orbits.
- **Counterexample at n = 8.** See the corrected step. The two imprimitive families
  with `|G|` = 192 and 384 are marked `[PROVED]` by short sketches. This review did
  not check the sketches. Their conclusions agree with the computed x-lit sets.
- **Lemma T.** Correct. The phrase "sheet k(i) or its inverse" leaves the direction
  open. That is harmless, because `M_t` is a group. The claim for arcs c and d is
  confirmed by literal braid words: `s0, s1^(2m), s0^-1` for c, and `s1^(2m)` followed
  by a global conjugation for d.
- **Corollary T1.** Correct. No other cycle length is divisible by 4, so the least
  common multiple `l` has 2-adic valuation at most 1, and `m = 2 mod 4`.
- **Corollary T2.** Correct. The cited theorem is classical. The theorem number is
  quoted from memory in the notes and was not re-read here.
- **Lemma C.** Correct given D0. Marks on one boundary component are excluded, as the
  notes say.
- **Lemma G.** Correct. For a class with no 2-cycle, `B_x` is discrete.
- **Proposition N.** Correct given D0. A shortest path does not revisit a point, so
  the a-point at `v` differs from `s`.
- **Proposition R.** See above.
- **Literature.** The citations were not re-verified in this review.

## Computation

All scripts are in this directory. They share no code with the authors' scripts. They
read the census representatives and verdicts from `d6-hurwitz-census`, and they read
`d12-lit-side/mine_nN.json` for comparison only. `room_r4.py` calls the d6 decider for
two verdicts. Every run used at most 2 worker processes.

| Script | What it does | Command |
| --- | --- | --- |
| `lib.py` | Permutation arithmetic, braid moves, block systems | |
| `check_m.py` | `M_t` by Schreier generators on the plain orbit; Lemma 1, Lemma F, Lemma T, T1 | `python3 -B check_m.py N 2` |
| `compare_m.py` | Compares with the census and with d12 | `python3 -B compare_m.py 4 5 6 7 8 9 10` |
| `check_u.py` | Theorem U from the definitions, all three kinds over every pillowcase base | `python3 -B check_u.py 4 5 6 7 8 9 10` |
| `percorner.py` | Corner-by-corner soundness, PRIM counts | `python3 -B percorner.py 4 5 6 7 8 9 10` |
| `check_c.py` | Lemma C cylinder witnesses | `python3 -B check_c.py N 2` |
| `room_r4.py`, `room_r1.py` | Fixed polygons for R4 and R1 | `python3 -B room_r4.py` |

Outputs: `m_nN.json.gz`, `u_nN.json.gz`, and the `.log` files. The directory holds
less than 1 MB.

### Theorem U (`check_u.py`)

| n | LIT pairs | LIT with a full certificate | DARK pairs | DARK with a full certificate |
| --- | --- | --- | --- | --- |
| 4 | 9 | 0 | 3 | 3 |
| 5 | 22 | 0 | 1 | 1 |
| 6 | 210 | 0 | 6 | 6 |
| 7 | 345 | 0 | 12 | 12 |
| 8 | 1,522 | 0 | 84 | 84 |
| 9 | 2,766 | 0 | 175 | 175 |
| 10 | 7,551 | 0 | 158 | 158 |
| Total | 12,425 | 0 | 439 | 439 |

- The table equals the table in `theory.md`, section 2.4.
- Full certificates over a proper pillowcase: 6 pairs at n = 8 and 6 at n = 10. All
  have base degree 2. Three of the n = 10 pairs have marks over two different corners.
- LIT pairs at n = 10 with certificates at two of three corners: 948. This equals the
  count in `theory.md`.
- DARK pairs with no separating parity factor: 3, 12, 87, 36 for n = 7 to 10. Of
  these, 3, 6, 87, 30 have certificates at b, c, d over `B`. The total is 126, as
  stated under D3.
- Corner by corner: 0 of 38,592 pair-corners are x-lit with a certificate at x.
- The search for a Rig arc never reached its state cap of 4,000.

### `M_t`, Proposition R, Lemma T (`check_m.py`, `compare_m.py`)

The run covers every census orbit with q >= 2: 12, 23, 114, 213, 541, 962, and 2,017
orbits for n = 4 to 10. That is 3,882 orbits. It includes all 214 imprimitive orbits
and all 27 primitive orbits without `A_n` at n <= 8.

| Check | Result |
| --- | --- |
| Plain orbit size against the census | Equal in 3,882 of 3,882 orbits |
| Pair verdict from chains closed under `M`, against the census | 0 of 12,864 differ |
| `|M|` and number of `M`-orbits on pairs, against d12 | Equal in every orbit |
| Per-corner x-lit and one-mirror flags, against d12 | 0 of 38,592 differ |
| `M`-orbits on pairs with mixed verdict | 0 |
| Orbits with `M` 2-homogeneous, some pair LIT, some pair DARK | 0 |
| Lemma 1 tree identity, every state and arc | 0 failures |
| Lemma T, twist element in `M` | 2,400,774 of 2,400,774 |
| Lemma T, literal braid words on arcs b, c, d | 30,237 pass, 0 fail |
| Lemma F, pinch gives a 4-cycle of `h_x` | 466,494 of 466,494 |
| T1, transposition in `M` | 364,272 of 364,272 |

`M_t` for G containing `A_n`, which equals the table in the notes:

| n | Orbits | M = S_q | 2-homogeneous, not S_q | Not 2-homogeneous |
| --- | --- | --- | --- | --- |
| 4 | 6 | 3 | 3 | 0 |
| 5 | 22 | 19 | 3 | 0 |
| 6 | 57 | 54 | 3 | 0 |
| 7 | 209 | 197 | 12 | 0 |
| 8 | 368 | 362 | 6 | 0 |
| 9 | 798 | 792 | 0 | 6 |
| 10 | 1,535 | 1,511 | 24 | 0 |

- PRIM with G containing `A_n`: 2,885 orbits, 8,952 pairs, 0 orbits fail
  2-homogeneity. Of the 2,885 orbits, 1,242 have q = 2, where the claim is vacuous.
  The other 1,643 have q >= 3.
- PRIM orbits that fail at n = 8: 6, with `|G|` = 1,344 or 336, q = 4, `|M|` = 8, and
  2 pair orbits.
- PRIM orbits that fail at n = 10: 3, with `|G|` = 60, q = 4, `|M|` = 4, and 3 pair
  orbits.
- G containing `A_n`, outside PRIM, that fail: 6 at n = 9 (a of type `[3,2,2,2]`, one
  identity corner, q = 3, `|M|` = 1).
- Proposition R is not vacuous in 1,916 orbits (2-homogeneous, q >= 3). All pairs are
  LIT in 1,870 of them and DARK in 46.
- PRIM pairs: 9,118, all LIT, all with a one-mirror witness.
- Take PRIM pair-corners with a 2-cycle at x. The one-mirror x-lit counts are 2,229
  of 2,235, 5,202 of 5,202, and 12,351 of 12,357 for n = 8, 9, 10.
- LIT pairs with a one-mirror witness: 12,398 of 12,425. The 27 others split 9, 3, 15
  for n = 8, 9, 10.
- Pair-corners that are not x-lit and have no certificate over `B`: 51, 18, 153 for
  n = 8, 9, 10.

### Lemma C (`check_c.py`)

| n | Pairs | DARK with a cylinder witness | LIT without a cylinder witness | PRIM pairs with a cylinder witness |
| --- | --- | --- | --- | --- |
| 4 | 12 | 0 | 3 of 9 | 0 of 3 |
| 5 | 23 | 0 | 12 of 22 | 10 of 19 |
| 6 | 216 | 0 | 60 of 210 | 57 of 99 |
| 7 | 357 | 0 | 75 of 345 | 270 of 339 |
| 8 | 1,606 | 0 | 246 of 1,522 | 790 of 958 |
| 9 | 2,941 | 0 | 693 of 2,766 | 1,866 of 2,325 |
| 10 | 7,709 | 0 | 765 of 7,551 | 4,898 of 5,375 |

The per-corner cylinder flags equal d12's flags on every pair-corner. The witness set
is closed under `M`, which is the same as a search over the marked orbit.

### Other reproduced facts

- Nielsen class n = 6, `[2,2,1,1]`, `[2,2,1,1]`, `[3,2,1]`, `[3,2,1]`: two `S_6` orbits
  of sizes 24 and 72.
- Nielsen class n = 7, `[2,2,2,1]`, `[3,2,1,1]`, `[3,2,1,1]`, `[3,2,1,1]`: two `S_7`
  orbits of sizes 360 and 102.

## What this review did not check

- Dictionary D0. Both write-ups take it from earlier project work.
- The witness-distance tables, the Klein symmetry data, the group `W`, `induct.py`,
  `pinned.py`, and the Face certificate counts in the notes.
- The two `[PROVED]` sketches for the imprimitive families at n = 8.
- `check_saved_rooms.py`, `immersed_flag.py`, and the failed designs in section 3.5 of
  `theory.md`. They read saved room data, and this review ran no room search.
- The literature citations and theorem numbers.
- Proposition N by computation. The census model has no flat distances.
- The patch for R4. It is a hand argument by one reader, with fixed-polygon checks
  only.
