# d163 wall-turn pattern ledger, W ≤ 20

Date: 2026-11-22. Status: COMPUTED (one implementation, unreviewed). Combinatorial only:
no ray, direction, reflection-word, room-size or by-area search. `python3 -B ledger.py`
runs in 1.4 CPU-seconds and writes `ledger.json` (every word, its realization, family,
status) and `ledger.log`.

Convention: a word lists vertex turns counterclockwise, L = convex, R = reflex,
#L − #R = 4. Words are taken up to rotation and reversal (mirror image).

## 1. Counts and status

| W | r | Words | COVERED | PARTIAL | OPEN |
| --- | --- | --- | --- | --- | --- |
| 4 | 0 | 1 | 1 | 0 | 0 |
| 6 | 1 | 1 | 1 | 0 | 0 |
| 8 | 2 | 4 | 4 | 0 | 0 |
| 10 | 3 | 8 | 0 | 1 | 7 |
| 12 | 4 | 29 | 0 | 2 | 27 |
| 14 | 5 | 79 | 0 | 0 | 79 |
| 16 | 6 | 280 | 0 | 1 | 279 |
| 18 | 7 | 912 | 0 | 0 | 912 |
| 20 | 8 | 3,260 | 0 | 0 | 3,260 |
| all | | 4,574 | 6 | 4 | 4,564 |

- Counts match an independent Burnside count of binary bracelets at every W.
- **Realizability.** Every word is realized by a strictly simple lattice polygon. This
  is a known result (for example Culberson and Rawlins, "Turtlegons", 1985). The
  script also proves it per word: remove an adjacent LR or RL pair, realize the shorter
  word, double the coordinates, and insert a unit jog. All 4,574 realizations pass an
  exact simplicity and turn-word check. Coordinates are in `ledger.json`.
- **COVERED** means d15 Theorem S (reviewed): every real pair is lit at r ≤ 2, for any real
  lengths. Nothing else covers a whole word. d161 and d157 reprove parts of W ≤ 8 only.
- **PARTIAL** means a reviewed theorem lights an infinite metric subfamily of that word
  (word-specific). The 4 words are listed in section 3.
- **OPEN** means only the universal bands below touch the word.
- **Strict reading.** Under the brief's literal definition, every W ≥ 10 word is PARTIAL.
  The reason is that d80 (irrational marks, n ≥ 120) applies to scaled copies of every
  word. The other universal bands are C9 (area ≤ 20, lattice pairs), Q-class closure
  (corner-only class, area ≤ 36, wall gaps ≤ 2 by d154), the 18-wall Q-class run (real
  marks), d64/d67 (proper factors) and d126 (one very deep piece). That reading carries no
  information, so the table uses the word-specific split.

## 2. Families

Rules are deterministic on the word and are applied in this order. A **dent** is an edge
whose two ends are both reflex. Dent lemma: horizontal lines meet the room in one interval
iff the room has no horizontal dent. This holds for every realization, so it is a property
of the word, and it matched the rasterized realization of all 4,574 words. Edge
orientation alternates, so the word fixes which dents are parallel.

| Family | Rule | 4 | 6 | 8 | 10 | 12 | 14 | 16 | 18 | 20 | Total |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| rectangle | W = 4 | 1 | | | | | | | | | 1 |
| L, T, Z/S, plus | no dents; corner vector (1,0,0,0), (1,1,0,0), (1,0,1,0), (1,1,1,1) | | 1 | 2 | | 1 | | | | | 4 |
| Ferrers staircase | no dents; one staircase corner (k,0,0,0) | | | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 7 |
| monotone staircase band | no dents; two opposite corners (a,0,b,0) | | | | 1 | 2 | 2 | 3 | 3 | 4 | 15 |
| pyramid | no dents; two adjacent corners (a,b,0,0) | | | | 1 | 2 | 2 | 3 | 3 | 4 | 15 |
| orthoconvex, 3–4 corners | no dents, other | | | | 1 | 2 | 5 | 9 | 13 | 20 | 50 |
| stacked hall, one bank | all dents parallel; word L⁴P, P ∈ {RL, LR}* (histogram) | | | 1 | 2 | 7 | 13 | 32 | 60 | 131 | 246 |
| two-bank (two-sided hall) | all dents parallel; word L P₁ LL P₂ L, not a histogram | | | | 1 | 7 | 21 | 68 | 166 | 428 | 691 |
| spiral | dents both ways; word L^(r+4) R^r, r ≥ 3 | | | | 1 | 1 | 1 | 1 | 1 | 1 | 6 |
| other | dents both ways | | | | | 6 | 34 | 163 | 665 | 2,671 | 3,539 |

"No dents" is exactly orthoconvex. Such a room is a rectangle whose 4 corners are replaced by
staircases of k₁…k₄ steps, with Σk = r. "All dents parallel" is exactly convex in one
direction. The 6-wall L, the T and the plus are the d161 shapes. The 8-wall U is the
one-bank histogram at W = 8. Dumbbells belong to the two-bank family.

## 3. Named rooms and word-specific results

| Room | W | Word | Family | Status of the word |
| --- | --- | --- | --- | --- |
| 6-wall L | 6 | LLLLLR | L | COVERED (d15, d161) |
| cross12 b = 7, CR34 | 12 | (LLR)⁴ | plus | PARTIAL: d161, hall + 4 full-side arms, real pairs |
| DB55, DBas, DBw2 | 12 | (L⁴R²)² | two-bank | PARTIAL: d112 (L > 4d, real), d111, d110, d108 (ℓ coprime to 5), d77 |
| U2 | 10 | L⁷R³ | spiral | PARTIAL: d84, U2 and its stretches, real pairs |
| cov279, st279 | 16 | LLLRLRLRLLLRLRLR | staircase band | PARTIAL: d127, stretches with q ≥ 4, 3 ∤ q, same-parity lattice pairs |
| S10 | 12 | LLLRLRLLLRLR | staircase band | OPEN |
| room 1843 | 12 | LLLRLLRLLLRR | two-bank | OPEN |
| cov446 | 18 | LLRLLRLLRLRLLRLLRR | two-bank | OPEN |
| cov2929 | 20 | LLLRLRLLRRLLLRLRLLRR | two-bank | OPEN |
| cov4181 | 20 | LLLLRRLLRLRLLLRRLLRR | two-bank | OPEN |
| cov4269 | 20 | LLRLLRLLRRLLRLLRLLRR | two-bank | OPEN |
| R22 | 22 | LLLRLRLLRLRLLRLRLLLRRR | other, 1 dent each way | outside W ≤ 20 |

Every named room with W ≥ 12 in this table, except R22, is convex in at least one
direction. R22 has one horizontal dent and one vertical dent. That is also why d161 and the
stacked-hall notes exclude it.

Pending, not counted: d162 (in review) gives a metric subfamily of each one-bank and
two-bank word. terrace-induction.md (unreviewed) gives one for each Ferrers word. Neither
covers every length assignment, so both would leave those words PARTIAL.

## 4. OPEN targets, ordered by OPEN words closed

Each line is one all-lengths theorem. The nested families overlap.

| # | Target theorem (every length assignment) | W = 10 … 20 | Total | Named rooms inside |
| --- | --- | --- | --- | --- |
| 1 | All dents parallel: convex in one direction, which includes two-sided stacked halls (M2) | 7, 20, 44, 115, 246, 588 | 1,020 | cov4181, cov4269, cov2929, cov446, 1843, S10, cov279 |
| 2 | Exactly one dent in each direction (R22's profile) | 0, 6, 26, 86, 240, 586 | 944 | R22 (W = 22) |
| 3 | One-bank stacked halls (histograms), which d162 aims at | 4, 10, 16, 36, 64, 136 | 266 | none |
| 4 | Orthoconvex rooms | 4, 7, 10, 15, 20, 29 | 85 | S10, cov279 |
| 5 | Spirals | 0, 1, 1, 1, 1, 1 | 5 | none (U2 is PARTIAL) |
| | Remainder: dents both ways, 2 or more in one direction | | 2,600 | |

**Smallest OPEN words** (W = 10, 7 of the 8 words). Coordinates are counterclockwise
vertices of one realization.

| Word | Family | Area | Vertices |
| --- | --- | --- | --- |
| LLLRLLLRLR | staircase band | 8 | (2,0) (4,0) (4,1) (3,1) (3,4) (0,4) (0,3) (1,3) (1,2) (2,2) |
| LLLRLLRLLR | orthoconvex, 3 corners | 9 | (1,0) (4,0) (4,1) (3,1) (3,4) (2,4) (2,3) (0,3) (0,2) (1,2) |
| LLLLLRLRLR | Ferrers staircase | 10 | (3,0) (4,0) (4,4) (0,4) (0,3) (1,3) (1,2) (2,2) (2,1) (3,1) |
| LLLLRLLRLR | pyramid | 10 | (2,0) (4,0) (4,4) (3,4) (3,3) (0,3) (0,2) (1,2) (1,1) (2,1) |
| LLLLLLRLRR | one-bank hall | 10 | (0,1) (0,0) (4,0) (4,4) (1,4) (1,3) (2,3) (2,2) (3,2) (3,1) |
| LLLLLRLLRR | one-bank hall | 10 | (0,1) (0,0) (4,0) (4,4) (3,4) (3,3) (1,3) (1,2) (2,2) (2,1) |
| LLLLRLLLRR | two-bank | 10 | (0,2) (0,0) (4,0) (4,1) (3,1) (3,4) (1,4) (1,3) (2,3) (2,2) |

The smallest OPEN words with dents in both directions are 6 words at W = 12, for example
LLLLRLLLLRRR: (2,2) (2,0) (5,0) (5,1) (4,1) (4,5) (0,5) (0,3) (1,3) (1,4) (3,4) (3,2).
The OPEN spiral at W = 12 is L⁸R⁴.

## 5. Ledger-based estimate

Share of words in each status:

| W | COVERED | PARTIAL | OPEN |
| --- | --- | --- | --- |
| 4–8 | 100% | 0% | 0% |
| 10 | 0% | 12.5% | 87.5% |
| 12 | 0% | 6.9% | 93.1% |
| 14 | 0% | 0% | 100% |
| 16 | 0% | 0.4% | 99.6% |
| 18, 20 | 0% | 0% | 100% |
| all W ≤ 20 | 0.13% | 0.09% | 99.8% |

A word count isn't a probability, for these reasons:

- Each word is an infinite family of length assignments. A PARTIAL word can keep all of
  its difficulty in the uncovered lengths. R22's darkness sits at short arm lengths, for
  example (d152).
- The words aren't equally likely to hold a dark room, and they aren't equally hard.
  The known darkness mechanisms need r ≥ 9 (d105, d145).
- The target is universal. One dark room in any word refutes it, so coverage doesn't add
  up like probability mass.
- The counts grow about 3.6× per step in W, so W = 20 dominates. Closing every orthoconvex
  word moves the W = 20 share by 0.9%, even if it is half of the needed ideas.

My view on the estimate:

- Report the ledger split as a mechanical progress measure, separate from the success
  estimate. For each W, give COVERED and PARTIAL words, and name the families closed.
- Keep the success estimate as a labelled GUESS. Factor it along the targets: P(one-direction
  convex closes, target 1) × P(the dents-both-ways remainder reduces to it). Most of the risk
  sits in that second factor: 82% of the W = 20 words (2,672 of 3,260), including R22's dent profile.
- On that basis the ledger doesn't move the current 10–12% estimate. The first factor rises
  only when a reviewed theorem covers a whole word at W ≥ 10, and none does yet.

## 6. Caveats

- Unreviewed. Family rules, the dent lemma and the target counts are this script's.
  The dent lemma is checked on one realization per word, not proved in a memo.
- Realizations aren't area-minimal. Their area and corner-only flags in `ledger.json`
  are one-sided evidence of band contact, not band membership.
- PARTIAL attributions use review scopes as recorded in RESULTS.md §11 and the d84,
  d108, d111, d112, d127 and d161 reviews. The dumbbell credit is for strict mouths only.
  Flush corridors give other words, and d112 doesn't state their scope.
- d76 (D58 ten-wall builder), d87 and d147 prove specific pairs or named rooms, not
  metric families, so they don't change any status.
- 45-degree walls are out of this ledger (milestone M4).
