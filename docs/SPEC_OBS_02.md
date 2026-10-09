# SPEC-OBS-02 — Invariants intrinsèques à deux sommets et collisions spectrales

**Research note / finite exact exploration (2026-10-08).** Scope: cyclic Cayley *digraphs* on `Z/nZ`, three distinct connection elements, **loops allowed**, adjacency over the integers. This extends SPEC-OBS-01 only on the draft research branch, not the stable manuscript or its public claim boundary.

**Status:** E = mathematical invariance and finite-horizon lemma proved below; finite examples checked exactly. N = **NON AUDITÉE** (no novelty or priority claim). Q = reproducible Python standard-library computation and independent small-case determinant cross-check; human review open.

## 1. Isomorphism-invariant observation

For a digraph with adjacency matrix `A`, define the two-point walk fingerprint for a finite horizon `H >= 1`:

`I_H(A) = multiset_{(u,v) in V x V} ( ((A^k)[u,v],(A^k)[v,u]) )_{k=1..H}`.

This multiset includes diagonal pairs and preserves the ordering within each pair of directed walk counts. A permutation relabeling `B=P A P^{-1}` sends `(u,v)` to `(P(u),P(v))`; therefore `I_H(A)=I_H(B)`. **If these multisets differ, the digraphs are nonisomorphic. The converse is NOT asserted.**

For `Z/nZ` with support `S` and `A[u,v]=1 iff v-u in S`, let `w_k(d)` be the coefficient of `x^d` in `(sum_{s in S} x^s)^k` modulo `x^n-1`. Then `(A^k)[u,v]=w_k(v-u)`. Every displacement occurs in exactly `n` ordered pairs, so the reduced invariant computed by the script is the multiset over `d in Z/nZ` of `((w_k(d),w_k(-d)))_{k<=H}`. Multiplying every multiplicity by `n` recovers `I_H(A)`.

### Finite-horizon lemma (under cospectrality)

If two `n x n` matrices have the same characteristic polynomial, Cayley-Hamilton gives **the same** order-`n` recurrence for every sequence `((A^k)[u,v],(A^k)[v,u])`, for `k>=1`. Consequently, equality of the two multisets `I_n` implies equality of `I_H` for *every* `H>=n`: a multiset matching of the initial `n` tuples remains a matching when each tuple is extended by the common recurrence. Thus examining horizons `1..n` is exhaustive **for this invariant** on a cospectral pair, not for all possible isomorphism invariants.

## 2. Concrete n=12 certificate

Known cospectral circulant supports (not a new example):
`S={1,3,9}` and `T={1,5,7}` in `Z/12Z`.

Both exact characteristic polynomials equal
`x^12 - 12*x^10 + 36*x^8 - 80*x^6 - 12*x^4 + 36*x^2 - 81`.

Define an edge-restricted local statistic
`E_k(A)=multiset_{(u,v):A[u,v]=1} (A^k)[u,v]`.
This is an isomorphism invariant for **any** directed graph. For `k=3`, the reduced histogram (one copy of each of three differences, all multiplicities multiplied by 12 for the full edge set) is:

| Walk count | S reduced count | T reduced count |
| --- | ---: | ---: |
| 3 | 0 | 1 |
| 4 | 1 | 0 |
| 5 | 1 | 0 |
| 6 | 1 | 2 |

Hence `E_3(S) != E_3(T)`: this **certifies nonisomorphism** of the digraphs without assuming the natural vertex labels match. `I_1` and `I_2` coincide; `I_3` differs. Remarkably, for this witness the unpaired marginal multiset `{w_k(d):d in Z/12Z}` is equal between the two graphs for each `k=1..12`; cross-length correlations recover information missed by those marginals.

## 3. Independent n=18 witness

On `Z/18Z`, take `S={1,5,13}` and `T={1,5,17}`. Exact characteristic polynomials agree. `I_1=I_2=I_3` but `I_4` differs. At length 4 alone, the reduced histogram of ordered `(w_4(d),w_4(-d))` differs:

- S has `(5,12),(8,10),(9,13),(10,8),(12,5),(13,9)` once each, along with common tuples.
- T has `(5,13),(8,9),(9,8),(10,12),(12,10),(13,5)` once each, along with common tuples.

The unpaired marginal multiset `{w_k(d)}` agrees for **each** `k=1..18`. This time retaining the two walk directions jointly already separates the graphs at one length.

## 4. Exhaustive finite sweep

All size-three subsets of `Z/nZ` were enumerated for the selected `n`, **including supports containing 0** (hence loops). A collision counts an unordered pair of **different support sets** with equal exact adjacency characteristic polynomial; it need not represent two nonisomorphic graphs. The final column counts collisions separated by `I_H` for some `H<=n`, with their first separating horizon.

| n | Supports | Spectral classes | Cospectral support pairs | Distinguished pairs (first H) |
| ---: | ---: | ---: | ---: | --- |
| 8 | 56 | 19 | 67 | 0 |
| 10 | 120 | 32 | 172 | 0 |
| 12 | 220 | 71 | 287 | 16 (H=3) |
| 14 | 364 | 64 | 884 | 0 |
| 15 | 455 | 65 | 1479 | 0 |
| 16 | 560 | 85 | 1783 | 0 |
| 18 | 816 | 147 | 2008 | 36 (H=4) |
| 20 | 1140 | 172 | 3569 | 0 |

The zeros **do not** show spectral determination or isomorphism: the invariant can fail to distinguish nonisomorphic graphs. The counts are not a classification of isomorphism classes or of general valency-three Cayley digraphs. No claim extends beyond these enumerated orders and support constraints.

## 5. Reproduction and checks

`python3 reproducibility/verify_spec_obs_02.py`

The standard-library script performs integer cyclic walk convolution, computes exact characteristic polynomials from traces via Newton identities, groups collisions, evaluates all horizons `1..n`, and asserts the table above. It checks relabeling invariance by an explicit nontrivial permutation and by a cyclic unit multiplier; it also checks the witness histograms. Independent SymPy determinant computations were carried out locally for the `n=12` and `n=18` witnesses (SymPy is **not** a dependency of the submitted script).

Source for fixed outputs: `reproducibility/results/spec_obs_02_exact_summary.json`. Reconstructed/current calculation, not a claim of historical original execution.

## 6. Comparison, next tests and boundaries

Relevant background includes Godsil's *Algebraic Combinatorics* graph-spectra material and work on walk matrices (Liu–Siemons, 2019; [arXiv:1911.00062](https://arxiv.org/abs/1911.00062)) and recent work on graph characterization by counts of walks ([Discrete Applied Mathematics, 2026](https://www.sciencedirect.com/science/article/pii/S0166218X25004536)). **These are leads, not a completed novelty audit**, and their graph conventions differ from directed loops-allowed supports.

Next: (i) remove loops and stratify generated/connected examples without changing the frozen counts; (ii) compute a certified isomorphism partition separately from the spectral partition and `I_H` partition; (iii) test whether the local edge histograms `E_k` suffice on a narrowly specified family; (iv) formalize isomorphism invariance and the finite-horizon lemma in Lean 4, with local no-sorry compilation checks. Preserve counterexamples and explicit negative controls.

**No change** to 10A6/10C3/10B1, prior-art status `N = NON AUDITÉE`, release gate, or manuscript. Public repository remains `0.1.x` review; no version bump, DOI, stable tag or external publication.
