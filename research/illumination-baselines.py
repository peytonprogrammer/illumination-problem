import contextlib,io,runpy
from pathlib import Path
from illumination_geometry import *
base=Path(__file__).parent
with contextlib.redirect_stdout(io.StringIO()): old=runpy.run_path(str(base/'check-illumination-tiling.py'))
w=dict(triangles=old['triangles'],marked=[(0,0),(2,2)],slits=[],provenance='Integer reconstruction of Wolecki Figure 1 SVG')
save(base/'illumination-22.json',w)
# Image y axis reversed; unit grid idealizes the visibly imperfect raster drawing.
poly=[(-2,0),(-1,1),(0,1),(0,2),(1,1),(2,1),(2,2),(3,1),(3,0),(4,0),(3,-1),(2,-1),(2,-2),(1,-1),(0,-1),(0,-2),(-1,-1),(-1,0)]
ts=[t for t in patch(-2,4,-2,2) if inside((sum(p[0] for p in t)/3,sum(p[1] for p in t)/3),poly)]
w20=dict(triangles=ts,marked=[(0,0),(2,0)],slits=[[(1,0),(1,1)]],outer_polygon=poly,provenance='Idealized integer reconstruction from Bhavya1805 Wikimedia image; original coordinates unavailable')
save(base/'illumination-20.json',w20)
for name,data in [('22',w),('20',w20)]:
    try:
        result=check(data); print(name,result);draw(data,base/f'illumination-{name}-certified.png');save(base/f'illumination-{name}-check.json',result)
    except AssertionError as e: print(name,'FAIL',e);raise
