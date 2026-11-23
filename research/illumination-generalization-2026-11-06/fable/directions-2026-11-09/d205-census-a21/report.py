"""Aggregate sealed shards only; estimate area 22 from observed work at 20 and 21."""
from collections import Counter
from pathlib import Path
import hashlib
import json
import math
import statistics

root=Path(__file__).resolve().parent
folder=root/'a21'
manifest=json.loads((folder/'manifest.json').read_text())
assert manifest['shards']==84
records=[json.loads((folder/f'{i}.done.json').read_text()) for i in range(84)]
ver=json.loads((root/'validation/PASS.json').read_text())
rows=Counter();same=Counter();diff=Counter();surv=Counter();eligible=Counter()
fixed=Counter()
for i,record in enumerate(records):
    f=folder/f'{i}.counts'
    assert i==record['shard'] and hashlib.sha256(f.read_bytes()).hexdigest()==record['counts_sha256']
    for line in f.read_text().splitlines():
        v=line.split()
        if v[:2]==['#','fixed']: fixed[int(v[3])]+=int(v[4])
        if v[:2]==['#','count']:
            assert int(v[3])==21
            w=int(v[5]); rows[w]+=int(v[7]); eligible[w]+=int(v[9])
        if v[0]=='SHOT':
            a,w,e,s,d,u=map(int,v[1:]); assert a==21
            same[w]+=s;diff[w]+=d;surv[w]+=u
    assert len((folder/f'{i}.sv').read_text().splitlines())==record['survivors']
assert fixed[20]==ver['area20_fixed']
tot={key:sum(d[key] for d in records) for key in ('rooms','eligible','same_pairs','different_pairs','survivors','cpu_s','orbit_cpu_s')}
assert (sum(rows.values()),sum(same.values()),sum(diff.values()),sum(surv.values()))==(tot['rooms'],tot['same_pairs'],tot['different_pairs'],tot['survivors'])
if tot['survivors']:
    orbit_text=(folder/'orbits.log').read_text()
    assert orbit_text.count(' LIT\n')==tot['survivors'] and ' DARK' not in orbit_text
assert not (folder/'DARK.json').exists()
val=[json.loads((root/'validation'/f'{i}.done.json').read_text()) for i in range(28)]
# Use root-to-limit node totals because both workers traversed their prefixes.
node_ratio=sum(fixed.values())/(sum(fixed.values())-fixed[21])
room_ratio=tot['rooms']/ver['area20_rooms']
pairs20=sum(int(l.split()[3]) for i in range(28) for l in (root/'validation'/f'{i}.counts').read_text().splitlines() if l.startswith('EXPECT '))
pair_ratio=(tot['same_pairs']+tot['different_pairs'])/pairs20
enum20=sum(d['cpu_s'] for d in val)
cpu=tot['cpu_s']; enum21=min(cpu,enum20*node_ratio); pair21=cpu-enum21
forecast=enum21*node_ratio+pair21*pair_ratio
lo=cpu*min(room_ratio,node_ratio,pair_ratio);hi=cpu*max(room_ratio,node_ratio,pair_ratio)
wall=max((folder/f'{i}.done.json').stat().st_mtime for i in range(84))-(folder/'manifest.json').stat().st_mtime
peak=max(d['peak_rss_bytes'] for d in records)
report={**tot,'by_W':{w:dict(rooms=rows[w],eligible=eligible[w],same=same[w],different=diff[w],orbit_pairs=surv[w]) for w in sorted(rows)},'fixed':dict(fixed),'wall_s':wall,'max_worker_rss_bytes':peak,'shard_cpu_s_min_median_max':[min(d['cpu_s'] for d in records),statistics.median(d['cpu_s'] for d in records),max(d['cpu_s'] for d in records)],'forecast22':dict(node_ratio=node_ratio,room_ratio=room_ratio,pair_ratio=pair_ratio,pairs20=pairs20,enum_cpu20=enum20,modeled_enum_cpu21=enum21,modeled_pair_cpu21=pair21,cpu_s=forecast,sensitivity_cpu_s=[lo,hi],wall_s=forecast*wall/cpu)}
(folder/'totals.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report))
