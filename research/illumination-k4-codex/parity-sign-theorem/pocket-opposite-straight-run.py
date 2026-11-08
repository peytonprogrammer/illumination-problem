from pathlib import Path
import subprocess
b=Path(__file__).resolve().parent
p=subprocess.run(['claude','-p','--model','opus','--tools','','--strict-mcp-config','--setting-sources','','--no-session-persistence'],input=(b/'pocket-opposite-straight-prompt.txt').read_text(),capture_output=True,text=True)
(b/'pocket-opposite-straight-review.txt').write_text(p.stdout)
(b/'pocket-opposite-straight-review.log').write_text('exit '+str(p.returncode)+'\n'+p.stderr)
print('opposite straight review exit',p.returncode)
