# Rational mouth section: exact finite-state repair, not nonemptiness

This hand derivation corrects the proposed identification of LR01 with a walk on interior A points. It uses LR01's already accepted physical map. It creates no new search, engine, cutoff, positive family or optical existence claim.

Fix any original integral ordered spiral and a native actual source. Normalize |vy|=1 and fix tau=p/q>0 in lowest terms. A valid signed upward left-mouth state is xi in(-a,a), encoding position |xi| and horizontal velocity tau*F'_a(xi); at xi=0 choose the outgoing smooth-wall convention. Put k=q*xi.

## 1. Native arrivals lie on a direction-dependent rational grid

Every unfolded image of an even-even source has even integer coordinates. At a physical height h, developed ordinates differ from h or -h by even integers. A ray of slope magnitude p/q therefore satisfies, after any finite integer-wall development,

    q*x_developed = even*q + p*(h + even), up to signs,
    k is an integer and k = p*h (mod 2).

Centering the signed phase subtracts an even integer wall period. Multiplication by q preserves this parity. Thus all legal native-source mouth arrivals are contained in

    K_(p,q) = { k in Z : -a*q < k < a*q, k = p*h (mod 2) }.

This retains the signed coordinate; +k and -k generally encode different physical germs. Its size is aq-1 when aq and ph have the same parity, otherwise aq. Zero is included only when its parity is allowed and denotes one outgoing regular-wall state. Actual h-reflex endpoints k=+/-aq are excluded.

This is a containment, not a claim that every grid point is accessible from the source. Repeating the same argument backward from native T gives the SAME necessary parity class at height h. Consequently this parity invariant does not by itself separate the source and target fibers or force their intersection.

## 2. LR01 preserves this grid with every physical guard

A genuine cap L-exit at descending contact n and its following floor return have

    k_d = k + 2n*beta*p - 2A*q*m,
    k_u = k_d + 2V*p - 2a*q*i,

where beta=H-h and V=h-b. Both are integers in the same parity class. The exact LR01 guards become

    a*q < q*F_A(xi+2j*beta*p/q) < w*q for all earlier cap contacts,
    k+(2j-1)*beta*p not in A*q*Z for all roof contacts,
    k_d+V*p not in a*q*Z at the actual left floor,
    -a*q < k_u < a*q at the actual return.

Use the original fold and signs, rather than interpreting these inequalities as permission to reflect at a mouth. The inherited map is a partial injection on its actual reachable subset of K_(p,q), because LR01's physical reverse path is unique. A failed guard terminates the declared programme.

Each cap episode from L is finite at rational tau: the descending phase increment is 2beta*p/q modulo 2A. Its order is

    Aq / gcd(beta*p,Aq) <= Aq.

At that order it returns to its starting signed L phase, so a regular first mouth exit occurs no later, unless an earlier original corner terminates it. This is a per-fixed-rational-direction fact, not a uniform direction cutoff.

## 3. Correct stopped outcomes and limit of a finite rank

From an admitted upward L state, the stopped LR01 programme has four possibilities:

1. A first R exit and the declared tail attains actual T (or its proved legal actual-T prefix).
2. A true corner or another required physical guard fails before success.
3. A first R exit occurs, but the declared tail misses T. The restricted return programme stops; the real billiard trajectory can continue outside it.
4. Legal left returns repeat a signed mouth state and hence form a periodic cycle without a successful R exit.

At fixed p/q there are at most |K_(p,q)| distinct admitted mouth states before a repeat or stop. For a deterministic partial injection any repeat in a forward orbit already forces return to its initial state: cancel the common iterates using injectivity. Thus the number of unseen reachable states is a valid finite tracing rank at fixed direction. It does NOT force success, because outcomes 2–4 remain possible. The state bound depends on q, which is unbounded over all candidate directions. The cap-contact bound GSE05 controls a different index and does not replace q by its Q.

This repair gives exact phase-space matching and all stopped outcomes, rather than an all-word or target-existence theorem. Any positive argument must prove success for some common p/q with the ORIGINAL source and actual target, and must separately justify coverage of any physical continuations omitted at outcome 3. No pigeonhole argument from the finite state count alone does so.
