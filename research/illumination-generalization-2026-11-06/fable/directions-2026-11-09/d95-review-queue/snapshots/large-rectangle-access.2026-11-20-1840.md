# Repeated crossings inside one large rectangle

**Theorem for review.** Let the rectangle be [0,W]×[0,H], with W/H≥ρ₀>0. Its horizontal sides are reflecting walls. Its vertical sides are reflecting except for d open doors, each of width at most w. Count any artificial cut on a vertical side as a door to avoid. Take two exterior marks with continuous legal access paths into two specified doors on **opposite** vertical sides over one common interval of positive slope magnitudes of width δ. Fix the entry and required exit sheets on this interval. There is an explicit H₀(ρ₀,δ,d,w) such that H≥H₀ lights the pair. Door centers may be arbitrary real heights and may vary with H. The result permits other doors on both vertical sides. The access paths can be through nonrectangular chambers. It requires that each specified path reach its chosen door before meeting any removed mirror.

A single crossing can miss the target height on the available interval when W and H are comparable. The proof instead uses several traversals and certifies that the intermediate side contacts are real reflections. It produces a physical light path; it does not assert that many distinct off-class midpoints are reached.

## Constants

Take a closed access subinterval of width δ (shrink an open chart first). Write

    B = max(64, ceil(32/(ρ₀ δ))),
    k₀ = 4d+8,       P = 2^(k₀) B,       Q = 32P,
    H₀ = 8w P Q^d.

These liberal constants also work in the same-side extension below. Choose one prime in each of the k₀ disjoint intervals (2ⁱB,2ⁱ⁺¹B), 0≤i<k₀, by Bertrand's postulate. They are odd and at most P. Their product exceeds Q^d: it exceeds B^k₀ 2^(k₀(k₀−1)/2), while Q^d=B^d 2^((k₀+5)d). This choice is a proof of existence and does not enumerate optical directions.

Normalize vertical heights by H. Let c₁,…,c_d be the door centers in [0,1]. Simultaneous approximation gives integers 1≤D≤Q^d and Cᵢ such that |cᵢ−Cᵢ/D|≤1/(QD). Indeed two of the Q^d+1 vectors of fractional parts of jc, 0≤j≤Q^d, lie in the same one of Q^d boxes. Choose a prime p from the list not dividing D. This order of choices gives useful clearance even when the original centers have very large denominators or are irrational.

## Matching the last crossing

Reflect coordinates if needed to start on the left. Write ρ=W/H. In the unfolded vertical coordinate let a(s) and b(s) be the signed normalized heights of actual entry and required exit. For magnitude s and the fixed sheets, use the sign of vertical velocity in the forward path at either door. The heights are continuous representatives modulo 2. Their distances to the corresponding signed door centers a,b are ≤w/(2H). For b(s) use the forward velocity obtained by reversing the leg traced from the target. Vertical-side reflections reverse only the horizontal velocity. Thus after q traversals the exact matching equation is

    qρs + a(s) − b(s) = 2k.

For opposite sides take q=p. At the j-th side crossing the developed transverse height, for a matched path, will be

    yⱼ = (1−j/q)a(s) + (j/q)b(s) + 2jk/q.

Write A and B₁ for the signed integer approximants to Da and Db. Choose k so that (b−a+2k)/(qρ) lies in the middle half of the access interval and

    B₁−A+2kD ≠ 0 modulo p.

Consecutive k give nominal slopes spaced by 2/(qρ). Since pρδ≥32, the middle half contains at least two consecutive k, and just one residue class modulo p is forbidden. At the endpoints of the full interval the centered mismatch has opposite signs with magnitude at least qρδ/4. Replacing the centers by the actual access heights perturbs it by at most w/H. The intermediate value theorem therefore gives an interior matching slope with the same k. Both exterior legs are legal there.

## Every intermediate crossing stays on a wall

Replace a(s),b(s) in yⱼ by A/D,B₁/D to get Yⱼ. Its numerator over qD reduces modulo p to j(B₁−A+2kD). For 0<j<p this is nonzero, so

    dist(Yⱼ, (1/D)ℤ) ≥ 1/(qD).

This one grid contains the rational approximants to **both reflected images of every door center**, their translates by 2, and every corner height. At a matching slope |yⱼ−Yⱼ|≤w/(2H)+1/(QD). Including the displacement from a door-center approximant to either physical door edge costs at most another w/(2H)+1/(QD). The total satisfies

    w/H + 2/(QD) < 1/(2pD)

by H≥H₀, D≤Q^d and p≤P. Hence all intermediate vertical contacts miss the closed doors and the rectangle corners. All intervening horizontal contacts are on uninterrupted reflecting walls. The final path can therefore be folded with all required physical contacts and velocities.

## Same-side marks and the middle crossing

For two specified access doors on the same vertical side (possibly the same door), keep the entrance sheet and use the required forward exit sheet for an even number of traversals. Take q=2p and prescribe the parity of k. The middle-half count still supplies two k of that parity, differing by two; p is odd and p∤D. For 0<j<2p other than j=p, the same modular proof works with spacing 1/(2pD). At j=p the path hits the far vertical side and the exact height is (a(s)+b(s))/2+k. There are only two possible center predictions modulo 2, namely (a+b)/2 and (a+b)/2+1.

Thus the same bound lights the pair if **either prediction** lies at normalized circular distance greater than w/H from every reflected far-side door center and every integer corner height (corner clearance greater than w/(2H) already suffices). Choose that parity. If both predictions land in doors, the calculation furnishes no valid middle reflection. This identifies the one crossing at which the prime argument cannot impose clearance; it is not a darkness verdict.

## Scope for the area goal

If each exterior mark lies in a bounded lattice chamber with just its one door into the rectangle, the [effective chamber theorem](effective-chamber.md) supplies the common δ independently of the absolute door heights. For example, with m=4 max(chamber areas) and T=1+F_(3m−1), use δ=1/(2T²) for lattice marks. For real marks the proof there gives an open component of width at least 1/(18H₁²), H₁=1+2F_(3m); use a closed subinterval of width 1/(36H₁²). The local chart is for first hits in each sealed chamber, so no removed mirror is used earlier. The large-rectangle theorem works even when the entrance width stays one lattice unit and W/H stays one. It gives genuinely additional cross-pair coverage in the compact-aspect regime where treating the full central height as the corridor width leaves the single-traversal test short.

The theorem does not force an arbitrary BBBB marked room to supply the two specified access charts. The saved odd crosses have openings on perpendicular sides of their central square; their separate cap construction remains the relevant argument. A mark inside the big rectangle, access through perpendicular mouths, or a horizontal side interrupted by openings changes the congruence: the simple grid-clearance proof above only controls the vertical-side crossing times. Pairs both sitting inside one rectangle already see each other by a chord.

**Next effective question.** For perpendicular access, an unfolded line must terminate on a horizontal image of the target door. Can the intermediate contacts on both sets of walls be certified using the same pair of integers that make the endpoint slope admissible? Success there would address a placement excluded by the present theorem even when the central rectangle and access intervals are already given. There is still no global n₀(r) or full-census CPU estimate. The z=3 notes and the d121 witness replay are outside this calculation.
