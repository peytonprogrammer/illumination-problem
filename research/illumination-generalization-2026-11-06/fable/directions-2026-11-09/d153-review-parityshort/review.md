# Review of parity-shortening (snapshot 2026-11-22-0320)

**Verdict: sound with gaps.** Every computational claim I tested reproduces with an independent room builder and an exact tracer. None of the gaps below breaks the stated conclusion. Two of them are about precision of scope and the stated period.

Reviewed files are the read-only snapshots `d95-review-queue/snapshots/parity-shortening.2026-11-22-0320.{md,py}`. Context came from `qclass-closure/bbbb/uniform-tail.md` and `length-periodicity.md`. My script is `checks.py`, its output is `checks.log`, and it runs in under 0.1 CPU-seconds. It does not import `cyl.py`. It uses Fraction positions on a continuous ray, named rooms only, and no searches.

## Check results

1. **Room and line test: confirmed.** The room R(X,Y) is three 3×3 chambers at x=0, 3+X, 6+X+Y, with unit corridors over 1<y<2. Boundary tracing gives one component and 20 vertices, with no pinch points. The room has 12 convex and 8 reflex corners, and the horizontal wall gcd is 1 at all four named lengths. Areas are 35, 33, 83 and 81. With S=(2,1), T=(4+X,1), and direction (2,1) under signs −−, −+, +−, ++, the results are:
   - X=Y=28: corner, repeat, repeat, corner. The line misses T for all four signs.
   - X=26, Y=28, T=(30,1): corner, repeat, repeat, target.
   - X=Y=4 and X=2, Y=4 match the note's table too.

   S is unchanged and T moves by 2 in x, so both mark parities are preserved. "Repeat" is a valid miss certificate because billiard flow is invertible: a recurring state means the start state lies on the cycle.
2. **Period: true, but 12 is not the least period.** For a full traversal with |v|=(2,1) in width w=1, the formula gives T(2,1) = 2·1·2/gcd(1,4) = **4**. The direct phase computation restores exit height and sign at insertions 4, 8 and 12, and not at 1, 2, 3 or 6. Room-level replays agree at period 4 and with Y shifted alone. The tested rooms are (8,8)/(6,8), (16,16)/(14,16), (4,8)/(2,8), (28,32)/(26,32) and (40,40)/(38,40). So there is no mismatch: 12 = 3·4 is a valid period. The likely reason for 12 is normalization, since X ≡ Y ≡ 1 mod 3 keeps the horizontal gcd at 1. Period 4 alone would allow X=Y=12, where that gcd is 3. The note doesn't say this (gap 2). Its derivation (±6 transverse travel, height phase period 2) is correct.
3. **Two-cycle removal: confirmed by cell counts.** At each of the 4 parity sites, X=Y=28 has n=83, f=3, r=2 and q=37. X=26, Y=28 has n=81, f=3, r=2 and q=36. Each site loses exactly one incidence-2 lattice point of the corridor, and corner counts don't change. The identity n=f+2q+3r holds only if q counts incidence-2 points once and interior (incidence-4) points twice. I didn't recompute the monodromy permutations. The cell-count argument is enough for the claim.
4. **Dilation argument: valid under stated conditions.** Take a long room with corridor length L+1. Dilate it by an even m, shorten the corridor by 2 m/2 times, then shrink back. This telescopes correctly from m(L+1) to mL. The argument requires:
   - the descent hypothesis holds on the non-normalized dilated rooms, with corridor width m and wall gcd m, and on every intermediate room;
   - the threshold depends on wall count only, not on the enlarged dimensions or the door width;
   - the predicate is existence of a real-mark dark pair, which dilation preserves.

   The note states the first and third conditions and the normalized-only caveat. Under these conditions the argument also gives descent by any positive integer amount, not only 1. My tracer confirms dilation invariance at m=2 on the two small rooms. The contrapositive is also correct: a unit dark-to-lit example in that range would refute uniform 2-step descent.
5. **Scope: the note refutes only fixed-direction transfer.** The independent shot (X/2+1, 1) hits T after 1 reflection at X=4, 2, 28 and 26, so the pair is lit at both lengths. The precise statement the note refutes is the following. For a fixed unoriented primitive direction v and fixed marks with T carried along, "v joins S to T in the shortened room" does not imply "v joins S to T in the longer room". This holds at X=4+12k versus X=2+12k, Y=4+12k, for every k≥0, inside normalized 20-wall rooms that are BBBB for k≥2. The note doesn't refute:
   - pair-level monotonicity of darkness;
   - room-level descent;
   - any transfer that may change the direction with the length. The lighting shot here does exactly that, with slope 2/(X+2).

   The note says this in its fourth section. The opening verdict sentence, "monotonicity for individual shots is false", is looser (gap 1).

## Gaps

1. **Medium. Scope sentence is looser than the result.** The verdict line and "It refutes the proposed ordering of directions through a door" should name the refuted statement exactly. That statement is fixed primitive direction, fixed marks, and implication from shot-in-short to shot-in-long. The note should also say that the pair is lit in both rooms by a length-dependent direction. Without this a reader may take "shot monotonicity" to include transfer of some shot.
2. **Low. Period 12 isn't explained as non-minimal.** By the length-periodicity formula and the replay, the least period is 4. The note should say that 12 is chosen to keep X ≡ Y ≡ 1 mod 3 for normalization. Otherwise a reader comparing with T(p,q) sees a mismatch.
3. **Low. "All four canonical relations universal" and "all four canonical quotient degrees stay one for k≥2" have no support.** Neither the snapshot script nor this review checks them, and the note gives no link or computation.
4. **Low. The weighting in n=f+2q+3r is implicit.** The identity requires interior lattice points to count as two regular two-cycles. The cell-count conclusion (Δq=1 at each site) is correct, but the identification should be stated or linked precisely.
5. **Low. The dilation lemma's threshold condition is implicit.** The phrase "above a wall-only threshold" carries this. The lemma needs the threshold to be independent of the other dilated dimensions and of the door width m. The lemma also gives descent by any integer, not only 1, and could say so.
6. **Low. The snapshot script doesn't run from the snapshot location.** `parents[2]` resolves to `directions-2026-11-09/`, so the `cyl` import path doesn't exist there. It resolves correctly from `qclass-closure/bbbb/`. Its asserts cover only k=0 and k=2.

The R22 one-unit section and the d142/d144/d8 citations are outside this review's scope and remain unchecked.
