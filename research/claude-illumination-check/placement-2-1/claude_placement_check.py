"""Claude's independent whole-placement check of target(2,1).

Cuts: every (room, witness path) found anywhere in the frozen mask12 inputs is checked with
Claude's exact path checker for marks (0,0),(4,2). Claude then builds each cut itself from
the tiles whose closure meets the path, indexed in Claude's own support. Codex tile_facts
and triangle indices are not used.

Model: claude_k3_strong.py, with no Codex cut loading (use_cuts=False).
Partition: Claude splits on the used outside-cell set (every connected set the model
allows), then on the 8-tile fan at A-cell (1,0), and then on the fan at (1,1) for any
branch that is still UNKNOWN. Each split covers every value of its variables, so the
leaves cover the whole model.
Usage: claude_placement_check.py [--mono SECONDS]
"""
import json
import os
import sys
import time
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE.parent), str(HERE.parent/'two-star-k3'), str(HERE.parent/'three-star')]
from claude_ray_guard_check import cell_tiles, check_path
from claude_two_star_k3_geometry import support
from claude_three_star_reduction import neighbors
from claude_k3_strong import build, connected_outside_sets

TARGET = tuple(int(v) for v in os.environ.get('CLAUDE_TARGET', '2,1').split(','))
MARKS = [(0, 0), (2*TARGET[0], 2*TARGET[1])]
TAG = f'{TARGET[0]}-{TARGET[1]}'
INPUTS = Path(os.environ.get('CLAUDE_PLACEMENT_INPUTS', str(HERE/'run/.context')))
norm = lambda tri: frozenset(tuple(sorted(tuple(v) for v in t)) for t in tri)
full, allowed, r = support(TARGET)
ts = sorted({t for c in allowed for t in cell_tiles(*c)})
index = {t: i for i, t in enumerate(ts)}
R = set(full) | neighbors(full)
outside = sorted(allowed - R)


def walk(x, found):
    if isinstance(x, dict):
        room, wit = x.get('room'), x.get('witness')
        if isinstance(room, dict) and isinstance(wit, dict) and wit.get('status') == 'illuminated' and 'path' in wit:
            key = (norm(room['triangles']), json.dumps(wit['path']))
            found.setdefault(key, None)
        for v in x.values():
            walk(v, found)
    elif isinstance(x, list):
        for v in x:
            walk(v, found)


def collect():
    found, files = {}, 0
    for f in sorted(INPUTS.rglob('*.json')):
        if TAG not in f.name:
            continue
        files += 1
        walk(json.loads(f.read_text()), found)
    cuts, rejected, vacuous = set(), 0, 0
    for (room, path) in found:
        ok, _, touched = check_path(room, json.loads(path), MARKS)
        if not ok:
            rejected += 1; continue
        if any(t in room and t not in index for t in touched) or not room <= set(ts):
            vacuous += 1; continue  # room leaves Claude's support; the cut can never fire
        cuts.add(tuple(sorted((index[t], int(t in room)) for t in touched if t in index)))
    return dict(files=files, witnesses=len(found), rejected=rejected, vacuous=vacuous), sorted(cuts)


def model(cuts, cells=None, fans=()):
    def extra(m, x, idx, used, _):
        for facts in cuts:
            m.add_bool_or([x[i].Not() if v else x[i] for i, v in facts])
        if cells is not None:
            for c in outside:
                m.add(used[c] == int(c in cells))
        for cell, mask in fans:
            p = (2*cell[0], 2*cell[1])
            for j, t in enumerate(t for t in ts if p in t):
                m.add(x[idx[t]] == (mask >> j & 1))
    return build(TARGET, use_cuts=False, extra=extra)


def main():
    t0 = time.time()
    stats, cuts = collect()
    print(json.dumps(stats | dict(cuts=len(cuts))), flush=True)
    out = dict(stats=stats, cuts=len(cuts), leaves=[], open=[])
    if '--mono' in sys.argv:
        os.environ['CLAUDE_CAP'] = sys.argv[sys.argv.index('--mono')+1]
        res = model(cuts)
        out['monolithic'] = res
        print('monolithic', json.dumps({k: v for k, v in res.items() if k != 'room'}), flush=True)
    os.environ['CLAUDE_CAP'] = os.environ.get('CLAUDE_LEAF_CAP', '60')
    sets = [frozenset(s) for s in connected_outside_sets(R, outside, r)]
    for cells in sets:
        res = model(cuts, cells); st = res['status']
        if st == 'INFEASIBLE':
            out['leaves'].append(dict(cells=sorted(cells), status=st)); continue
        print('split', sorted(cells), st, flush=True)
        if '--fans' not in sys.argv:
            leaf = dict(cells=sorted(cells), status=st, room=res.get('room'))
            out['leaves'].append(leaf); out['open'].append(leaf); continue
        for a in range(256):
            res = model(cuts, cells, [((1, 0), a)])
            if res['status'] == 'INFEASIBLE':
                out['leaves'].append(dict(cells=sorted(cells), fan10=a, status='INFEASIBLE')); continue
            for b in range(256):
                res = model(cuts, cells, [((1, 0), a), ((1, 1), b)])
                leaf = dict(cells=sorted(cells), fan10=a, fan11=b, status=res['status'])
                out['leaves'].append(leaf)
                if res['status'] != 'INFEASIBLE':
                    leaf['room'] = res.get('room')
                    out['open'].append(leaf); print('OPEN', json.dumps({k: v for k, v in leaf.items() if k != 'room'}), flush=True)
    out['outside_sets'] = len(sets)
    out['status'] = 'EXCLUDED' if not out['open'] else 'OPEN'
    out['seconds'] = round(time.time() - t0)
    print(json.dumps(dict(status=out['status'], outside_sets=len(sets), leaves=len(out['leaves']),
                          open=len(out['open']), seconds=out['seconds'])), flush=True)
    (Path(os.environ.get('CLAUDE_PLACEMENT_OUT', str(HERE)))/f'claude-placement-{TAG}.json').write_text(json.dumps(out, indent=1)+'\n')


if __name__ == '__main__':
    main()
