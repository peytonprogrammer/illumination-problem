# A finite parameter reduction for every critical-line rectangle family

Codex01a18403. Candidate exact affine proof with hand sampling argument. Independent review required. This does not complete the finite optical cases or the room theorem.

## Input and exclusions

The exact RREF classification critical-rectangles.py/json assigns one of the10critical depth lines to each of the four rectangle corners (a,b),(A,b),(a,B),(A,B), imposing a,b>0,A>a,B>b. It records90one-parameter affine families and288isolated points, with no feasible higher-dimensional family. This classification is an independent pending proof dependency.

Sixteen families have an effective depth equality identically on at least one sheet. The accepted outer-leg-transfer/equal-effective-depth result closes them at all endpoint placements. Seventy-four families remain. The present packet treats those74.

For each family, parameter lambda is one recorded free coordinate, and each depth is affine over Q. Each of the four one-pass sheet pairs has its recorded primitive short-relation triple. Each three-pass sheet pair has the primitive triple derived in three-pass-circle.md.

## Circle guards with a physical phase margin

For a one-pass sheet, shrink every unit portal interval by eta at both ends. Its circle intersection is represented by the two strict affine endpoint guards in short-line-margin.md.

For a three-pass sheet, shrink the entry, two intermediate ledge residue intervals and exit interval by eta at both ends. Their intersection in the phase coordinates (E,v mod4) is an open convex polygon. Polygon vertices and linear-form extrema are computed exactly with Fraction arithmetic. The required circle level meets this polygon exactly when its value lies strictly between the two normal extrema. These are again two strict affine guards in actual s,t.

family-joint-margin.py generates the one-pass clauses of all four sheets and then the three-pass clauses of all four sheets. Starting from CLOSED [0,1]^2, it subtracts their OPEN intersections with the frozen closed-complement helper. Axis points, edges and vertices are retained. Every one of the74families is COMPLETELY covered already at eta=1/8. The JSON stores the actual guard clauses that changed the residual set, ending in an empty complement, plus their sheet, mode, primitive relation and cutoff. The program never samples endpoint coordinates.

The cover is uniform in the family parameter: the circle normals depend on the affine family, not on lambda. Every strict guard certifies the selected relation-level intersection for all real endpoint values in its open cell.

## Quantitative sampling without Euclidean overestimates

For a primitive relation mE+nv=C modulo4, the tangent vector is (-n,m). Parameterize the connected lifted line by (E,v)+tau*(-n,m). The finite rational phase orbit samples each of its components in equally spaced tangent-parameter increments4/q. This follows from the exact component/spacing calculation in lattice-sampling.md: the Euclidean spacing4*sqrt(m^2+n^2)/q divided by the tangent vector length is4/q.

For one-pass coordinates (E1,E2), each original interval guard changes along this tangent by coefficient -n or m. If the chosen point is in the eta-shrunken rectangle, an open tangent interval of length at least2eta/K stays inside the original rectangle, where K=max(|m|,|n|).

For three-pass coordinates (E,v), the physical interval arguments are E+jv, j=0,1,2,3. Their tangent derivatives are jm-n. Hence the same conclusion holds with

    K=max_{j=0,1,2,3}|jm-n|.

K>0 because (m,n) is nonzero. The artificial choice of a fundamental range for v does not create a physical boundary; the tangent segment can pass to the neighboring period-4 chart. All actual wall guards still remain strict by the interval margin. Thus the rational orbit hits the original physical phase window whenever

    q>2K/eta.                                       (1)

This is a finite equally-spaced-grid argument, not density. Strict inequalities preserve portal/ledge corner avoidance.

## Compare one-pass and three-pass denominators

For rational effective depths U=p/D,V=r/D in minimal joint denominator, gcd(p,r,D)=1. The one-pass primitive phase denominator is q1=p+r+D, since gcd(p,p+D,p+r+D)=gcd(p,r,D)=1. The three-pass denominator for phases U/(U+V+3),1/(U+V+3) is q3=p+r+3D by the same gcd calculation. Therefore

    q3=q1+2D>q1, and q3<3q1.

For a one-pass clause use q1 in (1); for a three-pass clause use q3. If the corresponding sheet q1 exceeds the clause's recorded cutoff, so does q3. Consequently, if ALL FOUR one-pass sheet denominators exceed the maximum cutoff Q among the clauses in a family cover, every actual endpoint placement has a guaranteed one-pass or three-pass hit on some sheet.

The computed Q values are32,48or64; the maximum over ALL74families is64.

## The genuinely finite remaining parameter obligation

If a rational member of one of these74families remains unclosed, at least one of its four one-pass sheets must have primitive phase denominator q1<=Q<=64. There are finitely many such phases 0<A<C<q1. Inverting gives its effective depths A/(C-A),(q1-C)/(C-A). The affine family equations determine lambda from that sheet, because neither effective pair is constant in these74non-equality families. Checking the recorded open parameter interval and the other depth equality gives an exact finite list of candidate family parameters.

This is an analytic justification for the cutoff. Enumerating those parameters is not a sample of arbitrary real rooms. The actual finite rooms must still be proved illuminated by strict continuous endpoint covers or another rigorous construction, and the RREF and margin certificates require independent review. Mixed rectangles containing one of the11finite exceptional depth points must be enumerated separately. No full room theorem is claimed before these obligations close.
