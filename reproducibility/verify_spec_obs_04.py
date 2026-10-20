#!/usr/bin/env python3
"""Exact Shrikhande vs 4x4 rook graph check, Python standard library only."""
from itertools import combinations
from collections import Counter
V=[(a,b) for a in range(4) for b in range(4)]
SH={(1,0),(3,0),(0,1),(0,3),(1,1),(3,3)}
RO={(1,0),(2,0),(3,0),(0,1),(0,2),(0,3)}
def graph(S):
 return [[int(((b[0]-a[0])%4,(b[1]-a[1])%4) in S) for b in V] for a in V]
def mm(a,b):
 n=len(a);return [[sum(a[i][k]*b[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
def fp(a,h):
 n=len(a);p=[[int(i==j) for j in range(n)] for i in range(n)]
 d=[[[] for j in range(n)] for i in range(n)]
 for _ in range(h):
  p=mm(p,a)
  for i in range(n):
   for j in range(n):d[i][j].append((p[i][j],p[j][i]))
 return Counter(tuple(d[i][j]) for i in range(n) for j in range(n))
def k4(a):
 return sum(all(a[u][v] for u,v in combinations(t,2)) for t in combinations(range(16),4))
def localtri(a):
 return Counter(sum(all(a[u][v] for u,v in combinations(t,2)) for t in combinations([j for j in range(16) if a[i][j]],3)) for i in range(16))
def commonedges(a):
 return Counter(sum(a[u][v] for u,v in combinations([t for t in range(16) if a[i][t] and a[j][t]],2)) for i in range(16) for j in range(16) if a[i][j])
x,y=graph(SH),graph(RO)
for a in (x,y):
 assert all(a[i][i]==0 and sum(a[i])==6 for i in range(16))
 assert all(a[i][j]==a[j][i] for i in range(16) for j in range(16))
 sq=mm(a,a)
 assert all(sq[i][j]==(6 if i==j else 2) for i in range(16) for j in range(16))
assert fp(x,20)==fp(y,20)
assert (k4(x),k4(y))==(0,8)
assert localtri(x)==Counter({0:16}) and localtri(y)==Counter({2:16})
assert commonedges(x)==Counter({0:96}) and commonedges(y)==Counter({1:96})
# Identity A^2=4I+2J and AJ=6J proves equality of walk fingerprint for ALL horizons.
print("SPEC-OBS-04 EXACT CHECK PASS")
print("SRG=(16,6,2,2), spectrum 6^1,2^6,(-2)^9")
print("Two-point walk signatures identical through 20 and all horizons by identity")
print("4-cliques Shrikhande/Rook:",k4(x),k4(y))
print("Neighbor triangles:",dict(localtri(x)),dict(localtri(y)))
print("Adjacent-root common-neighbor induced edge counts:",dict(commonedges(x)),dict(commonedges(y)))
