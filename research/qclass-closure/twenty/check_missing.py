"""Finish hard rooms with the alternate-axis or reciprocal-bin certificates."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import sys
from alternate import run,boxes_for
from pixel_finish import solve
root=Path(sys.argv[1])
def finish(status):
    d=status.parent;text=status.read_text().split()
    if (d/'pixel').exists():return
    if not int(text[text.index('failed')-1]):return
    rows=boxes_for(d/'shears')
    failing=[key for key,v in rows.items() if not(v[0][1] and v[1][1])]
    if len(failing)<=12:
        run(root,d)
        if all((d/'alternate'/'_'.join(map(str,key))/'axis').exists() for key in failing):return
    solve(root,d)
if __name__=='__main__':
    with ThreadPoolExecutor(2) as ex:list(ex.map(finish,sorted((root/'hard').glob('*-*/status'))))
