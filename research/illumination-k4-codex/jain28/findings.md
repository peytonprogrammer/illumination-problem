# Spider's home: boundary-pair darkness and local rigidity

Status: independently accepted by Opus (2026-11-01).

## Result and limits

The idealized square-grid reconstruction of Jain's published Spider's home
has 28 walls and 16 unit squares. Its center is dark to each of four long-wall
midpoints. A finite exact certificate establishes local rigidity of each
center–midpoint pair among nearby simple orthogonal rooms with the same cyclic
edge directions and marks allowed to move in the closed room. The dark
configurations in that neighborhood are exactly positive axis-affine images
(translations and independent horizontal/vertical scales).

This tests a boundary-mark example. It does not lower the wall count for two
interior marks, prove global isolation, or establish the global minimum.
Original author coordinate files were not recovered; equal unit-square grid
spacing is an explicit idealization of the published raster, supported by
the video's square-construction description. The theorem is about room.json.

## Source and reconstruction

Jain's author project index links George Tokarsky's video
https://www.youtube.com/watch?v=ahm4knwln7I, “The Spiders Unilluminable home.”
The description credits Bhavya Jain, states the center and four midpoint
marks, and gives the square ABCD rule. The thumbnail supplies the outline.

`reconstruct.py` transcribes the outline onto a six-by-six unit grid, checks
all 36 cell centers against thumbnail colors, constructs its square union,
and checks that the boundary is one degree-two cycle with 28 maximal walls.
The center is (0,0); targets are (±2,0),(0,±2). `darkness-check.py` verifies
that every non-even-even grid vertex in the closed polygon is an actual
corner. The proof in darkness.md then excludes every positive-length finite
path by the first primitive lattice point of the unfolded segment. It also
excludes positive-length returns to the center. No sampled rays establish
this darkness conclusion.

## Certificate

The chart has 34 coordinates: two anchor coordinates, 28 positive edge
lengths and four mark coordinates. Two closure equations leave dimension
32. The certificate combines 181 signed one-corner event rows and one active
boundary row. Exact rank is 28; the common kernel has dimension four and is
exactly the axis-affine symmetry span. All 182 rational dependence weights
are strictly positive, and their sum of rows is exactly zero modulo closure.

The boundary constraint is h=n·(t-v_wall)>=0, with the wall anchor moving
along with the polygon. The target remains away from the wall's endpoints.
The event constructor includes target time equal to final wall time, stopping
before appending that wall reflection. The limiting final approach is
transverse. The local argument is stated explicitly in darkness.md.

`certificate-check.py` rebuilds every supplied reflection word and its endpoint
map, verifies its unique intermediate reflex-corner image, and recovers all
6,154 derivative coordinates by exact quadratic differences. It checks rank,
the four symmetries and all positive dependence coefficients over fractions.
The LP only proposes a basis; no floating-point identity proves the result.

The first boundary target suffices: the square union is invariant under a
quarter turn, checked exactly. Rotation carries this certificate to each of
the other three marked midpoints.

## Local proof

A dark admissible deformation satisfies h>=0 and every signed corner
determinant f_i>=0. At the base all these expressions vanish. Normalize the
first vertex and first two edge lengths by translation and axis scales;
the edges are perpendicular. The resulting slice has dimension 28. Exact
rank makes the combined row kernel zero on that slice. A positive dependence
therefore ensures that every nonzero slice vector has a negative row value.
By compactness of its unit sphere, this negativity has a uniform margin.

Each determinant has a quadratic remainder. The boundary function is linear.
For a sufficiently small nonzero slice displacement, either h<0, contradicting
admissibility, or some f_i<0, giving an illuminating connection through that
event's valid word. All other finite-word contacts persist by strictness;
the smooth boundary endpoint is covered by h>=0 and transversality. Hence no
such dark displacement exists. Conversely, positive axis-affine maps preserve
orthogonal billiard paths, corners and boundary incidence, so they preserve
the parity-proved darkness. The neighborhood radius is not computed.

## Construction history and controls

Radius 6 supplied 16 events, rank 14 with the boundary row. Radius 12 supplied
80 events and full rank 28 but failed positive span. `cone-witness.json`
contains an exactly checked non-affine vector satisfying those 81 inequalities,
with 73 tangent and eight strict. This is only a witness against that finite
certificate, not a dark deformation. Radius 18 supplies 181 events and the
exact positive dependence. No larger direction bound or room search was run.

`validate.py` checks every event-specific descending deformation with the
target on its moving wall, then tests exact fixed-word predictions for a
wall-tangent perturbation and an inward target perturbation. All 543 controls pass: 181 event-specific descents and 362 additional
predictions, including inward endpoint motion. These controls corroborate the local event signs;
the written local proof and finite algebra supply the theorem.

## Reproduce

```sh
uv run --with pillow python -B .context/illumination-k4-codex/jain28/reconstruct.py
python3 -B .context/illumination-k4-codex/jain28/darkness-check.py
python3 -B .context/illumination-k4-codex/jain28/boundary-check.py
python3 -B .context/illumination-k4-codex/jain28/certificate-check.py
python3 -B .context/illumination-k4-codex/jain28/validate.py
```

Frozen-certificate replay requires no LP or direction construction. The
construction-only commands are rigidity.py 18 and positive-span.py (the latter
uses the existing illumination-venv OR-Tools installation). Shared imports
are Codex's earlier event_geometry.py and check.py; no Opus executable is used.


## Independent acceptance

Opus independently replayed the boundary-target construction and accepted
the proof. His R18 certificate contains 182 optical events (one more axis
direction than Codex's 181), plus the active boundary normal. All 181 Codex
unfolded endpoints match his events. Both certificates have rank 28 and an
exact positive dependence; his 725 inward-endpoint predictions agree. His
R12 certificate also has full rank but no positive dependence, consistent
with the exact surviving cone vector here. He separately confirmed quarter-
turn symmetry and the parity darkness argument. This acceptance retains
the thumbnail-reconstruction and boundary-mark limitations.
