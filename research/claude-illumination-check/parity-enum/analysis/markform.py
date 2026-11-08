import json,glob,numpy as np
from collections import Counter
exec(open('/tmp/radius.py').read().split('out=[]')[0])
D8=[np.array(m) for m in ([[1,0],[0,1]],[[0,-1],[1,0]],[[-1,0],[0,-1]],[[0,1],[-1,0]],[[1,0],[0,-1]],[[-1,0],[0,1]],[[0,1],[1,0]],[[0,-1],[-1,0]])]
bad=0;tot=0;classes=Counter();perclass_ok=Counter()
for f in sorted(glob.glob('certs/funcs-parity-*-R12.json')):
 tag=f.split('funcs-')[1].replace('-R12.json','')
 G,C,R,_=load(tag)
 byR={}
 for g,r in zip(G,R):
  w=np.array(r['dir'],float);gs=g[-4:-2];gt=g[-2:];tot+=1
  # expect gs = k*(w_y,-w_x) up to sign, and gt = R^T gs for some dihedral R
  perp=np.array([w[1],-w[0]])
  if abs(gs@w)>1e-9:bad+=1;continue
  found=[i for i,M in enumerate(D8) if np.allclose(gt,M.T@gs)]
  if not found:bad+=1;continue
  i=found[0];sgn=np.sign(gs@perp);byR.setdefault(i,[]).append(sgn*perp/np.linalg.norm(perp))
 # per class: do directions positively span R^2?
 ok=0
 for i,V in byR.items():
  V=np.array(V);angs=np.sort(np.arctan2(V[:,1],V[:,0]));gaps=np.diff(np.concatenate([angs,[angs[0]+2*np.pi]]))
  if gaps.max()<np.pi-1e-9:ok+=1
 classes[len(byR)]+=1;perclass_ok[ok]+=1
print('events',tot,'not of form (s-part perp w, t-part = dihedral image):',bad)
print('number of dihedral classes per room',sorted(classes.items()))
print('classes whose directions positively span R^2, per room',sorted(perclass_ok.items()))
