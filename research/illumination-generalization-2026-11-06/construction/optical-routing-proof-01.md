# OR01: positive guarded interval lemma

Author hand proof, pending independent review. Candidate: optical-routing-candidate-01.md. This proves its LOCAL sufficient lemma only. The global G8 selection statement remains unproved.

## 1. Complete physical scattering

Use the candidate's physical chamber E and open section M. Parameter m is horizontal velocity divided by positive vertical velocity on entry. Put x=alpha+a*m. The rectangle unfolding sends the first return to y=0 to horizontal coordinate z=x+2h*m. Define f_w(z) by folding the real line into [0,w]:

- f_w(z)=z-2nw on (2nw,2nw+w), with derivative +1;
- f_w(z)=2nw-z on (2nw-w,2nw), with derivative -1.

Provided z is not in wZ, the physical first return is (f_w(z),0), with velocity proportional to (f_w'(z)*m,-1). Elapsed chamber time is 2h*sqrt(1+m^2) at unit speed. Before then its vertical folded coordinate is strictly between 0 and h, except the one top contact. Thus there is no earlier mouth crossing. Vertical side reflections can occur finitely many times, since z ranges over a finite interval along this finite path.

No additional physical wall is inside E, by the chamber hypothesis. Every vertical-side contact away from y=0,h is smooth and satisfies the specular law. The sole possible chamber corner event other than a mouth endpoint is at the top, when x+h*m is an integer multiple of w. Both top corners are actual convex right angles. Bottom endpoints are excluded by the strict entry/exit guards, even if a particular mouth endpoint is regular in D.

The source and reverse-target branches in the hypothesis have actual lift labels and positive flight times. Their unfoldings can be placed in the terminal physical mouth frame, yielding images (alpha,-a) and (beta,-b). Their stated relations, rather than a target projection, are used below. There is no assumed reflecting mouth.

## 2. Exact direction AND position matching

Write L=a+b+2h>0. The forward target suffix must start at x_T=beta-epsilon*b*m with velocity (epsilon*m,-1). Matching both exit position and the horizontal sign is exactly

    z=2nw+epsilon*x_T,
    alpha+(a+2h)*m=2nw+epsilon*beta-b*m,
    L*m=2nw+epsilon*beta-alpha.                 (1)

Because 0<x_T<w throughout J, (1) lies inside the correct open folding strip for epsilon, not on a fold boundary. Consequently it implies f_w(z)=x_T AND f_w'(z)=epsilon. Conversely every matching first return in that signed chart has (1) for some integer n. The common velocity scale is positive and identical along the joined ray; normalization uses sqrt(1+m^2). No mixed slopes or concatenated directions appear.

All exact matches thus occur at the arithmetic progression

    m_n=(2nw+epsilon*beta-alpha)/L, n in Z,

of spacing 2w/L. These are choices of complete paths, not same-position resonance of a chosen path.

## 3. A positive choice, not just an equation

Let ell=u-l. Under L*ell>2w, the image interval

    ((L*l-epsilon*beta+alpha)/(2w),
     (L*u-epsilon*beta+alpha)/(2w))

has length greater than one. It contains an integer n. For example choose the least integer strictly larger than its left endpoint; the length condition places that integer strictly below its right endpoint, including when the left endpoint itself is an integer. Then m_n belongs to the SAME guarded connected interval J.

Both actual external branches exist at m_n by the universal guard hypothesis. Section 2 proves the chamber return matches actual position and directed velocity, so concatenation reaches actual T. If its top contact is smooth, the whole path is already a legal finite specular trajectory.

## 4. Convex-corner root removal preserves the actual pair

A top-corner root does not prove its nominal reflection word legal. Instead use the following explicit retracing argument. The top right-angle continuation reverses the physical velocity: in the developed plane, crossing the corner changes both coordinate reflection signs. It exactly retraces the incoming physical path.

Let gamma:[0,A]->D be the concatenated continued path, parametrized by length, and c its only actual corner-contact time. Source and target branches avoid all corners, so only this chamber contact needs removal. Uniqueness of ordinary billiard motion implies gamma(c+v)=gamma(c-v) until min(2c,A).

- If A<2c, actual T already occurs at time 2c-A<c. Truncate the source path there.
- A=2c would imply actual T=S, excluded.
- If A>2c, gamma(2c)=actual S. Discard the initial excursion and retain the segment from time 2c to A. It contains no corners and reaches actual T.

These are legal paths between the original physical endpoints. They need not retain an individually selected unfolding label or the nominal reflection word; the goal permits that. This is the same accepted removable-corner principle recorded in parity-sign-theorem/pocket-detection.md Section20. It is rederived here, not used to ignore reflex corners.

Thus every matching root in J yields a legal actual S-to-T path, directly or by removal, proving the local lemma.

## 5. Scope and the unproved global implication

The lemma needs no r bound and is consistent with the dark r9 control: that control cannot admit data satisfying all of these hypotheses. It does NOT justify filling or deleting anything, and makes no claim about a reduced-room witness. It also does not assume an open set of exact target hits: it selects an isolated exact root from two guarded prefix curves.

The inequality L*ell>2w is a sufficient quantitative shooting condition. Low r has not been shown to force it for any chamber/branch choice. Large a,b from long recurrence do not suffice: ell depends on the complete first-hit guards and may shrink faster. Qualitative recurrence supplies no lower bound for L*ell. The source/target prefix domain is not the whole independent phase box in the older robust-portal lemma; however this new narrower interval hypothesis still needs a global existence proof.

Therefore G8 is OPEN and no full r<=8 illumination claim follows. A useful next implication would bound the total loss at the endpoints of these guard intervals in terms of ORIGINAL reflex corners. Any such proof must account for multiple distinct encounters with the same corner; optical-routing-reflex-reuse.md records a one-reflex obstruction to naive injective counting.
