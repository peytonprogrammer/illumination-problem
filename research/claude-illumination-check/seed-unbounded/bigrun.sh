set -e
cd <SOURCE_WORKSPACE>/.context/claude-illumination-check/seed-unbounded
g(){ <SOURCE_WORKSPACE>/.context/illumination-k4-codex/bounded-proof/venv/bin/python -B big.py "$1" >> big_rooms.jsonl; }
g '{"cells":[[0,0],[2,0],[4,0],[6,0],[8,0]],"wmax":110,"count":3,"seed":1}'
g '{"cells":[[0,0],[2,0],[4,0],[2,2],[2,-2]],"wmax":110,"count":3,"seed":2}'
g '{"cells":[[0,0],[2,0],[2,2],[4,2],[4,4],[6,4]],"wmax":130,"count":3,"seed":3}'
g '{"cells":[[0,0],[2,0],[4,0],[4,2],[4,4],[6,4]],"wmax":130,"count":3,"seed":4}'
g '{"cells":[[0,0],[3,0],[6,0],[9,0]],"wmax":110,"count":3,"seed":5}'
g '{"cells":[[0,0],[2,0],[4,0],[6,0],[8,0],[10,0]],"wmax":130,"count":2,"seed":6}'
