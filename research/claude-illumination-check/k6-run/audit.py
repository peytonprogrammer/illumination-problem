# Independent re-check of every guard in the listed cases with guard_audit.check.
import sys,json,os,glob
tags=sys.argv[1:]
H=os.path.dirname(os.path.abspath(__file__))
sys.argv=['x','0','0']; os.chdir(H+'/../k5-residual')
exec(open('guard_audit.py').read().split('idx=random')[0])
os.chdir(H)
for t in tags:
    n=0; bad=[]
    if not os.path.exists(f'cases/{t}/guards.jsonl'): print(json.dumps({'tag':t,'n':0,'fail':0,'first':[]}),flush=True); continue
    for i,l in enumerate(l for f in sorted(glob.glob(f'cases/{t}/guards*.jsonl')) for l in open(f)):
        r=check(json.loads(l)); n+=1
        if r!='ok': bad.append((i,r))
    print(json.dumps({'tag':t,'n':n,'fail':len(bad),'first':bad[:3]}),flush=True)
