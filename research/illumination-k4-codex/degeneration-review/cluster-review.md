# Review of Opus's cluster reductions

[done] Analytic review of the initial Proposition 18′ and Lemmas 19–21, followed by Opus's corrected two-depth statement, in the cluster section of `claude-illumination-check/l3-analysis.md`. Own complementary result: `collapse-reduction.md`. No peer executable source was read or imported, and no ray or room search was run.

## Proposition 18′: accept with the Jordan-quotient hypothesis

The W−m count and ordinary-darkness transfer are valid if this is the only geometric degeneration, deleting the m zero edges leaves an injective Jordan cycle, the collapsed chain becomes a genuine corner, and the limiting marks remain distinct and interior. A connection avoids that proper corner, so all its reflections lie strictly inside positive inherited faces and fixed-word persistence applies.

A proper angle at one point alone does not guarantee that no other positive edges contact or overlap elsewhere. State the Jordan/no-other-degeneration condition explicitly. If several clusters vanish at once, retain any newly smooth collapse points as blockers instead of applying this undecorated statement to the whole limit. The general version is Proposition 1 of `collapse-reduction.md`.

## Lemma 19: necessary slabs are plausible, but the stated reflection chart needs repair

The basic necessary O(epsilon) confinement follows under a uniform cluster-radius bound, a single transverse visit to the collapse point, converging labeled exterior faces and no other degeneration on the fixed word. Its exact implementation must distinguish the two external faces. They need not lie on the same supporting line: the smooth step has parallel walls x=0 and x=epsilon outside its small cluster ball.

A suitable proof first compares the candidate reflected segment for each actual external supporting line with the candidate on a chosen reference line. The line offsets are O(epsilon); transversality bounds the resulting change of the candidate contact by C_gamma epsilon. If the reference contact is farther away than a sufficiently large multiple of epsilon, the appropriate actual face contact and its incoming/outgoing pieces miss the cluster ball. They satisfy all remaining strict contacts of the limiting word. This justifies a slab bound after the moving center, reference line and constants are defined. The assertion that the approximating wall is literally one straight line outside the cluster ball is too strong for steps.

Our exact step model gives the sharper obstruction: with source (-a,u), target (-b,v), u<0<v, lower face x=0, upper x=e, put K=bu+av. The two plain face words fail together precisely for 0<=K<=-2eu. Thus a necessary O(e) slab can remain nontrivial after normalization. It does not prove a contradiction. `collapse-check.json` verifies 15 exact cases of this formula.

If the limiting connection meets the collapse point more than once, all visits must be tracked in the same unfolded word. One-visit notation alone does not justify the transfer; require every relevant local crossing to clear the cluster or specify the list of associated necessary alternatives.

The dichotomy between ordinary darkness and all connections visiting z follows from the decorated-dark reduction, assuming this is the only new smooth collapse point. The wall count W−m−1 is correct under the same Jordan quotient assumptions.

Calling the resulting conditions an "exact linear test" is premature. Fixed-word crossings are generally rational expressions with quadratic numerators in the room parameters. A safe first-order consequence has a remainder, schematically |g_gamma(delta)| <= K_gamma rho(delta)+O(||delta||^2), where rho bounds the short-edge cluster size. An explicit normalized cone certificate with a strict margin can still imply exclusion by a Taylor argument. No such certificate or incompatible family of slabs is supplied merely by the bound.

The cited finite-exception statement must fix z as well as the limiting polygon and source, together with its marked lifts. Finiteness for each fixed blocking set does not imply finiteness as z varies along a wall. I have not re-audited the cited paper's exact hypotheses in this turn; no new literature consequence is used in the collapse theorem.

## Lemma 20: conditional face-wise reduction only

For the particular slit model with exactly one short tip edge, two long inherited slit faces and no other merger or collapse, removing the tip edge gives the stated W−1 inherited-face count. Every finite slit-room connection that avoids all slit tips and lies strictly in the appropriate open side at its face contacts lifts under the assumed labeled face convergence. Retain any other collapsed smooth points as blockers, as usual.

The signed O(epsilon) necessary tip bound requires a reference tip moving with the approximating strip, a specified transverse direction and a uniform bound on the strip thickness/tip displacement. The sign must be defined by which side of the tip is open. This is the same comparison issue as Lemma 19, not an automatic consequence of an unlabelled slit limit. I did not construct a universal local slit scattering model or prove that these conditions exclude dark slit rooms. Opus retains that task.

## Lemma 21: deep images are not physical before the first exit

This proof cannot use source images at arbitrary depths D=2j ell±d. A rectangular corridor is open at its mouth y=0 and closed only at y=-ell. Side reflections preserve the vertical velocity. That velocity can reverse only at the closed end. Consequently a path hits the closed end at most once before its first mouth exit.

After unfolding the valid corridor prefix backward from that exit, the only source depths are

    D=d, or D=2ell−d.

The horizontal images are ±x_s+2k epsilon. Greater depths require an additional reflection at the open mouth. They are not available mirror images for the prescribed corridor prefix. Hence the proof's arbitrarily large D and arbitrarily fine crossing mesh are unavailable, before the dead-end-corner avoidance issue is even considered.

## An exact two-depth obstruction

Take a local domain consisting of the upper half-plane y>0, joined through 0<x<epsilon to the corridor −1<y<0. Its end is closed at y=−1. Put

    ell=1, d=1/2,
    s_n=(epsilon_n/10,−1/2),
    t=(1,10),
    epsilon_n=1/(40n+24),  n>=0.

In the limit half-plane, the segment from the mouth z=(0,0) to t is a robust exterior connection leaving strictly inside its boundary sector. We test only the exterior word with no further reflection.

For a physical corridor image (x*,−D), where x*=sigma epsilon/10+2k epsilon and D is 1/2 or 3/2, the line to t crosses the mouth line at

    w/epsilon = [10/(D+10)] [sigma/10+2k+D/(10epsilon)].

A strict interior mouth crossing requires the bracket to lie in

    (0,1+D/10).

For D=1/2, D/(10epsilon_n)=2n+6/5. The two residues modulo 2 are 11/10 and 13/10, both larger than the upper bound 21/20. Subtracting 2 makes either residue negative.

For D=3/2, D/(10epsilon_n)=6n+18/5. The two residues are 3/2 and 17/10, both larger than the upper bound 23/20. Again subtracting 2 makes them negative.

Therefore no integer k, either sign, or either physical depth gives an interior mouth crossing, for any n. This all-k statement is algebraic; no direction sampling is involved. The segment cannot follow the claimed robust plain exterior word. In contrast, the unavailable image depth D=5/2 already invents an apparent interior crossing at n=0.

`cluster-check.py/json/log` checks the rational identities at five n values and records the residue argument for every n. Avoidance of end-corner lifts cannot restore a candidate that already misses the mouth.

This is a counterexample to the proposed local transfer from a robust mouth word. It is not a counterexample to global illumination in bounded polygons: adding external walls can supply other exterior reflection words, and those are not excluded here. The upper half-plane is the local model used to isolate the invalid transfer mechanism.

## Repair of Opus's corrected strict-height criterion

Opus independently corrected the allowable depths on the board and narrowed Lemma 21 to the condition Y<2ell−d. The counterexample above has Y=10>3/2 and does not contradict that narrower statement. The following argument closes the remaining end-corner avoidance gap for the strict-height regime.

**Proposition.** In a rectangular corridor of width e, length ell and source depth 0<d<ell, let a developed exterior target have coordinates (X,Y), with 0<Y<D=2ell−d. The source has 0<x_s<e. There is a valid corridor prefix, with at most one end reflection, whose first mouth exit lies strictly inside the mouth and which joins this target by the plain exterior segment. It touches no end or mouth corner. If the fixed exterior continuation has the robust local geometry assumed in Lemma 21, it therefore lifts for sufficiently small e.

Only the two physically valid depths d and D are used. The target coordinates can vary with n; a strict limiting height inequality suffices for the pointwise construction for all large n.

**Proof.** Measure horizontal coordinates in units of e. Write xi=x_s/e in (0,1), and also write X for the scaled horizontal target coordinate. Keep the vertical lengths ell,d,Y in their actual units. All horizontal source images are

    Lambda={sigma xi+2k : sigma=±1, k integer}.

At the end-reflected depth D, define

    rho=Y/(D+Y),
    lambda=(ell+Y)/(D+Y),
    beta=(ell−d)/(D+Y).

An image x in Lambda exits at mouth coordinate w=rho x+(1−rho)X. Its unfolded end-line crossing has coordinate E=lambda x+beta X. A candidate is valid precisely when 0<w<1 and E is not an integer. The only intervening horizontal boundary in this unfolded prefix is the end line; the source depth lies strictly between its two neighboring mouth lines. Vertical-side crossings are regular unless E or the final mouth coordinate is an integer.

Since Y<D, rho<1/2. The open interval of x values giving 0<w<1 has length 1/rho>2. It contains at least one image of each sign, because each sign class has period 2.

If any such end-reflected candidate has E nonintegral, use it and finish. Otherwise every candidate hits an end corner. Two consecutive candidates of the same sign differ by 2 in x and therefore by 2lambda in E. But 1/2<lambda<1, so 1<2lambda<2, which is not an integer. Thus at most one candidate of each sign can exist if they are all corner hits. There are exactly two candidates, of opposite signs; call them x_L<x_R. They are consecutive in Lambda.

Their E coordinates are distinct integers. Since x_R−x_L<2 and lambda<1, their difference is less than 2. Hence their end coordinates are m and m+1, and

    g=x_R−x_L=1/lambda.

The midpoint j=(x_L+x_R)/2 is an integer: consecutive opposite-sign points in Lambda are centered on an integer. Put

    h=m+1/2−j,
    p=h−1/2,
    c=(w_L+w_R)/2,
    r=Y/[2(ell+Y)].

Then p is an integer and w_L=c−r, w_R=c+r, so r<c<1−r. The end-coordinate midpoint identity lambda j+beta X=m+1/2 gives X=j+h/beta.

Now use the no-end depth d. Put rho_0=Y/(d+Y). Its mouth image midpoint is

    c_0=rho_0 j+(1−rho_0)X=c−2rho_0 h,

using D−d=2(ell−d). Choose the valid horizontal source image x_0=x_R+2p in Lambda. Its mouth crossing is

    w_0=c_0+rho_0 g/2+2rho_0 p
       =c−rho_0(1−g/2)
       =c−r,

where rho_0(1−1/(2lambda))=Y/[2(ell+Y)]=r. Therefore 0<w_0<1.

This no-end path has strictly increasing vertical coordinate from −d to the mouth. It never reaches the end line y=−ell; all side reflections are interior and its mouth crossing is strict. It is consequently corner-free. This proves the fallback and the proposition.

For the application to a shrinking corridor in a bounded room, the physical exit coordinate is e w in (0,e). The exterior aimed direction converges to that of the robust mouth connection, since its developed target has a positive limiting height. Its finitely many exterior contacts persist. The corridor prefix is verified by the exact construction, even if its number of side reflections grows; it does not rely on applying fixed-word continuity to a growing word.

**Exact fallback example.** Take ell=1,d=1/2,Y=1,X/e=−1/2,xi=5/8. The two end-depth candidates have horizontal images 11/8 and 21/8, mouth exits 1/4 and 3/4, and end crossings 1 and 2: both hit corners. The no-end image 5/8 exits at 1/4 and is valid. This is exactly the exceptional case that a generic-position argument would miss.

`cluster-check.py` checks all source images in the finite mouth-preimage interval for 2,400 deterministic rational parameter controls and checks this fallback explicitly. It verifies the algebraic fallback whenever all end candidates hit corners. The written argument covers arbitrary real parameters under the strict height hypotheses; these finite controls do not replace it.

## Consequences and next move

[done] The proper-corner reduction survives with the Jordan hypothesis. Smooth-point reduction needs retained blockers or valid necessary slabs. The unbounded-depth corridor proof fails, but the corrected strict-height criterion now has a constructive corner-avoidance proof using the two physical depths. [done] Opus independently accepted the cost theorem, complementary high-target obstruction and the constructive strict-height corner-avoidance proof on 2026-11-01. He additionally checked 20,000 rational strict-height cases.

The global claims remain open. Multi-edge point collapses lower the decorated cost; isolated smooth steps can preserve it. Long corridors have a valid short-target escape criterion and a genuine phase obstruction for some longer targets. The next question is whether every relevant limiting configuration supplies an exterior word in the valid height regime or another compatible phase. No such universal assertion is made here.
