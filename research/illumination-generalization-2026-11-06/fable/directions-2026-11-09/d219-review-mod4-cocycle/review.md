# D219 review: mod-4 cocycle note (note-snapshot.md)

Referee: independent. Date: 2026-11-23. Named rooms only: R22 (manuscript vertex list), R22 dilated by 5 (marks (0,0), (10,10)), and cov4181 (d64 covers.json index 4181). Checks: [checks.py](checks.py), output in [checks.log](checks.log). Result: 33 PASS, 0 FAIL, 0.19 CPU-seconds.

checks.py imports the d218 FC-graph code (`regular_graph`, `components`, `note_test`, `pure_move`, `single_moves`) unchanged. It uses the five d218 states (base and σ₁^{±2}, σ₂^{±2}) and no direction, word or room search. The one non-room computation is an algebraic descent on primitive vectors with |p|,|q| ≤ 40, used for the converse in claim 2. It shoots no rays.

**Overall.** No claim is wrong. Claims 1, 2, 3, 5, 6 and 7 are correct. Claim 4 is correct with one wording gap. The note advances **L1** negatively: it closes the mod-4 cocycle and double-cover route and leaves the single-state walk test as the only live form of L1.

## Verdicts

| # | Claim | Verdict |
|---|---|---|
| 1 | (a) Two-step graph; h exact iff every cycle has C ≡ 0 mod 4; c(t)−c(s) = D/2 mod 2 on a component | CORRECT |
| 2 | (b) Darkness ⇔ marked lifts in different regular components in every state and class | CORRECT (the note proves ⇒; ⇐ also holds, see below) |
| 3 | Dilated R22: y = −12 cycle has C = 10; darkness preserved | CORRECT |
| 4 | Triangle A, B, C: boundary sum 1, no cocycle on the corner complement | CORRECT WITH GAPS |
| 5 | (c) A character on H gives a cover above Q°; outer degree-two quotient has z = 0 | CORRECT |
| 6 | cov4181 hand calculation and class-b parity flip | CORRECT |
| 7 | n = 22 counts: R_other ≥ 3; ≥ 13 under d208 §4 (15 at d = 21) | CORRECT |

### 1. Single-state parity

The note's graph is the d218 bipartite graph with each degree-2 x-vertex contracted. A cycle of FC length C has C/2 edges. Every edge has h = 1, so h = δc exists iff every cycle has even edge count, that is, C ≡ 0 mod 4. Paths are trees and always admit c. On an exact cycle the two directions give D/2 and (C−D)/2, which agree mod 2. On a C ≡ 2 mod 4 cycle they differ, so both residues occur.

checks.py confirms this on abstract cycles (k = 1…12 passages, including loops and 2-cycles) and paths. It also confirms it on all 30 (state, class) rows of R22 and cov4181. For example, cov4181 base class b has three C = 2 cycles, which are not exact, and two C = 4 cycles, which are. In every exact component the colour difference of the S and T lifts equals the d218 distance D/2.

### 2. Darkness and separation

Forward direction: a shared regular component gives a nonbacktracking walk through regular sites only. d218 matched these walks to the integer billiard in every row, so the walk is a corner-avoiding billiard path from S to T. Its parity is irrelevant. checks.py confirms that sharing a component and having a joining walk coincide in all 30 rows. R22 shares none. cov4181 shares components only in class b.

Converse, which the note doesn't state but the task's "⇔" asserts: a lighting path unfolds to N steps of a primitive vector v. It visits only a- and x-class lattice points for x = class(v), all regular. The level-2 shears (v₀ ± 2v₁, v₁) and (v₀, v₁ ± 2v₀) carry every primitive v back to its class base arc up to sign. checks.py checks this for |p|,|q| ≤ 40, and it's the standard Γ(2)-orbit fact. So every lighting path is a walk in some state, and ⇐ holds.

Gap (minor): this converse uses the d218 calibration that a pure move acts on directions by those shears. d218 verified this only for single moves. For composite words it needs the action to be a homomorphism, which is standard but not checked here.

### 3. Dilated R22

- The R22 bottom row is the single cell (1,−3), with cells (0,−2) and (1,−2) above it.
- After dilation by 5, the lowest band is −15 < y < −10 with section 5 < x < 10. The dilated room has area 375 and 9 reflexes.
- On y = −12, the sites (5,−12) and (10,−12) are smooth and (6..9,−12) are interior.
- The class-b component through (6,−12) is a cycle with C = 10. Its a-points are (6,−12), (8,−12) and (10,−12), all even-even, and the x-class is odd-even. C/2 = 5 is odd, and the edge cochain on this component is not exact.
- Neither marked lift lies on this cycle.

Darkness follows from the scaling argument: the inverse dilation preserves straight paths and maps corners to corners. checks.py also finds no shared S–T component in the 15 checked rows.

Observation: undilated R22 shows only C = 4 cycles in all 15 rows. So dilation is what produces the odd half-period here. The note says the example isn't normalized or primitive, and that's accurate.

### 4. Triangle

- A = (6,−14), B = (8,−14) and C = (8,−12) are even-even and interior. The side midpoints (7,−14), (8,−13) and (7,−13) are interior.
- On copy 0, the class-b, class-d and class-c graphs each contain exactly one passage joining the corresponding vertices.
- The boundary sum is 3 ≡ 1. The closed triangle lies in the open bottom square, and no lattice point lies strictly inside it.

The disk argument is then sound: any closed 1-cochain on the corner complement vanishes on ∂Δ. The note correctly limits the conclusion to "the corner complement" and keeps the regular sites.

Gap: the triangle exists only on copy 0. On copy 1, neither class-c sheet at A reaches C. The two passages from (A,1) end at (B,0) and (6,−12) on copy 0, each after a wall reflection; checks.log prints both. The note says "on one copy", which is accurate. However, "the same disk argument applies on any unbranched lifted disk carrying all three prescribed edges" should note that a given disk may carry the edges on one copy only.

### 5. Covers and quotients

- ker χ ⊂ H gives a cover above Q°. An intermediate factor needs a subgroup K with H ⊊ K ⊊ G. The two inclusions point opposite ways, so the claim is correct.
- The double of a simply connected room is a sphere, so H¹ = 0.
- On a punctured sphere, the odd peripheral values must be even in number, so two suffice.
- A 2-block system of the generic sheets is a block system for the monodromy, so it gives an outer degree-two quotient. Local degrees over B are then at most 2. Per [fold-converse](../../../../qclass-closure/bbbb/fold-converse.md), z counts the quotient points with local degree 3 (angle 3π). So z = 0, and the kz forced reflexes vanish.

### 6. cov4181

- The d66 cell rows give these statuses: S → (3,3) → T runs through interior sites, and (3,3) is class (1,1) = b. Base class b has S and T on one path with D ∈ {2, 6}.
- The line x = 2 runs over y = 2..4 and x = 4 runs over y = 0..6, with smooth ends. In base class d, S lies on a C = 4 cycle and T on a separate C = 12 cycle. Both cycles are exact. The two copies of S are at D = 2 on the C = 4 cycle.
- Class b under σ₂^{±2}: the distances are S₀T₀ = 12, S₀T₁ = 4, S₁T₀ = 4 and S₁T₁ = 12. The base values are 2, 6, 6 and 2. Every pairing flips D/2 parity: all base values are odd and all twisted values are even. These match d218 checks.log lines 111 and 147.
- Class d shares no component in any of the five states.

The "seven candidate coincidences" figure is taken from d218 (R_other = 14 + 0 + 7) and not recomputed here. The note's caveat is correct: different relative homotopy classes could carry a nonzero period, so this calculation alone doesn't disprove a cohomology class.

### 7. n = 22 counts

- From d ≥ 2n/3: d ≥ ⌈44/3⌉ = 15, so R_other ≥ 30 − 16 − 11 = 3.
- From [d208 §4](../d208-review-condition-i-low/review.md) (r ≤ 8, normalized): d ≥ 20 gives ≥ 13, and d = 21 in the primitive case gives 15.

d208 §4 depends on R1, Fact L, the matching lemma, and the degree-11 and degree-22 group lists, which rest on CFSG. The note cites d208 as "reviewed", which is accurate.

## Which lemma advanced

**L1**, negatively:
1. The off-class relay can't be certified by a mod-4 cocycle or a double cover. Darkness doesn't force cycle parity: dilated R22 has a C = 10 cycle. A local triangle blocks any single class across all three directions. Within one class, the cov4181 σ₂² flip blocks a state-independent coloring on identified lifts.
2. A character gives a cover above Q°, not a factor. A two-color sheet partition gives z = 0.

What remains of L1 is the single-state walk test from d218. No closure is proved.

## First case still open

The first open case is n = 22: a nondirect, same-parity, interior pair in a positive normalized eight-reflex BBBB chart. The task is to find a class x and one state in which compatible lifts share a regular component with D ≡ 2 mod 4, or with gcd(C,4) | 2 − D on a cycle. Under d208 §4 there are at least 13 regular off-class candidates, or 15 when d = 21. Neither the count nor any parity coloring supplies the walk.
