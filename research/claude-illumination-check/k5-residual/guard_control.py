import sys,random,copy
sys.argv=['x','3','0']
exec(open('guard_audit.py').read().split('idx=random')[0])
from collections import Counter
random.seed(7); C=Counter()
for i in random.sample(range(len(L)),200):
    g=L[i]
    a=copy.deepcopy(g); a['U']=[T for T in a['U']]; a['U'].pop(random.randrange(len(a['U'])))   # drop a U tile
    b=copy.deepcopy(g); k=random.randrange(1,len(b['path'])-1); x=b['path'][k][0]; b['path'][k][0]=[x[0]*1000+1,x[1]*1000]  # nudge a bounce
    c=copy.deepcopy(g); c['Z'].append(c['U'][0])  # contradictory tile
    C['drop-U '+('caught' if check(a)!='ok' else 'MISSED')]+=1
    C['nudge '+('caught' if check(b)!='ok' else 'MISSED')]+=1
    C['U∩Z '+('caught' if check(c)!='ok' else 'MISSED')]+=1
print(dict(C))
