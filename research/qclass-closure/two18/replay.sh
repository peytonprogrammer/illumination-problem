#!/usr/bin/env bash
# Run from any directory with a fresh output path.
set -euo pipefail
base=$(cd "$(dirname "$0")" && pwd)
mkdir "${1:?provide a fresh directory}"
out=$(cd "$1" && pwd)
python3 "$base/localize.py" "$out"
cmp "$base/rooms" "$out/rooms"
cc -O2 -fsanitize=undefined -fno-sanitize-recover=all "$out/localize.c" -o "$out/localize"
COVER_ALLDIRS=1 "$out/localize" 18 1 6000 < "$out/rooms" > "$out/regions.txt"
python3 "$base/endpoints.py" "$out"
python3 "$base/export_labels.py" "$out/export.c"
cc -O2 "$out/export.c" -o "$out/export"
c++ -std=c++17 -O2 -fsanitize=undefined -fno-sanitize-recover=all "$base/shear.cpp" -o "$out/shear"
for t in 00 01 10 11; do
    case "$t" in 00|10) period=8;; 01) period=16;; 11) period=12;; esac
    "$out/export" < "$out/room$t" > "$out/labels$t"
    "$out/shear" "$out/labels$t" 3856 "$period" 28 5000 < "$out/ends$t" > "$out/cert$t.txt"
    # Equal-cost directions can be sorted differently by another standard library.
    # Verify both the saved trees and the newly generated trees on that platform.
done
python3 "$base/verify.py" "$out"
python3 "$base/verify.py" "$out" "$out"
