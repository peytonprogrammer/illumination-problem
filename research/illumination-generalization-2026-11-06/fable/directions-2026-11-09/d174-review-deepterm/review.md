# Review: deep-terminal-band.md (snapshot 2026-11-22 1332)

**Verdict: sound with gaps.** The floor-return theorem (A) and the prime-power case are both correct, including equality. Every replayed shot lands exactly on T. The union of all tests still leaves an infinite lattice region uncovered, so LLLLLRLRLR stays **PARTIAL**. Checks: `checks.py`, `checks.log` (48 PASS, 0 FAIL, 0.9 CPU-seconds, `python3 -B`, named rooms only). The tracer and `Room` class are copied from d171.

Notation follows d170 and d171. Widths w<u<v<W and heights c,d,e,h run top to bottom. The source is (x, y3+a) with 0<x<w and a>0. The target is (z, h−b) with v<z<W and 0<b<h.

## 1. Floor-return theorem (A)

**Statement.** d(W−u) ≤ (u−w)(e+h) and (d+e)(W−v) ≤ h(v−w).

- **Choice of E.** E−as = E(1+a/L) − az/L. Setting this equal to R ≡ x+az/L (mod 2w) gives E−as ≡ x (mod 2w), so the line starts at an even lift of the source. With |R| ≤ w, |E| ≤ w·L/(L+a) < w because a>0.
- **Slope and gates.** s=(z−E)/L. The developed line is E+st, with t measured from the first gate. Its values at t=d and t=d+e are exactly the note's second and third gate coordinates. At t=L the value is z. This passes exactly on 4,000 random rational rooms.
- **Gate 2.** |g2| < ((e+B)w+dW)/L strictly, because |E|<w and z<W. The bound is ≤u iff d(W−u) ≤ (u−w)(e+B). Since B>h, the first inequality of (A) gives this with strict margin. The lower side g2>−u holds for any z>0.
- **Gate 3.** The same argument gives |g3|<v iff (d+e)(W−v) ≤ B(v−w), and B>h gives the margin.
- **Strictness at equality.** Equality in (A) is safe, for two reasons: |E|<w is strict, and B>h. The rooms E1=(2,3,5,7; 2,1,1,3) (equality in the first inequality) and E2=(1,2,3,5; 1,1,1,2) (equality in both) replay correctly.
- **Floor crossing.** X_f = g3(1−h/B) + (h/B)z with h/B in (1/2,1). This gives X_f > v(2h/B−1) > 0 and X_f < max(g3,z) < W. So the floor contact is interior.
- **Fold agreement.** |developed X| is below the narrower width at each gate, so both folds give |X| with the same velocity. X=0 is a contact with the single left wall at a non-vertex.
- **Corners.** In each lower band X interpolates between gate values (and z), so |X|<u in band 2 and |X|<v in band 3. In the bottom band, −v<X<W. So no contact with x=u, x=v, or x=W occurs below the first gate, and the corners (w,y3), (u,y2), (v,y1), (W,h), (0,0), and (W,0) are all avoided. After the floor contact the ray rises only h−b<h.
- **Uniformity.** Both bounds improve as B grows, so (A) works for all b in (0,h), all a>0, and all x. Only the + source sign is used, which suffices.

**Replays.** These replay counts were obtained:

| Room | Pairs | Result | Max reflections |
|---|---|---|---|
| U1 | 195 half-lattice, 40 random | 235/235 | 5 |
| U2 | 175 half-lattice, 40 random | 215/215 | 7 |
| E1 | 135 half-lattice, 40 random | 175/175 | 3 |
| E2 | 9 half-lattice, 40 random | 49/49 | 3 |

In every replay, the trace hits exactly one floor point, at the predicted X_f. The note's U1 shot (slope 17/20, 3 reflections) and U2 shot (14/31, 5) match exactly.

## 2. Prime-power case

**Statement.** Let q = den(P0·h/W). Assume some prime power p^k dividing q satisfies p^k ≥ W/w.

- **Rotations.** The two rotations Pb/(2W) and P(2h−b)/(2W) sum to Ph/W. A prime power dividing lcm(q1,q2) divides q1 or q2. So one terminal rotation has spacing 2W/q_i ≤ 2w, which gives |Z| ≤ w (closed).
- **Gates.** Each gate value is X(1−τ/D) + Zτ/D with τ<D and |X|<w, so it is strictly inside (−w,w) even when |Z|=w. Both source signs can't give ±w, because 0<x<w.
- **Floor corner.** The early-stop argument is correct. A point reflection through a floor corner preserves the bottom-band fold. The two points at depth ±(h−b) fold to T, and the incoming one comes first. The check builds this case explicitly. In U2b with S=(1/2,15/2), b=1/5, and M=30, both signs aim at (0,0). The full trace stops at that corner. The trace truncated at travel a+d+e+b ends exactly at T (z=319/75 and 281/75).

**Replays.** These replay counts were obtained:

- **The note's U2b shot.** b=5/3, B=19/3, M=18, Z=0, 1065/59, and 57 reflections. All values match.
- **U2b and T1.** All half-lattice pairs and 40 random rational pairs per room were replayed. Each runs twice, once with the direct route preferred and once with the floor route preferred. All 132 shots reach T, with up to 1,091 reflections.

## 3. Coverage of LLLLLRLRLR (key)

Write W₀ = min{u+(u−w)(e+h)/d, v+h(v−w)/(d+e)} and c₀ = min{eu/(v−u)−d, w(d+e)/(v−w)}. Then (A) holds iff W ≤ W₀. The transpose (A)ᵀ, which reads (v−u)(c+d) ≤ eu and (v−w)c ≤ w(d+e), holds iff c ≤ c₀. C, A170, and A170ᵀ don't involve W or c.

**Answer: not covered.** A real room is uncovered exactly when all of these hold:

- **(i)** d(v−u) > e(u−w).
- **(ii)** w(e+h) > ud, or (u+w)h(e+h) > ve(d+e+h).
- **(iii)** hu > (e+h)(v−u), or (e+2h)wu > v(u−w)(d+e+h).
- **(iv)** W > W₀.
- **(v)** c > c₀.
- **(vi)** d168's span condition (1) and (1)ᵀ fail.
- **(vii)** B, Bᵀ, the prime-power case, and its transpose all fail. For a lattice room, let q = W/gcd(W,P0h). Then B fails iff q ≤ ⌊W/w⌋², and the prime-power case fails iff every prime-power factor of q is below W/w.
- **(viii)** The room isn't RES.

**Real lengths.** Conditions (i) to (v) define a nonempty open set, unbounded in W and c. Condition (vi) cuts it to a null set, but that null set contains every commensurable room in (i) to (v) that also meets (vii).

**Without transposes.** Drop (iii), (v), and the transposed parts of (vi) and (vii). The region grows. For example, U1b=(2,3,5,9; 1,1,1,3) is covered only by the transposed prime-power case.

**Explicit uncovered lattice rooms.** All nine tests fail on these, in both orientations:

- **V1** = (2,3,5,9; 3,1,1,3). q=1 and transposed q=1. (A) fails 6>4, and (A)ᵀ fails 8>3.
- **V2** = (1,2,3,6; 3,2,1,4). q=1 in both orientations.
- **Infinite family** (2,3,5,90m; 40n−5,1,1,3) for m,n ≥ 1. Here q=m and transposed q=n. The check verifies m,n ≤ 5.

The note's own grid (0,10,11,13,2860k) also fails all nine tests (k ≤ 5 checked). This is a residual of sufficient tests only. The V1 pair (1,13/2)–(7,3/2) has both rotations at denominator 2, yet the (A) shot still lights it.

**Updated attributions.** These differ from d171:

- U1 and U2 are covered by (A).
- U2b is covered by the prime-power case.
- **T1 is covered by the prime-power case directly** (q=13 ≥ 13/3), so it no longer needs d170's transpose.
- RES still needs d171's certificate.

## Gaps

1. **High (ledger).** The union doesn't cover the word. V1, V2, and the family above are uncovered lattice rooms. LLLLLRLRLR stays PARTIAL. The note says this correctly.
2. **Medium.** "Equality extension of the terminal strip construction" overstates the relation. The prime-power test and d168's q > ⌊W/w⌋² test are incomparable. W=60, w=8, q=60 passes B but has prime powers 4, 3, and 5, all below 7.5. U2b passes only the prime-power test. Both tests follow from one test: q is not lcm(q1,q2) for any q1,q2 < W/w (checked for W<60). State that test as the result.
3. **Medium.** The note misses that T1 is covered by its own prime-power case, and that U1b is covered by its transpose. It also doesn't state (A)ᵀ or the transposed prime-power case, though it uses the transpose for d170. The coverage table should list all of these.
4. **Low.** The (A) proof should say why the bounds are strict (|E|<w from a>0, z<W, and B>h). It should also say why no corner is hit in the lower bands: X stays between gate values, and −v<X<W in the bottom band.
5. **Low.** "Every real pair is lit" means pairs of interior marks. The open pair comes from (A), and all other pairs rest on d169, which covers interior points only.
6. **Low.** "Contains a prime power" should read "is divisible by a prime power p^k ≥ W/w", with P=P0 optimal.

The note's polygon for LLLRLLLRLR has that turn word and area 8 (checked). This review didn't check that it's the smallest OPEN word.
