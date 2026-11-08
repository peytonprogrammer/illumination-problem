import json,glob,sys,numpy as np
from scipy.optimize import linprog
def load(tag):
 f=json.load(open(f'certs/funcs-{tag}-R12.json'));R=json.load(open(f'certs/events-{tag}-R12.json'))['rows']
 G=np.array([[float(eval(x)) for x in g] for g in f['funcs']]);C=np.array([[float(eval(x)) for x in c] for c in f['clos']])
 return G,C,R,f['target']
def proj(G,C):
 Q,_=np.linalg.qr(C.T);return G-(G@Q)@Q.T
def rank(M):return 0 if len(M)==0 else np.linalg.matrix_rank(M,tol=1e-7)
def pos(M):
 # exists c>=1 with c@M = 0 ?
 if len(M)==0:return False
 r=linprog(np.zeros(len(M)),A_eq=M.T,b_eq=np.zeros(M.shape[1]),bounds=[(1,None)]*len(M),method='highs')
 return r.status==0
out=[]
for f in sorted(glob.glob('certs/funcs-parity-*-R12.json')):
 tag=f.split('funcs-')[1].replace('-R12.json','')
 G,C,R,target=load(tag);P=proj(G,C)
 k_rank=k_pos=None
 L=np.array([max(abs(r['dir'][0]),abs(r['dir'][1])) for r in R])
 for k in range(1,13):
  idx=np.where(L<=k)[0];M=P[idx]
  if k_rank is None and rank(M)>=target:k_rank=k
  if k_rank is not None and pos(M):k_pos=k;break
 out.append((tag,k_rank,k_pos,target))
from collections import Counter
print('rank radius',sorted(Counter(o[1] for o in out).items()))
print('positive radius',sorted(Counter(o[2] for o in out).items()))
json.dump(out,open('radius.json','w'))
