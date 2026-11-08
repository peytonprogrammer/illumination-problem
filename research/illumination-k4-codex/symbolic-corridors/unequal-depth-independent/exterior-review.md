# Independent acceptance of the exterior-irrational reduction

Codex01a1a00f, 6 November 2026.

Verdict: ACCEPT the pinned exterior-irrational.md without mathematical
correction. Every permitted independent outer pair illuminates if at least
one of a/g,b/g,h_-/g,h_+/g is irrational. The full native goal remains
OPEN when all four vertical parameters are rational in units of g.
The horizontal width ratio d/g and both endpoint coordinates remain
arbitrary real values; this is not a reduction to a finite integer grid.

## 1. Required dependencies and effective vertical-only conclusion

The all-noncommensurable-depth theorem is now independently accepted in
phase-lines-review.md and phase-lines-acceptance.json. The actual-mirror L
reduction and the conditional physical cap-sheet lemma are also separately
audited. Normalize d=g=1 and reduce to0<s,t<=1. Cases with irrational a
or b are already closed. Let the remaining a=p/q,b=r/q be positive
rationals with common positive integer q, and put H0=a+1+b>0.

An application to a virtual target/source can be made in an auxiliary
three-band room with its outer cap chosen beyond that virtual mark.
This satisfies the interior hypotheses of phase-lines.md. Only its
VERTICAL chart is subsequently used, so no mirror on the auxiliary cap
is introduced into the physical original room.

Using the full proof rather than just the illumination statement matters:
phase-lines.md can require horizontal cap repairs at centered alpha=1/2
or beta=1/2. In the present effective constructions BOTH phases are
irrational, as checked below, so those exceptions cannot arise. Its proof
therefore supplies a genuine strict vertical chart for every allowed s,t.
No hidden appeal to a path on an artificial exterior wall is needed.

## 2. Irrational upper cap

Let h=h_+>b be irrational. Reflect the virtual target across the actual top
cap, giving B=2h-b>b>0 and H=a+1+B=2h+a+1-b. This H is irrational.
Its effective alpha=a/H and beta=(a+1)/H are irrational because their
numerators are nonzero rationals. Thus neither is1/2, and the accepted
phase-lines proof yields a strict vertical chart for some fixed u,epsilon
and finite integer M.

Write z_M=(u+epsilon*t-s+4M)/H. For free z the portal coordinates are
E1=s+a z,E2=s+(a+1)z. Their residues modulo4 are periodic with period4q.
The sequence z_M on this circle has irrational normalized increment
(4/H)/(4q)=1/(qH), and hence is dense by the already independently
audited elementary circle lemma.

There is a NONEMPTY OPEN subset of this circle where that fixed chart's
two strict portal boxes hold. A successful chart from phase-lines.md
provides a point in the preimage; continuity and strict intervals make it
open. Alternatively, the primitive normal is proportional to(a+1,-a),
with relation constant0 and coprime integer normal after reduction, so the
free-z parametrization covers its connected closure. The possibly nonminimal
period4q does not discard points. The direct preimage argument already
suffices and needs no additional density premise.

At the actual top cap the developed horizontal coordinate is
Xcap=s+(a+1+h)z_M. Since a+1+h=(H+H0)/2, this is exactly
(s+u+epsilon*t)/2+2M+(H0/2)z_M. The upper fold shift u is0 or2,
so a cap corner means Xcap-u in2Z, equivalently Xcap in2Z.
The term2M disappears modulo2. The remaining affine map has nonzero
slope H0/2. Increasing z by4q changes it by2(p+q+r), an even integer.
It therefore defines a well-defined map of the z-circle to the cap phase
circle modulo2; this period check is essential.

Its even-integer set is finite. Indeed over a half-open period of length4q
the affine value traverses an interval of length2(p+q+r), producing exactly
p+q+r zero residues, irrespective of the possibly irrational intercept
containing s and t. A finite set cannot exhaust a nonempty open set.
Removing it leaves a nonempty open subset; density supplies a finite M
in that subset. Both portals and the cap are then strictly legal.

Fold the developed portion above1+h by Y=2(1+h)-y. It ends at actual
T because the virtual target height is1+2h-b. After the cap the physical
height is between1+b and1+h, strictly in the upper band except at the
smooth cap contact. Every vertical reflection there is on an actual upper
side. Simultaneous cap/side contacts are precisely the excluded even phases.
The conditional cap-sheet lemma supplies full velocity matching, finite
smooth contacts, actual endpoints and corner avoidance. If T occurs earlier,
the prefix ending at its FIRST visit is the desired finite connection.

## 3. Irrational lower cap

Let h=h_->a be irrational, A=2h-a>a>0, H=A+1+b. The effective phases
are alpha=1-(1+b)/H,beta=1-b/H; both are irrational since b and1+b
are nonzero rationals and H is irrational. Again no centered half-phase
exception can occur, and a strict vertical chart is supplied.

With the same z_M formula, use the EXACT congruent portal expressions
E1 congruent to u+epsilon*t-(1+b)z_M modulo4,
E2 congruent to u+epsilon*t-b z_M modulo4.
They follow by substituting H z_M=u+epsilon*t-s+4M. Their free-z maps
have period4q, while z_M is dense on that circle for the same reason as
above. A successful strict chart yields a nonempty open preimage.
The corresponding rational normal(-b,1+b) has relation constant1;
after clearing denominators and their common gcd its integer normal is
coprime, so its closure is connected as claimed. A rational multiple-cover
period still parametrizes the whole same circle.

The virtual cap is at-h, a distance A-h=h-a=(H-H0)/2 from the
virtual source. Thus Xcap is exactly
(s+u+epsilon*t)/2+2M-(H0/2)z_M. Its zero residues modulo2 are finite
on the same circle, since the change over4q is-2(p+q+r) and H0>0.
Avoid them in the successful open set. Folding y<-h by Y=-2h-y
starts at actual S: the virtual source is-a reflected across-h.
It travels down to the actual smooth lower cap, then up through the
original portal. The reflected piece lies below y=0, so it cannot enter
the middle band prematurely. All other actual-wall and target details
follow from the already audited cap-sheet lemma. No second irrationality
or independent simultaneous-cap choice is required.

## 4. Exact checks and remaining scope

Run `python3 .context/illumination-k4-codex/symbolic-corridors/unequal-depth-independent/exterior-check.py`.
The independent program verifies the upper/lower cap-coordinate identities,
period increments, congruent lower portal formulas, strict portal conditions
and cap-corner avoidance on two PRESCRIBED exact quadratic-radical examples.
Including reflected reversals, all4actual paths and8wall contacts pass the
own exact full-edge/strict-mirror/first-target validator. No candidate search
or peer code is executed. The open-set/density and finite-zero arguments
above establish arbitrary-real coverage; the examples are not that proof.

The source hash matches the peer's frozen request. Prior accepted proofs
and all original exterior interior constraints are preserved. Combining
this lemma with phase-lines.md closes every case where ANY of the four
normalized vertical parameters is irrational, for arbitrary independent
horizontal marks and arbitrary positive d/g.

What remains is an UNBOUNDED commensurable class: a/g,b/g,h_-/g,h_+/g
all rational, unequal endpoint depths, left-left horizontal marks not both
centered. Equal depths and all centered pairs are already accepted.
The four-cap-sheet covering conjecture is not used or accepted here.
No full rational-class proof, dark pair, all-interior-pair result, another
room family, novelty claim or universal wall minimum follows.
