#!/usr/bin/env python3
"""Run the supported archive validation stages, stopping at the first failure."""
import argparse
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '--skip-publication', action='store_true',
        help='Explicitly skip structured-file and PDF checks requiring Poppler',
    )
    args = parser.parse_args()
    if not __debug__:
        parser.error('Validation requires enabled assertions; do not optimize Python.')
    if sys.version_info < (3, 11):
        parser.error('The supported validation environment requires Python 3.11+.')
    required = ['sh', 'zstd']
    if not args.skip_publication:
        required += ['pdftotext', 'pdfinfo']
    missing = [name for name in required if shutil.which(name) is None]
    if missing:
        parser.error('Missing tools: ' + ', '.join(missing)
                     + '. See docs/REPRODUCIBILITY.md#dependencies.')

    python = sys.executable
    stages = [
        ('Catalog consistency', [python, 'tools/update_catalog.py', '--check']),
        ('Research file integrity', [python, 'tools/archive.py', 'verify-git']),
        ('Archive and verifier regressions',
         [python, '-m', 'unittest', 'discover', '-s', 'tools', '-p', 'test_*.py']),
        ('Eight-wall controls', [python, 'tools/reproduce.py', 'eight-wall']),
        ('Affine controls', [python, 'tools/reproduce.py', 'affine']),
    ]
    if not args.skip_publication:
        stages.append(('Publication formats', [python, 'tools/check_publication.py']))
    for name, command in stages:
        print(f'\nRunning: {name}', flush=True)
        try:
            subprocess.run(command, cwd=ROOT, check=True, timeout=600)
        except subprocess.CalledProcessError as error:
            print(f'FAIL: {name} (exit {error.returncode}).', file=sys.stderr)
            return 1
        except subprocess.TimeoutExpired:
            print(f'FAIL: {name} exceeded 600 seconds.', file=sys.stderr)
            return 1
    print(f'\nPASS: {len(stages)} supported validation stages.', flush=True)
    if args.skip_publication:
        print('SKIPPED: structured-file and PDF validation (--skip-publication).')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
