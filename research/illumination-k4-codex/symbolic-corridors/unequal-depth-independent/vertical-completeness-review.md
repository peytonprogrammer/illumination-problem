# Independent completeness audit of the four vertical charts

Codex01a1a00f, 6 November 2026.

Verdict: for an outer-to-outer pair in this precise corridor, the union of
ALL four compatible chart boxes, both target signs and integer M is
necessary AND sufficient for a finite legal connection reflecting only
at vertical walls. Individual charts remain merely sufficient. This
completeness statement validates exact rational-period mechanism failures;
it does not assert that vertical-only paths suffice for illumination.

## Necessity for arbitrary real parameters

Any vertical-only connection from S below y=0 to T above y=g has constant
strictly positive vertical velocity. Thus it crosses each portal exactly
once and never leaves and returns to a chamber in y. Unfolding its lower
vertical reflections gives X(y)=s+v(y+a), with initial developed source s
and a signed real slope v. The lower physical x is F_(2d)(X).
Its first open portal has physical x in(d,2d). Consequently the developed
first residue r=X(0) mod4d lies in either(d,2d) or(2d,3d), with lower
fold derivative +1 or-1, respectively. No other residue gives an interior
portal point.

Matching both value AND derivative at this portal uniquely determines
the middle strip fold modulo4d: d+F_(2d)(X-d) for r in(d,2d), or
d+F_(2d)(X-3d) for r in(2d,3d). Indeed each is an unfolding of the
middle rectangle between its actual walls x=d,3d, and it has exactly
the specified portal position and velocity. The billiard evolution up
to the next corner is unique; a finite corner-avoiding trajectory must
therefore follow that fold throughout the middle band.

For middle offset c=d, the next physical portal is in(d,2d) only if
E2 mod4d lies in(0,d) or(d,2d). In the first case the middle fold is
2d-E2 with derivative-1, matching upper F_(2d)(X-2d), so u=2d.
In the second it is E2 with derivative+1, matching upper F_(2d)(X),
so u=0. For c=3d, the only permitted intervals are(2d,3d) and
(3d,4d): the middle fold is4d-E2 (derivative-1,u=0) or E2-2d
(derivative+1,u=2d), respectively. This gives exactly the four boxes
in the peer's proof and program. Interval endpoints yield portal corners
and are excluded by legality; no extra boundary case is lost.

Continue unfolding through the upper band with that uniquely matched
upper fold. At actual T its developed coordinate L must satisfy
F_(2d)(L-u)=t. Since0<t<2d, its complete image set is
L=u+epsilon*t+4dM, epsilon=+1 or-1, M integer. With
H=a+g+b, the straight unfolded slope is therefore (L-s)/H,
exactly the slope used in the four-chart construction. These observations
exclude additional vertical-only paths hidden outside that union.

The converse is the already independently accepted strict-box folding
argument: matched velocities at portals, actual vertical sides inside
bands, strict corner avoidance, finite contacts and first actual T by
strictly increasing y. Zero horizontal slope is included whenever its
strict boxes pass. No rationality or positive slope assumption is needed.

## Exact finite period and centered simplification

For rational alpha=a/H and beta=(a+g)/H let q be any common denominator.
M->M+q adds4d times integers at both portal times. For every fixed box
and target sign, M=0,...,q-1 therefore exhausts all phase outcomes,
including those of negative M. A successful residue elsewhere yields a
valid finite path at this representative; only the finite number of
vertical contacts may differ. This proves exact whole-period completeness
for the mechanism, not a bounded-angle or bounded-reflection cutoff.

At s=t=d, every possible unfolded target is an odd multiple L=(2k+1)d.
Both u=0 and u=2d permit any such target when their corresponding signs
are chosen. The normalized portal residues become
x=(1+2k alpha) mod4, y=(1+2k beta) mod4. The union of the four boxes
is exactly
1<x<2 and y in(0,1) union(1,2), OR
2<x<3 and y in(2,3) union(3,4).
The excluded y=1,3 values are genuine portal corners. For
alpha=A/q,beta=C/q, k=0,...,2q-1 is a complete period, exactly as used
by center-failure-graph.py. Its preliminary reduction gcd(A,C,q)=1 removes
duplicate rational pairs, but is unnecessary for the period argument.

## Three explicit peer failure candidates

I independently checked the THREE supplied rational center pairs
(a/g,b/g)=(1/2,1/2),(1/2,1),(1,1/2), with d=g=1 normalization.
They have(alpha,beta)=(1/4,3/4),(1/5,3/5),(2/5,4/5).
The complete respective odd-lift periods contain8,10,10 phase rows.
Every row misses every compatible open box. A second direct enumeration
of all four chart boxes, both signs and M modq verifies the same result
in112 exact chart tests. Thus each has NO vertical-wall-only connection,
for any admissible outer cap heights. This is stronger than merely failing
a chosen chart, because necessity was proved independently above.

Run `python3 .context/illumination-k4-codex/symbolic-corridors/unequal-depth-independent/vertical-failure-check.py`.
Its saved tables are exact Fraction values. It imports or executes no peer
program, scans no new parameter range and seeks no replacement trajectory.
It validates these explicit proposed mechanism failures only.

The equal-depth(1/2,1/2) pair already has an independently accepted
three-contact connection. No darkness inference follows for any of them.
I have NOT independently reproduced the full649pair discovery graph,
proved that these and |a-b|=g exhaust its failures, or inferred an
all-parameter rectangle-avoidance theorem from a denominator cutoff64.
The peer owns that classification and its associated covering argument.
Cap-corner exclusions remain an additional requirement after reflecting
endpoint depths; avoiding a rectangle of vertical failures alone would
not automatically eliminate simultaneous cap/side corners.
