#!/usr/bin/env python3
"""Exact finite checks for a prescribed translated Cayley support.

H = Z^2 / <(a,0),(b,d)>,  a,d>0, 0<=b<a.
Generators k=(1,0), k'=(0,1). This separate implementation recovers
the historical p=3 scan counts. Spectral calculations are exact.
"""
from __future__ import annotations
import argparse
from collections import Counter
from functools import lru_cache
from math import isqrt
import json
from pathlib import Path
import platform
import time

def prime(n):
    return n >= 2 and all(n % k for k in range(2, isqrt(n)+1))

def polynomial_exact_division(numerator, denominator):
    """Low-to-high integer coefficients, monic denominator."""
    remainder=list(numerator)
    quotient=[0]*(len(numerator)-len(denominator)+1)
    while len(remainder)>=len(denominator):
        shift=len(remainder)-len(denominator)
        factor=remainder[-1]
        quotient[shift]=factor
        for j,value in enumerate(denominator):
            remainder[shift+j]-=factor*value
        while remainder and remainder[-1]==0:remainder.pop()
    assert not remainder
    return tuple(quotient)

@lru_cache(maxsize=None)
def cyclotomic(n):
    result=(-1,)+(0,)*(n-1)+(1,)
    for divisor in range(1,n):
        if n % divisor==0:
            result=polynomial_exact_division(result,cyclotomic(divisor))
    return result

def in_lattice(r, t, a, b, d):
    return t % d == 0 and (r-b*(t//d)) % a == 0

def distinct_generators(a, b, d):
    return not in_lattice(1, -1, a, b, d)

def h_condition(a, b, d, p):
    return any((w*a) % p == 0 and (w*b+d) % p == 0 for w in (1, 2))

def beta_condition(a, b, d):
    return (a % 2 == 0 and (b+d) % 2 == 0
            and in_lattice(0, a, a, b, d)
            and in_lattice(d, b, a, b, d))

@lru_cache(maxsize=None)
def root_vectors(n):
    """Coefficients of X^j modulo Phi_n, in a fixed integer basis."""
    phi = cyclotomic(n)
    degree = len(phi)-1
    coeff = phi[:-1]
    current = (1,) + (0,)*(degree-1)
    result = []
    for _ in range(n):
        result.append(current)
        leading = current[-1]
        shifted = (0,)+current[:-1]
        current = tuple(shifted[i]-leading*coeff[i] for i in range(degree))
    assert current == result[0]
    return tuple(result)

def plus3(v1, v2, v3):
    return tuple(a+b+c for a,b,c in zip(v1,v2,v3))

def spectral_multisets(a, b, d, p):
    n = p*a*d
    roots = root_vectors(n)
    left, right = Counter(), Counter()
    for i in range(a):
        u = (n*i//a) % n
        for j in range(d):
            v = (p*(j*a-b*i)) % n
            for k in range(p):
                z = k*a*d
                left[plus3(roots[u], roots[(u+z)%n], roots[v])] += 1
                right[plus3(roots[(u+z)%n], roots[(u+2*z)%n], roots[(v+z)%n])] += 1
    assert sum(left.values()) == n == sum(right.values())
    return left, right

def reduce_element(r, t, a, b, d):
    quotient, residue = divmod(t, d)
    return ((r-b*quotient)%a, residue)

def adjacency(a, b, d, p, translated):
    elements = [(r,t,k) for r in range(a) for t in range(d) for k in range(p)]
    index = {e:i for i,e in enumerate(elements)}
    support = [(1,0,0),(1,0,1),(0,1,0)]
    if translated: support = [(r,t,(k+1)%p) for r,t,k in support]
    A = [[0]*len(elements) for _ in elements]
    for row,(r,t,k) in enumerate(elements):
        for dr,dt,dk in support:
            rr,tt = reduce_element(r+dr,t+dt,a,b,d)
            A[row][index[(rr,tt,(k+dk)%p)]] += 1
    return A

def characteristic_polynomial(A):
    """Faddeev-LeVerrier over integers; return monic high-to-low coefficients."""
    n=len(A)
    B=[[int(i==j) for j in range(n)] for i in range(n)]
    rows=[[(k,x) for k,x in enumerate(row) if x] for row in A]
    coefficients=[1]
    for step in range(1,n+1):
        C=[[sum(value*B[k][j] for k,value in row) for j in range(n)] for row in rows]
        trace=sum(C[i][i] for i in range(n))
        assert trace % step==0
        coefficient=-trace//step
        coefficients.append(coefficient)
        for i in range(n):C[i][i]+=coefficient
        B=C
    assert not any(any(row) for row in B)
    return tuple(coefficients)

def matrix_check(a,b,d,p):
    left,right = spectral_multisets(a,b,d,p)
    A,B = adjacency(a,b,d,p,False), adjacency(a,b,d,p,True)
    matrix_cospectral = characteristic_polynomial(A) == characteristic_polynomial(B)
    assert matrix_cospectral == (left == right)
    return {'hnf':[a,b,d], 'p':p, 'vertices':p*a*d,
            'matrix_cospectral':matrix_cospectral, 'h':h_condition(a,b,d,p),
            'beta':beta_condition(a,b,d) if p==3 else None}

def scan(p, bound):
    counts = Counter(); mismatches=[]
    for order in range(1,bound+1):
        for a in range(1,order+1):
            if order % a: continue
            d = order//a
            for b in range(a):
                if not distinct_generators(a,b,d):
                    counts['excluded_equal_generators'] += 1
                    continue
                left,right = spectral_multisets(a,b,d,p)
                cos = left == right
                hc = h_condition(a,b,d,p)
                bc = beta_condition(a,b,d) if p==3 else False
                expected = (hc or bc) if p==3 else hc
                counts['tested'] += 1
                counts['cospectral'] += cos
                counts['h'] += hc
                counts['beta'] += bc
                if p==3:
                    regime = 'without_3_torsion' if order%3 else 'with_3_torsion'
                    counts[regime+'_tested'] += 1
                    counts[regime+'_cospectral'] += cos
                    if order%3==0: assert not bc or hc
                    else: assert not hc
                if cos != expected:
                    mismatches.append({'hnf':[a,b,d],'cospectral':cos,'h':hc,'beta':bc})
    return {'p':p,'max_H_order':bound,'counts':dict(counts),'mismatches':mismatches}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--bounds', default='3:120,5:30,7:20,11:12',
                        help='prime:max_H_order, comma separated')
    parser.add_argument('--output',type=Path,default=Path('results.json'))
    args=parser.parse_args()
    start=time.monotonic()
    scans=[]
    for item in args.bounds.split(','):
        p,bound=map(int,item.split(':'))
        if p<3 or not prime(p):raise ValueError('Odd prime required')
        row=scan(p,bound); scans.append(row)
        print(json.dumps(row),flush=True)
    # C4 pair, reflection, loop obstruction, and rank-two example.
    examples=[matrix_check(4,1,1,3), matrix_check(5,3,1,5),
              matrix_check(1,0,5,5), matrix_check(3,0,3,3),
              matrix_check(3,2,1,3), matrix_check(6,0,1,3),
              matrix_check(5,2,1,5), matrix_check(9,4,1,3),
              matrix_check(12,7,1,3)]
    result={'description':'New exact HNF checks for the 2026-10-04 publication preparation',
            'python':platform.python_version(),'dependencies':'Python standard library only',
            'method':'Integer coefficient vectors modulo cyclotomic polynomial; matrices for examples',
            'scans':scans,'matrix_examples':examples,
            'elapsed_seconds':round(time.monotonic()-start,3),
            'all_checks_passed':all(not r['mismatches'] for r in scans)}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    if not result['all_checks_passed']:raise SystemExit(1)

if __name__=='__main__':main()
