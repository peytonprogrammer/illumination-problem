"""Independent check of Codex's four-cell lemma: every 4-point set in Z^2 has >= 8 external axis neighbors.
Own method: grow sets point by point under the distance<=2 adjacency, translation-canonical (no radius box)."""
N4=((1,0),(-1,0),(0,1),(0,-1))
def b(F): return len({(x+dx,y+dy) for x,y in F for dx,dy in N4}-F)
def norm(F):
    mx=min(x for x,y in F); my=min(y for x,y in F); return frozenset((x-mx,y-my) for x,y in F)
near=[(dx,dy) for dx in range(-2,3) for dy in range(-2,3) if 0<abs(dx)+abs(dy)<=2]
level={norm({(0,0)})}
for n in range(2,5):
    level={norm(F|{(x+dx,y+dy)}) for F in level for x,y in F for dx,dy in near if (x+dx,y+dy) not in F}
    print(n,'point connected sets (mod translation):',len(level),'min b:',min(b(F) for F in level))
# components at Manhattan distance >=3 share no external neighbor; each nonempty set has b>=4,
# so a disconnected 4-set has b>=8. Check the separation claim by brute force on small offsets:
assert all(not ({(dx,dy)} and {(1,0),(-1,0),(0,1),(0,-1)} & {(dx+a,dy+c) for a,c in N4})
           for dx in range(-6,7) for dy in range(-6,7) if abs(dx)+abs(dy)>=3)
m=min(b(F) for F in level); print('four-cell lemma holds:',m>=8,'(minimum',m,')')
# caps
for k in (4,5):
    print('k',k,'I cap',(15+2*k)//6,'P+m caps',{I:(21-4*I+2*k)//2 for I in (2,3,4)})
print('old k4 W<=23 caps',{I:(23-4*I+8)//2 for I in (2,3)})
mins=[F for F in level if b(F)==8]
print('b=8 sets mod translation:',len(mins),'rooted listings:',4*len(mins))
