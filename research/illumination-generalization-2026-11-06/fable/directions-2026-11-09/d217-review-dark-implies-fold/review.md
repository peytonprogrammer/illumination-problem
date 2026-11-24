# D217 review: dark implies fold (note-snapshot.md)

Referee: independent. Date: 2026-11-23. Named rooms only (R34-base, R22, P6, and the 5-cell staircase tiles). Checks: [checks.py](checks.py), output in [checks.log](checks.log): 0 failures, under 1 CPU-second. The only ray work is the requested bounded check from the R34 mark (2,0): 224 primitive directions with |p|,|q| ≤ 9, grid crossings capped at 4·area = 76.

**Overall.** No claim is wrong. Claims 1, 3, 4 and 5 are correct. Claims 2 and 6 are correct but have wording gaps. The note advances **L1** by scoping it, not by closing it. It refutes fold-only necessity (R34), records r ≥ 9 for the corner-only-upstairs branch, and restates the open reachability lemma as a mod-4 walk condition.

## Verdicts

| # | Claim | Verdict |
|---|---|---|
| 1 | Closure graph gives the finest G-invariant equivalence; a nontrivial proper partition gives an intermediate cover | CORRECT |
| 2 | Off-class midpoint witness ⇔ legal single-state FC walk of length ≡ 2 mod 4 | CORRECT WITH GAPS |
| 3 | R34-base: strictly simple, degree 19, only even-even regular sites, the pair is dark, no proper factor | CORRECT |
| 4 | All three off-classes corner-only upstairs ⇒ r ≥ 9 | CORRECT |
| 5 | Single-factor (k,z,m) table, areas ≤ 16, q = 2m−2−2z, 2 ≤ q ≤ ⌊m/2⌋ | CORRECT (one wording gap) |
| 6 | Hand check on R22 and P6 via N5 (q=2, z=3, k=3,4, kz=r) | CORRECT WITH GAPS |

### 1. Closure of A

The edge set {gi,gj} is G-stable, so G permutes components and the component partition is G-invariant. Any invariant equivalence containing A contains every translate gA, hence every edge, hence every component. Because Q is connected, G is transitive. Components are therefore translates of one another, all of the same size, and form a block system. A block system that is neither discrete nor universal corresponds to a subgroup strictly between a point stabilizer and G. That subgroup gives an intermediate cover of the punctured sphere, which completes over the poles. checks.py confirms finest-ness by brute force over all 203 partitions of six points for the dihedral group D6. The closures are {03|14|25}, {024|135}, and the universal block for A = {01}.

Minor gap: the note leaves transitivity implicit. It is needed for equal block sizes and for the covering correspondence.

### 2. Midpoint ⇔ length 2 mod 4

Fix a primitive direction v. The parity class of v is x−a. S and T are in the same class, so the developed displacement N·v has N even, N = 2j. The point S + j·v lies over a + j·(x−a), which is x exactly when j is odd. Legality makes every interior vertex regular, so a legal walk of length 2j with j odd has a regular midpoint over x. That midpoint is the off-diagonal coincidence of the two inward-running lifts, as in [midpoint-necessity](../../../../qclass-closure/bbbb/midpoint-necessity.md). Conversely, a realized regular midpoint over x is by definition the midpoint of a legal straight path. Its two halves concatenate to one single-state walk of length 2j with j odd. Both directions hold.

Gaps (wording, not logic):
- The equivalence holds per direction class. A witness over x can come only from walks in direction class x−a. The note says "for a single state, a single arc", which implies this but does not state it.
- "Off-class midpoint witness" has to mean a *realized* midpoint of a legal path, not membership of a regular coincidence in the marked algebraic component. Under the second reading the ⇐ direction fails. cov4181's seven unrealized class-d coincidences in midpoint-necessity show this.

### 3. R34-base

Exact data from `d8-perturbation-test/rooms.json`, entry `R34-base`:
- Area 19, which is prime. The room has 15 reflex and 19 convex vertices (34 walls), no pinch, and is strictly simple.
- The regular sites are exactly (2,0) and (6,0) (interior) and (4,0) and (8,−2) (smooth). All four are even-even, so all three off-classes are corner-only upstairs.
- Parity argument: reflection across x = c with integer c maps x to 2c−x, which keeps the parity of x. Every developed image of T is therefore even-even. A nonzero even displacement has gcd g ≥ 2, so its first primitive step lies strictly before T. That step has an odd coordinate, so it folds to a lattice site outside the even-even class, which must be a corner. checks.py also verifies the gcd and odd-coordinate facts for every even displacement in [−12,12]².
- Bounded exact ray check from S = (2,0) with the d212 tracer: all 224 primitive directions stop at a corner at primitive step 1. Of these stops, 182 are reflex and 42 are convex. Each stop corner has the parity of S+v. No ray reaches T or returns to S within 76 crossings.
- No proper factor: 19 = km with k, m > 1 is impossible. This matches d93 (`R34-base … [(1, 19)]`, G primitive).

Convention note: the argument stops rays at convex corners as well as reflex ones, which is the project's tracer convention. The 42 convex first hits would need separate treatment under a retro-reflection convention at 90° corners. The project does not use that convention.

### 4. Local count, r ≥ 9

The reasoning in the note is sound, including the cases the brief asks about:
- **Axial neighbours.** Each axial neighbour P of an interior mark carries the two edge-adjacent star cells. Two adjacent cells cannot form a pinch. Two cells would make P a smooth wall point and four would make it interior. Both are regular off-class sites, which the hypothesis forbids. So P has three cells and is reflex.
- **Shared neighbour.** T−S is a difference of two axial unit vectors. (±1,±1) changes the class, so the only case is (±2,0) or (0,±2). The shared site then carries all four cells, so it is interior and off-class, which is a contradiction. This is stronger than fold-converse.md's "directly visible", and it is correct.
- **Ninth.** The third cell at the east neighbour shares an edge with one cell of the S-star. That gives a diagonal neighbour with two edge-adjacent cells. The site is off-class (odd-odd relative to a), so it is reflex. Its parity differs from all eight axial reflexes, which are (odd,even) or (even,odd).
- **Boundary-adjacent marks.** Neighbours may lie on the wall. The argument uses only the four cells of each interior star and the absence of off-class regular sites, so boundary neighbours cause no gap. The argument does **not** apply to smooth-wall marks, which have two-cell stars. The note correctly restricts it to interior marks.

Instance: R34 has 8 distinct axial reflexes and diagonal reflexes (3,−1) and (1,1), with r = 15. checks.py also confirms that R22 and P6 are **not** in this branch. R22 has off-class smooth sites (−1,0), (1,0), (2,1), (2,3), and P6 has six. In both rooms the axial step fails, as expected.

### 5. Single-factor table

N is a sphere. Its preimage points over the poles have local degree 1, 2 or 3 (convex, regular, zero). Riemann–Hurwitz gives −2 = −2m + q + 2z, so q = 2m−2−2z. q ≥ 2 follows from distinct regular marked images. q ≤ ⌊m/2⌋ holds because every regular N-point lies over a and uses two of the m sheets there. Thus m ≥ z+2 and m ≤ 4(z+1)/3. With k ≥ 2 and kz ≤ 8, exact enumeration gives exactly (2,2,4), (3,2,4), (4,2,4), (2,3,5) and (2,4,6). The upstairs areas are 8, 12, 16, 10 and 12, and q = 2 in every row. r = kz + c₃ is correct, since a zero has local degree 3 over B, which forces local degree 1 in Q→N.

Wording gap: (c) must mean corner-only **in N**. "Corner-only upstairs" implies corner-only in N, because a regular N-point lifts only to regular points. Under the upstairs reading, though, claim 4 already gives r ≥ 9 and the table is redundant. The weaker N-level hypothesis is the one that covers R22 and P6.

### 6. R22 and P6 via N5

- Staircase base (d216 P0): m = 5, z = 3, 7 convex, and exactly 2 regular sites, (0,0) and (2,−2), both in the R22 mark class. q = 2·5−2−6 = 2 matches. The fibre sum is 7 + 2·2 + 3·3 = 20 = 4m.
- The P6 tile Qp is the same 5-cell staircase. Its two regular sites, (1,0) and (3,2), are in the P6 mark class (1,0).
- R22: area 15, k = 3, r = 9 = kz. P6: area 20, k = 4, r = 12 = kz. So c₃ = 0 in both.
- Separation argument: zeros lift only to reflex corners, so they are never live. Off-classes are corner-only in N5, so a live x-vertex is a degree-1 pole and reverses the walk onto the same arc. A legal walk in N5 therefore stays at its starting a-vertex and its at most two x-neighbours. This matches d61's special case "Parity factor at x". The marked images are distinct in N5 (d61 table: "images distinct in N5"), so every state is separated. This depends on the quotient, as the note says.

Gaps:
- The opening sentence "all three off-classes corner-only" holds in N5 only. Upstairs, R22 has 4 off-class smooth sites and P6 has 6. A reader who carries over the (b) hypothesis would misplace these rooms.
- The argument is independent of slope, but the note does not say so. Every direction class reduces to one primitive arc from a to x. The only input is the local degrees at the N5 poles.

## Which lemma advanced

**L1** (dark ⇒ costly obstruction), by scoping only:
1. Proper-fold necessity is false. R34 is dark by parity on a prime-degree cover with no factor.
2. The corner-only-upstairs branch costs r ≥ 9 with no factor needed.
3. The single separated-fold branch has no surviving (k,z) with kz ≤ 8.
4. The remaining gap is restated exactly as the existence of a single-state legal walk of length ≡ 2 mod 4.

The note proves no new closure for the BBBB core.

## First case still open

The first open case is the open reachability lemma at its smallest area. Take a nondirect, same-parity, interior pair in a normalized, positive, eight-reflex BBBB chart. Every B_x is universal, so no separating parity factor exists. Off-class regular sites exist, so claim 4 does not apply. The case has n = 21 and d ≥ 2n/3, which gives R_other ≥ 2. The task is to produce, for some x, one single-state legal FC walk of length ≡ 2 mod 4 joining the marks. The d81 threshold d ≥ 2n/3 is also unproved for areas 21 through 48. No dark instance of this case is known; the d216 pinned controls are lit.
