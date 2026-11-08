# A uniform sampling bound for finite rational portal orbits

Codex01a18403. Candidate hand theorem; independent review required. No computer enumeration enters this proof.

## Statement

Normalize d=g=1. Let alpha=A/q, beta=C/q with integers 0<A<C<q and gcd(A,C,q)=1. If q>100 and there is no nonzero pair of integers (m,n) with

    |m|+|n|<=4 and m*alpha+n*beta in Z,

then EVERY translate of the finite orbit

    {4j(alpha,beta) modulo 4 : j=0,...,q-1}

meets every open axis-parallel unit square on the period-4 two-torus.

In particular, for every real source/target horizontal placement s,t, the original common portal chart (both portal residues strictly in (1,2)) succeeds. It gives a legal actual connection reflecting only in vertical walls. Endpoint-cap sheets are not needed in this class.

Contrapositively: a failure of the full eight-chart vertical-only mechanism with no relation of l1 norm at most 4 must have primitive phase denominator q<=100. This does NOT prove that these remaining finitely many phase pairs have no failing endpoint placements. Their continuous endpoint squares still need exact coverage proofs or an exact counterexample. Rational parameter denominators are not globally bounded by this result: the short-relation families remain unbounded.

## 1. A short annihilator from an area argument

Define the integer lattice

    Lambda={(m,n) in Z^2 : mA+nC=0 modulo q}.

The map Z^2->Z/q given by (m,n)->mA+nC is surjective since gcd(A,C,q)=1. Therefore Lambda has index, and fundamental area, q.

Let w be the smallest nonzero l1 length |m|+|n| in Lambda. Then

    w<=sqrt(2q).

Here is the elementary area argument, including the constant. For any R>sqrt(2q), the open l1 diamond of radius R/2 has area R^2/2>q. Fold it into a fundamental parallelogram for Lambda. Integrating the number of preimages over that parallelogram gives the diamond's area. If every folded point had at most one preimage almost everywhere, this area would be at most q. Thus two distinct diamond points differ by a nonzero lattice vector. Its l1 length is less than R. Let R decrease to sqrt(2q); the integer minimum w obeys the asserted weak inequality.

Choose a minimizing vector (m,n) and set r=(mA+nC)/q. The triple (m,n,r) is primitive: a common divisor greater than one would give a strictly shorter nonzero vector of Lambda after division. Put g=gcd(|m|,|n|). Then gcd(g,r)=1. Also g divides q, because g divides rq and is coprime to r.

Under the theorem's hypothesis, w>=5.

## 2. The finite orbit samples all components, with an exact spacing

Work in R^2/(4Z)^2. Write v_j=v0+4j(A,C)/q for an arbitrary offset v0. All orbit points lie on

    m x+n y = m*v0_x+n*v0_y modulo 4.                 (1)

This level set consists of g parallel circles. Their common Euclidean circumference is

    length = 4*sqrt(m^2+n^2)/g,

because a primitive integer tangent vector is (-n/g,m/g), with parameter period 4.

The component label of v_j changes by r modulo g. Since gcd(r,g)=1, the orbit visits ALL g components. The orbit has q distinct points: its order is q because gcd(A,C,q)=1. Each component contains exactly q/g orbit points. On each component these points form a coset of a finite subgroup of that circle, so they are equally spaced. This last assertion follows by identifying the circle with R/Z: every finite subgroup of order k is {j/k : 0<=j<k}. Hence the exact Euclidean spacing along every component is

    spacing = 4*sqrt(m^2+n^2)/q.                     (2)

This counts disconnected components; replacing the level set by just its identity component would be invalid.

## 3. An open segment inside any unit portal square

Take any lift of an open axis-parallel unit square, with center z. The lifted components of (1) are the parallel lines

    m x+n y = m*v0_x+n*v0_y+4k, k in Z.

Choose one whose normal value differs from m*z_x+n*z_y by delta0 with |delta0|<=2. The point

    z' = z + (delta0/w)*(sign(m),sign(n))

is on that line. Each coordinate of z' differs from its square center by at most 2/w. Thus z' has l-infinity clearance at least

    rho=1/2-2/w=(w-4)/(2w)>0

from the square boundary. An open Euclidean segment of radius rho about z', tangent to the line, lies inside the open square: each coordinate displacement is at most its Euclidean displacement. Its length is 2rho=(w-4)/w.

If spacing (2) is strictly less than 2rho, this segment contains an orbit point, regardless of the offset of the uniform grid along its circle. Strict inequality ensures an interior hit even if a grid point lands at a segment endpoint. It is enough that

    q > 4w*sqrt(m^2+n^2)/(w-4),

and, since sqrt(m^2+n^2)<=w, it is enough that

    q > f(w), where f(w)=4w^2/(w-4).                 (3)

## 4. q>100 makes the sufficient bound automatic

For 5<=w<=sqrt(2q), f decreases up to 8 and increases after 8, since

    f'(w)=4w(w-8)/(w-4)^2.

Therefore its maximum on this interval is at an endpoint. At the first endpoint f(5)=100<q. At the other,

    f(sqrt(2q)) = 8q/(sqrt(2q)-4) < q,

because q>100 implies sqrt(2q)>12. Thus q>f(w), proving (3) and the required hit in any unit square.

## 5. Connection to the actual corridor

For the common original chart with target image t+4M, the two portal residues are

    E1=(1-alpha)s+alpha*t+4M*alpha,
    E2=(1-beta)s+beta*t+4M*beta modulo 4.

This is exactly an arbitrary offset plus the finite orbit in the statement. Applying the sampling result to (1,2)^2 supplies an integer M, 0<=M<q, with both portal crossings strict. The accepted common-chart folding lemma gives a finite actual corner-free specular S-to-T path. No phase-density argument for a finite orbit, reflection cutoff, limiting path through a corner, or assumed ending copy occurs here.

## Remaining proof task

The result justifies a FINITE exact check of the proposed stronger statement that every vertical-only failure has some annihilator of l1 norm at most 4: check primitive phases q<=100 with no such annihilator over the whole continuous endpoint square. A bounded endpoint grid does not suffice. If any endpoint cell fails, that refutes the stronger statement but leaves this q>100 theorem intact.

Even the stronger norm-four statement would not finish the room goal: the short-relation families, their four cap sheets, and remaining rational endpoint placements would still need universal closure. This packet is a uniform reduction, not a complete illumination theorem for the room family.
