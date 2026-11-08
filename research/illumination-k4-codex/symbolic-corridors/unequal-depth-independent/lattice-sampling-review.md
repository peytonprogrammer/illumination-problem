# Independent review of uniform sampling for finite rational portal orbits

Codex01a1a00f. ACCEPT the frozen q>100sampling lemma and its stated
contrapositive. This is a uniform theorem for arbitrary offset/unit-box
placement, not a finite-orbit density claim. It does not settle the q<=100
exceptions or the unbounded short-relation families.

## Short vector and the exact area constant

For primitive0<A<C<q, the homomorphism Z^2->Z/q,(m,n)->mA+nC is onto,
since gcd(A,C,q)=1. Its kernel Lambda has index and covolume q. Let w
be the smallest nonzero l1 length in Lambda. An open diamond of radius
R/2 has area R^2/2. When R>sqrt(2q), this area exceeds q. Folding its
translates into a fundamental parallelogram and integrating multiplicity
forces two distinct interior points congruent modulo Lambda. Their nonzero
difference has l1 length<R. Letting R decrease proves w<=sqrt(2q);
discreteness of integer lengths justifies the weak endpoint inequality.
The factor2is correct; using the full diamond without accounting for the
difference body would give a wrong constant. This argument includes axis
minimizers and requires no enumeration or unproved asymptotic estimate.

Choose a minimizing vector(m,n), r=(mA+nC)/q. Any common divisor of
(m,n,r) would give a shorter nonzero kernel vector, so that triple is
primitive. With g=gcd(|m|,|n|), gcd(g,r)=1 and g divides q because g
then divides rq and is coprime to r. The no-short-relation hypothesis gives
w>=5. Primitivity of the triple is distinct from primitivity of the normal;
gmay exceed1, an important case in the next step.

## Every component and its true sample spacing

On R^2/(4Z)^2, the translated orbit lies on the level
m*x+n*y=m*v0x+n*v0y mod4. Its lift comprises lines indexed by k inZ,
with normal level m*v0x+n*v0y+4k. Two such lines project to the same
circle exactly when their k values agree modg, so there are gcomponents.
A primitive integer tangent is(-n/g,m/g); its period4gives circumference
4sqrt(m^2+n^2)/g. For the raw orbit point v_j=v0+4j(A,C)/q, the line
index is jr. Thus component labels advance by r modg, and gcd(r,g)=1
forces visits to ALL components. The orbit has exactly qdistinct points:
q dividing both kA and kC implies q dividing k by Bezout with q. Each
component therefore has q/gpoints.

More explicitly, points in one component have indices j0+gk, and their
differences form a finite cyclic subgroup of the identity circle. Its
order is q/g. Every finite subgroup of R/Z is the complete evenly spaced
grid of its order; the order assertion also follows from the distinct
point count above. Hence the Euclidean spacing is exactly
4sqrt(m^2+n^2)/q on EACH component. Missing disconnected components or
multiplying this spacing by g would invalidate the bound; neither mistake
occurs in the proposed proof. Translation offsets change cosets only.

## An interior line segment and strict sampling

For any lifted unit square with center z, choose an integer k whose normal
level differs from m*zx+n*zy by delta0 with absolute value<=2. The point
z'=z+(delta0/w)*(sign(m),sign(n)) lies on that line, since the dot product
of the normal with its sign vector is w. Its coordinate clearance from
both square boundaries is at least rho=1/2-2/w>0. This remains true if
one normal coordinate is zero. An OPEN tangent segment of Euclidean radius
rho around z' is inside the open square. Its length is2rho=(w-4)/w.

If the component's sample spacing is STRICTLY below2rho, the segment contains
an orbit point for every possible phase offset along the circle. Strictness
handles the case where a sample sits at a segment endpoint. The stated
sufficient condition q>4w*sqrt(m^2+n^2)/(w-4) is exactly this inequality.
Replacing the square root by w gives the stronger sufficient bound
q>f(w)=4w^2/(w-4). No limit ray or boundary contact is being allowed.

On5<=w<=sqrt(2q), f decreases until8and increases afterwards, so its
maximum is at an interval endpoint. f(5)=100<q. At the other endpoint,
f(sqrt(2q))=8q/(sqrt(2q)-4)<q whenever sqrt(2q)>12, which is certainly
true for q>100. Thus the required inequality is uniform for all q>100.
The strict threshold is preserved throughout; q100is deliberately excluded.

## Actual corridor and exact remaining claim

For every allowed interior s,t, the common original chart has portal pair
((1-alpha)s+alpha*t,(1-beta)s+beta*t)+4M(alpha,beta) mod4. Apply the
uniform result to the open square(1,2)^2. The resulting integer M gives
both strict portals. The already accepted matched-fold argument supplies
a finite actual vertical-wall-only connection, for arbitrary allowed cap
heights. No horizontal reflection, arbitrary ending-copy assumption or
density of a rational orbit is invoked.

Contrapositively, a vertical-only failure with NO annihilator of norm<=4
has primitive phase denominator q<=100. This is a finite set of possible
phase PAIRS, not a global denominator bound: points on the short-relation
families can have arbitrarily large denominators. The independently verified
q14,norm5counterexample shows that extra low-denominator phase exceptions
really exist. It refutes the stronger norm4-only premise, not this lemma.
The valid next reduction is short-relation families PLUS finite exceptional
phase pairs. Their endpoint failure sets and four-cap interactions still
require proof before any full-room acceptance.

## Independent prescribed controls

The own checker uses exact rationals throughout, including squared Euclidean
distances instead of floating square roots. For nine fixed phase triples it
independently reconstructs a minimizing lattice vector, triple primitivity,
all orbit points, every component and a Bezout circle coordinate. In each
component the coordinate set equals the complete q/ggrid. It then constructs
the nearest lifted normal line and checks strict unit-square hits for four
prescribed translations per phase, verifying the exact half-spacing distance
bound. Axis minimizers with g11,12,13and32explicitly test disconnected kernels;
the q101,norm5case tests the near-threshold bound.

Controls cover2147exact orbit points,73components,36strict translated-box
hits and1649sufficient-bound inequalities. These support the implementation
but do not substitute for the universal area/component/segment proof above.
No peer program is executed, no discovery search or finite support enumeration
is performed, and no universal rational illumination conclusion is claimed.
No correction remains for the frozen packet.
