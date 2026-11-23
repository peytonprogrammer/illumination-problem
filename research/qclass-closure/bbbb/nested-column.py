"""Apply the three-run sufficient inequality to saved d169 position types at unit gaps."""
from itertools import groupby, product
from pathlib import Path
from runpy import run_path

slab = run_path(str(Path(__file__).with_name('wall-slab.py')))


def applies(cells, source, target, axis):
    direction = 1 if target[axis] > source[axis] else -1
    if source[axis] == target[axis]:
        return False
    first = source[axis] // 2 if direction == 1 else (source[axis]-1) // 2
    last = (target[axis]-1) // 2 if direction == 1 else target[axis] // 2
    bands = range(first, last+direction, direction)
    for path in product(*(slab['intervals'](cells,axis,i) for i in bands)):
        groups = [(k,len(list(g))) for k,g in groupby(path)]
        if len(groups) != 3:
            continue
        (top,_),(middle,d),(bottom,bmax) = groups
        if not (2*top[0] < source[1-axis] < 2*top[1] and
                2*bottom[0] < target[1-axis] < 2*bottom[1]):
            continue
        if all(A[0] >= B[0] and A[1] <= B[1] and
               (A[0] == B[0] or A[1] == B[1])
               for A,B in ((top,middle),(middle,bottom))):
            if (top[1]-top[0])*bmax <= (middle[1]-middle[0])*d:
                return True
    return False


if __name__ == '__main__':
    for word, records in sorted(slab['audit'](3).items()):
        solved = total = 0
        for nx,ny,mask,_,pairs in records:
            cells = {(i,j) for j in range(ny) for i in range(nx) if mask>>(i+nx*j)&1}
            total += len(pairs)
            solved += sum(any(applies(cells,s,t,k) for s,t in ((S,T),(T,S)) for k in (0,1))
                          for S,T in pairs)
        print(word,solved,total)
