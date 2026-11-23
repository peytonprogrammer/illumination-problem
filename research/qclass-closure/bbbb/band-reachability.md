# A pair that no axial twist brings to a common seam

**Verdict.** Universal band reachability fails in the named 12-wall BBBB room DBas, even though the obstructed pair is lit by reflecting first from the corridor floor and then from the right end wall. The same obstruction occurs at arbitrarily large prime sheet degree.

## The obstruction on the marks

Use the least pointwise rim-fixing horizontal and vertical multitwists H,V on the room double, as in [the two-band test](twist-overlap.md). On a doubled run of circumference C and transverse height h, the shear coefficient λ satisfies λh ∈ Cℤ. Its shift at integral distance j from the rim is ±λj modulo C. Thus if the simultaneous constraints force λ ∈ Cℤ for every cylinder of that orientation, the least twist itself fixes every lattice lift. This includes lifts on the critical graph, which the twist fixes pointwise. If this happens in both orientations, every word fixes each of the four starting lift pairs separately.

[D69's DBas](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d69-bbbb/README.md) has chambers [0,5]×[0,4] and [9,13]×[−1,5], joined by [5,9]×[1,2]. It has area 48, four reflex corners, and canonical type BBBB. Consider S=(1,3) and T=(11,3). Both are interior and odd in each coordinate. Their horizontal chord crosses the exterior.

Here is the calculation with corridor length ℓ, retaining the same chambers and door heights and translating the right chamber. The named room has ℓ=4. These are all doubled maximal runs, specified by (circumference, transverse height).

| Direction | Left chamber | Connecting band | Right chamber |
| --- | --- | --- | --- |
| Horizontal | (10,1), (10,2) | (2(9+ℓ),1) | (8,2), (8,3) |
| Vertical | (8,5) | (2,ℓ) | (12,4) |

The horizontal constraints force λ to be an integer multiple of 10 and 2(9+ℓ). Since 3λ is divisible by 8, so is λ. Vertically λ is a multiple of 3 since 4λ is divisible by 12. Then 8 divides 5λ, so 24 divides λ, and 24 itself works. In DBas the least coefficients are 520 and 24. Both twists therefore fix every lattice lift, in particular both choices at either endpoint.

In horizontal bands the endpoints are at equal height in **disjoint** runs. In vertical bands the profile between them changes twice, at x=5 and x=5+ℓ, with the intervening run of height one. There is neither a single band nor a seam with a constant run on each side all the way to the marks. Hence there are no admissible a,b,w to which the strict width inequality could apply. Widening an opening or improving the gcd estimate cannot repair this failure of the hypothesis.

## The degree and area splits

Area 48 supplies a one-room disproof in the requested 21–48 range. For the actual lighting question this particular pair has the exact certificate below. No residual list of small rooms follows from axial reachability.

At any positive integral ℓ take S=(1,3), and place T at height 3 and offset c from the left wall of the right chamber, with c=2 for even ℓ and c=1 for odd ℓ. The parity and the two changes of run persist. Strict simplicity and the four reflex corners are unchanged. Horizontal edge lengths include 5 and 4, and vertical lengths include 1, so the room is normalized. The degree is n=44+ℓ. By [d69 §1](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d69-bbbb/README.md), every normalized room with r≤8 and n>64 is BBBB; 67 is the first prime in that range. For any prime n≥67 this is a transitive prime-degree sheet action, hence primitive. Every class has a regular lift already in the left chamber, excluding the discrete case, and primitivity excludes a proper intermediate partition. Thus all four canonical relations are universal. By [d99](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d99-review-split/review.md) the sheet group contains A_n. Even here H and V act trivially on the lattice lifts. This conclusion uses the arithmetic of the two fixed chambers, without computing a monodromy group or sampling lengths.

For imprimitive inputs the same cylinder divisibility and geometric tests apply upstairs without alteration. Bounded-orbit descent gives no lifting statement for an adjacent band: the physical runs and the requirement of reaching the seam from each mark must hold upstairs. The calculation does not classify imprimitive rooms. The universal statement is already false in the primitive branch.

## The reflected passage that the bands miss

In DBas start from (1,3) with velocity (7,−2). The successive physical positions are

| Event | Position |
| --- | --- |
| Enter left door | (5,13/7) |
| Reflect from corridor floor | (8,1) |
| Exit right door | (9,9/7) |
| Reflect from right cap | (13,17/7) |
| Reach target | (11,3) |

Both door crossings are strictly inside (1,2). Linear interpolation keeps each open leg inside its rectangle, and both wall hits are smooth. This is one reversal of horizontal travel. The two axial tests fail even for a pair needing only this short itinerary.

The same turn works with a variable number of floor and ceiling hits. Write m=|dy/dx| and b=8−c for the horizontal travel in the right chamber via the cap. Shoot downward from S and, backward from T, downward toward the cap. The doorway heights above the floor are 2−4m and 2−bm. Both belong to (0,1) whenever 1/4<m<2/b for b=6 or 7. The chamber legs then meet no horizontal wall. The corridor must change downward motion to upward motion. On its doubled height circle the signed phases are −(2−4m) at entry and +(2−bm) at exit. Matching them is equivalent to

    (ℓ+4+b)m ∈ 4+2ℤ.

An admissible slope therefore exists whenever (ℓ+4+b)(2/b−1/4)>2. In particular for the odd-length choice b=7 this holds at ℓ>45. This certifies a single horizontal reversal for every obstructed prime-degree example with n>89. At ℓ=4, b=6, m=2/7 gives the displayed two reflections.

**Scope of the follow-on.** If “involves a turn” permits arbitrarily many smooth reflections, avoidance of every such passage is equivalent to actual darkness for distinct interior lattice marks. Indeed, start with any legal segment of unfolded displacement d. Choose an integral primitive nonaxial vector u not parallel to d. A positive power of the parabolic about u lifts to an affine map fixing all marked lattice lifts and corners, by the [finite-index argument](chain-map.md). Its j-th power sends d to d+jαu with α nonzero, preserving legality and the endpoints. The absolute horizontal and vertical displacements both grow without bound. On folding, these are the total absolute travels in the two coordinates. Once each exceeds the corresponding room span, the trajectory must reverse each coordinate at least once. This gives turning paths from any first witness. It supplies no first witness for an unknown pair.

The remaining useful question is narrower: can one force an itinerary with a specified cap reversal and compatible open doorway phases from the room geometry alone? The displayed interval proves this for the obstructed dumbbell placements above. A general BBBB room can lack a separating corridor, so neither this cap construction nor the axial band criterion proves illumination in all rooms with at most 20 walls.
