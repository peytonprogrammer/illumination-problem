"""Trace every open-leaf room with Codex's tracer (search only), then verify each found path
with Claude's exact checker. Usage: claude_trace_open.py claude-placement-X-Y.json [bound]"""
import json, sys
from pathlib import Path
sys.path[:0] = [str(Path(__file__).resolve().parents[1]), str(Path(__file__).resolve().parents[2])]
from claude_ray_guard_check import check_path
from illumination_paths import find_path
src = Path(sys.argv[1]); bound = int(sys.argv[2]) if len(sys.argv) > 2 else 12
d = json.loads(src.read_text()); tgt = d.get('monolithic', {}).get('target') or [int(v) for v in src.stem.split('-')[-2:]]
marks = [(0, 0), (2*tgt[0], 2*tgt[1])]
rows = []
for leaf in d['open']:
    if not leaf.get('room'):
        rows.append(dict(cells=leaf['cells'], status=leaf['status'], traced=None)); continue
    room = {tuple(sorted(tuple(v) for v in t)) for t in leaf['room']}
    w = find_path(dict(triangles=leaf['room'], marked=marks), bound)
    ok = w['status'] == 'illuminated' and check_path(room, w['path'], marks)[0]
    rows.append(dict(cells=leaf['cells'], traced=w['status'], verified=ok, direction=w.get('direction'),
                     bounces=w.get('bounces'), path=w.get('path'), room=leaf['room']))
    print(json.dumps({k: v for k, v in rows[-1].items() if k not in ('path', 'room')}), flush=True)
lit = sum(1 for r in rows if r.get('verified'))
print(json.dumps(dict(open=len(rows), lit=lit, unlit=len(rows)-lit)))
src.with_name(src.stem + '-traced.json').write_text(json.dumps(rows, indent=1) + '\n')
