# TR04: broaden the spiral order, then transpose the optical theorem

Pending independent review. This is a supplement with new quantified scope; frozen TR01/TR03 proofs remain unchanged. Use the hypotheses and thresholds of three-reflex-candidate-04.md.

## 1. Exact geometry under the non-overlap condition

Write the room as the union of four rectangles:

    C_L=[0,a]x[b,H], C_U=[0,A]x[h,H],
    C_R=[w,A]x[0,H], C_B=[l,A]x[0,c].

The source-column rectangle C_L and bottom rectangle C_B have disjoint closures whenever a<l or c<b. Each of C_L,C_R meets C_U in a positive-area rectangle; C_B meets C_R in a positive-area rectangle and is disjoint from C_U because c<h. The same displayed ten-wall cycle is their boundary. Its three consecutive right turns remain (a,h),(w,h),(w,c), independently of the orders of a,l and b,c.

For a direct noncontact check, the only potentially crossing inner pieces are x=a,b<=y<=h with the ledge y=c,l<=x<=w, or x=l,0<=y<=c with the ledge y=b,0<=x<=a. Such a contact requires l<=a and b<=c. The stated strict disjunction excludes it, including endpoint touches. The outer coordinates 0,A,0,H and the remaining strict orders exclude all other nonadjacent contacts. Every adjacent edge has positive length. Hence P is a strictly simple ten-wall disk of type (1,1,8).

No claim is made here about normalizing every abstract turn word to these coordinates. We prove optics for this actual class.

## 2. Re-establish the partial endpoint coverage with the correct left-column set

Keep Q=C_L union C_U union C_R and the L subroom

    R_L=([l,A]x[0,c]) union ([w,A]x[c,H]).

Replace the old G by

    G*=int(P) intersect
       ({x<a,y>b} union {y>=h} union {x>w,y>=c}).

The y>b guard is essential when l<a: a point x<a in the bottom arm below c is not a source-column point. Every G* point is strictly interior to Q. Every actual point outside G* lies in the lowest chamber B*={(x,y):l<x<A,0<y<c} and is interior to R_L. Conversely a point outside int(R_L) lies in the actual left column x<a,y>b or the upper cap y>h,x<=w, and belongs to G*. Thus the exact remaining unordered pair is again T in B* with S in the left column or upper cap/cut.

The specific U proof transfers on G* exactly with its original guards. Q's only artificial vertical wall is x=w,0<y<c. Its used right-arm contacts are strictly above the right endpoint height, which is at least c. The additional original corner (w,c) is avoided, including equality y_T=c. Source-column contacts have y>b. Their x=a and y=b walls are genuine: if l<=a, the disjunction forces c<b, placing the bottom arm strictly BELOW them; if a<l, horizontal separation suffices. The cap lies above h, so all its original mirrors and portal states are unchanged. All other placements and y=h seams use the same protected L/direct cases described and independently accepted in TR01.

For two strict-interior R_L marks, use the horizontal-only L proof. Its three horizontal walls y=0,c,H are genuine. In particular the ledge y=c,l<x<w is not covered by C_L: if l<a, then c<b; if a<=l, their interiors do not overlap in x. Its artificial vertical wall x=w above h and the corner (w,h) are avoided as before. Source endpoints on that artificial boundary are not inserted into the L theorem.

This is a new guarded reuse argument, not application of the bare W8 theorem to an enlargement. The only residual pairs are, after relabeling,

    l<t<A, 0<v<c,

with either 0<s<a,b<u<h, or h<=u<H,0<s<=w (actual interior).

## 3. The tall optical construction survives these new orders

Apply the full TR03 selection and fold construction to these residual pairs. The target window uses only 0<z=A-t<B=A-l and B>R=A-w. These remain true for every allowed l. Source and right phase counts use only 0<h-u<h and 0<h-v<h, with no comparison of b and c or of a and l. The root spacing uses only u<H,v<c. Thus the same positive component delta_v and the same explicit roof condition give one common slope strictly inside every portal window.

All physical bands are unchanged: x=0,a on b<y<h, x=0,A above h, x=w,A on c<y<h, x=l,A below c. The non-overlap condition makes every one of these stated wall portions genuine, as checked above. The strict portal and roof-corner arguments are identical algebraic assertions and preserve actual endpoints. Upper/cut sources and singular-roof actual-S return/truncation require only h<=u<H,0<s<=w and v<c<h, also unchanged.

One first-target detail requires a NEW check. For a left-lower source, the ascending part lies in x<a. If l>=a, its x coordinate is strictly less than the target's t>l. If l<a, strict simplicity forces c<b, so the ascending part instead has y>=u>b>c>v. In either case it cannot reach T early. Cap heights are at least h>v; after the roof (or legal suffix) height decreases strictly until v. Hence the final point remains the FIRST actual T. For upper sources u>=h>v, the original first-arrival argument is unchanged.

This proves the tall condition for the enlarged class, retaining all real metrics, finite contact counts and corner guards. The argument uses the independently accepted TR03 construction plus the explicitly checked new geometry and first-target facts.

## 4. Transposition is closed on the enlarged class

Swap the coordinates and reverse the boundary traversal to restore CCW order. The transposed polygon has exactly the same normal form with

    (a',l',w',A',b',c',h',H')
       =(c,b,h,H,l,a,w,A).

Every positive-order requirement holds because c,b<h<H and a,l<w<A. Its non-overlap disjunction is

    a'<l' OR c'<b'  <=>  c<b OR a<l,

exactly the original hypothesis. Thus no inadmissible metric or diagonal-wall model is substituted. Actual marks transpose to their exact coordinate swaps, preserving interiority, distinctness and even-even status in the lattice subcase.

Applying the just-proved tall theorem to that transposed ORIGINAL room gives the horizontal threshold stated in the candidate. Swapping coordinates back preserves Euclidean lengths up to isometry, finite wall intervals, specular reflection, actual target identity and all corner guards. It therefore supplies a physical path in P for every original pair under the wide condition.

## 5. Strict additional coverage and limits

For a concrete metric discriminator take a=4,l=12,w=20,A=680,b=4,c=8,h=20,H=28. The horizontal quantities are R_h=8,L_h=1,Ns_h=3,Nr_h=3,delta_h=1/7. Its horizontal threshold is A>=4+2*28*7=396 and holds. The original tall threshold fails (its required H exceeds 28). Therefore this is an entire new wide-room coverage mechanism at the original geometry, not a claim that the old tall inequality already held there. The theorem itself quantifies over all allowed metrics, not just this discriminator.

Still open: rooms failing both sufficient thresholds; other possible coordinate forms of (1,1,8); all remaining r3 types; r4..8. No dark conclusion follows from a failed inequality. There is no full-r3 completion, generic hull/corner-transfer assumption, discovery search or renewed old clock.
