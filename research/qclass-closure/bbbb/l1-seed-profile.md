Advances: L1 — the straight-chord seed for interior lattice pairs, using the exact-area-21 L2 census.

# What the first seed looks like at area 21

The largest **first-found** primitive height was 26, attained twice. Those two seeds made 42 and 51 reflections. A different pattern accounts for much of the hard tail: a ray can bounce repeatedly across a narrow passage while crossing a particular horizontal section just once. In 18 of the 20 displayed rooms this gives an infinite family in which every pair stays lit.

## Measurement

In [d205 shoot.c, make_dirs](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d205-census-a21/shoot.c) the outer loop is the sum (s=|p|+|q|), with decreasing (|p|) within a sum. The shooter tries the four signs and follows each ray to a forbidden corner, a return, or its finite step limit. It removes a target after its first verified hit. Thus e.g. (3,1) precedes (2,3). Height below means (h=max(|p|,|q|)) **of that first hit**. Exact minimum heights and their top-20 ranking cannot be read off this traversal. The first sum does give a lower bound (⌈s/2⌉) on the true minimum height, since every direction of smaller sum was exhausted.

Exact area 21 only, 84 original shards, nice 10, seven workers maximum, 46.29 worker CPU-minutes. Every shard reproduced its original room counts, expected pairs, parity counts and zero survivors. There were 538,025,823 canonical rooms, 364,183,172 with a pair, and 1,604,242,406 replay-verified first witnesses. Each witness was written to disk. A second pass decoded every record and reproduced the height histogram by reflex count; maxima over the archive were 17 primitive steps and 123 reflections (separate maxima). The hard-pair paths below were additionally reconstructed from exact intersections with the physical walls. [Run manifest](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/seed-profile-a21/a21/manifest.json) · [record layout](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/seed-profile-a21/records.md) · [decoded shard counts](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/seed-profile-a21/audit.log)

### Pairs by first-found height and reflex count, area 21

A dot is zero. Each column counts unordered pairs in canonical rooms with (r=(W-4)/2), including pairs in different parity classes.

| Height | r=0 | r=1 | r=2 | r=3 | r=4 | r=5 | r=6 | r=7 | r=8 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 54 | 748 | 21,485 | 316,962 | 2,966,527 | 18,880,347 | 83,435,226 | 260,576,368 | 580,637,752 |
| 2 | 12 | 127 | 4,174 | 69,744 | 682,717 | 4,439,128 | 19,845,858 | 62,520,798 | 140,267,465 |
| 3 | · | 2 | 660 | 19,871 | 294,929 | 2,485,887 | 13,262,993 | 46,968,566 | 113,932,832 |
| 4 | · | · | 92 | 3,119 | 61,608 | 665,194 | 4,203,455 | 16,940,442 | 45,508,075 |
| 5 | · | · | 95 | 4,719 | 104,570 | 1,115,084 | 7,075,654 | 28,717,824 | 78,152,923 |
| 6 | · | · | 5 | 148 | 4,069 | 59,292 | 484,330 | 2,449,429 | 8,008,203 |
| 7 | · | · | 7 | 453 | 14,774 | 219,214 | 1,765,968 | 8,588,529 | 26,773,565 |
| 8 | · | · | · | 54 | 2,091 | 36,292 | 331,286 | 1,816,362 | 6,301,413 |
| 9 | · | · | · | 18 | 1,047 | 21,929 | 235,944 | 1,428,739 | 5,334,137 |
| 10 | · | · | · | 2 | 104 | 2,891 | 35,883 | 247,921 | 1,028,655 |
| 11 | · | · | · | 11 | 470 | 9,837 | 107,915 | 689,076 | 2,686,607 |
| 12 | · | · | · | · | 5 | 315 | 6,557 | 58,556 | 296,127 |
| 13 | · | · | · | 1 | 30 | 1,033 | 16,323 | 129,323 | 589,438 |
| 14 | · | · | · | · | 8 | 205 | 3,045 | 26,223 | 129,411 |
| 15 | · | · | · | · | 1 | 26 | 733 | 7,157 | 38,682 |
| 16 | · | · | · | · | · | 6 | 255 | 3,485 | 22,569 |
| 17 | · | · | · | · | · | 26 | 501 | 5,196 | 28,766 |
| 18 | · | · | · | · | · | · | 6 | 211 | 1,597 |
| 19 | · | · | · | · | · | 3 | 56 | 627 | 3,898 |
| 20 | · | · | · | · | · | · | 9 | 89 | 567 |
| 21 | · | · | · | · | · | · | 2 | 54 | 359 |
| 22 | · | · | · | · | · | · | · | 7 | 92 |
| 23 | · | · | · | · | · | · | · | 8 | 50 |
| 24 | · | · | · | · | · | · | · | · | 5 |
| 25 | · | · | · | · | · | · | · | 3 | 2 |
| 26 | · | · | · | · | · | · | · | · | 2 |

### Twenty largest first-found heights

All 12 pairs of height at least 24 appear here, followed by eight of the 58 ties at height 23. Ties use shard number then original discovery order. Room ID is shard / one-based eligible-room ordinal. Launch at the signed direction shown, reflect specularly, and stop after (m) primitive lattice steps of developed displacement (m(p,q)). V and H count hits on vertical and horizontal walls. Green is the source and red the target. Each polyline shows the actual reflected path. [Exact ordered bounce coordinates for all 20](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/seed-profile-a21/paths.json)

![Twenty rooms and their first seed paths](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/seed-profile-a21/hardest.png)

| Rank | Room ID | r | Source → target | Launch | Height | m | V + H |
|---:|---|---:|---|---|---:|---:|---|
| 1 | 7/4319984 | 8 | (1,1) → (5,6) | (-26,3) | 26 | 3 | 40 + 2 = 42 |
| 2 | 44/327644 | 8 | (1,1) → (5,8) | (26,-5) | 26 | 3 | 47 + 4 = 51 |
| 3 | 1/6423922 | 8 | (1,1) → (4,8) | (3,25) | 25 | 1 | 0 + 7 = 7 |
| 4 | 1/7168679 | 8 | (1,1) → (4,7) | (-25,4) | 25 | 3 | 27 + 6 = 33 |
| 5 | 31/3460065 | 7 | (1,1) → (4,8) | (25,3) | 25 | 3 | 39 + 2 = 41 |
| 6 | 31/3466167 | 7 | (1,1) → (4,8) | (25,3) | 25 | 3 | 39 + 2 = 41 |
| 7 | 31/3466180 | 7 | (1,1) → (4,8) | (25,3) | 25 | 3 | 39 + 2 = 41 |
| 8 | 13/1421575 | 8 | (1,2) → (5,9) | (-24,-5) | 24 | 3 | 46 + 4 = 50 |
| 9 | 24/3500131 | 8 | (1,1) → (3,6) | (-24,5) | 24 | 1 | 13 + 0 = 13 |
| 10 | 34/1743479 | 8 | (1,2) → (5,9) | (-24,-5) | 24 | 3 | 46 + 4 = 50 |
| 11 | 48/1156563 | 8 | (1,1) → (3,6) | (-24,5) | 24 | 1 | 13 + 0 = 13 |
| 12 | 83/2685397 | 8 | (1,1) → (3,6) | (-24,5) | 24 | 1 | 13 + 0 = 13 |
| 13 | 5/2407176 | 8 | (3,1) → (6,8) | (23,5) | 23 | 3 | 34 + 5 = 39 |
| 14 | 5/2407454 | 8 | (3,1) → (6,8) | (23,5) | 23 | 3 | 34 + 5 = 39 |
| 15 | 11/2274238 | 8 | (4,2) → (5,5) | (23,-3) | 23 | 3 | 33 + 3 = 36 |
| 16 | 18/407409 | 8 | (1,1) → (6,6) | (23,-3) | 23 | 3 | 39 + 3 = 42 |
| 17 | 18/561577 | 8 | (1,1) → (6,6) | (23,-3) | 23 | 3 | 39 + 3 = 42 |
| 18 | 21/4136869 | 8 | (2,1) → (5,6) | (23,-5) | 23 | 3 | 24 + 5 = 29 |
| 19 | 22/4654146 | 8 | (1,1) → (2,6) | (23,5) | 23 | 3 | 39 + 4 = 43 |
| 20 | 24/4145154 | 8 | (1,2) → (2,5) | (23,-5) | 23 | 3 | 32 + 6 = 38 |

**Construction by rank.** Ranks 3, 9, 11 and 12 use a ray monotone in one coordinate with 7 or 13 parallel-wall reflections. Every other listed seed reverses both velocity components and makes at least 29 reflections. None of the 20 recorded seeds has the earlier one-wall-plus-roof itinerary. A simpler *different* witness remains possible. The drawings show why counting total reflections alone hides the distinction between repeated bounces across a passage and repeated trips through it.

## A conjecture the records can actually test

Let (Bₓ,Bᵧ) be the side lengths of the room's axis-aligned bounding box. Conjecture: every distinct interior lattice pair in a strictly simple orthogonal lattice room with (r ≤ 8) admits a legal seed with

**|p| ≤ 8Bₓ,  |q| ≤ 8Bᵧ,  min(m|p|/Bₓ, m|q|/Bᵧ) ≤ 15.**
Thus the proposed type is a path whose **total travel along at least one axis is at most 15 box spans**, regardless of how often it bounces on the other axis. Its primitive height is at most (8 max(Bₓ,Bᵧ)). The constants 8 and 15 are the separately rounded-up maxima over *all first records* in this one slice, computed before selecting the top 20. Both inequalities hold for the same witness of every pair here. They are empirical choices; there is no derivation of either from the reflex budget or evidence of optimality across areas.

## A proof for periodic stretches of the hard rooms

**Unit passage.** Suppose the entire horizontal slice through (y=j+1/2) is one interval of width one. Cut there, translate the entire upper part by an integer (E ≥ 0), and fill the gap with that same unit strip. The sides at the cut are straight and continue vertically, so wall count and strict simplicity are preserved. No new interior lattice mark fits across the strip. Old marks above the cut translate by (E); all others keep their positions.

Fix a base seed crossing the cut with (q ≠ 0). In the unfolded unit interval, its additional transverse displacement on each traversal is (± E|p/q|). A multiple of two restores both the horizontal position and the horizontal velocity sign, including a crossing at a side wall interpreted by continuation. The open strip has no corners on its straight sides. Thus (E) divisible by (2|q|/gcd(|p|,2|q|)) splices in a legal excursion at **every** crossing of that seed. A parallel ray from a lattice mark never lies along this half-integral cut. Noncrossing seeds carry over unchanged up to translation. Take the least common multiple of these periods for the chosen crossing seeds, one per base pair. Every pair in every resulting room is then lit.

**Quantitative part.** A seed crossing (v) times gains exactly (vE) units of total vertical travel, while (Bᵧ) increases by (E). If (m|q| ≤ 15Bᵧ) and (v ≤ 15), the new vertical travel is at most (15(Bᵧ+E)). The primitive direction stays the same, so the two height inequalities persist. A noncrossing seed keeps its original travel on both axes. This proves the conjectured estimates on the indicated growth progressions.

For each row below, exact wall intersections of **all** base-pair records give at most one crossing per seed at the displayed cut. Each crossing seed satisfies the initial vertical travel inequality. The period is the common period of their signed phases. This verifies the hypotheses on finite base data; the strip argument proves the conclusion for arbitrarily long extensions. [Cut and period checks](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/seed-profile-a21/profile.py) · [per-room results](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/seed-profile-a21/family.json)

| Rank | All base pairs | Cut row j | Permitted E (multiples of) |
|---:|---:|---:|---:|
| 1 | 6 | 2 | 6 |
| 2 | 3 | 2 | 70 |
| 3 | 3 | 4 | 50 |
| 4 | 3 | 2 | 40 |
| 5 | 6 | 2 | 42 |
| 6 | 6 | 2 | 42 |
| 7 | 6 | 2 | 42 |
| 8 | 3 | 4 | 30 |
| 9 | 3 | 4 | 30 |
| 10 | 3 | 4 | 60 |
| 12 | 3 | 4 | 10 |
| 13 | 1 | 2 | 10 |
| 14 | 1 | 4 | 10 |
| 15 | 3 | 3 | 6 |
| 16 | 3 | 2 | 24 |
| 17 | 3 | 2 | 48 |
| 19 | 1 | 2 | 10 |
| 20 | 1 | 3 | 10 |

For rank 1 the extremal seed crosses (y=5/2) at (x=4/3) travelling up-left in the interval ([1,2]). Its individual period is 3 and the six pairs together have period 6. For rank 2 the extremal seed crosses at (x=4/5) travelling up-left in ([0,1]); its period is 5 and the three pairs together have period 70. Ranks 11 and 18 have no internal unit row or column of this form.

**First open step.** Already for rank 1, adding one unit changes the extremal seed's unfolded phase by (26/3), nonzero modulo two. Its incoming state therefore fails the same-exit test. The length-one extension has area 22. Finding a compensating seed for all residues and all marks in this passage family remains open in this argument. The two rooms without a usable cut also require a different argument for growth. The census and the stretch proof supply no universal selection rule at (r=8).
