"""Task 3: monodromy and block systems of LIT rooms with <= 21 walls from the record.

Sources (lit status is the record's; each has a saved connecting path whose endpoints are checked
here to equal the marks, but the path itself is not replayed):
  ortho  - 30 orthogonal k7-pilot models + its W18 positive control (copied to ./inputs),
           analysed in the square (pillow) and the tri (canonical45) frameworks;
  screen - .context/transparent-simple-two-symmetric-screen.json records with W <= 21;
  global - .context/two-global-*.json records with W <= 21;
  learned- .context/illumination-k4-codex/k5-proof-continuation/learned.jsonl rooms (W <= 21).
The last three are read in place and their SHA-256 recorded.

Run: python3 -B task3_lit_controls.py   -> writes task3_lit_controls.json (several minutes)
"""
import hashlib
import json
import sys
from collections import Counter
from fractions import Fraction as Fr
from pathlib import Path

from monodromy import Room, analyse_room

HERE = Path(__file__).resolve().parent
INP = HERE / 'inputs'
CTX = HERE.parents[3]
assert CTX.name == '.context', CTX


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def frac_pt(p):
    return tuple(Fr(a, b) for a, b in p) if isinstance(p[0], list) else tuple(Fr(x) for x in p)


def ortho_rooms():
    for f in sorted((INP / 'k7-models').glob('model-*.json')):
        d = json.loads(f.read_text())
        path = json.loads((INP / 'k7-paths' / f.name).read_text())
        assert path['status'] == 'LIT'
        ends = [tuple(Fr(x) for x in path['path'][0]), tuple(Fr(x) for x in path['path'][-1])]
        assert ends == [tuple(map(Fr, m)) for m in d['marks']]
        yield 'ortho', f.stem, d['cells'], d['triangles'], d['marks']
    c = json.loads((INP / 'k7-controls.json').read_text())['controls'][0]
    assert c['SAT'] and c['reflections'] == 0
    tris = None
    yield 'ortho', 'k7-control-W18', c['cells'], tris, c['geometry']['interior_A']


def tri_records():
    p = CTX / 'transparent-simple-two-symmetric-screen.json'
    for i, r in enumerate(json.loads(p.read_text())['records']):
        if r['walls'] <= 21:
            assert r['witness']['status'] == 'illuminated'
            yield 'screen', 'screen-%d' % i, r['room']['triangles'], r['room']['marked'], r['witness']['path']
    for p in sorted(CTX.glob('two-global-[0-9]-[0-9].json')):
        for i, r in enumerate(json.loads(p.read_text())['records']):
            if r['counts']['walls'] <= 21:
                yield 'global', '%s-%d' % (p.stem, i), r['room']['triangles'], r['room']['marked'], r['witness']['path']
    p = CTX / 'illumination-k4-codex/k5-proof-continuation/learned.jsonl'
    with p.open() as fh:
        for i, line in enumerate(fh):
            r = json.loads(line)
            yield 'learned', 'learned-%d' % i, r['room'], [[0, 0], r['q']], r['path']


def row(r):
    proper = [b for b in r['block_systems'] if b['trivial'] == 'proper']
    return dict(name=r['name'], fw=r['framework'], W=r['ledger']['walls'], r=r['ledger']['reflex'],
                k=len(r['ledger']['transparent_nonA']), degree=r['degree'], order=r['order'],
                G='S_n' if r['is_symmetric'] else 'A_n' if r['is_alternating'] else 'other',
                primitive=r['primitive'], proper_block_sizes=[b['block_size'] for b in proper],
                proper_parity=[b['parity_property'] for b in proper],
                proper_separating=[b['phiS_disjoint_phiT'] for b in proper],
                parity_and_separating=[b['block_size'] for b in proper
                                       if b['parity_property'] and b['phiS_disjoint_phiT']])


def tally(rows):
    t = Counter()
    for x in rows:
        t['rooms'] += 1
        t['primitive'] += x['primitive']
        t['G=' + x['G']] += 1
        t['k=%d' % x['k']] += 1
        t['W=%d' % x['W']] += 1
        t['with_proper_parity_separating_factor'] += bool(x['parity_and_separating'])
        t['proper_block_sizes=' + str(x['proper_block_sizes'])] += 1
    return dict(sorted(t.items()))


def main():
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else None
    out = {'inputs_read_in_place': {}, 'groups': {}, 'flagged_full_detail': []}
    for p in [CTX / 'transparent-simple-two-symmetric-screen.json',
              CTX / 'illumination-k4-codex/k5-proof-continuation/learned.jsonl',
              *sorted(CTX.glob('two-global-[0-9]-[0-9].json'))]:
        out['inputs_read_in_place'][str(p.relative_to(CTX))] = sha(p)
    rows = {}
    for src, name, cells, tris, marks in ortho_rooms():
        for fw in ('square', 'tri'):
            if fw == 'square':
                room = Room(name, 'square', [tuple(c) for c in cells], marks)
            else:
                from monodromy import tris_of_squares
                room = Room(name + '_tri', 'tri', tris_of_squares([tuple(c) for c in cells]), marks)
            r = analyse_room(room)
            assert r['ledger']['walls'] <= 21
            rows.setdefault('ortho_' + fw, []).append(row(r))
            if any(b['trivial'] == 'proper' and b['parity_property'] and b['phiS_disjoint_phiT'] for b in r['block_systems']):
                out['flagged_full_detail'].append(r)
    seen = Counter()
    for src, name, tris, marks, path in tri_records():
        if limit and seen[src] >= limit:
            continue
        ends = [frac_pt(path[0]), frac_pt(path[-1])]
        assert ends == [tuple(map(Fr, m)) for m in marks], (name, ends, marks)
        room = Room(name, 'tri', [tuple(map(tuple, t)) for t in tris], marks)
        r = analyse_room(room)
        if r['ledger']['walls'] > 21:
            seen['skipped_W>21_' + src] += 1
            continue
        seen[src] += 1
        rows.setdefault(src, []).append(row(r))
        if any(b['trivial'] == 'proper' and b['parity_property'] and b['phiS_disjoint_phiT'] for b in r['block_systems']):
            out['flagged_full_detail'].append(r)
        if seen[src] % 2000 == 0:
            print(src, seen[src], flush=True)
    for g, rs in rows.items():
        out['groups'][g] = {'tally': tally(rs), 'rows': rs}
        print(g, json.dumps(tally(rs)))
    out['skips'] = {k: v for k, v in seen.items() if k.startswith('skipped')}
    print('flagged', len(out['flagged_full_detail']), out['skips'])
    (HERE / ('task3_lit_controls.json' if not limit else 'task3_lit_controls_sample.json')).write_text(
        json.dumps(out, indent=1, default=str) + '\n')


if __name__ == '__main__':
    main()
