# Candidate reduction: source-fixed affine orbits to directly visible seeds

Status after the follow-up audit: the conditional transfer proposition stands. The universal INTERIOR-seed assertion is REFUTED at W=6; a boundary-inclusive native assertion remains UNRESOLVED. The original word "inside" was ambiguous about smooth boundary seeds; see obstruction.md before using the universal candidate. This is not a proof of all W10, r<=8 or canonical45 W<=21. No claim.

## Precise setting and sufficient proposition

For an integral orthogonal Jordan room P, use its actual connected four-copy reflection unfolding M. Let Sigma contain EVERY physical corner lift, including regular convex corners. Let Z be the finite set of lifts of all physical integer-coordinate points, including boundary points; its exact membership is retained rather than declaring all regular lattice points forbidden. Fix the actual source lift p in the original copy, and the actual target lift q in the SAME copy. For the native problem both actual physical marks are distinct interior even-even points.

Let G_p be the group of globally defined affine homeomorphisms F of M (orientation preserving or reversing) with F(p)=p, F(Sigma)=Sigma and F(Z)=Z. Derivatives and local charts must actually glue; an integer matrix alone is not an automorphism. Let V_p be the subset of Z lying inside the original polygon copy and joined to p by a straight segment whose open part lies in that copy's physical interior. Thus V_p consists of sheet-correct directly visible seeds. Merely requiring physical visibility of the projection of F(q) would lose the target sheet and is not the criterion.

PROPOSITION: if G_p*q intersects V_p, the original actual S,T illuminate.

Proof: choose F with v=F(q) in V_p. The direct seed segment p->v is a genuine regular segment in M avoiding Sigma. Applying F^{-1} maps it to a SINGLE straight segment in translation charts, with one constant transformed direction, from p to q and avoiding Sigma because F^{-1}(Sigma)=Sigma. Refold that whole path in P. It avoids every genuine physical corner and obeys the actual mirror law. The source is the exact original p, and the endpoint is the exact original q, not another target sheet. Compactness of the finite seed segment and local regular flow away from the finite forbidden set ensure it crosses only finitely many physical seams. Equivalently subdivide its compact image into finitely many local charts; a straight regular segment cannot accumulate infinitely many crossings at a smooth wall. An interior initial source excludes a wall-gliding segment; any earlier actual target visit can be truncated. This gives a finite actual S->T ray.

Since Z is finite, orbit coverage is a finite point-permutation condition for each fixed input once the genuine automorphism action is supplied. This observation does not give a W-uniform state bound, action generators, or a uniform positive verdict.

## Quantified universal candidate (not proved)

For every original integral orthogonal room with r<=8, every native actual pair, and p,q in its original copy: G_p*q intersects V_p.

This is a STRONGER sufficient target than illumination itself and may be false in an already-lit low-wall room. The known r9/W22 dark example excludes an unrestricted claim. A failure in an already-lit room would retire this mechanism, not establish darkness. Do not infer it from the eight-wall illumination theorem.

The accepted WR01 full-fiber twists fix every Z point. They therefore cannot move q at all and supply no orbit coverage. Smaller genuine cylinder twists, composed with actual copy symmetries, can act nontrivially on Z while preserving Sigma and fixing p. The following explicit L calibration tests that distinction.

## Prescribed nonconvex calibration, declared before computation

P=([0,48]x[0,16]) union ([0,16]x[16,48]); S=(18,4), original T=(14,40), seed U=(10,40). All marks are actual interior even-even points. Direct S->T has x=50/3 at y16, outside its required portal x<16. Direct S->U has x=46/3 there, strictly inside.

The reflection unfolding has two horizontal cylinders in compatible translation charts:

 C_b=(R/96Z)x(-16,16),
 C_t=(R/32Z)x(16,80).

They have areas 96*32 and32*64, totaling4*area(P)=5120. Define the horizontal affine map H by

 H_b(x,y)=(x+3(y+16),y) mod96,
 H_t(x,y)=(x+3(y-16),y) mod32.

At both boundaries of C_b the displacement is0 or96; at both boundaries of C_t it is0 or192. They are identity pointwise on all horizontal cylinder boundaries, so they glue through the actual saddle connections with the SAME derivative [[1,3],[0,1]]. The inverse uses -3. Thus H is a genuine global affine homeomorphism. The six actual corner lifts are preserved: the two bottom convex corners at(x,y)=(0,0),(48,0) are exchanged, the two y16 corners are fixed on the cylinder boundary, and the two roof corners at y48 are fixed because shift96 is0mod32. This includes the regular physical corners. Integral coefficients and translations, plus the inverse, preserve Z.

Let R_x be the genuine copy involution with local expression(-x,y). It preserves the actual physical point, corner lifts and Z. Put F=R_x composed with H. Then on C_b,

 F(p)=(-18-3(4+16),4)=(-78,4)=(18,4) mod96.

On C_t,

 F(q)=(-14-3(40-16),40)=(-86,40)=(10,40) mod32.

Both representatives p and (10,40) are in the SAME original copy. Thus F in G_p sends the original hidden target lift to the visible seed. F has derivative [[-1,-3],[0,1]], and F is an involution cylinder by cylinder, so applying F^{-1} to the seed vector(-8,36) gives(-100,36), i.e. launch direction(-25,9).

Predicted exact physical path S->T: one lower left-wall contact at(0,262/25), then five upper contacts alternating x16,0,16,0,16 at heights406/25,550/25,694/25,838/25,982/25, and then T=(14,40). Its only upward portal is x46/3 at y16. All contacts lie strictly inside genuine maximal walls and strictly before target height40. There are6 reflections; no numerical direction choice, fitting or enumeration is involved.

Falsification checks: recompute both images and every corner image; reconstruct cylinder-boundary gluing and signs; verify the prescribed six-contact path against each original finite wall using the existing exact checker. Any failure withdraws this calibration. Success establishes this one source-fixed point-permutation example and the transfer proposition, NOT a universal orbit theorem or new L illumination coverage.

## What a useful next proof must establish

First test whether orbit coverage holds throughout an already-solved nonconvex low-wall family, or prove a structural obstruction there. Do not open an orbit census or call per-input decidability universal progress. A positive all-r<=8 theorem would need a low-reflex-specific argument forcing a visible seed in every relevant exact-lift orbit. No such argument is supplied here. Larger full-fiber twists, axis-direction normalization, and an unlabelled torus projection do not establish it.

## Completed prescribed verification and gluing audit

The declared check passed: `python3 -B check.py` produced `check.json` with 6 genuine reflections, 7 legs, 42 exact leg/wall guards and target time 4. The direct seed segment also passed the same finite-wall checker. No alternate direction, ray, room or orbit was searched.

For completeness, the actual horizontal-cylinder identifications can be written explicitly. Coordinates below are unfolded translation coordinates, not physical coordinates. Open subarcs are:

1. Lower cylinder (x,-16) and (x,16), for 16<x<80: the horizontal ledge gluing, with x unchanged.
2. Lower (x,16) and upper (x,16), for 0<x<16.
3. Lower (x,16) and upper (x-64,16), for 80<x<96.
4. Lower (x,-16) and upper (x,80), for 0<x<16.
5. Lower (x,-16) and upper (x-64,80), for 80<x<96.

The boundary endpoint identifications follow by continuity. Each chart transition is a translation. H is pointwise identity on all these boundaries, with common derivative [[1,3],[0,1]] on every incident sector. Therefore both its values and affine derivatives match through each regular seam. At the reflex cone it extends across the finite sector star; its inverse has the same property. The copy involution R_x swaps the two portal subarcs and respects the ledge gluing. It is globally defined independently of H. The corner list contains all six distinct physical-corner lifts: each convex corner has a regular lift and the reflex corner has one cone lift.

The finite-crossing argument in the conditional proposition uses the actual finite polygon-copy seam graph. The transferred compact segment avoids its vertex set Sigma, so has a positive distance from those vertices in the compact unfolded surface. In a regular chart it is straight and encounters only finitely many seam arcs. A seam-parallel segment cannot enter a seam from an interior source. A finite subcover of charts therefore gives finitely many crossings and hence finitely many physical reflections. No endpoint-limit or target-sheet substitution is used.

### Assessment

The conditional transfer is a valid sufficient mechanism; the explicit L example proves it is nonvacuous for a hidden target. It keeps the room fixed and simplifies the target's position, so it is not yet a reduction in reflex count. It supplies neither universal orbit coverage nor a descending complexity measure. The existing WR01 proof already supplies whole-path affine transport; the difference here is allowing a nontrivial permutation of target marks while fixing one exact source lift and demanding a sheet-correct visible seed. That distinction is not a claim.

A decisive next obligation is an all-parameter proof of orbit coverage in an already-solved nonconvex family, or a rigorous counterexample to this stronger condition in such a family. Another isolated successful path would not discharge it. The full r<=8 and canonical45 W<=21 targets remain open, and the peer native goals remain blocked.

## Follow-up: the seed convention matters

See `obstruction.md` and `obstruction-check.json`. The explicit native room with vertices (0,0),(28,0),(28,4),(16,4),(16,16),(0,16), source (26,2), target (8,8) disproves universal INTERIOR-seed coverage. Its intrinsic period quotient has a uniquely distinguished corner-image class; the hidden target is the only interior original-copy point in that class. The pair itself has an exactly checked one-reflection path.

Smooth boundary seeds are legitimate in the conditional transfer proof and must be included in a stronger revised candidate. They are NOT excluded by that native counterexample. In the same room, source (24,2) admits a genuine source-fixed vertical shear taking the hidden target to the visible smooth-wall seed (8,0).

Finally, for arbitrary real sources almost every source stabilizer is trivial, so this source-fixed route cannot prove the all-real illumination statement in a nonconvex L room. This is a separate result; it is not a lattice-endpoint counterexample. The next substantive obligation would be a positive arithmetic theorem for boundary-inclusive seeds, not more interior-only or all-real orbit claims.

## Subsequent repair: transport the ordered pair

The source-fixed requirement is unnecessary for exact endpoint restoration: if F maps BOTH original lifts to a regular straight seed, F^-1 recovers BOTH originals. The seed itself need not be a physical interior billiard path: a corner-free straight segment along a smooth wall seam is valid in the unfolded surface. See `pair-transport.md` for the exact theorem, the general L metric/target sufficient condition, all-real-source proof, and four prescribed path checks. This bypasses the earlier source-stabilizer limitation without invalidating that limitation in its original scope. Full metric/target coverage is still missing, and existing all-real L illumination is already stronger as an illumination statement.
