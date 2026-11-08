"""Independent bounded check of exactly the claimed parent2/leaf2 proof row.
No new rays, directions, archive queries or solver calls. Retained paths only.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from collections import Counter,defaultdict
import json,runpy,sys,hashlib,time
HERE=Path(__file__).resolve().parent;ROOT=HERE/'inputs'
sys.path.insert(0,str(ROOT/'k7-pilot/inputs'))
import illumination_geometry as geo
ck=runpy.run_path(str(ROOT/'lower-bound-proof-audit/full-replay/guard-checker.py'))
tri=lambda t:tuple(sorted(map(tuple,t)))
read=lambda rel:json.loads((ROOT/rel).read_text())
D=geo.DIRS
S,U,T=(0,0),(2,0),(2,2)
full={S,U,T};centers={'L':(-2,0),'B':(0,-2),'D':(2,-2),'R':(4,0),'E':(4,2),'T':(2,4),'N':(0,2)}
K=full|set(centers.values())
def fan(a,st,m):return frozenset(tri((a,(a[0]+D[i%8][0],a[1]+D[i%8][1]),(a[0]+D[(i+1)%8][0],a[1]+D[(i+1)%8][1]))) for i in range(st,st+m))
H=frozenset().union(*(fan(a,0,8) for a in full))
slots={n:tri(t) for n,t in read('zero-surplus-L/guard-incidence-check.json')['cap_options'].items()}
def sigma(p):return 2-p[1],2-p[0]
def shares(ts,us):return bool(set(e for t in ts for e in geo.edges_of(t))&set(e for t in us for e in geo.edges_of(t)))
def touched(ts):return sum(shares(ts,fan(a,0,8)) for a in full)
def angular(ts):
 out=defaultdict(int)
 for t in ts:
  for p in t:
   z=sum(1<<i for i in geo.wedge_slots(t,p));assert not out[p]&z
   out[p]|=z
 return dict(out)
def contiguous(z):return z==255 or sum(bool(z&(1<<i))!=bool(z&(1<<((i+1)%8))) for i in range(8))==2
paths={}
def add(name,raw):
 p=tuple(tuple(F(*c) for c in pt) for pt in raw);assert p[0]==S and p[-1]==T
 paths[name]=p
old=read('zero-surplus-L/cover-check.json')
for n,v in old['paths'].items():add('old:'+n,v['path'])
for rel in ['first-surplus-review/square-exchange-check.json']:
 for n,v in read(rel)['paths'].items():add(rel+':'+n,v['path'])
add('centerL3',read('first-surplus-review/residual-cover-check.json')['path'])
for n,v in read('fourth-surplus-review/remote22-check.json')['paths'].items():add('retained:'+n,v['path'])
for rel in ['third-surplus-review/healed-frozen.json','third-surplus-review/half-fan-frozen.json']:
 for n,v in read(rel)['hits'].items():add(rel+':'+n,v['path'])
frozen=read('fourth-surplus-review/remote22-frozen.json')
for family,v in frozen['families'].items():
 for t in v['terms']:add(f'family:{family}:{t["source_line"]}',t['path'])
add('new14',read('fourth-surplus-review/one-room-check.json')['path'])
# Preserve actual endpoints under reflection by reversing the reflected path.
for n,p in list(paths.items()):paths[n+':sigma']=tuple(sigma(q) for q in reversed(p))
guards={};unique={}
for n,p in paths.items():
 if p not in unique:
  u,z=ck['path_requirements'](p);unique[p]=(frozenset(u),frozenset(z))
 guards[n]=unique[p]
print('Retained paths independently checked:',len(unique),flush=True)
sys.path.insert(0,str(ROOT))
from second_guard_check import check as second_guard_check
for i,(p,(u,z)) in enumerate(unique.items(),1):
    raw={'U':sorted(u),'Z':sorted(z),'q':T,'path':[[[x.numerator,x.denominator] for x in point] for point in p]}
    assert second_guard_check(raw)=='ok',('second checker disagreement',i)
print('Second guard implementation PASS:',len(unique),flush=True)

# Recheck stored full guards and each published symbolic optical implication.
termchecks=0
for family,v in frozen['families'].items():
 fixed=frozenset(map(tri,v['fixed_triangles']));vs={n:tri(t) for n,t in v['variables'].items()}
 for t in v['terms']:
  u,z=guards[f'family:{family}:{t["source_line"]}']
  assert u==frozenset(map(tri,t['required_triangles'])) and z==frozenset(map(tri,t['forbidden_triangles']))
  assert u<=fixed|{vs[n] for n in t['requires']}
  assert not z&(fixed|{a for n,a in vs.items() if n not in t['forbids']})
  termchecks+=1
imp=read('fourth-surplus-review/remote22-check.json')['symbolic_implications'];impchecks=[]
for n,v in imp.items():
 if v['status']!='PASS':continue
 a,st,m=v['root'];b,ls,lm=v['leaf'];root=fan(tuple(a),st,m);leaf=fan(tuple(b),ls,lm)
 fixed=H|root|leaf|{slots[x] for x in v['present']}
 own={x for x,t in slots.items() if tuple(a) in t}
 possible=H|root|leaf|{t for x,t in slots.items() if x not in own and x not in v['absent']}
 key={'old13':'old:thirteen','L11':'first-surplus-review/square-exchange-check.json:L_thirteen','centerL3':'centerL3'}.get(v['path_key'],'retained:'+v['path_key'])
 u,z=guards[key];assert u<=fixed and not z&possible,(n,'failed implication')
 impchecks.append(n)
# Construct the entire necessary finite domain from the proved fan conditions,
# independently of the peer's nine named families or prescribed exclusions.
patterns=[]
for name,a in centers.items():
 for m in (3,4):
  for st in range(8):
   root=fan(a,st,m)
   if touched(root)!=1:continue # q=3, e=2 iff exactly one H side touched
   for b in ((a[0]+2,a[1]),(a[0]-2,a[1]),(a[0],a[1]+2),(a[0],a[1]-2)):
    if b in K:continue
    for ls in range(8):
     leaf=fan(b,ls,2)
     if not shares(root,leaf):continue
     patterns.append((name,a,st,m,b,ls,root|leaf))
print('Root/leaf angular patterns:',len(patterns),flush=True)
def proof_dispatch(name,a,st,m,b,ls,room):
    if name in ('T','E'):
        room=frozenset(tri(sigma(p) for p in t) for t in room)
        a=sigma(a);b=sigma(b);name='L' if name=='T' else 'B'
        rt=frozenset(t for t in room if a in t);lt=frozenset(t for t in room if b in t)
        st=next(j for j in range(8) if fan(a,j,m)==rt)
        ls=next(j for j in range(8) if fan(b,j,2)==lt)
    def works(key):
        u,z=guards[key];return u<=room and not z&room
    for key in ('old:one','old:one_sigma','old:four','old:four_sigma'):
        if works(key):return 'short forcing',key
    caps={n for n,t in slots.items() if t in room and a not in t}
    if name not in ('L','B'):
        for key in ('old:thirteen','old:thirteen_sigma'):
            if works(key):return 'noncritical',key
        raise AssertionError(('noncritical cover',name,st,m,b,ls,caps))
    def term(fam,row):return f'family:{fam}:{row}'
    if name=='L':
        assert {'B+','E-','T-'}<=caps
        assert 'L+' in {n for n,t in slots.items() if t in room}
        if b==(-2,-2):
            if (st,m) in ((6,3),(5,4)):key='centerL3'
            else:
                assert (st,m)==(6,4) and 'Nb-' in caps
                key='first-surplus-review/square-exchange-check.json:L_thirteen'
            branch='L south'
        else:
            assert b==(-2,2)
            if (st,m)==(7,3):
                assert 'Nr+' not in caps
                key=term('fixed_L_northquarter_Nrminus',2642) if 'Nr-' in caps else 'first-surplus-review/square-exchange-check.json:L_thirteen'
                branch='L north quarter'
            elif st==0:
                assert m in (3,4)
                if not caps&{'Nb-','Nb+'}:key='old:thirteen'
                elif 'Nb+' in caps:key=('third-surplus-review/healed-frozen.json:' if m==3 else 'third-surplus-review/half-fan-frozen.json:')+'remote_right_Nb+'
                elif m==4:key='third-surplus-review/half-fan-frozen.json:remote_right_Nb-'
                else:key=term('fixed_L_northtriple_Nbminus',2642)
                branch='L north half'
            else:
                assert (st,m)==(7,4)
                if ls==4:
                    assert 'Nb-' in caps and len(caps)==4
                    key=term('L_fullH_leftquarter',2642)
                elif ls==5:
                    row=3395 if 'Nr-' in caps else 3612 if 'R+' not in caps else 745
                    key=term('L_fullH_center',row)
                else:
                    assert ls==6 and len(caps)==4
                    row=3224 if 'D+' in caps else 652 if 'R+' in caps else None if 'R-' in caps else 2642
                    key='new14' if row is None else term('L_fullH_rightquarter',row)
                branch='L full H north leaf'+str(ls)
    else:
        assert {'E-','L+'}<=caps and 'Nb-' not in caps
        assert b==(-2,-2)
        assert (st,m) in ((1,3),(0,4),(1,4))
        assert not {'D+','R-'}<=caps and not {'Nr+','T-'}<=caps
        if (st,m)==(1,3):
            if 'Nb+' not in caps:row=883 if 'D-' in caps else 3715
            else:row=3040 if 'R+' not in caps else 60
            key=term('B_west_triple_center',row);branch='B triple'
        elif (st,m)==(0,4):
            if 'Nb+' not in caps:row=883 if 'D-' in caps else 119 if 'T+' in caps else 3608
            elif 'D-' in caps:row=60
            else:row=122 if 'T-' in caps else 98
            key=term('B_rectangle_center',row);branch='B rectangle'
        elif ls==7:
            row=3035 if 'T+' not in caps else 978 if 'D-' not in caps else 1312
            key=term('B_fullW_center',row);branch='B full centered'
        else:
            assert ls==0
            if 'Nr-' in caps:row=3800 if 'R+' in caps else 515
            elif 'Nr+' in caps:row=1266 if 'T+' in caps else 2257
            elif 'Nb+' in caps:row=103 if 'T+' in caps else 60
            elif 'T+' not in caps:row=60
            else:
                opt=caps&{'D+','D-','R+','R-'};assert len(opt)==1
                row={'D+':1036,'D-':2823,'R+':361,'R-':3224}[opt.pop()]
            key=term('B_fullW_upperquarter',row);branch='B full upperquarter'
    assert works(key),('named proof branch failed',branch,key,sorted(caps))
    return branch,key

counts=Counter();orient=Counter();failures=[];maxb=0;examples={};validmasks=[];branches=Counter()

for pi,(name,a,st,m,b,ls,extra) in enumerate(patterns):
 base=H|extra;basemask=angular(base)
 options=[[(None,None)]+[(n,t) for n,t in slots.items() if n.startswith(c) and (c!='T' or n in ('T-','T+'))] for c in centers if c!=name]
 # Prefix N correctly includes Nb and Nr, all other slot groups have one letter.
 for selection in product(*options):
  counts['assignments']+=1;room=base|{t for n,t in selection if t is not None}
  mask=basemask.copy()
  for n,t in selection:
   if t is None:continue
   for p in t:mask[p]=mask.get(p,0)|sum(1<<i for i in geo.wedge_slots(t,p))
  if any(not contiguous(z) for z in mask.values()):counts['noncontiguous']+=1;continue
  if {p for p,z in mask.items() if geo.label(p)=='A' and z==255}!=full:continue
  q=sum(3 if z.bit_count()==4 else z.bit_count() for p,z in mask.items() if geo.label(p)=='A' and z!=255)
  smooth={p for p,z in mask.items() if geo.label(p)!='A' and z.bit_count()==4}
  missing={p for p,z in angular(H).items() if geo.label(p)=='C' and z.bit_count()==4 and mask[p]==z}
  if q+len(smooth)!=12 or smooth!=missing:continue # Delta4 and b0
  J=sum(z==255 for p,z in mask.items() if geo.label(p)!='A')
  if J+len(smooth)!=6:continue
  angles=sum(z not in (255,) and z.bit_count()!=4 for z in mask.values())
  assert angles==20
  # Full independent geometric validation on every survivor, including holes.
  g=geo.check({'triangles':sorted(room),'marked':[S,T],'require_simple':True},strict=False)
  assert g['walls']==20 and g['simple_polygon']
  branch,key=proof_dispatch(name,a,st,m,b,ls,room);branches[branch]+=1
  caps={n for n,t in selection if n is not None};orient[(name,st,m,b,ls)]+=1
  matches=[(len(paths[n])-2,n) for n,(u,z) in guards.items() if u<=room and not z&room]
  if not matches:
   failures.append({'root':[name,st,m],'leaf':[b,ls],'caps':sorted(caps)});continue
  nb,pathkey=min(matches);assert nb<=23
  maxb=max(maxb,nb);counts['valid']+=1;counts['covered']+=1
  counts['new14_needed']+=all(n.startswith('new14') for _,n in matches)
  examples.setdefault(pathkey,{'root':[name,st,m],'leaf':[b,ls],'caps':sorted(caps)})
 print('pattern',pi+1,'/',len(patterns),'valid',counts['valid'],'gaps',len(failures),flush=True) if (pi+1)%16==0 else None
result={'status':'PASS' if not failures else 'FAIL','scope':'Complete finite specialization of exactly the stated parent2/leaf2 charge row, after hand structural reduction. Bounded proof audit, not new optical discovery. No full room universe or other surplus-four row enumerated.',
 'counts':dict(counts),'named_proof_branches':dict(branches),'angular_patterns':len(patterns),'valid_orientations':len(orient),'orientations':[{'root':[n,st,m],'leaf':[b,ls],'valid_cap_selections':c} for (n,st,m,b,ls),c in orient.items()],
 'second_guard_implementation':'PASS','unique_retained_paths_checked':len(unique),'frozen_symbolic_terms_checked':termchecks,'inherited_symbolic_implications_checked':impchecks,'maximum_selected_reflections':maxb,'failures':failures,'inputs':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in ROOT.rglob('*') if p.is_file() and '__pycache__' not in str(p)}}
(HERE/'check.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ('inputs','orientations','inherited_symbolic_implications_checked')},indent=2))
if failures:raise SystemExit(1)
