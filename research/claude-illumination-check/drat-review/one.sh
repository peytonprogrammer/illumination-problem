#!/bin/zsh
# Check one case's DRAT proof with Claude's own drat-trim build; output stays in this directory.
P=../../illumination-k4-codex/bounded-proof/cases/$1
./drat-trim $P/formula.cnf $P/proof.drat -t 3000 > log-$1.txt 2>&1
echo "$1 $(grep -m1 -o 's VERIFIED\|s NOT VERIFIED\|TIMEOUT\|timeout' log-$1.txt)"
