import sys, ast, re
from exact import run
dark=set()
for f in ['dark-k1.txt','dark-k2.txt','dark-k3.txt','dark-k4.txt']:
    for line in open(f):
        h,v=line.split('|');t=h.split()
        V=tuple(tuple(map(int,s.split(','))) for s in v.split())
        a=tuple(map(int,t[2][2:].split(',')));b=tuple(map(int,t[3][2:].split(',')))
        dark.add((V,a,b));dark.add((V,b,a))
for line in open(sys.argv[1]):
    m=re.match(r"HIT (\d+) (\[.*?\]) m (\d+) Wq (\d+) poly (\[.*?\]) pairs (\[.*?\]) lifts (\{.*\})",line)
    W,V,mm,Wq,poly,pairs,lifts=m.groups();V=tuple(ast.literal_eval(V));poly=ast.literal_eval(poly);lifts=ast.literal_eval(lifts)
    for a,b in ast.literal_eval(pairs):
        if a>b or (V,a,b) not in dark:continue
        for S in lifts[a]:
            for T in lifts[b]:
                d,P=run(poly,S,T,R=12)
                print('Wq',Wq,'base',V,'a',a,'b',b,'S',S,'T',T,'LIT' if d else 'NO-LIT-R12',d,'Q',poly,flush=True)
