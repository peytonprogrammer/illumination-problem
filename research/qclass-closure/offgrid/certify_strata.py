"""Apply the project's all-length illumination lemmas to residual position types."""
import sys
from collections import defaultdict
from pathlib import Path
sys.path.insert(0,str(next(Path(__file__).resolve().parents[2].glob('illumination-generalization*/fable/directions*/d15-small-r'))))
from lemmas import OT,arm_objects,certify_pair
from cap import cap

def classify(lines):
    candidates=defaultdict(list)
    for line in lines:
        fields=line.split()
        if fields[0]=='STRATA':
            rid,x,y,u,v=map(int,fields[1:])
            candidates[rid].append(((x,y),(u,v)))
        elif fields[0]=='ROOM':
            _,raw,_=line.split('|')
            rid=int(fields[1]);coords=list(map(int,raw.split()))
            cells=list(zip(coords[::2],coords[1::2]))
            ot=OT(1+max(x for x,y in cells),1+max(y for x,y in cells),cells)
            pairs=candidates.pop(rid,[])
            if fields[4]=='BIG':
                print(rid,'BIG');continue
            pts={z for pair in pairs for z in pair if ot.interior(z)}
            arms={z:arm_objects(ot,z) for z in pts}
            failures=[]
            for s,t in pairs:
                if s not in pts or t not in pts:continue
                if s!=t and not certify_pair(ot,s,t,arms) and not cap(cells,s,t):failures.append((s,t))
            print(rid,len(pairs),len(failures),failures[:4],flush=True)
if __name__=='__main__':classify(sys.stdin)
