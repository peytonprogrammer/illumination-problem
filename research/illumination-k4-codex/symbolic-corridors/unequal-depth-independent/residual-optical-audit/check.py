"""Replay frozen finite optical clauses with own guards and exact closed clips.
Prescribed certificate verification; no candidate/room/direction discovery.
"""
from fractions import Fraction as F
from pathlib import Path
from math import gcd,lcm
from importlib.util import spec_from_file_location,module_from_spec
import hashlib,json,time
HERE=Path(__file__).resolve().parent;REVIEW=HERE.parent;BASE=REVIEW.parent;PEER=BASE/'unequal-depth'
def load(name,path):
    sp=spec_from_file_location(name,path);m=module_from_spec(sp);sp.loader.exec_module(m);return m
H=load('own_frozen_integer_geometry',REVIEW/'finite-support-audit/check.py')
T=load('own_three_pass_template',REVIEW/'three-pass-check.py')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def guards(U,V,chart):
    mode=chart['mode'];assert mode in (1,3)
    u,c,eps,M=chart['u'],chart['c'],chart['eps'],chart['M'];assert u in (0,2) and c in (1,3) and eps in (-1,1)
    D=lcm(U.denominator,V.denominator);p=int(U*D);r=int(V*D);q=p+r+mode*D
    assert gcd(p,r,D)==1 and 0<=M<q
    pairs=[(0,1 if c==1 else 2,chart['shifts'][0]),(mode,{(0,1):1,(0,3):2,(2,1):0,(2,3):3}[u,c],chart['shifts'][1])]
    if mode==3:
        assert len(chart['inner'])==2
        for j,(lo,k) in enumerate(chart['inner'],start=1):
            assert lo in ((2,3) if c==1 else (0,1));pairs.append((j,lo,k))
    result=[]
    for j,lo,k in pairs:
        assert isinstance(k,int)
        n=p+j*D;aa=q-n;bb=eps*n;cc=n*(u+4*M)
        result.extend(((aa,bb,cc-q*(lo+4*k)),(-aa,-bb,q*(lo+1+4*k)-cc)))
    return tuple(result),q
def representative(gs):
    poly=H.DOMAIN
    for g in gs:poly=H.clip(poly,g)
    if not poly:return None
    s=sum(F(x,w) for x,y,w in poly)/len(poly);t=sum(F(y,w) for x,y,w in poly)/len(poly)
    if not (0<s<=1 and 0<t<=1 and all(g[0]*s+g[1]*t+g[2]>0 for g in gs)):return None
    return s,t
def main():
    names=['residual-optical.json','residual-optical.py','residual-optical-proof.md','residual-rooms.json','full-join.md']
    pins={n:sha(PEER/n) for n in names}
    source=json.loads((PEER/'residual-optical.json').read_text());rooms=json.loads((PEER/'residual-rooms.json').read_text())['rooms']
    assert source['status']=='COMPLETE_CONTINUOUS_ONE_THREE_PASS_COVER'
    assert source['input_sha256']==pins['residual-rooms.json']
    records=source['certificates'];assert len(records)==len(rooms)==22538
    assert [r['room_id'] for r in records]==list(range(len(rooms)))
    started=time.time();clausecount=guardcount=mode3rooms=0;controls=[];seen=set();summaries=[]
    for room,record in zip(rooms,records):
        a,A,b,B=map(F,room['rectangle']);pairs=((a,b),(A,b),(a,B),(A,B));pieces=[H.DOMAIN];three=False
        for clause in record['clauses']:
            si=clause['sheet'];assert isinstance(si,int) and 0<=si<4
            U,V=pairs[si];gs,q=guards(U,V,clause['chart'])
            assert gs==tuple(tuple(x) for x in clause['guards']),(room['id'],clause)
            chart=clause['chart'];three|=chart['mode']==3
            nxt={}
            for poly in pieces:
                for pp in H.subtract(poly,gs):nxt[tuple(sorted(set(pp)))]=pp
            pieces=list(nxt.values());clausecount+=1;guardcount+=len(gs)
            key=(chart['mode'],si,chart['u'],chart['eps'],chart['c'],tuple(x[0] for x in chart.get('inner',[])))
            if key not in seen and (sample:=representative(gs)) is not None:
                s,t=sample;v=(F(chart['u'])+chart['eps']*t+4*chart['M']-s)/(U+V+chart['mode']);E=s+U*v
                if chart['mode']==1:aux,_=T.G.chart_path(F(1),F(1),U,V,s,t,chart['M'],F(chart['c']),F(chart['u']),chart['eps'])
                else:aux=T.path(U,V,s,t,v,E,chart['u'],chart['c'])
                control=T.O.transfer(aux,a,b,(a+A)/2,(b+B)/2,si%2,si//2)
                controls.append({'room_id':room['id'],'chart':chart,'s':str(s),'t':str(t),**control});seen.add(key)
        assert not pieces,('published cover has admissible remainder',room['id'],pieces)
        mode3rooms+=three;summaries.append([room['id'],len(record['clauses']),three])
        if (room['id']+1)%500==0:
            progress={'rooms_verified':room['id']+1,'clauses_verified':clausecount,'guard_identities_verified':guardcount,'mode3_rooms':mode3rooms,'physical_control_keys':len(seen),'elapsed_seconds':time.time()-started}
            (HERE/'progress.json').write_text(json.dumps(progress,indent=2)+'\n');print(json.dumps(progress),flush=True)
    assert mode3rooms==source['progress']['three_pass_needed']
    assert all(sha(PEER/n)==h for n,h in pins.items())
    out={'status':'INDEPENDENT_ALL_FINITE_CONTINUOUS_OPTICAL_CERTIFICATES_PASS','rooms':len(rooms),'clauses_verified':clausecount,'integer_guard_identities_verified':guardcount,'three_pass_required_rooms':mode3rooms,'physical_control_keys':len(seen),'actual_paths_with_reverse_and_scaling':3*len(controls),'contacts_with_reverse_and_scaling':sum(2*c['contacts']+c['reverse_contacts'] for c in controls),'elapsed_seconds':time.time()-started,'source_sha256':{'unequal-depth/'+n:h for n,h in pins.items()},'coverage_digest':hashlib.sha256(json.dumps(summaries).encode()).hexdigest(),'physical_controls':controls,'limits':'Complete finite optical cover. Whole arbitrary-real theorem additionally requires separately accepted reductions and final hand join.'}
    (HERE/'result.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ('physical_controls','source_sha256')}),flush=True)
if __name__=='__main__':main()
