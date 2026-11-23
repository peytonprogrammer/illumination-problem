"""d59 second test: point monodromy group M_t and cusp group N on NAMED rooms only.

Uses the d14 definitions (cusp.py) and the d10 room-to-tuple map.  For each named room and
class origin it reports: n, primitivity of G, |G| (Schreier-Sims or Jordan), q, and the
orbits of M (all Schreier generators + deck maps) and of N (cusp loops) on regular a-points
and on unordered pairs.  No room, ray, direction or word search; the pure-braid orbit of
the one tuple is walked as in d14.
Run: python3 -B mt_named.py
"""
import sys, json, time
from collections import deque
from pathlib import Path
HERE = Path(__file__).resolve().parent
D = HERE.parent
for sub in ('d6-hurwitz-census', 'd10-mechanisms', 'd14-lemma-h'):
    sys.path.insert(0, str(D / sub))
from roomtools import room_tuple, cells_from_vertices  # noqa: E402
from hurwitz import pure_move, canon_plain, initial_pt, PURE_GENS  # noqa: E402
from cusp import twist, LABELS  # noqa: E402
import d4_monodromy as d4  # noqa: E402
from axis_twist import load  # noqa: E402


def orbits(gens, q):
    """Orbits on points and on unordered pairs, by generator BFS."""
    def bfs(start, act):
        seen = {start}
        st = [start]
        while st:
            x = st.pop()
            for g in gens:
                y = act(g, x)
                if y not in seen:
                    seen.add(y)
                    st.append(y)
        return seen
    pts, todo = [], set(range(q))
    while todo:
        o = bfs(min(todo), lambda g, i: g[i])
        pts.append(sorted(o)); todo -= o
    prs, todo = [], {(i, j) for i in range(q) for j in range(i + 1, q)}
    while todo:
        o = bfs(min(todo), lambda g, p: tuple(sorted((g[p[0]], g[p[1]]))))
        prs.append(len(o)); todo -= o
    return [len(p) for p in pts], sorted(prs)


def analyse(name, cells, origin, max_states=200000):
    t0c = time.process_time()
    room, t0 = room_tuple(cells, origin)
    n = len(t0[0])
    blocks = d4.min_block_partition if hasattr(d4, 'min_block_partition') else None
    # primitivity: for every pair (0, j) the finest invariant partition joining them is trivial
    prim = True
    for j in range(1, n):
        part = d4.min_block_partition([0, j], list(t0), n)
        if len(part) > 1:
            prim = False
            break
    cid, plen = initial_pt(t0[0])
    pt0 = tuple(c if plen[c] == 2 else -1 for c in cid)
    ids = sorted({p for p in pt0 if p >= 0})
    idx = {p: k for k, p in enumerate(ids)}
    q = len(ids)

    def canon_pt(t, pt):
        pc, labs = canon_plain(t, want_map=True)
        out = []
        for lab in labs:
            arr = [0] * n
            for s in range(n):
                arr[lab[s]] = pt[s]
            out.append(arr)
        return pc, out

    def perms(ref, arrs):
        res = []
        for arr in arrs:
            pi = [None] * q
            for c in range(n):
                u, v = ref[c], arr[c]
                if u >= 0:
                    pi[idx[u]] = idx[v]
            res.append(tuple(pi))
        return res

    pc0, arrs0 = canon_pt(t0, pt0)
    ref = {pc0: arrs0[0]}
    states = {pc0: (t0, pt0)}
    queue = deque([pc0])
    gensM = set(perms(arrs0[0], arrs0))
    while queue:
        pc = queue.popleft()
        t, pt = states[pc]
        for (i, s) in PURE_GENS:
            t2, _, pt2 = pure_move(t, LABELS, pt, i, s)
            pc2, arrs2 = canon_pt(t2, pt2)
            if pc2 not in ref:
                ref[pc2] = arrs2[0]
                states[pc2] = (t2, pt2)
                queue.append(pc2)
                if len(ref) > max_states:
                    print(json.dumps(dict(room=name, origin=origin, n=n, aborted='orbit too big')))
                    return None
            gensM.update(perms(ref[pc2], arrs2))
    gensN = set()
    for x in (1, 2, 3):
        done = set()
        for pc in ref:
            if pc in done:
                continue
            cyc, (t, pt), cur = [], states[pc], pc
            while True:
                cyc.append(cur); done.add(cur)
                t, pt = twist(t, pt, x)
                cur, arrs = canon_pt(t, pt)
                if cur == pc:
                    break
            w = len(cyc)
            for u in cyc:
                t, pt = states[u]
                for _ in range(w):
                    t, pt = twist(t, pt, x)
                cu, arrs = canon_pt(t, pt)
                gensN.update(perms(ref[u], arrs))
    e = tuple(range(q))
    gM = [g for g in gensM if g != e]
    gN = [g for g in gensN if g != e]
    rec = dict(room=name, origin=origin, n=n, G_primitive=prim, q=q, plain_orbit=len(ref),
               M_point_orbits=orbits(gM, q)[0] if q else [], M_pair_orbits=orbits(gM, q)[1] if q else [],
               N_point_orbits=orbits(gN, q)[0] if q else [], N_pair_orbits=orbits(gN, q)[1] if q else [],
               N_trivial=not gN, cpu=round(time.process_time() - t0c, 2))
    print(json.dumps(rec))
    return rec


if __name__ == '__main__':
    R22 = [(-1, -1), (-1, 1), (0, 1), (0, 2), (1, 2), (1, 3), (3, 3), (3, 2), (4, 2), (4, 1),
           (5, 1), (5, 0), (3, 0), (3, 1), (1, 1), (1, -1), (2, -1), (2, -3), (1, -3), (1, -2),
           (0, -2), (0, -1)]
    rooms = D / 'd41-two-param-cover' / 'rooms'
    out = []
    for name, cells, org in [('R22', cells_from_vertices(R22), (0, 0)),
                             ('r20a', load(rooms / 'r20a.txt'), (1, 3)),
                             ('cross12', load(rooms / 'cross12.txt'), (1, 0)),
                             ('cross12', load(rooms / 'cross12.txt'), (0, 0)),
                             ('dumb12', load(rooms / 'dumb12.txt'), (0, 0)),
                             ('dumb12', load(rooms / 'dumb12.txt'), (1, 0))]:
        out.append(analyse(name, cells, org))
    json.dump(out, open(HERE / 'mt_named.json', 'w'), indent=1)
