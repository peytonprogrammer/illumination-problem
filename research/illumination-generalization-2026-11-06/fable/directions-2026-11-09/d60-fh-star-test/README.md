# d60: falsification test of FH* (d59 route 1)

Date: 2026-11-18. Named rooms only (cross12, dumb12, R22, P6), exact
permutation arithmetic, one process at a time. Tags: **COMPUTED** (exact
check here), **PROVED** (argument here), **GUESSED** (judgment).

## Answer

- **FH\* as stated survives on interior marks under the weak reading.**
  Across all four rooms, every (room, minimal N, interior pair) row is
  `lifts` or `n/a`, with 0 violations (COMPUTED).
- **The strong reading is false.** "Every N-witness lifts" fails on lit
  pairs in cross12 and dumb12, including a pair with distinct images
  (COMPUTED).
- **The "or equal" branch is false under every lift reading.** It fails in
  three places (COMPUTED):
  - R22 with smooth wall marks, at its only (minimal) factor: 2 violations.
  - cross12 at the non-minimal 3-block factor: 2 interior violations.
  - cross12 at the tower step N6 -> N3, which the induction needs: 2
    interior failures.

  Every failure is a pair with equal images in N that is lit in DP and has
  no certificate.
- **Minimal repair.** Split FH\* into two branches:
  - Distinct images lit in N: the lift statement. It holds in every tested
    row (COMPUTED).
  - Equal images: the conclusion becomes "lit in DP", with no lifting. It
    holds in every tested row (COMPUTED), but it's a restatement of the
    target on one fibre.

## Definitions used

DP is the double of the room as an n-sheeted pillowcase cover with tuple
`(g_a, g_b, g_c, g_d)`. The tuple comes from d10 `room_tuple`, with class
origin S. N = DP / Pi for a block system Pi of G with 1 < |Pi| < n. "Minimal"
means no proper block system other than the discrete one refines Pi.

Pairs are all unordered pairs of interior lattice points, in all parity
classes:

- **Same class (T is an a-point).** The admissible arcs are a -> b, c, d.
- **Mixed class (T is an x-point).** The only admissible arc is a -> x.

The `--wall` runs also include smooth wall points as marks. These are an
extension beyond the brief.

Per basis in the pure-braid orbit, for each admissible tail arc:

| Flag | Meaning |
| --- | --- |
| Nlit | Some images phi(S~) != phi(T~) are joined in the N arc graph. Interior vertices must be 2-cycles of N. Endpoints may be N-regular or N-poles. |
| Nlit_reg | The same, with both endpoints N-regular (the d6 `marked_orbit` rule on N). Logged; it never changed a verdict. |
| Qlit | Some S~, T~ are joined in DP (ground truth). |
| Qadm | Some S~, T~ are joined in DP through interior vertices that are 2-cycles of DP **and** map to 2-cycles of N. |

A Qadm path is exactly a lift of an N-lighting path. DP -> N is unramified
over N-regular points, so the lift is unique once you fix the starting sheet.
A path in a cycle component may wrap more than once.

The block system is part of the canonical form, so every basis uses the same
factor. The readings of "some lift of an N-lighting path joins lifts of S and
T" are:

- **STRONG.** In every basis and arc with Nlit, Qadm holds in that same basis
  and arc. This means "the lift of the witness".
- **WEAK.** Qadm holds in some basis and arc. This means "a lift of some
  N-lighting path".
- **ANY.** Qlit holds somewhere, which means the pair is lit in DP. No factor
  condition applies.

The hypothesis is "images equal, or Nlit somewhere". Certificates come from
d10 `unified_test.analyse_pair` over all block systems. That covers Par, Cut,
and Rig over B, plus ParRel and RigRel. A pair counts as `certified` only
when every lift pair is certified. The framework defines certificates for
same-class pairs only, so mixed pairs are never certified.

The verdict for each row is:

| Verdict | Condition |
| --- | --- |
| `n/a` | Hypothesis fails. |
| `certified` | Hypothesis holds and the pair is certified. |
| `lifts` | Hypothesis holds, no certificate, and WEAK holds. |
| `VIOLATION` | Hypothesis holds, no certificate, and WEAK fails. |

Ground truth comes from three deciders:

- My BFS (Qlit).
- d9 `orbit.decide` on the pair, with early stop when lit.
- d6 `marked_orbit` on same-class pairs when n <= 15.

All three agree on every pair; the script asserts this.

## Classification table (COMPUTED)

### Interior marks (the brief)

Each row is one (room, N, pair) combination.

| Room (W, n) | Pairs: same / mixed | N (blocks, degree) | lifts | certified | n/a | VIOLATION | STRONG fails / computed | DP truth |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| cross12 (12, 12) | 2 / 8 | 3 minimal N6 (6, 2) | 30 | 0 | 0 | **0** | 4 / 30 | 10 lit |
| cross12 | same | non-minimal N3 (3, 4) | 8 | 0 | 0 | **2** | 0 / 8 | |
| dumb12 (12, 20) | 4 / 24 | minimal N10 (10, 2) | 28 | 0 | 0 | **0** | 5 / 5 (*) | 28 lit |
| R22 (22, 15) | 1 / 0 | minimal N5 (5, 3) | 0 | 0 | 1 | **0** | n/a | 1 dark |
| P6 (28, 20) | 1 / 0 | minimal N5 (5, 4) | 0 | 0 | 1 | **0** | n/a | 1 dark |

(*) For mixed dumb12 pairs, the BFS stops at the first Qadm basis
(`--early-mixed`), so STRONG isn't computed there. The 5 computed cases are
the 4 same-class pairs plus `strong_probe.py` on (1,1)-(1,2). That pair has
distinct images, and 1,984 of its 5,392 N-witnesses don't lift.

The R22 and P6 named pairs have images that are distinct and **dark** in N5,
so FH\* is silent on them. Each is certified by "one parity factor": Par at b,
c, and d over N5, for all 4 lift pairs. Across all runs:

- 0 certified pairs are lit.
- 0 same-class pairs are dark and uncertified.

The two cross12 violations at N3 are the named cross pair (1,2)-(3,2) and
its rotation (2,1)-(2,3). Both have equal images in N3 and are lit in DP. No
DP lighting path avoids points over N3-poles. The horizontal path goes
through the b-point (2,2), and N3 has only poles over b.

### Tower step (cross12, `fh_tower.py`)

In this check, N' = N6 plays the role of DP and N = N3 plays the minimal
factor.

| Marks | Steps | lifts | NO LIFT | Vacuous (images already equal in N6) |
| --- | --- | --- | --- | --- |
| Interior | 30 | 24 | **2** | 4 |
| Interior + wall | 108 | 96 | **4** | 8 |

The failures are the same pairs as above. Their images are equal in N3 and
lit in N6, but no lift of an N3-lighting path exists.

### Extension: smooth wall marks (`--wall`)

| Room | Pairs: same / mixed | N | lifts | certified | n/a | VIOLATION | DP truth |
| --- | --- | --- | --- | --- | --- | --- | --- |
| cross12 | 12 / 24 | 3 minimal N6 | 108 | 0 | 0 | **0** | 36 lit |
| cross12 | | non-minimal N3 | 32 | 0 | 0 | **4** | |
| R22 | 8 / 20 | minimal N5 | 22 | 0 | 4 | **2** | 24 lit, 4 dark |

The R22 violations are (0,0)-(4,0) and (2,-2)-(2,2). Both are uncertified,
lit in DP, and have equal images in N5. This is a violation of FH\* exactly
as stated: N5 is minimal above DP, and FH\* puts no condition on where the
marks sit. The 4 dark R22 pairs are all certified by one parity factor.

## Why the equal branch must fail (PROVED)

Suppose N has no 2-cycle over b, c, or d, as with R22's N5, a "parity
factor". Then:

- No N-lighting path exists between distinct a-images.
- Every same-class DP path has an interior x-vertex. Its image is a pole or a
  zero of N.

So WEAK fails for every same-class pair, and FH\* reduces to two cases:

- **Distinct images.** The pair has a Par certificate.
- **Equal images.** FH\* would require a lift that can't exist. Any lit pair
  with equal images is a violation.

cross12's N3 is the same mechanism at one class. Its b-points are all poles,
which is the d39 Cut picture.

## Repair and retest

Each candidate repair was checked against all rows above (COMPUTED):

| Candidate repair | Outcome |
| --- | --- |
| Read the conclusion as STRONG | Worse: 9 failures on lit pairs. |
| Allow lifts through a different minimal factor | Fixes cross12 N3, because the N6 factors lift. Doesn't fix R22: N5 is its only proper factor. |
| Drop "or equal" and require Nlit | 0 violations, but FH\* is then silent on every equal-image pair. At B every pair has equal images, so the induction can't start. |
| **Two branches: (a) distinct images lit in N ⇒ WEAK lift; (b) equal images and uncertified ⇒ lit in DP** | 0 failures. (a) holds on all 146 distinct-image, lit-in-N, minimal-factor rows (50 interior). (b) holds on all 18 equal-image uncertified rows (10 interior), all of them lit in DP. |

Branch (b) has no lifting content. It's the original "uncertified ⇒ lit"
target restricted to one N-fibre. That's where the Cut and fold mechanisms
live: light passes through DP-regular points over N-poles.

## What this means for route 1 (GUESSED, from the COMPUTED rows)

- The lifting half of FH\* looks sound. Distinct lit images lift in all 146
  such minimal-factor rows, with interior and wall marks combined. That half is
  the easy direction, close to covering-space path lifting.
- The hard content of route 1 sits in the equal-image branch at each level of
  the tower. At B, every pair is in that branch. The tower therefore doesn't
  reduce the problem. It relocates it to "an uncertified pair in one fibre of
  a minimal factor is lit". You'd need a fibre-level lemma about paths
  through points over N-poles, which is a Cut/fold-type statement, not a
  group-theoretic one.
- Interior marks alone hide this on R22 and P6, because each has only one
  interior pair. The minimum-wall question concerns interior marks. Even so,
  the induction must handle intermediate surfaces such as N6, whose marks
  aren't room-interior points. The tower failure on cross12 already happens
  with interior marks.
- Suggested next statement to test: "equal images in a minimal N and
  uncertified ⇒ some DP path joins them whose N-image is a closed N-path
  through N-poles". This is a fold-certificate converse, testable with the
  same scripts.

## Files and CPU

| File | Content |
| --- | --- |
| `fh_star.py` | The test. `python3 -B fh_star.py [--wall] [--early-mixed] [room]` writes `fh_star[_wall]_<room>.json`. |
| `fh_tower.py` | Tower step N6 -> N3 on cross12. Writes `log_tower_cross12[_wall].txt`. |
| `strong_probe.py` | Full STRONG check on dumb12 (1,1)-(1,2). Writes `log_strong_probe.txt`. |
| `summarize.py` | Counts. Writes `summary.log`. |
| `log_*.txt` | One line per (room, N, pair). |

CPU: final runs take about 35 s in total, with P6 at 22 s. The whole session
used about 6.5 CPU-minutes. About 5 of those went to abandoned runs: a d9
orbit with all 8 dumb12 marks labelled, and full mixed-class orbits on dumb12
of up to 165,888 states.
