"""Draw two exact, already-proved optical constructions. No ray search."""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import runpy

from reportlab.graphics.shapes import Drawing, Line, Polygon, PolyLine, String, Circle, Rect
from reportlab.graphics import renderPDF, renderSVG
from reportlab.lib.colors import HexColor
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen.canvas import Canvas
from shapely.geometry import Polygon as GeoPolygon, LineString, box
from shapely.ops import unary_union

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
WORKSPACE = ROOT.parents[1]
PDF = WORKSPACE / 'output/pdf/illumination-diagrams.pdf'
INK = '#18232F'
BLUE = '#1264A3'
MUTED = '#536474'
PALE = '#E7F0F8'
LIGHT = '#F4F6F8'
GRAY = '#8694A1'


def text(scene, x, y, words, size=11, color=INK, bold=False, anchor='start'):
    scene.add(String(x, y, words, fontName='Helvetica-Bold' if bold else 'Helvetica',
                     fontSize=size, fillColor=HexColor(color), textAnchor=anchor))


def paragraph(scene, x, y, words, width=516, size=11, leading=16, color=INK):
    line = ''
    for word in words.split():
        candidate = (line + ' ' + word).strip()
        if line and stringWidth(candidate, 'Helvetica', size) > width:
            text(scene, x, y, line, size=size, color=color)
            y -= leading
            line = word
        else:
            line = candidate
    if line:
        text(scene, x, y, line, size=size, color=color)
    return y - leading


def line(scene, a, b, color=INK, width=1, dash=None):
    shape = Line(*map(float, (*a, *b)), strokeColor=HexColor(color), strokeWidth=width)
    if dash:
        shape.strokeDashArray = dash
    scene.add(shape)


def polygon(scene, points, fill=None, stroke=None, width=1, dash=None):
    shape = Polygon([float(v) for p in points for v in p],
                    fillColor=HexColor(fill) if fill else None,
                    strokeColor=HexColor(stroke) if stroke else None, strokeWidth=width)
    if dash:
        shape.strokeDashArray = dash
    scene.add(shape)


def ray(scene, points, arrows=True, width=1.75):
    points = [tuple(map(float, p)) for p in points]
    scene.add(PolyLine([v for p in points for v in p], strokeColor=HexColor(BLUE),
                       strokeWidth=width, fillColor=None, strokeLineJoin=1))
    if not arrows:
        return
    for a, b in zip(points, points[1:]):
        dx, dy = b[0] - a[0], b[1] - a[1]
        length = (dx * dx + dy * dy) ** .5
        if length < 31:
            continue
        ux, uy = dx / length, dy / length
        tip = (a[0] + .58 * dx, a[1] + .58 * dy)
        base = (tip[0] - 6 * ux, tip[1] - 6 * uy)
        polygon(scene, [tip, (base[0] - 2.25 * uy, base[1] + 2.25 * ux),
                        (base[0] + 2.25 * uy, base[1] - 2.25 * ux)], fill=BLUE)


def page(title, subtitle, number):
    d = Drawing(612, 792)
    d.add(Rect(0, 0, 612, 792, fillColor=HexColor('#FFFFFF'), strokeColor=None))
    text(d, 48, 752, 'ILLUMINATION  /  REFLECTION DIAGRAMS', 9, MUTED)
    text(d, 48, 716, title, 22, bold=True)
    paragraph(d, 48, 692, subtitle, size=11, color=MUTED)
    line(d, (48, 44), (564, 44), '#DCE2E7', .7)
    text(d, 48, 27, 'All displayed paths use exact coordinates.', 9, MUTED)
    text(d, 564, 27, f'{number} / 2', 9, MUTED, anchor='end')
    return d


def pocket_page():
    d = page('A different pocket, the same exit',
             'Three reflections in a triangle can be replaced by one in a square.', 1)
    u, slope = F(1, 4), F(1, 4)
    triple = [(F(2, 5), -F(3, 5)), (F(0), -F(1, 2)), (F(2, 3), -F(1, 3))]
    entry, exit = (u, F(0)), (u + 2 * slope, F(0))
    incoming = (F(3, 20), F(2, 5))
    outgoing = (F(17, 20), F(2, 5))
    for ox, square in ((74, False), (354, True)):
        oy, scale = 566, 150
        t = lambda p: (ox + scale * float(p[0]), oy + scale * float(p[1]))
        text(d, ox + 75, 641, 'SQUARE: 1 REFLECTION' if square else 'TRIANGLE: 3 REFLECTIONS',
             11, bold=True, anchor='middle')
        if square:
            polygon(d, [t(p) for p in ((0, 0), (1, 0), (1, -1), (0, -1))], fill='#FFFFFF')
            polygon(d, [t(p) for p in ((0, -1), (1, -1), (1, 0))], fill=PALE)
            walls = [((0, 0), (0, -1)), ((0, -1), (1, -1)), ((1, -1), (1, 0))]
            path = [incoming, entry, (u + slope, -1), exit, outgoing]
        else:
            polygon(d, [t(p) for p in ((0, 0), (1, 0), (0, -1))], fill=LIGHT)
            walls = [((0, 0), (0, -1)), ((0, -1), (1, 0))]
            path = [incoming, entry, *triple, exit, outgoing]
        for a, b in walls:
            line(d, t(a), t(b), width=1.8)
        line(d, t((0, 0)), t((1, 0)), GRAY, 1, (4, 3))
        ray(d, list(map(t, path)))
        for mark, p, offset in (('E', entry, (-12, 7)), ('F', exit, (7, 7))):
            x, y = t(p)
            d.add(Circle(x, y, 2.7, fillColor=HexColor(INK), strokeColor=None))
            text(d, x + offset[0], y + offset[1], mark, 10, bold=True)
        text(d, ox + 75, 389, 'Same opening', 10, MUTED, anchor='middle')
    line(d, (48, 358), (564, 358), '#DCE2E7', .7)
    text(d, 48, 330, 'Same entry, same exit, same directions', 14, bold=True)
    y = paragraph(d, 48, 307,
                  'Both rays enter at E = (1/4, 0) and leave at F = (3/4, 0). '
                  'The pale triangle completes the square; its old diagonal wall is removed.', size=11)
    d.add(Rect(48, 171, 516, 91, rx=5, ry=5, fillColor=HexColor(LIGHT), strokeColor=None))
    text(d, 64, 239, 'The general return rule', 12, bold=True)
    text(d, 64, 218, 'Entry (u, 0), direction (d, -1)  ->  exit (u + 2d, 0), direction (d, 1).', 10.6)
    text(d, 64, 195, 'Conditions: 0 < u < 1 and 0 < u + 2d < 1.', 10.6)
    paragraph(d, 48, 143,
              'Only the part of the path inside the pocket changes. Every later segment '
              'can stay exactly as it was. These conditions keep all reflection points away from corners.',
              size=11)
    return d


def geometry_lines(geometry):
    if geometry.is_empty:
        return
    if geometry.geom_type in ('LineString', 'LinearRing'):
        yield list(geometry.coords)
    elif hasattr(geometry, 'geoms'):
        for item in geometry.geoms:
            yield from geometry_lines(item)


def room_page():
    source = ROOT / 'first-surplus-review/bottom-residual-check.json'
    raw = source.read_bytes()
    receipt = json.loads(raw)
    assert receipt['status'] == 'PASS' and receipt['reflections'] == 6
    path = [tuple(F(*v) for v in p) for p in receipt['path']]
    cap_options = json.loads((ROOT / 'zero-surplus-L/guard-incidence-check.json').read_text())['cap_options']
    core = unary_union([box(-1, -1, 1, 1), box(1, -1, 3, 1), box(1, 1, 3, 3)])
    required_names = ('B-', 'B+', 'T-', 'L+', 'E-')
    required = unary_union([core] + [GeoPolygon(cap_options[n]) for n in required_names])
    options = {'D1': 'D-', 'D2': 'D+', 'R1': 'R-', 'R2': 'R+', 'N1': 'Nb+', 'N2': 'Nr-'}
    portals = []
    for n in options.values():
        portals.append(required.boundary.intersection(GeoPolygon(cap_options[n]).boundary))
    constant_walls = required.boundary.difference(unary_union(portals))
    # Exact optical implications are rechecked independently of the drawing geometry.
    checker = runpy.run_path(str(ROOT / 'lower-bound-proof-audit/full-replay/guard-checker.py'))
    needed, absent = checker['path_requirements'](path)
    base_tiles = frozenset().union(*(checker['incident']((F(x), F(y)))
                                  for x, y in ((0, 0), (2, 0), (2, 2))))
    canonical = lambda t: tuple(sorted(map(tuple, t)))
    fixed = base_tiles | frozenset(canonical(cap_options[n]) for n in required_names)
    assert needed <= fixed and not absent & fixed
    assert all(canonical(cap_options[n]) not in absent for n in options.values())
    assert required.geom_type == 'Polygon' and len(required.interiors) == 0
    d = page('Six reflections reach the target',
             'The blue path is unchanged by every allowed gray attachment shown here.', 2)
    ox, oy, scale = 210, 405, 55
    t = lambda p: (ox + scale * float(p[0]), oy + scale * float(p[1]))
    polygon(d, list(map(t, required.exterior.coords)), fill=LIGHT)
    for n in ('B-', 'B+', 'T-'):
        polygon(d, list(map(t, cap_options[n])), fill=PALE)
    for label, n in options.items():
        triangle = GeoPolygon(cap_options[n])
        polygon(d, list(map(t, triangle.exterior.coords)), fill='#EEF0F2', stroke=GRAY, width=.9, dash=(3, 2))
        x, y = t(triangle.centroid.coords[0])
        text(d, x, y - 2, label, 8, MUTED, anchor='middle')
    for segment in geometry_lines(constant_walls):
        for a, b in zip(segment, segment[1:]):
            line(d, t(a), t(b), width=1.6)
    for a, b in (((1, -1), (1, 1)), ((1, 1), (3, 1))):
        line(d, t(a), t(b), '#D2D9DF', .65)
    ray(d, list(map(t, path)), width=1.6)
    for name, p, offset in (('S', path[0], (-18, -4)), ('T', path[-1], (11, -3))):
        x, y = t(p)
        d.add(Circle(x, y, 3.4, fillColor=HexColor(INK), strokeColor=HexColor('#FFFFFF'), strokeWidth=.6))
        text(d, x + offset[0], y + offset[1], name, 12, bold=True)
    positions = {1: (180, 480), 2: (148, 317), 3: (277, 326),
                 4: (273, 635), 5: (348, 618), 6: (311, 656)}
    for i, p in enumerate(path[1:-1], 1):
        x, y = t(p)
        d.add(Circle(x, y, 2.5, fillColor=HexColor('#FFFFFF'), strokeColor=HexColor(BLUE), strokeWidth=1))
        lx, ly = positions[i]
        line(d, (x, y), (lx + 3, ly - 3), GRAY, .55)
        text(d, lx, ly, str(i), 10, BLUE, bold=True)
    text(d, 216, 275, 'Centered bottom pocket', 10, MUTED, anchor='middle')
    line(d, (48, 251), (564, 251), '#DCE2E7', .7)
    text(d, 48, 227, '1 at the source roof  +  2 in the bottom pocket  +  3 in the top pocket', 11.2, bold=True)
    y = paragraph(d, 48, 206,
                  'S = (0, 0), T = (2, 2). Launch in direction (-1, 6). '
                  'All six hits are inside wall segments; the path avoids every corner.', size=10.8)
    text(d, 48, 161, 'Reading the gray triangles', 11.5, bold=True)
    y = paragraph(d, 48, 143,
                  'These are alternative additions, not a completed boundary. Choose at most one '
                  'triangle at D and at R; do not combine D2 with R1. Any subset of the N pair is allowed.',
                  size=10.2, leading=14)
    paragraph(d, 48, y - 3,
              'Adding a gray triangle removes its shared dashed edge. None of the six reflections '
              'uses those edges. The required side pockets and exposed source roof come from the family proof.',
              size=10.2, leading=14)
    return d, {'fixed_room_area': required.area, 'fixed_room_simple': required.is_valid,
               'optical_receipt_sha256': hashlib.sha256(raw).hexdigest(),
               'exact_required_tiles_in_drawn_base': True,
               'all_optional_triangles_avoid_forbidden_tiles': True,
               'optional_rule': 'At most one D, at most one R; not D2 and R1; any subset of N.',
               'source': [0, 0], 'target': [2, 2], 'reflections': 6}


def main():
    PDF.parent.mkdir(parents=True, exist_ok=True)
    first = pocket_page()
    second, qa = room_page()
    for name, drawing in (('pocket-exchange', first), ('six-reflection', second)):
        renderSVG.drawToFile(drawing, str(HERE / (name + '.svg')))
    c = Canvas(str(PDF), pagesize=(612, 792), pageCompression=1)
    c.setTitle('Reflection diagrams: pocket exchange and a six-reflection path')
    c.setAuthor('Daniel Wang and Peyton Wang')
    for drawing in (first, second):
        renderPDF.draw(drawing, c, 0, 0)
        c.showPage()
    c.save()
    qa.update({'pdf': str(PDF), 'pages': 2, 'render_review': 'pending',
               'scope': 'Illustrations of accepted local exchange and one family path; not a standalone full theorem proof.'})
    (HERE / 'qa.json').write_text(json.dumps(qa, indent=2) + '\n')
    print(json.dumps(qa, indent=2))


if __name__ == '__main__':
    main()
