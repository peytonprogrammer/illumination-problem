"""Independent polygon replay and exact universal implication of saved guards.
This never invokes the orbit classifier or discovers directions.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter,defaultdict
import importlib.util,json,hashlib,sys,time,shutil
ROOT=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('audit',ROOT.parent/'persisted-replay/audit.py');a=importlib.util.module_from_spec(sp);sp.loader.exec_module(a)

def sub(x,y):return (x[0]-y[0],x[1]-y[1])
def cross(x,y):return x[0]*y[1]-x[1]*y[0]
def dot(x,y):return x[0]*y[0]+x[1]*y[1]
def polygon(room):
 counts=Counter(tuple(sorted((t[i],t[(i+1)%3]))) for t in room for i in range(3))
 edges=[e for e,n in counts.items() if n==1];adj=defaultdict(list)
 for x,y in edges:adj[x].append(y);adj[y].append(x)
 assert all(len(v)==2 for v in adj.values())
 start=min(adj);cycle=[start];prev=None;cur=start
 while True:
  nxt=next(v for v in adj[cur] if v!=prev)
  if nxt==start:break
  cycle.append(nxt);prev,cur=cur,nxt;assert len(cycle)<=len(adj)
 assert len(cycle)==len(adj)
 corners={z for i,z in enumerate(cycle) if cross(sub(z,cycle[i-1]),sub(cycle[(i+1)%len(cycle)],z))!=0}
 return edges,corners

def physical(path,room):
 edges,corners=polygon(room);checks=0
 def inside(p):
  n=0
  for x,y in edges:
   d=cross(sub(y,x),sub(p,x))
   assert not(d==0 and min(x[0],y[0])<=p[0]<=max(x[0],y[0]) and min(x[1],y[1])<=p[1]<=max(x[1],y[1]))
   # Need oriented edges: use parity crossing, independent of their storage order.
   if (x[1]>p[1])!=(y[1]>p[1]):
    crossing=x[0]+(p[1]-x[1])*(y[0]-x[0])/(y[1]-x[1])
    if p[0]<crossing:n^=1
  return n==1
 assert inside(path[0]) and inside(path[-1])
 for x,y in zip(path,path[1:]):
  d=sub(y,x);assert d!=(0,0)
  for u,v in edges:
   e=sub(v,u);den=cross(d,e)
   if den:
    t=cross(sub(u,x),e)/den;s=cross(sub(u,x),d)/den
    assert not(0<t<1 and 0<=s<=1),('segment boundary hit',x,y,u,v)
   elif cross(sub(u,x),d)==0:
    j=0 if d[0] else 1;lo,hi=sorted(((u[j]-x[j])/d[j],(v[j]-x[j])/d[j]))
    assert max(lo,F(0))>=min(hi,F(1)),('wall gliding',x,y)
   checks+=1
  assert inside(tuple((x[k]+y[k])/2 for k in (0,1)))
 for prev,z,nxt in zip(path,path[1:],path[2:]):
  assert z not in corners,('corner bounce',z)
  tangents=set()
  for u,v in edges:
   e=sub(v,u)
   if cross(e,sub(z,u))==0 and min(u[0],v[0])<=z[0]<=max(u[0],v[0]) and min(u[1],v[1])<=z[1]<=max(u[1],v[1]):
    tangents.add((1,0) if e[1]==0 else (0,1) if e[0]==0 else (1,1) if e[0]*e[1]>0 else (1,-1))
  assert len(tangents)==1,(z,tangents)
  e=tangents.pop();d=sub(z,prev);out=sub(nxt,z);ref=tuple(2*dot(d,e)*e[k]-dot(e,e)*d[k] for k in (0,1))
  assert cross(ref,out)==0 and dot(ref,out)>0 and cross(e,sub(prev,z))*cross(e,sub(nxt,z))>0
 return checks

def peer():
 sp=importlib.util.spec_from_file_location('continuation',ROOT/'run.py');r=importlib.util.module_from_spec(sp);sp.loader.exec_module(r)
 source=ROOT.parent.parent/'claude-illumination-check/k5-residual'
 shutil.copy2(source/'classified.json',ROOT/'inputs/peer-classified.json');shutil.copy2(source/'packet-hashes.txt',ROOT/'inputs/peer-packet-hashes.txt')
 hashes=dict(line.split() for line in (ROOT/'inputs/peer-packet-hashes.txt').read_text().splitlines() if line.strip())
 records=json.loads((ROOT/'inputs/peer-classified.json').read_text());summary=json.loads((r.PILOT/'pass-summary.json').read_text());out=[];guards=[]
 for case in summary['results']:
  if case['status']!='RESIDUAL':continue
  folder=r.PILOT/'cases'/case['tag'];packet=json.loads((folder/'vertices.json').read_text());key=case['tag']+':'+json.dumps(packet['vertices']);record=records[key]
  assert hashes[case['tag']]==hashlib.sha256((folder/'vertices.json').read_bytes()).hexdigest()
  assert record['decider']=='LIT' and record['path'];path=tuple(tuple(map(F,z)) for z in record['path']['points']);room=json.loads((folder/'residual-room.json').read_text())['room']
  assert path[0]==tuple(room['marked'][0]) and path[-1]==tuple(room['marked'][1])
  checks=physical(path,a.triangles(room['triangles']));guard,receipt=r.normalized_guard(path,room,case['tag'],'peer-first-pass')
  guards.append(guard);out.append(dict(tag=case['tag'],physical_wall_checks=checks,reflections=len(path)-2,vertex_sha256=hashlib.sha256((folder/'vertices.json').read_bytes()).hexdigest(),receipt=receipt))
 write(ROOT/'peer-guards.json',guards);write(ROOT/'peer-check.json',dict(status='PASS',checked=len(out),results=out));print('peer paths PASS',len(out),flush=True)

def write(path,data):path.write_text(json.dumps(data,indent=2)+'\n')
def learned(limit=None):
 start=time.monotonic();raw=(ROOT/'learned.jsonl').read_text();lines=raw.splitlines()
 if not raw.endswith('\n'):lines=lines[:-1]
 if limit is not None:lines=lines[:limit]
 checks=0;reflections=0;vertex_bounces=0;max_bounces=0;offset=0
 prior_path=ROOT/'guards-audit.json'
 if prior_path.exists():
  prior=json.loads(prior_path.read_text());n=prior['checked']
  if n<=len(lines):
   assert hashlib.sha256(('\n'.join(lines[:n])+'\n').encode()).hexdigest()==prior['prefix_sha256']
   offset=n;checks=prior['segment_wall_checks'];reflections=prior['reflections'];vertex_bounces=prior['smooth_vertex_bounces'];max_bounces=prior['max_reflections']
 for i,line in enumerate(lines[offset:],start=offset):
  rec=json.loads(line);receipt=a.check_record(rec,tuple(rec['q']),True)
  path=tuple(tuple(F(*c) for c in z) for z in rec['path']);checks+=physical(path,a.triangles(rec['room']))
  reflections+=len(path)-2;max_bounces=max(max_bounces,len(path)-2);vertex_bounces+=receipt['vertex_bounces']
  gen=ROOT/'cases'/rec['source_case']/'generations'/str(rec['generation']);assert json.loads((gen/'guard.json').read_text())==rec
  if (i+1)%100==0:print('checked',i+1,'wall incidences',checks,flush=True)
 out=dict(status='PASS',checked=len(lines),prefix_sha256=hashlib.sha256(('\n'.join(lines)+'\n').encode()).hexdigest(),segment_wall_checks=checks,reflections=reflections,max_reflections=max_bounces,smooth_vertex_bounces=vertex_bounces,seconds=round(time.monotonic()-start,3),scope='Saved guard exact implication and independent physical polygon replay; no orbit or direction search.')
 write(ROOT/'guards-audit.json',out);print(json.dumps(out),flush=True)
if __name__=='__main__':
 if len(sys.argv)>1 and sys.argv[1]=='peer':peer()
 else:learned(int(sys.argv[1]) if len(sys.argv)>1 else None)
