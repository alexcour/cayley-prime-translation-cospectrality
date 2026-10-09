# Request for open mathematical review

Please help check this working preprint or identify an earlier theorem that covers all or part of it. No complete review or research-network membership is required to report a specific objection, reference or reproduction result.

## Reading order

| Review target | Source |
|---|---|
| Precise family, conventions and combined arguments | [Manuscript PDF](../manuscript/structured_cayley.pdf) · [LaTeX source](../manuscript/structured_cayley.tex) |
| Prime translation, p >= 5 | [Witness 10A6](../proofs/theorem_pge5_10A6.txt) |
| Ternary translation and torsion cases | [Synchronized witness 10C3](../proofs/theorem_p3_10C3.txt) |
| Spectral injectivity in the cyclic involution family | [Witness 10B1](../proofs/theorem_cyclic_injectivity_10B1.txt) |
| Known overlaps and unresolved priority comparisons | [Prior-art audit](../PRIOR_ART.md) |
| Exact finite reproduction | [Verification script](../reproducibility/verify_exact.py) |
| Scope and current publication status | [Claim boundary](../CLAIM_BOUNDARY.md) · [Release gate](RELEASE_GATE.md) |

The questions below can be answered separately: mathematical correctness, coverage by earlier work, and computational reproducibility. A partial review of one implication or one reference is useful. A successful replay alone does not establish correctness of a general proof or novelty. Please cite the exact reviewed commit.

## What to check

1. In the manuscript and witness 10A6: the short vanishing-sum argument, all allowed coincidences/repeated terms, the passage to a homomorphism h, and the automorphisms in the h(kappa)=1 and h(kappa)=2 cases. Check the full stated finite-abelian hypotheses, rather than only cyclic examples.
2. In the manuscript and synchronized witness 10C3: the unit-circle chord lemma including a=-b, multiplicities and zero values, the beta-symmetry case when 3 does not divide |H|, and the h criterion when 3 divides |H|. Check that h is an additive homomorphism H -> F_3 and that quotient/image steps follow under the stated hypotheses.
3. In the separate cyclic witness 10B1: the even-k / 3 not dividing k hypotheses, injectivity argument and use of historical computation. A finite injectivity scan alone does not prove the general statement.
4. In PRIOR_ART.md: the precise relation to Brown's already prior examples/subfamily and to Meng (1998), Huang-Chang (2001) and the Monius 2020 article. Give primary-source theorem and page numbers, and map hypotheses/conclusions. Distinguish a known example, special-case implication and full antedating.
5. In reproducibility/: replay the stated command from a clean checkout. Report Python version, commit, output and any mismatch; retain the distinction between original and new/reconstructed artifacts.

## Record a useful response

Open an issue using the proof, prior-art or reproduction template. Give the exact commit/version, the part checked, your argument or reference, and the consequence you think follows. An objection should identify a missing implication, hypothesis, counterexample or exact computation. A positive report should identify its checked scope and any remaining reservations. Reviews may be partial.

The author will link each relevant issue and correction from a dated version update. A closed issue alone does not certify a theorem or novelty; its resolution and checked scope must be documented. No external reviewer is claimed before an actual review is received.
