# d149 review: cyclic-separation.md (snapshot 2026-11-22-0050)

**Verdict: sound with gaps.** The all-slope cyclic criterion is correct, including its handling of forbidden corners and physical lifts. The finiteness claim is true, but it holds only for a fixed room and isn't effective at practical scale. On DB55, the stabilizer has index above 100,000 in SL(2,Z). The note proves no illumination result, and it says so. The two-class conjecture stays open.

Files:

- [checks.py](checks.py) runs in about 48 CPU-seconds with `python3 -B checks.py 24 100000 BCO`.
- [checks.log](checks.log) holds the output.
- The checks use only the named room DB55 and do no room search.

## What the checks computed

The room is DB55, made of the chambers [0,5]×[0,5] and [8,13]×[0,5] joined by [5,8]×[2,3]. It has 53 cells. The checks use three independent computations:

- **(A) Direct billiard.** The ray reflects at flat-wall lattice points and stops at every convex or reflex corner. The tracer starts the ray in all four sign choices of each unoriented primitive slope.
- **(B) Reference-arc criterion.** This is the note's test L^k I ∩ J ≠ ∅ with L = A³X³. It uses the archived `roomtools` pillowcase tuple, and I and J are the union of the two physical lift cycles.
- **(C) Labelled unfolding.** The 4-copy unfolding is a 212-square origami. Its squares carry labels for corner stops, S-lifts and T-lifts. SL(2,Z) acts on it by the two shears and −I. Each slope v gets a label for its cusp of H ∩ Γ(2). The label is the ⟨T,−I⟩-orbit of (g·O, g mod 2) with g v = e₁.

| Check | Result |
|---|---|
| (B) vs (A): reference slopes, all 336 same-parity interior pair-and-class rows in all four parities | 336 agree, 0 disagree |
| Relaxed control A·X instead of A³X³ | 52 rows connect only when the corner is not deleted |
| (A) vs horizontal flow on g·O, 720 slopes with max(\|p\|,\|q\|) ≤ 24, pair S=(2,2), T=(10,2) | 0 mismatches |
| Full orbit of (labelled origami, g mod 2) | over 100,000 states, so [SL(2,Z) : H∩Γ(2)] > 10⁵ |
| Cusps of H∩Γ(2) among the 720 slopes | 582 distinct; 85 contain at least two slopes; 51 of those 85 are lit |
| Cusps whose members have different lit status | 0 |
| Cusp widths | 10 to 690 |
| −I in H (deck rotation) | yes, for all 720 slopes |

For the pair (2,2), (10,2), the first lit slopes are:

| Class | First lit slopes | Lit / all slopes up to height 24 |
|---|---|---|
| (1,0) | (3,±2) | 166 / 243 |
| (1,1) | (3,±1) | 154 / 234 |
| (0,1) | (4,±1) | 146 / 243 |

All reference slopes are dark for this pair. This agrees with deletion-invariance.md: the zero-power arcs fail, and other arcs succeed. The pair is lit in all three classes.

## Item 1: the all-slope cyclic criterion

The criterion is correct.

- The cube removes corner continuations. U = A³ fixes every letter on a 1-cycle (convex corner, cone angle π) or a 3-cycle (reflex corner, 3π). It swaps exactly the regular 2-cycles. A walk on the arc preimage that alternates U and V therefore continues straight only through regular vertices. The 52 relaxed-only rows show that the cube is essential.
- Lift choice is handled. I is the union of the full A-cycles of both source lifts in the double, so it's U-invariant. The orbit ⟨U,V⟩I equals the union of (UV)^k I. Including all four lift pairs is correct and necessary.
- The converse step is correct. Each primitive step joins two lattice points of parities a and a+c. Consecutive steps differ by the point reflection x ↦ 2(P+v) − x, which lies in the pillowcase group. So the steps trace the same arc back and forth.

## Item 2: the finiteness claim

- **Finite index: yes.** The labelled cover has a finite SL(2,Z)-orbit. The kernel of the action on the finite marked fibres also has finite index. Γ(2) has three cusps, one per primitive parity class. So H∩Γ(2) has finitely many cusps in each class. The orbit-BFS in checks.py shows that you can compute them in principle.
- **Invariance: yes.** In the sample, no cusp has members with different lit status, across 85 cusps that contain at least two slopes. 51 of those 85 cusps are lit, so the test is not vacuous. The horizontal-flow check shows that the shear conventions in checks.py are correct.
- **Practicality: weak.** H∩Γ(2) has index above 10⁵, with cusp widths up to 690. Among the 720 slopes up to height 24, 582 lie in distinct cusps. So the finite set of representatives is probably in the thousands for this 12-wall room. Here the exact representative set wasn't computed, because the orbit exceeded the 10⁵-state limit within budget. Up to height 24, each class is lit through its representatives exactly when the direct billiard lights it. This comparison is limited to height 24.

## Item 3: scope

The note proves four things:

1. The exact single-slope criterion.
2. A per-room reduction of the all-slope question to finitely many cusp representatives. The reduction exists, but nobody has enumerated it.
3. The normal-closure transitivity theorem. Its Riemann–Hurwitz step is consistent: Q is a sphere, and a degree-two cover branched at four points has genus 1. This review didn't check that step numerically.
4. The 2-adic cylinder class table. The algebra checks out; see gap 6.

The note proves no illumination statement.

**Open statement.** Take any normalized BBBB, strictly simple orthogonal lattice room and any same-parity interior lattice pair in it. Then at least two distinct classes c each have a primitive v ≡ c (mod 2) and an integer k such that L_v^k I_v meets J_v.

The normal-closure theorem doesn't reach this statement. Normal closure allows a different conjugate at each step. The statement needs a single cyclic orbit to meet the target. The per-room finiteness gives no bound that holds uniformly across rooms.

## Gaps

1. **Medium.** The note calls the reduction "a finite all-slope statement". It is a reduction in existence only. The note gives no index, cusp count or algorithm. On DB55 the index exceeds 10⁵ and the cusps number in the hundreds or more. The note should state that the reduction is room-dependent and not effective at this scale. It should also not suggest that the reduction helps decide the conjecture.
2. **Medium.** The note states but doesn't prove the computation of I_v and J_v in the arc-adapted marking. You need to transport the lift labels along a Γ(2) word, or along a braid word for the arc. The criterion is only as checkable as that transport. Cite or state the algorithm from per-class-converse.md.
3. **Low.** The proof sketch skips the bounce case. At a stop, U or V fixes the letter, so the algebraic orbit reflects back through the regular source. It then continues in direction −v. This is harmless only because the slope is unoriented. State this explicitly.
4. **Low.** Pointwise fixing of mark lifts is stronger than needed. The weaker condition is that the affine map preserves each mark's lift set, or exchanges the S and T sets. That condition gives a larger group with fewer cusps. The deck rotation −I and the determinant −1 deck reflections diag(±1,∓1) are then free symmetries. Correctness is unaffected.
5. **Low.** The note doesn't say which surface "preserve the corner stops" refers to. In the half-translation double, every corner is a cone point, so any affine map preserves the stops automatically. In the 4-copy translation unfolding, convex corners are regular points and need explicit labels.
6. **Low, not independently checked.** This review didn't re-derive three items: the cov4181 two-class failure (d144), the 661/84/2 and 506/239/2 witness counts, or the claim that universality forces each site to move both blocks.
