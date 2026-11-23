# d176: review of l1-primitive-subset-action.md

Note: `../d95-review-queue/snapshots/1715/l1-primitive-subset-action.md`. It's identical to `qclass-closure/bbbb/l1-primitive-subset-action.md`.
Checks: `checks.py`, log in `checks.log` (about 3 CPU-seconds, `python3 -B checks.py`).

## Bottom line

**Sound, with one inherited Medium gap.** The group theory is correct and checked exactly for every cycle type with m ≤ 14 and 2 ≤ k ≤ m−2. The geometric dichotomy has no hole. In the subset-action branch, every reflex-bearing class is corner-only. The corner-only theorem then excludes dark pairs below 22 walls at every area.

The conclusion for lattice marks rests on a fully reviewed census (d102). For real marks it rests on the continuum extension, which d103 and d107 confirmed "with gaps."

The result is a branch exclusion, not L1. In d81 Proposition P it removes the λ = 2 subset-action residual (n = 21, 28). The natural action, primitive groups outside the Burness–Guralnick family with n ≤ 6z_x, and most imprimitive cases remain open.

## Verified items

1. **Faithfulness.** Brute force over all permutations for m ≤ 7 and every 2 ≤ k ≤ m−2: no nonidentity letter permutation fixes every k-subset. The note's argument (the k-subsets containing a letter intersect in that letter when k ≤ m−1) is correct for all m. Faithfulness isn't even essential: ord(g) divides ord(σ) is enough.
2. **Every order-6 letter permutation has a k-subset orbit of length 6.** checks.py enumerates all cycle types of S_m for 4 ≤ m ≤ 14 and all 2 ≤ k ≤ m−2, which is 4,332 (m, k, type) triples. No counterexample. The stronger statement also holds: among the 613 triples whose k-subset cycles lie in {1, 2, 3}, every letter type is 1^a 2^b or 1^a 3^c. None mixes 2- and 3-cycles.
3. **Both constructions.** For every order-6 type, checks.py builds the note's subset and confirms period exactly 6.
   - The 6-cycle interval works for every j in [max(1, k−(m−6)), min(5, k)]. The range is nonempty because k ≤ m−1.
   - The 2+3 choice (one letter of the 2-cycle, one or two of the 3-cycle) reaches every k from 2 to m−2.
4. **Contrast with k = 1.** Type 3+2 in the natural action has cycles {3, 2} and no 6-cycle, as the note's Limit says.
5. **Corner-only consequence.** A letter type 1^a 3^c never produces a 2-cycle on k-subsets (0 cases). So a reflex class in this branch has no 2-cycles on sheets.

## Geometric step (question 2)

The dictionary (d81 §1, D0; d102 item 1) maps a class-x grid point to cycles of g_x by its incident cells:

- 1 cell (convex corner) → fixed point
- 2 adjacent cells (smooth wall point) → one 2-cycle
- 3 cells (reflex corner) → 3-cycle
- 4 cells (interior point) → two 2-cycles on the double

Strict simplicity excludes diagonal pinches. So class x is corner-only exactly when g_x has no 2-cycle. The note's argument is a dichotomy on a class with z_x ≥ 1:

- If g_x has a 2-cycle, g_x has order 6 and no 6-cycle, which items 2 and 3 forbid.
- If g_x has no 2-cycle (only 3-cycles and fixed points), class x is corner-only by definition.

There's no gap. The "only 3-cycles and fixed points" case is the conclusion, not an exception. A reflex class exists whenever r ≥ 1. A rectangle (r = 0) is lit anyway.

## Corner-only closure (question 3)

`qclass-closure/twenty/README.md` states:

> **Computer-assisted theorem.** Fix a square grid and let the room be a strictly simple orthogonal polygon with vertices on that grid. Suppose that for at least one of even-even, even-odd, odd-even and odd-odd, every grid point of that class in the closed room is a polygon corner. If the room has fewer than 22 maximal walls, every two distinct interior points can be joined by a billiard path that avoids corners. Both endpoints may have arbitrary real coordinates.

Its "Why this covers every area" section gives n ≤ (r+4) + 3r ≤ 36 for r ≤ 8. This matches the note's budget n = f_x + 3z_x. The theorem has no area hypothesis, so it covers every area at W ≤ 21. The note's citation is accurate.

## Gaps

### High

None.

### Medium

1. **Real-mark strength of the cited closure.** The lattice-mark census of corner-only rooms with n ≤ 36 is reviewed as complete, with every witness replayed (d102). The real-endpoint extension is "confirmed with gaps":
   - d103 left the pixel-finished rooms and tile-level residuals partly unchecked.
   - d107 independently re-derived residuals for 11 of 24 shear-box rooms.
   - The README says the whole-room continuum solver "has not been independently reimplemented end to end."

   The note should say "no dark lattice-mark pair (reviewed); no dark real pair (computer-assisted, partly reviewed: d103, d107)."

### Low

2. **The d81 residual is smaller than the note says.** Cycle types plus Σf = r+4 and Σz = r ≤ 8 already rule out n = 28 (m = 8, k = 2): no type quadruple passes. Only n = 21 survives the counting. This doesn't affect the note's proof.
3. **Header overstates the advance.** "Advances: L1" fits only as a branch exclusion inside d81 Proposition P. It doesn't give an area bound for any room outside the branch. The Limit paragraph says this correctly. The header line should match.
4. **The closing question doesn't fit.** The note classifies rooms by monodromy group, not by wall word. So "No ledger word moves" is right, and the example word LLLRLLLRLR says nothing about this result.

## Does the branch occur? (question 4)

Room realizability wasn't checked, because the brief forbids room searches. At the formal level the branch isn't vacuous. checks.py searched exhaustively for letter 4-tuples with product 1 that are transitive on k-subsets and meet Riemann–Hurwitz with 1 ≤ r ≤ 8. It found:

| m, k | n | Formal tuple | r, W |
| --- | ---: | --- | --- |
| 4, 2 | 6 | yes (S_4 on pairs, imprimitive) | r = 2, W = 8 |
| 5, 2 | 10 | yes | r = 3, W = 10 |
| 6, 2 | 15 | yes | r = 5, W = 14 |
| 6, 3 | 20 | no | — |
| 7, 2 | 21 | yes: letter types 2³1, 2²1³, 3²1, 2³1 | r = 7, W = 18 |
| 7, 3 | 35 | no type quadruple | — |
| 8, 2 | 28 | no type quadruple | — |

The n = 21 tuple is the one d81 left unchecked. Its reflex class has f = 0 and z = 7, a corner-only class inside the 36-square budget. If a room realizes it, the 18-wall corner-only census already contains that room. Every n ≤ 20 case is also covered by L2.

## Which L1 cases remain open

- **Natural action (k = 1), including G ⊇ A_n.** This is the main primitive case. A 2-cycle and a 3-cycle coexist there without a 6-cycle, so no one-site argument works. d81 gives only d ≥ 2n/3 here, not darkness exclusion.
- **Primitive groups outside the Burness–Guralnick family with n ≤ 6z_x.** These cover 21 ≤ n ≤ 48, as in d81 Proposition P's second alternative. The note doesn't touch them.
- **Product actions with κ ≥ 2.** d81 excludes these for n ≥ 21 by counting z_x. This note adds nothing there.
- **Imprimitive groups.** These are the d81 §6 table rows below n = 49. The note covers an imprimitive group only if its sheet action is a k-subset action (for example S_4 on pairs). Most block systems don't have that form.
- **The step from d ≥ 2n/3 to an area bound, and L3/L4.** These are unaffected.
