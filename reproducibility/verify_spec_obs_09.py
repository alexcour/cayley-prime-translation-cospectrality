#!/usr/bin/env python3
"""SPEC-OBS-09: D9 complete degree-three right-Cayley holdout.
Requires networkx for independent digraph VF2. Python integer motif coding.
Other preregistered groups D10,D11,D12,S4 are deliberately NOT claimed tested.
"""
from itertools import combinations,permutations
from collections import defaultdict
import json,sys
import networkx as nx

M=9
N=2*M
def prod(x,y):return ((x[0]+(-1)**x[1]*y[0])%M,x[1]^y[1])
EL=[(a,b) for b in range(2) for a in range(M)]
IDX={v:i for i,v in enumerate(EL)}
TABLE=[[IDX[prod(x,y)] for y in EL] for x in EL]
def generating(S):
 seen={0};q=[0]
 for x in q:
  for s in S:
   v=TABLE[x][s]
   if v not in seen:seen.add(v);q.append(v)
 return len(seen)==N
def matrix(S):
 return [[int(j in {TABLE[i][s] for s in S}) for j in range(N)] for i in range(N)]
def canonical_motifs_4():
 edges=[(i,j) for i in range(4) for j in range(4) if i!=j]
 look={e:i for i,e in enumerate(edges)}
 trans=[[look[(p[i],p[j])] for i,j in edges] for p in permutations(range(4))]
 c=[]
 for mask in range(1<<12):
  c.append(min(sum(((mask>>j)&1)<<i for i,j in enumerate(t)) for t in trans))
 keys={v:i for i,v in enumerate(sorted(set(c)))}
 return edges,[keys[x] for x in c]
def histogram(A,look,quads):
 edges,canon=look;h=defaultdict(int)
 for q in quads:
  v=sum(A[q[i]][q[j]]<<z for z,(i,j) in enumerate(edges))
  h[canon[v]]+=1
 return tuple(sorted(h.items()))
def graph(A):
 g=nx.DiGraph()
 g.add_nodes_from(range(N))
 g.add_edges_from((i,j) for i in range(N) for j in range(N) if A[i][j])
 return g
def independent_sets(A,k):
 return sum(all(not A[u][v] and not A[v][u] for u,v in combinations(t,2))
            for t in combinations(range(N),k))
def main():
 look=canonical_motifs_4()
 quads=list(combinations(range(N),4))
 fibers=defaultdict(list)
 for S in combinations(range(1,N),3):
  if not generating(S):continue
  A=matrix(S)
  assert all(sum(row)==3 and row[i]==0 for i,row in enumerate(A))
  fibers[histogram(A,look,quads)].append((S,A))
 classes=0;vf2=0;witness_fibers=[]
 for family in fibers.values():
  groups=[]
  for S,A in family:
   G=graph(A)
   for part in groups:
    vf2+=1
    if nx.is_isomorphic(G,part[0][2]):
     part.append((S,A,G));break
   else:
    groups.append([(S,A,G)])
  classes+=len(groups)
  if len(groups)>1:witness_fibers.append([list(gr[0][0]) for gr in groups])
 assert sum(map(len,fibers.values()))==594
 assert len(fibers)==10 and classes==12 and len(witness_fibers)==2
 s=(1,9,12);t=(1,9,13)
 a,b=matrix(s),matrix(t)
 assert histogram(a,look,quads)==histogram(b,look,quads)
 assert (independent_sets(a,5),independent_sets(b,5))==(342,360)
 assert (independent_sets(a,6),independent_sets(b,6))==(87,129)
 assert not nx.is_isomorphic(graph(a),graph(b))
 result={'experiment':'SPEC-OBS-09','completed_group':'D9','order':18,'supports':594,
  'four_motif_classes':10,'isomorphism_classes':12,'vf2_checks':vf2,
  'fibers_with_multiple_isomorphism_classes':2,'representatives':witness_fibers,
  'certified_witness':{'S':s,'T':t,'same_four_motifs':True,
   'independent_5':[342,360],'independent_6':[87,129],
   'nonisomorphic':True},
  'incomplete_groups':['D10','D11','D12','S4'],
  'status':'EXACT_D9_ONLY; PRIORITY_NOT_AUDITED'}
 print('SPEC-OBS-09 D9 EXACT PASS',json.dumps(result))
 if len(sys.argv)>1:
  with open(sys.argv[1],'w',encoding='utf-8') as f:json.dump(result,f,indent=2);f.write('\n')
if __name__=='__main__':main()
