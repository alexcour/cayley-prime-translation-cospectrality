#!/usr/bin/env python3
"""SPEC-OBS-07: exact enumeration of nonabelian three-generator Cayley digraphs.
Only the Python standard library is needed.
Usage: python3 reproducibility/verify_spec_obs_07.py [output.json]

D_m denotes the dihedral group of order 2m, not order m.
Adjacency: A[u,v]=1 iff v=u*s for s in a right connection set S.
Only identity-free, three-element, group-generating supports are included.
"""
from collections import Counter, defaultdict
from itertools import product, permutations, combinations
import json
import sys

EXPECTED = {
  6:(10,3,3,3,18,0,0),
  8:(64,6,7,7,368,64,0),
  10:(80,5,5,5,660,0,0),
  12:(296,18,20,22,2908,720,288),
  14:(266,8,8,8,4816,0,0),
  16:(352,13,14,14,5712,1024,0)
}
def C2(k):return k*(k-1)//2

class Group:
 def __init__(self,name,elements,identity,multiply):
  self.name=name
  self.elements=[identity]+[e for e in elements if e!=identity]
  self.n=len(self.elements)
  pos={x:i for i,x in enumerate(self.elements)}
  self.table=[[pos[multiply(x,y)] for y in self.elements] for x in self.elements]
  self.inverse=[next(j for j in range(self.n) if self.table[i][j]==self.table[j][i]==0) for i in range(self.n)]
  assert all(self.table[0][i]==self.table[i][0]==i for i in range(self.n))
  assert all(self.table[self.table[i][j]][k]==self.table[i][self.table[j][k]]
             for i,j,k in product(range(self.n),repeat=3))
 def generates(self,S):
  seen={0};todo=[0]
  for u in todo:
   for s in S:
    v=self.table[u][s]
    if v not in seen:seen.add(v);todo.append(v)
  return len(seen)==self.n

def dihedral(m):
 return Group('D_'+str(m),[(a,b) for b in range(2) for a in range(m)],(0,0),
              lambda x,y:((x[0]+(-1)**x[1]*y[0])%m,x[1]^y[1]))
def quaternion():
 def op(x,y):
  sx,ax=x;sy,ay=y
  if ax==0:return (sx^sy,ay)
  if ay==0:return (sx^sy,ax)
  if ax==ay:return (sx^sy^1,0)
  z=6-ax-ay
  flip=int((ax,ay) not in ((1,2),(2,3),(3,1)))
  return (sx^sy^flip,z)
 return Group('Q8',[(a,b) for b in range(4) for a in range(2)],(0,0),op)
def alternating4():
 es=[p for p in permutations(range(4)) if sum(p[i]>p[j] for i in range(4) for j in range(i+1,4))%2==0]
 return Group('A4',es,tuple(range(4)),lambda a,b:tuple(a[b[i]] for i in range(4)))

def walks(G,S):
 v=[1]+[0]*(G.n-1);out=[]
 for k in range(G.n):
  new=[0]*G.n
  for i,c in enumerate(v):
   if c:
    for t in S:new[G.table[i][t]]+=c
  v=new;out.append(tuple(v))
 return out
def polynomial(W):
 n=len(W[0]);traces=[n*x[0] for x in W];coeff=[1]
 for k in range(1,n+1):
  t=sum(coeff[k-j]*traces[j-1] for j in range(1,k+1))
  assert t%k==0
  coeff.append(-t//k)
 return tuple(coeff)
def fingerprint(G,W):
 return tuple(sorted(tuple((x[u],x[G.inverse[u]]) for x in W) for u in range(G.n)))
def graph(G,S):
 W=walks(G,S)
 return {'G':G,'S':tuple(S),'W':W,'poly':polynomial(W),'fp':fingerprint(G,W)}
def matrix(obj):
 G=obj['G'];S=obj['S']
 return tuple(tuple(int(v in {G.table[u][s] for s in S}) for v in range(G.n)) for u in range(G.n))
def colors(obj):
 G=obj['G'];W=obj['W']
 return tuple(tuple(tuple((a[d],a[G.inverse[d]]) for a in W) for d in
                    (G.table[G.inverse[u]][v] for v in range(G.n)))
              for u in range(G.n))
def isomorphism(a,b):
 G,H=a['G'],b['G'];n=G.n
 if n!=H.n or a['fp']!=b['fp']:return None
 ca,cb=colors(a),colors(b)
 dom=[[v for v in range(n) if ca[0][u]==cb[0][v] and ca[u][0]==cb[v][0]]
      for u in range(n)]
 mapping={0:0};used={0}
 def find():
  if len(mapping)==n:return tuple(mapping[i] for i in range(n))
  choice=None;options=None
  for u in range(1,n):
   if u in mapping:continue
   cand=[v for v in dom[u] if v not in used and all(
     ca[u][x]==cb[v][y] and ca[x][u]==cb[y][v] for x,y in mapping.items())]
   if not cand:return None
   if options is None or len(cand)<len(options):
    choice,options=u,cand
    if len(cand)==1:break
  for v in options:
   mapping[choice]=v;used.add(v)
   ret=find()
   if ret is not None:return ret
   del mapping[choice];used.remove(v)
  return None
 p=find()
 if p is not None:
  A,B=matrix(a),matrix(b)
  assert all(A[u][v]==B[p[u]][p[v]] for u in range(n) for v in range(n))
 return p

def partition(objects,label):
 spec=defaultdict(list);fp=defaultdict(list)
 for x in objects:
  spec[x['poly']].append(x)
  fp[(x['poly'],x['fp'])].append(x)
 parts=[];counterexamples=[];checked=0
 for family in fp.values():
  classes=[]
  for obj in family:
   for cl in classes:
    checked+=1
    witness=isomorphism(obj,cl[0])
    if witness is not None:
     cl.append(obj);break
   else:classes.append([obj])
  parts.extend(classes)
  if len(classes)>1 and len(counterexamples)<4:
   a,b=classes[0][0],classes[1][0]
   counterexamples.append({'a_group':a['G'].name,'a_support':a['S'],
       'b_group':b['G'].name,'b_support':b['S'],
       'charpoly_coefficients':a['poly'],'equal_two_point':True,
       'isomorphic':False})
 s=sum(C2(len(v)) for v in spec.values())
 f=sum(C2(len(v)) for v in fp.values())
 i=sum(C2(len(v)) for v in parts)
 assert s>=f>=i
 return {'scope':label,'graphs':len(objects),'spectral_classes':len(spec),
         'two_point_classes':len(fp),'isomorphism_classes':len(parts),
         'cospectral_support_pairs':s,'nonisomorphic_cospectral_pairs':s-i,
         'separated_by_two_point':s-f,'indistinguishable_nonisomorphic_pairs':f-i,
         'exact_isomorphism_checks':checked,'counterexample_samples':counterexamples}
def independent_sets_of_4(obj):
 a=matrix(obj)
 return sum(all(a[u][v]==a[v][u]==0 for u,v in combinations(t,2))
            for t in combinations(range(obj['G'].n),4))
def induced_three_motif_distribution(obj):
 a=matrix(obj);d=Counter()
 for t in combinations(range(obj['G'].n),3):
  key=min(tuple(a[t[p]][t[q]] for p in perm for q in perm if p!=q)
          for perm in permutations(range(3)))
  d[key]+=1
 return d
def main():
 groups=[dihedral(m) for m in range(3,9)]+[quaternion(),alternating4()]
 byorder=defaultdict(list);rows=[]
 for G in groups:
  objects=[graph(G,s) for s in combinations(range(1,G.n),3) if G.generates(s)]
  r=partition(objects,G.name);rows.append(r)
  byorder[G.n].extend(objects)
  print('GROUP',G.name,'graphs',r['graphs'],'spectra',r['spectral_classes'],
        'fingerprints',r['two_point_classes'],'iso',r['isomorphism_classes'],
        'unresolved',r['indistinguishable_nonisomorphic_pairs'],flush=True)
 orders=[]
 for n,objects in sorted(byorder.items()):
  r=partition(objects,'all selected groups at order '+str(n))
  observed=tuple(r[k] for k in ('graphs','spectral_classes','two_point_classes',
     'isomorphism_classes','cospectral_support_pairs',
     'nonisomorphic_cospectral_pairs','indistinguishable_nonisomorphic_pairs'))
  assert observed==EXPECTED[n],(n,observed,EXPECTED[n])
  orders.append({'order':n,**r})
  print('ORDER',n,*observed,flush=True)
 g=dihedral(6);a=graph(g,(1,3,6));b=graph(g,(1,6,8))
 assert a['poly']==b['poly'] and a['fp']==b['fp']
 assert isomorphism(a,b) is None
 assert [independent_sets_of_4(a),independent_sets_of_4(b)]==[30,33]
 h=alternating4();c=graph(h,(1,3,5));d=graph(h,(1,3,6))
 assert c['poly']==d['poly'] and c['fp']==d['fp']
 assert isomorphism(c,d) is None
 assert induced_three_motif_distribution(c)!=induced_three_motif_distribution(d)
 report={'experiment':'SPEC-OBS-07','scope':'identity-free generating triples in D3..D8,Q8,A4',
     'groups':rows,'orders':orders,
     'D6_witness':{'support_a':[1,3,6],'support_b':[1,6,8],
       'charpoly':a['poly'],'independent_four_sets':[30,33]},
     'A4_witness':{'support_a':[1,3,5],'support_b':[1,3,6],
       'charpoly':c['poly'],'three_motif_histograms_differ':True},
     'status':'exact finite result, novelty not audited'}
 if len(sys.argv)>1:
  with open(sys.argv[1],'w',encoding='utf-8') as f:
   json.dump(report,f,indent=2);f.write('\n')
 print('SPEC-OBS-07 EXACT CHECK PASS')
if __name__=='__main__':main()
