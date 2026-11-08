"""Small integrity/selection tests; no research solver or network required."""
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import tarfile
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('archive', Path(__file__).with_name('archive.py'))
archive = importlib.util.module_from_spec(spec)
spec.loader.exec_module(archive)


class ArchiveTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.override = patch.object(archive, 'ROOT', self.root)
        self.override.start()
        (self.root / 'manifests').mkdir()
        self.manifest([])

    def tearDown(self):
        self.override.stop()
        archive.package_members.cache_clear()
        self.temp.cleanup()

    def manifest(self, rows, name='files.jsonl'):
        (self.root / 'manifests' / name).write_text(''.join(json.dumps(r) + '\n' for r in rows))

    def package(self, contents, extras=()):
        rows = [dict(source_path=name, storage='package', package='case.tar.zst', member=name,
                     bytes=len(data), sha256=hashlib.sha256(data).hexdigest()) for name, data in contents]
        raw = io.BytesIO()
        with tarfile.open(fileobj=raw, mode='w') as tf:
            for name, data in contents + list(extras):
                info = tarfile.TarInfo(name)
                info.size = len(data)
                tf.addfile(info, io.BytesIO(data))
        path = self.root / 'case.tar.zst'
        path.write_bytes(subprocess.check_output(['zstd', '-q', '-c'], input=raw.getvalue()))
        self.manifest(rows)
        meta = dict(id=path.name, name=path.name, files=len(rows), bytes=path.stat().st_size,
                    sha256=archive.digest(path), repository='example/research', release_tag='test')
        (self.root / 'manifests/packages.json').write_text(json.dumps(dict(packages=[meta])))
        return meta, path, rows

    def test_latest_record_overrides_location_without_duplicate_restore(self):
        self.manifest([dict(source_path='case/a.json', storage='dataset')])
        self.manifest([dict(source_path='case/a.json', storage='git')], 'files-2026-new.jsonl')
        self.assertEqual([r['storage'] for r in archive.records()], ['git'])
        self.assertEqual(len(list(archive.manifest_records())), 2)

    def test_package_integrity_and_readable_member_names(self):
        meta, path, rows = self.package([('case/formula.cnf', b'p cnf 0 0\n')])
        found = {}
        archive.read_package(meta, path, lambda r, chunks: found.update({r['member']: b''.join(chunks)}))
        self.assertEqual(found, {'case/formula.cnf': b'p cnf 0 0\n'})

    def test_unexpected_member_rejected(self):
        meta, path, _ = self.package([('case/a', b'a')], [('../escape', b'bad')])
        with self.assertRaisesRegex(ValueError, 'Unexpected'):
            archive.read_package(meta, path, archive.discard)

    def test_duplicate_member_rejected(self):
        meta, path, _ = self.package([('case/a', b'a')], [('case/a', b'a')])
        with self.assertRaisesRegex(ValueError, 'duplicate'):
            archive.read_package(meta, path, archive.discard)

    def test_bad_member_hash_is_not_installed(self):
        meta, path, rows = self.package([('case/a', b'a')])
        rows[0]['sha256'] = '0' * 64
        self.manifest(rows)
        with patch.object(archive, 'package_file', return_value=path):
            with self.assertRaisesRegex(ValueError, 'hash mismatch'):
                archive.restore(self.root / 'restore', rows, self.root / 'cache')
        self.assertFalse((self.root / 'restore/.context/case/a').exists())

    def test_restore_only_selected_package_members(self):
        meta, path, rows = self.package([('case/a', b'a'), ('other/b', b'b')])
        with patch.object(archive, 'package_file', return_value=path) as download:
            archive.restore(self.root / 'restore', rows[:1], self.root / 'cache')
        self.assertEqual(download.call_count, 1)
        self.assertEqual((self.root / 'restore/.context/case/a').read_bytes(), b'a')
        self.assertFalse((self.root / 'restore/.context/other/b').exists())

    def test_git_only_restore_needs_no_data_download(self):
        source = self.root / 'research/case/check.py'
        source.parent.mkdir(parents=True)
        source.write_bytes(b'pass\n')
        rows = [dict(source_path='case/check.py', storage='git', path='research/case/check.py',
                     bytes=5, sha256=archive.digest(source))]
        (self.root / 'manifests/packages.json').write_text('{"packages":[]}')
        with patch.object(archive, 'package_file', side_effect=AssertionError('network')):
            archive.restore(self.root / 'restore', rows, self.root / 'cache')
        self.assertEqual((self.root / 'restore/.context/case/check.py').read_bytes(), b'pass\n')

    def test_corrupt_cache_is_not_silently_replaced(self):
        meta, path, _ = self.package([('case/a', b'a')])
        path.write_bytes(b'corrupt')
        with self.assertRaisesRegex(ValueError, 'Cached package'):
            archive.package_file(meta, self.root, download=True)

    def test_restore_refuses_existing_workspace(self):
        (self.root / 'occupied').mkdir()
        (self.root / 'occupied/user-file').write_text('keep')
        with self.assertRaisesRegex(ValueError, 'must be empty'):
            archive.restore(self.root / 'occupied', [], self.root / 'cache')

    def test_traversal_rejected(self):
        for name in ['../outside', '/absolute', 'case/../../outside']:
            with self.assertRaisesRegex(ValueError, 'Unsafe'):
                archive.safe_path(self.root, name)


if __name__ == '__main__':
    unittest.main()
