# The Ferrers union is proper; cap reversal enlarges it

## Independent obstruction to the union

Take the symmetric Ferrers rank grid (0,10,11,13,N) on both axes for any integer N≥110. These are normalized lattice rooms: a unit step remains on each axis. They all have w=h=10, u=11, v=13, e=1, d=2. The chord condition fails because 2·2>1·1. The first d170 inequality fails because 10·11>11·2. Transposition gives the very same room. For the d168 integer-period test the denominator divides N, whereas floor(N/10)²≥N: if k=floor(N/10)≥11 then k²≥10k+9≥N. Thus none of the five named tests passes for any N in this family. The real-span test has no lattice instances. This argument counts no rooms or shots. It disproves the union implication; actual illumination of the family is a separate question. [D171's independent analysis](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d171-review-ferrers-res/review.md)

## A resonance-independent sufficient condition in the complement

Let c be the height of the narrow terminal band. Its distal cap must be a full physical wall. For a source a units from the first seam, 0<a<c, unfold across that cap, so the effective travel to the seam is a′=2c−a>c. A simultaneous contact with the cap corner does not invalidate this *existence* construction. In the formal rectangular folding both components reverse at that corner. The descending segment retraces the ascending segment until it reaches the source again at its original height. Discard that entire initial loop and launch from the source along the remaining suffix. This never invokes corner continuation in the legal path. The portion between the corner and the source is in the terminal rectangle. If the cap is hit away from its ends, retain the ordinary cap reflection. The case of a source right on the far cap is outside the interior-mark hypothesis.

Put L=d+e+h. A sufficient whole-room condition, in either orientation, is

    u(e+h)/L + w(e+h)/(c+L) ≤ u,
    vh/(e+h) + uh/L + wh/(c+L) ≤ v.                         (C*)

To prove it use d170's nearest integer j and then i with the true final travel b<h and L_b=d+e+b. Take the source image for the cap-extended initial travel a′. The two signed gate bounds are u(e+b)/L_b+w(e+b)/(a′+L_b) and vb/(e+b)+ub/L_b+wb/(a′+L_b). Both right sides increase in b (with the other lengths fixed), and a′>c gives strict slack. Thus (C*) suffices at every placement; the first seam clears since L_b/(a′+L_b)<1. D169 covers the other placement types. There is no arithmetic hypothesis or period in (C*). The transpose follows by reflecting across y=x, as in [the explicit substitution](ferrers-two-windings.md).

For example, take the full U1 family (2,3,5,W; c,1,1,3) identified in d171. In the transposed construction the narrow and two middle widths are 3,4,5; the two travels are 2 and 1, and the broad height is 2. The new cap depth is W−5. The left sides of (C*) at maximal final depth become 12/5+9/W and 10/3+8/5+6/W. Thus W≥90 suffices for both, for **every c≥7** in this part of d171's residual. This is a region of length assignments, not an isolated realization.

(C*) does not settle the word. On the symmetric family above, its second left side exceeds 13 even if the term involving c is dropped: 130/11+110/13>13. The sharper fixed-room interval proof uses correlated errors. It does not justify bounding each error independently on the entire residual cone.

## Pyramid and three-corner follow-on

All seven pyramid residual types have the three-run geometry in d172 and a closed cap at the narrow end. In canonical masks 761,763,6131,5111 this is the top cap; in 8051 it is the bottom cap. Let c be the length of that terminal run, h_T the full depth available in the broad target row, and put b₀=min(h_T,dV/u). Then the following criterion lights the whole pyramid realization:

    w b₀(d+b₀)/(c+d+b₀) ≤ ud.                                (P*)

Indeed d172's two roundings give error at the second joint at most min(ub,dV)/(d+b)+wb/(a′+d+b). The first joint clears strictly and the source-cap argument still applies. After multiplication by d+b, the excess of the error bound over the window is at most

    min(ub,dV)+wb(d+b)/(c+d+b)−u(d+b).

This function increases up to b=dV/u and decreases afterwards. On the decreasing branch the derivative of the fraction term is w[1−c(c+d)/(c+d+b)²]<w<u. Therefore its maximum over 0≤b≤h_T is attained at b₀. Substitution gives (P*), with strict clearance in the actual path because a′>c. The conclusion uses the seven type attributions in [d172](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d172-review-pyramid/review.md).

Here the cap reversal fills some but not all of the complement of wb≤ud. For a whole open example region, take mask 761 with w=2,u=3,V>9, d=1, h_T=4. Then b₀=min(4,V/3)>3. At c=1 the cap test fails since 2b₀(1+b₀)/(2+b₀)>3. For sufficiently large c it passes for the entire row. Strict failures persist under small length perturbations. A direct transposed application of the same lemma is unavailable for this mask: in the sweep from the right tip toward the left column the outermost left run extends *both below and above* the middle interval, so they share neither endpoint. This is a failure of that particular second sweep, not evidence of a dark pair.

For the three-corner list (P*) applies to its nested three-run placements whenever the source run ends at a physical cap. For example in mask 8052 it applies to the bottom tip against the upper broad run, including the target at its upper seam if interior. It does not give the placement strictly in the additional top tip. The three fully certified order types 187, 1278 and 16358 remain the source of the PARTIAL designation; there is no argument here for all 21 remaining placement types at every length.

## Ledger words moved and smallest word still OPEN

These inequalities move no word to COVERED. Ferrers LLLLLRLRLR remains PARTIAL. D172 supports PARTIAL for the pyramid LLLLRLLRLR, and confirms that LLLRLLRLLR merits PARTIAL through d169. A smallest still-OPEN word is LLLRLLLRLR, W=10, with vertices (2,0), (4,0), (4,1), (3,1), (3,4), (0,4), (0,3), (1,3), (1,2), (2,2).
