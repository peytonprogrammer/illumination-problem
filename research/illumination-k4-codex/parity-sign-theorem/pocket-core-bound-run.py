from pathlib import Path
import subprocess
b=Path(__file__).resolve().parent
p=subprocess.run(['claude','-p','--model','opus','--tools','','--strict-mcp-config','--setting-sources','','--no-session-persistence'],input=(b/'pocket-core-bound-prompt.txt').read_text(),capture_output=True,text=True)
(b/'pocket-core-bound-review.txt').write_text(p.stdout)
(b/'pocket-core-bound-review.log').write_text('exit '+str(p.returncode)+'\n'+p.stderr)
print('core-bound review exit',p.returncode)
