# D114: review of qclass-closure/bbbb/degree-gluing.md

Date: 2026-11-20. Reviewer: independent referee. All computation is exact
(`fractions.Fraction`), runs under Python with `-B`, and takes 6 CPU-seconds in
total. `tracer.py` is new code and shares nothing with d103, d109, d112 or d113.
Only named rooms are used: DBay (the note's 20-wall room) and its stretches
L = 4 + 66k, the odd crosses P_7 and P_9 with their cap doubles, and the
notched square from the note. No room or word search was run. Every traced
slope is one of three kinds: a constant stated in the note or d113, a root of
the note's phase equation, or a slope built through a named cap corner.

## Verdicts

| Claim | Verdict |
| --- | --- |
| 1. Cap doubling | Sound. The projection lemma is correct and checks exactly on P_7 and P_9. There are two minor citation gaps and no error. |
| 2. No local cancellation | Sound as a negative statement. One number in the supporting table text is wrong: "−+ after three" should read "after nine". |
| 3. Degree identity | Correct. The telescoping formula and the derivative (2j+1)L + Σ travels check exactly for j = 0, 1, 2. |
| 4. 31/23 and L = 4 + 66k | Correct. Every number reproduces. The fix from 8 + 86k to 6 + 86k is right and matters at k = 3. |
| 5. Scope | Accurate. The positive result is for a fixed hub, with a non-effective threshold. |

## Claim 1: cap doubling

**Statement as written.** A rectangle of length ℓ and width w attaches to a
junction J along one full mouth and ends in a flat cap with two convex corners.
Gluing two copies along the cap gives a 2ℓ separating passage between J and
its mirror. Projection lemma: a legal one-traversal connection between opposite
junction copies projects to a legal path between the original distinct marks.
Whole-room tail: for any fixed strictly simple bounded orthogonal junction with
a fixed positive-width mouth, all distinct interior pairs are lit for
sufficiently large ℓ, with a sufficient threshold ℓ ≥ max(w/δ, 2w/δ₁).

**Proof check.**

- *Fold.* The fold maps copy 2 isometrically onto copy 1 and preserves every
  wall and corner. The only exception is the cap: its two convex corners have
  angle π/2 in each copy, so in the double they become smooth points of
  angle π. An interior cap crossing folds to an ordinary cap reflection.
- *Cap-end event.* Suppose the double path meets a cap end at time a. The
  incoming velocity (vx, vy) reflects to (vx, −vy). Folding gives
  (−vx, −vy), so the folded path retraces the incoming path exactly. If the
  total time D satisfies D < 2a, then T lies on the incoming leg at time
  2a − D, before the corner. If D > 2a, the folded path passes S at time 2a
  and continues along −v for time D − 2a. That stretch is the fold of a part
  of the double path that doesn't cross x = ℓ again, so it is legal. D = 2a
  would force T = S. The lemma's "one crossing of the cap line" is automatic:
  horizontal velocity keeps its sign in a corridor, so one traversal crosses
  x = ℓ once.
- *Case split.* The cases are junction–junction (README theorem at length
  2ℓ), junction–strip (one-door version with depth h = 2ℓ − z ≥ ℓ, needing
  ℓδ₁ ≥ 2w), and junction–mouth (h = 2ℓ). Strip–strip, strip–mouth and
  mouth–mouth pairs are direct, since the arm is convex. Together these cover
  every pair. The README criteria (2ℓ + a + b)δ ≥ 2w and (h + a)δ₁ ≥ 2w give
  the stated threshold.

**Gaps (minor).**

1. The README theorem assumes the joined room is strictly simple at each
   length. The note instead says to keep the copies abstract, and not to
   apply theorems that need a planar embedding. This is harmless:
   - The README proof uses only the sealed chambers and the corridor.
   - For ℓ larger than the x-extent of J beyond its mouth, J' lies strictly
     past J and the double embeds as a strictly simple room. On P_7 and P_9
     the double is one boundary cycle with W = 20, r = 8.

   The note should say one of these two things.
2. Two claims are asserted, not proved:
   - "Uniform on compact nondegenerate junction families by joint first-hit
     stability" is a plausible sketch. Local constancy in the geometry is
     not written out.
   - The rectangular-junction remark cites resonant-gluing.md and isn't
     checked here.

δ and δ₁ have no values, so the threshold is non-effective. The note doesn't
claim otherwise.

**Exact test** (`cap.py`, `cap.log`). The east arm [2,b]×[−2,2] of P_b (w = 4,
ℓ = b − 2) is doubled across x = b. For each pair, the double path's slope is
an exact root of the note's phase equation F ∈ 8ℤ on fixed itineraries. Each
root comes from Newton steps on that piecewise-affine increasing F, started
from a fixed list of 8 base slopes. The full double path is then traced, and
its fold is traced in P_b.

| Pairs tested (each at b = 7 and b = 9) | Result |
| --- | --- |
| 4 junction–junction, including real marks (−3/2, 1/3)–(1/7, b − 6/5) | 8/8 double paths with one cap-line crossing; fold reaches T at the same time |
| 3 junction–strip, including (−1/3, −7/5)–(b − 1/9, 3/2) | 6/6, same |
| 2 junction–mouth: (−3,0)–(2,1) and (1, 2 − b)–(2, −3/2) | 4/4, same |
| 3 strip/mouth pairs | 6/6 direct segments |
| 3 built cap-corner cases: S = (0,1), v = (b,1) through (b,2), T' at τ = 3/2, 23/10, 37/10 | Fold hits the cap corner. T is reached at 2a − D = 1/2 on the incoming leg (τ = 3/2). For the other two τ, the reversed ray from S reaches T at D − 2a. 6/6 as the lemma predicts. |

None of the constructed matches happened to hit a cap end. The three built
cases are the only test of the deletion step, and they cover both of its
branches. ℓ = 5 and 7 are not claimed to exceed the theorem's threshold, so
these runs test the mechanism, not the threshold.

## Claim 2: no local cancellation

- The room double has cone angle 2 · (3π/2) = 3π at a reflex corner. The two
  limits of a graze leave at +π and −π from the incoming radius. Measured
  through the incoming side, the gap between them is 2π. The other way it is
  3π − 2π = π. Either way they are distinct germs, and they would coincide
  only at cone angle 2π.
- The pairing of sectors comes from varying a transverse section. A single
  source at one slope has exactly four launches, so the cone supplies no
  second ray. The note says the cone "gives" no such ray. It doesn't claim
  that one never exists, and that is the correct reading. A universal
  nonexistence claim would be unproved: a cone point of angle 6π in the
  4-fold unfolding has 3 incoming separatrices per direction.
- At 43/33 my tracer shows the four launches stop at (9,2), (3,4), (1,0) and
  (1,4). Only +− reaches (3,4), so no other launch realizes the other sector
  there.

The 43/33 table checks out (`room43.log`):

- I recomputed the cycles with my own full-room trace from the ±1/132
  offset starts, without the note's chamber-transport code. They match
  `degree-control.py`.
- The target phases are 65, 41, 5 and 43, so the required source phase is 49.
- The multiplicities are 55 below and 85 + 85 = 170 above.

`degree-control.py` reruns and reproduces the 450/450 counts at residue 0 and
450/335 at residue 4.

**Error.** Above the graze, launch −+ first reaches phase 49 at round trip
**9**, not 3; its cycle is [57, 9, 37, 5, 13, 45, 25, 23, 21, 49, 29]. The
values 5 (−+ below) and 7 (++ above) are right, and so are the
multiplicities. The conclusion stands.

The offset-start argument is sound for fixed finite itineraries. Two facts
support it:

- At slope 43/33 the developed ordinates on integer vertical lines are
  multiples of 1/33, and 1/132 is smaller than that.
- Both perturbations shift the developed line to the same side at all
  positive times.

The note correctly declines to exchange the limits.

## Claim 3: degree identity

- **Counting formula.** Hits on a regular increasing piece number
  H(F(b−)) − H(F(a+)), with θ generic. Telescoping over the pieces gives the
  endpoint change minus Σ[H(F(s+)) − H(F(s−))]. This is correct. Across the
  43/33 graze on [s₀ − 30/3300, s₀ + 30/3300] it gives
  0 = 1 − 1, which matches the regular branches exactly.
- **Derivative.** By unfolding, d(εy)/ds equals ε² times the developed
  horizontal travel, which is the travel itself. So F' is the total
  horizontal travel. I checked it exactly at s ± 10⁻⁹ on lit paths, with the
  backward target launch set to the reversed arrival direction:

| Path | Crossings (j) | F_j | dF/ds | Total travel |
| --- | --- | --- | --- | --- |
| 5/4 up, L = 4 | 1 (0) | 4 | 120 | 120 |
| 13/10 down, L = 4 | 3 (1) | 6 | 440 | 440 |
| 27/20 up, L = 4 | 3 (1) | 6 | 200 | 200 |
| 71/53 down, L = 70 | 5 (2) | 94 | 1060 | 1060 |

The note's remark that summing over unbounded j needs a normalization is
correct.

## Claim 4: 31/23 and L = 4 + 66k

**k = 0, s = 31/23, launch up.**

- The top hit is at x = 85/31. The unfolded height is 49, and
  49 − 33s = 104/23 > 4.
- The source door is at y = 40/23 = 57 − 41s, moving down, after travel 41.
- The target backward door is at y = 38/23 = 3 − s, moving down.
- F = 124/23 − 17/23 − 15/23 = 4, which equals 46s − 58. The continuation
  46s − 56 gives 6.
- The full trace reaches T after 26 reflections: 21 in the source chamber, 5
  in the corridor and 0 in the target chamber. It makes 1 crossing and has
  developed displacement (46, 62).
- Launched down at the same slope, the ray hits (1,4).

**The k ≥ 2 proof.**

- On the upper chart, F = (40 + 66k)s − 48, and F = 6 + 86k gives
  s_k = (54 + 86k)/(40 + 66k).
- s_k − 43/33 = 62/(33(40 + 66k)), which is positive and decreasing.
- s_2 = 113/86, and 46/35 − 113/86 = 1/3010.
- On (43/33, 46/35), three conditions hold: 47 − 31s > 4,
  47 − 33s < 4, and 1 < 47 − 35s < 2.
- The corridor entry and exit heights lie strictly in (1,2), so no lip is
  touched.
- s_0 = 27/20 and s_1 = 70/53 fall outside the window, which is why k ≥ 2 is
  needed.

The proof is complete.

**Traces of the designated pair.**

| k | L | s | Result |
| --- | --- | --- | --- |
| 0 | 4 | 31/23 up | lit, 1 crossing |
| 1 | 70 | 71/53 down | lit, 5 crossings, 818 reflections |
| 2 | 136 | 113/86 | lit, F = 178, 1 crossing |
| 3 | 202 | 156/119 | lit, F = 264, 1 crossing |
| 10 | 664 | 457/350 | lit, F = 866 |
| 100 | 6604 | 4327/3320 | lit, F = 8606 |
| 1000 | 66004 | 43027/33020 | lit, F = 86006, 86,023 reflections |

**Correction.** d113's numerator 56 + 86k gives F = 94, 266 and 868 at
k = 1, 3 and 10, which is 8 + 86k. Its review labels these "req + 2", which
is wrong. At k = 3 its slope 157/119 hits (1,0), while the corrected 156/119
is lit. The note's correction is right, so the pair is lit for every k ≥ 0.

## Claim 5: scope

The note's limits are stated accurately:

- There is no fixed-pair cancellation lemma.
- There is no length threshold from dropping the jump term.
- The cap theorem covers one long arm on a fixed hub.
- The note correctly says this gives nothing uniform for P_b, where three
  other arms grow too.

The notched-square obstruction checks out at m = 5, 9 and 21:

- W = 8 and r = 2, with the reflex corners at the notch bottom.
- The area is m² − 1.
- The wall gcd is 1 on both axes.
- Each parity class has interior points.
- The normalized gaps are 1/m in x and 1/m in y.

It is a geometric obstruction to compactness, not a dark pair, as the note
says. The claim that the BBBB class follows from the d69 area criterion is
cited, not checked. Nothing in the note closes any part of the open BBBB core.

## Re-run

From `d114-review-degree/`:

```
python3 -B room43.py > room43.log   # claims 2-4 (about 4.5 s)
python3 -B cap.py    > cap.log      # claim 1 and the notch (about 1.5 s)
python3 -B ../../../../qclass-closure/bbbb/degree-control.py   # the note's own control
```
