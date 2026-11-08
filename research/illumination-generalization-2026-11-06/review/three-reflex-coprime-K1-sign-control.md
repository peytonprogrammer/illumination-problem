# K1 exact native control: one entire seeded grid fails; the other reaches T

Reviewer hand deduction and prescribed exact replay. This is NOT a dark room, not a counterexample to LC01R (which assumes K>=2), and not a universal two-sign theorem.

Use e4,P3,K1,L4,N9,b1,c3,h5,H7. Thus a12,l20,w32,A36 and the original room boundary is

    (12,1),(12,5),(32,5),(32,3),(20,3),
    (20,0),(36,0),(36,7),(0,7),(0,1).

The polygon is strictly simple, orthogonal with ten maximal walls and three reflex corners. The specified actual interior native marks are S=(6,6), T=(30,2). All coordinates are integral; both marks are even-even and distinct. This is a qualifying room for the goal, but its explicit ray proves it illuminates this pair.

Here d0=0,C=3,g1=2,d2=1,D=6,z=A-t=6. Lambda=lcm(P,N,K)=9 and gcd(Lambda*d2,L)=1. Thus target coprimality alone is no obstruction.

## Entire positive-z grid fails the actual corner guard

The initial positive-image grid is

    tau_q=(A+z-s+2eq)/D=6+4q/3, q>=0 integer.

For any odd-A cap branch m the phase is X=6+3tau_q=24+4q. Strict cap access is

    |X-(2m+1)36|<4,
    equivalently |q-3-18m|<1.

Since q,m are integers, strict access forces q=3+18m. For q>=0 these branches have m>=0. At EVERY such q,

    tau=10+24m, z1=0,
    Y=z1+g1*tau=20+48m=4 modulo8.

This is precisely the genuine right/bottom reflex corner (w,c)=(32,3), where |z2|=4. No legal ray is supplied by ANY integer q in this positive-z one-roof grid. This proves failure of an entire prescribed grid family, not merely a chosen ray. It says nothing about other grids, roof counts or optical words. Final Lambda shifts retain this bad residual and cannot repair it.

## Negative-z seed supplies a legal actual ray

Start instead with the independent grid

    tau_q=(A-z-s+2eq)/D=4+4q/3.

At q4 choose tau0=28/3. Then X34 at m0 gives z1=-2; Y=50/3, k2 gives z2=2/3. Therefore E=z2+d2*tau0=10=-z+2e*J with J2. Solve J+9p=0 mod4 using p2, giving

    tau=28/3+2e*9*2=460/3,
    m6,k38, z1=-2,z2=2/3,
    E=154=-6 modulo32.

The full bottom fold F_16(E)=6 gives actual x=36-6=30. Both portals are strict. The final formal roof phase6+(460/3)(7-6)=478/3 is not a multiple of36, so the single roof contact is ordinary. The accepted original cap/right/bottom signed charts provide a legal path; the independent earliest-wall replay checks the path directly, including every true corner and first actual T.

## Consequence for the remaining proof obligation

The K>=2 restriction in LC01R cannot be removed by asserting that its same positive-image grid always contains a good cap/right choice at K1. Even with native even-even endpoints and target gcd1 that assertion is false. An extension must use another mechanism, such as the independent negative-image seed here, and prove availability across its actual simultaneous guards. This control does not prove all K1 rooms or all ten-wall rooms. It preserves the distinction between grid failure and physical darkness.
