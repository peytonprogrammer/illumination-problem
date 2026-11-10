# Independent review of the first unequal-depth lemmas

Codex01a1a00f, 6 November 2026.

Verdict: ACCEPT sections 1–3 captured in midpoint-source-snapshot.md.
These are partial lemmas, not a full unequal-depth illumination theorem.
The peer's proof.md remains live; the acceptance applies to the exact
snapshot and the mathematical statements specified here, not future edits.

## 1. Common-core endpoint reduction

If both s,t>d, the direct segment has d<x<2d throughout and lies inside
the common strip. If s<=d<t, use the L-shaped subroom
[0,2d]×[-h_-,0] union [d,2d]×[0,g+h_+]. Both marks lie in its interior.
Its horizontal walls are subsets of actual corridor walls: the bottom cap,
the lower-left ledge, and the top cap over d<=x<=2d. Its artificial walls
are vertical. The accepted L theorem gives a connection using horizontal
reflections only, hence it does not hit any artificial vertical wall.
Every contact remains a legal actual-wall contact in the full room.
This does not assume unrestricted illumination monotonicity.

The explicit isometry (u,v)=(y+h_-,2d-x) takes this subroom to
[0,A]×[0,c] union [0,a_L]×[c,C], with
A=h_-+g+h_+, a_L=h_-, c=d, C=2d. The reversed target is the cross-arm
source at (h_-+g+b,2d-t); the original source is the cross-arm target
at (h_--a,2d-s). For s<d<t, all strict L hypotheses follow from
0<a<h_-,0<b<h_+ and s<d<t<2d. Their depths are independent; no a=b
step appears in the L proof. At s=d<t, a direct common-strip segment
already works. The reflected/reversed argument handles t<=d<s.
Thus only 0<s,t<=d require the new argument.

Reflection about y=g/2 and reversal exchange (s,a,h_-) and (t,b,h_+).
They can impose a horizontal order while exchanging depths, but cannot
impose a second independent depth order. The peer explicitly preserves
this limitation. Positive independent coordinate scalings commute with
axis-reflection sign changes, so normalization d=g=1 is legal here.

I reread the complete accepted L argument and its separate prior review,
including the nonzero-image choice, sign reversal, strict portal, transpose,
and finite contacts. No extra hypothesis obstructs the unequal-depth use.
My own L implementation uses the actual independent b in the transformed
source and validates 96 prescribed paths in the FULL twelve-wall polygon,
including reversals, highly unequal positive depths, several aspect ratios
and very small cap clearances. All 1,752 wall contacts pass exact actual-edge,
strict-interior, specularity and target checks. These are formula controls;
the arbitrary-real reduction rests on the hand argument.

## 2. Four chart formulas

With H=a+1+b, alpha=a/H and beta=(a+1)/H, one has 0<alpha<beta<1.
Both displayed portal expressions follow by substituting y=0,1 into
X(y)=s+(u+epsilon*t+4M-s)(y+a)/H. The four boxes are precisely
those in the accepted equal-depth folding calculation. Their identities
depend only on residue, never on beta=1-alpha. On each full OPEN interval,
the affine values and derivatives of adjacent folds agree; all physical
portal coordinates lie in (1,2). The target lift maps to actual t,
and y increases strictly, yielding first target arrival and finitely many
actual vertical contacts. The independent checker rederives all four affine
identities. This is sufficient for a legal connection, not a criterion
whose failure establishes darkness or even excludes other vertical charts.

## 3. Midpoint obstruction to every vertical-only path

Normalize d=g=1, take s=t=1 and b=a+1, a>0. Consider ANY finite legal
connection using only vertical mirrors. Each vertical reflection preserves
the vertical velocity. Since the target has larger y, that velocity must
be strictly positive. Unfolding the entire reflection word therefore gives
one straight segment from (1,-a) to (L,1+b), with unchanged heights.
Every actual vertical mirror lies on x=j for integer j. Any finite
composition of x->2j-x sends odd integers to odd integers, so L is odd.

The upper portal y=1 occurs at time fraction
(a+1)/(a+1+b)=1/2. Its developed x is (1+L)/2, an integer. Refolding
the portion of the word already traversed preserves integrality, since
every individual reflection does. Thus its physical x is integral too.
There is no integer strictly between 1 and 2. A connection to the target
in the upper band must enter through this open portal, so it cannot do so.
Contacts at portal endpoints are forbidden polygon corners; x outside that
interval does not enter the upper chamber. This contradiction excludes ALL
vertical-only words, rather than only the four chosen charts.

There is no escape via zero or negative vertical velocity, tangency, a
repeated portal crossing or an outer cap: constant positive vertical velocity
rules each out in a vertical-only path. Degenerate r=0 is included in the
integer contradiction. Undoing the diagonal scaling gives every a>0,g>0,d>0
with s=t=d,b=a+g and arbitrary h_->a,h_+>b. Reversal/reflection also
implies the corresponding a=b+g center line. These are mechanism
obstructions; a connection with horizontal reflections may exist.
No darkness, nonillumination or rejection of the full goal follows.

## Checks, scope and remaining obligation

Run `python3 .context/illumination-k4-codex/symbolic-corridors/unequal-depth-independent/midpoint-check.py`.
It uses only my own frozen independent geometry implementation, never peer
code or peer writers. It pins the reviewed section snapshot and dependencies.
It checks four whole-interval affine identities, 96 actual L-subroom paths,
and 505 prescribed odd-lattice/midpoint arithmetic identities. These finite
controls support, and do not replace, the universal hand proof above.

An initial extreme-aspect prescribed verification run was terminated before
producing a receipt because its explicit contact expansion was unnecessarily
large. The current fixed controls retain unequal depths, varying aspect
ratios and small cap clearances while completing in under a second. This
was not a search or a failed mathematical case; no conclusion depends on
the stopped run.

The full unequal-depth theorem is OPEN. The peer owns the repair of the
center resonance using actual horizontal reflections and the remaining
parameter coverage. This receipt clears the first three lemma reviews only.
The generic finite-resonance foundation is separately accepted in
../arbitrary-endpoints-independent/review.md. No universal wall-minimum,
all-interior-pair is claimed.
