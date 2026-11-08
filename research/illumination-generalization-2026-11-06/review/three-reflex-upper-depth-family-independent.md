# UDPA01 independent acceptance

ACCEPT: for every odd integer N>=7 in the displayed original ten-wall family, actual S=(2,6) illuminates all seven native bottom targets T=(4N-2r,2), r=1..7. All 11 frozen pins pass before and after independent verification. The general proof was audited symbolically; four fixed original-wall replays cover all four k branches. No author code was executed.

This is a positive terminal-pair theorem in an unbounded family, including deltaN=N cases outside UP03. It is not all upper sources in those rooms, all pairs, arbitrary ordered spirals, or the full W10/r<=8 target.

## Claim decisions

1. **ACCEPT geometry, native endpoint scope and seed integrality.** For N>=7 the boundary has 0<4<4N-16<4N-4<4N and 0<2<3<4<N+5, hence is a genuine strictly simple ten-wall orthogonal ordered spiral. S lies in its original full-width cap. Its native bottom height is necessarily 2; the seven strictly interior horizontal native positions are exactly 4N-2r, r=1..7. The unique k in {2,3,4,5} with k=r+1 mod4 makes q=N^2+4N+(k-r-9)/4 positive and integral. Direct substitution in the complete target grid gives tau0=4N-2+k/(N+5), with no endpoint substitution.

2. **ACCEPT all four strict passages and actual indices.** Put d=N+5>=12. Directly centering the initial cap and left-loop phases gives npre=1, nleft=2N-1 and zpre=-2+2k/d, z0=-2+6k/d. Both lie strictly in (-4,4). The roof-cap index m=N gives z1=2k-6-2k/d, which is in (-4,4) for each k=2,3,4,5. The right index is (N-1)/2 for k<=4 and (N+1)/2 for k=5. Its residuals are respectively -2/d, 2-3/d, 4-4/d, -2-5/d, all strict. Actual centering follows from these inequalities; no independent sheet choices are inserted. The zero z0 at N7/k4 is allowed as a smooth outer-wall crossing.

3. **ACCEPT full target equality and final period.** The seed phase is E0=4N+2k-6-8*1_{k5}, so J=(2N+k-r-3)/4-1_{k5} is integral by odd N and k=r+1 mod4. N is invertible modulo 4, giving a unique p in 0..3 with J+Np=0 mod4. The final slope tau0+8Np preserves every literal earlier residual. Its four index increments are exactly (2p,4Np,2(N+1)p,Np), and E increases by 8Np. Therefore E=2r modulo 32 and F16(E)=2r gives the exact actual target t. The same one final slope is used throughout.

4. **ACCEPT ordinary floor, roof and true-corner guards.** The final floor phase folds to 2+4k/d, in (2,11/3], strictly inside the physical floor (0,4). Its ordinary status is preserved by the final slope increment. For the roof, z0+(N+1)tau has fractional part 2k/d in (0,1), because 2k<=10<d. Hence it is not a multiple of the integral width A=4N and cannot hit either roof corner. The four strict passage residuals exclude the other reflex vertices. The initial cap has width A; width 4 is used only below h. These are genuine walls and matching signed folds.

5. **ACCEPT first actual target and finite regular trajectory.** Initial cap, main cap and right-arm heights exceed 2. All left-loop visits to height 2 have x<=4<t, including the ordinary floor contact at elapsed 4. The bottom descent reaches y=2 only at its last time. Every finite N gives a finite positive slope and a finite itinerary with ordinary specular reflections. The independent earliest-wall verifier confirms first target time, physical wall bounds, unique ordinary contacts, signed velocities and every open segment inside the original polygon.

6. **ACCEPT compatibility with UDPO01; no broader conclusion.** The old seed 4N-3/d belongs to a different frozen wrong cap coset. The new seed changes its initial phases and never invokes a literal-preserving repair of that old seed. Thus the independently accepted obstruction and this positive theorem are compatible. The theorem includes the even r offsets not covered by the earlier half-odd target criterion. It does not prove arbitrary upper-source availability or full r3.

## Independent exact checks and calibration correction

The author corrected an unfrozen calibration typo before pinning: N7/r4 final nleft is **69**, not 41. The quantified formula 2N-1+4Np was correct throughout. The frozen proof and checker now both say 69; the independent original-wall replay confirms [5,69,39,18]. No material theorem gap remains.

`three-reflex-upper-depth-family-check.py/.json` verifies the formulas independently and replays exactly four declared controls:

- N7/r4/k5: slope 1661/12, indices [5,69,39,18], 273 reflections.
- N9/r2/k3: slope 479/14, indices [1,17,9,4], 67 reflections.
- Same N7 room, r1/k2: slope 1165/6, 381 reflections.
- Same N7 room, r3/k4: slope 583/3, 381 reflections, including smooth z0=0.

All pass: 1102 actual reflections and 11060 exact wall-leg guards. These fixed checks corroborate the all-N/all-r symbolic proof; they are not a census or evidence-by-sampling replacement for its quantifiers.

No discovery clock was opened or renewed. No worker, new engine, frozen edit or git mutation occurred. The full native theorem remains open.
