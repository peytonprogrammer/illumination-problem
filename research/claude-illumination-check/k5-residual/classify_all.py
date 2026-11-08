"""Classify every k5 SAT residual Codex has written (fixed rooms only; exact)."""
import json,sys,glob,os
sys.path.insert(0,'../reduction'); sys.path.insert(0,'../folded')
from origami_dark import decide
from exact import run
out={}
if os.path.exists('classified.json'): out=json.load(open('classified.json'))
for f in sorted(glob.glob('../../illumination-k4-codex/k5-*/cases/*/vertices.json')):
    case=f.split('/')[-2]
    j=json.load(open(f)); V=[tuple(p) for p in j['vertices']]; S,T=map(tuple,j['marked'])
    key=case+':'+json.dumps(j['vertices'])
    if key in out: continue
    d,n=decide(V,S,T,limit=3_000_000)
    rec=dict(case=case,walls=len(V),marks=[S,T],decider=d,orbit=n)
    if d!='DARK':
        r=None
        for R in (12,20,30):
            r=run(V,S,T,R=R)
            if r: break
        rec['path']=None if not r else dict(dir=list(r[0]),points=[[str(x),str(y)] for x,y in r[1]])
    out[key]=rec; print(case,len(V),'walls',d,n,'path' if rec.get('path') else '',flush=True)
json.dump(out,open('classified.json','w'),indent=1)
