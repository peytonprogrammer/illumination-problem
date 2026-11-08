"""Local root/single-remote interface templates; no completed rooms or caps."""
from pathlib import Path
import json,hashlib
HERE=Path(__file__).resolve().parent;BASE=HERE.parent
src=BASE/'surplus-four-local/R23-top6-search/verify.py';e={'__file__':str(src)}
exec(compile(src.read_text().split('\ndef path(d,nine):')[0],str(src),'exec'),e)
fan,H=e['fan'],e['H'];C=e['C']
def edges(ts):return {tuple(sorted((a,b)))for t in ts for a,b in zip(t,t[1:]+t[:1])}
def angle(ts,p):
 return sum(90 if e['dot'](*[e['sub'](v,p)for v in t if v!=p])==0 else 45 for t in ts if p in t)
HA=[(0,0),(2,0),(2,2)];Hedges={a:edges(fan(a,range(8)))for a in HA}
Kedges={k:edges(fan(k,range(8)))for k in C};known=set(HA)|set(C.values())
refs={'L':0,'B':1,'E':4,'Tc':5};rows=[]
for parent,p in C.items():
 for m in (3,4):
  for start in range(8):
   ss=[(start+j)%8 for j in range(m)]
   if parent in refs and refs[parent]not in ss:continue
   if parent=='N'and{6,7}<=set(ss):continue
   f=fan(parent,ss);ef=edges(f);Hs=[a for a,es in Hedges.items()if es&ef]
   if len(Hs)!=1:continue
   for dx,dy in [(2,0),(-2,0),(0,2),(0,-2)]:
    remote=(p[0]+dx,p[1]+dy)
    if remote in known:continue
    for i in range(8):
     leaf=fan(remote,[i]);shared=ef&edges(leaf)
     if not shared:continue
     assert len(shared)==1
     edge=next(iter(shared));c=next(v for v in edge if not(v[0]%2 and v[1]%2))
     assert angle(leaf,c)==90 and angle(f,c)in(90,180)
     if angle(f,c)!=180:continue
     local_contacts={k:sorted(ef&es)for k,es in Kedges.items()if k!=parent and ef&es}
     assert not local_contacts,(parent,ss,remote,i,local_contacts)
     other_remote_sides=[]
     for qdx,qdy in [(2,0),(-2,0),(0,2),(0,-2)]:
      q=(p[0]+qdx,p[1]+qdy)
      if q in known or q==remote:continue
      se=ef&edges(fan(q,range(8)))
      if se:other_remote_sides.append({'center':q,'BCedges':sorted(se)})
     rows.append({'parent':parent,'parent_sectors':ss,'m':m,'remote_center':remote,'remote_sector':i,'interface':edge,'shared_C':c,'parent_C_angle':180,'leaf_C_angle':90,'H_neighbors':Hs,'other_local_K_BCcontacts':local_contacts,'unoccupied_other_remote_sides':other_remote_sides})
counts={k:sum(r['parent']==k for r in rows)for k in C}
assert len(rows)==44 and counts=={'L':8,'B':2,'D':6,'R':6,'E':2,'Tc':8,'N':12},counts
out={'status':'PARENT_LOCAL_INTERFACE44_CHECK_NOT_FULL_ROW_CLASSIFICATION','counts':counts,'templates':rows,'extra_local_unit_root_reason':'EachretainedparenthasNOBCedgewithanyotherKpartialcell. A locald0unitwouldneedparentedge(ordinarycapsdonottransmit),impossible;thereforeextraunitHroot. ThirdBCsidescanexistbutalwaysleadtoanotherremotecell,excludedbysoleremote hypothesis.','limits':'Necessaryactiveparent/leaflocaltemplatesonly;criticalreferenceforcing/rootleafproof andbudget/ordinaryopticalcover remainseparatehandobligations. Not44validrooms/census/capassignments; nocomplete roomconstructed.','source_sha256':{str(p.relative_to(BASE)):hashlib.sha256(p.read_bytes()).hexdigest()for p in[src,Path(__file__),BASE/'fourth-surplus-review/structural-reduction.txt']}}
(HERE/'parent-templates.json').write_text(json.dumps(out,indent=2)+'\n')
print(out['status'],counts,'ALL44nootherKBCcontact')
for k in ['L','B','D','N']:
 print(k,[(r['parent_sectors'],r['remote_center'],r['remote_sector'])for r in rows if r['parent']==k])
