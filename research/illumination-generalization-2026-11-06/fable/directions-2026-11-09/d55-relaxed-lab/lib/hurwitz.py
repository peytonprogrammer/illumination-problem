"""Exact Hurwitz-orbit light decider for pillowcase covers given by permutation 4-tuples.

Conventions (all exact integer arithmetic)
------------------------------------------
* A permutation is a tuple p with p[i] = image of sheet i.
* Products act on the RIGHT: mul(p, q) applies p first, then q.  This is the same
  convention as d4_monodromy.mul.  Loops are concatenated left to right, and the
  monodromy of a loop product is the product of monodromies in the same order.
* A cover is a tuple t = (t0, t1, t2, t3) of corner monodromies of a GEOMETRIC basis
  (disjoint tails from a base point, in cyclic order) with t0 t1 t2 t3 = 1.
  Corner names are carried in `labels`; corner 'a' starts at position 0.
* Cycles of t_x are the points of Q over corner x; cycle length 1, 2, 3 = cone angle
  pi, 2 pi, 3 pi (pole, regular point, simple zero).
* Points of Q over 'a' carry fixed integer IDs.  `pt[i]` is the ID of the point over
  'a' whose cycle contains sheet i in the current basis.

Hurwitz moves (Artin action on the free group, base point fixed)
-----------------------------------------------------------------
  s_i      : (t_i, t_{i+1}) -> (t_i t_{i+1} t_i^-1, t_i)
  s_i^-1   : (t_i, t_{i+1}) -> (t_{i+1}, t_{i+1}^-1 t_i t_{i+1})
The new loop around a moved puncture is w * (old loop) * w^-1 for an explicit word w.
If the old loop's point P has cycle C, the new cycle of P is C^(m(w)^-1): the sheet x
is in the new cycle iff the lift of w from x ends in C.  Writing the new monodromy as
k^-1 g k (apply k^-1, g, k), the cycle map is C -> k(C), so pt' = pt o k^-1.

Pure mapping classes of the 4-punctured sphere are generated (up to the simultaneous
conjugation that the sphere relation and the full twist induce) by s_0^2 and s_1^2;
s_2^2 is the same mapping class as s_0^2 on the sphere and is used only as a check.

Arcs
----
In a geometric basis, the tails to 'a' (position 0) and to the corner x at position j
form a simple arc a -> x.  The lift through sheet i joins the 'a'-point pt[i] and the
x-point = cycle of t_j containing i.  Every isotopy class of simple arcs from 'a' to
another corner is the tail arc of some basis in the pure-braid orbit (PMod(S_{0,4})
= level-2 group acts transitively on each of the three slope parity classes).

Light rule
----------
A straight path may pass through a vertex only if it is a 2-cycle.  The marked 2-cycle
points sigma, tau over 'a' are connected along an arc iff they lie in one component of
the subgraph induced on the 2-cycle vertices (that component is a path or a cycle).
LIT iff connected for some basis in the orbit and some of the three arcs.
"""
from collections import deque


# ---------------------------------------------------------------- permutations

def mul(p, q):
    return tuple(q[i] for i in p)


def inv(p):
    r = [0] * len(p)
    for i, j in enumerate(p):
        r[j] = i
    return tuple(r)


def ident(n):
    return tuple(range(n))


def cycles(p):
    seen = [False] * len(p)
    out = []
    for i in range(len(p)):
        if seen[i]:
            continue
        c, j = [], i
        while not seen[j]:
            seen[j] = True
            c.append(j)
            j = p[j]
        out.append(c)
    return out


def cycle_type(p):
    return sorted((len(c) for c in cycles(p)), reverse=True)


def cycle_index(p):
    """cid[i] = index of the cycle containing i; also the list of cycle lengths."""
    cid = [-1] * len(p)
    lens = []
    for k, c in enumerate(cycles(p)):
        for x in c:
            cid[x] = k
        lens.append(len(c))
    return cid, lens


def conj_by(g, k):
    """k^-1 g k with right-action products, i.e. the permutation k o g o k^-1."""
    r = [0] * len(g)
    for i in range(len(g)):
        r[k[i]] = k[g[i]]
    return tuple(r)


def index_of(p):
    return len(p) - len(cycles(p))


def is_transitive(gens, n):
    seen = {0}
    q = [0]
    for x in q:
        for g in gens:
            y = g[x]
            if y not in seen:
                seen.add(y)
                q.append(y)
    return len(seen) == n


# ---------------------------------------------------------------- Hurwitz moves

def move(t, labels, pt, i, sign):
    """Apply s_i (sign=+1) or s_i^-1 (sign=-1). Returns (t', labels', pt')."""
    t = list(t)
    labels = list(labels)
    a, b = t[i], t[i + 1]
    if sign > 0:
        k = inv(a)                      # new_i = k^-1 b k = a b a^-1
        t[i], t[i + 1] = conj_by(b, k), a
        moved = labels[i + 1]           # puncture moving from i+1 to i gets conjugated
        labels[i], labels[i + 1] = labels[i + 1], labels[i]
    else:
        k = b                           # new_{i+1} = k^-1 a k = b^-1 a b
        t[i], t[i + 1] = b, conj_by(a, k)
        moved = labels[i]
        labels[i], labels[i + 1] = labels[i + 1], labels[i]
    if moved == 'a' and pt is not None:
        kinv = inv(k)
        pt = tuple(pt[kinv[x]] for x in range(len(pt)))   # pt' = pt o k^-1
    return tuple(t), tuple(labels), pt


def pure_move(t, labels, pt, i, sign):
    """s_i^2 or s_i^-2."""
    t, labels, pt = move(t, labels, pt, i, sign)
    return move(t, labels, pt, i, sign)


PURE_GENS = [(0, 1), (0, -1), (1, 1), (1, -1)]
PURE_GENS_WITH_S2 = PURE_GENS + [(2, 1), (2, -1)]


# ---------------------------------------------------------------- canonical forms

def _relabel(t, root):
    """BFS labelling from root using t0, t1, t2 (t3 = (t0 t1 t2)^-1 is implied)."""
    n = len(t[0])
    lab = [-1] * n
    order = [root]
    lab[root] = 0
    for x in order:
        for g in t[:3]:
            y = g[x]
            if lab[y] < 0:
                lab[y] = len(order)
                order.append(y)
    if len(order) != n:
        return None, None
    return lab, order


def _encode(t, lab, order, pt):
    enc = []
    for s in order:
        enc.append(lab[t[0][s]])
        enc.append(lab[t[1][s]])
        enc.append(lab[t[2][s]])
        if pt is not None:
            enc.append(pt[s])
    return tuple(enc)


def canon_plain(t, want_map=False):
    """Canonical form of a transitive tuple under simultaneous conjugation."""
    best, best_lab = None, None
    for r in range(len(t[0])):
        lab, order = _relabel(t, r)
        e = _encode(t, lab, order, None)
        if best is None or e < best:
            best, best_lab = e, [lab]
        elif e == best:
            best_lab.append(lab)
    return (best, best_lab) if want_map else best


def canon_marked(t, pt, roots):
    """Canonical form of (tuple, point IDs over 'a'); roots = the sheets of point ID 0."""
    best = None
    for r in roots:
        lab, order = _relabel(t, r)
        e = _encode(t, lab, order, pt)
        if best is None or e < best:
            best = e
    return best


def decode(enc, n, marked):
    w = 4 if marked else 3
    t0 = tuple(enc[w * i] for i in range(n))
    t1 = tuple(enc[w * i + 1] for i in range(n))
    t2 = tuple(enc[w * i + 2] for i in range(n))
    t3 = inv(mul(mul(t0, t1), t2))
    pt = tuple(enc[w * i + 3] for i in range(n)) if marked else None
    return (t0, t1, t2, t3), pt


# ---------------------------------------------------------------- light

def arc_components(ta, pt, plen, tx):
    """For the tail arc a -> x: connected pairs of 2-cycle 'a'-points in the subgraph
    induced on 2-cycle vertices. Returns a list of frozensets of point IDs (size >= 2)."""
    cid, lens = cycle_index(tx)
    parent = {}

    def find(u):
        while parent.setdefault(u, u) != u:
            parent[u] = parent[parent[u]]
            u = parent[u]
        return u

    for i in range(len(ta)):
        P = pt[i]
        if P < 0 or plen[P] != 2:
            continue
        find(('a', P))
        if lens[cid[i]] == 2:
            ru, rv = find(('a', P)), find(('x', cid[i]))
            if ru != rv:
                parent[ru] = rv
    comp = {}
    for u in list(parent):
        if u[0] == 'a':
            comp.setdefault(find(u), set()).add(u[1])
    return [frozenset(c) for c in comp.values() if len(c) > 1]


def initial_pt(ta):
    """Point IDs over 'a' = index of the cycle of ta (in cycles() order)."""
    cid, lens = cycle_index(ta)
    return tuple(cid), lens


def marked_orbit(t, gens=PURE_GENS, max_states=None, want_witness=False, targets=None):
    """BFS over the pure-braid orbit of (t, every 2-cycle point over 'a' labelled).

    Points over 'a' of cone angle pi or 3 pi all carry the common label -1: they stop
    light and are never marks, so distinguishing them would only enlarge the orbit.

    Returns dict with: states (orbit size), plain tuple canonical forms seen,
    lit (set of frozenset({P, Q}) of 2-cycle point IDs connected along some arc),
    witness[pair] = (word, arc position) if want_witness.
    If `targets` (a set of frozenset pairs) is given, stop as soon as one of them is lit
    (complete=False, stopped_lit=True).
    """
    labels = ('a', 'b', 'c', 'd')
    cid, plen = initial_pt(t[0])
    pt = tuple(c if plen[c] == 2 else -1 for c in cid)
    n = len(t[0])
    root_id = min((c for c in cid if plen[c] == 2), default=-1)

    def roots_of(pt_):
        return [i for i in range(n) if pt_[i] == root_id]

    start = canon_marked(t, pt, roots_of(pt))
    seen = {start: None}
    queue = deque([(t, pt, ())])
    lit = set()
    witness = {}
    while queue:
        t_, pt_, word = queue.popleft()
        for j in (1, 2, 3):
            for comp in arc_components(t_[0], pt_, plen, t_[j]):
                cl = sorted(comp)
                for x in range(len(cl)):
                    for y in range(x + 1, len(cl)):
                        pr = frozenset((cl[x], cl[y]))
                        if pr not in lit:
                            lit.add(pr)
                            if want_witness:
                                witness[pr] = (word, labels[j])
                            if targets and pr in targets:
                                return dict(states=len(seen), complete=False, stopped_lit=True, lit=lit,
                                            witness=witness, plen=plen)
        for (i, s) in gens:
            t2, lab2, pt2 = pure_move(t_, labels, pt_, i, s)
            assert lab2 == labels
            c = canon_marked(t2, pt2, roots_of(pt2))
            if c not in seen:
                seen[c] = True
                if max_states and len(seen) > max_states:
                    return dict(states=len(seen), complete=False, lit=lit, witness=witness, plen=plen)
                queue.append((t2, pt2, word + ((i, s),)))
    return dict(states=len(seen), complete=True, lit=lit, witness=witness, plen=plen, seen=seen)


def plain_orbit(t, gens=PURE_GENS):
    """Pure-braid orbit of the unmarked tuple, as a set of canonical forms."""
    labels = ('a', 'b', 'c', 'd')
    start = canon_plain(t)
    seen = {start}
    queue = deque([t])
    while queue:
        t_ = queue.popleft()
        for (i, s) in gens:
            t2, _, _ = pure_move(t_, labels, None, i, s)
            c = canon_plain(t2)
            if c not in seen:
                seen.add(c)
                queue.append(t2)
    return seen
