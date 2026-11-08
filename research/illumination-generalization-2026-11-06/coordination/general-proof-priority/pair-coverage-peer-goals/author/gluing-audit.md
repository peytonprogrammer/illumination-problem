# Actual four-copy cylinder gluing audit

This supplements the conditional-map orientation audit; it does not assert universal seed coverage, which the full-group counterexample refutes. It supplies explicit original-sheet geometry rather than an unlabelled matrix.

Take C_left: -a<x<a, y modulo2H and C_right: a<x<2A-a, y modulo2B. Their areas4aH and4(A-a)B add to4area(P). They represent respectively all four reflected copies of the left vertical rectangle and the lower right overhang. Use representatives0<=y<2H on the left and0<=y<2B on the right. The original copy is0<x<a,0<y<H in the left cylinder, and a<x<A,0<y<B in the right.

The open vertical boundary gluings are:

1. left(a,y) identified with left(-a,y) for B<y<2H-B. These are the original inner vertical-wall self-pairing.
2. left(a,y) identified with right(a,y) for0<y<B.
3. left(-a,y) identified with right(2A-a,y) for0<y<B.
4. left(a,y) identified with right(a,y-2H+2B) for2H-B<y<2H.
5. left(-a,y) identified with right(2A-a,y-2H+2B) for2H-B<y<2H.

The last two use the negative-y copy, normalized into each cylinder circumference. Every transition is a translation, and the endpoints extend to the finite actual sector stars. No interior mirror is inserted.

V_k(x,y)=(x,y+k(x+a)) on the left and(x,y+k(x-a)) on the right is identity as a CIRCLE map on every boundary when ka/H and k(A-a)/B are integers: shifts on the left boundaries are0,2ka, and on the right0,2k(A-a). Hence it respects all five identifications, including the different y-period normalizations. Its single derivative[[1,0],[k,1]] agrees through every regular seam; the inverse with-k respects the same gluings. This proves a global affine map on the actual unfolding.

The regular corner pair at x0,y0/H shifts by ka, a multiple of H and so is fixed or exchanged; the regular pair at xA,y0/B shifts by k(A-a), a multiple of B. The inner roof regular corner(a,H) and the reflex cone(a,B) are boundary points and fixed. Thus the full physical Sigma, not just the cone, is preserved.

Transposing ALL charts and all five arcs gives the horizontal cylinders and conditions in orientation-audit.md. The target belongs to the corresponding central rectangle; that is why a vertical target must have t<a and a horizontal target must have v<B.

In the uniform-source proof the transformed target(t,0) is an actual ORIGINAL bottom seam point, fixed by R_y. A right-arm source keeps its original positive x coordinate while its yphase is read modulo2B. Phases0/B are ordinary smooth floor/ledge points; the reflected phase branch is moved to the original lower copy by R_y. Therefore both transformed endpoints really belong to the same closed lower rectangle, including the allowed wall-aligned seed. The inverse restores BOTH original lifts. A torus projection without this sign/copy information would not justify that conclusion.

This is hand reconstruction only, with no computation, search, orbit enumeration, engine or new clock. The stronger one-copy universal assertion remains false; this audit preserves the correct conditional transport theorem.
