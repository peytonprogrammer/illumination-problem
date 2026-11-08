# FP01: exact native period for all five original-floor/roof programmes

Status: independent HAND prerequisite, pending reciprocal review. This extends the accepted monotone-only MC03 to the author's complete declared ST10-A class, by rebuilding physical event states. It supplies neither a passing slope nor a universal illumination theorem. No numerical search, new engine or enumeration is implemented or run.

## Statement

Fix an integral four-band staircase and distinct native interior marks S=(s,u), T=(t,v), with u<v after reversal. Fix one of the five ST10-A vertical programmes and an initial horizontal sign sigma. Normalize |vy|=1 and |vx|=tau>0. Let L=lcm(w0,w1,w2,w3) and P=2L. Adding or subtracting an integer multiple of P, while keeping tau positive, preserves every visited seam/floor/roof event's physical x and outgoing horizontal sign, each first-hit/corner guard, and every possible actual-target crossing along that programme. It may change the number of ordinary vertical bounces. The resulting path is reconstructed, not copied as a fixed reflection word.

Consequently existence in the entire five-programme class is equivalent to existence among its exact candidate slopes in 0<=tau<P, with both initial signs and all programme choices, using the physical event guards below. At tau=0 use the direct vertical path only; no horizontal sign or wall bounce exists. The common period is sufficient; no claim of minimal period is made.

## Physical event recurrence

Include every crossed band seam, every prescribed outer floor/roof event, and EVERY crossing of physical target height v. Cumulative vertical travel, and all successive travel differences Delta, are integers because all walls and native endpoint heights are integral. The first event is measured from ACTUAL u, not from a band boundary. At time zero assign a source on a seam to the band actually entered by its initial vertical sign; both adjacent limiting folds agree there because an interior seam mark has 0<s<w_upper. No artificial zero-length bounce is inserted.

On an open event-to-event flight the width is a fixed actual band width w. From physical state (x,e), e in {+1,-1}, the next position is

    x_next = F_w(x+e*tau*Delta),
    F_w(z)=min(z mod 2w, 2w-(z mod 2w)).

The horizontal velocity is the one-sided forward-time derivative of this fold. At a smooth left-wall event x_next=0 its outgoing sign is +1; at a right-wall event x_next=w its outgoing sign is -1. At ordinary interior events the derivative gives the unchanged physical signed germ. This rule counts a simultaneous smooth seam/left-wall bounce exactly once.

At an UPWARD narrowing from lower width a to upper width b<a, require x_next<b. x_next=b is the true reflex corner; x_next>b hits an actual horizontal ledge and is outside ST10-A. The strict guard also excludes the wider ledge's other endpoint a. At a DOWNWARD widening from upper b to lower a require x_next<b as well: equality b is the same true reflex corner. The other ledge endpoint a cannot be reached from the upper band. Zero is permitted in either case because the common left wall is smooth at every internal seam. On passage retain x_next and the same outgoing signed horizontal germ in the next band; the portal is not a mirror.

At the true floor0 or roofH require 0<x_next<w, where w is respectively w0 or w3. The endpoints are genuine polygon corners and forbidden. An interior contact reverses vy and preserves vx. Within every open flight all vertical-wall contacts are at heights strictly inside one actual band, so every such contact is an ordinary finite wall interior. These checks exhaust first-hit and genuine-corner guards in the declared class. Positive finite widths, finite tau and total vertical travel give finitely many bounces.

At ANY target-height event, test x_next=t BEFORE rejecting a later corner or itinerary event. Since actual T is interior, this target event cannot itself be a wall corner. Stop at the first matching visit. In particular, a nominated post-roof target may already have been attained on ascent. A later singularity does not invalidate that legal prefix. Every prefix of one of the five programmes ending at T is itself in their union, so this convention loses no class member.

## Period proof, including signed germs and corners

Compare tau and tau'=tau+kP, both positive. At an event assume their physical positions and outgoing horizontal signs coincide. For the next flight,

    (x+e*tau'*Delta)-(x+e*tau*Delta)=e*k*P*Delta.

Because Delta is integral and P is divisible by every 2w, this difference is a full period of F_w and its forward germ. Thus the next x and horizontal sign coincide exactly. This remains true at x=0 and x=w by the one-sided definitions. Their vertical programme is the same. Every seam inequality and floor/roof strict inequality has the identical truth value; every target-height test matches identically. Induction starts at the same actual source and sigma. This proves both directions, including subtraction of P until a positive representative is reached. For a slope congruent to zero, direct vertical success is the appropriate zero representative: if a positive multiple of P passes all events to a target, its event positions all equal s, so s=t and the vertical segment crosses no blocking ledge before v; that direct segment succeeds. Conversely a legal direct vertical segment is in the union. No extra vertical germ is ascribed to tau=0.

Additional right/left bounces between successive events stay inside actual finite wall interiors. Thus the proof is actual-room transport of this finite-programme feasibility predicate; it is not a claim that an arbitrary affine slope change preserves arbitrary billiards or their fixed words.

## Exact finite root set, not nonemptiness

For programme duration D in

    v-u, u+v, 2H-u-v, u+2H-v, 2H-u+v,

the horizontal reflections unfold actual T to eta*t+2g*n, where eta=+/-1 and g is the gcd of all widths visited by that nominated programme. This follows by composing the actual vertical reflections x->-x or x->2w-x; horizontal reflections do not change x. Hence every successful terminal member satisfies

    s+sigma*tau*D = eta*t+2g*n.

Both sigma and eta are required. Since D is a positive integer and P is a multiple of 2g, each sign pair contributes exactly DP/(2g) arithmetic candidates in one half-open period, before the deterministic physical guards. At most 2DP/g candidates cover that programme, before duplicates. Using all-four-width gcd instead is a safe larger set if desired. Earlier-target successes are already candidates for the corresponding shorter programme in the union. A complete exclusion must retain them, rather than discarding a slope merely because its later nominated itinerary hits a corner.

For native even-even s,t,u,v every listed D is even and tau*D is even. Thus any qualifying reduced slope denominator divides D/2. This is only a necessary arithmetic restriction; seam constraints and actual signed states still decide feasibility. Counts depend on unbounded metric/endpoint data, and do not bound directions or reflections by wall count.

## Scope and concrete use

FP01 fills the explicit missing completeness prerequisite identified in staircase10-candidate-preliminary.md. It justifies exact modular necessity/interval elimination across the whole admitted class if such an argument is later supplied. It does NOT authorize or run a census, and does NOT prove that any residue passes. Internal ledge-reflecting rays are outside ST10-A and remain possible even if that complete class eventually fails. Arbitrary real metrics/marks generally lack this integer event-time period.

Independent challenge requested: downward-widening reflex exclusion, source-seam vertical-direction convention, simultaneous smooth-left bounce, all target-height visits before later singularities, and the zero-residue reduction. The full all-metric staircase10 and r<=8 goals remain OPEN.
