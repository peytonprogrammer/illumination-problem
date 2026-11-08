# FR01: original floor-return transfer and a positive narrow-arm family

Independent review pending. This uses a genuinely additional horizontal contact. It does not assert that any one-roof path survives an added floor or that the one-roof mechanism is universally available.

## 1. Exact physical floor-prefix transfer

Use the original ordered spiral, b<u<=h,0<s<a and actual bottom target t in(l,A),v in(0,c). Let f=u-b>0,d=h+u-2b=2f+(h-u)>0,C=2(H-h),g1=h-c,d2=c-v,D=d+C+g1+d2. For a positive finite horizontal slope tau, unfold the downward floor contact: let time w run0..D, and use x=F_a(s+tau*w) through w=d. The physical height on this first band is u-w for0<=w<=f and b+(w-f) for f<=w<=d. Every open-band vertical wall x0/a and the single floor yb are ORIGINAL walls; the source remains strictly below h until its final passage.

At w=d define n=floor((s+d*tau+a)/(2a)), z0=s+d*tau-2a*n. Require |z0|<a. On the next cap band of length C, use F_A(z0+tau*(w-d)), ascending from h to H and descending to h. Require z0+C*tau=(2m+1)A+z1 with |z1|<R=A-w_wall. On the right band length g1 use A-F_R(z1+tau*(w-d-C)); center its endpoint to z2 with |z2|<R. On the bottom band lengthd2 use A-F_B(z2+tau*(w-d-C-g1)), whereB=A-l. Require F_B(z2+d2*tau)=A-t.

At every strict seam the adjacent triangular folds have the same value AND signed derivative. Each open-band reflection is on an original vertical wall, and the roof/floor reverse only vertical velocity. Disjoint ascending left and descending right mouths exclude a roof corner by triangular-wave symmetry. A zero seam residual is a smooth outer-wall contact.

There is exactly ONE extra possible true corner: at the floor timef, if s+tau*f=ka for some integer k. No optical continuation through it is allowed. Instead the fold identity gives
 F_a(s+2tau*f)=F_a(2ka-s)=s.
At time2f the formal ascending curve returns to EXACT actual S. Since2f<=d, it has not entered any artificial/source-above-h band. Delete the entire formal prefix including the floor corner and EMIT its remaining regular ascending suffix from S. For u<h this return precedes the h passage; for u=h it equals that passage, whose actual S is regular. The suffix contains no floor contact, and all later guards were already proved. This is an alternative actual ray from S, not a ray traversing a corner.

If the floor contact is regular, retain the whole path. On every source-band visit to heightv the abscissa is<=a<l<t; cap/right heights are>v; the bottom band reaches v only at its end. The retained path therefore reaches FIRST actual T. Positive widths and finite tau give finitely many reflections. This proves the transfer for all stated strict portal/actual-target data, with no additional floor guard needed when the exact-S suffix is used.

## 2. A quantified positive K1 family

Normalize a=Pe,A=Ne,R=e,B=Le with integersP>=1,N>P+L,L=2^j,K1,integer e>=1. Take integer0<b<c<h, h even,c odd,H=h+1, and actual native source S=(s,u) with u=2P-h+2b in(b,h],s even in(0,Pe). Take ANY actual native bottom target T=(t,v), t even in((N-L)e,Ne),v even in(0,c). Require N odd. Then
 d=h+u-2b=2P, C=2, g1=h-c odd,d2=c-v odd,
 D=2P+2+g1+d2 is even and D>=2P+4>=6.
No geometric size, aspect or reflection bound is assumed. The source ordinate is constrained; no all-pairs theorem for these rooms is asserted.

## 3. Simultaneously avoid the source corner and cap boundary

Let z=A-t and tau_q=(A+z-s+2eq)/D for integerq>=0. The numerator is positive. Actual source-bad means s+2P*tau_q=Pe modulo2Pe. Its solution set is empty or one class with period
 pS=PD/gcd(2P,PD)=D/2>=3.
Cap-boundary bad means
 s+(2P+2)*tau_q=(N+1)e modulo2e.
Its period is pC=D/gcd(2P+2,D)>=2, because0<2P+2<D. Both periods divide D. Their combined density is at most1/3+1/2<1, so someq in0..D-1 avoids BOTH. At thatq, actual z0 is strict, and X0=z0+2tau_q is not equal to A+e modulo2e. Source centering removes multiples2Pe, hence preserves the cap-boundary congruence.

## 4. Narrow cap access, then force a right-corner-safe choice

Increase slope by e*M for integerM>=0. Since d=2P, the source index increases byM and literal z0 remains identical. The cap phase increases by2eM. Modulo2A=2Ne these are the N equally spaced points in its coset, spacing2e. The OPEN cap interval (A-e,A+e) has exactly that length. Because the coset avoids its endpoints, exactly ONE representative lies strictly inside. Choose0<=M0<N producing that representative, so the actual cap residual |z1|<e. Some actual odd branch m is then fixed. No nearest-point equality is silently accepted.

Both slopes tau0+e*M0 and tau0+e*(M0+N) retain the SAME literal source/cap residuals. The second adds2A to the cap phase, increasing the actual cap index by1. Their right pre-fold phases differ by g1*e*N, an ODD multiple ofe. Modulo actual period2e this is a half-period shift. They cannot BOTH equal the true right-corner class e modulo2e. Choose the nonbad one. Its centered |z2|<e. It is permissible that both are safe; no corner failure is needed for the argument.

The full initial target index remains integral: D is even, so addingeM changes the grid index by DM/2, an integer. Precisely
 E=z+2eJ,
 J=q+DM/2-Pn-Nm-k.
No inference from portal strictness to actual target is made.

## 5. Complete target correction by a proved weighted period

The slope increase2eN*p, with integerp>=0, changes the actual source/cap/right indices by2N*p,2p,N*g1*p respectively. Therefore all literal signed residuals stay identical. E increases by2eN*d2*p and J by N*d2*p. Since N andd2 are odd andL is a power of2, gcd(N*d2,L)=1. Choose0<=p<L solving J+N*d2*p=0 moduloL. The bottom fold reaches exactly actual t.

Apply section1 to the FINAL slope: it either has an ordinary floor or uses the exact-S suffix if the final floor is singular. No preservation of a preliminary ordinary floor is assumed. All source, cap and right corners stay excluded by their final strict residuals, the roof is regular, and actual firstT follows. This proves the stated quantified native terminal-pair family at K1.

The new input is an actual floor-return itinerary with d0floor2P, not a renamed choice of a one-roof target root. Arbitrary source heights, cap heights, N parity, bottom width arithmetic, every K1 pair, all r3 and r<=8 remain OPEN. Some rooms in this family also admit a one-roof path; that is not assumed or needed.

## 6. Prescribed controls before execution

A. e4,P3,K1,L4,N9,b1c3h4H5,S8,4,T28,2. Chooseq0,tau0=18/5,z0=28/5,capM3 givingz1=4/5,z2=2/5,E16,J1. No Nflip is needed. Finalp3 gives tau1158/5,E232=8mod32,actualT28,2.

B. Same widths, b1c3h6H7,S8,2,T28,2. Chooseq1,tau0=11/3,z0=6,capM3 givingz1=4/3,z2=1/3,E16,J1. Finalp3 gives tau695/3,E232,actualT28,2. This is a genuine lower-source native case, not only the mouth placement.

C. e2,P2,K1,L4,N7,b1c3h4H5,S2,2,T10,2. Chooseq0,tau0=2,z0=2,capM0=2,z1=0. Its right phase6 is the true corner modulo4. Use M=M0+N=9, giving slope20,z1=0,z2=0,E20,J4 and finalp0. The actual target is10. This tests the necessary Nflip and smooth outer-wall zeros; no ray through the failed first choice is retained.

D. General-transfer-only suffix control, outside the native arithmetic family: e4,P3,K1,L4,N9,b1c3h4H5,S8,4,T=(88/3,2),tau172/3. Floor time3 reaches formal corner phase180=15a. At time6 it returns to EXACT S with source residual-8. Retain only its ascending suffix. Cap/right residuals-4/3 and0 are strict, E172/3 folds to20/3,actualtarget88/3; roof phase148/3 is ordinary. The prefix is FORMAL and is not claimed as a legal path. This confirms the otherwise delicate corner-deletion branch with explicit actual target arithmetic.

No discovery search, new clock, engine, census, worker or git mutation. Prescribed arithmetic and peer physical replay are verification of stated controls, not a substitute for this hand existence proof.
