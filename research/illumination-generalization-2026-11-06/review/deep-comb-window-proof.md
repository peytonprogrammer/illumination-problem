# R39: witness existence from three separated bend windows

Author theorem pending independent review. Universal canonical45W21 remains OPEN. This effort retains its original aggregate deadline in deep-comb-window-effort.json.

## Statement

Let a finite strictly simple two-sided rectangular-spine comb have core[0,c]x[0,G], c,G>0. Teeth are rectangles attached to either side, all their bands in[0,G], with positive gaps between same-side bands. Tooth widths, heights and placements are arbitrary positive REAL numbers; opposite-side bands may overlap. Let B>0 bound the heights of all teeth on the OPPOSITE side from two selected same-side teeth. Selected heights are u,v>0, and their actual middle-row interior marks are S=(c+D_s,s), T=(c+D_t,t), s<t, D_s,D_t>=0. Each selected width extends strictly beyond its own actual mark; D=0 is an actual interior seam point. Other same-side teeth can have arbitrary heights.

Define delta=(u+v)/4, h=(t-s)/2, mu=(s+t)/2, q=min(s,G-t). Suppose

    h >= B+delta,       q >= B+2delta.                 (1)

Then S illuminates T if W<=23. There is no equality exception in(1), initial witness, finite-prefix hypothesis, bound on endpoint depths or tooth widths, arithmetic commensurability assumption, or restriction on joint growth. W counts actual maximal straight walls. An arbitrary actual left/right or vertical reversal gives the corresponding orientation.

In particular, when all teeth have integer height2, B=2, u=v=2, conditions are h>=3,q>=4. This covers arbitrary independent integer tooth widths and UNEQUAL actual even abscissae. It includes genuine interior tooth marks, not just unit-width seams. No general all-pair comb theorem follows when these clearance inequalities fail.

## 1. Unequal-depth, unequal-height matched chart

Take any two selected copied rectangles with centers a<b, heights u_a,u_b, midpoint depths D_a,D_b>=0, bands disjoint, and equal core width c. Put Delta=b-a and H=Delta+(u_a+u_b)/2. The accepted A32 monotone finite matching has

    A=D_a+D_b+2c,
    n_a(tau)=floor(D_a*tau/u_a+1/2),
    n_b(tau)=floor(D_b*tau/u_b+1/2),
    Phi(tau)=(Delta+u_a*n_a(tau)+u_b*n_b(tau))/A.

Its increasing iteration from0 is bounded by H/(2c), has finitely many output values and stabilizes at a positive tau. At the FIRST stationary value no changing floor can jump: a jump there would strictly increase Phi beyond its preceding output tau. Zero-depth indices are constant0. Therefore the residuals

    r_a=u_a/2+D_a*tau-u_a*n_a(tau),
    r_b=u_b/2+D_b*tau-u_b*n_b(tau)

are strict: 0<r_a<u_a, 0<r_b<u_b, and r_a+r_b+2c*tau=H. The original A32 parity choices construct actual tooth prefixes with upward portal velocity, including an empty arm at D0. All tooth contacts occur strictly BETWEEN the selected mark and its mouth, so the unused far widths impose no upper bound and no far corner is met.

The lower portal is p_a=a-u_a/2+r_a, and upper portal p_b=b+u_b/2-r_b. The two straight core legs have identical slope tau and meet the opposite side at height

    z=(p_a+p_b)/2
     =(a+b)/2+[(r_a-u_a/2)-(r_b-u_b/2)]/2.

Consequently

    |z-(a+b)/2| < (u_a+u_b)/4 = delta.                (2)

These are strict matched paths with their original endpoint positions and one global direction. The opposite turn is valid in the full actual room whenever its height z lies on a smooth actual wall. A turn inside a tooth opening or on its endpoint is not accepted. No centered-tooth return or equality of endpoint depths is used in this argument.

## 2. Three actual end-reflected charts and their strict windows

Use the same genuine end fold F(y)=y on[0,G], F(-y)=F(y), F(y+2G)=F(y). Select original source center s and target image centers t,-t,2G-t. They are actual reflected copies of the selected target rectangle. Their bands are disjoint from the selected source band, as in the accepted A38 construction. If the target image is lower, swap the order for matching and reverse the resulting path. Its actual depths and heights remain attached to the correct endpoints.

The virtual mean heights fold to mu,h,G-h, respectively. The fold F is1-Lipschitz. Thus the three constructed opposite turns, after folding, have physical heights z_mu,z_h,z_top with

    |z_mu-mu|<delta, |z_h-h|<delta,
    |z_top-(G-h)|<delta.                              (3)

All windows are strictly inside(B,G-B): their centers are at least h from both ends or are between h and G-h, and h>=B+delta. In particular no turn is on a global end line.

If a chosen turn is a smooth actual opposite wall, fold the ENTIRE matched path. Every open core leg has0<x<c. Crossings of y=jG therefore become ordinary smooth reflections at the actual floor/roof. Strict portals are in the interiors of copied tooth bands, never on end lines. Every copied tooth contact maps to a real horizontal selected-tooth wall. Existing contacts of a flush tooth on an end line are ordinary reflections, not an extra crossing. Its two incident segments lie in that copied band; the local folding isometry preserves their reflection law. All reflections and crossings are finite. The path begins at original actual S and ends at original actual T. If an earlier actual T occurs, truncate there. There is no corner continuation, artificial seam mirror, or selected-lift substitution.

## 3. Darkness requires three different nonflush opposite teeth

Assume actual darkness. Then each of the three constructed turns must fail to be a smooth actual opposite wall, so lies in a CLOSED opposite tooth mouth band. This conclusion does NOT assume the turns are integers or equal to the nominal means. A band endpoint is correctly included as a failure. Every opposite tooth has height<=B.

The centers are ordered h<mu<G-h with gaps s and G-t. By(1) both are at least B+2delta. By the strict inequalities(3), any two successive actual turns therefore differ by STRICTLY MORE than B. One opposite tooth band of length at most B cannot contain both. At least THREE DIFFERENT opposite teeth must block these turns.

All three turns are strictly in(B,G-B), as just proved. A bottom-flush opposite tooth of height<=B ends at most at B; a top-flush one starts at least at G-B. Neither can contain a turn. Thus all three blockers are NONFLUSH. The two selected teeth are also nonflush: s>=q>=B+(u+v)/2>u/2 and G-t>=q>v/2. They are distinct same-side teeth and distinct from all three blockers.

For an arbitrary rectangular comb the full actual maximal-wall identity is

    W=4+4*N_nonflush+2*N_flush.

It holds for independent tooth heights and widths: a nonflush attachment splits one positive core-wall gap and adds its three outer sides, net4; a flush attachment extends a global end and adds two turns, net2. Positive same-side gaps prevent degeneracy. Opposite-side coincidences do not merge boundary walls through the core interior. No tooth spans the entire core height here: an opposite spanning tooth would have height G<=B, incompatible with(1), and each same-side tooth is separated from the two selected bands. Consequently the stated charge applies to the entire room, including unused attachments.

The five forced nonflush teeth give W>=24, contradicting W<=23. Hence at least one of the three matched turns is smooth and supplies the actual finite witness constructed in sections1-2.

## Scope and relationship to the strip-program gap

This supplies witness EXISTENCE directly, with no provided witness, finite list of gap residues, asymptotic threshold, or propagation assumption. All independent transverse tooth widths and endpoint depths can vary without limit while(1) holds. Varying the heights and vertical gaps is also permitted if(1) remains true for a valid bound B. This is a positive region of genuinely joint metric fibers.

The boundary regime q<B+2delta or h<B+delta is open here; so are general tooth/chamber geometries and diagonal walls. This theorem does not replace the remaining universal strip-generator witness or finite-prefix bridge. A47's unitwidth q>=3 theorem is stronger in that single restricted q3 regime; R39 instead removes the unitwidth/equal-abscissa and equal-height assumptions. No novelty, formalization or universal completion is claimed.
