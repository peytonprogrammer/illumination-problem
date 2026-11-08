# Unequal-aperture two-neck illumination and weighted resonant strips

Candidate A20, Codex01a18403; independent review pending. This removes the equal-width restriction from the accepted A18 mechanism. It retains two separate integer periods and actual source/target matching throughout. It does not illuminate the residual strips or prove the uncapped W<=21 objective.

## 1. Fixed geometric family and beam existence

Fix three finite strictly simple orthogonal chambers A,B,C, fixed opposing actual interior marks S,T, and two smooth mouths of positive widths w1,w2 on B's left and right vertical supporting lines x=0,h. The mouths may have different vertical origins r1,r2. Join the matching A/B and B/C mouths by horizontal rectangles of lengths L1,L2>0 and widths w1,w2. Assume the resulting room is a strictly simple disk without any other contact. All data except L1,L2 are fixed.

Use local vertical coordinates y1=y-r1 on the first mouth and y2=y-r2 on the second. They range over (0,w1) and (0,w2). Their origins need not coincide. The fixed end chambers have matching local mouth coordinates.

The accepted A18 Section 2 argument applies unchanged to unequal mouths: choose one common minimal nonaxis angular magnitude in the three closed auxiliary chambers, exclude corner paths from the actual S,T, take their finite first-mouth entry words, and choose the middle's last left-mouth departure before its first right-mouth arrival. This supplies a legal finite middle transit with neither mouth visited in between. Product openness in magnitude and entry ordinate gives fixed finite words on a nonempty slope interval and a nonempty input phase interval. All non-mouth contacts are transverse and corner avoiding. Auxiliary cap reflections are absent from the retained words.

Write the end virtual marks as S*=(-a,alpha) and T*=(b,beta) in their local mouth charts, with a,b>0. Write the middle's unfolded outgoing chart, relative to the input chart, as

    (x,y2) -> (x+d-h, kappa*y2+c0),  d>0,
    kappa=e0*e1.

The constant c0 includes the difference of vertical coordinate origins. The vertical signs eS,eT,e0,e1 are defined exactly as in A18. Consequently

    tau=eS*m,
    sigma1=eS*e0, sigmaout=eS*e1, sigma2=-eS*eT,
    kappa*zout+c0=z+e0*m*d.

All constants and signs are fixed by the words. Fix a bounded signed slope interval I=(u,v) excluding zero, of width delta>0, and an input interval J0 of length j>0 inside (0,w1), on which those words are valid. Shrink J0 if necessary so that

    j < w2/4.

Shrinking does not change a,b,d or the words. Let Z=sigma1*J0=(l,r), with r-l=j, taking its endpoints in increasing order.

## 2. Exact splice with two distinct periods

Set

    A1=L1+a, D=L1+L2+a+b+d, rho=A1/D,
    K=sigma1*c0+sigma2*beta-alpha.

Let n1,n2 be independent integers for the two horizontal wall unfoldings. Their periods are 2w1 and 2w2, respectively; they cannot be merged into one integer unless the widths have an appropriate relation.

The first neck's developed entry is 2w1*n1+sigma1*z. After unfolding the middle, its right-mouth chart has offset 2w1*n1+sigma1*c0 and derivative sigmaout. A target image in the second neck has developed ordinate

    2w1*n1+sigma1*c0+2w2*n2+sigma2*beta.

Thus the two exact equations to solve are

    tau*D = K+2w1*n1+2w2*n2,                         (E)
    tau*A1 = 2w1*n1+zeta-alpha,  zeta in Z.          (M)

The A18 sign calculation remains valid with each neck's own width. The first fold sends the actual slope to e0*m, the middle exit has slope e1*m, and the final physical slope is sigma2*tau=-eT*m, exactly the reversed actual-target word. All integer periods n1,n2 are allowed in the actual neck charts, independently of their fold signs.

A solution of (E),(M) with tau in I and zeta in Z is therefore a finite actual corner-avoiding S-to-T trajectory. The actual intermediate ordinate is z=sigma1*zeta; its fixed middle word has a strict exit in the second mouth. The second neck reaches the actual target word's strict mouth coordinate and velocity. No actual endpoint is replaced. Finitely many smooth horizontal contacts occur in the necks; all joint contacts are strictly inside their mouths.

## 3. One rotation controls the two exact integers

Eliminate tau from (E),(M). Put

    P=2w2*A1/D,
    theta=w1*(D-A1)/(w2*A1)>0,
    c=(alpha+rho*K)/P.

Then

    zeta/P = c+n2-theta*n1.                         (F)

Hence an integer n1 succeeds if the circular phase c-theta*n1 lies in Z/P modulo1. Once that phase is selected, some INTEGER n2 places the actual zeta in Z, and (M) fixes tau exactly; equation (E) then follows identically. In particular the source, target and middle entry have not been chosen independently.

For now assume A1>=D/4. Then

    P>=w2/2,
    E=j/P <=2j/w2 <1/2,
    E >= ell0:=j/(2w2)>0,
    theta<=Theta:=3w1/w2.

The actual circular arc Z/P therefore has length E strictly below1/2 and at least ell0. For EVERY zeta in Z, tau=(2w1*n1+zeta-alpha)/A1 lies in I provided n1 is strictly inside

    ((A1*u+alpha-l)/(2w1), (A1*v+alpha-r)/(2w1)).   (G)

This interval has length H=(A1*delta-j)/(2w1). Solving the phase equation within (G) is thus sufficient for the whole optical splice, even though zeta is fixed only after n1.

## 4. Explicit weighted strip theorem for this orientation

Choose an integer Q>4/ell0 and define

    C=4w1*w2*Q/delta,
    D0=4*(2j+8w1)/delta,
    Pmax=ceil(Q*Theta+1).

If A1>=D/4, D>D0 and the actual S,T are dark, then for some integers

    1<=q<=Q,  0<=p<=Pmax,

one has

    |q*w1*(L2+b+d)-p*w2*(L1+a)| <= C.              (S)

Proof. Pigeonhole the Q+1 fractional parts of 0,theta,...,Q*theta into Q equal intervals. For some q,p,

    gamma=|q*theta-p|<1/Q<ell0/4,
    1<=q<=Q, 0<=p<=Pmax.

If gamma=0, (S) holds. If gamma>0, the q-spaced orbit indices from 0 to q*floor(1/gamma) form, up to reflection, a mesh with maximum circular gap at most gamma. Including intervening indices cannot enlarge that gap. It meets every translate of the actual open phase arc of length E>=ell0.

If the deviation in (S) exceeds C, then

    w2*A1*gamma>C,
    m:=q*floor(1/gamma)<=Q/gamma
      <Q*w2*A1/C=A1*delta/(4w1).

Since A1>=D/4 and D>D0, one has A1>(2j+8w1)/delta. Therefore

    H=(A1*delta-j)/(2w1)>m+2.

The open interval (G) contains m+1 consecutive integers strictly inside it. Their phases c-theta*n1 translate the finite mesh. One lands in the actual arc Z/P, so Section 3 produces n2,zeta,tau satisfying the complete optical conditions. This contradicts darkness and proves (S). No irrationality or infinite density assertion was used.

## 5. Reverse orientation covers every length imbalance

The same finite middle transit may be reversed. Reflect the horizontal coordinate so travel is again left to right, retaining vertical local mouth coordinates, each with its own origin. The reversed entrance is the old exit; continuity of its affine contact map gives a product-open beam in the new entrance phase and common magnitude. Shrink that product as needed. The end entry words are exchanged, so

    a_rev=b, b_rev=a, d_rev=d,
    w1_rev=w2, w2_rev=w1,
    A1_rev=L2+b,
    D_rev=D.

Here d_rev=d because the reversed transit has exactly the same travel time and absolute horizontal speed. More explicitly e0_rev=-e1, e1_rev=-e0, kappa_rev=kappa and c0_rev=-kappa*c0; substituting these identities into the reversed middle equation verifies the chart directly. The signed interval and input width of its product beam may differ from the forward beam; use its own constants Q_rev,C_rev,D0_rev,Pmax_rev. No equality of beam widths or angular intervals is assumed.

If D>2d, then

    (L1+a)+(L2+b)=D-d>D/2,

so at least one of A1,A1_rev is greater than D/4. For

    D > max(2d,D0,D0_rev),

apply Section 4 in that orientation. Every possible failure lies in a FINITE union of weighted affine strips: either the forward strips (S) or the reversed strips

    |q*w2*(L1+a+d)-p*w1*(L2+b)| <= C_rev,

with that orientation's finite integer bounds. This statement covers arbitrary positive L1,L2, including sequences with one neck bounded. Membership in a strip proves neither darkness nor failure of another beam.

## 6. Lattice consequence and limits

For integer orthogonal chamber/mark coordinates and integer widths/neck lengths, a,b,d are integers and each weighted deviation is an integer. Each orientation therefore leaves only finitely many integer levels |c_int|<=floor(C) or floor(C_rev). For example a forward residual line is

    q*w1*L2-p*w2*L1
      =c_int-q*w1*(b+d)+p*w2*a.

If p>0, its positive integer solutions form at most one arithmetic ray after choosing a first positive solution, with primitive positive step

    (q*w1/g, p*w2/g),  g=gcd(q*w1,p*w2).

For p=0 it fixes L2, leaving L1 to vary. Thus unequal integer widths still give finitely many one-parameter arithmetic residual families for the fixed three-chamber data. For rational data use one common scaling. The theorem makes no claim that these families are illuminated or dark.

The constants depend on complete finite words and chamber/mark geometry. They are not bounded by W alone. This does not address moving chambers or marks, shrinking mouths, diagonal-wall chambers, more than two necks or an exhaustive decomposition of arbitrary canonical45 disks. No computation or discovery search supports the quantified proof; independent hand review of signs, both integer periods, mesh bounds and reversal is required. The full uncapped W<=21 theorem remains OPEN.
