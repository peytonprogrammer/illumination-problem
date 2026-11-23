# d144: referee report on dyadic-classes (snapshot 2026-11-22-0145)

Note under review: `../d95-review-queue/snapshots/dyadic-classes.2026-11-22-0145.md`. It's
byte-identical to the live `qclass-closure/bbbb/dyadic-classes.md`. Script: `checks.py`. Log:
`checks.log`. The run took 1.3 CPU-s and built only cov4181, R22's 22-gon Q, and the 2×4 rectangle.

## Verdict

**Sound.** All three claims check out. The cov4181 class exclusion now has an independent,
complete check that doesn't use d66's code. The gaps below are low-grade wording and scope
items. None affects a conclusion.

## Method

`checks.py` builds the 4-copy unfolding as an origami: two permutations `h` and `v` on 4n unit
squares. Each square carries its bottom-left vertex label: S lift, T lift, stop (any physical
corner lift, convex or reflex), or regular. Shears preserve these labels. The script runs a
BFS over the complete SL2(Z) orbit of the marked origami. It relabels squares canonically and
tracks `M mod 2`. Vertical flow, up and down, in the state `M·O` is direction `±M⁻¹e₂` in `O`.
So the finite orbit covers every primitive direction, both orientations, all four S lifts,
and all four T lifts.

A separate straight-line tracer on `O` uses no shears. It reproduces the state verdicts
(hits, step counts, and stop or cycle) for every state whose direction has |entries| ≤ 12:
341 of 341 in cov4181, 360 of 360 in R22, and 12 of 12 in the rectangle.

Controls:

- R22 (Q, S=(0,0), T=(2,2)) comes out dark in all three classes. This is the known dark pair.
- The rectangle pair comes out lit in all three classes.

So the decider has teeth in both directions.

## Check 1: cov4181

| Item | Result |
| --- | --- |
| Cells | 28. The script matches the d66 README list and the d86 copy. |
| Strictly simple | Yes. The room is connected, its boundary is one cycle with every vertex of degree 2, and it has no pinch points. |
| Walls | W = 20 maximal edges: 12 convex corners and 8 reflex corners. |
| Normalized | Yes. The gcd of the horizontal edge lengths is 1, and so is the gcd of the vertical edge lengths. |
| Pair | S=(2,3) and T=(4,3) are both interior, with the same parity (0,1). |
| Horizontal chord | Lit. The segment y=3, 2≤x≤4, runs through the interior point (3,3), and both unit edges are open. j=1. |
| Regular sites by absolute parity (0,0), (0,1), (1,0), (1,1) | 10, 8, 0, 11, matching the note. Parity (1,0) has 14 closed-room lattice points, and all 14 are corners. |
| v ≡ (1,1) | Dark. The R22-type point D/2ʲ has parity (1,0). It would be a lattice point on the path other than S or T, and every such site is a corner. The orbit agrees. |
| v ≡ (0,1) | Dark in the complete orbit (3,888 states), for every direction, both orientations, and every S and T lift. This confirms d66's four saved d-dark rows in `pair_level.json` by independent code. |
| v ≡ (1,0) | Lit. Travel counts are even. The attained j are {1, 2}, with no upper tail. |

## Check 2: R22's point

R22's Lemma (Parity obstruction) writes B = 2ʳz with r maximal and z having an odd
coordinate. With D = kv, r = ν₂(k) = j, and z = (k/2ʲ)v, an odd multiple of v. So
z ≡ v (mod 2). The identity is algebraic. `checks.py` confirms it on all 1,680 even D in
[−40,40]². The note also describes the manuscript correctly on two points:

- R22's staircase P has no regular site in any of the three odd classes. Its only non-vertex
  lattice points are a and b, both even.
- The seam-reversal lemma is a separate step.

Claim (2) is correct.

## Check 3: the 4n-state argument

- **Bound.** The 4-copy surface has 4n squares and therefore 16n square corners. An
  angle-2π lattice point uses exactly 4 corners, so there are at most 4n such points. Cone
  points over reflex corners use 12. cov4181 has 88 angle-2π points against a bound of 112.
  Of those 88, 76 aren't corner lifts.
- **Lattice hits.** From a lattice point in primitive direction v, the open segment to p+v
  contains no lattice point. Every singularity and every stop is a lattice point, so the
  only events are at the multiples of v. The one-step map is injective because the flow is
  reversible, so its orbits are chains or cycles of length ≤ 4n.
- **Valuations.** The chain case gives k < 4n. The cycle case gives h + ℓC with
  0 < h < C ≤ 4n. The ν₂ case split is correct, including the odd-difference step for
  j ≥ b = ν₂(C).
- **Conclusion.** A j above ⌊log₂ 4n⌋ can't come from a chain or from the ν₂(h) < b case.
  So it forces the full tail. The small-witness bound follows from the first arrival.

Claim (3) is correct as stated. The note also says correctly that it gives no bound on
direction or area.

## Check 4: scope

A pair that realizes only one of the three classes rules out any strategy that requires a
lit path in each class. It rules out the per-target and per-class versions of the
lighting lemma in W ≤ 20 normalized rooms, so a proof must be pair-level: one class at one
depth.

That conclusion was already in d66, which showed RL-room is false in R* using this same room.
The note adds the dyadic reading of it, and the two exclusions differ in kind:

- (1,1) is a pure parity certificate.
- (0,1) has 10 regular sites and no recognized certificate. It's a non-parity, orbit-level
  obstruction.

So parity certificates explain only one of cov4181's two missing classes. The note doesn't
overclaim. It says the BBBB version remains open, because cov4181 is BBBQ. Its closing claim
is also correct: BBBB supplies regular sites in all three off-source classes but no relay
trajectory.

## Gaps

1. **Low.** "The stated range" in the verdict isn't defined in the note. State it: strictly
   simple, normalized, r ≤ 8 (W ≤ 20).
2. **Low.** The (0,1) exclusion is supported only by citing d66 and the arc-to-orbit
   implication in per-class-converse. Cite an independent complete check, such as this d144
   orbit, so that the claim doesn't rest on a single code path.
3. **Low.** Say explicitly that the (0,1) exclusion isn't a parity certificate. Today the
   reader must infer it from "despite ten regular sites". This separation matters for the
   certificate program (see check 4).
4. **Low.** In the 4n-state argument, say that convex-corner lifts are angle-2π points on
   the surface but count as stops. The bound is unaffected. The strict first-arrival bound
   k < 4n gives j ≤ ⌊log₂(4n−1)⌋, a slightly sharper bound.
5. **Low.** The "named 2×4 rectangle" isn't defined in the note or elsewhere in `bbbb/`.
   This review assumed [0,2]×[0,4]. On that rectangle, the j ≤ 2 statement and both paths
   check out: j ∈ {1, 2}, and all three classes are lit.
6. **Low.** Novelty: the one-class phenomenon is d66's RL-room refutation in dyadic form. A
   sentence that credits d66 would keep readers from taking it as a new obstruction.
