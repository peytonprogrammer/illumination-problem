Advances: L1 — the short-denominator necessity for a fixed target image fails on the free-height chart. The rotation identity survives.

**Prediction and named check.** At (m,H,t,N,e)=(24,2,1,5998,1000) I predicted a miss for one upward target image and a hit for the other. With levels (−26,0,1,25,26,27), scan_general.py gave K/X=7030/7000, upward start, 752 horizontal bounces. Taking j=125 puts the third crossing at 180/7 and the second at 180/7−7030/7000. Both are strictly inside their gates. The final image is 7030−48·125=1030≡26 modulo 4.

**First failed implication.** Write z=(N+1)s−2mj. The affine determinant 4mH/X and the stated rotation modulo 2 lcm(m,H) are correct for a fixed image c. But the interval for z is

    (1,m+1) ∩ (m+1−s,m+1+H−s).

Its length is at most H. The permitted interval moves with s. In particular its relative length can be at most g/(2m), arbitrarily smaller than the proposed g/(2H) when m grows and H stays fixed. A gap bound for visits to a fixed interval cannot be applied using that proposed width.

**Exact obstruction.** Fix m=24,H=2,t=1 and let k be any positive integer, N=6k−2, e=k, X=7k. For c=24 the target equation is K=24+48j+4i. In this upward no-turn class the third crossing is y=(6/7)K−48j. Hence

    7(y−25)=−31−48j+24i ≡ 17 (mod 24).

The gate requires 0<7(y−25)<14. This excludes every winding for that image, independent of k. Yet (e+1)/X tends to 1/7, at positive distance from every rational with denominator below 2H=4. No neighborhood of radius O(H/(DX)) about those fractions can explain the miss. The obstruction instead comes from the third gate and the exact ratio (N+2)/X=6/7.

The free-height chart includes H<m. A theorem assuming H≥m+2 would need a different argument and a separate treatment of the excluded heights. This counterexample concerns a fixed c, the unit of the proposed rotation test. The other image succeeds at the scanned point. I have no full-list miss, assertion of membership in V, or bound H(C) from it. I stopped at the failed necessity as requested.
