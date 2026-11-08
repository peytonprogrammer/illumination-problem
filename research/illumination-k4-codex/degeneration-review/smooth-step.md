# Smooth-step equality: a scale-control and interval certificate

[done] Analytic criterion and exact algebra controls. [done] Opus independently accepted the geometric setup, scale absorption, normalized limit and exact dual criterion on 2026-11-01. This establishes a sufficient exclusion method for a fixed decorated boundary configuration. It does not exclude any new physical room or prove that every smooth step satisfies the criterion.

## What is new

The accepted collapse reduction preserves the integer cost W+2B only for isolated one-edge smooth steps. Near such a limit, several reflected connections give coupled interval constraints. There is a missing step before treating those intervals as a linear feasibility problem: other room parameters might move much farther than the short edge length.

The result here supplies that step. If the connection gradients have full rank along the collapsed boundary stratum, every nearby dark approach is O(epsilon), where epsilon is the step width. Consequently, an exact infeasibility certificate for a finite family of normalized closed intervals really excludes a dark approach, with quadratic errors controlled. Full rank or the number of listed paths alone is not an exclusion.

This first version treats an orthogonal normal step, with two vertical faces joined by one horizontal short edge. A diagonal short connector can have a different additional reflection branch and is not covered by the optical formula stated here. Several collapsing steps and multiple visits to the blocker also require their own charts.

## Fixed geometric setup

Start from a strictly simple orthogonal polygon with two distinct interior marks and one smooth boundary blocker z. Use the cyclic shape in which z is resolved into a short horizontal step between two upward vertical faces. Fix the orientation so its width epsilon is positive; the opposite orientation is a separate chart. At epsilon=0 the two vertical faces merge and z remains a labeled smooth blocker.

Use the usual affine chart of anchor coordinates, directed positive edge lengths and mark coordinates. Include the short edge coordinate, which vanishes at the base. Impose closure and a transverse normalization fixing translations and both positive axis scalings, using surviving horizontal and vertical edges. On this normalized linear slice, write the base as theta_0 and a displacement as delta in a d-dimensional vector space V. The short-edge width is a nonzero linear functional E(delta)=epsilon.

Choose finitely many limiting connections gamma_i of the undecorated base polygon. Each is blocked only by z: it reflects there exactly once, transversely, and all its other contacts are strictly inside inherited positive faces. Assume a nonzero tangential component at z and strict interior endpoints. Fix their exterior reflection words and which inherited face every exterior reflection uses.

Develop each prefix and suffix independently into the local wall chart, omitting the reflection at z. Orient the geometric below/above pair so their developed points are

    A_i(theta)=(-a_i(theta),u_i(theta)),
    T_i(theta)=(-b_i(theta),v_i(theta)),

with a_i,b_i>0 and u_i<0<v_i near the base. The local corner is the chart origin; its moving position and the moving face support are included. For orthogonal fixed words these four quantities are affine functions of theta. The lower face is x=0,y<0; the upper face is x=epsilon,y>0.

The two exterior words are fixed, and their other limiting contacts are strict. Therefore their local face replacements remain valid global connections whenever the local inequalities below are strict and theta is sufficiently close to theta_0. A dark nearby configuration must defeat both replacements for every i.

## Exact necessary interval

Put

    K_i(theta)=b_i(theta)u_i(theta)+a_i(theta)v_i(theta).

This is a quadratic polynomial and K_i(theta_0)=0. The lower-face replacement works if K_i<0. The upper-face replacement works if K_i>−2epsilon u_i. These are the exact formulas proved in `collapse-reduction.md`, not a first-order approximation. Hence every nearby dark configuration satisfies

    0 ≤ K_i(theta_0+delta) ≤ −2 E(delta) u_i(theta_0+delta).       (1)

The endpoints are included: hitting a corner invalidates a connecting word. Let

    g_i = dK_i(theta_0)|V,
    c_i = −2u_i(theta_0)>0.

Uniformly over this finite word list,

    K_i(theta_0+delta)=g_i(delta)+O(||delta||²),
    −2 E(delta)u_i(theta_0+delta)=c_i E(delta)+O(E(delta)||delta||).

These statements are necessary constraints only. Feasibility does not certify darkness, and unlisted connecting words can still light the room.

## Proposition: boundary rank controls the scale

Assume that the only v satisfying E(v)=0 and g_i(v)=0 for every i is v=0. Equivalently, the rows g_i restricted to the boundary tangent space ker E have rank d−1. Then every sufficiently small dark displacement with epsilon=E(delta)>0 obeys

    ||delta|| ≤ C epsilon,

for a constant C independent of the displacement.

**Proof.** The map v -> (E(v),g_1(v),…,g_m(v)) is injective on V. Finite-dimensional norm equivalence gives a constant L such that

    ||delta|| ≤ L (|E(delta)|+max_i |g_i(delta)|).

By (1) and boundedness of u_i in a fixed neighborhood, max_i |K_i(theta_0+delta)|≤C_0 epsilon. Taylor expansion therefore gives

    max_i |g_i(delta)| ≤ C_0 epsilon+C_1||delta||².

Consequently ||delta||≤A epsilon+D||delta||². For ||delta||<1/(2D), absorb the quadratic term and obtain ||delta||≤2A epsilon. If D=0, no absorption is needed. This proves the claim.

The assumption tests rigidity along the decorated boundary, including movements of the blocker and marks. It is not automatically implied by rigidity of one of the previously checked interior dark rooms. Nor does it follow from finiteness of unlit targets on a fixed polygon.

## Theorem: normalized interval incompatibility excludes the approach

Under the setup and rank hypothesis, suppose the finite affine system

    E(v)=1,
    0 ≤ g_i(v) ≤ c_i  for every i                              (2)

has no solution. Then some neighborhood of theta_0 contains no dark configuration with a positive step width.

**Proof.** Otherwise choose dark displacements delta_n->0 with epsilon_n=E(delta_n)>0. The proposition bounds v_n=delta_n/epsilon_n. Pass to a convergent subsequence v_n->v. Then E(v)=1. Divide (1) by epsilon_n. Since ||delta_n||=O(epsilon_n), its quadratic remainder divided by epsilon_n tends to zero, and the upper coefficient tends to c_i. Thus 0≤g_i(v)≤c_i for every i, contradicting infeasibility of (2).

This handles arbitrarily separated shrinking rates only when the boundary-rank hypothesis holds. It needs no numerical neighborhood radius, no sampled rays, and no claim about a uniform word length. It uses exactly the fixed finite words selected for the certificate.

## Exact dual certificate

Choose h in V with E(h)=1 and a basis of ker E. Write v=h+x in those coordinates, so

    g_i(v)=A_i x+b_i.

The normalized intervals become

    −A_i x≤b_i,
     A_i x≤c_i−b_i.

A sufficient infeasibility certificate consists of nonnegative rational lower weights lambda_i and upper weights mu_i with

    sum_i (mu_i−lambda_i)A_i=0,
    sum_i [lambda_i b_i+mu_i(c_i−b_i)]<0.                      (3)

Multiplying and adding the inequalities would give 0 bounded above by a negative number, impossible. At a rational base all these quantities can be rational and checked with exact arithmetic. A numerical solver can propose weights; its verdict alone is not the certificate. The checker must also verify the optical premises, derivatives, normalization and boundary rank, as in the earlier rigidity work.

The supplied exact example A_1=A_2=1, b_1=0,b_2=2,c_1=c_2=1 has dual weights lambda=(1,0), mu=(0,1), giving −1. It illustrates the certificate format; it is not asserted to arise from a room.

## What does not supply an exclusion

**Path reversal.** Reversing a connection and restoring the geometric below/above endpoint convention produces the same K and the same interval. It is not a second independent obstruction. The same warning applies to identical unfolded words disguised by labels. Any rank count must use actual restricted gradients.

**Shared endpoints.** The pair 0≤x≤1 and 0≤−x≤1 admits x=0. A step can remain positive while every tested constraint lands at a corner endpoint. Strictly positive interval widths do not remove that possibility.

**Full rank alone.** Even rows of full rank on the whole (x,y,epsilon) chart can allow epsilon=1. For example the rows x,−x,y,−y,epsilon/2 with upper bounds 1 admit (0,0,1). The actual interval feasibility or its dual must be checked separately.

**Ignoring scale control.** The algebraic band 0≤x²≤epsilon allows x=sqrt(epsilon), so x/epsilon diverges. Its derivative on the boundary tangent vanishes. This is an explicit reason the rank hypothesis cannot be skipped when replacing nonlinear conditions by epsilon-normalized linear ones. This is an algebraic diagnostic, not a constructed dark sequence.

**Only local steps.** A one-edge smooth step translates one part of a wall's support. A limiting connection can reflect on that translated part elsewhere in its prefix or suffix. Those support changes affect a_i,b_i,u_i,v_i and must be included. Keeping all exterior images artificially fixed can create a spurious common endpoint or a spurious incompatibility.

## Literature: usable facts and an important limit

Lelièvre–Monteil–Weiss permit regular marked stopping points in Section 2. Their Theorem 2 gives finitely many unlit targets for a fixed marked surface and source. This does not bound the family as the polygon or blocker varies. [Publisher PDF](https://msp.org/gt/2016/20-3/gt-v20-n3-p11-p.pdf).

Apisa–Wright's Theorems 3.6 and 3.16 impose a non-torus-cover hypothesis. Their Theorem 1.1 distinguishes the commensurable tiled case. Consequently those classification statements cannot simply be applied to our lattice-room unfoldings, which cover tori. [Author-hosted paper](https://websites.umich.edu/~alexmw/ApisaWright.pdf).

One physical wall blocker is also not one regular surface point. A smooth boundary point pairs adjacent copies under its wall reflection. With four unfolding copies for an orthogonal room it has two lifts; with eight copies for a genuinely mixed canonical-direction room it has four. Every lift must be treated as a stopping point, together with the corner lifts. A theorem about one prescribed surface blocker would not automatically cover this orbit of blockers.

These observations prevent unsupported shortcuts to universal blocker removal. They do not show that blocker removal is false, or preclude applying a suitable classification to a separately verified non-torus-cover limit.

## Verification and remaining task

[done] `smooth-step-check.py/json/log` verifies the exact abstract dual, rejects three corrupted certificates, checks the shared-endpoint/full-rank countercontrols, 108 reversal identities, and rank-deficient versus rank-injective algebraic scale examples. The examples are explicitly algebraic and do not exclude any new room.

[done] Opus independently accepted the geometric setup, scale-absorption argument, normalized interval theorem, exact dual and blocker lift counts. No fixed decorated limit with the needed independent connection list has yet been supplied. Instantiating the criterion requires those data and exact word/gradient verification; inventing a ray catalogue is outside this task.

**Next move:** obtain or derive a concrete low-cost decorated limit and determine whether its boundary gradients are injective. If so, test (2) with an exact dual certificate. If not, its residual kernel identifies the additional deformation or higher-order mechanism that must be addressed. Global minimality, universal smooth-blocker removal, diagonal connector scattering and multiple-step compatibility remain open.
