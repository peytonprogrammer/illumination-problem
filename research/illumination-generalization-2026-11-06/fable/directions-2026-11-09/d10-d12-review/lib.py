"""Reviewer's own permutation, braid, and block-system code.

Written from the definitions in d6-hurwitz-census/README.md. It imports nothing from the
authors' directories. The only shared input is the saved census JSON.

Conventions (forced by the saved tuples): a permutation is a tuple p with p[i] the image
of i. mul(p, q) applies p first. A cover is t = (g_a, g_b, g_c, g_d) with
mul(g_a, g_b, g_c, g_d) = identity.
"""
import gzip
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
D6 = HERE.parent / 'd6-hurwitz-census'
D12 = HERE.parent / 'd12-lit-side'


def mul(p, q):
    return tuple([q[i] for i in p])


def inv(p):
    r = [0] * len(p)
    for i, j in enumerate(p):
        r[j] = i
    return tuple(r)


def cyc(p):
    """Cycles of p as lists, ordered by smallest element."""
    seen = [False] * len(p)
    out = []
    for i in range(len(p)):
        if not seen[i]:
            c = []
            j = i
            while not seen[j]:
                seen[j] = True
                c.append(j)
                j = p[j]
            out.append(c)
    return out


def cyc_id(p):
    """(cid, lens): cid[i] is the index of the cycle of i, lens[k] its length."""
    cid = [-1] * len(p)
    lens = []
    for k, c in enumerate(cyc(p)):
        lens.append(len(c))
        for i in c:
            cid[i] = k
    return cid, lens


def ctype(p):
    return tuple(sorted((len(c) for c in cyc(p)), reverse=True))


# ------------------------------------------------------------------ braid moves

def conj_fn(g, k):
    """The permutation x -> k(g(k^-1(x))). Its cycles are the k-images of the cycles of g."""
    r = [0] * len(g)
    for i in range(len(g)):
        r[k[i]] = k[g[i]]
    return tuple(r)


def half_move(t, a_pos, pt, i, sign):
    """s_i (sign +1): (t_i, t_i+1) -> (t_i t_i+1 t_i^-1, t_i).
    s_i^-1 (sign -1): (t_i, t_i+1) -> (t_i+1, t_i+1^-1 t_i t_i+1).
    a_pos is the position of corner a. pt labels the sheets by the a-point they lie on.
    When the loop of a is replaced by w * loop * w^-1, the cycle C of a point becomes the
    set of sheets x whose w-lift ends in C. Returns (t', a_pos', pt')."""
    t = list(t)
    x, y = t[i], t[i + 1]
    if sign > 0:
        # new t_i = x y x^-1 : apply x, then y, then x^-1.  As a function: x^-1 o y o x.
        # Its cycles are x^-1(cycles of y).  The moved loop is the one that sat at i + 1.
        xi = inv(x)
        t[i], t[i + 1] = conj_fn(y, xi), x
        if a_pos == i + 1:
            # sheet s lies in the new cycle xi(C) iff x(s) in C
            pt = tuple([pt[x[s]] for s in range(len(pt))])
            a_pos = i
        elif a_pos == i:
            a_pos = i + 1
    else:
        # new t_i+1 = y^-1 x y : function y o x o y^-1, cycles y(cycles of x).
        t[i], t[i + 1] = y, conj_fn(x, y)
        if a_pos == i:
            yi = inv(y)
            pt = tuple([pt[yi[s]] for s in range(len(pt))])
            a_pos = i + 1
        elif a_pos == i + 1:
            a_pos = i
    return tuple(t), a_pos, pt


def pure_move(t, pt, i, sign):
    """s_i^2 or s_i^-2 on a tuple with a at position 0."""
    t, ap, pt = half_move(t, 0, pt, i, sign)
    t, ap, pt = half_move(t, ap, pt, i, sign)
    assert ap == 0
    return t, pt


GENS = ((0, 1), (0, -1), (1, 1), (1, -1))


def initial_labels(ga):
    """IDs for the 2-cycles of g_a (index in cyc order among all cycles), -1 elsewhere."""
    cid, lens = cyc_id(ga)
    return tuple([c if lens[c] == 2 else -1 for c in cid])


# ------------------------------------------------------------------ conjugacy of tuples

def canon(t):
    """Canonical form of a transitive tuple under simultaneous conjugation."""
    n = len(t[0])
    g0, g1, g2 = t[0], t[1], t[2]
    best = None
    for r in range(n):
        lab = [-1] * n
        lab[r] = 0
        order = [r]
        for x in order:
            for g in (g0, g1, g2):
                y = g[x]
                if lab[y] < 0:
                    lab[y] = len(order)
                    order.append(y)
        enc = []
        for s in order:
            enc.append(lab[g0[s]])
            enc.append(lab[g1[s]])
            enc.append(lab[g2[s]])
        enc = bytes(enc)
        if best is None or enc < best:
            best = enc
    return best


def conjugators(t1, t2):
    """All c with c(t1[j][x]) = t2[j][c(x)] for every j and x (t1 transitive)."""
    n = len(t1[0])
    out = []
    for r in range(n):
        c = [-1] * n
        c[0] = r
        stack = [0]
        ok = True
        while stack and ok:
            x = stack.pop()
            cx = c[x]
            for j in range(4):
                y = t1[j][x]
                cy = t2[j][cx]
                if c[y] < 0:
                    c[y] = cy
                    stack.append(y)
                elif c[y] != cy:
                    ok = False
                    break
        if ok and len(set(c)) == n:
            out.append(tuple(c))
    return out


# ------------------------------------------------------------------ block systems

def congruence(gens, n, pairs):
    """Finest partition invariant under gens that merges the given pairs. Returns a
    tuple `where` with where[i] the block index (blocks numbered by smallest element)."""
    par = list(range(n))

    def find(u):
        while par[u] != u:
            par[u] = par[par[u]]
            u = par[u]
        return u

    stack = list(pairs)
    while stack:
        u, v = stack.pop()
        ru, rv = find(u), find(v)
        if ru != rv:
            par[ru] = rv
            for g in gens:
                stack.append((g[u], g[v]))
    roots = {}
    where = []
    for i in range(n):
        where.append(roots.setdefault(find(i), len(roots)))
    return tuple(where)


def all_block_systems(t):
    """Every G-invariant partition, the singleton system and the one-block system included.
    Every congruence is a join of the principal congruences generated by (0, i)."""
    n = len(t[0])
    princ = {congruence(t, n, [(0, i)]) for i in range(1, n)}
    systems = {tuple(range(n))} | princ
    frontier = list(princ)
    while frontier:
        w = frontier.pop()
        blk0 = [i for i in range(n) if w[i] == w[0]]
        for i in range(1, n):
            if w[i] == w[0]:
                continue
            j = congruence(t, n, [(0, x) for x in blk0] + [(0, i)])
            if j not in systems:
                systems.add(j)
                frontier.append(j)
    return sorted(systems, key=lambda w: (-max(w), w))


def induced(g, where, m):
    r = [0] * m
    for i, b in enumerate(where):
        r[b] = where[g[i]]
    return tuple(r)


# ------------------------------------------------------------------ census access

def census_orbits(n):
    d = json.loads((D6 / f'census_n{n}.json').read_text())
    for cl in d['classes']:
        for o in cl['orbits']:
            if o.get('n_two_cycles_a', 0) >= 2:
                yield cl['cts'], o


def save_out(name, obj):
    """Write one output of this directory as gzipped JSON (name without .gz)."""
    with gzip.open(HERE / (name + '.gz'), 'wt') as f:
        json.dump(obj, f, separators=(',', ':'))


def load_out(name):
    with gzip.open(HERE / (name + '.gz'), 'rt') as f:
        return json.load(f)
