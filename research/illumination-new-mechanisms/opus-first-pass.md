# Proposal: midpoint avoidance for non-vertex targets

Your family places both marks on A points. My strongest candidate keeps one interior A star as the source and moves T to an interior edge midpoint. In that setting, darkness reduces to one exact condition: T must not be the midpoint of any generalized diagonal from S.

I have not run any computation. Each item below is labeled **established**, **derived** (my argument, which you should check), **recalled** (for Codex to verify), or **conjecture**.

## Framing: where a new mechanism can live

- **Derived.** Take a room with walls in the four 45° directions, commensurable offsets, and walls generating a discrete group. The walls lie on mirror lines of that group, so the room is a union of tiles of a scaled 45-45-90 tiling. A finer lattice therefore can't supply a new arithmetic mechanism. Only mark placement and monodromy remain, which matches your item 1.
- **Recalled.** Lelièvre–Monteil–Weiss (Geom. Topol. 2016) prove that each point illuminates all but finitely many points.
- **Recalled, uncertain.** Apisa–Wright, "Marked points on translation surfaces," say roughly the following. In non-arithmetic orbit closures, periodic points are fixed points of the hyperelliptic involution. On torus covers, periodic points are preimages of torsion points.
- **Recalled, uncertain.** Hubert–Schmoll–Troubetzkoy, "Modular fibers and illumination problems" (IMRN 2008), study Veech-group orbits on rational fibers.
- **Conditional consequence.** Any dark pair is either of involution type or arithmetic. In the arithmetic case, T is a rational point.

Your exclusions only cover A–A marks. The mechanisms below use rational marks that aren't vertices.

## Mechanism 1: midpoint-of-diagonal avoidance (strongest)

**(a) Obstruction (derived).** Assume S is an interior A star and k = 0, so every B and C point is an absorbing corner.

1. A ray from S in primitive direction (a, b) first meets a lattice point at (a, b). That point is B or C, never A, so the ray stops there.
2. An irrational direction from S never meets another rational point.
3. On the segment t(a, b) with 0 < t < 1, a point lies in ½ℤ² only at t = ½.
4. The direction class fixes which kind of edge midpoint sits at t = ½:
   - (odd, 0 mod 4): an A–C leg midpoint.
   - (odd, 2 mod 4): a C–B leg midpoint.
   - (odd, odd): a hypotenuse midpoint.
   - The cases with coordinates swapped behave the same way.

So an interior edge midpoint T is lit exactly when the room point under the unfolded midpoint (a/2, b/2) equals T for some (a, b). The midpoint here is a regular point and the endpoint is the blocker. In Tokarsky parity it's the other way around.

The reversed view is also exact. Take T at an A–C leg midpoint and a direction ±v of class (odd, 0 mod 4). The two opposite rays from T reach an A point and a C point at equal distance. T is lit exactly when that A end is S for some such v.

**(b) Escapes.**
- T is not an A star, so I = 1 instead of I ≥ 2.
- No exceptions are needed.
- The involution mechanism is not used.

**(c) Realization.** Build S's 8-tile star and attach pockets. Interior edges away from the star are chords between boundary corners. Walls have length at most 2 tile edges and may pass straight through a boundary A point. A boundary A point is never a first hit from S, so it can be smooth.

**(d) Budget.** Your identity with I = 1 and E = 0 gives W = 8 + Q. Your inequality gives W ≥ 12. Verify that neither assumes the marks are A stars. Euler's formula with one interior vertex gives the number of tiles equal to the number of boundary tile edges.

**(e) Cheap decisive experiment.**
1. Enumerate rooms with I = 1, k = 0, and W ≤ 23.
2. For each interior edge midpoint off the star, trace generalized diagonals for max(|a|, |b|) ≤ 64. That's about 10⁴ directions, each an O(|v|) corridor walk.
3. Any midpoint hit kills that T.
4. Send survivors to the Mechanism 2 certificate.
5. Optionally add tile points with denominators 3 and 4. These allow hits at t = k/q, a few per direction.

**(f) Likely hidden failure.** Aff_S may act transitively on each midpoint class. Then every T dies.

## Mechanism 2: modular-fiber orbit certificate (exact small combinatorial model)

**(a) Obstruction (derived, standard in spirit).**
- The unfolding X is square-tiled. Mark the lifts of all corners, including corners that are regular points of X but still absorb.
- The stabilizer Γ_S of the lift S̃ is finite index in SL₂(ℤ).
- For φ in Aff_S, the ray from S̃ in direction Dφ(v) is φ of the ray in direction v.
- So Reach(S̃) on rational points equals the union over the cusps c of Γ_S of Aff_S · Visit(v_c).
- Each Visit(v_c) is finite, because the ray either hits a marked point or closes.
- With rational marks, irrational directions are irrelevant.
- T is dark exactly when no lift of T lies in that finite union of orbits.

This test is exact in both directions. It turns your negative solver caps into proofs. It works for any k and for a source that isn't a vertex, where rays close inside cylinders.

**(b) Escapes.** It doesn't rely on parity or a single symmetry. The blocking point can sit at any fraction along the ray.

**(c) Realization.** It applies to any room in your family.

**(d) Budget.** It adds no new inequality.

**(e) Experiment.**
1. Check soundness first: the certificate should reproduce darkness on your 24-wall Jordan control.
2. Then run it on your exhaustive W ≤ 23 rooms with marks that aren't A points. Those rooms have never been tested for such marks.
3. Compute the SL₂(ℤ) orbit of (X, labeled points) through the generator action on permutation pairs. Stop at 10⁶.

**(f) Likely failure.** The index of Γ_S may blow up. Your 20k unresolved states suggest this. Corner marking also shrinks Γ_S further.

## Mechanism 3: deck-group involutions in a rectilinear room (unconventional)

**(a) Obstruction.** The LMW midpoint certificate needs one admissible involution per lift orbit. The number of lift orbits equals the order of the holonomy group H.
- Your 45° rooms have H = D₄, so they need 8 involutions.
- A rectilinear room has H = D₂, so it needs 4.

Build all four as ι_h = ρ₋ᵢ ∘ δ_h, where δ_h is in Trans(X). Require:
- ρδ_hρ = δ_h⁻¹, so ι_h is an involution.
- ι_h(S̃) = h·T̃.
- Fix(ι_h) is contained in the corner lifts.

**(b) Escapes.** This fixes your failure "the half-turn maps copies of the same source." The canonical ρ₋ᵢ alone preserves fibers. Composing it with a deck element that isn't central moves the S fiber onto the T fiber.

**(c) Realization.** Choose a polyomino Q that is reflection-tiled by a smaller P, with X_Q → X_P Galois.

**(d) Budget (derived).**
- With r reflex corners, X has genus g = r + 1 and W = 2r + 4 corners.
- Each corner has exactly one lift in X, so there are W corner lifts.
- A hyperelliptic-type ι has 2g + 2 = W fixed points. It must therefore fix every corner lift exactly.
- Other involutions need #Fix ≤ W.

**(e) Experiment.**
1. Enumerate polyominoes with at most 22 boundary edges.
2. Build X with 4n squares.
3. Compute Trans(X) as the centralizer of the monodromy group in S₄ₙ.
4. Discard every room where Trans(X) is trivial.

**(f) Likely failure.** For simply connected Q, Trans(X) may always be trivial. It may also only come from isometries of Q, which commute with ρ and preserve fibers. That would be a provable no-go lemma for Codex to look for.

## Trying to kill Mechanism 1

1. **The star is lit.** Directions (1, 0), (1, 1), and (2, 1) light the midpoints of all 8 star edges and of the star-boundary C–B legs. So T must lie outside the star. This is not fatal.
2. **Orbit pressure.** For φ in Aff_S, m(Dφ·v) = φ(m(v)). Parabolic elements preserve direction classes only modulo 4, so orbits split at least by edge class. Inside a class, I have no argument against transitivity. If transitivity holds, the mechanism is dead in that room.
3. **Small pockets.** I checked a pocket of one tile behind a chord. Rays can bounce in the pocket and leave again, so path length gives no bound. I can't produce a contradiction.
4. **Hidden exceptions.** Every B and C point, including boundary ones, must be a genuine corner for termination at the first lattice point. An interior chord between two boundary corners keeps the polygon simple. Smooth boundary A points are safe because S never hits A first.
5. **Consistency with LMW.** The mechanism predicts finitely many dark points for S, which is compatible.

**Verdict.** I found no theoretical kill. My prior is that most rooms die under the direction sweep, through transitive orbits.

**Conjecture.** Survivors, if any exist, have a pocket behind a width-1 doorway whose midpoint set forms a closed Aff_S orbit.

The first sweep in (e) is cheap. It decides quickly whether this path is worth the cost of the certificate.
