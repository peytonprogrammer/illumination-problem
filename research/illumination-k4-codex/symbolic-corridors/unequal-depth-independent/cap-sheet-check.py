"""Prescribed cap-sheet formulas; independent full physical geometry.
No candidate/orbit scan. Uses only own frozen independent helper.
"""
from fractions import Fraction as F
from pathlib import Path
from importlib.util import spec_from_file_location,module_from_spec
from math import lcm
import hashlib,json
HERE=Path(__file__).resolve().parent;BASE=HERE.parent
spec=spec_from_file_location('own_geometry',BASE/'arbitrary-endpoints-independent/check.py')
G=module_from_spec(spec);spec.loader.exec_module(G)

def construct(s,t,a,b,hm,hp,lc,uc,u,eps,M,c):
    d=g=F(1)
    A=2*hm-a if lc else a;B=2*hp-b if uc else b
    H=A+g+B;L=u+eps*t+4*M;v=(L-s)/H
    X=lambda y:s+v*(y+A)
    E1,E2=X(0),X(g)
    assert G.fold(E1,2)==1+G.fold(E1-c,2)
    assert 1+G.fold(E2-c,2)==G.fold(E2-u,2)
    assert 1<G.fold(E1,2)<2 and 1<G.fold(E2-u,2)<2
    lowercap=-hm if lc else None;uppercap=g+hp if uc else None
    if lc:assert X(lowercap)%2!=0
    if uc:assert (X(uppercap)-u)%2!=0
    def Y(z):
        if lc and z<-hm:return -2*hm-z
        if uc and z>g+hp:return 2*(g+hp)-z
        return z
    events=[]
    for ya,yb,offset,extra in [(-A,F(0),F(0),F(0)),(F(0),g,F(c),d),(g,g+B,F(u),F(0))]:
        lo,hi=sorted((X(ya),X(yb)))
        if v:
            for j in range((lo-offset)//2-1,(hi-offset)//2+2):
                xx=offset+2*j
                if lo<xx<hi:
                    zz=(xx-s)/v-A
                    assert ya<zz<yb
                    events.append((zz,(extra+G.fold(xx-offset,2),Y(zz))))
    if lc:events.append((lowercap,(G.fold(X(lowercap),2),-hm)))
    if uc:events.append((uppercap,(G.fold(X(uppercap)-u,2),g+hp)))
    assert len({z for z,p in events})==len(events),'simultaneous wall/cap contact'
    events.sort(key=lambda z:z[0])
    P=[(s,-a)]+[p for z,p in events]+[(t,g+b)]
    # A lifted target may fold to actual T before its final image. Existence
    # is established by the prefix ending at the FIRST actual T.
    target=(t,g+b);prefix=[P[0]];trimmed=False
    for i,(p,q) in enumerate(zip(P,P[1:])):
        w=G.sub(q,p)
        if G.cross(G.sub(target,p),w)==0:
            j=0 if w[0] else 1
            tau=(target[j]-p[j])/w[j]
            if 0<tau<=1:
                prefix.append(target);trimmed=i!=len(P)-2;break
        prefix.append(q)
    assert prefix[-1]==target
    n=G.verify(prefix,d,g,a,b,s,t,hm,hp)
    Q=lcm(*(r.denominator for r in [A/H,(A+g)/H]+([(A-hm)/H] if lc else [])+([(A+g+hp)/H] if uc else [])))
    for z in [0,g]+([lowercap] if lc else [])+([uppercap] if uc else []):
        assert (4*Q*(z+A)/H).denominator==1 and (4*Q*(z+A)/H)%4==0
    return prefix,n,trimmed,Q

def main():
    inputs=[('original',F(1),F(1),F(1,4),F(1,4),F(1,2),F(1,2),0,0,2,-1,1,1),
            ('upper',F(1),F(1),F(1,2),F(3,2),F(3,4),F(7,4),0,1,0,-1,1,1),
            ('lower',F(1),F(1),F(3,2),F(1,2),F(7,4),F(3,4),1,0,0,-1,1,3),
            ('both-first-target',F(3,2),F(3,2),F(1,2),F(3,2),F(3,4),F(7,4),1,1,0,1,0,1)]
    records=[];contacts=0
    for name,*args in inputs:
        P,n,trimmed,Q=construct(*args);contacts+=n
        records.append({'name':name,'path':[[str(x),str(y)] for x,y in P],'contacts':n,'trimmed_at_earlier_target':trimmed,'period':Q})
    assert records[-1]['trimmed_at_earlier_target']
    sources=['unequal-depth/cap-chart-screen.py','unequal-depth/cap-chart-screen.json','arbitrary-endpoints-independent/check.py']
    pins={n:hashlib.sha256((BASE/n).read_bytes()).hexdigest() for n in sources}
    pins['unequal-depth-independent/cap-sheet-check.py']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    out={'status':'PASS','prescribed_actual_paths':len(records),'wall_contacts':contacts,'early_target_prefix_fixture':True,'source_sha256':pins,'records':records,'limits':'Conditional cap-sheet sufficiency controls and rational-period identities only. No exhaustive coverage, discovery, darkness or peer-code execution.'}
    (HERE/'cap-sheet-check.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()
