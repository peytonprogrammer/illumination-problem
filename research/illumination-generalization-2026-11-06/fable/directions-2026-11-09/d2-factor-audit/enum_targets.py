"""Enumerate flat spheres N covering the unit pillowcase with the parity property.

Model.  The pillowcase PC = double of [0,1]^2 has corners A=(0,0), C1=(1,0),
B=(1,1), C2=(0,1).  A degree-d cover N has front faces f_0..f_{d-1} and back
faces g_0..g_{d-1}.  Label back faces so that f_i and g_i share the bottom edge
(y=0).  Three permutations describe the other gluings:
    left  edge (x=0) of f_i is glued to g_{lam[i]}
    right edge (x=1) of f_i is glued to g_{rho[i]}
    top   edge (y=1) of f_i is glued to g_{the[i]}
Lattice points of N are cycles of
    A : lam            C1: rho
    B : the^-1 rho     C2: lam^-1 the
and a cycle of length k is a point of cone angle k*pi.

Parity property: non-A classes have only cycle lengths 1 and 3.
Admissible: all cycle lengths <= 3 (needed for an orthogonal double to cover N).
No room enumeration happens here; this only lists the possible targets N.
"""
import itertools
import sys


def cycles(p):
    seen, out = set(), []
    for i in range(len(p)):
        if i not in seen:
            c, j = [], i
            while j not in seen:
                seen.add(j)
                c.append(j)
                j = p[j]
            out.append(tuple(c))
    return out


def ctype(p):
    return tuple(sorted(len(c) for c in cycles(p)))


def inv(p):
    q = [0] * len(p)
    for i, x in enumerate(p):
        q[x] = i
    return tuple(q)


def mul(p, q):
    """(p*q)(i) = p[q[i]] (apply q first)."""
    return tuple(p[x] for x in q)


def transitive(gens, d):
    seen, stack = {0}, [0]
    while stack:
        i = stack.pop()
        for g in gens:
            for h in (g, inv(g)):
                if h[i] not in seen:
                    seen.add(h[i])
                    stack.append(h[i])
    return len(seen) == d


def canon(triple, d):
    best = None
    for s in itertools.permutations(range(d)):
        si = inv(s)
        t = tuple(mul(mul(s, p), si) for p in triple)
        if best is None or t < best:
            best = t
    return best


def classes(lam, rho, the):
    return {
        "A": lam,
        "C1": rho,
        "B": mul(inv(the), rho),
        "C2": mul(inv(lam), the),
    }


def local_structure(lam, rho, the):
    """For each A point, list its 8 neighbours counterclockwise from E.

    Each neighbour is (class, cone angle in units of pi, id of the point).
    Valid for regular A points (2-cycles of lam) and poles (fixed points).
    """
    cl = classes(lam, rho, the)
    ptid = {}
    for name, perm in cl.items():
        for c in cycles(perm):
            for i in c:
                ptid[(name, i)] = (name, len(c), min(c))
    rinv = inv(rho)
    out = {}
    for c in cycles(lam):
        nb = []
        for i in c:  # quadrants: front i, back lam[i]
            nb.append(("E/W", ptid[("C1", i)]))
            nb.append(("diag-front", ptid[("B", i)]))
            nb.append(("N/S", ptid[("C2", i)]))
            nb.append(("diag-back", ptid[("B", rinv[lam[i]])]))
        out[("A", len(c), min(c))] = nb
    return out


def enumerate_targets(d):
    perms = list(itertools.permutations(range(d)))
    t13 = [p for p in perms if set(ctype(p)) <= {1, 3}]
    t123 = [p for p in perms if set(ctype(p)) <= {1, 2, 3}]
    # lam up to conjugacy: one representative per cycle type
    reps = {}
    for p in t123:
        reps.setdefault(ctype(p), p)
    found = {}
    for lam in reps.values():
        li = inv(lam)
        for rho in t13:
            for mu in t13:  # mu = the^-1 rho  => the = rho mu^-1
                the = mul(rho, inv(mu))
                if set(ctype(mul(li, the))) - {1, 3}:
                    continue
                if not transitive((lam, rho, the), d):
                    continue
                cl = classes(lam, rho, the)
                poles = sum(ctype(p).count(1) for p in cl.values())
                zeros = sum(ctype(p).count(3) for p in cl.values())
                if poles - zeros != 4:
                    continue  # genus 0 <=> Gauss-Bonnet
                key = canon((lam, rho, the), d)
                found[key] = (lam, rho, the)
    return found


if __name__ == "__main__":
    dmax = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    for d in range(1, dmax + 1):
        res = enumerate_targets(d)
        print(f"== d={d}: {len(res)} parity targets (up to relabelling)")
        for key in sorted(res):
            lam, rho, the = key
            cl = classes(lam, rho, the)
            desc = {k: ctype(v) for k, v in cl.items()}
            pA, RA, zA = (desc["A"].count(k) for k in (1, 2, 3))
            zN = sum(v.count(3) for v in desc.values())
            print(f"  z_N={zN} p_A={pA} R_A={RA} z_A={zA}  types={desc}")
            print(f"     lam={lam} rho={rho} the={the}")
            if "-v" in sys.argv:
                for pt, nb in local_structure(lam, rho, the).items():
                    print(f"     {pt}: {nb}")
