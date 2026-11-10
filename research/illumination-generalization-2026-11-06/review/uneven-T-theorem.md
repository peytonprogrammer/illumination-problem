# Every unequal-floor T8 room illuminates every interior pair

New arbitrary-real optical corollary of the accepted two-orientation L theorem. Independent review pending. No bound on scale, k, reflection count, aspect ratio, or endpoint arithmetic.

## Exact statement

Let 0<a<b<A and 0<u,v<C be arbitrary real numbers. Define the closed room

    P=([0,a]x[u,C]) union ([a,b]x[0,C]) union ([b,A]x[v,C]).

Its eight maximal-wall vertices are, cyclically,

    (a,0),(b,0),(b,v),(A,v),(A,C),(0,C),(0,u),(a,u).

Every distinct pair of interior points has a finite specular path avoiding every actual polygon corner. The equal-floor theorem T-room-theorem.md is the u=v subcase. This statement permits unequal floor heights u and v. Rigid motions and reflection preserve the theorem.

Only the accepted all-real L theorem is used: any two interior points in a six-wall L have a corner-free connection reflecting exclusively on horizontal walls, and another exclusively on vertical walls. All claims below preserve the same actual marked pair and one global path.

## 1. Stem and same-side placements

Partition the interior marks into three classes: left wing x<=a, strict stem a<x<b, and right wing x>=b. Interior marks on x=a have y>u, and interior marks on x=b have y>v; the actual reflex vertices and the lower seam wall portions are excluded by interiority. This is an exhaustive, disjoint assignment including all seams.

Two stem marks have direct visibility in [a,b]x[0,C]. Two left-wing marks have direct visibility in [0,a]x[u,C], and two right-wing marks in [b,A]x[v,C]. These segments remain in the interior of P. A segment lying entirely on a seam has both endpoint heights strictly above that seam's floor.

For one stem mark and one left-wing mark use

    Q_L=([0,b]x[u,C]) union ([a,b]x[0,u]).

Both marks are strictly interior to Q_L, including a left-wing mark on x=a. Choose the HORIZONTAL-only L connection. Its horizontal walls, at y=0, y=u over [0,a], and y=C, are genuine P walls. Its entire right vertical boundary x=b is avoided. This includes the artificial portion above v and the actual P reflex corner (b,v), which is smooth on that L boundary unless it coincides with a Q_L corner. All other P corners in Q_L are L corners, so avoided.

The right case uses

    Q_R=([a,A]x[v,C]) union ([a,b]x[0,v]),

again with horizontal-only reflections. Its avoided left boundary x=a contains the artificial cut and the possible smooth-in-L actual P reflex (a,u). Horizontal wall contacts all occur on actual P walls. A right-wing mark on x=b remains an interior Q_R mark since a<b<A and its height is above v.

## 2. Opposite-wing placements

Now S belongs to the left wing including its interior seam x=a, and T to the right wing including its interior seam x=b. Thus

    0<x_s<=a, u<y_s<C;  b<=x_t<A, v<y_t<C.

Reflect horizontally if necessary so u<=v. If y_s>=v, the segment S--T lies in the common upper rectangle [0,A]x[v,C]. Even when y_s=v, that endpoint is interior to P; the open segment has y>v since y_t>v. It encounters no actual boundary.

Otherwise u<y_s<v, so u<v strictly. Choose the six-wall L subroom

    Q=([0,A]x[v,C]) union ([0,b]x[u,v]).

Both S and T are strictly interior to Q, including x_s=a and x_t=b. Choose its VERTICAL-only connecting path. Every vertical Q wall is an actual P wall: x=0 above u, x=A above v, and x=b between u and v. The sole artificial Q wall is the bottom horizontal segment y=u over a<x<b; the selected path avoids every horizontal wall contact. In particular it avoids the actual reflex corner (a,u), which is smooth on Q's bottom wall. The other actual reflex (b,v) is already a Q corner and is avoided. All remaining actual P corners in Q are Q corners, and the two stem-bottom corners lie outside Q because u>0.

Thus every reflection and every open segment of the selected path is legal in P, with unchanged velocities and actual endpoints. The u>v case is its horizontal mirror. Reversing the connection handles either source order.

Sections 1 and 2 exhaust all interior pairs, including internal seam and floor-level equality cases, proving the theorem.

## 3. Why restoring the omitted part is safe

The proof does not use generic illumination monotonicity under containment. Each chosen L has artificial boundary in just one orientation, and the selected connection avoids that orientation altogether. New P corners that are smooth L wall points lie on the avoided boundary too. Actual horizontal/vertical mirror contacts retain their mirror line, so specular velocities match exactly. No local optical paths are concatenated.

## 4. Prescribed exact hostile control

Use a=4,b=5,A=10,u=1,v=2,C=4 and the distinct marks

    S=(1/2,11/10), T=(9,21/10).

Their direct segment exits P: at x=5 its height is 277/170<2. In the opposite-wing L of Section 2, reflect y to y'=4-y. The accepted vertical-only L formula connects T'=(9,19/10) to S'=(1/2,29/10) using target image -161/2, ratio r=9, and strict portal x=1/20.

In the actual room the path from T to S has the following 17 vertical contacts, in order:

    p_j=(0,(3579-100j)/1790) for j even,
    p_j=(5,(3579-100j)/1790) for j odd,
    j=0,...,16.

All contacts have 1<y<2, so x=0 and x=5 are actual smooth mirrors. The final point is the specified S. Reversing gives the prescribed S-to-T connection. The exact checker checks this fixed witness against all actual finite walls, corners, open segment interiors and reflection velocities. It does not discover a direction or prove the arbitrary-real theorem.

## Scope

This excludes all such unequal-floor T rooms without a k bound. It does not classify all eight-wall orthogonal shapes, prove the full W<=21 theorem, or supply any arbitrary-direction or universal-minimum conclusion.
