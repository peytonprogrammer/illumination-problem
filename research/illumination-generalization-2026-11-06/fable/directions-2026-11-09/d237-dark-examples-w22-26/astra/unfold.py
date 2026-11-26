"""Directions E,N,W,S. A vertex ID is the least incident abstract cell-corner index."""
import json
import subprocess
import sys
from pathlib import Path
from time import process_time

HERE = Path(__file__).resolve().parent
STAGES = HERE.parent.parent
def build(cells, selected=None):
    components = {}
    dec = {}
    marks = []
    for i, (x,y,*nb) in enumerate(cells):
        for s in range(4):
            root = (i,s)
            if root in dec:
                continue
            stack = [root]
            corners = {root}
            edges = 0
            while stack:
                cell, quadrant = stack.pop()
                for mask, direction in ((1,0 if quadrant&1 else 2),(2,1 if quadrant&2 else 3)):
                    adj = cells[cell][2+direction]
                    if adj < 0:
                        continue
                    edges += 1
                    other = (adj,quadrant^mask)
                    if other not in corners:
                        corners.add(other)
                        stack.append(other)
            cycle = len(corners)==4 and edges==8
            assert cycle or (len(corners)<=3 and edges==2*(len(corners)-1))
            label = -2 if cycle or len(corners)==2 else -1
            point = (x+(s&1), y+(s>>1))
            if cycle and (selected is None or point in selected):
                label = len(marks)
                marks.append((root,point))
            dec.update(dict.fromkeys(corners,label))
    h,v,labels=[],[],[]
    for i,(_,_,*nb) in enumerate(cells):
        for s in range(4):
            for perm,d,mask in ((h,2 if s&1 else 0,1),(v,3 if s&2 else 1,2)):
                j=nb[d]
                perm.append(4*j+s if j>=0 else 4*i+(s^mask))
            labels.append(dec[i,s])
    return marks,' '.join(map(str,[len(h),len(marks),*h,*v,*labels]))+'\n'

def control():
    data=json.loads((STAGES/'d205-census-a21/validation/PASS.json').read_text())
    left,right=data['control_problem'].split('|')
    a=list(map(int,left.split()))[1:]
    pos=list(zip(a[::2],a[1::2]))
    cells=[(x,y,*[pos.index(p) if p in pos else -1 for p in ((x+1,y),(x,y+1),(x-1,y),(x,y-1))]) for x,y in pos]
    marks,problem=build(cells,{(1,3),(3,5)})
    result=subprocess.check_output([str(HERE/'orbitr'),'10000'],input=problem,text=True).strip()
    print(marks,result)
    assert result=='FULL 2592 1 0 1'
if __name__=='__main__': control()
