# A regular-intermediate Farey triangle relation

Independent hand candidate, pending peer review. This is a nontrivial local relationship among directional endpoint maps, not a corner charge or a proof of the full illumination theorem. No computation, new room or discovery search is used.

## Exact covering and directional data

Let pi:M->R^2/Lambda be a finite translation covering of a connected compact translation surface, branched only over the origin. Here Lambda is a specified rank-two lattice. Write Z for genuine cone points, and V0=pi^{-1}(0). Points in V0 may be genuine cones or regular points; actual regular corner marks are regular for this lemma. Let Vreg=V0 minus Z.

For a primitive lattice vector a and x in Vreg, lift the straight based torus loop t*a, 0<=t<=1, starting at x. Its open part has no visit to the branch value, so its lift is uniquely defined and contains no cone. Its endpoint at time1 exists in the compact covering completion. Denote it E_a(x). If that endpoint is a genuine cone, the physical/cone-avoiding trajectory STOPS; no outgoing prong or continuation is selected. A regular endpoint permits the same-direction continuation. These are ONE primitive-period endpoint maps, not automatically first marked-return edges with arbitrary integer length.

Choose primitive u,v in Lambda with lattice determinant +1 or -1. Then w=u+v is primitive too. Suppose

    x in Vreg,
    z=E_u(x) in Vreg,
    y=E_v(z) in Vreg.

The claim is the exact completed-sheet identity

    E_{u+v}(x)=y.

In particular the straight lifted mediant from x to y is cone-avoiding. If x,y are actual interior endpoint lifts in an integral physical unfolding whose corners project to0, it also avoids ALL actual corner lifts on its open part.

## Proof by the lifted triangle, not by an optical turn

Use a lattice basis to identify Lambda with Z^2. Since det(u,v)=+/-1, the matrix with columns u,v is unimodular. Its inverse maps the closed triangle

    Delta=conv{0,u,u+v}

to conv{0,e1,e1+e2}. The latter has no integer lattice points except its three vertices. Thus Delta has no other lattice points, on its edges or in its interior. This proves the required branch exclusion without any bound on the coordinates of u,v.

Pull the torus cover back to the developed plane. Over the open triangle there is no branch point and the triangle is simply connected. Each connected sheet above it is therefore a single copy. Select the sheet adjoining the interior germ at the vertex0 determined by the REGULAR source x. Regularity means local degree one, so this germ is unique across the angle between u and u+v.

This sheet extends along the open side0->u and its endpoint is z, by uniqueness of the lifted u segment. Because z is REGULAR, a full sufficiently small disk about u lifts locally one-to-one at z. The triangle's two sides meeting there therefore belong to the same local lift: the continuation along u->u+v is exactly the v lift starting at z. Its endpoint is y by hypothesis.

The same selected sheet extends along the open diagonal0->u+v. Near u+v, the arriving side from u lies in the local degree-one neighborhood of the REGULAR y. Its incident triangle germ and the diagonal share that same endpoint neighborhood. Hence the lifted diagonal ends at y. Equivalently, the triangle sheet has consistent regular completions at all three vertices, so its three boundary sides lift to a closed triangle with vertices x,z,y.

Extensions to the closed sides are legitimate: away from the three vertices they lie over unbranched points; approaching a vertex within a triangle wedge is Cauchy in the pulled-back flat metric, with path lengths tending to zero, and the compact completion gives its unique endpoint. At regular x,z,y the local degree-one neighborhoods identify that completion with the stated points.

The diagonal is an actual single straight segment of direction u+v and primitive-period duration1. At intermediate times its basepoint is not0, so it meets no point of V0, including any genuine cone or removable physical corner lift. The broken two-leg route was used only to identify its exact endpoint sheet; it is not declared a legal ray with a turn at z.

For det(u,v)=-1 the selected triangle lies on the opposite side of its first edge. Local regularity and the same empty-triangle argument give the same identity. No preferred incoming/outgoing cone prong is assumed because the hypothesis excludes a cone at every vertex used in the proof.

## Exact necessary consequence for actual off-orbit darkness

In a qualifying physical unfolding, take the COMPLETE distinct actual source/target fibers X,Y contained in Vreg. If the original pair is dark, there cannot exist x in X and determinant-one primitive u,v with

    z=E_u(x) regular and E_v(z) in Y.

Such a chain would supply the straight mediant X-to-Y path just proved, contradicting actual darkness. This is more than the separate absence of X-to-Y edges in the u and v diagrams: the intermediate z is any regular completed base-fiber point and the second return starts at that exact point, with its true sheet.

More generally, where BOTH regular two-step chains E_v(E_u(x)) and E_u(E_v(x)) are defined with regular intermediate and terminal points, the two empty triangles give

    E_v(E_u(x))=E_{u+v}(x)=E_u(E_v(x)).

This is only a REGULAR-DOMAIN diamond identity. It is not a global commutation law for monodromy generators and says nothing about a word that passes through a genuine cone. A peripheral detour at a ramified basepoint may change its sheet/prong; replacing it by the straight mediator requires information absent from an arbitrary loop word.

## What it does not force

This relation does NOT assert that a regular two-step X-to-Y chain exists. If no such chain exists, it supplies no first-cone event and no blocker count. A source direction can be periodic on regular points and never encounter Y or Z. Darkness alone does not convert “not in Y” into “in Z.”

It also does not extend blindly to return durations m,n>1: a larger triangle may have extra lattice points in its interior or along its sides, and their lifted ramification/intermediate events must all be controlled. Every omitted repeated development remains part of the actual data. The lemma is uniform in unbounded primitive directions, not a claim that one-period tests decide illumination.

Even if one can eventually force cone interceptions for many pairs of directions, the same physical reflex can occur in multiple developed images or parity classes. No injective assignment or nine-distinct-reflex lower bound follows. The proof uses the one-branch-value cover structure; a low-reflex or disk-quotient contradiction needs additional geometry beyond this lemma.

## Required calibrations and lattice caveats

- Q0: accepted all-word physical darkness and the full-fiber cone-only transfer exclude the regular two-step cross-fiber chain above. The lemma provides a cross-direction consistency check, not a new proof of Q0 darkness, a parity-factor converse or a count of its nine reflex corners.
- Q100: actual darkness transports by diag(100,1). In the SAME old unit coordinate lattice this map changes a determinant by100, so Farey adjacency must not be claimed invariant. Use the transported base lattice diag(100,1)Lambda to preserve normalized determinant-one adjacency and one-branch-value hypotheses; or apply the lemma independently in the new unit-torus cover. Actual endpoints and sheets must be transported as well.
- Six-wall intrinsic half-turn control: its marked dark graph pairs the SAME physical point and includes removable regular blockers. It is not an off-orbit actual dark X times Y pair, and does not contradict this cone-only regular-domain relation.
- Heisenberg control: on its primitive area9 torus there are nine distinct branch images, so one-branch-value/empty-triangle hypotheses fail. On its unit-torus cover the entire origin fiber consists of genuine zeros, so there is no regular x there to which this lemma applies. Shifting a generic regular source's torus phase to0 shifts the branch values too; it does not repair the hypothesis. This is an applicability check, not a new physical exclusion argument.
- Weighted-return limitations: an arithmetic identity or a word in generators without these regular triangle domains still does not supply a straight ray. No finite direction set or W-bounded state quotient is introduced.

The exact new implication is the regular-intermediate endpoint/mediant relation and its necessary off-orbit darkness exclusion. Its premises and its limitation are explicit. It does not complete the full orthogonal r<=8 theorem or construct a qualifying dark counterexample. No novelty claim is made.
