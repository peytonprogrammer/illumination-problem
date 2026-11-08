"""Verify Codex's seed cuts: rays reused from lower-exception phases, recompiled to the k=3 support.

Each seed names (file, record_index, guard_index). Claude loads that guard's room and
witness, checks the path exactly, and checks the seed's tile facts (indexed in the
k=3 support) fix every tile whose closure meets the path to its state in the room.
Writes verified seed facts per target for claude_k3_strong.py.
"""
import json, os, sys
from pathlib import Path
HERE = Path(__file__).parent
sys.path[:0] = [str(HERE.parent), str(HERE), str(HERE.parent/'three-star')]
from claude_ray_guard_check import cell_tiles, check_path
from claude_two_star_k3_geometry import support

INP = HERE/os.environ.get('CLAUDE_INPUTS', 'inputs-df')
norm = lambda tri: {tuple(sorted(tuple(v) for v in t)) for t in tri}
summary, verified = {}, {}
for case in sorted((INP/'three-two-star').glob('case-*.json')):
    seeds = json.loads(case.read_text()).get('seeds', [])
    if not seeds: continue
    tgt = tuple(int(v) for v in case.stem.split('-')[1:])
    full, allowed, r = support(tgt)
    ts = sorted({t for c in allowed for t in cell_tiles(*c)}); index = {t: i for i, t in enumerate(ts)}
    marks = [(0, 0), (2*tgt[0], 2*tgt[1])]
    cache, fails, good = {}, [], []
    for s in seeds:
        src = INP/s['file'] if (INP/s['file']).exists() else INP/'three-two-star'/s['file']
        data = cache.setdefault(src, json.loads(src.read_text()))
        g = data['records'][s['record_index']]['derived_guards'][s['guard_index']]
        room = norm(g['room']['triangles'])
        ok, why, touched = check_path(room, g['witness']['path'], marks)
        facts = {i: v for i, v in s['tile_facts']}
        bad = (not ok or not room <= set(ts)
               or any(t in index and facts.get(index[t]) != int(t in room) for t in touched)
               or any(t not in index and t in room for t in touched)
               or any(v != int(ts[i] in room) for i, v in facts.items()))
        (fails if bad else good).append(s if bad else sorted(facts.items()))
    summary[str(tgt)] = dict(seeds=len(seeds), verified=len(good), failures=len(fails), first_failures=fails[:3])
    verified[f'{tgt[0]}-{tgt[1]}'] = good
    print(tgt, summary[str(tgt)]['seeds'], 'verified', len(good), 'fail', len(fails), flush=True)
(HERE/'claude-k3-seed-check.json').write_text(json.dumps(summary, indent=1)+'\n')
(HERE/'claude-k3-verified-seeds.json').write_text(json.dumps(verified)+'\n')
