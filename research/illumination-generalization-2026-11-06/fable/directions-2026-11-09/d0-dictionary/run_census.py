"""Test dictionary D0 on every strictly simple polyomino of area <= NMAX.

Usage: python3 -B run_census.py NMAX [WORKERS] [fixed|free|interior] [NMIN] [PYCAP] [CHECKCAP]

  fixed     every fixed polyomino (translation class)
  free      one polyomino per class under the 8 symmetries of the square
  interior  every fixed polyomino that has two interior lattice points of one class
  NMIN      smallest area (default 1)
  PYCAP     run the Python room decider R only when C reports at most PYCAP states
  CHECKCAP  run the state-level check S on the first CHECKCAP states of each orbit

For every room and every parity class with at least two regular points of DP:
  T  tuple side: marked pure-braid orbit of (g_a, g_b, g_c, g_d)   (d0lib.tuple_orbit)
  R  room side:  SL(2,Z) orbit of the decorated 4-fold unfolding    (d0lib.room_orbit)
  C  room side:  d8's orbit.c, compiled here as ./orbit_d8, fed with d0lib's unfolding
  S  state level: in every state and for each of the three arcs, the chain components
     must equal the straight-segment components at the slope M e_j (d0lib.state_check)
  W  witnesses: every tuple-LIT interior pair is turned into a room vector through the
     slope M e_j and replayed by d8's reflection tracer (no unfolding); every room-lit
     interior pair's witness vector is replayed the same way.

Writes census_nNMAX_MODE.json (summary, every interior pair, every disagreement).
"""
import json
import subprocess
import sys
import time
from collections import Counter
from multiprocessing import Pool

sys.dont_write_bytecode = True
import d0lib as L                                   # noqa: E402

sys.path.insert(0, str(L.HERE.parent / 'd8-perturbation-test'))
import tracer as d8tracer                            # noqa: E402

EPS = (1, -1)
MAX_NORM = 400
PYCAP = 60000
CHECKCAP = None
C_CAP = 30000000
ORIGINS = ((0, 0), (1, 0), (1, 1), (0, 1))


def d8_lit(cells, U, srcs):
    N = len(U.sq)
    lab = []
    for k in range(N):
        p = U.ll[k]
        lab.append(srcs.index(p) if U.st[p] in ('interior', 'flat') else -1)
    inp = f"{N} {len(srcs)} {C_CAP} 0\n0\n" + " ".join(map(str, U.h)) + "\n" + \
        " ".join(map(str, U.v)) + "\n" + " ".join(map(str, lab)) + "\n"
    out = subprocess.run([str(L.HERE / 'orbit_d8')], input=inp, capture_output=True, text=True)
    assert out.returncode == 0, out.stderr
    lit, status, states = set(), None, None
    for line in out.stdout.split("\n"):
        f = line.split()
        if not f:
            continue
        if f[0] == 'LIT':
            lit.add(frozenset((srcs[int(f[1])], srcs[int(f[2])])))
        elif f[0] == 'STATES':
            states = int(f[1])
        elif f[0] in ('DONE', 'EARLY', 'CAP'):
            status = f[0]
    assert status == 'DONE', status
    return lit, states


def replay(cells, S, T, D):
    """d8's reflection tracer: a signed version of D that joins S to T legally, or None."""
    try:
        return d8tracer.certify(set(cells), S, T, D)
    except (RuntimeError, AssertionError):
        return None


def do_room(cells):
    cells = frozenset(cells)
    U = L.Unfolding(cells)
    reg = L.regular_points(cells)
    out = dict(cells=sorted(cells), n=len(cells), inst=0, dp_pairs=0, dp_lit_T=0, dp_lit_R=0,
               dp_disagree=[], checks=0, mismatch=0, skipped=0, t_states=0, r_states=0,
               c_disagree=[], slide_only=0, interior=[], iota_bad=0, replay_fail=[],
               py_room=0, room_pairs=0, room_pairs_lit_T=0, room_pairs_lit_C=0, room_disagree=[])
    if len(reg) < 1:
        return out
    c_lit, c_states = d8_lit(cells, U, reg)
    out['r_states'] = c_states
    ro = None
    if c_states <= PYCAP:
        ro = L.room_orbit(cells)
        assert ro['complete']
        assert c_states == ro['states'], (c_states, ro['states'])
        out['py_room'] = 1
        r_room = {frozenset((u[0], w[0])) for u, w in map(tuple, ro['lit']) if u[0] != w[0]}
        if r_room != c_lit:
            out['c_disagree'] = [sorted(map(list, pr)) for pr in r_room ^ c_lit]
    for o in ORIGINS:
        lifts = L.a_lifts(cells, o)
        if len(lifts) < 2:
            continue
        chk, bad, skip, res = L.state_check(cells, o, EPS, max_norm=MAX_NORM, check_cap=CHECKCAP)
        assert res['complete']
        ident = res['ident']
        name = {v: k for k, v in ident.items()}
        t_lit = {frozenset(name[i] for i in pr) for pr in res['lit']}
        a_pts = set(ident)
        out['inst'] += 1
        out['checks'] += chk
        out['mismatch'] += bad
        out['skipped'] += skip
        out['t_states'] += res['states']
        # room-point level: tuple side against d8's C decider (every room)
        pts = sorted({u[0] for u in a_pts})
        t_room = {frozenset((u[0], w[0])) for u, w in map(tuple, t_lit) if u[0] != w[0]}
        c_room = {pr for pr in c_lit if pr <= set(pts)}
        out['room_pairs'] += len(pts) * (len(pts) - 1) // 2
        out['room_pairs_lit_T'] += len(t_room)
        out['room_pairs_lit_C'] += len(c_room)
        for pr in t_room ^ c_room:
            out['room_disagree'].append(dict(origin=o, pair=sorted(map(list, pr)),
                                             tuple=pr in t_room, d8c=pr in c_room))
        if ro is None:
            r_lit = None
        else:
            # DP-point level: tuple side against the Python room decider
            r_lit = {pr for pr in ro['lit'] if pr <= a_pts}
            r_ns = {pr for pr in ro['lit_noslide'] if pr <= a_pts}
            out['dp_pairs'] += len(a_pts) * (len(a_pts) - 1) // 2
            out['dp_lit_T'] += len(t_lit)
            out['dp_lit_R'] += len(r_lit)
            for pr in t_lit ^ r_lit:
                out['dp_disagree'].append(dict(origin=o, pair=sorted(map(list, pr)),
                                               tuple=pr in t_lit, room=pr in r_lit))
            # room pairs that are lit only by a segment running along a wall
            room_pairs_lit = {frozenset((u[0], w[0])) for u, w in map(tuple, r_lit) if u[0] != w[0]}
            room_pairs_ns = {frozenset((u[0], w[0])) for u, w in map(tuple, r_ns) if u[0] != w[0]}
            out['slide_only'] += len(room_pairs_lit - room_pairs_ns)
        # interior pairs: the statement D0 itself
        ints = sorted(p for (p, f) in a_pts if f == 1)
        for x in range(len(ints)):
            for y in range(x + 1, len(ints)):
                S, T = ints[x], ints[y]
                tt = {(fs, ft): frozenset(((S, fs), (T, ft))) in t_lit for fs in (1, -1) for ft in (1, -1)}
                if r_lit is None:
                    rr = {(fs, ft): None for fs in (1, -1) for ft in (1, -1)}
                else:
                    rr = {(fs, ft): frozenset(((S, fs), (T, ft))) in r_lit
                          for fs in (1, -1) for ft in (1, -1)}
                if tt[1, 1] != tt[-1, -1] or tt[1, -1] != tt[-1, 1]:
                    out['iota_bad'] += 1
                rec = dict(S=S, T=T, tuple_same=tt[1, 1], tuple_opp=tt[1, -1],
                           room_same=rr[1, 1], room_opp=rr[1, -1],
                           tuple_lit=any(tt.values()),
                           room_lit=None if r_lit is None else any(rr.values()),
                           d8c_lit=frozenset((S, T)) in c_lit)
                # replay: room witness
                for (fs, ft) in ((1, 1), (1, -1)):
                    pr = frozenset(((S, fs), (T, ft)))
                    if ro is not None and pr in ro['witness']:
                        steps, d = ro['witness'][pr]
                        D = (steps * d[0], steps * d[1])
                        if replay(cells, S, T, D) is None and replay(cells, T, S, D) is None:
                            out['replay_fail'].append(dict(kind='room', S=S, T=T, D=D))
                        rec.setdefault('room_vec', D)
                    # replay: tuple witness through the slope of its state
                    ip = frozenset((ident[(S, fs)], ident[(T, ft)]))
                    if ip in res['witness']:
                        word, j, M = res['witness'][ip]
                        sl = L.state_slope(M, j)
                        if abs(sl[0]) + abs(sl[1]) > 20 * MAX_NORM:
                            rec['tuple_vec'] = 'skipped'
                            continue
                        found = None
                        for k in U.squares_at(S):
                            if U.dp_point(k) != (S, fs):
                                continue
                            for steps, u in L.ray(U, k, sl):
                                if u == (T, ft):
                                    found = steps
                                    break
                            if found:
                                break
                        if not found:
                            out['replay_fail'].append(dict(kind='tuple-walk', S=S, T=T, slope=sl))
                            continue
                        D = (found * sl[0], found * sl[1])
                        if replay(cells, S, T, D) is None:
                            out['replay_fail'].append(dict(kind='tuple', S=S, T=T, D=D))
                        rec.setdefault('tuple_vec', D)
                        rec.setdefault('tuple_arc', 'abcd'[j])
                        rec.setdefault('tuple_word_len', len(word))
                out['interior'].append(rec)
    return out


def has_interior_pair(cells):
    ints = [p for p in L.lattice_points(cells) if L.status(cells, p) == 'interior']
    return any((p[0] - q[0]) % 2 == 0 and (p[1] - q[1]) % 2 == 0
               for k, p in enumerate(ints) for q in ints[:k])


def _init(pycap, checkcap):
    global PYCAP, CHECKCAP
    PYCAP, CHECKCAP = pycap, checkcap


def main():
    nmax = int(sys.argv[1])
    workers = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    mode = sys.argv[3] if len(sys.argv) > 3 else 'fixed'
    nmin = int(sys.argv[4]) if len(sys.argv) > 4 else 1
    global PYCAP, CHECKCAP
    if len(sys.argv) > 5:
        PYCAP = int(sys.argv[5])
    if len(sys.argv) > 6:
        CHECKCAP = int(sys.argv[6])
    assert workers <= 2
    t0 = time.time()
    polys = L.fixed_polyominoes(nmax)
    rooms = []
    tally = {}
    for n in range(nmin, nmax + 1):
        ss = [p for p in polys[n] if L.strictly_simple(p)]
        if mode == 'free':
            ss = [p for p in ss if L.is_free_rep(p)]
        if mode == 'interior':
            ss = [p for p in ss if has_interior_pair(p)]
        tally[n] = (len(polys[n]), len(ss))
        rooms += ss
    print('polyominoes (all, strictly simple kept):', tally, flush=True)
    agg = Counter()
    interior, dis, cdis, fails, rooms_with_pair = [], [], [], [], 0
    by_n = {n: Counter() for n in range(nmin, nmax + 1)}
    rdis = []
    with Pool(workers, initializer=_init, initargs=(PYCAP, CHECKCAP)) as pool:
        for k, r in enumerate(pool.imap_unordered(do_room, rooms, chunksize=4)):
            for d in r['room_disagree']:
                d['cells'] = r['cells']
                rdis.append(d)
            for key in ('inst', 'dp_pairs', 'dp_lit_T', 'dp_lit_R', 'checks', 'mismatch', 'skipped',
                        't_states', 'r_states', 'slide_only', 'iota_bad', 'py_room', 'room_pairs',
                        'room_pairs_lit_T', 'room_pairs_lit_C'):
                agg[key] += r[key]
                by_n[r['n']][key] += r[key]
            by_n[r['n']]['rooms'] += 1
            agg['rooms'] += 1
            agg['max_r_states'] = max(agg['max_r_states'], r['r_states'])
            if r['interior']:
                rooms_with_pair += 1
                by_n[r['n']]['rooms_with_interior_pair'] += 1
                for rec in r['interior']:
                    rec['cells'] = r['cells']
                    interior.append(rec)
                    by_n[r['n']]['interior_pairs'] += 1
            for d in r['dp_disagree']:
                d['cells'] = r['cells']
                dis.append(d)
            if r['c_disagree']:
                cdis.append(dict(cells=r['cells'], pairs=r['c_disagree']))
            for f in r['replay_fail']:
                f['cells'] = r['cells']
                fails.append(f)
            if (k + 1) % 200 == 0:
                print(k + 1, 'rooms', round(time.time() - t0), 's', dict(agg), flush=True)
    pat = Counter()
    for rec in interior:
        pat[(rec['tuple_lit'], rec['room_lit'], rec['d8c_lit'])] += 1
    lift = Counter((rec['tuple_same'], rec['tuple_opp']) for rec in interior)
    summary = dict(
        nmax=nmax, nmin=nmin, mode=mode, pycap=PYCAP, checkcap=CHECKCAP, eps=EPS, max_norm=MAX_NORM, seconds=round(time.time() - t0, 1),
        polyominoes={n: dict(all=a, strictly_simple=b) for n, (a, b) in tally.items()},
        totals=dict(agg), by_area={n: dict(c) for n, c in by_n.items()},
        rooms_with_interior_pair=rooms_with_pair, interior_pairs=len(interior),
        interior_verdicts={f"tuple={a},room={b},d8c={c}": v for (a, b, c), v in sorted(pat.items())},
        interior_lift_pattern={f"same_face={a},opposite_face={b}": v for (a, b), v in sorted(lift.items())},
        dp_disagreements=len(dis), room_disagreements=len(rdis), d8c_disagreements=len(cdis),
        replay_failures=len(fails))
    print(json.dumps(summary, indent=1))
    with open(L.HERE / f'census_n{nmin}-{nmax}_{mode}.json', 'w') as f:
        json.dump(dict(summary=summary, interior=interior, dp_disagree=dis, room_disagree=rdis,
                       d8c_disagree=cdis,
                       replay_fail=fails), f, separators=(',', ':'))


if __name__ == '__main__':
    main()
