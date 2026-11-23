# D79: Referee review of the eight-sheet note

Date: 2026-11-19. Target: `.context/qclass-closure/bbbb/eight-sheet.md`. Context read:
`three-sheet.md`, `low-valency.md`, `midpoint-necessity.md`, `d78-review-valency/review.md` and
`verify.py`, `d4-monodromy-blocks/monodromy.py` (sheet labels), and `d4-monodromy-blocks/task1_room22.*`.

Own code: `verify.py`, log `verify.log`. It reads cell sets only: `cyl.rooms()` (the 10 named rooms
plus the 4581 saved normalized rooms in `d64-finite-case/data/covers.json`) and four hand-built
rooms defined in the script. It rebuilds the edge involutions and d78's corner permutations from
cells. There's no search over rooms, rays, directions, or reflection words. CPU: under 1 s.

Re-run: `cd .context/illumination-generalization-2026-11-06/fable/directions-2026-11-09/d79-review-eight-sheet && python3 -B verify.py > verify.log`

## Verdict

**Sound, with minor fixable gaps.** Steps (a) to (d) are correct. The defects are wording and
missing pointers to where strict simplicity enters. No fatal finding.

## 1. Sheets versus cells

- Under D0, the degree-n cover Q → B has one sheet per cell: `monodromy.py` keeps one top face
  per tile, and d78's `g_x` uses the checkerboard side. At an interior mark S of class a, `g_a`
  acts on the 4 cells of the star as two 2-cycles (the two lifts of S). So "sheets incident to S"
  is the 4-cell star, and the count 8 is right. The stars of distinct same-parity marks are
  disjoint.
- `g_x = H_j V_i` or `V_i H_j` for x = (i,j). `verify.py` asserts this for all 4591 saved rooms.
  The order varies by class and room (4 patterns seen), so the note's "up to inverse" is needed
  and sufficient. G is the even subgroup of W: `V_0 V_1 = (V_0 H_0)(H_0 V_1)`. Correct.
- three-sheet.md's residual is a block of size k = 8 containing all 8 incident cells, so the block
  is exactly those 8 cells. That matches this note's hypothesis. This note needs neither
  maximality nor normalization.

## 2. Step (a), propagation

- `V_i` (i = S_x mod 2 = T_x mod 2) swaps the cells across x = S_x and x = T_x, so it fixes A.
  It normalizes G, so it maps the system {gA} to itself. G and `V_i` generate W. Correct.
- If an edge generator maps C to D ≠ C, no cell of C is fixed, so every cell takes its grid
  move. Reflection through an integer line keeps the parity of the crossed edge, and T − S is
  even. So D has the same offsets around S and T, not only "some 4 cells". The inward move at
  u = 1/2 lands back in C, so it can't occur when D ≠ C. Wall cells and reflex corners only
  affect moves with D = C, which step (b) treats separately. Correct.
- The 8 cells of each block are distinct: an overlap needs T_x − S_x = ±2u (odd) or S = T.

## 3. Step (b), parity

The y-multiset argument covers moves with D = C. Horizontally adjacent cells with opposite labels
give S_y − T_y ∈ {0, ±2v}, with 2v odd and S_y − T_y even, so S_y = T_y. Correct. A
consequence the note doesn't state: when D ≠ C the move preserves labels. So cross-label
adjacencies only occur inside one block. The room is R_S ⊔ (R_S + (T − S)), with R_S symmetric
about both axes through S.

## 4. Step (c), mirror

The conclusion is a reflection of the planar cell set. Each block is invariant under reflection
in y = S_y, and the blocks cover every cell. It isn't only a deck symmetry, and it can't be a
translation or a half-turn. (The reflection does also induce a fixed-point-free deck involution,
which gives a size-2 block system refining the size-8 one. That's consistent with three-sheet.md.)

## 5. Step (d), enclosure

The folding loop has winding number ±1 about a missing point X on the line. The argument
requires only that the open room is simply connected and invariant under the reflection. It
proves the closed segment lies in the open room. This excludes a wall along the line, which
would be a two-sided slit, and a reflex corner on the segment. "See" holds in the strongest
sense. Correct.

## 6. Combined statement

For a normalized room with n ≥ 120 and r ≤ 8, three-sheet.md gives d = n − 1 (primitive, n > 64),
or d ≥ n − k ≥ n − 8, or the 8-cell block. This note makes the last case directly visible. So
"directly visible or d ≥ n − 8" follows. The budget arithmetic checks: 2d ≥ 2n − 16, J ≤ 16,
and each class has R ≥ 2n − 32 − 3⌊n/2⌋. That's 28 at n = 120 and 30 at n = 121.

## 7. Saved-data checks

- **Named rooms.** None of the 10 named rooms has an 8-cell block for any same-parity interior
  pair. The minimal block containing the 8 cells is the whole room in each case.
- **R22.** For the dark pair (0,0), (2,2), the minimal block is all 15 cells. The hypothesis
  fails, as the contrapositive requires.
- **Saved covers.** Among 12185 same-parity pairs in the saved list, 3 pairs have an 8-cell
  block: cov3397 (n = 24), cov3608 (n = 24, the transpose), and cov4474 (n = 32). In each one,
  W permutes the blocks, every block has the claimed shape, the room is mirror-symmetric, and
  the segment lies in the open room.
- **Hand-built.** `bar24` is an 8 × 2 bar with four 2 × 1 bumps. It has S = (0,0), T = (4,0),
  r = 8 (all reflex corners of class (1,1)), and m = 3 blocks with offsets (½,½), (½,3/2),
  (3/2,½). Its transpose and two rectangles also pass. So the hypothesis is realizable below
  area 120.

## Findings

1. **Low.** Section 1 says V_i "crosses the vertical edge of the cell whose x-coordinate has
   parity i". Cell-center coordinates are half-integers. It should say "the vertical edge whose
   x-coordinate has parity i".
2. **Low.** Strict simplicity enters twice: edge-connectivity of the cell graph (step b) and
   simple connectivity of the open room (step d). The note names only the second. For example,
   two 2 × 2 squares meeting at a corner (S = (0,0), T = (2,2)) are not edge-connected, and S
   and T don't see each other. State both uses.
3. **Low.** The lemma statement says "a single block of the room-double monodromy". Say "a block
   of some G-invariant partition" and note that maximality and normalization aren't used. Only the
   combined n ≥ 120 statement needs them, through three-sheet.md.
4. **Info.** Moves between distinct blocks preserve the S and T labels. So the room splits as
   R_S ⊔ (R_S + (T − S)). This is a stronger structural conclusion, and future notes may find it
   useful.
5. **Info.** The three positive examples in the saved covers (n = 24, 24, 32) could replace the
   hand-built example as named controls.
