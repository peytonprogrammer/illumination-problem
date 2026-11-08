# R53: a lit20-wall room outside the full-box core-template mechanism

Author claim pending independent review. Universal W21 remains OPEN. Original conservative effort07:43Z/deadline07:57Z includes the first residue derivation. This is a calibration of R52's geometric hypothesis, not a darkness result.

Take core[0,c]x[0,9], right selected mouths[1,3],[5,7], left mouths[2,4],[5,7], arbitrary positive tooth widths. Consider a fixed finite rectangular-core word from source portal(c,2+delta_s) moving up-left to target portal(c,6-delta_t) moving up-right. Claim: NO such core word works for the ENTIRE independent box(delta_s,delta_t) in(-1,1)^2. There is no bound on its number of reflections or side traverses.

Any such word, entering no tooth, alternates left and right vertical sides. It makes2m horizontal core traverses for some integer m>=1. Unfolding horizontal walls gives an upward straight segment from2+delta_s to6-delta_t+18k with integerk>=0; the positive terminal derivative requires this target orientation. Let beta=(4+18k)/(2m), the nominal rise per traverse. At side event j, the developed height is

    2+j*beta+(1-j/(2m))*delta_s-(j/(2m))*delta_t.

For each internal j, the last two terms range over the ENTIRE open interval(-1,1). A necessary condition is therefore that the whole open interval of length2 centered at2+j*beta fold into a single smooth finite side mirror, never through an end corner or a tooth mouth.

The physical left smooth components are(0,2),(4,5),(7,9). Only components of length at least2 can contain this full interval. Its physical nominal center must consequently be EXACTLY1 or8. A developed nominal left center has residue1,8,10 or17 modulo18. The right smooth components are(0,1),(3,5),(7,9), so a robust developed right center has residue4,8,10 or14 modulo18. A developed interval cannot cross a multiple of9: that would give a forbidden floor/side or roof/side corner at an interior portal choice. This rules out interpreting a folded interval across an end corner as an additional smooth component.

For m1, endpoint closure forces beta2mod9, so the first left nominal height is4 or13mod18, folding to4 or5. Both are mouth corners. This fails even at the nominal portal pair.

For m>=2, the first left event implies

    beta in{17,6,8,15} modulo18.

The second side event is an INTERNAL right mirror. At beta17 or8 its nominal developed height2+2beta is0mod18, an end corner, so these two residues are impossible. At beta6 or15 it is14mod18, a possible right mirror. But the third side event is then an INTERNAL left mirror, with nominal height respectively2 or11mod18. These fold to2 or7, both left mouth corners. Thus these remaining residues are impossible as well.

All m>=1 are excluded by this finite residue argument. This is not a failed finite word search and not an exclusion of core words valid on smaller portal sets, variable words, signed target charts, or actual tooth excursions. In particular a down-right terminal core chart is OUTSIDE the claim. R52's required up-left/up-right full-box hypothesis cannot be assumed for every strip generator.

Nonvacuity is exact: for c1 and both selected widths1 this room DOES illuminate its actual seams. The independently accepted R47 D0 eight-reflection path, translated vertically by4, is

    (1,2), (0,14/3), (1,22/3), (3/8,9), (0,8),
    (9/8,5), (15/8,7), (2,20/3), (11/8,5), (1,6).

It enters the actual upper selected tooth and uses its genuine far wallx2. The left widths do not enter the path; it never hasx<0. Its eight actual reflections are smooth and corner-free. It is therefore entirely compatible with illumination and with the failure of the narrower robust-core hypothesis.

Own robust-core-calibration-check.py verifies the exact residue table and independently replays this actual eight-reflection path against original20-wall contours at three independent positive rational left-width pairs. The hand argument, not those controls, excludes every unbounded traverse count.

The next positive route must permit another target orientation, adapt the core word to the actual phases, or use genuine tooth returns. No failure of the universal illumination target is inferred. Frozen accepted sources remain unchanged; peer's h>=3 low-band inventory is disjoint.
