# GSE02: a joint two-image strict-window existence lemma

## General actual-pair statement

Consider any original ordered spiral, or the accepted non-overlap geometry

0<a<w<A,0<l<w,0<b<h<H,0<c<h,
a<l OR c<b,

a=Pe,R=A-w=Ke,B=A-l=Le,A=Ne,

with positive integer P,K,L,N and rational e>0, and integer vertical data. Let actual S=(s,u),0<s<a,h<=u<H and actual T=(t,v),l<t<A,0<v<c have integer heights. Horizontal marks may be rational; native even-even marks are included.

Put C=2H-h-u>0,g1=h-c>0,d=c-v>0,F=g1+d,D=C+F,z=A-t andLambda=lcm(N,K). Assume

 g=gcd(Lambda*d,L)=2G,
 G divides K,
 z/e=(2r+1)G for some integer r,
 K*D>g*C.

Then a finite ordinary actual S-to-T trajectory exists, avoiding every original corner. This is a proved joint intersection/choice result under explicit general hypotheses, not unrestricted availability. In particular g need not divideK; g=2K is allowed whenD>2C. No source-width metric condition or right-width coprimality is assumed.

## 1. Two target-compatible indices in ONE strict cap window

For initial positive horizontal direction use the root grid

 tau_q=(A+z-s+2e*q)/D, q integer.

Fix an odd-A cap centre (2m+1)A and require

 -Ke < s+C*tau_q-(2m+1)A < Ke.

Its pullback is an OPEN q interval of length KD/C, strictly greater than2G. Its centre grows linearly to+infinity with m. Choose a finite integer m>=0 so the whole interval is positive. Since A+z-s>A-a>0, all its q have positive tau.

The residue class q=Nm moduloG has spacingG. Every open interval of length>2G contains TWO consecutive such lattice points; call them q0,q0+G. They belong to the SAME cap branch m and both give a strict actual cap exit z1 in(-R,R). This is a simultaneous branch selection, not independent cap and target conditions.

Their right inputs are r_q=z1+g1*tau_q. Their exact difference is

 Delta_r=2eG(C+g1)/D.

Because0<C+g1<D andG<=K, this lies strictly between0and2eK=2R. True right-corner inputs differ by integer multiples2R. Thus BOTH candidates cannot be true corners. Choose a regular one and its actual unique centered index k, with z2=r_q-2eKk in(-R,R). Since r_q>-R, k is nonnegative. The source/cap phase is an actual upper/mouth chart; no source-arm fold is inserted aboveh.

## 2. Select the ACTUAL target image after the right state is known

Literal elimination gives

 E=z2+d*tau_q=z+2eJ,
 J=q-Nm-Kk.

Since q=Nm moduloG andG|K, J is a multiple ofG. Asg=2G, either J is0modg or J/G isodd. In the latter case z/e/G isodd, so J+z/e is0modg.

Thus ONE of the two integer target indices

 J_same=J,
 J_opposite=J+z/e

is g-divisible. The first represents actual image+z; the second represents actual image-z. This after-selection retarget is essential: separately trying two initial image grids does not replace it.

Change the slope by2eLambda*p. The cap branch changes by C*Lambda*p/N and the right branch by g1*Lambda*p/K, both integers. Therefore the EXACT signed residuals z1,z2 stay fixed. The root index changes byD*Lambda*p and J changes byLambda*d*p. Solve

 J_selected+Lambda*d*p=0 moduloL.

A solution exists becauseg=gcd(Lambda*d,L) dividesJ_selected. Choose its least nonnegative residue moduloL/g. All initial q,m,k andtau were nonnegative/positive, and every increment is nonnegative, so the corrected direction stays physical. The SAME selected actual image remains compatible because the index increment is divisible byg. The final phase is+z or-z moduloTRUEperiod2B, hence the endpoint is EXACT actualT. No half-period or sheet projection is used.

This constructs ONE finite direction and coherent fold indices for the whole path. It is not concatenation of independently tuned rays.

## 3. Original finite-wall and corner guards

Aboveh the cap is the genuine rectangle bounded by x0,A and roofH. The source begins at its actual position with velocity(tau,+1), including the regular mouthu=h. The descending h exit has x=A-|z1|>w, so it continues in the true right strip. Right-side reflections lie on actual xw/A at c<y<h. Its strict c state excludes(w,c); zero residuals are smooth outer-wall contacts, not vertex continuations.

The bottom rectangle [l,A]x[0,c] is genuine: if l<a,the separation hypothesisc<b puts the source column strictly above it. Its full width isB, and |z2|<R<B makes the initial position and signed horizontal derivative agree with the right chart. The final descent reaches heightv at its endpoint; cap/right portions are abovev. All mirror intervals are finite original walls. The extra original left reflex(a,h) cannot be hit on the descending h exit because x>w>a; it is not crossed on the earlier cap segment, which stays aboveh.

Inspect the FINAL roof phase. If it is ordinary, keep the full path. At u=h a roof corner would identify disjoint left and right h mouths, impossible. At u>h a formal roof corner returns EXACT originalS after2(H-u), with opposite horizontal direction and downward vertical velocity. This return is BEFORE the h exit because C-2(H-u)=u-h>0. Discard the singular prefix and emit only that regular suffix. It retains the SAME strict z1,z2 and final actualT. No arbitrary continuation through a corner is allowed.

Finite positive times, tau and widths give finitely many ordinary specular contacts. The endpoint is the actual firstT after the optional exact-S suffix because all prior retained portions are abovev and the bottom first reachesv at its endpoint.

## 4. Exact general application to the fixed-seed countercontrol

This application demonstrates a change of optical direction/representation that bypasses the accepted repair obstruction; it is NOT a new fixed-height family research programme.

In the peer countercontrol P=2^p,p>=5,K=P+1,N=5K,e2,L=2P, the original dimensions are a=2P,R=2K,B=4P,A=10K,b1,c3,h4,H5 and actualS=(2,2),T=(A-2,2).

Swap BOTH coordinates of the entire room and reverse endpoint order. The exact transformed parameters are

(a*,l*,w*,A*,b*,c*,h*,H*)
=(3,1,4,5,6P+10,2P,8K,10K).

This is the accepted separated geometry: a*3<w*4<A*5,0<l*1<w*,c*2P<b*6P+10, and both lower heights are<h*. The transformed actual source is S*=(2,10K-2), an interior upper-cap mark; transformed target T*=(2,2) lies in its actual bottom chamber. Sete*=1,P*=3,K*=1,L*=4,N*=5. Then

 C*=2K+2, d*=2P-2, D*=10K,
 Lambda*=5, g*=gcd(5*(2P-2),4)=2=2K*,
 z*/e*=3, K*D*=10K>2(2K+2)=g*C*.

All hypotheses of the GENERAL lemma hold for every p>=5, with no sample bound. The lemma gives a legal actual S*-to-T* path. Swap its entire ray back and reverse it to get an actual original S-to-T path. A global Euclidean isometry and reversal preserve every finite wall, corner and specular law; no cutting/gluing or altered endpoint is involved.

Thus the countercontrol remains a correct failure of fixed-state repair, but its ACTUAL pair illuminates by this different programme. This is a concrete optical consequence of the new general joint-image lemma, not a criterion restatement.

## Universal frontier and validation scope

The hypothesesg=2G,G|K,z/e/Godd andKD>gC are explicit remaining restrictions. They are not proved automatic for all ordered spirals. Cases with more than one unresolved target-index bit, noncommensurable image grids, or insufficient strict-window length remain part of the universal availability task. General first-return programmes with repeated genuine notch contacts remain under investigation.

No numerical checks, new search, engine, census, worker, frozen edit or git mutation was used. The argument is a quantified hand proof. Independent review is required, especially after-selection retargeting, the common m/residue choice, the FINAL direction and the separated-geometry application. Full ordered-spiral, allr3 andr<=8 goals remain open.
