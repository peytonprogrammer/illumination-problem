"""Regression checks for path validation and optimized-Python rejection."""
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'research'))

from illumination_geometry import patch
from verify_illumination_paths import verify


def witness(points, direction, bounces):
    return {
        'status': 'illuminated',
        'direction': direction,
        'bounces': bounces,
        'path': [[[value, 1] for value in point] for point in points],
    }


class VerificationTests(unittest.TestCase):
    def setUp(self):
        self.room = {
            'triangles': patch(-1, 3, -1, 1),
            'slits': [],
            'marked': [[0, 0], [2, 0]],
        }

    def test_direct_path_is_accepted(self):
        self.assertTrue(verify(self.room, witness([[0, 0], [2, 0]], [1, 0], 0)))

    def test_smooth_wall_reflection_is_accepted(self):
        path = witness([[0, 0], [1, 1], [2, 0]], [1, 1], 1)
        self.assertTrue(verify(self.room, path))

    def test_interior_bounce_is_rejected(self):
        path = witness([[0, 0], [1, 0], [2, 0]], [1, 0], 1)
        with self.assertRaisesRegex(AssertionError, 'bounce without wall'):
            verify(self.room, path)

    def test_incorrect_reflection_is_rejected(self):
        path = witness([[0, 0], [0, 1], [2, 0]], [0, 1], 1)
        with self.assertRaisesRegex(AssertionError, 'reflection law'):
            verify(self.room, path)

    def test_corner_crossing_is_rejected(self):
        # This historical fixture supplies the path that was accepted with -O;
        # it is distinct from the manuscript's strictly simple construction.
        room = json.loads((ROOT / 'research/illumination-22.json').read_text())
        source, target = room['marked']
        direction = [target[k] - source[k] for k in (0, 1)]
        with self.assertRaisesRegex(AssertionError, 'corner crossing'):
            verify(room, witness([source, target], direction, 0))

    def test_optimized_execution_is_rejected_before_verification(self):
        modules = ['illumination_geometry', 'verify_illumination_paths',
                   'illumination_sector_paths', 'illumination_decide']
        modes = [([], None), (['-O'], None), (['-OO'], None), ([], '1')]
        for module in modules:
            code = (
                f'import sys; sys.path.insert(0, {str(ROOT / "research")!r}); '
                f'import {module}'
            )
            for flags, optimization in modes:
                with self.subTest(module=module, flags=flags,
                                  PYTHONOPTIMIZE=optimization):
                    environment = os.environ.copy()
                    environment.pop('PYTHONOPTIMIZE', None)
                    if optimization is not None:
                        environment['PYTHONOPTIMIZE'] = optimization
                    result = subprocess.run(
                        [sys.executable, '-B', *flags, '-c', code],
                        cwd=ROOT, env=environment, capture_output=True, text=True,
                        timeout=15,
                    )
                    if not flags and optimization is None:
                        self.assertEqual(result.returncode, 0, result.stderr)
                    else:
                        self.assertNotEqual(result.returncode, 0)
                        self.assertIn('require enabled assertions', result.stderr)


if __name__ == '__main__':
    unittest.main()
