"""Independent geometric certificate of the frozen triangle-to-origami builder."""
from pathlib import Path
from fractions import Fraction as Q
from itertools import product
from datetime import datetime,timezone
import importlib.util,json,hashlib,re
R=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('geometry',R/'resumed-exact-check.py');geo=importlib.util.module_from_spec(sp);sp.loader.exec_module(geo)
sp=importlib.util.spec_from_file_location('frozen',R.parents[1]/'illumination-k4-codex/origami-decider-review/inputs/origami_dark.py');old=importlib.util.module_from_spec(sp);sp.loader.exec_module(old)
effort=json.loads((R/'marked-origami-decision-effort.json').read_text())
def deadline():assert datetime.now(timezone.utc)<datetime.fromisoformat(effort['deadline_utc'])
G=[((sx,0),(0,sy)) for sx,sy in product((-1,1),repeat=2)]+[((0,sx),(sy,0)) for sx,sy in product((-1,1),repeat=2)]
GI={g:i for i,g in enumerate(G)}
def ap(g,p):return(g[0][0]*p[0]+g[0][1]*p[1],g[1][0]*p[0]+g[1][1]*p[1])
def mul(a,b):return tuple(tuple(sum(a[i][k]*b[k][j] for k in(0,1)) for j in(0,1)) for i in(0,1))
def add(a,b):return(a[0]+b[0],a[1]+b[1])
def sub(a,b):return(a[0]-b[0],a[1]-b[1])
def linear_reflection(p,q):
    dx,dy=sub(q,p)
    return ((-1,0),(0,1)) if dx==0 else ((1,0),(0,-1)) if dy==0 else ((0,1),(1,0)) if dx*dy>0 else ((0,-1),(-1,0))
def inv(p):out=[0]*len(p);[(out.__setitem__(j,i)) for i,j in enumerate(p)];return out

def canonical(h,v,lab,s):
    order=[s];which={s:0}
    for x in order:
        for y in (h[x],v[x]):
            if y not in which:which[y]=len(order);order.append(y)
    return tuple(which[h[x]] for x in order),tuple(which[v[x]] for x in order),tuple(lab[x] for x in order)

def certify(V,S,T):
    deadline();V=list(map(tuple,V));S=tuple(S);T=tuple(T);geo.simple(V)
    assert all(isinstance(z,int) for p in V+[S,T] for z in p) and S!=T
    assert geo.location(V,S)==geo.location(V,T)==1
    expected=set()
    for a,b in geo.edges(V):
        dx,dy=sub(b,a);assert dx==0 or dy==0 or abs(dx)==abs(dy)
        if dx and dy:assert (a[0]+a[1])%2==0
        steps=max(abs(dx),abs(dy));step=(dx//steps,dy//steps)
        for k in range(steps):expected.add(frozenset(((a[0]+step[0]*k,a[1]+step[1]*k),(a[0]+step[0]*(k+1),a[1]+step[1]*(k+1)))))
    tri=[]
    for x in range(min(p[0] for p in V),max(p[0] for p in V)):
      for y in range(min(p[1] for p in V),max(p[1] for p in V)):
        a=(x+(x%2),y+(y%2));b=(2*x+1-a[0],2*y+1-a[1]);corners={(x,y),(x+1,y),(x,y+1),(x+1,y+1)}
        for o in sorted(corners-{a,b}):
            center=(Q(a[0]+b[0]+o[0],3),Q(a[1]+b[1]+o[1],3))
            if geo.location(V,center)==1:tri.append((a,b,o))
    incidence={}
    for i,t in enumerate(tri):
        for a,b in geo.edges(list(t)):incidence.setdefault(frozenset((a,b)),[]).append(i)
    assert all(len(v) in(1,2) for v in incidence.values())
    assert {e for e,ii in incidence.items() if len(ii)==1}==expected
    area2=abs(sum(a[0]*b[1]-a[1]*b[0] for a,b in geo.edges(V)));assert len(tri)==area2
    def across(state,e):
        i,k=state;others=[j for j in incidence[e] if j!=i]
        if others:return (others[0],k),(0,0)
        p,q=tuple(e);A=linear_reflection(p,q);shift=ap(G[k],sub(p,ap(A,p)))
        return (i,GI[mul(G[k],A)]),shift
    pairs=[];pair_of={};relative={};boxes=[]
    for i in range(len(tri)):
      for k,g in enumerate(G):
        state=(i,k)
        if state in pair_of:continue
        mate,shift=across(state,frozenset(tri[i][:2]));assert mate!=state
        points1=[ap(g,p) for p in tri[i]];points2=[add(ap(G[mate[1]],p),shift) for p in tri[mate[0]]]
        points=points1+points2;X=min(p[0] for p in points);Y=min(p[1] for p in points)
        assert max(p[0] for p in points)==X+1 and max(p[1] for p in points)==Y+1 and len(set(points))==4
        shared=set(points1)&set(points2);assert len(shared)==2
        aa,bb=tuple(shared);oo1=next(p for p in points1 if p not in shared);oo2=next(p for p in points2 if p not in shared)
        assert geo.det(sub(bb,aa),sub(oo1,aa))*geo.det(sub(bb,aa),sub(oo2,aa))<0
        number=len(pairs);pairs.append((state,mate));boxes.append((X,Y));relative[state]=(0,0);relative[mate]=shift;pair_of[state]=pair_of[mate]=number
    assert len(pairs)==4*len(tri)==4*area2
    h=[None]*len(pairs);v=[None]*len(pairs);labels=[];faces=0
    for number,pair in enumerate(pairs):
        X,Y=boxes[number];physical_SW=set()
        for state in pair:
            i,k=state;g=G[k];shift=relative[state];pts=[add(ap(g,p),shift) for p in tri[i]]
            for p,z in zip(tri[i],pts):
                if z==(X,Y):physical_SW.add(p)
            for jj in range(3):
                a,b=pts[jj],pts[(jj+1)%3];axis=None
                if a[0]==b[0]==X+1:axis=0
                if a[1]==b[1]==Y+1:axis=1
                if axis is None:continue
                e=frozenset((tri[i][jj],tri[i][(jj+1)%3]));neighbor,extra=across(state,e);nn=pair_of[neighbor]
                wanted=add(shift,extra);translation=sub(wanted,relative[neighbor]);target_box=add(boxes[nn],translation)
                assert target_box==(X+(axis==0),Y+(axis==1))
                assert {add(ap(G[neighbor[1]],p),wanted) for p in e}=={a,b}
                (h if axis==0 else v)[number]=nn;faces+=1
        assert len(physical_SW)==1
        p=next(iter(physical_SW));labels.append('block' if p in V else 'S' if p==S else 'T' if p==T else '.')
    assert sorted(h)==sorted(v)==list(range(len(pairs))) and faces==2*len(pairs)
    hi=inv(h);vi=inv(v);kap=[v[h[vi[hi[i]]]] for i in range(len(h))]
    assert all(labels[i]==labels[kap[i]] for i in range(len(h)))
    assert all(kap[i]==i for i in range(len(h)) if labels[i] in('S','T'))
    oh,ov,olab,os=old.build(V,S,T)
    ownroots={canonical(h,v,labels,i) for i,l in enumerate(labels) if l=='S'}
    oldroots={canonical(oh,ov,olab,i) for i,l in enumerate(olab) if l=='S'}
    assert ownroots==oldroots
    return {'triangles':len(tri),'squares_all_D4_copies':len(pairs),'geometric_oriented_side_certificates':faces,'source_lifts':labels.count('S'),'target_lifts':labels.count('T'),'distinct_rooted_components':len(ownroots),'source_component_square_counts':sorted({len(a[0]) for a in ownroots}),'permutations':(h,v,labels),'independent_root':next(i for i,l in enumerate(labels) if l=='S'),'source_root_matrix':G[pairs[next(i for i,l in enumerate(labels) if l=='S')][0][1]]}

def main():
    tex=R.parents[1]/'illumination-k4-codex/preprint-review-codex/revised.tex'
    text=tex.read_text().split(r'\label{eq:vertices}',1)[1].split(r'\end{equation}',1)[0];dark=[tuple(map(int,m)) for m in re.findall(r'\((-?\d+),\s*(-?\d+)\)',text)];assert len(dark)==22
    fixtures=[('square',[(0,0),(4,0),(4,4),(0,4)],(1,1),(2,2)),('diagonal',[(0,0),(4,0),(4,4)],(2,1),(3,1)),('L',[(0,0),(4,0),(4,2),(2,2),(2,4),(0,4)],(1,3),(3,1)),('known22',dark,(0,0),(2,2))]
    rows=[]
    for name,V,S,T in fixtures:
        result=certify(V,S,T);result.pop('permutations');result.pop('independent_root');result.pop('source_root_matrix');rows.append({'name':name,**result})
    out={'status':'ALL_FOUR_FULL_GEOMETRIC_BUILDER_CERTIFICATES_PASS','rows':rows,'total_oriented_side_certificates':sum(r['geometric_oriented_side_certificates'] for r in rows),'whole_goal_complete':False,'discovery':False,'scope':'Independent full finite gluing certificates for four prescribed rooms; hand general-builder proof separate, no orbit execution yet.','source_sha256':{'../../illumination-k4-codex/origami-decider-review/inputs/origami_dark.py':hashlib.sha256((R.parents[1]/'illumination-k4-codex/origami-decider-review/inputs/origami_dark.py').read_bytes()).hexdigest(),'../../illumination-k4-codex/preprint-review-codex/revised.tex':hashlib.sha256(tex.read_bytes()).hexdigest(),'resumed-exact-check.py':hashlib.sha256((R/'resumed-exact-check.py').read_bytes()).hexdigest()}}
    (R/'marked-origami-builder-check.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in('rows','source_sha256')}));print(json.dumps(rows))
if __name__=='__main__':main()
