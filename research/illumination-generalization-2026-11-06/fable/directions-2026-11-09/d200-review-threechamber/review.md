# d200 review: three-chamber family lighting theorem

Date: 2026-11-23. Reviewer: independent referee.

Reviewed file: `snapshot.md` in this directory. Context: `../PROGRAM.md` (top
section), the d152 entry in `../d70-writeup/RESULTS.md` §11, and
`../d199-review-darkstructure/review.md`.

Code: [checks.py](checks.py), log [checks.log](checks.log). It uses the
standard library and exact `Fraction` arithmetic, and it runs in 2.5
CPU-seconds. It traces only the rays the note prescribes, in the named rooms
k = 6..40. It runs no ray, direction, word or room-size search.

## Verdict

**Correct.** Every pair of distinct interior lattice points in the named
family is lit for k ≥ 6, and the proof also works for k ≥ 1. The gaps are
expository: two one-line justifications are missing, and the scope is
understated.

## Family identification

The room matches d152's three-chamber family with X = Y = 3k + 1.

- d152 and d199 build chamber [0,3]×[0,3], corridor [3, 3+X]×[1,2], chamber
  [3+X, 6+X]×[0,3], and so on. The middle chamber starts at x = 3 + X, so
  D = 3 + X = 3k + 4, which gives X = 3k + 1.
- Area is 3·9 + 2(D − 3) = 27 + X + Y = 29 + 6k. At k = 6 that's 65, as the
  note says.
- The boundary has 20 vertices, so W = 20, with 8 reflex corners.
- The interior lattice points are exactly the 12 points (iD + u, v) with
  u, v ∈ {1, 2}. The corridors contain no lattice points because 1 < y < 2.

`checks.log` confirms each of these facts for every k from 6 to 40.

## Per-part verdicts

1. **Zero and one horizontal reversal are impossible for equal offsets:
   correct with gaps.**
2. **Upper-pocket path: correct.**
3. **Adjacent one-bounce paths, different-row segments and same-chamber
   visibility: correct.** The adjacent step needs D > 4, so it fails at k = 0.
4. **Distinct-offset construction f(t) = 1 + 3t + t/H: correct.**
5. **Exhaustiveness and scope: correct.** The case list is complete. The scope
   statement is accurate but understated, because the proof works for k ≥ 1.

## 1. Zero and one reversal

**One reversal.** A path with one horizontal reversal consists of two pieces
that are monotone in x. If the path starts leftward, it reverses left of the
source. The only vertical wall there is x = 0. If it ends leftward, it
reverses right of the target, at x = 2D + 3. This step is implicit in the note
("must occur either left of the source or right of the target"), and it holds.

- Horizontal walls lie on integer lines, so every unfolded image of y = 1 is an
  odd integer. The unfolded midpoint ordinate is therefore an integer.
- For a left reversal, the midpoint abscissa is (−u + 2D + u)/2 = D. For a
  right reversal, it's (u + 4D + 6 − 2D − u)/2 = D + 3. Both are mouths of the
  middle chamber.
- Unfolded abscissas in [0, 2D + u] are actual abscissas on the forward pass.
  So the actual path crosses that mouth at an integral height, which isn't in
  the open aperture (1, 2).

*Gap (low).* The note asserts "each lies on the required forward transit" but
doesn't say why. The reason is the preceding sentence: the fold at the
reversal wall is the identity on the forward side.

**Zero reversals.** The midpoint is at abscissa D + u, local abscissa u in the
middle chamber.

- For u = 1, the chamber-unfolded ordinate one unit after entry is an integer
  m. So b = a + 3(m − a) = 3m − 2a. That's correct.
- The aperture condition is "residue mod 3 in (1, 2)". The fold has period 6,
  and (1, 2) ∪ (4, 5) mod 6 is exactly (1, 2) mod 3. That's correct.
- With a = 3t + 1 + ε, b ≡ 1 − 2ε (mod 3). This lies in (0, 1) for ε < 1/2,
  in (2, 3) for ε > 1/2, and equals 0 at ε = 1/2. It's never in (1, 2).
- The map x ↦ 2D + 3 − x together with path reversal sends the offset-2 pair
  to the offset-1 pair. That's correct.

*Gap (low).* The note invokes the integrality of the global unfolding but uses
the ordinate in the chamber unfolding. The two differ by y ↦ ±y + 2c with c an
integer, so integrality carries over. The note should say so in one clause.

The impossibility argument doesn't use D ≡ 1 (mod 3). So for every equal
corridor length X = Y, the equal-offset outer pair needs at least two
horizontal reversals.

## 2. The upper-pocket path

**Correct.** Here L = D − 1/2 and a = u − 1/2.

- **Leg 1.** The path stays in 1 < y < 2. At x = 3 the height is
  1 + (3 − u)/L, and at x = D it's 1 + (D − u)/L < 2. It reaches height 2 at
  x = D + u − 1/2, inside the middle chamber.
- **Leg 2.** The roof is hit at unfolded local abscissa a + L = D + u − 1.
  Since D ≡ 1 (mod 3), this is ≡ u (mod 3) and so not 0. The hit misses both
  roof corners.
- **Side hits.** The side hits are at multiples of 3 strictly between a and
  a + 2L. Neither endpoint is a multiple of 3, so every side hit is strictly
  between heights 2 and 3. None is at the corridor-end corners (D, 2) or
  (D + 3, 2).
- **Leg 3.** Since 2L = 6k + 7 ≡ 1 (mod 6), the path exits at local
  u + 1/2 ∈ (0, 3), moving right. There are 2k + 2 side hits, an even number,
  which is consistent with rightward motion.
- **Leg 4.** The path leaves height 2 at x = D + u + 1/2. At x = D + 3 and at
  x = 2D its heights are strictly between 1 and 2. It arrives at
  D + u + 1/2 + L = 2D + u, height 1.

`checks.log`: for each k, the traced pocket ray has exactly 2k + 3 bounces
(2k + 2 sides and 1 roof). The bounce points equal the predicted ones, there's
no corner hit, and the ray reaches the target. That's 4 pocket pairs (2
offsets × 2 rows) per room.

## 3. Adjacent, different-row and same-chamber cases

**Correct.**

- **Same chamber.** Each chamber is a convex 3 × 3 square.
- **Different rows.** The open segment has 1 < y < 2 throughout, so it crosses
  every chamber wall inside an aperture.
- **Adjacent chambers, same row.** The bounce abscissa (u + v + D)/2 lies in
  (3, D) if and only if D > 6 − u − v and u + v < D. At D = 4 (k = 0) and
  u = v, the bounce lands on the corner (3, 2) for u = 1, or (4, 2) for u = 2.
  Control 2 in the log shows the u = 1 corner. So this step needs k ≥ 1.

`checks.log`: 18 same-chamber, 24 different-row and 16 adjacent pairs per room
all reach their targets. Each adjacent bounce is at the predicted point.

## 4. Distinct offsets

**Correct.**

- H = 2D ± 1 is odd.
- Every seam (x = 3, D, D + 3, 2D) has integral t, with z = 1 + t/H ∈ (1, 2).
- For even t, both folds give z with a positive derivative. For odd t, the
  chamber shift is 3t ≡ 3 (mod 6) and the corridor shift is 3t ≡ 1 (mod 2).
  Both give 3 − z with a negative derivative. So the two prescriptions agree in
  position and velocity, and every mouth is crossed in its interior.
- At t = H, the unfolded ordinate is 2 + 3H ≡ 5 (mod 6), which folds to 1, the
  target.
- Wall hits between seams are at x with integral f(t). None of them is at a
  seam, which `checks.py` asserts. So none is at a corner.

`checks.log`: the traced ray's full bounce sequence equals the sequence
predicted from f. At k = 6 that's 121 bounces for (u, v) = (1, 2), and at
k = 40 it's 733. The optional one-reversal path for (2, 1) also reaches its
target in every room, with its x = 0 and (D − 1/2, 2) bounces as predicted.

## 5. Exhaustiveness and scope

**Correct.** The cases are:

- same chamber;
- different chambers, different rows;
- different chambers, same row, adjacent chambers;
- same row, outer chambers, equal offsets;
- same row, outer chambers, distinct offsets.

The row y = 2 follows by the symmetry y ↦ 3 − y. That covers all 66 unordered
pairs. The log's case counts per room are 18 + 24 + 16 + 4 + 4 = 66.

**Scope.** The note says no step uses W ≤ 20, and that's accurate. The proof
uses the aligned 3 × 3 chambers, unit apertures at 1 < y < 2, equal corridor
lengths, and D ≡ 1 (mod 3). D ≡ 1 (mod 3) is used only in Part 2.

The note states k ≥ 6, which is d152's BBBB range. Every step holds for
k ≥ 1 (D ≥ 7). The only failure at k = 0 is the adjacent step in Part 3.

The statements about R22 and the 8-versus-9 reflex threshold are accurate
disclaimers.

## Errors and fixes

1. **Low (Part 1).** The note doesn't say why the one-reversal midpoint lies
   on the forward pass. *Fix:* "unfolded abscissas in [0, 2D + u] (left case)
   or [u, 2D + 3] (right case) are actual abscissas".
2. **Low (Part 1, zero reversals).** The note doesn't justify moving from the
   global unfolding to the chamber unfolding. *Fix:* "the two unfoldings
   differ by y ↦ ±y + 2c, c ∈ ℤ, so m is an integer".
3. **Low (scope).** "For every k ≥ 6" is understated. *Fix:* "for every
   k ≥ 1; at k = 0 the adjacent equal-offset bounce lands on the corridor-end
   corners (3, 2) and (4, 2)". The proof doesn't settle k = 0 (X = Y = 1).
4. **Observation.** Part 1 holds for every X = Y, but Part 2 needs
   D ≡ 1 (mod 3).
   - If D ≡ 0 (mod 3), the u = 1 pocket ray hits a roof corner.
   - If D ≡ 2 (mod 3), it leaves the pocket moving left.

   So the first extension to equal lengths X = Y ≢ 1 (mod 3) needs a new
   construction. This is a separate issue from the unequal-length extension
   the note names.

## Which lemma does this advance, and what is the first case still open?

**L1.** The note lights the whole d152/d199 three-chamber family X = Y = 3k + 1.
d199 named that family as L1's first open case (k = 6, area 65), and it's now
closed. It no longer gives a candidate W ≤ 20 counterexample.

The first cases still open, all in the same 20-wall pattern with aligned 3 × 3
chambers and unit apertures:

- **X = Y = 1 (D = 4, area 29).** The proof fails only for the adjacent
  equal-offset same-row pairs. These are the first still-open case of this
  note's own family.
- **X = Y = 2 (D = 5, area 31)** and every X = Y ≢ 1 (mod 3). The pocket
  construction fails there.
- **Unequal corridors**, starting with (X, Y) = (1, 2), area 30.

Chamber sizes and aperture positions are also free lengths in the wall-turn
pattern, and this note fixes them. So the pattern's ledger status is PARTIAL,
not COVERED. Before you brief any of these, check whether a reviewed theorem
(d162, d172, d174) already covers them.

**What is the smallest W ≤ 20 room this result doesn't cover?** By area, it's
X = Y = 1 (area 29) in this pattern. That's above L2's area-20 census, so it
isn't covered there either.

## Does this count as a lighting-tail theorem for L1?

**Yes, narrowly.** It's a complete lighting theorem for a one-parameter
infinite family. It shows "large along this ray in length space forces lit".
It's not a pattern-level tail, because it fixes every length except one
corridor parameter (with X = Y and X ≡ 1 mod 3). Record it as a family
lighting theorem that closes d152's three-chamber obstruction. The wall-turn
pattern's ledger status stays PARTIAL.
