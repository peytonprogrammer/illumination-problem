"""d48 referee check of d47 Lemma 3.2 on named rooms only (22-wall room, 12-wall cross). No search.

Model: refine each room R by 3 (cells of side 1/3), so Q = DR is a cover of the unit pillowcase B3 of
3R with 9n sheets.  In 3R coordinates (origin at 3S, a lattice point of R):
  L = 3Z^2              <-> Lambda' = Z^2 (R's own base B_R)
  L = {x = y mod 3}     <-> Lambda  = Z^2 + Z(1/3, 1/3)
  L = {x = -y mod 3}    <-> Lambda  = Z^2 + Z(1/3, -1/3)
The factor P_L of Q -> B3 is the block system "sheet square mod <2L, -1>": a front face of tile (i, j)
sits at square (i, j), a back face at (i, -j-1) (chart p -> (x, -y)).

For each base L: canonical Par partition B^L_x (merge the 2-cycles of g_x lying in the corner block of
P_L over x) and canonical Rig partition R^L_y (merge all cycles of g_y in the corner block over y).
Reports separation of the four lift pairs, and checks the Lemma 3.2 mechanism: N' = N meet P_{3Z^2}
satisfies Par over B_R whenever N satisfies Par over P_Lambda.
Also shows where the back lifts of a sheared rational mark land (d47 Definition 1.2 "equivalently").
"""
import sys
import resource
import time
from pathlib import Path
resource.setrlimit(resource.RLIMIT_CPU, (120, 120))
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'd10-mechanisms'))
from roomtools import *  # noqa

LAT = {'3Z^2 (B_R)': [(0, 0)],
       'Z^2+Z(1/3,1/3)': [(0, 0), (2, 2), (4, 4)],
       'Z^2+Z(1/3,-1/3)': [(0, 0), (2, 4), (4, 2)]}


def scale(cells, k):
    return {(k * i + u, k * j + v) for (i, j) in cells for u in range(k) for v in range(k)}


def positions(room):
    out = []
    for f in room.sheets:
        k, c = room.faces[f]
        i, j = room.tiles[k]['key']
        out.append((i, j) if c == 0 else (i, -j - 1))
    return out


def lattice_partition(pos, t2l):
    def key(q):
        c = []
        for u in t2l:
            c.append(((q[0] + u[0]) % 6, (q[1] + u[1]) % 6))
            c.append(((-q[0] - 1 + u[0]) % 6, (-q[1] - 1 + u[1]) % 6))
        return min(c)
    blocks = {}
    for s, q in enumerate(pos):
        blocks.setdefault(key(q), []).append(s)
    return sorted(blocks.values())


def is_block(part, t):
    where = {s: b for b, blk in enumerate(part) for s in blk}
    return all(len({where[g[s]] for s in blk}) == 1 for g in t for blk in part)


def meet(p1, p2):
    w2 = {s: b for b, blk in enumerate(p2) for s in blk}
    out = {}
    for b, blk in enumerate(p1):
        for s in blk:
            out.setdefault((b, w2[s]), []).append(s)
    return sorted(out.values())


def corner_block(t, PL, x):
    ind = induced(t[x], PL)
    fx = [b for b in range(len(PL)) if ind[b] == b]
    assert len(fx) == 1, fx          # odd index: one corner of P_L over each corner of B3
    return set(PL[fx[0]])


def par_partition(t, PL, x):
    X0 = corner_block(t, PL, x)
    seeds = [tuple(c) for c in cycles(t[x]) if len(c) == 2 and set(c) <= X0]
    return closure_partition(len(t[0]), t, seeds), X0


def rig_partition(t, PL, y):
    Y0 = corner_block(t, PL, y)
    seeds = [(c[0], s) for c in cycles(t[y]) if set(c) <= Y0 for s in c[1:]]
    return closure_partition(len(t[0]), t, seeds), Y0


def no_regular_over(t, N, x, X0):
    ind = induced(t[x], N)
    inX0 = [b for b, blk in enumerate(N) if set(blk) <= X0]
    assert all(set(blk) <= X0 or not (set(blk) & X0) for blk in N)
    return all(not (ind[b] != b and ind[ind[b]] == b) for b in inX0)


def sep(t, N, LS, LT):
    return [a_image(t, N, s[0])[0] != a_image(t, N, u[0])[0] for s in LS for u in LT]


def report(label, cells, S, T):
    t0 = time.process_time()
    c3 = scale(cells, 3)
    o3 = (3 * S[0], 3 * S[1])
    room, t = room_tuple(c3, o3)
    n = len(t[0])
    pos = positions(room)
    rel = (3 * (T[0] - S[0]), 3 * (T[1] - S[1]))
    LS, LT = lifts(room, t, (0, 0), (0, 0)), lifts(room, t, rel, (0, 0))
    print('==', label, 'sheets of DR over B3:', n, '(= 9 n_R)')
    parts = {}
    for name, t2l in LAT.items():
        PL = lattice_partition(pos, t2l)
        assert is_block(PL, t), name
        parts[name] = PL
        A0 = corner_block(t, PL, 0)
        on = all(set(l) <= A0 for l in LS + LT)
        print('  base %-16s blocks %d (deg P_L->B3), all four mark lifts over the a-corner: %s'
              % (name, len(PL), on))
    PB = parts['3Z^2 (B_R)']
    assert all(any(set(b) <= set(c) for c in parts['Z^2+Z(1/3,1/3)']) for b in PB)
    for name, PL in parts.items():
        for xn, x in (('b', 1), ('c', 2), ('d', 3)):
            Bx, X0 = par_partition(t, PL, x)
            ok = no_regular_over(t, Bx, x, X0)
            s = sep(t, Bx, LS, LT)
            line = '  %-16s Par(%s): N blocks %3d, no regular over x: %s, separates %s' % (
                name, xn, len(Bx), ok, s)
            if name != '3Z^2 (B_R)':
                Np = meet(Bx, PB)
                BxB, XB = par_partition(t, PB, x)
                okp = no_regular_over(t, Np, x, XB)
                sp = sep(t, Np, LS, LT)
                coarser = all(any(set(b) <= set(c) for c in Np) for b in BxB)
                line += " | N' = N meet B_R: no regular over x: %s, separates %s, N' coarser than B^R_x: %s" % (
                    okp, sp, coarser)
                assert okp and coarser and all(a <= b for a, b in zip(s, sp))
            print(line)
        for yn, y in (('b', 1), ('c', 2), ('d', 3)):
            Ry, _ = rig_partition(t, PL, y)
            print('  %-16s R_%s: N blocks %3d, phi(sigma) != phi(tau) per lift pair %s'
                  % (name, yn, len(Ry), sep(t, Ry, LS, LT)))
    print('  CPU', round(time.process_time() - t0, 3))
    return room, t, parts


def back_lift_demo(cells, v0):
    """Sheared rational mark S' = v0 + (1/3, 1/3) (3R coords: offset (1,1) from vertex 3 v0)."""
    c3 = scale(cells, 3)
    o3 = (3 * v0[0], 3 * v0[1])
    room, t = room_tuple(c3, o3)
    pos = positions(room)
    print('== back-lift demo, vertex v0 =', v0, 'status of v0:', status(cells, v0))
    for name, t2l in LAT.items():
        PL = lattice_partition(pos, t2l)
        for q in ((1, 1), (2, 2)):
            cls, pts = room.points_at(q)
            xi = OFFS[cls]
            X0 = corner_block(t, PL, xi)
            desc = []
            for cy in pts:
                copies = {room.faces[room.sheets[s]][1] for s in cy}
                desc.append(('front' if copies == {0} else 'back' if copies == {1} else 'mixed',
                             set(cy) <= X0))
            print('  base %-16s point v0+%s/3 (class %s): lifts (face, over a corner of P_L) %s'
                  % (name, q, 'abcd'[xi], desc))


R22 = [(-1, -1), (-1, 1), (0, 1), (0, 2), (1, 2), (1, 3), (3, 3), (3, 2), (4, 2), (4, 1), (5, 1),
       (5, 0), (3, 0), (3, 1), (1, 1), (1, -1), (2, -1), (2, -3), (1, -3), (1, -2), (0, -2), (0, -1)]
C22 = cells_from_vertices(R22)
report('22-wall room, S=(0,0), T=(2,2)', C22, (0, 0), (2, 2))
CROSS = {(i, j) for i in range(4) for j in range(1, 3)} | {(i, j) for i in range(1, 3) for j in range(4)}
report('12-wall cross, S=(1,2), T=(3,2)', CROSS, (1, 2), (3, 2))
assert (-1, -1) in C22
back_lift_demo(C22, (-1, -1))
