# Exact matching prerequisite and a continuous-selection obstruction

Status: new HAND challenge pending independent review. This supplements the frozen BD01/GT01 packets; it does not modify them or establish source-to-target existence. Full ordered/r3/r<=8 remains open.

## Scope and prior work

Use the integral strictly ordered spiral and actual native marks from BD01/GT01. Restrict here to l<t<w, 0<v<c and 0<epsilon<1/(2H), tau=P+epsilon. Write L=w-t>0 and G=h-c. BD01/GT01 are still pending independent review. The source-branch affine identity below is an application of the previously recorded interval-root/unfolding method, not claimed new. The specific obstruction concerns using GT01's new safe target gates as a globally continuous target curve. No search, numerical experiment, new engine or new clock is used.

## MS01: the safe target gates have no global continuous selector

For the safe pre-left-turn gates, with sigma in {-1,+1}, m a nonnegative integer, put

    F_(m,sigma)=2cm+c+sigma*v,
    D_(m,sigma)=F_(m,sigma)+G=2cm+h+sigma*v,
    x_(m,sigma)(epsilon)=t+epsilon*D_(m,sigma).

These are genuine negative/downward cap states exactly on their strict gate domain

    0 < epsilon*F_(m,sigma)-L < 2c*epsilon.

Conditional on the BD/GT physical proofs, every such branch is corner-free before T. GT01 establishes at least one valid branch at every epsilon in the declared interval. Nevertheless there is NO continuous function x(epsilon) on the ENTIRE interval (0,1/(2H)) choosing one of these safe states at every epsilon.

Proof. Distinct indices have distinct D: within one sigma their differences are nonzero multiples of 2c; between signs equality would require an integer m difference equal to v/c, impossible since 0<v/c<1. Indeed their separation in D is at least delta=min(2v,2(c-v))>0. On any compact epsilon neighborhood away from zero, the strict thin gate bounds x between w+G*epsilon and w+(G+2c)*epsilon, so only finitely many D values can occur locally. Therefore a continuous selector must choose a locally constant branch index: two allowed branches never meet, and all other branches are uniformly separated near each positive epsilon. Connectedness makes that index constant throughout the interval. But every fixed branch has epsilon>L/F_(m,sigma)>0, and hence cannot cover epsilon arbitrarily close to zero. Contradiction.

At strict-alignment endpoints a branch is absent because its bottom entrance or first underside contact is a true corner. The other safe sign remains available, but at a different physical cap position. Replacing the missing branch by the surviving branch is a discontinuous switch, not continuation through a legal state.

Limits: this refutes a continuous-selector claim for the TWO SAFE preturn families only. It does not exclude a selection using the additional postturn gates, further target-return histories, or a more appropriate covering/cycle construction. No such larger continuous selection or nonzero degree is asserted. It also does not disprove existential illumination.

## MS02: each regular source/target branch match is transverse and rational

Fix one finite actual S-to-cap itinerary, including initial horizontal sign and all wall/prong choices, on an open epsilon component where it stays regular and ends at h with negative/downward germ. With |vy|=1 its vertical duration D_S is a positive integer: initial height, final height and all horizontal-wall heights are integral, and vertical reflections do not change absolute vertical speed. Composing vertical-wall reflections gives

    x_S(epsilon)=C_S-epsilon*D_S,

where C_S is an integer; the P*D_S term is absorbed in C_S. The minus sign is the ACTUAL final horizontal sign, not a chosen chart label. This identity follows by unfolding the whole fixed word, preserving actual S and all wall guards.

On one safe target branch x_T=t+epsilon*D_T with D_T=D_(m,sigma)>0, the exact difference is

    x_S-x_T=C_S-t-epsilon*(D_S+D_T).

Thus there is at most one match in that common regular component, at

    epsilon_*=(C_S-t)/(D_S+D_T).

It must lie STRICTLY within both physical guard domains. At that root the position and BOTH physical velocity signs coincide, so concatenation is one regular actual ray reaching T; an earlier actual T can be truncated. A corner at the candidate root invalidates that itinerary. The original source history need not be the last-source suffix; no uniqueness or global source-chart claim is needed.

For native even-even S,T and integral walls, C_S and t are even, so epsilon_*(D_S+D_T) is an even integer. In particular any match has rational epsilon. More generally, any finite regular actual native S-to-T ray has rational slope by integer unfolding, independent of this safe-target subclass. Hence irrational epsilon has NO source/target intersection even though GT01 supplies target access there. This is a check against a proposed fixed-epsilon surjectivity inference, not an obstacle to existence at some rational epsilon.

## What would establish positive progress

A sufficient next lemma is: for every residual actual pair there exist ONE finite regular negative/downward source branch, ONE safe target branch (or a proved larger target class), and a common strict guard component containing epsilon_* above. A sign change on a connected common component with a root remaining strictly guarded would prove this for that component. Neither an independently nonempty source set and target set nor opposite signs observed on different components proves it.

The two new packets reduce target-side availability; they do not provide this global selection. MS01 specifically blocks using their pointwise availability as an unproved continuous curve through all branch breaks. MS02 applies the old root identity to the newly explicit target branches and makes the missing common-component requirement precise; it is NOT another global theorem or room-coverage result. Independent author/coordinator review of BD/GT/MS is pending.
