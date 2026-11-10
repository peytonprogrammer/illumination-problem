# Proposed proof: coprime cap periods and target parity

Same geometry and scope as coprime-candidate.md. All integers and finite choices below are per-input. This proof does not depend on a monotone slope update.

## 1. Select a target-compatible slope grid

Write d0=h-u>=0, G=2(H-h)>0, g1=h-c>0, d2=c-v>0 odd, D=d0+G+g1+d2=2H-u-v, z=A-t in (0,2a). These developed heights are integers. At the initial slopes

    tau_q=(A+z-s+2a q)/D, q in Z,

one has s+D tau_q-A congruent z modulo2a. We will preserve this relation. In particular tau_q>0 for q>=0.

Let t1=d0, t2=d0+G, t3=D-d2. The three events to avoid are

    s+t1 tau_q = a                 (mod 2a),
    s+t2 tau_q-A = a               (mod 2a),
    s+t3 tau_q-A = a               (mod 2a).

The first is the source-arm top corner. The second means the cap orbit lies exactly on the endpoints of its width-2a return window. The third is the right-arm bottom corner. This second exclusion is sufficient for the forthcoming cap selection; it does not assert that all current q already cross the cap correctly.

If t1=0, the first equation has no solutions because 0<s<a. Each other equation defines either no integers q or one residue class modulo m_i=D/gcd(t_i,D)>=2: subtracting two instances gives t_i(q-q') divisible by D. The nonzero times are strictly ordered and belong to (0,D), so no two have m_i=2.

## 2. Three such classes cannot cover all integers

Elementary covering fact: three single residue classes with moduli >=2 can cover Z only if two moduli equal2, or all three equal3, or their multiset is (2,4,4). To see this, order moduli. Minimum>=4 has total density<=3/4. Minimum3 requires all3 by density. With minimum2 and second>=5 the density is<1. With second4 the third must4. With second3, the first two overlap with density1/6 and cover only2/3; a third modulus>=4 is insufficient. A second modulus3 gives at most5/6 coverage for the three classes together. Fewer than three classes are covered by the same argument.

Two2s are impossible since their times would both equal D/2. Three3s are impossible since only D/3 and2D/3 are possible nonzero times with that modulus. In the remaining (2,4,4) pattern, strict order forces

    t1=D/4, t2=D/2, t3=3D/4.

Thus G=t2-t1=D/4 and d2=D-t3=D/4, contradicting even G and odd d2. If t1=0 there are at most two classes with distinct nonzero times, which cannot cover either.

Consequently some q in 0..D-1 avoids all three events: each forbidden modulus divides D, so their union is D-periodic. Choose any such q and put tau0=tau_q.

## 3. Enter the strict cap window by a finite coprime rotation

Let n=floor((s+d0 tau0+a)/(2a)) and z0=s+d0 tau0-2na. The first exclusion gives |z0|<a (including d0=0).

Replace tau0 by tau=tau0+2aM. Since d0 is integral, z0 remains unchanged, with n increased by d0M. The developed cap phase is X=z0+G tau. As M ranges0..N-1, X modulo2A visits all N points of one lattice coset with spacing2a, because gcd(G,N)=1 and 2A=2Na.

The open cap window is X=(2m+1)A+(-a,a), modulo2A. It has length2a. The second exclusion says the phase coset does not meet its endpoints. Exactly one of the N points is therefore strictly inside this window. Choose its M and m, and set z1=X-(2m+1)A, so |z1|<a.

At the right-arm bottom let k=floor((z1+g1 tau+a)/(2a)), z2=z1+g1 tau-2ka. Modulo2a, this phase equals s+t3 tau-A. The third exclusion remains true after the slope shift, because t3 is integral. Thus |z2|<a.

## 4. Fix target parity without losing any portal

All three relevant widths are now a, A=Na, a, 2a. Expanding the formulas gives

    E=z2+d2 tau
     =s+D tau-2na-(2m+1)A-2ka
     =z+2a J

for an integer J, since s+D tau-A is congruent z modulo2a.

If J is even, E=z modulo4a already. If J is odd, increase tau by2aN. The source residual is unchanged (n increases by Nd0). The cap phase increases by2aNG=2AG, so m increases by G and z1 is unchanged. The right phase increases by2aNg1, so k increases by Ng1 and z2 is unchanged. Finally E increases by2aNd2. Because N and d2 are odd, this flips J parity. After at most one such shift, E=z modulo4a, hence F_(2a)(E)=z, where F_L(x)=distance(x,2L Z).

This matches actual t=A-z. It is not target projection or an approximation. All choices are finite and tau>0. Unlike TR06, there is no fixed-point or global-monotonicity assertion.

## 5. Actual optical trajectory

Use developed height eta from u to2H-v, and fold actual height at H. The four consecutive bands have x coordinates

    u..h:           F_a(s+tau(eta-u)),
    h..2H-h:        F_A(z0+tau(eta-h)),
    2H-h..2H-c:     A-F_a(z1+tau(eta-(2H-h))),
    2H-c..2H-v:     A-F_(2a)(z2+tau(eta-(2H-c))).

The first band is empty if u=h. Its endpoint agrees with the cap because z0=s in that case. Every other interface agrees locally, including signed velocity, by subtraction of the even source/right periods or the odd cap multiple A. A zero portal residual is one smooth outer-wall contact, not a corner or an artificial reflection. Strict bounds exclude (a,h), (w,h), (w,c) and the ledges.

Every open-band vertical mirror is genuine: x=0,a at heights between u>b and h; x=0,A above h; x=w,A between c and h; x=l,A below c. The original mark positions are interior. There are finitely many fold cusps since all widths, times and tau are finite.

A roof corner would make the cap triangular-wave phases at h and2H-h symmetric about a cusp and hence their x coordinates equal. The first lies in [0,a), the second in (w,A], so equality is impossible. Thus the sole roof reflection is smooth. All reflection velocities satisfy the specular law. The final point is actual T by section4. On the ascending part x<a whenever its height could be v<c, so it cannot reach T with t>l earlier. The descending part meets height v only at its end. This proves the lemma, subject to independent audit.

## 6. Entire thin-cap native-pair family

Take a,N,b,c,h integers, 0<b<c<h, N>=5 odd, c odd, H=h+1. Then G=2 and gcd(G,N)=1. Any actual even-even mark in the left terminal has b<u<H and u integral, so u<=h. Every bottom mark has v even and c-v odd. Hence all residual terminal pairs satisfy the lemma, including u=h.

For completeness, accepted TR01 protected U/L coverage covers all other pairs. In the present cap there are no integer-height interior marks with h<y<H. Thus every native mark is in G or int(R) in TR01; a pair outside both its same-region cases consists of a left terminal mark and a bottom mark (possibly with labels reversed). The lemma covers exactly these. Reversing a finite regular specular path is legal.

This gives ALL distinct actual interior even-even pairs in this variable-size ten-wall family. It is not an arbitrary-real endpoint result or a complete ten-wall theorem. No independent acceptance is claimed yet.
