import json,glob,numpy as np
from collections import Counter
exec(open('/tmp/radius.py').read().split('out=[]')[0])
cr=Counter();cp=Counter();share=[]
for f in sorted(glob.glob('certs/funcs-parity-*-R12.json')):
 tag=f.split('funcs-')[1].replace('-R12.json','')
 G,C,R,target=load(tag);room=json.load(open(f'certs/{tag}.json'));s,t=room['marked']
 near=np.array([min(max(abs(r['corner'][0]-m[0]),abs(r['corner'][1]-m[1])) for m in (s,t))<=1 for r in R])
 P=proj(G,C);M=P[near];share.append(near.mean())
 cr[rank(M)-target]+=1;cp[pos(M)]+=1
print('events at the 8 lattice points around a mark: mean share %.2f'%np.mean(share))
print('rank deficit using only those',sorted(cr.items()));print('positive span using only those',cp)
