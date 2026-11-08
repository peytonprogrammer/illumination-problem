"""Solve -> trace -> cut loop on the open (2,0) outside sets, then a full partition replay.

For each open set: solve Claude's strong model with all current cuts. If a room comes back,
search for an illuminating ray with Codex's tracer (search only; bounds 12, then 30), check it
with Claude's exact checker, and add the cut built from the tiles the path touches. A room
with no verified ray is recorded as an unlit candidate and its set stays open. Solver caps
also stay open. Finally every one of the 699 outside sets is re-solved with the final cuts.
Usage: claude_cut_loop.py [max_rounds_per_set]
"""
import json
import os
import sys
import time
from pathlib import Path
HERE = Path(__file__).resolve().parent
os.environ['CLAUDE_TARGET'] = '2,0'
os.environ['CLAUDE_PLACEMENT_INPUTS'] = str(HERE/'snapshot')
sys.path[:0] = [str(HERE.parent/'placement-2-1'), str(HERE.parents[1])]
import claude_placement_check as c
from illumination_paths import find_path

ROUNDS = int(sys.argv[1]) if len(sys.argv) > 1 else 300
OUT = HERE/os.environ.get('CLAUDE_LOOP_OUT', 'claude-cut-loop-2-0.json')
RESUME = [HERE/f for f in os.environ.get('CLAUDE_RESUME', '').split(',') if f]


def mirror(room_list, path):
    """Reflect y -> -y. It fixes both marks (0,0) and (4,0), so a lit room maps to a lit room."""
    return ([[[x, -y] for x, y in t] for t in room_list],
            [[[x[0], x[1]], [-y[0], y[1]]] for x, y in path])


def cut_of(room_list, path):
    room = c.norm(room_list)
    ok, why, touched = c.check_path(room, path, c.MARKS)
    assert ok, why
    return tuple(sorted((c.index[t], int(t in room)) for t in touched if t in c.index))


def ray(room_list):
    room = c.norm(room_list)
    for bound in (12, 30):
        w = find_path(dict(triangles=room_list, marked=c.MARKS), bound, 3000)
        if w['status'] == 'illuminated':
            ok, why, touched = c.check_path(room, w['path'], c.MARKS)
            assert ok, why  # the tracer and Claude's checker disagree: stop loudly
            cut = tuple(sorted((c.index[t], int(t in room)) for t in touched if t in c.index))
            return cut, w
    return None, None


def main():
    t0 = time.time()
    stats, base = c.collect()
    cuts = set(base)
    for f in RESUME:  # earlier loop rays, re-checked from scratch before use
        for r in json.loads(f.read_text())['rays']:
            cuts.add(cut_of(r['room'], r['witness']['path']))
            if os.environ.get('CLAUDE_MIRROR') == '1':
                cuts.add(cut_of(*mirror(r['room'], r['witness']['path'])))
    print(json.dumps(dict(base=len(base), resumed=len(cuts)-len(base))), flush=True)
    prev = json.loads((HERE/'claude-placement-2-0.json').read_text())
    os.environ['CLAUDE_CAP'] = '120'
    rays, sets = [], []
    only = os.environ.get('CLAUDE_ONLY')  # sets split by '|', cells by ';', e.g. '1,-1|1,1'
    for leaf in prev['open']:
        if only and ';'.join(','.join(map(str, c_)) for c_ in leaf['cells']) not in only.split('|'):
            continue
        cells = frozenset(map(tuple, leaf['cells']))
        row = dict(cells=sorted(cells), rounds=0)
        while row['rounds'] < ROUNDS:
            res = c.model(sorted(cuts), cells)
            row['status'] = res['status']
            if 'room' not in res:
                break
            cut, w = ray(res['room'])
            if cut is None:
                row['status'] = 'UNLIT_CANDIDATE'; row['room'] = res['room']; break
            assert cut not in cuts  # a cut already present would have excluded this room
            cuts.add(cut); row['rounds'] += 1
            if os.environ.get('CLAUDE_MIRROR') == '1':
                cuts.add(cut_of(*mirror(res['room'], w['path'])))
            rays.append(dict(cells=sorted(cells), room=res['room'], witness=w, tile_facts=list(cut)))
        else:
            row['status'] = 'ROUND_CAP'
        sets.append(row)
        print(json.dumps({k: v for k, v in row.items() if k != 'room'}), flush=True)
        OUT.write_text(json.dumps(dict(stats=stats, base_cuts=len(base), cuts=len(cuts), sets=sets, rays=rays), indent=1)+'\n')
    # Full partition replay with the final cuts.
    final = sorted(cuts); replay = {}
    for s in [frozenset(s) for s in c.connected_outside_sets(c.R, c.outside, c.r)]:
        st = c.model(final, s)['status']
        replay[st] = replay.get(st, 0) + 1
        if st != 'INFEASIBLE':
            print('replay open', sorted(s), st, flush=True)
    summary = dict(base_cuts=len(base), final_cuts=len(cuts), new_rays=len(rays),
                   loop={s: sum(r['status'] == s for r in sets) for s in {r['status'] for r in sets}},
                   replay_699=replay, placement_excluded=replay == {'INFEASIBLE': sum(replay.values())},
                   seconds=round(time.time()-t0))
    print(json.dumps(summary), flush=True)
    OUT.write_text(json.dumps(dict(summary=summary, stats=stats, sets=sets, rays=rays), indent=1)+'\n')


if __name__ == '__main__':
    main()
