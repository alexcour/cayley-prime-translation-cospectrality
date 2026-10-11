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

Gate Z must be checked on the **exact frozen candidate** before upload:

1. All selected source/results/test/provenance files and commands are self-contained. Original historical files still missing must remain identified as missing; current/reconstructed reproductions may be used with their provenance labels.
2. The SHA-256 manifest passes and exact-checks/manuscript-build succeed for the selected commit. Historic CI success does not validate a changed commit or an independently assembled archive.
3. E/N/Q and publication status, known prior-art overlap and independent review pending are explicit. Finite computational agreement is not a universal proof, a priority determination or independent human review.
4. The selected files contain no confidential FCI/patent material, private personal data or third-party content without rights. Previously approved public author identity and cited authors' bibliographic names are distinguished from private data. Repository findings must be rechecked against the actual archive; uninspected external files are not cleared.
5. Licences are reviewed per code/text/data category, including historical containers; third-party rights are preserved. Author/affiliation/ORCID and AI assistance are declared. Funding and competing-interest statements require the author's actual declarations; missing statements must not be replaced by assumed negatives.
6. Version, reference commit, accurate DOI-ready metadata, selected-file manifest and new archive SHA-256 are recorded. Title/description must prominently say **UNREVIEWED RESEARCH ARCHIVE / NOT PEER REVIEWED** and obey `CLAIM_BOUNDARY.md`. No DOI is invented; record only the version DOI actually returned by Zenodo after an explicitly approved deposit, and preserve the initial archive immutably with corrections in a linked later version or erratum.

A failed CI or incomplete licence/sensitivity audit means **Gate Z = HOLD**, even though review is not yet available. **Current Gate Z status: HOLD.** This PR repairs repository governance and integrity; it does not supply a frozen archival package, final metadata, archive checksum or complete funding/competing-interest declarations. See [the documentary audit](PR9_DOCUMENTARY_AUDIT_2026-10-11.md). Approval or merge of this PR is not approval of an upload, DOI creation, release or tag; no such action is part of this step.

The previous 2026-10-07 instruction `no Zenodo DOI before review` is superseded **only** for a compliant `0.1.x` non-peer-reviewed work archive. Independent review, priority checks and all gates listed under **Gates still open before stable v1.0.0** remain open. The E/N/Q doctrine is defined in `docs/status_E_N_Q.md`.

## Explicitly deferred actions

Until a later governance decision after the open review/antecedence gates (Gate Z authorizes only the limited exception above):

- no `v1.0.0`;
- no **stable / validated** Zenodo record; pre-review `0.1.x` is governed separately by Gate Z;
- no HAL deposit;
- no arXiv submission;
- no presentation of the repository as a validated or stable scientific publication.
