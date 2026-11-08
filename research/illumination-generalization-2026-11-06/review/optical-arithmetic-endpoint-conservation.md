# Conservation needed for exact residue coverage: endpoint multiplicity matters

Independent challenge, Codex01a1a00f, 2026-11-07. A finite-family hand theorem and quantified ABSTRACT countercontrols, not an actual room counterexample or a new positive low-reflex theorem. This identifies the extra condition a conservation/cyclic-order proposal must prove.

## 1. Rooted residue windows and their multiplicity

For each ACTUAL admissible branch component i, normalize its shooting coordinate as in optical-arithmetic-interval-prerequisite.md to an OPEN interval(A_i,B_i). Exact target roots correspond to integers in that interval. More generally define on the phase circle R/Z

    C(theta)=sum_i # {n in Z: A_i<theta+n<B_i}.

For a finite family this is a finite nonnegative integer-valued function. It retains multiple integer preimages of one window and repeated windows; it does not pretend every counted label is a distinct physical path. The fixed actual target has its designated phase theta0=0 after each branch normalization. An abstract window from independently chosen source/target image data must not be inserted without a common physically guarded branch.

The global goal needs C(0)>0 for some proven adequate actual family. Mere positive measure of C>0, positive average C, or a cyclic description with no registered target phase cannot establish that pointwise statement.

## 2. Exact jumps and boundary deficit

Let L(theta) be the number of lower endpoints A_i congruent to theta modulo1, and U(theta) the number of upper endpoints B_i congruent to theta. Counts include EVERY developed image and its multiplicity, even if several arise from the same physical corner. Taking one-sided limits gives

    C(theta+)-C(theta-)=L(theta)-U(theta),
    C(theta)=C(theta-)-U(theta)=C(theta+)-L(theta).

The second line is essential: both endpoints of every interval are excluded. It is invisible in an almost-everywhere or distributional derivative statement. If a proposed root lies at a physical forbidden boundary, no average or cancellation legalizes it. A separate accepted actual-path corner-removal argument can handle a removable case, but must be tied to that physical boundary; it cannot be assumed for every window endpoint.

The normalized total length identity is

    integral_0^1 C(theta) dtheta = sum_i (B_i-A_i).

It is an average identity, not a pointwise lower bound. It follows by integrating integer translates of each interval indicator; no optical conservation law is needed for this tautological identity.

## 3. Even PERFECT endpoint cancellation does not force the exact target

Suppose a proposed finite family actually proves the strongest local balance

    L(theta)=U(theta) at EVERY phase theta.

Then C has a constant integer value M on all nonendpoint arcs, with M=sum_i(B_i-A_i). At the endpoint phases, however,

    C(theta)=M-U(theta).

Hence in this balanced setting exact coverage of a fixed target phase is equivalent to

    M>U(theta0),

and coverage of EVERY phase is equivalent to M>max_theta U(theta). These are sharp conditions for this finite balanced-window model. Balance plus M>0 proves only generic coverage; the boundary multiplicity deficit must still be controlled. No bound by the number r of PHYSICAL corners follows, because OR02 already gives many developed encounters with one corner. A valid charge proof needs a quantitative excess after retaining all images and multiplicities.

Explicit countercontrol: the two windows(0,1/2),(1/2,1) have total length1 and pointwise L=U at both endpoint phases0,1/2. They cover every other phase exactly once, but C(0)=C(1/2)=0. Their closures cover the whole circle; their OPEN union misses the exact designated target. Repeating this pair N times gives M=N and U(0)=N, with C(0)=0 for EVERY positive integer N. Arbitrarily large average and exact charge cancellation still leave the target uncovered.

These are abstract windows, not claimed jointly realizable room data. They refute a general INFERENCE based only on balance/average/closure coverage, and identify the extra theorem needed before such facts could imply optical illumination. They do not refute any room-specific law that supplies that extra theorem.

## 4. Cyclic order requires a registered phase and a base multiplicity

For a finite family and a reference phase theta* not on a boundary, traverse a positively oriented lift from theta* to theta. The exact formula is

    C(theta)=C(theta*)
      + # lower endpoints strictly between theta* and theta
      - # upper endpoints after theta* and AT OR BEFORE theta.

All phases are lifted once consistently around the circle; a full loop has zero net jump. The upper endpoint at theta is subtracted, while the lower endpoint there does not enter yet. Thus a cyclic-order proof can force C(theta0)>0 only by controlling a base multiplicity and the cumulative deficit, with this exact endpoint convention. Knowing only total lower/upper charge (always zero for a finite family) supplies neither.

The previous failing pair and the translated pair(1/4,3/4),(3/4,5/4) have the same lengths and unrooted cyclic boundary structure, but the translated pair has C(0)=1. The target phase is fixed physical data and cannot be rotated independently of the windows. A certificate must register its position relative to the developed endpoints.

## 5. Unbounded word families need a justified limiting argument

The theorem target has no word bound. A proof using all words may have infinitely many endpoints or accumulation phases; OR02 makes finite physical-corner counts inadequate. Nonnegative window counts can be summed as extended values, but cancellation of infinite signed endpoint charges and expressions infinity-minus-infinity are not justified by nonnegative convergence. A finite cutoff needs a proved remainder bound, or the argument needs local finiteness/summability that actually holds for the selected family. None is assumed here.

An infinite sum of lengths can diverge while C(0)=0: infinitely repeat the same two failing open windows. This adds multiplicity without adding the missing phase. Distinct abstract duplicates are unnecessary as geometric evidence and are not proposed as a room construction; the example is a warning about the logical insufficiency of totals alone.

## Required missing implication

To advance the actual programme, prove that ORIGINAL r<=8 supplies an actual joint branch family with either a positive pointwise excess at0 (for example M>U(0) under a VALID balance law), a registered cyclic-order/base-count bound, or another legal actual-target construction. Neither the interval-root prerequisite nor these abstract window identities is that theorem. The original-r9 dark control must be excluded by a genuine geometric use of r<=8, not by an unconditional window conservation assertion.
