# Independent acceptance of the centered midpoint repair

Codex01a1a00f, 6 November 2026.

Verdict: ACCEPT the frozen milestone unequal-depth/midpoint-repair.md,
sections A and B and its stated limited scope, without corrections.
This closes the whole centered resonance b=a+g and its reflected/reversed
counterpart a=b+g. It does not close arbitrary unequal-depth outer pairs.

Let d,g,a,h_-,h_+>0, b=a+g, h_->a, h_+>b and h=h_+.
The actual marks are S=(d,-a), T=(d,g+b). Define
R=(2d,h-a), C=(2d-db/h,g+h). The claimed path S,R,C,T has exactly
two smooth contacts for every admissible real parameter tuple.

The right wall contact R satisfies g<h-a<g+h: the first inequality is
h>b=a+g, and the second follows from a+g>0. Its x=2d therefore lies
on the upper chamber's actual exterior right wall, strictly away from both
endpoints. Since 0<b/h<1, C_x=2d-db/h lies strictly in (d,2d).
Thus C lies in the smooth interior of the actual top wall y=g+h.
In particular neither contact requires a positive lower bound on h-b.

The first displacement is (d,h), so its direction is proportional to
(d/h,1). At y=0,g its x coordinates are d+da/h and d+db/h.
Both are in (d,2d) because 0<a<b<h. Before the first portal its
x is between d and d+da/h, inside the lower rectangle. Between portals
it remains in their common open strip. After the upper portal it has
x<2d until R and g<y<h-a<g+h. It therefore reaches R as its FIRST
boundary contact and crosses no polygon corner or horizontal ledge.

The second displacement C-R=(-db/h,b) is b*(-d/h,1), with b>0.
It changes only the first velocity component at R, as required by a
vertical mirror. Throughout the open segment, d<x<2d and
h-a<y<g+h, so it lies inside the upper chamber and hits its top first
at C. The third displacement T-C=(-d(h-b)/h,-(h-b)) is
(h-b)*(-d/h,-1), with h-b>0. It changes only the second velocity
component at C. Its open segment lies in the upper chamber, since
x runs strictly between d and C_x and y strictly between g+b and g+h.
The final point is the actual T, not a reflected image.

All segment lengths are positive and both reflections are transverse.
The first leg has x>d except at its source, the second leg has x>d
throughout, and T_x=d, so actual T is not encountered prematurely.
No lower cap contact occurs; h_->a is used only for S being interior.
Reflection about y=g/2 followed by reversing the path exchanges the
outer depths and caps, giving the counterpart a=b+g with a lower-cap
construction. This transformation preserves actual walls, positivity,
specularity, smoothness and first arrival.

The no-vertical-only claim in section A is accepted independently in
midpoint-review.md, section3: odd target images give an integral developed
x at the temporal-midpoint upper portal, and refolding preserves the
integer lattice. The two-reflection construction is consistent with that
obstruction because its top contact changes vertical direction. Neither
the obstruction nor its repair asserts that any pair is dark.

## Independent reproducible checks

Run `python3 .context/illumination-k4-codex/symbolic-corridors/unequal-depth-independent/repair-check.py`.
The program uses only the frozen independent geometry implementation from
my foundation review, never imports or executes peer code, and checks the
specified formula without searching for replacement paths. It verifies
146 actual-wall paths and292 contacts, including the reflected/reversed
partners, varying unequal depths/aspect ratios, cap clearance1/100000000,
and two exact irrational paths in Q(sqrt(2),sqrt(3)). All PASS.

Every contact is checked against all twelve actual edges, with first-wall
order, corner exclusion, strict mirror interiors, boundary nonoverlap,
positive specular direction and no premature target. The symbolic hand
inequalities establish the arbitrary-real theorem; the finite arithmetic
controls alone would not. Source hashes pin the frozen proof, parent
checker/receipt (read only), independent geometry and obstruction review.

## Remaining goal

Only s=t=d with b=a+g or a=b+g is repaired by this packet. Arbitrary
horizontal coordinates, other unequal depths and the full exceptional-plane
join remain for the peer to solve and this chat to review independently.
The native goal remains active. No global reflection bound, all-interior-pair,
other-room-family, novelty or universal wall-minimality conclusion follows.
