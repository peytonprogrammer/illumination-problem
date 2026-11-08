# LC03: target-compatible first crossing on a reduced grid

Independent review pending. The peer originated LC01R; its reciprocal hand acceptance is in construction/three-reflex-coprime-extension-forward-refined-review.md/.json. The extension below proves its offset variant explicitly rather than applying a theorem outside its cap integrality hypotheses.

## Statement and common physical geometry

Use LC03 candidate's original ordered spiral and terminal actual S,T. Retain a=Pe,A=Ne, right widthKe,bottom widthLe, the accepted d0,C,g1,d2,D,z, Lambda=lcm(P,N,K),g=gcd(Lambda*d2,L). Assume g|P,g|K,K>=2g. Put eprime=eg,Pprime=P/g,Kprime=K/g. All vertical data remain integral. Pprime>=1,Kprime>=2. Original A need NOT be an integer multiple of eprime; no such premise is used.

## Choose the cap center before the target residue

For any residue r in{0,...,g-1} set
 tau_r(0)=(A+z-s+2er)/D.
Its value is positive and at most tau_max=(A+z-s+2e(g-1))/D. Centering the lower source gives z0<a; for u>=h, z0=s<a. Thus ALL possible initial X_r(0)=z0+C*tau_r(0) are strictly less than B=a+C*tau_max.

Let rho=2eprime*(d0+C)/D<2eprime. Choose integer m>=0 so that
 U=(2m+1)A+Ke > B+4rho.
Such m exists because A>0. Now define r as the least nonnegative residue Nm modulo g. There is no circularity: B did not depend on m or its residue. Work only on
 q=r+gj, j>=0,
 tau(j)=tau_r(0)+2eprime*j/D.
The candidate cap window is (U-2Ke,U), with FIXED m throughout.

## Source reset and corner events in the j variable

Below h, use actual centering n=floor((s+d0*tau+a)/(2a)); above/at h put n=0,z0=s. Let X=z0+C*tau. It tends to infinity; each increment is at most rho, since n is nondecreasing. Let j* be the FIRST j with X>=U. The uniform bound forces j*>4. Every previous j*-i is below U, and at least U-i*rho.

Below h, actual source-bad means s+d0*tau=a modulo2a. Its solutions are empty or a single class modulo
 pS=Pprime*D/gcd(d0,Pprime*D)>Pprime.
At a source-bad index exactly one source reset occurs, because0<2eprime*d0/D<2a. Hence deltaX=rho-2a<0, so j* is source-good.

Use the sufficient right exclusion
 s+(D-d2)*tau-(2m+1)A=Ke modulo2eprime.
The event has empty solution set or a single class of period
 pR=D/gcd(D-d2,D)>=2.
Its offset depends on m. Nothing replaces this offset by A. For a selected cap index the actual pre-right phase is
 Y=s+(D-d2)*tau-2Pe*n-(2m+1)A.
The removed source term is a multiple2eprime because g|P. Also2Ke is a multiple2eprime because g|K. Consequently avoiding the stated sufficient event excludes the actual Y=Ke modulo2Ke. This remains valid for varying n.

## A strict compatible candidate always exists

For lower sources repeat the LC01R reset proof on THIS j grid:

* If pR=2, D-d2=D/2 and d0+C<D/2. Therefore rho<eprime; four predecessors fit into the strict cap window, whose width2Ke=2Kprime*eprime>=4eprime. Source period cannot be2. One class period2 and one period>=3 leave a survivor among four consecutive indices.
* If pS=2, Pprime=1,d0=D/2 and C<D/2. Source residual repeats every two j, while X increases by4eprime*C/D<2eprime. The source-good j* implies source-good j*-2,j*-4, both in the strict window. Their distance2 prevents pR>2 from rejecting both.
* Otherwise pS,pR>=3. The last two predecessors are cap-interior. If both are bad, they are one source and one right event. At least one reset occurs between j*-3 and j*, giving X(j*-3)>=U-3rho+2a>U-4eprime. Firstness supplies X<U. Distances1and2 from the two bad indices imply j*-3 avoids both.

Empty event classes can only ease these choices; their possible period formula remains valid. For u>=h no source event exists. The last two predecessors lie strictly inside the cap window, and the one right class cannot kill both since pR>=2. This proves ALL source heights.

Thus some q=r+gj has strict |z0|<Pe, |z1|<Ke, |z2|<Ke at the same m, where z1=X-(2m+1)A. A zero residual is a smooth outer-wall reflection.

## Match the entire actual target

The initial grid still gives exactly
 E=z+2eJ, J=q-Pn-Nm-Kk.
Because q=Nm modulo g and g divides P,K, the selected J is divisibleg, independently of source/right indices. Solve
 J/g + (Lambda*d2/g)*p=0 modulo L/g
with0<=p<L/g (p0 for modulus1). The coefficient is a unit by definition of g. The slope shift2eLambda*p preserves all three literal signed residuals: source/cap/right index shifts are Lambda*d0*p/P, Lambda*C*p/N, Lambda*g1*p/K. Therefore E=z modulo2Le and the bottom fold reaches exactly t.

Apply the accepted original physical band proof with these strict residuals. It matches position AND signed velocity at both original passages; all actual left/right reflex corners are excluded. Lower-source roof symmetry would equate disjoint mouths. An upper-source formal roof corner may be deleted only with the accepted EXACT-S descending suffix; the retained path traverses no such corner. The target is the original T, first reached at the final height by the accepted height/abscissa separation. There are finitely many original-wall reflections at one finite positive slope. No artificial cut is reflected, no target sheet changed, and no different directions concatenated.

## Whole native family and scope

Let e integral>=1,L=2^j,Nodd,N>P+L,codd,ANY ordered integral0<b<c<h<H,2<=K<L. Suppose v2(P)=v2(K)=nu and oddpart(K)>=3. At every native terminal pair v is even, so d2odd and
 g=gcd(Lambda*d2,L)=2^nu.
It divides P,K and K/g=oddpart(K)>=3>2. LC03 covers every terminal source height. The accepted TR01/TR05 placement join and reversal cover all other native pairs. This removes K|P from LC02: P,K need share only their exact power of2, with otherwise independent odd factors.

For general target arithmetic, the terminal theorem also permits K/g=2, although the stated power-two-bottom family has odd K/g. There is NO requirement that g divide N or that A/eprime be integral. Cases g not dividing P or K, reduced K/g<2, other ordered spiral forms, the other r3 turn types and r4..8 remain OPEN. This is neither a universal theorem nor a dark-room assertion.

## Three prescribed checks declared before execution

A: e2,P10,K6,L8,N23,b1c3h6H23,S4,4,T34,2. Lambda690,g2; K does not divide P. Uniform m1,r1 works. In j units X=(281+36j)/5 until crossing j*14. Choose j13/q27: tau81/20,z0=121/10,z1=59/5,z2=-1/20,J-2. Final p1 gives tau55281/20,J688,actualT34,2. The target gcd is2 with z/e6 even, outside the earlier uniform target-orbit criteria.

B: e2,P2,K4,L10,N17,b1c5h6H7,S2,2,T22,4. Lambda68,g2,Kprime2,Pprime1 and pS2. Uniform m0,r0; j*16. Choose j14/q28: tau39/2,z0=0,z1=5,z2=-15/2,J0,p0. Source bad indices are odd j; j* is source-good. The smooth zero source residual is permitted.

C: e2,P2,K4,L14,N19,b1c7h8H9,S2,6,T18,2. Lambda76,g2,Kprime2,pR2. Uniform m0,r0; j*22. Choose j21/q42: tau112/5,z0=-6/5,z1=28/5,z2=-4,J22. Right strong bad indices are even j. Target correction p3 gives tau4672/5,J1162,actualT18,2.

Only the fixed published controls and symbolic identities will be checked; no numerical quantifier proof, discovery search, new clock, census, worker or engine.
