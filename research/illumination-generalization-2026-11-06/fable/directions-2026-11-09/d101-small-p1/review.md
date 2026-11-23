# d101: referee report on Q07, Q08, and Q09

Date: 2026-11-20. Referee: Opus 5.5 subagent, independent of d66, d69, d81, and d82.
Scripts: `mp_check.py` (own exact tracer; it imports nothing from d8), `swap_check.py`.
Logs: `mp_check.log`, `swap_check.log`. Total CPU time is about 15 s.

## Verdicts

| Row | Item | Verdict |
| --- | --- | --- |
| Q07 | Normalization step (d66 step 1, RESULTS §3.1, §5.1 step 1) | **Sound.** Two wording fixes: translate first, and say "conjugates" instead of "commutes". |
| Q08 | Lemma MP (d69 §2, RESULTS §3.13) | **Sound** under the project's room definition, where walls lie on integer lines and pinches are excluded. 200 of 200 saved witnesses and 1,089 searched paths satisfy it. |
| Q09 | d81 findings 5 and 6 (README lines 58, 60) | **Wording only, no gap.** The threshold n ≥ 49 stands. Corrected text is in section 3. |

## 1. Q07: normalization

**Setting.** `P` is a strictly simple orthogonal lattice room. `g_h` is the gcd of the
horizontal wall lengths, and `g_v` is the gcd of the vertical wall lengths. Let
`A = diag(1/g_h, 1/g_v)`.

**Proof check.**

1. **Lattice structure.** Each difference of corner x-coordinates is a signed sum of
   horizontal wall lengths along the boundary. So after you translate a corner to the
   origin, every corner lies in `g_h Z × g_v Z`. Then `A P` has integer corners, so it's
   again a union of unit cells. The written step omits the translation. Without it,
   `A P` can have non-integer corners. For example, an `L` with corners at `x = 1, 3, 5`
   has `g_h = 2`, and its scaled corners sit at `x = 1/2, 3/2, 5/2`.
2. **Reflections.** `A` doesn't commute with the reflection `R_c` in `x = c`. Instead,
   `A R_c A^{-1} = R_{c/g_h}`, which is the reflection in the image wall. The same holds for
   horizontal walls. Equivalently, at a vertical wall the velocity rule
   `(v_x, v_y) -> (-v_x, v_y)` commutes with `A` acting on velocities. So `A` maps billiard
   paths to billiard paths, with time preserved and length not preserved.
3. **Illumination of a pair.** `A` is a homeomorphism of the plane that maps `P` onto
   `A P`. It maps interior points to interior points, and corners to corners. So it maps
   corner-avoiding paths to corner-avoiding paths. The same holds for `A^{-1}`. Hence
   `(S, T)` is lit in `P` exactly when `(A S, A T)` is lit in `A P`.
4. **W and strict simplicity.** `A` preserves maximal straight segments and turning
   points, so `W`, `r`, and the convex/reflex type of each corner are unchanged. A pinch is
   a boundary self-touch, which is a topological property, so `A` neither creates nor
   removes pinches. Connected interior and no holes are preserved too.
5. **Rational marks.** `A` has rational entries, so rational marks stay rational. Lattice
   marks of `P` can become non-lattice rational marks of `A P`, for example when `g_h = 2`
   and `x` is odd. Step 2 of the chain routes those to G2, so nothing is lost.
6. **Normalized.** The wall lengths of `A P` are the old lengths divided by `g_h` (or
   `g_v`), so each gcd is 1. Area becomes `n / (g_h g_v)`. Every later hypothesis (R*, the
   area ranges, and d81's `n`) applies to the normalized room. That's how the chain uses
   them.

**Computed (Part A of `mp_check.py`).** The test scales each of 200 saved witness rooms by
`(2, 3)`, which is the inverse direction of normalization. In all 200 cases:

- the scaled witness `(2 D_x, 3 D_y)` ends at the scaled `T` with no corner hit;
- the reflection points are exactly the images of the original reflection points;
- `W` is unchanged, the rooms stay pinch-free, and the wall gcds scale to `(2 g_h, 3 g_v)`.

**Proposed text** (d66 step 1, RESULTS §3.1):

> Normalization: translate a corner to the origin, then scale by `A = diag(1/g_h, 1/g_v)`.
> After the translation every corner lies in `g_h Z × g_v Z`, so `A P` is a lattice room
> with both wall gcds equal to 1. `A` conjugates the reflection in each axis-parallel
> wall to the reflection in the image wall. It maps corners to corners, so lighting paths
> correspond in both directions. `A` preserves `W`, `r`, and strict simplicity, and it
> maps rational points to rational points. Lattice marks may become non-lattice; step 2
> sends those to G2.

## 2. Q08: Lemma MP

**Proof check.** Let `S ≡ T (mod 2)` be lattice points of a lattice room, and `γ` a
lighting path.

1. Every wall lies on a line `x = c` or `y = c` with `c` an integer. The reflection
   `x -> 2c - x` preserves `x mod 2`. So the unfolded endpoint `T*` satisfies
   `T* ≡ T ≡ S (mod 2)`, and `T* - S ∈ 2Z²`. This is the parity of the unfolded
   displacement. It's the step d82 re-checked as `2S + Lv ∈ 2Z²`.
2. Unfolding is an isometry, so the point at half length unfolds to `M* = (S + T*)/2`.
   That point is in `Z²`.
3. Folding back is a composition of reflections in integer lines, so it maps `Z²` to `Z²`.
   The half-length point `M` of `γ` is therefore a lattice point.
4. `γ` avoids every corner, so `M` isn't a convex or reflex corner. A lattice point of the
   room with exactly two cells is a smooth wall point or a pinch, and strict simplicity
   excludes pinches. So `M` is interior or smooth.

**Hypotheses the proof uses.** The statement in d69 says "lattice room". The proof also
needs the following facts, and the project's room definition supplies each of them.

- **Walls on integer lines.** This fails before normalization only if corners are
  non-integer, which a lattice room excludes.
- **No pinch.** In a non-strictly-simple room, `M` can be a pinch point. Add "strictly
  simple" to the statement, or count pinches among the corners a path must avoid.
- **The edge cases are harmless.**
  - `M` can be a smooth wall point at which `γ` reflects. That's allowed.
  - `M` can equal `S` or `T`. That happened in 12 of 200 saved witnesses and in 26 of
    1,089 searched paths, as d83 also notes for non-shortest witnesses. The lemma still
    holds. A downstream use that needs `M ∉ {S, T}` must take a shortest path or argue
    separately.
  - Axis-parallel paths satisfy the same parity argument.

**Computed (`mp_check.py`, exact Fractions, own tracer).**

- **Part A.** 200 random saved witnesses (seed 101) from the 1,461 in
  `d8-perturbation-test/results.jsonl`, from the named R22 and R34 edit families. All 200
  reproduce. All 200 have `D ≡ 0 (mod 2)` and a lattice midpoint. 94 midpoints are
  interior, 106 are smooth, and none is a corner. 0 violations.
- **Part B (non-circular).** R22 and all 29 edits `R22-L1-*`. The search covers 298
  same-class pairs of regular lattice points and every `D` with `max|D_i| ≤ 12`, odd
  components included.
  - It finds 1,089 lighting paths. All have even `D`, and all satisfy MP: 461 midpoints are
    interior and 628 are smooth. 0 violations.
  - Control: 2,098 lighting paths of different-class pairs all have a non-lattice
    midpoint.
  - R22's dark pair `(0,0)-(2,2)` has no path within the bound, as expected.

**Proposed text** (d69 §2 and RESULTS §3.13, first sentence):

> Let `S`, `T` be lattice points of one parity class in a strictly simple lattice room,
> and `γ` a lighting path. Then the point of `γ` at half its length is a lattice point
> that is interior or smooth. It may coincide with `S` or `T`.

Record the status as PROVED (reviewed, d101).

## 3. Q09: d81 residual gaps (findings 5 and 6)

Both concern Proposition P, case `κ = 2, λ = 1`, where the sheets are `[μ]²` with `μ ≥ 5`.
This case is load-bearing for `n ≥ 49`. Product action with `μ ≥ 7` lies in that range,
and z_x ≤ 8 doesn't exclude it without these bullets.

### Finding 5: product relation (line 58)

**Verdict: citation error, no gap.**

- The monodromy tuple of any cover of the four-punctured sphere satisfies
  `g_a g_b g_c g_d = 1` (D0; d14 `proof.md` line 38, "a state is
  `(g_a, g_b, g_c, g_d)` with product 1").
- The map `S_μ wr S_2 -> S_2` that records swap type is a homomorphism to an abelian
  group. So the number of swap-type generators is even, whatever the order of the
  product.
- `G` is primitive, and the base group preserves the row partition. So `G` isn't in the
  base group, and at least one generator, and hence at least two, are swap type.
- check.py covers only the saved rooms with `21 ≤ n ≤ 40`. It can't justify a claim at
  `n ≥ 49`. It's a consistency check only.
- Line 61 uses "the two swap-type generators", which needs "exactly two". That follows
  once `g_x` is shown to be non-swap: an even count ≥ 2 among the 3 other generators
  is 2.

### Finding 6: "z_y ≥ 2μ − 3" against "f + 3z = μ" (line 60)

**Verdict: presentation flaw, no gap.**

- Both statements are true, and together they show that a swap-type generator has no
  3-cycles.
- Swap type with `z ≥ 1` gives `g² = (ab, ba)` with `ab` of order 3. With `t ≥ 1`
  3-cycles in `ab`, `g²` moves `μ² − (μ − 3t)² ≥ 6μ − 9` sheets, so `z ≥ 2μ − 3`.
- Line 59 gives `z ≤ μ/3`. Both bounds can't hold for `μ ≥ 2`.
- The bullet reads as if a swap-type reflex class existed with `z_y ≥ 2μ − 3`. It then
  rules out the swap type for `g_x` separately. The logic is valid, because the case is
  empty. The text should say so directly.
- The conclusions the rest of the proof uses all hold:
  - every reflex class has `z_y ≥ μ`;
  - only class `x` has reflex corners, since `2μ ≥ 10 > 8`;
  - `g_x` is non-swap;
  - the swap-type generators have `z = 0`, so `f = μ`. Line 61 uses this.

**Computed (`swap_check.py`, brute force over all `(a, b) ∈ S_μ²`).**

| μ | Swap-type g with cycle lengths in {1, 2, 3} | f + 3z ≠ μ | Max z (swap) | Least z (non-swap, z ≥ 1) |
| ---: | ---: | ---: | ---: | ---: |
| 5 | 120 | 0 | 0 | 5 = μ |
| 6 | 720 | 0 | 0 | 6 = μ |

Every such swap-type generator is an involution (`b = a^{-1}`), which matches the
argument.

**Other bullets re-checked.** Lines 59, 61, and 62 are correct:

- `g³` is a swap-type involution with μ fixed points.
- In line 61, the `t ≤ 1` bound comes from `tμ ≤ 8`. Also `b = 1`, and `2μ ≤ μ + 4`.
- In line 62, `μ = 5`, `z_x = 7`, `f_x = 4`, and `14 > 11`.

**Effect on the threshold.** None. Prop P's κ = 2 sub-case still yields no product-action
group at `n ≥ 21`. So d81's `n ≥ 49` (primitive row) is unaffected.

### Proposed replacement for d81 README lines 58 and 60

Line 58:

> - Generators of swap type exist, since G is primitive and the base group preserves rows.
>   The swap/non-swap map S_μ wr S_2 → S_2 is a homomorphism, and g_a g_b g_c g_d = 1
>   (Dictionary D0). So the number of swap-type generators is even, hence at least 2.
>   (check.py confirms a product relation in all 2,145 saved rooms. That's a consistency
>   check, not the justification.)

Line 60:

> - A swap-type generator has no 3-cycles. If z ≥ 1, then g² = (ab, ba) with ab of order 3,
>   so g² moves at least μ² − (μ − 3)² sheets and z ≥ 2μ − 3. This contradicts
>   z ≤ μ/3 from the previous bullet. So every reflex class y has non-swap g_y, and d14
>   step 4 gives z_y ≥ μ. Two reflex classes would need r ≥ 2μ ≥ 10, so only class x has
>   reflex corners. In particular g_x is non-swap, so exactly two generators are swap
>   type, and each has f = μ by the previous bullet.

Line 61 can then drop "have z = 0" and cite the bullet above for "each fixes μ sheets".
