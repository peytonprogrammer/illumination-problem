# D109: review of qclass-closure/bbbb/band-reachability.md

Date: 2026-11-20. Reviewer: independent referee. All computation is exact
(`fractions.Fraction`, integer cylinder data), Python with `-B`, under 15 CPU
seconds in total. Only named rooms are used: DBas from d69, and the note's
own corridor family at stated lengths ℓ.

## Verdicts

| Claim | Verdict |
| --- | --- |
| 1. Both least axial multitwists fix every lattice lift of (1,3) and (11,3) in DBas | Sound. Computed from the cells: λ_H = 520, λ_V = 24, and no lattice level moves in any cylinder. |
| 1'. Hence no admissible two-band configuration exists | Sound. It also survives the larger axial stabilizer that allows half-turns on fold rims (see below). |
| 2. Shot (1,3) with velocity (7,−2) | Sound. Exact events: door (5,13/7), floor (8,1), door (9,9/7), cap (13,17/7), arrival (11,3). No corner contact. d103's unfolded tracer agrees with v = (14,−4). |
| 3a. Obstruction at every corridor length, arbitrarily large prime n | Sound. Checked for all 64 primes n = 44+ℓ ≤ 400. |
| 3b. A_n at prime n ≥ 67 | Sound by citation (d99 claim 1a holds at n ≥ 49). The note doesn't explain the bound 67. It is the least prime above 64, where d69 §1 gives BBBB for any normalized room with r ≤ 8. |
| 3c. One-reversal path for n > 89 | Sound. The doorway criterion is correct, and the bound ℓ > 45 is tight for this construction. |
| 4. Scope | DBas is strictly simple and BBBB, with r = 4 and n = 48. It refutes universal axial band reachability, not twist methods in general. |

## Claim 1: cylinders of the double

`cylinders.py` builds the decomposition from the cell set. Two strips merge
only if their shared level has no corner on the closed run. DBas cells match
`d69-bbbb/decomp.py` exactly (`classtypes.py` asserts this).

| Direction | Cylinders (C, h) | Least λ |
| --- | --- | --- |
| Horizontal | (10,1), (10,2), (26,1), (8,2), (8,3) | lcm(10, 5, 26, 4, 8) = 520 |
| Vertical | (8,5), (2,4), (12,4) | lcm(8, 1, 3) = 24 |

This matches the note's table. Every rim sits at an integral level, so a
lattice point lies at integral distance j from its lower rim. Every C divides
λ, so the shift λj mod C is 0 at every j. That covers both sheets, and the
critical graph is fixed pointwise by construction. `cylinders.log` shows an
empty list of moved levels in both directions.

**Admissibility.** The horizontal test needs S′ and T′ at heights h−a and
h+b with a, b > 0. Here S and T stay at height 3. The axis-exchanged test
needs two constant-height column runs from x = 1 to x = 11. The column
profiles are [0,4], [1,2] and [−1,5], so three runs are needed. Both
orientations fail, and so does the reversed path.

**Strengthening (by hand).** Allow fold rims to turn by C/2, the only other
rotation compatible with the fold involution. Rims through reflex corners
stay pointwise fixed, because no nontrivial rotation preserves their
singular positions. The least shears are then μ_H = 260 and μ_V = 12.

- At S, the shifts are 260 mod 10 = 0 and 12·4 mod 8 = 0.
- At T, μ_H shifts by 260 mod 8 = 4, which swaps the front and back lifts of
  T. The physical point stays (11,3), since x ↦ 22 − x fixes x = 11.
- At T, μ_V shifts by 12·2 mod 12 = 0.

So even this larger axial group fixes S and T physically. It only permutes
lift choices, which the note already ranges over.

## Claim 2: the lighting path

`path.py` reflects a ray off the actual polygon edges, in exact arithmetic.
It raises an error at any vertex hit. Output, from `path.log`:

    reflect-horizontal wall      (8,1)
    reflect-vertical wall        (13,17/7)
    reach                        (11,3)
    door crossings [(5, '13/7'), (9, '9/7')]
    d103 unfolded trace v=(14,-4) -> (11,3)

Both door heights are strictly inside (1,2). Both wall hits are smooth: the
floor corners are at x = 5 and x = 9, and the cap corners at y = −1 and
y = 5. Two independent tracers agree.

## Claim 3: the corridor family

**Twists.** Every member has λ_V = 24 and λ_H = lcm(40, 2(9+ℓ)). No lattice
level moves for any of the 64 primes n = 44+ℓ ≤ 400. Each member has 12 walls
and 4 reflex corners, and no pinch: `boundary_cycle` asserts out-degree 1 at
every vertex and a single boundary cycle. The note's T has offset c, so T is
odd/odd like S.

**Types.** d66's `test_room`, as called by d69's `verdicts.py`, returns
BBBB and normalized at ℓ = 4, 23 and 53 (`classtypes.log`). For general
prime n ≥ 67, the note relies on this without stating it. d69 §1 supplies
it: a normalized room with r ≤ 8 and area > 64 is BBBB. This is a minor
presentation gap and needs no fix to the mathematics.

**Doorway criterion.** I rederived it as follows.

1. Unfold the corridor height onto a circle of length 2.
2. Entry at height e₁ = 2−4m above the floor while descending, and exit at
   e₂ = 2−bm while ascending, require (ℓ+4+b)m ≡ 0 mod 2.
3. The note writes this as "∈ 4+2ℤ". That set equals 2ℤ, so the notation is
   odd but not wrong.
4. The window 1/4 < m < 2/b is correct for b = 6 and b = 7.
5. An open interval of length > 2 contains an even integer.
6. Prime n > 2 forces odd ℓ, so b = 7, and (ℓ+11)/28 > 2 gives ℓ > 45.

The scan in `path.log` tests every prime n ≤ 400. Every slope that the
criterion admits traces exactly to T, with one vertical-wall reflection,
both doors open, and d103's tracer in agreement. These are 6 slopes at n ≥ 383.

**Named members.** The note defines members only by ℓ. I traced ℓ = 53
(n = 97, m = 9/32, 15 corridor bounces) and ℓ = 57 (n = 101, m = 9/34).
Both reach T. The doors are at 15/8 and 33/32 for ℓ = 53, and at 33/17 and
39/34 for ℓ = 57.

**Tightness.** n = 67, 73 and 89 have no admissible slope of this form. At
n = 89 the interval is exactly (14,16). This is consistent with "n > 89".
These three pairs are still lit: d103's `find_path` returns v = (−36,−8),
(−42,−8) and (−58,−10). Those paths first travel left, so they use two
horizontal reversals (`family.log`).

## Claim 4: scope

- DBas is strictly simple, with 12 walls, r = 4, n = 48, normalized, and type
  BBBB. The class types agree with d69's verdicts.log.
- The pair is **lit**. DBas is a counterexample to universal axial band
  reachability, not to illumination.
- It refutes the following strategy: reach the two-band test, as stated in
  twist-overlap.md, by words in the axial multitwists. This holds at r = 4 and
  n = 48, and for an infinite primitive family with G ⊇ A_n.
- It doesn't refute twist methods in general. Three routes stay open:
  - Multitwists in nonaxial rational directions, which can move lattice
    points.
  - Windows certified by reflected routes, as DB55 already uses.
  - Itinerary-level criteria like the note's cap reversal.
- The note's scope paragraph says this correctly. It also notes that a
  general BBBB room may lack a separating corridor, which is the honest
  limit of the cap construction.

## Re-run

From this directory:

    python3 -B cylinders.py 4 23 53 57 > cylinders.log
    python3 -B classtypes.py 4 23 53     > classtypes.log
    python3 -B path.py 400               > path.log
    python3 -B family.py 400             > family.log
