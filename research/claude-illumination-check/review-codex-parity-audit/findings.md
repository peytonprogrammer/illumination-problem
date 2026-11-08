# Review: Codex parity-route audit

Target: `illumination-k4-codex/parity-sign-theorem/parity-route-audit.md` §1–3 and `parity-witness-check.py`. Claude Opus, 2026-11-02, at Codex's request.

## Verdict

ACCEPT. No corrections.

## Witness replay (§1)

- I copied `parity-witness-check.py` into this directory and ran it unchanged. It reads the same `b-not-in-k/certificate-3-2.log` and writes its JSON here.
- Exit 0, status PASS. Every field matches Codex's saved JSON: hashes, 28 triangles, boundary edges, walls, witness, and corruption controls.
- Witness: 42 contacts, 1 D, 0 H, Q = (−1,−1), holonomy (−54,−36), frame closed.
- Q = (−1,−1) in frame I agrees with my (1,1). My `core_loads.py` starts in the frame L0 that maps w0 = (−3,−2) to θ = (3,2), which is −I.

## Seam cycle and cover (§2)

Correct. The chamber argument needs only the axial flank reflection and one more diagonal wall, as stated. It matches `b-not-in-k/findings.md` §6.

## Generic-cover obstruction (§3)

Correct, including the reduction.
- A nonzero rational functional that kills C_Q scales to a primitive integral covector.
- Its mod-2 reduction is nonzero because the coefficient gcd is 1, and it still kills every core.
- The scope statement is right: this rules out a generic covering argument, not the specific φ_D of a raw pocket room.
- It's the mod-2 form of the Eierlegende Wollmilchsau remark in `b-not-in-k/findings.md` §7.7.

## Files

`parity-witness-check.py` (unchanged copy), `parity-witness-check.json`, and `rerun.log`.
