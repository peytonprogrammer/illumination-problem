# A horizontal far-end twist repairs a midpoint mouth corner

A37 candidate, pending independent review. This handles a mouth-ENDPOINT obstruction, separately from the peer's smooth far-wall midpoint splice. No global room symmetry is required.

## Geometry and claim

Use a rectangular core [0,c] x [y_min,y_max]. Two right teeth have the SAME width w>0, height2, and bands centered at mu-h and mu+h, h>1. Both actual marks have the SAME depth D, 0<D<w:

    S=(c+D,mu-h), T=(c+D,mu+h).

Both selected tooth bands and the core lie in the actual strictly simple room. Other attachments are permitted, provided their interiors do not remove a used selected-tooth wall. The open left-core segment x=0, mu-1<y<mu is required to be a smooth actual mirror. At y=mu an opposite tooth may begin: that point can be a genuine mouth corner. No reflecting wall at that point is assumed.

There is a finite actual corner-avoiding S/T path if the explicitly constructed slope below has (w-D)*tau noninteger. For integer c,D,w,h the sufficient arithmetic condition

    gcd(c+D,2(w-D)) does NOT divide h(w-D)                  (1)

guarantees this nonresonance, and hence illumination. All selected endpoints are actual; no far-end image replaces the target physically.

## 1. The finite matching slope and opposite central displacements

Put z=w-D>0, D_f=2w-D=D+2z and B=2(w+c). Define

    n_f(tau)=floor(D_f*tau/2+1/2),
    n_d(tau)=floor(D*tau/2+1/2),
    Phi(tau)=[2h+2n_f(tau)+2n_d(tau)]/B.

Iterate from tau0=0. The accepted A32 proof applies to virtual midpoint depths D_f,D, both height2, with vertical selected separation H=2h+2. The map is nondecreasing, positive at0, bounded on [0,(h+1)/c], and has finitely many outputs there. Its first stationary value tau>0 is not a floor jump. Thus

    r_f=D_f*tau+1-2n_f in(0,2),
    r_d=D*tau+1-2n_d in(0,2),
    r_f+r_d+2c*tau=2h+2.                                  (2)

The virtual source-only-far construction has central left-wall ordinate

    mu+m, m=(r_f-r_d)/2=z*tau-(n_f-n_d) in(-1,1).          (3)

Interchanging the two virtual depths leaves Phi, its entire iteration and tau unchanged. It exchanges r_f,r_d and therefore gives central ordinate mu-m. This interchange means choosing the TARGET-only far image instead of the source-only far image; actual S and T remain fixed.

Furthermore

    m=0  iff  z*tau is an integer.                         (4)

The forward implication follows directly from (3). Conversely, if z*tau is integral, (3) is an integer, and m in(-1,1) forces m=0.

If z*tau is nonintegral, choose the source-only or target-only far chart for which its central ordinate is mu-|m|. It lies STRICTLY in the protected actual mirror segment (mu-1,mu). Both open central legs have 0<x<c. They cannot hit any other tooth or its mouth corner. Strict selected portals come from (2), including their nonzero lower residues.

## 2. Why the horizontal far chart is an actual path

For the lower far chart, temporarily use the virtual midpoint source at x=c+D_f in a tooth extended to that abscissa. Fold the part x>c+w back across the ACTUAL selected far wall x=c+w. Its starting point becomes exactly x=c+D, so it starts at actual S. Its physical first horizontal motion is toward the far wall, reflects there once, then moves left to the strict mouth. Its vertical folds are the same legitimate +/- midpoint images used in A32. Horizontal and vertical folds commute inside the rectangle.

Every horizontal tooth contact is strictly beyond the mouth, at c<x<=c+w; equality at the far wall is the only possible corner. At that far crossing, the unfolded horizontal distance from the virtual source is z. A source middle-row ordinate is one unit from either horizontal boundary. Therefore a simultaneous far/horizontal contact requires

    z*tau to be an ODD integer.

Our nonintegrality hypothesis excludes this. The actual far contact is consequently smooth, and all horizontal contacts have c<x<c+w. No corner purification or legal passage through a vertex is needed.

The target-only far chart is the reversed upper version of the same construction. Its final reflected horizontal image folds to the actual T. Its possible far corner has the same necessary odd-integer phase z*tau and is excluded. Its other contacts are also strict. The actual source/target may be met earlier along a folded rectangle trace; truncate at the first actual T, after the last prior actual S if necessary. With no corners anywhere in the constructed trace, such truncation preserves a legal actual connection.

The selected source/target arms and central core legs use no mirror in another tooth. A virtual selected rectangle need not be a subset of the physical room: its sole removed portion x>c+w is explicitly reflected into the ACTUAL selected rectangle. This is reflection at the actual far end, not an optical monotonicity assertion under adding or deleting a chamber.

All contact counts are finite by the finite A32 matching construction. This proves the real-data nonresonance theorem.

## 3. A sufficient exact arithmetic exclusion of resonance

Assume c,D,w,h are positive integers with w>D and h>1. Suppose, for contradiction, that m=0. Put p=z*tau, an integer by (4). From (2) and equal residuals, the central ordinate mu is equivalent to

    (D+c)*tau=h+2n_d.

Multiplying by z gives the integer equation

    (D+c)*p - 2z*n_d = h*z.                               (5)

Its left side is divisible by gcd(D+c,2z). Condition(1) makes (5) impossible. Therefore m is nonzero and the actual path in sections1–2 exists. No upper bound on the floor indices, ray count or reflection count is being inferred from a finite sample.

Equivalently, condition(1) holds precisely when h is odd and

    v_2(D+c) > v_2(w-D),

where v_2 is the exponent of2 in a nonzero integer. To verify equivalence, the odd part of gcd(D+c,2z) already divides z, and its2-part exceeds that of hz exactly in the stated case. Equation(5) is only a necessary resonance condition; when it has integer solutions, the constructed first stationary slope may still be nonresonant. Divisibility NEVER implies darkness.

## 4. An uncapped canonical thin-comb consequence

In an integer two-sided height2 comb with globally separated tooth bands, suppose two right middle-row actual A marks have the same even x=X, their selected right far ends have the same ODD x=R, and their mean ordinate mu is ODD. Set h=(y_T-y_S)/2>1. Since y_S,y_T are even, h is odd. Here D+c=X is even and z=w-D=R-X is odd, so (1) holds.

If an opposite tooth begins at mu and extends upward, global positive integer gaps ensure that the whole interval (mu-1,mu) on x=0 is an actual smooth mirror: any other left tooth ending below mu ends at most at mu-1. The theorem therefore gives a legal actual connection around this genuine mouth corner. An opposite tooth ending at mu is covered after reflecting y about mu, with the protected mirror interval above it instead. Arbitrary other teeth, widths and gaps do not affect the guarded path.

This covers every parameter choice meeting those explicit hypotheses, with no k, area, diameter, size or growth-ratio cap. It is a positive mouth-corner repair even for shallow marks. It complements the peer's centered-opposite-opening repair. Unequal actual depths or unequal outer far-end widths, even midpoint ordinates, and resonant divisibility branches are not covered automatically. No universal W<=21 conclusion, dark counterexample is made.
