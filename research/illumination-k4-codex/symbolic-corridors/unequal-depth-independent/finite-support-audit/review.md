# Independent acceptance of the complete vertical-failure support theorem

Codex01a1a00f. ACCEPT the10critical-depth-lines plus11finite-depth-points
NECESSARY support condition for vertical-only failure, with the mandatory
irrational-depth clarification. This is not acceptance of the full room
illumination theorem or any rectangle/optical closure claim.

## Exact accepted statement and dependency correction

Normalize d=g=1. For any positive real a,b and real0<s,t<=1, failure of
all compatible vertical-only charts implies membership in

a1,b1,b=a+1,a=b+1,b=2a+1,a=2b+1,b=2a+2,a=2b+2,b=3a+1,a=3b+1,

or in the exact11point set
(1/2,1/2),(1/5,3/5),(3/5,1/5),(3,5),(5,3),
(1/3,7/3),(7/3,1/3),(1/7,3/7),(3/7,1/7),(5,8),(8,5).
These are supports only: not every horizontal placement fails there, and
none is asserted dark. Arbitrary original positive d,g follow by the
accepted axis scaling. Cap heights do not enter vertical-only trajectories,
except the original strict endpoint interior inequalities.

The first irrational-depth paragraph of frozen finite-support-theorem.md
is overbroad on its own. The accepted phase-lines result sometimes uses
cap repairs for its two centered irrational exceptional rows. Read the
original theorem WITH finite-support-irrational-clarification.md: first
restrict OUTSIDE the10critical lines. The two exceptional phase rows
alpha1/2orbeta1/2 correspond precisely to a=b+1or b=a+1, already excluded.
Every remaining irrational depth pair has a vertical-only chart. Therefore
an outside-support candidate must have rational phases. This correction
is necessary, preserves the final statement and is included in the receipt.
It does not silently upgrade a physical cap connection to a vertical one.

For primitive rational phases(alpha,beta)=(A/q,C/q), the independently
accepted lattice theorem eliminates q>100with no short relation. A short
relation has a representative in the reviewed30primitive triples. Outside
all10critical lines, every relation present is one of the20good lines;
the reviewed eta1/8margin eliminates q above its certified16l1cutoff.
If several good relations hold, the smallest cutoff is sufficient. Any
critical relation puts the pair directly in the support, so no intersection
case is lost. q<3has no integer0<A<C<q. This reduces the outside-support
proof to exactly the two finite groups verified below, without a global
bound on rational denominators along the critical lines.

## Independent primitive-phase enumeration and symmetry

The own check.py independently enumerates every primitive0<A<C<q through
q100. It matches short relations by equality against the separately accepted
30triple table and cross-checks equivalence to all40nonzero raw normal pairs
of l1norm<=4. The outside-short group contains115408phase pairs. The good-line
group excludes EVERY critical line, requires a good relation and q no larger
than its smallest cutoff; it contains4332phase pairs throughq64. These groups
are disjoint. Both counts and the predicates match the frozen classifiers.

The actual independent optical proof computes59950canonical phase cases,
not119740separate cases. The reduction is exact: reflect y->1-y and reverse
a vertical-only path. This exchanges depths a,b and horizontal coordinates
s,t, and maps phase(A,C,q) to(q-C,q-A,q). It preserves primitive denominator,
the full admissible endpoint SQUARE, strict portals and corner avoidance.
It is a bijection, so complete coverage/failure at one phase transfers to
its partner by transposition. The square is essential; ordering s,t at fixed
unequal depths would be invalid. The own enumerator explicitly verifies
that every partner stays in the same finite group. Self-partners A+C=q are
counted once; other canonical phases count twice. This gives all119740full
phase classifications. No unproved symmetry of a fixed asymmetric room or
fixed-depth ordered endpoint triangle is used.

## Independent chart generator and exact homogeneous geometry

No peer executable, helper, clipper, wrapper or writer is imported or run.
The own proof uses normalized integer homogeneous vertices(x,y,w),w>0,
representing(x/w,y/w). This differs from the parent's Fraction coordinate
representation and its guard-translate enumeration. For an integer affine
guard(a,b,c), the exact sign at a vertex is the sign of ax+by+cw.
For an edge with endpoint guard numerators u,v, an opposite-sign crossing
is the normalized homogeneous vector u*B-v*A. Its guard value is exactly
zero. Gcd reduction and positive denominator normalization preserve the
point. The implementation retains polygons, segments and isolated points;
it never drops a piece for zero area.

For each phase, all four compatible boxes, both target signs and M0..q-1
are generated. The portal numerator x(s,t)=(q-A)s+epsilon*A*t+A(u+4M)
has exact minimum xmin and maximum xmax on the closed square. A translated
strict interval(q*lo+4qk,q*hi+4qk) can meet it exactly when
k>(xmin-q*hi)/(4q) and k<(xmax-q*lo)/(4q). The own integer floor/ceiling
bounds enumerate this complete translate range, with strict equality handled
correctly. The same independent derivation is applied to the second portal.
M->M+q adds multiples of4to both portal residues, proving full signed-integer
period completeness, not a reflection/direction cutoff.

Each successful chart is an intersection of FOUR OPEN affine halfplanes.
To subtract it from a current closed convex piece, the own algorithm keeps
the portion satisfying the negation of the first guard, then the portion
satisfying the first weak guard and the negation of the second, and so on.
Their union is exactly the complement of the open conjunction: every equality
is retained until some other strictly legal chart covers it. The final all-
guards-positive portion is removed. The early all-nonpositive/all-positive
vertex tests are valid because each guard is affine on a convex piece.
All intersections use closed halfplanes, including at degenerate edges and
points. Normalized vertex-set deduplication merges identical convex regions
without losing any point or changing cyclic order of the retained polygon.

A piece is discarded as inadmissible only if its maximum x or maximum y is
zero. All pieces remain in[0,1]^2. If both maxima are positive, the average
of its vertices has BOTH coordinates positive, even if distinct vertices
attain the two maxima. Thus this filter discards exactly the pieces confined
to an excluded axis. It cannot discard a segment joining opposite axes or
an admissible boundary/vertex. Upper edges s1and t1and the center(1,1) are
retained. The implementation has explicit point/segment/equality sanity
controls in addition to the hand audit of these formulas.

## Complete positive verification and negative evidence

The initial independent run finished ALL59950canonical cases and thereby
ALL119740finite cases:119729full endpoint squares covered,11phase pairs
with a nonempty admissible complement. It applied1102472exact integer-guard
clauses. Every unexpected nonempty complement or false reported exception
would fail an assertion; no mismatching phase was tolerated. All negative
convex-piece barycenters were independently rechecked across the complete
four-box/sign/lift period, totaling944explicit chart evaluations. The depth
conversion a=A/(C-A),b=(q-C)/(C-A) gives exactly the11points above. The
special point(1/2,1/2) is retained at s=t1, so the center exception is not
lost by the boundary treatment.

A durable replay imports ONLY the own frozen homogeneous functions, reruns
the complete finite domains and verifies every canonical classification,
guard count, residual piece and witness against the original receipt. It
also passed with identical counts and residual coordinates. It does not call
the initial timed main, so the proof remains reproducible after the original
audit clock expires. All original peer and own source hashes remain unchanged.

The additional failure-unions.py uses a DISTINCT planar face/edge/vertex
arrangement from the previously audited own geometry helper. It partitions
by every boundary line and vertex coordinate of both the parent's failure
pieces and the own reconstructed pieces, including degenerate sets. On each
admissible relative cell it compares membership in both closed unions and
independently evaluates all chart periods. All1192relative cells across
ALL11phase pairs agree. This establishes the parent failure unions on the
whole admissible square, not merely their supplied representatives or an
endpoint grid. Their boundary pieces can therefore be used in later reviews
subject to the original endpoint interior hypotheses.

## Reproducibility, clock and remaining objective

The conservative840second aggregate clock was persisted before coding. The
initial full proof finished75.30seconds after that start, including setup;
its process returned0and is terminal. No restart, clock reset, worker or
replacement search was used. Durable replay and failure-union reconciliation
are prescribed proof verification of the same frozen finite data, not new
discovery. The initial checker/result/clock remain preserved.

Run the long-term full proof replay:

    python3 .context/illumination-k4-codex/symbolic-corridors/unequal-depth-independent/finite-support-audit/replay.py

Run the independent complete failure-union comparison:

    python3 .context/illumination-k4-codex/symbolic-corridors/unequal-depth-independent/finite-support-audit/failure-unions.py

The support theorem now follows from the reviewed irrational clarification,
unbounded lattice/margin reductions and complete independent finite proof.
No mathematical finding remains after the mandatory addendum. All published
freeze hashes match. The original whole-room objective is still incomplete:
four cap-sheet support rectangles must be reduced using their actual failure
sets and optically closed. Support membership, rank-family counts and the
existence of a three-pass circle window do not yet establish finite rational
paths or a dark example. These remain separate peer review obligations.
