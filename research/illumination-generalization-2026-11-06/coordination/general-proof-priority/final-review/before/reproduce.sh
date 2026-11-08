#!/bin/sh
# Runs every prescribed exact check in the eight-wall chain from a scratch copy.
# Never executes a peer script in place. Usage: sh reproduce.sh [scratch-dir]
set -eu
ROOT=<SOURCE_WORKSPACE>/.context
G=$ROOT/illumination-generalization-2026-11-06
K=$ROOT/illumination-k4-codex
S=${1:-$(mktemp -d /tmp/eight-wall-checks.XXXXXX)}
mkdir -p "$S/g/review" "$S/g/construction" "$S/k4/single-boundary-blocker" "$S/k4/two-reflex-blocker"
for f in whole-staircase-check.py staircase-floor-check.py staircase-floor-effort.json staircase-floor-proof.md \
         whole-staircase-candidate.md uneven-T-check.py uneven-T-theorem.md T-room-theorem.md \
         wide-middle-constructor-check.py wide-middle-onepass-effort.json wide-middle-onepass.md \
         wide-middle-boundary-controls.py eight-wall-turn-check.py eight-wall-frontier.md \
         staircase-window-check.py staircase-roof-check.py staircase-overlap-check.py; do
  cp "$G/review/$f" "$S/g/review/"; done
for f in T-whole-check.py staircase-window-proof.md staircase-roof-proof.md staircase-overlap-supplement.md; do
  cp "$G/construction/$f" "$S/g/construction/"; done
cp "$K/single-boundary-blocker/arithmetic-check.py" "$S/k4/single-boundary-blocker/"
cp "$K/two-reflex-blocker/all-heights-check.py" "$K/two-reflex-blocker/check.py" "$S/k4/two-reflex-blocker/"
run() { printf '\n### %s\n' "$1"; ( cd "$(dirname "$1")" && python3 -I "$(basename "$1")" ) | head -c 1200; echo; }
run "$S/g/review/eight-wall-turn-check.py"
run "$S/k4/single-boundary-blocker/arithmetic-check.py"
run "$S/k4/two-reflex-blocker/all-heights-check.py"
run "$S/g/construction/T-whole-check.py"
run "$S/g/review/uneven-T-check.py"
run "$S/g/review/wide-middle-constructor-check.py"
run "$S/g/review/wide-middle-boundary-controls.py"
run "$S/g/review/staircase-window-check.py"
run "$S/g/review/staircase-roof-check.py"
run "$S/g/review/staircase-floor-check.py"
run "$S/g/review/staircase-overlap-check.py"
run "$S/g/review/whole-staircase-check.py"
echo; echo "ALL CHECKS EXITED 0. Scratch dir: $S"
