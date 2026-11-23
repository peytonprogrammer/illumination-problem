# D155: review of all-factor-first-shot.md (snapshot 2026-11-22 03:45)

Date: 2026-11-21. Reviewer: adversarial referee.

Reviewed file: `d95-review-queue/snapshots/all-factor-first-shot.2026-11-22-0345.md`. Context read: `qclass-closure/bbbb/thin-gap-periods.md` and `clean-site-cost.md`, the d129, d135, d138 and d139 reviews, the d143 review's C3 paragraph, the d154 V-notch control and the d11 README.

Code: [checks.py](checks.py), log [checks.log](checks.log), 5.6 CPU-seconds. It uses exact integer and Fraction arithmetic on 12 named mixed rooms, 3 diagonal strips and the dumbbell at b = 1, 2, 3. For each mixed room it tests every lattice Γ with Λ_abs ⊆ Γ ⊆ ℤ². That's a finite list per room, not a room search. No network calls.

## Verdict

**Sound with gaps.** No gap is high. The clean-fiber area bound is correct, and the V-notch attains it in every normalization. The axis-span lemma is correct and nearly tight. The dumbbell claim holds exactly at b = 1, 2, 3. The diagnosis of the orthogonal problem is accurate. The note proves nothing new there beyond restating BBBB as graph connectivity. The gaps concern a sharper normalization the note misses, the clean-site hypothesis and how far the dumbbell evidence reaches.

## 1. The 45° area bound

**Counting proof.** It's correct. X → T is a branched cover with derivative the identity, so each point's local degree is its cone angle over 2π. A clean site x has its whole fiber in corner lifts, so D_x = deg = 8·area/V. Distinct sites have disjoint fibers. All corner lifts together carry 8·Σαᵢ/2π = 4(W − 2). Hence deg·|J| ≤ 4(W − 2), that is, area ≤ V(W − 2)/(2|J|). If only some corners stop rays, the bound still holds, because stopping corners are a subset of all corners.

**Normalization.** Each step checks:

- A D4-invariant lattice contains (a, b) + (a, −b) = (2a, 0). If its entry gcd is 1, it contains 2ℤ². The only D4-invariant lattices between 2ℤ² and ℤ² are 2ℤ², the checkerboard D and ℤ². So content 1 gives covol(Λ_rel) ≤ 2.
- The half-turn −I lies in every corner stabilizer, because the stabilizer has order 8/gcd(4, a) and a ≠ 4. That gives 2Λ_rel ⊆ Λ_abs. It holds in all 12 rooms in the log.
- Γ ⊇ Λ_abs, so V ≤ 4·2 = 8.

**Cover.** It's the right one. X is the 8-copy unfolding, which d135 identified with the fourth-root cover of the quartic differential. That cover is connected for every mixed room. The script builds X from the gluing g ↦ g·R_e and gets 8 copies every time. The note's "torus site" is any point of any translation torus quotient. That's more general than half- or quarter-period classes, and the count needs nothing more. |J| counts points of T, not D4-classes (gap 3).

**Exact replay** (`checks.log` §1). At every Γ, the generic-fiber count equals 8·area/V, and D_x = deg holds at every clean site.

| Room | Content | Λ_rel covol | Λ_abs covol | Clean sites on R²/Λ_abs | Area | Bound V(W−2)/(2J) |
|---|---:|---:|---:|---:|---:|---:|
| V-notch B | 2 | 8 | 32 | 4 | 12 | 12 (equality) |
| B/2 | 1 | 2 | 8 | 4 | 3 | 3 (equality) |
| F⁻¹(B/2) = (0,0),(1,−1),(2,0),(1,0),(1,1) | 1 | 1 | 4 | 4 | 3/2 | 3/2 (equality) |
| M (d138) | 1 | 1 | 2 | 0 | 27/2 | vacuous |
| A, C, D (d135) | 1 | 1 | 4 | 0 | 7/2, 25/2, 31/2 | vacuous |
| R2, R3 (d139) | 1 | 1 | 2 | 0 | 10, 13 | vacuous |
| C1 (d139) | 1 | 1 | 4 | 0 | 11/2 | vacuous |
| C2 (d139) | 1 | 2 | 8 | 2 | 5 | 6 |
| hexagon (d138) | 1 | 2 | 8 | 2 | 6 | 8 |

- The V-notch attains equality on R²/Λ_abs (degree 3, J = 4) and on every coarser Γ that has a clean site. In each case deg·J = 12 = 4(W − 2), so every corner lift lies in a clean fiber. The note's numbers (area 12, V = 32, degree 3) and the halved version (area 3, V = 8) match. The clean sites of B/2 are (0,0), (0,2), (1,1) and (1,3) mod Λ_abs.
- M has no clean site on any Γ, so the bound says nothing about M. That agrees with d139, where corner lifts reach two sites but never cleanly. The d11 README names no mixed room in vertex form, so I didn't test a d11 example.
- C2 and the convex hexagon have clean sites. A clean site is a corner-only fact. It doesn't imply darkness.

**Sharper normalization the note misses (gap 1).** V = 8 occurs only when Λ_rel = D (c = 2). The similarity F⁻¹(x, y) = ((x + y)/2, (y − x)/2) maps such a room to an integral room with Λ_rel = ℤ² and half the area (d138 gap 3). The ratio area/V doesn't change under similarity, so the bound is the same inequality in either unit. In c = 1 units, 2ℤ² ⊆ Λ_abs gives V ≤ 4. Then area ≤ 2(W − 2)/|J|. F⁻¹(B/2) attains this with V = 4.

## 2. Axis span and the W = 20 numbers

The lemma is correct. Vertices are integral and walls have slopes 0, ∞ and ±1. So no vertex or wall crossing lies strictly between integer columns, and the section length is affine on each unit slab. At an interior integer column, a disk around an interior point gives positive one-sided limits with integral endpoints, so each one-sided length is at least 1. Summing the slab trapezoids gives area ≥ L − 1.

The strip (0,0),(1,0),(L, L−1),(L, L) has area L − 1/2 at L = 3, 10 and 40. So no bound of the form span ≤ area + c with c < 1/2 holds, and the lemma is within 1/2 of tight.

At W = 20 and |J| ≥ 1: area ≤ 8·18/2 = 72 and span ≤ 73. The arithmetic checks. In c = 1 units the same hypothesis gives area ≤ 36 and span ≤ 37. The higher-genus line also checks: 2g(X) − 2 = 4(W − 2) − #lifts ≤ 3W − 8, and floor(52/2)·72 = 1872. It drops to 936 in c = 1 units.

## 3. Dumbbell

The room is (0,0),(U,0),(U,2),(U+2,2),(U+2,0),(2U+3,0),(2U+3,5),(U+2,5),(U+2,3),(U,3),(U,5),(0,5). It has a = 10·lcm(1,…,b), U = 2a, S = (U − a, 2) and T = (U + 2 + a, 2). Results from the exact tracer (`checks.log` §3):

| b | a | Area (= 20a + 7) | Reflexes | Axis gcds | Directions 1 ≤ \|p\| ≤ b, \|q\| ≤ 40 | All stop at (U, 2) | (a+1, 1) |
|---:|---:|---:|---:|---|---:|---|---|
| 1 | 10 | 207 | 4 | (1, 1) | 162 | yes | reaches T, 1 reflection |
| 2 | 20 | 407 | 4 | (1, 1) | 242 | yes | reaches T, 1 reflection |
| 3 | 60 | 1207 | 4 | (1, 1) | 350 | yes | reaches T, 1 reflection |

The vertical launches bounce in the first chamber. The proof in thin-gap-periods.md covers every vertical component: a is divisible by 10|p|, so the height is exactly 2 at x = U. The checked range |q| ≤ 40 only replays that argument. BBBB membership rests on the cited r = 4 large-area classification. I didn't recheck it, as d129 gap 2 also notes.

## 4. The diagnosis

It's accurate. The graph on sheets uses every monodromy translate of each regular transposition, so a path in it may conjugate each edge independently. A shot needs one marking and one arc for both matchings and both endpoint labels.

The equivalence between "a regular point over x on every factor" and "the graph is connected" is correct:

- The component partition is G-invariant.
- A crossing transposition forces a block 2-cycle.
- A block 2-cycle lifts to 2-cycles, since upstairs cycle lengths are at most 3.

This restates the reviewed BBBB hypothesis. The note says so. Beyond it, the note proves nothing new about completeness. The cylinder paragraph cites cyclic-separation.md, and the note states plainly that the implication is unproved. The dumbbell rules out every finite direction menu fixed before the geometry. It doesn't separate graph connectivity from shot existence, because a legal shot exists (gap 4).

## 5. Census scope

The bound doesn't shrink d139's gap. It gives a finite but larger target, and only for rooms with a clean site. The table below uses d11 tiles: N = 2·area for a canonical room, and N = 4·area for the F-image of a mixed-parity room. The bounds are for W = 20 and |J| ≥ 1.

| Class | Proven V | Area bound | Census N needed |
|---|---:|---:|---:|
| Canonical, c = 2 (Λ_rel = D) | ≤ 8 | 72 | 144 |
| Canonical, c = 1 | ≤ 4 | 36 | 72 |
| Mixed parity (always c = 1) | ≤ 4 | 36 | 144 (F-image) |

A mixed-parity room always has c = 1. If Λ_rel = D, every vertex has one checkerboard colour, so all diagonal intercepts share a parity.

M, R2 and R3 have V = 2, which would give N ≤ 72. That value is observed on named rooms only. So the clean branch at W = 20 needs a census up to N = 144, compared with d139's A/B range of N = 34–80 and d11's completed N ≤ 32. The bound covers the A–B pairs that d11 never checks only in the clean branch. Dark pairs without a clean site have no area bound from this note. d11 found no k = 0 (clean) room below W = 24 for N ≤ 32. The bound doesn't justify the area-20 target behind d139's N = 80.

## Gaps

1. **Medium: the normalization isn't the sharp one.** V ≤ 8 is attained only by c = 2 rooms, which are F-images of integral rooms with half the area. In c = 1 units V ≤ 4, which gives area ≤ 2(W − 2)/|J|, so area ≤ 36 and span ≤ 37 at W = 20. The higher-genus figure drops to 936. Under F⁻¹, marks off the D-lattice become half-integral. State both units and say which one any census uses.
2. **Medium: the W = 20 consequence covers only the clean branch.** Nothing in the note shows that a dark mixed pair at W ≤ 20 has a clean torus site. d11 found the smallest clean room at W = 24 within N ≤ 32. Reword "At W=20 one clean site gives area ≤ 72" as a conditional bound for the clean branch. Also say that it doesn't reduce the census in §5 for other dark pairs.
3. **Low: |J| counts torus points.** The proof counts distinct points of T over any Γ ⊇ Λ_abs, including Γ that aren't D4-invariant. A D4-class of sites may contain several points, which only strengthens the bound. Say this, because "torus site" elsewhere means a half- or quarter-period class.
4. **Low: the dumbbell's evidential weight is overstated.** "Physical evidence for the distinction between graph connectivity and a compatible direction" claims too much. The example shows that a direction bound independent of the geometry fails, and it has a legal shot. BBBB membership is cited, not rechecked here (inherited d129 gap 2).
5. **Low: tightness isn't recorded.** The V-notch attains the area bound with deg·J = 4(W − 2) on every Γ that has a clean site. The strip (0,0),(1,0),(L, L−1),(L, L) shows that span ≤ area + 1 can't be improved below area + 1/2. One sentence each would fix this.

## Re-run

```sh
python3 -B checks.py > checks.log
```
