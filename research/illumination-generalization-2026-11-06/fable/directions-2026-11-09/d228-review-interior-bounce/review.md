# D228 review: interior bounces, interval chains and the sign cone

Date: 2026-11-23. Reviewer: Opus, independent. Note under review:
[note-snapshot.md](note-snapshot.md). Checks: [checks.py](checks.py), output
[checks.log](checks.log): 40 PASS, 0 FAIL, 0.67 CPU-seconds at `nice -n 10`.
The exact `Fraction` tracer, R22 and the six-reflex builder are imported from
[../d227-review-pinned-pairs/checks.py](../d227-review-pinned-pairs/checks.py).
The interval-chain test, the sign-cone rules and the note's sufficiency
construction are new code in this directory.

## Verdict

Every claim holds. The two theorems are correct reformulations, and the
brute-force test found no counterexample to the three cut rules. R22 behaves
exactly as the note says. Its single excursion turns at the corner (1, 2), and
none of the 20 traced count and winding combinations reaches T. The note
closes no new case. The six-reflex closure was already shown in d227.

| Claim | Verdict |
| --- | --- |
| 1. q = s − Hα, one- and two-reflection formulas | CORRECT |
| 2. Interval-chain theorem | CORRECT WITH GAPS (definitional) |
| 3. Six-reflex closure table, all t > 0 | CORRECT (traced m = 1, 2, 5) |
| 4. Three-cut sign-cone theorem | CORRECT |
| 5. Simultaneous clearance and residual | CORRECT (residual is a restatement) |
| 6. R22: in the cone, zero clearance | CORRECT; no positive-clearance combination found |

## Claim 1: displacement formulas — CORRECT

- The developed line gives X − (X₀ + Kα) = (K/H)(s − Hα) exactly.
- The one-reflection values −2(U−D)α and (−2V)(1−α) hold. Only one leg of
  each itinerary lies in 0 < y < D, so "throughout" is accurate.
- The up–down–up table holds for U < D and for U > D, with H = D + 2L. In
  travel order the signs run minus, then one zero at α = U/(D+L) on the
  descent, then plus. For U = 3, V = 1 and D = 4 the sequence is
  (−,−,−,−,0,+,+,+).
- The down–up variant gives H = 2(U−V) − D, and q = −2V − (H−D)α on the middle
  leg.
- A single turn at 0 < U < D can't reach D, because no later vertical
  reversal exists.

This review doesn't re-derive the identification of q with the unfolded
offset μ at a graze. That rests on d226 claim 4.

## Claim 2: interval-chain theorem — CORRECT WITH GAPS

Necessity is evaluation of X at each visit. Sufficiency holds when every piece
of the chain is a rectangle. Within a rectangle the side walls span the full
slab height, so a developed strip of reflected copies is convex. A leg's
interior stays strictly between the two levels. Every side hit is therefore
transverse and away from corners, because visit points lie in open intervals
inside a single copy. A horizontal turn doesn't change X, so legs glue
consistently.

I looked for counterexamples:

- **Side-wall hit at a horizontal level.** This needs X at a copy boundary at
  a visit. Open intervals inside one copy exclude it.
- **Turn face versus overlap.** At R22 y = 2, x = 2 lies in the overlap
  (1, 3). The code rejects a planned roof turn there and accepts a
  transmission.
- **Exact corners.** Zero clearance is rejected, as the note requires.

The theorem agreed with the tracer on nine chains:

- Six-reflex m = 1 with k = 0–5 middle excursions. k = 1, 2, 3 pass with
  clearances t/2, t/3 and t/4. k = 0 and k = 4 fail with zero clearance at
  the corner (t, t). k = 5 fails because the floor visit lands in an opening.
- Three R22 chains, below.

The gaps are definitional:

1. Sufficiency needs every component to be a rectangle. Components between
   consecutive vertex levels are rectangles, and so are unions joined across
   artificial cuts with the same x-range. The note's "tier" should be pinned
   to that meaning. An L-shaped "tier" would break convexity.
2. For a fixed chain and winding, K and H are both fixed. The "iff" is
   therefore a membership test for one number, not a range of slopes. The
   note's sentence on varying target images covers this.

## Claim 3: six-reflex table — CORRECT

For m = 1, 2 and 5 (t = 11, 21, 51) the checks confirm the following:

- The visits fall at s = t, 3t, 5t, 7t and x = t/2, 3t/2, 5t/2, 7t/2.
- The intervals are (0, t), (0, 3t), (t, 4t) and (3t, 4t), computed from the
  room.
- T lies in the upper component (3t, 6t).
- The minimum clearance is t/2, and the shifts are −t/2 and +t/2.
- The tracer's direction (1, 2) reaches T with reflections exactly at
  (3t/2, 3t) and (5t/2, t), and no vertical wall is touched.

All visited faces are multiples of t, and m enters only the end tiers, which
this route doesn't visit. So the strict inequalities hold for every t > 0.
This is the d227 witness, and the note credits it.

## Claim 4: sign-cone theorem — CORRECT

- The shift formula qᵢ = Σ_{cⱼ<i} hⱼ − αᵢE reproduces the traced (1, 3)
  crossings t/3 and 11t/3. That route has two excursions at cut 1.
- **Random instances.** I tested 600 instances: p ≤ 3, α ∈ {k/12}, random
  available cuts, one or two quanta per cut from {1, 2, 3, 4, 6}, and random
  demands.
  - Necessity: none of the 335 rule-violating instances has integer counts
    with per-cut totals ≤ 12.
  - Sufficiency: the note's run construction, with counts floor(Mw/λ) and M
    doubling, produced valid counts on all 265 rule-satisfying instances. The
    bounded search alone found 259. The other six need totals above 12.
- **Exhaustive cases.** For p ≤ 4 with equally spaced α, I checked every cut
  set and demand, 680 cases in all. The rules hold if and only if counts
  exist.
- The note's examples hold. (−,+,−) needs cut 1 and cut p, and (+,−) needs no
  internal cut.

The proof is complete. Within a run the demand is a plus prefix and a minus
suffix. The run intervals are ordered, so strictly increasing constants
exist. The integer step is a limit argument with finitely many strict
inequalities. One scope condition stays implicit: delays must not change the
transverse image K. Roof and floor turns satisfy it. Side hits whose copy
chain changes with the counts are left to claim 5, as the note says.

## Claim 5: clearance and residual — CORRECT

- The visit times s₀ + (2h−1)L, s₀ + 2hL and s₀ + (2m+1)L check out for
  m = 1, 2, 4.
- The expression min{Ks − H(l − X₀), H(u − X₀) − Ks}/H equals min(X − l,
  u − X), so strict positivity is the chain test.
- The first-and-last-hit shortcut follows from monotone X on one developed
  interval.

The residual is a restatement of "no itinerary in this move set". The clause
"failure of a cut rule" is redundant. A cut-rule failure already makes every
count fail clearance. The statement isn't wrong, but it isn't a reduction.

## Claim 6: R22 — CORRECT; no positive-clearance combination

- The slab 1 < y < 2 is (0, 4). Its roof is exposed over (0, 1) and (3, 4),
  and its floor over (1, 3).
- The single excursion has H = 4. It crosses y = 1 at x = 1/2 and turns at
  the roof at s = 2, x = 1, which is the corner (1, 2). The clearance is
  exactly 0, and the tracer dies at (1, 2).
- The target-end delay with E = 2 also crosses y = 2 at x = 1. Two excursions
  (E = 4) reach the floor at x = 1, the corner (1, 1).
- In the direct winding, one excursion needs 4 < H < 6, but H = 2 + E is
  even. The failure is an exact lattice coincidence.
- **Traced combinations.** I traced 20 hand-chosen directions (K, ±H):
  - Direct winding with E = 0, 2, 4, 6, 8, 10, 12, starting up or down.
  - Target images reflected in x = 0, x = 3, x = 4 and x = −1.
  - Result: 18 die at corners, and (2, ±8) reach the 400-reflection cap.
    None reaches T, so R22 darkness is not contradicted.
- The single minus demand with cut p available is in the sign cone. So R22
  separates the cone from legal paths, as stated.

## Which lemma advanced

**L1**, pinned-pair route. The note supplies a correct calculus for one move
set: exact visit displacements, an interval-chain test, the cut rules for
strict sign vectors, and simultaneous clearance. R22 is a control that the
cone alone can't certify lighting. No new pair is closed. The six-reflex
closure repeats d227, and no darkness or B(r) bound follows.

## First case still open

Take a nondirect pinned pair with at most eight reflexes whose demand lies in
the sign cone. The open case is when every count vector at every winding
fails clearance, and no itinerary outside slab excursions is known. R22 shows
the likely mechanism at nine reflexes. Integer quanta make H even, and the
turn abscissas 2s/H land exactly on corner abscissas. So the first concrete
test is an eight-reflex pinned pair whose only excursion slab has
turn-face endpoints at the lattice abscissas 2s/H for every admissible H. I
know no such example, and none was searched for here.
