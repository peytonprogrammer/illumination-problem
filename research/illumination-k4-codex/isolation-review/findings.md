# Independent review of general-isolation Lemmas 25–27

Status: accept the parity darkness and necessary midpoint statements with
explicit lattice/lift hypotheses. Accept the relative-period reformulation
after fixing the exported sign convention. Do not accept the claimed coverage
of all known dark rooms or the proposed growth law as established facts.

## 1. The parity subclass omits our known 22-wall room

The four examples in the new section pass its parity premise. But the final
claim that every known canonical45 dark room is a parity room is false under
that definition. The independently certified cand-2_2-1 has non-A smooth
lattice points (-1,0), (1,0), (2,1), (2,3). None is even-even and none is a
polygon corner. Its source and target remain (0,0),(2,2).

Thus parity-room isolation is a restricted structural target, not yet a
classification of the known mechanisms. The reflected-copy/retracing proof
for cand-2_2-1 is already an example the raw non-A-corner criterion misses.
One possible later extension is to pass to a suitable finite reflected
quotient carrying the obstruction, but that requires an explicit theorem;
this audit does not supply it.

## 2. Lemma 25: accept with the parity-preserving tiling stated

Use A=s+2Z^2, with s,t in this same class. Every corner is integral. Every
wall reflection must preserve Z^2 and A. In the canonical tiling this holds
for integer-coordinate horizontal/vertical walls and diagonal lines x±y=2k.
It would not hold for arbitrary diagonal lattice walls x±y=2k+1. For example,
reflection in x+y=1 sends (0,0) to (1,1). “45-degree lattice room” alone is
therefore insufficient; the canonical parity-preserving hypothesis matters.

Under these conditions, unfold any proposed finite positive-length path.
The developed target is s+2g w, g>=1 and w primitive, with nonzero displacement.
The point s+w lies strictly inside the developed segment, is non-A, and folds
to a non-A lattice point of the closed room. The corner premise obstructs it.
This proves the statement, including smooth-wall endpoints if final arrival
there is allowed. It does not imply local isolation of these configurations.

## 3. Lemma 26: accept as a necessary structure of one-corner events

Suppose the event has exactly one intermediate developed corner image. The
g points s+(2j+1)w, 0<=j<g, are non-A corners. They are distinct developed
points even if some project to the same physical vertex. Therefore g=1 and
the unique interior lattice point is the midpoint s+w.

All 932 frozen optical endpoint records pass the exact primitive-half-vector
check: 168 for room24,179 for room34,403 for Wolecki22 and182 for Jain28.
Every half vector is integral and primitive. This is a frozen-data identity,
not a newly discovered trajectory or an independent revalidation of the
extra Jain axis event. Previously accepted event validity supplies the
one-corner premise.

The combinatorial construction still needs a labeled unfolding, corner
sheet/sector ownership and an admissible side continuation. Simply saying
“fold the midpoint and next point” cannot erase those choices. Regular
45/90-degree corner continuations reverse physical direction; contact
vertices may have distinct labels at one coordinate. For an admissible
one-corner continuation that reaches t at s+2w before another corner, the
midpoint test is sufficient. The primitive midpoint structure makes a finite
cover combinatorics approach plausible; it does not remove the need to
calculate the folding state and valid local side.

## 4. Lemma 27: valid relative-period identity, exported sign needs repair

All paths and relative classes must live on the same unfolded surface, with
actual lifts of s,c,t among the marked endpoints. Let C=hol(gamma1) and
A=hol(gamma1)+hol(gamma2). At the base, C=w and A=2w. Let
eta=[gamma2]-[gamma1]. Then hol(eta)=0 at the base and
boundary(eta)=s+t-2c, with the lifted labels understood.

The exported certificate functional uses f=side*cross(A,C). Direct
calculation gives

    d cross(A,C) = -cross(w, delta hol(gamma2)-delta hol(gamma1)).

Consequently, with sigma equal to the exported side,

    g_e(delta) = -sigma * <p delta y - q delta x, eta>.

The displayed plus-sign formula is correct only if sigma is defined as the
negative of the exported side, or eta is reversed. This is a convention fix,
not a failure of the zero-holonomy reformulation. All48 exact algebra controls
pass. One elementary check is w=(1,0), delta gamma1=0, delta gamma2=(0,1):
the exported cross(A,C) derivative is -1, while the displayed plus pairing
is +1. Signs cannot be left implicit when proving positive span.

The bend-angle derivative is cross(w,delta hol(eta))/|w|^2. The angle condition
must be stated on the appropriate developed corner sheet. It cannot mean
an ordinary physical angle >=pi inside a convex135-degree corner. Such
corners do occur in the accepted Wolecki event list.

An ambient GL(2,R) period variation annihilates eta because hol(eta)=0.
For the room chart, restrict to GL variations that actually preserve the
billiard family. With diagonal walls and fixed canonical directions this
gives translations and uniform scale, not arbitrary shears. Orthogonal
rooms additionally allow independent axis scales. This agrees with the
previously verified kernel dimensions.

## 5. Growth is not the missing positive-span theorem

A fit for |g|/a over a<=32 does not prove sublinear growth of eta. The row is
a direction-dependent contraction of relative periods pulled back to the
room chart; a bound on that contraction is not automatically a norm bound
on the whole relative class. Even an actual sublinear norm bound would say
nothing by itself about the required signs.

For an exact algebraic control, take rows m e_j in dimension three and set
length a=m^2. Their norms grow exactly as sqrt(a); their common kernel is
zero. Nevertheless their positive cone is only the positive orthant. No
strictly positive combination vanishes. Thus full rank plus sublinear growth
does not establish isolation.

Forni's primary paper treats generic conservative flows and deviations of
ergodic averages via the Kontsevich–Zorich cocycle:
https://arxiv.org/abs/math/0405031. That statement does not directly supply a
uniform signed-spanning theorem for this collection of rational saddle
connections. Treat the KZ link as a proposed research direction. It requires
a bridge from these particular relative classes/admissible sides to a
recurrence or distribution theorem, and then a separate argument forcing
both signs against every nonsymmetry deformation. No such bridge is in the
memo yet.

## Suggested next structural target

State the exact missing sign theorem: for every nonzero normalized room
variation delta, some admissible midpoint event e has
-sigma_e*cross(w_e,delta hol(eta_e))<0. The sphere compactness argument then
extracts a finite certificate, provided the event implication holds in a
neighborhood. This separates the desired geometric sign recurrence from
unproved norm-growth claims. Proving it for the parity subclass would be a
real advance, but would still leave the reflected-copy22 mechanism outside
its current scope.
