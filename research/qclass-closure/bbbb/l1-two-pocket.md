Advances: L1 — lighting tail for aligned three-chamber rooms with unit necks.

The two mouth tests must use one common slope. The calculation below compares the two possible midpoint lifts and records where the common-carrier construction stops.

## A dimension theorem

Use the geometry of l1-chamber-general. The common open band is (0,1) in height, the chamber widths are w₁,w₂,w₃, both shoulders at each mouth are positive and integral, and the total horizontal span is P. Write E₀ for the four internal neck endpoints on the horizontal axis. All depths and both neck lengths may vary independently.

**Theorem.** Every interior lattice pair is lit if P is odd, coprime to each chamber width, each width is at least three, and no two elements of E₀ sum to P. The width condition can be weakened to allow width one in any chamber. Such a chamber has no marked column. A width-two chamber can also be used under the pair-level clearance test below.

**Proof.** Same-chamber pairs have a straight segment. The preceding note covers opposite-side pairs and same-side pairs of opposite abscissa parity under the stated coprimality. For a remaining pair reflect vertically if necessary. Let a,b be the respective nonnegative depths below the bottom of the band. Unfold its outer end walls with horizontal period 2P. Let X=x_S, Y=±x_T be lifts and let E consist of ±E₀ modulo 2P. Set M=2 lcm(w₁,w₂,w₃). An integer carrier speed n divisible by M can realize any even horizontal advance K modulo 2P because gcd(M,2P)=2. We take n positive and as large as needed to make the final speed positive.

There are two solutions to 2z=X+Y modulo 2P. They differ by P, so exactly one, z, has the parity of X. Neither folds to an outer wall since the two physical marks have distinct abscissas. If z is outside E, take K=z−X and speed n. At every integral depth in a chamber the carrier returns to the same abscissa and direction. At z the ray either reflects from the neck wall or enters the opposite pocket, reflects at its roof and returns to z. A second band crossing ends at Y after the target stub. This is the previous zero-drift test.

Suppose z is a seam. Write Z=z+P modulo 2P. Its physical horizontal position is P minus that of z. Hence Z is regular unless **two physical seam coordinates sum to P**. At regular Z set h to zero for a neck or to the opposite pocket depth for a chamber. For either sign s=±1 take

    K=Z−X−s,    D=a+2+2h+b,    η=2s/D,    c=n+η,
    n=0 (mod M),    n=K (mod 2P).

K is even. At the two near-band gates the slow coordinates are X+aη and Y−bη. At entry to the opposite pocket, its roof, and its return, respectively, they are

    Z+s(a−b−2h)/D,    Z+s(a−b)/D,    Z+s(a−b+2h)/D.

Indeed the first band crossing adds K in the global unfolding, and each pocket half-trip adds zero carrier phase modulo twice the local width. The second crossing adds K again, giving X+2K+Dη=Y modulo 2P. The three displayed offsets have absolute value strictly less than one. An integral regular Z has clearance at least one on either side, so all three contacts are interior on the required sheet. Between contacts, folding inside each rectangle gives legal side-wall reflections. For h=0 only the central wall contact is needed.

The remaining exact clearance test for this construction is that, for one sign s, X+2sa/D and Y−2sb/D belong to the open lifted spans of their respective chambers. Both displacements are strictly less than two, and at most one is at least one since 2a+2b<2D. A mark in a chamber of width at least three has at least two units available on one side. Choose s to point the larger displacement into that side. This proves the theorem, including arbitrary depths. A width-two mark has one unit available in either direction, so it passes this test precisely when its displacement magnitude is less than one (with the other mark's clearance also enforced).

## What simultaneous failure requires

For odd coprime P and marked widths at least three, apply the two-root argument with both target lifts. Failure requires that **both** parity-compatible midpoints lie in E ∩ (E+P). This strengthens the older E-only obstruction. It rules out the earlier seam example with widths (4,6,4+156k) and neck lengths (2,1), k≥1, since all four seams lie below P/2. The argument compares attainable phases with a shared speed. Distinct widths alone do not imply independent choices of the two phases.

A third test disposes of some of the seam equation itself. If Z is a seam and a≠b, use h=0, and choose s so Z+s(a−b)/(a+2+b) falls on its neck side. This is a regular bounce. The same two near-gate inequalities suffice for this forced sign. If a=b, first reflect S from its own floor of depth p>a, replacing a by A=2p−a. Use the same formula with A in place of a and test the source floor contact X+(p−a)η as well. It lies between X and X+Aη, and the carrier dies modulo twice the source width at both contacts. Hence all seam pairs with at least two units of clearance on both sides of each mark are disposed of, even at equal depths. These tests impose no denominator bound.

One can also relax coprimality on each fixed branch. With source, target and opposite-pocket widths u,v,w, replace M by

    M*=lcm(2u/gcd(2u,a), 2v/gcd(2v,b), 2w/gcd(2w,h)).

Omit the last factor for a neck. The same formulas for regular midpoints or forced neck bounces work when gcd(M*,2P) divides K, since only the carrier advances at the indicated integral depths must vanish. For a reflected source use A in place of a and include the extra factor 2u/gcd(2u,p−a). This divisibility is necessary and sufficient for these specified carrier congruences. It need not be necessary for a ray with different return phases.

**First open implication.** For an odd coprime span with a mirrored seam pair, a same-side, equal-parity pair can still require a proof when both midpoint choices are seams in both lifts and the forced signs lack clearance. More generally width-two clearances and incompatible carrier congruences for other spans remain. I cannot infer joint vanishing of the full strip tests from any of these conditions, or prove that another strip test is positive there. The seam equation is necessary for failure on the stated width and coprimality domain. Its necessity for all dimension tuples and the existence of a pair missed by every earlier test are both open. The area-21 and area-23 families retain their separate proofs in the preceding note.

## Long-neck lemma for L1 (conjectural)

Seek an absolute C such that in every strictly simple integral orthogonal room with at most eight reflex corners, a separating rectangular neck of longitudinal length at least C implies that every two interior lattice marks are lit. Here a separating neck joins two components through its opposite open ends and has solid longitudinal walls. Even for unit necks the preceding theorem requires aligned chambers and arithmetic hypotheses. It gives no such C.

There is a geometric obstruction to the proposed budget argument for general necks. For every integer L≥3 attach two width-one, height-H end chambers (H≥5) to a horizontal neck of length L at heights (1,H−1), with chamber floors at zero. There are four reflex corners, and the neck has interior lattice marks. Consider a full-mouth integral rectangular pocket of width at least three and depth at least one, with solid flanks and roof and an open base across its width. Its roof needs inward-pointing solid flanks at both ends. The long horizontal neck walls have reflex endpoints, the end-chamber horizontal walls have length one, and the vertical shoulders have length one. The two outer vertical walls have enough length, but their flanks run only one unit and the proposed base at that depth meets solid shoulders. A proper subsegment of a straight wall cannot supply both perpendicular flanks either. Thus this family lacks that pocket for arbitrarily long necks despite its corner budget. This is a shape argument, with no claim of darkness. It also explains why the R22 no-pocket observation supplies no converse at eight reflex corners.

The obstruction persists for strictly inset **unit-height** necks with marks on both sides. Take an end chamber with boundary vertices (0,0),(2,0),(2,3),(1,3),(1,2),(0,2), in order. Attach the neck to x=2 at heights (1,2) and put the reflected end chamber at its far end, for arbitrary integral length L≥3. Each stepped chamber contributes one reflex vertex and each mouth two, giving six in total (16 walls). The lattice mark (1,1) and its reflected counterpart are interior. After attachment every wall except the two longitudinal neck walls has length at most two. Each long wall ends at reflex corners, so neither can be the roof of a pocket with two solid flanks. This excludes the stated pocket in either orientation uniformly in L.

Consequently a general long-neck proof must provide a different illumination mechanism for rooms without that pocket, or establish a weaker pair-dependent pocket and prove access to it. The illumination claim remains open even though this proposed geometric implication fails.
