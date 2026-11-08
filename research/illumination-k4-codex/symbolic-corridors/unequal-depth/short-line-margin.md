# Twenty short-relation families have a uniform rational sampling margin

Codex01a18403. Candidate computer-assisted affine-cover reduction; independent review required. This uses the circle-spacing argument of lattice-sampling.md and the already accepted four compatible portal boxes. It does not require or assert the disproved norm-four failure premise.

## The finite relation list

Use normalized phases 0<alpha<beta<1. If a relation m*alpha+n*beta=r has 0<|m|+|n|<=4, divide any common factor of (m,n,r), then change sign to make m>0 or m=0,n>0. The range on the open phase triangle is strictly between min(0,n,m+n) and max(0,n,m+n). Therefore enumerate precisely the primitive triples with r strictly between these integer endpoints. There are30 triples; short-line-margin.json records every one. Every short relation has a representative in this list.

The corresponding depth line is

    (m+n-r)*a-r*b=r-n.                                (1)

Each triple is primitive even when gcd(m,n)>1. No components of its level set may be dropped.

## Exact circle-to-box guards

For target shift u=0 or2, target sign epsilon=+1 or-1, the required portal residue level is

    m*E1+n*E2 = C modulo4,
    C=(m+n-r)*s+r*epsilon*t+r*u.

For each compatible unit portal rectangle I1xI2, let lo,hi be the minimum and maximum of mx+ny over its closure. Replace it by the concentric open square whose four sides have moved inwards by eta. Its strict image under the normal is

    (lo+eta*w, hi-eta*w), w=|m|+|n|.

Thus the translated relation circle meets that smaller open square exactly when

    lo+eta*w < C+4k < hi-eta*w for some integer k.     (2)

These are two strict affine guards in s,t. All k=-9,...,9 suffice: on the closed endpoint square, |C|<=16 and the box normal extrema have magnitude<=16, so any successful k has |4k|<32. The range is deliberately a safe overestimate.

## Exact finite closed-square proof

short-line-margin.py begins with the CLOSED square [0,1]^2, including every edge and vertex. For every clause (2) it removes the OPEN intersection of its two guards. It retains the exact closed complement as a union of convex polygons, segments and points. Arithmetic uses Fraction throughout. No endpoint grid is sampled.

For clarity, subtracting {f>0,g>0} from P keeps (P intersect{f<=0}) union (P intersect{f>=0,g<=0}). A guard boundary f=0 remains in the first part, so using the weak inequality in the second part never loses a failure boundary. Sutherland-Hodgman clipping against closed halfplanes is also applied to segments and points. No axis-admissibility filter is used here; unlike the finite physical endpoint checker, this program must retain s=0 and t=0.

At eta=0, exactly20 of the30 triples cover the WHOLE closed square. Each of those same20 also covers it at eta=1/8. The other10 have nonempty closed blind boundary pieces, explicitly retained in the JSON. The stronger shrunken-square cover, not merely compactness or a positive sample margin, is the certificate used next.

## Uniform denominator cutoff on the20 good lines

For a rational phase pair (A/q,C0/q) in lowest joint denominator and a primitive relation triple, lattice-sampling.md Section2 shows that its finite orbit visits every component of the relation level set with Euclidean spacing

    4*sqrt(m^2+n^2)/q.

For every endpoint placement in [0,1]^2 the eta=1/8 affine cover supplies a compatible relation line through the inward-shrunk portal square. The selected point has l-infinity clearance strictly greater than eta from the original portal boundary. Hence a tangent Euclidean segment of length2eta lies in the original open rectangle. A rational orbit point must hit it whenever

    q > 2*sqrt(m^2+n^2)/eta.

The rational sufficient cutoff q>16w follows from eta=1/8 and sqrt(m^2+n^2)<=w. All w<=4, so q>64 suffices. Each row records its own safe cutoff16w (32,48or64).

This is uniform over real horizontal endpoints, including their closed boundary limits in the phase calculation. Actual billiard conclusions still require the original interior endpoints. No finite-orbit density assumption is used.

## The10 genuinely unbounded candidate depth lines

The rows without a closed-square cover correspond to exactly

    a=1, b=1,
    b=a+1, a=b+1,
    b=2a+1, a=2b+1,
    b=2a+2, a=2b+2,
    b=3a+1, a=3b+1.

The word candidate matters: membership does not imply a vertical-only failure, much less darkness. Along these families the circle-window margin can vanish at endpoint boundary limits, so the present compact uniform sampling argument supplies no fixed q cutoff.

Combining this result with lattice-sampling.md gives the following CONDITIONAL support reduction. Outside these10 depth lines, any vertical-only failure must occur either at (i) one of the finitely many primitive phase pairs q<=100 with no short relation, or (ii) a phase on one of the20 good short-relation lines with q at most that line's cutoff. The two finite continuous endpoint classifications are saved separately. They must complete and be independently verified before claiming their precise exceptional depth set.

No full four-cap rectangle theorem, dark example, universal reflection bound or complete room theorem is claimed here.
