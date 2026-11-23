"""D103 negative control: the 22-wall room R22 has a known dark lattice pair.
The d74 certifier must leave it, and D103's tracer must find no path for it."""
import subprocess, sys
from fractions import Fraction as F
from pathlib import Path
from tracer import find_path
here = Path(__file__).resolve().parent
room = (here / '../../../../qclass-closure/r22-control.room').read_text().split('|')[0].split()
raw = list(map(int, room)); C = set(zip(raw[2::2], raw[3::2]))
out = subprocess.run([here / 'bin/cert', here / '../../../../qclass-closure/r22-control.room', '0', '8'], capture_output=True, text=True).stdout
fin = [l for l in out.splitlines() if l.startswith(('FINAL', 'PIECE'))]
print('\n'.join(fin))
dark = ((F(1), F(3)), (F(3), F(5)))
print('dark pair path (R=6):', find_path(C, *dark, 6))
