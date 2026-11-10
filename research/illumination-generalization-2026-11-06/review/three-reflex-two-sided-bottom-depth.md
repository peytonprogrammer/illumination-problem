# BD01: the final bottom episode needs unbounded depth and a thin negative gate

Status: new hand argument, offered for independent review. No whole-room illumination theorem is claimed. This addresses the full two-sided programme rather than another fixed number of right returns. It supplies a history-independent necessary condition and an exact target-entry relation for one terminal placement, with unbounded bottom return count retained.

The previously accepted two-sided A/B result concerns unbounded RIGHT-floor-cap circuits conditional on illumination. It expressly allows later bottom-only excursions but gives no bound below on their number. The following last-entry argument isolates those actual excursions. I found no equivalent last-bottom bound in the consulted two-sided packet or earlier stopped first-R proofs;

## 1. Domain and actual last entry

Use the original strictly simple integral ordered spiral with boundary

    (a,b),(a,h),(w,h),(w,c),(l,c),
    (l,0),(A,0),(A,H),(0,H),(0,b),

where 0<a<l<w<A and 0<b<c<h<H. Let S be a native terminal source with 0<s<a, b<u<H, and T=(t,v) a native actual interior target with

    l<t<w, 0<v<c.

The strict placement t<w is essential. The result does not include t=w or t>w. All parameters and target coordinates are integral; native even-even marks are included. Put

    B=A-l, R=A-w, W=w-l,
    P=2*lcm(a,A,R,B), tau=P+epsilon,
    0<epsilon<1/(2c), Delta=2c*epsilon<1.

Normalize |vy|=1. All horizontal and vertical reflection signs remain physical. Suppose ANY finite legal actual S-to-T ray exists at this tau, with arbitrary earlier left/right/cap/bottom returns. Stop it at its first actual T. Since S is outside the bottom rectangle (l,A)x(0,c), its final bottom episode starts at a LAST downward crossing of y=c from the right strip. Write its actual entry position as (x_e,c), with w<x_e<=A and vy=-1. The inner point x=w is a true reflex corner and is forbidden. If x_e=A, use the unique outgoing ordinary vertical-wall germ.

Before T, the episode cannot leave through the open right mouth and later return: that would contradict its being the last entry. All earlier upward c contacts in the episode must therefore be genuine reflections on the underside l<x<w. Let m be their number. The time from this entry to T is EXACTLY

    D = 2mc+c+sigma*v, sigma=-1 for downward arrival,
                            sigma=+1 for upward arrival.

No other horizontal wall lies in this rectangle. In particular b creates no extra bottom-chamber wall or corner. The same fixed tau governs the entire original ray and this episode.

## 2. Uniform depth bound — independent of all earlier history

Let F_B be the triangular fold of period 2B, and let eta_e be a phase representing the actual horizontal entry position AND sign. Then

    x_e = l+F_B(eta_e),
    t   = l+F_B(eta_e+tau*D).

The triangular fold is globally 1-Lipschitz on the real line. Since D is an integer and P is a multiple of 2B,

    F_B(eta_e+tau*D)=F_B(eta_e+epsilon*D).

Hence

    x_e-t <= epsilon*D < 2c*epsilon*(m+1).

The left side is strictly greater than w-t>0 because x_e>w. Therefore

    m >= floor((w-t)/(2c*epsilon)).                  (BD01)

The strict inequality before the floor also handles equality of (w-t)/(2c*epsilon) with an integer. Because w-t is a positive integer and Delta<1, m>=1. Thus a successful path cannot reach this target in its final direct/floor-only bottom tail.

For any fixed M, choosing epsilon<(w-t)/(2c*(M+1)) forces m>M. This holds regardless of how many cap/right excursions precede the last entry. A uniform finite bound on bottom-only returns therefore also fails near P. It is a necessary limitation on a complete itinerary class, not failure of one sampled ray.

## 3. The last entry MUST have negative horizontal velocity

There is at least one genuine underside reflection by section 2. At its first possible time 2c after entry, the bottom trajectory has horizontal phase eta_e+Delta modulo 2B.

If the actual entry horizontal velocity is positive, the slow folded distance needed to reach x=w in that positive phase direction is

    (A-x_e)+(A-w) >= R >= 1 > Delta.

So the first upward c crossing is still strictly right of w and exits the bottom episode. It cannot be an underside reflection. The outgoing germ at x_e=A is negative and belongs to the other case, not to this positive case.

For negative entry velocity use eta_e=-(x_e-l). Since x_e-l>W>=1>Delta, the first upward c phase remains negative and its actual position is x_e-Delta. An ordinary underside reflection requires

    l < x_e-Delta < w.

The left inequality is automatic from W>Delta. The right one is equivalent to

    w < x_e < w+2c*epsilon,
    vx=-tau, vy=-1.                                (NG01)

Thus every successful near-P ray to t<w must enter its FINAL bottom episode through this shrinking NEGATIVE-velocity gate. The initially accepted first-R blind-stripe state has positive horizontal velocity, so it is not this gate. A global existence proof must actually generate the opposite directed germ after further physical scattering; it cannot match only the entry position.

## 4. Complete target-entry relation within that last episode

The unbounded m can be retained exactly without enumerating it. Fix a downward incoming state in NG01 and write

    r=x_e-l, y=t-l, W=w-l,
    eta(D')=-r+epsilon*D' at integer section times.

Here W<r<W+Delta<B, and 0<y<W. At upward c contacts, phases advance in steps Delta. A legal episode remains in the bottom only while these contacts have |eta|<W (and eta!=0, the corner at l,c). A step cannot jump from below W beyond B, because Delta<R. Therefore, before the first return to the right strip, all relevant floor/target/ceiling phases stay strictly in (-B,B). At most one SLOW fold through eta=0 occurs; the many physical vertical-wall bounces caused by P are still present.

To hit actual T in this episode, its phase must be either -y or +y. Let kappa=-1 or +1 encode that actual target-image choice. The exact equation is

    epsilon*(2mc+c+sigma*v) = r+kappa*y,
    sigma in {-1,+1}, m>=0.                        (BT01)

Equivalently, set L_kappa=W+kappa*y, which is positive, and let

    d=x_e-w=epsilon*(2mc+c+sigma*v)-L_kappa.

The entry gate demands 0<d<Delta. For each (kappa,sigma), there is at most ONE integer m satisfying this inequality: increasing m increases d by exactly Delta. Unless an endpoint alignment occurs, that integer is

    m = floor((L_kappa/epsilon-c-sigma*v)/(2c))+1.   (BT02)

If the expression inside this floor is an integer, the strict gate has NO solution for that branch: the adjacent choices give d=0 or d=Delta. Both correspond to a genuine reflex failure at entry or the first underside contact, not an allowed limiting state.

For native data and epsilon<1/(2c), L_kappa>=w-t>=1>Delta. Every admissible m in BT02 is nonnegative (indeed positive). Thus the entire target-reaching last-entry set contains AT MOST FOUR physical signed states, not an infinite choice of free m at fixed epsilon. The states depend on epsilon and geometry, and m is unbounded as epsilon tends to zero. This is not a finite direction list or a W-only state quotient.

### Sufficiency and true-corner guards

For every admissible (kappa,sigma,m), define x_e=w+d with d from BT01. Start there with the exact negative/downward germ NG01. The first upward c contact has phase -r+Delta in (-W,0), so it reflects on the actual underside. At each subsequent upward c contact before the target the phase is larger but still below the target phase kappa*y<W. Therefore every required ceiling contact remains strictly in (-W,W), unless its phase equals zero. There is no premature right-mouth exit.

Every floor phase before T lies between -r and kappa*y, both strictly in (-B,B). Outer-floor/roof corner phases +/-B are impossible. The only possible true corner in this episode is x=l at a floor or underside contact, namely

    r/(c*epsilon) is a positive integer k,
    contact time k*c before D.

- For kappa=-1, D*epsilon=r-y<r. The zero phase occurs AFTER the target, so no such corner is encountered. BOTH pre-turn branches are legal automatically when their strict entry states exist.
- For kappa=+1, D*epsilon=r+y>r. Here the zero lies BEFORE T, so literal legality requires r/(c*epsilon) NOT in Z. If it is an integer, the contact is the genuine convex corner (l,0) for odd k or (l,c) for even k. It must be excluded; no generic-mouth suffix repair is silently applied.

These conditions are sufficient: the rectangular folds give one common-direction physical path; every c reflection before T is on the actual underside; floor reflections are ordinary; all other reflections use the original vertical walls l,A. Target height v is interior, and the exact fold equation gives actual x=t. If an earlier actual T occurs, truncate at that earlier legal visit. No chosen target sheet is substituted independently of the actual trajectory.

Conversely, any legal final bottom episode must obey its time formula, NG01 and the two fold-image choices. The phase range excludes additional 2B windings before leaving the episode, so BT01/BT02 and the stated corner guard recover it. Thus the set described is COMPLETE for legal bottom-episode entry states reaching T before the next exit to the right, at the declared small-positive-epsilon and strict t<w hypotheses. Branches can coincide or fail strict alignment; exactly four distinct states are NOT claimed.

### BT03: the target-side gate is nonempty for EVERY small epsilon

Restrict to kappa=-1, the two automatically corner-free pre-turn branches. Their strict-alignment expressions in BT02 differ by v/c, which lies strictly between zero and one. They therefore CANNOT both be integers. At least one branch has its unique m and strict entry point; if neither expression is integral, both do. The two entry points are distinct when both exist, since coincidence would require an integer difference of m values equal to v/c.

Consequently, for EVERY 0<epsilon<1/(2c) and every actual target l<t<w,0<v<c in this integral domain, there is at least ONE exact negative-gate state whose ordinary original-wall continuation hits actual T BEFORE its first slow fold at x=l. Its at least one genuine bottom-underside return and all corner guards are proved above. This is an unconditional target-SIDE existence statement; it assumes no prior source-to-target illumination.

It does not assert that the actual source reaches that state. A nonempty backward target set and an existing source exit set need not intersect. Their position, direction, first-hit history and common epsilon must still be matched. The unbounded m has been selected exactly, not bounded away or obtained by sampling.

## 5. What this changes and what remains open

The previous accepted A/B result forces unbounded right circuits for successful normalized paths. BD01 now forces an unbounded number of genuine bottom-underside returns in the FINAL bottom episode for t<w, with NO restriction on prior history. NG01 adds a necessary opposite horizontal sign. BT01/BT02 replace an unspecified infinite final-tail choice by at most four EXACT candidate incoming states with full physical guards at each fixed epsilon. BT03 proves that the safe pre-turn target-side entry set is NONEMPTY at every such epsilon, including the strict alignment cases. This advances the route-completeness challenge; it is not merely another stopped-return formula or a new narrow room family.

The still-missing positive implication is concrete: for every unknown residual actual pair with t<w, some common epsilon and actual-source trajectory must reach one of these admissible negative-gate states, at that same position and signed velocity. The target entrance states alone do not force source access. The accepted twists provide such paths only when prior illumination is already known. Targets with t=w or t>w need separate analysis, as do the other r3 shapes and r4..8. No full native goal criterion is met.

No room/direction search, numerical example, replay, new engine, census, worker, clock renewal, frozen edit or git mutation was used. Independent review of this hand proof is requested from the existing author/coordinator, without spawning anyone. The SAME native goal is preserved; its actual observed backend state remains blocked during this explicitly authorized hand continuation.
