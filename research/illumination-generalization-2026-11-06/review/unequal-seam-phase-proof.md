# R50: explicit positive seam phases for unequal selected widths

Author theorem pending independent review. Original conservative effort start07:23Z/deadline07:37Z includes the least-fixed-point derivation. Universal canonical45W21 remains OPEN.

## 1. Exact direct witness criterion

Let P be a finite strictly simple two-sided rectangular-spine comb with positive REAL core widthc and independently arbitrary positive REAL tooth widths. Every vertical band edge and core floor/roof coordinate is integral and every tooth has height2. Same-side bands have positive gaps, opposite overlaps are allowed. Consider ACTUAL SAME-SIDE interior seam midpoint marks S=(c,s),T=(c,t), s<t, with even t-s. They may have UNEQUAL selected widths w_s,w_t. Put

    h=(t-s)/2>=2, mu=(s+t)/2,
    H in {h,mu,G-mu}.

For ANY realw>0 andH>=2 define the explicit functions

    n_H(w)=floor((w/c)*(H-1/2)+1/2),
    tau_H(w)=(H+n_H(w))/(c+w),
    m_H(w)=w*tau_H(w)-n_H(w)
          =((w/c)*H-n_H(w))/(1+w/c).                (1)

If, for ANY of the three displayedH,

    m_H(w_s)*m_H(w_t)>0,                            (2)

then S illuminates ORIGINALT by a finite corner-avoiding ordinary specular path. No wall bound, input witness, width equality, commensurability, finite-prefix assumption, reflection cap or size/diameter bound is required. Actual A pairs are applications when their physical coordinates have that designation. The optical statement itself permits real horizontal data.

The key distinction from the equal-width A37/A56 response is that the two complete candidates generally have DIFFERENT slopes. I construct EACH complete S-to-T candidate using its own matched slope, then choose one. I never join a source arm at tau_s to a target arm at tau_t.

## 2. Closed formula for the FIRST stationary phase, all equality cases

Writeq=w/c>0. The accepted far-only seam iteration is

    tau_0=0,
    tau_(j+1)=(H+floor(w*tau_j+1/2))/(c+w).

Its integer-index map is f(n)=floor(q*(H+n)/(1+q)+1/2). A fixed integern satisfies EXACTLY

    qH-(1+q)/2 < n <= qH+(1+q)/2.                  (3)

The least integer strictly above the lower endpoint is

    n*=floor(q*(H-1/2)+1/2).

It is nonnegative forH>=2. The interval length in(3) is1+q>1, so this least integer lies STRICTLY below the upper endpoint as well. Thus it is a fixed point with BOTH strict half-integer phase guards; no floor discontinuity is accepted.

Starting with index0, monotonicity of f makes the integer sequence nondecreasing. Sincef(n*)=n*, every index is<=n*. Therefore finitely many index increases lead to a fixed index. Every fixed index is>=n* by its minimality in(3), so the first stationary index is EXACTLYn*. Its slope andm are(1), with

    -1/2<m_H(w)<1/2.                              (4)

This handles every real ratioq and every equality in the floor argument. It does not assume the iteration picks an arbitrary fixed point or replace it by a convenient nearby phase.

## 3. Two actual COMPLETE far-only paths in the ordinary chart

First take copied lower/upper seam centersa<b, withH=(b-a)/2 and meanM=(a+b)/2. Use the original charta=s,b=t initially.

For the SOURCE-ONLY far response setn_s=n_H(w_s), tau_s=tau_H(w_s), m_s=m_H(w_s). The strict source mouth is at(c,a+2m_s). Develop the source arm in its height2 strip over depthr in[0,2w_s], with depth folded by

    p(r)=r forr<=w_s, p(r)=2w_s-r forr>=w_s.

Written in reverse from that mouth, its height is

    a-1+F(1+2m_s-tau_s*r),

whereF is folding modulo4 into[0,2]. At r=2w_s the phase is1-2n_s and folds to the ORIGINAL seam midpointa at physicaldepth0. Reverse the finite arm to start at actualS. Its outgoing mouth velocity is left/up with slopetau_s. Then take the two core legs through

    (0,M+m_s), then ORIGINALT=(c,b).

They match EXACTLY becausec*tau_s=H-m_s. The source prefix's genuine far crossing atdepthw_s has phase1+w_s*tau_s-2n_s; a far corner would requirew_s*tau_s an ODD integer. Ifm_s!=0, (4) makesw_s*tau_s=n_s+m_s nonintegral, excluding it. All internal horizontal contacts have positive physical depth; the only depth0 points are the actual source and its strict final portal. The target arm is EMPTY and its unused width never enters this complete construction.

For the TARGET-ONLY far response independently computen_t,tau_t,m_t fromw_t. Start at actualS=(c,a), turn at

    (0,M-m_t), then enter the strict target mouth(c,b-2m_t).

The two core legs have their OWN common slopetau_t, again usingc*tau_t=H-m_t. Append the target arm over0<=r<=2w_t, physicaldepthp(r), height

    b-1+F(1-2m_t+tau_t*r).

Its terminal phase is1+2n_t, so it ends at ORIGINALT with depth0, not at a virtual depth2w_t mark. Its far corner is excluded by nonintegrality ofw_t*tau_t whenm_t!=0. The source arm is EMPTY, no seam is a mirror, and no false horizontal continuation through an open mouth is inserted.

Thus these are two DIFFERENT complete candidate trajectories, with opposite-signed nominal turn shifts when(2) holds. Every core leg has strict0<x<c. Their portals are strict by(4), and all selected contacts use the actual selected tooth rectangles. Their only possible missing wall is the designated opposite side turn. Each source/target far reflection is on its own true finite wall; no unequal width is substituted for the other.

## 4. Selecting a genuine opposite mirror and the actual end charts

If the nominal mean level is a smooth actual opposite wall or a tooth MIDPOINT, accepted A38/R35 already provides an actual connection without(2). At an integer opposite-mouth ENDPOINT, integer band edges and positive same-side gaps leave a genuine smooth adjacent wall interval of length at least1 on one side. The sourcefar and targetfar displacements arem_s and-m_t, each nonzero with magnitude<1/2. Under(2) they have opposite signs. Choose the complete candidate whose turn lies on that protected smooth side. Its turn is strict and cannot be a mouth or global corner. All other legs and contacts are protected as in section3, so it is an actual ordinary trajectory.

This proves the ordinaryH=h case at physicalmeanmu. For H=mu orG-mu use exactly the actual lower/upper end charts of acceptedA38: target centers-t or2G-t, with the two endpoints ordered before the construction. Reordering may exchangew_s,w_t; their phase PRODUCT is unchanged. The physical nominal mean becomesh orG-h. End folding may reverse both turn signs, but they remain opposite, so one still lies on the actual protected side. All three integer nominal levels lie strictly inside the physical spine, at distance>=2 from the ends.

Fold the complete chosen trace by the actual floor/roof fold. Its two selected arms map into their original actual teeth and original midpoint seams. Every open core end-line crossing has0<x<c and is a genuine smooth floor/roof reflection. A horizontal contact in a flush selected tooth on an end line is already an ordinary horizontal reflection and is not counted twice. The opposite turn and strict selected portals avoid end-line coincidences; the selected far corner was excluded independently. The terminal point is ORIGINALT. Earlier actual target arrival can be truncated; the prescribed controls also check first arrival directly.

Therefore (2) at ANY displayedH supplies a finite actual connecting path. No equality case with product0 is claimed; such cases need another mechanism.

## 5. Two explicit unbounded positive consequences

### A wide-core cutoff, without a wall bound

If

    c>(2h-1)*max(w_s,w_t),                          (5)

then0<(w_i/c)*(h-1/2)+1/2<1 for both selected widths. Thusn_h(w_i)=0 andm_h(w_i)=w_i*h/(c+w_i)>0. Criterion(2) applies. This proves illumination for EVERY other tooth width and arrangement in the stated integer-band geometry. It gives an actual first witness on this unbounded transverse tail; it is not propagation from a supplied witness. Joint growth withh orselected widths outside(5) is not thereby settled.

### Exact finite phase residues for integer horizontal data

If c,w_s,w_t are positive integers, let

    P=c/gcd(c,w_s,w_t).

Thenw_i*P/c is integral. Formula(1) givesn_(H+P)(w_i)=n_H(w_i)+w_i*P/c and m_(H+P)(w_i)=m_H(w_i). Hence the sufficient phase condition has an EXACT finite residue description for arbitrary unbounded integerH. A table onH2..P+1 covers every residue without using nonphysical small half-separations. This is a finite arithmetic criterion, not a finite inventory of actual rooms, a direction bound or darkness test.

In particular, if BOTH selected widths are strictly less thanc, thenm_1(w_i)=w_i/(c+w_i)>0. Periodicity implies(2) for every actual integerH>=2 withH congruent1 moduloP. Thus any one ofh,mu,G-mu in that residue class proves actual illumination for arbitrary independent OTHER widths and unlimited vertical size. Width equality is unnecessary. Remaining residues with product<=0 are not declared dark or impossible.

## 6. Reproducible evidence and precise remaining gap

unequal-seam-phase-check.py independently compares the closed formula with the actual first-stationary iteration on14400 prescribed integer/rational phase controls, including widths larger than the core and exact rounding equalities. It checks the exact period as well. These finite controls support, but do not replace, the all-real proof in section2.

It then constructs108 complete ACTUAL original-wall paths across all three end charts, both opening-start/opening-end orientations, positive and negative phase products, all four index-parity combinations, unequal selected widths and a rational-horizontal fixture satisfying(5). Opposite widths vary independently. All540 reflections and11384 exact finite-wall/leg guards pass, including original seam arrival and first target. No author optical code or ray discovery was executed; all candidates are prescribed by the proven formulas. The finite controls do not prove unchecked metric parameters.

The new positive criterion attacks unequal selected widths left outsideA56. It does not establish those phases must have positive product in arbitrary W21 rooms, settle the product-zero/opposite-sign residues, or cover nonseam/deeper/more general polygons. It supplies no universal witness-existence/finite-prefix/joint-growth theorem. The main goal and accounting remain unfinished. Independent peer acceptance of this packet is required.
