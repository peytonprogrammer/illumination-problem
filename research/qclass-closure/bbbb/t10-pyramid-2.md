Advances: T10, pyramid — exact two-axis criteria for the strict mask-761 placement, and an equivalence eliminating three free outer dimensions from the existence of a joint miss.

**Prediction and check.** Before calculation I favored (a). For the single new candidate (w,u,V;q,h,d,f;x,z,a,b)=(24,30,1800;2,16,5,6;1,90,4,15), I predicted a vertical miss and a horizontal hit. The coordinator's onepass.py gave 0/86400 vertical and 59760/1734432 horizontal, first horizontal numerator 56. This supplies a witness at every V>90 for these other dimensions.

**Corner rules.** Work in the strict ranges 0<x<w<u<z<V, 0<a<f, 0<b<h, with positive integral gaps. On descent the first opening is [0,w] and the second [0,u]. Zero is a smooth common wall at both; the other endpoint is reflex. Moving left, the first opening is [0,h] with reflex endpoint h only. At the next opening both 0 and U=h+d are reflex: the last column extends below and above the middle column. These are exactly the singular sets in the code. At a smooth shared endpoint either incident sign gives the same subsequent fold, including the integer-division convention when an incoming slope hits zero exactly. Between gates each transverse endpoint is a genuine wall. Signed displacements are integral by unfolding integer marks across integer mirrors. Adding twice the sweep distance times the lcm of widths preserves unfolded phase and sign at each gate by induction. This verifies the list definition in onepass.py for the stated ranges.

**Exact cosets.** For either axis use local widths w,u,V and travels a,d,b as in d172. The first two intervals start at zero. Write the last interval as [l,l+V], the physical source and target ordinates as x,z, and L=d+b, D=a+L. Choose source representative σx, σ=±1. The two terminal representatives are c=z and c=2l−z. Set, with integers i,j,k,

    Z=c+2Vj,   M=(Z+2ui)/L,   R=dM−2ui,   X=σx+aM+2wk,
    E=XL/D,    F=R+bX/D.

Vertical: require |E|<w and |F|<u (l=0). Horizontal: use (w,u,V)=(h,U,q+U+f), (a,d,b)=(z−u,u−w,w−x) in original room variables. The source and target ordinates are h−b and U+a, and l=−q. Require |E|<h and **0<F<U**. This last window has only half the signed width. A negative developed second crossing is handled by reflecting the entire developed line so F is positive; the free source sign permits that convention.

For sufficiency the line with slope M−X/D starts at σx+2wk. At the first joint it reaches E; at the second it reaches F+2ui; at the endpoint it reaches Z+2ui. The gate inequalities make the folds agree in position and transverse velocity. Conversely develop any one-pass path using its first common wall, subtract a period of the middle interval at the second crossing, and choose the global sign as above. Reading the first and last images gives the displayed integers. A zero crossing on a vertical shared wall is included. Thus finite unions of these cosets give equivalences.

With g=gcd(dV,ub) and η=gcd(wg,auV)/g, the rows in R have spacing 2g/L. On each row X has spacing 2η. The kernel move (Δj,Δi)=(ub/g,dV/g) changes M by 2uV/g. This proves the asserted covolume 4gη/L, with a generally sheared basis. For each row intersect (−wD/L,wD/L) with (D/b)(J−R), where J=(−u,u) or (0,u). If the resulting interval is (A,B) and X₀ is any row representative, its exact hit test is floor((A−X₀)/(2η))+1 < (B−X₀)/(2η), with A<B. Only rows with dist(R,J)<wb/L matter. Vertical window area divided by covolume is wuD/(gη)≥D/b since η≤w and g≤ub. Horizontally the ratio is half that expression in local parameters.

**Eliminating the outer dimensions.** In local parameters let P=b·lcm(w,u). Replacing a terminal image Z by Z+2P can leave (R,X) exactly fixed: increase i by dP/(ub), then decrease k by aP/(wb). Both shifts are integral. This yields an exact test for the universal choice of outer dimensions:

1. Vertically retain only Z=z. Its negative gives the same test by global sign. This restricted list works for every V>z. When V is any multiple of P above z, it is the full test.
2. Horizontally retain only Z=U+a in original variables. This test works for every q>0 and f>a. With P′=(w−x)lcm(h,U), choose q≡−(U+a) mod P′ and f so q+U+f≡0 mod P′. Both terminal representatives and all their translates now coincide modulo 2P′. The restricted test is exact for these choices.
3. The two choices are independent. For a fixed inner tuple (w,u,h,d,x,z,a,b), some outer tuple (V,q,f) misses both axes **iff** both restricted tests miss. One such miss would give infinitely many rooms by these congruences. This is stronger than checking horizontal independence of V alone.

**Where the attempt stops.** The two restricted tests still have independent middle and source windings. I cannot force either open row interval to contain its required residue, or exhibit an inner tuple where both fail. The single-axis area ratio does not resolve the simultaneous offset condition. No joint miss or all-size closure is claimed.

**Other residual masks** (canonical horizontal rank gaps g₀,g₁,… and vertical gaps h₀,h₁,…; d172 variable b is target depth):

- 763: same three widths as 761, w=g₀, u=g₀+g₁, d=h₂; outside when g₀b>(g₀+g₁)h₂.
- 8051: three residual pairs, A=g₀+g₁, w=A, u=A+g₂, d=h₁; outside when Ab>(A+g₂)h₁.
- 6131: w=g₀, u=g₀+g₁+g₂, d=h₂; outside when g₀b>(g₀+g₁+g₂)h₂.
- 5111: w=g₀, u=g₀+g₁, d=h₂; outside when g₀b>(g₀+g₁)h₂.
