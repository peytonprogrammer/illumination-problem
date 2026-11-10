# Repeated visits disappear in the orthogonal smooth-step case

Status: proof and exact controls completed by Codex; independent Opus review
requested. This is an elementary local-flow reduction, not a global
illumination theorem.

## Main result

Let P be an orthogonal polygonal room, s,t distinct interior points, and z a
point strictly inside a maximal boundary wall. A valid connecting trajectory
has positive length, finitely many ordinary specular reflections, and no
corner contacts. Stop it at its first arrival at t.

**Theorem.** This trajectory reflects at z at most once.

It follows that the repeated-visit exclusion in our orthogonal smooth-step
criterion is unnecessary for first-arrival limiting connections. There are
no coupled repeated-visit branches to analyze in that precise setting.
The rank hypothesis and normalized-band incompatibility remain unproved in
general; this result does not eliminate either of those gaps.

## Proof: same outgoing state forces an earlier target

Parameterize by constant-speed time. Suppose two visits to z occur at times
r1<r2<T, before the first target arrival T. Put L=r2-r1. If their outgoing
velocities agree, both the position and outgoing velocity states agree.
Billiard evolution is unique between ordinary reflections and remains
unique through a smooth specular reflection. Comparing the paths starting
at r1 and r2 therefore gives

    alpha(T-L)=alpha(T)=t,

where T-L>r1>=0. This contradicts the choice of first target arrival.
The reasoning only compares portions of the existing finite trajectory;
it assumes no extension through a corner or beyond the endpoint.

## Proof: the other outgoing state is impossible for nonaxial motion

Rotate the coordinate frame so the walls are horizontal or vertical. Each
reflection changes the sign of one velocity component, so |vx| and |vy| are
constant along the trajectory. First suppose both are nonzero.

Take z on a vertical wall with the room locally to its left. Its outgoing
velocity must be one of

    (-p,q), (-p,-q),    p>0, q>0.

The same-state case was excluded. If the first outgoing velocity is v and
the second is the other one, the incoming velocity at the second visit is
-v. Consider only the excursion beta from the first visit to the second.
Its time reversal beta(L-u) starts at z with outgoing velocity v, exactly
as beta(u) does. Uniqueness and reversibility give

    beta(u)=beta(L-u),    0<=u<=L.

At the temporal midpoint, there are two possibilities. If the midpoint is
inside the room, differentiating this identity gives a nonzero velocity
equal to its negative, which is impossible. If it is an ordinary wall
collision, the one-sided velocities satisfy

    v_after=-v_before.

For a specular reflection in a line, this happens only at normal incidence.
At an orthogonal wall, normal incidence requires vx=0 or vy=0. That
contradicts the conserved nonzero component magnitudes. A corner midpoint
is prohibited by path validity. These exhaust the finite-trajectory cases.
The horizontal-wall argument interchanges x and y. The argument also works
with the opposite inward normal.

## Axial directions

If one component vanishes, a transverse visit to z has only one possible
outgoing velocity. Thus any two visits have the same state, already
excluded. A trajectory starting in the interior cannot glide along a wall
without first hitting one of its endpoints, which would be an invalid
corner contact. This proves the theorem for all valid connecting paths.

## Stronger corollary for an essential smooth boundary blocker

Suppose a finite set of smooth boundary blockers makes s,t dark, but after
removing z there is a corner-free connection avoiding the other blockers.
Stop that connection at its first target arrival. It must meet z, and the
theorem says it meets z exactly once.

Furthermore, it cannot be axial. A horizontal trajectory starting at s
stays in the closure of one connected interval of the horizontal line's
intersection with P. Its target lies in that same open interval. The direct
segment from s to t therefore lies entirely in the interior and avoids
all boundary blockers. The vertical case is identical. Such an axial
connection would contradict decorated darkness.

Consequently a connection witnessing that z is essential can be chosen
with nonzero normal and tangential velocity at its unique reflection at z.
The single-visit and nonzero-tangential-component premises of our local
step formula are automatic here. Other strict-contact/face-convergence
premises of the smooth-step theorem still need to hold.

## Consequence for the accepted smooth-step criterion

In a Jordan orthogonal point-collapse limit with distinct interior marks,
a smooth collapse point z is a genuine smooth wall point of the undecorated
limit room. Any ordinary finite connecting word used to test whether z is
an essential blocker may be truncated at first target arrival. It then
reflects at z once, with nonzero tangential component, or avoids z entirely.
An avoiding word is already a persistence obstruction to a dark sequence.
An essential word is covered by the existing exact local band

    0 <= K_i(theta) <= -2 epsilon u_i(theta).

This removes a coverage limitation of that criterion. It supplies no new
finite list of such words, no automatic rank, no incompatible-band
certificate, no uniform length or clearance, and no treatment of real
limits that are already ordinarily dark. Multiple distinct collapsing
points, contact/slit limits, and nonorthogonal families remain separate.

## Why the orthogonal hypothesis matters

A fixed analytic counterexample occurs in the right-isosceles triangle
0<y<x<2. Let

    s=(7/4,3/4), z=(2,1), c=(3/2,3/2), t=(3/2,1/2).

The prescribed corner-free path is

    s -> z -> c -> z -> t.

Its directions are NE, NW, SE, SW. Both z contacts are inside the vertical
wall; c is inside the diagonal wall. The collision at c is normal and
reverses the entire velocity, so the z-to-z excursion retraces itself.
The target is not encountered on any earlier leg. This is exactly the
midpoint alternative excluded by orthogonality in the proof. The room and
marks are directly visible, so it is not a dark-room counterexample.

The no-repeat theorem must not be extended to general canonical45 rooms
with diagonal walls. It proves the precise orthogonal claim we need, and
the triangle explains the scope sharply.

## Verification

check.py verifies the four formal nonaxial outgoing-state alternatives,
the exact normal-reversal matrix kernels, the two axial cases, and the
prescribed triangle path's three reflections, interior legs, absence of
corner contacts and first target arrival. These controls use no trajectory,
word, direction or room search. The uniqueness/reversibility proof above
establishes the theorem; finite algebra checks alone do not.

Run:

    python3 -B .context/illumination-k4-codex/smooth-step-multivisit/check.py
