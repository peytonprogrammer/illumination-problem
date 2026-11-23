# Two independently rounded windings in the ten-wall Ferrers staircase

**All-pairs theorem for review.** Use horizontal runs of widths w<u<v<W from top to bottom, all starting at x=0. The heights of the two middle runs are d,e; the bottom height is h. Every distinct pair of real interior marks is lit if

    w(e+h) ≤ ud,        (u+w)h(e+h) ≤ ve(d+e+h).                 (1)

Either this test or its transpose suffices. The top height and W do not appear in the inequalities. Integer lengths may have arbitrary common winding resonances. In particular this covers the whole lattice room on grid (0,2,10,23,230) in both coordinates. The previous common-period construction failed there even for the marked pair (1,115)–(115,1).

## Proof

By the d15 r=3 partial certificate (mask 4991), only open top-cell to open bottom-right-cell placements are outstanding. Descend from source abscissa x at distance a>0 above the first joint to target abscissa z at depth 0<b<h below the last joint. Write L=d+e+b, D=a+L. For integers i,j introduce a real slope M=(z+2ui+2vj)/L. Starting from zero at the first joint, its signed positions after subtracting the chosen periods at the second and third joints would be

    R₁=dM−2ui,          R₂=(d+e)M−2ui−2vj.

At the target the signed position is exactly z. This uses the folding criterion at both joints with the **same slope**. The two integers belong to different bands; there is no requirement that one slope restore both phases.

Choose j nearest to ez/(2vb). For this j the real value i₀=d(z+2vj)/(2u(e+b)) makes R₁ zero. Substitution gives R₂=(ez−2vbj)/(e+b), hence |R₂|≤vb/(e+b). Choose i nearest to i₀. The changes in R₁ and R₂ per unit change in i are −2u(e+b)/L and −2ub/L. Thus

    |R₁|≤u(e+b)/L,      |R₂|≤vb/(e+b)+ub/L.

It remains to launch at the actual source, since the starting phase at the first joint was arbitrary. Take the representative X of x+Ma modulo 2w in [−w,w]. In the developed frame, start at X−Ma and use slope M−X/D. In addition to the preceding positions this introduces the affine correction X(1−t/D), where t is total descent from the source. It vanishes at the target. At the first joint the signed position is XL/D, strictly inside (−w,w). At the second and third joints the correction has magnitudes bounded respectively by w(e+b)/D and wb/D. It follows that the gates clear strictly if

    w(e+b)≤ud,          (u+w)b(e+b)≤ve(d+e+b).

Indeed the resulting absolute bounds are strictly below (u+w)(e+b)/L and vb/(e+b)+(u+w)b/L, respectively, by D>L. The latter expressions are ≤u and ≤v under the displayed conditions. The two tests follow from (1): e+b increases, and b(e+b)/(d+e+b) is increasing for positive b. In particular equality in the room test is allowed.

At each joint both neighboring runs fold the signed position by absolute value in a neighborhood of the crossing. A zero here is a smooth contact on the common left side. The initial unfolded position is an image of x; the last position is the specified physical z. Transverse reflections within open bands meet genuine vertical sides. No horizontal mirror, cap, commensurability assumption, or lower bound on the distance of a mark to a seam enters this construction. D15 already deals with the other placement types, including marks on internal grid lines. [D15 reduction checked by d168](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d168-review-ferrers/review.md)

## Exact control and remaining lengths

On the previous obstruction w=2,u=10,v=23,d=13,e=8,h=2. The two comparisons in (1) are 20≤130 and 240≤4232. For S=(1,115), T=(115,1) the rounding gives j=20, i=75, M=2535/22 and X=21/11. The downward slope dx per unit descent is 2189/19. The d164 exact tracer returns (115,1) after 5,490 side reflections. The count pertains to this prescribed shot; all-pairs coverage follows from (1). [Earlier obstruction](ferrers-lattice-return.md)

**Explicit residual.** Take the symmetric coordinate grid (0,10,11,13,100) on each axis and the Ferrers rows of widths 10,11,13,100 from top to bottom. The staircase has ten walls and axis gcd one. The reflex (11,11) is strictly below the chord from (10,13) to (13,10). Here d=2,e=1,h=10. The first inequality already fails, 110>22, in both orientations. The least common middle slope period is 286, giving Ph/W=143/5, and the last increment 87 exceeds w. Thus neither the earlier large-denominator nor half-period room theorem settles it. For example S=(5,55), T=(55,5) lie in the outstanding placement type. This demonstrates failure of the *room-wide sufficient inequalities*. It does not establish failure of all choices of i,j for that pair, or darkness.

The remaining geometry includes rooms where the top run is wide compared with the first middle height in both orientations. Nearest-integer rounding treats the unknown source correction and the two rounding errors as if they could all point toward the same lip. The open issue is whether the choice of the source sign, the adjacent integer at either rounding, or a longitudinal reversal can always keep the true signed positions within the two gates in this regime.

## Ledger words moved and smallest word still OPEN

None. LLLLLRLRLR remains PARTIAL, with an additional all-marks lattice region for review. A smallest OPEN word is LLLRLLLRLR (W=10), realized by (2,0), (4,0), (4,1), (3,1), (3,4), (0,4), (0,3), (1,3), (1,2), (2,2).
