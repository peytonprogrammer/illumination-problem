"""Independent four fixed paths, supplied West polygon and ELEVEN old fixtures.
No peer checker execution/import, new rooms, search or archive retrieval.
"""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
HERE=Path(__file__).resolve().parent;BASE=HERE.parent.parent
src=BASE/'surplus-four-local/R23-top6-search/verify.py';e={'__file__':str(src)}
exec(compile(src.read_text().split('\ndef path(d,nine):')[0],str(src),'exec'),e)
fan,H=e['fan'],e['H'];allK=H|set().union(*(fan(k,range(8))for k in e['C']))
reads=[src,Path(__file__)];provenance_notes=[]
def read(rel):
 p=BASE/rel;reads.append(p);return json.loads(p.read_text())
def pins(receipt,key='source_sha256'):
 for rel,h in receipt[key].items():
  p=BASE/rel;reads.append(p);raw=p.read_bytes()
  if hashlib.sha256(raw).hexdigest()!=h:
   assert key=='input_hashes' and rel=='fourth-surplus-review/mixed-e2-e1/critical-L.txt',rel
   marker=b'\nIndependent review checkpoint, 4 November2026:\n'
   before,after=raw.rsplit(marker,1)
   expected='Peer HAND ACCEPT without corrections, sections1–6, in\nsurplus-four-local/mixed-critical-L-review/review.txt. Complete eleven-room\nnecessary reduction accepted; all eleven optical closures still open.\n'.encode()
   assert after==expected and hashlib.sha256(before).hexdigest()==h
   provenance_notes.append({'source':rel,'change':'Only appended acceptance checkpoint; exact original proof prefix matches historical review hash','old_prefix_sha256':h})
fp=lambda pts:[tuple(F(x)for x in p)for p in pts]
decode=lambda ts:{tuple(sorted(map(tuple,t)))for t in ts}
def angle(ts,p):
 return sum(90 if e['dot'](*[e['sub'](v,p)for v in t if v!=p])==0 else 45 for t in ts if p in t)
peer={k:read(rel+'/check.json')for k,rel in [('West','fourth-surplus-review/west-D1-search'),('seven','fourth-surplus-review/mixed-eleven-transfer'),('three','fourth-surplus-review/mixed-Llower-Nsw-search'),('last','fourth-surplus-review/mixed-Llower-Nsw-Rplus-search')]}
for receipt in peer.values():pins(receipt)
fixtures=read('fourth-surplus-review/mixed-e2-e1/critical-L-check.json')
prior=read('surplus-four-local/mixed-critical-L-review/check.json')
pins(prior,'input_hashes')
P={
 'West':fp([(0,0),(-1,-2),('-2/3','-8/3'),(-1,'-5/2'),(0,-2),(2,2)]),
 'seven':fp([(0,0),(-2,'1/3'),('16/5','6/5'),('24/7','18/7'),(1,'13/6'),(2,2)]),
 'three':fp([(0,0),('-2/3','-4/3'),(3,'1/2'),(1,'3/2'),(2,2)]),
 'last':fp([(0,0),('2/3',1),(2,-1),('16/5','4/5'),('-2/5','-8/5'),(2,2)])}
W={
 'West':[((-1,-3),(-1,-1)),((-1,-3),(1,-1)),((-1,-3),(-1,-1)),((-1,-3),(1,-1))],
 'seven':[((-2,0),(-2,1)),((3,1),(4,2)),((3,3),(4,2)),((1,2),(1,3))],
 'three':[((-1,-1),(0,-2)),((3,0),(3,1)),((1,1),(1,2))],
 'last':[((0,1),(1,1)),((1,-1),(3,-1)),((3,1),(4,0)),((-1,-1),(0,-2))]}
mi={'West':H|fan('B',[1,2,3,4]),'seven':H|fan('L',[0,1])|fan('E',[3,4]),'three':H|fan('B',[1,2]),'last':H|fan('B',[1,2])|fan('R',[3])}
expectedZ={'West':fan('B',[0,5,6,7])|fan((-2,-2),[0,7]),'seven':fan('L',[2])|fan('E',[2,5])|fan('N',[0]),'three':fan('B',[3])|fan('R',[3])|fan('N',[7]),'last':fan('B',[3])|fan('D',[1,2])|fan('R',[2])|fan('N',[6])}
images={'West':(-4,-8),'seven':(-12,2),'three':(-4,-8),'last':(8,12)}
records={};guards={}
for name,path in P.items():
 u,z,proof=e['audit'](path,W[name],mi[name],allK-expectedZ[name],images[name])
 assert z==expectedZ[name]
 for a,b in zip(path[1:-1],path[2:]):assert not e['on']((0,0),a,b)
 if name=='seven':record=peer[name]
 else:record=peer[name]['fixed_paths'][{'West':'West_four','three':'Bcenter_three','last':'accepted_B12_R3_four'}[name]]
 assert u==decode(record['required'])and z==decode(record['forbidden'])
 guards[name]=(u,z)
 records[name]={'path':[[str(x)for x in p]for p in path],'required':sorted(u),'forbidden':sorted(z),'proof':proof}
 print('PASS fixed',name,len(u),'U',len(z),'Z',flush=True)
# One supplied West geometry, independent boundary extraction and replay.
raw=read('fourth-surplus-review/west-D1-search/room.json')
room=decode(raw['triangles']);assert room==H|set().union(*(fan(k,ss)for k,ss in raw['spec'].items()))
V=e['boundary'](room);assert len(room)==35 and len(V)==20 and set(V)==set(map(tuple,raw['vertices']))
def ledger(ts):
 pts={p for t in ts for p in t};A={p for p in pts if p[0]%2==p[1]%2==0}
 assert {p for p in A if angle(ts,p)==360}=={(0,0),(2,0),(2,2)}
 J=sum(angle(ts,p)==360 for p in pts-A);sN=sum(angle(ts,p)==180 for p in pts-A)
 Q=sum(3 if angle(ts,p)==180 else angle(ts,p)//45 for p in A if angle(ts,p)!=360)
 return J,sN,Q,J+sN,Q+sN-8
assert ledger(room)==(4,2,10,6,4)
e['physical'](P['West'],V);e['physical'](P['West'][::-1],V)
e['physical']([e['sigma'](p)for p in P['West'][::-1]],[e['sigma'](p)for p in V])
for p in [(-1,-2),(0,-2)]:
 assert angle(room,p)==angle(mi['West'],p)==180 and p not in V
 hits=[(a,b)for a,b in zip(V,V[1:]+V[:1])if e['on'](p,a,b)]
 assert len(hits)==1 and p not in hits[0]
assert e['incident']((F(1),F(0)))<=H and e['on']((1,0),P['West'][-2],P['West'][-1])
assert not expectedZ['West']&set().union(*(fan(k,range(8))for k in e['C']if k!='B'))
# THREE strict hand intervals: arithmetic at monotone endpoints/root.
lo,hi=F(3,7),F(3,5);d=F(1,2)
assert lo<d<hi and 8*d-2==2
for t in (lo,hi):
 a=2*(t-1)/(1+t);c=(4*t-2)/(1-t)
 assert -3<=-1/t<=-1 and -1<=a<=1 and -3<=3*t-4<=-1 and -1<=c<=1
 assert 0<=5*t-2<=1 and 1<=7*t-2<=3
assert P['West']==fp([(0,0),(-1,-1/d),(2*(d-1)/(1+d),2*(d-1)/(1+d)-2),(-1,3*d-4),((4*d-2)/(1-d),(4*d-2)/(1-d)-2),(8*d-2,2)])
lo,hi=F(3,7),F(4,7);assert lo<F(1,2)<hi
for t in (lo,hi):
 assert -1<-2*t/(1+t)<0 and 0<=5*t-2<=1 and 1<=7*t-2<=2 and -1<=1/t-2<=1
lo,hi=F(1,7),F(2,11);assert lo<F(1,6)<hi
for t in (lo,hi):
 a=(2+4*t)/(1-t);c=(2+12*t)/(1+t)
 assert 0<2*t<1 and 3<=a<=4 and 3<c<4 and 2<=4-11*t<=3
 assert 1<=7*t<=2 and 1<=1/t-4<=3
# Explicit disjoint 7+3+1 partition of the authoritative ELEVEN names.
seven={r['fixture']for r in peer['seven']['physical_replay']}
three=set(peer['three']['applications']);last={'Llower_Bcenter_Nsw_R+'}
assert len(seven)==7 and len(three)==3
assert not seven&three and not seven&last and not three&last
assert seven|three|last==set(fixtures['optically_open_fixture_names'])
applications=[]
for name in fixtures['optically_open_fixture_names']:
 chosen='seven'if name in seven else'three'if name in three else'last'
 f=fixtures['hand_forced_fixtures'][name];ts=decode(f['triangles']);v=e['boundary'](ts)
 assert len(v)==20 and set(v)==set(map(tuple,f['vertices']))
 J,sN,Q,k,delta=ledger(ts);assert k==6 and delta==4
 u,z=guards[chosen];assert u<=ts and not z&ts
 path=P[chosen];e['physical'](path,v);e['physical'](path[::-1],v)
 e['physical']([e['sigma'](p)for p in path[::-1]],[e['sigma'](p)for p in v])
 applications.append({'fixture':name,'path':chosen,'reflections':len(path)-2,'J':J,'sN':sN,'Q':Q,'k':k,'Delta':delta,'actual_firstwall_firstT_reverse_sigma':'PASS'})
 print('PASS fixture',name,chosen,flush=True)
# Existing complement cover is independently accepted <=13, not newly4.
reads += [BASE/'surplus-four-local/mixed-critical-L-review/review.txt',BASE/'surplus-four-local/mixed-critical-L-review/coverage.txt',BASE/'fourth-surplus-review/mixed-e2-e1/critical-L.txt']
for rel in ['west-D1-search','mixed-eleven-transfer','mixed-Llower-Nsw-search','mixed-Llower-Nsw-Rplus-search']:
 reads += [BASE/'fourth-surplus-review'/rel/n for n in ['argument.txt','check.py','coverage.txt']]
out={'status':'INDEPENDENT_WEST_FOUR_AND_COMPLETE_L_T_ELEVEN_JOIN_ACCEPT','West_whole_family_bound':4,'mixed_L_T_whole_original_bound':13,'eleven_residual_bound':4,'new_path_records':records,'fixture_dispatch':applications,'provenance_reconciliations':provenance_notes,'independent_West_geometry':{'tiles':35,'walls':20,'J':4,'sN':2,'Q':10,'k':6,'Delta':4,'smooth_contacts':[[-1,-2],[0,-2]]},'limits':'Exactly FOUR named fixed paths, ONE supplied West polygon and ELEVEN already accepted supplied fixtures. No new room/cap census/discovery/archive/peer execution. Accepted criticalL complement/classification inherited; independent AI review not formal/expert verification. Other mixedB/E/remote/fullDelta4 obligations remain.','source_sha256':{str(p.relative_to(BASE)):hashlib.sha256(p.read_bytes()).hexdigest()for p in dict.fromkeys(reads)}}
(HERE/'check.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
print(out['status'])
