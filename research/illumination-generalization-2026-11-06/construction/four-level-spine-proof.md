# Four physical turning levels from actual spine-end reflections

A38 candidate, pending independent review. This constructs actual finite paths; an auxiliary infinite strip is used only with explicit reflection guards. No complete W<=21 theorem is claimed.

## 1. Domain and result

Let P be a finite strictly simple two-sided rectangular-spine comb. Translate its global bottom to0, so its core is [0,c] x [0,G], c,G>0. Every tooth band lies in [0,G]; same-side tooth bands have positive gaps. Opposite-side bands may overlap. Two selected right teeth have the same height u and actual middle-row marks

    S=(c+D,s), T=(c+D,t), 0<s<t<G, D>=0.

Their actual far ends lie strictly beyond c+D. D=0 denotes actual interior mouth-seam midpoints. Their two selected bands are disjoint because they lie on the same side. Put

    h=(t-s)/2, mu=(s+t)/2,
    L={h,mu,G-mu,G-h}.                                    (1)

Every member of L lies strictly in(0,G). If ANY level ell in L is either a smooth actual left-core wall point (0,ell), or the middle ordinate of an actual left tooth, then S and T illuminate by a finite corner-avoiding actual path.

For integer geometry, selected height2 teeth and actual A marks, every level in L is an integer. If every opposite left tooth ALSO has height2, actual darkness therefore requires EVERY level in L to be an actual left-mouth ENDPOINT. This is necessary only; simultaneous endpoint obstruction does not imply darkness.

## 2. Exact physical spine unfolding

Define the triangular fold F:R->[0,G] by

    F(y)=y on[0,G], F(y+2G)=F(y), F(-y)=F(y).

On each open cell between consecutive multiples of G it is an isometry with derivative+1 or-1. Reflect copies of the two selected right teeth and all other teeth at the global horizontal ends; their bands are corresponding images under y->+/-y+2jG. The core becomes the infinite strip 0<=x<=c. Each copied tooth is an image of an ACTUAL tooth; a hypothetical extra mirror at a tooth mouth is never introduced.

Use one of the four ACTUAL target images with centers

    t_1=t, t_2=t+2G, t_3=-t, t_4=2G-t.

The source center stays s. Reflection in each image midpoint a_i=(s+t_i)/2 interchanges the two equal-height, equal-depth selected marks in this extended strip. The physical midpoint levels are respectively

    F(a_1)=mu, F(a_2)=G-mu,
    F(a_3)=h, F(a_4)=G-h.                                  (2)

Neither a_i nor either selected portal is at a multiple of G. The first assertion follows because all levels in(2) are in(0,G). The second follows because a strict portal is inside a copied tooth band, whose interior lies strictly between its associated global end lines. This includes teeth flush to a global end: their strict portals avoid that endpoint.

The two selected right-band images are disjoint in every case. For t_1 this is the actual same-side separation. The t_2 band is above the entire base cell. The t_3 band is below0 and the source band is in[0,G]. The t_4 band is aboveG and the source band belowG. Thus the same-side midpoint matching construction applies after ordering the two virtual endpoints; when necessary reverse its path to start at the actual source image s.

## 3. Smooth-wall level gives an actual reflected-spine path

Suppose ell=F(a_i) is a smooth actual left wall point. Apply the equal-arm accepted A32 construction in the extended core, using only the two selected tooth images. Its floor indices and residuals agree at both ends, so its unique left-wall reflection is exactly(0,a_i). Every selected tooth horizontal contact is between its mouth and its actual mark x coordinate. Every open core leg has0<x<c. If D=0 both tooth arms are empty, their indices0 and residuals u/2; the core legs begin/end at the actual strict seam points.

Fold this finite path by (x,y)->(x,F(y)). Its selected-tooth horizontal mirrors map to actual selected-tooth mirrors. Its reflection at(0,a_i) maps to the specified SMOOTH actual left wall. Every crossing of a global end line y=jG on an OPEN core leg has0<x<c and produces exactly an ordinary specular reflection at the ACTUAL horizontal spine end. It cannot be a corner: the left reflection and both portals have already been excluded from end-line coincidences. The slope is nonzero, so these crossings are isolated and finite.

If a selected tooth is flush to an end, a horizontal tooth-wall contact may itself be at y=jG with x>c. The virtual trace then bounces on that line rather than crossing it; folding conjugates that existing actual tooth-wall reflection and does not insert a second reflection. Its x is strictly within the selected wall. There is no gliding or multiple-wall event.

The starting image folds to S and the terminal target image folds to ACTUAL T. No other tooth mirror is touched: all core legs have strict x, and selected arms stay within their copied rectangles. The result is a legal finite actual connection. Truncation at an earlier actual T, if present, preserves legality.

## 4. Centered-tooth level gives an actual far-wall return

Suppose ell=F(a_i) is the middle ordinate of an actual left tooth. One reflected copy of that tooth is centered at a_i. Its band is the inverse image of the whole physical band under a single local branch of F. Let its width be w and its far-wall midpoint be M=(-w,a_i).

Apply the protected opposite-side midpoint construction to the virtual source and M, using their actual copied rectangles and the core strip. This is the R35 opposite-side finite floor matching. Its proof uses only open core segments and selected tooth mirrors, so choose any finite auxiliary strip height containing these bands if a finite polygon is desired; neither artificial end is touched. A zero source depth is permitted directly: its floor index stays0, its residual is u/2, and its arm is empty. The nonempty central leg starts inward from the actual seam. The terminal far-wall midpoint has nonzero horizontal arrival component and is its first far-wall hit.

Follow this prefix by its reversed image under J_i(x,y)=(x,2a_i-y). The copied left tooth is J_i-invariant. The used source tooth portions map to the selected TARGET image portions because their equal heights/depths are symmetric about a_i; unused far ends may differ. All central segments remain in the extended strip. At M, reverse plus J_i gives outgoing(-v_x,v_y), exactly the actual vertical far-wall reflection law. M is a smooth tooth-wall midpoint, not a mouth endpoint or convex corner.

Now fold the COMPLETE finite trace by F. Its source and target copied arms map to their original actual teeth and actual endpoints. The centered left tooth copy maps to its actual tooth; all far and horizontal contacts stay smooth. Open core crossings of end lines again occur strictly at0<x<c and are ordinary ACTUAL floor/ceiling reflections. The far midpoint has F(a_i)=ell strictly between0,G, so no far-wall splice coincides with a global end. Contacts of a flush tooth on an end line are treated as existing horizontal reflections exactly as in section3. Therefore the finite folded connection is legal. This argument requires local symmetry only in the selected copied rectangles, not global symmetry of P or commutation of J_i with F.

## 5. Necessary endpoint obstruction and a complete low-branch consequence

Assume all boundary coordinates are integral and every tooth has height2. For actual A marks, the unshifted s,t relative to the integer global floor are integers with even difference. Thus h,mu and all four levels(1) are integers. An integer level strictly inside a height2 opposite band is exactly its midpoint. A level outside all closed opposite bands is a smooth actual left-wall point. Every level in L lies strictly inside the spine height range. Sections3–4 therefore show that ACTUAL DARKNESS requires every one of those levels to be an opposite mouth endpoint.

There are at least THREE distinct levels: h<G-h, while both mu and G-mu lie strictly between them, since s>0 and t<G. A single opposite tooth has only two mouth endpoints. Consequently EVERY vertically aligned actual A pair in same-side height2 teeth illuminates whenever there is at most ONE opposite-side tooth. This conclusion has no k, wall, size, width, depth or diameter cap and no finite-prefix remainder. Horizontal reflection gives the other orientation. Opposite-side pairs already illuminate by R35/A35.

For width1 integer teeth, every actual outside-core A point is a mouth seam midpoint: the tooth has no interior integer x coordinate and no other interior integer y row. Thus, as an additional complete subclass, every actual A pair illuminates in every such comb with at most three total teeth, all of height2. Strict-core pairs and strict-core/midrow pairs use direct protected paths from A35; same-tooth pairs are directly visible; opposite-side pairs use A35/R35, including empty seam arms; distinct same-side seam pairs have the same x and at most one opposite tooth, just proved. Core width may be odd or even and tooth bands may overlap across sides. No arbitrary off-midline seam point is admitted.

For more opposite teeth, simultaneous corner obstructions can occur in this four-level construction. No darkness is inferred. The prescribed core[0,1]x[0,16] with right bands[1,3],[13,15], left bands[6,8],[10,12], unit left widths and right width2, has levels6,8,8,10, all mouth endpoints for S(2,2),T(2,14). This only identifies a residual optical case for a new mechanism, not a dark counterexample. The general uncapped W<=21 theorem remains OPEN.
