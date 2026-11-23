# D156: review of multitwist-first-shot.md (snapshot 2026-11-22 03:55)

Date: 2026-11-21. Reviewer: adversarial referee.

Reviewed file: `d95-review-queue/snapshots/multitwist-first-shot.2026-11-22-0355.md`. Context read: `qclass-closure/bbbb/thin-gap-periods.md`, `all-factor-first-shot.md`, `cusp-first-shot.md` (opening section), and the d155 review and checks.

Code: [checks.py](checks.py), log [checks.log](checks.log), 0.9 CPU-seconds. The tracer is new and independent of d155's. It scales x by |q| and y by |p|, so a shot in direction (p,q) becomes a 45-degree billiard with integer events. Shots stop at a vertex, at T, or on return to S with the launch direction. The only room is the named dumbbell (0,0),(U,0),(U,2),(U+2,2),(U+2,0),(2U+3,0),(2U+3,5),(U+2,5),(U+2,3),(U,3),(U,5),(0,5) with U = 2a, S = (a,2), T = (3a+2,2), at d155's a = 10, 20, 60. There are no room searches and no network calls.

Scope of this review: the dumbbell section and the stabilizer obstruction. The DB55 and odd-cross bullets, the V-notch section and the area-72 paragraph aren't reviewed here.

## Verdict

**Sound with gaps.** No gap is high. The cylinder data, the value c = 18,060 and both residue claims check exactly at all three parameters. The stabilizer obstruction is a complete proof. The gaps concern a missed strengthening, a smaller twist the note doesn't mention, and how the scope is stated.

## 1. Cylinders, c and the two residues

**Cylinder decomposition.** The script computes it from the vertex list. It cuts at every corner ordinate 0, 2, 3, 5, and each band rectangle gives two cylinders in the 4-copy unfolding, one per vertical-sign class.

| Band | Circumference | Height | C/gcd(C,h) |
|---|---:|---:|---:|
| Left chamber, 0<y<2 and 3<y<5 | 4a | 2 | 2a |
| Right chamber, 0<y<2 and 3<y<5 | 4a+2 | 2 | 2a+1 |
| Through band, 2<y<3 | 8a+6 | 1 | 8a+6 |

The least pointwise rim-fixing shear is lcm(2a, 2a+1, 8a+6). That's 18,060 at a = 10, 136,120 at a = 20 and 1,176,120 at a = 60, matching the note. S and T both sit at y = 2, a rim ordinate, so the multitwist H fixes every lift of each.

**Residue p ≡ 0 (mod c) misses.** The proof is correct. H^k fixes the lift sets and maps vertical to (kc,1). A hit would pull back to a vertical legal segment from x = a to x = 3a+2, and vertical billiard paths keep x fixed. The exact traces agree. For k = 1, −1, 2 the shot from S closes on itself after vertical travel 10 and horizontal travel 10|p|, without meeting T or a corner. That's the H^k image of the closed vertical orbit at x = a. At a = 60, k = 2 this took 176,178 reflections.

**Residue p ≡ a+1 (mod c) hits.** The proof is correct. H^k is a homeomorphism that fixes the corner lifts and the endpoint lifts, so it carries the one-reflection witness to a legal shot in direction (a+1+kc, 1). The exact traces reach T for k = ±1, ±2 at all three parameters. Each hit has vertical travel exactly 2, as the shear predicts. For example, at a = 10 the direction (18071,1) reaches T after 841 reflections, and (−18049,1) reaches T after 841.

**Other residues.** The note says the two residues need not be the only ones. That's right. At a = 10, 45 values of p in [−150, 150] give a hit, including p = 20, 22 and 27.

## 2. The stabilizer obstruction

The proof is complete. Each step checks:

- Let F be an affine automorphism that preserves the corner-lift set and the horizontal line field. F maps critical horizontal leaves to critical leaves, so it maps the corner-cut cylinders bijectively onto themselves. It scales every circumference by the same factor |α|. A finite set can't be carried onto itself by a bijection that scales every element by |α| ≠ 1, so |α| = 1. Circumferences are preserved, and so are heights, because |det DF| = 1.
- The circumferences 4a, 4a+2 and 8a+6 are pairwise distinct. The closures that contain S are a 4a-cylinder and the (8a+6)-cylinder. The closures that contain T are a (4a+2)-cylinder and the (8a+6)-cylinder. The 4a-closures project to x ∈ [0, 2a], and the (4a+2)-closures to x ∈ [2a+2, 4a+3]. The log confirms all of this at the three parameters.
- If DF(0,1) were a successful direction, F⁻¹ of the witness would be a legal vertical segment from F⁻¹(S̃) to F⁻¹(T̃). Those points have x ≤ 2a and x ≥ 2a+2. A vertical billiard path has constant x, even if it runs along a wall. That's a contradiction.

**Must F preserve each cylinder?** No, and the proof doesn't assume it. It uses only the circumference class of the cylinder whose closure contains each endpoint. Elements that permute cylinders of equal circumference exist:

- The vertical-sign deck involution of the unfolding has derivative diag(1, −1). It swaps the two 4a-cylinders of each left band and permutes the lifts of S.
- The twist H' in gap 2 swaps the convex lifts of (0,0) and (2a,0).

**Must F permute lifts of S?** No. The argument applies to F⁻¹(S̃), wherever it lands, so it covers elements that move S̃ off the lift set of S.

**Transposed seed.** The note doesn't treat this case for the dumbbell, but it also fails. The vertical stabilizer maps horizontal to (±1, m). Every such direction ends at the lower doorway lip (2a, 2), by the thin-gap-periods argument, which allows any vertical component. The log replays 1 ≤ |m| ≤ 60 for both signs at all three parameters.

**A strengthening the note misses (gap 1).** The obstruction extends beyond the horizontal stabilizer for the witness family. Any affine automorphism of the unfolding, marked or not, has DF ∈ GL(2,ℤ), because it preserves the absolute period lattice 2ℤ². If DF(0,1) points along (a+1,1), then DF(0,1) = ±(a+1,1). DF then maps a closed vertical leaf with holonomy (0,m) to a closed leaf with holonomy ±m(a+1,1). Corner-cut vertical cylinders have m ∈ {2, 10}. Every closed leaf the script samples in direction (a+1,1) has m = 2·area(P): 414, 814 and 2,414 at a = 10, 20 and 60. A single such leaf is enough. So no affine automorphism maps vertical to (a+1,1). The directions (a+1+kc, 1) are H^k-images of that direction, so none of them is an affine image of vertical either. At a = 10 the same test also excludes all 45 successful p in [−150, 150]. Each of them has a sampled closed leaf with m ∉ {2, 10}.

## 3. The three d155 parameters

| a | c (note) | c (computed) | (kc,1), k = 1, −1, 2 | (a+1+kc,1), k = ±1, ±2 | c' = c/2 residues |
|---:|---:|---:|---|---|---|
| 10 | 18,060 | 18,060 | closed, misses | hit, \|dy\| = 2 | 9,030: same behavior |
| 20 | 136,120 | 136,120 | closed, misses | hit, \|dy\| = 2 | 68,060: same behavior |
| 60 | 1,176,120 | 1,176,120 | closed, misses | hit, \|dy\| = 2 | 588,060: same behavior |

## 4. Scope

**What it refutes.** It refutes a first-shot method that fixes the vertical reference direction and moves it by the horizontal stabilizer. That includes powers of the least multitwist. For this pair, the obstruction covers every corner-preserving element that preserves the horizontal direction. With gap 1 it also covers the full affine group, but only for the known successful directions.

**What it doesn't refute.**

- **The BBBB completeness claim.** The pair is lit: (a+1,1) reaches T with one reflection. So the dumbbell is no counterexample to illumination in BBBB rooms, and it doesn't separate every-factor regularity from shot existence (d155 gap 4). The room's BBBB membership is cited, not rechecked (inherited d129 gap 2).
- **Parabolic methods with a geometry-dependent seed.** On a square-tiled surface every rational direction is parabolic. The (a+1,1) cusp itself gives a positive numerator E_v in the cusp-first-shot test. The note's last paragraph states this correctly: a parabolic theorem needs a reason to pick a successful reference orbit.
- **Seeds or pairs outside this family.** The obstruction concerns the vertical seed and this physical pair only, as the note says.

## Gaps

1. **Low: a missed strengthening.** Holonomy multiplicities show that the witness family (a+1+kc, 1) isn't in the orbit of vertical under any affine automorphism, not only under the horizontal stabilizer. The test is m ∈ {2,10} for vertical against m = 2·area(P) for (a+1,1). The same holds for every successful (p,1) with |p| ≤ 150 at a = 10. This doesn't exclude every successful direction, so the obstruction stays a statement about specific seeds.
2. **Low: c is least only for pointwise rim fixing.** Leave uncut the leaves y = 0 and y = 5, which hold only convex corners. The mirror bands then merge into height-4 cylinders. The twist H' with c' = lcm(a, 2a+1, 8a+6) = c/2 preserves the corner-lift set, fixes S and T, and swaps the convex lifts of (0,0) and (2a,0). Both residue claims therefore hold modulo c/2, which the traces confirm at all three parameters. The stabilizer obstruction already covers H'. One sentence would prevent a reader from treating 18,060 as the residue period.
3. **Low: the obstruction proof should state two steps.** First, F maps the corner-cut horizontal decomposition to itself because it maps critical leaves to critical leaves. Second, the argument applies to F⁻¹(S̃) wherever it lands, so F need not preserve the lift sets of S or T. The note's phrase "even if an automorphism permutes cylinders" covers the conclusion but not the reason.
4. **Low: the transposed pencil isn't stated for the dumbbell.** For the odd cross the note rules out both axial pencils, but for the dumbbell it only rules out the horizontal one. The vertical stabilizer gives directions (±1, m), and these all stop at (2a, 2) by the thin-gap-periods proof. Add one sentence.
5. **Low: say plainly that this is a method obstruction.** The note's last paragraph is accurate. A one-line statement would stop the result being read as evidence against BBBB completeness: the pair is lit, and BBBB membership is cited, not rechecked.

## Re-run

```sh
python3 -B checks.py > checks.log
```
