# Exact null-fiber audit for a proposed general right-window selection

This is an exact constraint on one fixed source/cap seed and its target-grid-preserving continuation. It is neither a universal existence theorem nor a claim that failure of this continuation excludes other seeds or itineraries.

## Set-up

Use lower band times X,C,F=G+d,D=X+C+F and a=Pe,A=Ne,R=Ke,B=Le. Let g be a positive integer and begin with an actual source/cap-strict seed

q=Pi+Nm+gj,
tau=(A+epsilon*z-sigma*s+2eq)/D,
z0=sigma*s+X*tau-2Pe*i,
z1=z0+C*tau-(2m+1)A,
r=z1+G*tau.

No g|K is assumed. Choose eta=g/gcd(g,K). In order that J=gj-Kk be g-divisible, it suffices and is equivalent, within this q-grid, to select an actual right index k in eta Z.

## ALL-real preserving subgroup for this nominated grid

A real slope increment 2e*delta preserves the literal z0,z1 and the integer i,m,j grid exactly when

    X*delta/P, C*delta/N, F*delta/g are all integers.

Let H=gcd(NgX,PgC,PNF). The exact subgroup of such delta is

    (PNg/H) Z.

This is not an arbitrary integer-period suborbit. Integrality of each displayed increment proves one containment. Conversely Bezout on NgX,PgC,PNF expresses H; multiplying by delta/(PNg) expresses delta*H/(PNg) as an integer combination of the three required integers. Hence it is an integer, proving the other containment. The generator may be rational; do not silently drop fractional nulls.

The right input changes by 2e*q0 per null, q0=GPNg/H. Target-compatible right indices have center spacing 2e*K*eta. Thus the exact normalized additive mesh is

    rho=gcd(GPNg,K*eta*H)/H,

where the numerator is the ordinary integer gcd. In particular

    q0 Z + K*eta Z = rho Z.

For THIS seed, existence of a strict right guard with k in eta Z along this entire preserving subgroup is EXACTLY

    dist(r/(2e), rho Z) < K/2.                 (NF)

Indeed r/(2e)+q0*n-K*eta*k' runs over r/(2e)+rho Z. This gives both directions, including all signed null integers and all right-index centers. Positivity can be restored by positive common returning periods once a strict state exists.

## Consequences for completeness

- rho<K guarantees NF for every offset by nearest rounding, including ties because rho/2<K/2.
- rho=K requires excluding the exact half-mesh offset; a non-strict bound is insufficient.
- rho>K permits missing cosets. It does not imply this actual seed's coset misses, and does not exclude a different seed.
- P<=K alone does NOT prove rho<K. AP07 succeeds under an explicit stronger gcd calculation; that calculation cannot be erased when stating a general theorem.
- This is a continuation on the selected q-grid. It is not a characterization of all straight rays or all ways of changing the earlier source/cap residuals inside their windows.

## Actual target correction must also be audited

If g is chosen as gcd(Lambda*d,L) with Lambda=lcm(P,N,K), then after selecting strict z2 and k in eta Z the physical target discrepancy J=(z2+d*tau-epsilon*z)/(2e) is integer and g-divisible. A common PHYSICAL shift 2eLambda preserves the actual source/cap/right fold states and increments J by Lambda*d. Therefore solve J+Lambda*d*p=0 modulo L and restore positive actual indices by adding multiples of L/g.

Do not require the auxiliary j-coordinate to remain integer under every later physical shift unless it is actually used: j may cease to describe the original seed subgrid. The physical residual and target calculations remain valid if their displayed integer actual fold increments and J update are checked. Conversely if a smaller period is claimed, explicitly establish both its actual fold increments and gcd(M*d,L); a proof of one does not provide the other.

The unresolved universal step is selecting SOME original source/cap state (or another true-contact program) whose exact joint right/target condition holds. A transitive generated group, abstract graph, small covolume, or an already open prefix supplies no such selection by itself. This is the concrete criterion against which to challenge the author's next general null-orbit claim.
