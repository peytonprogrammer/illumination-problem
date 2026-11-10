# R41: unbounded unequal-depth phase repair in width-one cores

Author theorem pending independent review. Conservative original deadline06:48:00Z includes preliminary phase algebra. The universal canonical45W21 goal remains OPEN.

## Quantified theorem

Let P be a finite strictly simple integer two-sided rectangular-spine comb with core width1. All teeth have height2; their horizontal widths are arbitrary independent positive INTEGERS. Same-side bands have positive gaps, opposite-side overlaps are allowed. Consider two actual interior A marks in distinct teeth on the same side. Let their unequal integer depths from that side's core seam be D_s,D_t>=0. They have the same parity because their ORIGINAL abscissae are even. If their unordered depths are NOT one of

    {0,2}, {1,3}, {2,4},

then they illuminate whenever W<=23, without any bound on depths, widths, room height, support, exceptions or diameter. Equal-depth pairs are deliberately outside this statement. The three exceptional pairs are NOT declared dark.

All such marks lie on their selected tooth midrows, since those are the only interior integer ordinates in a height2 band. Write their ordered floor-relative heights s<t, h=(t-s)/2>=2, mu=(s+t)/2. Their original even ordinates give integral h,mu despite an odd relative floor. The actual far end of each selected tooth extends strictly beyond its own mark.

## 1. Strict finite phase data

Put p=min(D_s,D_t), q=max(D_s,D_t), e=(q-p)/2>=1, M=(p+q)/2+1=p+e+1, A=2M=p+q+2. For integer R define

    n_p(R)=floor(pR/A+1/2), n_q(R)=floor(qR/A+1/2),
    f(R)=R-n_p(R)-n_q(R),
    d(R)=(p-q)R/A-[n_p(R)-n_q(R)].

Call R strict if neither pR/A nor qR/A is a half-integer. At a strict R both residuals 1+2pR/A-2n_p,1+2qR/A-2n_q lie strictly in(0,2), so |d(R)|<1. No corner equality is accepted.

The following explicit choices provide strict R with f=0 and nonzero d, and strict R with f=1 and nonzero d, for EVERY allowed unbounded p,q.

| Parity needed | Parameter case | R | n_p,n_q | f | d |
|---|---|---|---|---|---|
| even | e>=2 | 1 | 0,1 | 0 | 1-e/M |
| even | e1,M>=5 | 2 | 1,1 | 0 | -2/M |
| odd | p odd | M-1 | (p-1)/2,(q-1)/2 | 1 | e/M |
| odd | p even,e>=2 | M-1 | p/2,q/2-1 | 1 | e/M-1 |
| odd | p even,e1,M>=6 | M-2 | p/2-1,q/2-1 | 1 | 2/M |

Here e<M, so every listed d is nonzero with absolute value<1. All R satisfy0<R<A. For the first row p<M<q<2M, so p/A<1/2<q/A<1 strictly. For the second q=M and p=M-2; at R2, pR/A=1-2/M is strictly between1/2 and1 and qR/A=1. For p odd at R=M-1, the values are p/2-p/(2M) and q/2-q/(2M); p<M and M<=q<2M put them in the indicated nearest-integer intervals, strictly away from half-integers, including q=M. For p even,e>=2, p/(2M)<1/2<q/(2M)<1 gives the fourth row, with p0 harmless. For the last row p/M=1-2/M in(1/2,1), q/M=1, giving its strict indices. These inequalities prove the table for unbounded depths; a finite scan is not its proof.

The cases omitted by this table are precisely e1,M2/3/4, namely(p,q)=(0,2),(1,3),(2,4). There are no other missing parameter values. Direct arithmetic on their4/6/8 residues shows that(0,2),(2,4) have no strict nonzero d of either f parity, and(1,3) has strict nonzero d only at odd f. This explains failure of THIS repair, not actual darkness or completeness of all billiard words.

## 2. Two opposite bend shifts at EVERY integer half-separation H>=2

For strict R, reflection R'=A-R is also strict. Nearest-integer complementarity gives

    n_p(R')=p-n_p(R), n_q(R')=q-n_q(R),
    f(R')=2-f(R), d(R')=-d(R).

Fix any integer H>=2 and choose the table row of its parity. Its f is0 for even H or1 for odd H. The reflected f' is2 or1 respectively. Both f,f' have the same parity as H and are<=H. For EACH residue put

    k=(H-f)/2 >=0, N=R+A*k, tau=2N/A >0.

The actual indices at tau are n_p(R)+pk and n_q(R)+qk. Their sum satisfies

    N - n_p(N) - n_q(N) = f(R)+2k = H.

Equivalently

    (p+q+2)*tau = 2H+2n_p(N)+2n_q(N).

This is exactly the two-middle-row matching equation for a width-one core and selected center separation2H. Strictness of both portals is unchanged by the integer phase shift. The lower selected tooth prefix, the opposite wall turn and the reflected reverse upper prefix are the actual A32 construction for that STRICT matching, with its legitimate initial vertical signs. It does not require that this fixed point be the first stationary value; the strict fixed equation and explicit prefix guards are sufficient. All counts are finite, however large the depths.

The resulting turn is at the mean of the selected centers shifted by d(R), and the reflected residue yields the opposite shift. If the actual lower depth is q rather than p, the shift signs swap, leaving BOTH signs available. The unused far widths never enter a prefix, which stays strictly between each actual mark and its own mouth. No virtual far-wall image is involved.

Thus every allowed unequal-depth pair has TWO fully matched opposite-turn candidates at mean +/-epsilon for every H>=2, with0<epsilon<1. This is actual witness construction, not one-witness propagation or a conjectured finite state bound.

## 3. Actual end charts and the stronger darkness consequence

Apply the preceding construction to original source s and target images t,-t,2G-t. Their positive half-separations are h,mu,G-mu, all integers>=2. The two endpoint data are reordered if the target copy is lower, then the constructed path is reversed. In every chart BOTH opposite shift signs remain available. Fold the COMPLETE finite paths by the true end map F(y)=y on[0,G], F(-y)=F(y), F(y+2G)=F(y).

The physical nominal means are respectively mu,h,G-h. All lie in[2,G-2]. Their shifts have absolute value<1, so each mean lies in one open isometry cell of F with its entire shifted interval; the two physical turn candidates are precisely ell+/-epsilon. They cannot meet a global end. Strict selected portals and actual tooth contacts fold into the original selected rectangles. Every open core crossing of an end line has0<x<1 and becomes a true smooth floor/roof reflection. No copied mouth or selected-lift replacement is accepted. Any earlier actual T can be used as the valid first arrival.

At an INTEGER nominal level ell outside all closed opposite tooth bands, both shifted turns stay on a smooth wall: integer endpoints are at least distance1 away. At a mouth ENDPOINT ell, one shifted turn is on the adjacent smooth actual wall interval of length at least1, because integer same-side bands have positive gaps. Only when ell is STRICTLY INSIDE a band can both candidates fail. A height2 integer band has exactly one interior integer level, its MIDPOINT.

Therefore ACTUAL DARKNESS forces ALL THREE nominal levels

    h, mu, G-h

to be midpoints of opposite teeth. This is stronger than a corner obstruction; the nonzero symmetric phase shifts repair every nominal corner.

## 4. Entire-room wall contradiction

The three levels are distinct, with successive gaps mu-h=s and G-h-mu=G-t. If q0=min(s,G-t)<=2, two required opposite tooth midpoints have distance<=2. Their height2 bands overlap or touch, contradicting the stipulated positive same-side gap. (The symbol q0 here is an end distance, distinct from larger depth q.)

If q0>=3, both selected teeth are NONFLUSH. The three opposite blockers are different and nonflush, since their centers lie in[2,G-2], whereas flush height2 tooth midpoints are1,G-1. Thus five distinct nonflush teeth force the ENTIRE-room maximal-wall count W>=4+4*5=24. Unused attachments cannot decrease it, and opposite band overlaps cannot merge boundary walls through the open core. This contradicts W<=23.

All actual placements and all integer H/depth parameters in the theorem are therefore covered. The proof leaves equal depths and the three named small unordered depth pairs unresolved by this method; it supplies no universal polygon theorem, no darkness claim from finite failure, and No formal verification claim.
