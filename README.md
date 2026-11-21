# Cospectrality of a structured three-element support under prime cyclic translation

[Manuscript PDF](manuscript/structured_cayley.pdf) · [LaTeX source](manuscript/structured_cayley.tex) · **0.1.4-review · unstable public review snapshot**

Let $H=\langle\kappa,\kappa'\rangle$ be a finite abelian group with $\kappa\ne\kappa'$, and let $p$ be an odd prime. Identify a generator of $C_p$ with $1\in\mathbb F_p$. In $G=H\times\mathbb F_p$, put $T=\{(\kappa,0),(\kappa,1),(\kappa',0)\}$ and $T^+=T+(0,1)$. For a support $S$, the arcs are $g\to g+s$ for $s\in S$, with loops retained. Write $\operatorname{Spec}(S)$ for the multiset of complex adjacency eigenvalues, including multiplicities.

| Regime | Statement | Proof witness |
| --- | --- | --- |
| $p\ge 5$ | $\operatorname{Spec}(T)=\operatorname{Spec}(T^+)$ iff there is an additive homomorphism $h:H\to\mathbb F_p$ with $h(\kappa')=1$ and $h(\kappa)\in\{1,2\}$, iff a group automorphism of $G$ sends $T$ to $T^+$. | [10A6](proofs/theorem_pge5_10A6.txt) |
| $p=3$ | If $3\mid\lvert H\rvert$, cospectrality is equivalent to the same $h$ criterion. If $3\nmid\lvert H\rvert$, it is equivalent to $\beta(\Gamma)=\Gamma$, where $\Gamma=\{(\psi(\kappa),\psi(\kappa')):\psi\in\widehat H\}$, $\widehat H$ is the complex character group, and $\beta(u,v)=(-v,-u)$. | [10C3](proofs/theorem_p3_10C3.txt) |
| $p=3$, $H=C_k$, $k$ even, $3\nmid k$ | For each such $k$, $\mu\mapsto\operatorname{Spec}(T_\mu)$ is injective on $\{\mu\in(\mathbb Z/k\mathbb Z)^\times:\mu^2=1,\ \mu\ne 1\}$, with $T_\mu=\{(1,0),(1,1),(\mu,0)\}$. | [10B1](proofs/theorem_cyclic_injectivity_10B1.txt) |

The statements have internal proof witnesses (status E). Independent human review remains open. The [review guide](docs/OPEN_REVIEW.md) identifies individual proof steps and shows how to report a specific objection, earlier result, or replay result. Please cite the commit you checked.

## Replay the finite checks

Run from the checkout with Python 3 and its standard library. The script checks finite instances by exact arithmetic.

```bash
python3 reproducibility/verify_exact.py --output /tmp/results_local.json
```

## Relation to earlier work

Brown's Theorem 3.1 recovers the power-of-two subfamily with $\mu=1+k/2$, including the known 12-vertex pair. Mönius's Theorem 10 recovers adjacency cospectrality for $4\mid k$, $3\nmid k$, $\mu=1+k/2$. The positive $h$ cases have noncyclic ambient group $H\times C_p$. The [claim-by-claim comparison](PRIOR_ART.md#comparison-at-a-glance) details these correspondences and the open primary-source checks for Meng and Huang–Chang. Priority for the general statements remains unaudited.

## Status, provenance and reuse

[Publication status](PUBLICATION_STATUS.md) · [Claim boundary](CLAIM_BOUNDARY.md) · [Release gate](docs/RELEASE_GATE.md) · [Provenance](PROVENANCE.md) · [Reproducibility](REPRODUCIBILITY.md)

The stable release remains blocked. Cite a commit hash or review tag for a fixed reference.

Alexandre Couret, independent researcher, France · [ORCID](https://orcid.org/0009-0000-8246-7146). See [authorship and AI assistance](AI_ASSISTANCE.md) and [licensing](LICENSE.md).

[Présentation du programme en français](https://github.com/alexcour/couret-finite-verifications/blob/main/RESEARCH_VISION_FR.md) · [Research programme in English](https://github.com/alexcour/couret-finite-verifications/blob/main/RESEARCH_VISION_EN.md). The first-person plural in the linked vision refers to Alexandre Couret's work with AI assistants. Alexandre Couret is the author responsible for the programme.
