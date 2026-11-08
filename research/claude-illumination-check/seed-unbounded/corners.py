import json
from collections import Counter
C=Counter()
for l in open('results.jsonl'):
    r=json.loads(l); V=[tuple(v) for v in r['V']]; n=len(V)
    if sum(V[i][0]*V[(i+1)%n][1]-V[(i+1)%n][0]*V[i][1] for i in range(n))<0: V=V[::-1]
    for h in r['hits']:
        c=tuple(h['verified'][0]); i=V.index(c); a,b=V[i-1],V[(i+1)%n]
        turn=(c[0]-a[0])*(b[1]-c[1])-(c[1]-a[1])*(b[0]-c[0])
        C[('C' if (c[0]+c[1])%2 else 'B','convex' if turn>0 else 'reflex')]+=1
print(dict(C))
