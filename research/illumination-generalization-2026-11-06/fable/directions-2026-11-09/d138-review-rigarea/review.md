# D138: review of rigidity-area.md (snapshot 2026-11-21 23:30)

Date: 2026-11-21. Reviewer: adversarial referee.

Reviewed file: `d95-review-queue/snapshots/rigidity-area.2026-11-21-2330.md`. Context read: d39 `astra.md` and `brief.md`, the d43 review, the d9 and d11 READMEs, the d132, d133 and d135 reviews, and the parametric-orbits and primitive-dark-flats snapshots. I didn't review `corner-orbit-rigidity.md` (d137) or the R22 shear paragraph.

Code: [checks.py](checks.py), log [checks.log](checks.log), 0.3 CPU-seconds. It uses exact integer and Fraction arithmetic on named rooms only. It runs no search over rooms, rays, directions or reflection words, and it makes no network calls.

## Verdict

**Sound with gaps.** No gap is high. The scope audit of d39 is correct. The primitive progression lemma is correct. The identity area = c·d/8 with c ∈ {1, 2} holds exactly on every mixed room I built, including a c = 2 control. The finite-maximum paragraph is a valid deduction from the finite-flat theorem. That theorem is itself conditional (d132 gaps 1 and 2), and the paragraph covers only isolated shapes with integral marks. The gaps concern scope and wording.

## 1. Scope audit

**d39 applies only to essential Rig certificates.** d39 claim 3 is stated for "an essential Rig certificate at r ≤ 8" with corners in at least 3 parity classes. Its proof runs on the canonical quotient Q = DP → N = Q/R_y over the unit pillowcase. It counts ramification of that quotient, and n is the cover degree in unit cells. d43 narrows this further: certificates must be ordinary, meaning over the unit pillowcase, equivalently normalized presentations. Marks must be interior, same-class lattice points. Rooms must be orthogonal. Nothing in d39 or d43 concerns velocities that preserve corner alignments. So the note is right that tangent (first-order) rigidity yields no area bound from d39. The BBBB remark is also consistent. When every B_x is one block, every R_y is too, and no nontrivial quotient exists for essential Rig to use. The note says "universal" for the one-block partition, which is correct but unusual wording.

The note restates the d43 scope as "r ≤ 8, three parity classes, essential Rig over the unit pillowcase". It omits the interior same-class lattice-mark restriction (gap 5). It does flag that mixed rooms need a separate dictionary.

**Census coverage.** `checks.log` §1 confirms each quoted scope line in the READMEs.

- d9 covers every strictly simple polyomino with area ≤ 20 and W ≤ 22, with same-class interior lattice pairs. The note's wording is correct. It omits the W ≤ 22 cap, which doesn't matter at W ≤ 20.
- d11 tiles are half unit squares, so area 20 means N = 40 tiles. A/B pairs are covered for N ≤ 32 and W ≤ 24. C pairs are covered unconditionally for N ≤ 24. C pairs are also covered for N ≤ 32 inside rooms that have an A/B pair. The note's three gap ranges are therefore correct: A/B at N = 33–40, C at N = 25–32 in rooms without an A/B pair, and C at N = 33–40. "N=2 area" in the note means N = 2·area and should be written that way.
- The note mentions a missing piece but doesn't place it in the gap list. canonical45 requires every diagonal wall on a line x ± y ∈ 2ℤ. The named room M = (0,0),(3,0),(4,1),(4,2),(2,4),(0,4) is strictly simple with area 27/2. It has one diagonal wall on x − y = 3 and one on x + y = 6. A G-translation (a, b) changes both intercept parities together, and D4 preserves the pair of parities as a set. So no G-image of M is a canonical45 room. Doubling M gives area 54 > 20. Rooms with mixed intercept parities are therefore uncovered at **every** N, not only at N = 25–40 (gap 4).

## 2. Unbounded-area lemma

The argument is correct. I checked each step.

- **Linear flat.** Dilation is a connected group acting on a finite set of maximal flats, so it fixes each one. A dilation-invariant affine flat contains its limit point 0, so it's linear. The cell inequalities are homogeneous in anchored coordinates. So the positive part L ∩ C is an open convex cone in L.
- **Choice of v.** V = span(L ∩ ℤᵏ) contains e, and V ∩ C is relatively open in V. If the wall projection of V has dimension ≥ 2, then V ∩ C contains rational points with wall vectors not proportional to E, arbitrarily near e. Note that v must lie in V, not merely in L. The note's phrase "its rational span" covers this. Closeness to e isn't needed; any such v works.
- **Primitivity.** Fix columns i, j with |det[E; V]_{ij}| = J ≠ 0. Then det[E + 2JtV; V]_{ij} = ±J. If a prime p divides the content of E + 2JtV, then p | J, so E + 2JtV ≡ E (mod p), which contradicts content(E) = 1. On the named chamfered family (side 18, leg 7; v = side 6, leg 2; J = 6), content is 1 for t = 1…1500. Without the factor J, content 3 appears at t = 2, 5, 8, … (`checks.log` §2), so J is needed.
- **Parity and physicality.** The step 2Jtv is even, so mark classes and diagonal-intercept parities are unchanged. Convexity of the cone keeps e + 2Jtv in C. The log shows every member is strictly simple, with interior marks and preserved parities.
- **Limit.** (e + 2Jtv)/(2Jt) = v + e/(2Jt) → v. The maximum vertex deviation is 1.5, 0.75, 0.3, 0.03 and 0.003 at t = 1, 2, 5, 50 and 500. The point v lies in the open cell, so it's strictly simple and keeps the cell's tie pattern. Every nonzero gap of v is positive, so gap-to-diameter ratios stay bounded below. The area grows like (2Jt)²·area(v).

The orthogonal case needs axis primitivity. The log's L-room has scalar content 1 but x-content 3. The note defers this case to primitive-dark-flats.md, which d133 found sound. The lemma assumes an actual dark flat with these hypotheses, and none is exhibited. The note says so.

## 3. Area = c·d/8

I computed Λ in two independent ways:

1. **From the gluing.** Copy g is glued to copy g·ρ_e along wall e. I placed the copies by breadth-first search, recorded every holonomy, and took the ℤ-span of all developed corner differences plus holonomies.
2. **From edge images.** I took the span of the edge vectors' images under the room group.

I computed d directly by counting the preimages in X of two generic points of ℝ²/Λ. That count doesn't use the area.

| Room | Copies | Area | Λ (HNF) | c | d | c·d/copies |
| --- | ---: | ---: | --- | ---: | ---: | ---: |
| L-tromino (orthogonal) | 4 | 3 | ℤ² | 1 | 12 | 3 |
| L with x-content 3 (orthogonal) | 4 | 9 | 3ℤ×ℤ | 3 | 12 | 9 |
| 12-wall cross (orthogonal) | 4 | 12 | ℤ² | 1 | 48 | 12 |
| r = 4 dumbbell, U = 4, L = 1 | 4 | 46 | ℤ² | 1 | 184 | 46 |
| r = 4 dumbbell, U = 4, L = 2 | 4 | 47 | ℤ² | 1 | 188 | 47 |
| r = 4 dumbbell, U = 5, L = 1 | 4 | 56 | ℤ² | 1 | 224 | 56 |
| d135 chamfer, q = 3 (side 18, leg 7) | 8 | 599/2 | ℤ² | 1 | 2396 | 599/2 |
| d135 chamfer, q = 6 (side 36, leg 23) | 8 | 2423/2 | ℤ² | 1 | 9692 | 2423/2 |
| d135 room A | 8 | 7/2 | ℤ² | 1 | 28 | 7/2 |
| hexagon (0,0),(2,0),(3,1),(2,2),(0,2),(−1,1) | 8 | 6 | ⟨(1,1),(0,2)⟩ | 2 | 24 | 6 |

In every room, the two constructions of Λ agree and Λ ⊆ ℤ². The gcd of Λ's entries equals the scalar content. All holonomies lie in Λ, and the degree is the same at both test points.

- **Mixed rooms.** Λ is D4-invariant and contains 2ℤ². The identity area = c·d/8 holds exactly. The note's chamfer formulas d = 288q² − 4(2q+1)² and area 36q² − (2q+1)²/2 match at q = 3 and q = 6. The hexagon confirms that c = 2 occurs.
- **Orthogonal rooms** (the L, the cross and the dumbbells). Only V4 acts and the connected unfolding has 4 copies. The identity is area = c·d/4 with c = g_x·g_y. The 8-copy formula fails here; for the L-tromino it gives 3/2 instead of 3. The D4 argument for c ∈ {1, 2} also fails: the L with x-content 3 has scalar content 1 and c = 3. The note states section (b) only for mixed rooms, so it makes no false statement. Under axis normalization the orthogonal thresholds are d ≤ 80, with c = 1 and 4 copies. The note doesn't state these thresholds (gap 2).
- **A normalization the note misses.** The map (x, y) ↦ ((x+y)/2, (y−x)/2) is a similarity that maps the c = 2 lattice onto ℤ² and preserves 45° rooms. It sends the c = 2 hexagon (area 6) to a c = 1 lattice room of area 3 (`checks.log`, last room). Its walls stay integral. Marks stay lattice points exactly when mark − anchor has x ≡ y (mod 2) (gap 3).
- The gcd(6q, 4q − 1) = 1 condition holds for every q ≢ 1 (mod 3), not only for 3 | q. The note's condition is sufficient, so it's correct.
- The Riemann–Hurwitz remark is correct: on a torus the base contributes 0, so the degree drops out.

## 4. The finite maximum

The deduction is valid given its input.

- Suppose an isolated dark marked shape modulo dilation lies at an interior point of a maximal flat of dimension ≥ 2. Then the flat supplies nearby nonhomothetic dark shapes, which contradicts isolation. So the maximal flat through it is a ray, which is linear by §2.
- A rational ray λw contains at most one point whose wall content is 1. An irrational ray contains no integral point.
- Cells, including tie cells, and flats per cell are finite. So integral isolated mixed shapes have bounded area for fixed W.
- The direction "rigid in the full family ⇒ rigid in its cell" is the one the proof needs. A shape in a tie cell that bounds a 2-dimensional flat in a neighbouring cell is counted as a ray of its own cell, which only enlarges the finite list.

The claim needs these qualifications:

- The input is conditional. The finite-flat theorem rests on marked-stratum algebraicity and on a classifying map that is only sketched (d132 gaps 1 and 2; d135 gap 1). The note says "Grant", which is honest.
- "Rigid" here means isolated modulo dilation. That isn't d137's first-order notion, and neither notion implies the other. The heading "rigid subproblem" invites the reader to combine it with d137 (gap 1).
- It covers integral marks only. Rational, real and boundary marks aren't covered.
- It's non-effective. It doesn't compare the maximum with 20; the note says so.

## Gaps

1. **Medium: "rigid" in the finite-maximum paragraph means isolated modulo dilation, not first-order rigid.** Neither notion implies the other. The result is doubly conditional: on the finite-flat theorem, and through it on d132 gaps 1 and 2. To fix this, rename the heading to "isolated (ray) subproblem". State that d137-style tangent rigidity doesn't place a shape on a dark ray. List integral marks and fixed W as hypotheses.
2. **Low: no orthogonal statement of the area identity.** For orthogonal rooms the identity is area = c·d/4 with c = g_x·g_y. That gives c = 1 and d ≤ 80 at area 20 under axis normalization. The 8-copy formula fails for them (L-tromino: 3/2 ≠ 3). Scalar content 1 allows c = 3 (the L with x-content 3). Add one sentence giving the orthogonal thresholds, because the area target covers both room types.
3. **Low: content one isn't the full similarity normalization for mixed rooms.** The √2 rotation-similarity maps every c = 2 room to a c = 1 lattice room of half the area. Marks stay lattice points when mark − anchor has x ≡ y (mod 2). That shrinks the c = 2 branch: d ≤ 80 at c = 2 becomes the c = 1 case at area ≤ 10, except for marks off the D-lattice. This doesn't affect finiteness.
4. **Low: the census gap list leaves out the intercept-parity gap.** canonical45 can't represent mixed rooms whose diagonal intercepts have different parities, at any N. Room M has area 27/2 and isn't covered by d9 or d11. The note mentions "arbitrary diagonal intercept patterns" but lists only N-ranges as the extra work. Add M-type rooms at N ≤ 40 as a fourth range. Also write "N = 2·area".
5. **Low: the d39 scope summary is incomplete.** Add that d39 and d43 concern orthogonal rooms with interior same-class lattice marks and ordinary (normalized) presentations, as d43 states. The tangent/Rig separation stands regardless.
6. **Low: minor wording in the lemma.** v must lie in the rational span V, and closeness to e is unnecessary. Assuming an actual dark flat is a hypothesis; no such flat is exhibited.

## Re-run

```sh
python3 -B checks.py > checks.log
```
