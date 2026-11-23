# d66: the pair-level proof chain for the W <= 20 orthogonal target

Date: 2026-11-18. Theory plus exact checks on named rooms and on the saved d64 room list
(reading only). No room, ray, direction, or reflection-word discovery search.
Tags: **PROVED** (argument here), **COMPUTED** (script and log here), **CITED** (file),
**GUESSED** (judgment).

## Answer

- **The chain has one open lemma for same-class pairs, and it's narrower than RL-B.** After
  d64, the open rooms are R*: normalized, `r <= 8`, and every one of the four classes has
  `N_x = B` (one block) or `N_x = Q` (discrete). d64 closes every room with at least one
  class of degree `1 < deg N_x < n`, whatever the pair's class (PROVED by reading
  `d64-finite-case/dark_pairs.py` and its completeness argument). The d9 census closes
  R* rooms of area at most 20. The open lemma OL (section 5) is R* with area at least 21.
- **In that range, OL is a pure lit statement (PROVED from CITED results).** At a Q target,
  Par certifies every pair. At a B target, Par and Cut can't occur, and Rig is essential.
  So it forces area at most 20 (d39, corrected in d43). A pair that OL concerns can't be
  certified. "Dark implies certified" and "every pair is lit" say the same thing there.
- **Per-target statements fail even inside R* (COMPUTED).** Two W = 20, area-28 R* rooms
  (`cov4181`, `cov4269`) each have an interior room pair with these properties:
  - It's dark on all four lift pairs at one B target.
  - It's uncertified, and its deck group is trivial.
  - It's lit at the other B target.
  Exact billiards agree up to `max(p, q) <= 60`. So d65's RL-room is false in R* too. Only
  the pair-level form can hold.
- **Lemma M pairs reduce to visibility of the symmetry centre (PROVED, Relay lemma).** If
  `S~` sees a fixed point of a deck involution `delta`, then `S~` and `delta S~` are lit,
  at the class of that fixed point. So a dark pair `{S, sigma S}` in a centrally symmetric
  room needs a dark pair `{S, C}`. That's a different-class pair (G1) when C's class
  isn't `a`. COMPUTED: in 30 of 30 x-dark delta rows, the same lift pair is lit at the
  fixed-point class.
- **Other gaps:** G1 (different-class lattice pairs) and G2 (non-lattice rational marks).
  Both have open lit sides in every room, the finite range included. d64 tested neither.
  New evidence follows. 27,190 different-class interior pairs in all 4,581 d64 rooms plus
  11 named rooms are lit by exact billiard paths. In the 11 named rooms, 8,025
  half-integer pairs are lit.
- **Tests:** 4,782 same-class interior pairs, 0 pair-level dark in W <= 20 rooms. The
  positive controls R22, P6, and P6found are reported DARK. In R*, 4,757 pairs in 1,781
  rooms are tested. CPU is about 333 s in total, one process at a time.

## 1. Terms

- Room: a strictly simple orthogonal lattice room `P`. `W = 2r + 4`, so `W <= 20` means
  `r <= 8`. Normalized: the gcd of horizontal edge lengths is 1, and so is the gcd of
  vertical edge lengths (d10 R1).
- `Q = DP -> B` has degree `n` = area. A pair `S != T` is **lit** when some lift pair
  `(S~, T~)` is x-lit for some target `x`. **x-lit** is the pure-braid orbit verdict: some
  state joins the lifts along an arc `a -> x`. It equals billiard light (d61 FC, d62
  review, d64 billiard checks; CITED).
- For each of the four classes `x`, `B_x` is the finest block system that merges every
  2-cycle of `g_x`. `B_x` depends only on `x`, so this sorts a room's classes into three
  types:
  - **B**: one block, so `N_x = B`.
  - **Q**: discrete, so `N_x = Q`. This happens exactly when class `x` has no
    transparent point: no interior lattice point and no smooth wall point.
  - **proper**: `1 < deg N_x < n`.
- **R\***: the normalized rooms with `r <= 8` in which all four classes have type B or Q.
- For a pair of class `a`: `X_B(a)` is the set of B targets, and `X_Q(a)` is the set of
  Q targets.

## 2. The chain (pair-level form)

Target T20: in every room with `W <= 20`, every pair of distinct interior points is lit.

| Step | Statement | Status |
| --- | --- | --- |
| 0 | Real to rational: all rational interior pairs lit implies all real interior pairs lit. | CITED, reviewed (`d16-real-to-rational/`, `d16-review/`) |
| 1 | Normalization: scale by `(1/g_h, 1/g_v)`. Diagonal maps commute with reflections in axis-parallel walls, so billiard paths correspond. `W` is unchanged, and rational points stay rational. So WLOG `P` is normalized, and the marks are rational. | PROVED |
| 2 | Split: (i) same-class lattice pairs; (ii) different-class lattice pairs (G1); (iii) at least one non-lattice rational mark (G2). | PROVED (exhaustive) |
| 3a | (i) when some class has a proper factor: every same-class interior pair is lit. | COMPUTED (`d64-finite-case/`, 2,800 rooms, 6,680 pairs). Completeness PROVED in d64 section 2. It rests on the d52 enumerator (refereed in d54). d64 itself is unreviewed. |
| 3b | (i) in R* with area <= 20. | CITED, COMPUTED (d9 census: no dark pair at `W <= 21`, area <= 20) |
| 3c | (i) in R* with area >= 21. | **OPEN: lemma OL (section 5)** |
| 4 | (ii) G1: the one target is the class of `T`. Lit side: "x-dark implies Rig(x)". Certificate side: d46, d56 Set A, and the d56 shortcut. | Lit side OPEN everywhere. Certificate side CITED. |
| 5 | (iii) G2: the natural base is `P_Lambda0`, `Lambda0 = Z^2 + ZS + ZT`. It's non-normalized (it has `B` as an intermediate pillowcase), and it's sheared when `Lambda0` is. Certificate side: d46-d50 and d56 Set E. | Lit side OPEN. Certificate side CITED. |

Notes on the chain:

- **The fold side isn't load-bearing for (i).** Steps 3a and 3b are direct lit verdicts.
  In 3c, no certificate can exist (section 6, Prop. 2). So d62's C4 caveat doesn't touch
  (i): certificate types may mix across lift pairs and targets. The fold side (d46, d52,
  d56) is needed only to turn a "dark implies certified" form of G1 or G2 into a lit
  statement.
- **Theorem U** (d10) is the soundness side. The lit chain doesn't use it, except through
  Prop. 2.
- **Out of scope here:** wall marks and 45-degree walls. The target concerns interior
  points, and d16 is stated for interior points. Wall marks appear only as tools, as in
  the Relay lemma.

## 3. Gap list

| Id | Gap | Where it bites | Status |
| --- | --- | --- | --- |
| OL | Same-class interior lattice pairs in R*, area 21 or more (section 5) | Infinite family: every normalized room with area > `8r` is in R* (d63 corollary) | OPEN |
| G1 | Different-class lattice pairs: "x-dark implies Rig(x)", with `x` the class of `T` | Every room. d64 didn't test these. Census evidence reaches area 16 to 20. | OPEN. 27,190 pairs lit here (section 7). |
| G2 | Non-lattice rational marks: the lit side over `P_Lambda0`. Non-normalized presentation, where per-target forms fail (cross scaled by 3). Sheared `Lambda0` gives a non-orthogonal affine image of `DP`. | Every room | OPEN. 8,025 half-integer pairs lit in the named rooms. The R* sample is incomplete (section 7). |
| C1 | d64 is unreviewed: the completeness argument, `enum_K.c`, and the `delta = 2` covers | Step 3a | Needs a referee |
| C2 | d39's essential-Rig bound (area <= 20). d43 found two unproved assertions and fixed them. | Prop. 2 only (it makes OL certificate-free). The chain stays valid without it, in the lit form of OL. | CITED, one referee |
| C3 | The orbit model of light (pure-braid states, Gamma(2) transitivity) | Steps 3a and 3b, and all tests | CITED (d62 review). Billiard checks agree in d62, d64, and here. |

Irrational points are covered by step 0. Coarsest base and normalization are covered by
step 1 and R1: for lattice marks in a normalized room, `B` is the only pillowcase factor.
They come back only in G2.

## 4. Hidden per-target uses (all removed above)

| Source | Use | Verdict |
| --- | --- | --- |
| d61 section 6 step 2; d63 section 1.3 step 2 | RL per lift pair and per target | False: d64 (830 rows) and d65 (`S10`) |
| d65 section 4 | RL-room: per target, all four lift pairs | False outside R* (room 1843, d64) and **inside R*** (`cov4181`, `cov4269`, here). Its "suffices" proof is right, but the lemma is false. |
| d63 section 2.2 | RL-B = Lemma H + E_x for primitive G | It's per target. The R* failures have imprimitive G: one 4-block system, the `R_y` of the Q class, with trivial deck group. So they don't refute abstract Lemma H. But per-class transitivity isn't available for rooms. |
| d37 joint majority | per class | Already false (d38) |
| d10 D2 | dark (all targets) implies certified at each target | Pair-level hypothesis: fine. In R* with area >= 21 it's equivalent to OL. |
| d64 RL-fin | per target | False. d64 replaced it with the direct pair test, which is fine. |

## 5. The open lemma

**OL (pair-level lemma for R\*).** Let `P` be a strictly simple orthogonal lattice room
with these properties:

- normalized;
- `r <= 8`;
- area at least 21;
- each of its four corner classes has `B_x` either one block or discrete.

Let `S != T` be interior lattice points of one class `a`. Then some lift pair `(S~, T~)`
is x-lit for some `x != a` with `N_x = B`.

Equivalent forms (PROVED from Prop. 2):

- "Dark implies a certificate at every target" in this range (d10 D2 restricted to R*).
- "No pair is x-dark for every `x` in `X_B(a)`."

Q targets never light anything, because they have no regular point.

Structure (PROVED, section 6):

- `X_B(a)` is non-empty for any class with two interior points. If it were empty, Par
  would hold at all three targets, and d46 and d56 exclude that (CITED). So OL splits:
  - **OL1, `|X_B(a)| = 1`.** OL is the per-target statement at the one target. At least
    one of `b`, `d` is a Q class, so the class `a` has at most 4 interior points (Prop. 1).
    Data: 15 pairs in 12 rooms, all lit.
  - **OL2, `|X_B(a)| >= 2`.** OL is genuinely pair-level. Per-target forms fail here
    (`cov4181`, `cov4269`).
- Pairs `{S, sigma S}`, with `sigma` a half-turn of `P` about a lattice point `C` whose
  class isn't `a`, follow from G1 for the pair `{S, C}` (Relay lemma).

## 6. Residual case: results

**Prop. 1, Q-class geometry (PROVED).** Let class `y` be of type Q. Then:

- Every horizontal edge at a height congruent to `y_2` has length at most 2. So does every
  vertical edge at an abscissa congruent to `y_1`. A longer edge has smooth points of both
  parities.
- Suppose `y = a + (1, 0)`. For every interior a-point `S`, both `S + (1, 0)` and
  `S - (1, 0)` are reflex corners.
  - `S + (1, 0)` already has the two cells to its left, so it's smooth, reflex, or
    interior. Only reflex is opaque.
  - A reflex corner is a horizontal neighbour of at most one interior a-point. If it had
    two, all four of its cells would be present.
  - So class `a` has at most `r_y / 2 <= 4` interior points. The vertical case
    `y = a + (0, 1)` is the same.
  - If both `b` and `d` are Q, at most `r / 4 = 2` points remain: one pair, and
    `X_B(a) = {c}`.

**Prop. 2, no certificates in OL's range (PROVED from CITED results).** Let `P` be in R*,
and let the pair have class `a`.

- At a Q target, Par holds for every lift pair: `B_x` is discrete, so it separates them
  (R3).
- At a B target:
  - Par fails, because `B_x` is one block.
  - Cut fails: by d10 R4, Cut with a transparent target class forces the 12-wall cross.
    The cross isn't in R*: its class (0, 0) has degree 3 (COMPUTED).
  - Rig is essential, so it forces area at most 20 (d39 claim 3, fixed in d43).

So at area >= 21 no pair has a certificate at any B target.

**Relay lemma (PROVED).** Let `delta` be a deck involution of `DP -> B`. By Lemma M, its
fixed points `F_1`, `F_2` are regular points over corners. Suppose a light path `gamma`
joins a lift `S~` to some `F_i`. Then `S~` and `delta S~` are lit, at the direction class
of `gamma`.

Proof:

1. `delta` fixes `F_i`, and `Q -> Q / delta` has local degree 2 there. So in the flat
   chart, `delta` is the rotation by pi about `F_i`.
2. `gamma` arrives at `F_i` with direction `v`, so `delta gamma` arrives with `-v`.
3. Reversed, `delta gamma` leaves `F_i` with direction `v`. So `gamma`, followed by
   `delta gamma` reversed, is one geodesic through the regular point `F_i`.
4. It passes only regular points, and it ends at `delta S~`.

**Corollary (PROVED).** Let `sigma` be the half-turn about `C`, with `C` in class
`c != a`. Then `delta` fixes `C_f` and `C_b`, both over `c` (d65). Suppose `{S, sigma S}`
is dark. Then `{S, C}` is a dark different-class pair, because every lift path to `C_f`
or `C_b` is blocked.

So in OL, delta-pairs need nothing beyond G1 for `{S, C}`. For a mirror symmetry, the
fixed points are the two wall points on the axis. The same relay needs `S` to see a wall
point, which isn't a target statement. This replaces d65's Gap S for the delta-pair. The
`iota delta`-pair isn't needed.

**What Lemma M plus Relay leave (the minimal gap).** The rows not explained by a deck
involution. In R*, every x-dark row at a B target is one of two kinds:

- a delta-pair (6 rows), lit at the fixed-point class;
- a row of `cov4181` or `cov4269` (8 rows). These rooms have trivial deck group and an
  imprimitive `G`. The only proper block system is the 4-block `R_y` of the Q class. It
  has identity at `y`, but Rig fails.

Both rooms are BBBQ, so this is OL2. Light arrives through the second B target, along the
straight segment `ST` through an interior point of that class. No argument here shows
that a second target must succeed. The two FC conditions, darkness at `b` and at `d`, are
about different 2-cycle graphs (`g_a` with `g_b`, and `g_a` with `g_d`). No closure
relates them. Approach (i) of d63 fails for the same reason: x-lit isn't transitive.

So the minimal gap is: **OL2 for pairs that aren't delta-pairs, plus OL1 (at most 6 pairs
per room).** Within that, rooms with trivial deck group are the old Lemma H territory.
The dead-end list applies, and nothing here reaches them.

GUESSED:

- Per-target failures in R* need a Q class. They come with the imprimitive `R_y`, so OL
  may hold per target in BBBB rooms. Every room with area > `8r` and four transparent
  classes is BBBB. The only BBBB test room is dumb12, which has 0 dark rows. That's weak
  evidence.
- Probability that OL2 is provable with current tools: about 5%, unchanged from d59.

## 7. Tests (COMPUTED)

`pair_level.py`: full per-target orbit verdicts, a state cap of 20,000 (never reached:
0 unresolved, max 4,608 states), and Rig over `DP / R_y` on dark rows.

| Room | n | W | Types (classes 00, 01, 10, 11) | R* | Same-class pairs | Pair verdict | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| cross12 | 12 | 12 | 3, B, B, Q | no | 2 | lit | 2 room pairs x-dark at B (Cut), 8 delta rows, relay lit 8/8 |
| dumb12 | 20 | 12 | B, B, B, B | **yes** | 4 | lit | 0 dark rows |
| R22 | 15 | 22 | B, 5, 5, Q | no | 1 | **DARK** | positive control |
| P6, P6found | 20 | 28 | three 5s, one B | no | 1 each | **DARK** | positive controls |
| Lroom, R24 | 12, 8 | 6, 4 | | not normalized | 3, 1 | lit | |
| Z12, T8, Z8 | 10, 8, 8 | | | no | 0 | n/a | |
| S10 | 10 | 12 | 5, B, B, B | no | 1 | lit | 4 delta rows dark at B, relay lit 4/4 |
| room 1843 | 20 | 12 | B, B, B, 5 | no | 9 | lit | 4 room pairs per-target dark (proper factor), relay 6/6 |
| room 1490 | 18 | 20 | 3, B, B, Q | no | 2 | lit | relay 2/2 |
| room 453 | 16 | 12 | B, B, B, 4 | no | 0 | n/a | |

**R\* rooms in `d64/data/covers.json`.** These are the normalized rooms outside d64's
scope. There are 1,781: 1,746 BBBQ and 35 BBQQ. 1,299 of them have a same-class pair,
641 of those with area >= 21. W ranges over 12 to 20, with 1,134 at W = 20.

| Count | Value |
| --- | --- |
| Same-class interior pairs | 4,757 (BBBQ 4,742; BBQQ 15) |
| Pair-level dark | **0** |
| x-dark rows at a B target | 14 |
| ... delta-pairs, relay class lit | 6 of 6 (`cov80`, `cov82`, `cov137`) |
| ... other (room pair per-target dark, pair lit) | 8 rows, 2 room pairs (`cov4181`, `cov4269`) |
| Dark rows with Rig over `DP / R_y` | 0 |
| `iota` symmetry check, (S_f,T_f) ~ (S_b,T_b) per target | 9,499 ok, 0 fail (named rooms included) |

Room `cov4181` has 28 cells, `r = 8`, and `W = 20`. Its cells are `(0,0..5) (1,2) (1,3)
(2,2) (2,3) (3,0..5) (4,0..5) (5,2) (5,3) (6,2) (7,0..2)`. The pair is class `a = (0,1)`,
with `S = (2,3)` and `T = (4,3)`.

```
y=5 #..##...
y=4 #..##...
y=3 ######..
y=2 ########
y=1 #..##..#
y=0 #..##..#
```

- The types are `d` B, `b` B, and `c` Q.
- All four lift pairs are d-dark, with complete orbits. They're b-lit along the segment
  through the interior point `(3,3)`.
- Billiards (`billiard_check.py`, `H = 60`): class `b` reaches both copies, and classes
  `c` and `d` reach none.

`cov4269` is a different room, not an isometric copy, with the same pattern at `x = b`.

**G1 (`g1_check.py`, exact billiards, `H = 8`, then 30).** Every different-class interior
pair in 4,592 rooms is lit. That's the 4,581 normalized d64 rooms plus 11 named rooms:
27,190 pairs, 0 unresolved. A control run at `H = 1` leaves 4,167 unresolved, so the
check has teeth.

**G2 (`g2_check.py`, half-integer marks via `2P`, `H = 6`, then 24).** The 11 named rooms
have 8,025 pairs, and all are lit. R22 and P6 are included: their one dark pair is a
lattice pair.

The R* sample with area >= 21 hit the 300 s CPU cap before it finished. Up to that point,
33 rooms had 117 pairs with no witness at `H <= 24`. Those pairs are unresolved, not dark,
and weren't sent to the exact decider. The log has no total line. Treat this part as
incomplete.

## Files and CPU

| File | Content | CPU |
| --- | --- | --- |
| `pair_level.py`, `pair_level.log`, `pair_level.json` | Room types, R* membership, pair and per-target verdicts, Rig, deck and relay data | 27.0 s |
| `billiard_check.py`, `billiard_check.log` | Exact billiards on the R* rows | 0.7 s |
| `blocks_check.py` | Block systems and deck group of the R* failure rooms | about 1 s |
| `g1_check.py`, `g1_check.log`, `g1_check_all.log` | Different-class pairs (two sanity runs at `H = 1, 2` were not saved) | 3.7 s |
| `g2_check.py`, `g2_check.log` | Half-integer pairs (stopped at the 300 s cap) | 300 s |

Run with `python3 -B <file> [args]` from this directory. The usage lines are in each
docstring. Reused read-only: d64 `rl_test` (paths and Rig over `R_y`), d63 `realize`,
d65 `rl_room.centraliser` and `notch12`, d62 `billiard.shoot` (copied with a parity
argument into `g1_check.py`), and d10 `roomtools`.

Total: about 333 CPU-s (5.6 CPU-minutes), one process at a time, under the 10-minute cap.
Nothing was written outside this directory, and nothing in git changed.
