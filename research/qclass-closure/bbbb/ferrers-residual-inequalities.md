# All three named d170 residual rooms are lit

**For review.** O1 and O2 follow from the earlier d17 chord lemma. The symmetric staircase RES with grid (0,10,11,13,100) has a new all-real-marks certificate below. These are whole-room results. The all-length Ferrers word remains open.

For general Ferrers parameters the three reflex vertices from upper left are (w,h+e+d), (u,h+e), (v,h). Comparing the middle vertex with the chord of the other two by cross multiplication gives d(v−u)≤e(u−w) for the middle vertex to be on or above the chord. By d17 this suffices for the remaining terminal pair type, and d169 covers all other types. O1 and O2 both have d=e=1 and v−u=u−w=1. Thus both lie on the chord boundary for every placement. RES has d(v−u)=4>1=e(u−w). The statement that all four tests in d170 fail for these three rooms was correct. [D17 chord proof](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d17-r3/r3.md) · [Reviewed type reduction](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d169-review-d15r3/review.md)

## Recenter the line at its first doorway

In RES let S=(x,13+a), T=(z,10−b), where 0<x<10, 0<a<87, 13<z<100 and 0<b<10. Descend directly (B=b) or unfold at the full floor (B=20−b). The middle widths and travels are (11,2) and (13,1). Set L=3+B. Choose a transverse slope offset M and two windings i,j with

    2M=22i,     3M−22i−26j=t,     t an integer.

The solutions are i=19t+26k, M=209t+286k, j=(11i−t)/26, since 11·19≡1 modulo 26. The terminal offset is t+MB. Write Z=z−t−MB, allowing the usual target period 200 in Z. Use physical slope M+(Z−E)/L per unit of unfolded descent, where E is the signed first crossing. The source constraint is

    (1+a/L)E ≡ ±x + aM + aZ/L      modulo 20.

For each sign choose the representative after scaling nearest zero. If a≥a₀≥0 this gives |E|≤η=10L/(L+a₀), with |E|<10 for interior marks. At the next two gates the signed coordinates, after removing the indicated periods, are exactly

    (1+B)E/L + 2Z/L,           t + BE/L + 3Z/L.

At the target the signed position is z modulo 200. Thus sufficient strict inequalities are

    |Z| < A = [11L−η(1+B)]/2,     |Lt+3Z| < H = 13L−ηB.

They guarantee the signed gates are in (−11,11) and (−13,13), respectively. Each neighboring physical interval folds by absolute value at the seam. The source sign remains free. On the floor route the two E choices differ by a nonzero quantity of magnitude at most 20; their floor coordinates differ by (B−10)ΔE/L, strictly between zero and 100 in absolute value. At least one misses every floor corner. Thus each open interval certified here covers *all* source abscissas at the allowed heights.

## Exact rational interval certificate

For rational B write q=den(286B/200). Modulo 200 the k-translates give precisely the grid of spacing 200/q. For fixed t the target interval has center (209B+1)t plus the intersection

    (−A,A) ∩ ((−H−Lt)/3,(H−Lt)/3).

Only |t|≤floor((H+3A)/L) can contribute. These bounds integrate the full sufficient inequalities over the windings. The checker projects intervals on the abscissa axis and merges *strictly overlapping* intervals only. It does not sample launch directions, rays, placements, or wall words.

1. By the reviewed direct/floor rotation lemma every b is covered unless both 286b/200 and 286(20−b)/200 have reduced denominators ≤10. There are exactly 142 such b: enumerate fractions 0<r<143/10 of denominator ≤10 with den(143/5−r)≤10 and set b=200r/286.
2. Take a₀=0. The direct and floor intervals together cover the entire open range (13,100) at 141 of those depths. The sole remaining depth is b=100/11. There the three covering intervals meeting the target range are (−395/22,395/22), (485/22,1275/22), and (1365/22,3035/22). In particular any unlit target must have z≥395/22.
3. The room is invariant under reflection across y=x. Reverse the endpoints after reflection. A dark original pair is a dark reflected pair, so step 2 also forces the original source ordinate to be at least 395/22. Hence a≥109/22. Recompute just the last depth with this lower bound: the union contains the single open interval (−71341/550,126891/550), strictly containing (13,100). This contradicts darkness.

[Exact checker](residual-windows.py) · [Reviewed rotation and source-image argument](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d168-review-ferrers/review.md)

## Scope of the residual calculation

The same two-gate calculation can be written for other integral dimensions. Choosing M=2ui/d and putting t=eM−2vj gives terminal offset t+MB and gate deviations (e+B)E/L+dZ/L and t+BE/L+(d+e)Z/L, with L=d+e+B. The terminal phases form rational progressions at each exceptional b. This is a fixed-room sufficient test, including in asymmetric rooms where the transposed calculation uses different parameters. A universal proof would need to show the two projected residuals always exclude each other or that a different passage clears their intersection. The interval identities for RES use its actual integer lengths and do not establish that universal claim.

## Ledger words moved and smallest word still OPEN

No word moves to COVERED. LLLLLRLRLR remains confirmed PARTIAL. A smallest OPEN word is LLLRLLLRLR, W=10, with vertices (2,0), (4,0), (4,1), (3,1), (3,4), (0,4), (0,3), (1,3), (1,2), (2,2).
