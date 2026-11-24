# d224 referee review: seam parity and the band multi-twist

Note: `note-snapshot.md`. Checks: `checks.py`, log in `checks.log`. The run takes under 0.1 s of CPU at nice 10 and ends with 0 failures. It uses two hand-made axial rooms: the d223 room P (area 22, 8 reflexes) and one new room R2 (area 22, 4 reflexes). Every billiard trace is exact rational arithmetic along a direction chosen by hand or its sheared image. There's no room enumeration, no ray, direction, word, or room-size search, and no network call. The only loops run over the 6 off-axis interior lattice marks of each named room and over one period of λ.

## Summary

| # | Claim | Verdict |
|---|---|---|
| 1 | Seam-contact parity records the target side; the character of f is mod-2 intersection with β | CORRECT |
| 2 | Attainable set ∪{ε} ∪ (ε+⟨η⟩); exact obstruction; odd open-cylinder case | CORRECT WITH GAPS (minor) |
| 3 | Band multi-twist, translation by Wₜ, divisibility test | CORRECT WITH GAPS (wording, scope, a practical limitation) |
| 4 | Seam-end partner construction and non-composability | CORRECT |
| 5 | Half-turn quotient: two branch values; cut-arc rule | CORRECT WITH GAPS (minor) |
| 6 | First open case | CORRECT WITH GAPS |

Overclaim: none found. The note states that the twist test is only sufficient and that no case is closed in general.

**Main finding.** The twist is a genuine affine automorphism of Q, and it flips the seam parity on exact traces. On lattice marks, though, it needs a seam-crossing band of height at least 2 with the target on an interior level. In the d223 room, the only available 8-reflex example, every band has height 1. All lattice marks lie on band boundaries there, so the test is vacuous for every pair.

## Hand-made rooms

- **P (d223).** H = {(0,0)–(0,4), (1,0)–(1,3), (2,1), (2,3)}, and P is H plus its mirror about x=0. P has 8 reflexes and 20 walls. Its bands are the five rows, with widths 4, 6, 4, 6, 2, so L = 24.
- **R2 (new).** H = rows 0–1 at x∈{0,1,2}, row 2 at x=0, and rows 3–4 at x∈{0,1}. P = H plus its mirror, with area 22, 4 reflexes, 12 walls, and no pinch. The seam ends (0,0) and (0,5) are smooth in P and convex in H. Its bands are [0,2]×[−3,3], [2,3]×[−1,1], and [3,5]×[−2,2], so L = 12. All six off-axis interior lattice marks lie strictly inside a band. R2 has no same-parity, distinct-orbit off-axis pair, so it tests the mechanism, not the open case.

## 1. Seam parity and the character: CORRECT

- Over the front sheet of N lie front H and rear σH of Q. Crossing a non-seam wall of H in N keeps the physical half, and crossing β switches it. So the sheet of f toggles exactly at β, and the character of a closed curve off b₁, b₂ is its mod-2 intersection with β. On the sphere N, a simple closed curve meets the arc β an odd number of times exactly when it separates the ends.
- Exact traces in both rooms: the H seam-contact count equals the P axis-crossing count. Even counts reach T and odd counts reach σT (P: 1 contact, σT; R2: 1 contact, σT).
- The sufficiency-only statement ("necessity would need an additional argument") is correct. A legal P-path through a smooth seam end has no ordinary H-projection.

## 2. Attainable parity set: CORRECT WITH GAPS (minor)

- **Exactness.** By the d221 criterion, every legal chord lies on one regular circle or one open saddle connection in one orbit state. On an interval the subarc between two chosen lifts is unique. On a circle, the forward arcs differ by whole turns and the backward arc is the forward arc minus one turn. Both change ε by a multiple of η, so the set is ε+⟨η⟩. The union over states, components, and lift choices is exactly the attainable set.
- **Obstruction.** "Only one parity" is equivalent to "all common circles have η=0 and all contributing ε agree." That's the stated condition.
- **Odd open cylinder.** In the developed strip, chords from s to t and to t+C stay in the open strip and avoid the boundary. Their difference is one core loop, so their bits differ when the core character is odd. Correct.
- **Consequence the note doesn't state.** Every horizontal cylinder of H that touches the seam has a core crossing β exactly once, so its character is odd. In both rooms every horizontal cylinder of H touches the seam (checked). So two marks strictly inside one common seam-adjacent horizontal cylinder already have both parities.

Gaps:

- The result inherits d221's gaps, mainly the definition of "compatible lifts."
- The note asserts that the orbit stays finite after adding the two-sheet seam cover. That's true, because the extra data is a finite cover of a finite marked orbit, but the note gives no reason.
- The sentence "The continuation retains the terminal velocity as well as the terminal point" has no visible role in the criterion. Delete it or say what it's for.

## 3. Band multi-twist: CORRECT WITH GAPS

Verified points:

- **Affine gluing.** In every oriented chart the derivative is [[1,λ],[0,1]], because chart changes are ±I and −I commutes with it. With 2W | λh, each band map is the identity on both boundary circles. `checks.py` confirms this on every band of both rooms.
- **Corners and seam ends.** Every corner of an orthogonal room ends a horizontal wall, and the seam ends lie on horizontal walls. All 22 (P) and 14 (R2) corners and seam ends lie on band boundaries, so the twist fixes them. An affine homeomorphism that fixes the cone points and the seam ends maps a legal path that misses them to another one. The exact traces confirm legality in P and in H.
- **ξ-coordinates and σ.** With ξ = x−a on the front and ξ = W+(b−x) on the rear, translation by W sends (x, front) to (a+b−x, rear) and (x, rear) to (a+b−x, front). That's a lift of σT exactly when the interval is centered on the axis. Every seam-crossing interval of a symmetric room is centered. The log also shows that on a non-centered interval the same translation gives a+b−x, not σx.
- **The shift is W, the physical width, which is half the circumference 2W.** The note calls Wₜ the "full upstairs width." That's wrong wording: the full upstairs circumference is 2Wₜ. The formula uses the correct quantity.
- **Fixing S.** The twist moves the front lift of S by +λdₛ and the rear lift by −λdₛ physically. So 2Wₛ | λdₛ fixes one lift exactly when it fixes the other, and "both lifts" costs nothing extra. It's also more than needed. Only the starting lift must land on a lift of S, which also allows λdₛ ≡ ±2(bₛ−xₛ) mod 2Wₛ. Alternatively, S can swap to σS while T stays fixed. The note's "precisely when" is correct only for the scoped family (both lifts of S fixed, T swapped).
- **Divisibility test.** In all 48 ordered off-axis, distinct-orbit pairs of the two rooms, gcd(Lₛdₜ, 2Wₜ) | Wₜ agrees with brute force over one λ period (0 mismatches). In R2 the generalized condition passes 16 pairs, against 8 for the note's test. The other 8 are exactly the reversed-role pairs that the note's "second test" covers, so the extra freedom added nothing in R2.
- **Exact sheared rays.**

| Room | S → target | λ | Original | Image |
|---|---|---|---|---|
| R2 | (1,1) → (1,4) | 12 | vel (−2,3), reaches σT, 1 seam contact | vel (34,3), reaches T, 10 contacts, legal in P and H |
| R2 | same | −12 | same | vel (−38,3), reaches T, 12 contacts, legal |
| P | (1,1) → (1/2,5/4) | 24 | vel (−2,1), reaches T, 0 contacts | vel (22,1), reaches σT, 1 contact, legal |
| P | (1,1) → (1/2,25/16) | 96 | vel (8,1), 1 reflection, reaches T, 0 contacts | vel (104,1), reaches σT, 9 contacts, legal |
| P | (1,1) → (1,3) (control) | 24 | vel (−1,1), reaches σT, 1 contact | vel (23,1), still reaches σT (T on a boundary, fixed) |

For each sheared ray, the image endpoint and 9 sampled interior points equal φ(original) exactly in Q, with sheets. The R2 samples cross all three bands. The P targets are rational because P has no lattice mark strictly inside a band.

Gaps:

- **Band choice.** "Split at the horizontal wall levels" can mean a global split at every wall level. With that reading, h is smaller, L is larger, and more marks fall on boundaries. Maximal horizontal cylinders are enough and give the weakest condition. In both test rooms the two readings agree.
- **Practical scope for lattice marks.** A lattice target needs a seam-crossing band of height at least 2 with dₜ strictly between 0 and h. In P, the only 8-reflex example available, every band has height 1, so no lattice pair passes. The note's sentence "A mark on a band boundary ... can defeat this construction" is correct, but it understates how often this happens.
- **"Wₜ is the full upstairs width"** should read "Wₜ is the physical width, half the circumference."

## 4. Seam-end partner construction: CORRECT

- For a vertical axis the wall at E is horizontal. Its reflection is diag(1,−1) = −Dσ, which is the velocity of the reversed σ-prefix.
- Exact trace in R2: T=(1,1) with velocity (−1,4) reflects at E=(0,5) and reaches σT=(−1,1).
- Extension of a known ray: from S=(2,1) with velocity (−1,4), the path reflects at (7/4,2) and (5/4,0), passes T=(1,1), reflects at E, and reaches σT. One straight itinerary lights T and σT. The same itinerary stops at the convex seam end in H, as the note says.
- The non-composability caveat is right. Joining an S→T ray to a T→σT ray needs equal germs at T in one lift, and even then the joined path visits E.

## 5. Half-turn quotient: CORRECT WITH GAPS (minor)

- The lifted half-turn on Q preserves each copy and fixes only the front and rear lifts of O, so f has exactly two branch values. Riemann–Hurwitz gives 2 = 2·2 − 2. O is interior and a lattice point (d223 §5, §6).
- Each branch value is a cone point of angle π in N, so it's a pole. "Two of the eight poles" uses the area-22, r=8 count Σpₓ = 8 from d223. The other six poles are unbranched, with σ-paired convex corners above them. That's correct at area 22, but the sentence should cite the count.
- **Cut-arc rule.** A double cover of a sphere branched at two points has character equal to mod-2 intersection with any arc joining them. The arc must avoid u and v. The rule and the odd-core cylinder case are correct.
- "Separate quotient mirror lifts must be tested with their physical target labels" is too vague to check. Spell it out or delete it.
- Statements about the census are correct: P/σ is a cone disk, not a planar room.

## 6. First open case: CORRECT WITH GAPS

The statement matches what the note proves. Add these points:

- The test is vacuous in the d223 room, so the first open case should name this subcase: every seam-crossing band containing a mark has height 1.
- Two marks strictly inside one common seam-adjacent horizontal cylinder of H are already closed (§2).
- The test can be widened before you call a pair open. Use maximal cylinders and the reversed roles. Also allow S to land on its other lift or on σS.
- The mixed case with one mark on the axis is still unlisted. It's the d223 gap.

## Lemma advanced and first open case

**Lemma advanced: L1, as a sufficient condition.** The horizontal multi-twist is a correct parity-flipping tool. It closes the axial branch for any pair that passes the divisibility test, at any area where one ordinary H-witness is known. No general case closes, and no bound on W moves.

**First open case.** Take the axial area-22 branch with distinct off-axis same-parity marks in different orbits. One ordinary parity is known. Every seam-crossing band containing either mark has height 1, so both marks lie on band boundaries. No common odd cylinder is known. The d223 room is a concrete instance of the band condition: its pair (1,1), (1,3) is closed only by the two hand traces in d223, not by the note. The half-turn branch has no census reduction and stays open.
