"""Specialize the independent cell-growth census to exactly eight reflex vertices."""
from pathlib import Path
import sys
base=Path(__file__).resolve().parent
s=(base.parent/'independent.c').read_text()
s=s.replace('marks=0','reflex=0').replace('marks+=mask==15','reflex+=__builtin_popcount((unsigned)mask)==3').replace('marks>=2','reflex==8')
assert 'marks' not in s
Path(sys.argv[1]).write_text(s)
