#!/usr/bin/env python3
"""SPEC-OBS-01: exact finite checks; standard library only."""
def mul(a,b):
 n=len(a);return [[sum(a[i][k]*b[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
def tr(a):return sum(a[i][i] for i in range(len(a)))
def ident(n):return [[int(i==j) for j in range(n)] for i in range(n)]
def cp(a):
 n=len(a);p=ident(n);s=[]
 for k in range(1,n+1):p=mul(p,a);s.append(tr(p))
 c=[1]
 for k in range(1,n+1):
  v=sum(c[k-j]*s[j-1] for j in range(1,k+1))
  assert v%k==0
  c.append(-v//k)
 return c
def graph(n,S):return [[int((j-i)%n in S) for j in range(n)] for i in range(n)]
def bump(a,i,j):b=[r[:] for r in a];b[i][j]+=1;return b
a=graph(12,{1,3,9});b=graph(12,{1,5,7})
assert cp(a)==cp(b)
for i in range(12):assert cp(bump(a,i,i))==cp(bump(b,i,i))
assert a[0][3]==1 and b[0][3]==0
aa=bump(a,3,0);bb=bump(b,3,0)
assert tr(mul(aa,aa))-tr(mul(bb,bb))==2 and cp(aa)!=cp(bb)
for m in (a,b):
 p=ident(12)
 for _ in range(6):
  p=mul(p,m);assert len({p[i][i] for i in range(12)})==1
print("SPEC-OBS-01 EXACT CHECK PASS")
print("original charpoly:",cp(a))
print("12 diagonal perturbations: cospectral")
print("rank-one directed perturbation: quadratic trace difference = 2")
