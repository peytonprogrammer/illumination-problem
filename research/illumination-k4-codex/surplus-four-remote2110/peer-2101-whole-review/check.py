"""Independent2101 fan/angle/slot/directguard proof audit; no peer execution."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import json,hashlib
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];PEER=ROOT/'fourth-surplus-review/remote2101'
src=ROOT/'surplus-four-local/R23-top6-search/verify.py';e={'__file__':str(src)};exec(src.read_text().split('\ndef path(d,nine):')[0],e)
fan,H,C=e['fan'],e['H'],e['C'];pins={}
def read(rel):
 p=ROOT/rel;pins[rel]=hashlib.sha256(p.read_bytes()).hexdigest();return json.loads(p.read_text())
def dec(ts):return {tuple(sorted(map(tuple,t)))for t in ts}
def edges(ts):return{tuple(sorted((a,b)))for t in ts for a,b in zip(t,t[1:]+t[:1])}
def angle(ts,p):return sum(90 if e['dot'](*[e['sub'](v,p)for v in t if v!=p])==0 else 45 for t in ts if p in t)
def pointset(ts):return{p for t in ts for p in t}
capdoc=read('triangle-composition/inputs/caps.json')['cap_options'];caps={n:tuple(sorted(map(tuple,t)))for n,t in capdoc.items()}
site={n:next(k for k,c in C.items()if c in t)for n,t in caps.items()}
assert len(caps)==16 and {t for t in caps.values()}=={t for k in C for i in range(8)for t in fan(k,[i])if edges({t})&edges(H)}
for name,k,i in [('L+','L',0),('B+','B',1),('E-','E',4),('T-','Tc',5)]:assert{caps[name]}==fan(k,[i])
parent=read('fourth-surplus-review/remote2101/classification.json');final=read('fourth-surplus-review/remote2101/final-dispatch.json');non=read('fourth-surplus-review/remote2101/noncritical.json')
for receipt in [parent,final,non]:
 for rel,h in receipt['source_sha256'].items():
  p=ROOT/rel;assert hashlib.sha256(p.read_bytes()).hexdigest()==h,rel;pins[rel]=h
known=set(C.values())|{(0,0),(2,0),(2,2)}
def key(k,ss,remote,i):return(k,tuple(sorted(ss)),tuple(remote),i)
peerrows={key(r['site'],r['sectors'],r['remote_A'],r['remote_sector']):r for r in parent['templates']}
ours={}
for k,ref,forced in [('L',0,['B+','E-','T-']),('B',1,['L+','E-'])]:
 a=C[k]
 for m in [3,4]:
  for start in range(8):
   ss=[(start+j)%8 for j in range(m)]
   if ref not in ss:continue
   root=fan(k,ss)
   for dx,dy in [(2,0),(-2,0),(0,2),(0,-2)]:
    remote=(a[0]+dx,a[1]+dy)
    if remote in known:continue
    for i in range(8):
     leaf=fan(remote,[i]);joint=edges(root)&edges(leaf)
     if not joint:continue
     assert len(joint)==1
     fixed=H|root|leaf|{caps[n]for n in forced};variable=[n for n in caps if site[n]!=k and site[n]not in {site[n]for n in forced}]
     options={j:[()]+[(n,)for n in variable if site[n]==j]for j in C if j!=k and j not in{site[n]for n in forced}}
     maxsupport=fixed|{caps[n]for n in variable};pts=pointset(maxsupport);J=sum(angle(fixed,p)==360 for p in pts if p[0]%2 or p[1]%2)
     cH=sum(angle(H,p)==180 and angle(root,p)==180 for p in pts if p[0]%2!=p[1]%2);assert J==2+cH
     for p in pts:
      if p[0]%2==p[1]%2==0:continue
      maximum=angle(fixed,p)+sum(max([0]+[angle({caps[n]},p)for n in variable if site[n]==j])for j in options)
      assert angle(fixed,p)==360 or maximum<360
     fixedsmooth=[p for p in pts if (p[0]%2 or p[1]%2)and not(p[0]%2!=p[1]%2 and angle(H,p)==180)and angle(fixed,p)==angle(maxsupport,p)==180]
     row=peerrows[key(k,ss,remote,i)]
     assert dec(row['minimum'])==fixed and dec(row['maximum'])==maxsupport and row['J']==J and row['ordinary_cap_count']==J+2
     assert set(map(tuple,row['fixed_extra_smooth']))==set(fixedsmooth) and row['excluded_b1']==(len(fixedsmooth)>=2)
     assert set(row['variable_caps'])==set(variable)
     # Compare every recorded extra-B coefficient independently from geometry.
     Bterms={tuple(r['point']):r for r in row['extra_B_terms']}
     expectedB={}
     for p in pts:
      if not(p[0]%2 and p[1]%2):continue
      aa=angle(fixed,p);co={n:angle({caps[n]},p)for n in variable if angle({caps[n]},p)}
      maximum=aa+sum(max([0]+[v for n,v in co.items()if site[n]==j])for j in options)
      if aa<=180<=maximum:expectedB[p]=(aa,co)
     assert set(expectedB)==set(Bterms)
     for p,(aa,co)in expectedB.items():assert aa==Bterms[p]['fixed_degrees'] and co==Bterms[p]['cap_degrees']
     outsC={p for p in pts if p[0]%2!=p[1]%2 and angle(H,p)==0 and angle(fixed,p)==180};assert outsC==set(map(tuple,row['extra_C_constant']))
     ours[key(k,ss,remote,i)]={'row':row,'fixed':fixed,'options':options,'pts':pts,'J':J}
assert set(ours)==set(peerrows)and len(ours)==18 and sum(v['row']['excluded_b1']for v in ours.values())==3
# Restore the accepted fixed guard catalog, not classification's sufficient-condition list.
old=read('fourth-surplus-review/three-unit-b1-independent/check.json')['named_guards'];guards=dict(old);short={}
for rel in final['source_sha256']:
 if not rel.endswith('.json')or rel.endswith(('classification.json','support.json','noncritical.json')):continue
 data=read(rel)
 for name,g in data.get('fixed_paths',{}).items():guards[rel+':'+name]=g;short[name]=g
for rel in ['triangle-composition/seven-path.json','triangle-composition/six-path.json']:
 g=read(rel);guards[rel]={'required':g['required_triangles'],'forbidden':g['forbidden_triangles'],'reflections':len(g['path'])-2}
for rel in ['fourth-surplus-review/remote2101-left-N6/check.json','fourth-surplus-review/remote2101-B-roof-R3/check.json']:
 for name,g in read(rel)['fixed_paths'].items():guards[rel+':'+name+':sigma']={'required':sorted(e['transform'](dec(g['required']))),'forbidden':sorted(e['transform'](dec(g['forbidden']))),'reflections':g['reflections']}
def sigma_g(g):return{'required':sorted(e['transform'](dec(g['required']))),'forbidden':sorted(e['transform'](dec(g['forbidden']))),'reflections':g['reflections']}
Bguards={**short,'sigma_core_three':sigma_g(short['core_three']),'sigma_N6_four':sigma_g(short['N6_four']),'sigma13':old['N_CO_BTc_SW'],'Btwo':old['forcing_missingT_outerB'],'Bfive':old['N_CO_LB_NE']}
expectedlabels={}
for data in ours.values():
 r,fixed,opts,pts,J=data['row'],data['fixed'],data['options'],data['pts'],data['J']
 if r['excluded_b1']:continue
 for tup in product(*(opts[j]for j in opts)):
  names={n for entry in tup for n in entry}
  if len(names)!=J+2-len(r['forced_caps']):continue
  # Scalar angle addition only. These are necessary labels, never polygons.
  support=fixed|{caps[n]for n in names}
  b=sum(angle(support,p)==180 for p in pts if (p[0]%2 or p[1]%2)and not(p[0]%2!=p[1]%2 and angle(H,p)==180))
  if b!=1:continue
  # Separate peer b formula must also equal the direct complete angular sum.
  peerb=len(r['extra_C_constant'])+sum(t['fixed_degrees']+sum(v for n,v in t['cap_degrees'].items()if n in names)==180 for t in r['extra_B_terms']);assert peerb==b
  expectedlabels[(r['name'],tuple(sorted(names)))]=(support,r)
assert len(expectedlabels)==205
seen=set()
for r in final['rows']:
 k=(r['template'],tuple(r['variable_caps']));assert k in expectedlabels and k not in seen;seen.add(k);support,row=expectedlabels[k];label=r['hand_dispatch_guard'];g=Bguards[label]if row['site']=='B'else guards[label]
 u,z=dec(g['required']),dec(g['forbidden']);assert u<=support and not z&support and g['reflections']==r['reflections']<=13
assert seen==set(expectedlabels)and max(r['reflections']for r in final['rows'])==13
# Fresh own Fraction halfplane constraints for all six noncritical witnesses.
zero=read('zero-surplus-L/cover-check.json')['paths']
def fp(P):return[tuple(F(*v)for v in p)for p in P]
Pone=fp(zero['one']['path']);Pfour=fp(zero['four']['path']);P13=fp(zero['thirteen']['path']);Ps13=fp(zero['thirteen_sigma']['path'])
sig=lambda P:[e['sigma'](p)for p in P[::-1]]
paths={'forcing_missingB':Pone,'forcing_sigma_missingB':sig(Pone),'forcing_missingT_ordinaryB':Pfour,'forcing_sigma_missingT_ordinaryB':sig(Pfour),'N_OO_L-E_NE':P13,'N_CO_BTc_SW':Ps13}
allK=H|set().union(*(fan(k,range(8))for k in C));catalog={}
for name,P in paths.items():
 walls=[]
 for a,p,b in zip(P,P[1:],P[2:]):
  v=e['sub'](p,a);w=e['sub'](b,p);v=tuple(x/max(map(abs,v))for x in v);w=tuple(x/max(map(abs,w))for x in w)
  t=tuple(v[k]+w[k]for k in (0,1))
  if t==(0,0):t=(-v[1],v[0])
  walls.append((tuple(p[k]-t[k]for k in (0,1)),tuple(p[k]+t[k]for k in (0,1))))
 u,z,_=e['constraints'](P,walls);assert(u,z)==(dec(old[name]['required']),dec(old[name]['forbidden']))
 assert u|z<=allK
 if name.startswith('forcing'):assert not(u|z)&set().union(*(fan(k,range(8))for k in ['D','R','N']))
 else:assert not(u|z)&(fan('D',range(8))|fan('R',range(8)))
 ur,zr,_=e['constraints'](P[::-1],walls[::-1]);assert(u,z)==(ur,zr)
 catalog[name]=(u,z)
base=H|{caps[n]for n in ['B+','E-','L+','T-']};u1,z1=catalog['N_OO_L-E_NE'];u2,z2=catalog['N_CO_BTc_SW'];assert u1<=base and u2<=base
assert z1&fan('N',range(8))==fan('N',[5,6])and z2&fan('N',range(8))==fan('N',[0,7])
assert not(z1|z2)&(base|fan('D',range(8))|fan('R',range(8)))
windows=[]
for m in [3,4]:
 for start in range(8):
  ss=[(start+j)%8 for j in range(m)];root=fan('N',ss)
  touched=sum(bool(edges(root)&edges(fan(a,range(8))))for a in [(0,0),(2,0),(2,2)])
  if touched!=1:continue
  assert not z1&root or not z2&root;windows.append(tuple(sorted(ss)))
assert set(windows)=={tuple(r['sectors'])for r in non['N_windows']}and len(windows)==8
# Finalreview depends on already accepted optics plus our lasttwo fresh review.
for rel in ['surplus-four-remote2110/peer-final-optical-review/check.json','fourth-surplus-review/remote2101/theorem.txt','fourth-surplus-review/remote2101/classification.txt','fourth-surplus-review/remote2101/final-dispatch.txt','fourth-surplus-review/remote2101/noncritical.txt','fourth-surplus-review/remote2101/manifest.json']:
 p=ROOT/rel;pins[rel]=hashlib.sha256(p.read_bytes()).hexdigest()
pins[str(src.relative_to(ROOT))]=hashlib.sha256(src.read_bytes()).hexdigest();pins[str(Path(__file__).resolve().relative_to(ROOT))]=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
(HERE/'check.json').write_text(json.dumps({'status':'INDEPENDENT_WHOLE_REMOTE2101_WITHIN13_ACCEPTED','critical_interfaces':18,'fixed_b1_excluded':3,'necessary_labels':205,'noncritical_fresh_guard_count':6,'N_windows':windows,'bound':13,'source_sha256':pins,'limits':'Independent fan/angle/slot/guard and handjoin audit. Prior exact optical proofs explicit dependencies; no peer programexecution,newpolygon,validitycensus,discovery,archive orworker. Notformalverification.'},indent=2)+'\n')
print('PASS whole2101:18interfaces/3exclusions/205labels +6freshnoncriticalguards/eightNwindows, actualST<=13')
