# SPEC-OBS-06 — Noncyclic abelian Cayley digraphs of valency three

**Status:** E = reproducible exact finite classification within explicitly listed corpus; N = **NON AUDITÉE**, no novelty or priority claim; Q = independent VF2 validation of all six vertex orders and independent symbolic characteristic polynomial verification of the witness. Remains in draft PR #6.

## Frozen protocol and domain

Enumerate all three-element subsets S not containing the identity of each group G in C2×C2, C2×C4, C2³, C3², C2×C6, C4², C2×C8, C2²×C4, C2⁴, C3×C6. Include exactly the supports generating the entire abelian group, so the corresponding **directed** Cayley graphs are strongly connected and loopless. Supports may contain inverses. Each graph is 3-out-regular.

Compute (1) integer adjacency characteristic polynomial through traces and Newton identities; (2) isomorphism-invariant two-point walk fingerprint I_n of SPEC-OBS-02, including both directions and walk lengths 1..|G|; (3) exact graph isomorphisms via backtracking with explicit adjacency preservation. Isomorphism partitioning is also performed **across distinct underlying noncyclic groups of the same order**, not just within each group.

## Results: full within stated finite scope

| Order | graphs | spectral classes | two-point classes | isomorphism classes | cospectral nonisomorphic support pairs |
|---:|---:|---:|---:|---:|---:|
| 4 | 1 | 1 | 1 | 1 | 0 |
| 8 | 60 | 5 | 5 | 5 | 0 |
| 9 | 56 | 3 | 3 | 3 | 0 |
| 12 | 134 | 15 | 16 | 16 | 144 |
| 16 | 928 | 33 | 33 | 33 | 0 |
| 18 | 584 | 18 | 18 | 18 | 0 |

Overall: 1,763 generating supports; 42,129 cospectral unordered pairs of supports; 144 are nonisomorphic; **all 144 are distinguished by I_n**. An order-16 subgroup C2^4 has zero generating triplets, because it needs four generators; do not confuse this with zero possible Cayley graphs of other valencies. Distinct support pairs are not independent mathematical phenomena. Finite absence of counterexamples is not a universal classification theorem.

## Intrinsic n=12 nonisomorphism witness

In G=C2×C6 choose
S={(0,1),(0,3),(1,0)}, T={(0,1),(0,5),(1,1)}.
Their exact characteristic polynomial coefficients, from x^12 downward, coincide:

`[1,0,-12,0,36,0,-82,0,12,0,-36,0,81]`.

On the three directed connections, the multiset of three-step walk counts equals [4,5,6] for S and [3,6,6] for T. The full edge-restricted histogram repeats each of these values 12 times. This is invariant under graph isomorphism, therefore the graphs are not isomorphic. The full I_n signatures differ first at horizon 3.

## Higher-order refinement (separate pilot, not all 1763 graphs)

On that witness, a direct implementation of the explicitly defined tuple-color algorithms found:
- 2-WL with separately aggregated coordinate replacements: no difference through six rounds (stationary).
- correlated 2-FWL: difference on round 1;
- 3-WL with separate replacements: difference on round 1;
- correlated 3-FWL: difference on round 1.

This is a **single-witness pilot**. No all-corpus WL completeness claim is made. The term FWL means the *joint* multiset of coordinate-replacement color vectors for a common replacement vertex, as distinguished from separately aggregated WL.

## Independent controls and reproduction

The main standard-library script `reproducibility/verify_spec_obs_06.py` enumerates the corpus and asserts expected class numbers. A separate local audit with NetworkX VF2 independently recomputed actual isomorphisms in **all spectral fibers at every order 4,8,9,12,16,18**; the class counts agree. SymPy independently verified the exact witness polynomial and NetworkX verified its non-isomorphism. The dependencies of these optional independent controls are not dependencies of the committed standard-library main script.

Frozen summary: `reproducibility/results/spec_obs_06_exact_summary.json`. The full local classification file includes per-group rows and selected explicit cross-group isomorphism permutations; it is **not** part of the frozen JSON summary and must not be assumed archived there.

## Interpretation and research continuity

This extends *finite* SPEC-OBS-03 evidence from cyclic to enumerated noncyclic abelian groups at valency three, and does not overturn SPEC-OBS-04/05: the Shrikhande/rook obstruction is valency six. Possible next steps: preregister further group orders or valencies; seek actual non-isomorphic graphs with identical I_n; compare WL refinements with coherent configurations and exact group invariants, while keeping the tested families separate.

**No claim of originality**: antecedent search incomplete. N remains NON AUDITÉE; no Lean proof, no stable release, no merge, no change to manuscripts 10A6/10C3/10B1.
