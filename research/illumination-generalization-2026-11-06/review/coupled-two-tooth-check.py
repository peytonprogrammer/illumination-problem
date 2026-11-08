"""R51 bounded coupled-profile discovery. Fixed family only; exact guards retained."""
from pathlib import Path
from fractions import Fraction as Q
import itertools,json,time,datetime,importlib.util,ast
R=Path(__file__).resolve().parent
DEADLINE=datetime.datetime.fromisoformat('2026-11-07T07:43:00+00:00').timestamp()
def clock():
 if time.time()>=DEADLINE:raise TimeoutError('R51 original aggregate deadline')
def add(x,y):return tuple(a+b for a,b in zip(x,y))
def scale(x,n):return tuple(n*a for a in x)
def value(x,a,b):return x[0]*a+x[1]*b+x[2]
def make(es,et,m,n,ns,nt,k,l):
 C=(es+et)//2+m+n+2;N=6+nt-ns+2*(k+l);L=(1,1,C)
 if N<=0:return
 Y=lambda u,v:add(scale(L,u),(0,0,v*N))
 sy=Y(2+2*ns,es);ty=Y(14+2*nt,-et)
 p1=add(sy,(0,0,(2*m+1)*N))
 p2=add(add(p1,(2*N,0,0)),scale(L,-4*k))
 p3=add(p2,(0,0,2*N))
 p4=add(add(p3,(0,2*N,0)),scale(L,-4*l))
 assert p4==add(ty,(0,0,-(2*n+1)*N))
 guards=[]
 def between(x,lo,hi):guards.extend([add(x,scale(L,-lo)),add(scale(L,hi),scale(x,-1))])
 between((0,0,N),1,3)
 for x,lo,hi in [(sy,1,3),(ty,13,15),(p1,6,8),(p2,6,8),(p3,10,12),(p4,10,12)]:between(x,lo,hi)
 for j in range(m):between(add(sy,(0,0,(2*j+1)*N)),0,6)
 for j in range(1,m+1):between(add(sy,(0,0,2*j*N)),3,13)
 for j in range(n):between(add(p4,(0,0,(2*j+2)*N)),12,16)
 for j in range(n):between(add(p4,(0,0,(2*j+1)*N)),3,13)
 between(add(p2,(0,0,N)),3,13)
 far=[add(add(p1,scale(L,-6)),(N,0,0)),add(add(p3,scale(L,-10)),(0,N,0))]
 if es==3:far.append(add(add(sy,scale(L,-1)),(0,0,-2*N)))
 if et==3:far.append(add(add(ty,scale(L,-13)),(0,0,2*N)))
 return {'params':[es,et,m,n,ns,nt,k,l],'C':C,'N':N,'guards':guards,'far':far,'points':[sy,ty,p1,p2,p3,p4]}
def good(c,a,b):
 L=a+b+c['C']
 return all(value(g,a,b)>0 for g in c['guards']) and all((value(f,a,b)/L/2).denominator!=1 for f in c['far'])
def cell(c,a,b):
 L=a+b+c['C'];gs=list(c['guards'])
 for f in c['far']:
  j=(value(f,a,b)/L)//2;gs.extend([add(f,scale((1,1,c['C']),-2*j)),add(scale((1,1,c['C']),2*j+2),scale(f,-1))])
 return {**c,'cell_guards':gs}
def covers(c,box):
 a,b,A,B=box
 return all(min(value(g,x,y) for x,y in [(a,b),(a,B),(A,b),(A,B)])>0 for g in c['cell_guards'])
def construct(c,a,b):
 sp=importlib.util.spec_from_file_location('g',R/'resumed-exact-check.py');g=importlib.util.module_from_spec(sp);sp.loader.exec_module(g)
 mod=ast.parse((R/'minimal-prefix-physical-check.py').read_text());scope={'Q':Q,'g':g};exec(compile(ast.Module(body=[z for z in mod.body if isinstance(z,ast.FunctionDef) and z.name in ['events','arm']],type_ignores=[]),'own arm definitions','exec'),scope)
 es,et,m,n,ns,nt,k,l=c['params'];tau=Q(c['N'],a+b+c['C']);sy,ty,p1,p2,p3,p4=[value(p,a,b)/(a+b+c['C']) for p in c['points']]
 # Right selected arm has width2; length1 normal or3 far; physical endpoint depth1.
 def right(y,e,sg,lo):
  E=scope['events'](y-lo,sg*tau,e,2);return [(1+(r if r<=2 else 4-r),lo+g.fold(y-lo+sg*tau*r,Q(2))) for r in E]
 path=list(reversed(right(sy,es,-1,Q(1))))
 for j in range(1,2*m+2):path.append((Q(0 if j%2 else 1),sy+j*tau))
 def tooth(entry,w,lo):
  return [(-(r if r<=w else 2*w-r),lo+g.fold(entry-lo+tau*r,Q(2))) for r in scope['events'](entry-lo,tau,2*w,w)]
 path.extend(tooth(p1,a,Q(6))[1:]);path.extend([(Q(1),p2+tau),(Q(0),p3)])
 path.extend(tooth(p3,b,Q(10))[1:])
 for j in range(1,2*n+2):path.append((Q(1 if j%2 else 0),p4+j*tau))
 path.extend(right(ty,et,1,Q(13))[1:])
 V=[(0,0),(1,0),(1,1),(3,1),(3,3),(1,3),(1,13),(3,13),(3,15),(1,15),(1,16),(0,16),(0,12),(-b,12),(-b,10),(0,10),(0,8),(-a,8),(-a,6),(0,6)]
 V=[tuple(map(Q,z)) for z in V];g.simple(V)
 assert path[0]==(2,2) and path[-1]==(2,14)
 assert not any(g.on(u,v,path[-1]) for u,v in zip(path[:-2],path[1:-1]))
 return {'a':str(a),'b':str(b),'params':c['params'],'tau':str(tau),'path':path,**g.path_check(V,path)}
def main():
 clock();profiles=[]
 for args in itertools.product([1,3],[1,3],range(4),range(4),range(-5,1),range(-1,6),range(4),range(4)):
  if len(profiles)%500==0:clock()
  c=make(*args)
  if c and all(max(value(g,x,y) for x,y in [(Q(1,2),Q(1,2)),(Q(1,2),Q(2)),(Q(2),Q(1,2)),(Q(2),Q(2))])>0 for g in c['guards']):profiles.append(c)
 print('possible profiles',len(profiles),flush=True)
 cells=[];hits=[];missing=[]
 for a,b in itertools.product([Q(1,2)+Q(3*i,32) for i in range(17)],repeat=2):
  clock();c=next((c for c in profiles if good(c,a,b)),None)
  if c:
   cc=cell(c,a,b);cells.append(cc);hits.append(construct(c,a,b))
  else:missing.append([str(a),str(b)])
 print('grid hit',len(hits),'missing',len(missing),flush=True)
 (R/'coupled-two-tooth-check.json').write_text(json.dumps({'whole_goal_complete':False,'profiles':len(profiles),'grid_hits':len(hits),'missing':missing,'physical':hits,'cells':cells},indent=2,default=str)+'\n')
if __name__=='__main__':main()
