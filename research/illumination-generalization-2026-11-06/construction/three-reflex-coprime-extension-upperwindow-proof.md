# CE08 hand proof: actual-target residue selection in one upper cap window

Independent review pending. Quantified scope is upperwindow-candidate.md.
All geometry is original; no artificial floor reflection or endpoint change.

## 1. One cap window gives a long interval of candidate integers

Since h<=u<H, there is no source-arm band: start with the actual cap
chart F_A(s+tau*(eta-u)) at eta=u. The actual source is regular and
inside the room even when u=h, because0<s<a and b<h.
Use the endpoint-compatible grid

    tau_q=(A+z-s+2e*q)/D, q>=0 integral.

It is positive. Let C=2H-h-u>0 and choose an odd cap center(2m+1)A.
The condition

    (2m+1)A-Ke < s+C*tau_q < (2m+1)A+Ke

is an OPEN q interval I_m of lengthK*D/C. Its lower endpoint tends
to infinity with m. Choose an integer m>=0 large enough that I_m
lies in q>=0. This only increases horizontal unfolding windings: the
physical height rises to H and falls to h ONCE. It is not a permission
for extra floor returns or extra reflections at an open passage.

Write g=gcd(Lambda*d2,L),Lambda=lcm(N,K). By hypothesis length(I_m)>2g.
In the lattice q=N*m+g*Z, any open interval longer than2g contains
two consecutive lattice points q0,q1=q0+g. For example the first
lattice point strictly above the lower endpoint and its successor work.
Both are nonnegative and both have STRICT cap residuals

    z1(q)=s+C*tau_q-(2m+1)A in(-Ke,Ke).

The same integer m is retained for BOTH candidates.

## 2. The actual right-corner guard cannot reject both

The pre-fold right phase inside this cap branch is

    Y(q)=z1(q)+g1*tau_q
        =s+(C+g1)*tau_q-(2m+1)A.

A true right/bottom portal corner occurs iff Y(q)=Ke modulo2Ke.
When this event is nonempty, subtracting solutions gives the exact
q period

    p_bad=K*D/gcd(C+g1,K*D).

Because0<C+g1<D, its gcd is at most C+g1<D, so p_bad>K.
The two q candidates differ by g, and g|K gives0<g<=K<p_bad.
Thus they cannot BOTH be in the bad class. Pick a survivor and fold

    k=floor((Y+Ke)/(2Ke)), z2=Y-2Ke*k.

Then |z2|<Ke is STRICT. This uses the actual endpoint period2Ke,
not an overrestrictive unit-period surrogate. A zero z2 is a smooth
outer-wall reflection. The cap and actual right guards are now simultaneous.

## 3. The same q also supplies actual target compatibility

The terminal phase is

    E=z2+d2*tau=s+D*tau-(2m+1)Ne-2Ke*k
     =z+2eJ, J=q-N*m-K*k an integer.

Both candidates were selected with q=N*m modulo g. Since g|K,
EVERY integer k leaves J divisible by g. Therefore the survivor has
BOTH physical guards AND a soluble full target congruence

    J+p*Lambda*d2=0 modulo L.

Divide by g and invert Lambda*d2/g modulo L/g (use p=0 for modulus1).
Choose0<=p<L/g, and shift tau by2eLambda*p. There is no source
band to preserve; cap index m increases by Lambda*C*p/N, and right
index k by Lambda*g1*p/K, both integers. Literal z1,z2 are identical.
The final E equals z modulo2Le, so F_(Le)(E)=z and actual x=A-z=t.
The target is the nominated actual point, not a residue projection.

The unrestricted starting q=Nm modulo g is material: a strict cap/right
candidate in another class can have an unreachable J along this final
period orbit. Conversely selecting a target-compatible class alone would
not rule out a right corner. Sections1-2 supply that missing intersection.
No claim is made that these sufficient inequalities are necessary.

## 4. Complete original-room optical transfer

Use the upper-source cap/right/bottom charts from accepted CE04:
F_A(s+tau*(eta-u)) until eta=2H-h;
A-F_(Ke)(z1+tau*(eta-(2H-h))) until eta=2H-c;
A-F_(Le)(z2+tau*(eta-(2H-c))) until eta=2H-v.
Actual height is eta up to H and2H-eta afterward. All three open
bands use only actual outer vertical walls. The odd-A cap relation with
|z1|<Ke and right/bottom |z2|<Ke<Le make both interface positions
AND signed derivatives identical. Their endpoints exclude the original
reflex/ledge corners. Zero residuals are smooth outer-wall contacts.

Apply the roof guard to the FINAL selected slope. At u=h a roof corner
would make the two h-mouth coordinates equal, contradicting source
x=s<a<w and final cap-exit x>w. At u>h, if the formal roof phase is
jA, fold symmetry returns at eta*=2H-u in(H,2H-h) to EXACT actual S.
Emit only the descending suffix from that regular source, with its actual
signed departing velocity; no path traverses the discarded corner.
Otherwise the single roof hit is ordinary. All remaining finite-wall and
specular guards are exactly those of the strict original charts.
The cap/right heights exceed v, and on descent the height equals v only
at the end. Source u>=h>c>v excludes an earlier ascent target. Therefore
this reaches FIRST actual T with a finite positive slope and finitely many
ordinary reflections. One final direction controls the full retained ray.

## 5. Entire cap-only native family, with arbitrary cap depth

Let e>=1 integral,P any positive integer,N odd,N>P+L,L=2^j,
2<=K<L with K/g0>=3 for g0=2^v2(K). Equivalently K is not a pure
power of two. Set b anypositive even integer,c=b+1,h=b+2,
H ANY integer>h. Native left-terminal sources have even u>b, so
u>=b+2=h. Thus EVERY remaining terminal source starts in the cap/mouth.
Each native bottom v is even and c is odd, so d2 is odd.

Here Lambda=lcm(N,K) has2-adic valuation v2(K) because N is odd.
As K<L=2^j, v2(K)<j, and hence

    g=gcd(Lambda*d2,L)=g0,
    g|K, K>=3g, K*D/C>K>=3g>2g.

All hypotheses hold for EVERY native terminal pair, with NO gcd in C,
NO prime N, NO cap-depth restriction and NO condition on source P parity.
The accepted TR01/TR05 placement join supplies all other actual pairs
in this ordered original geometry; regular reversal exchanges labels.
Therefore all distinct actual interior even-even pairs illuminate throughout
this full family. Neither counting rooms nor a reflection cutoff is used.

## 6. Entire second family with lower sources allowed

Take e integral,P,K,N odd,K>=3,L a power of two,N>P+L,
ordered integer0<b<c<h,c odd,H=h+epsilon with arbitrary positive integer
epsilon, and gcd(2P*epsilon,N)<K. For native sources BELOW h, C=2epsilon
and the accepted CE04 strict cap hypothesis holds for all such sources.
Lambda_full=lcm(P,N,K) and d2=c-v are odd, so its final target gcd is1.
For native sources AT/ABOVE h, the new lemma has Lambda=lcm(N,K) odd,
g=1 and K*D/C>K>=3>2; it needs no cap gcd or depth bound.
TR01/TR05 and reversal finish all complementary placements. Thus the
whole native family illuminates for composite N and arbitrary cap depths
meeting only the displayed lower-source gcd. Upper native C may fail
that gcd completely. Primality and2epsilon<N are not assumed.

## 7. Fixed hand controls and genuine failed alternatives

A. e4/P1/K3/L4/N9,b1,c3,h6,H10,S(2,8),T(28,2):
C6,g1=3,d2=1,D10,z8, q1 gives tau5 and cap X32 at odd center36.
Then z1=-4,k0,z2=11,E16,J1. Lambda9,g=1,p3 yields tau221,J28,
E232=8 mod32. Old gcd(PC,N)=3=K fails its strict cap bound.

B. SAME widths,b2,c3,h4,H10,S(2,4),T(28,2) is a member of the
unrestricted-depth whole family: q0 gives tau3,X38,z1=2,z2=5,E8,J0,
p0. The source is on the regular actual mouth u=h and no source band
or artificial cut reflection is introduced.

C. e4/P1/K6/L8/N11,b2,c3,h4,H10,S(2,4),T(28,2):
C12,g1=1,d2=1,D14,z16,Lambda66,g2,window length7>4.
At fixed m0, q2 gives tau37/7,z1=150/7,k1,z2=-149/7,E=-16,J=-4.
p2 gives tau7429/7,J128,E1040=16 mod64. Adjacent q1 has BOTH
strict portals but J1 is odd, so no final66-step correction reaches T.
This is exactly why target-compatible q selection is required.

D. e1/P1/K2/L3/N8,b1,c3,h5,H7,S(1/2,6),T(39/5,1):
C3,g1=2,d2=2,D7,z1/5,Lambda8,g=1. For fixed m2, cap window(38,42)
contains q41 and42. q41 gives tau897/70,z1=-37/35,k6,z2=4/7,
E131/5,J13; p2 yields tau3137/70,J45,E451/5=1/5 mod6.
But q42 has cap X199/5=39.8 strict, tau131/10, z1=-1/5 and
right pre-phase26=2 modulo4. It hits the TRUE corner(w,c)=(6,3).
Thus a cap interval alone does not justify any arbitrary q. The actual
corner-period argument is needed to retain q41 while discarding42.

These are hand-prescribed arithmetic checks, not discovery searches.
No formula control substitutes for the quantified physical proof. The
full spiral/r3/r<=8 theorem still has genuinely uncovered cases.
