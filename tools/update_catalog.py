#!/usr/bin/env python3
"""Generate the data catalog, snapshot counts, and result index from current records."""
import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def catalog_outputs():
    packages = json.loads((ROOT / 'manifests/packages.json').read_text())['packages']
    by_id = {p['id']: p for p in packages}
    if len(by_id) != len(packages):
        raise ValueError('Duplicate package ID')
    sources, members = set(), set()
    counts, sizes, package_counts = Counter(), Counter(), Counter()
    with (ROOT / 'manifests/files.jsonl').open() as stream:
        for line in stream:
            record = json.loads(line)
            source = record['source_path']
            if source in sources:
                raise ValueError('Duplicate source path: ' + source)
            sources.add(source)
            storage = record['storage']
            if storage not in {'git', 'package'}:
                raise ValueError('Unknown storage: ' + storage)
            counts[storage] += 1
            sizes[storage] += record['bytes']
            if storage == 'package':
                key = record['package'], record['member']
                if key in members or key[0] not in by_id:
                    raise ValueError('Duplicate member or unknown package: ' + source)
                members.add(key)
                package_counts[key[0]] += 1
    for package in packages:
        if package_counts[package['id']] != package['files']:
            raise ValueError('Package member count differs: ' + package['id'])
    total_bytes = sum(p['bytes'] for p in packages)
    snapshot = {
        'snapshot_date': '2026-11-08',
        'research_paths': len(sources),
        'git_research_files': counts['git'],
        'git_research_bytes': sizes['git'],
        'packaged_research_files': counts['package'],
        'package_count': len(packages),
        'compressed_package_bytes': total_bytes,
        'file_manifest': 'files.jsonl',
        'package_manifest': 'packages.json',
        'result_index': 'results.json',
    }
    data = f'''# Evidence by theorem and case

Small supporting files are directly readable under [research/](../research/README.md). Larger evidence is stored in independent case packages. Each download is a complete archive; no concatenation is required. A large case can span several packages.

| Coverage | Current value |
|---|---:|
| Research source paths | {len(sources):,} |
| Research files in Git | {counts['git']:,} |
| Research files in packages | {counts['package']:,} |
| Independent packages | {len(packages):,} |
| All packages, compressed | {total_bytes:,} bytes |

## Select evidence

```sh
python3 tools/archive.py list-data --prefix illumination-k4-codex/symbolic-corridors/
python3 tools/archive.py download --prefix illumination-k4-codex/symbolic-corridors/
python3 tools/archive.py restore --workspace /path/to/empty-workspace \\
  --prefix illumination-k4-codex/symbolic-corridors/
```

Prefixes are original research-relative paths, without `research/` or `.context/`. An exact file path also works. Only packages containing selected files are downloaded. See [reproduction](REPRODUCIBILITY.md) for dependencies, cache options, and verification.

## Packages

Expand a source area to browse its cases. Download sizes are compressed bytes.

'''
    grouped = defaultdict(list)
    for package in packages:
        grouped[package['family'].split('/')[0]].append(package)
    for family, group in sorted(grouped.items()):
        data += f'<details>\n<summary>{family}: {len(group)} packages</summary>\n\n'
        data += '| Research family or case | Download | Files | Size |\n|---|---|---:|---:|\n'
        family_counts = Counter(p['family'] for p in group)
        positions = Counter()
        for p in sorted(group, key=lambda p: (p['family'], p['name'])):
            positions[p['family']] += 1
            label = ('Download' if family_counts[p['family']] == 1 else
                     f"Package {positions[p['family']]} of {family_counts[p['family']]}")
            url = f"https://github.com/{p['repository']}/releases/download/{p['release_tag']}/{p['name']}"
            case = p['family'].removeprefix(family + '/') if p['family'] != family else '(shared evidence)'
            data += f"| `{case}` | [{label}]({url}) | {p['files']:,} | {p['bytes']:,} bytes |\n"
        data += '\n</details>\n\n'
    data += 'Package checksums are in [packages.json](../manifests/packages.json). File-level paths and hashes are in [files.jsonl](../manifests/files.jsonl); see [the manifest reference](../manifests/README.md) for field definitions.\n\nRefresh this catalog with `python3 tools/update_catalog.py`.\n'

    # Preserve curated categories and review metadata; derive descriptions and links from the inventory.
    existing = json.loads((ROOT / 'manifests/results.json').read_text())
    records = {r['id']: r for r in existing}
    text = (ROOT / 'RESULTS.md').read_text()
    sections = re.split(r'^### (R\d{2})\. (.+)\n', text, flags=re.M)
    results = []
    for i in range(1, len(sections), 3):
        result_id, title, body = sections[i:i + 3]
        body = body.split('\n## ', 1)[0].split('<a id=', 1)[0].strip()
        if result_id not in records:
            raise ValueError('Classify the new result in manifests/results.json first: ' + result_id)
        statement, separator, source_text = body.partition('\n\nSources:')
        if not separator:
            raise ValueError('Missing Sources paragraph: ' + result_id)
        source_text = source_text.split('\n\n', 1)[0]
        links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', source_text)
        if not links:
            raise ValueError('Missing source links: ' + result_id)
        record = dict(records[result_id])
        record.update(title=title, summary=statement.split('\n\nPriority:', 1)[0].strip(),
                      source_links=[list(link) for link in links], inventory='RESULTS.md')
        results.append(record)
    if len(results) != len(records) or {r['id'] for r in results} != set(records):
        raise ValueError('Result IDs differ between RESULTS.md and manifests/results.json')
    return {
        'docs/DATA.md': data,
        'manifests/current-snapshot.json': json.dumps(snapshot, indent=2) + '\n',
        'manifests/results.json': json.dumps(results, indent=2) + '\n',
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Report stale catalogs without writing')
    args = parser.parse_args()
    changed = []
    for name, text in catalog_outputs().items():
        path = ROOT / name
        if path.read_text() != text:
            changed.append(name)
            if not args.check:
                path.write_text(text)
    if args.check and changed:
        parser.exit(1, 'Stale generated files: ' + ', '.join(changed) + '\nRun python3 tools/update_catalog.py\n')
    print('Catalogs are current.' if args.check else f'Updated {len(changed)} catalog files.')


if __name__ == '__main__':
    main()
