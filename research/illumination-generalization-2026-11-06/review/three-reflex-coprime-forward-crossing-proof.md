# LC01 hand proof: one-sided increment forces a guarded cap window

Status: reviewer-originated proof awaiting independent author challenge. No finite sample establishes these quantifiers.

## 1. Exact phase growth despite source folds

Take the candidate hypotheses and notation. For every integer q>=0 the slope tau(q)>0. Define n,z0,X as in the candidate even at algebraically bad endpoint indices; such indices are used to locate a window, not as legal rays.

The centered floor guarantees -Pe<=z0(q)<Pe. Since tau(q) tends to infinity and C>0, X(q)=C*tau(q)+z0(q) tends to infinity. Because tau increases and d0>0, n(q+1)>=n(q), so

    X(q+1)-X(q)
      =2e(d0+C)/D - 2Pe*(n(q+1)-n(q))
      <= 2e(d0+C)/D = hstep < 2e.

There is no claimed lower increment bound or monotonicity. The strict inequality follows from D=d0+C+g1+d2 with g1,d2>0.

## 2. A whole block inside one physical cap window

Choose an integer m>=0 with U=(2m+1)A+Ke > X(0)+K*hstep. Define q* as the FIRST nonnegative integer for which X(q*)>=U. Existence follows from unbounded growth. Repeated upper increment bounds give X(j)<=X(0)+j*hstep<U for 0<=j<=K, so q*>K.

For every j=1,...,K, firstness gives X(q*-j)<U, and telescoping the upper increment bound gives

    X(q*-j)>=X(q*)-j*hstep>=U-j*hstep>U-2Ke.

Thus the K consecutive positive indices q*-K,...,q*-1 have cap phases strictly in the SAME physical open interval ((2m+1)A-Ke,(2m+1)A+Ke). Equalities at the threshold q* cause no problem: q* itself is discarded. Source-fold backward jumps do not invalidate either inequality. The odd center and its m are common to every retained candidate.

## 3. Four consecutive indices cannot all be bad

For the initial source strong bad event, time is d0; for the right strong bad event, time is D-d2. Each time is strictly between0 and D. For rational offsets an event is empty or one integer residue class with period D/gcd(time,D)>=2. The times are distinct because their difference is C+g1>0, and both periods cannot be2: that would force both times=D/2.

An elementary local noncover lemma applies to ANY four consecutive integers. If neither period is2, each class contains at most two of the four; containing two requires period3 and those two must be the first and last. Two such classes cannot supply four distinct members. If one period is2, it supplies precisely the two integers of one parity. The other class, of period>=3, cannot supply both remaining integers, whose difference is2. Empty events are easier. Hence the union misses at least one index in every four-block.

Since K>=4, choose one such good q in the preceding block. The strong source event excludes both actual endpoints modulo2Pe and gives |z0|<Pe. The cap interval already gives |z1|<Ke, where z1=X-(2m+1)A. The strong right event implies |z2|<Ke after folding z1+g1*tau by2Ke, because 2Pe*n and2Ne*m are multiples2e.

## 4. The actual target correction and original walls

The seeded slope gives E=z2+d2*tau=z+2eJ with J=q-Pn-Nm-Kk integral. Set Lambda=lcm(P,N,K), and choose0<=p<L such that J+Lambda*d2*p=0 mod L. The candidate target gcd ensures existence. Add2eLambda*p to tau and respectively add (Lambda/P)d0*p,(Lambda/N)C*p,(Lambda/K)g1*p to n,m,k. All increments are integral and preserve the THREE literal signed residuals z0,z1,z2. The final bottom fold is exactly z, so actual x=t. The final slope is positive and finite.

Apply the accepted original source/cap/right/bottom band charts from CE04 at THIS final slope. Both adjoining position and signed velocity match at every portal; endpoint residuals are strict, zero residuals are smooth wall hits. Every reflected wall belongs to the original room. The lower source stays above b, and the bottom descent stays above0. The lower-source roof-corner impossibility uses the ascending h mouth x<a and descending h mouth x>w, disjoint since a<l<w; thus no roof suffix repair is needed in this lower-only lemma. The actual target height occurs on descent only at the end; ascent below h has x<a<l<t. This is one finite ordinary specular ray to first actual T, not concatenated directions or an artificial-wall transfer.

## 5. Whole native family and exact limits

In the candidate native corollary, native v is even and c is odd, hence d2 is odd. Odd P,N,K make Lambda odd, so gcd(Lambda*d2,2^j)=1. Every below-h terminal source satisfies LC01. Every at/above-h terminal source satisfies announced CE08 with Lambda_cap=lcm(N,K) odd,g=1 and K>=5; CE08 must be independently accepted before claiming the combined corollary as reconciled. TR01/TR05 already cover every complementary placement in this ordered spiral; reversal exchanges labels. All hypotheses are pointwise for unbounded integer room metrics. This proves the proposed family conditional on reciprocal LC01 review and final CE08 acceptance, not all W10 or r<=8.

The remaining general lower-source K=2,3 and arbitrary target arithmetic are not resolved. Neither failed earlier gcd hypotheses nor this sufficient proof imply darkness in their complements. Other spiral forms and r3 types remain open.
