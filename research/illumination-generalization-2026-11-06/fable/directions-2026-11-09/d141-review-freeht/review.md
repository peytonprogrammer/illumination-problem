# D141: review of free-half-turns.md (snapshot 2026-11-22 00:45)

Date: 2026-11-21. Reviewer: adversarial referee.

Reviewed file: `d95-review-queue/snapshots/free-half-turns.2026-11-22-0045.md`. Context read: the d135 and d139 reviews and the `half-turn-fibers` snapshot (20:20), which is under separate review.

Code: [checks.py](checks.py), log [checks.log](checks.log), about 4.5 CPU-seconds. Exact integer and Fraction arithmetic on 8 named rooms. It runs no room search and no ray search. It makes no network calls.

## Verdict

**Sound with gaps.** No gap is high. The classification theorem and the count are correct, and I found no counterexample on 6 named mixed rooms. One of those rooms (B) has hidden translation automorphisms and hidden −I automorphisms, so the test isn't vacuous. The theorem survives because every hidden −I involution has non-forbidden fixed points. The gaps concern scope: the result is about involutions on the full unfolding X only. Intermediate translation covers carry half-turns, with all fixed points forbidden, that come from hidden symmetries and from quarter turns.

## Method

For each room I built the unfolding X combinatorially on quarter-square triangles. A tile is (T, g), with T a physical triangle and g a sheet. The sheet is kept across interior edges and becomes g·s_w across a wall w.

An affine automorphism with derivative A is a tile permutation (T, g) ↦ (f(T), g*). Here f is affine with linear part g*⁻¹Ag, and the map commutes with every gluing. I seeded one base tile at each of the |X| possible images and propagated. This finds every automorphism that preserves the tiling. Once X has a cone point, every automorphism does: cone points sit at lattice points and the derivative lies in D4. All mixed rooms here have genus at least 3.

An automorphism is *physical* if its affine part f is one map for every tile and sheet. Otherwise it's *hidden*. I computed fixed points exactly over all tile vertices and edge midpoints, using the point model (p, g·Stab(p)). A −I map that preserves the tiling can't fix a triangle interior, so this candidate set is complete.

## Rooms used

| Room | Vertices | Angles (π/4) | Genus of X | Symmetries |
|---|---|---|---:|---|
| H, d138 hexagon | (0,0),(2,0),(3,1),(2,2),(0,2),(−1,1) | 3,3,2,3,3,2 | 5 | y=1, x=1, centre |
| D, two opposite chamfers | (1,0),(3,0),(3,2),(2,3),(0,3),(0,1) | 3,2,3,3,2,3 | 5 | x+y=3, y=x, centre |
| A, one chamfer (d135) | (0,0),(2,0),(2,1),(1,2),(0,2) | 2,2,3,3,2 | 3 | y=x |
| B, V-notch (d135) | (0,0),(4,0),(4,4),(2,2),(0,4) | 2,2,1,6,1 | 3 | x=2 |
| O, four chamfers | (1,0),(2,0),(3,1),(3,2),(2,3),(1,3),(0,2),(0,1) | 3 ×8 | 9 | full D4 |
| M, asymmetric (d139) | (0,0),(3,0),(4,1),(4,2),(2,4),(0,4) | 2,3,3,3,3,2 | 5 | none |
| L, orthogonal (control) | (0,0),(2,0),(2,1),(1,1),(1,2),(0,2) | 2,2,2,6,2,2 | 2 (4-copy) | y=x |
| Cross, 12 walls (control) | plus shape on [0,3]² | 2,2,6 ×4 | 5 (4-copy) | full D4 |

All rooms are strictly simple. The six mixed rooms have wall group D4 and a connected 8-copy unfolding. In every mixed room, each corner has gcd(4, a) lifts.

## 1. Claim (a): free −I involutions are lifts of two-vertex reflections

**Both directions hold on every mixed room** (`checks.log` §1).

| Room | −I autos | Hidden | Free −I involutions | Predicted by the note |
|---|---:|---:|---|---|
| H | 4 | 0 | lift of y=1 | y=1 (tips (−1,1), (3,1)) |
| D | 4 | 0 | lift of x+y=3 | x+y=3 (vertices (3,0), (0,3)) |
| A | 2 | 0 | none | y=x hits edge midpoint (3/2,3/2) |
| B | 6 | **4** | none | x=2 hits edge point (2,0) |
| O | 8 | 0 | none | every axis hits edge midpoints |
| M | 1 | 0 | none | no symmetry |

- For the physical lifts, the formula (p, g) ↦ (σp, −gL⁻¹) gives exactly the automorphisms found. The predicted count matches in every room.
- Lifts of reflections whose axis meets an open edge have fixed points over that edge point (A, B, D, H, O), as the note says. Central-symmetry lifts have 8 fixed points over the centre.

**Hidden symmetries exist and don't break the theorem.** In room B, Trans(X) has order 6 with element orders 1, 2, 2, 2, 3, 3, so it's S3. Only 2 elements are physical. The hidden ones come from B's tiling by three right isosceles triangles, folded across y=x and x+y=4. A hidden translation sends S = (53/40, 27/40) to (27/40, 53/40) or to (133/40, 107/40), depending on the sheet. The 4 hidden −I maps split as follows:

- 2 involutions with 4 non-forbidden fixed points each, over the open-edge points (4,2) and (0,2).
- 2 maps of order 6 whose 2 fixed points each are forbidden corner lifts.

Neither kind is a free involution, so the classification holds. This is the case the question anticipated: square-tiled surfaces with extra Veech symmetry. The descent proof handles it correctly without mentioning it.

**The descent proof checks.** I followed each step:

- τ is central among ±I automorphisms, by the common-fixed-point argument at a true zero. I confirmed that τ commutes with all of Trans(X) in all 6 mixed rooms, including B.
- δ = τη is a free translation involution.
- b is free on Y.
- Y is not a sphere, and the hyperelliptic or elliptic step makes η commute with R.
- η then also commutes with the deck reflections, because it commutes with circle reflection downstairs. So it descends to an isometry σ with σ² = 1.

The Riemann–Hurwitz side check holds. H and D have genus(Y) = 1, which is odd. A, B and the controls have genus(Y) = 0 and no free involution. O has genus(Y) = 3 and no free involution.

**Orthogonal controls (outside the hypotheses).** On the natural 4-copy unfolding, L and the cross have no hidden ±I automorphisms. L has only τ, whose 6 fixed points are its Weierstrass points. Their diagonal-axis reflections meet the boundary at two vertices, (0,0),(1,1) and (1,1),(2,2). Their −I lifts don't exist on the 4-copy surface. On the 8-copy surface the lifts are free automorphisms that swap the two components, so they're vacuous for the midpoint argument (§2 of the log). The mixed hypothesis is therefore needed for the converse direction, and the note states it.

## 2. "Fixed-point-free" versus "all fixed points forbidden"

The theorem uses the literal definition: no fixed points at all. The consequence section uses "all fixed points forbidden" and bridges the two by proving that such an involution with a nonempty fixed set equals τ. The bridge is correct for involutions. In every room, τ's fixed set is exactly the set of corner lifts: 8 in each mixed room, 6 for L, 12 for the cross. The regular corner lifts (a = 1, 2) are genuine points of X and are included.

For **non-involutions** the two definitions come apart. O has fixed-point-free −I automorphisms of order 4, the quarter-turn lifts. B has hidden −I maps of order 6 whose fixed points are all forbidden. So the involution hypothesis is load-bearing, and the title "Free half-turns" is looser than the theorem (gap 2).

The midpoint argument on X needs only a −I map φ that swaps the two lifts, so I checked whether a non-involution could do it. It can't. If φ(a) = b and φ(b) = a, then φ² is a translation fixing the regular point a, so φ² = id. The note doesn't say this, but it closes that loophole.

## 3. Claim (b): one lift, at most one of 8

- **Uniqueness of the lift.** At an interior point the target sheet is forced by g′L = −g, so the −I lift of σ is unique. The bisector is the only reflection sending S to T.
- **Count, replayed on H.** S = (1, 1/2) and T = (1, 3/2). The −I involutions with all fixed points forbidden are τ and the lift η of y=1. For each of the 8 source sheets, exactly 1 target lift of T is blocked. From sheet I it is sheet diag(−1,1) (§3).
- The central-symmetry lift also sends (S, I) to a lift of T, namely (T, I). It has non-forbidden fixed points over (1,1), so it blocks nothing.

## 4. Claim (c): the hexagon chord

The replay matches the note exactly (§4):

- S and T are interior. The closed chord meets no edge and no corner.
- σ(S) = T, and η(S, g) = (T, −gL⁻¹) ≠ (T, g) for all 8 sheets.
- The chord's midpoint (1,1) on sheet I is sent to sheet diag(−1,1), so it isn't fixed.
- The doubled marks (2,1) and (2,3) in 2H share parity, and 2H has content 2.

The marks are edge midpoints of the unit grid, not d11 lattice or square-centre marks. The square centres (1/2,1/2) and (1/2,3/2) are mirrored by y=1 and joined by an interior vertical chord. They give the same demonstration in H itself, with no doubling (gap 4).

## 5. Scope: intermediate covers and "darkness is symmetry"

The midpoint argument also works on a quotient X/Γ, where Γ is a subgroup of Trans(X). Take a −I map ψ that normalizes Γ, with ψ² ∈ Γ. If every element of the coset Γψ has only forbidden fixed points, then [ψ] is a half-turn of X/Γ whose fixed points are all forbidden. It blocks every path from x to every point of Γψ(x).

I enumerated every such pair (Γ, ψ) in the 6 mixed rooms (§5). These are subgroups of a known group of order at most 8, not a search over rooms.

| Room | Mechanisms beyond X | Targets blocked from (S, I) | Physical symmetry? |
|---|---|---|---|
| H, D | Γ of order 2 (the free lift's translation partner) | the mirror image of S, 1 lift | yes, the same reflection |
| O | Γ = ⟨central-symmetry translation⟩, ψ = quarter-turn lift | R(S) and R³(S), 1 lift each | yes, but a **rotation** |
| B | Γ = C3 (hidden), ψ = τ | (27/40, 53/40) and (133/40, 107/40), 1 lift each | **no** |
| A, M | none beyond τ | none | — |

These results cut both ways:

- **What it settles.** On the full unfolding X of a mixed room, the direct midpoint mechanism is always a physical reflection through two vertices. It never blocks more than 1 of 8 target lifts. So it can't prove a pair dark on its own, at any wall count. In all 6 rooms the bound of 1 lift per target point also held for the union of all quotient mechanisms.
- **What it doesn't settle.** "Darkness is symmetry" fails once you pass to translation quotients. In B, the half-turn [τ] on X/C3 has all fixed points forbidden. It blocks a lift of a point that isn't the image of S under any symmetry of B. In O, the blocking half-turn comes from a quarter turn, not a reflection. The note disclaims intermediate covers in its first paragraph and again at the end, and that disclaimer is correct. But "rules out that direct midpoint mechanism … at every wall count" holds for X only. Nothing proves that quotient mechanisms block at most one lift in general. Nothing shows the other 7 lifts are lit, and the note says so.

## Gaps

1. **Medium. Translation quotients aren't covered, and they carry new mechanisms.** Room B has Trans(X) ≅ S3 with 4 hidden elements. X_B/C3 has a half-turn whose fixed points are all forbidden and that isn't a physical symmetry. O's quotient has a free half-turn that comes from a quarter turn. The note should change "rules out that direct midpoint mechanism on the mixed unfolding at every wall count" to say "on X itself". It should name translation quotients X/Γ, for Γ in Trans(X), as the open case. It should also record that Trans(X) can exceed the physical symmetry group. The per-target count of 1 survived in all 6 rooms but has no proof.
2. **Medium. The involution hypothesis is essential and under-flagged.** The theorem is about involutions, but the title and the user-facing summary say "half-turns" (any −I automorphism). Fixed-point-free −I automorphisms of order 4 exist (O), and hidden −I maps of order 6 with all fixed points forbidden exist (B). The note should state this. It should also add the one-line argument that a −I map swapping two regular points is automatically an involution, because a translation fixing a regular point is the identity. That argument is what makes the restriction harmless on X.
3. **Low. Two definitions of "free".** The theorem means no fixed points. The consequence section means all fixed points forbidden. The bridge through τ is correct, and I verified Fix(τ) = all corner lifts. The note should state both definitions in one place and say that they differ only by τ for involutions.
4. **Low. The named example uses non-standard marks.** S = (1, 1/2) is an edge midpoint, which forces the doubling remark. The square-centre pair (1/2,1/2), (1/2,3/2) in H gives the same demonstration with d11-type marks and no doubling.
5. **Low. A redundant restriction.** "Linear parts are signed permutation matrices" is automatic. A symmetry permutes the wall directions present, and a horizontal edge (integer length) can't map to a diagonal edge (length k√2). The note can say this instead of stating it as a hypothesis.
