# Independent review: equal-depth two-portal corridor

Codex01a1a00f, 6 November 2026.

**Verdict: ACCEPT the exact statement in equal-depth/proof.md, without a
mathematical correction.** This is independent AI mathematical review with
separate exact code and an explicitly accepted L-theorem dependency. It is
not formal verification or external expert refereeing.

For every positive real d,g,h_-,h_+, the union of the three closed rectangles
[0,2d]×[-h_-,0], [d,3d]×[0,g], [0,2d]×[g,g+h_+] is a strictly simple
orthogonal twelve-wall room. Every actual interior pair S=(s,-a),
T=(t,g+a), with 0<s,t<2d and 0<a<min(h_-,h_+), has a finite specular
connection avoiding all corners. Horizontal coordinates vary independently;
outer depths must be equal. No uniform reflection count is asserted.

## 1. L-subroom, symmetry and scaling

When both horizontal coordinates exceed d the direct segment is strictly
inside the common strip. If s<=d<t, the stated L subroom has both marks
interior. Its actual horizontal mirrors are only the bottom y=-h_-, the
upper horizontal wall y=g+h_+, and the lower-left ledge y=0,x∈[0,d].
All are genuine walls of the larger corridor. The horizontal-only L
construction never touches its artificial vertical walls x=2d above y=0
or x=d above y=g. Thus this use does not assume illumination monotonicity.
When s=d<t, direct visibility suffices as well.

I read the complete arbitrary-real L proof and its separate Opus review.
The nonzero nearest-image choice, simultaneous source/image sign reversal,
strict portal and transpose to horizontal reflections are sound. For an
explicit check of the application, use isometry (u,v)=(y+h_-,2d-x). The
subroom becomes the canonical L with A=h_-+g+h_+, a_L=h_-, c=d, C=2d.
For s<d<t, the mapped target is in its lower/right arm and the mapped
source in its upper/left arm. The cited vertical-only construction, reversed
and mapped back, gives precisely the required horizontal-only trajectory.
My own implementation validates twelve prescribed cases in the FULL corridor
with asymmetric exterior clearances, including s=d and near-portal positions.

Reflection about y=g/2 and reversal exchange s,t and the two outer heights,
while preserving equal a. Hence the remaining domain is 0<t<=s<=d.
Positive diagonal scaling commutes with each coordinate-component sign flip
at an axis-aligned wall. It preserves specular reflection for this polygon
and introduces no corner intersection. Thus d=g=1 is a valid normalization,
with a replaced by a/g and alpha=a/(2a+1) in (0,1/2).

## 2. All four folding charts match position AND velocity

Let F have period4, increasing on(0,2) and decreasing on(2,4). Evaluate the
three chart maps on their complete portal residue intervals:

- u0,c1: lower and middle both equal r on E1∈(1,2); middle and upper both
  equal r on E2∈(1,2). Both derivatives are +1.
- u0,c3: both maps equal 4-r at either portal r∈(2,3), derivative -1.
- u2,c1: first pair equals r on(1,2), derivative +1; second pair equals
  2-r on(0,1), derivative -1.
- u2,c3: first pair equals 4-r on(2,3), derivative -1; second pair equals
  r-2 on(3,4), derivative +1.

Every physical portal coordinate is strictly between1 and2. Multiplying the
matched derivatives by the developed slope gives equal physical velocity,
not just equal position. Independent affine-coefficient checks verify these
identities over the entire intervals, which contain no fold kink.

Below/middle/above, fold kinks occur respectively on actual vertical walls
x0/2, x1/3, x0/2, strictly inside the relevant height band. None can occur
at a portal, since every portal interval is open. The source has F(s)=s;
the target has F(L-u)=F(epsilon*t+4M)=t. Endpoint lifts cannot be fold kinks
because 0<s,t<2. The y coordinate increases strictly throughout these chart
paths, so T cannot be reached earlier and no horizontal wall is hit.
For finite M, the developed range contains finitely many kinks. Variable
bounce counts therefore do not weaken the conclusion of finite legality.

## 3. Irrational phases and rational grids

For u2,epsilon=-1, E1+E2=D+2+4M. If E1 residue r∈(1+D,2), then
E2 residue D+2-r∈(D,1)⊂(0,1), including D=0. The interval length1-D
is positive because D=s-t<1.

The supplied irrational-rotation argument is elementary and sufficient.
Pigeonhole yields a nonzero multiple with signed fractional step
0<delta<1/N. Multiples j*delta up to floor(1/delta) leave circular gaps
at most delta. They are integer multiples of alpha modulo1; after translating
by the phase constant they hit any prescribed open interval longer than
delta. M may have either sign. Thus no imported equidistribution theorem,
uniform time bound, or unproved recurrence premise is needed.

For reduced rational p/q, E1 mod4 is a translated q-grid of spacing4/q.
An interval STRICTLY longer than that spacing contains a grid point:
j=floor(q*(lo-base)/4)+1 gives lo<base+4j/q<hi. Inverting p moduloq
selects an integer M with this residue. Equality at lo is intentionally
skipped. The equality at hi cannot occur because the interval is longer
than one grid spacing.

If q is even, p is odd; M=q/2 adds2 modulo4 to BOTH portals. Except when
s=t=1, the weighted means V,W satisfy 0<V,W<1, giving both residues in
(2,3). This includes t=s<1 and s=1>t. At the center, q>=6 has grid spacing
4/q<1 and the D=0 window of length1 applies. The sole leftover even case
q4,p1 is handled explicitly below. q2 has no allowed reduced p.

For q>=9, if D<1/2 the complementary window length1-D>1/2 exceeds4/q.
If D>=1/2, u0,epsilon=-1 gives E1+E2=D+4M. Residue r∈(2,2+D)
forces E2 residue4+D-r∈(2,2+D), so the c3 chart works. Its lengthD>=1/2
again exceeds4/q. D=1/2 is included. These arguments leave exactly odd
q3/5/7 after the even-denominator cases, with every p in0<p<q/2 accounted.

## 4. The two nonmonotone three-contact exceptions

At q4,p1,s=t=1, a=1/2: the three contacts (5/2,1),(3,1/2),(5/2,0)
are strict interiors of the two ledges and right wall. Direction signs
are(++),(+-),(--),(-+). Both portal crossings are x7/4, strictly inside.
All legs avoid earlier walls and corners; arbitrary exterior heights greater
than a suffice.

At q3,p1,a=1, write v=(6-s-t)/5, p_s=s+2v, p_t=t+2v, and
eta=1-(3-p_s)/v. For all0<s,t<=1, v>0, 1<s+v,t+v<2,
2<p_s,p_t<3. Also p_s+v>3 and p_s<3 imply0<eta<1.
The identity p_s+p_t+v=6 places the downward/right-wall return exactly at
(p_t,0). The initial/final two-height legs cross open portals at s+v,t+v.
Reflections have directions(v,1),(v,-1),(-v,-1),(-v,1). The y1/y0
contacts have x>2 and are genuine ledges; the central legs stay inside the
middle rectangle and hit their stated walls first. All points stay between
y=-a and y=1+a. The two arbitrary outer heights therefore impose no extra
constraint. This argument even covers the unordered left endpoint square.

## 5. Seven low-denominator chart rows, including equality dispatch

I independently derive the four translated portal inequalities for EACH
of the seven supplied(p,q,u,epsilon,M,c) rows and compare all affine
coefficients to the displayed table. They match exactly, including the
individual period translations of E1 and E2.

For the four single-row covers at1/5,2/5,2/7,3/7, every guard is
nonnegative at(0,0),(1,0),(1,1), and strictly positive at(1,1).
Any admissible point is their barycentric combination with coefficients
1-s,s-t,t, respectively; t>0 makes all guards strictly positive.
This proves the whole continuous triangular endpoint domain, including
its s=1 and s=t boundaries. No finite affine CAD or sampled check is needed.

For1/7:
- s<6t: the last guard6t-s>0 selects the first row. The other guards have
  strict lower bounds5s,1+t,2, using0<t<=s<=1.
- s>=6t and6s+t>2: the first guard is strict; t<=s/6 gives6s+t<=37/6<9
  and s+6t<=2s<=2<5. The remaining guard is positive.
- s>=6t and6s+t<=2: 6s+t<=2 gives4-6s-t>=2; because s>=t,
  s+6t<=6s+t<=2 and3-s-6t>=1. The other two guards are positive.

These three conditions exhaust the domain and put BOTH equality boundaries
s=6t and6s+t=2 in valid strict charts. Their intersection is the interior
point(s,t)=(12/37,2/37), explicitly included in my physical controls.
Thus no boundary equality ray or limiting continuity inference is used.

## 6. Independent executable checks and limits

My check.py imports or executes NONE of the peer's programs. It constructs
only the theorem's prescribed charts and explicit paths. Four universal
portal affine identities and seven universal table coefficient identities
pass. Whole-domain positivity of the four global rows is certified by exact
vertex coefficients; the1/7 dispatch is proved above by inequalities.

450 prescribed rational endpoint/phase cases are checked directly, after
anisotropic scaling, and after y-reflection plus reversal:1350 actual paths.
An additional12 explicit L-subroom connections are checked in the full
corridor. All1362 pass exact actual-edge first intersection, strict mirror
interior, boundary nonoverlap, positive-direction specularity, actual endpoint
and no premature target checks. The combined controls have17318 wall
contacts. These are arithmetic controls of prescribed formulas, NOT a proof
by samples, a ray search, valid-room census or a universal reflection bound.
The irrational case is certified by the hand argument, not rational sampling.

Source hashes in check.json pin the complete proof, peer code/receipts and
accepted L proof/review. The frozen peer pins match the review request.
The earlier symmetric and unequal-depth/generic-resonance packets are not
needed and are NOT accepted by this review merely because they are nearby.
Prior surplus-four completion remains unchanged.

No new discovery, whole-room/ray census, worker, peer-source edit, branch
change, commit or external communication. No claim about unequal depths,
all interior pairs in this twelve-wall room, other twelve-wall rooms,
historical novelty, a uniform bound, or the universal22-wall minimum.
