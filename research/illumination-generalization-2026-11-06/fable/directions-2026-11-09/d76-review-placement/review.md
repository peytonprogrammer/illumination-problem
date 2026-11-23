# D76: Referee review of the D58 double-resonance placement claim

Date: 2026-11-19. Target: `.context/qclass-closure/bbbb/placement.md`, `placement.py`, `placement.txt`.
Own code: `verify.py`. It imports only the D58 builder (`tests_lib.resonant`, `door_geom.DOOR`) for
room geometry. Column extraction, lattice basis, counting, the k ≥ 16 construction, and the
billiard tracer are new code. Log: `verify.log`. CPU: about 110 s in total.

Re-run: `cd .context/illumination-generalization-2026-11-06/fable/directions-2026-11-09/d76-review-placement && python3 -B verify.py > verify.log`

## Verdict

**Sound, with minor fixable presentation gaps. No fatal finding.** Every table entry matches an
independent count. 64 explicit paths trace exactly to T with no vertex contact. The k ≥ 16
rounding argument holds at k = 16, 17, 20, 30, and 41, with every identity checked exactly.

## 1. Placement lemma

- Sign convention. In column j, put both seam crossings on the sheet where the unfolded
  coordinate, measured from the column bottom, lies in [0, h_j] mod 2h_j. The physical vertical
  velocity at each crossing then equals sign(s), so it agrees on both sides of every seam. The
  rise is d_j s = y_j − y_{j−1} + P_j m_j, independent of the column bottom. This gives the
  stated formula for y_i. Correct for either sign of s.
- Folding stays in the column. The x-range is [x_{j−1}, x_j], and folding in the column's top
  and bottom lines keeps y in [b_j, t_j]. Those two walls have vertices only at grid x, which are
  the seams. A top or bottom hit at a seam x would need y_i ∈ {b, t}, and the open overlap
  excludes it. Seam corners such as (21/32, 3) in 119 are excluded the same way.
- Endpoint. The path is monotone in x, so it reaches x = T.x once. The unfolded end height is
  T.y − b + P m on the direct sheet, which folds to T.y. The path ends at T itself, not at a
  reflected copy.
- Independent confirmation: 40 traced paths for k ≤ 15 and 4 completed traces at k = 16
  (others hit the 400,000-reflection cap, not a failure). The tracer is a cell-walker that
  rejects any pass through a grid point unless all four cells around it are in the room.

## 2. Full columns

For all 8 types and every k checked, each column between S.x and T.x is one contiguous vertical
run of cells, asserted in `columns()`. The two 122 types have 2 columns; the other six have 3.
The heights don't depend on k because D = 16h, h, and ℓ = 1/4 are fixed. Seams are at 15p/16 and
p as stated (the builder sets the viewer column to 15π/16).

## 3. Counts for k = 2..15

All 10 rows of `placement.txt` match, including `-` and `outside`. My method: integer row
reduction with tracked coefficients gives a basis {(g, t), (0, H)}. I count by a direct loop
when there are at most 400,000 first coordinates, and otherwise by an ACL-style floor sum. For
each instance, a lattice point is mapped back to integer indices m, shortened along the kernel,
and traced. 40/40 traced paths are valid (706 to 261,944 reflections).

## 4. k ≥ 16

Checked exactly at k = 16, 17, 20, 30, 41 for all 8 types:

- p/w = 14/5 + 32j and u/w = 6/5 + 32i, with j odd and i = (j+1)/2. n mod 12 ∈ {4, 8}.
- b = p/16, a = 15p/16 − u = 7b − 316c, c = w/20, 8a − 7X = −323c, and X/c = 33 + 320(j−1).
  At k = 16, X/c = 873,633.
- (P₁, P₂, M) = (13/2, 6, 78), (8, 6, 24), (6, 4, 12), (25/4, 6, 150), (6, 8, 24), (17/2, 6, 102).
  These match the claim. Overlap widths are 2, 3, or 4.
- A unit change in m₁ changes 8y₁ − 323y₂ by exactly −P₁. The step (7M/P₁, M/P₂, 0) preserves it
  and moves y₁ by −323Mc/X.
- Observed errors are at most 0.0081 for y₁ and 0.0125 for y₂, within the stated 0.031 and
  0.014. By hand: 323·150/(2·800,000) = 0.0303, and 8.5/646 + 4·150/800,000 = 0.0139.
- Two-column step P₁c/X ≤ 10⁻⁵, far below the overlap width.

## 5. Exclusions and scope

- `-` at k = 4, 5 for the six 3-column types: u > 15p/16, so the viewer falls outside its
  column and the builder's assertion fires. D58's log records the same at k = 4. This is a
  legitimate exclusion.
- `outside`: 971 (1,1)(3,5) and (5,5) have h ≠ ℓ/2. D58's T3 log shows E lights both at k = 8
  and 12. The 18 recorded H/E failures are exactly the other 8 types at k ∈ {4, 8, 12}, and each
  has a positive count. The claim "includes all 18" holds.
- The scope paragraph is accurate. The proof uses 8a − 7X = −323c, which is specific to this
  builder.

## Findings

1. **Minor, fixable (F1).** The k ≥ 16 section assumes, without saying so, that the builder
   gives the same combinatorial room for every k ≥ 16. Add one line: for j ≥ 2, a > 0 (so
   u < 15p/16), p + w < 4, and the ys don't depend on k. I checked this by hand and at 5 values
   of k.
2. **Cosmetic (C1).** "Its final visit to the target strip necessarily enters through the open
   horizontal door, with the required reflected target placement" is misleading. The path ends at
   T on the direct sheet, and no reflected target is involved. Replace it with the endpoint
   argument from section 1.
3. **Cosmetic (C2).** "Positive transverse orientation" is undefined. State that every seam
   crossing is on the sheet whose physical vertical velocity equals sign(s).
4. **Cosmetic (C3).** The counts are distinct seam-height vectors (lattice points), not paths.
   "Least positive common multiple" of rational periods should be defined as the least M > 0
   with M/P₁, M/P₂ ∈ ℤ.
