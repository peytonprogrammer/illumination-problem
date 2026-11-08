import json,glob,numpy as np
from scipy.optimize import linprog
from collections import Counter
exec(open('/tmp/radius.py').read().split('out=[]')[0])
res=Counter();ex=[]
for f in sorted(glob.glob('certs/funcs-parity-*-R12.json')):
 tag=f.split('funcs-')[1].replace('-R12.json','')
 G,C,R,_=load(tag);M4=G[:,-4:]  # marks only: s,t coordinates; walls and anchor fixed (closure automatically holds)
 L=np.array([max(abs(r['dir'][0]),abs(r['dir'][1])) for r in R]);kk=None
 for k in range(1,13):
  M=M4[L<=k]
  if len(M) and rank(M)==4 and pos(M):kk=k;break
 res[kk]+=1
 if kk and kk<=2 and len(ex)<3:ex.append((tag,[(r['dir'],r['corner'],r['side']) for r,l in zip(R,L) if l<=kk]))
print('mark-only certifying radius',sorted(res.items(),key=lambda x:(x[0] is None,x[0])))
for e in ex:print(e)
