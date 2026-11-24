# d223 referee review: the area-22 imprimitive quotient

Note: `note-snapshot.md`. Checks: `checks.py`, log in `checks.log`. The run takes 2 s of CPU at nice 10 and ends with 0 failures. It uses two hand-made symmetric rooms and a random permutation self-test. It runs no room enumeration and no ray, direction, word, or room-size search, and it makes no network calls. Every billiard trace uses a direction chosen by hand.

## Summary

| # | Claim | Verdict |
|---|---|---|
| 1 | N is a sphere; two simple branch values at poles with smooth preimages; c₂=2, c₃=0, z=4, q=12; fiber formulas | CORRECT |
| 2 | BBBB ⇔ qₓ≥1; 1≤qₓ≤5; ≥7 off-class sites exclude the (2,11) row; suborbits 1,1,20 | CORRECT (conditional on d208 §4) |
| 3 | I(S)∩I(T)≠∅ ⇔ T=σS; σ axial or half-turn; 24 regular coincidences, 24−2qₐ≥14 off-class; d=20 vs 21 | CORRECT |
| 4 | Double-cover graph test | CORRECT (brute force, 76,446 pairs, 0 mismatches) |
| 5 | Axial half-room H; census gives T or σT; seam-contact parity | CORRECT WITH GAPS (minor) |
| 6 | Stars, 4≤qₐ≤5, three fiber types, half-turn subcase | CORRECT WITH GAPS (a sharpening is missed) |
| 7 | Partner-pair sufficient tests | CORRECT |
| 8 | First open configuration | CORRECT |

Overclaim: none found. The note says plainly that it closes no case and has no dark example.

**New observation.** This branch is exactly the set of area-22 rooms with a parity-preserving symmetry. A degree-two subcover is always Galois, so a deck involution δ exists. By d91, δ descends to an axial reflection about a lattice line or a half-turn about a lattice point. Conversely, such a symmetry commutes with all four pole permutations (checked on both hand rooms). The branch is nonempty in the BBBB core: the hand room below is an area-22, 8-reflex, 20-wall room with every Bₓ universal and suborbits 1, 1, 20.

## Hand-made rooms

**Axial room P (area 22).** H has the 11 cells (0,0)–(0,4), (1,0)–(1,3), (2,1) and (2,3), and P is H plus its mirror (x,y)↦(−1−x,y). The axis is x=0.

- P has 8 reflexes, 20 walls and no pinch. The axis meets ∂P only at (0,0) and (0,5), both smooth.
- H has 11 cells, 4 reflexes and 12 walls. Both seam ends are convex corners of H.
- The cell mirror commutes with all four pole permutations, giving 11 blocks of size 2.
- Per-parity (p,q,z,b): (0,0) (2,3,1,1); (0,1) (1,2,2,1); (1,0) (2,3,1,0); (1,1) (3,4,0,0). The totals are (8,12,4,2).
- The two internal 2-cycles are at the seam ends, so the distinguished poles sit over the seam-end parities.
- The orbital valencies from one sheet are 1, 1, 20, and all four Bₓ are universal.
- For the marks S=(1,1) and T=(1,3), the stars are disjoint and fill 8 of H's 11 cells. The four lifts have four distinct regular images, and q₍₁,₁₎=4 with type (3,4,0). This pair is directly visible, so it only illustrates the structure.

**Half-turn room Z (area 16).** Z is [0,4]×[0,2] ∪ [2,6]×[2,4], with center C=(3,2). C is interior, and the two internal 2-cycles are the two lifts of C, both at parity (1,0).

## 1. Quotient and fibers: CORRECT

- **Sphere and branch points.** RH for a double cover of spheres gives exactly two simple branch points.
- **Where f can branch.** Branching over an N-point of local degree e gives 2e upstairs, and 2e≤3 forces e=1, a pole of N. Off the pillowcase poles, Q→B is unramified.
- **The smooth preimage.** It has local degree 2 over B, so it is regular.
- **Counts.** With k=2, c₂+2c₃=2 and local degree at most 2 force c₂=2 and c₃=0. Then r=2z gives z=4 at r=8. Next, q=22−2−8=12, and the pole count is Σpₓ=44−24−12=8.
- **Fiber formulas.** All 2,804 assignments with sums (8,12,4,2) and bₓ≤pₓ give an upstairs degree of 22 per pole. Each also gives 8 three-cycles, 26 two-cycles, 12 one-cycles and the genus-0 RH total of 42. The hand room realizes one of them.

Note on notation: d208 §4 says "z ≤ 3" at n=22. That bound is per pole (zₓ, the 3-cycles of hₓ on 11 blocks). The note's z=4 is the total number of zeros of N. The two don't conflict, but the note should say "z = Σzₓ = 4" so that nobody reads it against d208.

## 2. BBBB and uniqueness: CORRECT (conditional on d208 §4)

- **qₓ=0.** Every 2-cycle at x is internal to a block. The closure of internal pairs under G stays inside the G-invariant pair partition. The self-test checked this in 16,466 cases.
- **qₓ>0.** A 2-cycle over a regular N-site is inter-block. With one external orbital, its closure contains every external pair and hence everything. The self-test confirmed this whenever its random group had a single external orbital. The single orbital itself comes from d208's matching lemma (H ⊇ A₁₁, R1). The note cites this correctly.
- **The (2,11) row.** The bound 2qₐ≤11 gives qₐ≤5, which leaves at least 7 regular sites off-class. Case (ii) needs q≤⌊m/2⌋=5 with all q over a, so the row fails its hypotheses.
- **Uniqueness.** Blocks through i are unions of suborbits containing {i}. With sizes 1, 1, 20 and 22 sheets, only {i, i′} is a proper nontrivial block. The hand room shows that these suborbits occur in an actual room.

## 3. Coinciding images: CORRECT

- **The equivalence.** Distinct lifts with a common image are deck partners, which gives T=σS. Conversely, δ maps {s, ιs} onto both lifts of σS.
- **Possible symmetries.** δ is holomorphic over B, so its derivative is ±I in flat charts. On P it becomes a sign-diagonal isometry. It can't be the identity, because δ≠id and δ≠ι (ι is antiholomorphic). Diagonal reflections don't cover the identity of B.
- **External orbital count.** On the external orbital, R counts upstairs 2-cycles whose sheets are external. These are the 2·12=24 over regular N-sites, and the 2 at branch sites are internal. Then 2d=R+J gives 40=24+16, so J=2r exactly. Off-class, this leaves 24−2qₐ ≥ 14.
- **Partner orbital.** It has d=1, R=2 and J=0. It is marked exactly when T=σS, because a cell has one vertex of each parity. So d=20 or d=21, as stated.

## 4. Double-cover graph test: CORRECT

The test has to determine whether K separates b₁ from b₂ without using the transport. `checks.py` builds N as a cell complex from the lifted tree a–x–y–w. The faces are m discs and the edges are 3m lifted arcs. The double cover is a random 1-chain with boundary b₁+b₂, plus random face relabelings. The test sample was 120 genus-0 seeds of degrees 3–10, with 40 Hurwitz/conjugation variants each. That gave 4,800 double covers, with branch poles chosen at random over any of the four classes.

| Check | Result |
|---|---|
| Lifted cover is a sphere branched exactly at b₁,b₂ | 4,800/4,800 |
| Every quotient cycle cuts N into exactly two regions | all |
| One upstairs cycle ⇔ K separates b₁,b₂ (cell computation) | all 2,766 cycle cases (1,474 separating) |
| Rule vs. brute-force upstairs connectivity, ordered pairs of distinct regular a-lifts | 76,446 pairs, 0 mismatches |
| Path or nonseparating cycle without a pole: exactly one lift over v is reached | all 14,876 |
| Deck partners connect ⇔ pole component or separating cycle | all |
| Two-traversal partner witness ⇔ adjacent distinguished x-pole or odd 2-edge cycle | 16,128/16,128 |

The proof in the note is complete. It covers a branch pole at both ends of a path, which lifts to a cycle. It also covers parallel edges and isolated vertices.

An early run reported 114 mismatches. They came from a bug in my own consistency check, not from the note. After the fix, all checks pass.

## 5. Axial half-room: CORRECT WITH GAPS (minor)

- **The axis.** σ preserves parities, so c is an integer and H is a union of 11 whole cells. A reflection of a Jordan curve has exactly two fixed points, and a 90° or 270° sector can't be invariant. So the seam ends are smooth points with walls perpendicular to the axis, and the axis is otherwise interior.
- **Corner counts.** H has 4 reflexes and 8 convex corners (6 inherited plus the 2 seam ends), so it has 12 walls. It is strictly simple. The hand room confirms each count.
- **Census scope.** Area 11, W=12≤20. The census record certifies all distinct interior lattice pairs through area 21 in both parities. Area 11 is in the small validated run (225 same-parity and 3,483 different-parity pairs). An off-axis interior S of P is interior in H, even when it is next to the seam.
- **Legality.** "A legal H-ray misses both seam endpoints" is right: they are convex corners of H, and the census tracer stops at convex corners. Every other H-corner is a P-corner or its mirror, so the unfolded path is legal in P. A contact with the open seam, including at a lattice point, becomes a straight crossing of the interior axis. No H-ray runs along the seam, because S₀ is off the seam line.
- **Exact trace, hand room.** From S=(1,1) with velocity (−1,1), the H-ray hits the seam lattice point (0,2) once and reaches T=(1,3). In P, the same start passes (0,2) and reaches σT=(−1,3). The vertical ray, with 0 contacts, reaches T in both rooms.
- **Periodic-orbit remark.** It is correct as a conditional statement.

Gaps:

- The census conclusion is existential. It says nothing about which target is reached, and the note says so. It also doesn't cover the mixed case where one mark is on the axis and one is off it. The note's sentence about "a projected mark on the seam" covers this, but the first-open paragraph lists only the disjoint off-axis subcase.
- The census record is an imported input. This review didn't rerun it.

## 6. Stars and fiber types: CORRECT WITH GAPS

- **Stars.** Same-parity stars are disjoint, so 8 of 11 cells are prescribed. Four distinct regular images over a give 4≤qₐ≤5. Exactly (3,4,0), (0,4,1) and (1,5,0) remain, as Part A confirms.
- **Half-turn center.** The center is interior and a lattice point. Its two lifts are the ramification points, as the Z room confirms. Parity a forces pₐ≥2, which leaves only (3,4,0). The five stars use 20 cells.
- **Missed sharpening.** In the axial case the ramification points are the two seam ends: δ swaps the front and back sheets, so its fixed points lie on ∂P ∩ axis. The hand room confirms this. So bₓ counts the seam ends of parity x. If one seam end has parity a, (0,4,1) is excluded. If both do, only (3,4,0) remains. The note states the parity constraint only for the half-turn.

## 7. Partner-pair tests: CORRECT

- **Half-turn.** Dσ=−I, so the reversed and rotated prefix leaves C with the arrival velocity. C is interior and regular. In the exact trace on Z, from (1,1) with velocity (2,−3), the path reflects at (5/3,0), passes C=(3,2) straight, and reflects at (13/3,4). It then reaches σS=(5,3).
- **Axial.** For a vertical axis the seam-end wall is horizontal, and specular reflection is diag(1,−1)=−Dσ. In the exact trace, from (1,1) with velocity (−1,−1), the path reflects at the smooth seam end (0,0) and reaches σS=(−1,1). The same ray stops at the convex corner (0,0) in H. This confirms the note's remark that projecting to H loses connections through the seam ends.

## 8. First open configuration: CORRECT

Each ingredient is stated correctly: d=20 for disjoint images, qₓ≥1 at all x, ≥14 off-class candidates, and the residual given by claim 4. The equivalence "dark ⇔ separated in every state" is the d220 statement, conditional on FC as d220 noted.

## Lemma advanced and first open case

**Lemma advanced: L1.** The area-22 imprimitive branch is now an explicit, exactly testable degree-two problem. The double-cover rule is verified, and there is a census-based partial result: from S, T or σT is lit. No case closes.

**First open case.** Take a nondirect same-parity interior pair in an area-22, eight-reflex BBBB room with a parity-preserving half-turn and two distinct off-center orbits. This subcase has no census reduction. The axial off-axis subcase is the next one: σT is lit and T is not settled.

All of these rooms are determined by an 11-cell half. A symmetric-only area-22 run would therefore be small compared with the forecast 3.1 CPU hours for the full area-22 census. That run is a new compute search, so it needs Daniel's approval.
