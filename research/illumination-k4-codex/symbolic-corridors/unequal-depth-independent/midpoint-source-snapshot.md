# Unequal-depth corridor: live argument

Status: incomplete. Equal-depth theorem independently accepted and reconciled.
New lemmas below are parent arguments awaiting independent review.

## 1. Common-core reduction survives unequal depths

The equal-depth proof section1 does not use equality of depths. If at least
one horizontal coordinate is strictly greater than d, the same actual-mirror
L-subroom path works with arbitrary a,b. If both exceed d, the direct segment
works. Only 0<s,t<=d remain. Reversal and reflection about y=g/2 exchange
(s,a,h_-) with (t,b,h_+), so one may order horizontal coordinates if useful,
but this also exchanges depths and imposes no independent depth ordering.

## 2. Complementary charts for unequal depths

Normalize d=g=1 using positive diagonal scaling. Let H=a+1+b,
alpha=a/H, beta=(a+1)/H, so 0<alpha<beta<1. For u=0 or2,
epsilon=+1 or-1 and M integer, set L=u+epsilon*t+4M and
X(y)=s+(L-s)(y+a)/H. Then

    E1=(1-alpha)s+alpha*epsilon*t+alpha*(u+4M),
    E2=(1-beta)s+beta*epsilon*t+beta*(u+4M).

The SAME four portal boxes as the accepted equal-depth proof are sufficient:
(u,c; E1mod4,E2mod4)=(0,1;(1,2),(1,2)),
(0,3;(2,3),(2,3)), (2,1;(1,2),(0,1)), (2,3;(2,3),(3,4)).
Lower F2(X), middle1+F2(X-c), upperF2(X-u) match value and derivative
on each box. Endpoint lift and finite actual-wall legality are unchanged.
This is sufficient; chart failure is not darkness.

## 3. A genuine unequal-depth obstruction to ALL vertical-only paths

For s=t=1 and b=a+1 (arbitrary a>0), no legal S-to-T trajectory can
reflect only at vertical walls. Every vertical mirror has integer x. Its
unfolded target coordinate is an odd integer L, because reflections
x->2j-x preserve odd integers and actual target x=1 is odd. Vertical
velocity is positive and constant, so the developed line from (1,-a)
to (L,1+b) reaches y=1 at its midpoint: beta=(a+1)/H=1/2.
Its developed x there is (1+L)/2, an integer. Any composition of
reflections in integer vertical lines preserves the integer lattice,
so its physical x is an integer too. But crossing into the upper chamber
requires x strictly in(1,2), impossible at an integer. The trajectory
therefore hits a corner or fails to enter the chamber. This applies to
all reflection words, not just the four chosen chart families.

This is a continuum of unequal-depth obstructions to a proposed mechanism,
NOT a dark counterexample. The full polygon might admit a path involving
horizontal reflections. A proof by complementary vertical charts alone
cannot complete the objective.

