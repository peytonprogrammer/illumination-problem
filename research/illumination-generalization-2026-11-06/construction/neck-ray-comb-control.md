# Exact control: all integer stretches of the five-neck comb

A prescribed hand control for A21 and the peer's R19 sharpness family. It is not a census, direction search, general base-illumination theorem.

For integer n>=0 let P_n be the union of the spine [0,4]x[0,36] and five teeth

    [4,20+2n] x [8j,8j+4], j=0,...,4.

Take actual marks S_n=(8+2n,2), T_n=(8+2n,34). This varies the free gap between x=4 and the marks' x level by2n, extending all five teeth and translating both marks. Each room is a strictly simple orthogonal20-wall canonical45 disk. The marks are distinct interior even-even A points. Its corresponding generic vertical cut has five necks and a K1,5 tree.

Here is an exact actual path for EVERY n>=0. Starting at S_n, list the bottom-tooth contacts

    B_k=(8+2n-(k+1/2), 4 if k even else 0),
    k=0,...,3+2n.

Then reflect at V=(0,18). List the upper-tooth contacts

    U_k=(9/2+k, 36 if k even else 32),
    k=0,...,3+2n,

and finish at T_n. The total number of reflections is

    (4+2n)+1+(4+2n)=9+4n.

## Exact physical verification

The initial vector is (-1/2,2), of vertical/horizontal magnitude4. Consecutive bottom contacts differ by (-1,+/-4), with the sign of the vertical velocity reversing at each horizontal mirror. All bottom contact abscissae lie between9/2 and15/2+2n, strictly inside their floor/ceiling walls and strictly less than20+2n. In particular none is the true reflex corner at x=4 or an outer corner.

The last bottom contact is (9/2,0), because 3+2n is odd. From it the path goes to V with vector (-9/2,18), crossing the tooth/spine mouth at (4,2). Until V it stays strictly inside the spine, apart from the intended smooth left-wall contact at y18. Its horizontal velocity reverses there while vertical velocity stays positive.

The next segment goes from V to U_0=(9/2,36), with vector (9/2,18). It crosses the spine/upper-tooth mouth at (4,34), strictly inside it. Every intermediate height on the central transit has x<4, so no middle tooth boundary or artificially capped opening is touched. Additional middle teeth are physical openings, not mirrors used by this path.

Consecutive upper contacts differ by (1,+/-4), reversing vertical velocity at each actual horizontal wall. Their abscissae lie between9/2 and15/2+2n, strictly inside the upper tooth's floor/ceiling walls. Its last contact is (15/2+2n,32); the final vector to the ACTUAL T_n is (1/2,2), with the required slope and direction. T_n lies strictly inside the top tooth.

The whole finite path therefore obeys the actual law of specular reflection and avoids every genuine corner. All joint crossings have ordinate2 or34, strictly inside the relevant width4 mouths. For n=0 the listed nine-reflection witness is explicit; the formula additionally closes all integer stretches in this particular five-neck generator family, without relying on an eventual threshold or the pending tree extension.

This validates an actual branching control below21walls. It does not establish all pairs in these rooms, all coordinates/teeth dimensions, or any other generator/base family.
