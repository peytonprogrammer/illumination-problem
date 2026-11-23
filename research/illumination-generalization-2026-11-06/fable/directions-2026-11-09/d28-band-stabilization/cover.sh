#!/bin/sh
# cover.sh ROOMFILE PC PMAX : for every axis and row, search covering certificates up to level PC
rm=$1; PC=$2; PM=$3
LC=$(python3 -c "
from math import lcm
print(lcm(*range(1,$PC+1)))")
for ax in 0 1; do for cb in 0 1 2 3 4 5 6 7 8 9 10 11; do
  hdr=$(./band $ax $cb 1 3 0 1 < $rm 2>/dev/null | grep "^# points"); [ -z "$hdr" ] && continue
  L=$(echo "$hdr" | sed 's/.*L=\([0-9]*\).*/\1/'); nch=$(echo "$hdr" | sed 's/.*chords \([0-9]*\).*/\1/'); [ "$nch" = "0" ] && continue
  G=$((2*L*LC+3))
  echo "ROOM $rm ax $ax row $cb L=$L GMAX=$G $(./band $ax $cb $PM $G 0 1 < $rm | grep -v '^# pair\|chord\|^# points' | awk '$1=="C"&&$3=="cover"{c[$4]++} $1=="C"&&$3=="nocover"{nc++; ex=$0} $1=="U"{nu++} /quiet/{q=$0} END{s=""; for(k in c)s=s" "k"x"c[k]; print "covered:"s" | nocover "nc+0" ["ex"] | "q}')"
done; done
