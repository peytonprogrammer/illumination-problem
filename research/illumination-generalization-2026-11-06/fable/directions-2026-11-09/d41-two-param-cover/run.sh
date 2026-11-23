#!/bin/zsh
# run.sh ROOM AXIS B1 B2 DUP1 DUP2 PAIRS : one band2 run, PMAX=20, timed
cd "$(dirname $0)"
o=runs/$1_a$2_$3_$4_d$5$6
ULMAX=1100 /usr/bin/time -l ./band2 $2 $3 $4 20 $5 $6 $7 < rooms/$1.txt > $o.txt 2> $o.time
