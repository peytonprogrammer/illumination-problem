"""Independent checker for exhaustive fan partitions and verified DRAT leaves.
Does not import the encoder, SAT solver, its unit-propagator, or its fan table.
"""
from pathlib import Path
from collections import Counter
import hashlib,json,sys
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE.parent.parent));sys.path.insert(0,str(HERE/'inputs'))
from illumination_geometry import owners_of,check_fan_angles
stats=Counter();opens=[]

def digest(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()

def read_formula(p):
 clauses=[];nv=nc=None
 for line in p.read_text().splitlines():
  if not line or line.startswith('c'):continue
  if line.startswith('p'):
   _,kind,nv,nc=line.split();assert kind=='cnf';nv=int(nv);nc=int(nc);continue
  ints=list(map(int,line.split()));assert ints[-1]==0 and 0 not in ints[:-1];clauses.append(ints[:-1])
 assert nv is not None and len(clauses)==nc
 assert all(abs(l)<=nv for c in clauses for l in c)
 return clauses

def body(p):return p.read_bytes().split(b'\n',1)[1]

def legal_masks(folder,center,ring):
 variables={v:tuple(sorted(map(tuple,t))) for t,v in json.loads((folder/'tile-variables.json').read_text())}
 assert set(ring)=={v for v,t in variables.items() if center in t}
 tris=[variables[v] for v in ring];meta=json.loads((folder/'result.json').read_text());fulls={tuple(2*c for c in p) for p in meta['full']}
 isA=center[0]%2==center[1]%2==0;out=[]
 for mask in range(1<<len(tris)):
  ts=[t for i,t in enumerate(tris) if mask>>i&1];owners=owners_of(ts);opened={e for e,ids in owners.items() if len(ids)==2}
  angles,full=check_fan_angles(ts,center,owners,opened)
  if ts and not full and len(angles)!=1:continue
  if isA and full!=(center in fulls):continue
  out.append(mask)
 return out

def check_child_formula(parent,child,ring,mask,parentbody):
 units=''.join(f'{v if mask>>i&1 else -v} 0\n' for i,v in enumerate(ring)).encode()
 assert body(child/'formula.cnf')==parentbody+units,(str(child),'not exactly parent plus fan units')
 stats['child_extensions']+=1

def leaf(folder):
 v=json.loads((folder/'verification.json').read_text());assert v['status']=='VERIFIED'
 assert digest(folder/'formula.cnf')==v['formula_sha256']
 assert digest(folder/'proof.drat')==v['proof_sha256']
 assert v['connectivity_cuts_checked']==0
 stats['drat_leaves']+=1
 return True

def node(folder):
 if (folder/'verification.json').exists():return leaf(folder)
 if not (folder/'refinement.json').exists():opens.append(str(folder));return False
 clauses=read_formula(folder/'formula.cnf');trace=json.loads((folder/'unit-trace.json').read_text());values={}
 for lit,reason in trace['trace']:
  assert 0<=reason<len(clauses) and lit in clauses[reason]
  assert abs(lit) not in values
  assert all(abs(l) in values and values[abs(l)]!=(l>0) for l in clauses[reason] if l!=lit),(str(folder),'invalid unit reason')
  values[abs(lit)]=lit>0;stats['unit_reason_steps']+=1
 assert trace['conflict_clause'] is None
 r=json.loads((folder/'refinement.json').read_text());center=tuple(r['center']);ring=r['ring_variables']
 legal=legal_masks(folder,center,ring);assert legal==r['legal_masks']
 compatible=[m for m in legal if all(v not in values or values[v]==bool(m>>i&1) for i,v in enumerate(ring))]
 assert compatible==r['compatible_masks'] and compatible
 expected=[folder/'children'/f'mask{m}' for m in compatible]
 assert list(map(str,expected))==r['children']
 parentbody=body(folder/'formula.cnf');ok=True
 for child,m in zip(expected,compatible):
  check_child_formula(folder,child,ring,m,parentbody)
  if not node(child):ok=False
 stats['checked_partitions']+=1;stats['masks_excluded_by_verified_units']+=len(legal)-len(compatible)
 return ok

def root(folder):
 if (folder/'verification.json').exists():return leaf(folder),'DIRECT_DRAT'
 if not (folder/'split-manifest.json').exists():opens.append(str(folder));return False,'OPEN'
 m=json.loads((folder/'split-manifest.json').read_text());assert digest(folder/'formula.cnf')==m['base_sha256']
 center=tuple(m['center']);ring=m['ring_variables'];assert legal_masks(folder,center,ring)==m['masks']
 parentbody=body(folder/'formula.cnf');ok=True
 for mask in m['masks']:
  child=folder/'split'/f'mask{mask}';check_child_formula(folder,child,ring,mask,parentbody)
  if not node(child):ok=False
 stats['checked_partitions']+=1
 return ok,'EXHAUSTIVE_FAN_TREE'

if __name__=='__main__':
 provenance=HERE/'provenance'
 adopted=json.loads((provenance/'adopted.json').read_text());assert adopted['status']=='VERIFIED'
 assert digest(provenance/'source-input-lock.json')==adopted['source_input_lock_sha256']
 for item in json.loads((provenance/'source-input-lock.json').read_text()):
  assert digest(provenance/item['path'])==item['sha256'],item['path']
 for item in adopted['cases']:
  assert item['regeneration']=='BYTE_EXACT' and item['fresh_drat_check']
  assert digest(HERE/'cases'/item['tag']/'formula.cnf')==item['formula_sha256']
 stats['frozen_source_input_digests']=len(json.loads((provenance/'source-input-lock.json').read_text()))
 stats['byte_exact_regenerations']=len(adopted['cases'])
 cases=json.loads((HERE/'inputs/branch-support.json').read_text())['cases'];records=[]
 for c in cases:
  for i,pair in enumerate(c['mark_pairs']):
   tag=f'{c["tag"]}-pair{i}';ok,kind=root(HERE/'cases'/tag);records.append(dict(tag=tag,status='VERIFIED' if ok else 'OPEN',kind=kind))
   print(tag,records[-1]['status'],flush=True)
 out=dict(status='VERIFIED' if all(r['status']=='VERIFIED' for r in records) else 'INCOMPLETE',expected=31,verified=sum(r['status']=='VERIFIED' for r in records),cases=records,checks=dict(stats),open_nodes=opens)
 (HERE/'compose-check.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ('cases','open_nodes')},indent=2),flush=True)
