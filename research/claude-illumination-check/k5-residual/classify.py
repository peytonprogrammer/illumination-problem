import json,sys
sys.path.insert(0,'../reduction'); sys.path.insert(0,'../folded')
from origami_dark import decide
from exact import run
j=json.load(open('../../illumination-k4-codex/k5-proof-pilot/cases/I2_1_1-pair0/vertices.json'))
V=[tuple(p) for p in j['vertices']]; S,T=map(tuple,j['marked'])
print('walls',len(V),'marks',S,T)
print('decider',decide(V,S,T,limit=3_000_000))
r=run(V,S,T,R=12)
print('exact tracer R=12', 'LIT dir %s, %d bounces'%(r[0],len(r[1])-2) if r else 'no path found')
if r: print('path',[(str(x),str(y)) for x,y in r[1]])
