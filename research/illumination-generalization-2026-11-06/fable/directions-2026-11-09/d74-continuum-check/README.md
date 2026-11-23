# d74: independent continuum check of the area-15 result

Date: 2026-11-19. This directory re-verifies Astra's area-15 continuum claim with new code.
It was written from `d13-cylinder-cover/theory.md` (Lemma A') and `qclass-closure/off-grid.md`
prose only. No code of Astra's checker or of d13 was read. It reuses `d67-review-d64/indep.py`
(exact lattice billiards) only to replay residual lattice pairs.

Tags: **PROVED** (argument in this file), **COMPUTED** (script and log here), **GUESSED**.

## Verdict

- **The six hard area-15 rooms are fully certified (COMPUTED).** No pair of distinct interior
  points is left, apart from one lattice pair in room 1. That pair is lit by an explicit exact
  path. This independently confirms Astra for these six rooms.
- **R22 control passes (COMPUTED).** Both implementations leave exactly one residual pair,
  (1,3)-(3,5) in file coordinates. No 1- or 2-dimensional residue remains. Direction (4,7) is a
  one-cylinder direction.
- **The two 18-cell rooms aren't certified (COMPUTED).** The residue is 2-dimensional. It sits in
  small neighbourhoods of corner pairs, and they match Astra's 18 open tile pairs per room.
- **No disagreement with Astra was found.**

## Files

- `geom.py`: room reading, the DP-cylinder labels of one direction (`Direction`), exact convex
  clipping, and an exact rational billiard tracer (`trace`, `lit_pair`).
- `certify.py`: the certifier in Python with `Fraction`. It's slow and used for the R22 control.
- `cert.cpp`: a line-by-line C++ port. It uses exact rationals in int64 with int128
  intermediates, and aborts on overflow. Build it with `g++ -O2 -std=c++17 -o cert cert.cpp`. Run
  it as `cert ROOMFILE INDEX B [maxpieces]`. Set `D74ALL=1` to print every live piece.
- `validate.py`: checks Lemma A' certificates against `trace` by finding explicit paths.
- `poles.py`: the pole-pair test of Propositions O and O'.
- `cluster.py`: groups residual pieces by their nearest lattice point.
- `nearpoles.py`: path sampling near residual corner pairs. It's evidence only.
- Logs: `r22_B8.log` (Python), `r22_cpp_B8.log`, `hard15_<i>_B<B>.log`, `r18_<i>_B16*.log`,
  `r18_0_B24_aborted.log`, `eighteen_hard_B16.log`, `poles_r18_*`, `lattice_pairs.log`,
  `validate.log`, `nearpoles.log`.

Room files list `area walls x0 y0 x1 y1 ...`, with cells as lower-left corners. Indices count
from 0 in file order.

## Method

Fix the room P and a finite set Θ of directions (p, q) with 1 <= p, q <= B and gcd 1.

**Labels (one direction).** In a cell, the plus value is t = qx - py and the minus value is
s = qx + py. An open *band* is a strip k < t < k+1, or k < s < k+1, inside the open cell. An
*integer line* is t = k or s = k crossing the open cell. Each band and each line has two ends.
At each end the unoriented billiard flow continues in one of three ways:

- into the neighbouring cell, keeping the family and value;
- by reflection at a wall, which changes the family (the value formulas are in `reflect`);
- through a lattice point: straight on at an interior point, by reflection at a flat point.
  At a convex or reflex corner the end is *singular*.

Band midlines never meet lattice points. Union-find over flow links gives the line orbits. An
orbit is *singular* when it contains a singular end. A second union-find over band links, plus
merges across every non-singular integer line, gives the DP cylinders (labels).

For an interior point S, Λ(S) holds at most two labels. The plus label is the band label when
t(S) isn't an integer. When t(S) is an integer, it's the label of the merged bands if the line
through S is regular, and absent if that line is singular. The minus label works the same way.
K_D is the union of the closed bands, within closed cells, that carry label D.

**Pieces.** The state is a partition of int P into relatively open convex pieces of dimension
0, 1, and 2. The start is open cells, open interior edges, and interior lattice points. Each
piece f carries Q(f), a list of closed 2-dimensional convex polygons, each inside one closed
cell. Initially Q(f) holds every cell.

For each direction, each piece is split by the singular lines of that direction crossing its
relative interior, using its home cell. Each part reads Λ at one relative-interior point. Each
polygon W in Q is then replaced by the 2-dimensional pieces of W ∩ {i1 <= t <= i2} ∩
{j1 <= s <= j2}, over maximal runs [i1, i2] of plus bands and [j1, j2] of minus bands whose
labels aren't in Λ. When no part's Q changes, the direction is skipped for that piece and the
piece isn't split. A piece with empty Q is removed.

**Pruning.** A piece f is dropped when no live piece g has both closure(g) ∩ ∪Q(f) ≠ ∅ and
closure(f) ∩ ∪Q(g) ≠ ∅. A point piece is never paired with itself. This step is repeated. The
output is the remaining live pieces and their mutual partners.

## Soundness (PROVED, relying on Lemma A' and the Standard facts in d13 theory.md)

Write U(S) = int P \ Ill_Θ(S), where Ill_Θ(S) = ∪_{θ, D ∈ Λ_θ(S)} K_D.

1. **Labels are DP cylinders or finer.** Open bands avoid Σ, so each lies in one M-cylinder.
   Flow-adjacent bands lie in one DP cylinder: in M their lifts are adjacent in the same
   cylinder, or adjacent to its τ-image. A non-singular integer line is a regular closed leaf
   inside one cylinder, so both adjacent bands lie in it. So every computed label set lies
   inside one DP cylinder D, and its closed bands lie in K_D. Missing a merge only shrinks the
   computed K and keeps the method sound. A false merge would be unsound. Section "Validation"
   tests for that.
2. **Λ is read correctly and is constant on parts.** The lift of S on sheet (1,1) lies in an
   open cylinder exactly when its plus leaf is regular. That holds when t(S) isn't an integer,
   or when the line is a non-singular integer line. The label is then that leaf's label. Within
   a part, no singular line of θ crosses the relative interior. So t is either non-integer on
   the whole part, or the part lies on one integer line, or it crosses only regular integer
   lines. Labels agree across regular lines by step 1. So Λ_θ is constant on each part.
3. **Invariant (I1): U(S) ⊂ ∪Q(f) for all S in f.** This holds initially. Take T in W with
   T not in K_D for every D in Λ. Every closed band of T's cell that contains T has a label
   outside Λ. So T's t-value lies in a kept plus run and its s-value in a kept minus run, and T
   is in some new piece. The new U is open, and lower-dimensional pieces have empty interior. So
   dropping them keeps (I1). Skipping a direction for a piece keeps its old, larger Q, which
   still satisfies (I1) because Ill only grows.
4. **Removed pieces.** If Q(f) is empty, U(S) is empty for S in f. By Lemma A', S lights
   every T ≠ S.
5. **Pruning.** Let (S, T) be dark with S in f and T in g. By Theorem C(2), T is in U(S) and S
   is in U(T). Both f and g are live, because a removed piece has empty U. By (I1), closure(g)
   meets ∪Q(f) and closure(f) meets ∪Q(g), so f and g are mutual partners. A pruned piece has
   no live mutual partner, so its pairs are lit. Earlier-pruned pieces are lit in the same way,
   so later rounds may ignore them. All intersection tests are exact over-approximations
   using closed sets.
6. **Conclusion.** Suppose the output has no live pieces. Then every pair of distinct interior
   points is lit. Suppose instead the live pieces are all points. Then the only possibly dark
   pairs are the listed mutual point pairs (S0, T0). Each such pair is decided by an explicit
   exact billiard path (`lattice_pairs.log`), and such a path proves light by itself.

Arithmetic is exact. Python uses `Fraction`. C++ uses reduced rationals with int128
intermediates and exits with an error on any magnitude above 4e15. That never happened.

**Residues of measure zero.** No separate argument is needed. Segment and point pieces are
first-class pieces, with their own labels and Q. Lower-dimensional parts of U are absorbed by
(I1), because U is open.

## Validation (COMPUTED)

- **Explicit paths for certificates.** `validate.py` samples random rational S, a direction
  with p, q <= 5, and a label D in Λ(S). It then samples a random rational interior T in a
  closed band of D, endpoints included. It searches an explicit path with the independent
  tracer `trace`, over images up to radius 8. Over the named rooms there are 535 generic S and
  452 S on integer lines, regular or singular. All 987 certificates have an explicit path, and
  0 failed (`validate.log`). This guards against false merges.
- **Python and C++ agree on R22.** At B = 8 both leave exactly (1,3)-(3,5).
- **Easy rooms.** A 3 × 5 rectangle and a 5-cell L clear completely, at B = 3 in Python and
  B = 4 in C++.
- **R22 pair.** Neither `indep.py` (H <= 24) nor `lit_pair` (R <= 8) finds a path. That's
  consistent with the known dark pair.

## Results

### R22 (`qclass-closure/r22-control.room`)

The run used B = 8 (COMPUTED). Live pieces fall to 29 at direction (4,7), a one-cylinder
direction, and to 2 after it. The final residue is the points (1,3) and (3,5), each the other's
only partner. In manuscript coordinates this is (0,0)-(2,2): Astra's translated pair.

### Six hard area-15 rooms (`offgrid/fifteen-hard.rooms`)

| Index | Walls | B = 10 | B = 16 | Lattice pair replay |
|---|---|---|---|---|
| 0 | 20 | cleared | cleared | none |
| 1 | 20 | (2,1)-(4,3) left | (2,1)-(4,3) left | lit, direction (-2,3), both tracers |
| 2 | 16 | cleared | cleared | none |
| 3 | 20 | cleared | cleared | none |
| 4 | 18 | 3,308 live pieces | cleared | none |
| 5 | 20 | (1,2)-(4,5) left | cleared | lit, direction (1,-3) |

C++ CPU is at most 2.2 s per run. All six rooms are certified (COMPUTED, given the PROVED
soundness argument above).

### Two unresolved 18-cell rooms (`qclass-closure/two18/rooms`)

Not certified (COMPUTED). At B = 16, room 0 has 27,680 live pieces and room 1 has 30,434. At
B = 24, room 0 still has 104,900 after pruning. Every live piece lies in a small neighbourhood of one
of these lattice points:

- Room 0: convex corners (0,1), (0,3), (0,5), (0,7), (1,0), (1,8), (3,0), (3,4), (4,1), (4,3),
  and the flat point (1,4).
- Room 1: convex corners (0,0), (0,3), (0,5), (0,8), (2,7), (4,0), (4,3), the flat point
  (2,1), and the reflex corner (2,4).

The pole test (`poles.py`, p, q <= 16) finds the pairs below with no common cylinder in any
tested direction. Proposition O or O' then rules out covering their neighbourhoods with these
directions.

- Room 0, 15 pairs: {(0,1), (0,7), (4,1)} × {(1,0), (1,8), (3,0)}, and
  {(0,3), (0,5), (4,3)} × {(1,4), (3,4)}.
- Room 1, 6 pairs: {(0,0), (0,8), (4,0)} × {(2,1), (2,7)}.

Room 1 also keeps residue at {(0,3), (0,5), (4,3)} × reflex corner (2,4). Those pairs do share
a cylinder in some direction, but no sector-pair cover was found. Propositions O and O' don't
cover reflex corners.

Mapped to Astra's tile indices, these are exactly the 18 open tile pairs per room in
`eighteen-audit.txt`. The flat point (1,4) and flat point (2,1) each touch two tiles. Agreement
is COMPUTED, at the level of which corner pairs stay open.

Residue is 2-dimensional, so finitely many exact path checks can't close it. Sampling
(`nearpoles.py`) gives evidence only. It tried 72 random rational pairs within 1/20 of the
residual corner pairs and found explicit paths for 42 within image radius 10. The rest are
undecided, not dark. GUESSED: these pairs are lit, but proving it needs S- and T-dependent
directions without bound, which is the renormalization problem flagged in d13 Section 5.

### Extra (named file `offgrid/eighteen-hard.rooms`, 34 rooms, B = 16)

32 rooms are cleared or leave only lattice pairs, and those pairs are lit by exact paths:

- Index 18: (1,2)-(1,6) and (1,2)-(2,7).
- Index 25: (1,6)-(2,6) and (1,6)-(3,6).

Indices 26 and 27 are the two unresolved rooms above.

## Limits

- Directions are 1 <= p, q <= B. Axis directions aren't used. That only weakens the
  certificate.
- The skip rule, which forgoes a direction when no part improves, is a heuristic. It affects
  completeness only, not soundness.
- Lemma A', Theorem C, and Propositions O and O' are cited from d13 and are still unreviewed
  there. The soundness argument above depends on Lemma A' and Theorem C(2).
- CPU used in this directory is about 18 minutes in total. That includes one aborted B = 24 run
  of about 9 minutes, most of it printing partners.
