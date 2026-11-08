#!/usr/bin/env python3
"""Check JSON, JSONL, SVG and PDF file formats.

Requires pdftotext (Poppler) for PDF text and metadata inspection. This bounded
check validates file structure and PDF readability. It does not verify
mathematical proofs.
"""
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    if not shutil.which('pdftotext') or not shutil.which('pdfinfo'):
        parser.error('Install Poppler: pdftotext and pdfinfo are required.')
    names = sorted(set(subprocess.check_output(
        ['git', 'ls-files', '--cached', '--others', '--exclude-standard', '-z'],
        cwd=ROOT).decode().split('\0')) - {''})
    findings = []
    counts = {'tracked_and_new_files': len(names), 'text_files': 0,
              'pdf_files': 0, 'svg_files': 0, 'binary_files_not_semantically_checked': 0}
    pdf_cache = {}
    for name in names:
        path = ROOT / name
        if not path.is_file():
            findings.append({'path': name, 'check': 'listed-file-missing'})
            continue
        raw = path.read_bytes()
        if path.suffix == '.pdf':
            counts['pdf_files'] += 1
            digest = hashlib.sha256(raw).hexdigest()
            if digest not in pdf_cache:
                extracted = subprocess.run(['pdftotext', '-layout', str(path), '-'], capture_output=True)
                metadata = subprocess.run(['pdfinfo', str(path)], capture_output=True)
                xmp = subprocess.run(['pdfinfo', '-meta', str(path)], capture_output=True)
                if any(p.returncode for p in (extracted, metadata, xmp)):
                    findings.append({'path': name, 'check': 'pdf-unreadable'})
                pdf_cache[digest] = b'\n'.join(p.stdout for p in (extracted, metadata, xmp)).decode('utf8', errors='replace')
            continue
        try:
            if path.suffix == '.gz':
                raw = gzip.decompress(raw)
            text = raw.decode('utf8')
            if '\0' in text:
                raise UnicodeError()
        except (UnicodeError, OSError):
            counts['binary_files_not_semantically_checked'] += 1
            continue
        counts['text_files'] += 1
        try:
            if path.suffix == '.json':
                json.loads(text)
            elif path.suffix == '.jsonl':
                for line in text.splitlines():
                    if line.strip():
                        json.loads(line)
            elif path.suffix == '.svg':
                counts['svg_files'] += 1
                ET.fromstring(text)
        except (ValueError, ET.ParseError) as error:
            findings.append({'path': name, 'check': 'invalid-' + path.suffix[1:],
                             'detail': str(error)})
    report = {'status': 'FAIL' if findings else 'PASS', 'counts': counts,
              'findings': findings, 'scope': 'current worktree; JSON, JSONL, SVG and PDF readability'}
    if args.report:
        args.report.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))
    raise SystemExit(bool(findings))


if __name__ == '__main__':
    main()
