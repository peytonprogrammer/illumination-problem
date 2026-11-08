# UDPA01: explicit good seeds for every member of the wrong-coset control family

Independent review pending. This theorem changes the initial seed; it does not repair the peer's unrepairable seed. Its proof is uniform in an unbounded parameterN and all native bottom targets.

## 1. Original quantified family

For every odd integerN>=7 take e4,P1,K1,L4 with boundary
 (4,2),(4,4),(4N-4,4),(4N-4,3),(4N-16,3),
 (4N-16,0),(4N,0),(4N,N+5),(0,N+5),(0,2).
The strict ordered inequalities give a finite strictly simple orthogonal ten-wall polygon, with three reflex corners. Actual S=(2,6) is interior in the full cap. Every native bottom point hasv2 and t=4N-2r for exactlyr1..7. All are distinct fromS. Set d=N+5>=12,A=4N,a=R4,B16,z=2r.

The genuine itinerary has initial cap descent2, left loop4, roof cap2(N+1), right1, bottom1, totalD=2d. Only the actual initial cap walls0/A are used aboveh4; walls0/a are used in the left loop belowh4.

## 2. A uniformly available target-grid seed

Choose the unique integer k in{2,3,4,5} with k=r+1 modulo4. Put
 tau0=4N-2+k/d,
 q=N^2+4N+(k-r-9)/4.
The latter is a positive INTEGER: k-r-9 is divisible4. Direct substitution gives
 tau0=(A+z-s+2eq)/D.
Thus this is the complete target-compatible grid, not a projected or altered endpoint. Choosing k is an explicit four-case formula for r; no direction search or coefficient fitting is involved.

## 3. All four strict original passage guards

The exact initial cap fold index isnpre1, and its literal left-entry residual is
 zpre=2+2tau0-8N=-2+2k/d.
Because2<=k<=5 andd>=12, this lies strictly in(-4,4). It gives a genuine full-cap-to-left-opening descent.

After the left loop, nleft=2N-1 gives
 z0=zpre+4tau0-8(2N-1)=-2+6k/d,
again strictly in(-4,4). These indices are the ACTUAL centered indices since their displayed residuals lie in the open width4 intervals; no different sheets are chosen independently.

At the descending right h opening, cap indexm=N gives
 z1=z0+2(N+1)tau0-(2N+1)4N=2k-6-2k/d.
For k2 this is-2-4/d, k3 is-6/d, k4 is2-8/d, k5 is4-10/d. All are strictly between-4and4.

Let nu=1 whenk5 andnu=0 otherwise. The ACTUAL right index is
 kright=(N-1)/2+nu,
and its residual is
 z2=z1+tau0-8kright
    =2k-4-k/d for k<=4,
    =-2-5/d for k5.
For k2 this is-2/d, k3 is2-3/d, k4 is4-4/d, k5 is-2-5/d. Each is strictly in(-4,4). Thus all initial-entry/left-loop/cap/right guards hold simultaneously for EVERYN/r.

## 4. Full actual target correction

The developed final phase at the seed is
 E0=z2+tau0=4N+2k-6-8nu.
The exact integer target index is
 J=(E0-2r)/8=(2N+k-r-3)/4-nu.
It is integral because N is odd and k=r+1 modulo4. Choose the unique p in0..3 satisfying J+N*p=0 modulo4; N is a unit modulo4. Set
 tau=tau0+8N*p.

This is one FINAL slope. It changes first-cap/left-loop/roof-cap/right indices by2p,4N*p,2(N+1)p,N*p respectively. Every displayed literal passage residual is unchanged. E increases by8N*p, and its final index J+N*p is divisible4. ThereforeE=+2r modulo32, F16(E)=2r, and actual x=A-F16(E)=4N-2r=t. No physical target or actual endpoint lift is replaced. The negative image need not be used at the final slope.

## 5. Genuine ordinary floor and roof, signed path and firstT

The actual floor lies at full elapsed4. Its left-loop phase iszpre+2tau. Modulo its full period8 this equals
 2+4k/d.
For everyN>=7,k<=5 this lies in(2,11/3], strictly within the original floor(0,4). Thus the FINAL floor is ordinary; no prefix deletion is needed. The target also has height2, but its x>=4N-14>4, so this floor contact cannot be the target.

At the roof the phase isz0+(N+1)tau. Modulo integer multiples ofA, it has the noninteger fractional part2k/d in(0,1), because2k<=10<d. Therefore it cannot be a roof endpoint. Its contact is ordinary. All other potential reflex corners are excluded by the four strict passage residuals. Adjacent triangular folds have the same physical value AND signed derivative; original vertical walls reverse onlyvx and the two original horizontal contacts reverse onlyvy. The initial cap uses widthA; no artificiala-wall is used aboveh.

Initial cap heights exceed targetv2. Left-loop x<=4<t excludes every earlier visit to height2. Right/cap heights are>2, and the bottom reaches2 only at its last time. Hence the ray reaches FIRST actualT. The finite parameterN and finite positive final slope give finitely many ordinary original-wall reflections, with no uniform reflection cutoff claimed.

## 6. Relationship to UDPO01 and the full goal

The peer's UDPO01 wrong-coset seed has tau_bad=4N-3/d andq_bad=N^2+(9N-3)/2. Our tau0=4N-2+k/d andq above are different. We do not transform its bad seed while preserving its literal residuals, and its all-real preserving-increment obstruction remains correct. Instead the explicit seed jointly starts in a reachable cap coset. This closes actual upperS-to-ALL-native-bottom illumination in the entire parametric countercontrol family, including deltaN=N/P1 cases excluded by UP03's sufficient width inequality.

It does not prove every upper source in these rooms, all pairs, arbitrary upper depth, allr3 orr<=8. Earlier LC04 covers half-odd target offsets in broader families; this theorem ALSO covers evenr2,4,6 whose z/e is integral and missed by that criterion. The full goal remains OPEN.

## 7. Two prescribed checks declared before execution

N7,r4 givesk5,d12,tau0=317/12,J2,p2,final1661/12,Jfinal16,actualT20,2. Literal residuals -7/6,1/2,19/6,-29/12; actualfinalindices npre5,nleft69,m39,kright18.

N9,r2 givesk3,d14,tau0=479/14,J4,p0,final479/14,Jfinal4,actualT32,2. Literal residuals -11/7,-5/7,-3/7,25/14; actualindices npre1,nleft17,m9,kright4. This target has z/e1, outside the earlier half-odd target criterion.

Quantifiers follow from the explicit formulas and inequalities above, not from these finite controls. No discovery search, new clock, engine, census, fitting, worker or git mutation.
