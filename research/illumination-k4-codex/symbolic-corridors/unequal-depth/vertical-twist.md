# Remove irrational horizontal coordinates in a commensurable-height room

Codex01a18403, 6 November 2026. Parent hand milestone; review required.

## Statement and remaining goal

Normalize d=g=1. Suppose a,b,h_-,h_+ are positive rational numbers satisfying
the usual interior inequalities. If at least one of s,t is irrational, the
actual outer-chamber points S=(s,-a),T=(t,1+b) illuminate.
Together with the independently accepted irrational-height reduction, this
would reduce the full objective to ALL six normalized parameters
 a/g,b/g,h_-/g,h_+/g,s/d,t/d rational, without any denominator bound.
This is a reduction, not completion of that remaining rational class.

The L-subroom reduction handles either horizontal coordinate>1. Assume
0<s,t<=1 below; an irrational horizontal coordinate is then strictly<1.

## 1. A vertical affine twist fixing EVERY corner lift

Construct the standard four-copy translation unfolding X of the orthogonal
polygon: copies labeled by the signs of x and y reflection, glued along
corresponding mirror edges by translations. In a copy, use signed Cartesian
coordinates. Straight geodesics avoiding all polygon-vertex preimages fold
to finite ordinary specular paths. Remember that convex corner preimages
are REGULAR points on X; singularity avoidance alone would be insufficient.

Cut X on all lifted integer-x vertical lines. Each open unit-width strip
becomes a vertical annulus after the horizontal top/bottom mirror gluings.
There are two x-sign versions of each of these four strip types:

|physical x interval and component|vertical circumference|
|--|--|
|(0,1), lower chamber|2h_-|
|(0,1), upper chamber|2h_+|
|(1,2), common column through all three bands|2(h_-+1+h_+)|
|(2,3), middle chamber|2|

The total annulus area is
4h_-+4h_++4(h_-+1+h_+)+4=8(h_-+1+h_+), exactly four times
the polygon area. At noninteger physical x each vertical billiard simply
travels between the listed top/bottom walls, proving these annuli exhaust
X away from the cut fibers. Unit-width artificial subdivisions of a larger
cylinder are permitted; we do not require these annuli to be maximal.

Choose a positive integer L that is a multiple of every listed rational
circumference. Such L exists: take the least common multiple of the numerators
of the four circumferences in reduced form. The circumference2 forces L even.
In an annulus with signed transverse coordinate j<X<j+1, j integer,
and vertical coordinate Y modulo its circumference C, set

    A(X,Y)=(X,Y+L(X-j)) mod C.                           (1)

At X=j the shift is0; at X=j+1 it is L, an integer multiple of C.
Hence A fixes every cut boundary pointwise and glues across EVERY original
or artificial cut. In local translation charts its derivative is the SAME
matrix [[1,0],[L,1]]. Adjacent local formulas agree on their boundary and
have the same derivative, so they extend affinely across every regular cut
point. The inverse uses -L. Thus A is an affine homeomorphism of X, fixing
all cone singularities and ALL regular convex-corner lifts as well, since
every polygon vertex has integer horizontal coordinate and lies on a cut.
This last fact prevents a transported path from hitting a forbidden smooth
corner preimage. Integer translations of charts cause no difficulty: each
annulus formula is defined relative to its own j and agrees on its boundaries.

On the identity source copy in the lower-left annulus, A^ell moves its
vertical coordinate by ell L s modulo2h_-. On the upper identity copy it
moves T by ell L t modulo2h_+; on the x-reflected upper copy it moves the
vertical coordinate by -ell L t modulo2h_+. These formulas follow from(1):
subtracting the integer j changes the shift by a multiple of the circumference.
The x coordinate, and hence the physical horizontal mark, is unchanged.

## 2. Simultaneous small returns stay in the intended copies

For an integer ell, choose the small representatives

    delta_s = ell L s mod2h_-,
    delta_t = ell L t mod2h_+.

There are arbitrarily small simultaneous returns with ell!=0: pigeonhole
N²+1 multiples of(Ls/(2h_-),Lt/(2h_+)) into N² squares, then subtract two
indices. If at least one coordinate is irrational, no fixed nonzero ell
can give arbitrarily good returns, so the available return indices are
unbounded. Choose |delta_s|,|delta_t| below the four positive distances
of the marks from their chamber's horizontal walls. Then A^ell sends S
in its identity copy to a mark with depth a'=a-delta_s. It sends the upper
target in x-sign eta to a mark with depth b'=b+eta delta_t, still in that
SAME upper x-sign/y-positive copy. No cap or copy boundary is crossed by
these small net displacements. At an irrational s, delta_s!=0 and is irrational,
because ell L s minus an integer multiple of a rational circumference is
irrational. The same applies to t.

We will connect the actual image points on X, then apply A^-ell. This maps
a finite straight geodesic to another finite straight geodesic and fixes
all forbidden vertex lifts. Folding gives a legal original billiard path.
If actual T occurs before the chosen final lift, stop at its first encounter.
Finite corner-free segments have finitely many mirror crossings: away from
the finite forbidden set a compact path has positive clearance, and a straight
segment cannot enter and follow a mirror seam without passing a seam endpoint.

## 3. One horizontal coordinate rational, the other irrational

Exchange the chambers and endpoints by reflection/reversal if needed so s
is irrational and t rational. Choose a positive integer ell0 for which
ell0 L t is an integer multiple of2h_+. Every power A^(ell0 j) fixes ALL
four target lifts: their signed x coordinates are +t or-t modulo integer
translations, and the same divisibility holds in each upper annulus.

Along those powers choose a nonzero arbitrarily small source return.
The resulting source depth a' is irrational, while the target remains T.
The accepted noncommensurable-depth theorem gives a physical connection
between the image source and target. Lift it starting at the image source;
whichever target lift it reaches is fixed by A^(ell0 j). Applying the inverse
therefore connects the ORIGINAL source to a lift of ORIGINAL T, avoiding
all corners. This closes this entire horizontal-placement class.

## 4. Both irrational, with 1,s,t rationally independent

Take any nonzero simultaneous small return ell. The transformed depths are

    a'=rational - ell L s,
    b'=rational + ell L t.

An integer relation among1,a',b' would be an integer relation among1,s,t,
so none exists. Equivalently, the new phases alpha=a'/(a'+1+b'),
beta=(a'+1)/(a'+1+b') have no nontrivial integer relation with1.
The independently accepted generic foundation supplies a COMMON-CHART path
with upper offset0 and target lift t+4M. It reflects only at vertical walls.
The lower start fold has x-derivative+1 and the target fold has derivative+1;
there are no horizontal reflections. Hence the unfolded trajectory ends
in the identity-sign target copy, precisely A^ell(T in its identity copy).
This specified ending copy matters: an arbitrary unspecified target lift
would not suffice, because A need not commute with the billiard deck reflections.
Applying the inverse affine map proves the required original connection.

## 5. Both irrational, with one rational affine relation

The remaining case has a unique relation

    t=eta (p/q)s+mu,

where eta=+1 or-1, p,q are coprime positive integers, mu is rational.
We will use the upper target lift with x-sign eta, not choose it afterwards.

For the small returns of Section2, the expression

    p delta_s - eta q delta_t
      = -eta ell L q mu -2p h_- k_s +eta 2q h_+ k_t

is rational with a denominator bounded independently of ell,k_s,k_t.
Choose an integer D clearing these three rational coefficients. By taking
the simultaneous returns small enough, the expression has magnitude<1/D.
Being an integer multiple of1/D, it is therefore EXACTLY zero. Hence
eta delta_t=(p/q)delta_s. The image source and selected image target have

    a'=a-delta_s, b'=b+eta delta_t=b+(p/q)delta_s,
    R=p a'+q b'=p a+q b>0,                             (2)

with a',b' irrational and R rational. Both new phases are irrational:
substitute b'=(R-pa')/q in their denominators. A rational phase would force
a' rational, unless a positive constant q+R or p+R vanished, which it cannot.

All integer phase relations form one cyclic group. Its primitive generator is

    (m,n,r)=(k(p+R), -k(q+R), -kq),                    (3)

where k is the positive denominator of R in reduced form. Direct substitution
verifies(3). Conversely, writing sigma=m+n-r, the depth relation is
sigma a'-r b'+n-r=0. Its irrational coefficient gives
q sigma+p r=0, so sigma=kp,r=-kq for an integer k since gcd(p,q)=1.
The rational part then gives exactly(3). Minimal denominator k makes this
triple primitive: any common divisor divides k and kR, which are coprime.
Thus no orbit components are omitted.

The normal width is

    |m|+|n|=k(p+q)+2kR.

Here kR is a positive integer. This width is at least5 except when
p=q=1,k=1,R=1, where it equals4. For width>=5, the full-closure/common-box
lemma in phase-lines.md guarantees a COMMON chart with u=0 and the
PRESELECTED target sign epsilon=eta: its image interval has length>4,
so every translated source/target phase is attained. In the sole width4
case (m,n,r)=(2,-2,-1). The common box(1,2)^2 maps to(-2,2), while its
required phase is

    C=s-eta t.

For eta=+1 this lies in(-1,1). For eta=-1 it lies in(0,2), strictly,
because both irrational marks are<1. So the same common chart works there
too. The connected-kernel proof actually applies with all components from
(3); no rational-phase density premise is made.

At the endpoint, the common upper fold F2(eta t+4M) has derivative eta.
Since the lower start derivative is positive and y never reflects, the lift
ends in exactly the x-sign eta/y-positive target copy chosen at the outset.
This is A^ell applied to the original lift T^eta, by Section2. Thus the inverse
map sends the connecting geodesic to an original S-to-T^eta geodesic. It
avoids every vertex lift, because A fixes the whole forbidden set. Fold it
back to obtain the desired actual specular connection.

Sections3–5 cover every case with at least one irrational horizontal mark.
There is no assumption of rational independence when the marks satisfy an
affine relation, and no endpoint-sheet ambiguity has been ignored.

## Verification and limits

The affine surface construction, fixed regular corner lifts and selected
ending copies require independent hand review. Exact prescribed transport
controls are in twist-check.py/json; they test the original physical path
rather than merely checking the transformed endpoint equations.
No claim about the remaining fully rational marks follows from density.
That class consists of periodic affine orbits and needs a distinct argument
or a rigorously dark example. The native objective remains incomplete.
