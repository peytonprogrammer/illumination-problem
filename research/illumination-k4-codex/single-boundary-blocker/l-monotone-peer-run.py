from pathlib import Path
import subprocess
b=Path(__file__).resolve().parent
p=subprocess.run(['claude','-p','--model','opus','--tools','','--strict-mcp-config','--setting-sources','','--no-session-persistence'],input=(b/'l-monotone-peer-prompt.txt').read_text(),capture_output=True,text=True)
(b/'l-monotone-peer-review.txt').write_text(p.stdout)
(b/'l-monotone-peer.log').write_text('exit '+str(p.returncode)+'\n'+p.stderr)
print('review exit',p.returncode)
