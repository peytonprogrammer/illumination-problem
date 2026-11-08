# Exact strict-open root prerequisite

Independent hand derivation, Codex01a1a00f, sharper-root phase, 2026-11-07. This is a prerequisite only, not a global optical theorem. The accepted OR01 map is inherited, not re-proved as new progress.

## One signed, physically guarded component

For an actual jointly guarded source/chamber/target branch, fix epsilon in{+1,-1}, K=a+b+2h>0 and an OPEN connected domain J=(l,u), l<u. Its candidate roots are m_n=(2nw+epsilon*beta-alpha)/K. Put

    A=(K*l+alpha-epsilon*beta)/(2w),
    B=(K*u+alpha-epsilon*beta)/(2w).

Then m_n belongs to J if and only if A<n<B. The exact smallest and largest allowable integers are

    n_min=floor(A)+1,
    n_max=ceil(B)-1.

Hence a root exists exactly when floor(A)+1<=ceil(B)-1, and the number of integer labels on this component is

    N=max(0,ceil(B)-floor(A)-1).

This is valid for positive or negative endpoints, including negative winding numbers. No rounding tolerance or closed-interval replacement is permitted. If A is an integer, that integer is excluded. If B is an integer, it is excluded. For example(0,1) has no root, while(0,2) has exactly the label1. An interval of length exactly1 has one integer unless both endpoints are integers, in which case it has none. An interval shorter than1 may still contain an integer; its absolute position matters.

The two signs generally have different target access branches, parameters and domains. Evaluate the criterion separately on each ACTUAL common guard component; existence is an OR over those components and signs. Adding counts may double count aliases of the same path, so it counts labels, not distinct physical rays. Abstract independent source/target images with no joint access do not define an admissible component.

## Physical qualifications

The criterion is necessary and sufficient for an integer root inside THIS declared component. Through accepted OR01 it yields an actual S-to-T path if all source, actual-target/lift, first-hit, direction and exterior-chamber hypotheses are satisfied on that component; an ear roof-corner root is treated by the accepted actual-pair retracing removal. A root at a component boundary is not licensed by the OPEN-component proof. It may be illegal, or it may require a separate chart/removal argument; it cannot simply be added to a closed interval.

Finite-word guard domains may have several connected components. Do not replace their union by its convex hull, or use one component's lower endpoint and another's upper endpoint. For unbounded families of words, there need not be a finite partition; OR02 already proves infinitely many boundaries from a single physical reflex corner. Isolated direction charts (for example a zero denominator or a vertical direction) need explicit handling outside the chosen parametrization.

For K=0 in a proposed generalized defect equation, this formula does not apply; one must inspect the actual constant defect and positive time. K is strictly positive in OR01, so no such degeneracy is part of this prerequisite.

A failure of all declared components is not failure for all physical branches unless their coverage has been proved. Nor is the OR01 class of paths known to cover all actual illumination mechanisms. These quantifier distinctions apply to both the r2/r4 fixed-cap controls and the original-r9 dark control.

## Exact prescribed checks

The paired Python uses Fraction floor/ceiling arithmetic for endpoint-equality cases and the two target signs. It verifies the following analytically selected new narrow-root controls, whose actual geometry is in optical-arithmetic-narrow-cap-controls.md:

- Accepted r2 cap, K106, epsilon+1, alpha4,beta6,J=(1/100,3/100): (A,B)=(-47/1600,59/1600), only label0, m=1/53.
- Accepted nondirect r4 cap, K706, epsilon+1, alpha4,beta54,J=(7/100,9/125): (A,B)=(-29/1600,13/500), only label0, m=25/353.

Both intervals are far below the old sufficient width threshold. Exact root membership is useful evidence about those prescribed physical branches, not a reason that every original r<=8 room supplies one. A global residue-window argument still needs a noncircular positive coverage statement at the EXACT fixed-target residue, retaining open endpoint deficits and all developed-image multiplicities.
