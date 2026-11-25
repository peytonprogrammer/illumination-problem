# D230: fresh angles on L1 (2026-11-24)

Advances: L1 — a candidate effective replacement for the missing height estimate H(C) of d187.
Status: derived by the coordinator, not reviewed. No searches were run.

## Where the problem stands

- Folds are closed at r ≤ 8 for every area (d52). The gap is "dark implies fold" on lattice rooms.
- The dark locus is a finite union of rational flats (d89, d132, d134). That result is not effective.
- d187 reduced L1 to one estimate: a height bound H(C) for those flats.
- Every stopped route failed at the same step: aim one ray through two or more gates at a pinned target.
  Nearest winding controls one gate (d229). Nothing controlled the second.

## Angle 1 (new): lattice points in a gate box

Fix a vertical itinerary τ from S to T: slab visits 0..g, with a level event between consecutive visits.
Visit j has width w_j and vertical travel h_j. Event i has an open interval J_i (a gate, or a wall piece for a turn).
A chord of type τ is a choice of side-winding numbers k in Z^(g+1).

Let u_i be the folded abscissa at event i, Y_i = h_0 + ... + h_(i-1), H = Y_(g+1). Then

    u_i(k) = const_i + sum_j 2 w_j k_j (Y_i / H - [j < i]).

So the chords of type τ are the points of a lattice coset v + Λ_τ in R^g that lie in the box J_1 x ... x J_g.
Parity patterns of side reflections change v and coordinate signs only.

**Lemma 1 (dual lattice).** With moduli μ_j = h_j / (2 w_j),

    Λ_τ^* = { n in Z^(g+1) : sum_j n_j μ_j = 0 },   ℓ_i = n_(i-1)/(2 w_(i-1)) - n_i/(2 w_i).

Proof sketch: ℓ·∂Φ/∂k_j = 2 w_j (L - t_j) with L = sum ℓ_i Y_i / H and t_j = sum_{i>j} ℓ_i.
Put n_j = 2 w_j (t_j - L). Abel summation gives L H = sum_j t_j h_j, which is the relation.

**Lemma 2 (flatness criterion).** If no chord of type τ exists, some nonzero n in Λ_τ^* satisfies

    sum_i |J_i| · | n_(i-1)/(2 w_(i-1)) - n_i/(2 w_i) |  ≤  Flt(g),

where Flt(g) is the flatness constant (1 for g = 1, 1 + 2/√3 for g = 2, explicit in general).
This is Khinchine's flatness theorem applied to the box and the coset.

Consequences:
- g = 1 recovers nearest winding: |J| (h_A + h_B) ≤ 2 gcd(w_A h_B, w_B h_A).
- If the visit moduli are rationally independent, type τ always lights the pair.
- Relations are of two kinds. Arithmetic: distinct slabs with commensurable moduli, bounded coefficients.
  Universal: a slab visited twice (n = +1, -1). These encode the midpoint constraint of an excursion,
  which is the R22 "4 < H < 6" gap.
- Hand check on the five-reflex parabola family: for large m, u the monotone itinerary has no short relation,
  so the pair is lit. This matches d229.

Why it could close L1: darkness needs a short relation for every τ. Each relation bounds a modulus ratio
by Flt(g) · 2w / |J|. That is an H(C)-type bound, explicit in the aperture ratios.

Open steps:
1. Review Lemmas 1 and 2 (including turns at horizontal walls and marks strictly inside a slab).
2. Persistence: show that for r ≤ 8 a finite, chart-only family of itineraries cannot all be resonant
   unless the primitive room is small. Universal relations need thin boxes, which cost exposed walls.
3. Aperture lower bounds at chart faces (the ratio-compactness faces of d215).

Tests (named rooms, exact, no search):
- R22: exhibit the short relation for each short itinerary. Expect universal relations with even H.
- Six-reflex locked-gate family (l1-two-gate-boundary.md): the criterion must reproduce the lock and the roof unlock.
- Seven-reflex window family and the 20-wall obstruction family (l1-affine-transfer-obstruction.md).

Stopping rule: stop if the R22 test does not produce short relations, or if step 2 has no proof
for the two-gate family by 2026-11-26 20:00 HST.

## Angle 2: resonance-guided census (needs Daniel's approval)

Lemma 2 says dark rooms are totally resonant: every slab on every S–T itinerary sits in a short modulus relation.
A census restricted to totally resonant rooms reaches areas far above 22 at a fraction of the by-area cost.
A dark pair would refute the goal. With step 2 proved, the same run is the L2 extension.

## Angle 3: oblique twists (first check negative)

Dark pairs are invariant under every affine automorphism, not only the axis twists.
The affine-transfer note left non-axis twists open. `oblique_twist_check.py` tests them on the
20-wall obstruction family (t = 3, 7, 13; directions (1,1), (1,2), (2,1), (1,3), (3,1), (2,3), (3,2)).
Result: both marks lie on singular leaves in all 21 cases, so those twists fix them. The script is unreviewed.
Small-gap rooms have dense corners, so this was expected there. Large-gap rooms are untested. Low priority.

## Already explored, so not fresh

- EMM on the whole dark locus, generic line, periodic points: d89, d115, d116, d119, d122.
- Primitive monodromy implies A_n or S_n: l1-large-monodromy.md. It needs a braid-orbit lemma that is open.
- Compactness in gap ratios: d215.

## Corrections after review (d231, 2026-11-24)

Review: `../d231-review-gate-box/review.md`. Lemma 1 is correct. Read the rest of Angle 1 with these changes.

- Lemma 2 is a necessary condition for darkness. It never certifies lighting on an itinerary with a repeated full-height slab visit, because that visit pair gives a relation of width ≤ 2 < Flt(2).
- "Universal relations need thin boxes" (open step 2) is wrong, and so is "each relation bounds a modulus ratio" for universal relations.
- The parabola hand check is wrong. For even m with m | u−m ≤ 7m the monotone itinerary has a relation of width u/(4m). The pairs are lit (d229), but the criterion is silent.
- Flt(g) is known exactly only for g ≤ 2. Rational independence of the moduli never holds in a lattice room.
- The converse of the box statement needs closed endpoints at smooth wall points on a level. A mark strictly inside a slab gives a partial first or last visit with a different modulus.
- Astra's notes refute two further claims of mine: itinerary-level decoupling (`l1-total-resonance.md`) and "cross relations fail for all but finitely many winding pairs" (`l1-room-decoupling.md`).

What survives: a dark pair forces a short relation on each itinerary whose full-height visits use distinct slabs, a finite family. Turns and excursions need the exact coset test or a one-direction projection test.
