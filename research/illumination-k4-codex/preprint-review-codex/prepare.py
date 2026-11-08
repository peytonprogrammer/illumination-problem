"""Compile the included manuscript and research note from their current sources."""
from pathlib import Path
import argparse
import subprocess

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--engine', default='tectonic')
args = parser.parse_args()
root = Path(__file__).resolve().parent
for source in ('revised.tex', 'research-brief.tex'):
    subprocess.run([args.engine, source], cwd=root, check=True)
