# Research directions toward universal 22-wall minimality

Fable 5.2, 2026-11-09. Requested by Daniel. Peyton leads the dark-room work.

Status of every claim in this memo: hand-derived in one session, **not
independently reviewed**. Treat each lemma as a candidate. No search was run.
No novelty is claimed.

## Summary

- The restricted theorems are solid. The universal step is blocked, and the
  blocked routes all share one cause: they try to prove light exists without a
  structural description of darkness.
- Three items in the record are overlooked and cheap to test. One of them can
  disprove the target, so test it first.
- The stated target, minimality over all polygons, includes irrational
  polygons. No existing mathematics reaches them. Restate the target as
  rational polygons.

## Progress assessment

Established and reviewed inside the project:

- Sharp restricted minimum: `W <= 21` and `k <= 6` implies every interior A
  pair is lit (64 DRAT refutations, 193,480 guards).
- All real orthogonal rooms with `W <= 8`, the exact 12-wall corridor, comb
  and long-neck families, restricted 10-wall spirals.
- Fixed-support surplus layers 0 to 4 with bounds 13, 37, and 32 reflections.
- Whole-copy parity-fold minimum (R21).

Blocked or retired:

- Family-by-family construction does not converge toward `r <= 8`. Each
  family costs weeks and leaves the general room untouched.
- Affine transport needs the full affine group. The bound
  `min |DF(-d, d-1)|_1 = 2d - 1` is unproved and unrefuted.
- The discharging potential has no inequality. The `r = 9` control shows
  periodic cancellations that any potential must absorb.
- Finite blocking, monodromy-generator transitivity, limiting arguments, and
  covering reductions for spirals are retired.
- Both Codex goals (author `01a18403`, reviewer `01a1a00f`) are blocked on
  mathematical impasses, not on effort.

Diagnosis: every blocked route is a lit-side argument. The record contains no
W-independent statement of what a dark room must look like. Directions 2 to 4
supply candidates for that statement.

## Scope correction

Universal minimality over all polygons is not provable with known tools.
Illumination in irrational polygons is open even for triangles. Every dark
example in the literature is rational.

Use this target ladder instead:

1. Orthogonal lattice rooms (the `r <= 8` problem).
2. All lattice-tiling rooms: the (2,4,4), (2,3,6), (3,3,3), and rectangle
   reflection tilings. These are exactly the torus-cover cases in Apisa–Wright
   Proposition 3.11.
3. All rational polygons. The non-torus-cover case reduces to periodic points
   and `Q_min` identifications by Apisa–Wright and Eskin–Filip–Wright. The
   record mentions `Q_min` once and never uses it.

Step 2 is larger than the project's working scope. The record treats step 1
plus canonical45 as the whole arithmetic case. Direction 1 shows why that
matters.

## Direction 1: the 30-60-90 model is over-constrained

**Finding.** `.context/illumination_306090.py` line 121 requires every
occupied B (60 degree) and C (90 degree) lattice point to be an absorbing
corner. Only C points need to block.

**Derivation.** Let `L` be the triangular lattice of A (30 degree) points.
B points are triangle centroids. C points are edge midpoints. The three
nonzero classes of `(1/2)L / L` are all edge midpoints. So the midpoint of
every primitive A-to-A segment is a C point. A B point lies on such a segment
only at a one-third point, and the C midpoint still blocks the segment.
Contrast the square case, where primitive midpoints fall on both B and C.

**Consequences.**

- The recorded result "infeasible for `W <= 21`, radius 3" covers only the
  strict model. It says nothing about rooms with transparent B points.
- The model has no fold or seam-reversal rule. The 22-wall room needs that
  rule in the square tiling, so the 30-60-90 model also excludes the analogue.
- A relaxed room has fewer forced corners. It can have fewer than 22 walls.
  If one exists, the universal target is false as stated.

**Evidence that the relaxation is not vacuous.** A 12-wall pinwheel exists:
the 12-tile hexagon around one A point plus one tile on each side. It has six
270 degree C corners, six 30 degree corners, and no transparent C point. It
has one interior A point, so it is not a dark room. It shows C-clean rooms
are cheap.

**First step.** Rerun the existing search with B points free and with the
seam-reversal rule added. Run the same relaxation audit on the (3,3,3) and
rectangle tilings. This is a room discovery search. It needs Daniel's
approval under `GOALS.md`.

**Falsifier.** A relaxed exhaustive search at `W <= 21` that returns
infeasible supports minimality for the (2,3,6) tiling. A feasible room
disproves the universal target.

## Direction 2: structure conjecture, dark implies parity factor

**Conjecture (W-independent).** Let `DP` be the double of a lattice room
with a dark pair `S`, `T`. Then a half-translation cover `phi: DP -> N`
exists onto a flat sphere `N` such that:

- `phi(S)` and `phi(T)` are A-class points of `N`, and
- every midpoint-class lattice point of `N` is non-regular (cone angle is
  not `2*pi`).

`review/fold-route-contract.md` states this only for `W <= 21`, where it is
logically equivalent to the main theorem. The W-independent version is
stronger, and dark rooms at `W >= 22` can refute it. The 327-class census at
24 to 26 walls was a parity-family census, so it does not test the
conjecture.

**Riemann–Hurwitz threshold.** `DP` has cone angles `pi`, `2*pi`, `3*pi`
only. A cover of degree `delta` is unramified over simple zeros of `N`, and
`N` has no higher zeros. So

    r = delta * z_N + #(reflex corners over poles of N).

For a genus-0 base with `p_a` poles, `R_a` regular points, and `z_a` zeros
over the A class, and `Z'` zeros elsewhere, the count gives

    Z' = p_a + (3/2) R_a + 2 z_a - 1.

Check: the five-square staircase has `p_a = 1`, `R_a = 2`, `Z' = 3`. The
22-wall room has `delta = 3`, `z_N = 3`, so `r = 9 = 3 * 3`.

For `r <= 8`, the only cases are
`(delta, z_N)` in `{(2,2), (2,3), (2,4), (3,2), (4,2)}`, plus `delta = 1`,
which the `k <= 6` theorem covers. Area is bounded, so the check is finite.
R21 reaches the same count for polygon folds. The extension to bases that
are not polygon doubles is the open part.

**Why this matters.** If the conjecture holds, universal minimality for
lattice rooms reduces to that finite check. The whole difficulty moves into
one implication: dark implies factor.

**First step.** Ask the Codex reviewer to re-derive the two displayed
formulas and the case list from scratch. No search is needed. Then test the
conjecture by exhaustive enumeration of dark pairs at `W = 22`, which needs
Daniel's approval.

**Falsifier.** One dark room at any wall count with no such factor.

## Direction 3: two mechanisms of darkness

Darkness has two logically separate sources:

1. **Torus-level blocking.** Every straight candidate hits a corner image on
   the torus (Tokarsky parity).
2. **Sheet-arrival failure.** Clean directions exist, but no clean
   trajectory arrives on a sheet over `T`. The Heisenberg 27-square control
   is this type.

**Candidate lemma (torus level).** Normalize vertex coordinates to gcd 1 per
axis, and let `F` fold the room onto the pillow `[0,1]^2`. Every straight
candidate is blocked at torus level if and only if `F(S) = F(T)` is a pillow
corner.

Sketch: with `L = Z^2 + Z s + Z beta`, a coset `beta + 2 Z^2` contains an
`L`-primitive vector unless some prime `p` puts the coset inside `pL`. An odd
`p` forces `L / pL` cyclic, which is impossible. Only `p = 2` survives.

**Consequence.** For a pair in generic rational position, clean directions
always exist. Darkness there is pure sheet-arrival failure. No planar room
with that mechanism is known.

**Target.** Prove that a planar room has no pure sheet-arrival darkness. The
unused input is planarity: `DP` is a sphere, so its monodromy is a genus-0
constellation with a real structure. The Heisenberg control is not planar.
This target also extends the theorem from A pairs to all rational pairs.

**First step.** Review the lemma. Then list which hypotheses of the
Heisenberg control fail for a genus-0 constellation with hexagonal faces.

**Falsifier.** A planar room with a dark pair whose fold image is not a
pillow corner.

## Direction 4: monodromy block systems as a dichotomy

The unfolding has monodromy group `G <= (Z/2)^2 wr S_n`. Block systems of
`G` correspond to intermediate covers, which are the factors in direction 2.

Fable's earlier note used block systems only to reject a route. Use them as
a dichotomy instead:

- `G` primitive on sheets, or large in a precise sense, implies lit.
- `G` imprimitive supplies a factor, and direction 2 applies.

This turns "dark implies factor" into a permutation-group statement. Both
the restricted theorem's 64 refuted supports and the 22-wall room are data
for it.

**First step.** From existing certificates only, compute the block systems
for the 22-wall room and for the Castro and Tokarsky rooms. Confirm each has
the block system that direction 2 predicts. This reads saved artifacts and
is not a discovery search.

**Falsifier.** A dark room whose sheet monodromy is primitive.

## Direction 5: cylinder and Siegel–Veech forcing

No file in the record mentions Siegel–Veech constants. The reformulation:
a pair is dark if and only if its pair Siegel–Veech constant is 0.

Usable facts:

- Each direction has at most `2r` cylinders, and the cylinder data satisfy
  `sum m_i n_i = 2d`.
- In a one-cylinder direction with `S` on a regular core leaf, the leaf
  passes every A lift, so the pair is lit.
- Darkness therefore forces a zero onto the lattice level of `S` in every
  one-cylinder direction.

Each forcing consumes reflex corners. This is a counting route to `r >= 9`
that differs from the discharging potential, because it counts over
cylinder decompositions and not over slopes of one arc.

**First step.** Prove or refute by hand: every square-tiled room double with
`r <= 8` has a one-cylinder direction. Known origami results on one-cylinder
directions are the place to start.

**Falsifier.** The `r = 9` room must have no clean one-cylinder direction.
Check this on the saved 10,368-state certificate.

## Direction 6: omitted value of the exponential map

`T` is an omitted value of the exponential map at `S`. Near `T`, lit points
form half-disks bounded by generalized diagonals through reflex corners.
Each incoming ray at a reflex corner has two continuations. Count the
half-disks needed to leave `T` uncovered.

This direction is undeveloped. Its value is that it does not use the
lattice, so it is the only candidate that can reach non-arithmetic rational
polygons without Apisa–Wright. Do not start it before directions 1 to 3.

## Ranking

| Rank | Direction | Cost | Needs approval | Can refute the target |
| --- | --- | --- | --- | --- |
| 1 | Relaxed 30-60-90 search | Low | Yes, discovery search | Yes |
| 2 | Dark implies parity factor | Medium | Review no, `W = 22` census yes | Refutes the conjecture only |
| 3 | Two mechanisms, planarity | Medium, hand | No | No |
| 4 | Block-system dichotomy | Low first step | No | No |
| 5 | Cylinder forcing | Medium, hand | No | No |
| 6 | Omitted value | High | No | No |

## Routes to stop

- More room families (combs, spirals, staircases).
- Slope-by-slope discharging without a structural input.
- The full affine bound, until direction 2 says which surfaces matter.

## Review requests

- Codex reviewer `01a1a00f`: audit the midpoint derivation in direction 1,
  the two formulas and case list in direction 2, and the sieve lemma in
  direction 3.
- No request to the author goal until Daniel chooses a direction.

## Decisions

- 2026-11-09, Daniel: "minimal" means strictly simple rooms. Pinched (weakly
  simple) and slit rooms are out of scope. Wolecki's published 22-gon is
  pinched at (2,0), so it is outside the target class; see
  `directions-2026-11-09/lit-tokarsky/findings.md`.
- 2026-11-09, Daniel: approved the relaxed 30-60-90 discovery search and
  subagent parallelization with Fable as coordinator.

## Corrections after audit (2026-11-09)

- Direction 3, candidate lemma: false as stated, and the sieve sketch is
  invalid. See `directions-2026-11-09/d3-two-mechanisms/audit.md` for the
  corrected lemma.
- Direction 4: "G primitive implies lit" is false. See
  `directions-2026-11-09/coordinator-log.md` for the corrected dichotomy.
- Progress assessment: the sharp restricted minimum covers interior A pairs
  only. Rational non-A pairs are unproved for 9 <= W <= 21 outside the
  family theorems.
- Direction 2: the formulas and the r <= 8 case list are correct, but the
  conjecture must require phi(S) != phi(T) and must include class B. No
  finite check remains at r <= 8; the k <= 6 theorem covers every case. The
  exact open statement is the same-fibre conjecture in
  `directions-2026-11-09/coordinator-log.md`.
- Direction 1: the C-clean 30-60-90 minimum is 27 walls, so this class does
  not beat 22. Rooms with transparent C points are under search.
