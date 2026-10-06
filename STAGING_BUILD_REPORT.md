# Historical staging report

The text below describes an earlier preparation state. The current review decision is in docs/RELEASE_GATE.md and PUBLICATION_STATUS.md; licenses are in LICENSE.md. This report is retained for provenance.

# Public-review staging build report

Build date: 2026-10-06
Version: 0.1.2-review
Mode: PUBLIC REVIEW / 0.1.x

Changes relative to 0.1.1-dev:

- replaced the obsolete `NO-GO PUBLIC` gate with a two-level decision: GO for bounded public review in `0.1.x`, NO-GO for stable `v1.0.0`;
- retained `N = NON AUDITEE` for the general priority/antecedence claims;
- kept independent human review explicitly open;
- strengthened the public claim boundary against discovery/priority wording while N remains open;
- disabled archival-publication preparation in this stage: no Zenodo DOI, HAL deposit, or arXiv submission;
- changed citation/status metadata from private staging to unstable public-review snapshot;
- preserved theorem witnesses, original historical artifacts, and proof/reproduction claims without expansion.

Scientific content was not promoted by this governance synchronization. This build changes publication posture, not mathematical truth status or priority status.

Verification required for this build:

- run the base exact verifier;
- syntax-check bundled Python files;
- compile the manuscript from the packaged LaTeX source when the local TeX toolchain is available;
- regenerate `SHA256SUMS.txt` after all edits;
- confirm no stale `NO-GO PUBLIC` / `PRIVATE STAGING` governance statement remains on the public candidate surface;
- confirm no archival integration metadata capable of encouraging a Zenodo/HAL/arXiv action is included as an active release instruction.
