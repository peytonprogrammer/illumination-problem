"""Integer dilation and exact canonical subdivision of the known 24-wall control.

No billiard trajectories are computed. Darkness transfers by similarity.
"""
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
sys.path.insert(0, str(BASE))
from illumination_geometry import patch
from illumination_transparent_bound import counts


def subdivide(room, scale):
    coarse = [tuple((scale*x, scale*y) for x, y in tri) for tri in room['triangles']]
    xs = [p[0] for tri in coarse for p in tri]
    ys = [p[1] for tri in coarse for p in tri]
    def inside(tri):
        u, v = sum(p[0] for p in tri), sum(p[1] for p in tri)
        for coarse_tri in coarse:
            cross = [(b[0]-a[0])*(v-3*a[1])-(b[1]-a[1])*(u-3*a[0])
                     for a, b in zip(coarse_tri, (*coarse_tri[1:], coarse_tri[0]))]
            if all(t >= 0 for t in cross) or all(t <= 0 for t in cross):
                return True
        return False
    fine = [tri for tri in patch(min(xs), max(xs), min(ys), max(ys)) if inside(tri)]
    assert len(fine) == scale*scale*len(coarse)
    return dict(triangles=fine, marked=[[scale*x, scale*y] for x, y in room['marked']], slits=[])


def main():
    p = BASE/'illumination-search-simple-unrestricted.json'
    room = json.loads(p.read_text())
    base_counts = counts(room)
    assert base_counts['walls'] == 24
    result = dict(status='PASS', scope='Exact geometric dilation/subdivision and count checks. Darkness is inherited by the similarity theorem, not re-tested.',
                  input_sha256=hashlib.sha256(p.read_bytes()).hexdigest(), controls=[])
    for scale in (1, 2, 3, 4):
        scaled = subdivide(room, scale)
        c = counts(scaled)
        assert c['walls'] == base_counts['walls']
        assert c['triangles'] == scale*scale*base_counts['triangles']
        c['k'] = c['interior_nonA']+c['smooth_boundary_nonA']
        result['controls'].append(dict(scale=scale, **c))
        print(json.dumps(result['controls'][-1]), flush=True)
    assert result['controls'][-1]['k'] > result['controls'][0]['k']
    (HERE/'scaling-check.json').write_text(json.dumps(result, indent=2)+'\n')


if __name__ == '__main__':
    main()
