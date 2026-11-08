# TR03: every pair illuminates in sufficiently tall ordered spirals

Positive candidate for independent review. Use the ordered spiral P of TR01 with arbitrary real parameters 0<a<l<w<A and 0<b<c<h<H. Put

    R=A-w,
    L=R/(2c),
    Ns=ceil(L*h/(2a))+1,
    Nr=ceil(L*h/(2R))+1,
    delta=L/(Ns+Nr+1).

Claim: if

    H >= c+2A/delta,

then EVERY distinct actual interior pair S,T in ORIGINAL P has a finite corner-avoiding specular connection. There is no area, support, exception or reflection bound. The statement is over arbitrary real metrics and endpoints, so includes the corresponding canonical45 integral/even-even instances.

TR01 already covers pairs both in G or both in int(R_L), where R_L is its L subroom. For its exact uncovered pair, put T=(t,v) in the lowest chamber l<t<A,0<v<c. The other point S=(s,u) is either in the left lower column (0<s<a,b<u<h), or in the upper cap/cut (h<=u<H,0<s<=w, with S an actual interior point).

The new mechanism is not an isolated witness. A target-bottom portal window of length L can be chosen for every actual T. Removing at most Ns+Nr phase-boundary points leaves an open component of length at least delta on which the necessary source and right-arm period indices are fixed. The exact target roots as the upper-cap period index varies have spacing 2A/(2H-u-v), strictly less than delta under the stated height condition. One root therefore lies STRICTLY in that component and supplies one matched actual trajectory.

The proof must check all original finite walls, the three strict portal guards, source/cut and y=h,c endpoint cases, finite integer choices and original target identity. For an upper-cap source, a singular roof event is handled only if the prescribed folded curve demonstrably returns to the SAME ACTUAL S after that event and before the right portal, allowing its subsequent legal suffix to be used. No arbitrary continuation through a corner is licensed.

Success criterion: a complete all-endpoint optical proof for the stated variable-metric tall class, independently reviewed. Strongest objections: the uniform component bound may fail at endpoint phases; different integer indices must remain fixed over the chosen component; a target root might match only a wrong lift; the roof truncation must preserve an actual legal S-to-T suffix. These are proof obligations, not assumptions.

This would close an entire unbounded metric subclass of turn type (1,1,8), not all of that type, the full r3 milestone or the full r<=8 goal. No discovery search or clock has started. Hand proof and prescribed exact formula verification only.
