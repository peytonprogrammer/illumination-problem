"""Exhaustive enumeration, up to simultaneous conjugation, of transitive genus-0 tuples
(g_a, g_b, g_c, g_d) in S_n with g_a g_b g_c g_d = 1 (right-action products, as in
hurwitz.py) and every cycle length <= 3.

Method (exact, no sampling).
  A    = all permutations of {0..n-1} with cycle lengths <= 3.
  g_a  = one fixed representative of each cycle type.
  g_b  = one representative of each orbit of the centraliser C(g_a) acting on A by
         conjugation (orbits computed by BFS with generators of C(g_a)).
  (g_c, g_d): g_c g_d = (g_a g_b)^-1.  For every cycle type K a fixed representative
         rho_K is factorised once: F_K = {(c, d) in A x A : c d = rho_K^-1}, bucketed by
         ind(c) + ind(d).  If g_a g_b = s^-1 rho_K s then the completions are the
         s-conjugates of F_K.  Riemann-Hurwitz genus 0 means the index sum is 2n - 2, so
         only one bucket is used.
  Every tuple of the census is conjugate to one with g_a = rep and g_b = orbit rep, so
  this list is complete; duplicates are removed with the canonical form canon_plain.
  Transitivity is checked explicitly.

Run: python3 -B enumerate_tuples.py N   -> writes tuples_nN.json
"""
import json
import sys
import time
from pathlib import Path

from hurwitz import mul, inv, cycles, conj_by, is_transitive, canon_plain, decode

HERE = Path(__file__).resolve().parent


def allowed_perms(n):
    """All permutations with cycle lengths <= 3."""
    out = []
    p = [-1] * n

    def rec():
        try:
            i = p.index(-1)
        except ValueError:
            out.append(tuple(p))
            return
        p[i] = i
        rec()
        free = [j for j in range(i + 1, n) if p[j] == -1]
        for j in free:
            p[i], p[j] = j, i
            rec()
            p[j] = -1
            for k in free:
                if k != j:
                    p[i], p[j], p[k] = j, k, i
                    rec()
                    p[k] = -1
            p[j] = -1
        p[i] = -1

    rec()
    return out


def partitions(n, maxpart=None):
    if maxpart is None:
        maxpart = n
    if n == 0:
        yield ()
        return
    for k in range(min(n, maxpart), 0, -1):
        for rest in partitions(n - k, k):
            yield (k,) + rest


def standard_perm(ctype):
    p, x = [], 0
    n = sum(ctype)
    p = list(range(n))
    for L in ctype:
        for j in range(L):
            p[x + j] = x + (j + 1) % L
        x += L
    return tuple(p)


def ctype(p):
    return tuple(sorted((len(c) for c in cycles(p)), reverse=True))


def ind(p):
    return len(p) - len(cycles(p))


def centraliser_gens(g):
    n = len(g)
    cyc = cycles(g)
    by_len = {}
    for c in cyc:
        by_len.setdefault(len(c), []).append(c)
    gens = []
    for L, cs in by_len.items():
        if L > 1:                       # rotate the first cycle of this length
            p = list(range(n))
            c = cs[0]
            for j in range(L):
                p[c[j]] = c[(j + 1) % L]
            gens.append(tuple(p))
        if len(cs) > 1:                 # swap cycles 0,1 and shift all cycles of this length
            p = list(range(n))
            for j in range(L):
                p[cs[0][j]], p[cs[1][j]] = cs[1][j], cs[0][j]
            gens.append(tuple(p))
            p = list(range(n))
            m = len(cs)
            for k in range(m):
                for j in range(L):
                    p[cs[k][j]] = cs[(k + 1) % m][j]
            gens.append(tuple(p))
    return gens


def conjugator(src, dst):
    """s with conj_by(src, s) == dst (s o src o s^-1 = dst); src, dst of equal cycle type."""
    n = len(src)
    cs = sorted(cycles(src), key=len)
    cd = sorted(cycles(dst), key=len)
    s = [0] * n
    for a, b in zip(cs, cd):
        assert len(a) == len(b)
        for x, y in zip(a, b):
            s[x] = y
    s = tuple(s)
    assert conj_by(src, s) == dst
    return s


class ClassEnumerator:
    """Per-process caches for enumerating one Nielsen class (ct_a, ct_b, ct_c, ct_d) at a time."""

    def __init__(self, n):
        self.n = n
        self.by_type = {}
        for p in allowed_perms(n):
            self.by_type.setdefault(ctype(p), []).append(p)
        self.breps = {}
        self.ftab = {}

    def b_reps(self, ta, tb):
        key = (ta, tb)
        if key not in self.breps:
            cg = centraliser_gens(standard_perm(ta))
            seen, reps = set(), []
            for b in self.by_type[tb]:
                if b in seen:
                    continue
                reps.append(b)
                seen.add(b)
                q = [b]
                for x in q:
                    for g in cg:
                        y = conj_by(x, g)
                        if y not in seen:
                            seen.add(y)
                            q.append(y)
            self.breps[key] = reps
        return self.breps[key]

    def factors(self, K, tc, td):
        key = (K, tc, td)
        if key not in self.ftab:
            rho_inv = inv(standard_perm(K))
            out = []
            for c in self.by_type[tc]:
                d = mul(inv(c), rho_inv)            # c d = rho_K^-1
                if ctype(d) == td:
                    out.append((c, d))
            self.ftab[key] = out
        return self.ftab[key]

    def enumerate_class(self, cts):
        """All transitive tuples with cycle types cts = (ta, tb, tc, td), product 1, as a dict
        canon_plain -> tuple.  Genus is fixed by the cycle types."""
        n = self.n
        ta, tb, tc, td = cts
        ga = standard_perm(ta)
        found = {}
        for gb in self.b_reps(ta, tb):
            pi = mul(ga, gb)
            K = ctype(pi)
            fl = self.factors(K, tc, td)
            if not fl:
                continue
            s = conjugator(standard_perm(K), pi)
            for c0, d0 in fl:
                t = (ga, gb, conj_by(c0, s), conj_by(d0, s))
                if is_transitive(t, n):
                    key = canon_plain(t)
                    if key not in found:
                        found[key] = t
        return found


def genus0_classes(n):
    """Ordered 4-tuples of cycle types (parts <= 3) with index sum 2n - 2."""
    types = list(partitions(n, 3))
    iv = {t: n - len(t) for t in types}
    out = []
    for ta in types:
        for tb in types:
            for tc in types:
                for td in types:
                    if iv[ta] + iv[tb] + iv[tc] + iv[td] == 2 * n - 2:
                        out.append((ta, tb, tc, td))
    return out


def enumerate_n_by_class(n):
    E = ClassEnumerator(n)
    out = []
    for cts in genus0_classes(n):
        out.extend(E.enumerate_class(cts).values())
    return out


def enumerate_n(n, log=print):
    t0 = time.time()
    A = allowed_perms(n)
    Aset = set(A)
    target = 2 * n - 2
    ind_of = {p: ind(p) for p in A}
    log('n=%d |A|=%d (%.1fs)' % (n, len(A), time.time() - t0))
    # factorisation tables, built lazily per cycle type of the product
    Ftab = {}

    def factors(K, budget):
        if K not in Ftab:
            rho_inv = inv(standard_perm(K))
            buckets = {}
            for c in A:
                d = mul(inv(c), rho_inv)            # c d = rho^-1
                if d in Aset:
                    s = ind_of[c] + ind_of[d]
                    if s <= target:
                        buckets.setdefault(s, []).append((c, d))
            Ftab[K] = buckets
        return Ftab[K].get(budget, [])

    found = {}
    stats = dict(pairs=0, candidates=0, transitive=0)
    for ta in partitions(n, 3):
        ga = standard_perm(ta)
        ia = ind(ga)
        cg = centraliser_gens(ga)
        seen = set()
        reps = []
        for b in A:
            if b in seen or ia + ind_of[b] > target:
                continue
            reps.append(b)
            seen.add(b)
            q = [b]
            for x in q:
                for g in cg:
                    y = conj_by(x, g)
                    if y not in seen:
                        seen.add(y)
                        q.append(y)
        for gb in reps:
            stats['pairs'] += 1
            budget = target - ia - ind_of[gb]
            pi = mul(ga, gb)
            K = ctype(pi)
            rho = standard_perm(K)
            fl = factors(K, budget)
            if not fl:
                continue
            s = conjugator(rho, pi)            # pi = s o rho o s^-1 ; pi^-1 likewise
            for c0, d0 in fl:
                stats['candidates'] += 1
                gc, gd = conj_by(c0, s), conj_by(d0, s)
                t = (ga, gb, gc, gd)
                if not is_transitive(t, n):
                    continue
                stats['transitive'] += 1
                key = canon_plain(t)
                if key not in found:
                    found[key] = t
        log('  g_a %s: %d g_b reps, total tuples so far %d (%.1fs)' % (ta, len(reps), len(found), time.time() - t0))
    out = []
    for key, t in found.items():
        t2, _ = decode(key, n, False)
        assert mul(mul(mul(t2[0], t2[1]), t2[2]), t2[3]) == tuple(range(n))
        assert all(max(len(c) for c in cycles(g)) <= 3 for g in t2)
        assert sum(ind(g) for g in t2) == target
        out.append(t2)
    out.sort(key=lambda t: ([ctype(g) for g in t], t))
    stats['tuples'] = len(out)
    stats['seconds'] = round(time.time() - t0, 1)
    return out, stats


def main():
    n = int(sys.argv[1])
    tuples, stats = enumerate_n(n)
    print(stats)
    (HERE / ('tuples_n%d.json' % n)).write_text(json.dumps(dict(n=n, stats=stats, tuples=[list(map(list, t)) for t in tuples])) + '\n')


if __name__ == '__main__':
    main()
