"""Analyze quotients and symbolic paths of a saved finite proof; no ray search."""
from pathlib import Path
from collections import Counter,defaultdict
import json
HERE=Path(__file__).resolve().parent

def partition(n,pairs,perms):
 parent=list(range(n))
 def root(i):
  while parent[i]!=i:parent[i]=parent[parent[i]];i=parent[i]
  return i
 queue=list(pairs)
 while queue:
  i,j=queue.pop();i,j=root(i),root(j)
  if i==j:continue
  parent[i]=j
  queue.extend((p[i],p[j]) for p in perms)
 groups=defaultdict(list)
 for i in range(n):groups[root(i)].append(i)
 return tuple(sorted(tuple(g) for g in groups.values()))

if __name__=='__main__':
 raw=json.loads((HERE/'independent-orbit-certificate.json').read_text())
 initial=raw['independent_initial'];r,u,lab=initial['r'],initial['u'],initial['label'];n=len(r)
 blocks=sorted({partition(n,[(0,j)],[r,u]) for j in range(1,n)},key=lambda b:(len(b),b))
 quotients=[]
 for groups in blocks:
  index={x:i for i,g in enumerate(groups) for x in g}
  qr=[index[r[g[0]]] for g in groups];qu=[index[u[g[0]]] for g in groups]
  vertices=partition(len(groups),[(qu[qr[i]],qr[qu[i]]) for i in range(len(groups))],[])
  colors=[]
  for vertex in vertices:
   colors.append(''.join(sorted({lab[x] for j in vertex for x in groups[j]})))
  quotients.append(dict(squares=len(groups),block_size=len(groups[0]),vertex_colors=dict(Counter(colors)),groups=groups))
 patterns=Counter();steps=Counter();mixed=0
 for state in raw['states']:
  r0=state['r'];labels=state['label']
  for i,c in enumerate(labels):
   if c!='S':continue
   j=r0[i];seen={i};word='S'
   while j not in seen:
    word+=labels[j];seen.add(j)
    if labels[j] in 'BT':break
    j=r0[j]
   else:word+='(loop)'
   patterns[word]+=1;steps[len(seen)-1]+=1
 result=dict(quotients=quotients,source_symbolic_patterns=dict(sorted(patterns.items())),source_step_counts=dict(steps),scope='Saved-certificate algebra only; no new directions or billiard trajectories.')
 (HERE/'proof-compression.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({**result,'quotients':[{k:v for k,v in q.items() if k!='groups'} for q in quotients]},indent=2))

 # A geometric covering quotient must mark only universally blocked fibers as B.
 # Mixed fibers become clear; source/target fibers become overapproximations.
 import importlib.util
 spec=importlib.util.spec_from_file_location('verifier',HERE/'closed-orbit-audit.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
 from collections import deque
 q=next(q for q in quotients if q['squares']==20);groups=q['groups'];idx={x:i for i,g in enumerate(groups) for x in g}
 qr=[idx[r[g[0]]] for g in groups];qu=[idx[u[g[0]]] for g in groups]
 vertex_groups=partition(20,[(qu[qr[i]],qr[qu[i]]) for i in range(20)],[])
 qlab=['?']*20
 for vg in vertex_groups:
  colors={lab[x] for j in vg for x in groups[j]}
  assert not {'S','T'} <= colors
  c='S' if 'S' in colors else 'T' if 'T' in colors else 'B' if colors=={'B'} else '.'
  for j in vg:qlab[j]=c
 start=v.canonical((qr,qu,''.join(qlab)));seen={start};queue=deque([start]);verdict='dark';bad=None
 while queue:
  st=queue.popleft()
  try:v.check_horizontal(st)
  except AssertionError:verdict='lit_overapproximation';bad=st;break
  for nxt in v.transforms(st):
   key=v.canonical(nxt)
   if key not in seen:seen.add(key);queue.append(key)
  if len(seen)>50000:verdict='inconclusive';break
 result['degree_three_quotient']=dict(r=qr,u=qu,label=''.join(qlab),status=verdict,states=len(seen),remaining=len(queue),bad_state=bad)
 (HERE/'proof-compression.json').write_text(json.dumps(result,indent=2)+'\n')
 print('Quotient:',verdict,len(seen),'remaining',len(queue),flush=True)
