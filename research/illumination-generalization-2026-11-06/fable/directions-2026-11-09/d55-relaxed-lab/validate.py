"""Validation of the d55 tools on named and random rooms.  Run: python3 -B validate.py [nrandom]

1. 22-wall room: orbitr (d55 unfolding) vs orbitc (d9, unchanged) on all interior points;
   certificates for (0,0),(2,2) vs d10 room_certs (Par at b, c, d).
2. Hand cases for slits and pinches (expected verdicts written by hand).
3. Random relaxed rooms: orbitr vs hurwitz.marked_orbit (d6, on d4.Room with slits) for every
   same-class pair, and vs the scaled-by-2 marked_orbit for a sample of different-class pairs.
"""
import random
import subprocess
import sys
import resource
from pathlib import Path

resource.setrlimit(resource.RLIMIT_AS, (900 << 20, 900 << 20)) if sys.platform != 'darwin' else None
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE / 'lib'))
import lab                                     # noqa: E402
import certs                                   # noqa: E402
import d4_monodromy as d4                      # noqa: E402

R22 = [(-1, -1), (-1, 1), (0, 1), (0, 2), (1, 2), (1, 3), (3, 3), (3, 2), (4, 2), (4, 1), (5, 1),
       (5, 0), (3, 0), (3, 1), (1, 1), (1, -1), (2, -1), (2, -3), (1, -3), (1, -2), (0, -2), (0, -1)]


def orbitr(problems, cap=1_000_000):
    inp = '\n'.join(problems) + '\n'
    out = subprocess.run([str(HERE / 'orbitr'), str(cap)], input=inp, capture_output=True, text=True,
                         check=True).stdout.strip().split('\n')
    return [lab.parse_result(l) for l in out]


def orbitc_orig(cells, sources):
    exe = HERE / 'lib' / 'orbitc_orig'
    if not exe.exists():
        subprocess.run(['cc', '-O2', '-o', str(exe), str(HERE / 'lib' / 'orbitc_orig.c')], check=True)
    line = '%d %s | %d %s\n' % (len(cells), ' '.join('%d %d' % c for c in sorted(cells)), len(sources),
                                ' '.join('%d %d' % s for s in sources))
    out = subprocess.run([str(exe), '2000000'], input=line, capture_output=True, text=True, check=True).stdout
    dark = set()
    for l in out.strip().split('\n')[1:]:
        f = l.split()
        if f[4] == 'DARK':
            dark.add(((int(f[0]), int(f[1])), (int(f[2]), int(f[3]))))
    return out.split('\n')[0], dark


def dark_set(cells, slits):
    tab = lab.sector_table(cells, slits)
    src = lab.interior_points(cells, slits, tab)
    st, nst, pairs = orbitr([lab.problem_line(cells, slits, src, tab)])[0]
    return st, nst, {(src[a], src[b]) for a, b in pairs}, src


def main():
    nrand = int(sys.argv[1]) if len(sys.argv) > 1 else 60
    ok = True
    # 1. the 22-wall room
    cells = set(d4.squares_from_polygon(R22))
    st, nst, dark, src = dark_set(cells, set())
    head, dark_c = orbitc_orig(cells, src)
    w = lab.wall_counts(cells, set(), 0)
    print('22-wall room: area', len(cells), 'W', w, 'interior pts', len(src), '| orbitr', st, nst, sorted(dark),
          '| orbitc', head, sorted(dark_c))
    ok &= (dark == dark_c == {((0, 0), (2, 2))})
    c = certs.certify_pair(cells, set(), (0, 0), (2, 2))
    print('  certificate class', c['cls'], [(d['perx'], d['degs']) for d in c['lifts']][:1])
    ok &= c['cls'] == 'full'
    hd = certs.hurwitz_dark(cells, set(), (0, 0), (2, 2))
    print('  hurwitz marked_orbit dark', hd)
    ok &= hd[0]

    # 2. hand cases
    # (a) 4 x 3 rectangle, slit (2,0)-(2,1): tip (2,1); interior points (1,1),(3,1),(1,2),(2,2),(3,2).
    cells = {(i, j) for i in range(4) for j in range(3)}
    slits = {lab.ek((2, 0), (2, 1))}
    tab = lab.sector_table(cells, slits)
    print('hand (a): tip sectors', tab[(2, 1)], 'foot sectors', tab[(2, 0)],
          'interior', lab.interior_points(cells, slits, tab), 'W', lab.wall_counts(cells, slits, 1, tab),
          'valid', lab.is_valid(cells, slits, tab))
    ok &= tab[(2, 1)][0][0] == 4 and sorted(t for t, _ in tab[(2, 0)]) == [1, 1]
    ok &= lab.wall_counts(cells, slits, 1, tab) == (7, 6, 5)
    # (b) floating slit is invalid; slit cutting the room in two is invalid
    ok &= not lab.is_valid(cells, {lab.ek((2, 1), (2, 2))})
    ok &= not lab.is_valid(cells, {lab.ek((2, 0), (2, 1)), lab.ek((2, 1), (2, 2)), lab.ek((2, 2), (2, 3))})
    # (c) pinch: ring of 8 cells around (1,1) with corner cell (0,0) removed -> pinch at (1,1)
    ring = {(i, j) for i in range(3) for j in range(3)} - {(1, 1), (0, 0)}
    tab = lab.sector_table(ring, set())
    print('hand (c): pinch sectors', tab[(1, 1)], 'valid', lab.is_valid(ring, set(), tab),
          'pinches', lab.n_pinches(ring, set(), tab), 'W', lab.wall_counts(ring, set(), 0, tab))
    ok &= lab.is_valid(ring, set(), tab) and lab.n_pinches(ring, set(), tab) == 1
    ok &= not lab.is_valid({(i, j) for i in range(3) for j in range(3)} - {(1, 1)}, set())   # hole
    # (d) slit foot at a reflex corner: L-room, slit continuing a wall: one convex + one flat sector
    L = {(i, j) for i in range(3) for j in range(3)} - {(2, 0)}
    s2 = {lab.ek((2, 1), (2, 2))}
    tab = lab.sector_table(L, s2)
    print('hand (d): reflex foot sectors', tab[(2, 1)], 'W', lab.wall_counts(L, s2, 1, tab))
    ok &= sorted(t for t, _ in tab[(2, 1)]) == [1, 2]
    # (e) tip blocks: 5 x 1 corridor of height 2 with slit from bottom (2,0)-(2,1):
    # interior points (1,1),(3,1),(4,1); the straight path (1,1)->(3,1) runs through the tip.
    cells = {(i, j) for i in range(5) for j in range(2)}
    st, nst, dark, src = dark_set(cells, {lab.ek((2, 0), (2, 1))})
    st0, nst0, dark0, src0 = dark_set(cells, set())
    print('hand (e): 5x2 with slit: interior', src, st, nst, 'dark', sorted(dark), '| without slit dark', sorted(dark0))
    # with cap 1 only the initial state (horizontal direction) is scanned: the tip must block
    # (1,1)-(3,1) and (1,1)-(4,1); (3,1)-(4,1) is joined; without the slit all three are joined.
    sl = {lab.ek((2, 0), (2, 1))}
    r1 = orbitr([lab.problem_line(cells, sl, src)], cap=1)[0]
    r0 = orbitr([lab.problem_line(cells, set(), src)], cap=1)[0]
    print('  horizontal only: with slit unreached', r1[2], '| without slit unreached', r0[2])
    ok &= sorted(r1[2]) == [(0, 1), (0, 2)] and r0[2] == []

    # 3. random relaxed rooms vs marked_orbit
    rng = random.Random(55)
    polys = [c for a, c in lab.free_polyominoes(9) if a >= 6]
    tested = mism = 0
    ndark = 0
    while tested < nrand:
        cells = set(rng.choice(polys))
        tab = lab.sector_table(cells, set())
        if not lab.is_valid(cells, set(), tab):
            continue
        cfgs = list(lab.slit_configs(cells, tab, 2, 3))
        cfg = rng.choice(cfgs)
        slits = {e for (_, _, es) in cfg for e in es}
        tab = lab.sector_table(cells, slits)
        assert lab.is_valid(cells, slits, tab)
        src = lab.interior_points(cells, slits, tab)
        if len(src) < 2:
            continue
        st, nst, pr = orbitr([lab.problem_line(cells, slits, src, tab)])[0]
        dk = {(src[a], src[b]) for a, b in pr}
        tested += 1
        same = [(p, q) for i, p in enumerate(src) for q in src[i + 1:]]
        for (p, q) in same:
            sameclass = (p[0] - q[0]) % 2 == 0 and (p[1] - q[1]) % 2 == 0
            if not sameclass and rng.random() > 0.3:
                continue
            hd, hs, hc = certs.hurwitz_dark(cells, slits, p, q)
            if st == 'CAP' and (p, q) in dk:
                continue
            if hd != ((p, q) in dk):
                mism += 1
                print('MISMATCH', lab.room_str(cells, slits), p, q, 'orbitr dark', (p, q) in dk, 'hurwitz', hd)
            ndark += hd
    print('random rooms', tested, 'mismatches', mism, 'dark pairs among checked', ndark)
    ok &= mism == 0
    print('ALL OK' if ok else 'FAILURES')


if __name__ == '__main__':
    main()
