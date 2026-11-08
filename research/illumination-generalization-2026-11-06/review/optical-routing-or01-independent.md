# OR01 independent challenge: conditional local lemma accepted, G8 open

Codex01a1a00f, 2026-11-07. Final independent review of construction/optical-routing-review-request-01.json and all THREE pinned files. All pins checked before and after review; the author supplied hand arguments, not a checker packet. This is HAND algebra and an independent Fraction replay of specified controls. No discovery search, census or author checker execution.

## Decision on the stated candidate

ACCEPT the local sufficient implication, conditional on ALL actual source/target access guards holding on the WHOLE common interval J. The strict width inequality supplies a real exact-target root; it does not merely reformulate illumination. A proof of the global G8 availability claim has not been supplied. Do not count this local acceptance as completion of the full orthogonal target.

I independently derive the following proof of the local candidate rather than accepting its proposed construction on trust.

## 1. Signed scattering, including both orientations

Use the candidate's horizontal mouth coordinates. A source state (x_S, velocity(m,1)) enters the chamber. Before the roof y=h, the y-coordinate increases monotonically; afterwards it decreases until the next mouth hit. Side reflections change only the sign of horizontal velocity. The unfolded horizontal coordinate at exit is

    X=x_S+2h*m.

On the horizontal unfolding of [0,w], an exit at actual x_T with horizontal sign epsilon has exactly the image relation

    X=2n*w+epsilon*x_T, n in Z.

For epsilon=+1, X is in (2nw,(2n+1)w), so the fold has derivative+1. For epsilon=-1, X is in ((2n-1)w,2nw), so it has derivative-1. These intervals and their signs follow from x_T in(0,w), including negative n. They must not be replaced by an unsigned mod-w condition.

Substitute x_S=alpha+a*m and x_T=beta-epsilon*b*m:

    K*m=2n*w+epsilon*beta-alpha,
    K=a+b+2h>0.

The exit position AND velocity then equal the target branch's required position x_T and forward velocity(epsilon*m,-1). The source speed and reversed-target speed are equal after normalization because their slopes have the same magnitude. No direction change occurs at the mouth.

## 2. A genuine positive local intersection

As m ranges over the connected open interval J=(l,u), the quantity K*m-epsilon*beta+alpha ranges over an open interval of length K*(u-l)>2w. Every such interval contains a member of 2wZ strictly in its interior. Therefore at least one integer n gives an exact solution m in J. This is a true sufficient root-existence argument under the width hypothesis, not density, recurrence, or an equation presented as an existence theorem.

The WHOLE-J access hypothesis now matters: this root satisfies all source and reversed-target first-hit/corner guards because every m in J does. It also has both mouth coordinates strictly internal, excluding mouth endpoints on entry and exit. On an ordinary ear excursion the only true corners it could meet are the two convex roof corners. All other side hits occur with 0<y<h; it cannot revisit y=0 before the final exit. There are finitely many side reflections for finite h,w,m. At m=0, there are no side reflections and roof contact is smooth because x_S is strict interior.

## 3. Convex roof corners cannot simply be discarded

REJECT the stronger auxiliary claim that a root supplied by the width inequality must itself avoid the roof corners. This is not an error in the frozen author proof, which explicitly supplies retracing removal. It can be the ONLY root and can hit a roof corner. The exact actual r2 example below proves this.

Nevertheless the candidate's illumination conclusion survives by a direct deterministic-overlap argument, without permitting an illegal reflection. If the unfolded roof coordinate x_S+h*m equals q*w, the unfolded exit coordinate is2q*w-x_S. Since0<x_S<w, its folded value is x_S and its fold derivative is-1. Thus m is nonzero and the required matching sign is epsilon=-1, with x_T=x_S.

Consequently the actual source branch and actual REVERSED-target branch arrive at the same mouth point with the SAME upward velocity(m,1): the reversed-target velocity is(-epsilon*m,1)=(m,1). Reverse both branches from that section state. Physical billiards away from corners have a unique backward evolution. The shorter branch is therefore the initial portion of the longer one. If their lengths were equal, S=T, contrary to the hypothesis; hence one actual endpoint lies strictly along the other's branch. The intervening subpath is a legal finite actual S-to-T ray, reversed if necessary, entirely outside the chamber and without a roof-corner hit. The proof uses only the two stated corner-free prefixes and actual endpoint distinctness.

If a proposed source/suffix already reaches the other endpoint earlier, truncate there; that already supplies illumination. This does not justify a claimed later first-arrival word but suffices for the existential conclusion.

## 4. Exact sole-root corner fixture

Let D be the lower rectangle[-8,24]x[-24,0] with attached E=[0,16]x[0,8]. Its vertices in order are

    (-8,-24),(24,-24),(24,0),(16,0),
    (16,8),(0,8),(0,0),(-8,0).

This is a strictly simple integer orthogonal room with r=2. Set S=(4,-8), T=(-2,-16), both distinct actual even-even interior points. Take

    w=16, h=8, alpha=4, a=8,
    beta=-2, b=16, epsilon=-1,
    J=(1/5,11/10).

For every m in J the source and reversed-target branches are straight and first reach the mouth at4+8m and-2+16m, both strictly in(0,16). Their entire prefixes lie in the lower rectangle; they cannot encounter a true wall or corner first. The outside access domain is connected and full, as required.

Here K=40 and K*|J|=36>32. The only matching root in J is m=3/4 (n=1). Both mouth positions equal10 and the roof contact is(16,8), a true convex corner. Thus blindly using that root as a legal chamber path is invalid. But T->S->(10,0) is one straight reversed-target prefix: the direct S-to-T subpath is legal. This independently verifies the overlap repair under actual target-class geometry, not an abstract curve example.

Own replay optical-routing-or01-independent-replay.py/json checks signed fold identities for BOTH epsilon orientations in four prescribed roots, one actual smooth roof path, all affine guard extrema in this corner fixture, actual first-hit collision with the two roof-corner walls, its reflex count, and the legal shortened S-to-T segment. The universal local proof is the preceding algebra/uniqueness argument, not these finite checks.

## 5. Domain and global quantifier decisions

- ACCEPT requiring the source and reversed-target access guards on all J; this is exactly what makes the root legal outside the chamber.
- ACCEPT the two signed target charts and matching formula, with actual sheet identity included in the branch hypotheses.
- ACCEPT the strict inequality as sufficient. No necessity claim is established; equality or smaller width may still have legal roots and illumination.
- ACCEPT the frozen author proof section4: its explicit length-parametrized retracing cases implement the required removal and preserve actual S,T. The stronger corner-free-root assertion is false, but the author does not rely on it.
- OPEN G8: no noncircular reason original r<=8 forces an actual chamber with the required joint interval/width has been proved. Geometry reduction availability by itself does not supply this metric condition.

There is a quantitative access constraint worth retaining: from alpha+a*m and beta-epsilon*b*m in(0,w) on J one has a*|J|<=w and b*|J|<=w. Thus long access words, if they enlarge a or b, also constrain the admissible common interval. One cannot infer (C) just by making an access branch longer. These are necessary inequalities, not a proof that (C) cannot hold.

## 6. Inherited scope controls

The r1 nonresonance example forbids identical-state retuning of every reduced-room witness. OR01 allows different entry/exit positions and selects m jointly with n. Its local proof does not impose that forbidden retuning premise, so that r1 control does not refute OR01.

The original r9 known22 dark room rules out the unconditional statement that every orthogonal room/endpoint pair has OR01 data satisfying(C). Its all-pairs reflection control is inherited and not rerun. Since the conditional local lemma is valid independently of r, that dark room must fail at least one of its access/chamber/width hypotheses for every proposed branch data. This is a logical consequence, not a direct geometric classification of all chambers in that room and not a positive use of r<=8.

The independent r0 dense-disjoint control shows why irrational generic recurrence cannot supply actual endpoint access/intersection. OR01's finite real interval plus lattice-root argument is a different, valid conditional mechanism. It still needs the low-reflex availability theorem.

## Handoff

The local lemma is progress; the universal target remains OPEN. Next review target is a pinned full author argument and any claimed global forcing of(C). The concrete missing information is control of joint guard intervals relative to K and w across all nondirectly-visible original marked rooms with r<=8. Mixed axial/diagonal canonical45 remains separate and open.

## 7. OR02 independent all-n review

ACCEPT the pinned single-reflex reuse argument at its stated scope. For D=[0,8]x[0,4] union[0,4]x[4,8], S=(6,2), and m_n=2/(16n-2), the developed first top hit is(16n+4,4). At each intervening support x=8j, 1<=j<=2n, its height is

    2 + 2*(8j-6)/(16n-2).

Its minimum is strictly greater than2; its maximum at j=2n is4-8/(16n-2)<4. All2n side contacts are therefore smooth, and the next hit folds to the sole reflex corner(4,4). They precede any mouth/top encounter because y increases strictly from2 to4.

To verify both one-sided domains without an unspecified small perturbation, set the first developed top abscissa to16n+4 plus or minus1/2. The corresponding slopes are2/(16n-2 plus or minus1/2). Both retain exactly2n side supports and fold to x=9/2 or7/2. The latter enters the open mouth and the former hits the true top wall. This proves distinct first-mouth branch boundaries for every n>=1. The finite-word partition lemma remains intact; the infinite multiplicity is across different words.

Own optical-routing-or02-independent-replay.py/json checks prescribed n=1,2 from raw wall intersections. The displayed inequalities and one-sided formulas prove all n, without a reflection cutoff or census. This rejects only an injective charge from guard endpoints to distinct physical reflex vertices. It does not reject signed cancellation, a quantitative width estimate, G8 or the illumination theorem.

All FIVE review questions are answered: signed matching ACCEPT, strict interior root ACCEPT, actual-pair convex-corner removal ACCEPT, OR02 all-n guard obstruction ACCEPT, and a positive use of r<=8 remains OPEN.
