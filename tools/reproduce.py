#!/usr/bin/env python3
"""Run named prescribed controls in a disposable copy, without discovery searches.

This adapts historical workspace paths in the copy, never in the archive.
Passing fixed controls is not a proof of the quantified mathematical statements.
"""
import argparse
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
GENERAL = 'illumination-generalization-2026-11-06'
PACKET = GENERAL + '/fable/eight-wall-review-packet'
PRIORITY = GENERAL + '/coordination/general-proof-priority'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('suite', choices=['eight-wall', 'affine'])
    args = parser.parse_args()
    with tempfile.TemporaryDirectory(prefix='illumination-reproduce-') as directory:
        workspace = Path(directory)
        context = workspace / '.context'
        paths = [GENERAL + '/review']
        if args.suite == 'eight-wall':
            paths += [GENERAL + '/construction', PACKET,
                      'illumination-k4-codex/single-boundary-blocker',
                      'illumination-k4-codex/two-reflex-blocker']
            commands = [['sh', str(context / PACKET / 'reproduce.sh')]]
        else:
            paths += [PRIORITY + '/affine-seed-reduction', PRIORITY + '/target-fiber-peer-goals']
            commands = [[sys.executable, '-I', str(context / PRIORITY / entry)] for entry in
                        ['affine-seed-reduction/pair-transport-check.py',
                         'target-fiber-peer-goals/reviewer/diagonal-d5-control.py']]
        for relative in paths:
            source = ROOT / 'research' / relative
            target = context / relative
            shutil.copytree(source, target)
        # These substitutions are intentionally limited to archived local-path markers.
        # Numerical data and mathematical formulas are not edited.
        for path in context.rglob('*'):
            if path.is_file() and path.suffix in {'.sh', '.py', '.md', '.json'}:
                text = path.read_text()
                if '<SOURCE_WORKSPACE>' in text:
                    path.write_text(text.replace('<SOURCE_WORKSPACE>', str(workspace)))
        for command in commands:
            subprocess.run(command, cwd=workspace, check=True, timeout=60)
        print(f'PASS: {args.suite} prescribed controls; archive unchanged; no data download.')


if __name__ == '__main__':
    main()
