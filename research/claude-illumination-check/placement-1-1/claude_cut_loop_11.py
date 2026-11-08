"""Solve -> trace -> cut loop for placement (1,1), then a full 2,530-set partition replay.

Same method as placement-2-0/claude_cut_loop.py, with two changes:
- Symmetry: every isometry of the canonical tiling that maps the mark set {(0,0),(2,2)} to
  itself: (y,x), (2-x,2-y), and (2-y,2-x). Each image path is checked exactly in the image room.
- A cut is kept only if the room lies in Claude's support. A room outside the support can't
  occur in the model, so dropping its cut is sound.
Every new ray is appended to rays-1-1.jsonl as soon as it is found, so the loop can resume.
Usage: claude_cut_loop_11.py [max_rounds_per_set]
"""
import json
import os
import sys
import time
from fractions import Fraction as F
from pathlib import Path
HERE = Path(__file__).resolve().parent
os.environ['CLAUDE_TARGET'] = '1,1'
os.environ['CLAUDE_PLACEMENT_INPUTS'] = str(HERE/'snapshot2')
sys.path[:0] = [str(HERE.parent/'placement-2-1'), str(HERE.parents[1])]
import claude_placement_check as c
from illumination_paths import find_path

ROUNDS = int(sys.argv[1]) if len(sys.argv) > 1 else 3000
RAYS = HERE/'rays-1-1.jsonl'
MAPS = [lambda x, y: (y, x), lambda x, y: (2-x, 2-y), lambda x, y: (2-y, 2-x)]
SUPPORT = set(c.ts)


def image(g, room_list, path):
    room = [[list(g(*p)) for p in t] for t in room_list]
    pts = [g(F(*x), F(*y)) for x, y in path]
    return room, [[[v.numerator, v.denominator] for v in p] for p in pts]


def cut_of(room_list, path):
    room = c.norm(room_list)
    if not room <= SUPPORT:
        return None
    ok, why, touched = c.check_path(room, path, c.MARKS)
    assert ok, why
    return tuple(sorted((c.index[t], int(t in room)) for t in touched if t in c.index))


def cuts_of(room_list, path):
    out = {cut_of(room_list, path)}
    for g in MAPS:
        out.add(cut_of(*image(g, room_list, path)))
    return out - {None}


def ray(room_list):
    for bound in (12, 30):
        w = find_path(dict(triangles=room_list, marked=c.MARKS), bound, 3000)
        if w['status'] == 'illuminated':
            return w
    return None


def main():
    t0 = time.time()
    stats, base = c.collect()
    cuts = set(base)
    for r in json.loads((HERE/'claude-placement-1-1-traced.json').read_text()):
        path = r['path'] if r.get('verified') else json.loads(
            (HERE/f"unlit-{'_'.join(f'{a}{b}' for a, b in r['cells'])}.json").read_text())['retrace']['path']
        cuts |= cuts_of(r['room'], path)
    if RAYS.exists():
        for line in RAYS.read_text().splitlines():
            r = json.loads(line); cuts |= cuts_of(r['room'], r['path'])
    print(json.dumps(dict(stats=stats, base=len(base), start_cuts=len(cuts))), flush=True)
    open_sets = [frozenset(map(tuple, l['cells'])) for l in json.loads((HERE/'claude-recheck-open-codex.json').read_text())['open']]
    os.environ['CLAUDE_CAP'] = '120'
    rows = []
    for cells in open_sets:
        row = dict(cells=sorted(cells), rounds=0)
        while row['rounds'] < ROUNDS:
            res = c.model(sorted(cuts), cells)
            row['status'] = res['status']
            if 'room' not in res:
                break
            w = ray(res['room'])
            if w is None:
                row['status'] = 'UNLIT_CANDIDATE'; row['room'] = res['room']
                (HERE/f"candidate-{'_'.join(f'{a}{b}' for a, b in sorted(cells))}.json").write_text(
                    json.dumps(dict(triangles=res['room'], marked=c.MARKS))+'\n')
                break
            new = cuts_of(res['room'], w['path'])
            assert new - cuts  # the room's own cut must be new
            cuts |= new; row['rounds'] += 1
            with RAYS.open('a') as f:
                f.write(json.dumps(dict(cells=sorted(cells), room=res['room'], path=w['path'], direction=w['direction']))+'\n')
        else:
            row['status'] = 'ROUND_CAP'
        rows.append(row)
        print(json.dumps({k: v for k, v in row.items() if k != 'room'}), round(time.time()-t0), flush=True)
    final = sorted(cuts); replay = {}
    for s in [frozenset(s) for s in c.connected_outside_sets(c.R, c.outside, c.r)]:
        st = c.model(final, s)['status']
        replay[st] = replay.get(st, 0) + 1
        if st != 'INFEASIBLE':
            print('replay open', sorted(s), st, flush=True)
    summary = dict(final_cuts=len(cuts), loop={s: sum(r['status'] == s for r in rows) for s in {r['status'] for r in rows}},
                   replay=replay, placement_excluded=set(replay) == {'INFEASIBLE'}, seconds=round(time.time()-t0))
    print(json.dumps(summary), flush=True)
    (HERE/'claude-cut-loop-1-1.json').write_text(json.dumps(dict(summary=summary, sets=rows), indent=1)+'\n')


if __name__ == '__main__':
    main()
