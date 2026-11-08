"""Read-only audit of the existing fixed 22-wall certificate; no orbit search."""
from pathlib import Path
from collections import Counter
import gzip,hashlib,json,time
start=time.monotonic()
root=Path(__file__).resolve().parents[2]
p=root/'illumination-generalization-2026-11-06/review/marked-origami-known22-closure.gz'
raw=gzip.decompress(p.read_bytes());n=60
assert hashlib.sha256(raw).hexdigest()=='2f5540623e3d0a7c08b2d1bbe4487d607e9024cef82263de175c30bec7b7a346'
assert len(raw)%(3*n)==0
stats=Counter();profiles=Counter();regular_contacts=Counter()
for off in range(0,len(raw),3*n):
 h,v,labels=[raw[off+i*n:off+(i+1)*n] for i in range(3)]
 assert sorted(h)==sorted(v)==list(range(n))
 hi=[0]*n;vi=[0]*n
 for i in range(n):hi[h[i]]=i;vi[v[i]]=i
 k=[v[h[vi[hi[i]]]] for i in range(n)]
 sizes=[0]*n;seen=set();cycle_sizes=[]
 for i in range(n):
  if i in seen:continue
  cyc=[];j=i
  while j not in seen:seen.add(j);cyc.append(j);j=k[j]
  assert j==i
  cycle_sizes.append(len(cyc))
  for a in cyc:sizes[a]=len(cyc)
 assert Counter(cycle_sizes)==Counter({1:33,3:9})
 assert all(labels[i]==3 for i in range(n) if sizes[i]>1)
 assert Counter(labels)==Counter({3:40,0:12,1:4,2:4})
 a=h[0];steps=1;regular=0
 while a!=0:
  assert labels[a]!=2, 'A target was reached after removing only regular-corner stops'
  if sizes[a]>1:
   stats['stops_at_true_zero']+=1;break
  if labels[a]==3:regular+=1
  a=h[a];steps+=1
 else:stats['returns_to_source_without_true_zero']+=1
 regular_contacts[regular]+=1
 profiles[tuple(sorted(cycle_sizes))]+=1
stats['states']=len(raw)//(3*n)
out={'status':'FIXED_NEGATIVE_CERTIFICATE_TRUE_ZERO_AUDIT_PASS','certificate':str(p),'raw_sha256':hashlib.sha256(raw).hexdigest(),'counts':dict(stats),'surface':{'squares':60,'genus':10,'true_zeros':9,'zero_orders':[2]*9,'regular_vertices':33,'convex_corner_lifts':13,'source_lifts':4,'target_lifts':4,'other_regular_vertices':12},'regular_corner_contacts_before_stop':dict(sorted(regular_contacts.items())),'seconds':time.monotonic()-start,'new_discovery':False,'limitations':'One existing 22-wall control only. No lower bound, no smaller-room exclusion, no independent audit of original geometry or full SL2 closure.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
