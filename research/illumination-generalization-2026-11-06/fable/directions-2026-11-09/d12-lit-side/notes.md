# Lit side of Conjecture U*: witness data, orbit structure, and proof attempts

Date: 2026-11-09. Scope: degrees n <= 10 are complete for the witness data. The body
of this file states counts for n <= 9. The section "Degree 10" gives the n = 10
counts and says which statements change.

## Result in one paragraph

This direction does not prove U* or PRIM. It proves five lemmas and two
propositions, refutes the shortcuts listed under "Proof attempts", and reduces PRIM
for G containing A_n to two precise open statements. The main structural finding is
negative: **no corner-by-corner proof exists.** At n = 8 a primitive cover
(G = S_8) has a pair that is not b-lit. The pair has no certificate at b, and the
cover has no proper factor. The pair is lit through c and d. A proof of the lit
side must therefore combine corners.

Status tags used in this file:

- `[PROVED]`: the argument is in this file.
- `[CHECKED n <= N]`: exact computation, complete for all census orbits up to degree N.
- `[CITED]`: published source, with the theorem number when it was read in this session.
- `[CONJECTURAL]`: open.

## Conventions

- A state is a tuple t = (g_a, g_b, g_c, g_d) with g_a g_b g_c g_d = 1. Products
  apply the left factor first, as in `d6-hurwitz-census/hurwitz.py`.
- Cycle lengths are 1 (pole), 2 (regular point), and 3 (zero).
- q is the number of 2-cycles of g_a. The data covers every census orbit with q >= 2.
- A pair is *x-lit* when some state of the pure-braid orbit has a chain at corner x
  that joins the two marks. A pair is LIT when it is x-lit for some x in {b, c, d}.
- A *one-mirror witness* is a chain with one 2-cycle of g_x.
- The *arc-adapted pair* for x is (g_a, g_b), (g_a, g_c), or (g_d, g_a). For x = c
  the tuple is first moved to (g_a g_b g_a^-1, g_a, g_c, g_d). Write h_x for the
  product of the arc-adapted pair, and (g_y', g_z') for the two other entries.
- M_t is the group of permutations of the q regular a-points that the stabiliser
  of the plain tuple t induces. The stabiliser is taken in the pure braid group,
  with deck maps included.
- The *PRIM hypotheses*: G is primitive, no corner other than a has identity
  monodromy, and some g_x has a 2-cycle.
- Dictionary D0 (project standing model, d3 and d10, not re-proved here): Q carries
  the flat metric pulled back from the pillowcase. The cone angle of a point is pi
  times its cycle length. A chain in a state is a straight segment in the direction
  of that state's arc a-x, with no pole or zero in its interior.

## Task 1: witness complexity

All counts are `[CHECKED n <= 9]`. Source: `mine.py`, `summarize.py`, `prim.py`.

### Chain length

| n | LIT pairs | DARK pairs | min chain 1 | min chain 2 |
| --- | --- | --- | --- | --- |
| 4 | 9 | 3 | 9 | 0 |
| 5 | 22 | 1 | 22 | 0 |
| 6 | 210 | 6 | 210 | 0 |
| 7 | 345 | 12 | 345 | 0 |
| 8 | 1,522 | 84 | 1,513 | 9 |
| 9 | 2,766 | 175 | 2,763 | 3 |

- One mirror is not always enough. The first failures are at n = 8, with a [2^4]
  and the types [2,2,1^4], [3,3,1,1], [3,3,1,1] or [2,2,1^4], [2^4], [3,3,1,1] at
  the other corners. All 12 failures have G imprimitive (|G| = 192, 48, or 36).
- Under the PRIM hypotheses, every pair has a one-mirror witness: 3, 19, 99, 339,
  958, and 2,325 pairs for n = 4 to 9.
- Under the PRIM hypotheses, take any corner x with a 2-cycle. Every pair is
  one-mirror x-lit there, except 6 pair-corners at n = 8 (2,229 of 2,235). At n = 9
  the count is 5,202 of 5,202. The 6 exceptions are the Face family of Lemma F.

### Distance from a state to a witness state

Distance is the word length in the four generators s0^2, s0^-2, s1^2, s1^-2. For
each LIT pair, take the largest distance from any orbit state to a witness state.

| n | maximum | LIT pairs by that distance |
| --- | --- | --- |
| 4 | 0 | 0: 9 |
| 5 | 2 | 0: 10, 1: 10, 2: 2 |
| 6 | 4 | 0: 90, 1: 64, 2: 44, 3: 5, 4: 7 |
| 7 | 5 | 0: 9, 1: 135, 2: 112, 3: 68, 4: 9, 5: 12 |
| 8 | 5 | 0: 171, 1: 516, 2: 439, 3: 255, 4: 125, 5: 16 |
| 9 | 7 | 0: 123, 1: 506, 2: 678, 3: 798, 4: 512, 5: 105, 6: 38, 7: 6 |

- The distance grows with n (0, 2, 4, 5, 5, 7). A proof by bounded local search
  from an arbitrary state is not supported by the data.
- Witness states are dense. At n = 9, 46.7% of the (state, LIT pair) incidences are
  witnesses (5,888,001 of 12,607,704), and 78% are within distance 1.
- An example with distance 6: class [2,2,2,1,1,1], [3,3,1,1,1], [3,3,1,1,1],
  [3,3,2,1], marked orbit 7,488 states, orbit depth 12.

### Arcs

LIT pairs at n = 9 by the set of corners where they are x-lit: one corner, 193 for
each of b, c, d; two corners, 390 for each choice; all three corners, 1,017. No arc
is special. No pair is x-lit while a certificate holds at x (0 cases, n <= 9), which
agrees with Theorem U corner by corner.

## Task 2: orbit structure

### The pure-braid orbit does not fill the Nielsen class

`[CHECKED n <= 10 from the census]` Nielsen classes that contain at least two
pure-braid orbits with G containing A_n: 3, 10, 15, 22, and 39 for n = 6 to 10.
Example: n = 6, types [2,2,1,1], [2,2,1,1], [3,2,1], [3,2,1] has two S_6 orbits of
sizes 24 and 72. Source: `split_an.py`.

`[CHECKED n <= 9]` Most splits come from a Klein symmetry. The Klein four-group
acts on tuples by (a b)(c d) = s0 s2^-1, by the rotation (t2, t3, t0, t1), and by
their product. In a split of this kind, one orbit consists of symmetric covers and
the other orbit has none. The counts are 3 of 3 split classes at n = 6, 9 of 10 at
n = 7, 12 of 15 at n = 8, and 18 of 18 tested at n = 9. Four classes at n = 9 were
skipped for size. The 3 other classes at n = 8 have orbits of size 1.

`[CHECKED]` One split has no such explanation: n = 7, types [2,2,2,1], [3,2,1,1],
[3,2,1,1], [3,2,1,1], two S_7 orbits of sizes 360 and 102. No Klein element
preserves this ordered type. The invariant that separates the two orbits is unknown.

### Inside one orbit: the group M_t

`[CHECKED n <= 9]` For orbits with G containing A_n:

| n | orbits | M = S_q | 2-homogeneous, not S_q | not 2-homogeneous |
| --- | --- | --- | --- | --- |
| 4 | 6 | 3 | 3 | 0 |
| 5 | 22 | 19 | 3 | 0 |
| 6 | 57 | 54 | 3 | 0 |
| 7 | 209 | 197 | 12 | 0 |
| 8 | 368 | 362 | 6 | 0 |
| 9 | 798 | 792 | 0 | 6 |

The 6 exceptions at n = 9 have an identity corner and a of type [3,2,2,2]. They are
outside the PRIM hypotheses.

`[CHECKED n <= 9]` **M_t is not 2-homogeneous for every primitive G.** Six orbits at
n = 8 satisfy the PRIM hypotheses and have two M-orbits on pairs. They have a [2^4],
q = 4, |M| = 8, and |G| = 1,344 or 336. The types are [2,2,1^4], [3,3,1,1],
[3,3,1,1] (|G| = 1,344) and [2,2,2,1,1], [2,2,2,1,1], [3,3,1,1] (|G| = 336), in any
order at b, c, d. All their pairs are LIT. Under the PRIM hypotheses with G
containing A_n, M_t is 2-homogeneous in every orbit.

### What the literature gives

- `[CITED]` Liu and Osserman, "The irreducibility of certain pure-cycle Hurwitz
  spaces", arXiv math/0609118, Theorem 1.2: genus-0 pure-cycle Hurwitz
  factorizations form one pure-braid orbit. Theorem 1.3 gives the count
  min{e_i (d + 1 - e_i)} for four points. The introduction says that the statement
  fails quickly without the pure-cycle or genus-0 hypothesis. For the types here,
  pure-cycle means one nontrivial cycle of length at most 3 at each corner. Then
  n <= 5 and g_a has at most one 2-cycle. The theorem covers no marked pair.
- `[CITED]` Vetro, Indag. Math. 17 (2006) 115-127, Theorem 1: irreducibility for
  one special fibre over a base of genus at least 1, under a bound on the branching.
  The base here is the sphere. The paper's introduction attributes the sphere case
  with one special fibre to Natanzon and Kluitmann and two special fibres to
  Wajnryb. Those statements were read only in that secondary description.
- Index count `[PROVED]`: with four branch points and cycle lengths at most 3, one
  special fibre and three simple fibres force n <= 3. Two special fibres and two
  simple fibres force n <= 6. So the classical connectedness theorems (Clebsch,
  Hurwitz, Kluitmann, Wajnryb) apply to these types only for n <= 6.
- Conway-Parker and Fried-Voelklein type results are asymptotic in the number of
  branch points per class. They give nothing for four points.
- A bounded search found no classification of SL(2,Z)-orbits of genus-0
  pillowcase-tiled surfaces. Related preprints: arXiv 2210.11332, 2510.18255,
  1809.05016.

Conclusion for task 2: no published theorem gives connectedness for types
1^p 2^q 3^z with n >= 7, and the census shows that connectedness is false with full
monodromy S_n. A proof of PRIM cannot quote orbit transitivity on the Nielsen class.

## Proved statements

### Lemma 1 (tree of an arc) `[PROVED]` `[CHECKED n <= 9]`

Fix a state and a corner x. Call the orbits of <g_a, g_x> the Gamma-components, the
orbits of <g_y', g_z'> the T-components, and the cycles of h_x the annuli. Each
annulus lies in one Gamma-component and one T-component. The bipartite graph with
these vertices and the annuli as edges is a tree. Each component, with its annuli
capped by discs, is a genus-0 three-point cover.

Proof. Let gamma be the boundary of a thin neighbourhood of the arc a-x in B. The
curve gamma cuts B into a disc around {a, x} and a disc around {y, z}. Components
of the preimage of the first disc are the orbits of <g_a, g_x>. Components of the
preimage of gamma are the cycles of h_x, the monodromy of gamma. Q is a sphere, so
every preimage circle separates Q. The dual graph of a sphere cut along disjoint
circles is connected and loses connectivity when you remove any edge. That graph is
a tree. A subsurface of a sphere is planar, so each capped component has genus 0.

`mine.py` asserts the tree identity (components minus annuli equals 1) on every
state of every orbit.

### Lemma F (faces of a chain, and the Face certificate) `[PROVED]` `[CHECKED n <= 9]`

Let a chain at x have a-points s_0, ..., s_L and mirrors r_1, ..., r_L, on sheets
e_0, ..., e_(2L+1), with s_i = (e_2i e_(2i+1)) and r_i = (e_(2i-1) e_2i). Then h_x
maps e_0 -> e_2 -> ... -> e_2L and e_(2L+1) -> e_(2L-1) -> ... -> e_1. If g_x fixes
e_0 and e_(2L+1), these sheets form one cycle of h_x of length 2L + 2.

Proof. h_x(i) = g_x(g_a(i)). Then h_x(e_2i) = g_x(e_(2i+1)) = e_(2i+2) and
h_x(e_(2i+1)) = g_x(e_2i) = e_(2i-1). If g_x fixes e_0, then h_x(e_1) = e_0 and
h_x(e_0) = e_2. If g_x fixes e_(2L+1), then h_x(e_2L) = e_(2L+1).

Face certificate. Fix g_a and let g_x run over its class. Keep each g_x whose graph
with g_a has a chain between two distinct 2-cycles of g_a. Let Lam_chain(a, x) be
the set of cycle types of g_a g_x for these g_x. Let Lam(y, z) be the set of cycle
types of products of the two other classes. If the two sets are disjoint, write
**Face(x)**. Face(x) implies that no pair is x-lit, in any orbit of the class.

Proof. In every state the arc-adapted tuple gives h_x = (g_y' g_z')^-1, and cycle
types are conjugation invariant. A chain at x puts the type of h_x in both sets.

Tree criterion. A class has a state with a chain at x if and only if the following
gluing exists. One side is a collection of (a, x) dessins that contains a chain.
The other side is a collection of (y, z) dessins. Faces of equal length are glued
so that the graph of Lemma 1 is a tree. This is a restatement of Lemma 1, and it is
equivalent to "the class is not x-empty".

Data, source `face.py` and `classlevel.py`:

- A class-corner is *x-empty* when no pair in the class is x-lit. Counts for
  n = 6 to 9: 3, 6, 27, 12.
- The cycle-type test Face(x) holds in 15 class-corners at n = 8 and 3 at n = 9. It
  never holds for a class with an x-lit pair.
- At n = 8, 18 x-empty class-corners have a pair with no Par, Rig, or Cut
  certificate over B. Face(x) explains 12. The tree criterion explains the other 6
  (class a [3,2,2,1], [2^4], [2^4], [3,1^5]; checked by hand: the only matching face
  type [3,2,2,1] forces a double edge in the graph of Lemma 1).

### Counterexample to every per-corner converse `[PROVED]` `[CHECKED]`

Class a [3,2,2,1], b [2,1^6], c [2^4], d [3,3,2], n = 8, G = S_8, plain orbit 9,
marked orbit 18. Representative:
`[[1,2,0,4,3,6,5,7],[0,1,2,3,4,5,7,6],[5,6,3,2,7,0,1,4],[6,7,4,1,5,2,0,3]]`.
The only pair, cycles (3 4) and (5 6), is not b-lit. It is c-lit and d-lit by one
mirror.

Proof that it is not b-lit. g_b is one transposition, so a chain at b has one
mirror and its outer sheets are fixed by g_b. By Lemma F, h_b has type [4,3,1], and
so does g_c g_d. The cycle counts 3 + 4 + 3 = 8 + 2 show that (h_b^-1, g_c, g_d) is
one genus-0 component. Read the four 2-cycles of g_c as the edges of a planar map.
Its vertices are the cycles of g_d, of degrees 3, 3, 2, and its faces are the
cycles of g_c g_d. The connected multigraphs with these degrees are a triangle with
one doubled edge, a doubled edge with a pendant loop, and a path with two loops.
Their face types are (3,3,2), (5,2,1), and (6,1,1). None is (4,3,1).

Consequences:

- "x-dark implies Par(x), Rig(x), or Cut(x) over B or a pillowcase factor" is false.
  The cover is primitive, so it has no proper factor.
- "PRIM holds corner by corner" is false.
- The gloss on D2 in `d10-mechanisms/theory.md` ("an uncertified class has a legal
  path in a direction of that class") does not hold for abstract covers.
- U* is not affected. U* asks for certificates at all three corners.

Two more uncertified families at n = 8 have G imprimitive and no pillowcase factor
(9 pair-corners; with the 6 primitive ones they are the 15 found by `refine.py`).

- |G| = 192, a [2^4], b [2,1^6], c [3,3,1,1], d [3,3,2]. Blocks have size 2 and g_b
  acts trivially on blocks. The factor N is a three-point cover with no nontrivial
  deck map. In the sphere minus {a, c, d} the arc a-d is unique up to isotopy. So
  the graph of N at d does not depend on the state. The only regular d-point of Q
  lies over the d-pole of N. That pole is adjacent to one a-point of N. Pairs over
  the other a-point of N are never d-lit. `[PROVED]`
- |G| = 384, a [2,2,1^4], b [2,2,1^4], c and d [3,3,2]. Every 2-cycle of every
  conjugate of g_b swaps two blocks. Here q = 2, so a chain has one mirror. A mirror
  between the two marks then forces a closed leaf on 4 sheets. Its two annuli give
  a double edge in the graph of Lemma 1.
  `[PROVED]` by the case list of T-component sizes 2, 3, 5, 6.

The 36 other uncertified pair-corners at n = 8 and all 18 at n = 9 have a proper
pillowcase factor.

### Lemma T (twists give elements of M_t) `[PROVED]` `[CHECKED n <= 10]`

Fix a state and a corner x. If k = h_x^m commutes with g_a and g_x, then the
permutation of the regular a-points induced by k lies in M_t.

Proof. For x = b the full twist s0^2 conjugates g_a and g_b by h = g_a g_b, up to
the direction convention. After m twists the conjugator is h^m = k, so the tuple is
unchanged. The census label rule
moves the label on sheet i to sheet k(i) or its inverse. For x = c and x = d, apply
the same computation to the arc-adapted tuple. The twist about {d, a} is the twist
about {b, c} followed by a global conjugation, which the plain canonical form absorbs.

Corollary T1 (pinch transposition). Suppose a mirror r of g_x joins two distinct
regular a-points s and t, and g_x fixes the two outer sheets. Suppose also that no
other cycle of h_x has length divisible by 4. Then the transposition (s t) lies in M_t.

Proof. By Lemma F, h_x is the 4-cycle (e_0 e_2 e_3 e_1) on the component. Let l be
the least common multiple of the other cycle lengths. Take m = 2l for odd l and
m = l otherwise, so m = 2 mod 4. Then k = h_x^m is (e_0 e_3)(e_1 e_2) on the
component and the identity elsewhere. k commutes with g_a and g_x and swaps s and t.

Corollary T2. If M_t is primitive on the regular a-points and some state satisfies
T1, then M_t = S_q and every pair is LIT. Proof: a primitive group that contains a
transposition is symmetric (`[CITED]` Jordan; Wielandt, Finite Permutation Groups,
Theorem 13.3, number quoted from memory and not re-read in this session). The LIT
relation is invariant under M_t, and the pinch pair is LIT.

Data, source `twist.py`:

- Literal check on the arc a-b with `pure_move` (tuple returns, labels move by k):
  15, 17, 162, 318, 1,089, and 2,046 checks pass for n = 4 to 9, with no failure.
- Let W be the group generated by all twist elements with literal return,
  transported to the base state. |W| divides |M| in every orbit.
- W = M in 340 of 387 primitive orbits at n = 8 and 697 of 813 at n = 9.
- A twist transposition exists in 334 of 387 primitive orbits at n = 8 and 683 of
  813 at n = 9.
- So twist elements with literal return do not generate M_t in general. Twists
  that return only up to conjugation, and loops of the Hurwitz curve that are not
  cusp loops, also contribute.

### Lemma C (cylinders, abstract form) `[PROVED given D0]` `[CHECKED n <= 9]`

In the tree of Lemma 1, call a component a *regular leaf* when all its cycles are
2-cycles. A *maximal cylinder* is a maximal chain of annuli glued through regular
leaves. CylA: one mark lies on a regular leaf inside a maximal cylinder, and the
other mark lies in the closure of that cylinder. CylB: the marks lie on the two
different boundary components of one maximal cylinder. If CylA or CylB holds in
some state, the pair is LIT.

Proof. The maximal cylinder is a flat cylinder with no pole or zero in its interior.
Lift the two marks to the universal cover, a strip. Under CylA or CylB the lifts
are at different heights, or on one regular leaf. The straight segment between the
lifts has its interior in the open strip. By D0 it is a chain in the state whose
arc has the direction of the segment.

The proof fails for two marks on the same boundary component. That case is
excluded from CylA and CylB.

Data: no DARK pair has a cylinder witness. LIT pairs with no cylinder witness in
any state: 3 of 9, 12 of 22, 60 of 210, 75 of 345, 246 of 1,522, 693 of 2,766 for
n = 4 to 9. Under the PRIM hypotheses, pairs with a cylinder witness: 0 of 3,
10 of 19, 57 of 99, 270 of 339, 790 of 958, 1,866 of 2,325. The smallest LIT pair
with no cylinder witness: n = 4, a [2,2], b [2,1,1], c [2,1,1], d [3,1].

### Lemma G (B_x is generated by all lassos) `[PROVED]`

The fibres of B_x are the connected components of a graph on the sheets. The edges
of the graph are the 2-cycles of all G-conjugates of g_x.

Proof. The components of that graph form a G-invariant partition, since the edge
set is G-invariant. It merges every 2-cycle of g_x. Any G-congruence that merges
the 2-cycles of g_x merges the 2-cycles of every conjugate.

Reading. The conjugates of g_x are the monodromies of all lassos around x. The
values of g_x over the pure-braid orbit with g_a pinned, the set X_x, are the
lassos along simple arcs. The x-lit relation uses X_x only. The whole lit-side
difficulty is the gap between simple arcs and all paths. Example: in the n = 8
primitive counterexample, the pinned orbit has 216 triples and X_b has 19 of the
28 transpositions. The 9 missing ones are (3 4), (5 6), the four transpositions
between {3,4} and {5,6}, and (0 7), (1 7), (2 7). Source: `pinned.py`.

Remark (a tautology). "The transitive closure of the one-mirror relation at x
equals the transitive closure of x-lit" is true by definition. Consecutive
a-points on a chain are joined by one mirror in the same state. The matching counts
in `summary.json` are not evidence.

### Proposition N (nearest pair) `[PROVED given D0]`, not checked by computation

Let s and t be two distinct regular a-points. Suppose their flat distance is
minimal among all such pairs. If some shortest path from s to t contains no zero,
then the pair has a one-mirror witness.

Proof. A shortest path is a geodesic. It cannot pass through a pole, and it bends
only at zeros. With no zero on it, it is one straight segment with regular
interior. Develop the segment: a-points develop to the lattice Z^2 and the other
corners to half-lattice points. The holonomy is m v with v primitive. For m >= 2
the point at v is a regular a-point closer to s than t, which contradicts
minimality. So m = 1, the midpoint is a regular point over some corner x, and the
segment is a one-mirror chain.

Reading. A one-mirror witness is the same as a singularity-free segment of
primitive holonomy. Zeros are the only obstruction in this argument. Primitivity
of G is not used, so the proposition cannot prove PRIM alone.

### Proposition R (reduction) `[PROVED]`

If M_t is 2-homogeneous and one pair is LIT, then every pair of that orbit is LIT.
Proof: an element of the stabiliser that induces the permutation p maps the marked
tuple (t; P, Q) to (t; p(P), p(Q)) inside one orbit, so both pairs have one verdict.

## Proof attempts and where each one breaks

### (a) Mirror transport

Idea: move one mirror of g_x by braids until it joins the two marks. With g_a
pinned, this asks whether X_x contains a 2-cycle between the marks.

- For all lassos, Lemma G answers the question: the mirrors of the conjugates of
  g_x connect all sheets of one B_x fibre.
- For simple arcs the statement is false corner by corner (n = 8 primitive
  example). The break is exact: X_b misses 9 of 28 transpositions there.
- x-lit is transitive in every corner relation at n <= 7 and n = 9 (2,646
  nontrivial tests at n = 9). It fails in 12 corner relations at n = 8, all with a
  proper pillowcase factor. It fails in 18 corner relations at n = 10 with no
  pillowcase factor (|G| = 1,920 or 3,840). LIT is not transitive in 3 orbits at
  n = 9.
- Same B_x fibre but not x-lit: 6, 6, 69, and 156 pair-corners for n = 6 to 9. At
  n = 8, 51 of the 69 have no certificate over B.

Verdict: transport inside one corner cannot prove U* or PRIM. A transport argument
must switch corners, and no rule for the switch came out of the data.

### (b) Induction on the degree

Operation: delete a sheet i fixed by g_a and by g_x, and shorten the cycles through
i at the two other corners. `[PROVED]` The result is a product-one, transitive,
genus-0 tuple of degree n - 1 with the same 2-cycles of g_a. The script asserts
this in every case.

Data `[CHECKED n <= 8]`, source `induct.py`:

- Orbits with such a sheet in some state: 23 of 23, 63 of 114, 126 of 213, and
  379 of 541 for n = 5 to 8. About 30% of the orbits at n = 8 have no removable
  sheet of this kind.
- Verdict before and after removal, over all pairs tested:

| n | LIT to LIT | DARK to LIT | LIT to DARK | DARK to DARK |
| --- | --- | --- | --- | --- |
| 6 | 105 | 9 | 0 | 0 |
| 7 | 633 | 9 | 0 | 0 |
| 8 | 1,293 | 24 | 6 | 6 |

Break: the verdict is not monotone in either direction. A 3-cycle shortened to a
2-cycle creates a mirror (DARK to LIT). A 2-cycle shortened to a pole destroys one
(LIT to DARK, n = 8, a [3,2,2,1], [3,3,1,1], [3,2,1,1,1], [3,2,1,1,1]). Only the
twist about the removed sheet's two corners lifts, so witnesses do not transfer.

### (c) Cylinders

Lemma C is correct and has no false positives. It is not universal: 25% of LIT
pairs at n = 9 (693 of 2,766) and 20% of PRIM pairs (459 of 2,325) have no cylinder
witness in any state. A counting argument that forces a cylinder containing both
marks cannot exist for these pairs. The mechanism fails first at n = 4.

### (d) Other ideas

- Degeneration (Lemma F, tree criterion). It gives a complete static description of
  which classes have a chain at x. It says nothing about which orbit of the class
  has it, and classes split (task 2).
- Nearest pair (Proposition N). It breaks at zeros on the shortest path.
- Symmetry (Proposition R, Lemma T). It breaks at two points: 2-homogeneity of M_t
  is unproved for G containing A_n, and it is false for three primitive groups
  (two at n = 8, one at n = 10).

## Ranked strategies and the next lemma for each

1. **Symmetry plus one witness, for G containing A_n.**
   - Next lemma H `[CONJECTURAL]`: under the PRIM hypotheses with G containing A_n,
     M_t is 2-homogeneous on the regular a-points. True for all 2,885 such orbits
     (8,952 pairs) with n <= 10.
   - Next lemma E `[CONJECTURAL]`: every such orbit has one LIT pair. Lemma C and
     Proposition N give E under side conditions.
   - H and E give PRIM for G containing A_n by Proposition R.
   - A weaker route to H: prove that M_t is primitive and that one state satisfies
     Corollary T1. Then Corollary T2 gives M_t = S_q.
   - H is a connectedness statement: the space of covers in the orbit with two
     marked regular a-points is connected. No published theorem gives it.
2. **One-mirror PRIM.** Next lemma `[CONJECTURAL]`: under the PRIM hypotheses, any
   two regular a-points are joined by a singularity-free segment of primitive
   holonomy. This is stronger than PRIM and true for all 9,118 pairs with n <= 10.
   The gain is a statement about one segment, which Proposition N proves when no
   zero obstructs.
3. **Primitive groups without A_n.** Lemma H is false there. The genus-0 hypothesis
   limits these groups (Guralnick-Thompson conjecture, proved by Frohardt and
   Magaard; pointer only, not read in this session). Next lemma: list the primitive
   genus-0 groups generated by four elements of types 1^p 2^q 3^z, then check them.
4. **Cylinders.** Use Lemma C as a source of witnesses for lemma E only.
5. **Per-corner transport and degree induction.** Both are refuted in the forms
   tested. Do not invest further without a different formulation.

The single most promising next lemma is **H**. It turns PRIM into an existence
statement, and three proved tools already produce witnesses.

## Facts that would falsify the strategies

- A PRIM orbit with G containing A_n and two M_t-orbits on pairs falsifies H.
  The nearest known failures have |G| = 1,344 and 336 at n = 8, and |G| = 60 at
  n = 10.
- A PRIM pair whose minimal chain length is 2 or more falsifies strategy 2. All 27
  known cases of length 2 (n <= 10) have G imprimitive.
- A PRIM orbit in which no state has a mirror between two regular a-points
  falsifies both E through one mirror and strategy 2.
- A DARK pair with a CylA or CylB witness falsifies Lemma C or dictionary D0.
- A state where the count of components minus annuli is not 1 falsifies Lemma 1.
- A class with Face(x) and an x-lit pair falsifies Lemma F.
- An orbit where |W| does not divide |M|, or a literal twist check that fails,
  falsifies Lemma T.
- An x-lit pair with a certificate at x falsifies Theorem U at that corner.
- A dark pair under the PRIM hypotheses falsifies PRIM.

## Files and commands

Run every command from this folder with `python3 -B`.

| File | Purpose | Command |
| --- | --- | --- |
| `mine.py` | Fully marked orbits, witnesses, distances, cylinders, M_t | `mine.py N 3` |
| `mine_nN.json` | Output of `mine.py`, n = 4 to 10 | |
| `summarize.py` | Tables, writes `summary.json` | `summarize.py 4 5 6 7 8 9 10` |
| `prim.py` | PRIM hypotheses summary | `prim.py 4 5 6 7 8 9 10` |
| `refine.py` | Per-corner PRIM, transitivity, exceptions | `refine.py 8 9 10` |
| `probe1.py`, `probe2.py` | Mirror incidences; uncertified per-corner cases | `probe2.py 8` |
| `pinned.py` | Orbit with g_a pinned, the set X_x | see the file header |
| `split_an.py` | Orbits per Nielsen class, Klein symmetry | `split_an.py 6 7 8 9` |
| `classlevel.py` | x-empty classes against certificates | `classlevel.py 6 7 8 9 10` |
| `face.py` | Face certificate from cycle types | `face.py 4 5 6 7 8 9 10` |
| `induct.py` | Sheet removal test | `induct.py 5 6 7 8` |
| `twist.py` | Lemma T checks, group W against M | `twist.py 4 5 6 7 8 9 10` |

`mine.py` asserts, for every orbit, that its verdicts and orbit sizes equal the
census in `d6-hurwitz-census`.

## Degree 10

All counts in this section are `[CHECKED n = 10]`. `mine.py 10 3` processed 2,017
orbits and 38.7 million marked states in 2,412 s. Every assertion passed, including
equality with the census verdicts.

Counts:

- Verdicts: 7,551 LIT and 158 DARK. Totals for n <= 10: 12,425 LIT and 439 DARK.
- Minimal chain length: 1 for 7,536 pairs, 2 for 15 pairs. The 15 pairs have G
  imprimitive (|G| = 1,920 or 120, a of type [2^4,1,1]).
- Largest distance to a witness state: 8. LIT pairs by that distance: 0: 204,
  1: 1,509, 2: 1,920, 3: 1,780, 4: 1,477, 5: 490, 6: 122, 7: 29, 8: 20. The maximum
  for n = 4 to 10 is 0, 2, 4, 5, 5, 7, 8. The largest orbit depth is 16.
- Witness density: 43.3% of the (state, LIT pair) incidences are witnesses
  (83,952,576 of 193,941,498).
- Corners: 335 pairs for each single corner, 1,032 for each two corners, 3,450 for
  all three. No pair is x-lit while a certificate holds at x.
- Cylinders: 765 of 7,551 LIT pairs have no cylinder witness. No DARK pair has one.
- PRIM: 1,498 orbits and 5,375 pairs. Every pair is LIT and has a one-mirror
  witness. 4,898 pairs have a cylinder witness.
- Per-corner PRIM: 12,351 of 12,357 pair-corners are one-mirror x-lit. The 6
  exceptions are one primitive family with G = S_10: a [3,3,2,2], and [2,1^8],
  [2^5], [3,3,3,1] in any order. Face(x) holds for all 6. This is a second
  primitive counterexample to the per-corner converse.
- M_t for G containing A_n: 1,535 orbits, 1,511 with M = S_q, 24 that are
  2-homogeneous and not S_q, and none that fail.
- M_t under the PRIM hypotheses: 2-homogeneous in 1,495 of 1,498 orbits. The 3
  exceptions have |G| = 60, a primitive action of A_5 on 10 sheets. They have
  a [2^4,1,1], q = 4, |M| = 4, and 3 orbits on pairs. All 1,489 PRIM orbits with G
  containing A_10 are 2-homogeneous.
- Lemma T: 4,240 literal checks on the arc a-b pass, and |W| divides |M| in all
  2,017 orbits. W = M in 1,378 of 1,544 primitive orbits. A twist transposition
  exists in 1,359 of them. Source: `twist_n10.log`.
- Classes: 33 x-empty class-corners, 24 with an uncertified pair. Face(x) explains
  6. The other 18 have |G| = 3,840 or 14,400 and were not checked by hand.
- Uncertified per-corner darkness: 153 pair-corners are not x-lit and have no
  certificate over B (12 with the pair DARK, 141 with the pair LIT). 36 have a
  proper pillowcase factor. Of the 117 others, 6 are the primitive family and 111
  have |G| = 1,920 or 3,840. Each of these covers has one block system, with
  blocks of size 2 over a degree-5 factor.

Statements that change at n = 10:

- x-lit is not transitive in 18 of 6,051 corner relations. All 18 have |G| = 1,920
  or 3,840 and no proper pillowcase factor. At n = 8 every failure had a pillowcase
  factor. LIT is transitive in all 2,017 orbits.
- Covers with blocks of size 2 over a non-pillowcase factor are a systematic source
  of per-corner darkness with no Par, Rig, or Cut certificate. They have |G| = 192
  and 384 at n = 8, and 1,920 and 3,840 at n = 10. The two hand proofs for n = 8 show
  the mechanism. A general statement for this family is open.

Not run at n = 10: `induct.py` and the Klein symmetry test of `split_an.py`.
