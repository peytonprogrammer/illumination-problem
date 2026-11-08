import sys,json
sys.argv=['x','0','0']
exec(open('guard_audit.py').read().split('idx=random')[0])
from collections import Counter
C=Counter(); bad=[]
K='../../illumination-k4-codex/k5-proof-continuation/'
extra=json.load(open(K+'peer-guards.json'))
extra=extra if isinstance(extra,list) else extra.get('guards',list(extra.values()))
for name,G in (('learned',L),('peer',extra)):
    for i,g in enumerate(G):
        r=check(g); C[name+':'+('ok' if r=='ok' else 'FAIL')]+=1
        if r!='ok': bad.append((name,i,r))
print(dict(C)); print(bad[:10])
