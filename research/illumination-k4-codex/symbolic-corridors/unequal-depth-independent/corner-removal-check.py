"""Prescribed endpoint-loop trimming controls. No ray/parameter discovery.
Own constructor; only reviewer-owned exact all-edge geometry is imported.
"""
from pathlib import Path
from fractions import Fraction as F
from importlib.util import spec_from_file_location,module_from_spec
import hashlib,json
H=Path(__file__).resolve().parent;BASE=H.parent
sp=spec_from_file_location('own_frozen_geometry',BASE/'arbitrary-endpoints-independent/check.py')
G=module_from_spec(sp);sp.loader.exec_module(G)
BOX={(0,1):((1,2),(1,2)),(0,3):((2,3),(2,3)),(2,1):((1,2),(0,1)),(2,3):((2,3),(3,4))}

def construct(d,g,a,b,hm,hp,s,t,lc,uc,u,eps,M,c,scalar=F):
    A=2*hm-a if lc else a;B=2*hp-b if uc else b
    z0=-A;z1=g+B;L=u+eps*t+4*d*M;v=(L-s)/(A+g+B)
    X=lambda z:s+v*(z+A)
    def fx(z,offset=0,extra=0):return extra+G.fold(X(z)-offset,2*d)
    def Y(z):return -2*hm-z if lc and z<-hm else 2*(g+hp)-z if uc and z>g+hp else z
    def derivative(z,offset):
        r=(X(z)-offset)%(4*d);assert r!=0 and r!=2*d
        return 1 if r<2*d else -1
    cunit=(c/d).__floor__();uunit=(u/d).__floor__()
    assert c==cunit*d and u==uunit*d
    I,J=BOX[uunit,cunit]
    assert I[0]*d<X(0)%(4*d)<I[1]*d
    assert J[0]*d<X(g)%(4*d)<J[1]*d
    assert fx(0)==fx(0,c,d) and derivative(0,0)==derivative(0,c)
    assert fx(g,c,d)==fx(g,u) and derivative(g,c)==derivative(g,u)
    lowbad=bool(lc and X(-hm)%(2*d)==0)
    upbad=bool(uc and (X(g+hp)-u)%(2*d)==0)
    if lowbad:
        assert X(-a)==2*X(-hm)-s and fx(-a)==s
        z0=-a
    if upbad:
        assert X(g+b)-u==2*(X(g+hp)-u)-(eps*t+4*d*M)
        assert fx(g+b,u)==t
        z1=g+b
    assert z0<0<g<z1
    assert (fx(z0),Y(z0))==(s,-a)
    assert (fx(z1,u),Y(z1))==(t,g+b)
    events=[]
    for ya,yb,offset,extra in [(z0,scalar(0),scalar(0),scalar(0)),(scalar(0),g,c,d),(g,z1,u,scalar(0))]:
        lo,hi=sorted((X(ya),X(yb)))
        if v:
            for j in range((lo-offset)//(2*d)-1,(hi-offset)//(2*d)+2):
                xx=offset+2*d*j
                if lo<xx<hi:
                    z=(xx-s)/v-A;assert ya<z<yb
                    events.append((z,(extra+G.fold(xx-offset,2*d),Y(z))))
    if lc and not lowbad:events.append((-hm,(fx(-hm),-hm)))
    if uc and not upbad:events.append((g+hp,(fx(g+hp,u),g+hp)))
    events.sort(key=lambda e:e[0]);assert all(x[0]!=y[0] for x,y in zip(events,events[1:]))
    path=[(s,-a)]+[p for z,p in events]+[(t,g+b)]
    target=path[-1];early=False
    for i,(p,q) in enumerate(zip(path,path[1:])):
        w=G.sub(q,p);assert w!=(0,0)
        if G.cross(G.sub(target,p),w)==0:
            j=0 if w[0] else 1;tau=(target[j]-p[j])/w[j]
            if 0<tau<=1:
                early=i<len(path)-2 or tau<1;path=path[:i+1]+[target];break
    n=G.verify(path,d,g,a,b,s,t,hm,hp,scalar)
    reverse=[(x,g-y) for x,y in reversed(path)]
    reverse_target=reverse[-1];reverse_early=False
    for i,(p,q) in enumerate(zip(reverse,reverse[1:])):
        w=G.sub(q,p)
        if G.cross(G.sub(reverse_target,p),w)==0:
            j=0 if w[0] else 1;tau=(reverse_target[j]-p[j])/w[j]
            if 0<tau<=1:
                reverse_early=i<len(reverse)-2 or tau<1;reverse=reverse[:i+1]+[reverse_target];break
    reverse_n=G.verify(reverse,d,g,b,a,t,s,hp,hm,scalar)
    return {'reverse_contacts':reverse_n,'reverse_early_target_prefix':reverse_early,'lower_corner_removed':lowbad,'upper_corner_removed':upbad,'retained_virtual_start':str(z0),'retained_virtual_end':str(z1),'contacts':n,'early_target_prefix':early,'path':[[str(x),str(y)] for x,y in path]}

def main():
    # All cap choices use the SAME prescribed developed segment A=B5/2,
    # s=t1,u2,epsilon-1,M-2,c1. No trajectory is sought or optimized.
    records=[]
    for d,g,scalar,name in [(F(1),F(1),F,'unit'),(F(2,3),F(5,7),F,'rational scale'),(G.K((0,0,1,0)),G.K((0,1,0,0)),G.K,'exact radical scale')]:
        for low in ('none','smooth','corner'):
            for up in ('none','smooth','corner'):
                lc=int(low!='none');uc=int(up!='none')
                hm=g*(F(3) if low=='none' else F(3,2) if low=='smooth' else F(7,4))
                hp=g*(F(3) if up=='none' else F(3,2) if up=='smooth' else F(7,4))
                a=2*hm-F(5,2)*g if lc else F(5,2)*g
                b=2*hp-F(5,2)*g if uc else F(5,2)*g
                r=construct(d,g,a,b,hm,hp,d,d,lc,uc,2*d,-1,-2,d,scalar)
                assert r['lower_corner_removed']==(low=='corner')
                assert r['upper_corner_removed']==(up=='corner')
                r.update({'scale':name,'lower':low,'upper':up});records.append(r)
    # Zero horizontal slope, smooth caps, with early actual-target arrival.
    r=construct(F(1),F(1),F(1,2),F(3,2),F(3,4),F(7,4),F(3,2),F(3,2),1,1,F(0),1,0,F(1))
    assert not r['lower_corner_removed'] and not r['upper_corner_removed'] and r['early_target_prefix']
    r.update({'scale':'zero horizontal slope','lower':'smooth','upper':'smooth'});records.append(r)
    parent=json.loads((BASE/'unequal-depth/corner-removal-check.json').read_text())
    assert parent['status']=='PASS'
    for raw in parent['records']:
        fixture=raw['fixture'];s,t,a,b,hm,hp=map(F,fixture[:6]);lc,uc,u,eps,M,c=fixture[6:]
        r=construct(F(1),F(1),a,b,hm,hp,s,t,lc,uc,F(u),eps,M,F(c))
        assert r['path']==raw['path'] and r['contacts']==raw['contacts_after_removal']
        assert r['lower_corner_removed']==raw['lower_corner_removed']
        assert r['upper_corner_removed']==raw['upper_corner_removed']
        r.update({'scale':'peer prescribed fixture','fixture':fixture});records.append(r)
    sources=['unequal-depth/cap-corner-removal.md','unequal-depth/corner-removal-check.py','unequal-depth/corner-removal-check.json','arbitrary-endpoints-independent/check.py','unequal-depth-independent/corner-removal-check.py']
    out={'status':'PRESCRIBED_CORNER_REMOVAL_PHYSICS_PASS','prescribed_forward_paths':len(records),'actual_paths_including_reverses':2*len(records),'total_wall_contacts_including_reverses':sum(r['contacts']+r['reverse_contacts'] for r in records),'both_corner_fixtures':sum(r['lower_corner_removed'] and r['upper_corner_removed'] for r in records),'source_sha256':{r:hashlib.sha256((BASE/r).read_bytes()).hexdigest() for r in sources},'records':records,'limits':'Exact fixed formulas, rational and radical scalings, all cap flags and reversals. Universal real-parameter sufficiency requires separate hand proof. No peer code, discovery or universal portal-cover claim.'}
    (H/'corner-removal-check.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ('records','source_sha256')}))
if __name__=='__main__':main()
