#!/usr/bin/env python3
"""SPEC-OBS-02: exact two-point walk invariants, standard library only."""
from collections import Counter,defaultdict
from itertools import combinations
import json
EXPECTED={8:(56,19,67,0),10:(120,32,172,0),12:(220,71,287,16),14:(364,64,884,0),15:(455,65,1479,0),16:(560,85,1783,0),18:(816,147,2008,36),20:(1140,172,3569,0)}
def walks(n,S):
 a=[1]+[0]*(n-1); out=[]
 for _ in range(n):
  b=[0]*n
  for i,v in enumerate(a):
   if v:
    for s in S:b[(i+s)%n]+=v
  a=b;out.append(tuple(a))
 return out
def charpoly(w):
 n=len(w[0]);s=[n*v[0] for v in w];c=[1]
 for k in range(1,n+1):
  v=sum(c[k-j]*s[j-1] for j in range(1,k+1))
  assert v%k==0
  c.append(-v//k)
 return tuple(c)
def intrinsic(w,h):
 n=len(w[0])
 return tuple(sorted(tuple((w[k][d],w[k][(-d)%n]) for k in range(h)) for d in range(n)))
def edgehist(w,S,k):
 return sorted(Counter(w[k-1][s] for s in S).items())
def directed_matrix(n,S):
 return [[int((v-u)%n in S) for v in range(n)] for u in range(n)]
def mul(a,b):
 n=len(a);return [[sum(a[i][t]*b[t][j] for t in range(n)) for j in range(n)] for i in range(n)]
def full_intrinsic(a,h):
 n=len(a);p=[[int(i==j) for j in range(n)] for i in range(n)];powers=[]
 for _ in range(h):p=mul(p,a);powers.append(p)
 return tuple(sorted(tuple((q[i][j],q[j][i]) for q in powers) for i in range(n) for j in range(n)))
def control(n,S,h):
 w=walks(n,S);a=directed_matrix(n,S)
 reduced=intrinsic(w,h)
 assert full_intrinsic(a,h)==tuple(sorted(x for item in reduced for x in (item,)*n))
 p=list(range(n))[::-1];p=p[1::2]+p[::2]
 b=[[0]*n for _ in range(n)]
 for i in range(n):
  for j in range(n):b[p[i]][p[j]]=a[i][j]
 assert full_intrinsic(a,h)==full_intrinsic(b,h)
 assert intrinsic(w,h)==intrinsic(walks(n,{(-s)%n for s in S}),h)
def scan(n):
 groups=defaultdict(list)
 for S in combinations(range(n),3):
  w=walks(n,S);groups[charpoly(w)].append(w)
 collisions=0;first=Counter()
 for grp in groups.values():
  for a,b in combinations(grp,2):
   collisions+=1
   for h in range(1,n+1):
    if intrinsic(a,h)!=intrinsic(b,h):
     first[h]+=1;break
 result=dict(n=n,triplet_supports=sum(map(len,groups.values())),spectral_classes=len(groups),cospectral_support_pairs=collisions,intrinsic_two_point_separated_pairs=sum(first.values()),first_separation_horizon_distribution=dict(sorted(first.items())))
 assert tuple(result[k] for k in ('triplet_supports','spectral_classes','cospectral_support_pairs','intrinsic_two_point_separated_pairs'))==EXPECTED[n]
 return result
def main():
 a=walks(12,(1,3,9));b=walks(12,(1,5,7))
 assert charpoly(a)==charpoly(b)
 assert intrinsic(a,2)==intrinsic(b,2) and intrinsic(a,3)!=intrinsic(b,3)
 assert edgehist(a,(1,3,9),3)==[(4,1),(5,1),(6,1)]
 assert edgehist(b,(1,5,7),3)==[(3,1),(6,2)]
 assert all(Counter(a[k])==Counter(b[k]) for k in range(12))
 c=walks(18,(1,5,13));d=walks(18,(1,5,17))
 assert charpoly(c)==charpoly(d)
 assert intrinsic(c,3)==intrinsic(d,3) and intrinsic(c,4)!=intrinsic(d,4)
 assert all(Counter(c[k])==Counter(d[k]) for k in range(18))
 control(12,(1,3,9),3);control(18,(1,5,13),4)
 print('SPEC-OBS-02 EXACT CHECK PASS')
 print('n=12 edge length 3:',edgehist(a,(1,3,9),3),edgehist(b,(1,5,7),3))
 print('n=18 forward/reverse length 4: distinct')
 print('permutation and unit-multiplier controls: PASS')
 for n in EXPECTED:print(json.dumps(scan(n),sort_keys=True))
if __name__=='__main__':main()
