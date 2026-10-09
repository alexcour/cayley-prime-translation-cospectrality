#!/usr/bin/env python3
"""SPEC-OBS-05 exact 2/3-WL vs 3-FWL test (stdlib only)."""
from itertools import product, combinations
from collections import Counter
import json,sys
V=list(product(range(4),repeat=2))
R={(1,0),(2,0),(3,0),(0,1),(0,2),(0,3)}
S={(1,0),(3,0),(0,1),(0,3),(1,1),(3,3)}
def adj(s):return [[int(((v[0]-u[0])%4,(v[1]-u[1])%4) in s) for v in V] for u in V]
def colors(a,d):
 pts=list(product(range(16),repeat=d))
 return pts,[tuple((p[i]==p[j],a[p[i]][p[j]]) for i in range(d) for j in range(i+1,d)) for p in pts]
def wl(a,b,d,joint):
 p,ca=colors(a,d);_,cb=colors(b,d)
 def canon(x,y):
  cs={v:i for i,v in enumerate(sorted(set(x)|set(y)))}
  return [cs[v] for v in x],[cs[v] for v in y]
 ca,cb=canon(ca,cb);ix={v:i for i,v in enumerate(p)}
 sub=[[[ix[t[:j]+(w,)+t[j+1:]] for w in range(16)] for t in p] for j in range(d)]
 hist=[]
 for step in range(8):
  diff=Counter(ca)!=Counter(cb)
  hist.append((step,len(set(ca)),len(set(cb)),diff))
  if diff:break
  def sig(c):
   def repl(i):
    if joint:return tuple(sorted(tuple(c[sub[j][i][w]] for j in range(d)) for w in range(16)))
    return tuple(tuple(sorted(c[sub[j][i][w]] for w in range(16))) for j in range(d))
   return [(c[i],repl(i)) for i in range(len(p))]
  aa,bb=canon(sig(ca),sig(cb))
  if aa==ca and bb==cb:break
  ca,cb=aa,bb
 return hist
def triangles(a):
 tris=[t for t in combinations(range(16),3) if all(a[i][j] for i,j in combinations(t,2))]
 return Counter(sum(all(a[z][v] for v in t) for z in range(16) if z not in t) for t in tris)
def k4(a):return sum(all(a[i][j] for i,j in combinations(t,2)) for t in combinations(range(16),4))
def main():
 a,b=adj(R),adj(S)
 assert all(sum(a[i][z]*a[z][j] for z in range(16))==(6 if i==j else 2) for i in range(16) for j in range(16))
 assert all(sum(b[i][z]*b[z][j] for z in range(16))==(6 if i==j else 2) for i in range(16) for j in range(16))
 res={'2_WL':wl(a,b,2,False),'2_FWL':wl(a,b,2,True),'3_WL':wl(a,b,3,False),'3_FWL':wl(a,b,3,True)}
 assert all(not h[-1][-1] for k,h in res.items() if k!='3_FWL')
 assert res['3_FWL'][0][-1] is False and res['3_FWL'][1][-1] is True
 assert triangles(a)==Counter({1:32}) and triangles(b)==Counter({0:32})
 assert (k4(a),k4(b))==(8,0)
 perm=list(range(16))[::-1];p=[[a[perm[i]][perm[j]] for j in range(16)] for i in range(16)]
 assert not wl(a,p,3,True)[-1][-1]
 print('SPEC-OBS-05 EXACT PASS',res,'triangles',dict(triangles(a)),dict(triangles(b)))
 if len(sys.argv)>1:
  with open(sys.argv[1],'w') as f:json.dump({'test':'SPEC-OBS-05','WL':res,'triangle_extensions_rook':dict(triangles(a)),'triangle_extensions_shrikhande':dict(triangles(b)),'K4_rook':8,'K4_shrikhande':0,'novelty':'known antecedent'},f,indent=2)
if __name__=='__main__':main()
