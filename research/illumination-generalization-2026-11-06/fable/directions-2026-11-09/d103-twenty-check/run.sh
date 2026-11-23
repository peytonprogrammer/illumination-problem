#!/usr/bin/env bash
# D103: reproduce every check. Writes only under this directory (work/, bin/, logs).
# Expect about 7 CPU-minutes, most of it in step 5 (d74 certifier on tile-level rooms).
set -euo pipefail
here=$(cd "$(dirname "$0")" && pwd); cd "$here"
Q=../../../../qclass-closure/twenty
(cd "$Q" && shasum -a 256 -c data/SHA256SUMS)
rm -rf work && mkdir -p work/twenty work/lower bin
tar xzf "$Q/data/twenty-wall.tar.gz" -C work/twenty
tar xzf "$Q/data/below-18.tar.gz" -C work/lower
g++ -O2 -std=c++17 -o bin/leafchk leafchk.cpp
g++ -O2 -std=c++17 -o bin/cert ../d74-continuum-check/cert.cpp
# 1. fixed-seed samples (also reconciles stage counts with the archive)
python3 -B sample.py work/twenty 10 twenty 300 100 work/sample-twenty.txt
python3 -B sample.py work/lower 2 lower 200 0 work/sample-lower.txt
# 2-4. every shear tree, own root boxes and cylinder model; then the mutation control
python3 -B shear_check.py work/twenty/hard work/leaves-twenty.txt && bin/leafchk < work/leaves-twenty.txt | tail -3
python3 -B shear_check.py work/lower/hard work/leaves-lower.txt && bin/leafchk < work/leaves-lower.txt | tail -3
python3 -B shear_check.py work/twenty/hard work/leaves-mut.txt --mutate 2>/dev/null && bin/leafchk < work/leaves-mut.txt | tail -1
# 5. sampled rooms through the d74 certifier plus D103's exact tracer
python3 -B whole.py work/sample-lower.txt work/lower/hard whole-lower.log
python3 -B whole.py work/sample-twenty.txt work/twenty/hard whole-twenty.log
# 6. negative control on the 22-wall room
python3 -B control.py
