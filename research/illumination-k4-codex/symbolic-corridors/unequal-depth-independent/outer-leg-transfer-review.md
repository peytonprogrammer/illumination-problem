# Independent review of cap transfer with straight outer developments

Codex01a1a00f. ACCEPT the outer-simple transfer lemma and the sufficient
condition that any one cap sheet has equal effective depths. The proof does
not require a straight development through the middle rectangle. A nonfatal
q4portal-value typo in the frozen dependency and my old review is reconciled
in equal-depth-portal-erratum.md/json, without changing frozen files.

## General transfer lemma

The initial auxiliary outer portion has only vertical-wall reflections.
Its vertical velocity is constant and positive, since it starts below0and
reaches its first portal there. Its side-wall unfolding is therefore a
single affine horizontal function X_-(z) of height, starting at x=s.
Similarly the final upper portion has a single affine development X_+(z)
and positive vertical velocity after its last portal at1. Their slopes
and signed endpoint images need not agree with one another or with any
one global middle development. This is exactly the added flexibility.

If lc=1, A=2h_--a>h_- and A<2h_-. Folding its initial height z by
Y=-2h_--z below-h_- maps the virtual mark-A to actual-a, keeps the
whole outer portion in[-h_-,0], and is the identity near the strict lower
portal. It inserts one selected lower-cap contact. Away from a simultaneous
side contact, this is an ordinary smooth horizontal reflection; side-wall
folds remain ordinary smooth actual vertical reflections. The folded
portion below the cap stays below0, so meets no middle ledge prematurely.

If the cap contact is a side corner, X_-(-h_-)=2j. Even symmetry of the
period4triangular fold and linearity on this OUTER portion give the actual
source again at virtual height-a, strictly after that corner. Start there
and discard the prefix. Nothing requires legal corner traversal. For a
selected upper cap, the same symmetry of the FINAL outer development gives
actual T at virtual1+b before a bad upper corner. End there. The symmetry
applies to any signed target image with fold t, so it preserves the actual
target and does not require a specified global unfolding copy.

These source and target trims stay entirely outside the middle: every
retained start is below0and every retained end above1. They cannot overlap,
remove a middle reflection or remove either strict portal. Smooth cap
contacts remain legal; corner contacts are outside the retained subcurve.
The original middle path is unchanged, and all its assumed reflections
are on actual smooth middle walls. Values and velocities are unchanged
near the portals. The construction has finitely many contacts and interior
endpoints; take a first actual T prefix if needed. Unselected caps do nothing.
Zero horizontal velocity creates no cap corner for an interior endpoint.
Thus the general implication holds with precisely the stated hypotheses.

## Exhaustive equal-depth construction dependency

For0<s,t<=1, the accepted equal-depth proof Section1has already removed
common-column endpoint cases. Its remaining Sections2–7 use exactly:

- Straight-developed vertical-only chart paths for irrational phases,
  general even denominators except the stated center case, q>=9and the
  finite q5/q7dispatch. Their physical height is strictly increasing.
- The q4center explicit three-middle-contact path.
- The q3explicit three-middle-contact family, for every horizontal pair.

The q4andq3initial and final legs cross the portals strictly, remain in
the outer strips and use no outer horizontal wall. Their three middle
contacts are on the actual top ledge x>2, right wall x3and bottom ledge
x>2, with strict corner avoidance. They never revisit an outer strip before
the last exit. Section7uses the Section2charts and adds no other path type.
The source/target interchange by vertical reflection and reversal preserves
all these properties. Therefore the list really is exhaustive for the
entire required horizontal range and arbitrary real common depth. It does
not import the separate L-subroom construction, which can use outer caps.

The q4coordinates in the frozen source and old review need the supplemental
prose correction: the stated path crosses both portals at3/2, not7/4.
Exact interpolation proves this, and3/2is still strictly admissible. No path,
reflection, existence argument or outer-simple property changes. The old
physical checker already validates the correct coordinates. The correction
is explicit and separately pinned, preserving all old source hashes.

If any effective cap pair A=B, choose arbitrary auxiliary cap clearances
beyond these virtual marks and use the equal-depth theorem. Its listed
outer-simple paths never use those auxiliary caps, so their values do not
enter the construction. The new transfer lemma then returns actual S,T
for the original cap heights. This proves all four possible effective-depth
equalities, including2h_--a=2h_+-b. It does not assert transfer of an arbitrary
auxiliary path with extra outer-horizontal bounces or outer revisits.

## Independent controls and scope

The own checker imports only frozen reviewer-owned helpers. It reconstructs
paths from eleven fixed accepted equal-depth formulas and one already
accepted both-corner vertical chart. It interpolates cap contacts directly
on the auxiliary polyline, trims only the repeated-source/earlier-target
portions, folds the outer heights and leaves all middle points unchanged.
An independent all-edge checker validates each resulting actual path and
its first-target reverse and positive diagonal scaling.48forward paths,
144actual paths total and948strict contacts pass, including both-corner
trims and all three-reflection middle cases. The specified unequal-depth
five-bounce example matches every parent path coordinate exactly.

No peer executable, search or parameter enumeration was run. The fixed
controls support the implementation; the universal transfer and formula
exhaustion are the hand arguments above. With the supplemental numerical
correction, no mathematical finding remains for this packet. The universal
fully rational room theorem is still open outside accepted reductions.
