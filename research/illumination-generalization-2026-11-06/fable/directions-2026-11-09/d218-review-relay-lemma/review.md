# D218 review: relay lemma (note-snapshot.md)

Referee: independent. Date: 2026-11-23. Named rooms only: R22 (manuscript vertex list), P6 (d31 found.json, checked congruent to the d61/d217 P6), R34-base, cov4181, and the rectangle [0,8]×[0,4]. Checks: [checks.py](checks.py), output in [checks.log](checks.log). Result: 121 PASS, 0 FAIL, 0.06 CPU-seconds.

The only rays are shot in directions fixed before any comparison. These are the base-state arcs (1,0), (0,1) and (1,1), and their images under the four single pure-braid moves σ₁^{±2} and σ₂^{±2}. There is no direction, word or room search.

**Overall.** No claim is wrong. Claims 2, 3, 5 and 6 are correct. Claims 1 and 4 are correct with wording gaps. The note advances **L1** by scoping. It turns "realize one branch on U" into an exact distance test on one component in one state. It does not prove that test passes anywhere in the open case.

## Verdicts

| # | Claim | Verdict |
|---|---|---|
| 1 | Three-way split exhaustive under the single-factor meaning; (ii) rows have areas 8, 12, 16, 10, 12 and are census-covered | CORRECT WITH GAPS |
| 2 | Different-parity midpoints: fixed points of τₑ, 2dₑ regular candidates | CORRECT |
| 3 | Rectangle: all developed midpoints have source parity, yet the pair is lit | CORRECT |
| 4 | Dark-room controls R22, P6, R34 | CORRECT WITH GAPS |
| 5 | 2⌈2n/3⌉−16−⌊n/2⌋ > 0 regular off-class branches on U; value 2 at n=21 | CORRECT |
| 6 | Single-state path/cycle test | CORRECT |

### 1. Three-way split

The split is (i), (not i and F), (not i and not F), where F is "a single separating factor exists". It is a partition by construction. The (k,z,m) enumeration with k ≥ 2, kz ≤ 8 and 2 ≤ q = 2m−2−2z ≤ ⌊m/2⌋ gives exactly (2,2,4), (3,2,4), (4,2,4), (2,3,5) and (2,4,6). Their areas are 8, 12, 16, 10 and 12. All are at most 21, and [census-a21-status](../../../../qclass-closure/bbbb/census-a21-status.md) records areas through 21 as complete. Because r = kz + c₃ ≥ kz, the bound r ≤ 8 implies kz ≤ 8, so the table is complete for r ≤ 8.

Gaps:
- Under the single-factor meaning, rooms with separate factors for separate classes, or with separation at only one class, fall into (iii). The note says these "require their own argument" but doesn't say which branch they're in. They're in (iii). Such a room could be dark, which would make the (iii) "lit" conjecture false there. The BBBB universality sentence excludes them only in normalized BBBB charts. The note should state that (iii) contains them, and cite the reduction to normalized BBBB charts if one exists.
- The "stronger midpoint target" in (iii) is strictly stronger than lighting. The rectangle in claim 3 is lit with no off-class midpoint in any class. That pair is direct, so this doesn't refute the target for nondirect pairs. The target should carry the word "nondirect" explicitly.

### 2. Different parities

Let e = T−S mod 2, with e ≠ 0. Reflections preserve parity, so a developed displacement is N·v with N odd and v ≡ e. The half-time point is N·v/2, so 2u ≡ e mod 2. On B = (ℝ²/2ℤ²)/{±1}, the fixed points of τₑ are the solutions of u+e ≡ −u. checks.py finds 4 torus solutions for each e, in 2 sign orbits, and none is a pole. The pair (γ(t), γ(N−t)) lies on f(p) = τₑ f(q), because u(N−t) ≡ e − u(t). Each diagonal intersection lies over a fixed point where f is unramified and τₑ has derivative −1. The intersection is therefore transverse, so the bidegree-(1,1) count gives exactly 2dₑ distinct regular points. This matches [l1-bbbb-area-bound](../../../../qclass-closure/bbbb/l1-bbbb-area-bound.md).

Remark: there is no lower bound on dₑ beyond the marked branch itself, and d81 doesn't transfer to it. The note's eight-reflex theorem is phrased conditionally, so this is not an error.

### 3. Rectangle

The images of T are (±6+16i, ±2+8j). Each agrees with S = (2,2) modulo 4. Every displacement is therefore ≡ 0 mod 4, every gcd is divisible by 4, and every developed midpoint has the parity of S. The horizontal chord passes only the interior points (3,2), (4,2) and (5,2), so the pair is lit with midpoint (4,2) over a.

**Supporting named-room instance (new).** cov4181 is a normalized room with r = 8. In state σ₂^{±2}, class b, with exact billiard direction (1,∓2), both S lifts and both T lifts lie on one path component, with D = 4 and D = 12. Both are ≡ 0 mod 4. The pair is lit in that state with a source-parity midpoint, and the test correctly reports no off-class relay. This is the same phenomenon inside a normalized chart. The note's sentence "requires no claim about normalized BBBB charts" stays accurate.

### 4. Dark-room controls

All data checks pass.
- **R22.** The manuscript's 22-vertex list reproduces the d217 cells, with area 15 and r = 9. S = (0,0) and T = (2,2) are interior and even-even. (1,0) is smooth with parity (1,0) on the vertical mirror x = 1. The segment (0,0)–(1,0) lies on the open seam H. The off-class smooth sites are exactly the four seam endpoints E₁–E₄. midpoint-orbits.txt gives the marked component d = 12 with regular counts 6,0,0,0, so zero off-class regular branches lie on U.
- **P6.** The found.json cells give area 20, r = 12, strictly simple. The marks (−2,3) and (0,1) are interior, of class (0,1). At (3,2), cells (2,2) and (3,2) are present and cells (2,1) and (3,1) are absent, so the site is smooth, of class (1,0). There are six off-class smooth sites. The room is congruent to the d61/d217 P6, and midpoint-orbits gives 8,0,0,0.
- **R34-base.** The regular sites are exactly (2,0), (6,0), (4,0) and (8,−2), all even-even, so R34-base is in branch (i).

Gaps:
- "No choice of lifts and matched straight approaches through y can connect this pair" should read "with midpoint at y". Membership in U rules out y as a midpoint. A path that passes through y away from its midpoint is excluded only by darkness itself.
- The P6 row uses the found.json frame. d61, d217 and midpoint-necessity use a frame where the marks are (1,0) and (3,−2), of class (1,0). In that frame "(3,2), class (1,0)" is an on-class site. The row should name its frame.

### 5. Off-class branch count

The derivation follows [midpoint-necessity](../../../../qclass-closure/bbbb/midpoint-necessity.md): 2d = R + J, with J ≤ 2r and Rₐ ≤ ⌊n/2⌋. Together these give R_other ≥ 2d − 2r − ⌊n/2⌋. Integrality with d ≥ 2n/3 and r ≤ 8 gives f(n) = 2⌈2n/3⌉ − 16 − ⌊n/2⌋. The values are f(19) = 1, f(21) = 2, f(22) = 3 and f(49) = 26. checks.py confirms f(n+6) = f(n) + 5 and f > 0 for every n ≥ 19, so n ≥ 21 is a safe subset. Each regular point carries at most one off-diagonal branch, so f(n) also counts distinct regular off-class sites on U. Sanity check on cov4181 (n = 28, r = 8, d = 21): R_other = 21 ≥ 12 ≥ f(28) = 8.

The hypothesis d ≥ 2n/3 is still unproved at areas 21 through 48. The note states it as a hypothesis.

### 6. Single-state test

The graph claims hold:
- Regular vertices have two sheets, so the maximum degree is 2.
- The graph is bipartite (a versus x), so cycles are even. Parallel edges give 2-cycles.
- In Q there is no reversal, so a legal walk is the unique nonbacktracking continuation.
- On a path the length is the unique distance D.
- On a cycle the lengths are D + jC or C − D + jC. For even D these agree mod 4, so the test is gcd(C,4) | 2 − D.
- If C ≡ 2 mod 4, the test always passes.

Computation: 5 states (base and the four single pure moves) × 3 classes × 2 rooms gives 30 (state, class) rows.
- Every component satisfies the degree, evenness and tree claims.
- For all four lift pairs in every row, the note's verdict equals the exact residue of the straight Γ_α(Q) walks. The horizon is 6n traversals.
- The Γ walks equal the integer billiard in the predicted direction. The comparison covers every visited a-class point, plus the copy at T. It is non-vacuous in 15 rows, all classes b and d. Class c is vacuous in both rooms, because no class-c site is regular and every c ray stops at step 1.

Results:
- **R22.** The S and T lifts never share a component, as expected for a dark pair.
- **cov4181, base state.**
  - Class b: S and T lie on a 10-edge path with D = 2 or 6, both ≡ 2, so the test passes. This is the direct horizontal chord.
  - Class d: the test fails in all five states, consistent with D66.
  - Class b under σ₂^{±2}: the test fails with D = 4 and 12 while the pair is lit. See claim 3.

Convention note: reversing the twist sign maps an arc (p,q) to its mirror (p,−q). The front/back lift exchange absorbs this, so the check fixes the slope only up to mirror. That is sufficient here.

## Which lemma advanced

**L1**, by scoping only:
1. The realization step is now a finite, exact per-state test: one component, with D ≡ 2 mod 4 on a path, or gcd(C,4) | 2 − D on a cycle.
2. The different-parity case has an exact candidate set of 2dₑ transverse regular points.
3. The rectangle and the cov4181 σ₂² state separate lighting from off-class midpoints.

No closure in the BBBB core is proved.

## First case still open

The case is a nondirect, same-parity, interior pair in a positive normalized eight-reflex BBBB chart with off-class regular sites and no separating factor, with d ≥ 2n/3. The task is to show that in some state some compatible lift pair lies on one regular component and passes the D/C residue test. At n = 21 there are at least 2 candidate branches on U. L2 already lights area 21, so n = 21 is open only for this proof method. The first case that matters for the target is **n = 22**, where f(22) = 3 and the census stops. Per-class-separated rooms outside normalized BBBB charts, if any exist, are an additional unassigned case under the single-factor split.
