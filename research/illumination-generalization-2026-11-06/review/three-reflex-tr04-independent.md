# TR04 independent optical review

Hand verdict on the read candidate and argument: **ACCEPT at their stated conditional metric scope**. Final pinned receipt is recorded separately in `three-reflex-tr04-independent.json`; this Markdown alone does not assert that a source handoff was frozen. The author checker source has been inspected but not executed as independent evidence.

## 1. Expanded geometry: ACCEPT

Under `0<a<w<A`, `0<l<w`, `0<b<h<H`, `0<c<h`, the possible nonadjacent contacts that can break the displayed cycle require BOTH `l<=a` and `b<=c`. The condition `a<l OR c<b` excludes these, including boundary touches. Equivalently the left-column and bottom rectangles have disjoint closures, while cap/left/right and right/bottom overlap in positive area. Checking their union boundary gives precisely the claimed ten segments, without a hole or an additional wall. Equality l=a is permitted only with c<b; equality b=c requires a<l. These are included in the optical argument. Every edge has positive length, adjacent edges turn, and the reflex run is the same three consecutive vertices. No claim of a full normal-form classification follows.

## 2. Partial optical coverage with corrected column membership: ACCEPT

The new set G* uses `(x<a AND y>b)`, not x<a alone. This distinction is material when bottom and left arms overlap in x. An actual bottom-chamber point below c then is not incorrectly treated as a source-column point.

For a G* pair, Q is the same U subroom as before. Its artificial inner-right wall lies at x=w below c. The specific accepted U construction uses inner-right contacts strictly above its right endpoint, whose actual height is at least c, so all those contacts remain genuine, including the added corner (w,c). Original left-column mirrors lie at or above b. If the bottom reaches x<a, it lies strictly below b by c<b, so it cannot erase these mirrors or add a corner on the used portion. If it does not reach that column, horizontal separation gives the same conclusion. The top-cap and remaining protected L/direct cases are unchanged.

For an interior R_L pair, the accepted horizontal-only L construction uses genuine y=0,c,H intervals. The only possibly covered ledge y=c cannot meet the source column: c<b when l<a, and otherwise its open x interval lies to the right of that column. Artificial vertical x=w above h and the additional corner (w,h) remain unused. Added corners on x=l below c or x=a above b lie on separate band supports or outside the used horizontal contacts; no corner is silently declared smooth.

The actual interior is the union of G* and interior R_L. Points exclusive to G* are the left-column or upper-cap/cut placements with x<=w, and points exclusive to R_L are the lowest chamber. Therefore the two methods leave exactly the stated cross pairs. Seam points y=c in the right arm and y=h in the actual left mouth are handled in the same guarded cases. Points on true notch boundaries are not interior marks.

## 3. Tall all-endpoint construction on the enlarged class: ACCEPT

The previously accepted TR03 proof only needs `B=A-l>R=A-w>0`, source b<u<h, target 0<v<c<h, and the same positive cap widths. Neither root selection nor its strict interval counts needs a<l or b<c separately. The full new disjunction proves that all four-band vertical mirrors remain actual walls. Portal signed-velocity identities, exact target coordinate, roof symmetry exclusion, and upper-cap same-S suffix hold algebraically without those old orders.

There is a genuine first-arrival qualification, explicitly repaired by the author: when l<a, x separation no longer excludes T during source ascent. In this branch c<b, so ascent y>=u>b>c>v excludes T instead. When l>=a, t>l>=a excludes it by x. The cap is above h>v; the descent reaches y=v only at its end. Thus the final actual T is the first target, not a later target shadow.

## 4. Transposition and the wide theorem: ACCEPT

Coordinate swap is a global Euclidean isometry of the entire physical room and path. Direct reversal and cyclic relabelling of its ten-vertex boundary give

`(a',l',w',A',b',c',h',H')=(c,b,h,H,l,a,w,A)`.

All positive inequalities carry over, and the new disjunction is `c<b OR a<l`. Thus the enlarged class, unlike the earlier strictly ordered subclass, is closed under this swap. Actual S,T transpose exactly, retaining distinctness/interiority and even-even lattice status. Specular velocity, every finite mirror interval and true-corner exclusion are preserved by the same isometry; this is not an arbitrary affine shear or selected-ray transfer.

Substituting these parameters into the accepted tall inequality yields exactly the candidate's delta_h and `A>=a+2H/delta_h`. The wide numerical discriminator satisfies that inequality and fails the original-orientation tall condition. Hence the new theorem covers additional original metrics rather than claiming their original height already met TR03.

## 5. Independent prescribed evidence and remaining scope

`three-reflex-tr04-independent-check.py` reuses only reviewer-owned arithmetic and U/L functions through AST extraction, changing precisely the geometry assertion being reviewed. No physical guard is removed. Its independent paths are checked against all finite walls of the new original polygons. The twelve prescribed cases have 1161 reflections and 12010 wall/leg guards, all passing, including x-overlapping arms, equality of side coordinates or ledge levels, right-y=c seams, upper-cut sources, a bottom target strictly left of its source in x, and an exact swap/reversal into the wide original room. The swapped-back original path is also separately validated.

The real quantifiers follow from the hand proof and the accepted dependencies, not the finite cases. Source pins and the exact final replay totals belong to the separate receipt. No discovery effort, clock renewal, room census or author-code-based verification is used.

No mathematical correction is required at the stated scope. The accepted conclusion is all actual interior endpoint pairs in the enlarged non-overlap class whenever EITHER sufficient threshold holds. Metrics failing both thresholds, other possible coordinate forms, the full (1,1,8) type, the other seven r3 types, and r4..8 remain open. No failed threshold establishes darkness. The native full goal remains incomplete.
