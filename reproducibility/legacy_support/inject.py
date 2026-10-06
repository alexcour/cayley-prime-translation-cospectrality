from math import comb
import sys
# injectivity of mu -> spectral class for T_mu in C_k x C_3 : compare closed-walk counts W(n) exactly
def lat_pts(k,mu,n):
    # points (w,c), w+c=n, w,c>=0 with w+mu*c = 0 mod k
    return [(w,n-w) for w in range(n+1) if (w+mu*(n-w))%k==0]
def W(k,mu,n,R):
    return sum(comb(n,w)*R[w][0] for w,c in lat_pts(k,mu,n))
bad=0; tested=0
for k in range(4,401,2):
    if k%3==0: continue
    mus=[m for m in range(2,k) if (m*m)%k==1]
    if len(mus)<2: continue
    Nmax=3*k
    R=[[0]*3 for _ in range(Nmax+1)]
    for w in range(Nmax+1):
        for b in range(w+1): R[w][b%3]+=comb(w,b)
    seqs={}
    for mu in mus:
        seqs[mu]=tuple(W(k,mu,n,R) for n in range(1,Nmax+1))
    vals=list(seqs.values()); tested+=1
    if len(set(vals))!=len(vals):
        bad+=1; print("COLLISION at k=",k,[m for m in mus])
print("k tested:",tested,"collisions:",bad)
