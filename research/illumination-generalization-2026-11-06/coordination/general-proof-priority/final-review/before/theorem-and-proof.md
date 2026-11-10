# Illumination of orthogonal rooms with at most eight walls

Draft for external mathematical review, 2026-11-08. This note proves that every
finite strictly simple orthogonal polygon with at most eight maximal walls
illuminates every pair of distinct interior points by a finite specular path
that avoids every corner. The argument is a case analysis over a finite
classification of such polygons. Each case gives an explicit path formula.

Provenance: the proofs below were written and cross-reviewed by AI agents
(Codex and Claude) in a shared research tree during 2026-11-01 to 2026-11-07.
Each piece has a pinned source file and an acceptance record; see
`dependency-manifest.json`. The packet author (Claude Fable) re-derived every
inequality by hand while writing this note. No step has been machine-verified
in a proof assistant, and no human mathematician has refereed it. The exact
checks listed in `reproduce.md` evaluate the formulas on fixed inputs; they
are controls, not proofs. see `cover-note.md`.

## 0. Conventions and statement

**Room.** A room is a compact region P in the plane whose boundary is a Jordan
polygon with every edge horizontal or vertical. "Strictly simple" means the
boundary polygon has no self-contact. Suppress every vertex with a straight
angle. The remaining vertices are the corners of P, and the edges between
consecutive corners are the maximal walls. W denotes the number of maximal
walls, which equals the number of corners. A corner is convex if the interior
angle is 90 degrees and reflex if it is 270 degrees.

**Interior point.** A point of the open set int(P). Points on an internal seam
used in a proof are interior points of P; points on a wall are not.

**Specular path.** Let S and T be distinct interior points. A specular path
from S to T is a finite polygonal line S = p_0, p_1, ..., p_n = T such that:

1. Every open segment (p_i, p_{i+1}) lies in int(P).
2. Every intermediate vertex p_i, 0 < i < n, lies in the relative interior of
   a maximal wall. In particular p_i is not a corner.
3. At every p_i, 0 < i < n, the direction obeys the reflection law: the
   velocity component normal to that wall reverses and the tangential
   component is unchanged.

The path may pass through S or T at an intermediate time. If it passes
through T at an intermediate time, truncating there gives a shorter path, so
this convention loses nothing. Direct visibility, n = 1, counts as a path.
"P illuminates (S, T)" means such a path exists.

**Folding maps.** For l > 0, F_l denotes the even, 2l-periodic triangular wave
with F_l(z) = |z| for |z| <= l. It satisfies F_l((2j+1)l + z) = l - |z| and
F_l(2jl + z) = |z| for |z| <= l and integers j. Unfolding a path that bounces
between the walls x = 0 and x = l of a vertical strip is the same as applying
F_l to a straight developed coordinate. Each crossing of a multiple of l is
one reflection on a vertical wall, and the two velocity formulas agree on
both sides of a fold, so condition 3 holds automatically at such a contact.

**Main theorem.** Let P be a room with W <= 8. Then P illuminates every pair
of distinct interior points.

The proof has seven parts. Section 1 classifies rooms with W <= 8 into six
metric normal forms. Sections 2 to 6 prove illumination for each form.
Section 7 assembles the theorem and lists the degeneracies that are covered
explicitly.

## 1. Classification of rooms with at most eight walls

**Proposition 1.1.** Let P be a room with W maximal walls, c convex corners,
and r reflex corners. Then c - r = 4 and c + r = W, so W is even. For W <= 8
the only possibilities are W = 4 (rectangle), W = 6 (one reflex corner), and
W = 8 (two reflex corners).

*Proof.* Traverse the boundary counterclockwise. Each convex corner turns the
tangent by +90 degrees and each reflex corner by -90 degrees. The total
turning of a simple closed curve is 360 degrees, so c - r = 4. The two
equations give r = (W - 4)/2, which is a nonnegative integer. The three cases
follow.

**Proposition 1.2 (normal forms).** After a Euclidean isometry, possibly
including a reflection, every room with W <= 8 is one of the following, with
all parameters arbitrary positive reals subject only to the displayed
inequalities. Conversely every parameter choice satisfying the inequalities
gives a room of the stated type.

- **Rectangle** (W = 4): [0, A] x [0, C] with A, C > 0.
- **L** (W = 6): P = ([0, A] x [0, c]) union ([0, a] x [c, C]) with
  0 < a < A and 0 < c < C.
- **U** (W = 8, reflex corners adjacent, k = 1): a, b, M, c > 0, H_L > c,
  H_R > c, A = a + M + b, with cyclic corners
  (0,0), (A,0), (A,H_R), (a+M,H_R), (a+M,c), (a,c), (a,H_L), (0,H_L).
- **Staircase** (W = 8, k = 2): 0 < a < b < A and 0 < c < d < H,
  P = ([0,A] x [0,c]) union ([0,b] x [c,d]) union ([0,a] x [d,H]),
  corners (0,0), (A,0), (A,c), (b,c), (b,d), (a,d), (a,H), (0,H).
- **T with independent floor heights** (W = 8, k = 3): 0 < a < b < A and
  0 < u, v < C,
  P = ([0,a] x [u,C]) union ([a,b] x [0,C]) union ([b,A] x [v,C]),
  corners (a,0), (b,0), (b,v), (A,v), (A,C), (0,C), (0,u), (a,u).
- **Wide-middle offset corridor** (W = 8, k = 4): 0 < a, B < A and
  0 < b < c < C,
  P = ([0,B] x [0,b]) union ([0,A] x [b,c]) union ([a,A] x [c,C]),
  corners (0,0), (B,0), (B,b), (A,b), (A,C), (a,C), (a,c), (0,c).
  The order of a and B is unrestricted. If a > B the two outer arms have
  disjoint horizontal projections.

Here k is the shorter cyclic distance, in edges, between the two reflex
corners.

*Proof.* W = 4 forces a rectangle. For W = 6 there is one reflex corner; the
turn word is one minus sign and five plus signs, which fixes the eight edge
directions up to rotation and reflection. Positivity of the six edge lengths
with two closure relations leaves four free parameters, and the displayed L
realizes all of them.

For W = 8 there are two reflex corners among eight cyclic positions. Their
shorter cyclic distance k is 1, 2, 3, or 4. A cyclic relabeling and, if
needed, a reflection of the plane place the shorter arc first. Once k is
fixed and the first edge direction is fixed, the six plus and two minus turns
determine the entire edge-direction sequence. So each k has exactly one turn
word up to these operations. For each word, the eight edge lengths satisfy
two closure relations and leave six free parameters. The displayed vertex
lists realize them:

- k = 1: directions R, U, L, D, L, U, L, D with lengths
  A, H_R, b, H_R - c, M, H_L - c, a, H_L. Positivity gives a, b, M > 0 and
  H_L, H_R > c > 0. Horizontal closure is A = a + M + b.
- k = 2: directions R, U, L, U, L, U, L, D with lengths
  A, c, A - b, d - c, b - a, H - d, a, H. Positivity gives exactly
  0 < a < b < A and 0 < c < d < H.
- k = 3: directions R, U, R, U, L, D, R, D with lengths
  b - a, v, A - b, C - v, A, C - u, a, u. Positivity gives exactly
  0 < a < b < A and 0 < u, v < C. No relation between u and v follows.
- k = 4: directions R, U, R, U, L, D, L, D with lengths
  B, b, A - B, C - b, A - a, C - c, a, c. Positivity gives exactly
  0 < a, B < A and 0 < b, c < C.

For k = 1, 2, 3 every positive parameter choice is strictly simple, because
each displayed region is a union of axis-parallel rectangles glued along
seams of positive length whose closure boundary is one Jordan curve. For
k = 4 the non-adjacent edges x = B (0 <= y <= b) and y = c (0 <= x <= a)
intersect if and only if B <= a and c <= b. The opposite pair y = b
(B <= x <= A) and x = a (c <= y <= C) intersects under the same condition.
Every other non-adjacent pair has disjoint coordinate ranges. So the k = 4
polygon is strictly simple if and only if a < B or b < c. If b >= c, then
a < B holds, and the reflection across the line x = y gives new parameters
A' = C, B' = c, a' = b, b' = a, c' = B, C' = A with b' < c'. So the normal
form with b < c covers every strictly simple k = 4 room. This proves the
proposition.

The prescribed check `eight-wall-turn-check.py` enumerates the 28 labeled
reflex-corner positions and verifies one representative polygon per class.
That is a control on the combinatorics; the proof is the paragraph above.

## 2. Rectangles and L rooms

Two interior points of a rectangle see each other directly. The L room needs
the following theorem, which is used again in every eight-wall case.

**Theorem 2.1 (L, two orientations).** Let P = ([0,A] x [0,c]) union
([0,a] x [c,C]) with 0 < a < A and 0 < c < C, and let s, t be distinct
interior points. There is a specular path from s to t that reflects only on
vertical walls and whose y coordinate is monotone. There is also one that
reflects only on horizontal walls and whose x coordinate is monotone. A
direct segment counts as both.

*Proof.* P is the union of the convex rectangles R_1 = [0,A] x [0,c] and
R_2 = [0,a] x [0,C]. If s and t lie in a common R_i, the segment between them
lies in that rectangle. Interior points of P on the seam y = c (0 < x < a) or
on the line x = a (0 < y < c) belong to both rectangles, so the segment lies
in int(P) except for its endpoints. This covers every placement except, after
relabeling,

    s = (x_s, y_s) with a < x_s < A, 0 < y_s < c,
    t = (x_t, y_t) with 0 < x_t < a, c < y_t < C.

Write D_s = c - y_s > 0, D_t = y_t - c > 0, r = D_t / D_s. The images of x_t
under the reflections of the upper strip [0,a] form

    E = { e x_t + 2ma : e in {+1,-1}, m in Z }.

E is symmetric under negation. Its consecutive gaps alternate between 2x_t
and 2(a - x_t); both are strictly less than 2a.

Put h = -r x_s and choose x in E with 0 < |x - h| <= a. Such x exists: if h
is not in E, the nearest point of E is at distance less than a; if h is in E,
its nearer neighbor is at distance 2 min(x_t, a - x_t) <= a.

If x > h set X_s = x_s, X_t = x; if x < h set X_s = -x_s, X_t = -x. In both
cases X_t is in E. The straight developed segment from (X_s, y_s) to
(X_t, y_t) crosses y = c at

    q = (r X_s + X_t)/(1 + r) = |x - h|/(1 + r),

so 0 < q <= a/(1+r) < a. The crossing is strictly inside the open seam.

Fold the segment into P. Below y = c the developed x runs from X_s to q and
stays in (-A, A). If X_s = x_s there is no reflection. If X_s = -x_s the
segment crosses x = 0 exactly once, at a height strictly between y_s and c;
reflecting the negative part in x = 0 gives one smooth contact on the wall
x = 0. Above y = c apply F_a. The portal value q is fixed because 0 < q < a,
and the final value is F_a(X_t) = x_t. Each crossing of a multiple of a is
one reflection on x = 0 or x = a, at a height strictly between c and y_t < C,
so never at a corner. The developed segment is finite, so there are finitely
many folds. The y coordinate increases strictly, so no horizontal wall is
touched, and the seam crossing at (q, c) is an interior point. This is the
vertical-only path.

Exchanging the coordinates maps P to an L of the same form with parameters
(A', a', c', C') = (C, c, a, A). The construction gives a path from t to s
whose original x coordinate is monotone and which reflects only on horizontal
walls. Reverse it.

**Lemma 2.2 (source on the base).** In the L of Theorem 2.1 let the source be
(x, 0) with 0 < x < A on the base and the target (t, y) with 0 < t < a and
c < y < C. Then there is a vertical-only specular path from (x, 0) to (t, y)
whose y coordinate increases strictly, with no contact on the base after the
starting point.

*Proof.* If x <= a, the segment lies in the column [0,a] x [0,C]; after its
start its x coordinate is strictly less than a when x = a, because t < a. If
a < x < A, repeat the proof of Theorem 2.1 with y_s = 0: r = (y - c)/c, h =
-r x, choose x' in E with 0 < |x' - h| <= a, and q = |x' - h|/(1+r) in (0, a).
The lower fold crosses x = 0 at most once, at a height strictly between 0 and
c. Everything else is unchanged. The source height was used in Theorem 2.1
only to make the source interior, not in any inequality.

Lemma 2.2 is used where a base of an L subroom is an internal seam of a
larger room, so that (x, 0) is an interior point of that room. It never
admits a boundary point of the actual room as an endpoint.

**Corollary 2.3.** Every L room illuminates every pair of distinct interior
points.

## 3. U rooms (k = 1)

Fix a, b, M, c > 0, H_L, H_R > c, A = a + M + b, and the U room of
Proposition 1.2. The left arm is [0,a] x [0,H_L], the right arm is
[a+M, A] x [0,H_R], and the bottom rectangle is [0,A] x [0,c]. Interior
points on the level y = c have 0 < x < a or a + M < x < A.

**Theorem 3.1 (opposite arms).** Let s = (x_s, y_s) with 0 < x_s < a and
c <= y_s < H_L, and t = (a + M + x_t, y_t) with 0 < x_t < b and
c <= y_t < H_R. There is a specular path from s to t that reflects exactly
once on the floor y = 0, at a point with x in (M/2, A - M/2), and otherwise
only on vertical walls.

*Proof.* Step 1, arm lengths. For tau > 0 define

    L_n = a - x_s + 2na,   R_m = x_t + 2mb,   n, m >= 0,
    L(tau) = the first L_n strictly greater than (y_s - c) tau,
    R(tau) = the first R_m strictly greater than (y_t - c) tau.

Both are nondecreasing, right-continuous step functions of tau. Put

    l_s = L(tau) - (y_s - c) tau in (0, 2a],
    l_t = R(tau) - (y_t - c) tau in (0, 2b].

A remainder equals its upper bound exactly at a jump of its step function.
If y_s = c then L is the constant L_0 = a - x_s and l_s = a - x_s; likewise
for y_t = c.

Step 2, a fixed point. Choose tau_0 > 2 max(a, b)/c and an integer k >= 0
with B = M + 2kA > 2c tau_0. Put Sigma = y_s + y_t and

    H(tau) = (L(tau) + R(tau) + B)/Sigma.

Then Sigma tau - L(tau) - R(tau) = 2c tau - l_s - l_t, so H(tau) > tau if and
only if B + l_s + l_t > 2c tau. This holds at tau_0. H is nondecreasing, so
the iterates tau_{j+1} = H(tau_j) are nondecreasing. They are bounded by
tau_max = (B + 2a + 2b)/(2c), because 2c tau_max >= B + l_s + l_t gives
H(tau_max) <= tau_max. On [tau_0, tau_max] only finitely many values of
(L, R) occur, so the iteration is stationary after finitely many steps. Let
tau_n be the first stationary iterate; n >= 1 and tau_n > tau_{n-1}.

The fixed point is not a jump of L. If it were, then L(tau_{n-1}) <=
L(tau_n) - 2a and R(tau_{n-1}) <= R(tau_n), so H(tau_{n-1}) < H(tau_n) =
tau_n, contradicting tau_n = H(tau_{n-1}). The same argument applies to R.
Hence at tau = tau_n one has 0 < l_s < 2a and 0 < l_t < 2b, together with the
fixed-point relation Sigma tau = L + R + B, which is equivalent to

    2c tau = B + l_s + l_t.                                   (3.1)

Step 3, portals. Define the portal heights

    u = y_s - L/tau = c - l_s/tau,   v = y_t - R/tau = c - l_t/tau.

Since tau > tau_0 > 2 max(a,b)/c, both lie in (0, c). From (3.1),
u + v = B/tau.

Step 4, the left arm. From s travel with velocity (1, -1/tau) in the
developed left strip and fold with F_a. The developed horizontal distance
to the exit is L = a - x_s + 2n'a for some n' >= 0, so the path reaches
x = a moving right after n' full round trips, at height u. Every earlier contact with x = a is
at least 2a developed units before the exit, at height at least
u + 2a/tau = c + (2a - l_s)/tau > c. Every contact with x = 0 is at a height
strictly between u and y_s. All these contacts are on the walls x = 0
(0 < y < H_L) and x = a (c < y < H_L), at heights strictly below y_s < H_L
and strictly above c, so none is a corner and the roof is never touched.
When y_s = c, the path goes directly from s to (a, u) with no contact. The
path leaves the left arm through the open passage {a} x (0, c) at (a, u),
moving right and down.

Step 5, the bottom strip. For developed distance 0 <= d <= B from (a, u),
set X(d) = a + d, Y(d) = u - d/tau, and take the physical point
(F_A(X(d)), |Y(d)|). Since a + B = a + M + 2kA and 2kA is an even multiple
of A, F_A(a + B) = a + M, and after 2k vertical folds the horizontal
velocity is again positive. The developed height at d = B is
u - B/tau = -v, so the physical endpoint is (a + M, v) moving right and up.
Y vanishes exactly once, at d_0 = u tau, where the developed coordinate is

    X_0 = a + u tau = a + c tau - l_s = a + (B + l_s + l_t)/2 - l_s
        = a + M/2 + kA + (l_t - l_s)/2.

Since -a < (l_t - l_s)/2 < b, X_0 lies strictly between kA + M/2 and
kA + A - M/2, so X_0 is not a multiple of A and the physical floor contact
F_A(X_0) lies in (M/2, A - M/2). It is a smooth point of the floor, at which
the vertical velocity reverses and the horizontal velocity is unchanged.
Every vertical-wall contact in the strip is at developed X in A Z, hence at
nonzero height |Y| <= max(u, v) < c, on the walls x = 0 or x = A below the
level c. So the strip path stays in the bottom rectangle below y = c, avoids
the notch wall y = c and both inner walls, and touches no corner.

Step 6, the right arm. The mirror image of Step 4 carries the path from
(a + M, v), moving right and up, through developed distance R = x_t + 2mb to
t. Earlier contacts with x = a + M are at heights above c, and contacts with
x = A are at heights strictly between v and y_t < H_R.

At both portals the arm formula and the strip formula are the same affine
function folded by compatible maps, so positions and velocities match. All
contacts are ordinary reflections, there are finitely many of them, and the
path ends at t.

**Theorem 3.2.** Every U room illuminates every pair of distinct interior
points.

*Proof.* Classify the two points. If both lie in one arm column
[0,a] x (0,H_L) or (a+M, A) x (0,H_R), they see each other. If at least one
point has y < c and both have y <= c, both lie in the bottom rectangle and the
segment between them is interior, because a point with y = c is interior only
over an open mouth. If both have y = c and lie over opposite mouths, Theorem
3.1 applies with y_s = y_t = c. If both have y > c and lie in different arms,
Theorem 3.1 applies. The remaining case is one point with y > c in one
arm, say the left, and the other with y < c. Then both are interior points of
the L subroom Q = ([0,A] x [0,c]) union ([0,a] x [c,H_L]). Every vertical
wall of Q is a wall of P. The only part of the boundary of Q that is not on
the boundary of P is the segment y = c, a + M < x < A, which contains the
reflex corner (a + M, c) of P as a smooth point. The vertical-only path of
Theorem 2.1 touches no horizontal wall of Q, so it is a specular path in P.
The case of the right arm is symmetric.

## 4. T rooms with independent floor heights (k = 3)

Fix 0 < a < b < A, 0 < u, v < C, and
P = ([0,a] x [u,C]) union ([a,b] x [0,C]) union ([b,A] x [v,C]).

**Theorem 4.1.** P illuminates every pair of distinct interior points.

*Proof.* Assign each interior point to the left wing (x <= a), the stem
(a < x < b), or the right wing (x >= b). An interior point with x = a has
y > u and one with x = b has y > v.

Two points in one class see each other, because each class lies in a convex
rectangle contained in P: [0,a] x [u,C], [a,b] x [0,C], or [b,A] x [v,C]. A
segment along x = a or x = b has both endpoint heights above the
corresponding floor and is interior.

Stem and left wing. Use the L subroom

    Q_L = ([0,b] x [u,C]) union ([a,b] x [0,u]).

After the isometry (x, y) -> (b - x, C - y) it has the form of Theorem 2.1.
Both points are interior to Q_L, including a left-wing point on x = a. Take
the horizontal-only path. The horizontal walls of Q_L, namely y = C over
[0,b], y = u over [0,a], and y = 0 over [a,b], are walls of P. The vertical
boundary x = b of Q_L is partly artificial (v < y < C) and contains the reflex
corner (b, v) of P as a smooth point; the chosen path never touches a vertical
wall. So it is a specular path in P. Stem and right wing use
Q_R = ([a,A] x [v,C]) union ([a,b] x [0,v]) in the same way.

Opposite wings. Reflect across a vertical line if needed so that u <= v. Let
S = (x_s, y_s) with 0 < x_s <= a, u < y_s < C, and T = (x_t, y_t) with
b <= x_t < A, v < y_t < C. If y_s >= v the segment lies in the rectangle
[0,A] x [v,C]; its open part has y > v because y_t > v. Otherwise
u < y_s < v. Use the L subroom

    Q = ([0,A] x [v,C]) union ([0,b] x [u,v]),

which after y -> C - y has the form of Theorem 2.1. Both points are interior
to Q. Its vertical walls x = 0 (u <= y <= C), x = A (v <= y <= C), and x = b
(u <= y <= v) are walls of P. Its only artificial boundary is y = u over
(a, b), which contains the reflex corner (a, u) as a smooth point. The
vertical-only path of Theorem 2.1 touches no horizontal wall, so it is a
specular path in P. The case u > v is the mirror image.

These cases exhaust all placements, including every seam and floor-level
equality.

The equal-floor T room (u = v) is a special case of Theorem 4.1.

## 5. Wide-middle offset corridors (k = 4)

Fix 0 < a, B < A, 0 < b < c < C, and
P = ([0,B] x [0,b]) union ([0,A] x [b,c]) union ([a,A] x [c,C]).
Write W = A - a and g = c - b. Interior points on the seam y = b have
0 < x < B; interior points on the seam y = c have a < x < A.

**Theorem 5.1 (opposite arms).** Let S = (x_s, y_s) with 0 < x_s < B,
0 < y_s < b, and T = (x_t, y_t) with a < x_t < A, c < y_t < C. There is a
specular path from S to T with strictly increasing y coordinate that reflects
only on vertical walls.

*Proof.* Step 1, reduction to B >= W. Rotating P by 180 degrees about its
center gives a room of the same form with the roles of B and W exchanged and
g unchanged. The rotation exchanges S and T and preserves specular paths. So
assume B >= W.

Step 2, windows. Put H_s = b - y_s, H_t = y_t - c, D = H_s + g + H_t. Choose
an integer k >= 0 so large that, with K = (2k+1)A,

    (H_s K + g x_s)/(2Bg) >= 1,

and let n be a nearest integer to this quantity; then n >= 1 and

    |g theta - K| <= Bg/H_s,   where theta = (2nB - x_s)/H_s.            (5.1)

The slopes tau for which the developed point z = x_s + H_s tau - 2nB lies in
(-B, B) form the open interval I = ((2nB - x_s - B)/H_s, (2nB - x_s + B)/H_s),
which is entirely positive since n >= 1 and x_s < B. The affine map
U(tau) = x_s + (H_s + g) tau - 2nB sends I onto (g theta - R, g theta + R)
with R = B(H_s + g)/H_s. By (5.1) and B >= W,

    |K - g theta| + W <= Bg/H_s + W <= R,

so the open window (K - W, K + W) lies inside U(I). Its preimage

    J = ((2nB + K - x_s - W)/(H_s + g), (2nB + K - x_s + W)/(H_s + g))

is a nonempty open subinterval of I. For every tau in J,

    |z| < B,   z = x_s + H_s tau - 2nB,                               (5.2)
    |w| < W,   w = x_s + (H_s + g) tau - 2nB - K.                     (5.3)

Step 3, the target image. Put Y = A - x_t, so 0 < Y < W. On J the affine
coordinate Z(tau) = x_s + D tau - 2nB - K = w + H_t tau runs over an open
interval (Z_lo, Z_hi) of length 2W D/(H_s + g) > 2W. The points Y + 2mW have
spacing 2W, so one lies strictly inside: with m = floor((Z_lo - Y)/(2W)) + 1,
Z_lo < Y + 2mW <= Z_lo + 2W < Z_hi. Fix

    tau = (2nB + K + Y + 2mW - x_s)/D,

which lies in J and satisfies F_W(Z(tau)) = Y.

Step 4, the path. For y_s <= y <= y_t set

    x(y) = F_B(x_s + tau (y - y_s)),              y_s <= y <= b,
    x(y) = F_A(z + tau (y - b)),                  b <= y <= c,
    x(y) = A - F_W(w + tau (y - c)),              c <= y <= y_t.

At y = b the lower expression equals F_B(2nB + z) = |z| and the middle one
equals F_A(z) = |z| because |z| < B < A; near y = b both are the same function
|z + tau (y - b)|. At y = c the middle argument is K + w with K an odd
multiple of A and |w| < W < A, so F_A(K + w) = A - |w|, which is the upper
expression. Positions and velocities therefore match at both seams, including
the cases z = 0 and w = 0, which are single smooth contacts with the walls
x = 0 and x = A respectively.

The contacts of the lower piece are on x = 0 or x = B at heights in
(y_s, b); the seam point (|z|, b) avoids the reflex corner (B, b) by (5.2).
The contacts of the middle piece are on x = 0 or x = A at heights in (b, c).
The seam point (A - |w|, c) satisfies a < A - |w| < A by (5.3), so it avoids
the reflex corner (a, c) and the convex corner (0, c). The contacts of the
upper piece are on x = a or x = A at heights in (c, y_t), below C. The final
point is (A - F_W(Z(tau)), y_t) = (x_t, y_t) = T. The y coordinate increases
strictly, so no horizontal wall is touched and T is reached first at its own
height. Every horizontal velocity is +tau or -tau and every vertical velocity
is 1, so each fold is an ordinary reflection, and there are finitely many.

**Theorem 5.2.** P illuminates every pair of distinct interior points.

*Proof.* The subrooms

    Q_low = ([0,B] x [0,b]) union ([0,A] x [b,c]),
    Q_up  = ([0,A] x [b,c]) union ([a,A] x [c,C])

are L rooms up to isometry. All vertical walls of Q_low are walls of P; its
only artificial boundary is y = c over (a, A), which contains the reflex
corner (a, c) as a smooth point. All vertical walls of Q_up are walls of P;
its only artificial boundary is y = b over (0, B), which contains (B, b) as a
smooth point. A vertical-only path of Theorem 2.1 in either subroom is a
specular path in P.

If both points have y < c they are interior to Q_low. If both have y > b
they are interior to Q_up. Otherwise one point P_1 has y <= b and the other
P_2 has y >= c. Four subcases:

- P_1 in the open lower arm and P_2 in the open upper arm: Theorem 5.1.
- P_1 on the seam y = b and P_2 on the seam y = c: the segment lies in the
  middle rectangle with its open part strictly between the seams and with
  0 < x < A, so it is interior.
- P_1 in the open lower arm and P_2 = (x_2, c) on the upper seam with
  a < x_2 < A: apply the map y -> c - y to Q_low. It becomes an L of the form
  of Theorem 2.1 with lower rectangle [0,A] x [0,g] and upper rectangle
  [0,B] x [g,c], P_2 becomes the base point (x_2, 0) with 0 < x_2 < A, and
  P_1 becomes an interior point of the upper rectangle. Lemma 2.2 gives a
  vertical-only path whose contacts are on x = 0 or x = A at P heights in
  (b, c) and on x = 0 or x = B at P heights in (y_1, b). Reverse it.
- P_1 = (x_1, b) on the lower seam with 0 < x_1 < B and P_2 in the open upper
  arm: apply (x, y) -> (A - x, y - b) to Q_up. It becomes an L with lower
  rectangle [0,A] x [0,g] and upper rectangle [0,W] x [g, C - b], P_1 becomes
  the base point (A - x_1, 0) with 0 < A - x_1 < A, and P_2 an interior point
  of the upper rectangle. Lemma 2.2 applies.

These cases exhaust all placements.

## 6. Staircases (k = 2)

Fix 0 < a < b < A, 0 < c < d < H, and
P = ([0,A] x [0,c]) union ([0,b] x [c,d]) union ([0,a] x [d,H]).
Write g = d - c and h = H - d. Interior points on the seam y = c have
0 < x < b; interior points on the seam y = d have 0 < x < a. The points
(x, c) with b <= x <= A and (x, d) with a <= x <= b are on walls.

This is the only class whose proof needs a case split on the metric. Four
sufficient conditions on the six parameters are proved to cover every pair
(Sections 6.3 and 6.4), and Section 6.5 proves that every parameter choice
satisfies at least one of them.

### 6.1 Placements reduce to the cross placement

**Lemma 6.1.** Let S, T be distinct interior points of P. Then one of the
following holds:

1. Both have y < d, and both are interior points of the L room
   Q_low = ([0,A] x [0,c]) union ([0,b] x [c,d]).
2. Both have x < b, and both are interior points of the L room
   Q_up = ([0,b] x [0,d]) union ([0,a] x [d,H]).
3. After relabeling, S = (x_s, y_s) with b <= x_s < A and 0 < y_s < c, and
   T = (x_t, y_t) with 0 < x_t < a and d <= y_t < H.

In cases 1 and 2, P illuminates (S, T).

*Proof.* If neither 1 nor 2 holds, one point has y >= d, hence x < a < b, and
one point has x >= b, hence y < c (a point with x >= b and y = c is on a
wall). These are different points, giving case 3. In case 1, every vertical
wall of Q_low is a wall of P, and its only artificial boundary is y = d over
(0, a), which contains the reflex corner (a, d) as a smooth point. The
vertical-only path of Theorem 2.1 is a specular path in P. In case 2, every
horizontal wall of Q_up is a wall of P, and its only artificial boundary is
x = b over (0, c), which contains (b, c) as a smooth point. The horizontal-only
path of Theorem 2.1 is a specular path in P.

The cross placement 3 deliberately includes the two equalities x_s = b and
y_t = d. For it, write

    H_s = c - y_s > 0,   H_t = y_t - d >= 0,   T_0 = H_s + g.

### 6.2 Window lemmas

Both staircase charts start by passing the two reflex corners with strict
margins. The following two lemmas supply the slope windows.

**Lemma 6.2 (nested windows).** Let x_s, H_s, g, a, b, A be as in the cross
placement, except that H_s > 0 may be any positive number, and let
rho = g/H_s. Suppose rho <= (b - a)/(A - b). Choose an even multiple K = 2kb
of b so large that (H_s K + g x_s)/(2Ag) >= 1, and let n be a nearest integer
to that quantity. Then n >= 1, and every tau in the nonempty open interval

    J = ((2nA + K - x_s - a)/(H_s + g), (2nA + K - x_s + a)/(H_s + g))

is positive and satisfies

    |z| < b,   z = x_s + H_s tau - 2nA,                                (6.1)
    |w| < a,   w = x_s + (H_s + g) tau - 2nA - K.                      (6.2)

*Proof.* Put theta = (2nA - x_s)/H_s. Nearest-integer rounding gives
|g theta - K| <= Ag/H_s = A rho. The slopes with |z| < b form the positive
interval I = ((2nA - x_s - b)/H_s, (2nA - x_s + b)/H_s), and
U(tau) = x_s + (H_s + g) tau - 2nA maps I onto (g theta - R, g theta + R)
with R = b(H_s + g)/H_s = b + b rho. The window (K - a, K + a) lies inside
U(I) because |K - g theta| + a <= A rho + a <= b + b rho = R, where the last
inequality is rho (A - b) <= b - a. J is the preimage of that window, so
(6.2) holds on J, and J is a subset of I, so (6.1) holds on J.

**Lemma 6.3 (partial window).** In the cross placement put n = 1,
theta = (2A - x_s)/H_s, and let K be a nearest nonnegative even multiple of b
to g theta. Then there is a nonempty open interval J of positive slopes on
which (6.1) and (6.2) hold with this K and n = 1, and such that
U(J) = (K - a, K + a) intersect U(I) has length

    ell >= min(2a, a + bg/H_s) > a.                                  (6.3)

*Proof.* With R = b + bg/H_s and delta = |K - g theta| <= b, K lies strictly
inside U(I) = (g theta - R, g theta + R) and R > b > a. Both ends of
(K - a, K + a) cannot be clipped, since that needs 2a > 2R. If one end is
clipped the overlap has length R + a - delta >= R + a - b = a + bg/H_s;
otherwise it is 2a.

In both lemmas the first portal contact (|z|, c) has |z| < b, so it avoids
the reflex corner (b, c), and the second portal contact (|w|, d) avoids the
reflex corner (a, d). The values z = 0 and w = 0 are smooth contacts with
the wall x = 0.

**Lemma 6.4 (seams match).** For tau satisfying (6.1) and (6.2) with K an
even multiple of b, define on [y_s, c], [c, d], and [d, eta_1] respectively

    x = F_A(x_s + tau (y - y_s)),   x = F_b(z + tau (y - c)),
    x = F_a(w + tau (y - d)).

Then positions and velocities agree at y = c and at y = d, every contact of
the first two pieces is an ordinary reflection on a wall of P at a non-corner
point, and the first two pieces touch no horizontal wall.

*Proof.* At y = c the first expression is F_A(2nA + z) = |z| and the second
is F_b(z) = |z| because |z| < b; near c both equal |z + tau (y - c)|. At
y = d the second expression is F_b(K + w) = |w| because K is an even multiple
of b and |w| < a < b, and the third is F_a(w) = |w|. The contacts of the first
piece are on x = 0 or x = A at heights in (y_s, c); those of the second piece
are on x = 0 or x = b at heights in (c, d). The seam points avoid the reflex
corners by (6.1) and (6.2), and (0, c), (0, d) are not corners. The height
increases strictly on these pieces.

### 6.3 Floor chart: conditions F and Ft

    (A - b)(d - c) <= c(b - a),                                       (F)
    (H - d)(b - a) <= a(d - c).                                       (Ft)

**Theorem 6.5.** If F holds, P illuminates every cross placement with
y_t > d.

*Proof.* Reflect the source in the floor to (x_s, -y_s), and set
H_s' = c + y_s, D = H_s' + g + H_t with H_t > 0. Since H_s' > c,
rho' = g/H_s' < g/c <= (b - a)/(A - b) by F. Lemma 6.2 with H_s' in place of
H_s gives K = 2kb, n >= 1, and the interval J on which (6.1) and (6.2) hold
with z = x_s + H_s' tau - 2nA and w = x_s + (H_s' + g) tau - 2nA - K.

On J the coordinate Z(tau) = x_s + D tau - 2nA - K runs over an open interval
(Z_lo, Z_hi) of length 2a D/(H_s' + g) > 2a. The target images
E = {e x_t + 2ma} have consecutive gaps less than 2a, so (Z_lo, Z_hi)
contains two consecutive images Y_1 < Y_2 with 0 < Y_2 - Y_1 < 2a. Let
tau_1 < tau_2 be their slopes in J. The developed horizontal coordinate of
the floor contact is Lambda(tau) = x_s + y_s tau, and

    0 < Lambda(tau_2) - Lambda(tau_1) = y_s (Y_2 - Y_1)/D < 2a y_s/D < a < A,

because D > c + y_s > 2 y_s. Two numbers less than A apart cannot both be
multiples of A. Choose the index i with Lambda(tau_i) not in A Z and write
tau = tau_i, Y = Y_i.

Path. For -y_s <= q <= c set x(q) = F_A(x_s + tau (q + y_s)) and
y(q) = |q|; for c <= q <= d and d <= q <= y_t use the second and third
formulas of Lemma 6.4. The piece before q = 0 descends from y_s to 0 with
contacts on x = 0 or x = A at heights in (0, y_s). At q = 0 the contact is on
the floor at x = F_A(Lambda(tau)), strictly between 0 and A, so it is a
smooth floor reflection: the vertical velocity reverses and the horizontal
velocity is unchanged. After q = 0 the height increases strictly, with
contacts at heights in (0, c) on x = 0 or x = A. Lemma 6.4 handles both
seams. The contacts of the third piece are on x = 0 or x = a at heights in
(d, y_t), below H. The endpoint is (F_a(Y), y_t) = (x_t, y_t). The path never
touches the roof or a ledge, has finitely many contacts, and reaches T.

**Theorem 6.6.** If F holds, P illuminates every cross placement with
y_t = d.

*Proof.* Here T = (x_t, d) with 0 < x_t < a. If x_s = b the segment from S to
T has x < b at every point after S, so it lies in Q_up's column
[0,b] x [0,d] and is interior. If x_s > b, apply the proof of Theorem 2.1 in
the L room Q_low with the target on the top of its narrow arm: r = g/H_s,
h = -r x_s, choose x' in {e x_t + 2mb} with 0 < |x' - h| <= b, and the seam
crossing q = |x' - h|/(1 + r) lies in (0, b). The upper fold F_b ends at
F_b(x') = x_t, which is not 0 or b, so every upper contact is on x = 0 or
x = b at a height strictly between c and d. Lower contacts are at heights in
(y_s, c). The path ends at T, an interior point of P on the seam, and avoids
(a, d) because x_t < a. This argument does not use F.

**Corollary 6.7.** If F holds, P illuminates every pair of distinct interior
points. If Ft holds, the same is true.

*Proof.* Lemma 6.1 and Theorems 6.5 and 6.6 cover F. Exchanging the
coordinates maps the staircase with parameters (A, b, a; c, d, H) to the
staircase with parameters (H, d, c; a, b, A), which carries F to Ft.
Transposition is an isometry and preserves specular paths.

### 6.4 Roof chart: conditions Rv and Rh

    Q_v = min(2, 1 + b(d - c)/(ac)),   (H/d) Q_v >= 2,                  (Rv)
    Q_h = min(2, 1 + d(b - a)/(ca)),   (A/b) Q_h >= 2.                  (Rh)

**Theorem 6.8.** If Rv holds, P illuminates every cross placement,
including y_t = d.

*Proof.* Step 1, the slope. Apply Lemma 6.3 and let J be its interval, with
K an even multiple of b and n = 1. Put v = 2h - H_t and D = T_0 + v. Since
0 <= H_t < h, one has h < v <= 2h. On J the coordinate

    Z(tau) = x_s + D tau - 2A - K = w + v tau

runs over an open interval of length L = ell D/T_0. Since H_s < c one has
T_0 < d and, by (6.3), ell >= a min(2, 1 + bg/c) = a Q_v. Hence

    L = ell (1 + v/T_0) > a Q_v (1 + h/d) = a Q_v H/d >= 2a

by Rv. The target images E = {e x_t + 2ma} have gaps less than 2a, so one
image Y lies strictly inside the interval. Fix the slope tau in J with
Z(tau) = Y.

Step 2, the upper piece. Use the developed height eta as parameter. For
d <= eta <= d + v set

    x(eta) = F_a(w + tau (eta - d)),   y(eta) = d + F_h(eta - d).

Since h < v <= 2h, the height rises from d to H at eta = d + h, then falls to
d + (2h - v) = y_t at eta = d + v. The final x is F_a(Z(tau)) = x_t. Let
Beta = w + tau h be the developed x coordinate at the roof.

Step 3, the roof contact is ordinary unless Beta is in a Z. If Beta is not a
multiple of a, the roof contact is at (F_a(Beta), H) with 0 < F_a(Beta) < a,
a smooth point of the roof, and it does not coincide with a vertical fold.
There the vertical velocity reverses and the horizontal velocity is unchanged.
All other contacts of the upper piece are on x = 0 or x = a, at heights
strictly between d and H on the way up and strictly between y_t and H on the
way down. The point (a, d) is avoided by (6.2). So the whole path, assembled
by Lemma 6.4, is a specular path from S to T.

Step 4, earlier arrival when Beta is in a Z. Suppose Beta = ja for an integer
j. F_a is even and 2a-periodic, and 2Beta = 2ja is a period, so for every
real sigma

    F_a(Beta - sigma) = F_a(sigma - Beta) = F_a(sigma + Beta).

Take sigma = tau (H - y_t). Then Beta - sigma = w + tau H_t and
Beta + sigma = w + tau v = Z(tau), so

    x(y_t on the way up) = F_a(w + tau H_t) = F_a(Z(tau)) = x_t.

So the path is already at T at developed height eta = y_t, on the way up,
before the roof. Truncate there. The truncated path consists of the two
lower pieces and the part of the upper piece with d <= eta <= y_t; its upper
contacts are on x = 0 or x = a at heights strictly between d and y_t, and the
endpoint (x_t, y_t) has 0 < x_t < a, so it is not a wall contact. If y_t = d,
then H_t = 0 and the identity gives |w| = x_t, so the second piece already
ends at T = (x_t, d) and the upper piece is dropped. In every case the
truncated path is a specular path from S to T that never reaches the roof.

**Corollary 6.9.** If Rv holds, P illuminates every pair of distinct interior
points. If Rh holds, the same is true.

*Proof.* Lemma 6.1 and Theorem 6.8 cover Rv. Transposition carries Rv to Rh,
because it maps (A, b, a; c, d, H) to (H, d, c; a, b, A), which sends
b(d - c)/(ac) to d(b - a)/(ca) and H/d to A/b.

### 6.5 Every staircase satisfies F, Ft, Rv, or Rh

**Proposition 6.10.** For all 0 < a < b < A and 0 < c < d < H, at least one
of F, Ft, Rv, Rh holds.

*Proof.* Put alpha = a/b, beta = c/d, p = alpha beta, lambda = A/b,
mu = H/d, s = alpha + beta. Then 0 < alpha, beta, p < 1 and lambda, mu > 1.
In these variables

    b(d - c)/(ac) = (1 - beta)/p,   d(b - a)/(ca) = (1 - alpha)/p,
    F  <=> (lambda - 1)(1 - beta) <= beta (1 - alpha),
    Ft <=> (mu - 1)(1 - alpha) <= alpha (1 - beta).

If 1 - beta >= p then Q_v = 2 and mu Q_v = 2 mu > 2, so Rv holds. If
1 - alpha >= p then Rh holds likewise. Assume from now on that
1 - beta < p and 1 - alpha < p, so Q_v = (p + 1 - beta)/p and
Q_h = (p + 1 - alpha)/p. Assume also that F and Ft both fail; their
negations are

    lambda > (1 - p)/(1 - beta),   mu > (1 - p)/(1 - alpha),

using 1 - beta + beta(1 - alpha) = 1 - p. Define

    E_lambda = (1 - p)(p + 1 - alpha) - 2p(1 - beta),
    E_mu     = (1 - p)(p + 1 - beta) - 2p(1 - alpha).

If E_lambda >= 0 then (1 - p)/(1 - beta) >= 2p/(p + 1 - alpha), so
lambda Q_h > 2 and Rh holds. If E_mu >= 0 then Rv holds in the same way. It
remains to show that E_lambda + E_mu > 0. Expanding,

    E_lambda + E_mu = 2 - s + p(3s - 4) - 2p^2.                       (6.4)

The constraints alpha beta = p and 0 < alpha, beta < 1 give
2 sqrt(p) <= s < 1 + p, the second because (1 - alpha)(1 - beta) > 0. The
right side of (6.4) is affine in s with coefficient 3p - 1.

If p >= 1/3 it is nondecreasing in s, so it is at least its value at
s = 2 sqrt(p). With x = sqrt(p) in (0, 1) that value is
2 - 2x - 4x^2 + 6x^3 - 2x^4 = 2(1 - x)^2 (1 + x - x^2) > 0.

If p < 1/3 it is decreasing in s, so it is strictly greater than its value
at s = 1 + p, which is 1 - 2p + p^2 = (1 - p)^2 > 0.

Both polynomial identities are checked symbolically by
`whole-staircase-check.py`; they also expand by hand in a few lines.

**Theorem 6.11.** Every staircase illuminates every pair of distinct interior
points.

*Proof.* Proposition 6.10 and Corollaries 6.7 and 6.9.

## 7. Assembly and covered degeneracies

*Proof of the main theorem.* By Propositions 1.1 and 1.2, P is a rectangle,
an L, a U, a staircase, a T with independent floor heights, or a wide-middle
offset corridor, up to isometry. Isometries preserve interior points and
specular paths. Rectangles are convex. The other five cases are Corollary 2.3
and Theorems 3.2, 6.11, 4.1, and 5.2.

The following degeneracies are covered by explicit arguments rather than by
genericity:

- **Endpoints on internal seams.** Staircase: x_s = b and y_t = d are inside
  the cross placement (Theorems 6.5, 6.6, 6.8). U: y_s = c or y_t = c are
  inside Theorem 3.1. T: points on x = a or x = b are assigned to a wing and
  handled in Theorem 4.1. Wide-middle: seam points use Lemma 2.2 or a direct
  segment (Theorem 5.2).
- **Smooth-wall contacts at a seam height.** The values z = 0 and w = 0 in
  Lemmas 6.2 to 6.4 and (5.2), (5.3) give one ordinary reflection on x = 0 or
  x = A at the seam height; no corner lies there.
- **Reflex corners at seam ends.** Excluded by the strict guards |z| < b,
  |w| < a (staircase), |z| < B, |w| < W (wide-middle), the portal heights
  u, v in (0, c) (U), and the orientation choice (T, and all L subrooms).
- **Convex corners on the floor or roof.** U: the floor contact lies in
  (M/2, A - M/2). Staircase floor chart: two consecutive target images give
  floor contacts less than a apart, so one avoids A Z. Staircase roof chart:
  a roof corner would mean Beta in a Z, and then T is reached before the roof.
- **Target reached before the developed endpoint.** Handled by truncation,
  which is always legitimate under the path convention of Section 0.
- **Ties in nearest-integer choices.** Every rounding bound is a non-strict
  inequality that still gives open windows; either tie choice works.
- **Equality in F or Ft.** Covered, since Theorem 6.5 uses F only through
  rho' < g/c <= (b - a)/(A - b).

## 8. What is not claimed

The theorem is restricted to orthogonal rooms with at most eight maximal
walls. It says nothing about rooms with ten or more walls, rooms with
diagonal walls, blockers on walls, or the illumination of boundary points.
No bound on the number of reflections is claimed; the U construction in
particular uses a number of reflections that depends on the marks.
