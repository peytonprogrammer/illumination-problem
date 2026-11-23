"""Retry unresolved rooms with different direction bounds. Keep row-to-room association."""
import os,subprocess,sys
from pathlib import Path
exe,source,dest,bound,force,cap=sys.argv[1:]
with open(source) as stream,open(dest,'w') as out:
    for line in stream:
        if not line.strip():continue
        p=subprocess.run([exe,bound,force,cap],input=line,text=True,capture_output=True,env={**os.environ,'COVER_ALLDIRS':'1'})
        if p.returncode:
            print('ERROR',p.returncode,p.stderr.strip(),'|',line.rstrip(),file=out,flush=True)
        else:
            print(p.stdout.strip(),file=out,flush=True)
