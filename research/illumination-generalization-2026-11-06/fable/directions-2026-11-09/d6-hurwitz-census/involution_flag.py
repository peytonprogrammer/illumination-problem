"""Flag DARK counterexample tuples whose cover Q is the double of a planar rectilinear polygon.

Model.  The pillowcase is two unit squares F (front) and B (back) glued along the edges
bottom (a-b), right (b-c), top (c-d) and left (d-a); a, b, c, d are the corners in ccw order
on F.  A degree-n cover has front tiles F_i and back tiles B_j.  Label back tiles so that
F_i meets B_i across the bottom edge, and let L, R, T map i to the back tile across the
left, right and top edges of F_i.  With function composition, the corner loops on front
indices are g_a = L, g_b = R^-1, g_c = T^-1 R, g_d = L^-1 T, so g_a g_b g_c g_d = 1 in the
right-action convention of hurwitz.py.  Hence for a tuple t:
    L = t0,  R = t1^-1,  T = R o t2^-1.

Reflection.  The seam reflection of the pillowcase swaps F and B and fixes the four edges.
A lift iota to Q sends F_i -> B_phi(i) and B_j -> F_phi(j).  It is well defined iff phi and
E o phi are involutions for E in {id, L, R, T}, that is phi E phi = E^-1.  The group
<L, R, T> is transitive, so phi(0) determines phi; there are at most n candidates.

Double of a polygon.  iota is orientation reversing and Q has genus 0, so Q / iota is a disk
iff iota has a fixed point (else it is RP^2).  Edge e of F_i lies on the fixed circle iff
E(i) = phi(i).  Develop Q / iota in the plane: corner a sits at lattice points (even, even),
b at (odd, even), c at (odd, odd), d at (even, odd).  Across a non-fixed edge e, F_i meets
F_phi(E(i)).  The development is consistent and injective on cells iff Q / iota has no
interior cone point and is an embedded polyomino; a shared edge between two cells that are
not glued is reported as a slit.

Run: python3 -B involution_flag.py    (reads census_nN.json and summary.json, writes involution_flag.json)
"""
import json
from pathlib import Path

from hurwitz import inv, mul, decode, plain_orbit, cycles

HERE = Path(__file__).resolve().parent
EDGES = ('bottom', 'right', 'top', 'left')


def edge_maps(t):
    n = len(t[0])
    L = t[0]
    R = inv(t[1])
    T = tuple(R[inv(t[2])[i]] for i in range(n))   # R o t2^-1
    return {'bottom': tuple(range(n)), 'right': R, 'top': T, 'left': L}


def reflections(t):
    """All phi with phi and E o phi involutions for every edge map E."""
    E = edge_maps(t)
    n = len(t[0])
    out = []
    for v in range(n):
        phi = [-1] * n
        phi[0] = v
        q = [0]
        ok = True
        for x in q:
            for e in EDGES:
                M = E[e]
                Minv = inv(M)
                y, fy = M[x], Minv[phi[x]]          # phi(M x) = M^-1 phi(x)
                if phi[y] < 0:
                    phi[y] = fy
                    q.append(y)
                elif phi[y] != fy:
                    ok = False
                    break
            if not ok:
                break
        if ok and all(phi[phi[i]] == i for i in range(n)) and all(
                E[e][phi[E[e][i]]] == phi[i] for e in EDGES for i in range(n)):
            out.append(tuple(phi))
    return out


def step(cell, e):
    x, y = cell
    if e == 'bottom':
        return (x, y - 1) if y % 2 == 0 else (x, y + 1)
    if e == 'top':
        return (x, y - 1) if y % 2 == 1 else (x, y + 1)
    if e == 'left':
        return (x - 1, y) if x % 2 == 0 else (x + 1, y)
    return (x - 1, y) if x % 2 == 1 else (x + 1, y)


def develop(t, phi):
    """Place one front tile per iota-orbit. Returns (status, cells)."""
    E = edge_maps(t)
    n = len(t[0])
    if not any(E[e][i] == phi[i] for e in EDGES for i in range(n)):
        return 'no_fixed_points_RP2', None
    pos = {0: (0, 0)}
    q = [0]
    glued = set()
    for i in q:
        for e in EDGES:
            if E[e][i] == phi[i]:
                continue
            j = phi[E[e][i]]
            c = step(pos[i], e)
            glued.add(frozenset((pos[i], c)))
            if j not in pos:
                pos[j] = c
                q.append(j)
            elif pos[j] != c:
                return 'interior_cone_point_or_overlap', None
    cells = list(pos.values())
    if len(set(cells)) != len(cells):
        return 'overlap', None
    cs = set(cells)
    slits = sum(1 for c in cs for e in EDGES if step(c, e) in cs and frozenset((c, step(c, e))) not in glued) // 2
    return ('planar_polygon' if slits == 0 else 'planar_with_slits'), sorted(cells)


def flag_tuple(t):
    res = []
    for phi in reflections(t):
        status, cells = develop(t, phi)
        a_cycles = [c for c in cycles(t[0]) if len(c) == 2]
        fixed_a = [sorted(c) for c in a_cycles if sorted(phi[x] for x in c) == sorted(c)]
        res.append(dict(phi=list(phi), status=status, n_cells=len(cells) if cells else None, cells=cells,
                        a_two_cycles_on_boundary=fixed_a))
    return res


def main():
    summary = json.loads((HERE / 'summary.json').read_text())
    out = {'sanity_room22': None, 'families': []}
    # Sanity: the 22-wall room's square tuple must develop to its own 15-square polygon.
    import validate_rooms as V
    import d4_monodromy as d4
    k = V.build_constants()
    room = d4.Room('room22', 'square', d4.squares_from_polygon(k['ROOM22']), [(0, 0), (2, 2)])
    r22 = flag_tuple(V.square_tuple(room))
    out['sanity_room22'] = [dict(status=x['status'], n_cells=x['n_cells']) for x in r22]
    print('room22', out['sanity_room22'])
    for n, fams in summary['counterexample_families'].items():
        for f in fams:
            rep = f['representative']
            t = tuple(tuple(g) for g in rep['rep'])
            orbit = plain_orbit(t)
            per = []
            for enc in sorted(orbit):
                tt, _ = decode(enc, int(n), False)
                for x in flag_tuple(tt):
                    per.append(x['status'])
            rep_flags = flag_tuple(t)
            P, Q = sorted(rep['P_sheets']), sorted(rep['Q_sheets'])
            rep_info = []
            for x in rep_flags:
                phi = x['phi']
                rep_info.append(dict(status=x['status'], cells=x['cells'],
                                     sigma_on_boundary=sorted(phi[s] for s in P) == P,
                                     tau_on_boundary=sorted(phi[s] for s in Q) == Q,
                                     iota_swaps_sigma_tau=sorted(phi[s] for s in P) == Q))
            rec = dict(n=int(n), nielsen_class_up_to_bcd=f['nielsen_class_up_to_bcd'], mechanism=f['mechanism'],
                       plain_orbit_size=len(orbit),
                       orbit_tuples_reflection_status_counts={s: per.count(s) for s in sorted(set(per))},
                       representative=rep_info)
            out['families'].append(rec)
            print(n, f['nielsen_class_up_to_bcd'], f['mechanism'][:22], 'orbit', len(orbit),
                  rec['orbit_tuples_reflection_status_counts'],
                  [(r['status'], r['sigma_on_boundary'], r['tau_on_boundary'], r['iota_swaps_sigma_tau'])
                   for r in rep_info])
    (HERE / 'involution_flag.json').write_text(json.dumps(out, indent=1) + '\n')


if __name__ == '__main__':
    main()
