import json,glob,numpy as np
from scipy.optimize import linprog
exec(open('/tmp/radius.py').read().split('out=[]')[0])
rad={o[0]:o for o in json.load(open('radius.json'))}
stats=[]
for tag,kr,kp,target in list(rad.values()):
 f=json.load(open(f'certs/funcs-{tag}-R12.json'));room=json.load(open(f'certs/{tag}.json'))
 G,C,R,_=load(tag);S=np.array([[float(eval(x)) for x in s] for s in f['syms']])
 D=G.shape[1];W=D-6
 L=np.array([max(abs(r['dir'][0]),abs(r['dir'][1])) for r in R])
 M=G[np.where(L<=kp-1)[0]]
 # find delta with clos.delta=0, syms.delta=0 (orthogonal), M.delta>=0, maximize sum(M.delta), box |delta|<=1
 A_eq=np.vstack([C,S]);res=linprog(-M.sum(0),A_ub=-M,b_ub=np.zeros(len(M)),A_eq=A_eq,b_eq=np.zeros(len(A_eq)),bounds=[(-1,1)]*D,method='highs')
 d=res.x;wall=np.linalg.norm(d[2:2+W]);mark=np.linalg.norm(d[2+W:]);anchor=np.linalg.norm(d[:2])
 stats.append((tag,round(wall,3),round(mark,3),int((M@d>1e-7).sum()),len(M)))
import collections
print('surviving delta: fraction with marks fixed (mark norm<1e-6):',sum(1 for s in stats if s[2]<1e-6),'/',len(stats))
print('fraction with walls fixed:',sum(1 for s in stats if s[1]<1e-6))
print(stats[:8])
