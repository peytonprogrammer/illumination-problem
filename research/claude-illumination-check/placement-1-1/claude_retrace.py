import json, sys
from pathlib import Path
sys.path[:0] = [str(Path(__file__).resolve().parents[1]), str(Path(__file__).resolve().parents[2])]
from claude_ray_guard_check import check_path
from illumination_paths import find_path
rows = json.loads(Path(__file__).with_name('claude-placement-1-1-traced.json').read_text())
marks = [(0, 0), (2, 2)]
for r in [r for r in rows if not r.get('verified')]:
    room = {tuple(sorted(tuple(v) for v in t)) for t in r['room']}
    w = find_path(dict(triangles=r['room'], marked=marks), int(sys.argv[1]), 3000)
    ok = w['status'] == 'illuminated' and check_path(room, w['path'], marks)[0]
    print(json.dumps(dict(cells=r['cells'], status=w['status'], verified=ok, direction=w.get('direction'),
                          bounces=w.get('bounces'), counts=w.get('counts'), triangles=len(r['room']))), flush=True)
    Path(__file__).with_name(f"unlit-{'_'.join(f'{a}{b}' for a, b in r['cells'])}.json").write_text(json.dumps(dict(triangles=r['room'], marked=marks, retrace=w))+'\n')
