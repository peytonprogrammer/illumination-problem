"""Full-orbit seed density (approved fixed-room check): fraction of non-wall-parallel orbit states
with T at r^2(s) or r u r u^-1(s)."""
import sys,json,time
__file__='<SOURCE_WORKSPACE>/.context/claude-illumination-check/seed-unbounded/seedcheck.py'
ARGS=sys.argv[1:]; sys.argv=['x']; exec(open(__file__).read().split("if __name__")[0])
from collections import deque
def density(V,S,T,limit):
    r,u,lab,s0,fr=o.build(list(V),S,T); st=o.canon(r,u,lab,s0); seen={st}; Q=deque([st]); n=hit=0
    while Q:
        R,U,lab=Q.popleft(); n+=1; Ui=o.inv(U)
        if lab[R[R[0]]]=='T' or lab[R[U[R[Ui[0]]]]]=='T': hit+=1
        Ri=o.inv(R)
        for a,b in ((R,tuple(o.comp(U,Ri))),(tuple(o.comp(R,Ui)),U)):
            nn=o.canon(a,b,lab,0)
            if nn not in seen:
                seen.add(nn); Q.append(nn)
                if len(seen)>limit: return n,hit,len(seen),'CAP'
    return n,hit,len(seen),'COMPLETE'
rows=[json.loads(l) for l in open('study.jsonl')]
for r in rows[int(ARGS[0]):int(ARGS[1])]:
    t0=time.time(); n,h,sz,st=density([tuple(v) for v in r['V']],tuple(r['S']),tuple(r['T']),int(ARGS[2]))
    print(json.dumps(dict(W=r['W'],T=r['T'],pathlen=r['pathlen'],nseeds13=r['nseeds'],states=n,seed_states=h,frac=h/max(n,1),orbit=sz,status=st,secs=round(time.time()-t0))),flush=True)
