# R38: a four-reflection shuttle closes all B, C1 and C2 families

Candidate complete positive theorem, pending independent review. ALL parameters of the accepted A42 normal forms B,C1,C2 are covered directly. There is no finite-prefix, residue or asymptotic hypothesis. The universal canonical45 W21 theorem and the unclosed A1 family remain OPEN.

The planned finite residue search completed its fixed proof bases, but inspecting the returned paths revealed the following SINGLE all-parameter construction. The proof uses this construction, not an inference from the finite search outcomes.

## A local actual-wall shuttle

Let a rectangular core occupy0<=x<=c, with c>0. Let u,w>0 and mu be real, and REQUIRE w<c. Suppose the room has:

- a right source tooth[c,c+w] x [mu-3u/2,mu-u/2], with actual interior seam source S=(c,mu-u);
- a right target tooth of height u centered at mu+u, with actual interior seam target T=(c,mu+u) and any positive depth;
- a left tooth[-w,0] x [mu,mu+u];
- a smooth actual left-core mirror throughout mu-u/2<y<mu;
- a smooth actual right-core mirror at(c,mu).

All these bands and the open core segments used below must lie in the actual room's core height range. Other attachments may be arbitrary if they preserve those actual used mirrors. Neither source nor target seam is a reflecting wall.

Put alpha=u/(2(c+w))>0. Use the following SIX physical points in order:

    S=(c,mu-u),
    A=(c+w,mu-u+u*w/(2(c+w))),
    B=(0,mu-u*c/(2(c+w))),
    C=(c,mu),
    D=(-w,mu+u/2),
    T=(c,mu+u).                                      (1)

The consecutive horizontal velocities have signs +,-,+,-,+, while every vertical velocity is positive. Each leg has absolute slope alpha. Thus all four intermediate contacts obey the vertical-wall specular reflection law, with no horizontal reflection or changed angle between chamber pieces.

A lies strictly inside the actual source far wall: its ordinate lies between mu-u and mu-u/2 because0<w/(c+w)<1. The initial S-to-A leg is strictly inside the source tooth. On A-to-B, the exit through x=c has ordinate

    mu-u+u*w/(c+w),

which is strictly between mu-u and mu, but to stay inside the SOURCE tooth it must also be below mu-u/2. This exit ordinate condition is NOT automatic from c,w>0. The guarded shuttle therefore requires

    w<c.                                             (2)

Under(2), u*w/(c+w)<u/2, so this exit is strict inside the source band. The remainder of A-to-B lies in the open core. The point B belongs to the explicitly protected open left interval (mu-u/2,mu).

B-to-C is wholly in the core except its actual smooth endpoint mirrors. C is in the gap between the selected source and target tooth bands and is required to remain a smooth actual right wall. C-to-D crosses the left mouth at ordinate

    mu+u*c/(2(c+w)),

strictly between mu and mu+u/2. It therefore enters the actual left tooth. D is its smooth far-wall midpoint. On D-to-T the exit through x0 has ordinate

    mu+u/2+u*w/(2(c+w)),

strictly between mu+u/2 and mu+u. Thus the left tooth's entry, far reflection and exit are all corner avoiding. Its final core leg ends at the ORIGINAL actual target seam. No target-image substitution or auxiliary cap is used.

Every open leg lies in its stated actual tooth or open core. All contacts are strict wall interiors. The vertical coordinate increases strictly throughout the entire path, so no earlier actual T occurs. This proves a finite actual four-reflection S-to-T connection whenever the guarded hypotheses, including w<c, hold.

The inequality(2) is essential to THIS displayed five-leg path: if w=c its source exit is the source tooth's genuine mouth corner, and if w>c it reaches the tooth's horizontal wall before that nominal exit. No unsupported all-positive-width claim is made. It holds strictly in every application below, where c2,w1.

## Exact application to ALL B, C1 and C2

In every normal form below c2,w1,u2. The actual marks have the form S=(2,mu-2), T=(2,mu+2), and the selected right teeth are[2,3] x [mu-3,mu-1] and[2,3] x [mu+1,mu+3]. The left nonflush tooth is[-1,0] x [mu,mu+2]. The path(1) is simply

    (2,mu-2), (3,mu-5/3), (0,mu-2/3),
    (2,mu), (-1,mu+1), (2,mu+2).                    (3)

Its actual initial velocity is(3,1), and it has exactly FOUR smooth ordinary reflections. All five legs are monotone upward.

For B use G8,mu4. The opposite floor-flush tooth is[0,2] and the only other opposite tooth is[mu,mu+2]. Since mu-1=3>2, the protected open wall interval(mu-1,mu) is present. There is no opposite roof-flush tooth. The selected right gap contains(2,mu), and all path heights lie strictly between0,G.

For C1 use G10+4r,muG/2-1=4+2r, EVERY integer r>=0. Its opposite teeth are[0,2],[mu,mu+2],[G-2,G]. Again mu>=4 gives mu-1>2, so the required left interval is smooth. Also mu+2<G-2, and the selected tooth bands and all path points are strictly inside the global height range. The right gap at mu is genuine. No lower-gap insertion or limiting argument is needed at r0.

For C2 use G12+4r,muG/2=6+2r, EVERY integer r>=0. The same three opposite teeth occur. Here mu>=6 and mu+2<G-2 for every allowed r, giving the identical strict actual guards. The same formula(3) covers the entire family.

All three applications use actual positive seams, true selected source and opposite far walls, and the existing right/left core wall pieces. No unseen attachment may remove them: accepted A42 identifies the ENTIRE room and excludes extra attachments. Unit tooth width1 and c2 satisfy the required strict w<c. The first-target and corner guards of the local theorem are therefore sufficient for EVERY parameter in B,C1,C2.

Thus all three families illuminate, and none can contain the putative actual dark pair from A42. This proof uses four reflections uniformly over their unbounded parameters, not just eventuality or finite residue checks.

## Exact checks, prior failed plans and scope

c2-BC-closure-check.json records the original bounded proof-base discovery: one first orbit candidate for B, one for C1r0, and first q1/3 direction-pack witnesses for the twelve planned period bases. That search stopped per base and terminated before the original effort deadline. Its p3,q1 paths suggested(3), but those samples are not the general proof.

c2-BC-four-bounce-check.py independently constructs(3) for all fourteen already prescribed base rooms and for two explicitly prescribed large-parameter controls. It checks all finite-wall intersections, unique actual smooth mirrors, exact specular laws, strict original S/T and first arrival. These controls supplement the all-parameter inequalities above. No new room or direction DISCOVERY was used for the formula checks.

The source exit condition w<c was checked algebraically during authoring and is retained in the theorem. It cannot be dropped merely because the selected vertices appear to be inside a rectangular spine.

Accepted A0 and the remaining peer-owned A1 must still be reconciled/closed before claiming the entire c2 thin-comb W21 theorem. General c1 combs, deeper or taller teeth, arbitrary octilinear rooms and the universal uncapped W21 goal remain OPEN. No universal minimum claim is made. All authoring and search belong to the original R38 interval ending06:28:30.804732Z.
