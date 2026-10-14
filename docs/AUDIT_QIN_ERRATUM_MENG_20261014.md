# Cayley Gate C — Qin–Meng–Huang erratum and Meng source status (2026-10-14)

**Scope:** bibliographic audit only. No changes to theorem witnesses, software, licenses, external publication claims or mathematical proof statuses.

## Original and correction

- Z.-X. Qin, X.-P. Xu, J.-X. Meng and G.-P. Wang, *A Classification of Spectrum-determined Circulant Digraphs*, Acta Math. Appl. Sin. (English Series) 34 (2018), DOI [10.1007/s10255-018-0778-0](https://doi.org/10.1007/s10255-018-0778-0).
- Same authors, *Correction to “A Classification of Spectrum-determined Circulant Digraphs”*, Acta Math. Appl. Sin. (English Series) 37 (2021), 867–868, DOI [10.1007/s10255-021-1052-6](https://doi.org/10.1007/s10255-021-1052-6). [Primary two-page PDF](https://link.springer.com/content/pdf/10.1007/s10255-021-1052-6.pdf).

The authors explicitly withdraw the correctness of Lemma 4, Theorem 2 and Corollary 3 as originally stated in 2018. They give `n=3*5*7=105` with `phi(n)=48 < n/2=52.5`. The corrected theorem imposes a **three-distinct-odd-prime order** `n=p^a q^b w^c`, a totient inequality `phi(n)>n/2` and support restrictions. All the original 2018 theorem applications must be checked against the correction rather than cited as unchanged.

## Comparison by claim — theorem domain, not a novelty verdict

| Claim | Precise relevant domain | Does the corrected 2021 theorem directly cover it? | What remains open? |
| --- | --- | --- | --- |
| 10A6 | prescribed translation pair on `H x C_p`, `p>=5`, finite abelian `H` | **Not as a general theorem:** arbitrary `H x C_p` need not be cyclic; a specific cyclic presentation must be separately checked | Meng 1998 and equivalent Cayley-digraph formulations |
| 10C3 | prescribed pair with `p=3`, with distinct 3-torsion cases | **Not generally:** the corrected 2021 theorem is for special odd cyclic orders, not arbitrary `H x C_3` | beta criterion and known Brown/Mönius overlaps |
| 10B1 | cyclic `C_{3k}`, even `k`, `3∤k`, spectral injectivity among involutions | **No direct application:** the order `3k` is even, while the corrected theorem's specified order is odd | injectivity antecedence; other cyclic theorems could still be relevant |
| `C_m x C_6` examples | even `m`, generally not cyclic | **Not covered at stated generality** | Meng primary comparison indispensable |

Nonapplicability of one corrected theorem is **not proof** that the author's claim is new. The overlap of Brown (including a power-of-two cyclic subfamily) and Mönius (Theorem 10, DOI [10.4171/EM/404](https://doi.org/10.4171/EM/404), cospectrality for `p=3, 4|k, 3∤k, mu=1+k/2`) remains established as documented in [PRIOR_ART.md](../PRIOR_ART.md).

## J. Meng 1998 — primary not obtained

J. Meng, *Non-isomorphic cospectral Cayley digraphs*, *Graph Theory Notes of New York*, vol. 35 (1998), pp. 51–53. Reference corroborated by Liu–Zhou's published survey (2022), bibliography. **The three original pages have not been read**; no statement about its mathematical support or equivalence may be derived from the title.

Correspondence audit: an Outlook email entitled *Request for a copy of your 1998 paper on cospectral Cayley digraphs* was **sent 2026-10-08** to `mjx@xju.edu.cn`. No incoming reply from that address was located in the connected Outlook mailbox as of 2026-10-14. Do not repeat the same request as if no contact were made; use a polite follow-up or institutional library/archive channel if needed.

## Next steps and gate

1. Acquire pp. 51–53 with provenance, then record the exact **group / support / degree / eigenvalue convention / isomorphism conclusion** compared claim by claim with 10A6, 10C3, 10B1, `C_m x C_6`.
2. Compare all relevant corrected Qin–Meng–Huang cases, the full Huang–Chang (2001) text, Brown and Mönius statements at **support level**.
3. Maintain distinct states: internal proof claim `E`; bibliographic priority `N=NON AUDITÉE`; independent review `Q=OPEN`.

**Gate C remains open; Gate Z remains HOLD.** This audit adds no new DOI, release, peer-review claim, novelty claim or theorem proof.
