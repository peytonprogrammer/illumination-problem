"""Own exact three-pass polygons, physical paths and prescribed boundary witnesses."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product,combinations
from math import gcd,lcm
from importlib.util import spec_from_file_location,module_from_spec
import json,hashlib
HERE=Path(__file__).resolve().parent;BASE=HERE.parent;PEER=BASE/'unequal-depth'
def load(name,path):
    sp=spec_from_file_location(name,path);m=module_from_spec(sp);sp.loader.exec_module(m);return m
O=load('own_transfer',HERE/'outer-leg-transfer-check.py');G=O.G
BOXES=((0,1,1,2,1,2),(0,3,2,3,2,3),(2,1,1,2,0,1),(2,3,2,3,3,4))
def val(g,p):return g[0]*p[0]+g[1]*p[1]+g[2]
def cross(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
def hull(points):
    pts=sorted(set(points))
    def half(seq):
        out=[]
        for x in seq:
            while len(out)>1 and cross(out[-2],out[-1],x)<=0:out.pop()
            out.append(x)
        return out
    return half(pts)[:-1]+half(pts[::-1])[:-1] if len(pts)>1 else pts
def poly_from_guards(gs):
    pts=[]
    for (a,b,c),(d,e,f) in combinations(gs,2):
        det=a*e-b*d
        if not det:continue
        p=((b*f-c*e)/det,(c*d-a*f)/det)
        if all(val(g,p)>=0 for g in gs):pts.append(p)
    out=hull(pts)
    if len(out)<3 or sum(cross((0,0),a,b) for a,b in zip(out,out[1:]+out[:1]))==0:return []
    return out
def polygons(eta=F(0)):
    result=[]
    for u,c,l0,h0,l3,h3 in BOXES:
        for l1,l2 in product((2,3) if c==1 else (0,1),repeat=2):
            for ks in product(range(4),repeat=3):
                intervals=[(l0,h0)]+[(lo+4*k,lo+1+4*k) for lo,k in zip((l1,l2),ks[:2])]+[(l3+4*ks[2],h3+4*ks[2])]
                guards=[(F(0),F(1),F(0)),(F(0),F(-1),F(4))]
                for j,(lo,hi) in enumerate(intervals):guards.extend([(F(1),F(j),-F(lo)-eta),(F(-1),F(-j),F(hi)-eta)])
                vertices=poly_from_guards(guards)
                if vertices:result.append({'u':u,'c':c,'internal_lo':[l1,l2],'residue_shifts':list(ks),'guards':guards,'vertices':vertices})
    return result
def normal(a,b,height=3):
    # Solve the two coefficient identities for m*A+n=r*(A+B+height).
    x,y=a;z,w=b;raw=(x+z,x*(y+w+height)-(x+z)*y,x)
    den=lcm(*(v.denominator for v in raw));v=[int(t*den) for t in raw];gg=gcd(*v)
    assert gg
    v=[t//gg for t in v]
    if v[0]<0 or v[0]==0 and v[1]<0:v=[-t for t in v]
    m,n,r=v
    assert m*x==r*(x+z) and m*y+n==r*(y+w+height) and gcd(*v)==1
    return v
def path(A,B,s,t,v,E,u,c):
    X=lambda z:E+v*z
    events=[]
    for lo,hi,offset,extra in ((-A,F(0),0,0),(F(0),F(3),c,1),(F(3),3+B,u,0)):
        x,y=sorted((X(lo),X(hi)))
        for k in range(int((x-offset)//2)-1,int((y-offset)//2)+2):
            z=(offset+2*k-E)/v
            if lo<z<hi:events.append((z,extra+G.fold(X(z)-offset,F(2))))
    for z in (F(1),F(2)):events.append((z,1+G.fold(X(z)-c,F(2))))
    assert len({z for z,x in events})==len(events)
    def Y(z):return z if z<=1 else 2-z if z<=2 else z-2
    return [(s,-A)]+[(x,Y(z)) for z,x in sorted(events)]+[(t,1+B)]
def main():
    polys=polygons();assert len(polys)==8
    # Exact portal affine/velocity matching, one interior point fixes each affine piece.
    identities=0
    for u,c,l0,h0,l3,h3 in BOXES:
        for j,(lo,hi,off1,ex1,off2,ex2) in enumerate(((l0,h0,0,0,c,1),(l3,h3,c,1,u,0))):
            p=F(lo+hi,2)
            assert ex1+G.fold(p-off1,F(2))==ex2+G.fold(p-off2,F(2))
            slope=lambda off:1 if (p-off)%4<2 else -1
            assert slope(off1)==slope(off2);identities+=1
    paths=[]
    for p in polys:
        E,v=[sum(x[j] for x in p['vertices'])/len(p['vertices']) for j in (0,1)]
        assert v>0 and all(val(g,(E,v))>0 for g in p['guards'])
        s,t=F(1,3),F(2,3);A=(E-s)/v;M=1
        while (F(p['u'])+t+4*M-E)/v<=3:M+=1
        B=(F(p['u'])+t+4*M-E)/v-3
        aux=path(A,B,s,t,v,E,p['u'],p['c'])
        assert G.verify(aux,F(1),F(1),A,B,s,t,A+1,B+1)==len(aux)-2
        for lc,uc in product((0,1),repeat=2):
            a=A/2 if lc else A;b=3*B/4 if uc else B
            hm=(A+a)/2 if lc else A+1;hp=(B+b)/2 if uc else B+1
            z=O.transfer(aux,a,b,hm,hp,lc,uc);paths.append(z)
    parent=json.loads((PEER/'three-pass-circle.json').read_text());families=json.loads((PEER/'critical-rectangles.json').read_text())['positive_dimensional_families']
    witnesses=[];identities2=0
    for record in parent['records']:
        family=families[record['family_index']];expr=[tuple(map(F,e)) for e in family['affine_expressions']]
        assert not any(expr[i]==expr[j] for i in (0,1) for j in (2,3))
        assert record['affine_expressions']==family['affine_expressions']
        assert sorted(t['endpoint_boundary'] for t in record['boundary_tests'])==sorted(family['common_blind_boundary_points'])
        for test in record['boundary_tests']:
            s,t=map(F,test['endpoint_boundary']);w=test['three_pass_circle_hit'];i,j=w['sheet'];rel=normal(expr[i],expr[j]);assert rel==w['relation'];m,n,r=rel
            p=next(p for p in polys if (p['u'],p['c'],p['internal_lo'],p['residue_shifts'])==(w['u'],w['c'],w['internal_lo'],w['residue_shifts']))
            assert set(p['vertices'])=={tuple(map(F,z)) for z in w['polygon']}
            lo,hi=min(m*x+n*y for x,y in p['vertices']),max(m*x+n*y for x,y in p['vertices'])
            C=(m-r)*s+r*w['epsilon']*t+r*w['u']+4*w['level_k']
            assert lo<C<hi and list(map(str,(lo,hi)))==w['normal_interval'] and str(C)==w['level']
            for k in (F(-3,7),F(0),F(11,5)):
                A=expr[i][0]*k+expr[i][1];B=expr[j][0]*k+expr[j][1]
                assert m*A+n==r*(A+B+3);identities2+=1
            witnesses.append({'family_index':record['family_index'],'boundary':test['endpoint_boundary'],'relation':rel,'strict_gap':[str(C-lo),str(hi-C)]})
    assert len(parent['records'])==len(witnesses)==16
    names=['three-pass-circle.md','three-pass-circle.py','three-pass-circle.json','critical-rectangles.json']
    out={'status':'PASS','phase_polygons':len(polys),'portal_affine_matching_identities':identities,'forward_cap_transferred_paths':len(paths),'paths_with_reverse_and_diagonal_scaling':3*len(paths),'contacts_with_reverse_and_scaling':sum(2*p['contacts']+p['reverse_contacts'] for p in paths),'boundary_circle_witnesses':witnesses,'affine_relation_controls':identities2,'source_sha256':{'unequal-depth/'+n:hashlib.sha256((PEER/n).read_bytes()).hexdigest() for n in names},'limits':'Physical template and 16 strict circle-boundary hits; no rational finite-orbit or full family closure.','polygons':[{k:[[str(x) for x in z] for z in v] if k in ('vertices','guards') else v for k,v in p.items()} for p in polys],'paths':paths}
    (HERE/'three-pass-check.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ('paths','polygons','source_sha256','boundary_circle_witnesses')}))
if __name__=='__main__':main()
