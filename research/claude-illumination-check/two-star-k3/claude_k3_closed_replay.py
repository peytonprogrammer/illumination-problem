"""Replay one Codex-closed I=2/k=3 placement in Claude's relaxed model, using only verified cuts."""
import json, sys
from pathlib import Path
HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent)); sys.path.insert(0, str(HERE)); sys.path.insert(0, str(HERE.parent/'three-star'))
from claude_two_star_k3_geometry import support
from claude_three_star_replay import build

def guards(x):
    if isinstance(x, dict):
        if 'tile_facts' in x and 'witness' in x and 'room' in x: yield x
        for v in x.values(): yield from guards(v)
    elif isinstance(x, list):
        for v in x: yield from guards(v)

if __name__ == '__main__':
    tgt = (int(sys.argv[1]), int(sys.argv[2]))
    full, allowed, r = support(tgt)
    cuts = set()
    for f in (HERE/'inputs').glob(f'three-*/*{tgt[0]}-{tgt[1]}*.json'):
        for g in guards(json.loads(f.read_text())):
            cuts.add(tuple(sorted(map(tuple, g['tile_facts']))))
    _, res = build(full, allowed, [list(c) for c in cuts])
    print(json.dumps(dict(target=tgt, cuts=len(cuts), status=res['status'], walls=res.get('walls'))), flush=True)
    if 'room' in res:
        (HERE/f'survivor-{tgt[0]}-{tgt[1]}.json').write_text(json.dumps(res['room'])+'\n')
