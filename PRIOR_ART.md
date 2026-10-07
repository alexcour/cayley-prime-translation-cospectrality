# Prior-art status

Status date: 2026-10-07. **N = NON AUDITEE** for the general classification and the complete cyclic family. This update verifies particular bibliographic facts and one explicit overlap; it does not certify an exhaustive literature audit, independent mathematical review, or novelty.

## Repository statements being compared

The comparison concerns the statements in `manuscript/structured_cayley.tex` and the witnesses 10A6, 10C3 and 10B1, with their existing review status:

- `H = <kappa,kappa'>` is finite abelian, `kappa != kappa'`, `p` is an odd prime, `G = H x C_p`, `T = {(kappa,0),(kappa,1),(kappa',0)}`, and `T+ = T+(0,1)`.
- The invariant is the multiset of complex **adjacency** eigenvalues with multiplicities. The supports are directed and are not symmetrized; the repository retains a loop when the identity occurs.
- 10A6 (`p >= 5`): cospectrality is equivalent to an `h:H -> F_p` with `h(kappa')=1` and `h(kappa) in {1,2}`, and to an explicit group-automorphism isomorphism between this prescribed pair.
- 10C3 (`p = 3`): when `3` does not divide `|H|`, cospectrality is equivalent to `beta(Gamma)=Gamma`, where `Gamma` is the character-value subgroup and `beta(u,v)=(-v,-u)`; when `3` divides `|H|`, the homomorphism criterion applies.
- The cyclic specialization uses `H=C_k`, `p=3`, even `k` with `3` not dividing `k`, and `kappa=1`, `kappa'=mu`, where `mu` is a nonidentity unit with `mu^2=1 mod k`. Its ambient group is `C_{3k}`. Witness 10B1 concerns injectivity of `mu -> spectrum` inside this family, not classification of all cubic circulants.

A direct same-group circulant comparison requires `H x C_p` to be cyclic, hence `H` cyclic and `p` not dividing `|H|`. In a positive homomorphism case, surjectivity of `h` forces `p` to divide `|H|`; the product has noncyclic `p`-torsion. A theorem formulated on a cyclic group therefore does not directly cover that group presentation. This observation alone does not rule out a different cyclic representation of a digraph.

## Established overlap / priority retained from the earlier audit

- The 12-vertex circulant example is antecedent: equivalent pairs occur in Julia Brown's work and in Katja Mönius's thesis.
- Brown also contains an infinite subfamily corresponding to the power-of-two specialization `k=2^r`, `mu=1+2^(r-1)`.

These established entries are retained from `proofs/original_witnesses/PRIOR_ART_SOURCE_10D1_original.txt`; they are not newly inferred from an abstract. The 2020 article comparison below is separate from the 2021 thesis comparison.

## Verified bibliographic records and access evidence

| Work | Verified record | Evidence inspected on 2026-10-07 |
| --- | --- | --- |
| Meng 1998 | J. Meng, *Non-isomorphic cospectral Cayley digraphs*, **Graph Theory Notes of New York 35** (1998), 51-53. | Exact citation in Liu-Zhou's published bibliography, reference **[302]**, p. **158** ([journal PDF](https://www.combinatorics.org/ojs/index.php/eljc/article/download/v29i2p9/pdf)). This is secondary bibliographic corroboration; Meng's primary pages were not obtained. No DOI has been verified. |
| Huang-Chang 2001 | Qiongxiang Huang and An Chang, *Circulant digraphs determined by their spectra*, **Discrete Mathematics 240** (2001), 261-270. DOI [10.1016/S0012-365X(01)00198-4](https://doi.org/10.1016/S0012-365X(01)00198-4). | [Publisher record and abstract](https://www.sciencedirect.com/science/article/pii/S0012365X01001984), plus Liu-Zhou 2022, Theorem 93, which explicitly restates Huang-Chang Theorems 1--3 and their support/order hypotheses. A full primary PDF indexed at CORE remained inaccessible, so the restatement is authoritative secondary evidence rather than a substitute for primary reading. |
| Mönius 2020 | Katja Mönius, *Constructions of isospectral circulant graphs*, **Elemente der Mathematik 75**, no. 2 (2020), 45-57. DOI [10.4171/EM/404](https://doi.org/10.4171/EM/404). | [Publisher record](https://ems.press/journals/em/articles/16864) and [complete primary article in ETH's E-Periodica archive](https://www.e-periodica.ch/cntmng?bot=1&pid=edm-001%3A2020%3A75%3A%3A224), including visual inspection of Theorem 10, p. 54. |

### Meng: citation corroborated, primary comparison open

The title in the earlier file is corroborated by the published bibliography above; a failed index search does not establish a bibliographic error. This is not a substitute for reading the three primary pages.

The separately indexed Meng-Xu paper, *On the isomorphism problem of Cayley graphs of Abelian groups* ([publisher record](https://www.sciencedirect.com/science/article/pii/S0012365X98800071)), must not replace this entry merely because the author and year coincide.

Meng's group hypotheses, support construction, valency, spectral convention and conclusions remain unverified here. Consequently, no overlap or non-overlap with 10A6, 10C3, the cyclic family, or `C_m x C_6` is asserted. **N = NON AUDITEE** for each such comparison.

### Huang-Chang: order-level comparison only

The primary abstract specifies circulant orders `r^a` and `r^a s^b`, with distinct primes `r,s`; these symbols are kept separate from the repository's exterior prime `p`. It does not supply the exact support hypotheses needed for a theorem-level comparison. No unconditional determination-by-spectrum statement is inferred from the title or abstract.

The following are deductions from those order classes and the repository hypotheses, not claims about unread theorems:

- Positive `h` cases are not direct same-group circulant instances, by the noncyclicity observation above.
- For the cyclic specialization `n=3k`, the listed order classes intersect it precisely at `k=2^a` (`a>=1`): `n=2^a*3`. If even `k` has an odd prime factor other than `3`, then `n` has at least three distinct prime factors and lies outside those listed order classes.
- Coinciding orders do not establish coinciding support hypotheses or conclusions. In particular, `n=12` is in the stated order range and already contains an antecedent cospectral nonisomorphic pair; the abstract cannot be read as an unrestricted theorem for every support at that order.

Exact hypotheses and implications for `h`, `beta`, cyclic cospectrality, nonisomorphism and 10B1 remain pending primary reading. **N = NON AUDITEE**.

### Mönius: explicit primary-source overlap

The article allows directed, loop-free circulants and uses adjacency spectra (p. 46). Theorem 10 (pp. 54-55) gives cospectrality by partitioning odd equilibrium progressions of even length into equal halves. Use its complement branch with the additional set empty.

**Derived correspondence:** take `4|k`, `3` not dividing `k`, `mu=1+k/2`, `n=3k`. Use CRT coordinates `F(x,y)=a` with `a=x mod k`, `a=y mod 3`. Put

```text
S = F(T), P = F(T+), b = F(mu,2), a0 = F(1,0),
Eq = {a0 + j*n/6 mod n : 0 <= j < 6}.
```

Then `b` is a unit, `Eq` is one odd progression of length `d=6`, `S` contains three of its elements, and `bP=Eq\S`. Theorem 10 therefore recovers cospectrality of this entire subfamily. Multiplication by `b` preserves the adjacency spectrum. For `k=4`, `S={1,3,9}`, `P={1,5,7}`, `b=11`.

This establishes overlap for cospectrality. It does not establish antecedence of 10B1's injectivity, a nonisomorphism criterion, or the general `h`/`beta` classification. Other involutions remain unclassified by this comparison: **N = NON AUDITEE**.

The correspondence is an algebraic deduction in this update, not a quotation or a claim that the article names the repository family. A finite CRT check for all 67 eligible `k<=400` found no mismatch; that check supports the coordinate calculation and does not replace the general correspondence or independent review.

## Claim-by-claim audit boundary

| Repository claim | What this update establishes | Remaining status |
| --- | --- | --- |
| 10A6, `p>=5`, arbitrary finite abelian `H` | Cyclic source domains do not directly give its positive noncyclic group cases; this is not a novelty argument. | **N = NON AUDITEE**; Meng primary comparison and equivalent formulations remain open. |
| 10C3, ternary `h` and `beta` regimes | The article construction recovers the cospectrality subfamily specified above. | **N = NON AUDITEE** for the general equivalences. |
| Full cyclic involution family | Explicit Mönius overlap for `4|k`, `mu=1+k/2`, including `k=4`; previously established Brown overlap retained. | **N = NON AUDITEE** for other involutions and the complete family. |
| 10B1, spectral injectivity and family count | No antecedence conclusion is established by the comparison performed here. | **N = NON AUDITEE**. |
| `C_m x C_6` and noncyclic supporting examples | No primary Meng comparison was possible. | **N = NON AUDITEE**. |

## Context, not direct antedating by itself

- Poonen-Rubinstein: small vanishing sums of roots of unity used as an external proof dependency in 10A6.
- Lam-Leung: general background on vanishing sums of roots of unity.
- Toida / Dobson-Morris: CI context used in cyclic non-isomorphism arguments.
- Kovacs-Sinkovec: 3-DCI context for cyclic groups.
- Mans-Pappalardi-Shparlinski: spectral Adam-property context.

## Remaining primary-source gate

1. Obtain Meng's actual pp. 51-53 and compare its constructions and conclusions with each repository claim; the bibliographic corroboration is not this step.
2. Read Huang-Chang's complete theorem statements and proofs, retaining exact support restrictions and the spectral invariant. Secondary theorem summaries are not used here to close this gate.
3. Compare the remaining cyclic involutions with all relevant article constructions, and check equivalent group/support presentations before asserting exclusion.
4. Preserve the distinction between mathematical proof status, bibliographic priority and independent review.

The admissible formulation remains: the prescribed support-translation family is classified under the stated hypotheses; known constructions overlap explicit subfamilies; complete priority assessment remains in progress. **No novelty or priority claim is added.**
