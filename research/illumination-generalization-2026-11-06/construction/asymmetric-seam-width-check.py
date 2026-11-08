from pathlib import Path
from fractions import Fraction as F
from datetime import datetime,timezone
from math import floor,ceil
import ast,json
R=Path(__file__).resolve().parent;E=json.loads((R/'seam-width-rigidity-effort.json').read_text())
def alive():assert datetime.now(timezone.utc)<datetime.fromisoformat(E['deadline'])
def clip(ints,a,b,lo,hi):
 if a==0:return ints if lo<b<hi else[]
 x,y=sorted(((F(lo)-b)/a,(F(hi)-b)/a));return [(max(p,x),min(q,y)) for p,q in ints if max(p,x)<min(q,y)]
def avoid(ints,a,b,lo,hi):
 x,y=sorted(((F(lo)-b)/a,(F(hi)-b)/a));out=[]
 for p,q in ints:
  if q<=x or p>=y:out.append((p,q))
  else:
   if p<x:out.append((p,x))
   if y<q:out.append((y,q))
 return out
h,d,G,t=3,1,11,8;ys=(3,6);left=[(3,5),(6,8),(17,19),(14,16)];right=[(1,3),(7,9),(19,21),(13,15)]
results=[]
for tooth in (0,1):
 cs=[]
 for tc in (t,2*G-t):
  H=(tc-2)//2
  for Y in (ys[tooth],2*G-ys[tooth]-2):
   if Y>=tc+1:continue
   for es in(0,2):
    for et in(0,2):
     for ns in ((0,) if es==0 else range(-6,1)):
      for nt in ((0,) if et==0 else range(0,7)):
       alive();C=2+2*ns;B=tc+2*nt;pre0=clip([(F(0),F(7))],es,C,1,3);pre0=clip(pre0,-et,B,tc-1,tc+1)
       if not pre0:continue
       for l in range(1,25):
        pre=clip(pre0,es+2*l-1,C,Y,Y+2)
        if not pre:continue
        for j in range(1,2*l-1):
         for a,b in(left if j%2 else right):pre=avoid(pre,es+j,C,a,b)
         pre=avoid(pre,es+j,C,G,G)
         if not pre:break
        if not pre:continue
        for r in range(1,25):
         alpha=F(es-et,2)+l-r;K=H+2+ns+nt-Y
         if alpha==0 and K%2==0:continue
         ints=clip(pre,-et-2*r+1,B,Y,Y+2)
         if not ints:continue
         for j in range(1,2*r-1):
          for a,b in(left if j%2 else right):ints=avoid(ints,-et-j,B,a,b)
          ints=avoid(ints,-et-j,B,G,G)
          if not ints:break
         if es or et:
          for odd in range(1,8,2):ints=avoid(ints,1,0,odd,odd)
         for lo,hi in ints:
          den0=F(es+et,2)+l+r-1;need=F(4 if alpha else 2)/(hi-lo);N=max(1,floor(need-den0)+1)
          assert N+den0>need
          cs.append({'es':es,'et':et,'ns':ns,'nt':nt,'virtual_depth':F(es+et,2),'n':F(nt-ns,2),'l':l,'r':r,'lo':lo,'hi':hi,'w_min':N,'H':H,'Y':Y,'target_copy':tc,'G':G,'alpha':alpha,'phase0':K})
 cs.sort(key=lambda v:(v['w_min'],v['l']+v['r'],v['es']+v['et']))
 target={'tooth':tooth,'best':cs[0],'intervals':cs};results.append(target)
# Independently derived exact 1D width-cell test; only its own function definition is reused.
src=(R/'continuous-seam-width-check.py').read_text();tree=ast.parse(src);node=next(z for z in tree.body if isinstance(z,ast.FunctionDef) and z.name=='continuous');fn=ast.get_source_segment(src,node).replace("alpha=v['l']-v['r'];K=H+2-v['Y']", "alpha=v['alpha'];K=v['phase0']");g={'F':F,'floor':floor,'ceil':ceil,'alive':alive};exec(fn,g)
checks=[g['continuous'](target) for target in results]
alive();out={'status':'EXACT_CONTINUOUS_ASYMMETRIC_ARM_TEST','room':'A1h3d1 actualseams selectedwidth1 arbitraryREALoppositewidths','profile_families':results,'continuous_results':checks,'bounded_profile_generation':{'slope_upper':7,'l_r_upper_exclusive':25,'phase_offsets':[-6,6]},'original_deadline':E['deadline'],'finished_utc':datetime.now(timezone.utc).isoformat(),'discovery':True,'actual_path_validation_pending':True,'darkness_claimed':False,'whole_goal_complete':False};(R/'asymmetric-seam-width-check.json').write_text(json.dumps(out,indent=2,default=str)+'\n');print(json.dumps({'status':out['status'],'continuous_results':checks,'finished_utc':out['finished_utc']},indent=2,default=str))
