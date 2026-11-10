# Independent adversarial review: net charge

[done] ACCEPT the identity and the local lower bounds for slit-free canonical triangulated disks. No darkness or global size bound follows yet. Frozen peer inputs and hashes are in `inputs/` and `manifest.json`.

## Proof without sampled rooms

Each triangle has exactly one A, one B and one C vertex. Put weight 1/4 on a tile for an exceptional B vertex and 1/2 for an exceptional C vertex.

An interior B exception meets eight tiles and contributes total weight 2; a smooth B exception meets four and contributes 1. An interior C exception meets four tiles and contributes 2; a smooth C exception meets two and contributes 1. Summing tile weights therefore gives exactly E=2J+s_N.

The A-cell costs sum to 6I+Q: full cells cost 6, smooth boundary cells cost 3, and other occupied partial cells cost their triangle count m. The disk incidence/Euler identity gives W=2+6I+Q-E. Therefore

    W = 2 + sum_A_cells (cost - tile weights).

Every tile has weight at most 3/4. A full cell has eight tiles and cost 6, so its net is nonnegative. A smooth A half-plane has four tiles and cost 3, again giving nonnegative net. A nonsmooth proper fan has m tiles and cost m, giving net at least m/4. Empty cells have net zero. This proves all claimed inequalities for every eligible room.

The disk hypothesis matters: for an edge-connected planar union with h holes, the constant becomes 2(1-h), provided the same local manifold conditions hold. Disconnected fans, slits and contacts require separate accounting. The peer checker alone does not validate these geometric hypotheses, so its command-line output should not be treated as a general theorem for arbitrary triangle lists.

## Independent checks

`net-charge-audit.py` builds the canonical A star with Codex geometry. It checks every one of its 58 legal empty/contiguous/full fan masks against all 256 Boolean assignments of exception flags on its eight peripheral B/C vertices: **14,848 local cases**, all pass. The flag assignments include ones that might not extend to a physical room; accepting this larger local relaxation makes the bound stronger as a verification.

The same audit checks seven saved physical rooms independently: the 22-wall room and the first learned witness room from each of the six nonempty persisted-placement files. It verifies simple disk geometry, constructs exceptions from exact local sectors, verifies total tile weight E and the wall identity, and checks all cell nets nonnegative. No peer helper or optical routine is imported. No rays or new rooms are searched.

For the 22-wall room, total net is 20. Each marked A cell contributes 4; the other cells contribute 12 altogether. This matches Opus's stated values. The minimum occupied-cell net in this room is 2.

## What it does and does not buy

All nets are multiples of 1/4. At W<=21, total net is at most 19, so there are at most 76 positive-net cells, and the sum of m over nonsmooth partial A cells is at most 76. This bound concerns the charged part of the room; it does not bound total N or total exceptions.

Zero-net occupied cells remain. The local check finds one all-flags assignment making a full cell zero and 64 assignments across the eight smooth-half-plane fans. In any nonempty zero-net cell every incident tile must attain weight 3/4, so all its peripheral B/C vertices must be exceptions. Thus zero-net cells are transparent local regions, but their global arrangement can still carry essential reflection or connectivity information.

A promising next lemma would remove or normalize zero-net regions while preserving simple geometry, the marked A points, wall count and darkness. The charge identity supplies the finite charged skeleton only after such a lemma. Local transparency by itself does not establish a valid contraction; changing lengths or identifications can change billiard connections.

This is an exact reformulation of the previously known wall identity with useful local nonnegativity. It is not yet an additional illumination obstruction.

## Reproduction

    python3 -B .context/illumination-k4-codex/proofs/net-charge-audit.py

Result: `net-charge-audit.json`, status PASS. The 301-room count reported by Opus was not rerun or adopted as an independent count here; the seven-room and exhaustive-local checks above are the new evidence.

Next move: review L5/L6 and prove or disprove a darkness-preserving reduction of zero-net regions, with normalization stated explicitly.
