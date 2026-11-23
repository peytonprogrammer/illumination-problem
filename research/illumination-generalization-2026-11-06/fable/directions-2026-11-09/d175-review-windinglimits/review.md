# Review: winding-limit notes (snapshots 2026-11-22 1652)

This review covers `cap-character-lock`, `simultaneous-strip-misses`, and `per-gate-rank-one`.

**Bottom line.** The arithmetic in all three notes is correct. The combined claim is only half right.

- Every lit 10-wall pair the notes name fails the **common-strip** construction (d173 with uniform δ = w) on both axes and with every cap choice.
- Every one of those pairs is also lit by a **single-pass path in the same k = 0 chart**. That path stays inside the full per-gate windows but leaves the common strip.
- So the failure belongs to the uniform-δ strip, not to "fixed chart plus windings". Note 3's own exact per-gate test certifies all of these pairs.
- The one pair that fails the per-gate test (note 3, η = √2/10) has no lighting proof in any note. It could be lit or dark.

Checks: `checks.py`, output in `checks.log`. Result: 86 PASS, 0 FAIL, 62 CPU-seconds, `python3 -B`, exact `Fraction` arithmetic. `trace()` and `Room` are copied verbatim from d174, which copied them from d170 and d171. The per-pair check enumerates every primitive direction with max(|p|,|q|) ≤ 60, plus the 4 axis directions, with ≤ 60 reflections. It tests whether the path passes T before it reaches any vertex. The verbatim `trace()` replays every first hit and ends exactly at T. Only the named rooms and pairs were checked. No room search and no network were used.

## 1. cap-character-lock — sound with gaps

**Verified.**

- The four rotations are (A,B), (C−A,B), (A,E−B), (C−A,E−B). The source cap 2c − a maps A to C − A. If A and C are integers, (1,0) annihilates all four rotations (2,000 random B and E values).
- On the staircase grid (0,1,2,3,N) with N = 5, 6, 7, these values hold: P = 12, A = 6, C = 12(N−3). The room equals its transpose, so both axes carry the same relations. The d170 comparisons read 2 ≤ 2 and 6 ≤ 9.
- S = (1/2,4) and T = (4,1/2) are **lit** in all three rooms. The direction is (−1,−1), with 2 reflections: one on the left wall and one on the floor.
- The named-controls table matches: (P,C) for U1, U2, U2b, and T1 in both orientations. Each a = 2w/P is interior. The largest pure source character is 3.

**Gaps.**

1. **Medium.** The "unit character survives" point is vacuous as an obstruction. With δ = w, the source phase half-width is ε₁ = 1/2. A (1,0) relation then never blocks the rank-one test. This repeats d173 review gap 5. The note's real evidence is the inhomogeneous projection, and the note doesn't compute it.
2. **Medium.** The note misses its strongest case. For N = 6 the terminal lattice is 6ℤ and dist(4, 6ℤ) = 2 > w = 1. That holds for direct and floor travel and, by symmetry, on both axes. So the d173 chart test **fails strictly** on a lit 10-wall pair. For N = 5 and 7 the lattice is 2ℤ, and the test passes.
3. **Low.** The pyramid-761 paragraph, the "6H clearance" Cramer bound, and the smallest-OPEN-word line weren't re-run. The determinant argument (every term ≤ 1·H·1, six terms) is correct by inspection.

## 2. simultaneous-strip-misses — sound (narrow scope)

**Verified.** For V1, V2, and the family with m,n ∈ {1,2}, dist(z, PBℤ + 2Wℤ) exceeds w for direct and cap travel on both axes. The values match the note's table. Margins are V1 5 and 4, V2 4 and 4, and the family 13 and 7. All marks are interior.

**Are the pairs lit? Yes, all six.** First hits:

| Room | First direction | Reflections |
|---|---|---|
| V1 | (−1,3) | 38 |
| V2 | (−6,−7) | 13 |
| Family, each of the four members | (−1,−1) | 7 |

Single-pass lighting paths, monotone with caps only at the ends, exist on both axes for every pair. The y-chart and x-chart counts are V1 10 and 10, V2 35 and 27, and the family 12 and 20.

**Gaps.**

1. **Medium.** "Strengthens to an inhomogeneous obstruction" is true only for the uniform-δ common strip. That construction was already known to discard the wider deep windows (d173 review gap 3). The note states this caveat itself. Its headline should carry the caveat too.
2. **Low.** The last section restates the d174 lcm subsumption. That's correct, but it's unrelated to the title.

## 3. per-gate-rank-one — sound with gaps

**Verified.**

- **Per-gate test.** The test (K meets Θ + D(ℤ² + ℤα)) follows from affine interpolation, as in d173.
- **Helly witness bound.** The Helly numbers for ℝ², ℝ×ℤ, and ℤ² are 3, 4, and 4. That gives "at most four gate constraints" per chart and per lift. The bound 4 is attained: the check builds four open half-planes in ℤ² with no 3-subset witness.
- **Extrapolation envelope.** The envelope |Z| ≤ v + B(w+v)/(d+e) holds and ignores the middle gate.
- **Strict misses.** With 5 | m and 3 | n, the misses are strict on both axes:

  | Axis | Envelope | Required distance |
  |---|---|---|
  | Original | 8.5 / 22.5 | 15 − η / 75 − η |
  | Transposed | 23/3 / 13 | 10 − η / 30 − η |

  This was checked for (m,n) = (5,3), (10,6), (5,6), and (15,3).
- **Divisibility hypotheses.** Both are needed. Without 5 | m, the cap lattice drops to 30ℤ and 15 < 22.5. Without 3 | n, it drops to 20ℤ and 10 < 13.
- **Rank one.** The source depth 25 + η is irrational and b = 1 is rational, so the relation group is rank one.

**Gaps.**

1. **High.** Nobody shows that the note's pair (1, 30+η)–(75+η, 2) is lit. If it's dark, it's a smaller dark room than R22. If it's lit, the conclusion "R22's equality is not diagnostic" needs that proof. With η irrational and W = 450, the bounded exact check doesn't apply. Logically, "strict failure exists" shows only that failure doesn't imply equality. It doesn't show that equality fails to separate dark pairs from lit ones.
2. **Medium.** "At most four" holds per signed chart, lift, and winding progression. The union over infinitely many relative middle windings and itineraries has no finite witness, and that union is where the open question lives. The note says this, but the verdict line reads stronger than the result.
3. **Low.** For lattice data (rank two) the per-gate test is a finite orbit check. That is the case relevant to the ledger, and the irrational η example doesn't model it.

## 4. Assessment (key)

**Do the notes show that a fixed-chart + common-strip + windings family can't prove W ≤ 20?**

- **For the common-strip (uniform δ) family: yes.** Stair6 and the six item-2 pairs are lit 10-wall pairs that the family misses on both axes, with all caps.
- **For the same chart with full per-gate windows: no.** Every one of those pairs is lit inside that family.

**The lighting mechanism is a sloping reference line in the k = 0 chart.** The middle gates sit in their base copies, the line crosses every gate inside its own full window, and the end that uses the terminal cap lies far outside the strip. No itinerary change and no different band decomposition is needed. Developed data from `checks.log` item 4b:

| Pair | Slope | Gate offsets | Windows | Source lift | Terminal |
|---|---|---|---|---|---|
| Stair6 | −1 | −1/2, −3/2, −5/2 | 1, 2, 3 | 1/2 | −4 (floor cap) |
| V1 | 23/19 | −186/95, −71/95, 44/95 | 2, 3, 5 | −34/5 (source cap, winding −2) | 7 (floor cap) |
| V2 | −4/7 | 1/7, −1, −11/7 | 1, 2, 3 | 5/7 | −5 (floor cap) |
| Family | 7/3 | −4/3, 1, 10/3 | 2, 3, 5 | −13 (winding −3) | 15 (floor cap) |

In the d173 language this is an **asymmetric endpoint correction**: the terminal error far exceeds δ, while the gates still clear. It's the d170 / d174 (A) floor-return mechanism. The shortest lighting paths found first (V1 with 38 reflections, the family with 7) turn back at inner steps. Single-pass alternatives always exist, so turn-backs aren't required here.

**What remains open.** No note exhibits a lit pair that fails the *full-window* per-gate test in every chart. Note 3's η-pair is the only candidate, and its lit status is unknown. Until it's decided, the per-gate framework with full windows hasn't been shown inadequate at W ≤ 20.

## Verdicts

| Note | Verdict |
|---|---|
| cap-character-lock | Sound with gaps: 2 medium, 1 low |
| simultaneous-strip-misses | Sound for its stated construction: 1 medium, 1 low |
| per-gate-rank-one | Sound with gaps: 1 high, 1 medium, 1 low |

No ledger status changes.
