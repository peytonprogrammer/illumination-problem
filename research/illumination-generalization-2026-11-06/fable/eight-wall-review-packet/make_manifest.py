#!/usr/bin/env python3
"""Recompute SHA-256 of every source in the eight-wall chain and compare with
the hashes pinned in the acceptance files. Writes dependency-manifest.json.
Run from anywhere: python3 -I make_manifest.py"""
import hashlib, json, re, sys
from datetime import datetime, timezone
from pathlib import Path

CTX = Path("<SOURCE_WORKSPACE>/.context")
G = CTX / "illumination-generalization-2026-11-06"
K = CTX / "illumination-k4-codex"


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def pinned(acceptance_file, needle):
    """Find a 64-hex hash associated with `needle` inside an acceptance JSON (any nesting)."""
    txt = (acceptance_file).read_text()
    m = re.search(r'"' + re.escape(needle) + r'"\s*:\s*"([0-9a-f]{64})"', txt)  # bare key first
    if not m:
        m = re.search(r'"[^"]*/' + re.escape(needle) + r'"\s*:\s*"([0-9a-f]{64})"', txt)
    return m.group(1) if m else None


# (role, path, acceptance file that pins it, needle used to find the pin)
ROWS = [
    ("classification: W<=8 turn words and metric normal forms (Prop 1.1-1.2)", G / "review/eight-wall-frontier.md", G / "review/eight-wall-frontier-acceptance.json", "eight-wall-frontier.md"),
    ("classification: independent reconstruction review", G / "construction/eight-wall-frontier-review.md", G / "review/eight-wall-frontier-acceptance.json", "eight-wall-frontier-review.md"),
    ("classification: prescribed combinatorial check", G / "review/eight-wall-turn-check.py", G / "review/eight-wall-frontier-acceptance.json", "eight-wall-turn-check.py"),
    ("L theorem, two orientations (Thm 2.1)", K / "single-boundary-blocker/l-monotone-proof.md", G / "review/all-real-L-dependency-acceptance.json", "l-monotone-proof.md"),
    ("L theorem: independent hand reconstruction", G / "review/all-real-L-dependency-review.md", G / "review/all-real-L-dependency-acceptance.json", "all-real-L-dependency-review.md"),
    ("L theorem: prescribed exact check", K / "single-boundary-blocker/arithmetic-check.py", G / "review/all-real-L-dependency-acceptance.json", "arithmetic-check.py"),
    ("U theorem, opposite arms and all pairs (Thm 3.1-3.2)", K / "two-reflex-blocker/all-heights.md", G / "review/all-real-U-dependency-acceptance.json", "all-heights.md"),
    ("U theorem: independent hand reconstruction", G / "review/all-real-U-dependency-review.md", G / "review/all-real-U-dependency-acceptance.json", "all-real-U-dependency-review.md"),
    ("U theorem: prescribed exact check", K / "two-reflex-blocker/all-heights-check.py", G / "review/all-real-U-dependency-acceptance.json", "all-heights-check.py"),
    ("U theorem: wall verifier used by the check", K / "two-reflex-blocker/check.py", G / "review/all-real-U-dependency-acceptance.json", "check.py"),
    ("T theorem, independent floor heights (Thm 4.1)", G / "review/uneven-T-theorem.md", G / "review/uneven-T-acceptance.json", "uneven-T-theorem.md"),
    ("T theorem, equal floors (special case of Thm 4.1)", G / "review/T-room-theorem.md", G / "construction/T-whole-review.json", "T-room-theorem.md"),
    ("T theorem: independent review", G / "construction/T-whole-review.md", G / "review/uneven-T-acceptance.json", "T-whole-review.md"),
    ("T theorem: prescribed exact checks", G / "construction/T-whole-check.py", G / "construction/T-whole-review.json", "T-whole-check.py"),
    ("T theorem: prescribed exact check (reviewer)", G / "review/uneven-T-check.py", G / "review/uneven-T-acceptance.json", "uneven-T-check.py"),
    ("wide-middle theorem (Thm 5.1-5.2, Lemma 2.2)", G / "review/wide-middle-onepass.md", G / "review/wide-middle-onepass-acceptance.json", "wide-middle-onepass.md"),
    ("wide-middle: independent review", G / "construction/wide-middle-review.md", G / "review/wide-middle-onepass-acceptance.json", "wide-middle-review.md"),
    ("wide-middle: prescribed exact check", G / "review/wide-middle-constructor-check.py", G / "review/wide-middle-onepass-acceptance.json", "wide-middle-constructor-check.py"),
    ("wide-middle: rotation and seam controls", G / "review/wide-middle-boundary-controls.py", G / "review/wide-middle-onepass-acceptance.json", "wide-middle-boundary-controls.py"),
    ("staircase: nested windows and placement split (Lemmas 6.1, 6.2, 6.4)", G / "construction/staircase-window-proof.md", G / "review/staircase-window-acceptance.json", "staircase-window-proof.md"),
    ("staircase window: independent review", G / "review/staircase-window-review.md", G / "review/staircase-window-acceptance.json", "staircase-window-review.md"),
    ("staircase window: prescribed exact check", G / "review/staircase-window-check.py", G / "review/staircase-window-acceptance.json", "staircase-window-check.py"),
    ("staircase: partial window and roof chart (Lemma 6.3, Thm 6.8 Steps 2-3)", G / "construction/staircase-roof-proof.md", G / "review/staircase-roof-acceptance.json", "staircase-roof-proof.md"),
    ("staircase roof: independent review", G / "review/staircase-roof-review.md", G / "review/staircase-roof-acceptance.json", "staircase-roof-review.md"),
    ("staircase roof: prescribed exact check", G / "review/staircase-roof-check.py", G / "review/staircase-roof-acceptance.json", "staircase-roof-check.py"),
    ("staircase: floor chart under F/Ft (Thm 6.5-6.7)", G / "review/staircase-floor-proof.md", G / "review/staircase-floor-acceptance.json", "staircase-floor-proof.md"),
    ("staircase floor: independent review", G / "construction/staircase-floor-review.md", G / "review/staircase-floor-acceptance.json", "staircase-floor-review.md"),
    ("staircase floor: prescribed exact check and wall verifier", G / "review/staircase-floor-check.py", G / "review/staircase-floor-acceptance.json", "staircase-floor-check.py"),
    ("staircase: single-image roof chart, earlier arrival, Rv/Rh, exhaustive algebra (Thm 6.8 Step 4, Prop 6.10)", G / "review/whole-staircase-candidate.md", G / "review/whole-staircase-acceptance.json", "whole-staircase-candidate.md"),
    ("whole staircase: independent review (author side)", G / "construction/whole-staircase-independent-review.md", G / "review/whole-staircase-acceptance.json", "whole-staircase-independent-review.md"),
    ("whole staircase: reviewer acceptance record", G / "review/whole-staircase-acceptance.json", G / "review/whole-staircase-acceptance.json", None),
    ("whole staircase: review request with pinned dependency hashes", G / "review/whole-staircase-review-request.json", G / "construction/whole-staircase-independent-review.json", "whole-staircase-review-request.json"),
    ("whole staircase: prescribed symbolic identities and roof-corner controls", G / "review/whole-staircase-check.py", G / "review/whole-staircase-acceptance.json", "whole-staircase-check.py"),
    ("not required by the final chain (superseded sufficient condition)", G / "construction/staircase-overlap-supplement.md", G / "review/staircase-overlap-acceptance.json", "staircase-overlap-supplement.md"),
]
ACCEPTANCE = [
    G / "review/eight-wall-frontier-acceptance.json", G / "review/all-real-L-dependency-acceptance.json",
    G / "review/all-real-U-dependency-acceptance.json", G / "review/uneven-T-acceptance.json",
    G / "construction/T-whole-review.json", G / "review/wide-middle-onepass-acceptance.json",
    G / "review/staircase-window-acceptance.json", G / "review/staircase-roof-acceptance.json",
    G / "review/staircase-floor-acceptance.json", G / "review/staircase-overlap-acceptance.json",
    G / "review/whole-staircase-acceptance.json", G / "construction/whole-staircase-independent-review.json",
    G / "review/whole-staircase-review-request.json",
]
sources = []
mismatches = 0
for role, p, acc, needle in ROWS:
    h = sha(p)
    pin = pinned(acc, needle) if needle else None
    status = "matches pin" if pin == h else ("not pinned by name in that acceptance file; hash recorded here" if pin is None else "MISMATCH")
    mismatches += status == "MISMATCH"
    sources.append(dict(role=role, path=str(p.relative_to(CTX)), sha256=h, pinned_in=str(acc.relative_to(CTX)), pinned_sha256=pin, pin_status=status))
acc_rows = []
for p in ACCEPTANCE:
    d = json.loads(p.read_text())
    acc_rows.append(dict(path=str(p.relative_to(CTX)), sha256=sha(p), status=d.get("status"), agent=d.get("reviewer") or d.get("agent"), scope=d.get("scope"), limits=d.get("limits")))
packet = Path(__file__).resolve().parent
packet_files = {str(q.relative_to(packet)): sha(q) for q in sorted(packet.rglob("*")) if q.is_file() and q.name not in ("dependency-manifest.json", "status.json")}
out = dict(
    theorem="Every finite strictly simple orthogonal polygon with at most eight maximal walls illuminates every pair of distinct interior points by a finite corner-avoiding specular path.",
    generated_utc=datetime.now(timezone.utc).isoformat(timespec="seconds"),
    review_kind="AI hand review and prescribed exact computation by Codex and Claude agents; no proof-assistant verification; no human referee",
    novelty_claim="none",
    mismatched_pins=mismatches,
    sources=sources,
    acceptance_records=acc_rows,
    packet_files=packet_files,
)
(packet / "dependency-manifest.json").write_text(json.dumps(out, indent=1) + "\n")
print(json.dumps({"mismatched_pins": mismatches, "sources": len(sources), "acceptance_records": len(acc_rows)}))
for s in sources:
    if s["pin_status"] != "matches pin":
        print(s["pin_status"], s["path"])
