"""Reconcile the historical and new disjoint pair classes and recheck the area-21 seal."""
from collections import Counter
from hashlib import sha256
from pathlib import Path
import json

d9=Path('../../d9-census-w22')
phase=json.loads((d9/'census_totals.json').read_text())['per_W_area']
old_same=Counter()
for key,row in phase.items():
    w,a=map(int,key.split(','))
    if w<=20:
        assert row['pairs']==row['lit_by_shooting']
        old_same[a,w]+=row['pairs']
old_diff=Counter()
for line in (d9/'partA-totals.md').read_text().splitlines():
    v=[s.strip().replace(',','') for s in line.strip('|').split('|')]
    if len(v)!=19 or not v[0].isdigit(): continue
    w,a=map(int,v[:2])
    if w<=20:
        assert int(v[9])==int(v[10])==old_same[a,w]
        assert int(v[11])==int(v[12])
        old_diff[a,w]=int(v[11])

backfill=0
for a in range(17,21):
    result=json.loads(Path(f'a{a}/totals.json').read_text())
    assert result['same_pairs_tested']==0 and result['dark']==0
    backfill+=result['different_pairs']
    if a==20:
        all20=Counter()
        for file in Path('../validation').glob('[0-9]*.counts'):
            for line in file.read_text().splitlines():
                v=line.split()
                if v[0]=='EXPECT': all20[int(v[2])]+=int(v[3])
        for w in range(4,21,2):
            assert old_same[20,w]+result['different_pairs_by_w'].get(str(w),0)==all20[w]
root=Path('../a21')
prod=json.loads((root/'totals.json').read_text())
manifest=json.loads((root/'manifest.json').read_text())
twentyone=Counter()
for i in range(manifest['shards']):
    record=json.loads((root/f'{i}.done.json').read_text())
    assert record['counts_sha256']==sha256((root/f'{i}.counts').read_bytes()).hexdigest()
    for k in ('rooms','same_pairs','different_pairs','survivors'):
        twentyone[k]+=record[k]
for k,n in twentyone.items(): assert prod[k]==n
assert twentyone['survivors']==0
tot=sum(old_same.values())+sum(old_diff.values())+backfill+twentyone['same_pairs']+twentyone['different_pairs']
r=dict(same_through20=sum(old_same.values()),diff_through16=sum(old_diff.values()),different_17_20=backfill,all_at21=twentyone['same_pairs']+twentyone['different_pairs'],all_through21=tot)
Path('summary.json').write_text(json.dumps(r,indent=2)+'\n')
status=Path('../../../../../qclass-closure/bbbb/census-a21-status.md')
s=status.read_text()
if '## Contiguous L2 coverage' not in s:
    status.write_text(s+f'\n## Contiguous L2 coverage\n\n[done] All {backfill:,} different-parity pairs at exact areas 17–20 passed. Area 20 also reconciled by wall bucket against the independent all-pair counts from validation after adding the historical same-parity totals. After area 20 we rechecked all 84 area-21 shard seals and totals; its completed all-pair result was reused. Combining the disjoint classes in [the backfill summary](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d205-census-a21/parity-gap/summary.json) certifies **{tot:,} lit interior lattice pairs through area 21** for strictly simple orthogonal lattice rooms with W ≤ 20. The first open area for L2 is **22**.\n')
print(r)
