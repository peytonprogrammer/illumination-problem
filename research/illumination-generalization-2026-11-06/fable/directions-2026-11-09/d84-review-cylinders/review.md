# D84: review of adjacent-cylinders.md and convex-cylinder.md

Date: 2026-11-20. Reviewer: independent referee. Files under review are in
`qclass-closure/bbbb/`.

## Verdicts

- **adjacent-cylinders.md: sound with fixable gaps.** The rim test, the path, the
  midpoint and its class are correct. The U2 family passes at every k. All 23 new
  certificates replay. The gaps are wording and code scope, not mathematics.
- **convex-cylinder.md: sound.** The one-cylinder theorem and its parity scope are
  correct. U2-type rooms (three reflex classes) are outside its scope, as stated.

## Findings

1. **Minor, theorem statement.** "M has two cylinders exchanged by τ" must mean that
   these two are the whole decomposition. Otherwise the Q-cylinder doesn't fill Q and
   the "every pair is lit" proof fails. Say "exactly two".
2. **Minor, code scope.** Claim (1) is proved for any height H. rim-trees.py handles
   only H = 1: for H > 1 its `index[...]` lookup raises. That covers every normalized
   room, which is the only use. State the restriction.
3. **Minor, conservative test.** `complete()` drops one point from an arc longer than
   C. This can only cause a false failure, never a false pass. No saved case is
   affected.
4. **Minor, wording.** The midpoint can be a smooth wall point (incid 2). That is
   regular in d82's sense, but the note should say so.
5. **Note, replay semantics.** Both the authors' check and mine accept any of the
   four sign flips, in either direction. This certifies a legal off-class path. It
   doesn't certify the particular chart construction. The 747 count only needs the
   first.
6. **Note, edge count.** 2r + 2 counts tree edges. Building the trees still needs the
   area-dependent cylinder computation. The stored coverage loop runs over 2C samples,
   but an exact interval merge is O(r log r).
7. **Note, outside the reviewed files.** The d69 `decomp.py` comment gives U2 r = 4.
   The actual value is r = 3, at (2,2), (7,2) and (7,5).

## What I checked

**(a) Rim geometry.** On Q the open cylinder is embedded and its core separates the
sphere. So each side's critical graph is connected and acyclic (a cycle would bound a
face with no cylinder). Both sides of each edge face the one cylinder, so the gluing
is (x, y) ↦ (i + m − x, 2H − y). The point i + t pairs with m − t, where m is the image
of i. The arc (i − m, i − m + 2(j − i)) is right. It is open because endpoints are
corners. Wrapping edges are handled by developing j. The test samples every integer
and half-integer difference. For open arcs with integer endpoints, that is exactly
equivalent to covering (0, C).

**(b) Path.** The return leg has the negated velocity, so the travels are Δ and −Δ.
That gives s − t ≡ 2z − i − m. On M the path is straight with displacement (2Δ, 2H).
So z is the half-time point. Both open legs are inside the cylinder. The exchanged
cylinders contain no convex lifts, so no corner is hit.

H = 1 follows from three facts:

- The tops of A glue only to the bottoms of B. Self-gluing would join the two
  disjoint trees.
- The transverse coordinate mod 2H is therefore global.
- Twice each wall vector is a period, and the wall gcds are 1, so 2 is a period.

Same-class marks lie on one tree, because transverse parity is a function of the
class. Δ is an integer because the unfolded image of T is congruent to S mod 2. So
the midpoint is a lattice point of the other transverse parity, which is off-class.

**(c) Continuum.** The hypothesis is that each rim's arc union contains every nonzero
difference mod C. rim-trees.py checks that exactly. The open-cylinder, opposite-rim
and same-rim cases cover all pairs, including critical-graph pairs.

**(d) Count.** A tree with t reflex points (valence 3) and convex leaves (valence 1)
has t + 2 leaves and 2t + 1 edges. Summed over both sides, that's 2r + 2. U2 gives
5 + 3 = 8. R22 gives 7 + 13 = 20 = 2·9 + 2.

**(e) U2 family, own code.** indep.py doesn't use cyl.py's SL2 action, τ propagation
or tracer. It reads each rim by tracing an offset billiard ray (offset η = 1/1000003
toward the next lattice leaf) and recording lattice and half-lattice Q-points.
Results for k = 0 to 6:

- Each room is strictly simple and normalized, with 10 walls and r = 3.
- All four classes are present.
- Both rims are trees with C = 2n = 92 + 16k, and both rims pass.
- Origin-free (i − m, j − i) multisets equal rim-trees.txt's linear formulas at
  k = 0, 1, 2, 3 and 5.

For every k, rim 0 has arcs (0, 30+8k), (8, 58+8k), (34+8k, 84+16k) and
(62+16k, 92+16k), and the union is the whole circle minus 0. Rim 1 has
(0, 58+8k) ∪ (34+8k, C), and 58 + 8k > C/2. The insertion argument is sound:

- The column x = 7/2 lies only in the bar.
- A phase shift of 4k is a whole number of vertical periods.
- No corners are added.

At k = 0, 1 and 3, I built the rim path for every same-class interior lattice pair
(52, 80 and 160 pairs) and traced it. Every path reaches T, avoids all corners, and
has an off-class lattice midpoint. 52 matches the saved U2 pair count. 91, 120 and
190 non-lattice critical-graph pairs (abscissa n + 1/3) also trace correctly. The
stretches aren't claimed BBBB, but all four classes are present and the area is above
4r + 4.

**(f) Saved pairs.** adjacent-cylinders.py, rim-trees.py and convex-cylinder.py
reproduce their .txt files exactly. My tracer certifies all 23 new pairs, including
the 3 explicit DBw2 paths with midpoints (4,1), (10,5) and (10,3). It also certifies
all 37 pairs that convex-cylinder.md added: 687 + 37 + 23 = 747.

**(g) convex-cylinder.md.** The case analysis is complete. In the rim-rim case, the
midpoint is τ-fixed only if s ≡ t. The parity scope (H = 2, reflexes on one affine
parity line) is correct. U2's reflexes are in classes (0,0), (1,0) and (1,1), so U2
is outside it. My walk confirms that DBas in direction (−4,1) and the 58-cell bay room
each have one Q-cylinder:

| Room | C | Bottom tree | Top |
|---|---|---|---|
| DBas | 96 | 4 reflex, 6 convex | 2-leaf folded segment |
| 58-cell bay room | 116 | 8 reflex, 10 convex | 2-leaf folded segment |

The bay-insertion argument is informal, but the A = 2, B = 3 case matches it.

**(h) R22.** In both (4,7) and (7,4), both rims are trees with C = 30, and both fail.
One rim has 15 uncovered half-unit differences, starting at 4. The other has 33,
starting at 2. A failed test only leaves a room undecided. The note claims nothing
more: its "as a dark pair requires" is the contrapositive of claim (1).

## Re-run

`cd .context/illumination-generalization-2026-11-06/fable/directions-2026-11-09/d84-review-cylinders && python3 -B indep.py > indep.log`
(3.1 s CPU). This uses only named rooms, the U2 stretch family and saved D72 pairs.
