"""Mine obstruction supports from the SAVED known22 orbit. No new orbit states."""
from pathlib import Path
from collections import deque,Counter
import gzip,json,time,hashlib
start=time.monotonic();r=Path(__file__).resolve().parents[2]
raw=gzip.decompress((r/'illumination-generalization-2026-11-06/review/marked-origami-known22-closure.gz').read_bytes());n=60
assert hashlib.sha256(raw).hexdigest()=='2f5540623e3d0a7c08b2d1bbe4487d607e9024cef82263de175c30bec7b7a346'
states={tuple(raw[k+i*n:k+(i+1)*n] for i in range(3)) for k in range(0,len(raw),3*n)}
def inv(p):
 q=[0]*len(p)
 for i,j in enumerate(p):q[j]=i
 return q
def cycles(state):
 h,v,lab=state;hi,vi=inv(h),inv(v);k=[v[h[vi[hi[i]]]] for i in range(n)]
 seen=set();out=[]
 for i in range(n):
  if i in seen:continue
  c=[];j=i
  while j not in seen:seen.add(j);c.append(j);j=k[j]
  out.append(c)
 return out
def move(s,tags,kind):
 h,v,lab=s
 if kind=='T':hi=inv(h);hh=h;vv=bytes(v[hi[i]] for i in range(n))
 else:vi=inv(v);hh=bytes(h[vi[i]] for i in range(n));vv=v
 order=[0];seen={0:0}
 for a in order:
  for b in(hh[a],vv[a]):
   if b not in seen:seen[b]=len(order);order.append(b)
 return (bytes(seen[hh[a]] for a in order),bytes(seen[vv[a]] for a in order),bytes(lab[a] for a in order)),tuple(tags[a] for a in order)
s0=min(states);tags=[-1]*n;z=0
for c in cycles(s0):
 if len(c)>1:
  assert len(c)==3
  for a in c:tags[a]=z
  z+=1
assert z==9
seen={s0:tuple(tags)};parents={s0:None};q=deque([s0]);supports=Counter();no_target=0;witnesses={}
while q:
 s=q.popleft();tags=seen[s];h,v,lab=s;a=h[0];mask=0;trace=[0]
 for c in cycles(s):
  assert len({tags[x] for x in c})==1
  assert (tags[c[0]]>=0)==(len(c)==3)
 while a:
  trace.append(a)
  if tags[a]>=0:mask|=1<<tags[a]
  if lab[a]==1:mask=0;trace=[a] # last physical source departure
  if lab[a]==2:
   assert mask
   supports[mask]+=1
   if mask.bit_count()==1 and mask not in witnesses:
    word=[];cursor=s
    while parents[cursor] is not None:
     cursor,kind=parents[cursor];word.append(kind)
    word=''.join(reversed(word));replay=s0;rt=seen[s0]
    for kind in word:replay,rt=move(replay,rt,kind)
    assert replay==s and rt==tags
    assert lab[trace[0]]==1 and lab[trace[-1]]==2
    assert all(lab[x]!=1 for x in trace[1:])
    assert all(h[x]==y for x,y in zip(trace,trace[1:]))
    assert {tags[x] for x in trace if tags[x]>=0}=={mask.bit_length()-1}
    witnesses[mask]={'zero_id':mask.bit_length()-1,'shear_word':word,'h':list(h),'v':list(v),'labels':list(lab),'zero_ids':list(tags),'formal_source_to_target_trace':trace}
   break
  a=h[a]
 else:no_target+=1
 for kind in ['T','U']:
  nxt,nt=move(s,tags,kind);assert nxt in states
  if nxt not in seen:seen[nxt]=nt;parents[nxt]=(s,kind);q.append(nxt)
assert len(seen)==len(states)
best=[]
for mask in range(1<<9):
 if all(mask&s for s in supports):
  if not best or mask.bit_count()<best[0].bit_count():best=[mask]
  elif mask.bit_count()==best[0].bit_count():best.append(mask)
def bits(m):return [i for i in range(9) if m>>i&1]
out={'status':'FIXED_CERTIFICATE_SUPPORT_MINING_PASS','saved_states':len(states),'states_with_formal_target_cycle':sum(supports.values()),'states_without_target_in_horizontal_cycle':no_target,'distinct_corner_supports':len(supports),'support_size_distribution':dict(sorted(Counter({k:sum(v for s,v in supports.items() if s.bit_count()==k) for k in range(1,10)}).items())),'minimum_hitting_set_size':best[0].bit_count(),'minimum_hitting_sets':[bits(x) for x in best],'singleton_supports':[bits(s) for s in supports if s.bit_count()==1],'seconds':time.monotonic()-start,'limits':'Formal horizontal continuations through true zeros are NOT legal light paths. This only measures which named zeros stop the saved formal candidate words, with labels transported along one chosen certified shear path per state. It is NOT a new room, lower bound, general support theorem, or proof after a geometric corner removal.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
assert len(witnesses)==9
Path(__file__).with_name('negative-control-singleton-witnesses.json').write_text(json.dumps({'certificate_raw_sha256':hashlib.sha256(raw).hexdigest(),'initial_state':[list(x) for x in s0],'initial_zero_ids':list(seen[s0]),'transport_note':'T and U preserve C=v h v^-1 h^-1 before canonical relabeling; every transported zero tag is checked against actual commutator cycles. Shear words replay from the specified initial state.','witnesses':[witnesses[1<<i] for i in range(9)],'limits':out['limits']},indent=2)+'\n')
