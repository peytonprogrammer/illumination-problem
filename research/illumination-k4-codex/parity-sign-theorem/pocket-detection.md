# Detecting a sliding triangular pocket

[in progress] Universal detection by an actual source-to-target corner event remains open.
[done] Local, sign-transfer, binary-rank and topological lemmas accepted in tools-disabled Opus reviews, with corrections incorporated.
[done] Two-sided small-slide illumination established in the saved room, using its earlier optical seed and the reviewed affine-image theorem.
[done] Local six-map scattering classification and an odd-word sufficient criterion derived below.

## 1. Scope

Let P be a strictly simple canonical grid-triangle room with distinct interior A marks S,T. Every noncorner integer point is A; in particular, there are no interior B/C points. Keep every wall direction and the rest of P fixed. The pocket has vertices

    B_0=(1,1), A_0=(2,2), C_0=(1,2),

and portal x=1, 1<y<2. Immediately above and below the portal the physical wall also lies on x=1. Move B_0,A_0,C_0 by t u, where u=(0,-1), leaving both marks fixed. Thus the two moving mirror lines are

    D_t: y-x=-t,       H_t: y=2-t.

We seek an admissible event from a chosen source lift to a lift of the ACTUAL physical target T, through exactly one corner at the developed midpoint. The halves have equal displacement w; each avoids other physical corners. The selected intrinsic continuation at the corner bounds an embedded pi-sector. Wall-parallel directions are omitted when applying a physical opening inequality. These requirements cannot be replaced by reaching an arbitrary A point or by an arbitrary broken geodesic.

The global existence assertion has not been proved. The local return-map and single-excursion results do not need the grid or parity hypotheses on the rest of the room. The odd-word criterion only needs its wall reflection linear parts to lie in D4. The raw parity hypotheses matter for the proposed global existence and for the previously proved axis-twist transfer. No existence is inferred from accessibility of the pocket.

## 2. All local return maps

Translate the original pocket by (-1,-1), so its vertices are (0,0),(1,1),(0,1). At t=0 write

    D(x,y)=(y,x),       H(x,y)=(x,2-y).

Eight reflected triangles tile the square [0,2]^2 centered at (1,1). Their outer edges are eight images of the open portal x=0,0<y<1. A legal ray enters at (0,e), 0<e<1, with velocity proportional to (1,m). Until it leaves the pocket, its unfolded development is exactly the straight line through that point in the square. There are no exterior walls of the rest of the room in this local development.

It exits through the bottom, right, or top of the square. The images of the portal on these sides determine the following six return isometries. Words are read chronologically left to right in the physical pocket; the developed map is the displayed composition, with AB meaning A after B. The displayed words specify the isometries, not a unique chronological itinerary; the two four-reflection words represent the same half-turn.

|Developed exit|Slope interval|Portal image G|Linear part R_G|dG_t/dt=(I-R_G)u|
|---|---|---|---|---|
|bottom, 0<x<1|m<-e|D|(x,y)->(y,x)|(1,-1)|
|bottom, 1<x<2|-e<m<-e/2|DH|(x,y)->(-y,x)|(-1,-1)|
|right, 0<y<1|-e/2<m<(1-e)/2|DHD|(x,y)->(-x,y)|(0,0)|
|right, 1<y<2|(1-e)/2<m<(2-e)/2|DHDH|(x,y)->(-x,-y)|(0,-2)|
|top, 1<x<2|(2-e)/2<m<2-e|HDH|(x,y)->(-y,-x)|(-1,-1)|
|top, 0<x<1|m>2-e|HD|(x,y)->(y,-x)|(1,-1)|

Exclude equality cases, which hit a portal endpoint, and exclude m=1-e, which goes through the developed center, a lift of the physical tip A_0. Apart from these cases the straight segment avoids every physical corner lift in the square. Hence every interval, with that deletion, genuinely occurs locally. An individual interval need not have a single literal reflection word across the center-hit exclusion, but its return isometry is as stated.

For any legal fixed local itinerary, translating both mirrors gives

    G_t = tau_(t u) G_0 tau_(-t u).

Its linear part stays R_G and its affine translation derivative is (I-R_G)u. Exactly one of the six maps has zero derivative: DHD, reflection in the unchanged vertical line. For that branch G_t=G_0 exactly. This is the branch used by the continued axis trajectories. The other five maps change to first order.

This is a statement about the developed return map. It does not claim a ray at fixed entry and direction has fixed exit time or exit coordinate; for some branches these vary as well. The return-map derivative is the quantity entering a prescribed developed corner-event equation.

## 3. The exact wall-load identity for the slide

Write each fixed-direction physical reflection as

    F_i,t(x)=R_i x+b_i(t).

All R_i belong to D4. For the two moving pocket mirrors,

    a_D := b_D'(0)=(1,-1),
    a_H := b_H'(0)=(0,-2),

and every other a_i is zero. These follow either from conjugation by tau_(t u), or directly from the equations of D_t,H_t. Number hits j=0,...,n-1, so p is the number strictly before the chosen corner development. Let L_j be the product of the linear reflection parts strictly BEFORE hit j in the development from the source. Composition differentiation gives

    derivative of accumulated affine translation = sum_j L_j a_j.       (1)

Suppose an actual saved or constructed admissible midpoint event has n wall hits in its fixed word, with p hits before its corner c. Its physical corner velocity is v_c=u if c is B_0,A_0,C_0 and zero otherwise. Both actual marks are fixed. With eta=gamma_second-gamma_first, the period defect derivative is

    Q(eta) = sum_(j>=p) L_j a_j
             - sum_(j<p) L_j a_j - 2 L_p v_c.                         (2)

A corner can admit equivalent choices of the coincident split position. The identity uses the prefix matching the chosen labeled corner development. When comparing prefixes, differentiate the corner position too. Formula (2) follows from Q(eta)=T_image'-2 C_image'+S_image'; here S_image'=0. It therefore retains the actual target, the first-half transport and corner motion.

For a corner outside the pocket, group complete pocket excursions. Each contributes its transported vector L(I-R_G)u with a minus sign before the midpoint and a plus sign afterward. This proves a conditional geometric result:

Here a corner outside the pocket means c is not one of B_0,A_0,C_0. The actual interior A marks are outside the closed unit pocket because that triangle and its open portal contain no other integer points.

**Single-excursion criterion.** If an admissible actual S-to-T event has its sole corner outside the pocket, makes exactly one complete excursion into the pocket, and that excursion uses any return map except DHD, then Q(eta) is nonzero. More generally it suffices that all other excursions use DHD.

The proof is immediate from the table and invertibility of L. It applies with the remainder of the room arbitrary. In the D4 setting its nonzero defect is axis- or diagonal-parallel, so an admissible non-wall-parallel w also gives a nonzero scalar opening row. Its sign selects one sign of the slide. The criterion does NOT supply the event.

## 4. A stronger cancellation-resistant parity criterion

Equation (2) is integral. Reduce it coordinatewise modulo 2. Every D4 matrix permutes coordinates and changes signs, so it fixes (1,1) modulo 2. Consequently

    L_j a_D = (1,1) mod 2,
    L_j a_H = (0,0) mod 2,
    2 L_p v_c = (0,0) mod 2.

The sign distinguishing the two halves also disappears modulo 2. Thus, for EVERY admissible midpoint event in this family,

    Q(eta) = (# hits on this moving diagonal D mod 2) (1,1) mod 2.      (3)

In particular:

**Odd-word criterion.** Any admissible actual S-to-T midpoint corner event whose limiting development word contains an ODD number of factors for the pocket's moving diagonal has Q(eta) nonzero (vector detection). It cannot be canceled by other pocket excursions, moving-horizontal-wall hits, transport through the rest of the room, or the motion of its sole corner.

Count every diagonal factor in the chosen limiting development word, including any copy transition through the selected pi-sector at the corner. Such a corner transition is not a legal physical reflection at the vertex. If the corner lies outside the pocket, every counted diagonal factor is an ordinary transverse wall-interior hit. Equivalent coincident split positions must retain the same full development and the corresponding corner derivative in (2); (3) does not authorize arbitrary edits to the word.

For a complete excursion the four bottom/top exit maps in the table have odd diagonal-hit count. The two right-side exit maps have even count. This gives a sufficient condition even when many excursions occur: an odd total number of bottom/top exits in these developed pocket squares guarantees detection, provided the corner lies outside the pocket so every encounter is complete.

Nonzero vector defect alone need not make the ORIGINAL scalar row nonzero: w can be parallel to Q(eta). The axis-shear argument in Section 5 supplies the sign step rather than assuming it.

D-parity is a well-defined character of the local dihedral group: D^2, H^2 and (DH)^4 all have even D count. Equivalently, it records whether R_G swaps the coordinate axes. Thus the odd/even counts assigned to the six maps are independent of their chronological representation.

The converse is false locally: DHDH has even diagonal count but nonzero derivative (0,-2). Even-hit actual events require the full vector sum (2); they are not certified blind by parity.

## 5. Conditional two-sided opening, without an additional sign hypothesis

For the raw parity room, all continued base axis-core periods are constant under this slide. Hence Q(g eta)=Q(eta) for every g in the group generated by the two selected axis shears, as proved in `corner-rigidity.md`. Their shear parameters a,b are positive nonzero integers. Their affine maps fix the physical endpoint labels and preserve the selected intrinsic pi-sector.

Suppose an admissible odd-word event has half-vector w=(p,q), defect v=Q(eta), and side sigma. Both components v_x,v_y are odd integers and therefore nonzero. Under the horizontal shear (x,y)->(x+a n y,y), its event row is

    g_h,n = -sigma [p v_y-q v_x+n a q v_y].

If q is nonzero, this has nonzero slope in n. Arbitrarily large positive and negative integer n produce rows of opposite signs. Only finitely many such powers are wall-parallel. If q=0, p is nonzero; the vertical powers give

    g_v,n = -sigma [p v_y-n b p v_x],

again with nonzero slope. Choose one admissible integer power for each sign. The reviewed local opening proposition then gives a legal actual S-to-T connection for every sufficiently small positive slide and another for every sufficiently small negative slide. The two neighborhoods may have different radii; take their minimum.

Thus existence of ONE actual admissible odd-word seed would prove two-sided local destruction of darkness for this slide. It would not require proving the initial event's scalar determinant nonzero or favorable. This is a conditional consequence, not an event-existence proof. No new powers or optical paths are enumerated here.

More generally, on ANY variation for which Q is zero on the axis-core span, nonzero v suffices without a parity condition. If q v_y or p v_x is nonzero, use the corresponding formula above. If both vanish while w,v are nonzero, the only possibilities are w vertical/v horizontal or w horizontal/v vertical. In the first case one horizontal shear makes p nonzero, then vertical powers give both signs; exchange axes in the second case. At most one preliminary shear is needed. The defect remains v throughout, and the intrinsic side remains sigma. Therefore vector seed detection on an axis-isoperiodic subspace is equivalent to signed separation by their two-shear orbits on that subspace. More precisely, for a linear subspace E of D0 let H_E be its intersection with the actual translation directions. Uniform scaling is not in D0 since the axis cores have nonzero periods. If the common vector-seed kernel on E equals H_E, take a linear complement E_0 to H_E. Compactness of the unit sphere in E_0 extracts a finite positively spanning family of orbit rows. For the independently parameterized fixed-mark pocket slides of Section 7, H_E is zero. This elementary restricted statement does not need the cylinder-mixing spectral argument used for general, non-isoperiodic variations.

For clarity, the finite-family statement gives a uniform geometric neighborhood, not just a different interval for each direction. For each selected fixed word, the developed corner and target images are affine in delta. Its signed area is f_e(delta)=g_e(delta)+O(norm(delta)^2), with a uniform bound for that word. All noncorner crossing and vertex-avoidance conditions persist in a neighborhood; f_e<0 handles the sole corner as in the reviewed opening proposition. On the compact unit sphere, the finite rows have a margin c>0 such that some g_e(delta)<=-c norm(delta). With C the maximum of their quadratic bounds and epsilon the minimum of their legality neighborhoods, choose norm(delta)<min(epsilon,c/(2C)) (omit the second bound if C=0). The corresponding f_e is negative. This proves uniform local opening within E_0.

## 6. Frozen control: one uncanceled two-mirror visit

No new paths are needed to check the criterion against the existing control. Saved event1 has actual physical corner (-1,2), outside the pocket. Its recorded wall word includes exactly one pocket visit, the adjacent walls H,D (wall indices 3,2), before the corner, and no other hit on either pocket mirror. Its prefix transport sends a_HD=(1,-1) to (1,1). Therefore (2) gives

    Q(eta_1)=(-1,-1).

With w=(-12,5) and sigma=+1 its signed opening row is

    -sigma det(w,Q(eta_1))=-17.

This already supplies the odd seed required by Section 5 in THIS saved room. Its previously proved raw-parity and axis-core hypotheses apply. The initial row -17 opens t>0. The known horizontal shear has a=48; its first positive image has half-vector (228,5), unchanged defect (-1,-1), and signed row 223, which opens t<0. Both directions avoid wall parallelism. Thus the two fixed theorem-prescribed events establish illumination for all sufficiently small nonzero t in this literal pocket-slide family. The positive-power image is justified by the reviewed affine-event transfer; no new word or optical replay for that image is claimed, and no explicit uniform interval radius is computed here.

This is a completed restricted opening result, distinct from the earlier three-vertex ear deformation. It does not supply an event in an arbitrary room.

Saved event0 has no hits on either pocket mirror, and its physical corner is outside the pocket. Equation (2) gives zero, agreeing with its whole two-axis-shear orbit being blind.

The checker reconstructs both fixed affine developments directly from their physical wall reflections, compares them with the frozen corner/target forms, and evaluates (2) and (3). It performs no direction, word, ray or room search, and does not claim new optical validation of these previously audited events.

## 7. Several independent pockets: a finite-field sufficient condition

Suppose k disjoint pockets have independent legal unit slide parameters t_r, and both marks stay fixed. Their moving diagonal walls are distinct; no maximal wall or moving vertex is shared. D4 images of the pocket are allowed. The outer axis-wall derivatives remain even, and each diagonal-wall derivative has both coordinates odd. For any supplied admissible event e, (3) applies to each parameter:

    partial Q_x(eta_e) / partial t_r = B_er mod 2,
    B_er = number of factors on moving diagonal r, modulo 2.

The corner-motion term is still even. If a finite packet of actual events has rank k for B over F_2, a k-by-k minor of the integer x-defect matrix is odd. That minor is nonzero over the reals, so these event defects detect every nonzero real combination of these k pocket slides.

Assume, as required for the transfer, that each slide fixes the continued base axis periods in the k-pocket room. The local fixed DHD branch or its D4 image supplies the same reason as in the single-pocket argument. Then Section 5 converts this conditional vector injectivity into signed separation and a finite positively spanning orbit family on the k-dimensional slide subspace. This is a sufficient independence criterion. It neither supplies the events nor classifies the full axis-isoperiodic kernel as pocket slides. Failure of the binary rank test does not imply failure of real detection.

## 8. A topological bit is available; straight event realization is the gap

Let D_hat be the union of the lifts of this one moving diagonal wall in the eight-copy unfolding X. At both endpoints B_0,A_0, the adjacent mirror linear parts generate D4, so all eight sectors meet in one lift of that physical corner. Exactly four diagonal seam arcs meet there. Thus D_hat is a closed one-chain modulo2, and crossing it defines a character on closed paths. For a corner event, push its midpoint through the chosen pi-sector; its crossing count is precisely the diagonal-factor count in Section 4.

There is an elementary dichotomy.

*If this is the only physical diagonal wall*, colour copy g by 0 when g preserves the two coordinate-axis directions individually, and 1 when it swaps them. Axis-wall crossings preserve the colour; crossing this D wall changes it. Hence D_hat is the boundary modulo2 of the union of colour-0 copies. The bit of a path is determined by the colours of its endpoint copies. An odd actual S-to-T event would have to reach one of the four coordinate-swapped copies of T.

*If another physical diagonal wall E exists*, its reflection linear part is either R_D or -R_D. In the first case the prescribed copy crossing sequence D,E returns to the original copy. In the second case D,E,H,V returns, where H is the pocket horizontal mirror and V is an available vertical wall of the attachment. Indeed R_D R_E is respectively I or -I, and R_H R_V=-I. Choose crossing points in the open walls, connect them by arbitrary interior paths in the successive copies, then return to the starting point in its copy. This is a closed topological path crossing D_hat exactly once, so D_hat is nonzero in homology modulo2. These interior connecting paths exist because P is a connected disk; they are NOT asserted straight billiard paths.

In either case an odd continuous source-to-actual-target path exists. In the first case choose a swapped target copy; X is connected since R_D,R_H generate D4. In the second case append the odd closed path to any path to any chosen target lift if needed. Thus ordinary topological connectivity is not the missing obstruction. Replacing these paths by a straight midpoint connection through only one legal corner is an additional theorem and remains open.

## 9. The remaining global question

The odd-word criterion reduces one sufficient route to a precise endpoint question: can one construct a legal midpoint corner continuation from actual S to actual T whose word toggles a bit an odd number of times at this one diagonal wall? Toggle no bit at any other wall.

Connectivity of the fan tree does not answer that question. It supplies combinatorial routes to a pocket, but those routes need not be straight, need not put the sole corner at half-time, and need not return to the target's physical label. Likewise, generic rays can use the five moving return maps without giving any corner event for the chosen pair. Existence of an odd-hit event would prove the local detection lemma; failure to find one would not disprove it, because even-hit events can detect too.

The selected two axis multitwists cannot fix this existence gap: on the pocket slide Q vanishes on all their core increments, so they preserve Q(eta) on every seed orbit. A proof must construct a new seed, use a genuinely different action with a justified effect, or supply a structural counterexample. No universal detection or counterexample in the required polygon class is claimed here.

### 9.1 A precise non-axis transfer mechanism, conditional on a seed

The theory-only existence review57928 supplies no universal seed or
counterexample. Its useful remaining proposal can be stated without
assuming that every affine map preserves the particular slide defect.
Let e be an already supplied actual S/T one-corner event and eta its
zero-holonomy relative class. Let phi be a pure multitwist, after a power
fixing all physical-corner lifts, actual endpoint lifts and selected
prongs. Refine its periodic cylinders at the closed leaves through EVERY
actual regular marked endpoint and regular physical corner lift; singular
corner separatrices already lie on cylinder boundaries. Choose a further
power fixing these refined boundary leaves pointwise. This refinement is
necessary for the relative formula (Section9.2). Its pairwise disjoint
parallel refined-cylinder cores are c_i, and the signed twist powers are m_i. Fix the intersection convention so that

    phi_* eta = eta + N eta,
    N eta = sum_i m_i <c_i,eta> c_i.

The correction N eta is ABSOLUTE, even though eta is relative, and N^2=0
because the cores are disjoint. Hence for every integer n,

    phi_*^n eta = eta + n N eta,
    Q(phi_*^n eta)=Q(eta)+n Q(N eta).

Also hol(N eta)=0: both eta and phi_*eta have zero holonomy, since an
affine image of the original event has zero holonomy. Thus the needed
increment tests Q on a specific absolute zero-period cycle, not on an
arbitrary core independently.

If Q(N eta)!=0, at most one integer n makes the vector on the last line
zero. The images remain admissible actual endpoint events by the fixed
labels and prongs. A nonzero increment implies w is not parallel to the
multitwist cores: a parallel event avoids all interior core circles and
has every displayed intersection zero. Therefore only finitely many
powers give wall-parallel image directions. Choose a power avoiding
these exceptions and a possible zero vector. Section5 then supplies both
opening signs using the original axis shears.

This is a sufficient mechanism for obtaining detection even from a blind
seed Q(eta)=0. It does not manufacture a seed. Nor does the existence of
SOME absolute zero-period cycle detected by Q imply that one of these
special increments N eta is detected. Two exact obligations remain:
(1) a genuine actual S/T one-corner seed; (2) a pure non-axis multitwist
with Q(N eta)!=0, unless the seed already detects. No such new event,
cylinder or twist is discovered here.

### 9.2 Marked-cylinder correction and an exact non-axis flux criterion

**Status: accepted by independent tools-disabled Opus review (exit0),
with its relative-pairing and refinement corrections incorporated.** This section supplies
necessary conditions and an absolute-homology equivalence for the proposed
non-axis transfer. It does NOT construct an actual endpoint event.

First refine the cylinder decomposition at every closed leaf through an
actual regular mark, including regular physical corner lifts. Cone-point
separatrices already lie on cylinder boundaries. At an arithmetic base
the transverse heights are rational multiples of a common unit and the
cylinder moduli are commensurable; the heights need not be rational real
numbers in Euclidean unit normalization. After a
common power of the parabolic, each refined boundary leaf is fixed
pointwise and each open strip is an integral Dehn twist relative to its
boundary. The formula in Section9.1 then holds in ordinary marked relative
homology, with intersection numbers taken against these refined cores.
The refinement adds no singularity and does not alter the surface. Every
point in the support of boundary(eta) lies on the refined boundaries.
For relative eta the core in <c_i,eta> is fixed in H_1(X minus P), where P
is the finite marked set; use its Lefschetz pairing with H_1(X,P). Its
image in ordinary absolute homology is used for C, hol and Q below.

Fixing interior marks after taking a power is insufficient to justify the
UNREFINED relative formula. On the unit square torus, the affine shear
(x,y)->(x+2y,y) fixes marks s=(0,0),t=(0,1/2). A vertical marked arc s->t
acquires one horizontal core cycle. The unrefined annulus has twist number2,
so an unrefined core below t pairs to1 and predicts2cycles, while one
above t pairs to0 and predicts0. The unrefined relative prescription is
ill-defined and neither choice gives the correct one-cycle increment. Cutting
at the two marked horizontal leaves gives two strips of twist number1;
the arc crosses just one. This is a prescribed relative-homology control,
not a mirror room or a counterexample to the goal.

Work now in absolute H=H_1(X;R). Orient the r refined core classes c_i in
a common unit direction e and write

    hol(c_i)=ell_i e,   ell_i>0,
    C=span_R{c_i},      Z=C intersect ker hol.

Let a!=0 be the signed shear coefficient and h_i>0 the refined heights.
The twist coefficients satisfy m_i=a h_i/ell_i, so all m_i have the same
sign. Write Nx=sum_i m_i <c_i,x> c_i, using the convention of Section9.1.
Then the following exact identity holds:

    N(ker hol in H) = Z.                              (9.2a)

Proof of surjectivity onto C first. Choose coordinates on H and let T have
columns c_i. Nondegeneracy of the intersection form identifies x-><.,x>
with an invertible map H->H*. Therefore rank N equals rank(T M T^t), where
M=diag(m_i). Since M is positive or negative definite, this rank equals
rank T: after multiplying by the common sign, the kernel of T M T^t is
exactly ker T^t. Hence im N=C, even if the listed cores are dependent.

Affine holonomy covariance gives

    hol(Nx)=(A-I)hol(x)=a hol_perp(x) e.

Certainly N(ker hol) is contained in Z. Conversely take z in Z and choose
x with Nx=z using im N=C. The displayed covariance forces hol_perp(x)=0.
Choose any core c_0. Since Nc_0=0 and ell_0>0, subtracting
hol_parallel(x)c_0/ell_0 from x preserves Nx and makes both holonomy
components zero. This proves (9.2a). If the data are rational, all these
choices can be made over Q. Clearing denominators gives an integral
preimage of a MULTIPLE of z, not necessarily of z itself. Thus the
integral image has finite index in the integral zero-holonomy core
lattice. Since absolute cycles are also relative cycles, (9.2a) also holds
with the relative holonomy kernel on the left. Neither statement makes
the preimage an actual corner event.

For the pocket-slide functional Q:H->R^2, (9.2a) yields

    QN is nonzero on ker hol
      iff Q is nonzero on Z
      iff the vectors Q(c_i)/ell_i are not all equal. (9.2b)

For the last equivalence, hol|C has one-dimensional image. Q vanishes on
its kernel exactly when it factors through that one-dimensional image,
i.e. Q(c_i)=ell_i v for a common v. Explicitly, unequal ratios at i,j give
z=ell_j c_i-ell_i c_j in Z with Q(z)!=0. The surjectivity proof supplies
an absolute zero-holonomy preimage under N.

For a SUPPLIED actual event eta, let k_i=<c_i,eta>. The corresponding
calculation is more restrictive:

    sum_i h_i k_i=0,
    Q(N eta)=a sum_i h_i k_i [Q(c_i)/ell_i].           (9.2c)

Thus unequal normalized flux is necessary for this twist to change an
actual zero-holonomy event, but it is not sufficient for a particular
eta or for the existence of any actual event. Equation(9.2a) produces
arbitrary absolute cycles; it does not prove that actual S/T event classes
span them, or that their intersection vectors realize the required k_i.

Two exclusions follow without computing a direction or trajectory.

1. If C has dimension1, then Z=0 and this parabolic fixes EVERY zero-holonomy
   relative class, not merely its defect. In particular, a direction with
   one maximal unmarked cylinder cannot help: splitting it at marks gives
   homologous oriented cores and still dim C=1. Several cylinders with
   homologous cores have the same obstruction. Since every affine map
   preserves ker hol, the group generated by ALL such one-core-span
   parabolics at this base fixes ker hol pointwise, even when their
   directions differ. Their products cannot change a blind event either.
2. Let G be the group generated by the established slide-blind axis twists,
   so Q(gx)=Q(x) on marked relative homology for every g in G. A conjugate
   g phi g^-1 of another Q-preserving twist still preserves Q. In particular
   a conjugated axis twist supplies no new detection. To cover any other
   pure twist in that same direction, use discreteness of the Veech group:
   their derivatives have equal nonzero powers. Both maps fix the actual
   regular source lift, so their equal-derivative powers differ by a
   translation automorphism fixing a regular point, hence are equal.
   Since powers act as I+nN, blindness of a nonzero power implies blindness
   of the original twist. Thus these non-axis slopes in the axis cusp orbits
   supply no new detection;
   it is not a statement about every non-axis direction or the full affine
   group.

There is already a definite detected ABSOLUTE zero-holonomy cycle; its
existence need not be assumed. If Q vanished on the entire absolute
holonomy kernel it would factor as L composed with hol. Q vanishes on
horizontal and vertical core classes whose periods span R^2, forcing L=0,
contrary to the established nonzero absolute slide period. More explicitly,
Section17 supplies a cycle C with period(p,q+2t), where p,q are even
integers, while fixed cycles A,B have periods(-2,0),(0,-2). Use the same
side-crossing topological loop in the persistent copy cellulation for small
t: interior connecting arcs can be transported continuously, so this C
is locally constant in the homology chart. Then

    z=C+(p/2)A+(q/2)B,   hol_0(z)=0,   Q(z)=(0,2).

In the SAVED control p=-2,q=-4, this is z=C-A-2B; those two numerical
values are not asserted for every room.

These are previously supplied cycles, not a newly found optical word.
No prescribed multitwist or actual event is proved to realize z.

The remaining geometric target is consequently sharper: find a legal
actual S/T event with a nonzero pairing against a multi-cylinder contrast,
or prove it already detects directly. A detected absolute cycle, unequal
normalized cylinder flux, a non-axis slope, or group transitivity alone
is not that event. Universal existence and the96bounded portal implications
remain open.

### 9.3 Actual-event occupancy and the unimodular strip criterion

**Status: accepted by tools-disabled Opus review (exit0), after the
relative-pairing, sign and blind-seed scope corrections below.** Retain a
SUPPLIED legal actual S/T one-corner event, with primitive equal half-vector
w and class eta=(p->s)+(p->t), whose two summands have holonomies -w,+w.
Let Q be the pocket-slide functional on ordinary H_1(X,P), with values
in R^2, and use its restriction on absolute cycles. Fix a nonparallel
rational cylinder direction e of unit length. Let phi be a pure multitwist
with nonzero signed shear coefficient a, refining at all
marked endpoint levels as in Section9.2. For a maximal cylinder D, put

    r_D=Q(c_D)/ell_D,
    lambda_D^X=fraction of the half p->X inside D, X=s,t.

Orient the core c_D along e and choose the intersection convention so
upward transverse crossings of that core are positive, matching the
convention that positive a moves higher transverse points in the +e
direction. Because the halves
are not parallel to e, boundary contacts occupy zero parameter length,
and sum_D lambda_D^s=sum_D lambda_D^t=1. Group the refined-strip formula
by maximal cylinder. A net k_i signed crossings of strip i contribute
h_i k_i to transverse displacement. A single upward crossing adds
m_i c_i, with m_i=a h_i/ell_i, and hence defect a h_i r_D. Refined
cores inside D are homologous in ordinary H_1(X), though their punctured
classes can differ by peripheral loops around marks. Those loops die
before evaluating Q, so Q(c_i)/ell_i=r_D within D.
The two halves have constant transverse velocities -det(e,w),+det(e,w)
in normalized parameter0..1. Therefore

    Q((phi_*-I)eta)
      = a det(e,w) sum_D r_D (lambda_D^t-lambda_D^s). (9.3a)

No absolute value or unstated sign choice is used in this convention.
A pure twist changes only the coordinate parallel to e; it preserves
transverse coordinates and cylinder membership, so these occupancies
are invariant under that same twist. This also agrees with N^2=0.

There is a particularly sharp version when det(w,v)=1 for a primitive
integer vector v and e=v/|v|. Use the base torus map pi:X_0->R^2/Z^2
provided by the integer developing charts. Every physical corner and
actual A mark maps to0. Refine at ALL points of pi^-1(0), including any
auxiliary regular points, and their complete v-leaves. If the marked set
is enlarged for this punctured intersection pairing, eta is included in
the larger relative group. Only its absolute twist increment is evaluated
by Q, so no velocity or extension of Q for auxiliary endpoints is assumed.
The complement of
the closed torus v-geodesic through0 is an open cylinder of height1/|v|.
Its preimages are unbranched annulus covers, each of the same height and
with circumference n_D |v| for an integer n_D>0. These are refined strips
inside the maximal v-cylinders; no new trajectory is selected here.

Along either open half of the supplied event, the torus transverse
coordinate runs strictly between two successive integer levels because
|det(v,w)|=1. It never crosses the removed v-leaf in its interior.
Consequently each open half lies in ONE refined strip and hence in one
maximal cylinder, denoted D_s,D_t. Formula(9.3a) becomes

    Q((phi_*-I)eta)=a det(v,w)/|v| (r_Dt-r_Ds).       (9.3b)

Thus the supplied event's defect CHANGES under this nonzero twist iff the
two containing maximal cylinders have unequal normalized slide flux. If
Q(eta)=0, this is exactly when the image event becomes detecting.
Finding those maximal cylinders is GLOBAL gluing information; the last
statement is not a local visibility proof. Nor does it supply a seed.
The regular-midpoint exclusion already established in Section26 applies;
no new regular-corner existence argument is being assumed.

### 9.4 Finite residue reduction of all unimodular transfer directions

**Status: accepted by tools-disabled Opus review (exit0), with the
pure-twist, fixed-source and integral-lift qualifications below.** This is a
finite algebraic criterion for transferring a SUPPLIED blind event. It
is not a finite search run and does not supply an actual S/T seed.

Assume Q(eta)=0; otherwise the seed already detects. Choose a symbolic
Bezout partner v_0 with det(w,v_0)=1. Every integer v with det(w,v)=1 is
v_0+jw for a unique integer j. Unoriented directions with determinant-1
are represented by reversing v, so no additional case is needed.

All rational directions of this arithmetic base admit pure affine
multitwists fixing pi^-1(0) pointwise: in the annulus-cover decomposition
of Section9.3, choose a common multiple L of the finitely many n_D and
use derivative z->z+L det(v,z)v. Each strip twists an integral number of
times and its boundary is fixed pointwise; the maps glue to an affine
map of X. Pointwise fixation of the origin-fibre graph gives the actual
endpoint/corner-label and sector properties required here. No additional
immersed orbit-closure branch condition is used. For direction w choose
such a map g, with derivative

    A_w z=z+K det(w,z)w,    K a positive integer,
    g_*=I+N_w,             N_w^2=0.

The entire event lies in the preimage of the closed w-geodesic through0.
The chosen g fixes that boundary graph pointwise, including both halves,
so g_*eta=eta. This is a geometric fixed-path statement, not an inference
from hol(eta)=0 alone. In particular N_w eta=0.

For each SYMBOLIC residue j=0,...,K-1 let v_j=v_0+jw and choose one pure
twist tau_j in direction v_j, BUILT BY THIS TORUS-LIFT CONSTRUCTION. Put

    z_j=(tau_j*-I)eta,
    b_j=Q(z_j),       d_j=Q(N_w z_j).

The z_j and N_w z_j are absolute zero-holonomy classes. Do not infer that
every absolute zero-holonomy cycle has this form. Define the conjugate
phi_j,n=g^n tau_j g^-n, in direction v_j+nK w. Since g fixes eta and
N_w^2=0, for EVERY integer n,

    (phi_j,n*-I)eta = g_*^n z_j = z_j+n N_w z_j,
    Q(phi_j,n*eta)=b_j+n d_j.                      (9.4a)

Consequently some pure twist in a det(w,v)=1 direction turns this blind
seed into a detecting event iff at least one of the FINITELY MANY vector
pairs (b_j,d_j) is nonzero. For necessity for arbitrary pure twists in a
residue direction, apply the same-direction commensurability argument of
Section9.2: both pure twists fix the actual regular source lift. After
nonzero powers they agree, and taking a power multiplies the increment
by a nonzero integer. Q takes values in torsion-free R^2, so vanishing
of an increment is equivalent to vanishing of that multiple.
This criterion concerns all unimodular directions relative to THIS w;
it does not classify every rational direction or every actual seed.
The equivalence excludes non-pure parabolics, maps with finite cylinder
or label permutations, and products of twists in different directions.

If b_j or d_j is nonzero, at most one integer n kills its defect. Also
write the derivative of tau_j as

    A_j z=z+L_j det(v_j,z)v_j,   L_j a nonzero integer.

The image half-vector of the actual event under phi_j,n is

    A_w^n A_j w=(1-n K L_j)w-L_j v_j.              (9.4b)

It is nonzero and for a fixed wall-direction line at most one integer n
makes it parallel to that line: w and v_j are independent. The canonical
room has at most FOUR unoriented wall directions. Thus among ANY SIX
distinct integer n, at least one gives a non-wall-parallel detecting
actual event, retaining the supplied endpoints and legal intrinsic pi
sector by the reviewed affine-event theorem. The six-image bound is a
conditional symbolic guarantee; no image directions or words are generated
or traced in this work. Axis sign transfer then gives both slide signs.

This reduces the proposed infinite family of near-event directions to
2K vector coefficient tests and six images after a successful test. It
leaves two exact obligations: obtain an actual S/T event, and prove some
(b_j,d_j)!=0 for it (or prove direct Q(eta)!=0). The known detected absolute
cycle and rank>=3 tangent bound establish neither. Section9.5 gives a bound on K as a function of the cover degree; it is
not an absolute bound independent of room size.

### 9.5 A common twist coefficient bounded by the cover degree

**Status: accepted by independent tools-disabled Opus review (exit0),
with derivative-versus-chart wording corrected below.** In the raw
canonical base made of N triangles of area1/2, the eight-copy surface X
has area4N. Its integer-chart map to R^2/Z^2 is a branched translation
cover of degree d=4N, ramified only over0. Define

    K(d)=lcm(1,2,...,d).

For ANY primitive integer v, remove the entire inverse image of the closed
torus v-geodesic through0. The remaining components D_i are connected
unbranched finite covers of its open cylinder. If their degrees are n_i,
then sum_i n_i=d, each n_i<=d, their heights are1/|v|, and their
circumferences are n_i |v|. On each D_i use the shear of coefficient

    a=K(d)|v|^2,    twist number m_i=K(d)/n_i.

At the bottom boundary its displacement is0, and at the top it is
K(d)|v|, an integer multiple of that component's circumference. Thus
each completed boundary leaf is fixed pointwise. These maps extend as
identity on the removed graph and glue to an affine homeomorphism of X
with the SAME derivative in every chart. Denote this surface map Phi_v
and the corresponding linear torus map f_v. Precisely,

    D Phi_v = M_v = I+K(d) v det(v,.),
    pi composed Phi_v = f_v composed pi,
    Phi_v|pi^-1(gamma_v) = identity.                (9.5)

In arbitrary local charts the affine formula also has a chart-dependent
translation term. The displayed linear matrix is the derivative, not a
pointwise formula with translation0 in every chart.

Across an ordinary graph edge the two affine formulas agree on the edge
and have identical derivative, so they give one affine formula locally.
At a zero they extend continuously, preserve each incident v-sector and
are affine on its punctured sectors. The inverse uses -a; this proves
bijectivity as well. No base room symmetry or extra point permutation
is assumed. The construction fixes the entire fibre pi^-1(0), including
all actual marks/corner labels and the v-prong graph.

Accordingly Section9.4 may take K=K(d) and L_j=K(d) for all residues,
without any geometric direction computation. These maps already have
the endpoint and sector properties needed by the affine-event theorem;
no claim that they fix a chosen immersed orbit-closure branch is needed.
The finite transfer criterion has at most2K(d) vector coefficient tests
per supplied seed, followed by six images after a successful coefficient
pair. The size is deliberately crude; it is not a practical algorithm or
a bound independent of N. For a particular direction the exact minimal coefficient for a lift fixing
the ENTIRE graph pointwise is lcm_i n_i: fixing a bottom boundary forces
the shear translation there to0 modulo the component circumference,
and its top boundary is fixed iff n_i divides the integer coefficient.
This uses the annulus gluing argument, not merely fixation of its vertex
labels. No such decomposition or smaller coefficient is computed here.

This corollary does NOT prove that one coefficient pair is nonzero, does
not construct the supplied actual event, and does not permit replacing
that event by an arbitrary zero-holonomy cycle. No directions or optical
words have been enumerated or searched.

## Review status and resolutions

The first focused tools-disabled Opus review accepted the six-map classification, complete exception list, transported-load formula and mod2 identity. It requested clearer zero-based indexing, chronological composition, copy-sector factors and geometry-binding assertions; these are incorporated. It also distinguished vector detection from the original scalar opening row. Section 5 now supplies a separate two-shear argument for both signs, including the axis exceptions.

A separate global-existence analysis independently derived the same mod2 identity but found neither a proof nor a counterexample. Its unproved broader claims are not imported. In particular, excluding convex 45/90 corners does not by itself exclude convex 135-degree B corners, and a physical 45-degree wedge must not be confused with its unfolded pi-sector. The topological lemma in Section 8 has its own copy-colour proof above. The focused follow-up review accepts Sections 5,7,8; its requests for explicit nonzero shears, a named symmetry quotient, a uniform multi-parameter opening estimate and the completed saved-room consequence are incorporated. No separate numerical execution by a reviewer is claimed. The reviewer also retracts its earlier physical-wedge/pi-sector claim. Closedness of D_hat controls homotopies around a full cone; it must not be read as permission to change an event's outgoing prong or selected legal pi-sector.

### 9.6 Mixed coefficients and the limit of axis preconditioning

**Status: algebra, formal control and finite-generator closure accepted by
focused tools-disabled Opus review, with conjugacy and equal-half scope
corrections incorporated.** Let eta be a SUPPLIED actual event, of equal
primitive developed halves, so hol(eta)=0. Let h=I+H be a supplied pure
axis twist and f=I+N a supplied pure affine twist, both fixing the actual
endpoint/corner labels and selected prongs. With H^2=N^2=0 and the
established QH=0 on the marked relative group, a blind seed satisfies

    Q(f^a h^b eta)=a[Q(Neta)+b Q(NHeta)],            (9.6a)

for all integers a,b. All increments are absolute and have zero holonomy:
for example hol(NHeta)=(D_f-I)(D_h-I)hol(eta)=0. The composite group
actions, including inverses, preserve actual event admissibility. A nonzero
right side gives an actual detecting image; Section5 supplies non-wall
parallelism and both opening signs if necessary. If Q(NHeta)!=0, fixing
a=1 excludes at most one b. Under Q(Neta)=0, every nonzero b detects.
This is a conditional mixed-coefficient criterion, not a proof that the
coefficient is nonzero in any new room.

The order is essential: h is applied FIRST. But axis preconditioning is
not a genuinely new depth beyond all-direction first-stage tests. Since
Qh^(-b)=Q,

    Q(N h^b eta)=Q(h^(-b) N h^b eta).               (9.6b)

The conjugate is a pure twist in direction D_h^(-b)v if f has direction v.
For the torus-leaf construction it fixes that conjugated leaf graph
pointwise. Any equal-derivative translation ambiguity is removed by
fixation of an actual regular source point. Thus blindness of EVERY
rational-direction pure twist on eta would force Q(NHeta)=0 too.
Q-preserving letters in a longer word can similarly be moved to the left
by conjugation, and then drop out of Q.

This still extends the finite family of9.4, which covers ONLY
|det(w,v)|=1. For a horizontal shear of coefficient K and v=(r,s),

    det(w,D_h^(-b)v)=det(w,v)+b K w_y s.             (9.6c)

For the bounded seed w=(2,1),v=(1,1), it is1+bK, generally outside that
unimodular family. This symbolic relation is not a direction search.
If all rational first-stage contrasts really vanish, a higher-depth
attempt must instead use two non-Q-preserving twists or a longer product.
Neither universal vanishing nor a universal successful product is proved.

The prescribed formal seven-dimensional split-relative control in
pocket-seed-module.py has a six-dimensional symplectic absolute block
and one fixed relative boundary generator. Its two operators come from
positive isotropic core pairs, factor correctly through parabolic
holonomy actions, and satisfy QH=Qeta=QNeta=0 yet QNHeta=(-4,0).
The conjugate already detects, with determinant3 relative to w=(2,1).
It is explicitly NOT an actual surface, mirror room or event realization.
It rules out the single-direction algebraic shortcut only. Seven fixed
integer-power controls and the exact closure dimensions1,2,3,3 pass.

Finally, for any FINITE SUPPLIED set f_i=I+N_i on E=H_1(X,P;R), with
D=dim E, define V_0=span{eta}, V_(j+1)=V_j+sum_i N_i V_j. Its stable
space is exactly the supplied subgroup's actual orbit span: N_i=f_i-I,
and f_i^(-1)=I-N_i. Stability occurs by depth D-1 for nonzero eta.
If Q does not annihilate the stable space, a product of at most D-1
operators N_i has nonzero Q on eta. Expanding it as a signed sum of
actual group subwords makes at least one such actual image detecting.
If Q kills that stable space, the entire SUPPLIED subgroup is blind.
No chosen finite generator collection is asserted to generate all pure
affine maps or all actual detecting events. An abstract detected cycle
outside this orbit module does not satisfy the criterion.


## 10. The pocket forces the full base absolute-period lattice

At the raw grid base, every physical mirror has an even integral affine translation. Axis mirrors x=k,y=k contribute 2k in their normal coordinate; diagonal mirrors x+y=d or y-x=d have even d because they follow canonical A-B edges. Consequently every closed developed period belongs to 2Z^2.

Let V_1 be an actual vertical wall of the straight attachment. The already-proved pocket identity gives

    V_1 D_0 H_2 D_0 = V_1 V_2 = translation(-2,0).

Its linear copy label is the identity. This prescribed wall-crossing sequence can be realized by a continuous closed path in X: cross at open wall points and connect consecutive crossings through interiors of copies, then return to the starting point in the original copy. No straight billiard realization is asserted. Conjugating the sequence by D_0 gives period (0,-2). Thus the full absolute-period lattice is EXACTLY 2Z^2. Both displayed periods remain constant during the pocket slide. This does not say that the full period lattice stays equal to 2Z^2 off the grid: other absolute periods can acquire nonintegral derivatives. The even-offset assertion is a general consequence of canonical A-B walls; the numerical control checks it only on the frozen room.

This excludes a larger torus-lattice obstruction, but not a nontrivial branched intermediate cover. In particular it does not imply primitive action of the sheet permutations.

Here is an explicit algebraic warning. The six-square origami with zero-based permutation images

    r=(0,1,5,4,2,3),    u=(2,3,0,1,4,5)

is a connected unramified double cover of the three-square L, via square i mapping to floor(i/2). Its three two-element blocks are invariant. Nevertheless r fixes square0 and u fixes square4, giving absolute periods (1,0),(0,1), so its full period lattice is Z^2. Its two commutator cycles have length3; the base has one length3 cycle. These give genera3 and2 and show the intermediate cover is unramified. This is not a raw-room counterexample. It disproves the shortcut from full period lattice to primitive permutation action.

Terminology varies between authors, so this note uses the explicit properties. The distinction between monodromy primitivity and period data is discussed in [Shrestha, Sections1.2 and2](https://www.numdam.org/item/10.5802/ambp.392.pdf). The examples here are independently specified and verified finite controls.

## 11. A genuine obstruction outside the room class

The following marked translation surface shows that full lattice and odd ramification alone cannot ensure an admissible midpoint event between every two regular A points.

Let G=SL(2,F_7), and define

    r = [[1,1],[0,1]],   u = [[1,0],[2,1]],   z=-I.

The elementary matrices r,u generate G of order336. Their commutator has order3. Let E=R^2/2Z^2, with B=(1,1), and take the connected regular cover Y->E branched only at B specified by monodromy r,u for horizontal and vertical torus generators based at0. The branch order is3 and g(Y)=113. Mark every preimage of the three nonzero two-torsion points as forbidden; these are the B/C points. All points above0 are regular A points. Choose source s above0 with sheet label1 and target t with sheet labelz.

The group is perfect, and its period lattice is full. This can be proved without a search over primitive words. Put d=diag(2,4). Direct matrix calculation gives

    [d,r^5]=r,     [d,u]=u.

Thus both generators lie in the commutator subgroup. In the punctured-torus group F_2=<a,b>, choose any word delta mapping to d. The kernel contains

    a [delta,a^5]^-1,    b [delta,b]^-1,

whose exponent vectors are respectively (1,0),(0,1). Therefore the compact cover has full absolute lattice 2Z^2. The loop fillings at its branch points have zero torus displacement and do not change that conclusion.

**No admissible one-corner midpoint event connects s to t.** Any such event has integral half-displacement w. If w=k w_0 with k>=2 and w_0 primitive, it meets a forbidden B/C point already at displacement w_0, before its midpoint. Hence w must be primitive.

Its projected full chord on E is then the simple essential closed torus curve 0->2w. If its midpoint is B, push it through the selected embedded pi-sector: its projection makes a small semicircular detour around B. If its midpoint is one of the C points, no B detour is needed. In both cases the resulting loop on E minus B is still a simple essential nonseparating loop. It therefore represents a primitive element of F_2 (up to conjugacy, which preserves primitivity).

The image of a primitive element under a surjection F_2->G can be completed by one other element to a generating pair of G. It cannot equal z: z is nontrivial and central, so z and ANY one other element generate an abelian subgroup. G is nonabelian. Thus the selected pi-sector lift cannot end at t, a contradiction. The embedded pi-sector hypothesis is essential here. At a 6pi cone a continuation through 3pi can project to a semicircle plus a full peripheral turn; it need not represent a primitive word and is excluded from this event definition.

This proof retains the actual target label. It rules out every primitive direction by a group argument, not by enumeration. The construction is an arithmetic marked translation-surface control, NOT asserted to be a simple polygonal room or to possess the required literal pocket. It is not a counterexample to the active goal. It shows why an all-cover realization theorem would be false.

## 12. The disk gives a low-degree sphere quotient

A polygonal disk with wall directions in the four D4 directions has a stronger property than an arbitrary arithmetic cover. Its eight-copy unfolding X has a holomorphic order4 rotation action, induced by left multiplication of its copy labels by the quarter turn. The quotient X/C4 consists of two copies of P, distinguished by orientation, glued along their complete boundary. It is the double of a disk, hence a sphere. Thus X admits a degree4 holomorphic map to P^1, and its complex gonality is at most4. The pocket ensures the eight-copy unfolding is connected.

Gonality means the least degree of a nonconstant meromorphic function. It cannot increase under a finite map X->Y. Here is the norm proof, to fix the direction of the implication. If f on X has pole divisor D of degree k, the coefficients of its characteristic polynomial over C(Y) have poles bounded by the pushforward of D, of the same degree k. At least one coefficient is nonconstant, or f would be algebraic over C and hence constant. That coefficient gives a function of degree at most k on Y. Therefore EVERY holomorphic curve covered by this X has gonality at most4, even if the covering is not equivariant for C4.

This monotonicity and the Castelnuovo-Severi inequality used below are standard curve facts; see [Orlic, Proposition2.0.2 and the Castelnuovo-Severi section](https://web.math.pmf.unizg.hr/~petorli/index_files/Doctoral_dissertation.pdf). The disk-double argument and the application to our specific control are given explicitly here.

## 13. The perfect-central control cannot hide as an intermediate quotient

There is a short obstruction that excludes not just Y itself, but any translation cover of Y as the unfolding of a room in this class.

Consider a regular cover Y->E with perfect deck group G of order n, branched over exactly one torus point with common ramification order m. Suppose

    genus(Y)>9,      n/m>8.

Then Y has gonality greater than4.

First suppose a degree k<=4 pencil is unique (all degree-k maps differ by an automorphism of P^1). The deck group G then preserves it and acts on P^1. Its ramification divisor R_f is G-invariant. Every G-orbit on Y has length either n (away from the branch fiber) or n/m (in that fiber). Therefore n/m divides degree(R_f). Riemann-Hurwitz for Y->E and f:Y->P^1 gives

    degree(R_f)=2g(Y)-2+2k = n(1-1/m)+2k.

It follows that n/m divides 2k. This is impossible since 0<2k<=8<n/m. No classification of finite subgroups of PGL2 is needed.

It remains to justify that a low-degree pencil is unique, or handle its only exception. Degree2 is unique at genus>1, and degree3 is unique at genus>4 by Castelnuovo-Severi. For degree4, two distinct pencils either jointly generate C(Y), giving genus<=9, or have a common factor of degree2. In the latter case the intermediate curve has two independent degree2 maps to P^1 and therefore genus at most1. A genus0 intermediate would make Y hyperelliptic, already excluded. The only remaining possibility is a degree2 map Y->E' with E' elliptic.

At genus>5 this bielliptic involution is unique: two distinct degree2 elliptic maps would, by Castelnuovo-Severi, give genus<=5. Hence G acts on E'. Every finite subgroup of Aut(E') is an extension of an abelian translation group by a cyclic group, and is solvable. A perfect group has trivial image in a solvable group. Thus every element of G would be a deck transformation of a degree2 map, forcing |G|<=2, impossible here. This excludes the degree4 exception and proves the claim.

For the control in Section11, n=336,m=3,genus113 and n/m=112. It therefore has gonality>4. Section12 rules out ANY finite holomorphic map from a D4 polygonal-disk unfolding onto this Y. This closes the proposed way of importing that perfect-central obstruction into our rooms. It does not prove general midpoint-event existence: other endpoint obstructions might not arise from such a regular intermediate quotient. In particular, it says nothing about the gonality of a Galois closure above X, or a similar central-target obstruction in a nonregular fiber action. Holomorphic factorization X->Y is the exact excluded situation. The explicit genus and orbit-size hypotheses are retained; no small-group classification is used.

A focused tools-disabled Opus review accepts Sections10-13 with the lattice, pi-sector and literal-factorization scope clarifications now incorporated. This was a proof/code-reading review, not independent numerical execution. `pocket-monodromy.py/json/log` checks only the prescribed reflection identities, six-square cover, and SL(2,F7) matrix control. It does not search for rooms, directions, primitive words or origami orbits. The universal pocket-detection goal remains active.

## 14. A real sphere map with all forbidden fibers on the boundary

The quotient in Section12 carries more information than low gonality. Let
E=R^2/2Z^2 at the raw grid base, with quarter turn rho(z)=iz. The developing
cover pi:X->E is rho-equivariant: pi([p,g])=g p modulo2Z^2. All physical
reflection translations are even, so this is well-defined across every seam.
There is a commutative square

    X ----pi----> E
    |             |
    /C4           /C4
    |             |
    S^2 ---F----> S^2.

The quotient E/C4 has three branch values: A and B have stabilizer order4;
the two mixed-parity points form one orbit C with stabilizer order2.
If T is the number of canonical triangles of P, then deg(pi)=T, since
area(X)/area(E)=8 area(P)/4=2 area(P)=T. Thus deg(F)=T as well.

The two orientations of P in X/C4 are exchanged by an antiholomorphic
involution. Its fixed oval is exactly the glued physical boundary. Under
uniformization this is a real rational map of spheres. Its ramification
partitions have a direct description. Write each physical boundary angle as
m pi/4, including m=4 for a smooth boundary lattice point.

| Preimage | Local degree of F |
|---|---:|
|Boundary A or B|m|
|Boundary C|m/2|
|Interior A, in either orientation of P|4|

For example, a local complex coordinate on the doubled corner is proportional
to the physical coordinate raised to 4/m; a base A/B coordinate is the fourth
power of the torus coordinate. Their composition has degree m. At C the base
power is2 instead. This calculation also covers the smooth m=4 case.

In a raw room, every B/C point belongs to the physical boundary. Therefore
**every preimage of B and C under F lies on the real oval**. Every interior A
contributes a conjugate pair of nonreal preimages of A, each of degree4.
Boundary C has degree1 or3; smooth boundary C would have degree2 and is
forbidden by the raw premise. Boundary B need not have odd degree: right-angle
and reflex 270-degree B corners give degrees2 and6. No parity argument may
silently exclude them.

This is a necessary planar-real restriction on an actual room cover. It is
an additional restriction alongside the full-lattice condition in Section10. It does not by itself
show that a primitive straight chord lifts to the required target. A proof
using these partitions must still preserve the source/target fiber labels
and the selected embedded pi-sector.

## 15. The halfturn quotient has genus equal to diagonal runs minus one

Assume the connected eight-copy unfolding of the disk, as ensured by the
literal pocket. Let J be its left halfturn and put Z=X/<J>. A diagonal run
is a maximal consecutive block of diagonal walls in the cyclic physical
boundary; horizontal and vertical walls break such a run. Let d be the
number of these runs, W the wall count, and O the number of corners whose
angle in pi/4 units is odd. Then

    O=2d,       genus(Z)=d-1.                       (4)

To prove it, write the actual corner angles as m_i pi/4, i=1,...,W.
All m_i lie in {1,2,3,5,6,7}. A corner has g_i=gcd(m_i,4) distinct lifts
in X, each of cone angle 2pi m_i/g_i. Hence

    2 genus(X)-2 = sum_i(m_i-g_i).

Each lift is fixed by J: its rotational stabilizer has order4/g_i and
g_i is either1 or2. Conversely J fixes no point away from physical corners.
Interior and smooth boundary points have trivial halfturn stabilizer.
The number of fixed points is consequently

    F_J=sum_i g_i=2W-O.

The same count also gives genus(X)=W+d-3. Since sum_i m_i=4W-8, Riemann-Hurwitz for X->Z gives

    4 genus(Z)-4 = (4W-8-F_J)-F_J = 2O-8,

and genus(Z)=O/2-1. A corner angle has odd m_i exactly when one incident
wall is diagonal and the other axis-aligned. These are precisely the two
endpoints of each diagonal run, giving (4).

The residual quarter turn gives Z->X/C4=S^2 of degree2. Thus Z is
hyperelliptic when its genus is at least2. In particular, **if there is only
one diagonal run and genus(X)>=2, X itself is hyperelliptic**, because then Z is a sphere
and X->Z has degree2. This includes the hypothetical sole-diagonal subclass
of Section8. The literal pocket requires W>=5, so genus(X)=W-2>=3 in that subclass. The branch values of Z->X/C4 are precisely the2d images of odd-angle corners and lie on the real oval. It neither establishes that the raw subclass contains two
interior marks nor proves pocket detection there.

The connectedness qualification matters. Axis-only and all-diagonal polygons each have a formal
eight-copy unfolding with two components; inserting O=0 into the connected
formula would produce genus -1 and is invalid. The literal pocket includes an axis wall and a diagonal wall and excludes both cases.

`pocket-planar.py` independently constructs canonical triangles and identifies
vertices in X, Z and X/C4. On the34 frozen rooms, the three Euler genus counts
agree with (4) and the fixed-point count. The branch partition sums in
Section14 are consistency identities; the local degrees are proved by
the uniformizer argument, not independently verified by those sums. For the saved25-wall control: T=28, O=12, d=6, F_J=38, genus(X)=28,
genus(Z)=5, genus(X/C4)=0. Each A/B/C partition sums to28 and the total sphere
ramification is54=2*28-2. These are fixed-cell checks, not a room census or
any geodesic search.

## 16. What the broader realization review contributes

The separate tools-disabled realization analysis supplies a useful pocket
flux formulation, which can be justified directly from the six local maps.
The eight pocket triangles form an open square Pi in X. Its closure can
identify boundary vertices, so it must not be treated as an embedded closed
disk. Its four corners map to the B_0 lift, its center to the A_0 lift, and
opposite side midpoints map to the two C_0 lifts. The eight open boundary
half-sides are portal arcs. On an arc in copy g put e=g u, u=(0,-1).

For a continuous chain gamma transverse to these arcs, avoiding cone points,
and with both endpoints outside the closed pocket, its slide-period
derivative is

    delta(gamma)=sum_enter e - sum_exit e.          (5)

Indeed an excursion entering in copy g and exiting in copy h has load
(g-h)u; subdivision into several visits adds these loads. A core that lies
entirely in the open square cannot be a nonconstant closed straight geodesic.
A generic horizontal or vertical closed geodesic traverses the square from
opposite sides in the same half, whose portal fields agree. Thus (5) proves
that **every absolute axis-cylinder period has zero derivative for this
literal pocket slide**, without an additional constraint on the remainder.
This is stronger for this slide than general transverse alignment.

The absolute derivative is nevertheless nonzero. Enter the pocket through
the lower-left portal in copy I and exit through the upper-right portal in
copy -I. The load is (0,-2). Return outside the pocket by a continuous path:
the remainder P' is connected, and the reflection group of its exterior
walls contains -I. To see the last assertion, a bounded polygon has two
nonparallel wall directions; in D4 the product of their reflections has
order2 or4, so a power is -I. Do not require P' to have both a horizontal
and a vertical wall. Open wall crossings and paths in copy interiors then
connect copy -I to copy I outside the pocket. Equation(5) gives the stated
nonzero absolute period derivative. This is a continuous cycle, not an
admissible straight midpoint event.

For the sole-diagonal subclass, Section8 also yields a definite limitation
on every label-fixing affine map phi. The mod2 diagonal character vanishes
on absolute cycles. Since phi fixes the event endpoints, (phi-1)eta is
absolute, so its diagonal bit is zero and

    bit(phi eta)=bit(eta).

Thus enlarging the affine group cannot turn a blind even-bit seed into an
odd-bit seed in that subclass. The relative bit can still be nonzero: it is
the endpoint-copy colour difference. Vanishing on absolute cycles must not
be confused with vanishing on relative event classes. Even-bit events can
also detect through a nonzero even real derivative.

The review's general rational-direction twist proposal is conditional and
is not used to assert existence. Form the cylinder-direction saddle connections relative to the cone points
and every marked S/T lift. A suitable power of the parabolic fixes these
connections, all endpoints and prongs, and each cylinder. It does not fix
saddle connections in all directions. Omitting S/T from this marked set
would leave the endpoint-fixing premise unjustified.
Its event increment is the usual sum of core intersection numbers times
core classes. Neither an event with the actual target nor a nonzero pairing
with this sum has yet been constructed universally. The proposed exact
cylinder-boundary characterization of all midpoint events is not adopted
here without a separate endpoint and length-convention proof.

Sections14-16 passed a separate tools-disabled Opus proof/code-reading review.
Its corrections concerning incomparable lattice/planarity data, consistency
versus independent degree checks, connectedness, genus thresholds and marked
cylinder endpoints are incorporated. No independent numerical execution by
the reviewer is claimed. The opening/corner-term transfer remains imported
from the earlier reviewed theorem.

## 17. An exact rational/irrational dichotomy for the slide

Let ell be the smaller initial length of the two flanking vertical edges,
and let d>0 be the minimum Euclidean distance between nonadjacent closed
edges of the initial strictly simple polygon. Set epsilon=min(d,ell)/4.
For both positive and negative parameters with |t|<epsilon, the unfolding
of the literal slide is a translation cover of a torus **if and only if t is
rational** in the normalized coordinates of Section1.

The two independent absolute periods (-2,0),(0,-2) from Section10 remain
constant for every t in that interval. Each edge moves by Hausdorff distance
at most |t|, so nonadjacent edges stay at distance at least d-2|t|>0.
The flanking vertical edges retain lengths at least ell-|t|>0; the other
edge lengths stay fixed. Adjacent supporting-line directions stay distinct.
Thus the polygon stays strictly simple with the same wall pattern.
Here a fixed wall means a fixed supporting line; its endpoints can move.
The moving pocket also has the exact halfturn

    G_t=D_t H_t D_t H_t,
    G_t(x,y)=(-x+4,-y+4-2t).

Choose a word W using only fixed exterior walls of the remainder P' whose
linear part is -I. Such a word exists by the two-nonparallel-wall argument
in Section16. Its affine map is W(z)=-z+b, b in2Z^2. Consequently

    W G_t(z)=z+b-(4,4)+(0,2t).                     (6)

Its copy label closes. A continuous loop crossing the prescribed walls and
joining the crossings through interiors of copies realizes this absolute
period, just as in Section10. This construction is performed directly for each t; it does not require
a Gauss-Manin transport claim. It is not a billiard itinerary or a straight
corner event.

Subtracting its base period b-(4,4), an integer combination of the two fixed
periods, shows that the absolute period group contains (0,2t) as well as
(2,0),(0,2). For irrational t it is nondiscrete: Z+ tZ has arbitrarily small
nonzero elements, for example by the pigeonhole approximation argument.
A translation torus cover would have every absolute period in its torus
lattice, a discrete group. Thus no torus cover exists for irrational t.
For rational t=p/q all vertices have rational coordinates with a common
denominator. The8 polygon copies give a finite cellular decomposition of X.
Every edge displacement has rational coordinates, and first homology is
generated by cycles in this1-skeleton. Hence the absolute period group is
a subgroup of (1/N)Z^2 for one integer N. It contains the two independent
fixed periods, so it is a lattice Lambda. Integration of the differential
modulo Lambda gives a nonconstant holomorphic map X->C/Lambda whose local
derivative is the translation differential. Compactness makes it a finite
branched translation cover. This proves the dichotomy without a tiling
claim. If one instead refines the canonical A-B-C tiling, use mesh1/(2q),
not merely1/q; an odd numerator otherwise violates the even-diagonal-offset
convention. The old raw noncorner-label property is not preserved by this
refinement and is not used in the rational-direction proof.

A further exact consequence is that the Q-linear span of absolute periods
has dimension4 at every irrational t. Every reflection translation belongs
to Q^2+t Q^2, giving the upper bound4. The two fixed periods, the changing
period in (6), and its quarter-turn image span (2,0),(0,2),(2t,0),(0,2t)
over Q. These four vectors are Q-linearly independent for irrational t.
This is a period-group statement, not the rank of an affine orbit closure.

For the saved room a fixed exterior word is W=V_1 H_0. Equation(6) is the
period (-2,-4+2t). It is also twice the displacement between the fixed halfturn center(1,0)
and the moving tip(2,2-t). The prescribed symbolic reflection checker verifies
its base period, derivative and exact values at three rational controls,
with mirror incidence, positive edge lengths and the stated simplicity
bound checked separately. The
general result uses the displayed algebra and the elementary nondiscreteness
argument, not extrapolation from those controls.

For irrational t, no translation quotient of X can be a torus cover either:
composing its translation covering maps would make X a torus cover. This
applies in particular to the canonical minimal translation quotient.

This closes a specific loophole in using non-torus-cover illumination
results along this family. It does not close the goal: at an irrational t,
the exceptional periodic-point or minimal-quotient alternatives can still
support a particular finitely blocked pair. At a rational t the torus-cover
classification alone says nothing about darkness of this fixed pair.
Nor does this argument produce the first-order midpoint seed required by
the active goal.

A separate tools-disabled Opus review accepts the irrational argument and
the exact word algebra. Its requested rational-case cellular proof,
positive-length/simplicity bound, fixed-supporting-line wording, center
interpretation and intermediate-translation-quotient qualification are now
incorporated. No independent numerical execution by that reviewer is claimed.

## 18. Literature boundary for the new quotient route

The rotational quotient of a rational polygon unfolding as its doubled
sphere is established background, not a novelty claim here. It appears
explicitly in the proof of Proposition3.11 of
[Apisa–Wright, Marked points on translation surfaces, Section3.2](https://websites.umich.edu/~alexmw/ApisaWright.pdf).
Our use is the gonality test in Sections12-13 and the explicit halfturn and
raw-fiber restrictions in Sections14-15.

The same paper's Theorem3.6 retains periodic-point and minimal-quotient
alternatives for finitely blocked pairs. Theorem3.10 gives finitely many
exceptional pairs on a non-torus-cover rotational quotient. Neither proves
that this fixed pair escapes the exceptions under the pocket slide.
Regular lifts of physical convex corners must remain a finite marked
blocking set when relating physical darkness to these surface statements.

[Apisa's generic-stratum result](https://arxiv.org/abs/1601.07894) does not
apply just because a curve has a hyperelliptic involution. The square-tiled
base has a closed arithmetic orbit; a hyperelliptic underlying curve can
also carry a differential outside a hyperelliptic connected component of a
stratum. No claim of genericity for an irrational slide is made without
identifying its orbit closure. The torus-twist constructions of
[Johnson–Schmoll](https://ccjohnson.org/papers/involutions_2013_10_03.pdf)
also do not supply an actual labeled midpoint connection. Their quotient
and covering structure is useful context, not a solution to this event
realization problem.

## 19. A finite-degree obstruction to the nonperiodic alternative

A second tools-disabled Opus review accepts this fixed-surface argument,
subject to the explicit hypotheses and genus check recorded below.
It avoids assuming any extension of the canonical minimal-cover family over
an orbit closure. It imports the fixed-surface Apisa-Wright quotient and
blocked-pair classification explicitly.

Let X be a connected D4 disk unfolding that is not a translation cover
of any torus, with two distinct interior physical marks S,T. Here and in
Section20, "non-torus" always means this stronger no-torus-cover condition. Suppose all8S lifts are finitely blocked from all8T lifts,
and suppose none of those16points is M-periodic. Let pi:X->Y be its canonical
minimal translation quotient and let q:Y->Q be the minimal halftranslation
quotient. The quarter turn rho descends to r on Y. Surjectivity of pi and
rho^4=1 imply r^4=1; its derivative is i, so r has order4. Its square j=r^2
negates the differential. Minimality makes j the unique such involution and
q its degree2 quotient. Apisa-Wright Lemma3.3, including its proof,
identifies this Y/j with Q_min; this identification is an imported theorem,
not a consequence inferred merely from the existence of one quotient.

The blocked-pair theorem identifies q pi(x) with q pi(y) for every source
and target lift. In particular, the four points r^a pi(x) all belong to one
q-fiber. That orbit has size at most2, hence j fixes pi(x). A q-fiber through
a fixed point of j is a singleton. It follows that **all16marked lifts map
to one regular point p of Y, and r fixes p**. Thus

    deg(pi)>=16.                                  (7)

The point p is regular because the pullback differential is regular at each
mark; ramification or a target zero would give a source zero. Conversely
all16marks are unramified over p.

Write the physical angle counts as n_m for m in {1,2,3,5,6,7}. Every source
zero has even order: its order is m/gcd(m,4)-1. Every target zero also has
even order, since a target odd order would pull back to an odd source order
by ord_x(omega_X)+1=e_x*(ord_y(omega_Y)+1).

If genus(X)<=32, Riemann-Hurwitz and (7) force genus(Y)=2. Then Y has one
zero of order2. Its hyperelliptic involution negates every1-form, so the
uniqueness of the minimal negating involution makes it j. The quarter turn
r has exactly two fixed points: the unique zero and one regular point p.
Indeed, if a is the number of r-fixed points and g_prime is the genus
of Y/r, Riemann-Hurwitz gives

    2 = 4*(2*g_prime-2) + 3*a + (6-a),
    a = 2-4*g_prime.

The unique zero is r-fixed, so a>=1; therefore g_prime=0 and a=2.
This particular genus2 count does not need the disk-sphere hypothesis.

A source corner of type m=1,5,7 has a single rho-fixed lift and respective
zero order0,4,6. It cannot map to the target zero: the respective numbers
1,5,7 are not divisible by3. Therefore all these lifts map to p, contributing
local degrees1,5,7. They are distinct from the16interior marked points, so

    deg(pi)>=16+n_1+5n_5+7n_7.                    (8)

Over the unique target zero, only source zeros of order2 can occur, and
each must have local degree1. There are exactly n_3+2n_6 such source zeros.
Consequently

    deg(pi)<=n_3+2n_6.                            (9)

Thus for genus(X)<=32, the strict inequality

    16+n_1+5n_5+7n_7 > n_3+2n_6                  (10)

excludes the nonperiodic all-to-all blocked-fiber alternative. This says a
dark physical pair on a non-torus deformation with these angles must use
the periodic-point case. It does not exclude that case, prove illumination,
or construct a first-order event. The statement does not apply to the raw
square-tiled base itself, which is a torus cover.

The count-only implementation in `pocket-planar.py/json` satisfies(10) on
33of the34frozen angle patterns. Each frozen source genus is also checked
separately: all lie between27and29, hence all satisfy the required<=32
hypothesis. The remaining pattern is parity-W26-117,
which has n_5=0 and therefore cannot contain the stated straight pocket
(the pocket requires a225-degree B_0 corner). This does not assert that
every pattern with n_5>0 actually has the required literal attachment.
For the saved control, the lower bound is37and the upper bound is21.
These are arithmetic checks of a necessary cover-degree condition, not
optical exclusions or evidence of nonperiodicity of the actual marks.

## 20. Bounded-degree folds and the periodicity reduction

A first tools-disabled Opus review rejected transporting a generic family
of canonical minimal covers to a special surface; that shortcut remains
retired. The compact-target proof below instead permits arbitrary covers
of one fixed degree. The second review proposed this route, and a third
focused review accepts its expanded lift argument, finite-fiber argument,
and orbit-closure dimension step, with the standard inputs stated explicitly.

**Reduction.** If a connected D4 disk unfolding is not a translation cover
of a torus, every lift of a dark pair of distinct physical interior points
is periodic for the GL^+(2,R) orbit closure M of the unmarked unfolding.
The result does not assume a genus bound. It does not classify these
periodic points, prove illumination, or construct a midpoint event.

**Physical corners and the stronger empty-blocking statement.** It is safe
to infer finite blocking by all regular corner lifts, with zeros excluded
from geodesic interiors. In fact, for distinct physical endpoints one has
the stronger statement: physical darkness implies absence of straight
segments between EVERY source/target lift pair even when removable
corner lifts may be crossed. The earlier caution claiming otherwise was
too strong; it overlooked that all actual endpoint lifts are available.
[Wolecki, Remark2.2](https://arxiv.org/pdf/1905.09358) states this fact.
Here is an independent retracing proof for the present angles.

Suppose a zero-avoiding straight segment connects some lift of S to some
lift of T. Fold it into the polygon and permit continuations through its
regular corner lifts. At a physical corner of angle pi/4orpi/2, which are precisely the
removable corners in this canonical room class, straight continuation
reverses and retraces the physical path. The even number of unfolded
sectors is essential to this argument; no retracing assertion is made
here for general odd-denominator removable corners. Let a>0 be the
time of the first such contact, and L the total path length; no corner
occurs on [0,a). Until time min(2a,L), uniqueness of the ordinary reflected
flow gives gamma(a+u)=gamma(a-u).

If a<L<2a, T already occurs at time2a-L<a, giving an ordinary corner-free
connection from S to T. L=2a would give T=S, excluded. If L>2a, the path
returns to physical S at time2a; discard [0,2a] and restart from the lift
of S then occupied. The remaining segment is straight on the unfolding,
has the same actual physical endpoints, and has fewer regular-corner
contacts. There are finitely many such contacts on a finite segment
avoiding zeros, so iteration terminates in a corner-free physical
connection. A segment with no regular-corner contact already works.
Thus any unfolded connection between the actual fibers would contradict
physical darkness. A prescribed individual source/target lift pair need
not be preserved by deleting an excursion; the physical S/T fibers are.

The Section20 reduction only needs the weaker finite-blocking consequence,
so this correction strengthens its premise and does not change its proof.

**The mixed periodic case is covered.** The third reviewer asks for an
explicit source for one periodic endpoint forcing the other to be periodic.
The proof of Apisa-Wright Theorem3.6 supplies exactly this step: its first
paragraph treats one endpoint periodic or a zero before considering the
case of neither endpoint periodic. Both endpoints here are regular.
Consequently, if any one of the16lifts is periodic, finite blocking first
propagates periodicity to every lift in the opposite fiber and then back
to all lifts in the original fiber. No reflection-invariance argument is
needed. The exact source is
[Apisa-Wright, proof of Theorem3.6, page17](https://websites.umich.edu/~alexmw/ApisaWright.pdf).

If none is periodic, use the fixed-surface part of Section19, without
its subsequent genus bound: all16lifts map to one point fixed by the
negating involution j of the minimal translation quotient pi:X->Y.
The fold-locus lemma and finite-fiber argument below prove that every
regular point of pi^-1(Fix j) is M-periodic. This contradicts the assumption
that none is periodic and establishes the reduction.

### 20.1. Compact-target proof of fold-locus closedness

The second review proposed this route. The third focused review accepts
the expanded lifted-graph proof, including regular branch values, poles,
loops, nonbacktracking, target compactness, exact degree and fold persistence.
The standard compactness, minimal-quotient and orbit-closure inputs remain
explicit imports, not elementary results newly proved here.

**Lemma (bounded-degree fold persistence).** Fix a connected Abelian stratum
of genus at least2 and an integer D. Let (X_n,omega_n,x_n) converge to
(X,omega,x) in the smooth pointed stratum, with x regular. Suppose each
X_n admits a holomorphic map f_n to a connected finite-area quadratic
differential (Q_n,q_n), of degree exactly D, with

    f_n^* q_n = omega_n^2,
    f_n(x_n+u)=f_n(x_n-u) near u=0.

Then X admits such a map of the same degree D, folding at x. The target
stratum is allowed to depend on n. No target or source minimality is assumed.

**1. Finitely many target strata.** If a target singularity has order k,
and a point over it has source zero order a and local degree e, then

    2*a+2 = e*(k+2).                              (11)

Target zeros have k>=1 and only source-zero preimages, so their number
and orders are bounded in terms of the fixed source stratum. Also genus(Q_n)
<=genus(X_n) by Riemann-Hurwitz. Since the only target poles are simple,

    number_of_poles = sum_of_positive_zero_orders - 4*genus(Q_n)+4.

This bounds their number as well. Pass to one target stratum. The area
is area(X_n)/D, bounded above and away from zero. A fold at a regular
source point has a=0 and e>=2, so (11) forces e=2,k=-1; the target is
strictly halftranslation and has a singularity.

**2. Short target segments force short source geodesics.** Smooth convergence
in a fixed source stratum supplies near-identity piecewise-affine comparison
maps from one fixed triangulation. Consequently there is delta>0 such that,
for all large n, every source saddle connection and every nonconstant
closed regular source geodesic has length at least delta. For closed
geodesics one can either use the source flat systole, or extend the
geodesic to a maximal cylinder and use a saddle connection on its boundary.
A genus>=2 translation surface cannot consist of just that cylinder.

Let gamma be any target saddle connection of length epsilon. Away from
the finitely many branch values its inverse image has total edge length
D*epsilon. Split the inverse image at every source zero, including zeros
lying over regular branch values in the interior of gamma.

At a preimage of a target zero, (11) implies a>0, so the chain stops at a
source zero. At a preimage of a simple pole, (11) gives e=2*a+2. If a>0,
stop again. If a=0, e=2: exactly two incident lifts of gamma meet there,
and in the source flat coordinate they are opposite radial segments.
They join as one straight trajectory. No other regular preimage branches.

Thus the nonempty lifted finite graph, after continuing through its
regular valence2 vertices and stopping at zeros, is a union of source
saddle connections and closed regular geodesics. Each has positive length
at most its total length D*epsilon. There is no backtracking at the
regular vertices, because the two tangent directions are opposite.
Therefore

    systole_saddle(Q_n) >= delta/D.                (12)

This argument includes target segments ending at two poles, loops with
the same endpoint, and regular branch values in the segment interior.
It does not assume that preimages of simple poles are always zeros.

The compactness criterion for a fixed finite-area quadratic stratum says
that bounded normalized area and a positive lower bound on saddle lengths
give a compact set in that stratum. Applying it to (12), and normalizing
and then undoing the bounded area factors, gives a subsequence

    (Q_n,q_n) -> (Q,q)

in a smooth target stratum. This is a standard imported stratum-compactness
result, distinct from the compactness of the canonical minimal quotient.

**3. Limit the maps.** Choose near-identity piecewise-affine comparison maps
phi_n:X->X_n and psi_n:Q_n->Q from persistent triangulations, including x
in the source triangulation. Their flat Lipschitz constants and inverse
constants tend to1; their quasiconformal dilatations tend to1, also across
the finitely many cone points by removable-singularity extension. Each
f_n is1-Lipschitz for the flat path metrics: every path image has at most
the original length. Hence

    g_n = psi_n o f_n o phi_n : X -> Q

is equicontinuous and surjective. Arzela-Ascoli gives a uniform limit f,
and compactness of X shows f is surjective. It is nonconstant.

One can verify holomorphy without a quasiregular normal-family import.
Flat covering maps lift paths starting at any chosen preimage, preserving
length; at their finite branch points a continuation can be selected.
After the near-isometric comparisons, each g_n is correspondingly
co-Lipschitz with constant tending to1. Thus if f(a)=p, there are points
 a_n->a with g_n(a_n)=p: lift a shortest path from g_n(a) to p through
psi_n and then f_n. If a fiber of f had D+1distinct points, doing this
in disjoint neighborhoods would give D+1distinct preimages under g_n,
contradicting degree D. Hence every fiber has at most D points.
In particular f^-1(Sing(q)) is finite. Away from this finite set and the
source zeros, fixed source and target flat disks give f_n locally as
z->+z+c_n or z->-z+c_n. Passing to a subsequence fixes the sign; the
comparison charts converge, so f is locally z->+z+c or z->-z+c.
It is therefore holomorphic off a finite set. Continuity into Q makes
those isolated singularities removable, so f is holomorphic everywhere.

Uniformly close maps to the fixed smooth compact underlying surface Q
are homotopic, using any auxiliary smooth Riemannian metric on Q and its
positive injectivity radius. Thus deg(f)=deg(g_n)=D; no degree is lost.
On a regular source disk whose image avoids the finitely many target
singularities, f_n is a flat local map z->+z+c_n or z->-z+c_n. The sign
is constant on a sufficiently small such disk after taking a subsequence.
Passing to the limit proves f^*q=omega^2 there; holomorphic/meromorphic
identity continuation gives equality everywhere. This also verifies the
halftranslation nature of the limiting cover independently of the topology.

**4. Retain the marked fold.** Pick a fixed embedded flat disk about the
regular x, small enough that the corresponding disks about x_n persist.
On its flat coordinate disk the two holomorphic maps

    u -> f_n(x_n+u),     u -> f_n(x_n-u)

agree near0. The identity theorem extends that equality to the whole
fixed disk, even if its images contain a target pole. Uniform convergence
then gives f(x+u)=f(x-u) on the limiting disk. In particular its central
point is a regular fold, not merely a limiting pair of distinct points.
This proves exact-degree closedness using the explicitly imported stratum
compactness criterion and near-isometric period-coordinate comparisons.
The optional quasiregular normal-family input has been removed.

**Consequence for periodicity.** Let pi:X->Y be the canonical
minimal translation cover of degree d for a surface that covers no torus,
and let j be the unique negating involution of Y. Put D=2d. The closed
fold locus of the lemma is invariant under GL^+(2,R), because -I is central.
Over this particular X every fold cover of degree2d lifts to a degree d
translation cover of its orientation double. Minimal factorization makes
that double Y, and uniqueness of the negating involution makes its fold
set precisely the finite set of regular points in pi^-1(Fix j).

The marked orbit closure N of such a point therefore has finite fiber
over X. If its complex dimension were dim(M)+1, the equal-fiber-dimension
statement in Apisa-Wright Lemma2.1 would give a one-dimensional local
fiber through this point over X, contradicting finiteness. This local
argument avoids any assertion of global surjectivity of a marking. Hence dim(N)=dim(M), which is M-periodicity.

Combined with the fixed-surface quarter-turn and mixed-endpoint arguments
at the beginning of this section, this forces every lift of a dark interior physical pair on a non-torus
D4 unfolding to be M-periodic. This is a reduction of the exceptional
case, not a proof that these periodic pairs illuminate, nor any construction
of the actual one-corner midpoint event required by the active goal.

**Audit status.** The third tools-disabled Opus review accepts the
fold-persistence lemma and its finite-fiber/dimension consequence. Its sole
additional corollary question, the mixed periodic endpoint case, is resolved
by the first paragraph of the primary Theorem3.6 proof as described above.
The target compactness import includes simple-pole endpoints and saddle
loops; those are exactly the cases covered by the lifted graph. A standard
unit-area version for Abelian strata is stated in Minsky-Weiss Section7,
and the quadratic-with-simple-poles version is used in the cited quadratic
degeneration literature. The independent analytic-correspondence strategy
is unnecessary for this proof. Review sources are archived in
`inputs/pocket-periodic-first/`, `inputs/pocket-periodic-second/`, and the
current `pocket-periodic-review.txt`. No novelty claim is made for the
periodicity consequence before a separate literature comparison.


## 21. Transcendental parameters share one arithmetic orbit closure

A focused tools-disabled Opus review accepts this argument from the stated
inputs. The rational-basis, orbifold-chart, absolute-period and involution
qualifications requested by that review are included below. It refines the
orbit-closure question without assuming a full quadratic stratum or
deducing rank from the period Q-span.

Work in one sufficiently small fixed relative-period chart about X_0,
using a rational homology basis and a marked local cover if automorphisms
make the chart an orbifold chart. Let Sigma consist ONLY of actual zeros;
the freely moving interior S/T marks are not included in this stratum.
The literal slide has period vector

    v(t)=v_0+t*v_1,       v_0,v_1 in Q[i]^n.

The same formula defines translation surfaces on a small complex parameter
disk, even though nonreal parameters need not represent physical mirror
polygons. This complex extension is used only for analytic continuation.
Let M_tau be the GL^+(2,R) orbit closure for a real transcendental tau in
the disk. By Wright's field-of-definition theorem, each local branch has
homogeneous linear equations with coefficients in a real number field K.
For such an equation L, the equality

    L(v_0)+tau*L(v_1)=0

has algebraic complex coefficients. Transcendence forces both terms
L(v_0)=L(v_1)=0. Thus a neighborhood of tau in the parameter disk belongs
to that branch of M_tau. The whole parameter disk then belongs to M_tau. To see this without
following one immersion branch, let E be its closed preimage in the disk.
Near any parameter t_1 in E, proper immersion makes M_tau a finite union
of homogeneous linear subspaces in our period chart. An affine line meets
each subspace in no points, one point, or the entire line. Thus E is locally
either a finite set or a neighborhood of t_1. A boundary point of the
nonempty interior of E would be a nonisolated point of E, so would also
be interior. That interior is therefore closed as well as open in the
connected disk; it is the whole disk. In particular M_tau contains every
small real parameter and the square-tiled base X_0.

For any second transcendental sigma, this yields X_sigma in M_tau, hence
M_sigma subset M_tau by closed GL-invariance. Interchanging sigma and tau
proves equality. There is one orbit closure M_* for ALL sufficiently small
transcendental real parameters, and it contains the complete parameter disk.
This statement does not assert the same orbit closure for all irrational
algebraic parameters.

Wright's Theorem1.1 and Example1.2 give k(M_*)=Q because M_* contains X_0.
See [Wright, The field of definition of affine invariant submanifolds](https://websites.umich.edu/~alexmw/numfield.pdf).

The original field argument gives rank at least2; Section21.1 strengthens
this to rank at least3. If it had rank1, the absolute tangent space, defined
over Q, would be the complexification of a rational real2-plane. The real
and imaginary parts of omega belong to that plane and are independent.
After choosing two rational basis vectors and clearing their finitely many
denominators, all absolute periods would belong to the lattice generated
by two independent complex numbers. Integration modulo that lattice would
make X_tau a torus cover, contradicting Section17. That section rules
out every translation cover of a torus by nondiscrete ABSOLUTE periods;
it does not restrict branching to one point. This argument uses the
rational tangent-space theorem; the period Q-span computation alone would
not justify an orbit-closure rank statement. No upper rank bound follows.

There is also no relative tangent direction in M_*. Every actual source
zero is a corner lift fixed by the physical halfturn J. Under GL^+(2,R),
J still has derivative -I. To take a smooth limit, transport J_n to a common
source using the period-chart markings. These maps are near-isometries
for a convergent family of flat path metrics. Arzela-Ascoli, J_n^2=1 and
the differential relation J_n^*omega_n=-omega_n retain a nontrivial
involution fixing every noncolliding labeled zero in the limit.

On a fixed genus>=2 surface there are only finitely many automorphisms,
so locally there are finitely many possible induced J-actions. M_* is
locally contained in the union of their relative -1eigenspaces; each
irreducible linear branch lies in one such eigenspace. But

    ker[H^1(X,Sigma;C)->H^1(X;C)] = C^Sigma / C

has J-action +1 because J fixes Sigma pointwise. Its intersection with
the -1eigenspace is0. Hence rel(M_*)=0, and dim_C(M_*)=2*rank(M_*)>=4.
Adding the interior S/T marks would invalidate this rel0 argument, since
J exchanges those lifts rather than fixing them. No conclusion about
marked relative directions is smuggled into the unmarked argument.

**Remaining obstruction.** Including Section21.1, the conclusion is an arithmetic rank>=3,
rel0 orbit closure, not the entire stratum of canonical quadratic covers.
The generic full-stratum periodic-point classification cannot be applied
without proving that equality. A proper arithmetic covering locus can
still have periodic regular points away from Fix(J). The unmarked tangent
argument alone says nothing about whether our actual fixed S/T lifts are
among them. An analogous claim about their marked orbit closure requires
an explicit marked field-of-definition input as well as a nonzero vertical
marked tangent; neither is assumed here. Even excluding dark pairs at
transcendental parameters would still require a separate argument to
produce the original admissible one-corner midpoint event at t=0.


### 21.1 Constant area and D4 symmetry force rank at least three

**Status: accepted by independent tools-disabled Opus review (exit0).** For the
literal straight-attached pocket slide of this paper, the common unmarked
orbit closure M_* in Section21 has rank at least3, provided the established
D4 unfolding and common local-branch hypotheses are retained. This uses a
symplectic tangent theorem in addition to the prior field argument.

Use absolute real cochains x_0,y_0,x_1,y_1 of Section28, with
omega_t=x_0+i y_0+t(x_1+i y_1), and write B(u,v)=integral_X u wedge v.
The four classes are independent in absolute cohomology by the determinant16
period evaluation in Section28. The real underlying tangent V=p(T_R M_*)
contains all four. Indeed the local complex line belongs to one branch of
M_* by Section21; its derivative belongs to T_C M_*. This tangent is defined
over R, so the derivative's real and imaginary parts belong to T_R M_*.
Taking the real and imaginary parts of omega_t at two distinct real
parameters in that same homogeneous local branch puts x_0,y_0 there too.
This is the tangent of M_*, not the smaller orbit closure of X_0 itself.

There are fixed topological copy symmetries R,K on the unfolding, with
R orientation preserving of derivative rotation by90degrees and K
orientation reversing of derivative reflection in the x axis. They persist
for the real slide and give, for j=0,1,

    R* x_j=-y_j,   R* y_j=x_j,
    K* x_j=x_j,    K* y_j=-y_j.

Here K is the copy-exchanging anti-affine symmetry; the physical room
itself need not have reflection symmetry. Explicitly use copies (p,g),
g in D4, with coordinate g(p), and identify (p,g) with (p,g r_s) along
physical side s. Left multiplication (p,g)->(p,h g) respects every such
identification and has derivative h. Choosing h to be quarter-turn or
x-axis reflection gives R or K for every real t. Their mapping classes
are locally constant, so their cohomology matrices are fixed in the common
Gauss-Manin chart. Taking two real t values separates the j=0 and j=1
formulas; no polygon symmetry at nonreal parameters is asserted.
R preserves B and K reverses B. In particular

    B(x_0,x_1)=B(y_0,y_1)=0,
    B(x_1,y_0)=B(x_0,y_1).

The physical room is a fixed remainder with one triangle translated along
a straight wall. Its area, and hence the eight-copy unfolded area, is
constant for all sufficiently small real t. Expanding gives

    area(X_t)=B(x_0,y_0)
      +t [B(x_1,y_0)+B(x_0,y_1)]
      +t^2 B(x_1,y_1).

Thus B(x_1,y_1)=0 and both equal cross terms vanish. Consequently for
W=span_R{x_0,y_0,x_1,y_1},

    B restricted to W =
       [0,A,0,0; -A,0,0,0; 0,0,0,0; 0,0,0,0],
    A=area(X_0)>0,
    rad(B|W)=span_R{x_1,y_1},   dim W=4.             (21.1a)

By [Avila-Eskin-Moeller, Theorem1.4](https://arxiv.org/pdf/1209.2854),
B is nondegenerate on V. A symplectic vector space containing a
four-dimensional subspace with a two-dimensional radical must have
dimension at least6. For completeness, nondegeneracy makes the map
V->rad(W)^*, v->B(.,v)|rad(W), surjective. Its restriction to W is zero,
so V/W surjects onto a two-dimensional space. Hence

    dim_R V >= 4+2=6,      rank(M_*)>=3.            (21.1b)

This does not read rank from a period-span dimension: the cup-product
radical forces TWO additional absolute tangent dimensions beyond the
four-cochain pencil. Thus dim_C M_*>=6 even without rel0; the separately
established rel0 result gives the equality dim_C M_*=2 rank(M_*).
It remains an UNMARKED tangent statement. In particular the
new companion directions need not be vertical motions of the actual marks,
nor affine images available at a chosen rational slice. No actual midpoint
event, normalized cylinder flux contrast at the base, full-stratum result,
or illumination claim follows from this dimension bound alone.

## 22. Literature gates for the remaining periodic-point case

The rank>=3 bound in Section21.1 is still not the hypothesis of
the general high-rank classification. Apisa-Wright's high-rank theorem
requires rank>=genus/2+1. For the34frozen sources of genus27..29 this
requires rank>=15,15,16respectively, well beyond the new lower bound3.
The classification cannot be invoked merely because the rank exceeds1. See
[Apisa-Wright, High rank invariant subvarieties, Theorem1.1](https://public.websites.umich.edu/~alexmw/highrank.pdf).

Apisa's genus2 finite-blocking classification is stronger than the
periodic-point finiteness theorem: on a primitive genus2 translation
surface, a regular point is finitely blocked only from its hyperelliptic
partner. See [Apisa, Theorem4](https://arxiv.org/pdf/1710.05505).
However the source has not been reduced to primitive genus2. Section19's
genus2 conclusion used degree>=16 derived from NONPERIODIC all-to-all
blocking. It cannot be reused after replacing that hypothesis by the
periodic case; that would be circular. Nor can one push blocking of a
selected source/target lift down a nontrivial translation cover without
controlling the other endpoints in the target fibers.

Consequently neither theorem currently removes the actual periodic mark
exception. The remaining choices are to identify the relevant orbit
closure with sufficiently strong hypotheses, prove a direct marked-tangent
criterion for this leaf pocket, or construct the required actual one-corner
event. Outside-class covers, arbitrary continuous cycles and merely
nonzero absolute periods still do not satisfy the active goal.


## 23. What the broader exceptional-case review adds, and what is rejected

The independent `pocket-exceptional-review.txt` gives a useful extension
of Section21: the same unmarked orbit closure contains each small rational
slide X_r as well as X_0. Its tangent therefore contains the slide class
at every such r, and a finite-index stabilizer in Aff(X_r) preserves the
relevant local tangent branch. This exposes the affine actions at many
square-tiled parameters, not just at the base, as a possible structural
lever. No orbit enumeration or new cylinder/direction scan has been run.

Here the stabilizer statement is purely unmarked. An affine automorphism
of X_r acts on periods by its Gauss-Manin action together with its real2by2
derivative. It permutes the finitely many local branches of M_*; pass to
a finite-index branch stabilizer. A real-defined complex tangent is stable
under the derivative action itself, so it is stable under the induced
homology action as well. This does not assert that one finite-index group
works simultaneously for infinitely many r, or that the resulting module
is the whole tangent space.

Several stronger assertions in that review are NOT adopted:

- Rank>=2 does not make the generic quadratic-stratum marked-point theorem
  applicable. Section22 states the missing classification hypotheses.
- Periodicity of an arbitrary mark has not been shown to imply another
  halftranslation fold cover through it. The existing fold lemma proves
  fold=>periodic, not its converse.
- Pocket B_0 has physical angle225degrees and one source zero of order4;
  C_0 has physical angle270degrees and two source zeros of order2. Only
  A_0, of physical angle45degrees, has a regular lift. The90degree angle
  at C_0 belongs to the isolated triangle, not the whole room. The
  review's parenthetical assertion that all pocket vertices lift to
  regular points is incorrect.
- At the raw base every primitive integer half-vector, including odd-odd
  vectors, reaches a B/C corner. Actual canonical diagonal offsets are even:
  reflections in x=c,y=c,y-x=2k,x+y=2k preserve A and B individually and
  preserve C as a class. Thus the review's claimed odd-odd exception does
  not apply here. This is the primitive half-time fact already recorded
  in the earlier realization review, not a newly discovered event.
- A fixed event equation e_0+t*e_1=0 with e_0,e_1 in Q[i] and e_1!=0
  can occur only at a real rational t. If e_1=0 and e_0=0, the algebraic
  equation persists for all t; so the blanket claim that EVERY event
  occurs only at rational parameters is too strong. Geometric realization
  and an actual target fiber remain additional requirements.

The reviewer also proposes a marked multitwist cancellation criterion.
Its key prerequisite, a common marked orbit-closure tangent containing
the whole slide and stabilized at rational parameters, needs an explicit
marked field-of-definition justification; the original Wright source
checked here states the theorem for strata with actual zeros. The
unmarked Section21 result alone does not establish this prerequisite.
That marked module calculation is therefore retained as a possible route,
not as a proof that the actual marks move freely.

The remaining bridge is especially important: even generic illumination
along the slice would not by itself supply an admissible one-corner
midpoint event with a nonzero derivative at the raw base. Neither review
has produced that event or an in-class counterexample. The full goal
remains open.


### 23.1 Limit of the later existence review's quotient argument

Review57928 ends without a universal event or an in-class counterexample.
Its proposed half-period reformulations must retain ALL physical-corner
lifts as marked obstacles (Section26), not just actual zeros. Its claimed
absence of all invariant or structural obstructions is too broad and is
not adopted. A trivial W-equivariant quotient on which all chosen
half-turn elements act trivially would only rule out that particular
kind of quotient obstruction. It would not prove membership in the set
of realizable straight events, or exclude other structural mechanisms.

For an elementary outside-class control, the two permutations (12) and
(23) generate a transitive action on three letters, but neither sends1
to3 in a single step. Generated-group transitivity and normal-closure
arguments therefore do not supply a single admissible event. This is an
abstract logical control, not a polygon counterexample. Section9.1
retains the review's precise non-axis multitwist increment as a conditional
lever; existence of the seed and of a detecting increment both remain open.

## 24. Directed fan tree: compulsory mergers between full A fans

This is a cell-topological refinement of `axis-alignment.md`, not a
trajectory-realization theorem. Throughout this section require the RAW
condition: every B/C lattice point belonging to the room is a physical
boundary corner. The earlier axis-alignment theorem allowed smooth B/C
boundary points; that weaker hypothesis is insufficient here.

Cut the room at its interior BC edges as before. The resulting tree has
one vertex per contiguous A-centered fan. At a C point, a particular fan
contains either one triangle (an endpoint C of that fan) or two triangles
(an internal C). The two triangles of the latter occupy a half-plane.
Exactly one of its two BC edges must be a portal: neither would make C a
smooth physical boundary point, and both would make C interior. Both
possibilities violate the raw condition. Thus C has three triangles in
the room. Across the chosen portal, the neighboring A fan contains one
triangle at C. A portal cannot join two endpoint-C fans: their two
triangles would make C smooth. It cannot join two internal-C fans:
C would be interior. Orient each portal from its internal-C fan to its
endpoint-C fan. This orientation is therefore well-defined and unique.

A full fan has eight triangles, four internal C points, no endpoint C,
and hence outdegree4 and indegree0. It is a source of the directed tree.
For any boundary fan, write m for its number of triangles, q for the
number of its two radial boundary edges of type AB, h for its number of
internal C points, and e for its number of endpoint C points. Counting
triangle incidences at C and the two radial fan endpoints gives

    h=(m-2+q)/2,       e=2-q,
    outdegree=h,     indegree<=2-q.                  (24.1)

Here 1<=m<=7 and q is0,1or2. In particular every tree vertex has indegree
at most2. Every indegree2 vertex is a boundary fan with q=0: its two
radial boundary edges are AC, and its physical angle is90,180or270degrees.
Smooth A boundary points are allowed. An outdegree0 vertex can only have
(m,q)=(1,1)or(2,0); these are45or90degree boundary A fans. A45degree
triangular leaf pocket is consequently a sink with indegree1, provided
the room has more than one fan.

Let T be the total number of canonical triangles, V the number of A fans,
I the number of full fans, and D the total number of boundary AB UNIT
SEGMENTS counted at their A ends. Summing (24.1), treating each full fan
separately, and using the tree identity E=V-1 gives

    E=T/2-V+I+D/2,
    T+D+2I=4V-2.                                  (24.2)

D is not the number of merged diagonal physical walls. In particular two
collinear AB segments can meet at a smooth boundary A point and form one
physical wall; their contribution to D is still2. These identities alone
do not supply a lower bound on the physical diagonal-wall count.

Let Z be the number of boundary fans of indegree0, and M the number of
fans of indegree2. Every vertex has indegree0,1or2; summing indegrees yields

    M=I+Z-1.                                      (24.3)

For two distinct interior A marks S,T, the unique undirected fan-tree path
from the full fan at S to the full fan at T MUST contain an internal
vertex with both path edges directed into it. Indeed the first path edge
points forward, and the last points backward because both full fans are
sources. At a forward-to-backward change, both edges enter that vertex.
Thus every mark-to-mark fan path passes through an AC-ended boundary fan
of angle90,180or270degrees. More generally I full fans require at least
I-1 such merger vertices. The fan tree can therefore route a potential
connection through boundary A fans whose two incoming portals do not
force a physical corner contact at A itself.

**Exact finite audit.** `pocket-fan.py` reconstructs triangle incidence,
with no unfolded-surface permutations or trajectory operations. It checks
all56proper contiguous local fan sectors and all34previously frozen raw
rooms. The68full fans and306portals satisfy (24.1)-(24.3); all34actual
mark-to-mark fan paths contain a merger. These are implementation checks
of the proved identities, not a search for events. A focused tools-disabled Opus review accepts the incidence/count proof.
Its suggested optical-routing strengthenings are NOT adopted wholesale:
a path may meet several cuts at their shared B endpoint, and graph routing
does not imply positive-length passage through every intervening fan.
The checker does not trace any optical path. Here AB unit means one
canonical edge of Euclidean length sqrt(2); strict simplicity excludes
pinch vertices. The tree property is the previously reviewed crosscut
theorem in axis-alignment.md. Actual diagonal mirror offsets are even;
the review's assertion that arbitrary integer diagonal offsets preserve
A/B individually is incorrect.

**Exact remaining gap.** A directed portal-tree path is not a straight
billiard path. A merger is not the requested one-corner midpoint event.
These identities neither impose equal half-vectors nor show a nonzero
pocket period defect. Any proposed induction must additionally retain
reflection development, the actual S/T lift labels, and the intrinsic
pi-sector at its single physical corner. In particular a proof cannot
replace the admissible event by an arbitrary continuous walk through the
tree or by the existence of its unique connecting graph path.


### 24.1 Why cutting off a merger is not a raw-room induction

Cut a single BC portal, whose incident fans are directed upstream to
downstream. Locally C has three triangles: two on the upstream side and
one downstream. If the kept component is upstream, its new boundary
angle at C is180degrees. It fails the raw hypothesis. If the kept
component is downstream, its new angle at C is90degrees; it remains raw
precisely when its new angle at B is not180degrees. All other lattice
points are unchanged. The pieces are simple disks by the crosscut
property. Thus deleting a45degree leaf pocket always creates a smooth
non-A point at its C endpoint, exactly outside the class of this goal.

At a merger on the S/T fan path, each incoming cut separates S from T.
The separate components containing S and T are the upstream components
and acquire smooth C points. Neither inherits the two-interior-mark raw
hypothesis. Recombining subroom paths would also have to match their
physical directions, reflection developments and actual lift labels;
matching merely their portal endpoints does not give a straight event.
Capping such a cut with a triangle adds a new mirror and cannot silently
transfer its billiard paths back to the original room.

There is a second obstacle. A primitive integer half-vector based at A
ends at B or C, never at A; every developed corner image is integer.
Therefore the merger's own A vertex cannot be the midpoint of the
primitive event sought here, including when that A is a270degree corner.
Any successful use of merger structure must control its B/C endpoints
or a different physical corner, with the equal-half-vector and sector
conditions retained. The merger supplies a topological separator, not a
candidate midpoint at its A center.

The prescribed cell audit checks all306portal cuts in the34frozen
rooms: every upstream piece has exactly two incident triangles at C,
and every downstream piece has one. Of the downstream pieces,280retain
a nonsmooth B; the other26make B smooth as well. These counts validate
the incidence implementation only; the general cut obstruction is the
local argument above.

This does not rule out every conceivable induction. It rules out direct
application of the SAME raw-room hypothesis to the two pieces after
these cuts. A stronger induction would need explicit boundary scattering
and label data or allow controlled transparent C exceptions, and would
have to prove the gluing step. No such strengthened induction is proved.


## 25. Actual marked periods via an auxiliary branched cover

**Status: main marked-cover argument accepted by focused second Opus
review, with its labeling, orbifold and convergence details incorporated.**
The first review found a zero-period error and a descent ambiguity. The
relative-period correction and uniqueness argument below replace those
parts. No marked freeness or actual-event claim is made.

Take two distinct labeled actual regular lifts s(t),t(t) on X_t, over a
small complex period disk about the raw room. Shrink the disk so both
marks stay regular, distinct and separated from every actual zero. The
marked periods in an integral relative basis are exactly v_0+t*v_1 over
Q[i]. These are inputs from the material polygon/marked period chart.
The base has genus>=2, so n>=1 actual zeros. All their orders are even. Choose a connected double cover branched at exactly s,t.
A character of the punctured surface group sends each branch meridian
to1 in Z/2 and chosen handle generators to0; the surface relation holds
since1+1=0. There are2^(2g) choices, transported over the disk. The
pullback differential on Y_t has genus2g, two SIMPLE zeros at the branch
points, and two unramified even-order zeros over each old zero. Label
the two simple zeros to retain the actual source/target labels.

**Uniqueness removes the decoration ambiguity.** A translation
automorphism fixing a simple zero acts in a normalized uniformizer
omega=w*dw as w->w or w->-w. In the first case it is locally, hence
globally, the identity. Thus the stabilizer of a simple zero in the
translation automorphism group has order at most2. Any deck involution
of the required kind fixes BOTH simple zeros. If two such involutions
existed, their product would act as w->w at the first simple zero and
would be the identity. They are equal. Consequently Y with its two
labeled simple zeros determines a UNIQUE quotient (X,s,t). There is no
other involution through which the same upstairs surface can silently
lose the actual mark labels. Label old zeros compatibly with the deck
pairing, working in the usual finite labeled zero-stratum chart.

**Rational period identification.** Project any relative path upstairs
to X marked at Sigma union {s,t}. Its period is the corresponding
integer linear combination of marked downstairs periods. Conversely a
path from an old zero to a branch mark, or from s to t, lifts to a
relative path between ACTUAL upstairs zeros with the same period.
In particular the difference of the two lifted s-to-t paths is a closed
anti-invariant cycle of period ZERO, not twice the marked displacement.
The displacement is a relative period, never that absolute period.
Rational transfer divided by2 gives

    H^1(Y,Sigma_Y;Q)^tau = p*H^1(X,Sigma union {s,t};Q).

If X has n zeros, the invariant absolute dimension is2g, and its relative
kernel has dimension(n+2)-1=n+1, from n paired zero orbits and two fixed
simple zeros. Total dimension2g+n+1 agrees downstairs. Hence the cover
locus and quotient map have rational homogeneous linear period charts.
The actual lifted slide is vhat(t)=vhat_0+t*vhat_1 over Q[i].

**The two proper maps.** Let D_0 consist of (X,s,t,chi). Work globally on its finite enrichment
D whose objects additionally label the two preimages of each old zero.
A sheet-sign choice sigma in {+,-}^n and its simultaneous opposite give
isomorphic labeled-cover objects via the deck map; equivalently the
finite label fiber is {+,-}^n modulo the diagonal sign. Isomorphisms of
objects must preserve each individual zero label. Thus r below is a
well-defined map on D, not on unadorned D_0. Use the component containing
the actual lifted disk. Before compatible upstairs zero-label choices, the character fiber has
size2^(2g). Adding such labels makes only an additional finite cover.
Thus q:D->the marked base stratum is finite and proper; no exact degree
is asserted after adding those labels. The map r:D->the labeled upstairs
ACTUAL-ZERO stratum is locally a rational linear embedding and, by
uniqueness, is injective. It is also proper onto a closed locus. For this
last assertion, take a smooth convergent sequence upstairs. Its deck
involutions are flat isometries; Arzela-Ascoli gives a limit isometry,
locally a translation off the zeros and holomorphic across them. It is
nonidentity since at a labeled simple zero it acts as w->-w. It cannot
fix a regular point or an even-order zero: at a zero of even order a,
its multiplier must satisfy lambda^2=lambda^(a+1)=1, hence lambda=1,
forcing identity. It therefore fixes exactly the two simple zeros.
Riemann-Hurwitz gives quotient genus g, the two fixed zeros descend to
distinct regular marks, and the other zeros descend in free pairs of
the original orders. The quotient is the required smooth marked base.
This proves closedness and recovery of the cover data on upstairs limits.
For convergence of the covering DATA, transport the isometries to a
common marked smooth chart. Uniformly close maps are homotopic (use any
auxiliary smooth metric on the compact source). Thus eventually the deck
maps have the limit mapping class. Its fixed period subspace is exactly
the local lifted covering locus by the rational period identification,
so the recovered D-points converge to the limit D-point. This proves
properness, not just existence of an abstract limit quotient.

The orbifold automorphisms match too: every label-preserving upstairs
isomorphism conjugates the unique deck involution to itself, hence
descends to a compatible downstairs-cover isomorphism; conversely the
isomorphisms of D are defined by those labeled-cover isomorphisms. Thus
r is fully faithful on orbifold stabilizers as well as injective on
isomorphism classes. A proper injective local embedding with this
compatibility is a closed embedding. One may equivalently use compatible
torsion-free local level charts; no extra regular marked stratum theorem
is introduced.

Let A_tau be the decorated GL orbit closure in D. Since r is a closed
embedding, r(A_tau) is EXACTLY the actual-zero-stratum orbit closure
N_tau of Y_tau. The inverse quotient is unique. Thus A_tau inherits
N_tau's finite local branches and number-field homogeneous period
equations by the rational chart identification. This bypasses the first
review's finite-decoration branch-identification argument entirely.
It uses no marked-stratum field-of-definition theorem.

Apply Wright Theorem1.1 upstairs. At transcendental real tau, every local
number-field equation on A_tau separates its rational coefficients at
v_0+tau*v_1; both coefficients vanish. Therefore the ACTUAL decorated
slide disk lies locally in A_tau. The closed finite-branch line argument
of Section21 extends this to the whole disk in D; this continuation is
done BEFORE descent and retains the same actual marks throughout.
Mutual inclusion now shows A_tau=A_sigma for all small transcendental
real tau,sigma. This common A_* contains the rational/square-tiled base
cover Y_0. Wright Theorem1.1 and Example1.2 give k(N_*)=Q.

Since q is proper, q(A_*) is exactly the marked orbit closure M'_* of
(X_tau,s(tau),t(tau)): limits downstairs lift to convergent subsequences
in D. Its local branches are rational linear images of N_* branches.
Thus M'_* is defined overQ and contains the actual marked slice at EVERY
small parameter. This includes rational slices. At each rational slice,
a finite-index affine subgroup fixes the rational actual marks and the
finitely many tangent branches, so its cohomology action preserves the
marked tangent containing the physical slide direction.

Do NOT assert that forgetting marks maps M'_* onto the entire unmarked
M_* set-theoretically: marked points can collide or hit zeros in limits.
For the argument below define V as the IMAGE of the marked tangent V'
under forgetting, rather than assuming a surjectivity theorem. This
avoids the unnecessary global projection claim flagged by the review.

The simultaneous16-lift version branches at all16actual S/T lifts.
Shrink the disk so all16remain regular, pairwise distinct and separated
from the old zeros; at the raw room they are distinct interior-copy
points, so this is possible. The resulting cover has genus2g+7. All16new simple zeros are labeled and fixed by its deck
involution; uniqueness follows from the stabilizer of ANY one of them.
The same proof applies, and retains the whole physical endpoint fibers.

Primary field input: [Wright, The field of definition of affine invariant
submanifolds, Theorem1.1 and Example1.2](https://websites.umich.edu/~alexmw/numfield.pdf).
The covering construction, uniqueness and period descent above are
separate proof obligations, not statements attributed to Wright.

### 25.1 What this would enable, and what it still does not prove

Let V' be a local branch tangent of the common marked orbit closure and
V its image after forgetting marks. In a rational relative-homology
basis, split marked cochains into

    (absolute cycles, old-zero paths, path to s, path to t).

The forgetting kernel consists exactly of cochains(0,0,u,w). Therefore
a finite exact certificate that a combination of branch-preserving,
actual-label-fixing affine images of the slide tangent has zero first
two blocks but a nonzero last block would prove V' has a nonzero marked
kernel. All classes must be Gauss-Manin transported in the SAME local
system before combining parameters; no arbitrary tangent subtraction is
allowed. Existence of this certificate remains OPEN.

If the marks are both M_*-periodic, their joint marking lies in a
fiberwise union of periodic1-point markings. Its generic fiber dimension
is0. The following local-rank argument handles special branches without
set-theoretic surjectivity. Use a connected smooth immersion component
of a periodic1-point marking P. Its forgetful map is linear in period
charts, so its derivative rank is locally constant on that component,
and therefore constant. By the point-marking property in the introduction
of [Apisa-Wright](https://websites.umich.edu/~alexmw/ApisaWright.pdf),
its image contains M_* minus finitely many lower-dimensional invariant
submanifolds. The constant rank must be dim M_*: a smaller constant rank
would make its countably many local chart images have measure0 in M_*,
which cannot contain that open subset. Since dim P=dim M_* by periodicity,
the forgetful map is locally invertible on EVERY such immersion branch,
including branches over rational special surfaces as long as the marked
point remains regular. The fiberwise product of two such local maps has
zero-dimensional fibers too. The joint marking is locally contained in
this product, hence has zero forgetting kernel. For the16-point version,
repeat with the finite product of the periodic1-point markings.

This argument uses the actual point-marking image property and local
linearity, not the false assertion that a nonproper forgetful map has a
closed image. The main Section25 descent is now reviewed. The second review also
accepts the local cochain kernel and notes that local linear projection
rank removes the special-branch concern; the argument above makes that
rank step explicit using the primary point-marking property. It still
supplies no nonzero vertical vector.

Even successful exclusion of periodic marked pairs along transcendental
slides does not construct a one-corner midpoint event at t=0. Neither
equal primitive half-vectors nor an embedded intrinsic pi-sector follows
from a marked tangent vector. The original actual-event goal remains
open independently of this marked-field reduction.


## 26. Primitive midpoint events as adjacent MARKED cylinder edges

**Status: event/cylinder formulation and midpoint-offset identity
accepted by focused review93263, with the corrections below.** This
reformulates the actual event; it does not prove one exists. Distinguish Sigma_z, the actual zero
set, from Sigma_c, all physical corner lifts, including regular lifts of
45/90degree physical corners. The cylinder decomposition in this section
is relative to Sigma_c, not merely to Sigma_z. In a rational direction,
a regular marked corner on a closed leaf also cuts that leaf into
boundary saddle connections. This marked decomposition is finite because
the base is square-tiled and all these corner marks are rational.

In fact the equal-half and primitive conditions follow from a one-corner
intrinsic-pi connection between the actual A marks. Its first developed
half runs from an even-even integer to an integer corner, so has rational
direction; write its displacement k*w with primitive integer w. If k>1,
the earlier first integer point is B/C and a physical corner. Hence k=1.
After the corner, the endpoint A has displacement l*w with l a positive
odd integer. If l>=3, the point at displacement2w after the corner has
that corner's B/C class and is another physical corner. Thus l=1. This
removes a separate LENGTH-matching obligation once corner-free halves,
the actual endpoint and the intrinsic-pi continuation are established.
Aligning their direction/prong and reaching that endpoint remain hard.

For a primitive integer vector w and an actual regular A lift s, the
open segments from s to developed displacements +w and-w contain no
integer point. Reflection development preserves the canonical integer
lattice and the A/B/C classes. Thus neither segment meets a physical
corner earlier. Its endpoint belongs to B or C and is a physical corner
by rawness. Together they form a marked saddle connection alpha, of
holonomy2w, with midpoint s. Its endpoints may be regular as points of
the unmarked translation surface; stopping at ALL physical corner marks
is essential. This marked saddle connection is unique for the chosen s
and oriented direction w.

An admissible actual s-to-t primitive midpoint event through corner c
is equivalent to the following data: the marked saddle connection alpha
with midpoint s ends at c; a marked saddle connection beta with midpoint
t starts at c, has the same oriented holonomy2w, and is adjacent to
alpha on one boundary side of a w-cylinder. The local intervening sector
has anglepi and is embedded. Conversely those data give the two
half-edges s->c and c->t, each of holonomyw, with no other physical
corner. The target is the supplied actual lift t, not any regular A
midpoint on the boundary. Wall-parallel directions remain excluded for
the opening proposition. A cylinder boundary can contain shorter edges
between physical corners; one must require alpha,beta to be consecutive,
not merely both appear somewhere on that boundary.

A regular midpoint corner c cannot connect distinct physical S,T here:
its folded continuation reverses and retraces, so after the equal second
half it reaches the physical source S. Thus for S!=T the shared corner
is a TRUE zero, although the other endpoints of alpha,beta can be regular
physical corner marks. In particular it is wrong to conclude that every
A mark is a midpoint of a saddle connection between ACTUAL zeros of
length2w. That claim is only valid for the Sigma_c-marked decomposition.

### 26.1 The derivative contains marked midpoint offsets

Orient alpha:d->c and beta:c->e, with holonomy2w at the base. Transport
these classes and the paths d->s and c->t through the material deformation,
without claiming their geodesic representatives stay straight. Define
relative period offsets

    r_s(t)=hol_t(d->s)-hol_t(alpha)/2,
    r_t(t)=hol_t(c->t)-hol_t(beta)/2.

They vanish at0. With eta=path(c->t)-path(s->c), the exact period identity
is

    hol_t(eta)=(hol_t(beta)-hol_t(alpha))/2+r_s(t)+r_t(t),
    delta(eta)=delta(beta-alpha)/2+r'_s(0)+r'_t(0).       (26.1)

This follows by subtracting hol(s->c)=hol(alpha)-hol(d->s).
One may compute it in relative homology with Sigma_c union {s,t}; the
auxiliary d/e boundary coefficients cancel in the displayed combination.
Since c is a true zero, eta itself lies in relative homology with only
Sigma_z union {s,t}, which is the setting of Section25. Fixed PHYSICAL
marks need not stay affine midpoints of the transported whole saddle
connections, so the two r-derivatives cannot be discarded. Moving corner
terms are retained by this identity; they agree with Section3's full
reflection-load formula when all paths use the same material labels.

Thus a corner-only cylinder-edge calculation omitting r_s,r_t is not an
actual-mark detection proof. Section25 supplies a valid common marked
period setting, but does not force the two required adjacent edges or
a nonzero right side of (26.1).

### 26.2 Oblivious-point literature does not supply the missing adjacency

An oblivious point lies on no nonsingular closed geodesic. The primary
papers [Nguyen-Pan-Su](https://arxiv.org/pdf/1712.09066) and
[Adelstein-Desai-Ji-Zdeblick](https://arxiv.org/pdf/2008.08494) concern this
unmarked flat-metric condition. Our parity argument stops at physical
corner lifts, some regular; it therefore does NOT show actual A lifts
are oblivious on X. A path through a regular physical corner can be a
perfectly nonsingular geodesic on X. Branching over all such corner
marks would turn them into actual zeros, but changes the surface and
requires a new descent argument for the selected pi-sector and actual
endpoint labels. Even obliviousness on that different cover would not
by itself say that s and t are consecutive midpoints on one cylinder
boundary. Those papers are relevant background, not an event-existence
theorem for this room class.

The34frozen rooms all have I=2 full fans, no boundary indegree0 sources,
and exactly one merger in Section24's directed tree. This is an exact
read of existing pocket-fan.json, not a search over rooms. Even this
one-merger case needs the actual cylinder adjacency just described;
the cut obstruction of Section24.1 prevents applying the same raw-room
hypothesis independently on the two sides.


### 26.3 Review correction: tangent stability is not slide equivariance

Review93263 accepts the event equivalence and(26.1), but its claim that
shears preserve the scalar opening determinant is NOT adopted. Preserving
the marked tangent SUBSPACE does not assert phi*delta=Dphi*delta for the
particular pocket variation. For the selected base axis multitwists the
reviewed flux/twist proof gives phi*delta=delta instead. Thus

    delta(phi_*eta)=delta(eta),
    hol(phi_*first_half)=Dphi*w,

and the relevant determinant is det(Dphi*w,delta(eta)), which need not
keep its sign or remain zero. The saved seed w=(-12,5),v=(-1,-1) gives
signed rows-17and223after the prescribed horizontal shear48; this is an
existing exact control, no new path. The review's equation with BOTH
vectors transformed would compute a different variation.

Its mod2 observation det(w,v)=0mod2 for odd-odd w,v says EVEN, not ZERO.
An even determinant can become nonzero or change sign under an even
integer shear. Therefore its claim that odd-D detection plus axis
transfer works only at C corners is false. Section5's reviewed
vector-detection-to-both-signs theorem remains valid for B and C events.

The source lift may be fixed by D4 symmetry, but the target ranges over
ALL eight actual T lifts. One successful target lift suffices; failure
for one supplied lift is not a counterexample. Intrinsic-sector corner
fold factors remain counted in Section3, including the moving D/H loads.


### 26.4 Bounded actual-seed existence from the fan tree

**Status: hand proof accepted by independent tools-disabled Opus review
(exit0); local algebra and prescribed segment controls pass.** Let P be a
raw strictly simple canonical room with distinct interior A marks S,T and
W<=26 physical walls. Then there is an admissible connection between the
ACTUAL marks with exactly one physical C corner at its midpoint. Its two
developed halves have the same primitive integer displacement, and its
chosen continuation bounds an embedded intrinsic pi-sector. The direction
is not parallel to a physical wall. This theorem asserts existence of a
seed only: its pocket-slide defect may be zero. No assumption of darkness
or choice of a pocket is needed for this bounded assertion.

Use the fan tree and the charge convention of Sections24 and27.4.
Section27.4 gives W>=10I+2. The two interior marks imply I>=2; W<=26
therefore forces I=2, with S,T the only full A fans. Write P_A for the
number of partial A fans, to distinguish this count from the room P.
The raw identity is W=14+Q, so Q<=12. The partial degree sum gives

    Q>=2P_A-6,                  P_A<=9.                 (26.2)

Keep just the eight full-incident tree edges, their two full vertices,
and all b distinct partial neighbors. This subforest H has c=1or2
components. As in27.4, b=6+c. The two cases are handled below.

**Connected H.** The two full vertices have a common partial neighbor M;
otherwise this two-source forest would be disconnected. There is exactly
one such shared neighbor, since two would create a tree cycle. Portal
neighbors' A centers differ by2 times a cardinal unit vector. The full
spacing lemma27.1 excludes perpendicular incoming center offsets.
Consequently, up to a grid symmetry and translation,

    S=(0,0),        M=(2,0),        T=(4,0).

The two incoming portals must enter M at its opposite endpoint C points,
(1,0)and(3,0). Its contiguous partial fan therefore has m=4,q=0: it is
one of the two half-stars on the S/T line. Reflect vertically if necessary
so that it is the upper half-star. Its internal C is c_0=(2,1).
Rawness forces exactly one portal there, to a partial A fan centered at
(2,2). The three local C quadrants comprise both lower quadrants and
exactly one upper quadrant. Thus c_0 is a physical270degree corner.

The physical broken path is

    S -> c_0 -> T,

with no ordinary mirror hits on either open leg. The first leg lies in
the full S star and the upper-left quadrant of M's half-star; the second
lies in its upper-right quadrant and the full T star. Neither open leg
contains an integer point: their coordinate displacement is(2,1)or(2,-1).
Every physical corner is an integer point, so neither leg hits one.

At c_0 select reflection in its horizontal boundary flank. This flank is
a wall RAY, with direction right if the upper-right quadrant is missing,
and left if the upper-left quadrant is missing. Reflecting T in y=1 gives
T'=(4,2); the developed broken path is S,c_0,T', with both halves(2,1).
The sector must be checked in the actual cone, since this is a boundary
corner reflection, not a straight physical traversal. If the upper-right
quadrant is missing, develop the original physical link as angles
[pi/2,2pi]. The S germ has angle pi+atan(1/2); the T germ in the adjacent
copy across the horizontal ray has angle2pi+atan(1/2). The intervening
arc has lengthpi and stays within the original link plus that adjacent
copy. If the upper-left quadrant is missing, use the horizontal ray atpi
and the adjacent copy on the other side; the analogous interval goes
from atan(1/2)to pi+atan(1/2). It again has lengthpi. Both intervals embed
in the270degree-corner cone of total angle6pi, and preserve the labeled
horizontal-flank gluing. This proves an admissible intrinsic continuation.
The lower-half-star case is its reflection.

**Disconnected H: P_A=9 is impossible.** Here b=8, so P_A is8or9.
If P_A=9, (26.2)and Q<=12 give equality Q=12, with every partial
charge equal to its actual degree. The complete local list of such
partial types is

    m=1,q=1:  in=1, out=0, charge=degree=1;
    m=2,q=0:  in=2, out=0, charge=degree=2;
    m=4,q=0:  in=2, out=1, charge=degree=3.

These follow directly from(24.1)and q_A=m except q_A=3 when m=4.
All partial vertices have positive indegree. Thus the boundary-source
count Z is0 and(24.3)gives exactly I+Z-1=1 vertex of indegree2.
Every partial vertex with an outgoing edge has indegree2, so an incoming
neighbor of this unique merger cannot be partial: that neighbor would
be a second merger. Its two incoming neighbors are therefore the two
full vertices. They share a partial neighbor, contradicting disconnected H.
This rules out P_A=9 without geometric or trajectory enumeration.

**Disconnected H: P_A=8 gives a turning bridge.** All partial vertices
are already neighbors of a full vertex. The full tree has9 edges and H
has8. Its sole additional edge joins a neighbor M of S to a neighbor R
of T. All other six partial vertices have degree1; M,R have degree2.
Orient this bridge M->R, interchanging S,T for this argument if needed.
M has indegree1,outdegree1. Formula(24.1)forces its fan type to be
m=3,q=1 or m=4,q=0. In both types its incoming endpoint C and outgoing
internal C lie on perpendicular cardinal radii. R has indegree2,outdegree0,
so it has m=2,q=0: its endpoint C radii are perpendicular too.

Write the three center displacements as

    M-S=2a,      R-M=2b,      T-R=2d,

with cardinal unit vectors a,b,d. The local facts give b perpendicular
to a and d perpendicular to b, hence d=a or d=-a. The second alternative
would put T-S=2b, forbidden by27.1. Thus d=a. Normalize by a grid symmetry:

    S=(0,0), M=(2,0), R=(2,2), T=(4,2).

M includes its two upper-left triangles, and both triangles at its
internal C c_0=(2,1). R is its lower-right two-triangle quadrant.
The following six FORCED triangles contain the whole segment S->T:

    [S,(1,0),(1,1)],
    [(2,0),(1,0),(1,1)],
    [(2,0),(2,1),(1,1)],
    [(2,2),(2,1),(3,1)],
    [(2,2),(3,1),(3,2)],
    [T,(3,2),(3,1)].

They are portions of the given room, not a claim that their union alone
is a complete raw room. At c_0 the two M triangles occupy both lower
quadrants and the R triangle occupies the upper-right quadrant. The
missing quadrant is upper-left, so c_0 is a physical270degree corner.
The S germ points southwest and the T germ northeast. The angular interval
from pi+atan(1/2)to2pi+atan(1/2), contained in the physical link[pi,5pi/2],
is an embedded pi-sector entirely within one physical copy.

The actual straight segment S->c_0->T has primitive equal halves(2,1)
and no other integer point. Thus it has exactly one physical corner and
no other wall hit. Reversing this segment if the marks were interchanged
retains the actual original S and T. All grid symmetries preserve these
properties. This finishes the bounded seed construction.

**Scope and remaining obligation.** The direction(2,1), and its grid
images, is neither horizontal, vertical nor diagonal. Both constructions
satisfy the one-corner and actual-endpoint requirements of Section1.
They do not imply Q(eta)!=0. In particular a fixed local construction
can avoid the chosen pocket entirely. The universal goal for arbitrary W,
and even detection for W<=26, remain open. No seed is inferred merely
from abstract connectivity: the final two local configurations above
supply the physical or developed segments and the cone sectors explicitly.


### 26.5 Direct actual-endpoint construction from adjacent strips

**Status: conditional hand lemma accepted by independent tools-disabled
Opus review (exit0), with the qualifications below.** This is
an explicit sufficient construction without assuming a pre-existing seed.
It does not assert that the required strip incidences exist in every room.
Use the integer-torus map of Sections9.3-9.5. Choose a primitive integer
vector v and an integer vector u with det(v,u)=1. Cut X_0 along the full
inverse image of the torus v-leaf through0. Each open component is an
annulus covering the base open annulus. In coordinates x*v+y*u its height
is1 and circumference an integer m>0. Boundary walks can visit a singular
vertex several times; retain the specified boundary OCCURRENCES/prongs.

At a specified actual true corner lift p, choose an upper half-plane sector
and a consecutive lower half-plane sector sharing one v-prong. Their union
is an embedded2pi wedge in the local cone. Let their open strips be D_+,D_-,
of respective circumferences m_+,m_-. Use a local lift of p as(0,0)on
each strip. The upper far boundary has y=1; the lower has y=-1. Suppose
a specified actual T lift occurs on the upper far boundary at phase
x=a_t modulo m_+, and a specified actual S lift occurs on the lower far
boundary at x=a_s modulo m_-. The phases are integers because all these
points map to0 in the integer torus. Their physical labels are part of
the premise; an arbitrary A occurrence cannot replace either of them.

For an integer n the two straight halves from p in directions

    -w_n to S,       +w_n to T,       w_n=u+n*v

reach these occurrences exactly when

    -n = a_s mod m_-,           n = a_t mod m_+.       (26.3)

Put g=gcd(m_-,m_+)and L=lcm(m_-,m_+). The congruences have a solution iff

    a_s+a_t = 0 mod g.                               (26.4)

If compatible, all solutions are n=n_0+kL, k in Z. The two open halves
stay strictly between consecutive integer transverse levels. They meet
no point over0, and therefore no other physical corner. Their endpoints
are the specified actual s,t. Since det(v,w_n)=1, w_n is primitive.
The two chosen half-plane sectors contain these opposite germs; their
pi arc across the common v-prong is embedded in the supplied2pi wedge.
Thus reversing the lower half gives an actual admissible one-corner
S->p->T event with equal developed halves w_n.

This local wedge condition is substantive. Arbitrary two strips incident
to the same cone point need not be consecutive; their opposite germs
can be separated by3pi instead ofpi. The selected adjacent occurrences
avoid that mistake. For a regular physical corner the same construction,
if compatible, would return to the same physical source by Section26;
we require a true corner and distinct actual S,T here.

Orient the ordinary absolute strip core classes c_+,c_- along v. They have
periods m_+*v,m_-*v. Let eta_k be the zero-holonomy relative event class
(p->s)+(p->t)for n=n_0+kL, transporting the same material labels for Q.
Increasing n by L adds L/m_+ positive core turns to the upper half and
L/m_- negative turns to the lower half. Consequently

    eta_(k+1)-eta_k = (L/m_+)*c_+ - (L/m_-)*c_-,
    Q(eta_k) = Q(eta_0) + k*D,
    D=L*[Q(c_+)/m_+ - Q(c_-)/m_-].                   (26.5)

The difference is absolute and has zero holonomy. More explicitly take
Sigma'=pi^-1(0), a finite set including p,s,t, and compute first in
H_1(X,Sigma'). Its long exact sequence makes H_1(X)->H_1(X,Sigma')
injective because H_1(Sigma')=0. The closed annulus winding difference
therefore identifies the displayed ordinary absolute class uniquely.
Homotopies on a closed strip may pass through its singular boundary
points; that is permitted for this homology calculation. No auxiliary
boundary point velocity is assigned. Q is evaluated on these ordinary absolute
classes and on the actual relative event with p,s,t labels. Both halves
are allowed to wind within their supplied annuli; this is an exact annulus
homotopy calculation, not an optical search.

If the two normalized fluxes differ, D!=0. At most one k has zero vector
defect. For each of the at most four physical wall-direction lines, at
most one k makes w_(n_0+kL)parallel to that line, since u,v are independent.
Therefore among any six distinct k at least one gives a non-wall-parallel
actual event with nonzero vector defect. Section5's separately reviewed
axis transfer then gives both scalar opening signs. This last step uses
that transfer theorem, rather than claiming the determinant of w_k and
Q(eta_k)cannot vanish for all k on the present single affine line.

Changing the Bezout partner to u+h*v shifts a_t to a_t-h and a_s to a_s+h,
so (26.4)is unchanged. It only reindexes n. Thus the compatibility test is
independent of this coordinate choice.

**Qualifications.** The two selected sectors are allowed to belong to
the SAME annulus.
Then m_+=m_- and c_+=c_- in ordinary absolute homology, so D=0; this
case cannot supply flux contrast. The identity(26.5)is vector-valued in
R^2. Its eta_0 includes the material velocity of p if p is a moving
pocket corner; the absolute increment is unchanged by that fact.

A single actual source lift suffices for physical existence. If a
prescribed source copy is required, the persistent D4 copy automorphism
moves the WHOLE configuration to it and takes Q to its D4 image. If this
symmetry reverses orientation, use v'=-g*v,u'=g*u to restore det(v',u')=1;
this preserves upper/lower and sends n to-n. No actual S/T label is lost.

**What remains universal.** One must prove the existence of an adjacent
strip pair with actual far-boundary S/T occurrences, compatible phases,
and either unequal normalized flux or an already nonzero base defect.
The fan tree does not yet provide these three facts. This is a direct
construction criterion, not a proof of universal seed existence or pocket
detection. When a seed is already supplied and det(v,w)=1, it recovers the
transfer mechanism of Section9.3 in explicit endpoint coordinates.


### 26.6 The shared-neighbor cap pocket is detected directly

**Status: accepted by focused independent tools-disabled Opus review
(exit0); eight prescribed D4 algebra controls pass.**
In the connected-H configuration of26.4, suppose the specified literal
straight-attached one-triangle pocket is exactly the cap attached to M's
internal C c_0. Its A fan is the fan centered at(2,2)in the normalization
there. This extra hypothesis requires that fan to have one triangle and
the literal45/225/270 pocket angles and straight flanks. It is not
asserted for every cap or for another leaf pocket elsewhere in the room.
The local conclusion below needs no wall bound once this configuration
and literal cap are supplied.

The portal of this cap lies on y=1, from c_0 to one of(1,1),(3,1).
A literal slide translates the cap tangent to that line, with velocity
u=(1,0)or its negative, after choosing unit parameter normalization.
The admissible seed in26.4 reflects at c_0 in its HORIZONTAL boundary
flank, collinear with the portal. This supporting line remains y=1
throughout the slide. The vertical cap leg at c_0 is the moving pocket
mirror H; selecting the horizontal flank is essential. The actual
source and target marks remain fixed. Developing the target across this
fixed flank gives T'=(4,2), which is fixed as well; the developed midpoint
is c_0(t)=(2,1)+t*u. The full reflection-load formula of Section3 gives

    Q(eta)=T'_derivative - 2*c_0_derivative = -2*u != 0.

There are no ordinary mirror hits on the two base legs, so there is no
other mirror-load contribution to cancel this value. Splitting the
coincident horizontal-flank reflection on the other side of the midpoint
makes no difference: that reflection has zero translation derivative
and fixes the horizontal velocity u. The target is the ACTUAL T lift in
that adjacent copy, not a newly selected lattice point.

With w=(2,1)and u=(1,0), det(w,Q(eta))=2. Thus the base seed itself has
a nonzero scalar opening row for one sign of the slide. The separately
reviewed axis-transfer theorem supplies the other sign if required,
retaining this nonzero vector defect and the actual endpoint fibers. In the upper-left-missing case, one may instead
develop S across that same fixed flank to S'=(0,2); with T fixed and
corner image velocity u this also gives Q=-2u. The canonical slide direction
maps to the direction from c_0 toward the cap's B; both unit signs are
covered above. All reflected/rotated configurations follow by D4 covariance.

This proves detection for the CENTRAL literal cap pocket of the shared
neighbor configuration. It does not prove detection for a different
literal pocket in the same room, the turning-bridge configuration, or
an arbitrary room. Such a different pocket can leave this short seed
entirely fixed; that is a limitation of this seed, not a counterexample
to the existence of another detecting event. The remaining universal
question is unchanged.


### 26.7 Corridor-side literal leaves: explicit actual detection

**Status: focused independent Opus review accepts the scoped hand proof
(exit0), with its wall/portal and frame corrections incorporated. Exact
checks verify only the three prescribed segment formulas.** This is a
bounded geometric extension of26.6, not universal pocket detection.

First sharpen26.4: P_A=8 for every raw room in its W<=26 scope. If P_A=9,
then sum(q_A)=12 and every partial charge equals its actual degree. The three
equality types listed in26.4 all have positive indegree. Thus Z=0 and
there is exactly one indegree2 partial. The remaining eight partials are
one-triangle degree1 leaves. The unique merger has degree at most3.
The complete degree sum is therefore at most8+8+3=19, whereas the tree
on I+P_A=11 vertices requires20. This contradiction does not depend on
H connectivity. Connected H has seven partial neighbors; P_A=7 is
impossible because its shared M upper half-star has an outgoing neighbor
at(2,2), which is not among those seven. Disconnected H already has eight
partial neighbors. Hence both cases have exactly eight partials.

In connected H normalize S=(0,0), M=(2,0), T=(4,0), with M the upper
half-star. Its only further neighbor is N=(2,2). The complete tree consists
of these two full fans, M, and seven leaves centered at

    (-2,0), (0,2), (0,-2), (2,2), (6,0), (4,2), (4,-2).

Every leaf has indegree1,outdegree0, hence m=1 or2. If r leaves have m=2,
then sum(q_A)=3+7+r=10+r and W=24+r, so r<=2. In disconnected H there are the
M,R bridge and six leaves: M has charge3 whether m=3or4, R has charge2,
so sum(q_A)=11+r,W=25+r and r<=1. These are necessary fan shapes, not an
assertion that every choice embeds as a raw simple room. A consequence is the
unconditional lower bound W>=24 for this RAW class with two interior
A marks: if W<=23, the W<=26 analysis would force W=24+r or25+r,
a contradiction. This says nothing about rooms with transparent B/C
exceptions and does not prove the universal pocket-detection lemma.

Now suppose the specified literal pocket is the one-triangle leaf at
A=(4,2), on the corridor side of T. Its C is c=(4,1), and its B is either
(3,1)or(5,1). The slide translates these three vertices horizontally;
write u=(1,0) for one parameter sign. The line y=1 of the portal and
its fixed flank remains fixed. Denote by L the right leaf centered
at(6,0). Its sole incoming portal is either the upper or lower unit
segment at x=5. All the mirrors in L stay fixed under THIS pocket slide.
The forced region contains the open rectangle(-1,5) x(0,1), since the
full S/T squares and the upper M half-square join along interior portals.

**Upper right portal.** Use moving midpoint c=(4,1). The first leg is
the straight segment S->c, with displacement w=(4,1). It lies in the
forced corridor until its endpoint. Select the fixed horizontal flank
reflection at c. The outgoing physical displacement is(4,-1).
If L has m=2, it is the rectangle[5,6] x[0,1]. The ordinary reflection
at(6,1/2)in x=6 returns the path to the ACTUAL T=(4,0).
If L has m=1, it is the triangle with vertices(6,0),(5,0),(5,1).
Its two fixed mirrors are D_L:x+y=6 and H_L:y=0. The same effective return
in x=6 is realized by the prescribed D_L,H_L,D_L reflections, at

    (16/3,2/3), (11/2,0), (28/5,2/5).

The path enters L at(5,3/4), leaves at(5,1/4), and ends at T. Each
reflection point lies strictly inside its mirror segment. The intervening
segments stay inside the convex triangular leaf or the full T square.
The open first leg contains no integer point, since gcd(4,1)=1. None of
the subsequent open segments contains an integer point or another physical
corner, as the prescribed coordinate checks show. Both descriptions have
developed target(8,2), with c its midpoint and equal primitive halves(4,1).
Indeed D_L H_L D_L is reflection in x=6; composing with reflection in y=1
maps T to(8,2). This use of D_L H_L D_L is in a DIFFERENT, fixed leaf, so
there is no moving-mirror term from those ordinary reflections.

The cone sector at c is checked just as in26.4, now with alpha=atan(1/4).
If the upper-right quadrant at c is missing, the S germ is pi+alpha,
and the outgoing germ across the fixed horizontal flank develops to
2pi+alpha. If the upper-left quadrant is missing, the adjacent copy gives
the interval[alpha,pi+alpha]. Both have length pi and embed in the
6pi cone at this270degree corner. Rawness actually forces B separately in the two upper cases. For an
upper rectangular L, B=(3,1) would leave (5,1) smooth, with90degrees
from T and90degrees from L. Thus B=(5,1), and the upper-left quadrant
at c is missing. For an upper triangular L, B=(5,1) would have
90+45+45=180degrees, also forbidden. Thus B=(3,1), and the upper-right
quadrant is missing. In either case the horizontal ray on the side
opposite the pocket is an actual wall: the other triangle at A=(4,2)
is absent. These are the fixed flanks used in the two cone computations.

**Lower right portal.** The segment x=5,0<y<1 is then a fixed physical
mirror. The literal pocket must have B=(3,1). To see this, if B=(5,1),
T contributes90degrees at B and the pocket contributes45degrees, but
L with a lower portal contributes none: it lies at y<=0. No other
fan in the displayed complete fan shape reaches B. Thus B would have
angle135degrees, contrary to its specified literal225degree angle.

The left horizontal flank(2,1)--(3,1) must also be an actual wall.
The full T fan, M and the pocket already contribute90+90+45=225degrees
at b. If N's portal were on its right side, N would add45degrees
when triangular or90degrees when rectangular, contradicting the literal
225degree angle. Thus N's portal is on its left side; its fan may have
one OR two triangles there. This leaves the required left flank fixed.

Use instead the moving midpoint b=(3,1). The first leg S->b is inside
the forced corridor, with displacement w=(3,1). Select reflection in
the fixed horizontal flank y=1. The outgoing physical displacement(3,-1)
reaches the fixed right wall at(5,1/3), reflects, and ends at ACTUAL T.
Developing T successively across x=5 and y=1 gives(6,2), so b is its
midpoint and both developed halves equal the primitive vector(3,1).
There are no other corner hits: the legs are interior to the corridor
and full T square except for the one prescribed interior mirror hit.

Here b has the physical225degree link[pi,9pi/4]. Put alpha=atan(1/3).
The S germ is pi+alpha in the original copy. Reflect the outgoing T arm
across the horizontal flank with ray angle pi: its developed germ is
alpha in the adjacent copy. The interval[alpha,pi+alpha] crosses that
flank once, has length pi, and embeds in the total cone10pi. Thus this
is the required intrinsic pi continuation, not a3pi one.

**Defect and scope.** All selected corner-flank and ordinary mirrors
have fixed supporting lines during the specified slide. The actual marks
stay fixed. Only the chosen corner translates, with velocity u. In the
source frame the Section3 formula is therefore Q(eta)=-2u in all three
cases; det(w,Q)=2 in this normalized orientation. Every direction used
is neither axial nor diagonal.
Thus the specified literal corridor-side leaf is detected directly.
After reversing an event to restore source naming, the prefix can be
nontrivial: the general source-frame expression is Q=-2 L_p u, not
necessarily -2u in physical coordinates. The fixed-prefix linear map
L_p is orthogonal; under the grid symmetries and reversal below,
nonzero defect and |det(w,Q)|=2 are retained.
Reflection x->4-x and exchange of the actual endpoint names handles the
corridor-side leaf at(0,2). Whole-room vertical reflection handles the
lower-corridor normalization. It does NOT turn an opposite-side leaf in
a fixed upper-corridor room into a case covered here. The opposite-side
leaves, end leaves, disconnected-H pockets, and unrestricted wall counts
remain unresolved. No direction, word, trajectory or room scan is used:
the formulas above are prescribed by the forced corridor and fixed cap
return isometry; the checker verifies only those formulas.


### 26.8 Opposite-side detection and a withdrawn end-leaf attempt

**Status: the opposite-side conditional construction passes independent
focused Opus review(exit0). The proposed end-leaf extension is withdrawn:
its fixed-flank premise is incompatible with rawness, as explained below.**
Retain26.7's connected-H upper corridor. This does not settle all its
leaves, much less the universal goal.

**Opposite-side leaf.** Suppose the specified literal pocket is
A=(4,-2), C=(4,-1), B=(5,-1), and the segment y=1,1<x<2 is a fixed wall.
The last condition says the central N portal is on its right side.
At B the full T fan contributes90degrees and the pocket45degrees.
For the prescribed225degree B, the right leaf must contribute90degrees,
so it is the m=2 rectangle[5,6] x[-1,0]. There is no other possible
contributing fan in26.7's forced center list. The opposite orientation
B=(3,-1)would have only135degrees because M has no lower-half tiles;
thus it is not a literal pocket in this normalization.

The first half is the prescribed path

    S=(0,0) -> (5/3,1) -> B=(5,-1).

The first reflection is in the fixed central flank y=1. Its two open
segments lie in the forced corridor and full T square. Select the fixed
horizontal flank y=-1 at B, with its physical wall ray pointing right.
The second half, with initial physical velocity(5,3), is

    B -> (6,-2/5) -> (16/3,0) -> (11/3,-1)
      -> (3,-3/5) -> T=(4,0).

Its ordinary mirrors, in order, are x=6, y=0, y=-1 and x=3. The first
two hits are in the fixed right rectangle. The third lies in the FIXED
part3<x<4 of T's lower wall, outside the moving portal4<x<5. The fourth
lies in T's fixed left wall below the M corridor. It crosses the right
portal at(5,-1/5), never at an endpoint. Every displayed ordinary hit is
strictly interior to its physical mirror segment. Every open segment
lies in the given rectangles, has noninteger y throughout its interior
or at its isolated y=0 crossing has noninteger x; no further physical
corner occurs.

Unfold the first y=1 reflection. The developed corner is B'=(5,3).
Developing ACTUAL T through the subsequent fixed mirrors, the selected
corner flank and that first reflection gives T'=(10,6). Thus the halves
are both the primitive w=(5,3). The first leg has duration1 at speed|w|;
the second has durations1/5,2/15,1/3,2/15,1/5, totaling1.

For intrinsic legality put alpha=atan(3/5). The physical link at B is
[0,5pi/4], its source germ is pi-alpha, and the selected horizontal-flank
reflection puts its outgoing germ at -alpha in the adjacent copy. The
interval[-alpha,pi-alpha] has length pi and embeds across the fixed ray0
in the total10pi cone. This proves the required pi continuation.
All supporting mirror lines in this event are fixed during the specified
horizontal slide; B' has velocity u=(1,0). Consequently Q=-2u and
|det(w,Q)|=6. The chosen direction is neither axial nor diagonal.

**Withdrawn end-leaf attempt: local rawness defeats the premise.**
The earlier candidate took a literal ONE-TRIANGLE end pocket
A=(6,0),C=(5,0),B=(5,1),
and assumed y=1,2<x<3 was a fixed central wall, meaning N's portal was
on its LEFT side. It proposed first-half reflection at(5/2,1), followed
by the midpoint C and lower-T reflections. The reflected-coordinate
arithmetic gave equal halves(5,2), actual target image(10,4), and a
nonzero frame-correct defect(0,2). This algebra alone did NOT establish
an admissible event in the room class.

Focused review found that its lower hit(7/2,-1) could be a portal rather
than a wall. More fundamentally, a separate local incidence argument
shows that the assumed central wall cannot occur at all with this
literal end pocket. At B=(5,1), T contributes90degrees and the end
pocket45degrees. Literal225 forces the(4,2)leaf to be the upper-right
m=2 quadrant[4,5] x[1,2]. At the DIFFERENT B point b=(3,1), M and T
then contribute90degrees each. That upper-right quadrant contributes
nothing at b. No other leaf from26.7's complete center list reaches b
except N when its portal is on its RIGHT side. If N's portal were left,
b would be a smooth180degree boundary B, forbidden by Section1's raw
hypothesis that every occupied B/C lattice point is a physical corner.
Thus N's portal must be right, and the proposed first reflection point
(5/2,1) is inside that portal. The first half fails before its midpoint.

The proposed end-leaf event is therefore withdrawn as geometric progress,
not repaired by adding a lower-wall assumption. Its exact arithmetic is
retained only as a FORMAL negative-scope control in pocket-opposite.py.
It is not an in-class counterexample to universal detection. In particular
the review's optional two-reflection repair for a lower triangular leaf
would not fix the invalid first reflection. End leaves remain open.

The accepted opposite-side construction in THIS subsection still needs
the stated fixed left-central-flank hypothesis;26.11/26.12 later handle
the other N portal.  Whole-room grid symmetries preserve that
hypothesis; they do not remove it for a fixed specified pocket. Exact
checks verify its prescribed segments and target development. They are
not a room/direction/word scan or a proof of universal pocket detection.
The separate prescribed junction-incidence control checks the rawness
incompatibility above without constructing or enumerating rooms. A focused
independent junction review accepts these local deductions(exit0); its
ring-index correction and explicit diagonal-B query guard are incorporated.


### 26.9 End-leaf detection using its MOVING diagonal flank

**Status: focused independent Opus review12562 accepts this scoped
hand proof(exit0), with corrections incorporated; exact fixed-path and
nonvacuity controls pass.**
Retain26.7's connected-H upper corridor with S=(0,0), M=(2,0), T=(4,0).
Suppose the specified literal upper end pocket is
A=(6,0),C=(5,0),B=(5,1). Its vertical slide velocity is u=(0,1), and its
moving diagonal mirror is D_t:x+y=6+t. Additionally suppose the lower
leaf at(4,-2) uses its RIGHT portal y=-1,4<x<5. This extra hypothesis
is essential. Its alternative left portal is not treated here.

By literal225degrees at B, the upper leaf at(4,2) is the m=2 upper-right
quadrant. As26.8 proves, rawness consequently forces N's right portal.
This new construction does NOT reflect in that portal or assume it a
wall. At the other B point(5,-1), the full T star contributes90degrees,
the specified UPPER end triangle contributes none, and no other fan from
the complete list reaches it apart from the lower leaf. A right m=2
lower quadrant would add90degrees and leave this B smooth180degrees,
forbidden by rawness. Thus the assumed right-portal lower leaf is m=1:

    [(4,-2),(4,-1),(5,-1)].

Its two fixed mirrors are D_-:x-y=6 and V_-:x=4. Their composite
D_- V_- D_- is reflection in y=-2.

The first half is the straight forced-corridor segment S->B, with
primitive displacement w=(5,1), no other corner and no ordinary hit.
At B choose the MOVING diagonal flank D_t, rather than the fixed
vertical flank. At the base it sends incoming(5,1) to outgoing(-1,-5).
The ensuing physical half is prescribed exactly as

    B=(5,1) -> (9/2,-3/2) -> (4,-8/5)
      -> (13/3,-5/3) -> T=(4,0).

It enters the lower triangular leaf at(23/5,-1), uses its three fixed
mirrors D_-,V_-,D_-, and exits at(21/5,-1). Those ordinary hits all lie
strictly inside their mirror segments. Its successive velocities are
(-1,-5),(-5,-1),(5,-1),(-1,5), and durations are
1/2,1/10,1/15,1/3, totaling1. The portions outside the lower leaf are
inside the full T square. None of these open segments meets another
physical corner. The first and second half reach the specified ACTUAL
marks; no boundary A is substituted for T.

Developing ACTUAL T by the fixed lower cap reflects it to(4,-4).
Reflection in the selected diagonal flank then gives

    T'(t)=(10+t,2+t),       B(t)=(5,1+t).

At t=0 the two developed halves are both(5,1). In the original source
frame the complete moving-flank derivative is

    Qeta=T'_derivative-2 B_derivative=(1,1)-(0,2)=(1,-1),
    det(w,Qeta)=-6.

No ordinary mirror term moves under this END-pocket slide. The moving
corner reflection itself DOES contribute and is retained; simply using
-2u would be incorrect. For small t the fixed lower-cap hits remain
away from endpoints. Actual straight connection after opening is governed
by the same local derivative criterion as Section3; the prescribed
base event is what is asserted here.

For intrinsic legality put alpha=atan(1/5). At B the physical link is
[pi/2,7pi/4]: the upper-right quadrant, full T and end triangle together
have225degrees. Its source germ is pi+alpha. The outgoing physical germ
(-1,-5) lies at3pi/2-alpha. Across the diagonal flank ray7pi/4 it
develops to2pi+alpha in the adjacent copy. The interval
[pi+alpha,2pi+alpha] has length pi, crosses that labeled flank once and
embeds in the total10pi cone. Thus this is the legal pi continuation,
not a3pi one. The clockwise pi-continuation at B across the fixed vertical up-ray,
with outgoing(-5,1), is a DIFFERENT choice and is not used here. The
withdrawn26.8 attempt had midpoint C and failed at an earlier portal;
it was not this B continuation.

This conditional case is NONVACUOUS: Section33's prescribed actual W25
room, translated by(4,0), has every stated fan and both marked endpoints.
It also has all its diagonal-direction cylinder loads zero by the
separately accepted scoped proof in33. Consequently
that directional cylinder blindness does not prevent a directly detecting
one-corner event with a moving-diagonal continuation. Whole-room grid
symmetries preserve the conditional construction. Upper end pockets with
a LEFT-portal opposite lower leaf, lower-pointing end pockets in this
fixed upper-corridor normalization, disconnected-H placements and arbitrary
wall counts remain open. Whole-room reflection does not silently cover
the lower-pointing pocket: it also changes M's half-star. The left end
has the corresponding conditional construction by horizontal reflection
and actual endpoint exchange, preserving |det|=6. No direction/word/path/room scan is used.


### 26.10 End-leaf detection with the opposite LEFT portal and fixed S flank

**Status: focused independent Opus review86457 accepts the scoped hand
proof(exit0); prescribed topology/path/development controls pass. The
corner's pi-sector and fixed-flank incidence are HAND-reviewed, not
machine proofs of intrinsic geometry.** The broad hardleaf response supplied this
single candidate. Its interval-family classifications are not used here.
Retain26.9's upper literal end pocket A=(6,0),C=(5,0),B=(5,1),
with u=(0,1), D_t:x+y=6+t and H_t:y=t in that normalization, but now
suppose the lower leaf at(4,-2) uses its LEFT portal, and the S-left leaf
at(-2,0) uses its LOWER portal. These are conditional geometric hypotheses,
not a census or claim to settle other orientations.

Literal end geometry still forces the upper-right m=2 quadrant at(4,2),
and rawness forces N's RIGHT portal. Thus the central top segment y=1,
1<x<2 is fixed. The S-left lower portal makes x=-1,0<y<1 fixed. The
first half is

    S=(0,0) -> (-1,2/7) -> (3/2,1) -> C=(5,0).

Its velocities are(-7,2),(7,2),(7,-2), and durations are1/7,5/14,1/2,
which sum to1. The two ordinary bounces are on those fixed wall interiors.
The entire path stays in S's square, the forced upper corridor and T's
square, and meets no other physical corner. Its prefix development is
V_-1 H_1, giving developed C'=(-7,2) and primitive half-vector(-7,2).

At C choose the FIXED vertical flank x=5 pointing down. Its other half
is

    C -> (3,-4/7) -> (9/2,-1) -> (5,-6/7)
      -> (3,-2/7) -> T=(4,0).

It has velocities(-7,-2),(7,-2),(7,2),(-7,2),(7,2), with durations
2/7,3/14,1/14,2/7,1/7, totaling1. The four ordinary mirrors are x=3,
y=-1,x=5,x=3. All hits are in fixed T-wall interiors: M has no lower
part; the lower leaf's portal is LEFT while the bottom hit has x=9/2;
and the moving end triangle is UPPER while the x=5 hit is below0.
The lower leaf may have one or two triangles; neither lies on the used
right bottom flank. Actual T is attained, not a boundary A point.

Developing ACTUAL T through these fixed mirrors, the selected corner
flank and the two prefix reflections gives T'=(-14,4)=2C'. Thus both
halves are(-7,2). The end-pocket slide has velocity u=(0,1), and the
prefix linear part is -I, so C'_derivative=(0,-1). Every used supporting
line is fixed under this slide. Hence Qeta=(0,2) and det((-7,2),Qeta)=-14.

At C the physical link is[0,3pi/2]. For beta=atan(2/7), the source germ
is pi-beta and the outgoing germ is pi+beta. Across the selected down
flank it develops to2pi-beta. The interval[pi-beta,2pi-beta] has length
pi, crosses that flank once and embeds in the6pi cone. This gives the
specified intrinsic pi continuation. No3pi shortcut or corner deletion
is used.

These hypotheses are nonempty. A second FIXED hand-prescribed raw W25
assembly uses full stars0,0 and4,0, upper M2,0 and these seven leaves:
N2,2 right triangle;6,0 upper triangle(the pocket);4,2 right lower
quadrant;4,-2 left upper triangle; -2,0 lower right triangle;0,2 lower
right triangle;0,-2 upper right triangle. A strict geometry check and
exact supplied-path tile checks verify this one fixture. They do not
enumerate rooms or prove all abstract orientation assignments feasible.

Together26.9 and26.10 treat right opposite portal, and left opposite
portal with S-left lower, respectively. The left opposite portal with
S-left UPPER remains open, as do lower-pointing end pockets in the fixed
upper-corridor normalization and the disconnected-H cases. The full
universal theorem remains open.


### 26.11 Opposite-side detection through an interior physical pi-sector

**Status: focused independent Opus review7074 accepts this scoped hand
proof(exit0); prescribed actual-room/path/affine controls pass.**
Retain26.7's connected upper corridor and specified opposite pocket
A=(4,-2), C=(4,-1), B=(5,-1), sliding with u=(1,0). Literal225 at B
forces the right leaf to be the fixed m=2 rectangle[5,6] x[-1,0].
Assume N's portal is LEFT, the case not covered by26.8. At(3,1), M and
T already contribute180degrees; N-left contributes none. Rawness therefore
forces the upper T leaf's LEFT portal. In this subsection additionally
require that upper leaf to have m=1, namely[(4,2),(4,1),(3,1)]. Its fixed
diagonal mirror is D_+:x-y=2. The m=2 alternative remains outside this
statement.

The first half is

    S -> (7/3,1) -> (6,-4/7) -> B=(5,-1).

The first hit is in the FIXED right-central flank y=1,2<x<3, because N
is left. It then crosses into the right lower rectangle at(5,-1/7),
reflects at x=6 and reaches B. Its velocities(7,3),(7,-3),(-7,-3) have
positive durations1/3,11/21,1/7 totaling1. Prefix development is H_1 V_6,
so B'=(7,3) and the primitive half-vector is w=(7,3).

At B use the STRAIGHT continuation inside its physical225degree link,
not either selected flank reflection. Its ensuing half is

    B -> (4,-10/7) -> (22/5,-8/5) -> (16/5,6/5)
      -> (5,3/7) -> T=(4,0).

The first two bounces use the MOVING pocket mirrors x=4+t and x-y=6+t.
The third is on D_+ in the fixed upper T triangle; the fourth is on the
fixed right T wall ABOVE the right rectangle's lower portal. Velocities
are(-7,-3),(7,-3),(-3,7),(7,-3),(-7,-3), and durations are
1/7,2/35,2/5,9/35,1/7, totaling1. The upper-leaf portal is crossed at
(23/7,1) and(11/3,1); both are interior. The lower pocket portal is
crossed on exit at(29/7,-1), strictly between its endpoints. Every ordinary hit is an
interior point of its actual mirror segment; each intervening portion
lies in the forced corridor, full T star, right rectangle or the specified
two leaf triangles. No extra physical corner is encountered.

At B put alpha=atan(3/7). Its source germ points northeast at alpha,
and its outgoing germ points southwest at pi+alpha. Since alpha<pi/4,
the interval[alpha,pi+alpha] lies strictly inside the physical link
[0,5pi/4]. It is an embedded intrinsic pi-sector in ONE physical copy,
so no flank gluing or3pi continuation is needed at the midpoint.

Retain both moving ordinary-mirror terms in the development. Reading
backward from ACTUAL T gives

    T ->(6,0) ->(2,4) ->(10+t,-4-t) ->(-2+t,-4-t),

under fixed x=5, fixed D_+, moving x-y=6+t and moving x=4+t. Prefix
V_6 then H_1 gives

    T'(t)=(14-t,6+t),       B'(t)=(7-t,3).

Thus the two base halves are(7,3), and the complete actual-relative defect
is Qeta=(-1,1)-2*(-1,0)=(1,1), with det(w,Qeta)=4. The corner itself
has no flank reflection, but its translated position is still included.
Discarding either ordinary moving-mirror term would invalidate this value.
B is also a vertex of the right rectangle. The slide changes only its
bottom-edge length; the used right wall x=6 remains fixed.
N-left may have one OR two triangles. Neither its interior nor any S-side
leaf is used by this construction. Thus the same m=1 upper-T event also
applies at W26 if the second m=2 leaf is N or an S-side leaf.

The conditional geometry is nonempty. A FIXED raw W25 assembly has full
stars0,0 and4,0, upper M2,0, and leaves: N2,2 left triangle; right6,0
lower-left quadrant; the specified lower4,-2 upper-right triangle; upper
4,2 lower-left triangle; S-left-2,0 lower-right triangle; S-upper0,2
lower-left triangle; S-lower0,-2 upper-right triangle. The independent
strict geometry and exact supplied-segment checks apply to this one
prescribed assembly, not a search or orientation census.

**Bounded consequence, conditional on acceptance above.** At W<=25(necessarily W=25 for this pocket type),
a literal opposite-side pocket already forces one m=2 right leaf, so
r=1 in W=24+r. Every other leaf is m=1. If N is right,26.8 applies;
if N is left, rawness forces the upper T left triangle and this subsection
applies. Hence the connected-H opposite-side literal pocket is detected
throughout W<=25. Reflection x->4-x with actual endpoint exchange covers
the other opposite leaf and swaps the N sides. Whole-room vertical
reflection covers the lower-corridor normalization. Orthogonal source-frame
transport and reversal preserve nonzero defect and its determinant magnitude;
see26.7. They do not cover other pocket TYPES. The W26 upper-T m=2
left case is covered separately by26.12, rather than this triangular
formula. Disconnected-H cases and the unrestricted goal remain
open. No claim about all rays or an interval of candidate directions is
used: only the single prescribed construction above is verified.


### 26.12 The opposite-side square cap gives the same target development

**Status: focused independent Opus review69334 accepts the fixed square
construction(exit0);26.11 review7074 and26.7 are also accepted, so the
combined bounded opposite-pocket consequence below is established with
its stated scope. Exact prescribed W26 geometry/segment controls pass.**
Keep26.11's N-left geometry, actual marks, moving opposite pocket, first
half, moving B midpoint and STRAIGHT embedded physical pi-sector. Instead
of a one-triangle upper T leaf on its left portal, let that leaf be the
m=2 quadrant[3,4] x[1,2]. This shape is forced: the alternative
contiguous two-triangle fan across both halves of C=(4,1) would combine
with the full T half-plane to make C interior, forbidden by rawness.
The first two ordinary post-midpoint bounces
remain(4,-10/7)and(22/5,-8/5) on the moving pocket mirrors. Then use

    (22/5,-8/5) -> (3,5/3) -> (22/7,2) -> T=(4,0).

The new ordinary mirrors are the fixed upper quadrant's left wall x=3
and top wall y=2. The corresponding full second-half durations are
1/7,2/35,7/15,1/21,2/7, with velocities
(-7,-3),(7,-3),(-3,7),(3,7),(3,-7). They sum to1. The upper-leaf portal
is crossed at(23/7,1) on entry and(25/7,1) on exit. Each ordinary hit is
strictly interior to its actual wall; the last segment returns to ACTUAL T
inside its full square. Equal primitive halves and the midpoint's pi
legality are unchanged from26.11.

There is a simple reason the same event length and defect survive.
The fixed suffix in26.11 maps T as D_+ V_5(T)=(2,4). The present suffix
maps that SAME actual T as V_3 H_2(T)=(2,4). The two maps need not agree
on the whole plane. They agree on the endpoint that matters, and both
are independent of the pocket slide. Applying the two moving pocket
reflections and the fixed source prefix therefore gives the same

    T'(t)=(14-t,6+t),       B'(t)=(7-t,3),
    Qeta=(1,1),             det((7,3),Qeta)=4.

The raw W25 witness from26.11 becomes a raw W26 witness by replacing
only its one-triangle upper T leaf with this two-triangle quadrant.
The prescribed strict geometry and exact supplied-path controls check
this one assembly. They do not run a room or direction census.

**Combined connected-H opposite-pocket consequence (reviewed).** At W<=26,26.7 gives exactly the displayed fan tree.
For an opposite-side literal pocket, its B must point outward and its
adjacent end leaf must be m=2. If N's portal is right,26.8 supplies the
fixed-flank event. If N is left, rawness forces the upper T left portal;
its leaf has m=1 or2. Sections26.11 and26.12 respectively supply actual
interior-pi events with nonzero full defects. Whole-room grid symmetries
and actual endpoint exchange cover the other opposite-side leaf.
The m=1 event's supporting walls do not change when N or an S-side
leaf is the second m=2 fan. In the m=2 upper-T case r=2 is saturated,
so every other leaf is m=1. Thus this ENTIRE opposite-side pocket type
in connected H is covered through W26. Under endpoint reversal the full
period defect is transported by the orthogonal inverse of the endpoint
development frame, not in general by the fixed-mirror shortcut -2L_pu;
nonzero defect and |det| survive. This consequence does not include end pockets, disconnected H
or larger wall counts, and does not finish the universal goal.


### 26.13 The remaining upper-end orientation uses the source cap

**Status: focused independent review8090 accepts the scoped hand proof
(exit0), with corrections incorporated; prescribed controls PASS.** Retain the connected-H upper-corridor normalization
and upper end pocket A=(6,0), C=(5,0), B=(5,1), u=(0,1).
Suppose Tdown uses its LEFT portal and Sleft its UPPER portal.
The literal m1 triangle pocket forces Tup's right m2 quadrant, as in26.9.
At(3,1), T and M contribute90degrees each, Tup contributes none, and
Nleft would contribute none: rawness therefore forces Nright.
Use26.7's single-unit-portal leaf classification and Section24 throughout; two-triangle
fans spanning both portal sides are excluded by that classification.
The points(1,1) and(-1,1) are odd-odd, hence non-A. At(1,1),
S and M each contribute90degrees while Nright
contributes none; rawness forces Sup's RIGHT portal. Sup may be m1 or m2.
At(-1,1), Sup then contributes none and S contributes90degrees.
An m2 upper Sleft would contribute90degrees and create a forbidden
smooth non-A point. Thus Sleft is the fixed m1 triangle

    [(-2,0),(-1,0),(-1,1)].

Its mirrors D_L:x-y=-2 and H_0:y=0 have composite D_L H_0 D_L=V_-2,
reflection in x=-2. The first physical half is prescribed as

    S -> (-9/5,1/5) -> (-16/9,0) -> (-7/4,1/4) -> B.

Starting with w=(-9,1), its velocities are(-9,1),(1,-9),(1,9),(9,1).
Durations are1/5,1/45,1/36,3/4, totaling1. The three ordinary hits lie
strictly within the indicated fixed mirrors. The first leg enters the cap
through(-1,1/9). After the third hit the path leaves through(-1,1/3), then traverses
the full S square, forced open corridor and full T square until B. Its developed corner is V_-2(B)=(-9,1).

Choose the moving diagonal continuation D_t:x+y=6+t at B. It sends
physical incoming(9,1) to(-1,-9). The second physical half is

    B -> (43/9,-1) -> (40/9,2) -> (37/9,-1) -> T=(4,0).

Its ordinary mirrors are H_-1,H_2,H_-1; durations are2/9,1/3,1/3,1/9,
again totaling1. All these hits have4<x<5. Since Tdown's portal is
LEFT, the bottom RIGHT flank y=-1 is fixed; Tup's m2 RIGHT quadrant
supplies the fixed top y=2. The open legs stay in the full T square
and that upper quadrant. All ordinary reflections are fixed under the
specified slide. No other physical corner is met. No N, Sup, or Sdown
tile is used by this event, so their W26 variations preserve it. Tdown is
used only through the ABSENCE of its right-portal triangle.

The fixed suffix develops ACTUAL T to(4,-8). The moving diagonal sends
this to(14+t,2+t); the fixed source prefix V_-2 then gives

    T'(t)=(-18-t,2+t),       B'(t)=(-9,1+t).

Both developed base halves are the primitive vector(-9,1). Therefore

    Q=Tdot-2 L_P u=(-1,1)-2(0,1)=(-1,-1),
    L_P=diag(-1,1),             det((-9,1),Q)=10.

Frame consistency is essential. In the corner frame the vector/defect
are(9,1)/(1,-1), with determinant-10. Transport BOTH by L_P to the
source frame, preserving the determinant magnitude; do not mix frames.

For intrinsic legality the physical germ entering B points backwards
at pi+alpha with alpha=atan(1/9), and its outgoing germ is3pi/2-alpha.
The physical link is[pi/2,7pi/4]. Reflection across its diagonal end
ray7pi/4 develops the outgoing germ to2pi+alpha. Thus the interval
[pi+alpha,2pi+alpha] is an embedded pi-sector, just as in26.9; it crosses
one labeled moving flank. Its development then transports by the fixed
source prefix. No 3pi continuation is used. The primitive vector(-9,1)
is neither axial nor diagonal, so it is not wall-parallel. Strict ordinary-hit
clearance persists for small |t|. The nonzero determinant opens one slide
sign; Section5 supplies both signs because Q=(-1,-1) has odd components.

A hand-prescribed strict-raw W25 fixture with28triangles, checked in
pocket-end-upper.py/json, proves the hypotheses nonvacuous. The script
checks exact segments, ordinary reflections, unit halftimes and the
stated affine development. The independent hand review checks the
forcing, actual mirror intervals and embedded pi-sector separately.

Together with26.9 (TdownRIGHT) and26.10 (TdownLEFT,SleftLOWER), this
covers every literal m1 UPPER end triangle pocket in the connected-H
W<=26 census. Reflection x->4-x with actual S/T exchange covers the
left end and preserves M's upper half-star. This statement concerns the
specified literal sliding TRIANGLE, not an m2 end square. LOWER end pockets in this fixed
upper-corridor frame, disconnected H and arbitrary room geometry remain
open. No discovery search was run.


### 26.14 A lower-end pocket with an upper-left square cap

**Status: focused hand review31817 ACCEPTS the scoped square event
(exit0), with corrections incorporated; prescribed controls PASS.** Retain the connected upper corridor,
but let the end pocket point LOWER:

    A=(6,0), C=(5,0), B=(5,-1), u=(0,-1), D_t:x-y=6+t.

The specified A-fan is the SINGLE j=4 triangle; D_t is an actual
boundary flank. An m2 end fan falls outside this literal-pocket hypothesis.
Literal225 at B then forces the lower T leaf to be the RIGHT m2 quadrant
[4,5]x[-2,-1]: T contributes90degrees and the pocket45, so the remaining
90degrees must come from that leaf. Additionally assume N's portal is
RIGHT and the upper T leaf is the LEFT m2 quadrant[3,4]x[1,2]. These are
conditional hypotheses, not claimed consequences of the lower pocket.
By26.7's proved seven-leaf count W=24+r, the two m2 leaves saturate
r=2, so this branch is necessarily W26. The smooth half-star center
M=(2,0) has both coordinates even and is an A point, hence permitted
by the raw rule. Non-A smooth integer points remain forbidden.

The prescribed first half is

    S=(0,0) -> (5/3,1) -> B=(5,-1).

Its velocities are(5,3),(5,-3), with durations1/3,2/3. The first hit is
in the fixed LEFT central flank y=1,1<x<2 because N's portal is RIGHT.
The second leg crosses x=3 at y=1/5, inside the upper corridor; after
that it stays in the full T star until B. Prefix development is H_1.
The developed corner is H_1(B)=(5,3), giving primitive half-vector(5,3).

At B choose the moving diagonal flank. It sends incoming(5,-3) to
(-3,5). The second physical half is

    B -> (16/5,2) -> (3,5/3) -> T=(4,0).

It uses the fixed mirrors H_2 then V_3, with durations3/5,1/15,1/3.
Entry to the upper quadrant is at(19/5,1); exit is at(17/5,1).
Both are interior to its LEFT portal. The hits on y=2 and x=3 are
strictly inside their segments. The rest of the half is in the full T
star. These facts exclude intervening walls and corners. Both halves
last1 with equal speed sqrt34; both use the ACTUAL marks.

The suffix develops T by H_2 V_3 to(2,4). Applying moving D_t and the
fixed H_1 prefix gives

    T'(t)=(10+t,6+t),       B'(t)=(5,3+t),
    Q=(1,1)-2(0,1)=(1,-1), det((5,3),Q)=-8.

Only the selected corner flank moves; the ordinary mirrors stay fixed.
The corner velocity above is in the SOURCE frame, after H_1; its
physical velocity is(0,-1). Every ordinary hit has positive clearance,
so its word persists for small |t| under the Section3 opening criterion.

For pi legality write alpha=atan(3/5)<pi/4. The physical link at B is
[pi/4,3pi/2]. The backwards source germ is pi-alpha and the outgoing germ
is pi/2+alpha. Reflection across the diagonal end ray pi/4 develops the
outgoing germ to-alpha. Thus[-alpha,pi-alpha] is an embedded intrinsic
pi-sector crossing that flank once, through the adjacent physical copy.
It does not meet the other end of the link. Transport by the fixed
source prefix preserves this legality. No3pi continuation is used.

**A rejected triangular suffix is retained as a geometric control.**
Replacing the upper square by its j=5 one-triangle fan suggests the formal
suffix D_(x-y=2) V_5, which ALSO maps T to(2,4). Its putative physical
path would hit(7/2,3/2), then(5,3/5). However that intervening segment
crosses the absent tile[(4,1),(4,2),(5,1)]. The actual earlier hit
is its right-leg wall x=4 at(4,6/5), breaking the proposed word.
In fact the formal segment leaves the left
cap through x=4 at height6/5 before crossing the portal y=1. Thus equal
affine endpoint development alone does NOT establish a legal itinerary.
The square-cap result above is valid as a prescribed control; the
triangular alternative is WITHDRAWN and gives no detection result.

The obstruction has an exact cone form that can guide future proofs.
For a half leaving this B with velocity(-b,a), a,b>0, entry into the
upper LEFT cap occurs at q=5-2b/a on y=1. The entry is interior exactly
when1<a/b<2. Its reflection in x-y=2 would return to y=1 at x_exit=1+2a/b;
this is the actual cap exit exactly when x_exit<4. Hence that entire two-leg cap visit stays
inside the triangle exactly when1<a/b<3/2. Equality at3/2 hits the
portal endpoint(4,1), so the bound is strict. Our forced ratio5/3
lies outside that interval. The square supplies the extra room, with
H2/V3 replacing the invalid triangular suffix. These inequalities are
local admissibility conditions, not an exclusion of other actual events.

The supplied checker pocket-end-lower.py/json verifies one raw W26
square fixture, its strict-raw W25 triangle substitution, and the exact
earlier-wall/absent-tile obstruction in the latter. The midpoint
continuation is verified by the independent hand pi-sector argument,
not by the ordinary-reflection checker. The local cone inequality, added after31817, is separately accepted
by focused review57809. It runs no room, ray, direction or word discovery search.
Other lower-end orientations, disconnected H and unrestricted detection
remain open.


### 26.15 A lower-end pocket with its upper T portal on the RIGHT

**Status: focused hand review57809 ACCEPTS the scoped event and26.14
local cone inequality (exit0); corrections incorporated, controls PASS.** Keep26.14's literal LOWER
end pocket, Nright, first half S->(5/3,1)->B, moving diagonal continuation,
actual marks, and source H1 frame. Instead suppose the upper T leaf uses
its RIGHT portal. At(5,1), T contributes90degrees and the lower-pointing
end triangle contributes none. Any allowed right single-portal m2 leaf would contribute
90degrees and leave a forbidden smooth non-A point. The literal end
has no extra j5 tile, and26.7 excludes any additional fan at(6,2). Thus this upper leaf
is the m1 j=6 triangle. No upper-left cap is entered by the path below.

Use the following second physical half, starting with velocity(-3,5):

    B=(5,-1) -> (19/5,1) -> (3,-1/3) -> (17/5,-1) -> T=(4,0).

The mirrors are fixed H1,V3,H_-1; respective durations are
2/5,4/15,2/15,1/5. The first hit y=1 at19/5 is in the LEFT upper flank
of the full T square because the upper leaf's portal is RIGHT. The
second hit x=3 at-1/3 is in the fixed LEFT wall below the upper M
corridor. The third hit y=-1 at17/5 is in the LEFT bottom flank because
the lower leaf's forced m2 portal is RIGHT. All hits are strictly
interior, all intervening segments lie in the full T star, and their
durations sum to1. After B the upper and lower leaf portal SIDES fix these wall intervals;
no leaf interior or S-side leaf is entered.
The first half is unchanged and still legal for every single-portal
Nright size allowed by26.7. Both halves reach ACTUAL S and T.

The new fixed suffix sends T as

    H1 V3 H_-1(T)=H1 V3(4,-2)=H1(2,-2)=(2,4).

Consequently the moving diagonal and source H1 prefix give precisely
26.14's developed endpoint/corner:

    T'(t)=(10+t,6+t), B'(t)=(5,3+t), Q=(1,-1), det((5,3),Q)=-8.

The physical225degree link and embedded pi-sector at B are unchanged
from26.14. Strict hit clearance gives local word persistence. This
statement asserts the base event and full derivative, with opening
conditional on Section3. A prescribed raw W25 fixture verifies geometry,
segments and ordinary reflections; its pi-sector is independently hand
reviewed. The fixture has N m1 and W25; with N m2 the same path is
still valid at W26. The event does not depend on the three S-side leaves.
It is a different upper leaf, not the withdrawn LEFT triangle itinerary.

Use26.7's single-portal leaf classification and r<=2 budget for this
case split. For Nright lower-end pockets,26.14 covers upperTLEFTm2 and this section
covers upperTRIGHTm1. The upperTLEFTm1 case remains OPEN, as do Nleft,
disconnected H and arbitrary larger rooms. No discovery scan is used.


## 27. A90degree merger supplies a reflex B with a local pi window

**Status: local proof accepted by independent tools-disabled Opus
review, with the scope corrections below.** Let U be a merger A fan with m=2,q=0,
physical angle90degrees. It is one canonical unit square, and its two
incoming BC portals meet at the opposite B vertex b. Write a,b' in{1,2}
for the numbers of triangles at that B in the two incoming neighboring
A fans, counting only the contiguous parts meeting this merger.
Each is at least1 because the portal is present, and at most2 because
an A-centered fan can occupy at most90degrees at this B.

If both contributions were1, the merger's two triangles and these two
neighbors would occupy exactly four consecutive45degree sectors at B.
The fourth A quadrant cannot contain triangles without violating the
single contiguous boundary sector there: a missing second triangle of
each neighboring fan separates it from the occupied block. Thus B would
be a smooth180degree boundary point, contrary to rawness. Consequently

    a+b'>=3.

Any extra triangles in the fourth A quadrant only enlarge the occupied
sector, and B cannot be interior BY RAWNESS. Its physical angle is therefore225,
270or315degrees. In particular it is a TRUE zero in the unfolding.
This identifies a real candidate midpoint corner at the merger, unlike
its A center, which primitive parity excludes.

Take angular coordinates about B with the merger quadrant(0,pi/2), the
first incoming fan portion(-a*pi/4,0), and the second
(pi/2,pi/2+b'*pi/4). Opposite prongs theta and theta+pi lie strictly
inside the two incoming portions precisely when

    theta in (-a*pi/4,0) intersect (-pi/2,(b'-2)*pi/4).

That interval has width(a+b'-2)*pi/4:45degrees if one contribution is1,
and90degrees if both are2. The sector from theta to theta+pi through
the merger is an embedded physical pi-sector. It stays inside these
three fan portions. This is a positive-width LOCAL sector window, not
an assertion that the two upstream marks reach its endpoints with equal
half-vectors.

Exact audit: the34frozen rooms contain11right-angle mergers and23smooth
180degree mergers. All11right-angle cases satisfy the B-angle and
window inequalities. The checker also tests the9possible contiguous
local B-sector masks containing the four mandatory sectors and excluding
smooth B. These are local cell configurations, not room enumeration or
trajectory/direction discovery. Both records are in pocket-fan.json.

The remaining matching problem is explicit. The two upstream marks must
have primitive corner-free developments ending at THIS actual B lift,
with opposite incoming prongs in that window and the same developed
primitive direction. Equal length then follows from Section26's
one-corner/actual-endpoint argument; it is not an additional metric
assumption once those requirements hold. Two
individually accessible sectors do not imply this equality. A finite-index
affine group can have several orbits of primitive vectors, so independently
moving the two half-paths does not automatically align them. Pocket
involvement and nonzero defect in(26.1) are further requirements. The
lemma supplies none of those global conclusions and does not yet treat
smooth180degree or reflex270degree merger fans.


### 27.1 Full fans cannot be diagonally adjacent

Two full A fans cannot have coordinate difference(2,0)or(0,2), up to
sign: their common C would have four triangles and be interior, violating
rawness. They also cannot have difference(2,2), up to axis signs.
Translate those centers to S=(0,0),T=(2,2). Every full fan has exactly one
portal through each of its four side midpoints, and the A center across
a portal is the cardinal neighbor at distance2. Therefore BOTH
U=(2,0) and V=(0,2) are fan centers, with edges S-U,T-U,S-V,T-V.
These four edges make a cycle, contradicting the disk fan-tree theorem.
Strict simplicity is used to have one contiguous fan at each of U,V;
allowing a pinch would evade that premise.

Thus distinct full-fan centers have Chebyshev distance at least4 in the
physical integer coordinates. In particular a90degree merger cannot
have BOTH incoming neighbors full: that would place their centers
at opposite diagonal corners relative to the merger. The review's
conditional short event S->B->T for the path S->U<-T therefore has NO
realization in a raw strictly simple room. It must not be reported as
an established short-case construction. All34frozen full-fan pairs pass
the spacing bound, and all11right-angle mergers have at least one
nonfull incoming neighbor.

### 27.2 Scope corrections to the merger review

The local angular window lies inside one physical copy as a STRONG
sufficient way to obtain an embedded intrinsic pi-sector. The definition
of an admissible event requires the intrinsic sector in X, not this
stronger one-copy property. An orientation-preserving affine map takes
opposite prongs and their embedded half-plane to opposite prongs and an
embedded half-plane. It preserves the intrinsic pi-sector and labels
under the already stated finite-index conditions. Its image need not
lie inside one original polygon copy, which is not required. The
review's contrary affine-invariance objection imposes a different
admissibility definition and is not adopted. Affine maps still need
not preserve the pocket slide defect or pocket visit count; only the
previously proved selected-axis transfer has its stated defect invariance.

A primitive continuation from S through this B indeed ends at an A
lattice point after the second half, but I=2 alone does not make it T.
The endpoint may be a boundary A point, including a physical A corner,
or another lift of S. Hence a pigeonhole argument using just the two
INTERIOR A labels is invalid. Landing on the supplied actual T fiber
remains the missing global assertion. When B has angle270degrees it
has TWO unfolded lifts; selecting the actual one is essential as well.


### 27.3 This candidate B is always fixed by a literal leaf-pocket slide

The literal straight-attached pocket has a one-triangle A fan (angle45),
a B corner of angle225, and a C corner of angle270. The B opposite a
90degree merger cannot be that moving B. If its angle is270or315 the
angle already excludes it. If its angle is225, the five mandatory
triangles exhaust its sector: merger2 plus incoming contributions1+2.
There is no occupied fourth-A-quadrant fan. The merger fan itself has
two triangles. Each of the incoming fans has at least two triangles
because it contains an internal C and points OUT through that portal;
a one-triangle pocket fan has outdegree0. Hence none of the three
incident A fans is the one-triangle pocket fan required at the pocket B.
That possibility is excluded too.

Parity also prevents this B from being either the moving pocket A or C.
Therefore its physical velocity under ANY such literal pocket slide is0.
Any detecting event using it must acquire its defect from moving mirror
hits; a moving-midpoint-corner term cannot do the work. The merger review's
caveat about a one-triangle fourth-quadrant pocket at this same B would
raise the angle to at least270, so it is not the225degree B of the literal
straight-attached pocket in this goal. The11fixed merger audits verify
the five-sector exhaustion and absence of a one-triangle fan in that case.

The90degree merger also has outdegree0 by(24.1), so it is a terminal
merger. In the I=2,Z=0 case every other fan lies on one of its two incoming
tree components. A chosen leaf pocket lies in one such component. This
is a useful topological split for a future scattering argument, but it
still does not require an actual billiard half-path to stay in that
component or visit the pocket only once.


### 27.4 Raw-room wall count from the full-fan neighbor forest

**Hand theorem accepted by focused review86855 (exit0), with raw-only scope retained.** For a strictly simple
RAW canonical room with I>=1 full interior A fans,

    W >= 10I+2.

Here the raw hypothesis forbids both interior and smooth boundary B/C
points. It is stronger than the hypotheses of the earlier exception-budget
bounds; do not apply this inequality to a room with transparent exceptions.
In particular I>=3 implies W>=32, and a raw room with two interior marks
and W<=31 has exactly I=2 full A fans: the two distinct interior A marks
provide the separate lower bound I>=2.

Proof. Let the fan tree of Section24 have I full vertices and P partial
vertices. Every full vertex has degree4 and all its neighbors are partial:
its C points require exactly one portal, and a full-full portal would
make C interior. Let b be the number of DISTINCT partial vertices adjacent
to at least one full vertex. Keep just those4I incident edges, the I full
vertices and their b neighbors. This is a nonempty forest, being a subgraph
of the fan tree. If it has c components, the forest identity gives

    4I=I+b-c,       b=3I+c>=3I+1,       P>=b.

No lattice placement enumeration or minimum-spacing argument is used.

For a partial A fan of m canonical triangles, define its standard charge
q_A=m, except q_A=3 for a smooth m=4 fan. Its number q of radial AB ends
is0,1or2. Section24 gives

    d <= (m-2+q)/2 + (2-q) = (m+2-q)/2.

This implies q_A>=d in every case: m=1 requires q=1 and d<=1;
m=2 gives d<=2; m=3 gives d<=2; m=4 gives d<=3=q_A;
and for m>=5, d< m=q_A. (The integer/parity conditions leave ten partial
fan types, all checked by the prescribed local algebra.) Summing over
partial vertices and using full degree4 in the complete tree gives

    Q=sum q_A >= sum_partial d
      =2(I+P-1)-4I =2P-2I-2 >=4I.

Finally the established boundary identity at zero exceptions is
W=2+6I+Q, yielding W>=10I+2. This proves the theorem, subject to the
previously reviewed fan-tree/raw-C incidence and wall identity inputs.

This bound supplies no midpoint event. It does justify the I=2 premise
of the saved-guard portal audit for raw rooms with W<=26 (indeed W<=31).
The sealed core of a literal leaf loses no interior A fan, since the
removed A_0 fan has only one triangle, so its I is unchanged. The core is
NOT raw, and the inequality is never applied to the core itself.

For equality W=10I+2, necessarily P=3I+1 and every partial charge equals
its tree degree. There are then no partial-partial edges. The local table
leaves only m=1 leaves and m=2,q=0 degree2 connectors: a smooth m=4,q=0
fan would have an outgoing partial-partial edge. Thus any equality room
would have I-1 such two-triangle connectors and2I+2 one-triangle leaves.
These are necessary combinatorial conditions; this argument does not
establish that all such abstract trees geometrically embed. In particular,
the earlier spacing restrictions must still be respected.

## 28. All rational-parameter AXIS groups still cannot free the marks

**Status: accepted by focused axis-pencil review16850, with its
pure-multitwist and all-core qualifications incorporated.** Section25 makes rational
slice affine actions available on one actual marked tangent. But its
axis-only version has a uniform obstruction; changing rational slice
does not remove it. This statement concerns that specified generated
module, not the full tangent or all affine directions.

Use one Gauss-Manin chart for the small slice, with actual marks
retained. Write omega_t=x_0+i*y_0+t*(x_1+i*y_1), where all four cochains
are real and rational. Let

    W_R=span_R{x_0,y_0,x_1,y_1}.

Working overR avoids needing a rational shear coefficient. At rational
r all periods/cylinder moduli are rational, so the rational version also
holds, but is unnecessary for this obstruction.

The full pocket-flux argument of Section16 applies at EVERY slice
parameter, not just the raw base: the eight translated pocket triangles
still form an isometric open square. For the core class of EVERY axis cylinder, choose a representative
leaf avoiding the finitely many physical corner and portal-endpoint
positions. If it meets Pi, each visit enters/exits opposite sides in
the same half, with equal portal fields. If it avoids Pi, its flux is
zero because there are no portal crossings at all. A nonconstant closed
leaf cannot be contained in the embedded open square. Thus BOTH real
components of delta vanish on every axis core, including newly thin
cylinders at nonzero r; no conclusion is drawn just from transverse
alignment. At rational r take PURE MULTITWIST powers of the axis
parabolics: fix every cylinder, every directional boundary saddle
connection pointwise, all actual marks and prongs, and the chosen branch. A marked path's twist increment is a sum of complete core
cycles, possibly with integer winding counts at fixed rational-height
marked endpoints. A different point-pushing choice contributes only a small loop around
a regular mark, which is zero in ordinary relative H_1(X,Sigma), not a
residue class in punctured homology. Evaluating delta gives0, so each
such parabolic fixes
x_1 and y_1 as MARKED relative cohomology classes.

If a horizontal parabolic at r has derivative(x,y)->(x+a*y,y), then
phi*omega_r=H_a*omega_r and phi*delta=delta. Consequently

    phi*x_0=x_0+a*y_0+r*a*y_1,    phi*y_0=y_0,
    phi*x_1=x_1,                 phi*y_1=y_1.          (28.1)

For a vertical parabolic with derivative(x,y)->(x,y+b*x), similarly

    psi*x_0=x_0,    psi*y_0=y_0+b*x_0+r*b*x_1,
    psi*x_1=x_1,   psi*y_1=y_1.                        (28.2)

The a,b may depend on r and the label-fixing powers. Nothing requires a
common subgroup or common power at different parameters. For marked
relative classes use the endpoint-level refinement of Section9.2; its
subcylinder cores are homologous to the maximal axis cores, so their slide
flux still vanishes. These formulas
show W_R is invariant under EVERY one of these transported axis actions.
Their real module generated from the real/imaginary parts of the base
differential and actual slide is contained in W_R, and the module generated from delta alone is fixed.

Forgetting actual marks is INJECTIVE on W_R, already after projecting
to absolute periods. Evaluate the four cochains on the two fixed cycles
A,B of periods(-2,0),(0,-2), the changing cycle C of Section17 with base
period(p,q) and derivative(0,2), and its quarter-turn image R C. Physical
copy quarter-turn symmetry persists throughout the polygon slice, so
period(R C)=i*period(C) and its derivative is(-2,0). The evaluation matrix
with columns x_0,y_0,x_1,y_1 is

    [-2,  0,  0, 0]
    [ 0, -2,  0, 0]
    [ p,  q,  0, 2]
    [-q,  p, -2, 0].

Its determinant is16, independently of p,q. Thus no nonzero element of
W_R (or its complexification) vanishes on all absolute cycles. In particular no finite combination
of iterated axis affine images, even mixing arbitrarily many rational
slice parameters, can produce the marked-only vector required by
Section25.1 from these four starting cochains.

This does NOT say V'=W_R complexified, that other affine directions preserve W_R,
or that the marks are periodic. It rules out the axis-pencil generated
module as a freeness certificate. A new direction/action or a direct
actual-event construction remains necessary. It also does not prevent
a supplied event from pairing nontrivially with delta and being converted
to both opening signs by the original base axis shears of Section5.






## 29. Sealing the pocket: a one/two-visit reduction

**Status: accepted by focused review56531 (exit0), with the supplied-connection and portal-avoidance hypotheses retained.** Let P^- be the
room obtained by deleting the triangular leaf and sealing its portal
with the vertical segment B_0C_0. The remainder is connected. Both marks
stay interior. The only new smooth non-A lattice points are B_0 and C_0;
all other B/C points in P^- remain physical corners. All mirror lines
still have the canonical even integral reflection translations.

Consider a finite ordinary billiard connection in P^- from S to T,
with no physical corners and non-wall-parallel direction. Stop at its
first T and start at its last preceding S. This gives a connection
without internal occurrences of either endpoint. A smooth boundary point
q in ANY D4-direction room can then occur at most twice. To prove this,
record its incoming physical velocities. They lie in the8-element D4
orbit of the initial velocity. Exactly four point towards the wall.
The involution

    K_q(v)=-R_wall v

pairs those four incoming states in two pairs. If a later q visit has
the SAME incoming state as an earlier one, deterministic billiard flow
is periodic from there and cannot first reach T later. If it has the
K_q state, the reflected outgoing velocity is exactly minus the earlier
incoming velocity. Its subsequent path reverses the earlier S-to-q
history and reaches S before T, also impossible. Thus at most one state
from each of the two pairs occurs, proving the bound2. No interior
source recurrence or corner ambiguity is allowed in this argument.

There is a sharper canonical-grid bound at a smooth C point q. Write
the developed S-to-T vector as2n*w with primitive integer w; the factor
2 follows because both marks are even-even and every reflection has
even integral translation. A q hit is at an integer multiple of w,
necessarily an ODD multiple, with C parity. Consequently all developed
images of this particular q have the SAME coordinate-parity subtype.
Since q is mixed-parity, their copy matrices all have the same
axis-swap bit. Physical incoming velocities at q therefore have only
one assignment of |w_x|,|w_y| to horizontal/vertical components. At a
fixed axis wall, the inward states are just one K_q pair. Hence q occurs
at most ONCE. A C point cannot lie on a canonical even-offset diagonal
wall; this covers all its possible smooth walls.

Apply this to P^-. Its ordinary connection must pass a transparent
endpoint: every ODD developed integer step is B or C. If w is odd-odd,
all those steps are B and must hit B_0; the connection cannot visit C_0.
If w has mixed parity, they are C and must hit C_0; it cannot visit B_0.
There are n such odd steps before the developed target2n*w. Therefore:

- A C_0-using reduced connection has n=1, one C_0 hit, and total vector2w.
- A B_0-using reduced connection has n=1or2, one or two B_0 hits, and
  total vector2w or4w. In the two-hit case the hits occur at w and3w;
  the intermediate A point is at2w.

This is a reduction of SUPPLIED ordinary connections, not an existence
theorem for them. If I=2, the intermediate A in the two-hit case is a
smooth boundary A point: it cannot be an interior A other than S,T,
and those were removed from the path interior. If Z=0, it lies on an
axis wall, since a smooth diagonal A fan has q=2 and is a forbidden
boundary indegree0 source.

### 29.1 The necessary portal-avoidance condition

Sealing changes the billiard map on the OPEN portal, not just at its
endpoints. Thus a P^- connection does NOT automatically give a path in P.
For the following consequences require that the supplied path has no
reflection on the open segment B_0C_0. All its reflections then use
common actual walls, except its hits at the selected endpoint. This
portal-avoidance assumption is a real remaining obligation. An affine
map of the sealed unfolding need not preserve the portal cut arcs and
cannot silently be used to remove this condition.

If such a path has only one endpoint hit, it becomes an admissible
one-corner event in P. Its corner pi-sector crosses the fixed vertical
flank (the original smooth-wall reflection), not the moving D/H wall.
The developed full word uses only fixed mirrors, so

    Q(eta)=-2*L*u,       u=(0,-1),

an axis vector. It is nonzero; the non-wall-parallel direction makes its
scalar row nonzero as well. Section5 gives both opening signs by base
axis transfer. This includes EVERY C_0-using portal-avoiding connection.

For B_0 two-hit connections, simply identifying the two occurrences of
B_0 and deleting the intervening loop does not always give a legal
pi-sector. The two reduced incoming states must have swapped coordinate
assignments: equal/opposite-K states were excluded above. Normalize the
first sheet toI and let its physical incoming vector be(p,q), p>0,
q!=0, |p|!=|q|. The second incoming vector is(|q|,eps*p), eps=+1or-1.
The cone at B_0 has angle10pi. Put its I-copy physical wedge between
pi/4and3pi/2. Its8copies have width5pi/4 each, alternating orientation,
with sheet labels I,V,VD,VDV,-I,-V,(VD)^3,(VD)^3V.
An exact local angular computation for the would-be shortcut gives:

| sign(q) | eps | directed arc / pi | smaller arc / pi |
|---|---|---|---|
| + | + | 7 | 3 |
| + | - | 3 | 3 |
| - | + | 9 | 1 |
| - | - | 3 | 3 |

Thus only the(-,+)case supplies an intrinsic pi shortcut in this
normalization. It crosses the moving D seam at B_0. Its two open halves
still use only common fixed walls; the load is

    Q(eta)=L*(a_D-2u)=L*(1,1),

which detects in a non-wall-parallel direction. The other cases give
3pi/7pi sectors, explicitly excluded by the goal. Their equal vectors
and actual endpoint are not enough. The table is local cone algebra,
not a discovered optical path or an in-class counterexample.

A portal-avoiding B_0 path still opens for small NEGATIVE t even in a
3pi-shortcut case: B_0(t) moves up, so all old endpoint reflection points
lie below it on the unchanged vertical flank. The fixed P^- polyline
is then an ordinary legal P_t path. The analogous C_0 single-hit path
opens for positive t. Finitely many other reflection points have positive
clearance from the old closed portal and stay legal for small parameters.
This one-sided argument alone does not satisfy the one-corner goal.

### 29.2 Why an open-seal reflection cannot persist locally

This is a local obstruction to using an arbitrary sealed connection as
an opening certificate; it is not an obstruction to a different connection.
Let q be a point of the OPEN segment B_0C_0. It is an interior point of P,
so a closed disk of some radius r>0 about q lies in the interior of P.
After reducing r and the slide interval, the same disk lies in every P_t.
A transverse reflection at q in P^- changes a nonzero normal component
of the velocity. Its two germs therefore form a genuine kink.

No sequence of unit-speed ordinary billiard paths in P_t can converge
locally uniformly, with the reflection time fixed, to this kink as t->0.
On a short time interval about that time, uniform convergence would keep
the approximating paths inside the common free disk. They have no wall
hit there and hence are straight affine functions of time. Their uniform
limit is also straight, contradicting the kink. This rules out local
persistence even if a different reflection word is proposed nearby. It
does not rule out unrelated P_t connections elsewhere in phase space.

The already prescribed DHD pocket return does not implement the sealed
mirror. In global coordinates,

    V_seal(x,y)=(2-x,y),
    (D_t H_t D_t)(x,y)=(4-x,y),
    (D_t H_t D_t)-V_seal=(2,0).

For an entry at (1,y) with velocity proportional to (1,m) in the DHD
return branch at t=0, its exit is (1,y+2m) with reflected velocity proportional
to(-1,m). The branch requires 1<y+2m<2, together with the exclusions in
Section2. A sealed reflection instead turns at the original (1,y).
Thus replacing the sealed mirror with the unchanged-return branch
introduces both a travel interval and a tangential displacement.

More generally, take a supplied fixed sealed word with r open-seal
reflections. FORMALLY replace each such factor by DHD, assuming nothing
about geometric realization. Their linear parts agree. If L_j is the
product of linear parts preceding that sealed factor in the development,
the target image changes by exactly

    Delta V = 2 sum_(j=1)^r L_j (1,0).

This is ordinary composition of affine maps with identical linear parts.
The final D4 copy label is unchanged because the linear parts agree;
the developed target lift can nevertheless shift by this absolute period.
Even if the sum vanishes, legal branch inequalities and absence of new
corner hits still need proof. An even integral shift does not make the
old straight segment reach that new developed endpoint. This
calculation explains why a formal return-map substitution cannot remove
portal avoidance from Sections29-30.

### 29.3 Bounded-wall sealed-core existence from the prior k<=3 result

**Corollary accepted by focused review26170 (exit0), with inherited
computer-assisted premises explicitly bound below.** The report
`../../three-triples/three-exception-complete.md` and its composition JSON
state that a strictly simple canonical room with distinct interior A
marks and at most3transparent B/C exceptions is illuminated whenever
W<=23. This is the earlier computer-assisted family result, with its
stated finite-reduction, exact-guard and CP-SAT qualifications; it is not
a new computer search or a new analytic proof of that theorem. Its scope
explicitly includes smooth-boundary B/C exceptions. Its W counts maximal
straight walls: the independent model `../../claude-illumination-check/claude_relaxed_replay.py`, vertex_table, assigns corner=0 to a180degree
fan and sums only corner indicators. These checks discharge the review's
H1 (smooth exceptions allowed) and H2 (smooth points do not split walls).

Deleting this literal pocket removes exactly ONE canonical triangle.
The fan tree regards it as a leaf, so its deletion leaves a connected
strictly simple disk, with S,T still interior. At B_0 the boundary angle
changes from225to180degrees; at C_0 it changes from270to180degrees.
The45degree A_0 vertex disappears. All other B/C points keep their
original nonsmooth boundary status. Thus the sealed core has exactly
TWO transparent B/C points, both smooth boundary points; it has no
interior B/C points.

The original local boundary has four maximal wall pieces: the lower
vertical flank, D, H, and the upper vertical flank. In the sealed room
these become one straight vertical wall. Their far endpoints and all
other corners are unchanged, so

    W(P^-)=W(P)-3,       k(P^-)=2.

Consequently, if W(P)<=26, the inherited k<=3 exclusion supplies an
ordinary actual S-to-T connection in P^-. This conclusion is about the
specified pair; it does not substitute an arbitrary A point. There is
no restriction to exactly two full A fans.

For applying Section29, its direction can also be shown NOT wall-parallel.
This last claim has an elementary proof independent of the computer bound:

* Axis directions: their primitive vector is a coordinate unit vector.
  Every odd developed lattice step must hit the only transparent C point,
  C_0. A legal axis hit on its vertical smooth wall is normal, and reverses
  the entire preceding path. It cannot connect distinct S and T after
  truncation at first T and last S. A tangential wall approach from the
  interior is impossible without an earlier corner.
* Diagonal directions: the D4 orbit consists of four diagonal velocities.
  At smooth vertical B_0 the two incoming states form a single K-pair, so
  the reduced path visits B_0 at most once by the Section29 reversibility
  argument. Every odd developed lattice step is B; hence its full vector
  must be2w with w=(+/-1,+/-1). Each primitive half has no reflection in
  its open interior. Indeed a unit diagonal between integer vertices
  crosses no integer axis mirror in its interior, and it meets no
  transverse canonical even-offset diagonal mirror there. A parallel
  mirror glide cannot start at an interior mark. Thus the two physical
  halves are direct diagonals meeting the vertical wall at B_0.
  Since the core lies to the left of that wall near B_0, the source and
  target would be (0,0) and(0,2), in either order. Their two full A stars
  jointly contain a neighborhood of C=(0,1), making this C an interior
  point of the original room, contrary to rawness.

Therefore every supplied reduced core connection in this bounded range
falls into the NON-wall-parallel B/C dichotomy of Section29. This removes
the existence obligation for W(P)<=26, using prior computational evidence.
The separate OPEN-PORTAL avoidance obligation remains entirely unproved.
For W(P)>=27 even core illumination remains an additional question.
This corollary neither proves the universal goal nor supplies a one-corner
certificate in the two-B 3pi cases.

## 30. Candidate two-corner opening mechanism for the remaining B case

**Status: conditional two-sided opening accepted by review56531; distinct from the active one-corner objective.** A
portal-avoiding two-hit B_0 connection becomes a generalized P path with
two intrinsic pi continuations at the SAME B_0 zero, at developed times
w and3w, and actual target at4w. It has no other physical corners.
Each continuation uses the fixed vertical-flank fold. Define relative
zero-holonomy classes

    E_1=gamma-4*gamma_1,      E_3=3*gamma-4*gamma_3,

where gamma ends at actual T and gamma_j ends at the j-th developed
corner occurrence. With the all-fixed-mirror word,

    delta(E_1)=-4*L_1*u,     delta(E_3)=-4*L_3*u.

The two incoming states swap coordinate assignments, so these are
nonzero ORTHOGONAL axis vectors. Base axis multitwist powers fixing all
corner/actual endpoint labels preserve delta on ALL relative classes
by the axis-core flux argument, while taking w to A*w. Each local
opening row, up to a fixed positive factor, is

    ell_j(A*w)=-sigma_j*det(A*w,delta(E_j)).

These two forms are independent coordinate forms. Use arbitrary INTEGER
powers, including inverse powers: inverses retain label/prong fixing and
cohomology invariance. Any prescribed quadrant for A*w is attained by a
horizontal power followed by a vertical power: first choose the sign of the horizontal component, then
that of the vertical component. Avoid the finitely many wall-parallel
choices. Thus both rows can be made to have the opening sign for
positive t, and both can also be made to have the opening sign for
negative t, with two supplied affine-image generalized paths.

The finite-word opening proposition applies to TWO selected pi-sector
visits to the same cone: strict local inequalities at both visits suffice
by the local proposition below, subject to its precise finite-itinerary
hypotheses. Focused review56531 independently accepts this extension. Distinct visits
need not have disjoint images on the surface. This gives conditional
two-sided local illumination
from a two-corner certificate even when deleting its loop gives3pi.
It still does NOT construct the required one-corner event or refute its
universal existence. Keep the original goal open. No sealed connection,
affine word, direction or ray is discovered or enumerated here.


### 30.1 Finite multiple-corner opening proposition

**Local proof; the finite-visit extension is independently accepted in seal review56531 Section5.** Fix a finite
source-to-target generalized geodesic on the base unfolding. Its only
physical-corner encounters occur at distinct parameter times
0 < lambda_1 < ... < lambda_m < 1. At every encounter choose a labeled
embedded intrinsic pi-sector bounded by the two geodesic germs. The
source and actual target are regular; all other crossings are transverse
to the prescribed mirror seams and avoid every physical-corner label.
The initial direction is not parallel to a wall. Keep this finite
itinerary and each selected sector fixed under a sufficiently small
fixed-angle deformation.

Use the initial source chart and write V(t) for the developed target
relative to the source, C_j(t) for the developed corner at visit j.
At the base, C_j(0)=lambda_j V(0). Choose sigma_j so that displacement
of the proposed straight segment into the selected half-plane is
expressed by

    f_j(t)=sigma_j det(V(t), C_j(t)) < 0.

The precise sign is fixed by the chosen half-plane in that local
chart; it is not inferred solely from the physical corner's angle.
If every f_j'(0) is strictly negative, the same developed straight
segment gives an ordinary actual source-to-target connection for all
sufficiently small positive t. Reverse all derivatives for negative t.

Proof: choose pairwise disjoint small intervals in the PARAMETER of the
base path around its corner visits, and small intervals around its
ordinary seam crossings. On the complement, compactness and the finite
corner-label set give positive clearance. At an ordinary crossing,
transversality preserves the crossing and its order. Near a corner,
cut the local cone outside the selected pi-sector. The selected sector
develops injectively as a half-disk. The base path lies on its diameter;
the strict determinant inequality moves the nearby segment into the
chosen half-disk and misses the vertex. The corner's longitudinal
projection stays inside its chosen parameter interval, and the two
ends stay close to the original ends. Since its direction is separated
from the finitely many seam directions, it crosses the intervening
seams transversely in the prescribed order. Shrinking the deformation
interval handles every one of these finitely many conditions at once.
The endpoint remains the specified actual target lift by construction.

The parameter intervals must be disjoint; their IMAGES need not be.
Repeated visits to the same physical corner, or even the same zero of
the unfolding, impose separate local inequalities. Surface paths may
self-intersect, so overlap of these images is not a further exclusion.
This argument does not use disjoint prong sectors at repeated visits.
It asserts sufficiency for the supplied finite itinerary, not existence
of such an itinerary.

For Section30, V(0)=4w and C_j(0)=jw, j=1,3. Differentiation gives

    f_j'(0) = -sigma_j det(w, j V'(0)-4 C_j'(0))
             = -sigma_j det(w, delta(E_j)).

Thus the two orthogonal defect vectors really give the two local rows
used there. Any further optical hypothesis must enter through existence
and portal-avoidance of the supplied sealed connection, or through the
previous affine-event transfer premise; it cannot be dropped from this
local proposition. In particular this proposition does not provide a
one-corner midpoint event.


## 31. Literal-pocket localization at four zero-period necks

**Status: accepted by independent focused tools-disabled Opus review
(exit0), with the material-neighborhood qualifications below.** This concerns ABSOLUTE slide cohomology and a specific pair
of neck classes. It supplies neither an actual event nor a nonzero pairing
for the actual event module. Actual relative endpoint terms remain separate.

Let R be the persistent copy quarter-turn of Section12, so X/<R> is a
sphere. The branch points are the physical polygon corners on its real
oval. At a canonical corner of angle m*pi/4, the local monodromy exponent
of the C4 cover is m mod4. One can see this directly from the quartic
quotient differential: its order is m-4. In a local root coordinate its
canonical fourth root has monodromy i^(m-4)=i^m. The cover has four sheets
at odd m and two-sheet local ramification at m=2or6. All full interior A
marks are regular nonbranch points of this sphere map.

The literal pocket's consecutive physical corners B_0,A_0,C_0 have
m=5,1,6 and therefore exponents1,1,2. Choose a disk D in the quotient
sphere enclosing exactly these three branch points and a collar of the
pocket, with boundary avoiding all actual marks and other branch points.
For a sufficiently small epsilon, take an intrinsic epsilon neighborhood
N of the closed pocket in P. Strict simplicity, finitely many other
corners, positive flank lengths, and positive separation from the actual
marks let N be a disk meeting the physical boundary in one arc containing
exactly B_0,A_0,C_0. Doubling N ALONG THAT PHYSICAL-BOUNDARY ARC gives D;
its remaining internal crosscut doubles to boundary D. The collar meets
the rest only in fixed charts. Work with |t|much smaller than epsilon. The preimage U is connected because its branch
monodromies generate C4. Their sum is0mod4, so the preimage of boundary D
has four components b_0,...,b_3, cyclically permuted by R. Orient them as
boundaries of U. Riemann-Hurwitz for surfaces with boundary gives

    chi(U)=4-(4-1)-(4-1)-(4-2)=-4,
    2-2g(U)-4=-4,             g(U)=1.              (31.1)

Thus U is a genus1 subsurface with four boundary circles. Its complement
Y contains all actual S/T lifts. U and Y can be transported in the same
material topological chart through the small pocket slide. Choose the
collar boundaries away from the moving mirrors and their endpoints.
For a precise material identification choose N' compactly inside N
relative to P, still containing the closed pocket and its three vertices.
Choose a smooth PLANAR cutoff phi, equal1 on a Euclidean neighborhood
of the closed pocket and supported so that its intersection with P lies
in N. Make phi=1 on N', phi=0 outside N relative to P, and even in the
normal coordinate near the two transition flank segments. Its Lipschitz
constant below is Euclidean, not intrinsic. Put
h_t(p)=p+t*u*phi(p). For |t|Lip(phi)|u|<1 this is a bi-Lipschitz
orientation-preserving map. It translates both moving mirrors and their
vertices, maps the two straight flanks along the same line, and fixes all
other boundary pieces. It therefore maps P to P_t. Apply it copywise;
it respects every mirror gluing and commutes with R. On the complement
of U the pulled-back differential is literally the old differential.
This material marking agrees with Gauss-Manin on the contractible
parameter interval. Outside U all supporting mirrors crossed by a path
are fixed. The material coordinates are fixed too. Consequently
both slide cochains x_1,y_1 restrict to zero in H^1(Y;R): every closed
period represented in Y has derivative0. This is a localization assertion
about the literal slide, not arbitrary deformations with the same angles.

By the long exact sequence, excision and Poincare-Lefschetz duality, their
absolute Poincare duals xi,psi belong to image[H_1(U;R)->H_1(X;R)]. The
persistent R action gives R_*xi=psi, R_*psi=-xi. Use Section21.1's
independence and cup computation: xi,psi are linearly independent and
have intersection0. These are established inputs, not a fresh inference
from the period span alone.

Write L_boundary for the span of the four oriented boundary circles in H_1(U).
It has dimension3, with sole relation sum b_j=0. The quotient

    H_1(U;R)/L_boundary

is the two-dimensional symplectic handle space, and its induced R action
squares to-Id. To justify the latter, U/<R^2> is the double cover of D
with branch exponents1,1,0 modulo2. It is an annulus: chi=2-1-1=0 and its
boundary has two components. Hence H_1(U)^(R^2) has dimension1, already
accounted for by the invariant boundary class b_0+b_2=-(b_1+b_3).
There is no invariant handle vector. The invariants statement uses the
usual real transfer for a finite branched surface quotient; branch points
can be included in an equivariant cellulation and averaging is exact.

Choose an R-equivariant lift of xi,psi to H_1(U), possible by averaging
over the finite group. More concretely, first project any lift of xi by
(I-R_*^2)/2 and call it a; then R_*a lifts psi and R_*^2a=-a. On the
handle quotient, a and R_*a are linearly independent unless a projects
to0, because R_*^2=-Id there. In a two-dimensional symplectic space,
independent vectors have nonzero intersection. But their intersection
in U equals the intersection of xi,psi in X, which is0. Therefore a has
zero handle projection and belongs to L_boundary. Its R-rotated lift does too.
The slide duals therefore lie in the image of the antisymmetric neck plane

    L_- = span{b_0-b_2, b_1-b_3}.                  (31.2)

Since xi,psi are independent, the inclusion into H_1(X) is injective on
this two-plane, and their span equals its image. No assertion of
injectivity on the whole H_1(U) or its whole boundary space is needed.

Let beta_0=b_0-b_2,beta_1=b_1-b_3 denote the included classes. With an
intersection/Poincare-duality sign convention fixed once, there are real
a,b, not both0, such that for every ABSOLUTE cycle z,

    Q_x(z)=a<beta_0,z>+b<beta_1,z>,
    Q_y(z)=-b<beta_0,z>+a<beta_1,z>.               (31.3)

This follows from R beta_0=beta_1,R beta_1=-beta_0 and the same relations
for xi,psi. The coefficient matrix has determinant a^2+b^2>0. In particular
Q(z)!=0 iff z pairs nontrivially with at least one of these two SPECIFIC
neck classes. It is not enough merely that z have zero holonomy.

Every b_j has zero developed period, throughout the slide. Indeed the
constant-area D4 cup computation of21.1 makes the tautological plane
span{x_t,y_t} orthogonal to span{x_1,y_1} for every small real t. Equation
(31.2)thus gives hol_t(beta_0)=hol_t(beta_1)=0. Since R has derivative i,

    hol_t(b_2)=-hol_t(b_0),    hol_t(b_3)=-hol_t(b_1).

Hence hol_t(beta_0)=2hol_t(b_0)and similarly for b_1. All four vanish.
The boundary classes are nontrivial in the combinations(31.2), despite
these zero holonomies; zero period is not zero homology.

For a supplied actual seed eta and a supplied pure affine twist N,
its increment Neta is absolute. Equations(31.3)therefore give a geometric
reformulation of its detecting increment: at least one of

    <beta_0,Neta>,          <beta_1,Neta>

must be nonzero. The same applies to a mixed increment NHeta. Proving
that pairing for the actual event remains open. Equation(31.3)is NOT
asserted for Q(eta) itself without retaining its actual relative endpoint
terms, particularly when its corner is moving or when Y is disconnected.
The central-cap direct calculation of26.6 retains those terms separately.



### 31.1 Explicit collar weights, retaining actual relative endpoints

**Status: accepted by a separate focused tools-disabled Opus review
(exit0), with the metric, frame, label and count conventions below.** This supplies a PARTICULAR relative extension of the
absolute neck classes, determined by the actual slide and actual material
endpoints. It does not choose an arbitrary extension of absolute Q.

Use the canonical normalization u=(0,-1)and the fixed flank reflection
V=r_v:(x,y)->(-x,y)for its linear part. Thus V u=u. Choose N,N' as in31,
with their internal crosscuts joining two points of x=1, one below B_0
and the other above C_0. The region N minus interior N' is a rectangle
up to smoothing, bounded by those crosscuts and two fixed-flank segments.
There are no other physical walls or corners in it. BOTH flank pieces
have the SAME reflection V, and V u=u; this essential literal-attachment
hypothesis makes the pairing below possible. In the unfolding,
its eight copies glue in pairs g,gV along the two flank segments. They
form four disjoint collar annuli A_j, joining the four outer necks to
the corresponding boundaries of U'=preimage(N'double). Label them by
cosets R^j{I,V}, j=0,1,2,3. Fix b_j to be the OUTER boundary of this
specific annulus, oriented as boundary U, and use intersection sign
<a,c>=sign(a',c'). Then b_(j+1)=R b_j and a positive entry into U has
<b_j,z>=+1. This fixes the labels/signs previously arbitrary in31.
Along A_j the cutoff phi extends to one
function phi_j, equal0 on its outer boundary and1 on its inner boundary.

Inside a physical copy g, the differential is g(dp). Pulling back by
h_t gives g(dp)+t*g(u)*d phi. The two coefficients agree across either
fixed-flank gluing because gV(u)=g(u). Away from the four annuli, d phi=0.
Consequently the derivative of the ACTUAL pulled-back differential is

    delta omega = sum_(j=0)^3 R^j(u) d phi_j.        (31.4)

The one-forms d phi_j are extended by0 off A_j; choose the cutoff flat
near its two boundary levels. The equality holds piecewise smoothly and gives a closed R^2-valued
1-form; it is not claimed holomorphic for X_0's complex structure.
In fact h_t*omega_t=omega_0+t*delta omega exactly, so for each fixed
material relative class hol_t(z)=hol_0(z)+t*Q(z) exactly. It is zero on U'
and Y, with exactly the stated collar transitions. No global primitive
for any one phi_j is assumed; its two complementary sides can be joined
outside that annulus, which is why its extended d phi_j can be nonexact.

For a supplied chain z with endpoints in U' or Y, let nu_j(z)be its net
number of crossings of A_j from outer to inner, counted negatively for
the reverse. After a harmless transverse perturbation this is an integer,
and equals integral_z d phi_j. This applies to ALL actual event endpoints:
S,T are fixed in Y, a moving pocket corner is translated inside U', and
every other physical corner is fixed in Y. Thus the true period derivative,
with exactly those material endpoints, is

    Q(z)=u*(nu_0-nu_2)+(R u)*(nu_1-nu_3).          (31.5)

It is nonzero iff the SIGNED NET counts satisfy
(nu_0,nu_1)!=(nu_2,nu_3); one unequal pair suffices. When z
is the actual event eta=(p->s)+(p->t), both arms start at the selected
actual corner lift p. If p moves, each arm beginning in U' contributes
its exit with a MINUS sign. Its corner-motion term is therefore already
included in(31.5); it must not be added a second time.

For example, at the central-cap seed the two arms exit through necks
with the same weight because the selected fixed flank preserves u.
Their total is-2g_p*u, where g_p is the corner's selected copy frame;
g_p=I in26.6's normalization, giving-2u. Formula(31.5)uses the absolute
copy frame. Section3 normalizes at the chosen source copy g_S, so its
vector is g_S^(-1)*Q_collar. Nonvanishing is identical in either frame. More generally an arm beginning
at a moving corner with initial sheet g and ending its first partial
pocket visit in sheet g' has derivative-g'u: the local conjugation load
(g-g')u is supplemented by its initial velocity term-gu. A complete
excursion contributes gu-g'u. These match Section3's prefix-and-corner
formula. The subsequent fixed part has derivative0.

For closed cycles, nu_j is the intersection pairing with the oriented
neck b_j (fix its sign to count entries). In the canonical normalization,

    Q_x=nu_1-nu_3,          Q_y=nu_2-nu_0.

So the absolute coefficients in31.3 can be fixed to(a,b)=(0,1)for these
neck labels and signs. The cochains and the two-neck support are therefore
explicit, not only an unspecified nonzero rotation/scaling of the neck plane.
The topological genus1/four-neck proof remains a separate corroboration.

Each neck also has zero period directly: it consists of an internal
crosscut alpha of N in copy g and its reverse in copy gV. Its two physical
endpoints lie on x=1, so its displacement Delta is vertical. Therefore
hol(b_j)=g Delta-gV Delta=0. This holds throughout the slide because the
crosscut and the fixed flank do not move. It independently corroborates
the cup-product argument in31 without asserting a straight representative
for a zero-period homology class.

This exact relative criterion still does not prove existence of a legal
actual event with unequal opposite-neck counts. It identifies the missing
realization condition without dropping actual endpoints or corner motion.
The prescribed checks evaluate only already-stated local return isometries
under the eight D4 prefixes; no trajectory, direction or word is discovered.


## 32. Zero-mean cylinder loads and exact overlap detection

**Status: accepted by independent focused tools-disabled Opus review
(exit0), with torus-strip scope and transport details below.** These are exact identities
and a conditional test on SUPPLIED strips. There is no cylinder, direction,
room or event discovery. No universal nonzero test is asserted.

### 32.1 The slide load has mean zero in every rational direction

Let e be a unit rational direction, with maximal cylinders D of heights
h_D and positively oriented core classes c_D. For either component alpha
of the absolute pocket slide cochain Q=(x_1,y_1), identified by the
same literal slide and persistent material/Gauss-Manin chart as21.1,
the closed transverse form
beta=det(e,hol) is a real linear combination of x_0,y_0. In cylinder
coordinates(s,tau), beta=d tau. The integral of a closed representative
of alpha on each parallel core is constant. Consequently

    integral_D beta wedge alpha = -h_D*alpha(c_D),
    sum_D h_D Q(c_D)=0.                            (32.1)

Choose a smooth closed representative of alpha, vanishing near the
finitely many zeros after subtracting local exact forms. Compute on
truncated cylinders and pass to the limit; the flat transverse form
restricts to0 on each level boundary and the closed core integral stays
constant. The second equality follows by summing over the full-measure
cylinders and using the established21.1 orthogonality of x_1,y_1 to x_0,y_0.
This is valid in ANY rational direction of the fixed arithmetic base,
not merely in the two slide-blind axes.

For the integer-torus torus-lift strips in primitive direction theta, write
n_E for the annulus cover degree. Each has area n_E, circumference
n_E*|theta|and height1/|theta|. Define the vector-valued step function

    f_theta = Q(c_E)/n_E on E.

Equation(32.1)becomes sum_E Q(c_E)=0, or integral_X f_theta dA=0.
For maximal cylinder ratios r_D=Q(c_D)/ell_D, it equivalently says
sum_D Area(D)*r_D=0. Thus the9.2b criterion "normalized fluxes not all
equal" simplifies here to "at least one core has nonzero flux."
This detects SOME abstract zero-holonomy cycle; it does not replace the
actual event obligation. Any nonzero real component of f_theta has both
positive and negative values, but that does not make any selected pair
of strips have different averages.

### 32.2 Core intersection is exactly signed overlap area

Let theta,phi be nonparallel primitive integer vectors. Let E,D be
SUPPLIED torus-lift strips in these respective directions, with cores
oriented along theta,phi and intersection convention matching the signed
planar determinant. Then

    <c_E,c_D> = det(theta,phi)*Area(E intersect D).    (32.2)

Proof. Put F(z)=(det(theta,z),det(phi,z)). Its linear determinant is
m=det(theta,phi), not necessarily positive. The torus leaves through0
pull back to the integer lines of the two F coordinates. Their complement
consists of |m| open parallelograms on the torus, each of area1/|m|:
F(Z^2)has index|m|in Z^2. These faces are simply connected and avoid0,
so their preimages are isometric open faces. Each lifted face lies in
one theta strip and one phi strip. E intersect D is the union of exactly
those faces assigned to both.

Choose generic core levels in E and D. On each such face the two F
coordinates vary independently over one open unit square; the chosen
core levels select exactly one intersection. Its sign is sign(m).
Thus the signed core intersection equals sign(m)times the number of
common faces, whereas their total area is that number divided by|m|.
This proves(32.2), including annulus covers of degree larger than1.
The boundaries have area0. No claim is made that an arbitrary overlap
matrix satisfying the resulting arithmetic is realizable by a surface.

### 32.3 Four actual event images certify a nonzero average contrast

Retain a SUPPLIED actual one-corner primitive seed eta of half-vector w.
Choose a symbolic primitive v with epsilon=det(v,w)=+1or-1. Its two open
halves occupy supplied torus-lift v-strips D_s,D_t. Let their areas/cover
degrees be n_s,n_t. Fix the common torus-leaf twist coefficient
kappa=K(d)from9.5 and let tau_v be that pure twist. Its absolute increment is

    z=(tau_v*-I)eta=epsilon*kappa*(c_Dt/n_t-c_Ds/n_s).  (32.3)

This is the9.3 formula with a fixed sign convention. Let gamma be any
SUPPLIED pure orientation-preserving affine automorphism fixing the
actual marks and selected prongs. At THIS raw base Section10 proves that the FULL absolute-period lattice
is exactly2Z^2. The automorphism gamma_* permutes integral absolute cycles,
so its derivative preserves that full lattice in both directions.
Consequently A_gamma Z^2=Z^2; area preservation gives det A_gamma=1,
hence A_gamma lies in SL2(Z). This supplies the transport input flagged
by the focused review, which did not include Section10 among its inputs.
It is not inferred merely from an arbitrary proper period sublattice.
Since gamma fixes an actual source s over0, integrating along paths from
s gives pi composed with gamma = A_gamma composed with pi. Thus gamma
preserves the entire origin fiber and maps torus-lift strips to torus-lift
strips. This conclusion is asserted only at the raw arithmetic base. It maps these strips to torus-lift A_gamma*v strips
of the same areas. Choose a supplied theta twist Phi_theta with the same
kappa, and write N_theta=Phi_theta*-I. For theta nonparallel to A_gamma*v,
(32.2)and the pure twist formula give

    Q(N_theta gamma_* z)
       =epsilon*kappa^2*det(theta,A_gamma*v)
          *[ Avg_(gamma D_t) f_theta - Avg_(gamma D_s) f_theta ]. (32.4)

Indeed N_theta x=sum_E(kappa/n_E)<c_E,x>c_E. Substitute(32.3)and then
(32.2); summing f_theta over the overlap faces gives the two averages.
Areas n_s,n_t, not their square roots or circumferences, normalize them.
The prefactor has a nonzero signed determinant, so a nonzero vector
average contrast is exactly a nonzero Q value of this SPECIFIC absolute
increment.

The increment is a signed sum of FOUR actual event classes:

    N_theta gamma_* z
       =Phi_theta* gamma_* tau_v* eta - gamma_* tau_v* eta
          -Phi_theta* gamma_* eta + gamma_* eta.       (32.5)

If(32.4)is nonzero, at least one of those four actual images has nonzero
Q. All retain the supplied actual endpoint labels and embedded intrinsic
pi continuation by the previously reviewed affine-event transfer. If its direction is wall-parallel, apply the established Q-invariant
axis group (9.2item2)and Section5's axis powers avoiding the at most
four wall lines. They make the actual image non-wall-parallel and supply
either opening sign without changing Q.
Thus this is an actual-event sufficient test, not just an arbitrary
absolute-cycle existence statement.

Conversely, suppose every actual image of eta in the supplied pure
affine group is Q-blind, and this group contains the displayed compositions
Phi_theta*gamma*tau_v, gamma*tau_v and Phi_theta*gamma. Then for each such
(v,theta,gamma), Avg_(gamma D_t)f_theta=Avg_(gamma D_s)f_theta. This is a necessary separation obstruction, not a proof that any
particular contrast is nonzero. The finite9.4 family tests much less:
it keeps the original half-vector's unimodular directions and selected
conjugacies. General two-step/transported tests require this wider scope.

The broad review's assertion that cylinder cores/twists span the relevant
absolute tangent at this special arithmetic base is not adopted. Nor is
its proposed hidden translation symmetry an actual room counterexample.
What is proved here is zero mean, exact overlap, and the four-event
certificate CONDITIONAL on a supplied nonzero contrast. Proving that an
actual bounded seed separates an arbitrary specified pocket remains open.


The three formal overlap-table controls in pocket-overlap.py check only
the substitutions/normalizations in32.4 and a gamma=id four-term basis
identity. They do NOT test or prove the geometric intersection theorem32.2,
realizability of a table, or cylinder-load mean cancellation in a room.
The transverse-coordinate hand proof and its independent mathematical
review supply those identities. Zero mean does not force a contrast on
any selected pair; the first prescribed table explicitly has none.


## 33. An actual raw two-mark room can be blind in both diagonal directions

**Status: focused independent Opus review21728 accepts this scoped hand
proof(exit0); prescribed strict-raw topology and symbolic reflection
controls pass. The review's periodicity, moving-endpoint and strictness
qualifications are incorporated below.**
The attempted shortcut "the AB-normal diagonal direction must contain a
loaded cylinder through the literal pocket" is false even with two full
interior A marks. This is not a counterexample to universal one-corner
S/T detection. It only defeats that proposed diagonal-cylinder shortcut.

Use the following FIXED fan assembly, prescribed analytically rather than
found by a room or trajectory search. Full A stars are centered at
S=(-4,0), T=(0,0). The shared M=(-2,0) is its upper half-star. The seven
leaf fans are:

| Center | Specified fan |
|---|---|
|(-2,2)|one triangle [(-2,2),(-2,1),(-1,1)]|
|(2,0)|one triangle [(2,0),(1,0),(1,1)] -- specified pocket|
|(0,2)|the two-triangle quadrant [0,1] x[1,2]|
|(0,-2)|one triangle [(0,-2),(0,-1),(1,-1)]|
|(-6,0)|one triangle [(-6,0),(-5,0),(-5,1)]|
|(-4,2)|one triangle [(-4,2),(-4,1),(-3,1)]|
|(-4,-2)|one triangle [(-4,-2),(-4,-1),(-5,-1)]|

The room has28canonical triangles, area14, exactly25physical walls, no
slits, no boundary contacts and no transparent B/C point. Its only full
interior A stars are S,T. The prescribed topology checker verifies these
facts directly for this single assembly. The selected pocket has
A=(2,0), C=(1,0), B=(1,1), with angles45/270/225degrees.
This is exactly Section1's template under(x,y)->(x,2-y), including
its slide velocity and both moving mirror equations. Its portal is
x=1,0<y<1. The adjacent fixed vertical wall continues above B along the
right edge of the(0,2)quadrant, and below C along T's right edge. Thus it
is the required straight-attached literal pocket. Translate it by t*u,
u=(0,1). Its moving mirrors are D_t:x+y=2+t and H_t:y=t; the portal's
supporting line and both actual marks stay fixed.

**A prescribed entire normal-return family.** Fix0<a<1. For sufficiently
small |t| compared with min(a,1-a), define normal-collision endpoints

    d_0(t)=((3+t-a)/2, (1+t+a)/2),
    d_1(t)=((3+a-t)/2, (1+3t-a)/2).

They are interior points of D_t. The physical path between them is

    d_0(t) -> (-a,-1) -> (-1,-a) -> (1,2-a)
      -> (1-a,2) -> (0,1+a) -> (1+a-t,t) -> d_1(t).

The successive ordinary mirrors are

    y=-1, x=-1, x=1, y=2, x=0, y=t.

The first five are FIXED supporting lines, all at actual wall points.
Specifically the lower-T hit(-a,-1) is on the fixed half-BC segment
-1<x<0 because the bottom leaf uses its right portal. The left-T hit
(-1,-a) is below the shared M's upper portal. The next three bounces
are the right, top and left AC walls of the fixed upper-right quadrant.
The last bounce(1+a-t,t) lies on the MOVING pocket leg H_t. This moving
hit cannot be dropped from the derivative calculation.

The path starts with velocity(-1,-1); after each mirror it has the
appropriate diagonal sign. Its positive durations are

    (3+t+a)/2, 1-a, 2, a, 1-a, 1+a-t, (1+t-a)/2.

Their sum is7, identically in both a and t. It crosses the original right
portal at(1,a) twice, with different velocities; it also enters and exits
the upper quadrant through its lower portal. All those crossings are
interior. Every ordinary mirror hit stays strictly interior to its segment
for each fixed a and sufficiently small |t|. The prescribed open segments
stay inside T's square, that fixed upper quadrant or the moving pocket.
The trajectory never enters the shared M or the other full star S.
Corner avoidance can also be read directly from its three lines in T's
square: y=x+a-1, y=x+1-a and x+y=1+a. For0<a<1 none contains a physical
corner or T. The other hits have one coordinate strictly between
successive integers. The affine containment inequalities are strict in
the open parameter rhombus unless identically zero; those zero identities
are precisely the intended D/H mirror or portal incidences. The allowed
t-range need not be uniform as a approaches the separating boundary:
only the derivative of each base cylinder core is asserted.

At both d_0 and d_1 the path is normal to D_t. Reflecting at d_1 reverses
it exactly; it retraces to d_0, where another normal reflection closes
the billiard state. Thus it is a corner-free periodic physical path of
length14sqrt(2), independent of t. This argument retains the actual
periodic path; it is not the period of an arbitrary abstract cycle.

**Exact developed period.** The product of the six ordinary reflections
in encounter order, acting on endpoint coordinates, is

    G_t(x,y)=(-x-4, -y-6+2t).

It sends d_1(t) to d_0(t)-(7,7). Moreover G_t is an involution and

    (G_t R_Dt)^2(x,y)=(x-14,y-14).

Its linear part is the identity and its translation has derivative zero.
The closed lifted path is a positive integer multiple of its containing
cylinder core, so Q(core)=0. A source-frame D4 change preserves zero.
The cancellation is between the moving diagonal endpoints and the
moving horizontal-leg bounce; treating all intervening AC walls as fixed
would give a false nonzero result.

At t=0, d_0(a) traverses the first open half of D and d_1(a) the other
open half, excluding the middle separating trajectory and the physical
endpoints. Every diagonal-direction path that enters this triangular
pocket either meets D normally directly or first reflects at H and then
meets D normally. There is no through passage via H alone: H cannot
reverse the horizontal component toward the sole vertical portal. A path
parallel to D can only reach D after H changes its diagonal sign. Hence
all nonsingular base diagonal cylinders meeting a moving mirror are
represented by this family, up to reversal and D4 copy. The other
cylinders avoid both moving mirrors and have zero period derivative.
The integer-vertex D4 unfolding is square-tiled, hence these rational
directions are completely periodic; no omitted minimal component needs
separate treatment. Moving portal endpoints can change widths and
boundary saddle connections. A core avoiding both moving mirrors still
has positive clearance from those finitely many endpoints, so those
changes do not alter its period derivative.
Consequently ALL cylinder-core slide loads in the two primitive diagonal
directions(1,1)and(1,-1) vanish in this actual room.

**Scope.** The normal family does not join S and T; it is a cylinder
control only. It does not show that other rational directions are blind,
that a supplied actual S/T event has zero response under every affine
image, or that no detecting one-corner event exists. In particular it is
not an in-class counterexample to the full goal. It rules out a tempting
universal direction choice and makes the missing multiple-direction or
actual-event realization step explicit. The room and all formulas are
prescribed once; verification does no room, ray, direction, word,
cylinder or origami discovery scan.

**Conditional-on-coverage group corollary.** Once the all-diagonal-cylinder
coverage argument above is accepted, the blindness is global on marked
relative homology, not just on the particular periodic family. For any
pure multitwist f=I+N in either diagonal direction, Section9.2 gives
Neta as a linear combination of its ordinary absolute cylinder cores.
All those core loads vanish here, so QN=0 for every marked relative
class eta. Both diagonal pure multitwists therefore preserve Q, just as
the established horizontal/vertical pure multitwists do for this slide.
Every word in the group generated by these FOUR direction families
preserves Q. It cannot unblind a supplied blind actual event. Their
conjugate cusp directions remain blind by9.2's source-fixed
commensurability argument. No finite-index or full-Veech-group assertion
is made for this generated subgroup, and no all-rational-direction
blindness follows. In particular, this is not the sought structural
counterexample to universal detection.


## 34. A moving-diagonal detecting family with no wall-count bound

**Status: focused independent review97361 accepts the scoped all-k hand
proof with corrections incorporated; universal pocket detection OPEN.** This extends26.9's mechanism beyond the bounded fan census.
It proves a specified infinite FAMILY, not the universal pocket lemma.
No parameter, direction, room or trajectory discovery scan is used.

Let k>=1 be an integer, D=4k and M=D+1. Suppose a canonical room has
actual interior marks S=(0,0),T=(D,0), contains the open upper corridor
(0,D+1) x(0,1), and has the following actual cap geometry at T. Its full
star contains[D-1,D+1] x[-1,1]. The fixed upper cap is the rectangle
[D,D+1] x[1,2], with actual top mirror y=2. Its fixed lower cap is the
triangle[(D,-2),(D,-1),(D+1,-1)], with actual mirrors x=D and x-y=D+2.
The specified straight-attached upper end pocket is

    A=(D+2,0), C=(D+1,0), B=(D+1,1),

sliding by u=(0,1). It has the literal45/270/225angles, fixed vertical
flanks on x=D+1 and moving diagonal D_t:x+y=D+2+t. The remainder of the
room is fixed. These are geometric hypotheses, not consequences of
arbitrary room topology.

Then there is an ACTUAL S/T one-B-corner midpoint event, with equal
primitive halves(M,1), an embedded intrinsic pi continuation, and

    Qeta=(1,-1),         det((M,1),Qeta)=-(M+1)=-(4k+2).

**First half and corner.** Take S->B directly through the open corridor.
Its displacement(M,1) is primitive, and it meets no other integer point.
Choose reflection at B in its MOVING diagonal flank, sending(M,1) to
(-1,-M). The physical225degree link and embedded pi-sector are exactly
26.9's computation with alpha=atan(1/M). The interval
[pi+alpha,2pi+alpha] crosses the moving diagonal once and embeds in the
10pi cone.

**Lower-cap return lemma.** In local coordinates relative to T, enter
the lower triangular cap at(q,-1) with velocity(-1,-M), where

    M>1,          2/M < q < 1.

The fixed three-reflection word D_- V_- D_- returns through(q-2/M,-1)
with velocity(-1,M), after elapsed time2/M. Here D_-:x-y=2 and V_-:x=0.
This is a prescribed triangular reflection identity, not a trial word.
The first D hit has x=(M*q-1)/(M-1); the V hit is
(0,-2+q-1/M); the second D hit has x=(M*q-1)/(M+1) and y=x-2.
All are interior points of their mirror segments. The last portal x
coordinate q-2/M is positive by hypothesis. The consecutive durations
are

    (1-q)/(M-1),
    (M*q-1)/(M*(M-1)),
    (q-1/M)/(M+1),
    (1-(M*q-1)/(M+1))/M.

Their sum is2/M. The first leg reaches D before x=0 since Mq>1.
The second leg moves away from D and reaches x=0 strictly above(0,-2).
On the third leg y decreases and x-y increases, so its only possible
exit is D. The fourth leg reaches the portal with x=q-2/M>0.
These first-hit comparisons exclude intervening edges and vertices. In development the word is exactly reflection
in y=-2. Thus this REAL triangular cap realizes the same outgoing state
as a horizontal reflector at y=-2, with unchanged horizontal phase.

**Upper cap and repeated returns.** In the fixed upper rectangle an
entry at(q,1) with velocity(-1,M), again q>2/M, simply hits y=2 and
returns through(q-2/M,1) with velocity(-1,-M) in time2/M. No vertical
side is met because x stays between q-2/M and q, both in(0,1).

Starting at B, use the virtual vertical interval[-2,2]. Its j-th far-wall
hit, indexed j=0,...,k-1, occurs after vertical distance4j+3, at time

    t_j=(4j+3)/M.

The hits alternate lower,upper,lower,upper. Each corresponding cap entry
occurs at time(4j+2)/M and has horizontal portal coordinate

    q_j=1-(4j+2)/M >=3/M >2/M.

Thus EVERY return is geometrically valid by the two cap lemmas. The
coordinate x relative to T is1-t whenever the path is outside the lower
triangle, and each triangular return exits at that same predicted phase.
The final cap exit is at time4k/M, phase1/M and height either+1or-1.
The remaining time1/M brings the path to(0,0) relative to T. Hence the
second half reaches ACTUAL T at time1, with no earlier arrival. Its total
Euclidean length equals the first half because all velocities have norm
sqrt(M²+1), including the swapped components in the lower cap.

In the fixed development, k alternating far-wall reflections take ACTUAL
T to(D,-4k)=(D,-D). Reflection in the selected moving corner flank gives

    T'(t)=(2D+2+t,2+t),       B(t)=(D+1,1+t).

Thus T'(0)=2B(0), both developed halves equal(M,1), and the full defect
is(1,1)-2(0,1)=(1,-1). All ordinary cap mirrors are fixed. Since(M,1)
is primitive and every base reflection preserves the canonical integer
lattice, no open half can meet another physical corner. The construction
uses k analytically prescribed cap returns; no bounded ray run or guessed
reflection scan is needed for the all-k proof.

**An explicit unbounded raw family realizing the hypotheses.** For every
k>=1, put full stars at(4j,0), j=0,...,k. For j=0,...,k-1 put the upper
half-star at(4j+2,0), with a lower-right (right-portal) one-triangle leaf at(4j+2,2). At each
full star put an upper-right one-triangle leaf centered at(4j,-2).
Put a lower-right one-triangle leaf at(4j,2) for j<k, and the lower-right
two-triangle quadrant at(D,2). Add a lower-right triangle at(-2,0) and
the specified upper-left triangle at(D+2,0) (the latter is the upper end
pocket, directed back toward T). Each named triangle is the unique
canonical triangle on the stated side of its inward C portal.

The fan graph is a tree: there are k+1full fans, k shared half-stars and
3k+4leaves. Its5k+4portals join5k+5fans. The unit-box geometry has no
nonlocal overlaps. All shared B links are contiguous; their angles are
90,135or225degrees, never180or360. All C links are90or270degrees. The
only smooth boundary A points are the k half-star centers. These local
facts repeat by translation along the chain; the two ends have the
explicit literal225/270 pocket and the harmless135degree left B tip.
Thus the connected disk has a simple boundary and is raw. This is a hand
construction, not a completeness enumeration.

There are15k+13canonical triangles. There are k+1 interior A full stars, including the two specified marks;
extra interior A points are allowed by Section1. The partial charge is6k+5, since
k half-stars contribute3k and the3k+4leaves have only one m=2 member.
The raw identity gives

    W=2+6(k+1)+(6k+5)=12k+13.

In particular k=1 has W25 and k=2 has W37. A SINGLE fixed k=2 fixture
and its prescribed two-cap event provide exact geometry/segment controls;
those checks are not the proof for all k. Every ordinary hit has strict
open-segment clearance; for each fixed k this persists for sufficiently
small |t|, so the Section3 opening criterion applies conditionally.
For this upward slide a_D=(1,1); the downward-pocket table uses the
opposite convention. This construction needs D divisible by4: if
D=2 mod4 the same virtual endpoint folds to the A corner(D,+/-2),
not to T. Those corridors and other cap configurations remain open.
The universal theorem remains
open because arbitrary raw rooms need not contain this corridor and pair
of cap geometries.


## 35. Expanded verification of the neutral channel already in Section 2

**Expanded verification, not a new mechanism or detection theorem.**
Section2 ALREADY states the exact neutral slope interval and the
t-independent D H D return map. This appendix supplies explicit hit
coordinates, flight time and conditional finite-event persistence for
that same channel. Independent review of these added details is pending.
The prior description as a new exact-domain result overstated its novelty.
No room/ray/word search or room counterexample is supplied.

Normalize the literal triangle to vertices B=(0,0), A=(1,1), C=(0,1),
with open internal portal x=0, 0<y<1. Its reflecting walls are
D:y=x and H:y=1; the room core is on the left of the portal. The slide is
u=(0,1): D_t:y=x+t, H_t:y=1+t. The vertical attachment line stays x=0.
Let an incoming ray enter at (0,q) with velocity (a,b), a>0, and set
m=b/a. Velocity is parametrized by physical flight time, not unit arclength.

**Neutral-channel lemma.** The prescribed three ordinary reflections
D,H,D, in that chronological order, give a legal first return to the open
portal if and only if

    0<q<1,      0<q+2m<1.                            (35.1)

In that case the ray returns at (0,q+2m) with velocity (-a,b), after
time2/a. Every mirror hit lies in the open mirror segment, with no
intervening corner or boundary hit. This is the exact scattering law of
a virtual vertical reflector at x=1.

**First-hit proof.** Condition(35.1) is equivalent, for fixed q, to
-q/2<m<(1-q)/2; in particular -1/2<m<1/2. The three hit points are

    P1=(q/(1-m), q/(1-m)),
    P2=(q+m, 1),
    P3=((q+2m)/(1+m), (q+2m)/(1+m)).              (35.2)

All three relevant x coordinates lie strictly between0 and1.
For P1 this follows from q>0 and m<1-q; for P2 from
q/2<q+m<(1+q)/2; for P3 positivity is (35.1), and its upper bound
is equivalent to q+m<1.

The first leg has velocity(a,b). Its difference y-x decreases and it
reaches D before H because m<1-q. It cannot leave through the portal
because x increases. After D the velocity is(b,a): y-x increases, so
there is no D re-hit; y reaches1 at P2, and x stays positive until then
even if b<0. After H the velocity is(b,-a): y-x decreases to0 at P3,
whose positive x coordinate excludes an earlier portal exit. Finally D
changes the velocity to(-a,b). The difference y-x now increases, so D
cannot be re-hit; the outgoing portal height q+2m lies in(0,1), which
also excludes H before exit. Convexity of the triangle between each pair
of these points excludes any other wall encounter.

The consecutive durations are

    q/[a*(1-m)],
    [1-q/(1-m)]/a,
    [1-q-m]/[a*(1+m)],
    [q+2m]/[a*(1+m)].                              (35.3)

The first two sum to1/a, as do the last two, proving the flight time2/a.
Conversely, a legal D,H,D return has the composite isometry
D H D:(x,y)->(2-x,y). Its unfolded outgoing line starts at(2,q), with
velocity(-a,b); its first portal time is2/a and height q+2m. An open
portal return therefore requires (35.1). This proves the iff claim.

**Exact invariance under the slide.** Keep the ABSOLUTE incoming point
(0,q_0) and velocity(a,b) fixed. In the translated triangle the relative
height is q_0-t. Condition(35.1) holds exactly when

    max(q_0-1,q_0+2m-1) < t < min(q_0,q_0+2m).       (35.4)

If the base state is strict, this open interval contains0. Throughout
it, D_t H_t D_t is the SAME vertical reflection x=1. The absolute exit
point (0,q_0+2m), outgoing velocity(-a,b), and flight time2/a are all
independent of t. This is an OPEN incoming-state channel, not a tangency
or zero-measure direction. The individual mirror hits need not stay fixed.

**Consequence for actual supplied events.** Take an actual S/T one-corner
midpoint event whose selected corner is fixed outside the moving pocket.
Suppose every visit of each open arm to the pocket consists of a strict
neutral excursion as above. Use the supplied event's finite reflection itinerary; each straight leg
has at most one strict portal crossing, so there are finitely many visits.
Intersect their open t intervals (35.4), along with the ordinary strict
clearance intervals on the fixed remainder of the event. Inductively,
each unchanged incoming state has an unchanged outgoing state and flight
time, so the next fixed-core segment and subsequent incoming state are
unchanged. The actual S and T endpoints, the selected fixed corner, the
two half lengths, and their chosen intrinsic pi sector persist. No target
lift is replaced and no new optical corner is passed through.

Thus this actual event stays a one-corner event of equal halves for
all sufficiently small t, and its TRUE period defect is identically zero,
not merely zero to first order. In the reflection formula each complete
excursion has a t-independent affine map, all intervening maps and the
selected corner are fixed, so the full equality has no t term. Equivalently
its collar crossing weights cancel. The vector conclusion Q(eta)=0 does
not rely on inferring optical validity from an algebraic word alone:
(35.1)--(35.3) provide that validity.

**Scope.** This lemma does not say every excursion or every seed is
neutral. It does not apply when the selected corner moves, when there is
another corner encounter, or when (35.1) fails. It supplies no room in
which all actual S/T events use only this channel. No universal detection
or counterexample follows. It does rule out a local argument that a seed
must acquire nonzero defect merely because an arm enters the moving
triangle. A successful global argument must force an uncompensated
non-neutral excursion or handle a moving selected corner, retaining the
actual target and local pi continuation. Multiple non-neutral excursions
can still cancel; this statement does not resolve that possibility.
