"""Check the two standalone proofs against the fixed construction packets."""
from pathlib import Path
import hashlib
import importlib.util
import json
import re

from pypdf import PdfReader
from pypdf.generic import IndirectObject, StreamObject

ROOT = Path(__file__).resolve().parent
MARKERS = ("mailto:", "mail.google.com", "app.slack.com")


def no_external_links(value):
    if isinstance(value, bytes):
        lowered = value.lower()
        for name in MARKERS:
            for encoding in ("utf-8", "utf-16-le", "utf-16-be"):
                assert name.encode(encoding) not in lowered, "Restricted link in PDF bytes"
    else:
        assert not any(name in str(value).casefold() for name in MARKERS), "Restricted link in PDF text"


def scan_pdf_objects(reader):
    seen = set()

    def walk(obj):
        if isinstance(obj, IndirectObject):
            key = (obj.idnum, obj.generation)
            if key in seen:
                return
            seen.add(key)
            return walk(obj.get_object())
        if isinstance(obj, StreamObject):
            no_external_links(obj.get_data())
        if isinstance(obj, dict):
            for key, value in obj.items():
                no_external_links(key)
                walk(value)
        elif isinstance(obj, (list, tuple)):
            for item in obj:
                walk(item)
        elif isinstance(obj, (str, bytes)):
            no_external_links(obj)

    walk(reader.trailer)
    return len(seen)


def same_cycle(a, b):
    return len(a) == len(b) and any(
        a == cycle[i:] + cycle[:i]
        for cycle in (b, b[::-1])
        for i in range(len(cycle))
    )


spec = importlib.util.spec_from_file_location("fixed_geometry", ROOT / "check.py")
geometry = importlib.util.module_from_spec(spec)
spec.loader.exec_module(geometry)
reports = {}
for copies, filename, pages in ((3, "proof-expanded.pdf", 4), (4, "additional-example.pdf", 2)):
    packet = geometry.check(copies)
    path = ROOT / filename
    reader = PdfReader(path)
    assert len(reader.pages) == pages, "Unexpected page overflow"
    texts = [page.extract_text() for page in reader.pages]
    assert all(len(text) > 700 for text in texts), "Nearly empty page"
    text = "\n".join(texts)
    no_external_links(text)
    no_external_links(str(reader.metadata))
    no_external_links(path.read_bytes())
    objects = scan_pdf_objects(reader)
    assert "\ufffd" not in text and "\u25a0" not in text
    boundary_text = text.split(f"Cyclic coordinates of the {packet['room']['walls']}-wall boundary", 1)[1]
    printed = [tuple(map(int, p)) for p in re.findall(r"\((-?\d+),\s*(-?\d+)\)", boundary_text)]
    expected = [tuple(p) for p in packet["room"]["vertices"]]
    assert same_cycle(printed, expected), "Printed boundary differs from exact room"
    for name, fiber in packet["mark_fibers"].items():
        fiber_text = "".join(texts[-1].split())
        assert all(f"({x},{y})" in fiber_text for x, y in fiber), name
    reports[filename] = {
        "pages": pages,
        "walls": packet["room"]["walls"],
        "convex_corners": len(packet["room"]["convex"]),
        "concave_corners": len(packet["room"]["concave"]),
        "smooth_reversal_points": len(packet["reversal_points"]),
        "publication_marker_scan": "PASS: extracted text, metadata, raw bytes and reachable decoded PDF objects",
        "scanned_pdf_objects": objects,
        "boundary_and_fibers": "PASS",
        "exact_topology_and_reversal_checks": "PASS",
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
    }

for name in ("build.py", "figures.py", "proof-expanded.md"):
    no_external_links((ROOT / name).read_text())

result = {
    "status": "PASS",
    "proofs": reports,
    "scope": "Final proofreading and fixed-geometry consistency; no ray search or new theorem",
    "visual_review": "Render inspection recorded separately in proofread.md",
}
(ROOT / "proofread.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
