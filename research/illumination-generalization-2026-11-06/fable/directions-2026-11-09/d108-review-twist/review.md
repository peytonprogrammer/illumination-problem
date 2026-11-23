# D108: review of qclass-closure/bbbb/twist-overlap.md

Date: 2026-11-20. Reviewer: independent referee. Scope: the two-band
inequality, the DB55 witness, the DB55 stretch corollary, and scope against
RESULTS.md §11. Named rooms only (DB55 and its stretches at saved lengths ℓ =
3, 7, 9, 21, 451, 457, plus ℓ = 5, 15 as controls). Exact `Fraction`
arithmetic, 2.5 CPU-seconds in total. No room, direction, or word search.

## Verdicts

| Claim | Verdict |
| --- | --- |
| 1. Wall-width inequality | Sound as a sufficient lighting test, so sound as a necessary condition for darkness. One hypothesis is implicit: both twisted lifts must lie on the same vertical sheet. |
| 2. DB55 witness | Confirmed exactly with two tracers. |
| 3. DB55 stretches | The conclusion holds on every named member, but the written proof has a gap. 16 of 64 cross-chamber pairs per length fall outside it. A one-line repair closes it. |
| 4. Scope | Removes only the DB55 stretch family with 5 ∤ ℓ, for same-class lattice pairs. The class-wide criterion removes no room. DB55 has r = 4, not r > 8. |

## Claim 1: wall-width inequality

**Derivation.** In each band, unfold horizontal reflections. The doubled
coordinate X (x on the front sheet, 2L − x on the back) moves linearly with
slope p per unit rise, modulo P = 2W. A front-sheet seam crossing at c needs
c ≡ X₀ + a p (mod P₀) and c ≡ X₁ − b p (mod P₁). Solutions p form
(c − X₀)/a + (P₀/a)ℤ and (X₁ − c)/b + (P₁/b)ℤ. These meet iff
(a+b)c − bX₀ − aX₁ ∈ bP₀ℤ + aP₁ℤ = gℤ, g = gcd(bP₀, aP₁). Here a, b, P₀, P₁ are
integers, so the gcd is the right generator. The admissible c form a coset of
(g/(a+b))ℤ. An open window I of length w therefore always contains one when
(a+b)w > g. That is the stated bound, with g = gcd(2bW₀, 2aW₁).

**Legality.** Each band is a full rectangle over its open height range, with
walls on both sides. Wall contacts occur strictly between levels, because at
the endpoint and seam levels the path sits at x₀, c, or x₁, all horizontally
interior. Those contacts are therefore smooth. The seam point (c, h) is
interior. The inverse word is a rim-fixing affine map, so it fixes cone points
and maps the segment to a corner-free segment between the original lifts.
Correct.

**Implicit hypothesis.** A path with no horizontal-wall contact keeps its
vertical sheet. So the two twisted lifts must share a vertical sheet. The note
writes "heights h−a and h+b" without stating this. The DB55 stretch proof
then relies on the test "for whichever final sheets", which is false (claim 3).
State the hypothesis explicitly.

**Machine check.** `band()` in `check.py` builds c and p from the lattice and
traces every resulting band path exactly. Across 6 lengths and all sheet
choices, every band path reached its upper mark legally. No assertion fired.

## Claim 2: DB55 witness

With the convention that V moves a front-horizontal lift at offset d by
Y ↦ Y + 2d (mod 10), S on (front, back) goes from Y = −1 to 1, and T on
(front, front) goes from 1 to 3. On the back horizontal sheet the shift is −2d.
The note's "adds two at both marks" assumes both marks are on the front
horizontal sheet.

- σ from (1,1) with displacement (64, 2): the d8 tracer ends at (9,3), legal.
  The only intermediate lattice site is (3,2). The leg counts of 6 and 2
  vertical-wall contacts match a by-hand count (X crosses 5, 10, …, 30, then
  13 and 26).
- Pullback by V⁻¹: Q-displacement (64, 2 − 128). The physical velocity from S
  on its (front, back) lift is (64, 126). Both tracers end at (9,1), legal.
  Lattice sites: (3,4), then (9,1).
- An independent lattice choice (c = 1, p = 60) gives physical velocity
  (120, 238), also legal at (9,1).
- Control: perturbing the pulled-back velocity hits the reflex corner (5,2).

## Claim 3: DB55 stretches

Same-chamber pairs are lit by a chord in a convex square. For cross-chamber
pairs, `check.py` follows the note's recipe literally: horizontal sheets front,
dj ≡ y (mod 5), first mark back → front, and the second mark's vertical lift
chosen to reach the other height.

| ℓ | Same-class cross pairs | Note recipe lit | Sheet mismatch | Repaired recipe lit |
| --- | --- | --- | --- | --- |
| 3, 7, 9, 21, 451, 457 (each) | 64 | 48 | 16 | 64 |

**The gap.** For equal heights, the second mark can land on the back vertical
sheet while the first lands on the front. Example: ℓ = 3, (1,1)–(11,1). Here
d = 1, d′ = 3, j = 1, and the shift is 6, so 1 ↦ 7, which is height 3 on the
back. The two-band test does not apply then. Negating j or swapping the first
mark's lift doesn't help, because the mismatch is invariant under the global
sign. The "four possible shifts ±3±1" count silently lets the final sheet vary.

**The repair.** Choose the second mark's *horizontal* lift independently. On
the back horizontal sheet V shifts by −2d′, which replaces r = d′/d (mod 5) by
−r. For y = 1 the good ratios are {1, 2}, and for y = 3 they're {3, 4}.
Negation swaps the bad set onto the good one. With free sheets, every named
member lights 64/64 pairs, each pulled back and traced exactly. For ℓ ≤ 9 the
d8 cell tracer confirmed each path.

Controls: at ℓ = 5 and 15 (5 | ℓ), the band test fails in 8 of 64
(mark, sheet) configurations. This is the equality case g = (a+b)w = 10, and
the corollary correctly excludes it.

## Claim 4: scope

- DB55 has **r = 4** (scope.log: 4 reflex corners at ℓ = 3, 7, 451, no pinch).
  The brief's "r > 8" is wrong. DB55 and every stretch are BBBB with r = 4 and
  area 50 + ℓ ≥ 21, so they're members of the open core's room class.
- The class-wide criterion is only a necessary condition for darkness. It
  lights no pair by itself, so it removes no room.
- The repaired corollary removes, for **same-class lattice pairs only**, every
  DB55 stretch with 5 ∤ ℓ. Prior coverage was ℓ = 3 (computed), ℓ = 3 + 6k
  (saved paths), and ℓ ≥ 450 (d75). The new lengths are, for example, ℓ = 1,
  2, 4, 7, 8, 11, 13. Lengths 5 | ℓ < 450 that aren't ≡ 3 (mod 6) stay
  open. Different-class pairs and general BBBB layouts are untouched.

## Requested edits to the note

1. In the two-band section, add "both images on the same vertical sheet".
2. In the stretch corollary, replace "whichever final sheets" with the
   horizontal-lift repair.
3. In the DB55 lock paragraph, say that the +2 shift is for front-horizontal
   lifts (−2 on the back). The common-j conclusion is unaffected.

## Re-run

```
cd .context/illumination-generalization-2026-11-06/fable/directions-2026-11-09/d108-review-twist
python3 -B check.py > check.log    # ~2.5 s; imports ../d8-perturbation-test/tracer.py
```

The `scope.log` one-liner counts reflex corners using `d8-perturbation-test/room.py`.
