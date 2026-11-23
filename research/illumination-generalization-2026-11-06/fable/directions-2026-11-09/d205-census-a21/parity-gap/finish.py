from collections import Counter
from pathlib import Path
from hashlib import sha256
import json
import sys

area=int(sys.argv[1])
folder=Path(f'a{area}')
manifest=json.loads((folder/'manifest.json').read_text())
assert manifest['nice']>=10 and manifest['area']==area
assert manifest['binary']==json.loads(Path('validation.json').read_text())['binary']
rooms=Counter(); by_wall=Counter(); historical=Counter(); metrics=Counter()
peak=0
for i in range(manifest['shards']):
    f=folder/f'{i}.counts'
    record=json.loads((folder/f'{i}.done.json').read_text())
    assert record['shard']==i and record['counts_sha256']==sha256(f.read_bytes()).hexdigest()
    assert record['same_pairs']==0
    for k in ('eligible','rooms','different_pairs','survivors','cpu_s'):
        metrics[k]+=record[k]
    peak=max(peak,record['peak_rss_bytes'])
    for line in f.read_text().splitlines():
        v=line.split()
        if v[:2]==['#','count']: rooms[int(v[5])]+=int(v[7])
        if v[0]=='SHOT': by_wall[int(v[2])]+=int(v[5])
for f in Path('../../d9-census-w22/runs/a20').glob('job-*.counts'):
    for line in f.read_text().splitlines():
        v=line.split()
        if v[:2]==['#','count'] and int(v[3])==area and int(v[5])<=20:
            historical[int(v[5])]+=int(v[7])
assert rooms==historical and sum(rooms.values())==metrics['rooms']
assert sum(by_wall.values())==metrics['different_pairs']
assert not (folder/'DARK.json').exists()
if metrics['survivors']:
    assert (folder/'orbits.log').read_text().count(' LIT\n')==metrics['survivors']
wall=max(f.stat().st_mtime for f in folder.glob('*.done.json'))-(folder/'manifest.json').stat().st_mtime
data=dict(metrics,peak_rss_bytes=peak,wall_s=wall,dark=0,same_pairs_tested=0,rooms_by_w=dict(rooms),different_pairs_by_w=dict(by_wall))
(folder/'totals.json').write_text(json.dumps(data,indent=2)+'\n')
status=Path('../../../../../qclass-closure/bbbb/census-a21-status.md')
assert status.exists()
s=status.read_text()
if '## Different-parity backfill' not in s:
    s+='\n## Different-parity backfill\n\nThe parity-only filter reproduced all 3,483 different-parity pairs through area 11 with zero same-parity tests. The control-validated orbit binary and independent plane replay are unchanged. Each row below was added after its shards reconciled against the archived room counts by wall count.\n\n| Exact area | Canonical rooms | Rooms with different-parity pairs | Different-parity pairs lit | Orbit referrals | DARK | Worker CPU seconds |\n|---:|---:|---:|---:|---:|---:|---:|\n'
row=f"| {area} | {metrics['rooms']:,} | {metrics['eligible']:,} | {metrics['different_pairs']:,} | {metrics['survivors']} | 0 | {metrics['cpu_s']:.2f} |\n"
if row not in s: status.write_text(s+row)
print(json.dumps(data))
