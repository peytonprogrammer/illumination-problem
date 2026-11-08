# A conditional signed-spanning mechanism from cylinder twists

[done] Initial conditional fixation lemma accepted by independent tools-disabled Opus review, with clarifications incorporated.
[done] Stronger aligned-core slope algebra and crossing/cochain signs accepted by independent tools-disabled Opus review.
[done] All52 theory-prescribed image paths pass independent original-framework optical/gradient replay.
[done] Prescribed horizontal/vertical homology test on the frozen ear surface.

This is a sufficient criterion, not the parity-room sign theorem. Its strong cylinder hypothesis fails on the frozen test room. The arguments below explain exactly which weaker geometric premise could still make this route useful.

## 1. Event classes and the missing sign

Let X be a translation surface obtained by unfolding a polygon. Mark a finite set A containing every lift of every polygon vertex, all of which are forbidden to a ray and all lifts of the source and target. A legal path avoids corners even at a reflex graze. For a strict one-corner midpoint event, let gamma1 run from its source lift to its corner lift, and gamma2 from that corner to its target lift. Both have the same developed half-displacement w. Set

    eta = gamma2 - gamma1 in H1(X,A;R),    hol(eta)=0.

The signed event row for an allowed polygon deformation v is

    g_e(v) = -sigma det(w, delta_hol_v(eta)).

Use actual half-displacements, not independently normalized primitive directions. Positive rescaling of rows does not change positive spanning, but it changes stress weights.

Assume that the chosen event has an admissible local continuation on its stated side, and every other point of its itinerary avoids A. The event-row identity and its implication for a negative derivative are the geometric inputs from the existing corner-event framework. No homology statement alone supplies those inputs.

## 2. Two twists fixing the event classes suffice

Suppose orientation-preserving affine maps f_h and f_v fix A pointwise and preserve the intrinsic local side used for smoothing the event on the unfolded surface. Physical wall sectors need not be fixed. Their derivatives are

    P_h = [[1,a],[0,1]],    P_v = [[1,0],[b,1]],    ab != 0.

Most importantly, assume for each event in a finite seed family that

    (f_h)_* eta_e = eta_e,    (f_v)_* eta_e = eta_e.          (F)

Suppose the seed rows span the full dual of the chosen deformation quotient. Then affine images of these events admit a finite strictly positive zero stress with full quotient rank.

**Proof.** An affine map takes a straight segment to a straight segment, preserves midpoint ratios and orientation, and takes the marked set to itself. Thus its images retain the sole forbidden corner contact and its admissible local side. A finite choice of powers avoids the finitely many projected wall-parallel directions. Under (F), the image rows are

    g_(h,n)(v) = -sigma det(P_h^n w, delta_hol_v(eta)),
    g_(v,m)(v) = -sigma det(P_v^m w, delta_hol_v(eta)).

This formula does not assert that the affine maps persist on the deformed surface: their action on the fixed topological classes is what is differentiated.

First take w=(p,q) with pq != 0. Choose positive integers N,M large enough that

    |A0|=|Naq| > 2|p|,    |B0|=|Mbp| > 2|q|.

Choose them also to avoid wall-parallel directions. The four image directions are

    (p+A0,q), (p-A0,q), (p,q+B0), (p,q-B0).

Give these four events weights

    1/4-p/(2 A0), 1/4+p/(2 A0), 1/4-q/(2 B0), 1/4+q/(2 B0).

All weights are positive, sum to one, and their weighted directions sum to zero. Bilinearity of the determinant gives a positive zero stress on the four event rows. The average of the first two rows equals the original seed row, so the packet span contains the seed row.

If p=0 or q=0, first apply a nonzero power of the other shear to make both components nonzero. Condition (F) still holds for the resulting event. Its four-row packet spans both determinant component functionals for this eta (differences of the horizontal and vertical row pairs give them separately), hence includes the original seed row too.

Repeat for each seed and add the packet stresses. The union has full quotient rank because it contains the span of all seed rows. A strictly positive zero stress on full-rank rows implies that every nonzero quotient deformation has at least one negative row: if all evaluations were nonnegative, their positive weighted sum being zero forces every evaluation to vanish, contradicting rank. This proves the conditional claim.

Duplicate events may be merged by adding their positive weights. The conclusion concerns a finite event family; it makes no uniform assertion about the size or length of the necessary powers.

## 3. A strong sufficient geometric condition for (F)

Suppose all horizontal cylinder core classes span a single nonzero line in H1(X;R). A horizontal affine multitwist that fixes A can be represented as a product of Dehn twists on annuli avoiding A. If a regular marked point lies in a cylinder, cut at its closed horizontal leaf and choose a sufficiently large common shear so that the twist is integral on every resulting subannulus. Square-tiled coordinates make these finitely many moduli and marked heights rational. Cylinder boundaries are pointwise fixed; a further power fixes all finite labels and sectors.

For a relative class eta, the twist difference is an absolute class in the span of the annulus cores:

    f_*eta - eta = sum_i n_i intersection(eta,c_i) c_i.

All c_i are homologous up to scalar under the one-dimensional hypothesis. On the other hand, affineness gives

    hol(f_*eta-eta) = (P_h-I)hol(eta) = 0

when hol(eta)=0. A nonzero horizontal core has nonzero horizontal holonomy, so holonomy is injective on that one-dimensional span. Therefore f_*eta=eta. The vertical argument is identical.

This uses one-dimensional **absolute homology span of cylinder cores**. A statement about Teichmuller rank, rational moduli, or one-dimensional holonomy images does not imply it. In particular, every horizontal cylinder period is horizontal, even when the cores represent many independent homology classes.

The twist construction is only asserted here for square-tiled surfaces and rational marked coordinates; no existence claim is made for arbitrary marked translation surfaces.

## 4. Exact applicability check: the strong condition fails

`twist-cylinders.py` builds only the frozen parity-W25-24 surface, using the previously audited square builder copied to `inputs/twist_origami.py`. It never calls a darkness decider or explores a shear orbit. For permutations r,u on n squares, the oriented cellular face row is

    h_s + v_(r(s)) - h_(u(s)) - v_s.

A cycle of r gives the sum of its horizontal edge rows; a cycle of u gives the corresponding vertical sum. These are homology representatives of core curves at an interior height. Stacked rows may duplicate a cylinder's core; including all of them does not change their span. Exact rational elimination computes

    rank(face rows + core rows) - rank(face rows).

Checks include permutation validity, connectivity, zero boundary of face/core chains, face rank n-1, vertex boundary rank, and Euler genus. Two prescribed controls are a one-square torus and a three-square genus-two L surface. The script also checks one rational instance of the four-weight formula.

|Surface|Squares|Genus|Horizontal core rank|Vertical core rank|
|---|---:|---:|---:|---:|
|Frozen ear example|112|28|15|15|
|One-square torus control|1|1|1|1|
|Three-square L control|3|2|2|2|

Thus Section 3 cannot justify (F) for our test room. This does not prove (F) false for particular event classes; it invalidates using the blanket rank-one-core shortcut here.

## 5. The remaining useful target

The weaker necessary input for Section 2 is that the chosen event classes are fixed by both twists. One could weaken it further to equality after evaluation by every allowed polygon-deformation period derivative, provided this equality is proved for every integer power used by the packets. For a multitwist T, (T-I)^2=0 on these relative classes because the cores avoid the marked endpoints. Hence one-step evaluated invariance implies invariance for every integer power. If an axis seed is first moved by the other twist, however, the evaluated invariance must also hold for that changed class. Full class fixation avoids this cross-twist issue.

The initial core-rank check did not compute that action. The follow-up fixed-event calculation now does so, as described next. Full absolute homology has dimension56 in the test room, whereas allowed room deformations have a much smaller image. Core rank15 therefore neither proves nor refutes the weaker evaluated-action condition.

A productive next calculation would reconstruct the actual relative chains of the already-saved events, their twist actions and their evaluations on the polygon deformation chart. It must account for corner sector labels and all regular marked lifts. It would use fixed event data and topological algebra, with no direction discovery. Until that premise is proved, the four-weight identity is a conditional mechanism, not a general illumination result.


## 6. Stronger mechanism: aligned core drift cancels the quadratic term

Class fixation is unnecessary if core period derivatives stay parallel to their cylinder direction. Assume the horizontal and vertical multitwists act by I+N_h and I+N_v on H1(X,A), with N_h^2=N_v^2=0. Write their derivatives I+L_h and I+L_v, where

    L_h(p,q)=(a q,0),    L_v(p,q)=(0,b p).

For an event class eta, the exact signed row of its nth horizontal affine image is

    g_h,n(v) = -sigma det(w+n L_h w, E(v)+n H(v)),
    E(v)=delta_hol_v(eta),    H(v)=delta_hol_v(N_h eta).

Suppose H(v) is horizontal for every allowed deformation. Then det(L_h w,H(v))=0, so

    g_h,n = g_0 + n s_h,
    s_h(v) = -sigma [det(L_h w,E(v)) + det(w,H(v))].

Similarly, if Z(v)=delta_hol_v(N_v eta) is vertical, then

    g_v,n = g_0 + n s_v,
    s_v(v) = -sigma [det(L_v w,E(v)) + det(w,Z(v))].

Neither identity requires H or Z to vanish. Each uses powers of a single twist acting on the original seed; it never composes different twists and needs no axis-seed reduction. An axis seed can have a zero slope for one twist and a useful slope for the other.

**Signed-slope criterion.** If finitely many slopes s_h,s_v obtained this way span the full deformation quotient dual, then affine images of the corresponding seed events positively span that dual.

Indeed, for any nonzero v some slope s(v) is nonzero. The sequence g_0(v)+n s(v) is negative for integers n of one sign with sufficiently large magnitude. Powers giving a projected wall-parallel direction can be omitted: when the twist changes the direction, only finitely many powers are bad; when it does not change the direction, that twist has zero slope under the alignment hypothesis and need not be used in a slope basis. This proves that all these orbit rows oppose every nonzero v. Compactness on the unit sphere and continuity of each row give a finite subfamily.

The only admissibility conditions used are: an unfolded straight event with one forbidden corner at its midpoint; distinct endpoint lifts; an admissible side for smoothing the corner; no other forbidden vertex contact; isolated wall-interior contacts away from that corner; and no segment parallel to a projected wall. There is no prescribed length bound, angle window, or minimality requirement. An orientation-preserving affine map fixing all vertex and endpoint lifts preserves straightness, midpoint ratio, sidedness and the incidence/avoidance conditions. Removing wall-parallel powers supplies isolated physical wall contacts. Thus images are geometrically available without discovering new reflection words.

**An explicit finite positive stress.** Select d independent slopes s_1,...,s_d. Write the corresponding base rows as g_i=sum_j A_ij s_j; this is possible because the slope basis spans the quotient. Choose an integer n larger than every absolute column sum of A, and avoid wall-parallel powers for the chosen events. Set

    c_j = sum_i A_ij,
    lambda_j,+ = (1-c_j/n)/2,
    lambda_j,- = (1+c_j/n)/2.

These weights are strictly positive, and

    sum_j [lambda_j,+ (g_j+n s_j) + lambda_j,- (g_j-n s_j)] = 0.

The row differences recover every s_j, so the 2 d-row family has rank d. This is a direct exact stress certificate, stronger than a rank-only observation.

## 7. Fixed-room realization and its scope

`twist-action.py` computes only the two prescribed annulus systems and the already-saved167 event words. It performs no orbit search and traces no affine-image paths. It constructs a piecewise-linear material deformation of the frozen triangular cellulation: original corners follow the supporting-line chart, smooth boundary grid points follow their wall fractions, the two marks follow their variables, and unmarked interior grid points may be held fixed. Each oriented cell edge carries the derivative of its developed vector. All112 face cochains are checked closed in both coordinates. Core sums therefore evaluate actual absolute-period derivatives, independent of this auxiliary interior gauge.

For every saved event, the checker reconstructs its original developed segments and locates crossings of horizontal or vertical annulus midlines. The difference of the second-half and first-half oriented crossing counts gives the intersection numbers of eta with the cores. At grid-line ambiguities every possible triangle assignment must produce the same annulus. No new direction is chosen or searched.

Every row-annulus has height1; the cylinder widths divide48. The maps which shear each horizontal annulus by48, or each vertical annulus by48, glue along pointwise-fixed boundaries, since48 is divisible by every width. They fix all grid vertices and the horizontal prongs for the horizontal shear, or vertical prongs for the vertical shear. Other directions, including physical wall sectors, generally move. They are affine maps of the original surface; their existence does not assume the deformed room is square-tiled.

The exact calculation finds:

- Horizontal and vertical core homology ranks are15, so class fixation does not follow from the earlier rank-one criterion.
- No saved event has a vanishing horizontal twist increment after evaluation on the room chart;8 have a vanishing vertical increment. None is fixed by both in this evaluated sense.
- Nevertheless, **every horizontal core-period derivative is horizontal and every vertical one is vertical** throughout the fixed-wall-direction deformation chart. The event increments therefore satisfy the alignment needed by Section 6.
- The combined signed slopes have rank26 in the29-dimensional chart, whose three symmetry dimensions are translation and uniform scaling.
- An exact26-slope basis yields52 affine-image rows at powers+2 and-2 of the shear48 maps, all away from wall-parallel directions. They have rank26 and a strictly positive rational zero stress. The smallest weight is12955111/32221952.

This supplies a computer-assisted structural explanation of signed spanning in this fixed room: all52 predicted orbit rows now also pass the original event framework's independent optical and signed-gradient replay. The earlier relative-action/sign-transfer blind spot is therefore checked directly for this certificate. It does not establish a universal parity-room sign theorem. The later `axis-alignment.md` now proves alignment in the full stated no-interior-B/C disk class. `twist-positivity-reduction.md` then transfers ordinary seed rank (or vector corner-period rigidity) to positive spanning of affine orbits. The remaining universal task is that seed-rigidity premise; the recorded one-room numerical rank does not prove it.


## 8. A geometric explanation of alignment in the fixed example

The final checker also identifies exactly two normal-incidence boundary crossings in each of the20 horizontal and20 vertical row cycles. These are crossings of a physical horizontal or vertical wall by a perpendicular axis-directed segment; they are not diagonal turns. The witness pairs are included in `twist-action.json`.

At a normal wall hit a billiard trajectory reverses and retraces its physical route. Between the two normal walls, the existing finite strict itinerary persists under sufficiently small supporting-line changes. It still travels in axis directions, since all mirror directions stay fixed. At the far normal wall it reverses and retraces again. Its developed return displacement is therefore along its original cylinder direction. This explains why its transverse period derivative vanishes; the cochain calculation checks that statement for the specific cellular classes.

This initially suggested a general alignment lemma. The subsequent fan-tree proof in `axis-alignment.md` now proves the normal-reflection property for the full stated no-interior-B/C disk class. The corresponding statement for arbitrary rational polygons is false: a polygon with only diagonal walls can have axis-directed closed trajectories with no normal reflection. The subsequent cylinder-mixing reduction replaces the separate universal signed-slope-rank problem by ordinary event rigidity; that rigidity premise remains open.


## 9. Intrinsic side convention and independent path validation

The exported side sigma is the sign of the infinitesimal angular perturbation at the source: velocity w+epsilon sigma Jw, where J is the counterclockwise quarter turn. It is not a side measured against a physical incident wall. For an orientation-preserving derivative P,

    det(Pw, P Jw) = det(P)|w|^2 > 0.

Thus P Jw is a positive multiple of J(Pw), plus a component parallel to Pw. The positive angular side is preserved; the parallel component changes speed only. On the tangent cone the lifted angle map satisfies phi(theta+pi)=phi(theta)+pi. Hence the intrinsic pi-side continuation is preserved even when the physical copy sector changes. The earlier corner framework explicitly requires labeled lifts and a legal side continuation; it has no path-length window or minimality hypothesis.

The original exact event engine provides a check against any error in this transfer or in the computed twist increments. `twist-replay.py` takes the52 directions, endpoint images and gradient rows already predicted by the action certificate, and uses the earlier independent infinitesimal event model to reconstruct their actual wall words. It checks the same physical corner, the exact target image at twice the transformed half-displacement, and the entire signed gradient in the original edge-length chart, after the established chart pullback. A cap is derived from the finite set of lattice mirror lines crossed before the prescribed target; it is not a direction radius or an evidence threshold. A failure is not reclassified as dark or used to choose another direction.

All52 prescribed cases passed, including the entire signed-gradient comparison. The replay reconstructs 49414 wall contacts in total; the longest word has1630 reflections. Results and actual words are in `twist-replay.json`. This validation is a prescribed-certificate replay, not a discovery search. The universal parity-room claims in Sections 7–8 remain open regardless of this fixed-room result.
