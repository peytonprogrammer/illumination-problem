"""Run Claude's exact ray-guard checker over every saved guard in the frozen I=2/k=3 inputs."""
import hashlib, json, re, sys
from pathlib import Path
HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent)); sys.path.insert(0, str(HERE))
from claude_ray_guard_check import cell_tiles, check_path
from claude_two_star_k3_geometry import support

def guards(x):
    if isinstance(x, dict):
        if 'tile_facts' in x and 'witness' in x and 'room' in x:
            yield x
        for v in x.values():
            yield from guards(v)
    elif isinstance(x, list):
        for v in x:
            yield from guards(v)

def digests(x):
    if isinstance(x, dict):
        for k, v in x.items():
            if k == 'triangle_index_sha256' and isinstance(v, str): yield v
            else: yield from digests(v)
    elif isinstance(x, list):
        for v in x: yield from digests(v)

norm = lambda tri: {tuple(sorted(tuple(v) for v in t)) for t in tri}
report, total, fails = {}, 0, []
for f in sorted((HERE/__import__('os').environ.get('CLAUDE_INPUTS','inputs')).glob('three-*/*.json')):
    m = re.search(r'(\d)-(\d)', f.name)
    if not m: continue
    tgt = (int(m[1]), int(m[2]))
    data = json.loads(f.read_text())
    gs = list(guards(data))
    if not gs: continue
    full, allowed, r = support(tgt)
    ts = sorted({t for c in allowed for t in cell_tiles(*c)})
    index = {t: i for i, t in enumerate(ts)}
    dg = hashlib.sha256(json.dumps([[list(v) for v in t] for t in ts]).encode()).hexdigest()
    recorded = set(digests(data))
    marks = [(0, 0), (2*tgt[0], 2*tgt[1])]
    nf = 0
    for g in gs:
        room = norm(g['room']['triangles'])
        ok, why, touched = check_path(room, g['witness']['path'], marks)
        facts = {i: v for i, v in g['tile_facts']}
        bad = (not ok or not room <= set(ts)
               or any(t in index and facts.get(index[t]) != int(t in room) for t in touched)
               or any(t not in index and t in room for t in touched)
               or any(i >= len(ts) or v != int(ts[i] in room) for i, v in facts.items()))
        if bad:
            nf += 1; fails.append(dict(file=str(f.relative_to(HERE/__import__('os').environ.get('CLAUDE_INPUTS','inputs'))), why=why))
    report[str(f.relative_to(HERE/__import__('os').environ.get('CLAUDE_INPUTS','inputs')))] = dict(guards=len(gs), failures=nf, digest_recorded=sorted(recorded), digest_match=dg in recorded if recorded else None)
    total += len(gs)
    print(f.name, len(gs), 'fail', nf, 'digest', report[str(f.relative_to(HERE/__import__('os').environ.get('CLAUDE_INPUTS','inputs')))]['digest_match'], flush=True)
out = dict(status='PASS' if not fails else 'FAIL', total=total, files=report, failures=fails[:50])
(HERE/('claude-k3-guard-check-'+__import__('os').environ.get('CLAUDE_INPUTS','inputs')+'.json')).write_text(json.dumps(out, indent=1)+'\n')
print(out['status'], total, len(fails))
