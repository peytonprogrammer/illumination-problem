"""Stream eligible disc complexes through the d55 orbit decider."""
from collections import Counter
from itertools import combinations
import json
from pathlib import Path
import subprocess
from unfold import HERE, build

def main():
    counts=Counter()
    proc=None
    with open('dark.tsv','w', buffering=1) as dark, open('undecided.tsv','w', buffering=1) as pending:
        for f in (dark,pending):
            f.write('complex\tmark_a\tmark_b\tstates\tstatus\n')
        try:
            for line in open('jobs.txt'):
                area,*numbers=map(int,line.split())
                cells=[numbers[i:i+6] for i in range(0,len(numbers),6)]
                assert len(cells)==area
                marks,problem=build(cells)
                bucket='OVERLAP' if len({tuple(c[:2]) for c in cells})<area else 'TOUCHING'
                total=len(marks)*(len(marks)-1)//2
                if proc is None:
                    proc=subprocess.Popen([str(HERE/'orbitr'),'100000'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,text=True)
                try:
                    proc.stdin.write(problem)
                    proc.stdin.flush()
                    response=proc.stdout.readline().split()
                    if not response: raise BrokenPipeError()
                    status=response[0]
                    states,n,*pairs=map(int,response[1:])
                    assert status in ('ALLLIT','FULL','CAP') and len(pairs)==2*n
                    missing=list(zip(pairs[::2],pairs[1::2]))
                except BrokenPipeError:
                    proc.wait()
                    proc=None
                    status='CRASH'
                    states=-1
                    missing=list(combinations(range(len(marks)),2))
                counts[area,bucket,'lit']+=total-len(missing)
                for a,b in missing:
                    f=dark if status=='FULL' else pending
                    print(line.strip(),json.dumps(marks[a]),json.dumps(marks[b]),states,status,sep='\t',file=f)
                    counts[area,bucket,status]+=1
                if status=='FULL' and missing:
                    raise SystemExit('STOP: FULL survivor; independently reproduce')
        finally:
            if proc is not None:
                proc.stdin.close()
                proc.wait()
            with open('lighting.tsv','w') as out:
                print('area','bucket','result','pairs',sep='\t',file=out)
                for k,n in sorted(counts.items()): print(*k,n,sep='\t',file=out)
if __name__=='__main__':main()
