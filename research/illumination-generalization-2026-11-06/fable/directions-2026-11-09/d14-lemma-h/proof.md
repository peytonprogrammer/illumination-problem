# D14: Lemma H, one LIT pair, the group reduction, and the conditional theorem for rooms

Date: 2026-11-09. Scope: the 3,882 saved census orbits with q >= 2, degrees 4 to 10.
This direction enumerates no cover beyond n = 10 and searches no rooms.

## Result in one paragraph

**Lemma H is not proved, and the planned proof cannot work.** Step (i) of the plan
is false. In 72 orbits under the PRIM hypotheses with G containing A_n, every cusp
loop of the Hurwitz curve acts trivially on the regular a-points. Six of them have
q >= 3 (first: n = 7, G = S_7, q = 3, M_t = S_3). There, no state satisfies the
pinch corollary T1, and every twist element is trivial. H is then a statement
about the handles of the Hurwitz curve, and no local tool reaches it. This file proves the tools that do exist.
Lemma H1 is a general twist lemma. Proposition H2 relates M_t, the cusp group,
and the genus of the Hurwitz curve. Lemmas L1 and L3 prove E for rooms in two
ranges. The companion reduction holds with **N_0 = max(6z, z^2) <= 64**. Its
source is a fixed-point-ratio theorem of Burness and Guralnick, read in this
session. For imprimitive covers the file proves projection, lifting, and
double-cover lemmas. The assembled theorem for rooms is conditional on H and on
dictionary D0. **The weakest link is H.** All evidence is at n <= 10 and q <= 5.
The theorem applies at every n > N_0, and N_0 = 64 in the worst case.

## Status tags

- `[PROVED]`: the argument is in this file.
- `[PROVED given D0]`: the argument is in this file and uses dictionary D0.
- `[PROVED elsewhere, reviewed]`: proved in d10 or d12 and confirmed in
  `d10-d12-review/review.md`.
- `[CITED, verified]`: published statement, read from the source in this session.
- `[CITED, from memory]`: published statement, not re-read in this session.
- `[CHECKED n <= N]`: exact computation on every saved orbit up to degree N.
- `[CONJECTURAL]`: open.

## Conventions

This file uses the conventions of `d12-lit-side/notes.md`. The points that matter:

- A state is t = (g_a, g_b, g_c, g_d) with product 1. Products apply the left
  factor first. Cycle lengths are 1 (pole), 2 (regular point), and 3 (zero).
- q is the number of 2-cycles of g_a. A pair is two distinct regular a-points.
- A pair is x-lit when some state of the pure-braid orbit has a chain at x that
  joins the two marks. A pair is LIT when it is x-lit for some x in {b, c, d}.
- A **link** at x is a 2-cycle of g_x whose two sheets lie in two distinct 2-cycles
  of g_a. A link is a chain with one mirror.
- h_x is the product of the arc-adapted pair. The Gamma-components, T-components,
  and annuli of a state are those of d12 Lemma 1.
- The PRIM hypotheses: G is primitive, no corner other than a has identity
  monodromy, and some g_x with x != a has a 2-cycle.
- Families of orbits: **AN** (PRIM and G contains A_n), **PRIM**, and **ALL**.
- Dictionary D0 (rooms to tuples) is the project's standing model. Nobody has
  checked it. Every statement about rooms in this file depends on it.

### Review notes applied

The coordinator's review (`d10-d12-review/review.md`) changes five things here.

1. **Definition of M_t.** This file uses the reviewer's definition throughout: M_t
   is the set of permutations pi of the point IDs such that (t, pi L) lies in the
   marked pure-braid orbit of (t, L). M_t is a group and doesn't depend on the
   state. `cusp.py` builds M_t from Schreier generators with deck maps and asserts
   that its order equals the order saved by `d12-lit-side/mine.py`.
2. **q = 2 is vacuous for H.** Of the 2,885 AN orbits, 1,242 have q = 2 and 1,643
   have q >= 3. Every count for H in this file is split that way.
3. **At q = 2, E is the whole content of PRIM.** The section "Task 2" treats q = 2
   separately.
4. **Normalized** means gcd 1 of the horizontal edge lengths and gcd 1 of the
   vertical edge lengths. The assembled theorem doesn't need the word (Remark R0').
   The imprimitive lemmas of "Task 4" don't assume that a fold target is planar.
5. **D0 is listed as an unchecked dependency** of the assembled theorem.

### Deck maps under the PRIM hypotheses `[PROVED]`

If G is primitive and n >= 4, the deck group C(G) is trivial.

Proof. The centraliser C of a transitive group is semiregular. Its orbits are
blocks of G. If C != 1 and G is primitive, C is transitive, so C is regular. Then
G lies in the centraliser of a regular group, which is regular. So G is regular
and primitive, hence cyclic of prime order n. Its elements are n-cycles, and cycle
lengths are at most 3. So n <= 3.

## Task 1: Lemma H

**Lemma H `[CONJECTURAL]` `[CHECKED n <= 10]`.** Under the PRIM hypotheses with G
containing A_n, M_t is 2-homogeneous on the regular a-points.

### 1.1 Test of every intermediate claim

Source: `cusp.py`, `post.py`, `post_q3.py`. The cusp group **Nbar** is the normal
closure in M_t of all cusp elements. A cusp element is the label permutation of
T_x^w at a state u, where w is the first return time of the plain state u.

Counts for the family AN, n = 4 to 10:

| Claim | q = 2 (1,242 orbits) | q >= 3 (1,643 orbits) |
| --- | --- | --- |
| C1 some cusp element is nontrivial | 1,176 | 1,637 |
| C2 one cusp loop is a transposition or a 3-cycle | 1,176 | 1,637 |
| C4 M_t contains a transposition or a 3-cycle | 1,242 | 1,643 |
| C5 M_t is transitive | 1,242 | 1,643 |
| C6 M_t is primitive | 1,242 | 1,643 |
| C7 M_t is 2-homogeneous (Lemma H) | vacuous | 1,643 |
| C8 M_t = S_q | 1,242 | 1,640 |
| C9 Nbar is transitive | 1,176 | 1,637 |
| C10 Nbar is 2-homogeneous | vacuous | 1,637 |
| C11 Nbar = M_t | 1,176 | 1,622 |
| C12 the transpositions of Nbar connect all points | 1,176 | 1,619 |
| Hurwitz genus 0 | 93 | 114 |

AN orbits with q >= 3 per degree: 21, 71, 165, 508, and 878 for n = 6 to 10. The
values of q are 3 (988 orbits), 4 (451), and 5 (204). So H has 655 tested orbits
with q >= 4, and M_t = S_q in all 655.

First failure of each claim (smallest n, then smallest plain orbit):

| Claim | Family | First failure |
| --- | --- | --- |
| C1, C2, C9, C11, C12 | AN | n = 5, [2,2,1], [2,2,1], [3,1,1], [3,1,1], plain 9, G = A_5, q = 2, M = S_2, Nbar = 1, genus 1 |
| C1, C2, C9, C10, C11 | AN, q >= 3 | n = 7, [2,2,2,1], [2,2,2,1], [3,2,1,1], [3,2,1,1], plain 36, G = S_7, q = 3, M = S_3, Nbar = 1, genus 7 |
| C8, C12 | AN, q >= 3 | n = 6, [2,2,2], [3,1,1,1], [3,1,1,1], [3,2,1], plain 8, G = S_6, q = 3, M = Nbar = C_3, genus 0 |
| C4, C5, C6, C7 | AN | no failure for n <= 10 |
| C5 | PRIM | n = 10, [2^4,1,1] three times and [3,3,3,1], plain 9, G of order 60, q = 4, M of order 4 |
| C6, C7 | PRIM | n = 8, [2^4], [2,2,2,1,1], [2,2,2,1,1], [3,3,1,1], plain 15, G of order 336, q = 4, M of order 8 |
| C7 | ALL | n = 6, [2,2,2], [2,1^4], [2,2,1,1], [3,3], plain 3, G of order 48, q = 3, M of order 2 |

For the family PRIM with q >= 3: 1,680 orbits, M_t 2-homogeneous in 1,671.

### 1.2 Step (i) of the plan is false

The plan's step (i) says that every orbit has a pinch state, or another state
that gives a transposition or a 3-cycle in M_t.

**Fact `[CHECKED n <= 10]`.** 72 AN orbits are **cusp-trivial**: Nbar = 1. The
counts per degree are 0, 3, 3, 24, 18, 14, and 10 for n = 4 to 10. Of these, 66
have q = 2 and 6 have q >= 3:

- n = 7: [2,2,2,1], [2,2,2,1], [3,2,1,1], [3,2,1,1] in any order at b, c, d. Three
  orbits, plain 36, G = S_7, q = 3, M_t = S_3, Hurwitz genus 7.
- n = 9: [2^4,1], [2^4,1], [3,3,1,1,1], [3,3,1,1,1] in any order. Three orbits,
  plain 36, |G| = 181,440, q = 4, M_t = S_4, Hurwitz genus 10.

`check_cusp_trivial.py` confirms the first n = 5 and n = 7 cases with a separate
method. It compares cycle lengths of T_b, T_d, and T_b T_d on marked and plain
states. It also shows
that cusp-triviality belongs to the orbit and not to the Nielsen class. The n = 7
class has a second orbit, plain 84, with Nbar = M_t = S_3.

**Consequence `[PROVED]`.** In a cusp-trivial orbit no state satisfies d12
Corollary T1, and every twist element of d12 Lemma T is trivial. Proof: the set
of m with T_x^m u = u (plain) is w Z. So a Lemma T element at u is a power of the
cusp element at u. Deck maps are trivial under the PRIM hypotheses.

So the "weaker route to H" of d12 (M_t primitive plus one T1 state) fails in
these orbits. This isn't an error in d12 Corollary T2, which is conditional. It
is a limit on its reach.

For q >= 3 the data supports a dichotomy: **Nbar = 1 or Nbar is 2-homogeneous**
(1,643 of 1,643 AN orbits). `[CHECKED n <= 10]` `[CONJECTURAL]`

### 1.3 Lemma H1 (general twist lemma) `[PROVED]` `[CHECKED n <= 8]`

Fix a state t and take x = b. Write h = g_a g_b, Gamma = <g_a, g_b>, and
T = <g_c, g_d>. Let C_Gamma and C_T be their centralisers in S_n. Then h lies in
both Gamma and T. For a permutation k, write k . g for k o g o k^-1.

1. m full twists T_b give (h^-m . g_a, h^-m . g_b, g_c, g_d). The label on sheet s
   moves to sheet h^-m(s). This is the convention of `hurwitz.py`.
2. The plain state returns after m twists if and only if h^m lies in C_Gamma C_T.
3. At a return, write k = c o h^-m with c in C_T and k in C_Gamma. The element of
   M_t is the permutation that k induces on the 2-cycles of g_a. The element c is
   unique up to the deck group, which is the intersection of C_Gamma and C_T.
4. k permutes the Gamma-components and c permutes the T-components. Both map
   annuli to annuli, and k(A) = c(A) for every annulus A. So the pair (k, c) is an
   automorphism of the tree of d12 Lemma 1, and it fixes a vertex.
5. Suppose c = 1 (the tuple itself returns). Then k maps every Gamma-component Y
   to itself. On Y it is trivial or it moves every sheet. If it is nontrivial, Y
   has at most two annuli. With one annulus, k has order 2 on Y and fixes one
   regular point of Y, or order 3 and fixes one zero. With two annuli, k fixes no
   a-point and no b-point of Y.

Proof.

- Part 2. The tuple after m twists is conjugate to t by some sigma. Then sigma
  fixes g_c and g_d, so sigma lies in C_T. And sigma o h^-m fixes g_a and g_b, so
  it lies in C_Gamma. So h^-m lies in C_T C_Gamma. The converse reads the same
  lines backwards.
- Part 3. The label of the a-point through s sits on sheet h^-m(s) after the
  twists. The conjugation c carries that sheet to c(h^-m(s)) = k(s). Two choices
  of c differ by an element that centralises both groups, hence G.
- Part 4. k commutes with h because h is in Gamma. So k maps cycles of h to
  cycles of h. The same holds for c. For s in an annulus A, k(s) = c(h^-m(s)) and
  h^-m(s) is in A. So k(A) meets c(A), and k(A) = c(A). Incidence is preserved.
  An automorphism of a finite tree fixes a vertex or an edge. This one preserves
  the two colours of vertices, so a fixed edge has two fixed ends.
- Part 5. k = h^-m is a power of h, so it fixes every annulus and every
  Gamma-component Y. On Y it commutes with the transitive group Gamma, so it is a
  deck map of the three-point cover Y. Deck maps act freely on sheets. By d12
  Lemma 1 the capped component is a sphere. A nontrivial deck map of finite order
  on a sphere is a rotation with exactly two fixed points. It fixes the centre of
  every capped annulus. So Y has at most two annuli. A fixed point other than a
  centre is a ramified a-point or b-point, and the order of k divides its cycle
  length.

For x = c and x = d, apply the lemma to the arc-adapted tuple, as in d12 Lemma T.

Check (`twistcheck.py`, arc a-b, every state of every saved orbit, n = 4 to 8):

| n | twist steps | returns | literal returns | k trivial on regular a-points | nontrivial components, 1 annulus | 2 annuli |
| --- | --- | --- | --- | --- | --- | --- |
| 4 | 35 | 21 | 19 | 10 | 14 | 3 |
| 5 | 519 | 153 | 130 | 137 | 28 | 4 |
| 6 | 4,114 | 1,128 | 952 | 897 | 306 | 22 |
| 7 | 47,797 | 9,407 | 7,921 | 8,633 | 1,940 | 84 |
| 8 | 532,691 | 84,987 | 74,343 | 79,659 | 12,864 | 507 |

The script asserts parts 1, 2 (both directions, by brute force over C_T), 3, and
5 at every step. No assertion fails. Part 4 follows from parts 2 and 3 and has no
separate check.

What H1 gives: one state decides every cusp element at that state. A literal
twist element is a product of involutions, 3-cycles, and free rotations on the
components with at most two annuli. The pinch of d12 Corollary T1 is the
one-annulus case of order 2 about the mirror.

### 1.4 Proposition H2 (M_t, the cusp group, and the Hurwitz curve) `[PROVED]` `[CHECKED n <= 10]`

Let O be the plain orbit and N = |O|. The pure mapping class group of the sphere
with four marked points is free on T_b and T_d. The classes T_b, T_c, and T_d
are its three peripheral classes. `[CITED, from memory: Farb and Margalit, A
Primer on Mapping Class Groups, Section 4.2]` Let X be the cover of the thrice-punctured sphere with
fibre O. Its punctures are the cycles of T_b, T_c, and T_d on O. Its closure has
genus g with 2g = 2 + N - (number of cusps). Let D be the image of the deck group
in M_t.

**Statement.** Nbar D is normal in M_t, and M_t / (Nbar D) is a quotient of the
fundamental group of the closed surface of genus g. So 2g elements generate M_t
modulo Nbar D.

Proof. The stabiliser S of t is the fundamental group of the punctured curve X.
The label action is a surjective homomorphism rho from S to M_t / D. The kernel K
of the map from S to the fundamental group of the closed curve is the normal
closure of the peripheral elements. Those are the conjugates of the loops T_x^w
based at the states u. The image of a normal closure under a surjection is the
normal closure of the image. So rho(K) = Nbar D / D, and rho induces a surjection
from S / K to M_t / (Nbar D).

**Corollary H3 `[PROVED]`.** If the Hurwitz curve has genus 0 and the deck group
is trivial, then M_t = Nbar. Lemma H1 then computes generators of M_t from single
states.

Check: `cusp.py` asserts that the genus formula gives an integer in every orbit.
Nbar = M_t in all 509 saved orbits with genus 0 and no deck map (207 of them in
AN). Only 207 of the 2,885 AN orbits have genus 0, so H3 covers 7% of the data.

**Corollary H3' `[PROVED]`.** In a cusp-trivial orbit with no deck map, M_t is a
quotient of a surface group of genus g. All of M_t comes from the handles of X.

### 1.5 Elementary reductions `[PROVED]`

- q = 2: H is vacuous. q = 3: H is equivalent to transitivity of M_t, because a
  pair of three points is the complement of a point.
- If the transpositions in M_t connect all q points, then M_t = S_q. Proof: the
  transpositions along a spanning tree generate S_q. No Jordan theorem is needed.
- If Nbar is 2-homogeneous, H holds for that orbit. This covers 1,637 of the 1,643
  AN orbits with q >= 3, as a computed fact and not as a theorem.
- d12 Corollary T2 `[PROVED elsewhere, reviewed]`: M_t primitive and one T1 state
  give M_t = S_q.

### 1.6 Extra hypotheses, and what rooms satisfy

I found no proof of H under any of the sample hypotheses of the brief.

- **Some corner has exactly one 2-cycle.** The cusp-trivial orbit at n = 7 has
  exactly one 2-cycle at c and at d. So this hypothesis doesn't supply a cusp
  element.
- **g_a has at least k fixed points.** The cusp-trivial orbits named in 1.1 and
  1.2 have one fixed point of g_a. I didn't test the hypothesis for k >= 2.
- **q <= bound.** H is vacuous at q = 2 and equals transitivity at q = 3. The
  rooms of the assembled theorem have q >= 4.
- **A one-cylinder or two-cylinder state exists.** Not tested. H1 part 5 shows
  what a closed leaf gives: a free rotation of its a-points, under a divisibility
  condition on the other annuli.

For a room state under D0 `[PROVED given D0]`:

- T1 never holds for a mirror at S + e, where S is an interior a-point and e is a
  unit axis vector. The outer sheets have their x-corner at S - e, which lies in
  at least two cells, so g_x doesn't fix them.
- A wall of length 4 between two convex corners of class x, with flat points of
  classes a, x, a, is the T1 configuration. It gives a transposition in M_t when
  no other cycle of h_x has length divisible by 4.
- Let S be an interior a-point with S + e and S - e both flat. The four cells at
  S form a regular leaf with two annuli of length 2. It gives the transposition
  (S+ S-) when every other cycle of h_x has odd length.

The side conditions on h_x are arithmetic conditions on the whole room. No
hypothesis that every room satisfies gives H.

### 1.7 Where the proof stops

By H2, M_t is generated by the cusp group, the deck maps, and the images of 2g
handle loops. H1 computes the cusp group. Nothing computes the handle loops from
local data. Six cusp-trivial AN orbits have q >= 3. There, all of M_t = S_q
comes from the handles of a curve of genus 7 or 10.

So a proof of H must contain a global connectedness argument. Take the cover of
the Hurwitz curve whose fibre is the set of pairs of regular a-points. H says
that this cover is connected. d12 found no published theorem that gives it.

H also depends on the group, and not only on local structure. It fails for the
primitive groups of order 336, 1,344, and 60, which have the same cycle lengths.

## Task 2: one LIT pair (Lemma E)

**Lemma E `[CONJECTURAL]` `[CHECKED n <= 10]`.** Under the PRIM hypotheses, every
orbit with q >= 2 has a LIT pair.

### 2.1 Reformulation `[PROVED]`

Some pair of an orbit is LIT if and only if some state of the orbit has a link.
Proof: the first mirror of any chain is a link, and a link is a chain.

So E has no hidden extra hypothesis. It says that some state has a 2-cycle of some
g_x between two distinct regular a-points.

### 2.2 Data

Source: `cusp.py` (links per state), `post.py`, `cyl_e.py`.

| Statement | AN, q = 2 (1,242) | AN, q >= 3 (1,643) | PRIM without A_n (47) |
| --- | --- | --- | --- |
| Some state has a link (E) | 1,242 | 1,643 | 47 |
| The base state has a link | 815 | 1,489 | 42 |
| Some pair has a cylinder witness (d12 Lemma C) | 942 | 1,454 | 26 |

- Every state has a link in 658 of the 2,885 AN orbits. The smallest share of
  states with a link in one AN orbit is 0.087 (n = 9). The mean share is about 0.7.
- Each PRIM hypothesis is needed for E `[CHECKED n <= 10]`:
  - Primitive, a 2-cycle, and an identity corner: 24 of 39 orbits have no link.
    First: n = 7, [3,2,2], [1^7], [3,2,2], [3,2,2], G = A_7.
  - Imprimitive, a 2-cycle, and no identity corner: 36 of 798 orbits have no link.
    First: n = 8, [2,2,1^4], [2^4], [2^4], [3,3,1,1], |G| = 96.
  - No 2-cycle at b, c, d: no link can exist.

### 2.3 The case q = 2

At q = 2 the orbit has one pair, H is vacuous, and PRIM is the statement E.

- `[CHECKED n <= 10]` E holds in all 1,242 AN orbits and all 1,252 PRIM orbits
  with q = 2.
- `[CONJECTURAL]` No proof for abstract covers. The cusp group doesn't help: 66 of
  the 1,242 AN orbits are cusp-trivial.
- Rooms: q = 2 means one interior a-point and no flat a-point, or two flat
  a-points. The assembled theorem needs two interior a-points, so it has q >= 4.

### 2.4 Lemma E1 (counting) `[PROVED]`

In one state, let k_x be the number of 2-cycles of g_x. Let d_x be the number of
2-cycles that g_x shares with g_a. Let p_a and z_a be the numbers of fixed points
and 3-cycles of g_a. If k_x - d_x > p_a + 3 z_a, the state has a link at x.

Proof. Take a 2-cycle of g_x that is not shared with g_a and is not a link. One
of its sheets lies in a pole or a zero of g_a. Those sheets number p_a + 3 z_a,
and distinct 2-cycles of g_x are disjoint.

The lemma has no version in cycle types alone, because d_x depends on the state.

### 2.5 Rooms `[PROVED given D0]`

P is a strictly simple orthogonal lattice polygon with n cells and r reflex
corners. A lattice point of P is convex, flat, reflex, or interior. The first and
third are vertices. Class a is the class of points with both coordinates even.

**Lemma L1 (rays).** Let S be an interior a-point and e a unit axis vector. The
room state has a link at S + e, with two exceptions. Exception 1: S + e is
reflex. Exception 2: S + e is interior and S + 2e is reflex.

Proof. The two cells at S on the side of e contain S + e, so S + e isn't convex.

- S + e flat: g_x swaps those two cells. They are adjacent at S, and g_a pairs
  opposite cells at S. So they lie in the two different 2-cycles of S.
- S + e interior and S + 2e not reflex: S + 2e lies in two cells, so it is flat or
  interior. Apply Lemma L2 to the segment from S to S + 2e.

**Corollary L1' (few reflex corners).** If P has two distinct interior a-points
and r <= 5, the room state has a link. So E holds for the orbit of P.

Proof. Suppose no link exists. By L1, each interior a-point S needs a reflex
corner at S + e or S + 2e for each of the four e. Let C be a reflex corner, with
edges in directions e_1 and e_2. Only C - e_1 and C - e_2 can be interior.

- C = S + e forces S = C - e_1 or C - e_2. At most one of them has class a.
- C = S + 2e with S + e interior forces S = C - 2 e_1 or C - 2 e_2.

So a corner serves one point twice in no case, and two points only when it has
class a. Two points S and T share a corner only if T - S = 2(e - e') with e, e'
perpendicular. That equation has two solutions. So S and T need at least
4 + 4 - 2 = 6 reflex corners.

**Lemma L2 (segments).** Let A_1 and A_2 = A_1 + 2e be a-points and F = A_1 + e.
Suppose the closed segment from A_1 to A_2 lies in P and none of A_1, F, A_2 is a
vertex. Then g_x has a link at F, where x is the class of F.

Proof. F is flat or interior.

- F interior. g_x swaps a cell c with corners F and A_1 with the opposite cell c'
  at F, which has corners F and A_2. A_1 is the only a-corner of c, and A_1 is
  flat or interior. So c lies in a 2-cycle of g_a at A_1. In the same way c' lies
  in a 2-cycle at A_2. The two 2-cycles differ.
- F flat. The segment passes through F on both sides, so the wall at F runs along
  e. F isn't a vertex, so the wall edge reaches A_1 and A_2. They aren't
  vertices, so they are flat points of that edge. g_x swaps the two cells at F.
  One lies in the 2-cycle of A_1 and the other in the 2-cycle of A_2.

**Lemma L3 (large rooms).** If n > 52 r + 68, the room state has a link. So E
holds for the orbit of P. For r = 8 the bound is n > 484.

Proof. Call a segment as in L2, with or without vertices, a candidate.

1. Cut P along the horizontal chords through the reflex corners. The pieces are
   at most r + 1 lattice rectangles of sizes w_i by h_i, with total area n. The
   vertical sides of each piece lie on walls.
2. An even horizontal domino is two cells side by side whose left edge has even
   x. One of its two long sides lies on a line of even y. That side is a
   candidate. A candidate is a long side of at most two dominoes. Vertical
   dominoes behave the same way.
3. A row of w cells has at least floor((w - 1) / 2) even horizontal dominoes.
   Put f(w, h) = h floor((w - 1) / 2) + w floor((h - 1) / 2). The piece i has at
   least f(w_i, h_i) even dominoes.
4. f(w, h) >= (w h - 4) / 4. For w, h >= 2, f >= w h - w - h, and the claim is
   (3w - 4)(3h - 4) >= 4. For w = 1, f = floor((h - 1) / 2) >= (h - 4) / 4.
5. So P has at least (n - 4(r + 1)) / 8 = n/8 - (r + 1)/2 candidates.
6. A candidate with a vertex contains it as an endpoint or as the midpoint. A
   convex a-vertex is an endpoint of at most 2 candidates, a reflex a-vertex of
   at most 4. A convex vertex is never a midpoint, and a reflex vertex is the
   midpoint of at most 1. So at most 2(r + 4) + 4r = 6r + 8 candidates have a
   vertex.
7. If n/8 - (r + 1)/2 > 6r + 8, a candidate without a vertex exists. Apply L2.

The constant is crude. Step 6 assumes that every vertex has class a.

Check (`roomlink.py`, 10 fixed polygons in the 4 parity positions, not a search):
281 instances of L2 and 428 instances of L1 pass. The two counts of L3 hold in
all 40 cases.

**What stays open for rooms.** E for 6 <= r <= 8 and n <= 52 r + 68.
`[CONJECTURAL]` L1 can't drop its exceptions. The pinwheel octomino (r = 4, one
interior point, q = 2) has no link in its room state.

### 2.6 Side conditions of d12 Lemma C and Proposition N

- **Lemma C `[PROVED elsewhere, reviewed]`.** It gives E exactly when some state
  has a maximal cylinder with one of two properties. CylA: a regular leaf inside
  the cylinder carries a regular a-point, and another regular a-point lies in the
  closed cylinder. CylB: regular a-points lie on both boundary components. Two
  marks on one boundary component don't qualify. The condition fails first at
  n = 4: [2,2], [2,1,1], [2,1,1], [3,1], plain 3, G = S_4, q = 2. It fails first
  with q >= 3 at n = 6: [2,2,2], [2,1^4], [3,1,1,1], [3,3], plain 2, G = S_6. It
  holds in 2,396 of the 2,885 AN orbits (table in 2.2).
- **A regular leaf with at least two a-points gives a link with no use of D0.**
  `[PROVED]` Its a-points and x-points alternate, so a mirror joins two a-points.
- **Proposition N `[PROVED elsewhere, reviewed]`.** Its side condition is: some
  shortest path between a nearest pair of regular a-points contains no zero. I
  didn't test it. The test needs flat distances, and no saved script computes
  them. Its conclusion is a link, so by 2.1 it can't hold in more orbits than E.

## Task 3: the companion reduction

### 3.1 Sources

| Source | Statement used | Status |
| --- | --- | --- |
| Burness and Guralnick, "Fixed point ratios for finite primitive groups and applications", Adv. Math. 411 (2022) 108778, arXiv 2112.03967v2, Corollary 2 | For x of prime order p in a primitive group, fpr(x) <= 1/sqrt(p + 1), or G lies in S_m wr S_k and contains (A_m)^k, with S_m on l-subsets and the product action | `[CITED, verified]`, depends on the classification of finite simple groups |
| Same paper, Remark 2 | In that family you may assume 1 <= l < m/2 | `[CITED, verified]` |
| Same paper, Theorem 1 | fpr(x) <= 1/(p + 1) outside a longer list of exceptions | `[CITED, verified]`, not used in the proof |
| Maróti, survey "Minimal degree, base size, order: selected topics on primitive permutation groups", Theorem 3.1, quoting Babai, Ann. of Math. 113 (1981) 553-568, Theorem 6.14 | A primitive group without A_n has minimal degree > (sqrt(n) - 1)/2 | `[CITED, verified]` in the survey only |
| Same survey, quoting Liebeck and Saxl, Proc. London Math. Soc. (3) 63 (1991) 266-314 | Minimal degree >= n/3 outside the family of Corollary 2 | `[CITED, verified]` in the survey only |
| Same survey, quoting Guralnick and Magaard, J. Algebra 207 (1998) 127-145 | Classification of minimal degree <= n/2 | description only, not used |
| Same survey, Section 3 | A primitive group with a transposition or a 3-cycle is S_n or A_n | `[CITED, verified]` in the survey |
| Jordan (1871); Wielandt, Finite Permutation Groups, Theorems 13.3 and 13.9 | The same statement, and prime cycles | `[CITED, from memory]` |
| Bochert (1892); Wielandt, Theorem 15.1 | Minimal degree at least n/4 - 1 for 2-transitive groups | `[CITED, from memory]`, not used |
| Manning, Trans. Amer. Math. Soc. 35 (1933) | Bounds for elements of order 3 with few cycles | `[CITED, from memory]`, not used |

The two downloaded files were read as text only.

### 3.2 Theorem G `[PROVED from Corollary 2]`

Let G be a primitive group of degree n.

- (a) Suppose G has an element of order 3 with exactly z >= 1 cycles of length 3.
  Then G contains A_n or **n <= max(6z, z^2)**.
- (b) Suppose G has an involution with exactly kappa >= 1 cycles of length 2.
  Then G contains A_n or n <= max((3 + sqrt 3) kappa, kappa^2).

Proof of (a). The element x has fpr(x) = 1 - 3z/n.

1. If fpr(x) <= 1/2, then n <= 6z.
2. Otherwise G is in the family, with n = C(m, l)^k and 1 <= l < m/2. Write Gam
   for the set of l-subsets and x = (x_1, ..., x_k) pi.
3. If pi != 1, pi has a 3-cycle on the coordinates. A fixed point is determined
   by its other k - 2 coordinates. So fpr(x) <= 1/|Gam|^2 <= 1/4 and n <= 4z.
4. If pi = 1, some x_i is a nontrivial product of 3-cycles of S_m. A subset fixed
   by x_i is fixed by each of its 3-cycles. One 3-cycle moves the l-subsets that
   meet its support in 1 or 2 points. Their number is
   3 C(m-3, l-1) + 3 C(m-3, l-2) = 3 C(m-2, l-1). The element x moves every point
   whose coordinate i is moved by x_i. So 3z >= C(m, l)^(k-1) 3 C(m-2, l-1), and
   **z >= C(m, l)^(k-1) C(m-2, l-1)**.
5. l = 1 and k = 1: G contains A_n in its natural action.
6. l = 1 and k >= 2: z >= m^(k-1), so n = m^k <= z^(k/(k-1)) <= z^2.
7. l = 2 and k = 1: z >= m - 2, so n <= (z + 1)(z + 2)/2. This is at most 6z for
   z <= 8 and at most z^2 for z >= 4.
8. l >= 3 and k = 1: n = C(m-2, l-1) m(m-1) / (l(m-l)). Here m >= 7,
   l(m-l) >= 3(m-3), and C(m-2, l-1) >= (m-2)(m-3)/2. The inequality
   2m(m-1) <= 3(m-2)(m-3)^2 holds for m >= 7. So n <= C(m-2, l-1)^2 <= z^2.
9. l >= 2 and k >= 2: z^2 >= C(m, l)^(2k-2) >= C(m, l)^k = n.

Proof of (b). The same steps with fpr(x) = 1 - 2 kappa/n and the bound
1/sqrt 3. Step 1 gives n <= (3 + sqrt 3) kappa. Step 3 gives n <= 4 kappa. In
step 4 one transposition moves 2 C(m-2, l-1) subsets, so
kappa >= C(m, l)^(k-1) C(m-2, l-1). Steps 5 to 9 are unchanged, and in step 7
(kappa + 1)(kappa + 2)/2 <= (3 + sqrt 3) kappa for kappa <= 6.

Sharpness `[PROVED]`. S_8 wr S_2 on 64 points is primitive and doesn't contain
A_64. A 3-cycle in one factor moves 24 points, so z = 8 and n = 64 = z^2. Group
theory alone can't lower the bound at z = 8.

Check `[CHECKED n <= 10]`: the 49 saved orbits with primitive G, no A_n, and a
3-cycle have n = 6 to 10 and z = 2 or 3. All satisfy n <= max(6z, z^2).

### 3.3 The bound for rooms `[PROVED given D0]`

Under D0 the reflex corners of class x are the 3-cycles of g_x, and g_x^2 has
order 3 with the same 3-cycles. Let z_x be their number, for all four classes.

**Lemma R0.** If G is primitive and P has an interior lattice point, then r >= 1.

Proof. Let P be a rectangle with p columns and q rows. Take a cell in column i
and its corner of class x, with first coordinate u. The rotation about that
corner sends the cell to column 2u - 1 - i, or keeps the column at a wall. The
number u depends only on i and x. So the columns form a block system.
An interior point needs p, q >= 2, so the blocks are proper.

**Theorem G for rooms.** Let G be primitive, with an interior point in P. Let z
be the least positive z_x and **N_0 = max(6z, z^2)**. If n > N_0, G contains A_n.

| Condition | z | N_0 |
| --- | --- | --- |
| r <= 8 (W <= 21) | <= 8 | 64 |
| general r | <= r | max(6r, r^2) |
| reflex corners in at least two classes, r <= 8 | <= 4 | 24 |
| reflex corners in at least three classes, r <= 8 | <= 2 | 12 |
| some class has exactly one reflex corner | 1 | none: G contains A_n for every n |

The last row is Jordan's theorem on 3-cycles. Values of max(6z, z^2) for
z = 1 to 8: 6, 12, 18, 24, 30, 36, 49, 64. Suppose G is primitive without A_n
and n > 49. Then z = 8 and n <= 64, and one class holds all 8 reflex corners.

**The 2-cycle route.** g_x^3 is an involution with kappa_x cycles, where kappa_x
is the number of 2-cycles of g_x. If kappa_x = 1, G = S_n. In general Theorem G(b)
needs n > max(4.74 kappa_x, kappa_x^2). In a room, kappa_x counts the flat points
plus twice the interior points of class x. That grows with the area, so this
route applies only to rooms with very few transparent points in some class.

**Other routes.**

- Liebeck and Saxl: the same proof gives n <= max(9z, z^2), so 72 for z = 8.
- Babai, with no classification: 3z > (sqrt n - 1)/2, so n < (6z + 1)^2 = 2,401
  for z = 8.
- Burness and Guralnick, Theorem 1, gives n <= 4z outside a list of exceptions.
  It doesn't lower 64, because the product family is among the exceptions.

### 3.4 What remains

- **Primitive G without A_n, n <= N_0.** The census has such groups of order 10,
  60, 14, 168, 336, 1,344, 216, 432, 1,512, 60, and 720 at n = 5 to 10. H fails
  for three of them. I know no room with such a group. `pinwheel.py` tests one
  guess, the pinwheel octomino. The guess is wrong: |G| = 96 and G is imprimitive.
- **Imprimitive G.** See "Task 4".
- The genus-0 condition and the cycle lengths of all four generators are unused
  in Theorem G. They are the natural input for a lower N_0.

## Task 4: imprimitive G

Let Pi be a block system, N = Q / Pi, and phi the factor map. This section uses
d10 Fact L, the live points, and the live graph K_N. It never assumes that N or a
fold target is a planar polygon. N is any genus-0 cover of B.

### 4.1 Projection, lifting, and the induction step

Fix a state and a corner x. The live graph of N has the live a-points and
x-points of N as vertices and the sheets of N between them as edges. A regular
point has degree 2 and a live pole has degree 1. So every component is a path or
a cycle.

**I1 (projection) `[PROVED elsewhere, reviewed]`** (d10 Lemma 1). A chain of Q
projects to a walk in the live graph of N.

**I1' (same fibre) `[PROVED]`.** Suppose a chain joins two regular a-points over
one point u of N. Then the live component of u is a cycle or contains a live
pole.

Proof. The chain doesn't backtrack in Q. Its image backtracks only at a vertex
where two edges of Q have one image. That vertex has local degree 2, so it is a
live pole. With no backtracking, a closed walk in a path or a cycle is a circuit
of the cycle.

**I2 (lifting) `[PROVED]`.** Let u != u' be a-points of N in one live component.
Suppose at least one of them is regular in N. Then some regular a-points sigma
over u and tau over u' are joined by a chain in that state.

Proof. Say u is regular. The inner vertices of the path from u to u' have degree
2, so they are regular in N. By Fact L every point over a regular point is
regular with local degree 1. Choose a regular tau over u', which exists because
u' is live. Lift the path backwards from tau. The lift is unique and ends at a
point sigma over u, which is regular.

I2 can fail when both points are live poles. The lift from a regular point over
u can end at a pole or a zero over u'. The six non-transitive relations of order
48 at n = 8 are of this kind (4.3).

**Definitions.** M_Pi is the subgroup of M_t that preserves the fibres of phi on
the regular a-points. It induces a group on the a-points of N. The image of a
pair is an unordered pair {u, u'} or a single point. **FH(Pi)** (fibre
homogeneity): two pairs lie in one M_Pi-orbit if and only if their images lie in
one orbit of the induced group.

**I3 (induction step) `[PROVED]`.** Assume FH(Pi). Let (sigma, tau) be a pair
with images u != u', at least one of them regular in N. Then (sigma, tau) is
x-lit if and only if u and u' lie in one live component of N at x in some state.

Proof. "Only if" is I1. For "if", I2 gives an x-lit pair over (u, u'). FH puts
all pairs over (u, u') in one M_Pi-orbit, and x-lit is invariant under M_t.

So an induction on factors needs three inputs: FH(Pi), a verdict for live
connection in N, and a verdict for the pairs I3 excludes (same fibre, or two live
poles).

### 4.2 Test of FH on the census `[CHECKED n <= 10]`

Source: `ind.py`, for every imprimitive orbit and every maximal proper factor
(minimal blocks). An orbit is **rigid** when Q or one of its factors has identity
monodromy at b, c, or d.

| n | incidences | not rigid: FH holds | rigid: FH holds | rigid: FH fails |
| --- | --- | --- | --- | --- |
| 4 | 12 | 0 of 0 | 12 | 0 |
| 6 | 78 | 3 of 3 | 72 | 3 |
| 8 | 196 | 58 of 58 | 111 | 27 |
| 9 | 161 | 41 of 41 | 114 | 6 |
| 10 | 503 | 260 of 260 | 210 | 33 |

- FH holds in all 362 incidences that are not rigid, and fails in 69 of 588 rigid
  ones.
- Orbits where FH holds for every maximal factor: 6 of 6, 51 of 54, 133 of 154,
  146 of 149, and 446 of 473 for n = 4, 6, 8, 9, 10.
- The LIT verdict is constant on the classes that N predicts, except in 6 rigid
  incidences at n = 9 with |G| = 36.
- Block sizes in this data are at most 5.

**Conjecture FH\* `[CONJECTURAL]` `[CHECKED n <= 10]`.** Suppose neither Q nor
any factor of Q has identity monodromy at b, c, or d. Then FH(Pi) holds for every
maximal proper factor.

FH\* is the precise lemma that makes the induction work. For N = B it is Lemma H
without the group hypothesis, so it is at least as hard as H. The data has no
case where the group of Q over N is large and FH\* fails, but the range is small.

### 4.3 Double covers and the failure of x-lit transitivity

**Lemma D2 (double covers) `[PROVED]` `[CHECKED n <= 10]`.** Let the blocks have
size 2. Fix a state and a corner x. Let u be a regular a-point of N with fibre
{s_1, s_2}, and let C be the live component of u.

- If C is a path, s_1 and s_2 are joined by a chain if and only if C contains a
  live pole.
- If C is a cycle, they are joined if and only if the lift of C isn't closed.
  Call such a cycle **odd**.

Proof. For a double cover, every point over a live point is regular. A sheet of
Q over an edge of C joins two regular points. A sheet of Q over any other sheet
of N at C has a non-regular end. So the preimage of C is a union of chain
components. It is a double cover of C, branched exactly over the live poles. An
unbranched double cover of a path is two copies. Now let C contain a live pole
p. Lift the path from u to p, once from s_1 and once from s_2. Both lifts end at
the one point over p. An unbranched double cover of a cycle is connected exactly
when the lift of the cycle isn't closed.

Check (`double.py`, every state, every size-2 block system, every corner):

| n | path cases | failures | cycle cases | lift not closed |
| --- | --- | --- | --- | --- |
| 4 | 24 | 0 | 12 | 9 |
| 6 | 270 | 0 | 18 | 12 |
| 8 | 2,169 | 0 | 261 | 159 |
| 10 | 21,219 | 0 | 1,677 | 936 |

**Corollary D3 `[PROVED]`.** Take a same-fibre pair over a regular point u. It
is x-lit if and only if, in some state, the live component of u has a live pole
or is an odd cycle. The saved verdicts agree for every orbit with one size-2
block system. That is 1,269 corner relations: 9, 72, 270, and 918 for
n = 4, 6, 8, 10.

**Account of the failure at n = 10.** x-lit is not transitive in 18 corner
relations. All have |G| = 1,920 (12 relations) or 3,840 (6), one block system,
blocks of size 2, and N of degree 5 with a-type [2,2,1].

- N has two regular a-points u_1 and u_2. Their fibres are {s_1, s_2} and
  {s_3, s_4}.
- In one state, a live path from u_1 to u_2 without a live pole lifts to two
  chains. They define a bijection between the fibres. `[PROVED]` by D2.
- Different states give both bijections. So all four cross pairs are x-lit.
  `[CHECKED]`
- No state has a live pole or an odd cycle at that corner. By D3 the two
  same-fibre pairs are not x-lit. `[CHECKED]`
- So s_1 ~ s_3 ~ s_2 while s_1 and s_2 are not x-lit.

The cause is the definition: x-lit is a union over states of equivalence
relations. On a double cover each state transports one fibre to the other, and
two transports compose to a same-fibre relation that no single state realises.
In 12 of the 18 relations N has identity monodromy at one corner. In 6 it has
none, so rigidity isn't the cause.

At n = 8 the six non-transitive relations with a non-pillowcase double factor
have |G| = 48. The missing pair lies over two different live poles of N, which is
the excluded case of I2. Eighteen more relations at n = 8 have |G| = 16 and three
size-2 block systems.

For blocks of size 2, the lemmas D2, D3, and I2 give the x-lit verdict from the
live graphs of N over the orbit. If N has identity monodromy at a corner, the
live graph at that corner doesn't depend on the state, as in d12.

## Task 5: the conditional theorem for rooms

### 5.1 Statement

**Theorem R `[conditional on H and D0]`.** Let P be a strictly simple orthogonal
lattice polygon with n cells and W <= 21 walls. Then W = 2r + 4 with r <= 8. Let
S != T be interior lattice points of one parity class a. Let G be the monodromy
group of the double DP over the pillowcase B, and suppose G is primitive. Let z
be the least positive number of reflex corners in one parity class, and
N_0 = max(6z, z^2) <= 64. Suppose n > N_0. Assume:

- **(H)** Lemma H for the pure-braid orbit of the tuple of P.
- **(E)** Lemma E for that orbit. You need it only if 6 <= r <= 8 and
  n <= 52 r + 68.

Then every pair of lifts of S and T is LIT, and a billiard path joins S and T.

With n > 484 in place of n > N_0, the theorem needs H and D0 and not (E).

### 5.2 Proof from the lemmas

1. D0 gives a tuple of genus 0 with cycle lengths at most 3. Sheets are cells.
2. Lemma R0: r >= 1, so z is defined.
3. Theorem G for rooms: G contains A_n.
4. The PRIM hypotheses hold. G is primitive. d10 Proposition R2 excludes an
   identity corner, because P has two interior points. Lemma R6 gives a 2-cycle.
5. q >= 4, because S and T each have two lifts.
6. E holds by L1' (r <= 5), by L3 (n > 52 r + 68), or by assumption.
7. H and d12 Proposition R: every pair of the orbit is LIT.
8. D0: a chain between lifts of S and T unfolds to a billiard path.

**Lemma R6 (a transparent point exists) `[PROVED given D0]`.** Let P have two
distinct interior a-points S and T, and r <= 8. Then some class other than a has
a flat or interior point.

Proof. Suppose not. Each of the four points S +- e lies in two cells of the star
of S, so it is reflex. The same holds for T. Two of these points coincide only as
S + e = T - e. Such a point lies in four cells, so it is interior. So the 8
points are distinct, and r = 8. One of the two cells beyond S + e_1 exists, so a
diagonal neighbour of S lies in at least two cells. It isn't convex, and its
class isn't a, so it isn't flat or interior.
So it is a ninth reflex corner.

**Remark R0' (normalization) `[PROVED given D0]`.** Suppose g >= 2 divides all
horizontal edge lengths, and n > g. Then DP factors through the pillowcase of the
g by 1 rectangle, and G is imprimitive. So a primitive G implies gcd 1 in each
direction. Theorem R doesn't need "normalized" as a hypothesis.

Proof. After a translation every vertical wall lies on a line x in gZ. Fold the
plane along the lines x in gZ and y in Z. This maps DP onto the double of the g
by 1 rectangle, and the map to B factors through it. That double has degree g
over B, and 1 < g < n.

### 5.3 Dependencies and their status

| Dependency | Used in step | Status |
| --- | --- | --- |
| Dictionary D0 (rooms to tuples, chains to billiard paths) | 1, 4, 6, 8 | standing model, **checked by no one** |
| Lemma R0 (primitive implies r >= 1) | 2 | `[PROVED given D0]` here |
| Burness and Guralnick, Corollary 2 | 3 | `[CITED, verified]`, uses the classification |
| Theorem G | 3 | `[PROVED]` here from the citation |
| d10 Proposition R2 (no identity corner) | 4 | `[PROVED elsewhere, reviewed]` |
| Lemma R6 (a 2-cycle exists) | 4 | `[PROVED given D0]` here |
| Lemmas L1, L1', L2, L3 (E for rooms) | 6 | `[PROVED given D0]` here, checked on 10 fixed polygons |
| Lemma E for 6 <= r <= 8 and n <= 52 r + 68 | 6 | `[CONJECTURAL]`, `[CHECKED n <= 10]` for abstract covers |
| **Lemma H** | 7 | `[CONJECTURAL]`, `[CHECKED n <= 10]`: 1,643 orbits with q >= 3, 655 with q >= 4 |
| d12 Proposition R with the reviewer's definition of M_t | 7 | `[PROVED elsewhere, reviewed]` |

H1, H2, H3, and the lemmas of "Task 4" are not used in Theorem R.

### 5.4 Cases outside the theorem

- n <= N_0. At most 64 cells, and at most 24 if the reflex corners lie in two
  classes.
- Imprimitive G. This includes every room that isn't normalized, and every room
  with a proper factor. The known dark rooms are here.
- Primitive G without A_n. Theorem G confines it to n <= N_0.
- W >= 22. Theorem G still applies with N_0 = max(6z, z^2), and L3 with
  n > 52 r + 68. Lemma R6 and L1' need r <= 8 and r <= 5.
- Pairs with a wall point, pairs of different classes, and points off the lattice.

### 5.5 The single weakest link

**Lemma H.** Three reasons:

1. The evidence is 655 orbits with q >= 4, all with n <= 10 and q <= 5. Theorem R
   uses H at every n > N_0, with no upper bound on n. N_0 runs from 6 (z = 1) to
   64 (z = 8), so almost all of that range has no evidence.
2. The only proof plan on record fails at its first step (1.2).
3. H is false for primitive groups without A_n that have the same local data. A
   proof must use the group, and no tool in this project does.

D0 is the second weakest link, for a different reason. It is unreviewed, and
every room statement rests on it.

## Errors found in earlier lemmas

None. The reviewer confirms d12 Lemmas 1, F, T, C, G, Corollaries T1, T2, and
Proposition N. Two points limit their use and are not errors:

- The "weaker route to H" of d12 can't reach the 72 cusp-trivial AN orbits (1.2).
- d12 states H for "2,885 orbits (8,952 pairs)". 1,242 of the orbits have q = 2,
  where H is vacuous. The real evidence is 1,643 orbits and 7,710 pairs.

One error of my own, corrected: I guessed that the pinwheel octomino has a
primitive group of order 1,344. `pinwheel.py` gives |G| = 96, imprimitive.

## Facts that would falsify these statements

- An AN orbit with q >= 3 where Nbar is neither trivial nor 2-homogeneous
  falsifies the dichotomy of 1.2.
- A return of a twist with h^m outside C_Gamma C_T, or a literal return with a
  nontrivial component of three annuli, falsifies H1.
- A genus-0 orbit with no deck map and Nbar != M_t falsifies H2.
- Take a primitive group without A_n and an element of order 3 with z cycles.
  Degree n > max(6z, z^2) falsifies Theorem G or the cited corollary.
- A room with n > 52 r + 68 and no link in its room state falsifies L3 or D0.
- A non-rigid imprimitive orbit where FH fails for a maximal factor falsifies FH\*.
- A double cover and a state where a path component with no live pole joins a
  fibre falsifies D2.

## Files and commands

Run every command from this folder with `python3 -B`. All scripts read the saved
orbit representatives in `../d12-lit-side/mine_nN.json` and enumerate nothing new.

| File | Purpose | Command |
| --- | --- | --- |
| `cusp.py` | M_t, cusp elements, links per state, Hurwitz genus | `cusp.py N 3` |
| `cusp_nN.json` | Output of `cusp.py`, n = 4 to 10 (n = 10: 649 s) | |
| `post.py` | Normal closure Nbar, claims C1 to C12 and E1 to E3, first failures (3 s) | `post.py 4 5 6 7 8 9 10` |
| `post_q3.py` | The same counts split by q = 2 and q >= 3. Run `post.py` first. | `post_q3.py` |
| `check_cusp_trivial.py` | Separate check of cusp-trivial orbits | `check_cusp_trivial.py` |
| `twistcheck.py` | Lemma H1 on every state, arc a-b (n = 8: 34 s) | `twistcheck.py 4 5 6 7 8` |
| `cyl_e.py` | Orbits where a link or a cylinder gives one LIT pair | `cyl_e.py 4 5 6 7 8 9 10` |
| `roomlink.py` | Lemmas L1, L2, L3 on 10 fixed polygons | `roomlink.py` |
| `ind.py` | FH for every factor of every imprimitive orbit | `ind.py 4 5 6 7 8 9 10` |
| `blocks2.py` | x-lit against the fibre map for size-2 blocks | `blocks2.py 8 10` |
| `double.py` | Lemma D2 on every state, Corollary D3 | `double.py 4 6 8 10` |
| `pinwheel.py` | Group of one octomino (a refuted guess) | `pinwheel.py` |
| `post.log`, `ind.log`, `double.log`, `cusp_n9.log`, `cusp_n10.log` | Saved outputs | |

`post.py` writes `post_summary.json` (1.1 MB) and `ind.py` writes
`ind_summary.json` (0.4 MB). Both were deleted to keep the folder small. The
folder holds 3.0 MB, of which the seven `cusp_nN.json` files take 2.9 MB.
