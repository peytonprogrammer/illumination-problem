# Illumination theorems for rooms with few reflex corners

Date: 2026-11-09. Direction d15 (small r).

## Results

- **r = 0, 1, 2 are proved, in a stronger form than L(r).** In every room with
  at most 2 reflex corners, a billiard path joins every two distinct interior
  points. The points can be real, not only lattice points. So L(0), L(1), L(2)
  and the different-class statements L'(0), L'(1), L'(2) hold.
- **r = 3 and r = 4 are partial.** The same lemmas certify 13,030 of 13,608
  position-type pairs at r = 3, and 503,328 of 564,629 at r = 4. Only 3 of the
  70 order types at r = 3 are fully certified, and 1 of 1,283 at r = 4, the
  cross. The gap is an explicit list.
- **Tests found no failure.** One test covers all 290,060 rooms with at most 8
  walls in a 12 x 12 box. It traced the lemma paths for 357 million lattice
  pairs. A second test covers a sample of 100,000 rooms with 10 or 12 walls.
  It traced the lemma paths for 389 million pairs. In that sample, shooting
  lit all 29 million pairs that have no certificate.
- **The proofs never use parity.** Each lemma holds for real points. That is
  why L'(r) comes with L(r) where a certificate exists. It also limits the
  method. A parity-free certificate shows that all real pairs of its position
  types are lit. That is false for some pair at r = 9. Whether it holds for
  every pair at r <= 8 is unknown.
- **The mechanical method in the requested form isn't feasible for r = 8.**
  For the reasons and the numbers, see
  [Mechanical method and feasibility for r = 8](#mechanical-method-and-feasibility-for-r--8).

| r | Walls | Order types | Position-type pairs | Certified | Status |
| --- | --- | --- | --- | --- | --- |
| 0 | 4 | 1 | 1 | 1 | Proved for all real interior pairs |
| 1 | 6 | 1 | 15 | 15 | Proved for all real interior pairs |
| 2 | 8 | 8 | 543 | 543 | Proved for all real interior pairs |
| 3 | 10 | 70 | 13,608 | 13,030 | Partial, 578 pairs open |
| 4 | 12 | 1,283 | 564,629 | 503,328 | Partial, 61,301 pairs open |

Order types are counted up to the 8 symmetries of the square.

## Setting

- A room P is a strictly simple orthogonal polygon with integer vertex
  coordinates. It has r reflex corners and W = 2r + 4 walls.
- An interior point is a point of the topological interior of P.
- A valid path is a billiard path of finite length that touches no vertex of P.
  It can pass through any interior point and reflect at any wall point that
  isn't a vertex.
- A pair of points is lit when a valid path joins them.
- L(r): in every room with r reflex corners, every two distinct interior
  lattice points of the same parity class are lit.
- L'(r): the same statement for two interior lattice points of different
  parity classes.

Two facts are used throughout.

- **Straight wall fact.** If a straight segment lies in the boundary of P, no
  point of its relative interior is a vertex. The boundary is a simple closed
  curve, so it doesn't turn inside a straight piece.
- **Unfolding.** A billiard path is the image of a straight segment under
  successive reflections in wall lines. The path is valid when the segment
  crosses each wall line at a point that isn't the image of a vertex.

## Lemmas

Each lemma is stated in a canonical frame. Apply any of the 8 symmetries of the
square to get the other frames. S and T are real points.

### Lemma A (rectangle)

**Statement.** Let Q be a closed rectangle inside P. Let S and T be distinct
interior points of P that lie in Q. If the open segment ST contains no vertex,
the segment ST is a valid path. The open segment can contain a vertex only when
S and T lie on one axis-parallel line.

**Proof.** The interior of Q lies in the interior of P, so no vertex is
interior to Q. A segment in a convex set touches the boundary at a relative
interior point only if the segment lies in a supporting line. So the open
segment misses the boundary of Q, or it lies in one side of Q. In the second
case S and T are on one axis-parallel line.

### Lemma A2 (V-path for collinear points)

**Statement.** Let S = (s1, y) and T = (t1, y) with s1 < t1 be interior points.
Suppose that y' < y, that R = [s1, t1] x [y', y] lies in P, and that the side
[s1, t1] x {y'} lies in the boundary of P. Then the path S, M, T with
M = ((s1 + t1)/2, y') is valid.

**Proof.** S and T are corners of R, and M is a relative interior point of the
opposite side. So both open segments lie in the interior of R. By the straight
wall fact, M isn't a vertex. The reflection at M sends the first segment to the
second.

### Lemma B (one door with a flat end)

**Hypotheses.** Let p < q, d < e, and w = q - p.

1. The corridor E = [p, q] x [d, e] lies in P. Its sides {p} x [d, e] and
   {q} x [d, e] lie in the boundary of P.
2. T = (t1, t2) with p < t1 < q and d < t2 <= e.
3. S = (s1, s2) with s1 > p and s2 < d.
4. The rectangle Q* = [p, max(q, s1)] x [s2, d] lies in P.
5. Flat end: {p} x [s2, d] lies in the boundary of P.

The door is the segment [p, q] x {d}. Hypothesis 5 says that the wall x = p
continues straight past the door end (p, d).

**Statement.** For each sign eps in {+1, -1}, some integer k gives a valid path
from S to T. Its unfolding is the segment from S to
T' = (p + eps (t1 - p) + 2 w k, t2).

**Proof.** Let lambda = (d - s2)/(t2 - s2), so 0 < lambda < 1. The segment from
S to T' crosses the line y = d at x* = s1 + lambda (X - s1), where X is the
first coordinate of T'. For a fixed sign, the values x* form an arithmetic
progression with step 2 w lambda < 2 w. The open window (p - w, p + w) has
length 2 w, so it contains a value x*. Fix that k.

- If p < x* < q, the open segment from S to (x*, d) lies in the interior of
  Q*. The point (x*, d) is interior to P.
- If x* = p, the path reaches the wall point (p, d). By hypotheses 1 and 5 and
  the straight wall fact, (p, d) isn't a vertex.
- If p - w < x* < p, the segment crosses x = p at a height strictly between s2
  and d. That point isn't a vertex, by hypothesis 5. The reflected path stays
  in the interior of Q* and crosses the door at 2p - x*, which lies in (p, q).

Past the door, the path stays in E up to height t2. It meets the side walls at
heights strictly between d and t2. Those points aren't vertices, by the
straight wall fact. The segment isn't vertical along a wall line, because
p < t1 < q. So the path is valid.

### Lemma B' (one door, near viewer)

Certificates don't use this lemma, because it compares S with T.

**Statement.** Assume hypotheses 1 and 2 of Lemma B. Let S = (s1, s2) with
s2 < d. Suppose that the bounding box of S and the door lies in P, and that
d - s2 <= t2 - d. Then for at least one sign, some integer k gives a valid path
whose unfolding goes from S to T' and crosses the door at a point of (p, q). If
d - s2 < t2 - d, both signs work.

**Proof.** Here lambda <= 1/2, so the progression of x* has step at most w.
The open door (p, q) has length w.

- If the step is less than w, the door contains a value x*.
- If the step equals w, the door contains a value x* unless the progression
  meets p. For lambda = 1/2, x* = (s1 + p + eps (t1 - p))/2 + w k. Both signs
  meet p only if t1 - p is a multiple of w. That contradicts p < t1 < q.

The open segment from S to (x*, d) lies in the interior of the bounding box.
The point (x*, d) is interior to P. The rest is as in Lemma B.

Lemma B' needs no flat end. Without a flat end and with d - s2 > t2 - d, the
progression can miss the door. For an example, see
[Candidates that fail](#candidates-that-fail).

### Hubs, arms, and full-period windows

A hub is a closed rectangle G inside P. An arm of G is a corridor attached to a
side of G, with these properties.

- The corridor is a rectangle outside G with one side, the door, on a side of
  G. The two sides of the corridor that are perpendicular to the door lie in
  the boundary of P.
- The door has a flat end F at a corner of G.
- The side of G that is adjacent to the door at F lies entirely in the boundary
  of P. That side is the mirror side of the arm.

An arm point is an interior point of P in the corridor. It lies strictly
between the two corridor walls and not on the door line. It can lie on the far
end of the corridor.

Let w be the door width and f the coordinate of F along the door line. The
full-period window of the arm is the open interval (f - w, f + w) on the door
line. Half of it is the door. The other half is the image of the door in the
mirror side. Seen from G, the images of an arm point with coordinate v along
the door are at f + eps (v - f) + 2 w k. Here eps is a sign and k an integer.

### Lemma B2 (viewer in the hub, one reflection)

**Hypotheses.** G is a hub, T is an arm point of an arm of G, and the side of G
opposite to the door lies entirely in the boundary of P. S is an interior point
of P in the closed rectangle G.

**Statement.** For at least one sign eps, some integer k gives a valid path
from S to T. The path first reflects in the side opposite to the door.

**Proof.** Take G = [0, L] x [0, H], the door on the side x = 0 with F = (0, 0),
and the corridor in x < 0. The floor [0, L] x {0} and the side {L} x [0, H] are
walls. Reflect the arm in the line x = L. The door image is on the line
x = 2L. Images of T are at (2L + beta, theta) with theta = eps t + 2 w k, where
T = (-beta, t). The segment from S to an image crosses x = 2L at a height y*.
As in Lemma B, each sign gives a value y* in the window (-w, w).

- If 0 < y* < w, the segment crosses x = L at a height strictly inside (0, H).
  That point isn't a vertex. The path then returns through the interior of G to
  the door.
- If y* = 0, the path arrives at F, which isn't a vertex.
- If -w < y* < 0, the segment also crosses the floor line y = 0, at some x°
  with 0 < x° < 2L. If x° differs from L, both reflection points are relative
  interior points of walls. If x° = L, the path meets the corner (L, 0), and
  the candidate is invalid.

The corner case fixes y* for the given S. The two signs give different heights
theta, because 0 < t < w. So they give different values y*, and at most one
sign meets the corner case with its only window value.

### Lemma C (two doors on one hub)

**Hypotheses.** G is a hub. S is an arm point of arm 1 and T is an arm point of
arm 2. The two arms are different arms of the same hub G. One of three forms
holds.

- **par.** The doors are on opposite sides of G.
- **perp.** The doors are on adjacent sides of G.
- **same.** The doors are on the same side of G, their flat ends are the two
  corners of that side, and the opposite side of G lies entirely in the
  boundary of P.

**Statement.** For every pair of signs (eps1, eps2) there are integers k1 and
k2 with the following property. The segment from the image of S to the image
of T is the unfolding of a valid path from S to T. The segment crosses each
door line inside the full-period window of its arm.

**Proof, par form.** Take G = [0, L] x [0, H], door 1 on x = 0 and door 2 on
x = L. Let S = (-alpha, s) and T = (L + beta, t). Let f1, f2 in {0, H} be the
flat ends, and w1, w2 the door widths. Let sigma0 = f1 + eps1 (s - f1) and
theta0 = f2 + eps2 (t - f2).

Take a line of slope kappa that crosses x = 0 at height a and x = L at height
b. It passes through (-alpha, a - alpha kappa). That point is an image of S of
sign eps1 when a is congruent to sigma0 + alpha kappa modulo 2 w1. In the same
way, the line passes through an image of T of sign eps2 when b is congruent to
theta0 - beta kappa modulo 2 w2.

For a real kappa, let a(kappa) be the representative of sigma0 + alpha kappa
modulo 2 w1 in [f1 - w1, f1 + w1). Let b(kappa) be the representative of
theta0 - beta kappa modulo 2 w2 in (f2 - w2, f2 + w2]. The line exists when
kappa is a zero of

    Phi(kappa) = (b(kappa) - a(kappa))/L - kappa.

- Between jumps, Phi is continuous and strictly decreasing.
- Phi is right-continuous. Every jump of a is downward and every jump of b is
  upward, so every jump of Phi is upward.
- Phi is positive for very negative kappa and negative for very positive
  kappa, because a and b are bounded.

Let kappa° be the infimum of the set where Phi <= 0. By right continuity,
Phi(kappa°) <= 0. The left limit is >= 0. Jumps are upward, so Phi(kappa°) is
at least the left limit. So Phi(kappa°) = 0 and Phi has no jump at kappa°. The value
a = f1 - w1 occurs only at jumps of a, and b = f2 + w2 only at jumps of b. So a
and b lie in the open windows.

Validity. The corridors unfold to the half planes x < 0 and x > L. Their wall
hits are relative interior points of straight walls. Because s isn't on a
corridor wall, the segment isn't along a wall line. Inside the hub, the segment
from (0, a) to (L, b) lies in G and its mirror images in the mirror sides.

- If f1 = f2 = 0: |a| < w1 <= H and |b| < w2 <= H. The segment crosses the
  floor line at most once, at a relative interior point of the floor or at a
  flat end. The case a = b = 0 doesn't occur, because then kappa = 0 and
  a = sigma0, which isn't f1.
- If f1 = 0 and f2 = H: a < w1 <= H and b > H - w2 >= 0. The segment crosses the
  floor line only if a < 0, and the ceiling line only if b > H. Both crossings
  have 0 < x < L, or they are flat ends.

**Proof, perp form.** A door can't lie on a side that is entirely wall. So up
to symmetry, door 1 is on x = 0 with F1 = (0, 0), and door 2 is on y = H with
F2 = (L, H). The mirror sides are the floor and the side x = L. Let
S = (-alpha, s) and T = (t, H + beta). A line of slope kappa > 0 through (0, a)
and (b, H) has kappa b = H - a. Let a(kappa) be the representative of
sigma0 + alpha kappa in [-w1, w1). Let b(kappa) be the representative of
theta0 - beta/kappa modulo 2 w2 in [L - w2, L + w2). Let

    F(kappa) = kappa b(kappa) + a(kappa) - H.

Between jumps F is strictly increasing, F is right-continuous, and all jumps
are downward. F is negative near 0 and positive for large kappa. The same
argument gives a zero at a point of continuity, so a and b lie in the open
windows.

Validity in the hub. The segment goes from (0, a) to (b, H) with positive
slope. It can cross the floor line (if a < 0) and the line x = L (if b > L).
The only vertex that it could meet is the corner (L, 0). That needs
(-a)(b - L) = L H. But -a < w1 <= H and b - L < w2 <= L, so the product is less
than L H. The corner case never occurs.

**Proof, same form.** Take both doors on x = 0, with F1 = (0, 0) and
F2 = (0, H). The floor, the ceiling, and the side x = L are walls. The two
corridors are disjoint and no wall has zero thickness, so w1 + w2 < H. Reflect
arm 2 in x = L. The problem becomes the par form on the hub [0, 2L] x [0, H]
with f1 = 0 and f2 = H. The segment crosses x = L at height (a + b)/2. That
height lies strictly between (H - w1 - w2)/2 and (H + w1 + w2)/2, so strictly
inside (0, H). The crossing point isn't a vertex.

### Lemma D (two corridors at one corner)

**Hypotheses.** Let V = (0, 0), w > 0, and h > 0.

1. Corridor 1 is E1 = [-w, 0] x [0, e1]. It lies in P, and its sides
   {-w} x [0, e1] and {0} x [0, e1] lie in the boundary of P.
2. Corridor 2 is E2 = [0, e2] x [-h, 0]. It lies in P, and its sides
   [0, e2] x {-h} and [0, e2] x {0} lie in the boundary of P.
3. The block [-w, 0] x [-h, 0] lies in P.
4. S = (-b, e) with 0 < b < w and 0 < e <= e1. T = (a, -c) with 0 < a <= e2
   and 0 < c < h.

The two doors are the top side and the right side of the block. They share the
end V.

**Statement.** S and T are lit.

**Proof.** The bounding box of T and door 1 is [-w, a] x [-c, 0]. The bounding
box of S and door 2 is [-b, 0] x [-h, e]. Both lie in the union of the block
and the corridors.

- If c <= e, use Lemma B' with viewer T and corridor 1.
- If b <= a, use Lemma B' with viewer S and corridor 2.
- Otherwise c > e and b > a, so a e < b c. The segment from T to S crosses
  x = 0 at height -c + a (c + e)/(a + b), which is negative and more than -c.
  So it crosses door 2 at an interior point. It then crosses the block and
  crosses y = 0 at a point with -b < x < 0, inside door 1. Every point of the
  segment is interior to P.

The hypotheses compare each point with grid objects only. The comparison of S
with T happens inside the proof. So Lemma D gives metric-free certificates.

## Order types, position types, and certificates

**Order type.** Sort the distinct x-coordinates of the vertices as
x_0 < ... < x_nx, and the y-coordinates as y_0 < ... < y_ny. The order type of
P is the set of grid cells [x_i, x_i+1] x [y_j, y_j+1] inside P. A room with r
reflex corners has r + 2 vertical walls, so nx <= r + 1 and ny <= r + 1.
`enum_types.c` lists all cell sets that are connected, have no hole and no
pinch point, have W vertices, and have a vertex on every grid line.

**Position type.** A point gets doubled index coordinates (X, Y). X = 2i means
that the point lies on the grid line x = x_i. X = 2i + 1 means that it lies
strictly between x_i and x_i+1. The same holds for Y.

**Certificate.** A certificate for (order type, type of S, type of T) names a
lemma and the grid objects that satisfy its hypotheses. `lemmas.py` searches
for certificates in the order A, A2, B, B2, C, D.

**Why a certificate is metric-free.** Every hypothesis of Lemmas A, A2, B, B2,
C, and D is one of these.

- A set of grid cells lies in P.
- A set of unit grid edges lies in the boundary of P.
- A point lies on a named grid line, or strictly between two named grid lines.

None of them compares S with T, and none uses a length. So a certificate holds
for every room of that order type, for all edge lengths, including non-integer
ones. It holds for every pair of real interior points of those position types.

The one exception is the vertex test of Lemma A for two points on the same grid
line. The code refuses the certificate when a grid vertex lies strictly between
the two position types.

## Theorems for r <= 2

**Theorem 0.** In a rectangle, every two distinct interior points are lit. This
is Lemma A with Q = P. A segment between interior points of a rectangle touches
no corner. L(0) and L'(0) follow.

**Theorem 1.** In every room with 1 reflex corner, every two distinct real
interior points are lit. L(1) and L'(1) follow.

**Proof.** Take P = [0, a] x [0, b] minus (c, a] x (d, b], with 0 < c < a and
0 < d < b. The reflex vertex is (c, d). P is the union of the rectangles
R1 = [0, a] x [0, d] and R2 = [0, c] x [0, b].

- If S and T lie in R1, or both lie in R2, use Lemma A. A collinear pair has
  no vertex strictly between its points. The only vertex in the interior of
  the bounding box is (c, d). The interior points of P on the line y = d have
  x < c, and those on the line x = c have y < d.
- Otherwise one point, say T, has t2 > d and t1 < c, and S has s1 > c and
  s2 < d. Use Lemma B with p = 0, q = c, e = b. The corridor is
  [0, c] x [d, b]. Q* = [0, s1] x [s2, d] lies in R1. The wall x = 0 runs from
  (0, 0) to (0, b), so the door end (0, d) is flat.

The certificate table `cert_r1.json` has the same case split: 14 position-type
pairs by Lemma A and 1 by Lemma B.

**Theorem 2.** In every room with 2 reflex corners, every two distinct real
interior points are lit. L(2) and L'(2) follow.

**Proof.** There are 8 order types up to symmetry. The following table shows
them, with rows listed from top to bottom. For each one, the search finds a
certificate for every pair of position types. `cert_r2.json` has the counts.

| Grid | Shape | Name | A | A2 | B | B2 | C |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2 x 3 | `#./##/.#` | Z, reflex corners on one line | 23 | 0 | 4 | 0 | 1 par |
| 2 x 3 | `#./##/#.` | T, tab centered on a grid line | 26 | 0 | 2 | 0 | 0 |
| 2 x 3 | `##/#./##` | U, equal prongs | 35 | 1 | 6 | 2 | 1 same |
| 3 x 3 | `#../###/..#` | Z, thin neck | 36 | 0 | 8 | 0 | 1 par |
| 3 x 3 | `##./###/.##` | Z, wide neck | 134 | 0 | 16 | 0 | 1 par |
| 3 x 3 | `#../###/##.` | T, general | 82 | 0 | 8 | 0 | 0 |
| 3 x 3 | `#../#.#/###` | U, unequal prongs | 46 | 1 | 12 | 4 | 3 same |
| 3 x 3 | `#../##./###` | Staircase | 81 | 0 | 8 | 0 | 1 perp |

The proof of Theorem 2 has three parts: the lemma proofs, the completeness of
the type list, and the certificate search. The search is a finite computation
that you can repeat with `python3 -B run_cert.py 2 v`.

**How the hard pairs go.**

- T shapes. The tab door has two reflex ends, so the tab point has no
  full-period window. Swap the roles: the tab point is the viewer, and the far
  part of the bar is the corridor. Its door has a flat end on the long wall.
- U shapes. Two points on the line of the notch bottom, one in each prong, use
  Lemma A2 or Lemma B2. Two points deep in the two prongs use Lemma C, same
  form.
- Z shapes use Lemma C, par form. The staircase uses Lemma C, perp form.

## Different-class pairs, L'(r)

Lemmas A, A2, B, B2, and C don't use parity or integrality. So each certified
position-type pair is lit for same-class pairs, different-class pairs, and
non-lattice points alike.

- L'(0), L'(1), and L'(2) are proved (Theorems 0, 1, 2).
- L'(3) and L'(4) are stated and open. They hold for every pair whose position
  types have a certificate. The open pairs are the same lists as for L(3) and
  L(4). L'(3) holds for the 3 fully certified types, and L'(4) for the cross.

A remark on the open pairs. Let S be an interior lattice point and D a
primitive integer vector. The unfolded segment from S to S + D has no lattice
point in its interior, so the path of length |D| from S touches no vertex
before its end. Its end point M is a lattice point of a different class from S.
The path is valid when M isn't a vertex. This reduces L'(r) to a reachability
question, but it doesn't say which points M occur. Nothing more is proved here.

## Partial theorems for r = 3 and r = 4

**Theorem 3 (partial).** Let P have 3 reflex corners. Let S, T be distinct real
interior points. If the position types of S and T aren't in the `uncovered`
list of the order type of P in `cert_r3.json`, the pair is lit.

**Theorem 4 (partial).** The same statement holds for 4 reflex corners and
`cert_r4.json`.

**The gap.** The link distance of a pair is the least k with this property:
rectangles R1, ..., Rk inside P exist with S in R1 and T in Rk, and
consecutive rectangles share a cell. `classify_gap.py` gives these counts of open position-type
pairs.

| r | k = 1 | k = 2 | k = 3 | k = 4 | k = 5 | Total |
| --- | --- | --- | --- | --- | --- | --- |
| 3 | 15 | 246 | 269 | 48 | 0 | 578 |
| 4 | 1,182 | 23,515 | 28,992 | 7,124 | 488 | 61,301 |

The open fraction per type ranges from 0% to 20% at r = 3, and from 0% to 37%
at r = 4. Overall it is 4.2% at r = 3 and 10.9% at r = 4.

**Fully certified types.** For these order types, every two distinct real
interior points are lit, so L and L' hold for every room of the type.

- r = 3: `.#./###/##.`, `.#./##./###/.##`, and `##../####/.###/.##.`. Each
  needs Lemma D for 1 pair.
- r = 4: the cross `.#./###/.#.`. Opposite arms use Lemma A. Adjacent arms use
  Lemma D.

The open pairs fall into three kinds.

1. **k = 1: collinear pairs separated by a vertex.** S and T lie in one
   rectangle, on one grid line, with a reflex vertex between them, and no wall
   satisfies Lemma A2. First case: type `#../###/#.#`, position types (1, 2)
   and (5, 2).
2. **Half-period doors.** One point is in a corridor whose door has two reflex
   ends, and Lemma D doesn't apply. Lemma B' lights such a pair when the viewer
   is at least as near to the door line as the corridor point. The rest is
   open.
3. **Chains and non-rectangular hubs.** The path must pass 2 or more doors
   that don't lie on one rectangular hub. First cases: the snake
   `#./##/.#/##` with position types (1, 1) and (1, 5), and the 4-step
   staircase in the following example.

**Example of a pair that Lemma D closes.** In type `.#./###/##.`, S is in the
top tab and T is in the right arm. Both doors have two reflex ends, so no
full-period window exists. The two doors share the reflex vertex V. Lemma D
applies with the middle cell as the block. Without the weak form of Lemma B',
the pairs with S + T = 2V stay open: there the direct segment meets V.

**Example of a pair that stays open.** In the 4-step staircase
`#.../##../###./####`, S is in the top cell and T is in the cell at the far
right. Each door has a flat end, so both full-period windows exist. But the
region between the doors is an L shape, not a rectangle. A line that solves
the two window conditions of Lemma C can pass the middle reflex vertex on the
outer side. The proof of Lemma C gives no control of that.

## General lemma candidates

### (i) Common rectangle implies lit

- **Proved:** Lemma A, when no vertex lies on the open segment.
- **Refuted as a statement about the direct segment.** Room: [0, 4] x [0, 6]
  minus (2, 4] x (2, 4), a U with 8 walls. S = (2, 1) and T = (2, 5) are
  interior points of the same class in the rectangle [0, 2] x [0, 6]. The
  segment ST contains the reflex vertices (2, 2) and (2, 4).
- **Status of "lit".** That pair is lit by Lemma A2 through (0, 3). In general,
  "two points in one rectangle are lit" is open. The 15 open pairs with k = 1
  at r = 3 are the first cases without a proof.

### (ii) Two candidates suffice

**Refuted in this form:** no bound on the number of reflections works for all
rooms, even for r = 1.

Room: [0, 60] x [0, 2] together with [0, 1] x [0, 100], an L with 6 walls.
S = (50, 1) and T = (1/2, 99), or any lattice-scaled copy. Let m be the
absolute slope of a path from S to T.

- Between its last visit to x = 50 and its next visit to x = 1, the path moves
  monotonically in x inside a strip of height 2. It reflects at least
  49 m / 2 - 1 times.
- After its last visit to y = 2, the path climbs 97 inside a strip of width 1.
  It reflects at least 97/m - 1 times.

The sum is at least 2 sqrt(49 x 97 / 2) - 2, which is more than 95. Scaling
the lengths makes the count as large as you want. So a certificate must be a
family with an integer parameter and an existence argument, as in Lemmas B and
C. A fixed finite list of candidate paths can't work.

### Candidates that fail

The one-door family can be empty when the door has no flat end. Room: the bar
[0, 31] x [0, 10] with the tab [20, 30] x [10, 12], a T with 8 walls.
S = (5, 1) and T = (21, 11) have the same class. Paths that go straight from S
to the tab door and then stay in the tab unfold to segments from S to
(20 +/- 1 + 20 k, 11). They cross y = 10 at x* = 0.5 + 0.9 (20 +/- 1 + 20 k).
The values are 17.6 + 18 k and 19.4 + 18 k. None lies in the door (20, 30).
The pair is still lit: swap the roles and use Lemma B.

### (iii) Lattice translation reduction

Not proved and not refuted. One related fact is proved: a certificate depends
only on position types. So inside one cell of the grid of vertex lines, you can
move S and T freely. No statement that moves a point across a vertex line is
proved.

### (iv) Induction on r by cutting along a chord

Not proved. Two obstacles are specific.

- A path in a piece can reflect in the chord. The chord isn't a wall of P.
- The existence argument of Lemma C has one free parameter, the slope, and
  two windows. A chain of 3 doors has three windows and still one parameter.
  The monotone jump argument doesn't extend.

## Mechanical method and feasibility for r = 8

### What exists

1. `enum_types.c` enumerates order types by depth-first search over cell sets
   on an nx x ny grid, with nx <= ny <= r + 1.
2. `lemmas.py` searches certificates per pair of position types.
3. `verify.c` re-solves each certificate in metric rooms with integer
   arithmetic and traces each solution with a billiard tracer that doesn't use
   the lemma.

### Counts of order types

| r | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Order types | 1 | 1 | 8 | 70 | 1,283 | 29,621 | 866,041 |

The counts are up to symmetry. `check_types.py` confirms 8 and 70 by brute
force with separate code. The successive ratios are 8, 8.75, 18.3, 23.1, and
29.2. If the ratio keeps growing by about 6 per step, r = 7 has about
3 x 10^7 order types and r = 8 has about 10^9. That estimate is an
extrapolation, not a count.

At r = 4 a type has 440 position-type pairs on average. The number grows like
(r + 1)^4, so expect about 4,600 pairs per type at r = 8. That is about
5 x 10^12 certificates.

### Why the requested design doesn't close r >= 3

The task proposes a finite candidate list per order type. Validity regions are
linear inequalities, and blocking conditions are linear equations. Three facts
block that design.

1. **No finite candidate list exists.** See candidate (ii). Each certificate
   must be a family with integer parameters and an existence proof.
2. **Validity isn't linear.** For symbolic edge lengths and symbolic points,
   the condition "the segment passes a vertex on a given side" is a sign of a
   cross product. It is bilinear in the lengths and the point coordinates.
3. **A parity-free certificate proves too much.** It shows that all real pairs
   of its position types are lit. The dark pair of the r = 9 room has no such
   certificate. It is unknown whether some room with r <= 8 has a real pair
   that isn't lit. If one exists, L(r) for that room needs arithmetic: the gcd
   of the developing vector and the lattice points on the segment.

### What r = 8 needs

- **A chain lemma.** An existence argument for a path through 3 or more doors.
  At r = 4, 60% of the open pairs have link distance 3 or more.
- **A half-period door lemma that uses parity.** The worked example shows the
  shape of the gap: pairs that are symmetric in a reflex vertex.
- **A collinear lemma** for two points on a grid line with a vertex between
  them.
- **An enumerator for a 9 x 9 grid.** The cell mask needs 81 bits.
  `enum_types.c` holds 64.
- **A compiled certificate search.** `lemmas.py` takes about 12 ms per type at
  r = 4.

## Claims to test

The tests check the lemmas on metric rooms. They aren't a search for dark
rooms. Each claim is stated here before its test runs.

The populations and the cap come from the coordinator's note of 2026-11-09.
That note replaces the area limit of the original task. This document has no
way to confirm that Daniel approved the change.

Populations:

- **(a)** Every room with at most 8 walls inside a 12 x 12 bounding box, up to
  symmetry. That is every order type with r <= 2 and every vector of integer
  gap lengths with sum at most 12 on each axis.
- **(b)** A random sample of 100,000 rooms inside a 16 x 16 bounding box:
  50,000 with 10 walls and 50,000 with 12 walls. Seed 20261109. The order type
  is uniform over the canonical types. On each axis, the vertex coordinates are
  a uniform random subset of {1, ..., 16} of the needed size.

In every room, the test takes every pair of distinct interior lattice points,
in all parity classes.

Claims:

- **C1 (Lemma A, A2).** For each pair with an A or A2 certificate, the one
  segment that the lemma names traces to a valid path from S to T.
- **C2 (Lemma B).** For each pair with a B certificate, each of the 2 signs has
  an integer k that meets the window condition. The tracer confirms a valid
  path from S to T for that k.
- **C3 (Lemma B2).** For each pair with a B2 certificate, at least 1 sign has a
  solution that the tracer confirms. A candidate inside the window fails only
  by meeting a vertex.
- **C4 (Lemma C).** For each pair with a C certificate, each of the 4 sign
  pairs has a solution that the tracer confirms.
- **C5 (no false candidate).** Outside the B2 corner case, every candidate that
  meets the window conditions of its certificate traces to a valid path from S
  to T.
- **C6 (Theorem 2 on lattice points).** In population (a), every pair has a
  certificate.
- **C7 (L and L' on the open pairs, r = 3 and 4).** In population (b), every
  pair without a certificate is lit. The test shoots primitive directions
  (u, v) with |u| + |v| <= 40, then <= 400. This claim is a conjecture, not a
  theorem of this document.
- **C9 (Lemma D).** For each pair with a D certificate, shooting primitive
  directions finds a valid path. Lemma D has no fixed family of images, so the
  test shoots. This claim was added after the first run of population (b). It
  is tested by a second run on the same 100,000 rooms.
- **C8 (tracers agree).** On a sample of confirmed paths, the tracer of
  `verify.c`, the d8 tracer `tracer.py`, and the wall-by-wall ray caster
  `raycast.py` give the same verdict.

If a pair in C7 is undecided, the run stops, and the pair goes to a second
decider.

One run happened before this section existed: a first check of `verify.c` on
all rooms with at most 8 walls inside a 5 x 5 bounding box. It took under 2
seconds and reported no failure.

## Test and count results

All tests ran on 2026-11-09 with at most 3 worker processes. They used about
8 minutes of wall-clock time in total. The directory holds 56 MB.

| Test | Population | Pairs | Failures | Wall-clock |
| --- | --- | --- | --- | --- |
| First check, before the claims were written | 925 rooms, at most 8 walls, 5 x 5 box | 15,055 | 0 | 2 s |
| (a) Claims C1 to C6 | All 290,060 rooms with at most 8 walls in a 12 x 12 box | 356,724,940 | 0 | 10 s |
| (b) run 1, claims C1 to C5, C7 | 100,000 sampled rooms, 16 x 16 box | 417,791,881 | 0 | 200 s |
| (b) run 2, claim C9, same rooms | The same 100,000 rooms | 417,791,881 | 0 | 172 s |
| (b) run 3, same-class pairs only | The same 100,000 rooms | 102,776,263 | 0 | 15 s |
| C8, rooms with at most 8 walls, 6 x 6 box | 3,632 traced paths | | 0 after one fix | about 1 min |
| C8, 684 rooms of the sample | 3,934 traced paths | | 0 | 4 s |

One more run of population (b) was stopped after about 20 seconds, because
its path dumps were on course to exceed the output cap. Its output was
deleted.

**Test (a), pairs by lemma.** A: 318,714,484. A2: 226,512. B: 30,187,080.
B2: 1,698,840. C par: 1,646,568. C perp: 627,264. C same: 3,624,192. No pair
lacks a certificate. Every sign class of Lemmas B, B2, and C has a traced
solution for every pair. The largest path has unfolded length 219 in the
1-norm.

**Test (b), pairs by lemma (run 2).** A: 322,921,290. A2: 457,142.
B: 49,993,910. B2: 3,299,700. C par: 4,996,061. C perp: 818,851.
C same: 6,308,306. D: 174,530. No certificate: 28,822,091. The sample contains
all 70 order types with 10 walls and all 1,283 with 12 walls.

- Claims C1 to C5 hold on every pair. Every sign class has a traced solution.
  No candidate inside a window fails the tracer.
- Claim C3. The B2 corner case never occurs in these runs. That is expected:
  the search tries Lemma A first, and a viewer below the door height is in a
  common rectangle with the arm point. So both signs work in every B2 pair.
- Claim C7. Shooting lights all 28,996,621 pairs without a certificate in
  run 1, with |u| + |v| <= 40. No pair needs the second bound. No pair is
  dark or undecided, so no second decider ran.
- Claim C9. Shooting lights all 174,530 pairs with a D certificate.
- Classes. Run 3 has 7,234,054 same-class pairs without a certificate, all
  lit. So 21,588,037 different-class pairs without a certificate are lit.
- Claim C8. The first version of `raycast.py` tested vertices past the first
  wall hit. It reported 1 false mismatch in 14 paths. After the fix, all
  three tracers agree on 7,566 paths.

The tests use lattice points and integer lengths. The lemmas claim more: real
points and real lengths. The tests don't cover that part.

## Whether a step needs larger rooms

No step of the proofs for r <= 2 depends on a room size. The tests on larger
rooms were confirmation, and they are done. For r = 3 and r = 4, more testing
can't close the gap. The open pairs need new lemmas.

## Weakest step

The weakest step of the proved part is the link between `lemmas.py` and the
lemma hypotheses. Theorem 2 holds only if each certificate that the search
prints satisfies the hypotheses of its lemma for every room of the type.

- The 14 certificates at r = 2 that use Lemma B2 or C were printed and read
  against the shapes. Four were checked by hand in full: one each for the
  par, perp, and B2 forms, and the wide-neck Z.
- The 64 Lemma B certificates and 463 Lemma A certificates at r = 2 weren't
  read one by one.
- The tests support the link on lattice points. They can't show it for
  irrational points or lengths.

The weakest step of the mathematics is the jump argument in Lemma C. It was
checked twice by hand, and the tests found a solution in the open window for
every sign class of 18 million pairs.

For r = 3 and r = 4, the certificates for Lemma D come from code that no test
checks at the level of hypotheses. The test of claim C9 confirms only the
conclusion.

## Files

- `theorems.md`: this document.
- `enum_types.c`: order type enumerator. `types_r0.txt` to `types_r5.txt`: its
  output, one line `nx ny W mask` per type. `count_r6.txt`: the r = 6 count.
- `check_types.py`: brute-force count of order types for r <= 3.
- `lemmas.py`: certificate search. `run_cert.py`: driver.
  `cert_r0.json` to `cert_r4.json`: counts and open pairs per type.
  `old/`: the r = 3 and r = 4 tables from before Lemma D.
- `classify_gap.py`: link distance of the open pairs.
- `export_cert.py`, `verify.c`: the metric test. `verify2` is the binary that
  includes the Lemma D check.
- `sample_rooms.py`: the sampler for population (b). `runs/b_sample.txt`: the
  100,000 sampled rooms.
- `raycast.py`, `crosscheck.py`: the tracer comparison.
- `aggregate.py`: sums the test output. `runs/`: inputs, outputs, and timings.
