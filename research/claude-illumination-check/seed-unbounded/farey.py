"""Seeds whose direction is a Farey neighbor of a wall direction (approved fixed-room check).
For v in the four wall directions, test every w with |det(v,w)|=1 and |n|<=N, by exact physical walk."""
import sys,json,time,os
ARGS=sys.argv[1:]; sys.argv=['x']
__file__='<SOURCE_WORKSPACE>/.context/claude-illumination-check/seed-unbounded/seedcheck.py'
exec(open(__file__).read().split("if __name__")[0])
FAM={'h':lambda n,e:(n,e),'v':lambda n,e:(e,n),'d':lambda n,e:(n,n+e),'a':lambda n,e:(n,e-n)}
def farey(V,S,T,N):
    out={}
    for k,f in FAM.items():
        hits=[]
        for n in range(-N,N+1):
            for e in (1,-1):
                w=f(n,e)
                if (abs(w[0]),abs(w[1])) in {(1,0),(0,1),(1,1)}: continue
                r=verify(V,S,T,w)
                if r: hits.append([w,list(r[0])])
        out[k]=hits
    return out
rows=[json.loads(l) for l in open(ARGS[0])]
for r in rows[int(ARGS[1]):int(ARGS[2])]:
    t0=time.time(); V=[tuple(v) for v in r['V']]; res=farey(V,tuple(r['S']),tuple(r['T']),int(ARGS[3]))
    print(json.dumps(dict(W=len(V),S=r['S'],T=r['T'],pathlen=r.get('pathlen'),counts={k:len(v) for k,v in res.items()},first={k:v[:3] for k,v in res.items()},secs=round(time.time()-t0))),flush=True)
