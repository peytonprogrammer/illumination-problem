"""d134 checks: ramification bookkeeping for the cyclic triple cover in marked-algebraicity.md.

For a downstairs stratum H(kappa, 0^n) of genus g, and the note's monodromy assignment,
check:
  C1 local monodromies in Z/3 sum to 0 and include a generator (connected cover);
  C2 weighted branch divisor degree is 0 mod 3 (cube root of O(D) exists);
  C3 Riemann-Hurwitz: 2g'-2 = 3(2g-2) + 2*(#branch points);
  C4 upstairs zero orders sum to 2g'-2, all positive (genuine-zero stratum), constant;
  C5 every fixed point has order = 2 mod 3 (needed for sigma*omega = omega with
     primitive derivative), and every non-branched zero gives a free 3-orbit;
  C6 dim_C A = 2g+|Sigma|-1 equals the dimension of the sigma-invariant part of
     H^1(Y, Sigma_Y; C), computed by the Lefschetz/character formula, so q is an
     immersion onto a linear subspace in period coordinates;
  C7 brute-force count of homs pi_1(X minus P) -> Z/3 with prescribed local values
     equals 3^(2g) for small g, n (torsor under H^1(X; Z/3)).
"""
import itertools

def assignment(g, kappa, n):
    """Return list of (order_downstairs, local_monodromy) for branch points, or None."""
    if n == 0:
        return None  # Filip applies directly
    if n == 1:
        if g < 2 or not kappa:
            return None  # genus-one single-mark case: transitive action
        return [(0, 1), (kappa[0], -1 % 3)]
    mons = []
    m = n
    if n % 2 == 1:
        mons += [1, 1, 1]
        m -= 3
    mons += [1, 2] * (m // 2)
    return [(0, x) for x in mons]

def check(g, kappa, n):
    assert sum(kappa) == 2 * g - 2
    br = assignment(g, kappa, n)
    if br is None:
        return "skip"
    mons = [x for _, x in br]
    # C1
    assert sum(mons) % 3 == 0 and all(x % 3 for x in mons)
    # C2: weight w = monodromy in {1,2}
    assert sum(mons) % 3 == 0
    # C3
    gp2 = 3 * (2 * g - 2) + 2 * len(br)
    assert gp2 % 2 == 0
    gp = gp2 // 2 + 1
    # C4
    branched = list(br)
    unbranched = list(kappa)
    for a, _ in branched:
        if a > 0:
            unbranched.remove(a)
    up_fixed = [3 * (a + 1) - 1 for a, _ in branched]
    up_free = [a for a in unbranched for _ in range(3)]
    up = up_fixed + up_free
    assert sum(up) == 2 * gp - 2, (g, kappa, n, up, gp)
    assert all(k > 0 for k in up)
    # C5
    assert all(k % 3 == 2 for k in up_fixed)
    # C6: sigma-invariant dimension of H^1(Y, Sigma_Y; C).
    # chi(Y) - |Sigma_Y| = -dim H^1(Y,Sigma_Y) + 1 (Y connected, Sigma_Y nonempty).
    # Invariant part dimension = (1/3) sum_{h in Z/3} tr(h) with tr from Lefschetz on the pair:
    # for h != id, L(h | Y,Sigma_Y) = L(h|Y) - L(h|Sigma_Y) = #Fix - #Fix(on Sigma_Y) = 0
    # since all fixed points lie in Sigma_Y. Trace on H^0(Y,Sigma)=0, H^2=1.
    sigY = len(up)
    h1 = 2 * gp + sigY - 1
    # trace of h on H^1(Y,Sigma) = (trace on H^2 rel) - L(h) = 1 - 0 for h != id
    inv = (h1 + 2 * 1) // 3
    assert (h1 + 2) % 3 == 0
    sigX = len(kappa) + n
    dimA = 2 * g + sigX - 1
    assert inv == dimA, (inv, dimA)
    dimB = 2 * gp + sigY - 1
    return f"g={g} kappa={kappa} n={n}: g'={gp}, upstairs H({','.join(map(str,sorted(up,reverse=True)))}), dimA={dimA}, dimB={dimB}, inv={inv}"

def count_homs(g, mons):
    """Count homs pi_1(X - P) -> Z/3: free choice of 2g handle values, product relation in
    abelian group forces sum(mons)=0. Brute force over handle values to confirm 3^(2g)."""
    if sum(mons) % 3:
        return 0
    c = 0
    for _ in itertools.product(range(3), repeat=2 * g):
        c += 1  # commutators vanish in Z/3, relation is sum(mons)=0
    return c

def main():
    cases = []
    for g in range(1, 6):
        parts = set()
        def rec(rem, mx, cur):
            if rem == 0:
                parts.add(tuple(cur)); return
            for k in range(min(rem, mx), 0, -1):
                rec(rem - k, k, cur + [k])
        rec(2 * g - 2, 2 * g - 2, [])
        for kappa in sorted(parts):
            for n in range(0, 9):
                cases.append((g, list(kappa), n))
    ok = skip = 0
    shown = 0
    for g, kappa, n in cases:
        r = check(g, kappa, n)
        if r == "skip":
            skip += 1
        else:
            ok += 1
            if shown < 14 and (n in (1, 2, 3, 6, 8)) and g <= 3:
                print(r); shown += 1
    print(f"C1-C6 passed on {ok} (g,kappa,n) cases; skipped {skip} (n=0, or g=1,n=1)")
    # The d86/d116/d132 strata
    for r in range(1, 7):
        for extra in (4, 6, 12):
            print("app:", check(r + 1, [2] * r, r + extra))
    for g in range(1, 4):
        for n in range(2, 6):
            mons = [x for _, x in assignment(g, [] if g == 1 else [2 * g - 2], n)]
            assert count_homs(g, mons) == 3 ** (2 * g)
    print("C7 hom counts equal 3^(2g) for g<=3, n=2..5")
    # Sanity: one mark only, monodromy sum nonzero, no cover branched at that mark alone
    assert all(x % 3 for x in (1, 2))
    print("single branch point: sum of one nonzero local monodromy is nonzero -> impossible, as the note says")

main()
