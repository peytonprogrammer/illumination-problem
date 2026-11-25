Advances: L1 — the x-monotone list lights the entire d234 residual, including every integer m ≥ 2.

**Prediction and test.** Before the construction I predicted upward first hits below slope 2 at m=7,8. The exact d234 scan returned 4757/4705 and 6180/6145 respectively. Neither rounding based on these hits nor a split into regimes is needed.

**A. Select a later image.** Write X=96m²+1 and N=64m². Start upward at height zero. Put K=3mj+m, taking j a nonnegative multiple of 2(m+2). The allowed slopes s=K/X form a progression of spacing 6m(m+2)/X < 1/8 for m≥2. Choose its nearest member to m/2+1; the first member m/X is below this value. Thus |s−(m/2+1)|<1/16.

At the three transmissions the intended ordinates, all moving upward, are

    s,   (2m+s)/3,   (2m+4s)/3.

Indeed the second is (N+1)s−2mj by 3(N+1)=2X+1, and the third adds s. The first and second lie strictly in (1,m+1). The third lies strictly in (m+1,2m+3): its central value is (4m+4)/3 and its error is less than 1/12. Thus the first and third legs have no turn. The middle leg makes j complete periods between its two regular transmissions. In the last column the endpoint folds from K−2mj=mj+m, congruent to m modulo 2(m+2). Reflection about the floor m+1 sends the image m to the target m+2. This chooses the negative one of the two allowed target offsets. All horizontal wall hits inside columns occur on open wall segments. The four columns and these strict gates therefore give a legal chord for every m.

**B. A larger region with an explicit witness.** I predicted a hit with the target one unit below the roof at m=3,7. The scan gave upward hits K=886,4778 respectively. In fact, retain the transverse supports, let N be any positive even integer, and use levels (−a,0,1,m+1,m+1+t,m+1+H), with a positive. Suppose m≥3, H≥m+2 and 1≤t≤m+1. Set X=3N/2+1. A sufficient condition independent of a and t is

    3mH / gcd(m,2H) < X/2.

Put c=m+1−t and K=3mj+c. Require j a nonnegative multiple of 2H/gcd(m,2H). Choose s=K/X nearest to m+1/2. The progression spacing is 6mH/(X gcd(m,2H)), which under the displayed condition is less than one. Its initial member c/X lies below the aiming point. Hence m<s<m+1. The transmissions are s,(2c+s)/3,(2c+4s)/3 by the same identity as in A. For 0≤c≤m and m≥3, the second lies in (1,m+1). The third is above m+1 and below 2m+3≤m+1+H. The endpoint image mj+c reduces to c modulo 2H and folds about m+1 to the chosen target. This proves horizontal lighting even without vertical lock. In particular it applies throughout the tested displaced-target subfamily.

**Where the chart proof stops.** For arbitrary transverse gaps let a,b,d,e be the four consecutive column travels, X=a+b+d+e. After j middle periods the second ordinate is (a+b)K/X−2mj (source level zero). The cancellation above uses 3(a+b)=2X+a, equivalently b=2(d+e). V's two projected-spacing inequalities alone supply no such equality. For example displace the target abscissa by N and use supports (0,N−1,N,2N,2N+1,7N/2,4N,5N). All end mirrors still lie in (N/2)ℤ, the marks have the same residues, and the d233 bound still places the family in V for N=64m². Here e=3N/2−1. The identity used in A fails. This illustrates the scope of the proof only; no horizontal miss is claimed.

For a gate of width d the dual-width bound controls a potential difference by Flt(3)/d. Converting potentials back to integers multiplies by twice the corresponding column height. Consequently the short-relation list is finite for fixed dimensions; its size bound depends on the free height-to-aperture ratios. Also a short relation alone does not certify hollowness. I have neither a bounded exceptional set nor a joint miss. No H(C) or deadline closure follows from A.
