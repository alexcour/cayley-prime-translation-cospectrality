#!/usr/bin/env python3
"""SPEC-OBS-08: induced directed 3/4-vertex motifs of Cayley digraphs.

Corpus is identical to SPEC-OBS-07: all identity-free generating 3-subsets
of D_3,...,D_8 (dihedral order 2m), Q8 and A4; right multiplication.
Dependencies: Python standard library and networkx >= 3.0 for independently
checking graph isomorphism. No numerical floating-point calculations.
Run: python3 reproducibility/verify_spec_obs_08.py [output.json]
"""
from collections import Counter, defaultdict
from itertools import product, permutations, combinations
from math import comb
import json,sys
import networkx as nx

def canonical_lookup(k):
    pairs=[(i,j) for i in range(k) for j in range(k) if i!=j]
    positions={a:i for i,a in enumerate(pairs)}
    transforms=[[positions[(p[i],p[j])] for i,j in pairs] for p in permutations(range(k))]
    table=[]
    for code in range(1<<len(pairs)):
        best=code
        for transform in transforms:
            renamed=sum((1<<i) for i,j in enumerate(transform) if code>>j&1)
            if renamed<best:best=renamed
        table.append(best)
    return pairs,table
ARCS={};CANON={}
for k in (3,4):ARCS[k],CANON[k]=canonical_lookup(k)

class Group:
    def __init__(self,name,els,e,mult):
        self.name=name;self.els=[e]+[x for x in els if x!=e];self.n=len(els)
        inds={x:i for i,x in enumerate(self.els)}
        self.mul=[[inds[mult(x,y)] for y in self.els] for x in self.els]
        self.inv=[next(j for j in range(self.n) if self.mul[i][j]==self.mul[j][i]==0) for i in range(self.n)]
        assert all(self.mul[i][0]==self.mul[0][i]==i for i in range(self.n))
    def generates(self,S):
        seen={0};todo=[0]
        for u in todo:
            for s in S:
                v=self.mul[u][s]
                if v not in seen:seen.add(v);todo.append(v)
        return len(seen)==self.n
def dihedral(m):
    return Group('D'+str(m),[(a,b) for b in range(2) for a in range(m)],(0,0),
                 lambda x,y:((x[0]+(-1)**x[1]*y[0])%m,x[1]^y[1]))
def quaternion():
    def mult(x,y):
        s,u=x;t,v=y
        if u==0:return (s^t,v)
        if v==0:return (s^t,u)
        if u==v:return (s^t^1,0)
        return (s^t^int((u,v) not in ((1,2),(2,3),(3,1))),6-u-v)
    return Group('Q8',[(a,b) for b in range(4) for a in range(2)],(0,0),mult)
def alternating4():
    els=[p for p in permutations(range(4)) if sum(p[i]>p[j] for i in range(4) for j in range(i+1,4))%2==0]
    return Group('A4',els,tuple(range(4)),lambda x,y:tuple(x[y[i]] for i in range(4)))
def walks(G,S):
    a=[1]+[0]*(G.n-1);out=[]
    for _ in range(G.n):
        b=[0]*G.n
        for i,v in enumerate(a):
            if v:
                for s in S:b[G.mul[i][s]]+=v
        a=b;out.append(tuple(a))
    return out
def polynomial(G,W):
    c=[1]
    for k in range(1,G.n+1):
        t=sum(c[k-j]*G.n*W[j-1][0] for j in range(1,k+1))
        assert t%k==0
        c.append(-t//k)
    return tuple(c)
def fingerprint(G,W):
    return tuple(sorted(tuple((w[i],w[G.inv[i]]) for w in W) for i in range(G.n)))
def adjacency(G,S):
    return tuple(tuple(int(v in {G.mul[u][s] for s in S}) for v in range(G.n)) for u in range(G.n))
def motifs(A,k):
    pairs=ARCS[k];canon=CANON[k];counts=Counter()
    for verts in combinations(range(len(A)),k):
        code=sum(1<<b for b,(i,j) in enumerate(pairs) if A[verts[i]][verts[j]])
        counts[canon[code]]+=1
    return tuple(sorted(counts.items()))
def graph(G,S):
    W=walks(G,S);A=adjacency(G,S)
    return {'group':G.name,'S':S,'n':G.n,'cp':polynomial(G,W),
            'i2':fingerprint(G,W),'m3':motifs(A,3),'m4':motifs(A,4),'A':A}
def groups(data,key):
    d=defaultdict(list)
    for item in data:d[key(item)].append(item)
    return d
def npairs(d):
    return sum(len(a)*(len(a)-1)//2 for a in d.values())
def nxgraph(A):
    g=nx.DiGraph();g.add_nodes_from(range(len(A)))
    g.add_edges_from((u,v) for u in range(len(A)) for v in range(len(A)) if A[u][v])
    return g
def real_isomorphism_classes(items):
    # Motif equality is necessary for isomorphism. Exact VF2 handles all survivors.
    cls=[];comparisons=0
    for candidate in groups(items,lambda x:(x['cp'],x['m4'])).values():
        local=[]
        for g in candidate:
            ng=nxgraph(g['A'])
            for cl in local:
                comparisons+=1
                if nx.is_isomorphic(ng,cl['nx']):
                    cl['members'].append(g);break
            else:local.append({'nx':ng,'members':[g]})
        cls.extend(local)
    return cls,comparisons
def summarize(items,label):
    by={'spectrum':groups(items,lambda x:x['cp']),
        'i2':groups(items,lambda x:(x['cp'],x['i2'])),
        'm3':groups(items,lambda x:(x['cp'],x['m3'])),
        'm4':groups(items,lambda x:(x['cp'],x['m4'])),
        'i2+m3':groups(items,lambda x:(x['cp'],x['i2'],x['m3'])),
        'i2+m4':groups(items,lambda x:(x['cp'],x['i2'],x['m4']))}
    iso,checks=real_isomorphism_classes(items)
    iso_pairs=sum(len(c['members'])*(len(c['members'])-1)//2 for c in iso)
    noniso=npairs(by['spectrum'])-iso_pairs
    unresolved={name:npairs(v)-iso_pairs for name,v in by.items() if name!='spectrum'}
    assert all(x>=0 for x in unresolved.values())
    assert len(iso)>=len(by['m4'])
    return {'scope':label,'graphs':len(items),
       'spectral_classes':len(by['spectrum']),'i2_classes':len(by['i2']),
       'motif3_classes':len(by['m3']),'motif4_classes':len(by['m4']),
       'i2_plus_motif3_classes':len(by['i2+m3']),
       'isomorphism_classes':len(iso),
       'cospectral_support_pairs':npairs(by['spectrum']),
       'cospectral_nonisomorphic_pairs':noniso,
       'nonisomorphic_undistinguished':unresolved,
       'VF2_pair_comparisons':checks}
def witness(G,S,T):
    a=graph(G,S);b=graph(G,T)
    a4=dict(a['m4']);b4=dict(b['m4'])
    return {'group':G.name,'supports':[list(S),list(T)],
     'charpoly_equal':a['cp']==b['cp'],
     'I_n_equal':a['i2']==b['i2'],
     'motif3_equal':a['m3']==b['m3'],
     'motif4_equal':a['m4']==b['m4'],
     'motif4_differences':[(v,a4.get(v,0),b4.get(v,0)) for v in sorted(set(a4)|set(b4)) if a4.get(v,0)!=b4.get(v,0)]}
def main():
    byorder=defaultdict(list); bygroup={}
    for G in [dihedral(m) for m in range(3,9)]+[quaternion(),alternating4()]:
        gs=[graph(G,S) for S in combinations(range(1,G.n),3) if G.generates(S)]
        bygroup[G.name]=gs;byorder[G.n].extend(gs)
        print('GROUP',G.name,'supports',len(gs),flush=True)
    assert sum(map(len,bygroup.values()))==1068
    expected={6:(10,3,3,3),8:(64,6,7,7),10:(80,5,5,5),
              12:(296,18,20,22),14:(266,8,8,8),16:(352,13,14,14)}
    orders=[]
    for n,data in sorted(byorder.items()):
        s=summarize(data,'order '+str(n))
        assert tuple(s[k] for k in ('graphs','spectral_classes','i2_classes','isomorphism_classes'))==expected[n]
        assert s['nonisomorphic_undistinguished']['m4']==0
        orders.append({'order':n,**s})
        print('ORDER',n,'spectrum',s['spectral_classes'],'3motif',s['motif3_classes'],
              '4motif',s['motif4_classes'],'iso',s['isomorphism_classes'],
              'undistinguished',s['nonisomorphic_undistinguished'],flush=True)
    assert orders[3]['nonisomorphic_undistinguished']['i2']==288
    assert orders[3]['nonisomorphic_undistinguished']['i2+m3']==144
    G=dihedral(6);H=alternating4()
    ws={'D6':witness(G,(1,3,6),(1,6,8)),
        'A4':witness(H,(1,3,5),(1,3,6))}
    assert ws['D6']['charpoly_equal'] and ws['D6']['I_n_equal']
    assert ws['D6']['motif3_equal'] and not ws['D6']['motif4_equal']
    assert ws['A4']['charpoly_equal'] and ws['A4']['I_n_equal']
    assert not ws['A4']['motif3_equal'] and not ws['A4']['motif4_equal']
    # Motif histograms must be invariant under an arbitrary relabeling.
    for k in (3,4):
        a=adjacency(G,(1,3,6));p=list(range(G.n))[::-1]
        b=tuple(tuple(a[p[i]][p[j]] for j in range(G.n)) for i in range(G.n))
        assert motifs(a,k)==motifs(b,k)
    output={'experiment':'SPEC-OBS-08','scope':'SPEC-OBS-07 exact nonabelian corpus',
       'method':'all induced directed 3/4-vertex unlabelled motifs (canonical over permutations)',
       'orders':orders,'groups':[summarize(g,k) for k,g in bygroup.items()],
       'witnesses':ws,'status':'exact finite, NetworkX VF2 isomorphism, novelty NON AUDITEE'}
    if len(sys.argv)>1:
        with open(sys.argv[1],'w',encoding='utf-8') as f:
            json.dump(output,f,indent=2);f.write('\n')
    print('SPEC-OBS-08 EXACT CHECK PASS')
if __name__=='__main__':main()
