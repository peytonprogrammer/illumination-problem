"""Bounded local mutations: does the sheet certificate admit transparency?"""
import itertools,json,time
from pathlib import Path
from illumination_geometry import patch,check,save,owners_of
from illumination_cover import build,D4,mat
from illumination_cover_certificate import certify,relation
base=Path(__file__).parent;started=time.monotonic();stats={};successes=[];comparisons=[]
for name in ['illumination-20','illumination-22','illumination-search-simple-unrestricted']:
 d=json.loads((base/(name+'.json')).read_text());ts={tuple(sorted(map(tuple,t))) for t in d['triangles']};pts=[p for t in ts for p in t];legal=set(patch(min(p[0] for p in pts)-1,max(p[0] for p in pts)+1,min(p[1] for p in pts)-1,max(p[1] for p in pts)+1));owners=owners_of(sorted(legal));near={t for t in legal if t in ts or any(len(set(t)&set(u))==2 for u in ts)};counts=dict(tried=0,valid_transparent=0,certified=0,parity_equivalent=0)
 for size in (1,2):
  for flips in itertools.combinations(sorted(near),size):
   if time.monotonic()-started>50:break
   changed=ts^set(flips);data=dict(d,triangles=sorted(changed));counts['tried']+=1
   try:r=check(data,strict=False)
   except (AssertionError,ValueError,KeyError):continue
   if not r['transparent_vertices']:continue
   counts['valid_transparent']+=1;c=build(data);R,count=relation(c['H'],c['V']);parities=[]
   for pair in c['states']:
    g,i=pair[0];points=[mat(D4[g],p) for p in c['triangles'][i]];parities.append(tuple(min(p[k] for p in points)%2 for k in (0,1)))
   equiv=all(bool(R[i]>>j&1)==(tuple(a^b for a,b in zip(parities[i],parities[j]))!=(1,1)) for i in range(len(R)) for j in range(len(R)))
   counts['parity_equivalent']+=int(equiv);result=certify(data,True)
   if result['status']=='DARK':
    counts['certified']+=1;path=base/f'cover-transparent-dark-{len(successes)+1}.json';save(path,data);save(path.with_name(path.stem+'-certificate.json'),result);successes.append(dict(file=path.name,walls=r['walls'],transparent=r['transparent_vertices']))
  if time.monotonic()-started>50:break
 stats[name]=counts
 if time.monotonic()-started>50:break
result=dict(status='complete_bounded_pilot',seconds=time.monotonic()-started,stats=stats,certified_transparent=successes,time_cap=50,scope='One/two tile flips in original rooms and immediate edge neighbors; independent of prior smaller-room searches. Noncertification is not illumination.')
save(base/'cover-mutation-probe.json',result);print(json.dumps(result))
