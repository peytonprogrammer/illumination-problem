from pathlib import Path
import subprocess,time
root=Path(__file__).resolve().parent
start=time.time()
with (root/'all-heights-peer-review.txt').open('w') as out,(root/'all-heights-peer.log').open('w') as err:
    p=subprocess.run(['claude','-p','--model','opus','--tools','','--strict-mcp-config','--setting-sources','','--no-session-persistence'],input=(root/'all-heights-peer-prompt.txt').read_text(),text=True,stdout=out,stderr=err)
    err.write(f'\nexit_code={p.returncode}; elapsed_seconds={time.time()-start:.2f}\n')
raise SystemExit(p.returncode)
