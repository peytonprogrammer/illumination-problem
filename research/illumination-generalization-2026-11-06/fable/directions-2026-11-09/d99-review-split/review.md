# D99: review of primitive-stabilizer.md and bbbb-split.md (snapshots)

Date: 2026-11-20. Reviewer: independent referee. Reviewed files:
`primitive-stabilizer.snapshot.md` (SHA-256 prefix `333ad76f`) and
`bbbb-split.snapshot.md` (`6354f371`). Both prefixes match the live originals
in `qclass-closure/bbbb/`.

## Verdicts

| Claim | Verdict |
| --- | --- |
| 1a. Primitive sheets contain A_n at n ≥ 49 | Sound. It rests on Burness–Guralnick, not on Jordan. |
| 1b. A lit lift pair in the source class at n ≥ 73 | Sound, but nearly empty. Such a pair already exists in every class of both named rooms, including dark R22 at n = 15. |
| 1c. The missing step is an affine return from a dark edge to a lit edge | Accurate. For the commonest seed it's exactly the d92 mirror-suborbit question. |
| 2a. Descent inequality, with an area-independent loss | Sound. The loss is uniform in area. |
| 2b. Degree-2 loss ≤ 56 | Sound. On the cross, the actual index I is 2, 2 and 1. |
| 2c. Both endpoints collapsed means one axis, so the pair is directly visible | Sound. It restates d91's kernel-escape lemma for one involution. |
| 2d. Degree-2 bound as a new restriction on a dark pair | No. See the last section. |

## Claim 1: primitive-stabilizer.md

**Which classification.** Proposition P of d81 is a fixed-point-ratio
argument. Burness–Guralnick Corollary 2 (CFSG) applies to u = g_x², which has
prime order 3. Outside the product-action family it gives fpr(u) ≤ 1/2, so
n ≤ 6z_x. d81 then excludes the product-action family, and the d82 review
checked that exclusion. Jordan's 3-cycle theorem covers only z_x = 1. From
memory: Guralnick–Magaard's minimal-degree theorem (support ≥ n/2 outside
listed families) gives the same bound. Liebeck–Saxl's n/3 would give only
n ≤ 9z_x ≤ 72.

**Support bound.** Cone angles on the double are π, 2π and 3π. So g_x has
cycle type 1^f 2^q 3^z, and supp(g_x²) = 3z_x ≤ 3r ≤ 24. Then
6z_x ≤ 48 < 49 for every reflex-bearing class, so the bound is correct at
r ≤ 8. The off-class count 2(n−1) − 2r − q_a is exact in the full component U,
because each reflex corner contributes exactly two diagonal branches. It
equals 56 at n = 49, r = 8 and q_a = 24.

**The n ≥ 73 step.** I checked the lemma step by step and found no gap:

- A smooth first hit gives a perpendicular return to ιx.
- A transverse crossing lands on a same-parity interior lattice point.
- A reflex corner has two inward half-rays.
- The constrained triangulation has W + b + 2i − 2 triangles.
- A marked interior vertex lies in at least 4 triangles, and a smooth wall
  mark in at least 2.

The arithmetic n > 4r + 4 + f_a + 3z_a ≤ 8r + 8 holds.

The conclusion is weak, though. The seed from step 1 is a mirror pair
{x, ιx}. It exists whenever one cardinal ray from one interior mark ends on a
smooth wall. [r22.py](r22.py) found no interior mark, in any class of R22 or
the b = 7 cross, whose four cardinal rays all end at reflex corners. That
includes the dark R22 endpoints S = (0,0) and T = (2,2). So "a lit pair in the
source class" holds far below 73 and carries little information. For the seed
{s, ιs} at the source, an M-map sending it to {s, t} must fix s and send ιs to
t. That means t ∈ F_s·ιs, which is d92's mirror suborbit. In R22 that set is
{ιs, (4,0) wall lift}, so no such map exists. The note states the gap honestly.
The lemma only matters in classes with i ≤ r/2 and no smooth cardinal hit.

**Other parts.** The centralizer paragraph is correct. Block-diagonal
relabelings of the 2-cycles are even, so C_{A_n}(g_a) maps onto S_q. A_n has
no nontrivial action on q ≤ n/2 points. The d14 S₆ example (q = 3, M = C₃) is
in d14 proof.md, line 119. I didn't recompute it. The finite-residue procedure
gives valid necessary conditions, but it wasn't run.

## Claim 2: bbbb-split.md

**Uniformity in area.** The genus can't vary: N is covered by the sphere Q,
so N is a sphere. A zero of N has exactly k reflex preimages, so kz ≤ r. The
pole count is z + 4 ≤ 4 + ⌊r/k⌋ ≤ 8. The punctured base has free π₁ of rank
z + 3. So I ≤ (k!)^(z+3) depends only on r. Its largest value at r = 8 is
(8!)^4 ≈ 2.6·10^18, at k = 8 and z = 1. The orbit of the cover class under F_N
lies in this finite set. The index chain [(F_N)_u : J] ≤ I·k and the inclusion
J·v ⊂ f((F_Q)_s·t) both check, so the inequality holds.

**Degree-2 loss.** Riemann–Hurwitz from genus 0 to genus 0 gives exactly 2
branch values, and both are poles. The cover is fixed by that unordered pair,
so I ≤ C(z+4, 2) ≤ C(8, 2) = 28, and kI ≤ 56. Note one more point: a degree-2
factor is Galois, so δ ∈ K ⊂ (Z/2)² (d91). Degree-2 factors exist only in rooms
with an axial or half-turn symmetry.

**Collapse.** f(s) = f(ιs) forces δs = ιs, so δ lifts an axial reflection that
fixes S. If both endpoints collapse, they lie on the axis of that one
reflection. A simply connected symmetric room meets its axis in one interval,
so the endpoints are directly visible. In the exchange case there's no
interior fixed lift. In the preserve case the only fixed interior lifts are
the two lifts of the half-turn center. Both cases check. This is d91's
kernel-escape lemma for a single involution.

The odd-winding lighting test is a valid sufficient condition.

## Claim 3: named rooms

[blocks.py](blocks.py) ([log](blocks.log)) builds the sheet monodromy. It
computes every block system by closure and the group order by deterministic
Schreier–Sims. R22's order was cross-checked by brute-force enumeration.

| Room | n | r | Primitive | Block systems | \|G\| |
| --- | --- | --- | --- | --- | --- |
| R22 | 15 | 9 | No | One system: 5 blocks of size 3. The block action is A₅. | 233280 |
| Cross b = 7 | 96 | 4 | No | Three size-2 systems (rx, ry, rot), and one size-4 system (K-orbits) above all three. The action on 24 blocks is S₂₄. Each 48-block action is imprimitive. | ≈ 8.73·10^37 |

R22 has r = 9, which is outside r ≤ 8. It has |K| = 1, so the degree-2 section
doesn't apply to it. Its fold is a non-Galois k = 3 quotient, the double of the
5-cell staircase (7 poles, 3 zeros). Both marks map to the wall points u and
v. Upstairs |F_s·t| = 3, and downstairs |(F_N)_u·v| = 1.

[affine.py](affine.py) ([log](affine.log)) computes F for Q and for each deck
quotient. It reproduces d91 and d92 exactly on Q: index 12672, |F·s| = 40,
|F_s·t| = 36, and e(S) = e(T) = 2. In this table, S = (6,0) and T = (0,6).

| N | k | z, poles | Veech index | Collapsed | \|(F_N)_u·v\| | Quotient mirror suborbits | I (bound) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Q/⟨ry⟩ | 2 | 2, 6 | 12672 | S only | 18 | 1 at T | 2 (15) |
| Q/⟨rx⟩ | 2 | 2, 6 | 12672 | T only | 18 | 1 at S | 2 (15) |
| Q/⟨rot⟩ | 2 | 2, 6 | 12672 | neither | 18 | 1, 1 | 1 (15) |
| Q/K | 4 | 1, 5 | 3168 | both | 9 | 1, 1 | not computed |

All images are regular, and every case matches 2c. The inequality holds with
large slack, for example 18 ≤ 2·2·36. Downstairs suborbits are upstairs/k
here, so descent loses size and doesn't amplify it.

## Is the degree-2 constraint a new restriction?

No. The constraint has three parts, and none of them is new:

- It applies only to symmetric rooms.
- Its non-collapse part is d91's kernel-escape lemma.
- Its bound, |(F_N)_u·u′| ≤ 56 e(S), is d92's unevaluated upstairs bound
  multiplied by 56.

It excludes a dark pair only with a growth theorem on N, and no such theorem
exists. On the cross, every non-collapsed quotient mirror suborbit has size 1,
so the bound holds and constrains nothing. Axis marks always have e ≤ 3
(d92), so symmetric-room candidates on axes remain untouched.

## Method and limits

The arithmetic is exact, on integers and permutations. Only named rooms were
used, and no web access. Total CPU time was about 75 s. Burness–Guralnick,
Guralnick–Magaard and Liebeck–Saxl are cited from memory, and d82 had read
Burness–Guralnick Corollary 2. The F_N enumeration assumes Veech groups in
SL(2,Z). If F_N is larger, the computed orbits are lower bounds.

Re-run: `python3 -B blocks.py order > blocks.log; python3 -B affine.py Q > affine.log; python3 -B r22.py > r22.log`.
