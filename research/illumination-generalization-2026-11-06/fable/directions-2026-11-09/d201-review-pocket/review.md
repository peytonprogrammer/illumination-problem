# d201 review: pocket lemma and the unequal-length three-chamber theorem

Date: 2026-11-23. Reviewer: independent referee.

Reviewed file: `snapshot.md` in this directory. Context: `../PROGRAM.md` (top
section), `../d200-review-threechamber/review.md`,
`../d154-review-r22arm/review.md` and `../d163-pattern-ledger/STATUS.md`.

Code: [checks.py](checks.py), log [checks.log](checks.log). It uses the
standard library and exact `Fraction` arithmetic, and it runs in 3.2
CPU-seconds. For each of the 729 rooms with 4 ≤ D₁, D₂ ≤ 30 and each of the 66
lattice pairs, it builds the path the note prescribes. For pocket paths it
computes a from the criterion with one floor operation. It traces that single
ray and compares the full bounce list with the predicted one. It runs no ray,
direction, word or room-size search.

## Verdict

**Correct.** The pocket lemma, the matching criterion and the theorem for
independent D₁, D₂ ≥ 4 all hold, and every prescribed ray in all 48,114 traced
pairs reaches its target with exactly the predicted bounces. The errors are one
broken link and three missing one-line justifications. None of them affects a
proof step.

## Per-part verdicts

1. **Pocket return map: correct.**
2. **Matching criterion: correct.** Necessity, sufficiency, roof clearance and
   the spacing wg/(g+h) all hold.
3. **Main theorem: correct.** The outer-wall bounces, the residual middle-pocket
   cases and the D = 4 adjacent repair all hold.
4. **X = Y = 1 and X = Y ≢ 1 (mod 3): correct, and consistent with item 3.**
5. **Corner budget and R22 control: correct with gaps.** No claim is overstated
   in substance. One link is broken, and the R22 argument is slightly stronger
   than stated.

## 1. Pocket return map

**Correct.** The pocket is (0, w) × (0, h) with the mouth on y = 0. Unfolding
the two side walls turns the pocket into the strip ℝ × (0, h), with horizontal
coordinate a + c·(vertical travel).

- The ray meets the roof at a + hc and returns to the mouth at a + 2hc.
- The fold of the strip onto (0, w) has period 2w. A phase s in (0, w) mod 2w
  folds to s with rightward motion, and a phase in (w, 2w) folds to 2w − s with
  leftward motion. So the map is translation by 2hc on the circle ℝ/2wℤ, with
  vertical velocity reversed.
- Side hits occur at unfolded multiples of w strictly between a and a + 2hc.
  Such a hit is at a corner only if it coincides with the roof contact
  (a + hc ∈ wℤ) or the return (a + 2hc ∈ wℤ). The start a is in (0, w), so it
  isn't a multiple of w. These are exactly the note's two exclusions.
- A leftward start at a has phase 2w − a ≡ −a, as the note says.

## 2. Matching criterion

**Correct.** The band legs give c = (a − U)/g and b = V − gc = M − a.

- The return condition is a + 2hc ≡ b (mod 2w). Substituting c gives
  (2 + 2h/g)a ≡ M + (2h/g)U (mod 2w).
- Entry and return in the open mouth mean 0 < a < w and 0 < M − a < w, and
  c > 0 means a > U. Together these give max(0, M − w, U) < a < min(w, M).
- **Rightward exit is automatic.** The congruence puts the return phase in the
  class of b, and b is in (0, w), so the phase is in the rightward half.
- **Roof clearance is automatic.** Adding a to both sides gives
  2(a + hc) ≡ M (mod 2w), so a + hc ≡ M/2 (mod w). A roof corner needs
  M ∈ 2wℤ, but 0 < M < 2w. The mouth-endpoint exclusion holds because
  b ∉ wℤ.
- **Necessity.** Any path with these two band legs and one pocket excursion
  determines c and b as above. So it satisfies both conditions. The note
  states this correctly, restricted to this itinerary.
- **Spacing.** The coefficient of a is 2(g + h)/g, so solutions are spaced by
  2w·g/(2(g + h)) = wg/(g + h). An open interval longer than the spacing
  contains a solution. The note's strict inequality is the right condition,
  because an interval of exactly the spacing can have solutions only at its
  endpoints.

*Gap (low).* The criterion assumes both band legs lie in the room, and the
note states this as a hypothesis. In the theorem the whole band
(0, P + 3) × (1, 2) is in the room, so the hypothesis holds there.

`checks.log`: the control at D₁ = D₂ = 6 shows that the criterion's
a = 1 reaches the target, and a = 5/4, which is off the progression, hits a
corner.

## 3. Main theorem

**Correct.** The room has chambers [s, s + 3] × [0, 3] at s = 0, D₁, P with
P = D₁ + D₂, and corridors at 1 < y < 2. It has W = 20 and exactly 12 interior
lattice points (s + u, y) with u, y ∈ {1, 2}. That gives 66 pairs: 18
same-chamber, 24 different-row, 16 adjacent same-row and 8 outer same-row.

**Same chamber and different rows.** Each chamber is convex. The open band
(0, P + 3) × (1, 2) lies in the room, so every different-row segment is legal.

**Outer chambers, wall bounces.**

- Left case. The image of the source is −u, and the midpoint is (P + v − u)/2.
  Relative to D₁ it is (Δ + v − u)/2. If that's negative, the midpoint is below
  D₁. It also exceeds 3, because P ≥ 8 and v − u ≥ −1 give at least 7/2.
- Right case. The image of the target is P + 6 − v, and the midpoint is
  (P + 6 + u − v)/2, which is 3 + (Δ + u − v)/2 relative to D₁. If that
  exceeds 3, the midpoint is past D₁ + 3. It is less than P because
  P > 6 + u − v.
- Both outer-wall hits are at heights in (1, 2), so they're regular. All legs
  are in the open band.

**Residual cases.** Neither test holds exactly when u − v ≤ Δ ≤ v − u. This
forces u ≤ v, so the residual cases are u = v with Δ = 0, or (u, v) = (1, 2)
with |Δ| ≤ 1. The boundary cases, where the midpoint is at (D₁, 2) or
(D₁ + 3, 2), are corners and are correctly placed in the residual set.

- The note uses the middle upper pocket with w = 3 and h = g = 1, U = u − D₁
  and V = D₂ + v. Then M = Δ + u + v ∈ {2, 3, 4}.
- U ≤ −2 < 0, so the interval is (max(0, M − 3), min(3, M)). Its length is
  min(M, 6 − M) ≥ 2, which is more than 3/2.
- The pocket's flanks x = D₁ and x = D₁ + 3 are solid on [2, 3], and its mouth
  (D₁, D₁ + 3) × {2} is open. So the lemma applies.

**Adjacent chambers.** The bounce (D + u + v)/2 lies in (3, D) if and only if
D > max(6 − u − v, u + v). For D ≥ 4 this fails only at D = 4 with u = v. The
repair unfolds the source to −u and uses the first chamber's upper pocket with
U = −u and V = 4 + u. Then M = 4, and the interval (1, 3) has length 2. The
x = 0 hit is at height 1 + u/(a + u) ∈ (1, 2), so it's regular. Reversing the
room x ↦ P + 3 − x moves a chambers-2-and-3 pair to the front, and it keeps
u = v.

`checks.log`, over 729 rooms:

| Construction | Pairs |
|---|---:|
| Same chamber | 13,122 |
| Different rows | 17,496 |
| Adjacent bounce | 11,448 |
| Adjacent repair (D = 4) | 216 |
| Outer, left-wall bounce | 2,810 |
| Outer, right-wall bounce | 2,756 |
| Outer, middle pocket | 266 |

The middle-pocket paths split as M = 2 (106), M = 3 (54) and M = 4 (106). The
longest bounce list has 21 hits. The controls confirm the failures the note
works around:

- At D = 4, the plain adjacent bounces hit (3, 2) and (4, 2).
- At D₁ = D₂ = 7, the outer left-wall bounce for u = v = 1 hits (7, 2).
- At (D₁, D₂) = (6, 7) with (u, v) = (1, 2), the left-wall midpoint falls
  inside the middle chamber, and the ray hits the corner (9, 3).

**Agreement with d200.** For D₁ = D₂ = 3k + 1, the criterion's first value is
a = u − 1/2 in all 16 checked cases. That is d200's pocket ray. d200's
"at least two horizontal reversals" holds here too, because the pocket ray
makes an even number of side hits, and at least 2.

## 4. Items 1 and 2

**Correct and consistent with item 3.**

- **Item 1 (X = Y = 1, D = 4).** The congruence is 4a ≡ 4 − 2u (mod 6). The
  first solution above 1 is a = 2 for u = 1 and a = 3/2 for u = 2. Both equal
  (5 − u)/2. Also b = 4 − a, the unfolded travel gives a + 2c − b = 6, and the
  roof contact 2a + u = 5 isn't a multiple of 3. `checks.py` asserts each of
  these facts. The item is the same as item 3's repair.
- **Item 2 (X = Y ≢ 1 mod 3).** This forces X ≥ 2, so D ≥ 5 and every
  adjacent bounce clears. At Δ = 0 the congruence is
  4a ≡ u + v + 2(u − D₁) (mod 6). `checks.py` asserts this for every
  chosen a with D₁ = D₂.
- **Item 3 (X ≠ Y).** The only unequal residual is (u, v) = (1, 2) with
  Δ = ±1, so M = 2 or 4, as the note says.

## 5. Corner budget and R22 control

**Local return region: correct.** Take a topmost horizontal wall [x₀, x₁] at
height y_max, and let y₂ be the next lower horizontal-wall height in the room.

- A vertical wall that crosses a height in (y₂, y_max) must end at y_max. So
  its endpoint is a vertex of a topmost wall, and none lies in (x₀, x₁).
- So (x₀, x₁) × (y₂, y_max) is interior, and the walls below x₀ and x₁ flank
  it.
- Its height can be less than 1. This is why the R22 control needs height ≥ 1.

**Reflex budget: correct.** An orthogonal room has W = 2r + 4, so W ≤ 20 gives
r ≤ 8. A corridor inset on both sides costs 4 reflex corners, so at most two
fit. The note says correctly that this bound forces no structure.

*Gap (low).* "Strictly inset" carries the claim. A corridor flush with one
chamber wall costs only 2 reflex corners, so a W ≤ 20 room can have three or
four flush necks. The note should say so.

**R22 control: correct.** Running `checks.py` on d8's `R22-base` cells
recomputes d154's fact: the odd–odd class has 9 corners and no interior or
smooth points. The parity argument is sound.

- The open horizontal span has at least 2 integers, so it has an odd one.
- The closed vertical span has at least 2 integers, so it has an odd one.
- The resulting point is interior, an open-mouth point or a smooth roof point.
  The roof is smooth because the room is strictly simple.

`checks.py` lists every integral full-mouth pocket with width ≥ 3 and
height ≥ 1, in all four orientations. It finds none.

*Strengthening (observation).* "Integral" is automatic for the flanks and the
roof, since they are lattice walls. A pocket with a fractional mouth and
height ≥ 1 contains an integral one, with its mouth at ⌈y₀⌉. So the hypothesis
can be weakened to width ≥ 3 and height ≥ 1.

*Scope.* R22 has W = 22, so it's a control and not a W ≤ 20 statement. The
note doesn't claim that a pocket forces lighting in general, and it shouldn't.
The note doesn't overstate this.

**Broken link (low).** The D154 link
`../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d154-review-r22arm/review.md`
doesn't resolve from this directory. *Fix:* use
`../d154-review-r22arm/review.md`.

## Errors and fixes

1. **Low (§5 link).** The D154 link is broken. *Fix:*
   `../d154-review-r22arm/review.md`.
2. **Low (§5 budget).** The four-shoulder count needs a corridor inset on both
   sides. *Fix:* add "a corridor flush with a chamber wall costs two reflex
   corners, so flush necks are not bounded by this count".
3. **Low (§2).** The note asserts the band-leg containment for the theorem
   without saying why. *Fix:* "the open band (0, P + 3) × (1, 2) lies in the
   room".
4. **Observation (§5 R22).** The R22 exclusion holds without "integral". See
   the strengthening above.
5. **Scope (theorem).** The theorem covers lattice marks only. Real and
   rational marks (L3) aren't treated, although the pocket criterion itself
   doesn't need lattice marks.

## Which lemma does this advance, and what is the first case still open?

**L1.** The note extends d200's one-parameter family X = Y = 3k + 1 to all
independent corridor lengths X, Y ≥ 1, with every lattice pair lit. This
closes the three cases that d200 left open: X = Y = 1, X = Y ≢ 1 (mod 3), and
X ≠ Y. It gives a two-parameter lighting tail for aligned 3 × 3 chambers. The
pocket criterion is also a reusable tool for other band-plus-pocket rooms.

**First case still open.** In the same wall-turn word, every room with a
chamber that isn't 3 × 3, or with an aperture other than 1 < y < 2, is still
open. The smallest by area has X = Y = 1 with one chamber 4 wide, or the
middle chamber 4 tall with the aperture still at 1 < y < 2. Each has area 32.

The 4-tall middle chamber has an asymmetric pocket with h = 2 and g = 1, and
the criterion's spacing drops to 1. So the residual-case argument needs a new
interval estimate. The note's named next case, vertically displaced apertures,
is also in this word, and it is the harder of the two. Real marks remain open
in every case.

**Smallest W ≤ 20 room not covered.** In this word, area 32, as above. That's
above L2's area-20 census.

## Ledger effect

The room's wall-turn word is `LLLLRRLLRRLLLLRRLLRR` (W = 20, r = 8, family
"one-direction convex"). `ledger.json` still lists it as OPEN, and `STATUS.md`
has no row for d200 or d201. The coordinator should record it as **PARTIAL**,
citing d200 and d201.

**It doesn't move to COVERED.** COVERED needs every length assignment of the
word. The theorem fixes every length except the two corridor lengths. These
lengths are still missing:

- the three chamber widths (fixed at 3);
- the three chamber heights (fixed at 3);
- the two corridor heights (fixed at 1);
- each aperture's vertical position in each chamber wall it pierces (fixed at
  1 < y < 2 in all four walls, so the two corridors are aligned).

Real (L3) marks are also missing for every assignment.
