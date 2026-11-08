from pathlib import Path
import os,signal,subprocess,sys,time,json
HERE=Path(__file__).resolve().parent
E=json.loads((HERE/'effort.json').read_text());remaining=E['deadline_epoch']-time.time()
assert remaining>0,'original setup deadline spent'
with (HERE/'run.log').open('w') as log:
    p=subprocess.Popen([sys.executable,str(HERE/'audit.py')],stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
    print(json.dumps({'pid':p.pid,'original_deadline':E['deadline_epoch'],'remaining_seconds':remaining}),flush=True)
    try:code=p.wait(timeout=max(.01,E['deadline_epoch']-time.time()))
    except subprocess.TimeoutExpired:
        os.killpg(p.pid,signal.SIGTERM)
        try:p.wait(timeout=2)
        except subprocess.TimeoutExpired:os.killpg(p.pid,signal.SIGKILL);p.wait()
        code=124
out={'returncode':code,'finished_epoch':time.time(),'original_deadline':E['deadline_epoch'],'aggregate_elapsed_seconds':time.time()-E['started_epoch'],'deadline_enforced':True}
(HERE/'supervisor.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out),flush=True)
raise SystemExit(code)
