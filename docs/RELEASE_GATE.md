# Release gate

Current decision (11 October 2026): **GO PUBLIC REVIEW / 0.1.x; conditional GO UNREVIEWED ZENODO WORK ARCHIVE after Gate Z; NO-GO STABLE v1.0.0.**

## Gate R -- public review 0.1.x

The public `0.1.x` GitHub repository remains within Gate R only while all of the following remain true:

- `PUBLICATION_STATUS.md` states `PUBLIC REVIEW / 0.1.x` and `N = NON AUDITEE` for the general claims;
- `CLAIM_BOUNDARY.md` forbids priority/discovery wording while the antecedence audit is open;
- README and release notes state that the snapshot is unstable and intended for external review;
- reconstructed/current reproduction artifacts remain labeled by provenance;
- no workflow in this stage automatically creates a Zenodo DOI, HAL deposit, arXiv submission, or stable scientific release; an explicitly approved `0.1.x` Zenodo work archive can be deposited manually only after Gate Z;
- no `v1.0.0` tag is created in this stage.

**Gate R status: PASS for the published bounded public-review snapshot. Repository-side file/commit verification completed on 2026-10-07 at commit [`5e31912134fb6303639facedf4150d32255795bd`](https://github.com/alexcour/cayley-prime-translation-cospectrality/commit/5e31912134fb6303639facedf4150d32255795bd).**

The repository is public. After PR #1 was merged, [verify #4 (run 37585311793)](https://github.com/alexcour/cayley-prime-translation-cospectrality/actions/runs/37585311793) completed successfully on that exact merge commit: `exact-checks` and `manuscript-build` both passed.

## Gates still open before stable v1.0.0

- Confirm by independent review that the synchronized 10C3 wording (`3∣|H|` and the chord-lemma coincidence clause) leaves every downstream argument valid.
- Obtain an independent human mathematical review of 10A6 and 10C3.
- Complete the targeted primary-source antecedence checks listed in `PRIOR_ART.md`.
- Authorship, independent affiliation, ORCID and original-contribution licenses are confirmed for the review series by the author. Document funding/conflict statements and final archival citation details before a later stable/archival step.
- Pass clean-checkout reproducibility and manuscript build checks from the exact stable candidate.
- Review all public metadata again for claim-boundary compliance.

Closing Gate R does not close any of these stable-release gates.

## Gate Z -- optional Zenodo pre-review work archive (separate from stable release)

The author's 11 October 2026 policy permits a **non-peer-reviewed work archive before human mathematical review**, for external scrutiny. Its DOI identifies the deposited bytes, not proof, originality, priority or independent review. This is NOT an automatic permission to publish an unfinished snapshot.

Gate Z must be checked on the **exact frozen candidate** before upload: (1) all selected source/results/test/provenance files and commands are self-contained; (2) the SHA-256 manifest passes and exact-checks/manuscript-build succeed for the selected commit; (3) claims E/N/Q/D, prior art overlap and independent review pending are explicit; (4) no confidential FCI/patent material, personal data or third-party content without rights; (5) licences reviewed per code/text/data category, author/ORCID and AI assistance declared; (6) version, commit, DOI-ready metadata and new archive SHA-256 recorded. A failed CI or incomplete licence/sensitivity audit means **Gate Z = HOLD**, even though review is not yet available. After deposition, record only the DOI actually returned by Zenodo and preserve the initial version immutably.

The previous 2026-10-07 instruction `no Zenodo DOI before review` is superseded **only** for a compliant `0.1.x` non-peer-reviewed work archive. Independent review, priority checks and stable-release Gates B/C remain open.

## Explicitly deferred actions

Until a later governance decision after the open review/antecedence gates (Gate Z authorizes only the limited exception above):

- no `v1.0.0`;
- no **stable / validated** Zenodo record; pre-review `0.1.x` is governed separately by Gate Z;
- no HAL deposit;
- no arXiv submission;
- no presentation of the repository as a validated or stable scientific publication.
