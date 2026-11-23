# D113: review of qclass-closure/bbbb/general-gluing.md

Date: 2026-11-20. Reviewer: independent referee. All computation is exact
(`fractions.Fraction`), Python with `-B`, under 5 CPU-seconds in total. Only
named rooms are used: the note's 20-wall room (called DBay here), its
corridor-lengthened copies at L = 4 + 66k, the odd crosses P_7, P_9 and P_41,
and DBas as a detector control. The tracer in `geo.py` is new code. The d103
unfolded cell tracer replays every reported path and door hit. No room, word
or direction search was run. Every slope traced is a listed constant or a root
of one of the note's formulas.

## Verdicts

| Claim | Verdict |
| --- | --- |
| 1. Upward jump at s₀ = 43/33 | Correct. All numbers check exactly. The pair is lit anyway, by 4 of the 12 candidate rays traced. |
| 2. Persistence at L = 4 + 66k | Correct as stated. It has no darkness content: from k = 3 on, the same two branches carry single-traversal roots at the neighbouring even values. |
| 3. Odd crosses break the dichotomy | Correct for P_7 and P_9, and for P_41 as an extra member. |
| 4. Compact covering problem | The counts and the bound of 20 variables are correct. It's a template with three unfixed inputs, not one precise problem. |
| 5. Scope | Stated accurately. One sentence about L = 4 lighting is cited, not checked here. |

## Claim 1: the upward jump

**Room** (`jump.py`, `jump.log`). The cells are
[0,5]×[0,4] ∪ [1,3]×[4,48] ∪ [1,3]×[−3,0] ∪ [5,9]×[1,2] ∪ [9,13]×[−1,5].
The boundary is one cycle with no pinch, so the room is strictly simple.

- W = 20 and r = 8. The reflex corners are (1,0), (3,0), (5,1), (9,1),
  (9,2), (5,2), (3,4) and (1,4).
- The area is 142. The wall gcd is 1 on both axes.
- Each parity class has interior points: 32, 31, 5 and 6 of them. So no class
  is corner-only.
- The area exceeds 8r = 64, so d69 makes the room BBBB.
- S = (2,47) and T = (10,3) are interior points. Both have parity (0,1).

**Mismatch.** I re-derived the gluing condition from scratch. Take the
forward unfolded height with the ray going down. Matching at x = 9 gives
h_A + h_B − 4s ∈ 2ℤ, which is F = 4s + f_A + f_B ∈ 2ℤ with the note's signs.
Every intermediate value checks by hand:

- the hit at x = 0 at height 3/33;
- the floor hit at 3/43 and the top hit at 135/43, both outside the bays;
- the door heights 52/33 and 46/33;
- the travels 41 and 35;
- y_A = 55 − 41s and y_A = 47 − 35s;
- f_B = s − 2.

The two branches give F = 46s − 56 and F = 40s − 48. Their limits at s₀ are
130/33 and 136/33, which straddle 132/33 = 4. Their roots, 30/23 and 13/10,
each lie on the wrong side of s₀.

**Exact trace.** At s₀ the source ray hits the vertex (3,4). I traced 7
offsets ε on each side, from 1/100 to 10⁻⁹. The traced F equalled the branch
formula exactly in all 14 cases. Both door hits were in (1,2), with downward
sign on the source leg. The source ray makes 20 bounces below s₀ and 16 above.
On a grid of step 1/3300, the formulas hold for 34 steps below s₀ and 37
steps above. That gives branch widths of about 0.0103 and 0.0112.

At s₀ ∓ 1/10000 the trace reproduces the note's d109 numbers exactly:

- door heights 521353/330000 and 91769/66000;
- F = 649241/165000 and 34033/8250.

The d103 tracer, given developed displacements of 41 and 35, ends at x = 5 at
the same two heights.

**Is the pair lit?** Yes. I traced only the six branch-formula roots for
F = 2, 4 and 6, each with the source launched down-right and up-right. That
is 12 rays. Four reach T, and d103 replays each one exactly:

| Slope | Launch | Bounces | Crossings of x = 5 |
| --- | --- | --- | --- |
| 13/10 | down | 227 | 3 |
| 31/23 | up | 26 | 1 |
| 5/4 | up | 62 | 1 |
| 27/20 | up | 109 | 3 |

The rest hit corners, or don't reach T within 5,000 bounces. The note never
claims the pair is dark, so this doesn't contradict it. It does show that
first-door monotonicity fails for a pair that is lit.

## Claim 2: large L

For k = 1, 3, 10 and 30, the room keeps W = 20 and r = 8, with no corner-only
class. Moving T to (10 + 66k, 3) keeps its parity. The limits are
130/33 + 86k and 136/33 + 86k. They straddle 4 + 86k, and the traced F at
s₀ ± 10⁻⁶ agrees.

In general the roots for 4 + 86k are (60 + 86k)/(46 + 66k), which is above
s₀, and (52 + 86k)/(40 + 66k), which is below. Cross-multiplying against 43/33
shows this for every k ≥ 0. So the jump persists at every length.

That persistence is weak, though. Each branch has fixed width near 0.01,
while dF/ds grows like L. So at large L, the same two branches cross the
neighbouring even values 2 + 86k and 6 + 86k. The traces confirm this:

| k | Branch | Slope | Result |
| --- | --- | --- | --- |
| 1 | above, F = 92 | 71/53 | Lit, multi-traversal (5 crossings) |
| 3 | below, F = 260 | 79/61 | Lit, single traversal |
| 10 | both | 459/353, 229/175 | Lit, single traversal |
| 30 | both | 1319/1013, 659/505 | Lit, single traversal |

d103 replays all of them. At k = 1 the below-branch slope hits the corner
(3,0), and at k = 3 the above-branch slope hits (1,0).

A jump in a single leg's phase is less than 2w, because f ∈ (−w, w). So an
upward jump skips at most one even value, or two if both legs jump together.
A counting variant of the d112 argument could therefore work: if a slope
window's range holds more even values than there are upward jumps, F crosses
one of them inside a regular piece. That would need a bound on the number of
lip thresholds per window, and I haven't proved one. This remark is a
suggestion, not a result.

## Claim 3: the odd crosses

From `cross.py` and `cross.log`:

| Room | W | r | Area | gcd x/y | Gaps | Ratio |
| --- | --- | --- | --- | --- | --- | --- |
| P_7 | 12 | 4 | 96 | 1/1 | 5, 4, 5 | 5/4 |
| P_9 | 12 | 4 | 128 | 1/1 | 7, 4, 7 | 7/4 |
| P_41 | 12 | 4 | 640 | 1/1 | 39, 4, 39 | 39/4 |

- The gaps are the same on both axes.
- Every class has interior points, and the area exceeds 8r = 32, so all three
  rooms are BBBB.
- After normalizing, the middle gap is 2/b, which tends to 0. So no
  ε-thick chart contains the family.

The corridor detector checks every rectangle whose four corners are reflex
vertices. For a genuine corridor, the two mouths must be open and the two
long sides must be walls. In every cross the only candidate is the hub
[−2,2]², on both axes. Its mouths are open, but its long sides are interior,
so it isn't a corridor. The arms end in walls, so they are capped arms. As a
control, the detector finds DBas's corridor [5,9]×[1,2] and nothing else.

I checked the wider artificial-cut convention, L/d ≤ 1, by hand from the
three constant-run ranges. It holds.

## Claim 4: the compact covering problem

The arithmetic checks (`count.py`, `count.log`):

- With m ≤ 10 vertical and m ≤ 10 horizontal edges, the free coordinates
  number (v − 2) + (h − 2) + 4 ≤ 20.
- Σ_{m=2}^{10} m^{2m}(m−1)⁴ = 6.567 × 10²³. Most of that is the m = 10 term,
  6.561 × 10²³.
- The word count equals a direct count of words with no immediate repeat.
- Independent axis scalings are legitimate. A diagonal map commutes with both
  reflections, so it preserves lit and dark pairs. This note scales each side
  to one, while thick-thin.md normalizes only the larger side. Both are valid,
  but the two files differ.

It isn't a single precise problem:

- It doesn't fix ε, the word bound B, or how marks near the boundary are
  handled. On marks, it offers two alternatives: distance bounds or
  endpoint certificates.
- It doesn't define "legal unfolded word domain" in the note. One reading
  works: distinct marks, an unfolded segment that misses every vertex image,
  and open mouths respected.
- It covers every real room in the chart, not only lattice rooms. A real
  W ≤ 20 room with a dark pair would make it fail even if the lattice target
  is true.

The note concedes all of this. With ε fixed, the problem covers only a thick
part, and claim 3 shows the complement isn't compact. So it's a correct
conditional template.

## Claim 5: scope

**Killed:**

- the no-upward-jump proof of first-door monotonicity for one fixed launch in
  non-rectangular chambers, including the developed-travel version;
- the claimed dichotomy between bounded gap ratios and a two-mouth corridor
  with large L/d, for every c;
- any whole-core computation sized from that dichotomy.

**Left open:**

- aggregate, counting or min/max arguments over launches (see the remark
  under claim 2);
- a replacement compactification that handles capped arms and junctions;
- the BBBB r ≤ 8 core itself.

Nothing here produces a dark pair. The note's claim that the L = 4 room is
fully lit by the one-cylinder theorem is cited, not checked.

## Re-run

From `d113-review-general/`:

```
python3 -B jump.py  > jump.log    # claims 1-2 (uses ../d103-twenty-check/tracer.py)
python3 -B cross.py > cross.log   # claim 3
python3 -B count.py > count.log   # claim 4
```
