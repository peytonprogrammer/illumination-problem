# d73: geometric BBBB rooms, area 21 to 36, W <= 20 — stopped at the estimate

Date: 2026-11-18. Tags: **PROVED**, **COMPUTED** (script and log here), **GUESSED**.

## Verdict

- **The full run doesn't fit the 2 CPU-hour cap, so it wasn't run (brief step 2).** Area 21
  alone has about 5.4e8 free rooms with W <= 20 (GUESSED, extrapolated from exact counts).
  Areas 21 to 36 together are on the order of 1e11 to 1e12 rooms (GUESSED). That's
  thousands of CPU-hours at the measured cost.
- **The enumerator is written, argued complete, and cross-checked (PROVED + COMPUTED).**
  Its counts match d9's Redelmeier census and Q's census in every compared cell.
- **Slice test: no dark pair (COMPUTED).** 31,612 geometric BBBB rooms gave 1,001,339 pairs.
  All are lit after one retry, and every witness replayed with 0 verify failures.
- **No candidate dark room.** True-BBBB classification and the cylinder test weren't run.

## Completeness argument (PROVED)

`enum.c` maps rooms to triples (S, w, h).

1. Let x_0 < ... < x_C be the distinct corner x-coordinates of room P, and y_0 < ... < y_R
   the y-coordinates. Every wall lies on one of these lines. So each grid rectangle
   [x_i, x_i+1] x [y_j, y_j+1] lies wholly inside or outside P. That gives a 0/1 skeleton S
   (C columns, R rows) plus widths w_i >= 1 and heights h_j >= 1.
2. The map from S to P is an order-preserving piecewise-linear homeomorphism. It preserves
   the 2-by-2 configuration at every grid vertex. So corners, reflex count, pinches,
   connectivity and holes agree between S and P.
3. Every line x_i carries a corner. So adjacent columns of S differ, and the boundary
   columns are nonempty. If two adjacent columns were equal, every vertex on the line
   between them would have 0, 2 (vertical pair) or 4 cells, so no corner. Rows behave
   the same way.
4. Conversely, let S be a strictly simple skeleton with nonempty, pairwise-adjacent-distinct
   rows and columns. Then any w, h >= 1 gives a room whose skeleton is exactly S. So the
   correspondence is a bijection with translation-normalized fixed rooms.
5. Skeletons are built column by column. The corners on the line between two columns depend
   only on those two columns, so the counts are exact as each column is added. Pruning is
   sound for these reasons:
   - The count stops at reflex > 8, convex > 12, or a pinch.
   - The closing line needs at least 2 more corners, so the search stops at
     corners + 2 > 20.
   - Skeleton cells can't exceed 36, because area >= |S|.
   - The final check needs nonempty rows, adjacent rows that differ, connectivity, and
     convex minus reflex = 4. With no pinch, that means no hole.
6. Widths and heights are enumerated in full under area <= AMAX. One representative is kept
   per D4 orbit: the room is kept when its triple is minimal over the 8 images. A triple
   determines the room, so this is exact.
7. Parity: the four-class condition is invariant under translation and the 8 symmetries,
   because they permute the classes. So the code tests it at the room's own origin.
   Smooth points are the points with k = 2, because pinches are excluded.

## Cross-checks (COMPUTED)

| Check | Result |
| --- | --- |
| Free rooms per (area, W) against d9's independent Redelmeier census (`census_totals.md`), W <= 14, area <= 20 | All 64 rows of d9's table are equal. For example, W = 14, area 20: 2,668,579, and W = 12, area 20: 328,007. d9's table omits cells with no eligible pair. |
| Rooms with a Q class and >= 2 interior points against Q's census (`witnesses.txt.gz` R lines filtered by W), W <= 10 and W <= 12 at areas 1 to 36, W <= 14 at areas 1 to 22 | All equal (`compare_q.log`). This confirms the partition: Q's list is exactly the complement, and the overlap is empty by definition. |
| Witness replay on the slices (`verify_plane.c`) | 0 failures |

The brief also asked for a brute-polyomino check to area 16. That wasn't run separately:
d9's table already gives an independent polyomino count through area 20.

## Cost estimate

- **Exact counts (COMPUTED, `logs/cnt_r4.txt`, `logs/cnt_r5_a22.txt`).**
  - W <= 12, areas 21 to 36: 92,657,242 free rooms. Area 36 alone has 17,482,415.
  - W = 14: 4,196,402 at area 21 and 6,421,343 at area 22.
  - Area 21 with W <= 14: 4,696,440 rooms. All but one are geometric BBBB.
- **Area 21 estimate (GUESSED).** d9 gives W = 16, 18, 20 at areas 18 to 20. The growth
  ratios fall slowly: for W = 20 they are 2.62 and 2.44. Extrapolating one step gives
  about 2.6e7, 1.2e8 and 3.9e8 rooms. The area-21 total is about 5.4e8.
- **Areas 21 to 36 (GUESSED).** W = 12 grows 37x from area 21 to area 36. Higher W grows
  faster, so the total is about 1e11 to 1e12 rooms.
- **Per-room cost (COMPUTED).**
  - Shooting with BOUND 12 costs about 10 us per room at area 21 (r <= 8 slice) and about
    53 us at area 36 (r <= 3 slice).
  - Retrying the 766 misses at BOUND 60 resolved all 14,573 pairs in those rooms.
  - The enumerator costs about 0.08 us per fixed room (7.5e8 fixed rooms in 61 s).
- **Conclusion.** Area 21 alone needs about 1.5 CPU-h of shooting, plus about 0.1 to 0.5 h
  for enumeration and the r <= 8 skeleton search. That's at or over the cap. Areas 21 to
  36 need about 1e3 CPU-h or more.

## Slice results (COMPUTED, `logs/`)

| Slice | Rooms | Pairs | Lit, BOUND 12 | Lit after retry, BOUND 60 | Verify failures |
| --- | --- | --- | --- | --- | --- |
| Area 21, r <= 8, first skeletons in search order (R <= 4), every 35th | 20,237 | 187,503 | 186,858 | all | 0 |
| Area 36, r <= 3, every 40th | 11,375 | 813,836 | 813,715 | all | 0 |

These samples follow the search order and aren't random. They show only that the pipeline
works. They aren't evidence about the full range.

## Reduced plans (for Daniel's choice; none were run)

1. **W <= 12 (r <= 4), areas 21 to 36:** 92.7M rooms, about 0.5 to 1 CPU-h. This fits, but
   it's far from the 22-wall regime.
2. **W <= 14, areas 21 to 24:** about 35M rooms, about 0.2 CPU-h.
3. **r <= 8, area 21 only:** about 5.4e8 rooms, about 2 CPU-h. This needs a raised cap.
4. **Better route (GUESSED).** D64 closes every room with a proper factor, so only true
   BBBB rooms matter. d72 found 0 true BBBB rooms among 2,466 geometric BBBB normalized d64
   rooms. Enumerating true BBBB rooms directly, through a structural characterization,
   would likely shrink the search by orders of magnitude. Brute force over geometric BBBB
   doesn't scale.

## Files and CPU

- `enum.c`: skeleton enumerator. Build with `cc -O3 -o enum enum.c`. Run as
  `./enum RMAX AMAX AOUTMIN outfile|-`.
- Shooter: `patch -o all_pairs.c ../d9-census-w22/shoot.c < ../../../../qclass-closure/all-pairs.patch`,
  then `cc -O3 all_pairs.c ../d9-census-w22/verify_plane.c -o shoot`.
- `compare_q.log`: the comparison with Q's census.
- `logs/`: counts, slice outputs, and compressed slice rooms and survivors (about 400 KB).
- CPU: about 6 minutes in total. That includes an aborted first r <= 8, area <= 16 run of
  about 2.5 min. Nothing was written outside this directory, and git is unchanged.
