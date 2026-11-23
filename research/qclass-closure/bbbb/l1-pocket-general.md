Advances: L1 — A pocket excludes darkness for a specified pair only when its entry and return states match legal exterior legs. The two strictly inset necks account for eight reflex corners.

Scope: normalized orthogonal lattice rooms and interior lattice marks. Wall-turn words are cyclic, taken up to reflection. A prescribed layout and a wall-turn word are distinguished throughout.

### The ledger word and its two relatives

Trace a rectangle counterclockwise. Inserting a strictly inset rectangular neck leading outward from one side to an end chamber adds RRLLLLRR along that side: two reflex turns to reach the end chamber's first shoulder, four convex turns around its body, then two reflex turns on the return. The original four convex turns of the middle chamber remain. Write F=RRLLLLRR. For two such attachments the cyclic word is F L^j F L^(4−j), where j counts middle-chamber corners on one boundary arc between the attachments. Exchanging the attachments identifies j with 4−j. The exact d163 dictionary keys, using least rotation or reversal, are:

| Mouths on middle chamber | j | Ledger word |
|---|---:|---|
| Opposite sides (the d152 chain) | 2 | LLLLRRLLRRLLLLRRLLRR |
| Adjacent sides (a right-angle chain) | 1 | LLLLRRLLLRRLLLLRRLRR |
| Same side (two distinct mouths) | 0 | LLLLRRLLLLRRLLLLRRRR |

These are all three positions for two distinct, disjoint, strictly inset straight rectangular necks attached to a rectangular middle chamber with rectangular ends. If “same shape” requires opposite parallel sides, there is only the first word. A turn word records no alignment of nonconsecutive wall segments; even a theorem for every such rectangular assembly would require a realization argument before covering the entire word. STATUS.md gives aggregate ledger changes; the three derived keys occur in its companion ledger.json. No ledger status is changed.

### Arbitrary rectangles and displaced apertures: a sufficient matching test

Use middle chamber coordinates 0<x<w. Let the left neck open into the chamber at heights (l₁,r₁), and the right at (l₂,r₂), with δ=l₂−r₁>0 (reflect vertically for the opposite ordering). The strip r₁<y<l₂ has two solid vertical flanks. Instead of a round trip to a roof, traverse this strip from bottom to top. For a ray with c=|dx/dy|, entry at x=a directed up and right, its exit phase is a+δc modulo 2w. An exit at b in (0,w) on the rightward sheet has the original horizontal sign. There are no roof contacts; strict entry and exit exclude both endpoint levels' corners, and every intervening side contact is on a solid flank. This is the one-pass version of the pocket map.

Take S=(U,r₁−g₁) in the left outer chamber and T=(V,l₂+g₂) in the right outer chamber, with U<0, V>w, g₁,g₂>0. Require the initial and final straight legs to clear their corridors. A sufficient placement is 0<g₁≤r₁−l₁ and 0<g₂≤r₂−l₂, with interior marks in the respective end chambers: each leg stays strictly within its aperture's height range on the corridor crossing. The proof likewise applies to any legal unfolded exterior legs with the same data after checking their crossings. It uses no upper bound on any chamber dimension.

Entry and exit are a=U+g₁c and b=V−g₂c. Hence the exact test for the specified rightward itinerary, given clear exterior legs, is

    max(0,−U/g₁,(V−w)/g₂) < c < min((w−U)/g₁,V/g₂),
    (g₁+δ+g₂)c ≡ V−U (mod 2w).

The inequalities put both contacts inside the middle chamber. The congruence matches b on the rightward sheet. Unfolding the middle flanks glues all three legs with the same slope. Conversely those conditions follow from any such transit. An open interval longer than 2w/(g₁+δ+g₂) guarantees a solution. For overlapping apertures, the earlier roof-pocket lemma continues to apply when both exterior legs clear their mouths and meet its interval and congruence. Neither test by itself covers marks at every height.

**An unbounded displaced subfamily.** For g₁=g₂=1 write A=−U and K=V−w. The interval has length w−|A−K| when positive. Thus |A−K|<wδ/(δ+2) suffices, uniformly in the two corridor lengths and chamber dimensions. In particular, equal horizontal distances A=K work for every integral δ≥1. This is a statement about the specified pairs, including pairs separated by disjoint apertures.

### What darkness excludes and what eight corners buy

For a fixed pair, consider every allowed incoming state at a pocket from S and every outgoing state that can continue to T. At a common speed ratio c and with a common velocity convention, discard entries that hit a corner or return through a closed part of the mouth. Darkness forces the image of the remaining incoming set under θ ↦ θ+2hc modulo 2w to be disjoint from the outgoing set. Otherwise the three legal pieces concatenate. The displaced strip has the analogous exclusion under θ ↦ θ+δc. A room-wide absence of pockets does not follow. D154's exclusion of integral full-mouth pockets of width ≥3 and depth ≥1 in R22 uses its separate corner-only odd–odd fiber.

**The target word does not guarantee even that R22 comparison pocket.** For every integer H≥5 take three chambers of width 1 and height H, with two length-one necks at heights (1,H−1). Each neck is strictly inset at both ends, producing the opposite-side word and all eight reflex shoulders. Points at integral mouth abscissas and heights 2 through H−2 are interior lattice marks. All horizontal edges and vertical shoulder edges have length one. The only walls long enough to be the solid roof of a width-three pocket, in either orientation, are the two outer vertical walls. For solid perpendicular flanks on both ends of such a roof, it must use that whole outer wall. The flanks extend just one unit to the end chamber's neck, where the putative base has only a partial opening (1,H−1). Therefore no integral full-mouth pocket of width ≥3 and depth ≥1 exists anywhere in this family. Narrower pockets and other light paths remain possible.

**First failed covering step.** The wall count fixes the number of shoulders but neither distances nor aperture heights. Even for g₁=g₂=1, choosing |A−K|≥w makes the displaced-strip entry interval empty. For disjoint unit apertures there is also a direct obstruction to applying the old roof test above both mouths. An unreflected incoming leg through a left neck of length L has |dy/dx|<1/L; reaching the upper pocket at or above the top of the right unit mouth across middle width w requires a climb greater than δ+1. If (δ+1)L≥w the same straight leg cannot do both. The reflected lower-pocket obstruction applies from the right when its neck is comparably long. These failures concern the prescribed exterior legs. They do not exclude exterior wall bounces, a different middle itinerary, or illumination.

**Verdict.** L1 gains a symbolic sufficient condition for separated apertures. The opposite-side word remains uncertified as a whole. A first residual is the pair across disjoint unit mouths with a nonpositive interval for the direct strip transit and insufficient straight-leg clearance to the upper and lower pockets. Controlling at least one other legal exterior approach for these marks is open, already within rectangular assemblies and before passing to more general realizations of the word.
