# Exact full-fiber shear stabilizers on the square calibration

Independent hand challenge of WR01 availability. The author candidate was read before its final argument. No final author packet is accepted here before its pins arrive. This proof covers all n>=2 and all pure affine shear powers/translations, not a direction cutoff or a finite test.

## Actual marked surface

Put B=8n^2. The connected four-copy reflection unfolding of [0,B]^2 is M=R^2/(2B Z^2). In the usual physical projection its actual source fiber is

    X={(epsilon B/2,delta B/2):epsilon,delta in {+1,-1}},

and actual target fiber is

    Y={(epsilon (B/2+2n),delta (B/2+2)):epsilon,delta in {+1,-1}},

with coordinates taken modulo 2B. The four forbidden lifts of the physical convex corners are

    Sigma={(0,0),(B,0),(0,B),(B,B)}.

They are regular surface points but forbidden physical corner marks. None is an endpoint. These are complete physical fibers; one chosen target image is not substituted for Y.

A horizontal pure affine shear on this torus has form

    F(x,y)=(x+a y+c_x,y+c_y).

Its derivative preserves the lattice 2B Z^2 iff a is an integer: applying it to (0,2B) gives (2Ba,2B). The inverse then preserves the lattice too. Translations c are torus-valued. Similarly a vertical pure affine shear has integer coefficient b.

## Horizontal stabilizer, including translations

Assume F(X)=X and F(Y)=Y setwise. Since X is the coset (B/2,B/2)+B Z^2 modulo2B, preservation of X implies

    c_y in {0,B},  c_x+a B/2=0 modulo B.

The two-point set {+t_y,-t_y}, t_y=B/2+2, has no nonzero translation stabilizer. Indeed a nonzero translating symmetry of a two-point set must exchange its points, requiring 4t_y=0 modulo2B. But 4t_y=2B+8 and 2B=16n^2 does not divide8 for n>=2. Therefore Y preservation forces c_y=0 modulo2B.

For each fixed target y=+t_y or -t_y, the x pair {+t_x,-t_x}, t_x=B/2+2n, is also nonantipodal: 4t_x=2B+8n is not0 modulo2B for n>=2. Its translating stabilizer is trivial. Consequently

    c_x+a t_y=0 modulo2B,
    c_x-a t_y=0 modulo2B.

Reduce the first equation modulo B and compare it with the source equation. It gives 2a=0 modulo B, hence a=4n^2 k for an integer k. Substituting in the target equation yields

    c_x=B k modulo2B,  c_y=0.

Conversely these data do preserve both X and Y: a B/2=16n^4 k is0 modulo2B, and 2a=B k, so c_x +/- a t_y is0 modulo2B. They preserve Sigma as well: a B is0 modulo2B and c_x is0 or B. We have therefore proved the EXACT stabilizer in this horizontal affine-shear class, even though setwise corner preservation was not needed for necessity.

## Vertical stabilizer

Now F(x,y)=(x+c_x,y+b x+c_y). Source preservation gives

    c_x in {0,B},  c_y+b B/2=0 modulo B.

The nonantipodal target x pair forces c_x=0 modulo2B. For each target x sign the y pair then forces

    c_y+b t_x=0 modulo2B,
    c_y-b t_x=0 modulo2B.

Comparison modulo B gives 2n b=0 modulo B=8n^2, so b=4n k. Substitution gives c_y=B k modulo2B. Conversely these coefficients/translations preserve X,Y and Sigma. Thus the exact vertical stabilizer is

    b=4n k,  c_x=0,  c_y=B k modulo2B.

Neither derivation assumed pointwise endpoint fixing. The result includes every allowed translation and all integer powers in the specified pure-shear class.

## WR01 rank consequence

The direct actual interior ray has primitive direction w=(n,1). For a nonzero horizontal stabilizer coefficient a=4n^2 k,

    |n+a| >=4n^2-n > n.

For a nonzero vertical coefficient b=4n k,

    |1+b n| >=4n^2-1 >1.

Thus EVERY nontrivial allowed horizontal or vertical pure shear strictly INCREASES rho=|p|+|q| at this direction. Replacing the map by its inverse only changes k's sign and is already covered. k=0 is the identity and does not decrease rank. The actual pair is illuminated directly, with no reflections, and r=0.

This rigorously rejects WR01's proposed universal availability of a decreasing pure marked-fiber shear step for every non-axis direction, even with arbitrary setwise fiber-preserving translations. It does not reject the validity of a particular global affine transfer, the conditional strict-rank rule where it applies, composite non-parabolic affine maps, a different rank, an induced tower reconstruction, or illumination itself. A rule that accepts a direction as an illuminated terminal case before reducing it avoids this particular availability claim but then must PROVE terminal recognition and global terminal availability. No such completion is supplied here.

The accepted growing primitive norm calibration is respected. These arithmetic congruences retain all n and all k; no finite state quotient or bound depending only on W is inferred. No claim involving nine distinct reflex corners follows.
