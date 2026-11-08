import json,glob,numpy as np
from collections import Counter
from scipy.optimize import linprog
exec(open('analysis/radius.py').read().split('out=[]')[0])
fails=Counter(); short=Counter(); N=0; surv=[]
for f in sorted(glob.glob('certs/funcs-parity-*-R12.json')):
 tag=f.split('funcs-')[1].replace('-R12.json','')
 G,C,R,target=load(tag);room=json.load(open(f'certs/{tag}.json'));s,t=room['marked']
 P=proj(G,C)
 def off(r,m): return (r['corner'][0]-m[0],r['corner'][1]-m[1])
 axis=np.array([any(sorted(map(abs,off(r,m)))==[0,1] for m in (s,t)) for r in R])
 if rank(P[axis])>=target and pos(P[axis]): continue
 N+=1
 # which single diagonal corner, added to axis4-both, repairs it?
 fixes=[]
 for m,name in ((s,'s'),(t,'t')):
  for d in ((1,1),(1,-1),(-1,1),(-1,-1)):
   mk=axis|np.array([off(r,m)==d for r in R])
   if rank(P[mk])>=target and pos(P[mk]): fixes.append(name+str(d))
 fails[len(fixes)>0]+=1
 # rank deficit of axis4
 short[target-rank(P[axis])]+=1
print('axis4 holdouts',N,'repaired by one extra diagonal corner',fails[True],'rank deficit histogram',sorted(short.items()))
