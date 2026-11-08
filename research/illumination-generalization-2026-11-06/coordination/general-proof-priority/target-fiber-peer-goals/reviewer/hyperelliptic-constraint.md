# Full-group central reflection constraint for every L metric

HAND derivation for the entire nondegenerate orthogonal L family. No room, ray, direction or orbit search and no arithmetic parameter restriction. This is a necessary structural lemma, not a proof or disproof of the assigned complete-target-fiber seed gate.

Let M be the connected four-copy unfolding of a strictly simple L room. It has five convex physical corners and one reflex corner. Let J=RxRy be simultaneous copy-label reversal. Write Sigma for every physical corner lift, including the five regular convex ones.

## 1. Surface and fixed points

The four polygon interiors are disjoint. A smooth wall identifies only the two copies differing in its normal reflection label. J changes both labels, so it fixes neither an interior point nor a smooth-wall point. At each physical vertex all four local copies join into one point. Thus

Fix(J)=Sigma,

with five angle-2pi points and one angle-6pi point. There are exactly six fixed points. The polygon cell decomposition has four faces, twelve glued edges and six vertices, so chi(M)=-2 and M has genus 2. These assertions use only the actual boundary gluing; an artificial rectangle cut is not another wall or fixed locus.

J is a genuine global affine involution with derivative -I. In particular it is an isometry for the unfolded flat metric.

## 2. The derivative kernel is trivial

Suppose h is an affine automorphism with derivative I. The unique angle-6pi cone c must be fixed. In a small neighborhood of c, a translation coordinate w wraps three times about the ordinary plane. Derivative I means w(h(z))=w(z)+constant on regular patches. Taking z to c makes that constant zero. Therefore h locally permutes the three sheets over w by a deck rotation. It is either locally the identity or a rotation of order 3. Local identity extends over the connected regular surface, hence globally. In the nonidentity case h has order 3 globally, since h^3 is locally identity.

A nonidentity derivative-I map cannot fix any regular point: a fixed point makes its local translation constant zero, hence makes it locally and globally identity. Thus an order-3 h would act freely except at c. The quotient N=M/<h> is a closed oriented surface. The unique branch point has ramification index 3; covering Euler characteristics give

chi(M)=3chi(N)-2.

Since chi(M)=-2, chi(N)=0, so N is a torus. Removing c and its image yields a connected regular degree-3 cover of a once-punctured torus with deck group C3. Its monodromy lies in the abelian group C3. A peripheral loop of a once-punctured torus is a commutator of the two handle loops, so its image in C3 must be the identity. But local index-3 branching requires nontrivial order-3 monodromy around that same loop. Contradiction.

Therefore the derivative kernel contains only the identity. The area/Euler calculation alone would not exclude h; the puncture monodromy contradiction is essential.

## 3. Every genuine affine map commutes with J

Let F be any affine homeomorphism of M, including orientation-reversing maps. Its commutator with J has derivative

D(F)(-I)D(F)^-1(-I)=I.

The derivative-kernel result forces F J F^-1 J^-1=1. Hence FJ=JF. Consequently F automatically preserves Sigma=Fix(J). On this L surface the complete physical-corner preservation requirement imposes no extra restriction beyond being a genuine affine automorphism. This conclusion has been proved here only for the L unfolding and is not an authorization to transfer the kernel argument to surfaces with several cones.

## 4. Exact structure of all four transformed target lifts

Put z=F(q) and w=F(Rx q). Because J Rx=Ry and FJ=JF,

F(Gq)={z,Jz,w,Jw}.

These are four distinct actual points when T is interior. This uses exact points and the actual involution J, not merely torus residues or projected physical coordinates. It is a full-group necessary invariant for every L metric, without an integer-lattice preservation hypothesis.

It does NOT imply F(Gq)=G F(q). The second representative w need not equal Rx z or Ry z; the accepted H2 control already violates normalization of G. Thus the four targets have a guaranteed pairing, but the transverse pair cannot be chosen by convenient physical projection.

## 5. Antipodal obstruction and its exact limitation

No finite straight regular unfolded segment can join a point x outside Sigma to Jx while avoiding Sigma. If gamma:[0,L]->M were such a segment, define eta(t)=J gamma(L-t). Its initial point is x and its initial velocity equals gamma's, because reversal and derivative -I cancel. Uniqueness of the straight flow away from Sigma gives eta=gamma throughout. Then gamma(L/2)=J gamma(L/2), placing the midpoint in Fix(J)=Sigma, a contradiction.

This is an actual geometric obstruction, not a failure of a shear or a selected direction. But it cannot alone refute the present gate for distinct physical S,T. For any g in G, gq=Jp would imply T=rho(gq)=rho(Jp)=S. Since S and T are distinct, no original target lift is Jp. Centrality then shows no F(gq) is JF(p). Thus all four admitted targets avoid this particular full-group obstruction automatically. Absence of this obstruction is not a visibility or affine-seed availability theorem.

## Frontier

The lemma constrains the entire affine group and all four target lifts. It does not establish that either antipodal target pair meets the source's polygon copy in a visible point. It supplies no arithmetic descent, terminal availability or universal seed. A claimed proof that every non-antipodal pair has a one-copy seed still needs a separate quantified argument; existing physical L illumination does not supply that implication.
