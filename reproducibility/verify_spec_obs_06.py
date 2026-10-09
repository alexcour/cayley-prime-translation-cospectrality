#!/usr/bin/env python3
"""SPEC-OBS-06: exact comparison of spectrum, two-point signatures and isomorphism.

Finite corpus: noncyclic abelian groups of order at most 18 (listed below);
all three-element identity-free generating connection supports.
Directed, strongly connected, loopless Cayley digraphs.
All arithmetic and isomorphism tests use Python standard library only.
Usage: python3 reproducibility/verify_spec_obs_06.py [results.json]
"""
from collections import defaultdict
from itertools import product, combinations
from math import prod
import json
import sys

GROUPS=((2,2),(2,4),(2,2,2),(3,3),(2,6),(4,4),(2,8),
        (2,2,4),(2,2,2,2),(3,6))
EXPECTED_GROUP={
 '2x2':(1,1,1), '2x4':(32,5,5), '2x2x2':(28,1,1),
 '3x3':(56,3,3), '2x6':(134,15,16), '4x4':(352,7,7),
 '2x8':(352,27,27), '2x2x4':(224,3,3), '2x2x2x2':(0,0,0),
 '3x6':(584,18,18)}
EXPECTED_ORDER={4:(1,1,1,1,0),8:(60,5,5,5,0),
 9:(56,3,3,3,0),12:(134,15,16,16,144),
 16:(928,33,33,33,0),18:(584,18,18,18,0)}

def add(x,y,mod):
    return tuple((a+b)%d for a,b,d in zip(x,y,mod))
def neg(x,mod):
    return tuple(-a%d for a,d in zip(x,mod))
def generated(s,mod):
    z=(0,)*len(mod); seen={z};todo=[z]
    for x in todo:
        for y in s:
            t=add(x,y,mod)
            if t not in seen:seen.add(t);todo.append(t)
    return len(seen)==prod(mod)
def walks(elements,s,mod):
    ix={v:i for i,v in enumerate(elements)}
    n=len(elements);v=[0]*n;v[0]=1;out=[]
    for _ in range(n):
        b=[0]*n
        for i,c in enumerate(v):
            if c:
                for t in s:b[ix[add(elements[i],t,mod)]]+=c
        v=b;out.append(tuple(v))
    return out
def poly(w):
    n=len(w[0]);p=[n*t[0] for t in w];c=[1]
    for k in range(1,n+1):
        t=sum(c[k-j]*p[j-1] for j in range(1,k+1))
        assert t%k==0
        c.append(-t//k)
    return tuple(c)
def graph(mod,s):
    el=tuple(product(*(range(d) for d in mod)))
    ix={v:i for i,v in enumerate(el)};n=len(el)
    w=walks(el,s,mod)
    inv=tuple(sorted(tuple((t[i],t[ix[neg(x,mod)]]) for t in w)
                     for i,x in enumerate(el)))
    def disp(u,v):return ix[add(el[v],neg(el[u],mod),mod)]
    colors=[[tuple((t[disp(u,v)],t[disp(v,u)]) for t in w)
             for v in range(n)] for u in range(n)]
    mat=[[int(any(add(el[u],t,mod)==el[v] for t in s))
          for v in range(n)] for u in range(n)]
    assert all(sum(row)==3 for row in mat)
    assert all(mat[u][u]==0 for u in range(n))
    return {'group':mod,'support':s,'n':n,'cp':poly(w),
            'inv':inv,'colors':colors,'matrix':mat}
def exact_iso(g,h):
    # Any Cayley isomorphism can be postcomposed with a target translation
    # to send the identity (vertex 0) to vertex 0.
    n=g['n'];assert n==h['n']
    a,b=g['colors'],h['colors']
    candidates={u:[v for v in range(n) if a[0][u]==b[0][v]
                 and a[u][0]==b[v][0]] for u in range(n)}
    mapping={0:0};used={0}
    def solve():
        if len(mapping)==n:
            assert all(g['matrix'][u][v]==h['matrix'][mapping[u]][mapping[v]]
                       for u in range(n) for v in range(n))
            return tuple(mapping[u] for u in range(n))
        best=None;choices=None
        for u in range(1,n):
            if u in mapping:continue
            opts=[v for v in candidates[u] if v not in used and all(
                  a[u][i]==b[v][j] and a[i][u]==b[j][v]
                  for i,j in mapping.items())]
            if not opts:return None
            if choices is None or len(opts)<len(choices):
                best=u;choices=opts
                if len(opts)==1:break
        for v in choices:
            mapping[best]=v;used.add(v)
            result=solve()
            if result is not None:return result
            used.remove(v);del mapping[best]
        return None
    return solve()
def c2(n):return n*(n-1)//2
def partition(graphs,label):
    spec=defaultdict(list);fing=defaultdict(list)
    for g in graphs:
        spec[g['cp']].append(g)
        fing[(g['cp'],g['inv'])].append(g)
    iso=[];checks=0;cross=[]
    for group in fing.values():
        parts=[]
        for g in group:
            for cl in parts:
                checks+=1
                permutation=exact_iso(g,cl[0])
                if permutation is not None:
                    if g['group']!=cl[0]['group'] and len(cross)<3:
                        cross.append({'group_a':list(g['group']),
                         'support_a':list(map(list,g['support'])),
                         'group_b':list(cl[0]['group']),
                         'support_b':list(map(list,cl[0]['support'])),
                         'mapping':list(permutation)})
                    cl.append(g)
                    break
            else:parts.append([g])
        iso.extend(parts)
    pc=sum(c2(len(v)) for v in spec.values())
    pf=sum(c2(len(v)) for v in fing.values())
    pi=sum(c2(len(v)) for v in iso)
    assert pc>=pf>=pi
    return {'scope':label,'graphs':len(graphs),
     'spectral_classes':len(spec),'two_point_classes':len(fing),
     'iso_classes':len(iso),'cospectral_support_pairs':pc,
     'separated_by_two_point':pc-pf,
     'nonisomorphic_cospectral_pairs':pc-pi,
     'nonisomorphic_not_separated':pf-pi,
     'isomorphism_checks':checks,
     'cross_group_isomorphism_witnesses':cross}
def main():
    rows=[];by_order=defaultdict(list)
    for mod in GROUPS:
        el=tuple(product(*(range(d) for d in mod)))
        z=(0,)*len(mod)
        supports=list(combinations([v for v in el if v!=z],3))
        gs=[graph(mod,s) for s in supports if generated(s,mod)]
        name='x'.join(map(str,mod))
        r=partition(gs,name);r['all_nonzero_supports']=len(supports)
        assert (r['graphs'],r['spectral_classes'],r['iso_classes'])==EXPECTED_GROUP[name]
        rows.append(r);by_order[prod(mod)]+=gs
        print('GROUP',name,r['graphs'],r['spectral_classes'],r['two_point_classes'],r['iso_classes'])
    orders=[]
    for n,gs in sorted(by_order.items()):
        r=partition(gs,'all-noncyclic-groups-order-'+str(n))
        assert (r['graphs'],r['spectral_classes'],r['two_point_classes'],
                r['iso_classes'],r['nonisomorphic_cospectral_pairs'])==EXPECTED_ORDER[n]
        assert r['nonisomorphic_not_separated']==0
        orders.append(r)
        print('ORDER',n,r['graphs'],r['spectral_classes'],r['two_point_classes'],r['iso_classes'],r['nonisomorphic_cospectral_pairs'])
    mod=(2,6);S=((0,1),(0,3),(1,0));T=((0,1),(0,5),(1,1))
    g=graph(mod,S);h=graph(mod,T)
    assert g['cp']==h['cp'] and g['inv']!=h['inv'] and exact_iso(g,h) is None
    el=tuple(product(range(2),range(6)))
    w1=walks(el,S,mod);w2=walks(el,T,mod)
    assert sorted(w1[2][el.index(x)] for x in S)==[4,5,6]
    assert sorted(w2[2][el.index(x)] for x in T)==[3,6,6]
    data={'program':'SPEC-OBS-06',
     'scope':'all loopless generating 3-element supports in listed noncyclic abelian groups',
     'groups':rows,'orders':orders,
     'witness':{'group':[2,6],'support_s':list(map(list,S)),
       'support_t':list(map(list,T)),
       'edge_length3_s':[4,5,6],'edge_length3_t':[3,6,6],
       'characteristic_polynomial_coefficients':list(g['cp'])}}
    if len(sys.argv)>1:
        with open(sys.argv[1],'w',encoding='utf-8') as f:
            json.dump(data,f,indent=2);f.write('\n')
    print('SPEC-OBS-06 EXACT SEARCH COMPLETED')
if __name__=='__main__':main()
