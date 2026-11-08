#!/bin/zsh
d=regen/$1; r=$(./drat-trim $d/formula.cnf $d/proof.drat -t 1200 2>&1 | tr '\r' '\n' | grep -oE "s (VERIFIED|NOT VERIFIED)|TIMEOUT" | head -1)
echo "$1 ${r:-NO_RESULT}"
