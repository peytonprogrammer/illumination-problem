# Independent audit of the W<=22 parity enumeration

Status: ACCEPT the source-level completeness/pruning argument and the recorded
four-start W22 exclusion, with the execution trust boundary stated below.
No duplicate exhaustive run was performed.

## Result and trust boundary

The frozen completed receipts report 4,639,278,650 visited nodes,
2,238,256 closed candidates and zero outputs across four start-parity files.
The audited algorithm covers every strictly simple canonical parity room
with at most 22 walls and at least two interior A points.

The audit checks the algorithm, its finite state bounds, exact geometry,
source/binary correspondence and persisted terminal receipts. It does not
independently repeat those billions of DFS nodes or supply a formal proof
certificate for the exhaustive execution. The correspondence of the four
historical launch arguments to start indices 0..3 relies on the peer run
record and receipt filenames; the footer itself records WMAX but not that
start argument. This is ordinary recorded-execution trust, not a
cryptographically authenticated launch record.

The result concerns the parity subclass. It does not rule out the already
known non-parity simple22 room or arbitrary dark rooms. W<=22 includes the
sub-22 question for this subclass; it does not by itself exclude W=23.
The continuing W24/W26 jobs were not audited as completed runs here.

## 1. Roots and orientation are complete

The walk uses atomic unit steps in the eight canonical directions. Every
boundary of a union of canonical triangles has this representation; smooth
intermediate lattice points are retained during the walk.

Choose the boundary lattice point minimal by (y,x), translate by an even
integer vector into one of (0,0),(1,0),(0,1),(1,1), and traverse the boundary
counterclockwise. The program tries those four start representatives and
all eight possible first directions, except those leading below the root
or taking a prohibited diagonal through a mixed-parity point. None of those
excluded first steps can belong to the chosen rooted canonical boundary.
No orientation/D4 quotient is assumed by this exclusion run.

Visited flags prohibit repeated atomic boundary vertices. Canonical tiling
edges form an embedded planar graph: they cannot cross in the interior of
a unit edge. The prohibited immediate reversal also rules out retraced
edges. A closed accepted walk is therefore a simple cycle. The signed turn
sum eight selects counterclockwise orientation. Holes and point contacts
are outside the enumerated class.

## 2. Allowed turns match the canonical grid

The code's integer classes are A=0 (even-even), mixed parity=1 and odd-odd=2.
The older comments/board description interchange the letters B and C; the
implemented conditions are correct by parity.

A mixed-parity point has only axis-aligned incident canonical edges. A
proper corner there must turn +90 or -90 degrees; straight continuation
would be a non-A smooth point, forbidden in a parity room. At an odd-odd
point all eight canonical rays are available; every nonzero turn except
an immediate reversal is allowed. At A points, straight continuation is
allowed, together with all genuine canonical turns.

Thus the algorithm does not incorrectly restrict all odd-odd corners to
90/270 degrees. Independent local cross-product geometry checks all120
allowed representative wedges, including odd-odd135-degree corners.

## 3. Tile-sector assignments are necessary

At a processed boundary vertex, the open counterclockwise sector from the
outgoing direction to the reversed incoming direction is the room interior.
The local canonical tiles strictly within this sector must be inside; the
other incident tiles must be outside.

The tile_of construction uses eight45-degree sectors at A/odd-odd points
and four90-degree sectors at mixed points. Its triangle-centroid keys are
unambiguous: canonical tile interiors are disjoint and each centroid is
strictly interior to its tile. Different tiles cannot have the same centroid.
The120 independent local checks compare these memberships against
cross-product sector tests and verify canonical ABC tile geometry.

An inside/outside contradiction therefore excludes every completion of
that boundary prefix. These are necessary constraints, not an assumption
that the current marked-inside tiles constitute the whole eventual room.

## 4. The future-corner budget is a safe lower bound

vin[v] counts distinct currently-inside tiles incident to v. req counts
non-A vertices with vin>0 that the boundary has not yet visited. Each such
vertex belongs to the closed eventual room. Parity requires it to be a
genuine boundary corner. Because the cycle has not yet visited it, it must
be visited later and contribute a distinct future nonzero turn.

Consequently future wall count is at least walls+req. The program's prune
walls+req>WMAX cannot discard a valid parity completion. Newly visited
vertices may still incur a turn later even though they have just left req;
that only weakens this lower bound and is safe.

mark_in updates vin only on a tile's inside count crossing zero. visit and
unvisit update req exactly when the point becomes visited/unvisited and
already has positive vin. The independent local controls verify the counts;
fixed boundary controls verify nested updates and complete rollback.

## 5. Conflict bookkeeping is sound under the actual stack protocol

At every recursive entry, no tile has positive inside and outside counts
simultaneously. A newly added wedge mentions each of its tiles once and
puts it on exactly one side. Its conflict increments count precisely the
tiles assigned against a positive opposite-side count. It therefore yields
zero iff the augmented state is consistent.

If a contradiction occurs, the program does not recurse before removing
that wedge. Its removals undo exactly those increments. If no contradiction
occurs, recursion returns the same state by induction, and removing the
wedge again restores the entry state. The temporary closure wedge follows
the same protocol. This protocol matters: conflict is not intended as a
correct arbitrary-operation counter for unconstrained interleavings.

All24 fixed boundary replays finish with req, conflict, visited, vin, tin
and tout completely zero after rollback. They run with address and
undefined-behavior sanitizers enabled.

## 6. The closure-distance prune is safe

A parity wall contains at most one smooth intermediate lattice point: any
two consecutive lattice points cannot both be A. Thus every maximal wall
has at most two atomic steps, including diagonal walls.

After taking the proposed edge, at most one atomic step can remain in its
current straight wall. Each remaining future turn can start at most two
more atomic steps. If R=WMAX-walls, any valid completion has at most
1+2R remaining steps. Chebyshev displacement to the root cannot exceed
that number, since each atomic step changes either coordinate by at most
one. The program's test

    max(|x-sx|,|y-sy|) <= 2*(WMAX-walls)+1

is therefore a necessary closure condition. Counting the root's eventual
turn among the remaining budget can only make this estimate looser.

## 7. The fixed arrays do not impose a hidden window at these caps

A prefix with w counted turns has at most 2(w+1) atomic steps: straight
continuation can occur only at isolated A subdivision points. An accepted
recursive endpoint also obeys the closure-distance bound. Therefore its
Chebyshev displacement from the root is at most

    min(2w+2, 2(WMAX-w)+1) <= WMAX+1.

The root coordinates are at most one. The next proposed endpoint and each
new local tile vertex are within one additional coordinate unit. All array
vertex coordinates therefore satisfy |x|,|y|<=WMAX+3.

For WMAX<=26, this is at most29. visited/vin use offset48 in96 entries, so
indices lie between19 and77. Tile centroids are represented by sums of
three vertex coordinates; with offset144 their indices lie between57
and231 in300 entries. Prefix arrays of length300 are also ample: no prefix
at these caps needs more than 2WMAX+3 atomic vertices. These inequalities
cover tested intermediate candidates, not only eventual valid polygons.
Thus no out-of-range access or implicit clipping removes a valid room at
W22, W24 or W26.

The host's long is64 bits, so the recorded multi-billion node counters do
not overflow. Exact point-in-polygon products are also far below overflow
at these coordinate bounds.

## 8. Terminal check and fixed controls

After closure, every boundary lattice vertex remains visited, and every
non-A visited vertex has a genuine turn. The integer horizontal-ray winding
test visits every non-boundary lattice point strictly within the bounding
box. It rejects any non-A interior point and requires at least two distinct
interior A points. Boundary points are skipped by visited flags, avoiding
an ambiguous point-on-edge convention. Output prints only nonzero-turn
vertices and therefore counts maximal straight walls.

Eight D4 images each of the frozen24- and34-wall parity rooms pass the full
prescribed-boundary replay, all pruning checks, the terminal check and
rollback. Eight D4 images of Jain28 pass the boundary/parity checks but are
correctly rejected at the terminal two-interior-A test: that room has only
one interior A mark. No room search is involved in these24 controls.

The sanitizer harness includes the frozen source under a renamed unused
main. Its compile warning about a missing return concerns that renamed
function; the original C main has the language's implicit zero return.
It is not an execution failure or a search-code change.

## 9. Completed binary versus the audited source

The current enum2.c was edited after the completed enum2 binary. This was
reconciled by reconstruction rather than ignored:

1. Compiling the frozen current source with clang -O2 reproduces enum3's
   complete disassembly.
2. Removing only the optional argv[3] initial-direction partition produces
   the archived reconstruction inputs/enum2-pre-direction-split.c.
3. Compiling that source with clang -O2 reproduces completed-run enum2's
   complete disassembly.
4. binary-compare.py verifies byte equality of every executable and data
   section, identical zero-fill layouts and identical indirect-symbol
   bindings for both pairs. Mach-O UUID/signature/link-edit bookkeeping is
   deliberately outside this comparison.

The pre-split file is explicitly a reconstructed source with verified
executable equivalence; it is not represented as the recovered historical
source file. The DFS, pruning, geometry and terminal check are unchanged.
The later direction partition is inactive with the ordinary two arguments.

## Reproduce this audit

Run check.py and binary-compare.py from this directory's parent workspace.
The frozen harness/build and disassembly artifacts are retained. Rebuilding
uses clang -O1 -g -fsanitize=address,undefined for the small harness, and
clang -O2 for the two source/binary reconstructions. No exhaustive run is
part of this audit.

Inputs are hashed in inputs/receipt-manifest.json and manifest.json. Outputs
are check.json, binary-compare.json, cases.jsonl and fixed-controls.log.
