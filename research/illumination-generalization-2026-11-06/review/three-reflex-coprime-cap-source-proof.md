# CS01: a guarded cap-source extension

Reviewer-originated hand proof submitted for reciprocal independent challenge. This is a positive restricted-family claim, not a complete r3 theorem. No discovery search was used.

## 1. Correction to the initial candidate

The unrestricted candidate's roof-corner step was missing: a cap source above h does not furnish two physical h-crossings. The old roof-symmetry exclusion cannot be inherited. The following sufficient extra hypotheses repair this exact gap:

    C=2H-u-h<N, R=H-u, and C/gcd(C,R) is even.

The broader candidate without these hypotheses is NOT accepted or refuted here. The remainder of this proof claims only the guarded extension.

## 2. Exact terminal statement and initial selection

Keep CE01's rational a>0, integers L>=2,N>=L+2, A=Na,w=(N-1)a,l=(N-L)a, integer0<b<c<h<H. Let rational actual S=(s,u),T=(t,v) satisfy0<s<a,h<u<H,l<t<A,0<v<c, with integral u,v. Set

    R=H-u>0, delta=H-h>0, C=R+delta,
    g1=h-c>0,d2=c-v>0,D=C+g1+d2=2H-u-v,z=A-t.

Require gcd(C,N)=gcd(Nd2,L)=1, C<N and C/gcd(C,R) even. Then a finite regular actual one-roof S-to-T ray exists.

Use tau_q=(A+z-s+2aq)/D and exclude only

    s+C*tau_q-A = a (mod2a),
    s+(C+g1)*tau_q-A = a (mod2a).

For integral q each event is empty or one class of period D/gcd(t,D)>=2. Two such classes can cover all integers only when both have period2 and opposite residues. That would require both distinct times C,C+g1 to equal D/2, impossible. Thus a q in0..D-1 avoids both. The slope is positive since A+z-s>A-a>0. This is an exact finite selection consequence, not a reflection cutoff.

There is no source-band bad event: the actual source is already in the full-width cap, and its initial phase is exactly s.

## 3. Strict cap and actual target

Set X=s+C*tau_q. Under tau->tau+2aM, X modulo2Na visits N points of one spacing2a coset, because gcd(C,N)=1. The excluded first event ensures that coset misses the endpoints of A+(-a,a). There is exactly one strict return point, with

    z1=s+C*tau-(2m+1)A in(-a,a).

Set k=floor((z1+g1*tau+a)/(2a)) and z2=z1+g1*tau-2ka. The second excluded event, preserved by integral times, gives |z2|<a. Now

    E=z2+d2*tau=z+2aJ, J integral.

The shift tau->tau+2aNp changes m by C*p and k by N*g1*p, preserving z1,z2 EXACTLY. It adds Nd2*p to J. The assumed gcd(Nd2,L)=1 supplies p in0..L-1 making J zero modulo L, so F_(La)(E)=z. This is the actual target period2La. Every step uses one single common slope.

## 4. New roof-corner exclusion

A genuine roof corner would mean s+R*tau=jA for an integer j. The already strict cap-exit identity is s+C*tau=(2m+1)A+z1. Eliminate tau:

    A*[C*j-R*(2m+1)] = (C-R)*s+R*z1 = delta*s+R*z1.

Since0<s<a and |z1|<a, the right side lies strictly between -R*a and C*a. C<N gives both bounds strictly inside(-A,A). The bracket is an integer, so it must be zero:

    C*j=R*(2m+1).

Divide by d=gcd(C,R). The assumed even C/d is coprime to R/d, so R/d is odd. The left side is even and the right side odd, a contradiction. This excludes both genuine roof corners at x=0,A. The proof concerns the final corrected slope as well: all cap-exit residuals remain strict and the same elimination applies to its updated m.

## 5. Physical path and first target

Use increasing developed height eta from u to2H-v and the actual height eta before H,2H-eta afterward. Set

    u..2H-h:       x=F_A(s+tau*(eta-u)),
    2H-h..2H-c:    x=A-F_a(z1+tau*(eta-(2H-h))),
    2H-c..2H-v:    x=A-F_(La)(z2+tau*(eta-(2H-c))).

These are original full-width cap, right corridor and bottom chamber. No artificial h-crossing ascent or reflection at a cut is inserted. At the cap exit the odd-A center makes both charts locally A minus the same absolute value; at the next portal their even2a period makes the charts agree locally, including signed horizontal velocity. Zero residual is an original smooth x=A contact; strict a-bounds exclude the reflex/ledge endpoints. All open-band vertical mirrors are the original finite x=0,A above h, x=w,A between c,h, and x=l,A below c. The new roof argument excludes the only remaining horizontal-wall singularities. Positive finite widths and a finite slope give finitely many reflections, each specular.

The endpoint is exactly(A-F_(La)(E),v)=(t,v). Its height v<c<h<u is absent during ascent and in the cap/right corridor; the descending bottom trajectory reaches v only at its endpoint. Thus it is first actual T.

## 6. Whole native family with cap depth greater than one

Take positive integer a; L=2^e,e>=1; odd prime N>=L+2; integer0<b<c<h; c odd; h even; H=h+delta with delta positive ODD and2delta<N. Claim: every distinct actual interior even-even pair in the original ten-wall room illuminates.

For native left sources u<=h, CE01 applies since G=2delta is nonzero and below prime N, and each native bottom target has d2=c-v odd, hence gcd(Nd2,L)=1. For native left-cap sources h<u<H, the integer C=2H-u-h lies strictly between delta and2delta, so0<C<N and gcd(C,N)=1. Native u and h are even, while H is odd. Therefore C is even and R=H-u odd, giving C/gcd(C,R) even. The terminal lemma above applies.

All actual native pairs outside left-to-bottom terminal placements are covered by the accepted protected U/L theorem TR01 EXCEPT possible middle-upper-cap-to-bottom pairs. Those additional cap pairs with a<=s<=w,h<u<H are covered by accepted TR05; its actual rotated-U guards apply for every cap depth. Upper-right-cap sources x>w and bottom targets lie in the protected right L. These placements exhaust the entire cap and all TR01 residual pairs. Reverse a regular path when labels are exchanged.

This extends the thin-cap family to unbounded odd cap depths as N grows, including native sources strictly inside the cap. The proof needs the prime/width/parity hypotheses just stated. Arbitrary spiral metrics, other r3 turn types and r4..8 remain open. Reciprocal independent review of CS01 is still required before treating this new claim as accepted.
