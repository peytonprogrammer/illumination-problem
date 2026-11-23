# D135: review of the mixed 45° extension in parametric-orbits.md

Date: 2026-11-21. Reviewer: adversarial referee.

Reviewed file: `d95-review-queue/snapshots/parametric-orbits.2026-11-21-2230.md`, SHA-256 prefix `6cc2d3b76e0925e1`. Scope: only the new section "Mixed axial and 45° walls" and the new closing sentence about the numerical bound. I diffed against the 22:00 snapshot. The other changes are citation edits. The axial argument was reviewed in [d132](../d132-review-paramorb/review.md) and isn't redone here. Marked-point algebraicity is assumed, as instructed. I checked that `marked-algebraicity.md` states its reduction for an arbitrary stratum, so it covers the higher-order zeros that appear here.

Own code: [checks.py](checks.py), log [checks.log](checks.log), 0.03 CPU-seconds. Exact integer and rational arithmetic. Named rooms only. No network use.

## Verdict

**Sound with gaps.** No gap is high. The mixed extension is mathematically correct. The doubled room carries a quartic differential, not a quadratic one. Its cyclic fourth-root cover is the 8-copy Katok–Zemlyakov unfolding. The note's ramification indices, zero orders, behaviour at infinity and integrability exponent are all correct. I confirmed them on four named mixed rooms against an independent combinatorial gluing. The cell construction and local linearity carry over, with denominators of 2. The o-minimal step and the Presburger step carry over unchanged. The gaps are an inherited sketch of the classifying map and several unstated identifications and conventions. The conclusion stays conditional on the assumed marked-algebraicity input.

## 1. Unfolding: translation surface, root cover, cone data

**What the double is.** On a wall with direction angle θ = kπ/4, reflection sends dw to e^{2iθ} conj(dw). Then dw⁴ is invariant exactly when 8θ ∈ 2πℤ. So the doubled sphere has a well-defined quartic differential q = c⁴∏(z − aᵢ)^(aᵢ−4) dz⁴. It isn't a half-translation surface: dw² is not invariant across slope ±1 walls (check 1b: (1+i)⁴ = −4). A root cover is needed, and the note supplies one.

**Fourth root versus 8 copies.** These agree. The double is 2 copies of the room, and the canonical cover v⁴ = P has degree 4 over it, giving 8 copies. For a mixed room the walls generate the full dihedral group of order 8, because an axial reflection composed with a diagonal reflection is a quarter turn. The canonical cover is connected exactly when P isn't a square in ℂ(z) (Kummer theory), that is, when some aᵢ is odd. In a mixed room some aᵢ is always odd: if every angle were a multiple of π/2, every edge would lie in one of the two direction classes, axial or diagonal. So the note's "if the root equation splits" clause never applies to mixed rooms. It applies only to the axial case, where v⁴ = P splits into v² = ±√P (two 4-copy components).

**Exponents and orders.** Every formula checks:

- SC exponents (aᵢ − 4)/4 sum to −2, since Σaᵢ = 4(n − 2).
- The worst endpoint exponent is −3/4, at a 45° convex corner (a = 1). It is integrable.
- With mᵢ = aᵢ − 4, the ramification index is e = 4/gcd(4, mᵢ) = 4/gcd(4, aᵢ). The order of ω is e·aᵢ/4 − 1 ≥ 0. The cone angle is 2π·aᵢ/gcd(4, aᵢ). The corner has gcd(4, aᵢ) lifts.
- At infinity, deg P = −8 ≡ 0 (mod 4). The cover is unramified there, and ω is regular and nonzero.

**Exact replay (checks 1 and 4).** For each room I built the 8-copy gluing independently: copy g is glued along edge e to copy g·R_e. I computed vertex cycles, cone angles and V − E + F, then compared with the root-cover formulas and with Riemann–Hurwitz for v⁴ = P.

| Room | Vertices | aᵢ | Zeros | Genus | RH = gluing |
| --- | --- | --- | --- | --- | --- |
| A, square with one convex chamfer | (0,0),(2,0),(2,1),(1,2),(0,2) | 2,2,3,3,2 | two of order 2 | 3 | 4 = 4 |
| B, V-notch | (0,0),(4,0),(4,4),(2,2),(0,4) | 2,2,1,6,1 | two of order 2 (at the 270° corner) | 3 | 4 = 4 |
| C, L with chamfered reflex corner | (0,0),(4,0),(4,2),(3,2),(2,3),(2,4),(0,4) | 2,2,2,5,5,2,2 | two of order 4 | 5 | 8 = 8 |
| D, 45° notch | (0,0),(4,0),(4,4),(3,4),(2,3),(2,4),(0,4) | 2,2,2,3,7,2,2 | orders 2 and 6 | 5 | 8 = 8 |

All four rooms are strictly simple and generate a group of order 8. Every corner matches between the gluing and the root cover. For room A, Riemann–Hurwitz gives 2g − 2 = 4·(−2) + 2·3 + 3·2 = 4, so g = 3. The axial L-room control generates a group of order 4. Its 4-copy gluing has one point per corner, half of what the connected 8-copy cover would predict. This is the split case.

**A fact the note doesn't state.** The axial dichotomy "convex ⇒ regular lift, reflex ⇒ zero" fails here. A 135° convex corner lifts to one zero of order 2 with cone angle 6π (rooms A and D). A 45° convex corner lifts to one regular point. A 90° corner lifts to two regular points. The stratum is H(2^(n₃+2n₆), 4^(n₅), 6^(n₇)) with n₁ + 2n₂ forbidden regular corner marks plus the endpoint marks. Here n_a is the number of corners with angle aπ/4. The project forbids contact with every convex corner. For 135° corners that is forced anyway, since the corner is a cone point. The note's text, "corners whose lifts are regular and must be labelled forbidden", is correct but incomplete (gap 3).

**Lit pair (check 4).** Room B has S = (7/2, 3) and T = (1/2, 3). The direct segment crosses the notch at (2, 3), which lies outside the room. The exact tracer finds S → (2, 0) → T with one bounce, so the pair is lit. The horizontal launch from S hits the diagonal wall at (3, 3) and enters a period-4 orbit that never meets T. The cap was 200 steps, and the orbit repeated at step 5.

## 2. Cells and linearity

- Offsets x, y, y − x and y + x are integral forms. Intersections of nonparallel lines have determinant ±1, except slope 1 with slope −1, which has determinant 2 (check 2). Intersection points are rational linear in the offsets with denominator dividing 2. Comparisons along lines are therefore rational linear sign conditions, and cells are convex rational polyhedral.
- The order type along every line, including equalities, fixes the arrangement's face lattice. Concurrences show up as equalities along a line, and coincident lines show up as equal parallel offsets. Walls lie on arrangement lines, so each face is inside or outside the room. Mark interiority is fixed by the order of edge crossings on the mark's horizontal line. Strict simplicity is fixed by the order of endpoints and crossings along each edge line. Incidences are constant on cells.
- Face vertices and barycenters are rational linear on a cell, because the number of distinct vertices is fixed. Edge holonomies in copy g are g applied to rational linear vectors, where g is a signed permutation matrix. Relative periods are linear on the cell, with coefficients in ½ℤ.
- Check 2 replays the order type on a named family. Room A scaled by k = 1, 2, 3, 5, with marks scaled too, has a constant order type of 21 lines. Changing the chamfer t = 1…4 at side 6 changes the order type at every step. Cells are fine-grained, but finiteness and the qualitative claim don't depend on their size.

One omission: the note doesn't define the "input coordinates" for mixed rooms (gap 4). The natural choice is the vertex and mark coordinates on the type subspace. That subspace is cut out by integral equations: an axial edge fixes x or y, and a diagonal edge satisfies Δy = ±Δx with a fixed sign. Its lattice points are exactly the lattice rooms. Diagonal walls join lattice points automatically once the vertices are integral.

## 3. O-minimal finiteness and Presburger

- **Definability.** The integrands (z − aᵢ)^(mᵢ/4) on the closed upper half-plane have semialgebraic branches: take the principal fourth root and raise it to the power mᵢ. The exponents are at least −3/4, so Cluckers–Miller Theorem 1.3 applies exactly as in d132. The quartic-differential reflection and the cover family are algebraic over the distinct-prevertex space. The classifying-map paragraph is more explicit than the axial one: it gives the local ramification charts, the finite étale root choices and the sections over z and z̄. It is still a sketch (gap 1).
- **§3 finiteness.** The extension lemma and the countable-definable-set argument use only that D is relatively closed, definable and locally a finite union of flats on a convex cell. Both properties hold here, so the step carries over verbatim.
- **Presburger.** Cells are rational with denominator 2, and flats meet ℤᵏ in cosets of finitely generated subgroups. Integral darkness on each cell is Presburger. Congruence tests, such as the canonical45 even-even A marks, remain Presburger. The 45° lattice condition adds only integral linear equalities, so nothing changes.
- **Correctly disclaimed.** No height bound, no orthant gap coordinates and no primitive normalization for mixed rooms. The note also doesn't claim the independent-axis product.

## 4. Numerical sentence

"d = 22, H = 1 gives about 3.2 × 10³⁵" checks: Δ = 22¹¹ ≈ 5.84 × 10¹⁴, and 4d⁴Δ² ≈ 3.199 × 10³⁵ (check 5). This closes d132 gap 6.

## Gaps

1. **Medium (inherited from d132 gap 2): the classifying map is still a sketch.** The proof needs simultaneous normalization of the cyclic 4-cover family over the distinct-prevertex space. It also needs smoothness from the constant ramification type, sections over a finite étale cover, and a morphism into the marked stratum's algebraic structure. The mixed paragraph states these, but it doesn't prove them or cite a reference for families of cyclic covers. To fix both cases at once, cite the standard smooth family of cyclic covers of ℙ¹ with fixed local monodromy, for example the Deligne–Mostow or Bouw–Möller setups.
2. **Low: the two unfolding models are identified only by assertion.** §1-style linearity uses the 8-copy reflection gluing, and definability uses the root cover. D must be the same set in both. Add one sentence: on each sheet over the upper half-plane, the developing map of c·v·dz is the SC map times a fourth root of unity. Sheets over the lower half-plane are reflected copies, so the sheets are indexed by the order-8 group with gluing g ↦ g·R_e. Checks 1 and 4 confirm the combinatorics on rooms A–D.
3. **Low: corner types and the stratum aren't stated.** 135° convex corners are genuine zeros of order 2, not regular marks, and 45° corners lift to a single regular point. State the stratum H(2^(n₃+2n₆), 4^(n₅), 6^(n₇)) with n₁ + 2n₂ forbidden regular marks. Also repeat the convex-contact convention here, since "physical darkness" depends on it.
4. **Low: mixed input coordinates and lifts aren't specified.** Define the type subspace with its integral equations Δy = ±Δx. Also clarify "the marks lift over their two half-plane arguments": each mark has 8 lifts, 4 over z and 4 over z̄, which gives 64 lift pairs.
5. **Low: the splitting hedge is vacuous for mixed rooms.** Some aᵢ is always odd, so v⁴ = P is irreducible and the cover is connected. State this instead of "choose a connected component".
6. **Low: the theorem statement doesn't mention the extension.** The headline theorem still says "cyclic orthogonal polygon type", and "Review priorities" doesn't mention the mixed section. Add a corollary statement for kπ/4 rooms with its own scope line: no product structure, no height bound and no effective data.

## Re-run

```
cd d135-review-mixed45 && python3 -B checks.py > checks.log
```
