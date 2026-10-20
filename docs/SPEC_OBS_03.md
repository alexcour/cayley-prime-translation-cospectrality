# SPEC-OBS-03 — Exact isomorphism audit of two-point walk signatures

Research note; **E: exact finite check**, **N: NON AUDITÉE**, **Q: independently cross-checked with NetworkX VF2 (local only)**. This work remains confined to draft PR #6 and does not modify manuscript, publication status or prior-art claims.

## Scope and definitions

All three-element subsets S of cyclic group Z/nZ at n=8,10,12,14,15,16,18,20. Directed Cayley adjacency A_uv=1 iff v-u in S; loops permitted. Spectral partition uses the exact integer characteristic polynomial, via Newton identities and length <=n cyclic walk counts. The two-point partition uses multiset of vectors ((A^k)uv,(A^k)vu) over ordered vertex pairs and 1<=k<=n. The isomorphism partition uses an exhaustive adjacency-preserving backtracking permutation search fixing 0, after unit-multiplier orbit reductions (valid since translating a Cayley graph permits any isomorphism to fix 0). Color constraints prune the search but accepted witnesses preserve directed adjacency via k=1. A second, independent VF2 NetworkX calculation of graph isomorphisms agrees with all final class counts.

## Exact finite results

| n | supports | spectral classes | two-point classes | exact isomorphism classes | cospectral support pairs | nonisomorphic among them | unresolved nonisomorphic |
|---|---:|---:|---:|---:|---:|---:|---:|
| 8 | 56 | 19 | 19 | 19 | 67 | 0 | 0 |
| 10 | 120 | 32 | 32 | 32 | 172 | 0 | 0 |
| 12 | 220 | 71 | 72 | 72 | 287 | 16 | 0 |
| 14 | 364 | 64 | 64 | 64 | 884 | 0 | 0 |
| 15 | 455 | 65 | 65 | 65 | 1479 | 0 | 0 |
| 16 | 560 | 85 | 85 | 85 | 1783 | 0 | 0 |
| 18 | 816 | 147 | 148 | 148 | 2008 | 36 | 0 |
| 20 | 1140 | 172 | 172 | 172 | 3569 | 0 | 0 |
| **Total** | **3731** | **655** | **657** | **657** | **10249** | **52** | **0** |

The totals of classes are sums across **distinct graph orders** and are not one combined isomorphism classification. The 52 pairs are pairs of supports, not 52 unrelated novelty claims. There are 10,197 isomorphic support pairs inside spectral collision fibers.

## Connected loopless stratification (pre-specified follow-up)

| n | supports | spectral classes | two-point classes | exact isomorphism classes |
|---|---:|---:|---:|---:|
| 8 | 34 | 10 | 10 | 10 |
| 10 | 80 | 21 | 21 | 21 |
| 12 | 154 | 44 | 45 | 45 |
| 14 | 266 | 46 | 46 | 46 |
| 15 | 360 | 49 | 49 | 49 |
| 16 | 420 | 54 | 54 | 54 |
| 18 | 614 | 103 | 104 | 104 |
| 20 | 884 | 119 | 119 | 119 |

The loopless connected subcorpus remains fully separated by the two-point signature at these orders. It does NOT imply a universal completeness theorem.

## Important non-affine isomorphisms

Multiplication by a unit modulo n is *not* an exhaustive isomorphism test even here. For example on Z/8Z the supports {1,5,6} and {1,2,5} are isomorphic via the 0-fixed vertex mapping [0,1,6,7,4,5,2,3], although they belong to different unit-multiplier orbits. Similar phenomena occur at n=16. The exact search and independent NetworkX VF2 validation prevent spuriously counting these as nonisomorphic.

## Reproducibility, qualifications and next test

Run `python3 reproducibility/verify_spec_obs_03.py` (standard-library only). The full locally generated dataset includes witness permutations, counts, and stratifications. The independent NetworkX VF2 audit was executed in the local analysis environment and matched all eight orders; VF2 code/results are not yet deposited as a separate GitHub artifact. The GitHub script embeds the exact expected-count regression oracle.

**Evidence boundary:** this is not a novel theorem, general characterization, complete prior-art audit, verified Lean formalization, or external scientific publication. An isolated finite coincidence, however exhaustive within its declared bounds, cannot certify an infinite-family statement. E/N/Q remain separate; N=NON AUDITÉE; human review outstanding. **Next:** determine a structural explanation for completeness at these orders, then preregister larger n and alternative families with possible counterexamples.
