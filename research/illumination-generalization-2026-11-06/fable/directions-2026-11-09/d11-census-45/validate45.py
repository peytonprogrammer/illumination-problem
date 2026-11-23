"""Validation of the d11 pipeline before the census.

Rooms:
  dark:  Castro 24, Tokarsky 26 (worksheet coordinates, marks (2,-2),(6,-2));
         the known 22-wall orthogonal room as 30 triangles, marks (0,0),(2,2);
         Wolecki's pinched 22-gon (weakly simple), marks (0,0),(2,2);
         the 327 clean census rooms at W = 24..26 from d4/inputs/census.
  lit:   transparent-simple-two-symmetric-screen.json (W <= 21), two-global-*.json
         (W <= 21), and the first 200 rooms of learned.jsonl.

Steps: shoot45 (exact shooting + independent plane tracer) on every room and every
same-class pair; orbit45 (complete orbit decider) on every marked dark pair and on
40 marked lit pairs; d6's Hurwitz decider on the dark pairs; N_min separation.
Also a negative test of the plane tracer (wrong target must be rejected).

Run: python3 -B validate45.py > validate45.log
"""
import glob
import json
import subprocess
import time
from pathlib import Path

import rooms45 as R

HERE = R.HERE
OUT = HERE / 'validation'
OUT.mkdir(exist_ok=True)


def load_rooms():
    k = R.worksheet_constants()
    rooms = []

    def add(name, kind, tiles, marks, expect, polygon_W=None):
        b = R.boundary(tiles)
        rooms.append(dict(name=name, kind=kind, tiles=sorted(tiles), marks=[tuple(m) for m in marks], expect=expect,
                          simple=b['simple'], W=b['W_cycle'], n_cycles=b['n_cycles'], polygon_W=polygon_W,
                          corners=len(b['corners'])))

    add('castro24', 'dark', R.tiles_from_polygon(k['CASTRO24']), k['PUBLISHED_ST'], 'DARK', 24)
    add('tokarsky26', 'dark', R.tiles_from_polygon(k['TOKARSKY26']), k['PUBLISHED_ST'], 'DARK', 26)
    add('room22_tri', 'dark', R.tiles_from_polygon(k['ROOM22']), [(0, 0), (2, 2)], 'DARK', 22)
    add('wolecki22_pinched', 'dark', R.tiles_from_polygon(R.WOLECKI22), [(0, 0), (2, 2)], 'DARK', 22)
    for f in sorted((R.D4 / 'inputs' / 'census').glob('parity-W*.json')):
        d = json.loads(f.read_text())
        poly = [tuple(p) for p in json.loads(d['vertices'])] if isinstance(d['vertices'], str) else [tuple(p) for p in d['vertices']]
        marks = json.loads(d['marked']) if isinstance(d['marked'], str) else d['marked']
        add(d['tag'], 'census_dark', R.tiles_from_polygon(poly), marks, 'DARK', len(poly))
    p = R.CTX / 'transparent-simple-two-symmetric-screen.json'
    for i, r in enumerate(json.loads(p.read_text())['records']):
        if r['walls'] <= 21 and not r['room'].get('slits'):
            add('screen-%d' % i, 'lit', [R.tri_to_ijh(t) for t in r['room']['triangles']], r['room']['marked'], 'LIT', r['walls'])
    for p in sorted(R.CTX.glob('two-global-[0-9]-[0-9].json')):
        for i, r in enumerate(json.loads(p.read_text())['records']):
            if r['counts']['walls'] <= 21 and not r['room'].get('slits'):
                add('%s-%d' % (p.stem, i), 'lit', [R.tri_to_ijh(t) for t in r['room']['triangles']], r['room']['marked'], 'LIT',
                    r['counts']['walls'])
    with (R.CTX / 'illumination-k4-codex/k5-proof-continuation/learned.jsonl').open() as fh:
        for i, line in enumerate(fh):
            if i >= 200:
                break
            r = json.loads(line)
            add('learned-%d' % i, 'lit', [R.tri_to_ijh(t) for t in r['room']], [[0, 0], r['q']], 'LIT')
    return rooms


def corner_count_rule(room):
    """W as shoot45 counts it: distinct corner points (a pinch point once)."""
    return room['corners']


def main():
    t0 = time.time()
    rooms = load_rooms()
    print('rooms loaded', len(rooms), {k: sum(1 for r in rooms if r['kind'] == k) for k in ('dark', 'census_dark', 'lit')})
    for r in rooms:
        if r['kind'] == 'dark':
            print('  %-18s tiles %2d strictly_simple %s W(boundary walk) %d polygon_W %s cycles %d' % (
                r['name'], len(r['tiles']), r['simple'], r['W'], r['polygon_W'], r['n_cycles']))
    bad_w = [r['name'] for r in rooms if r['polygon_W'] is not None and r['W'] != r['polygon_W']]
    print('rooms whose boundary-walk W differs from the record W:', bad_w)
    inp = OUT / 'rooms.txt'
    inp.write_text(''.join(R.room_line(r['tiles'], corner_count_rule(r)) + '\n' for r in rooms))
    subprocess.run([str(HERE / 'shoot45'), '40', '99', str(inp), str(OUT / 'shoot.out'), str(OUT / 'shoot.sv'),
                    str(OUT / 'problems.txt'), 'all'], check=True)
    # parse per-pair lines
    res = {}
    rid = None
    stats = {}
    for line in (OUT / 'shoot.out').read_text().splitlines():
        if line.startswith('R '):
            rid = int(line.split()[1])
        elif line.startswith('P '):
            p = line.split()
            S, T = (int(p[2]), int(p[3])), (int(p[4]), int(p[5]))
            res[(rid, frozenset((S, T)))] = line
        elif line.startswith('# verify_fail') or line.startswith('# max_steps'):
            stats[line.split()[1]] = int(line.split()[2])
    print('shoot45 verify_fail', stats.get('verify_fail'), 'max_steps', stats.get('max_steps'))
    summary = {}
    for idx, r in enumerate(rooms, start=1):
        line = res.get((idx, frozenset(r['marks'])))
        if line is None:
            r['shoot'] = 'NO_PAIR_LINE'
        else:
            p = line.split()
            r['shoot'] = 'LIT' if p[6] == 'L' else 'SURVIVOR'
            r['k'] = int(p[p.index('k') + 1])
            r['sep'] = int(p[p.index('sep') + 1])
            r['shoot_line'] = line
        key = (r['kind'], r['shoot'])
        summary[key] = summary.get(key, 0) + 1
    print('shoot45 on marked pairs:', {'%s/%s' % k: v for k, v in sorted(summary.items())})
    print('N_min separation on marked pairs:',
          {'%s sep=%s' % (kind, s): sum(1 for r in rooms if r['kind'] == kind and r.get('sep') == s)
           for kind in ('dark', 'census_dark', 'lit') for s in (0, 1)})
    lit_sep = [r['name'] for r in rooms if r['kind'] == 'lit' and r.get('sep') == 1]
    print('lit controls with a separating N_min:', lit_sep)
    # orbit45 on marked dark pairs and 40 marked lit pairs
    probs = {}
    for line in (OUT / 'problems.txt').read_text().splitlines():
        c = line.split('#')[1].split()
        probs[(int(c[0]), frozenset(((int(c[2]), int(c[3])), (int(c[4]), int(c[5])))))] = line
    chosen = [i for i, r in enumerate(rooms, start=1) if r['kind'] == 'dark']
    chosen += [i for i, r in enumerate(rooms, start=1) if r['kind'] == 'census_dark'][:3]
    lit_ids = [i for i, r in enumerate(rooms, start=1) if r['kind'] == 'lit']
    chosen += lit_ids[:13] + lit_ids[13:320:12] + lit_ids[320::20]
    lines = [probs[(i, frozenset(rooms[i - 1]['marks']))] for i in chosen]
    (OUT / 'orbit_input.txt').write_text('\n'.join(lines) + '\n')
    with open(OUT / 'orbit_input.txt') as fin:
        out = subprocess.run([str(HERE / 'orbit45'), '3000000'], stdin=fin, capture_output=True, text=True, check=True).stdout
    for i, ol in zip(chosen, out.splitlines()):
        p = ol.split()
        rooms[i - 1]['orbit45'] = dict(states=int(p[1]), verdict=p[2])
    print('orbit45 results:')
    agree = 0
    for i in chosen:
        r = rooms[i - 1]
        o = r['orbit45']
        ok = (o['verdict'] == r['expect']) or (o['verdict'] == 'UNDECIDED_CAP')
        agree += o['verdict'] == r['expect']
        if r['kind'] != 'lit' or o['verdict'] != 'LIT':
            print('  %-20s expect %s orbit45 %s states %d k %s sep %s shoot %s' % (r['name'], r['expect'], o['verdict'], o['states'],
                                                                                r.get('k'), r.get('sep'), r['shoot']))
    print('orbit45 agrees with expectation on %d of %d chosen pairs (lit ones not listed agree)' % (agree, len(chosen)))
    # d6 decider on the dark rooms
    for r in rooms:
        if r['kind'] == 'dark':
            t1 = time.time()
            try:
                r['d6'] = R.d6_decide(r['tiles'], r['marks'], max_states=200000)
            except Exception as e:  # noqa
                r['d6'] = dict(error=repr(e))
            print('  d6 %-18s %s (%.0f s)' % (r['name'], r['d6'], time.time() - t1))
    # negative test of the plane tracer: replay every lit certificate of the controls with a wrong target
    neg = subprocess.run([str(HERE / 'negtest45'), str(OUT / 'shoot.out'), str(inp)], capture_output=True, text=True)
    print('negative tracer test:', neg.stdout.strip(), neg.stderr.strip())
    keep = [dict((k, v) for k, v in r.items() if k != 'tiles') for r in rooms if r['kind'] != 'lit' or 'orbit45' in r]
    (HERE / 'validate45.json').write_text(json.dumps(keep, indent=1, default=str) + '\n')
    print('done in %.0f s' % (time.time() - t0))


if __name__ == '__main__':
    main()
