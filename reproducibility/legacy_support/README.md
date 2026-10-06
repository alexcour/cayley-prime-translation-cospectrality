# Legacy support artifacts

These files are historical support/provenance artifacts copied from the Drive corpus. They are **not** the canonical current reproduction layer.

Included because the public staging surface refers to the corresponding finite examples or checks:

- `inject.py` — historical 10B1 injectivity scan script. The current internal theorem witness reports 83 relevant values of `k<=400` and zero collision.
- `local_cayley_certificates.py` — short graph-invariant certificates for the three U(210) primitive pairs. Requires `networkx`.
- `noncyclic_circulant_audit.py` — historical audit of cyclic Cayley representations; requires `networkx` and `local_cayley_certificates.py`.
- `PROOF_FAMILY.txt` — written proof/certificate note for the three collisions and `C_m x C_6`.
- `CERTIFICAT_COURET_CAYLEY_210_FAMILLE_2026-10-03.zip` — archived finite certificate package.
- `CERTIFICAT_C3_CP_COURET_2026-10-03.zip` — archived C3/Cp certificate package.

The original files are preserved without rewriting their scientific claims. New reproductions belong outside this directory.
