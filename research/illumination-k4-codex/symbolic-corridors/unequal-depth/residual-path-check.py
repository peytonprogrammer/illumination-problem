"""Physical replay of prescribed charts selected from finite-cover certificates."""
from pathlib import Path
from fractions import Fraction as F
import importlib.util,json,time,signal,hashlib
B=Path(__file__).parent

def load(name,path):
    s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
V=load('all_edge_validator',B/'corner-removal-check.py')
def clipped(P,g):
    out=[]
    def val(p):return g[0]*p[0]+g[1]*p[1]+g[2]
    for C,D in zip(P,P[1:]+P[:1]):
        c,d=val(C),val(D)
        if c>=0:out.append(C)
        if c*d<0:
            z=c/(c-d);out.append(tuple(x+z*(y-x) for x,y in zip(C,D)))
    return list(dict.fromkeys(out))
def pick(clause):
    P=[(F(0),F(0)),(F(1),F(0)),(F(1),F(1)),(F(0),F(1))]
    for g in clause['guards']:P=clipped(P,g)
    if not P:return None
    s,t=[sum(p[j] for p in P)/len(P) for j in (0,1)]
    if not (0<s<=1 and 0<t<=1):return None
    if not all(g[0]*s+g[1]*t+g[2]>0 for g in clause['guards']):return None
    return s,t

def construct(room,clause,s,t):
    a,A,b,Bb=map(F,room['rectangle']);hm=(a+A)/2;hp=(b+Bb)/2
    lc,uc=[(0,0),(1,0),(0,1),(1,1)][clause['sheet']];U=A if lc else a;W=Bb if uc else b
    info=clause['chart'];ell=info['mode'];u,eps,M,c=[info[x] for x in ['u','eps','M','c']]
    v=(u+eps*t+4*M-s)/(U+W+ell);X=lambda z:s+v*(z+U)
    cl=bool(lc and X(-hm)%2==0);cu=bool(uc and (X(ell+hp)-u)%2==0)
    start=-a if cl else -U;end=ell+b if cu else ell+W
    def Y(z):
        if z<0:return -2*hm-z if lc and z<-hm else z
        if z>ell:return 2*(ell+hp)-z-(ell-1) if uc and z>ell+hp else z-(ell-1)
        j=z%2;return j if j<=1 else 2-j
    assert V.fold(X(start))==s and Y(start)==-a
    assert V.fold(X(end)-u)==t and Y(end)==1+b
    events=[]
    for za,zb,off,add in [(-U,F(0),0,0),(F(0),F(ell),c,1),(F(ell),ell+W,u,0)]:
        za,zb=max(za,start),min(zb,end)
        if za>=zb or v==0:continue
        low,high=sorted((X(za),X(zb)))
        for j in range(((low-off)/2).__floor__()-1,((high-off)/2).__floor__()+2):
            x=F(off+2*j)
            if low<x<high:
                z=-U+(x-s)/v;assert za<z<zb
                events.append((z,add+V.fold(x-off)))
    for j in range(1,ell):events.append((F(j),1+V.fold(X(F(j))-c)))
    if lc and start<-hm<end:
        assert not cl;events.append((-hm,V.fold(X(-hm))))
    if uc and start<ell+hp<end:
        assert not cu;events.append((ell+hp,V.fold(X(ell+hp)-u)))
    events.sort();assert len({z for z,x in events})==len(events)
    path=[(s,-a)]+[(x,Y(z)) for z,x in events]+[(t,1+b)]
    target=path[-1]
    for i,(C,D) in enumerate(zip(path,path[1:])):
        w=V.sub(D,C)
        if V.cross(V.sub(target,C),w)==0:
            j=0 if w[0] else 1;tau=(target[j]-C[j])/w[j]
            if 0<tau<=1:path=path[:i+1]+[target];break
    return path,(a,b,hm,hp),{'lower_corner_trimmed':cl,'upper_corner_trimmed':cu}

def main():
    E=json.loads((B/'residual-path-effort.json').read_text())
    def timeout(*_):raise TimeoutError('original prescribed path840sdeadline')
    signal.signal(signal.SIGALRM,timeout);signal.setitimer(signal.ITIMER_REAL,max(.001,E['deadline']-time.time()))
    rooms=json.loads((B/'residual-rooms.json').read_text())['rooms'];proof=json.loads((B/'residual-optical.json').read_text());assert proof['status']=='COMPLETE_CONTINUOUS_ONE_THREE_PASS_COVER'
    checks=[]
    # Every room requiring three-pass, one actual path from its first used three-pass clause.
    # Also first/last100 one-pass rooms, including cap sheets and small endpoint clearances.
    selected=[]
    for cert in proof['certificates']:
        cs=[c for c in cert['clauses'] if c['chart']['mode']==3]
        if not cs and not (cert['room_id']<100 or cert['room_id']>=len(rooms)-100):continue
        options=cs if cs else list(reversed(cert['clauses']))
        chosen=next((c for c in options if pick(c) is not None),None)
        assert chosen is not None,('no strict control clause',cert['room_id'])
        selected.append((cert['room_id'],chosen))
    for i,clause in selected:
        s,t=pick(clause);path,params,trim=construct(rooms[i],clause,s,t);n=V.validate(path,*params)
        a,b,hm,hp=params
        rev=[(x,1-y) for x,y in reversed(path)];assert V.validate(rev,b,a,hp,hm)==n
        scaled=[(x*F(3,5),y*F(7,3)) for x,y in path];assert V.validate(scaled,a*F(7,3),b*F(7,3),hm*F(7,3),hp*F(7,3),F(3,5),F(7,3))==n
        checks.append({'room_id':i,'s':str(s),'t':str(t),'sheet':clause['sheet'],'mode':clause['chart']['mode'],'reflections':n,**trim,'path':[[str(x),str(y)] for x,y in path]})
    out={'status':'PASS_PRESCRIBED_ACTUAL_PATHS','records':checks,'physical_paths':3*len(checks),'wall_contacts':3*sum(c['reflections'] for c in checks),'effort':E,'source_sha256':{n:hashlib.sha256((B/n).read_bytes()).hexdigest() for n in ['residual-optical.json','residual-rooms.json','corner-removal-check.py']},'scope':'Prescribed controls of physical interpretation, not a substitute for quantified hand geometry or full continuous proof.'}
    (B/'residual-path-check.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='records'}))
if __name__=='__main__':main()
