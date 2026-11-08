# Independent conditional audit of the four cap sheets

Codex01a1a00f, 6 November 2026.

Verdict: the acceptance conditions in the pinned cap-chart-screen.py are
SUFFICIENT for an actual finite connection, with a first-target truncation
step when needed. Its rational finite-period screen is valid for these
specified families. The 1,350 passing parameter controls do not prove
continuous coverage. No whole unequal-depth theorem is accepted here.

## Conditional lemma, arbitrary real dimensions

Choose lc,uc in {0,1}. Set A=a if lc=0, else A=2h_--a; set B=b
if uc=0, else B=2h_+-b. All are positive. Let H=A+g+B and develop
from (s,-A) to (L,g+B), with L=u+epsilon*t+4dM, u=0 or2d,
epsilon=+1 or-1, and finite integer M. Write
X(z)=s+(L-s)(z+A)/H, E1=X(0), E2=X(g).

Use the previously accepted four strict portal boxes and their lower,
middle and upper folds F_(2d)(X), d+F_(2d)(X-c), F_(2d)(X-u),
with c=d or3d. In addition, if lc=1 require
X(-h_-) not in 2d Z; if uc=1 require X(g+h_+)-u not in 2d Z.
These are exactly the two modulo-2 exclusions in the normalized program.

Fold the vertical coordinate independently by
Y(z)=-2h_--z for z<-h_- when lc=1;
Y(z)=2(g+h_+)-z for z>g+h_+ when uc=1;
and Y(z)=z in between. Because 0<a<h_-, the reflected lower start
-A lies strictly between -2h_- and -h_- and maps to actual -a.
The lower reflected portion remains strictly below y=0. Similarly,
0<b<h_+ puts the reflected upper endpoint g+B strictly between
g+h_+ and g+2h_+, and it maps to actual g+b; that reflected
portion remains strictly above y=g. Thus both portal crossings retain
Y=z and unchanged upward velocity. No extra horizontal ledge is encountered
by either cap excursion.

At each vertical-fold event the reflected horizontal component changes
sign, with the vertical component unchanged, so it is a smooth actual
vertical-wall reflection. At each included cap event Y' changes sign,
with horizontal velocity unchanged; the added cap-phase exclusion prevents
a simultaneous vertical-fold event and excludes both cap corners.
The strict portal boxes already exclude every other possible band-corner
collision. The physical x folds always lie in their correct chamber widths.
The source and target are their actual prescribed interior points.
A finite developed segment has finitely many fold events.

Consequently the entire folded curve obeys the actual-wall specular law
and avoids all corners. It may pass through actual T earlier than the final
lifted image. In that event take its prefix ending at the FIRST actual T.
Since T is interior, this cuts an interior straight segment and preserves
every reflection already traversed. Finitely many segments ensure that
an earliest positive target visit exists. This proves a finite legal
connection with first arrival; it does not require every full lifted curve
to have first arrival at its final image.

## Actionable first-arrival detail

A successful cap chart must not be rejected merely for encountering T
before its final image. Nor should the untrimmed curve be reported as
first-arrival without checking. Concrete prescribed fixture:
d=g=1, s=t=3/2, a=1/2,b=3/2,h_-=3/4,h_+=7/4,
lc=uc=1,u=0,epsilon=+1,M=0,c=1. The developed line is vertical,
both strict portals and both cap exclusions pass. The full curve would
reflect at both caps, but it already reaches T on its first upward trip.
Its first-arrival connection is simply
(3/2,-1/2) -> (3/2,-3/4) -> (3/2,5/2), with one lower-cap reflection.
This is a bookkeeping issue for physical certificates, not a counterexample
to the existence mechanism. The peer's screen currently claims only
phase-coverage controls, so it has not falsely certified those trajectories.
Include prefix truncation or an equivalent earliest-hit rule in any full
physical validator and final existence proof.

## Finite rational period

For fixed lc,uc,u,epsilon, let alpha=A/H,beta=(A+g)/H, and include
cap times gamma_l=(A-h_-)/H and gamma_u=(A+g+h_+)/H when their caps
are selected. If these ratios are rational, the program's Q equal to the
lcm of their denominators satisfies Q*lambda integral for every tested
time lambda. Replacing M by M+Q changes each tested X by4d times
an integer. It preserves both modulo-4d portal phases and modulo-2d cap
exclusions. Therefore M=0,...,Q-1 covers all arithmetic outcomes of
this SPECIFIED family, including outcomes for negative M. Q need not be
minimal. Horizontal coordinates s,t need not be rational for this periodicity;
the implemented controls nevertheless use fixed rational placements.

Failure across all four sheets and all finite periods would exclude this
mechanism at those exact rational depth/cap parameters only. It would not
exclude additional cap repetitions, other reflection words, or prove darkness.
The current receipt reports all 1,350 prescribed parameters covered and
17,853 chart tests. I read its code and receipt; I did not execute its writer
or independently rerun that discovery census. No inference of universal
coverage follows from these reported counts.

## Independent prescribed physical checks

Run `python3 .context/illumination-k4-codex/symbolic-corridors/unequal-depth-independent/cap-sheet-check.py`.
This own program scans no candidate integer, direction or parameter family.
Its four fixed tuples exercise original, upper-cap, lower-cap and both-cap
sheets, with the last explicitly testing early-target truncation. All four
actual paths and six wall contacts pass the independent actual-edge checker.
It verifies cap guards and rational-period identities at every included
event time. The general conditional theorem is proved above by folding;
the four examples do not establish a full-family covering theorem.

Hashes in cap-sheet-check.json identify the exact screen revision reviewed.
That live peer algorithm may change; future claims and counterexamples need
fresh review and source reconciliation. Parent solving remains with the peer.
