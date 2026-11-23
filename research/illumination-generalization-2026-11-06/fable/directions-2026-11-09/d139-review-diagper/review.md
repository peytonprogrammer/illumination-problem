# D139: review of diagonal-periods.md (snapshot 2026-11-22 00:10)

Date: 2026-11-21. Reviewer: adversarial referee.

Reviewed file: `d95-review-queue/snapshots/diagonal-periods.2026-11-22-0010.md`. Context read: the d11 and d9 READMEs, the d138 review and `qclass-closure/bbbb/rigidity-area.md`.

Code: [checks.py](checks.py), log [checks.log](checks.log), about 1 CPU-second. It uses exact integer and Fraction arithmetic on 5 named rooms plus F(M) and 3M. It runs no search over rooms, directions or reflection words. It makes no network calls.

## Verdict

**Sound with gaps.** No gap is high. Every mathematical claim I tested holds exactly on M and on two more mixed rooms I built. The minimality proof is correct. The census arithmetic matches the d11 cutoffs. The period lattice, the index, both degrees, the one-site and two-site statements, the cone-angle count and the mod-2 direction claim all check. The gaps are an omitted branch of the degree dichotomy, an uncited lemma, and missing qualifiers.

## Rooms used

| Room | Vertices | Area | W | Diagonal intercepts | Corner angles (π/4) |
|---|---|---:|---:|---|---|
| M | (0,0),(3,0),(4,1),(4,2),(2,4),(0,4) | 27/2 | 6 | x−y=3, x+y=6 | 2,3,3,3,3,2 |
| R2 | (1,0),(4,0),(4,2),(2,2),(1,3),(1,4),(0,4),(0,1) | 10 | 8 | x+y=4, x+y=1 | two reflex 5π/4 |
| R3 | (0,0),(2,0),(2,1),(3,1),(4,2),(4,4),(1,4),(0,3) | 13 | 8 | x−y=2, x−y=−3 | one reflex 3π/2 |
| C1 (canonical, c=1) | (0,0),(3,0),(3,1),(2,2),(0,2) | 11/2 | 5 | x+y=4 | control |
| C2 (canonical, c=2) | (0,0),(2,0),(2,2),(1,3),(0,2) | 5 | 5 | x+y=4, x−y=−2 | control |

All five are strictly simple and scalar-primitive. R2 and R3 are non-convex.

## 1. The map F(x,y) = (x−y, x+y)

Every claim holds on M, R2 and R3 (`checks.log` §1).

- **Canonical image.** All image diagonal intercepts are even. Each image is strictly simple, with the same W and the same corner angles in order.
- **Area.** The area ratio is exactly 2. A direct count of d11 tiles in each image gives N = 54, 40 and 52, equal to 4·area.
- **Paths.** I traced 9 fixed directions from one mark in each room with an exact billiard tracer. In 27 of 27 rays, F of the original trace equals the trace of the image, including the stop reason (corner, target or bounce limit).
- **Marks.** F maps interior lattice points onto the interior A/B points of the image, bijectively. The class is A when x+y is even and B when it's odd. No lattice point maps to a C point; image C points are images of unit-square centres.

## 2. Minimality

The proof is correct. I checked each step.

- Similarities that preserve the four directions have linear part t·g or t·g·F/√2, with g in D4. So "t Id or tF up to a signed permutation" is the full list, reflections included.
- In case t·Id, scalar content 1 forces t to be an integer. Odd t keeps an odd intercept difference, so t ≥ 2 and the area is at least 4·area.
- In case tF, the anchored image entries have gcd dividing 2. Mixed parity gives vertices of both colours (`checks.log` §2: colours {0,1}), so an odd entry occurs and the gcd is 1. Hence t is an integer, and t = 1 gives 2·area.
- For all three rooms, every image under D4 and the four translation residues mod 2 keeps the parity set {0,1}. (1/2)F isn't integral.
- The 3M control has content 3. Its least canonical image F(M) has area 27, below 2·area(3M) = 243. The primitivity hypothesis is therefore needed, and the note states it.

## 3. Census consequence

The arithmetic is right. A d11 tile is half a unit square, so the F image of a room of area A has N = 4A tiles. The A/B cutoff N ≤ 32 gives A ≤ 8, and A = 20 gives N = 80.

The sentence omits two d11 qualifiers:

- d11's A/B census also requires W ≤ 24 and interior, distinct, same-class marks. Pick's theorem makes the W cap automatic here. A = I + B/2 − 1 with I ≥ 2 gives W ≤ B ≤ 2A − 2 ≤ 14 at A ≤ 8. At A = 20 the same bound allows W up to 38, so the cap must be restated there. It's harmless for a W ≤ 20 target.
- The C-pair ranges (N ≤ 24, and N ≤ 32 inside A/B rooms) don't apply to lattice marks, because no lattice point maps to C. They cover only square-centre marks of the original room.

The note correctly says that opposite-checkerboard lattice pairs become A–B pairs, which d11 doesn't check at any N. The new mixed range is A/B pairs at N = 34–80 (original area 17/2 to 20), plus A–B pairs at every N.

## 4. Periods

I computed Λ_abs two independent ways for each room:

1. **From the unfolding.** I built the 8-copy unfolding on quarter-square triangles and took the span of the holonomies of the dual-graph cycles.
2. **From the group.** I took the translation subgroup of the affine reflection group, anchored at an axial-diagonal vertex. That vertex's two reflections generate a group of order 8 in every room.

I counted degrees as preimages of two generic points, without using the area.

| Room | Λ_abs (HNF) | Λ_rel | Index | d_abs | d_rel | Corner sites |
|---|---|---|---:|---:|---:|---:|
| M | ⟨(1,1),(0,2)⟩ | ℤ² | 2 | 54 = 4·area | 108 | 2 |
| R2 | ⟨(1,1),(0,2)⟩ | ℤ² | 2 | 40 = 4·area | 80 | 2 |
| R3 | ⟨(1,1),(0,2)⟩ | ℤ² | 2 | 52 = 4·area | 104 | 2 |
| F(M) | 2ℤ² | ⟨(1,1),(0,2)⟩ | 2 | 54 | 108 | 2 |
| C1, c=1 | 2ℤ² | ℤ² | 4 | 11 = 2·area | 44 | 4 |
| C2, c=2 | ⟨(2,2),(0,4)⟩ | ⟨(1,1),(0,2)⟩ | 4 | 5 = area | 20 | 4 |

The two constructions of Λ_abs agree in all six rooms.

- **Mixed class.** Λ_abs is the checkerboard lattice, Λ_rel = ℤ², the index is 2 and d_abs = 4·area. M has d_abs = 54 and d_rel = 108, and F(M) has the same degrees.
- **Endpoint lifts.** Every interior lattice mark in M, R2 and R3 has 8 lifts, and all 8 project to S mod Λ_abs. So all 16 lifts of each of the 12 + 2 + 9 same-checkerboard pairs lie over one site. Corner lifts cover exactly the 2 sites, and the quarter turn fixes both.
- **Canonical c=1 branch.** C1 confirms Λ_abs = 2ℤ² and d_abs = 2·area.
- **Half-turn lemma.** 2Λ_rel ⊆ Λ_abs holds in all six rooms.
- **Cone angles.** In M, R2 and R3, each corner of angle aπ/4 has gcd(4,a) lifts, each of cone angle 2πa/gcd(4,a). That gives a outgoing germs per direction. The tested angles are a = 2, 3, 5 and 6.
- **Direction classes.** In the basis (1,1),(1,−1), a primitive leaf from the marked site meets the other site exactly when p and q are both odd. That class is the set of physical primitive directions (m,n) with m+n odd, including both axial directions. The two avoiding classes are the physical directions with m and n both odd, including both diagonals. I checked 10 directions.

## 5. Scope and overstatement

The note's opening paragraph is accurate. It claims a census gap and a degree target, and it explicitly disclaims any degree bound for dark rooms. The final paragraph correctly says that a chain count doesn't force a source lift to meet a target lift. The issues are below.

## Gaps

1. **Medium: the degree dichotomy omits the canonical c=2 branch.** "The distinction is exact" compares only the mixed class (d_abs = 4·area) with canonical c=1 (d_abs = 2·area). Canonical c=2 rooms have no single formula. C2 has d_abs = area, so its area-20 target would be 20. F(M) has d_abs = 2·area. F⁻¹ separates them: a canonical c=2 room is F of an integral room of half its area. If that room is mixed, d_abs = 2·area; if it's canonical c=1, d_abs = area. To fix this, add one sentence giving this split and state which area normalization the area-20 bound uses. This sharpens d138 gap 3.
2. **Low: the half-turn lemma is cited but not stated.** A proof fits in two lines. The deck map −I fixes every corner lift, because a corner of angle aπ/4 with a ≠ 4 has a stabilizer of order 8/gcd(4,a) that contains −I. For a path γ between corner lifts, γ followed by the reverse of −Iγ is a closed loop with holonomy 2·hol(γ). So 2Λ_rel ⊆ Λ_abs, which `checks.log` §3 confirms in six rooms.
3. **Low: the census sentence omits qualifiers.** Add W ≤ 24 and interior, distinct marks. Pick makes W automatic at A ≤ 8 (W ≤ 14 with an interior pair), but not at A = 20. Say that the C ranges don't apply to lattice marks. State the new range as A/B at N = 34–80, plus A–B pairs at every N.
4. **Low: the direction classes are given only in lattice coordinates.** Add the physical translation. The meeting class is m+n odd, which includes the axial directions. The avoiding classes are m and n both odd, which include the diagonals.
5. **Low: the germ and chain count assumes every corner lift is forbidden.** That matches the d9 and d11 tracers, which stop at any corner. If only reflex corners stop, the a = 1 and a = 2 lifts (cone 2π) don't break leaves, and the sum must run over stopping corners. The a = 3 lifts (cone 6π) would then need an explicit convention. State the convention.
6. **Low: wording.**
   - "The vertices cannot then all have x+y even" follows from mixed parity, not from primitivity.
   - "54 half-tiles" means 54 d11 tiles, each half a unit square. Write "N = 54 tiles".
   - Case t·Id should say that even t gives 4·area, so the comparison is 2·area against 4·area.

## Re-run

```sh
python3 -B checks.py > checks.log
```
