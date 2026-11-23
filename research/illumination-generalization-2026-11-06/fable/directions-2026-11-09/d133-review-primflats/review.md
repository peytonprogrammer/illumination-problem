# D133: Referee review of primitive-dark-flats.md

Date: 2026-11-21. Target: snapshot `d95-review-queue/snapshots/primitive-dark-flats.2026-11-21-2200.md`. It's identical to the live `.context/qclass-closure/bbbb/primitive-dark-flats.md`. I assumed the candidate finite-flat theorem in `parametric-orbits.2026-11-21-2200.md` and didn't review it. I also read `high-valency-geometry.md` (d80), the d80 review, `search-plan.md` and the d66 README, and I grepped the bbbb notes for the parity convention.

Code: `checks.py`, log `checks.log`, run with `python3 -B checks.py > checks.log`. It uses exact rationals, one named L-shaped room and hand-built integer matrices. There's no search over rooms, rays, directions or reflection words. CPU time is under 0.1 s.

## Verdict

**Sound with gaps.** I found no error in the factorization, the one-axis primitive test, the Smith/progression argument, or the use of d80. The gaps concern scope: what the conditional reduction covers relative to the W≤20 goal, and one uncited decision step.

## 1. Axis factorization

- **Stretching preserves darkness in orthogonal rooms.** The map D=diag(a,b) isn't an isometry: (1,1) at 45° becomes 9.46° for a=3, b=1/2. It sends direction (p,q) to (ap,bq), which is a bijection on directions. D commutes with both axis reflections, and a convex-corner reversal −v also commutes with D. Lines map to lines and corners map to corners of the same kind. So D conjugates the billiard flow, including stopping at reflex corners. Darkness is quantified over all directions, so D preserves the dark set and its inverse does too. `checks.log` §1 traces four rays in the L-room: two stop at the reflex corner (2,2) and two make 40 bounces. Each stretched trace matches event for event at the stretched points.
- **The weak-order cell is preserved**, since D acts by a positive scalar on each axis's gaps.
- **Splitting.** Maximal flats of the cell map to maximal flats. The diagonal group is connected and acts continuously on a finite set, so it fixes each flat. Invariance under common dilation makes L linear. Then (2x,y)−(x,y)=(x,0)∈L gives L=Lx×Ly. Integer points split the same way: if (x,y) is integral, so is (x,0). So V=Vx×Vy for the rational spans. This step needs the finite-flat theorem: a continuum of flats could move under the group. The note says so.
- **Scope.** The conjugation fails for 45° walls. D·R·D⁻¹ for the diagonal reflection is [[0,6],[1/6,0]], which is not the specular reflection in the stretched wall (§1 of the log). The stated target still includes 45° walls, although only orthogonal rooms are being worked. See gap 4.

## 2. The one-axis primitive test

- **Primitivity.** The gcd of the wall gaps equals the gcd of all wall-edge displacements, because the boundary visits every level. This is the per-axis normalization in d80 ("horizontal and vertical wall-length gcds are one"). In the project, "same parity" means the same class in E[2], that is x and y separately mod 2. So the per-axis parity lattice Λ is the correct factor.
- **Rank one.** Az=k·g, so gcd(Az)=|k|·gcd(g). Only the positive one of ±g can be a primitive wall vector. Each fine gap lies in [1, its wall gap], so the enumeration is finite. Toy V3 has exactly one witness, [1,2,3,1,1]. In toy V4, parity forces g=(4,2,6), and the test correctly rejects.
- **Rank ≥ 2.** The first Smith invariant equals the gcd of the entries; that condition is necessary. It's also sufficient: U·B·V=D with d₁=1 makes the first column of B·V equal U⁻¹e₁, which is primitive. Matrix B1 shows this matters: its columns have gcd 2 and 3, but its entries have gcd 1. The Smith step finds a=(1,−4,3). Proportional images are handled by v=Nv₊+w. The minor argument is correct: any prime p dividing all of a+tMb divides det=±M, and then a+tMb≡a mod p, which contradicts primitivity of a. The log confirms 2000/2000 primitive terms for B1. Without the factor M, terms t=1,3,4,5,7 fail, so M is needed. Toys V1 and V5 give 300/300 positive primitive points of Λ. V5 has a free mark, so A has a kernel there. Toy V2 (d₁=2) is rejected. So the test either refutes or yields an arithmetic progression in rank ≥ 2, and a finite certified list in rank 1. Rank 0 is impossible once a positive vector exists.
- **Count.** An orthogonal W-gon has W/2 vertical edges, so at most 10 x-levels at W=20. Adding 2 marks gives 12 coordinates and 11 gaps; the count of eleven is correct. The bound (d+1)(2H+1)^(d²) holds; the log checks it exactly for d≤3. That gives 144(2H+1)^242 pairs per cell, which is 10^117.6 at H=1. The note already calls this a design and not a run.

## 3. The d80 restriction

d80 says: in a strictly simple normalized orthogonal lattice room with r≤8 and area n≥120, every pair of distinct interior points with an irrational coordinate is lit. The d80 review rates it "sound with fixable gaps." W≤20 gives r=(W−4)/2≤8. The perturbation keeps the walls fixed, so it stays in the same normalized room of area ≥120. It moves at least one mark along a real kernel direction inside L∩C⊂D, and a suitable ε makes that mark's coordinate irrational. That contradicts d80, so A is injective on the real factors. The citation supports the claim as stated, including its restriction to the room where d80 applies. The final sentence ("puts its product flat in this injective regime") applies only when the pair of factors is the true dark flat, not to every enumerated kernel. That needs a wording fix (gap 5).

## 4. Sufficiency of H

The logic is correct for the **primitive same-parity lattice** subproblem. Setting y=0 in combined rows bounded by H gives x-rows bounded by H, and an independent subset of them can be chosen. The true pair (Vx,Vy) appears in the enumeration. Its saved witnesses (wx,wy) lie in V∩C⊂L∩C⊂D, so the pair is dark. Every dark output is a genuine counterexample, and the largest constructed area is a valid cutoff for primitive examples. It is **not** by itself a reduction of W≤20 (gap 1).

## Gaps

1. **Medium: the reduction covers only part of the W≤20 goal.** The test finds only per-axis-normalized rooms with same-parity lattice marks. Toy V2 in §4 of the log shows the problem. Its flat contains positive integral points with every wall gcd even. Those are normalized rooms with marks at 1/2 and 5/2, and the primitive test rejects the flat. Several cases fall outside the test:
   - Rational non-lattice marks.
   - Different-parity lattice pairs.
   - Irrational marks at area <120, where d80 doesn't apply. The real flat through such a mark may have no positive rational points, so no H helps there.
   - Boundary and corner targets.

   With H supplied, the unrestricted-integral Cramer bound in parametric-orbits covers the rational cases. The note should say that the full reduction combines the two and should name the residual irrational case.
2. **Low to medium: the "individual-room decision procedure" is uncited.** Step 2 relies on it. The project's pair-level route (d66, `search-plan.md` item 4) gives a negative only after a complete orbit and an independent check of the decision theorem's hypotheses. Cite a terminating procedure for same-parity lattice marks. A finite SL₂(ℤ) orbit of a marked square-tiled surface would do. Otherwise step 3 doesn't terminate with a certified answer.
3. **Low: the dependence on finite flats is load-bearing for factorization.** Name the parametric-orbits theorem explicitly in the Result line as the reason the diagonal group fixes each flat.
4. **Low: the factorization is restricted to orthogonal rooms.** Stretching fails for 45° walls (checks §1). State that the note doesn't apply to the 45° part of the stated target.
5. **Low: wording.** The last sentence of the d80 section should say "if this product is a dark flat." "Certifies that none exists" should say "no primitive positive same-parity lattice point on V in the cell." It doesn't certify that the pair is lit.
6. **Low: the effectivity audit is unchecked.** I didn't verify the d130 remarks and the remark on supplied-direction residues. They don't affect the theorem.

## Overstatement

Mostly none. The note says "this note does not provide either" for H and "not a proposed run." The Result line's "terminating test" is accurate for primitive inputs. The phrase "the outstanding effective input" overstates slightly, because of gap 1.
