# d235 review: two-list closure note, sections A and B

Reviewer: independent Opus subagent, 2026-11-25. Scope: sections A and B of note-snapshot.md, plus a check that the closing two paragraphs don't overstate them. The column model of d233 is taken as given. I found no conflict with it, and the room tracer agrees with it at every point.

## Verdicts

- **Section A: ACCEPT.** Every step checks by hand, with strict margins of at least 1 at all three gates. The exact room trace hits for m = 2 to 10, 16 and 20 with zero vertical reflections.
- **Section B: ACCEPT WITH CORRECTIONS (wording only).** The proof is correct under its stated hypotheses. Make two edits:
  1. Replace "In particular it applies throughout the tested displaced-target subfamily" with a named family: "In particular it covers the target-one-below-the-roof family, N = 64m², levels (-(m+2), 0, 1, m+1, 2m+2, 2m+3), for every m ≥ 3." The bare phrase is ambiguous. In d234/rotation-sketch.md, "displaced target" means the abscissa shift e = 3N/2 - 1, where B's identity fails and B says nothing. B also needs m ≥ 3 in this family, because c = 0 there.
  2. Replace "let N be any positive even integer" with "let N be a positive even integer". Then add: "The displayed condition forces N ≥ 20, so N/2 - 1 ≥ 9 and the supports are strictly ordered." The reason: g = gcd(m, 2H) divides m, so 3mH/g ≥ 3H ≥ 3(m+2) ≥ 15, which gives X > 30. The proof is already correct without this sentence. It closes a question a reader will ask.
- **Closing paragraphs:** they don't overstate A or B. The identity 3(a+b) = 2X + a is equivalent to b = 2(d+e), and the displaced-abscissa example has e = 3N/2 - 1, so b ≠ 2(d+e). I checked both. One nit: the letter `a` there is a column travel, not B's depth a. Consider renaming it.

## Hand check, section A

Setup: N = 64m², X = 96m² + 1, levels y0..y5 = (-(m+2), 0, 1, m+1, m+2, 2m+3). The columns are [y0,y3], [1, m+1], [1, 2m+3] and [m+1, 2m+3], with widths 1, N, 1 and 32m² - 1.

1. **Progression.** K = 3mj + m with j ∈ 2(m+2)ℤ≥0 has K-step 6m(m+2). The spacing 6m(m+2)/X < 1/8 is equivalent to 48m² - 96m + 1 > 0, which holds for m ≥ 2 and fails for m = 1. The bound is tight at m = 2: 48/385 = 0.12468.
2. **Nearest member.** The first member m/X lies below m/2 + 1, and the progression is unbounded above. So the nearest member has j ≥ 0 and |s - (m/2+1)| ≤ spacing/2 < 1/16. At m = 2 the nearest member equals the aim exactly (K = 770, s = 2).
3. **Identity.** 2X = 3N + 2, so 3(N+1) = 2X + 1. Then (N+1)s = 2K/3 + s/3 = 2mj + (2m+s)/3.
4. **Crossings.**
   - The first crossing is s ∈ (m/2 + 15/16, m/2 + 17/16), inside (1, m+1). It stays below the column 1 roof m+1, so column 1 has no turn.
   - The second crossing is (2m+s)/3 = 5m/6 + 1/3 ± 1/48. Its distance to 1 is at least 5m/6 - 2/3 - 1/48 > 0.97, and its distance to m+1 is at least m/6 + 2/3 - 1/48 > 0.97.
   - The third crossing is (4m+4)/3 ± 1/12. Its distance to m+1 is at least (m+1)/3 - 1/12 ≥ 0.91, and it lies below 2m+3, so column 3 has no turn.
   - No crossing can land on a gate endpoint.
5. **Middle column.** Column 2 has height m. The developed position goes from s - 1 to 2mj + (2m+s)/3 - 1, and both ends lie in (0, m). That gives exactly 2j wall hits, that is, j full periods, and the leg arrives moving up. The trace's turn counts agree: 2j hits.
6. **Fold.** The total developed ordinate is sX - 2mj = mj + m ≡ m (mod 2(m+2)). Column 4 has floor m+1 and period 2(m+2), and m reflects to m+2 = y4. The ray reaches the target moving down, which is the negative offset, as the note says.
7. **Corners.**
   - The wall hits in columns 2 and 4 lie on the open floor and roof segments, which are straight walls.
   - A wall hit at a column boundary would need a crossing at a gate endpoint, which step 4 excludes.
   - A lattice point strictly inside an open gate is an interior point of the room. At m = 2 the chord passes (2N, 2) and (2N+1, 4), and the tracer reports no corner there.

Hypotheses A uses: m an integer, m ≥ 2. Only the spacing bound uses m ≥ 2. A is the case t = 1, H = m+2, a = m+2 of B's level pattern, but A reaches m = 2 because it aims at m/2 + 1 instead of m + 1/2.

## Hand check, section B

Levels: (-a, 0, 1, m+1, m+1+t, m+1+H). Set c = m+1-t, K = 3mj + c and g = gcd(m, 2H), with j ∈ (2H/g)ℤ≥0.

1. **Spacing.** The spacing 6mH/(gX) is less than 1 exactly when the displayed condition holds. The first member c/X ≤ m < m + 1/2, so the nearest member has j ≥ 0 and |s - (m + 1/2)| < 1/2, that is, m < s < m+1, strictly.
2. **Gate 1.** 1 < m < s < m+1, and the column 1 roof m+1 lies above s, so there's no turn. The depth a is never used.
3. **Gate 2.** The second crossing is (2c+s)/3.
   - Lower bound: 2c + s > 3 needs c ≥ 0 and s > 3. That second fact uses m ≥ 3 when c = 0. If c ≥ 1, m ≥ 2 suffices.
   - Upper bound: (2c+s)/3 < (3m+1)/3 < m+1 uses c ≤ m, that is, t ≥ 1.
4. **Gate 3.** The third crossing is (2c+4s)/3.
   - Lower bound: (2c+4s)/3 > 4m/3 ≥ m+1 uses m ≥ 3, again only for small c.
   - Upper bound: (2c+4s)/3 < 2m + 4/3. This lies below m+1+H as soon as H ≥ m+1.
   - H ≥ m+2 is used only to keep y4 < y5 when t = m+1. It's sufficient, slightly more than gate 3 needs.
5. **Fold.** The developed endpoint is mj + c. Because 2H/g divides j, 2H divides mj. Column 4 has floor m+1 and period 2H, and c reflects to 2(m+1) - c = y4. Correct for c = 0 too.
6. **Chart.** 5N/2 must be an integer, so N must be even. As computed under correction 2, the condition forces N ≥ 20, so the chart is non-degenerate. "Positive" alone would not exclude N = 2, which has a zero-width last column, but the condition does.

Exact hypotheses B uses: integers m ≥ 3, H ≥ m+2, 1 ≤ t ≤ m+1, a ≥ 1, N even, and 3mH/gcd(m, 2H) < X/2. The proof uses m ≥ 3 only at gates 2 and 3, and it can be relaxed to m ≥ 2 when t ≤ m. I didn't adopt that as a claim.

## Numerical check

Script: `review_check.py`. It contains my own column fold, kept independent of scan_general.py. It also calls d234's exact cell tracer `trace` on the real tier room, with direction (X, K) from (N-1, 0) to (5N/2, y4). Predictions are in `predictions.txt` and were written before the run.

To re-run it:

```
cd .context/illumination-generalization-2026-11-06/fable/directions-2026-11-09/d235-review-two-list-closure
python3 review_check.py
```

Total CPU: 7.7 s. The full output is in `review_check.out`. Summary (trace result = (status, vertical reflections, horizontal reflections)):

| Point | Parameters | K / X | Column fold | Room trace |
|---|---|---|---|---|
| A m=2 | N=256 | 770/385 | ok, forms match | HIT, 0, 319 |
| A m=3 | N=576 | 2163/865 | ok, forms match | HIT, 0, 623 |
| A m=4 | N=1024 | 4612/1537 | ok, forms match | HIT, 0, 1023 |
| A m=5 | N=1600 | 8405/2401 | ok, forms match | HIT, 0, 1519 |
| A m=6 | N=2304 | 13830/3457 | ok, forms match | HIT, 0, 2111 |
| A m=7 | N=3136 | 21175/4705 | ok, forms match | HIT, 0, 2799 |
| A m=8 | N=4096 | 30728/6145 | ok, forms match | HIT, 0, 3583 |
| A m=9 | N=5184 | 42777/7777 | ok, forms match | HIT, 0, 4463 |
| A m=10 | N=6400 | 57610/9601 | ok, forms match | HIT, 0, 5439 |
| A m=16 | N=16384 | 221200/24577 | ok, forms match | HIT, 0, 13311 |
| A m=20 | N=25600 | 422420/38401 | ok, forms match | HIT, 0, 20479 |
| A m=2, K+1 (control) | N=256 | 771/385 | ends on a wall level, not y4 | MAXSTEPS (no hit) |
| B1, target one below roof | m=3, N=576, a=5, t=4, H=5 (c=0) | 3060/865 | ok | HIT, 0, 883 |
| B2, t=1, minimal N | m=3, N=60, a=1, H=5 | 363/91 | ok | HIT, 0, 103 |
| B3, c=0, even m, minimal N | m=4, N=24, a=2, t=5, H=6 | 180/37 | ok | HIT, 0, 39 |
| B4, t=1, g=3, minimal N | m=9, N=144, a=1, H=12 | 2169/217 | ok | HIT, 0, 219 |
| B5, H=m+2, minimal N | m=5, N=140, a=3, t=3, H=7 | 1263/211 | ok | HIT, 0, 227 |
| B6, large H, minimal N | m=6, N=240, a=10, t=3, H=20 | 2524/361 | ok | HIT, 0, 321 |
| B7, target one below roof | m=7, N=3136, a=9, t=8, H=9 (c=0) | 35154/4705 | ok | HIT, 0, 4649 |
| B8, outside B (m=2, c=0) | N=256, a=4, t=3, H=4 | 960/385 | gate 2 fails (crosses at 90/77, moving down) | HIT, 0, 399 |

At B2 to B6, the condition fails at N - 2, so these points sit on the edge of the condition. Every closed form s, (2c+s)/3, (2c+4s)/3 matches the fold exactly.

Prediction score: 19 of 20 held. B8 missed: I predicted no hit, and the trace hit.

## Surprises

- **B8.** At m = 2, c = 0, B's recipe breaks the note's argument. The second developed ordinate s/3 lies below the floor 1, so the ray crosses gate 2 moving down at 2 - s/3. It then bounces once off the column 3 floor and still lights the target, with no vertical reflection. This is a different itinerary from the one the proof describes, so it isn't evidence for B at m = 2. It does suggest that a sign-flexible version of the argument might cover the target-one-below-the-roof family at m = 2. That's a guess, and I didn't test it.
- **A at m = 2.** The nearest member equals the aim exactly (s = 2), and the spacing bound has only 0.0003 of slack. The 1/16 margin is never close to binding, though: the actual errors are below 0.0007 for every m tested.
- **The control's fold.** In the K+1 control, the fold ends exactly on a wall level at the target abscissa. That's harmless: it's a straight wall, and the ray reflects there.
