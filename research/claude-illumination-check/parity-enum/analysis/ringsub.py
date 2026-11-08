"""Which ring-corner subsets alone give full rank and positive span? Re-analysis of R=12 certs."""
import json,glob,numpy as np
from collections import Counter
exec(open('analysis/radius.py').read().split('out=[]')[0])
subsets={
 'ring8 both marks': lambda d: d<=1,
 'axis4 both marks': lambda d: d==('axis',),
}
res=Counter(); N=0
for f in sorted(glob.glob('certs/funcs-parity-*-R12.json')):
 tag=f.split('funcs-')[1].replace('-R12.json','')
 G,C,R,target=load(tag);room=json.load(open(f'certs/{tag}.json'));s,t=room['marked']
 P=proj(G,C); N+=1
 def off(r,m): return (r['corner'][0]-m[0],r['corner'][1]-m[1])
 masks={}
 for name,ms in (('s',[s]),('t',[t]),('both',[s,t])):
  ring=np.array([any(max(map(abs,off(r,m)))==1 for m in ms) for r in R])
  axis=np.array([any(sorted(map(abs,off(r,m)))==[0,1] for m in ms) for r in R])
  diag=np.array([any(list(map(abs,off(r,m)))==[1,1] for m in ms) for r in R])
  masks['ring8-'+name]=ring; masks['axis4-'+name]=axis; masks['diag4-'+name]=diag
 for k,mk in masks.items():
  M=P[mk]; ok=rank(M)>=target and pos(M); res[k]+=ok
for k in sorted(res): print(f'{k:16s} certifies {res[k]} of {N}')
