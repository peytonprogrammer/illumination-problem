# Coupled-neck resonance obstructs direct composition of the long-neck proof

Candidate hand obstruction, Codex01a18403. Independent review pending. This is an obstruction to a specified construction, not a dark pair. In fact the control rooms have eight walls and are illuminated by the independently accepted whole-eight-wall theorem.

## Missing global implication

The accepted A16 theorem fixes both end chambers and lets ONE neck length grow. To apply it twice, one would need to control phases when the other chamber itself contains a second growing neck. Local entry/transit beams do not by themselves provide that control. The following all-parameter family rules out the direct one-pass composition in which the middle chamber is crossed without any wall contact, even allowing every outer horizontal reflection word and one outer vertical bounce at either end.

## Explicit family and actual endpoints

Fix M>0, neck width w=4, central-chamber width h=4 and bridge height epsilon=1/4. The left end chamber is [-2,0]x[0,4], with actual S=(-1,3). Its neck has length L1=M+4. The fixed middle chamber, in its local coordinates, is

    ([0,1]x[0,4]) union ([0,4]x[0,1/4]) union ([3,4]x[0,4]).

Translate it to start at x=L1. A right neck of length L2=M follows it, and the right end chamber has width2 and height4. The actual right mark has depth1 in that chamber and height1:

    T_M=(2M+9,1).

The full room has the eight-vertex cycle

    (-2,0), (2M+10,0), (2M+10,4), (M+7,4),
    (M+7,1/4), (M+5,1/4), (M+5,4), (-2,4).

It is a finite strictly simple orthogonal disk for every M>0. Both marks are strictly interior. For positive integer M, common factor4 gives a canonical45 room with interior A marks (-4,12),(8M+36,4) and eight maximal walls. Its transparent-exception count is unbounded: the bottom wall alone contains4M+24 smooth mixed-parity lattice points. This is an arbitrarily large control family inside the active model, not a finite sampled room.

## Precisely excluded class of paths

Assume a finite actual S-to-T_M trajectory crosses each neck once and crosses the middle chamber without any wall contact there. Arbitrarily many horizontal-wall reflections in either outer chamber or neck are allowed. An initial reflection in the far-left vertical wall and a final reflection in the far-right vertical wall are also allowed. This includes every possible outer-strip itinerary consistent with a single middle transit: before entering the middle, horizontal velocity can reverse only at the far-left wall, so at most one such reversal is possible; the reverse argument applies to the target end.

The claim is that NO path in this class exists, for ANY M>0. Paths with a middle wall contact or multiple middle/neck passages are outside the exclusion and may illuminate the pair.

## All endpoint images and outer wall words retained

Unfold the permitted far-left reflection if present. The source's horizontal coordinate is -a, where a=1 or3, while its initial vertical coordinate is3. The corresponding right virtual target coordinate is L1+h+L2+b with b=1 or3. All horizontal wall reflections outside the middle are encoded by the fold F4, distance to8Z. Every possible developed target ordinate is

    eta + 8n,  eta in {+1,-1}, n any integer.

Let tau be the signed vertical/horizontal slope of this developed segment. No bounded-direction or bounded-word hypothesis has been imposed. The exact target condition is

    D=L1+L2+h+a+b,
    tau=(eta+8n-3)/D.

The developed horizontal distance from source to the first middle mouth is A=L1+a. Since L1-L2=h=4,

    A-D/2=(a-b)/2 = e in {-1,0,1}.

Therefore the developed ordinate at that mouth is

    Y_entry=(3+eta+8n)/2 + e*tau.

The unperturbed term folds to2 when eta=+1, and to1 or3 when eta=-1. These are ALL possible target-image phases: n modulo2 exhausts them because the term increases by4 as n increases by1 and F4 has period8. The 1-Lipschitz property of distance to8Z consequently gives the actual entry height

    z=F4(Y_entry) >= 1-|e*tau| >= 1-|tau|.

This step retains both target signs, every integer n and both optional outer vertical bounces. It is not a test of selected slopes.

## Straight middle passage gives contradictory bounds

With no wall contact in the middle, its physical path is one straight segment y(x)=z+mu*x in local middle coordinates. Its slope magnitude equals |tau|; unfolding may change the sign but not this magnitude.

At the two inner transitions x=1 and x=3, a corner-avoiding straight passage through the bridge requires

    0<y1=z+mu<epsilon,
    0<y3=z+3mu<epsilon.

Equalities at the upper endpoints hit true reflex corners. A floor equality cannot provide a straight interior passage; a floor reflection would be a middle wall contact and is already outside the class.

Subtracting gives |tau|=|mu|<epsilon/2=1/8. Also

    z=(3*y1-y3)/2 < 3*epsilon/2 = 3/8.

But exact endpoint phase matching gave z>=1-|tau|>7/8. Contradiction. The gap is strict and independent of M, n and all allowed outer words. This proves the stated construction obstruction for the entire unbounded family.

## Why local beams are insufficient here

Each outer rectangle has an open set of near-horizontal entry directions from its actual mark. The middle chamber also has open direct-transit beams: for example ordinate1/8 and slopes of magnitude less than1/64 stay strictly inside its central bridge. Thus all three pieces independently admit compatible angular magnitudes. What fails is their common EXACT endpoint phase. The coupled lengths keep the middle entry near the forbidden phase classes1,2,3 instead of letting it sample that small transit aperture.

The one-neck theorem does not claim this composition. If either whole side is treated as an end chamber, that chamber changes and grows with M; the fixed-data and nondegenerate-limit hypotheses fail. Consequently this example does not refute A16 or the possibility of some different coupled-neck theorem.

## Proof-strategy consequence and limits

A global argument cannot iterate one-neck integer-spacing reasoning while ignoring the intermediate phase constraint. It must either use additional middle-wall interactions/returns, vary the chamber itinerary with proved phase control, or establish a joint arithmetic covering statement. The already accepted U8 theorem guarantees illumination here, so the missing mechanism is real rather than a dark-pair conclusion.

No general W<=21 theorem, no darkness certificate and The exact finite residue check corroborates the analytic all-image argument; it is not a ray or word discovery search. Independent review of the quantified restricted-path exclusion is required.
