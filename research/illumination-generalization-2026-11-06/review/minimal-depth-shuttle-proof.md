# R45: explicit width tails in the minimal-depth h2 B/C families

Author proof pending independent review. Conservative original start06:52/deadline07:06Z includes initial symbolic shuttle reasoning. Universal canonical45W21 remains OPEN.

## Statement and exact residual region

Fix D in{0,1,2}. The core is[0,1]x[0,G]. Selected RIGHT teeth have width D+1 and height2 bands[mu-3,mu-1],[mu+1,mu+3], with actual common-depth marks S=(1+D,mu-2), T=(1+D,mu+2). Opposite LEFT teeth include a floor-flush band[0,2] of arbitrary positive width f, and a central band[mu,mu+2] of integer width w>=1. Use one of:

* B: mu4,G8, no roof-flush tooth.
* C1: any integer mu>=4,G=2mu+2, plus a roof-flush tooth[G-2,G] of arbitrary positive width g.
* C2: any integer mu>=5,G=2mu, plus the same roof-flush tooth.

All same-side bands have positive gaps; opposite overlaps are permitted. These literal rooms have18 or20 maximal walls. The selected points are actual interior midrow marks; original integer translations may make their names even-even A points. No claim that they are the only A points is made. The unused flush widths f,g vary independently without an upper bound, and may even be positive real numbers.

The selected pair illuminates for EVERY stated mu and f,g whenever the central INTEGER width satisfies

    D0: w>=13;     D1: w>=20;     D2: w>=67.           (1)

No starting witness or propagation assumption is used. The smaller w prefixes remain open in this packet; previously accepted unitwidth certificates do not automatically cover their arbitrary flush widths.

## 1. Choose an exact winding phase

Let a_D=5 forD0/1, a_D=6 forD2. We choose j=k+1 positive integer with

    tau=2j/(w+a_D)

in the following STRICT interval:

| D | Allowed tau | Allowed j interval | Its length |
|---|---|---|---|
|0| (2/7,2/5) | ((w+5)/7,(w+5)/5) | 2(w+5)/35 |
|1| (1/4,1/3) | ((w+5)/8,(w+5)/6) | (w+5)/24 |
|2| (2/9,1/4) | ((w+6)/9,(w+6)/8) | (w+6)/72 |

Each length is STRICTLY greater than1 under(1). Taking j=floor(lower endpoint)+1 therefore gives a strict interior integer, including when the lower endpoint is integral. This proves existence uniformly over unbounded w, not a sampled residue statement. k=j-1>=0.

## 2. The actual selected-source arm and four core mirrors

Start fromS with velocity(+1,tau), reflect at its actual far point

    (D+2,mu-2+tau).

This is a strict source far-wall point. Its source-mouth exit at x1 has ordinate mu-2+(D+2)tau, strictly below mu-1 because (D+2)tau<1 in every stated interval. The arm stays inside the actual minimal-width tooth with no horizontal-wall contact.

Continue through the following FOUR actual core mirrors:

    L1=(0,mu-2+(D+3)tau),
    R1=(1,mu-2+(D+4)tau),
    L2=(0,mu-2+(D+5)tau),
    R2=(1,mu-2+(D+6)tau).

Both left turns lie strictly in(2,mu). The lower bound follows from mu>=4 and tau>0. The upper bound follows from(D+5)tau<2, using respectively tau<2/5,1/3,1/4. Thus neither arbitrary-width floor-flush tooth nor the central tooth removes a left mirror. Both right turns lie strictly in the selected gap(mu-1,mu+1), since(D+4)tau>1 and(D+6)tau<3. Their initial and final velocities alternate horizontal sign with the same upward component.

The next segment enters the central left tooth at x0 and ordinate

    P1=mu-2+(D+7)tau.

Its lower bound is precisely the strict lower tau bound: (D+7)tau>2. Its upper bound(D+7)tau<4 is immediate in all three intervals. Hence P1 is a strict actual mouth point in(mu,mu+2). The roof-flush tooth starts strictly above mu+2 in both C families and cannot affect any of these core contacts.

## 3. A genuine middle-tooth excursion with EVEN horizontal bounces

Put B_D=3 forD0, B_D=D+1 forD1/2, and prescribe the exit

    P2=mu+2-B_D*tau.

It is strictly inside(mu,mu+2). The selected winding equation is

    P1+2w*tau = P2+4k,                               (2)

because D+7+B_D+2w equals2(w+a_D), and tau=2(k+1)/(w+a_D). In the actual tooth, develop horizontal distance r in[0,2w] with physical x=-r forr<=w, x=r-2w forr>=w. Fold the increasing height phase P1-mu+tau*r into[0,2] modulo4.

Equation(2) makes the exit phase P2-mu+4k, so the exit vertical velocity is UPWARD, matching the core. There are exactly2k ordinary horizontal-wall reflections and one actual far reflection atx=-w. All horizontal contacts have strict depth between0 andw; strict portals exclude contacts at either open mouth.

The far phase relative to mu is

    beta_D*tau+2k,   beta_0=2, beta_1=beta_2=3.

This lies strictly between consecutive nonintegral bounds: beta_0*tau in(4/7,4/5), beta_1*tau in(3/4,1), beta_2*tau in(2/3,3/4). It is NONINTEGER. In particular it is not an even integer, the only way a horizontal-wall collision could coincide with the far wall. Thus every middle excursion is an actual finite corner-avoiding path; no open-mouth reflection or fictitious periodic return is inserted.

## 4. Actual target completion

ForD1/2, leave the middle mouth(0,P2) toward the actual mark(1+D,mu+2). The horizontal distance isD+1=B_D, so the slope is exactlytau. At target mouthx1 the ordinate is mu+2-D*tau, strictly in the target band; the remaining actual target arm is straight and reaches ORIGINALT before its unused far end.

ForD0, leave(0,P2) toward the ACTUAL upper selected far point(2,mu+2-tau), reflect vertically there, then reach actual seamT=(1,mu+2). The target-mouth entry atx1 is mu+2-2tau, strictly above mu+1 because tau<2/5<1/2. The far point and the final arm are strict within the original target tooth. No actual seam is used as a mirror.

All non-middle core legs are open in0<x<1. Middle horizontal folds stay inside that actual tooth. No floor or roof reflection is used. Original target is reached first: all source-arm points have y<mu-1, all core points before entry remain outside the target abscissa/band, the middle arm has x<=0, and the final selected target arm reaches its actual mark with the stated strict entry. Reflection counts are7+2k forD0,6+2k forD1/2.

This proves every unbounded width tail in(1), uniformly in mu and independent flush widths. It closes no smaller-w member by inference, supplies no all-comb theorem, and does not change the native goal's unfinished status. It is a direct witness-existence result for a disjoint portion of the three minimal common-depth configurations left by R43.
