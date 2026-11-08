# A57 supplement: arbitrary independent actual depths, no arithmetic restriction

Author theorem pending independent review. The frozen actual-word-cell-proof.md is preserved. This supplement supersedes its depth restrictions, for the SAME literal room. Original discovery deadline remains 07:39Z; the argument below was completed before it. No new discovery clock is opened.

## Theorem

In the literal A57 room, for EVERY positive REAL c,a,b,w_s,w_t and EVERY REAL 0<=D_s<w_s, 0<=D_t<w_t, the actual points S=(c+D_s,2), T=(c+D_t,8) illuminate. No integrality, common depth, commensurability or width bound is needed. The path uses five core reflections plus finitely many selected horizontal reflections, entering neither opposite tooth. It stays inside the marked abscissae of the selected teeth, so unused selected widths disappear too. This is one complete parameterized room family, not the universal W21 theorem.

## Coupled least-index matching

Let L=4c+D_s+D_t, E=D_s+D_t, and for nonnegative integers N define

F(N)=floor(D_s(28+2N)/(2L)+1/2)+floor(D_t(28+2N)/(2L)+1/2).

This map is nondecreasing. Start N_0=0,N_(j+1)=F(N_j). The integer sequence is nondecreasing. Moreover

F(N)<=E(14+N)/L+1.

An integer B>= (14E+L)/(4c) therefore satisfies F(B)<=B. Induction bounds every iterate by B, so the sequence stabilizes after finitely many increases. Denote its first stationary value N, set tau=(28+2N)/L, and n_i=floor(D_i*tau/2+1/2). Then N=n_s+n_t.

Put delta_i=D_i*tau-2n_i. By the floor rule -1<=delta_i<1. In fact delta_i>-1 for BOTH i. If delta_i=-1, the corresponding floor argument at N is an integer. Decreasing N to N-1 decreases that argument by D_i/L>0, so that floor drops by at least one; the other floor cannot increase. Hence F(N-1)<=N-1. Such a supersolution bounds the entire monotone iteration from zero by N-1, contradicting its stationary value N. N=0 cannot be this case: the integer floor argument at least1/2 would force a positive n_i. Thus both portals are strictly interior:

-1<delta_s,delta_t<1.

The exact matching equation is

4c*tau=28-delta_s-delta_t.                 (1)

## Actual normal arms

For each endpoint depth D_i use its OWN prototype from (c+D_i,2) to (c,2+delta_i): for 0<=r<=D_i,

x=c+D_i-r, y=1+F_2(1-2n_i+tau*r),

where F_2 folds modulo4 into[0,2]. It starts at the actual midpoint since F_2(1-2n_i)=1. It ends at the strict portal because 1+delta_i is in(0,2), with upward vertical velocity. Insert contacts when its developed height is an even integer. Exactly n_i contacts occur, all at 0<r<D_i, so their actual depths are strictly between0 and D_i. They hit genuine horizontal selected walls and avoid all corners and unused far ends. A zero-depth arm is empty and has n_i=delta_i=0.

Use the source prototype directly. For the target use the reverse of its OWN prototype, reflected by y->10-y. It starts at strict target portal (c,8-delta_t) with up-right velocity and ends at ORIGINAL T. No seam is treated as a mirror; both splices match velocities.

## Robust five-reflection core

Let beta=c*tau=7-(delta_s+delta_t)/4. Develop horizontal distance z from0 to4c and fold

x(z)=F_c(c-z), y(z)=F_11(2+delta_s+tau*z).

The developed heights at the side events are

j=1: 9+(3delta_s-delta_t)/4 in(8,10),
j=2: 16+(delta_s-delta_t)/2 in(15,17),
j=3: 23+(delta_s-3delta_t)/4 in(22,24),
j=4: 30-delta_t in(29,31).

Thus the first left reflection is at physical height in(8,10), ABOVE all left mouths; the middle right reflection is at height in(5,7), strictly inside the actual right gap(3,7); the second left reflection is at height in(0,2), BELOW all left mouths. The last event folds to the correct target portal height8-delta_t with upward velocity.

The developed path starts at height in(1,3), ends in(29,31), and has positive slope. It crosses exactly the two end lines11 and22. Neither crossing is a side event by the strict intervals just listed. Hence each gives one ordinary roof/floor reflection with0<x<c, not a corner. Together with the three side reflections, there are exactly FIVE genuine core reflections. Every open core segment has0<x<c; no unintended wall can intervene. Both selected portals remain strict interiors of actual mouths.

Concatenation is a finite ordinary specular path with n_s+n_t+5 reflections. The source arm stays in its lower band. Within the core, the only intermediate right-side turn has height in(5,7), so it cannot reach T in the upper tooth. Within the target arm the marked abscissa c+D_t is reached only at its endpoint. Thus first arrival is at the actual T, including either zero-depth case.

## Consequence and limits

The divisibility condition in the frozen A57 Section4 was sufficient for a rigid midpoint-portal subconstruction. It is NOT needed for the actual room theorem: variable portals remove that obstruction. The proof retains all real horizontal dimensions and independent actual depths, with no supplied witness or residual finite prefix. It does not cover other band heights/locations, every pair inside this room, taller teeth, or every canonical45 disk. Universal objective remains OPEN.
