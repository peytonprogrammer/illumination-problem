# Witness propagation on a fixed parallel-neck tree

A21 scope supplement; same original effort and deadline. Frozen earlier packets are unchanged. Independent review pending.

## Quantified statement

Let a finite strictly simple orthogonal polygonal disk be partitioned into finitely many fixed orthogonal chamber shapes joined by horizontal rectangular necks. The chamber adjacency graph is a finite tree. Distinct neck interiors and chamber interiors are disjoint, and the only joins are full smooth mouth apertures. Different mouths of one chamber may lie on the SAME side; arbitrary branches are permitted.

Each chamber moves only by a horizontal rigid translation as the neck lengths change. Its shape, vertical coordinates and actual marked points stay fixed in its local coordinates. Each neck e has a fixed positive width w_e, with a common positive multiple H satisfying H/w_e a positive integer for every e. The neck lengths are

    L_e(lambda)=p_e*lambda+c_e,  p_e nonnegative integers.

Assume this gives valid strictly simple disks for a final interval of real lambda. The actual S,T may belong to any fixed chambers, including the same one. They remain distinct actual interior points. Suppose at one parameter lambda0 there is a finite actual corner-avoiding S-to-T path. Then the actual pair illuminates at EVERY sufficiently large real parameter.

If the witness uses no growing neck, that SAME physical path, translated rigidly with its visited fixed subnetwork, persists for all later parameters. If it uses a growing neck, the realized-copy congruence argument below produces eventual illumination. No one-pass or leaf-to-leaf condition is imposed. The statement is not a claim that any witness exists on any given ray.

## Why neither a serial chain nor opposite mouths are needed

Absorb sufficiently short fixed end rectangles from every neck into its adjacent chambers. Choose the cuts away from the finitely many witnessed horizontal reflection positions, as in the A21 buffer proof. All cut crossings are strictly interior and transverse. This repartitions the physical room without introducing mirrors or forbidden points. At lambda>=lambda0, buffered lengths remain positive.

Every neck visit is a full traversal: inside a horizontal rectangle, horizontal velocity cannot reverse. Decompose the finite witness into its chamber blocks and neck traversals. A chamber block may return to the same mouth, leave through a different mouth on the SAME wall side, or visit a branch. Record its actual finite reflection word, entry and exit and all signs. These are ordinary finite nonsingular segments in a fixed orthogonal chamber; their strict guards are open. No auxiliary cap reflection or claim of minimality in a multi-mouth chamber is used.

Unfold the complete finite witness with initial horizontal speed positive and normalized to1. If it visits a growing neck, that component is nonzero. Each complete traversal contributes its neck's positive length to developed horizontal travel. The cumulative developed abscissae at designated cuts and at the actual target have the form

    X_i(lambda)=r_i*lambda+d_i,
    D(lambda)=q*lambda+C,
    r_i=sum over preceding traversals of p_e,
    q=sum over ALL traversals of p_e >0.

These r_i and q are integers. Across a chamber block r_i does not change, regardless of which physical mouths it connects. Across a neck e it increases by p_e. The distances inside each recorded chamber word are fixed by its vertical supporting lines; a return or same-side block has a positive developed horizontal distance, not a negative traversal contribution.

Let the reference actual-T image ordinate relative to S be Y0=tau0*D(lambda0). Choose an integer z and slope

    tau_z=(Y0+2Hq*z)/D(lambda),
    |tau_z-tau0|<=Hq/D(lambda),

using nearest-integer selection. At EVERY designated cut,

    tau_z*X_i(lambda)-tau0*X_i(lambda0)
      =2H*r_i*z+(d_i-r_i*C/q)*(tau_z-tau0).

Propose the actual reference portal/chamber copies translated vertically by2H*r_i*z. The remaining local-coordinate perturbations tend uniformly to zero over the finite itinerary.

The copy induction in the commensurate supplement now applies verbatim:

* The initial block has r_i=0 and starts at actual S.
* A chamber block has equal r_i at both ends, so one uniform vertical translation preserves its ENTIRE witnessed word, even with same-side or same-mouth exits.
* A neck e changes the proposed copy shift by2H*p_e*z, an exact integer multiple of its own period2w_e. The straight developed segment realizes that allowed winding with the recorded fold signs and strict mouth coordinates.
* The terminal block has r_i=q, so its actual target image shifts by exactly2Hq*z, the endpoint imposed by the chosen line.

A finite common slope tolerance keeps all chamber words and cut phases legal. Since D tends to infinity, nearest-image slopes meet that tolerance for every sufficiently large lambda. The exact target-copy equality realizes the actual T, rather than just a projected or modulo image. Finitely many reflections occur for each finite parameter; extra interior revisits are permitted.

If q=0, the witness uses only fixed-length necks. Its visited chambers form a connected subgraph containing no growing edge. Fixed lengths and fixed chamber-mouth local positions force their relative translations to stay constant. The entire witnessed geometry therefore moves by one rigid horizontal translation, preserving the actual path and marks. This also covers a wholly vertical witness within a fixed chamber.

Thus the number of chambers, tree branching and same-side port combinations cause no additional proof obstruction. The essential hypotheses are fixed chamber geometry/marks, parallel necks of commensurate widths, nonnegative rational-affine length growth and a supplied actual finite witness.

## Application to an orthogonal coordinate-gap generator

This is a CONDITIONAL application pending independent acceptance of both this optical supplement and the peer's separate geometric strip-generator theorem. That theorem claims that varying one free coordinate gap cuts an orthogonal disk into a tree of fixed chambers joined by parallel necks, with the actual marks retained in the chambers by collars. For a vertical free gap, the necks are horizontal. In lattice data every width is an integer, so H exists. Each neck has the same integer growth coefficient, and all other geometry is fixed. Rotating the coordinate frame treats a horizontal gap.

If those structural claims hold, then ONE actual illuminating witness at any parameter on a single-gap ray implies eventual illumination along that ray, including all multi-mouth, same-side and branching cases. The proof does not need to solve new auxiliary multi-mouth billiards; it only reuses the finite actual witnessed itinerary.

This does not prove that the geometric bases illuminate, that one witness exists on each ray, that their thresholds are uniform across other gaps, or that arbitrary combinations of perpendicular gap changes preserve a witness. Independently varying other generators changes chamber shapes and lies outside this fixed-shape argument. No full W<=21 theorem follows without those additional implications. There is no practical atlas enumeration, discovery search.
