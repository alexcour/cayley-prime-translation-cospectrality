# D9 — independent nauty computation, 21 October 2026

**Follow-up:** explicit certificates now verify every member map and all 66 representative separations without nauty/VF2. The 12 representatives have distinct spectra, and traces 6 and 9 already separate them. See `D9_EXPLICIT_CERTIFICATES_2026_10_21.md`. The historical VF2 membership reserve below remains open.

**Result:** nauty independently finds **12 directed isomorphism classes** among the **594** generating identity-free three-element right-Cayley supports on D9 (order 18). Ten classes have 54 supports and two have 27. **No VF2 computation was rerun.** The complete nauty partition, input matrices, digraph6 files, original-label representatives, canonical labels, commands, logs, software identities and SHA-256 manifests are archived under `reproducibility/results/d9_nauty_20261021/`.

## Frozen source and search boundary

Source PR: https://github.com/alexcour/cayley-prime-translation-cospectrality/pull/6

Source HEAD: `89d2709f03bc003b97ebb36765786935b97de0a3`, branch `research/spec-obs-01-rooted-observations`.

- Corpus/VF2 script: `reproducibility/verify_spec_obs_09.py`, SHA-256 `e8c1ca53872bf141241ea9ea2b9628184cdb66621704304b33fb340ae12e35aa`.
- Historical result: `reproducibility/results/spec_obs_09_D9_exact_summary.json`, SHA-256 `798170f8941f03a6a7be36f6ca3c065d2ce1e7ac3ad2d2e478047e9092510993`.
- Preregistration: `docs/SPEC_OBS_09_PREREG.md`.
- The priority erratum `docs/SPEC_OBS_09_ERRATUM_2026_10_09.md` remains applicable: the pair {1,9,12}/{1,9,13} is **not cospectral**. This replay does not test or promote joint spectral reconstruction.

All 15 remotely advertised branches were cloned and searched before implementation. No nauty/direct6/digraph6/shortg/amtog implementation or full VF2 membership table was found in their tracked text. The search terms, exact refs and commit SHAs are archived in `branch_inventory.json` and `search_provenance.json`. A commit-message search also returned no matches. This is not a statement about unavailable local work, deleted branches, unadvertised refs or external environments.

## Representation and controls

Elements are indexed 0..8 for (a,0), 9..17 for (a,1); multiplication is `(a,b)(c,d) = (a + (-1)^b*c mod 9, b+d mod 2)`. Arcs are **u → u*s**, not an undirected edge or a left-multiplication substitution. Enumeration uses lexicographic three-subsets of 1..17 and retains precisely the 594 generating supports. Each graph has 18 vertices, 54 arcs, in/out-degree 3 and no loops.

The new script generates these matrices with a separate index formula and verifies all 594 against the frozen script's corpus definitions. It extracts only pure corpus/motif definitions by AST; it imports neither NetworkX nor the old script's `main` or VF2 helpers. The existing VF2 script and historical summary are unchanged.

The compact directed format called **direct6** in the correspondence is called **digraph6** by gtools. Files start with `&`; all 18×18 entries, including diagonal zeros, are encoded row by row. `amtog -z` produces exactly the same bytes as the Python encoder; `listg -A` recovers every adjacency matrix exactly. An asymmetric control digraph and its transpose remain two separate classes, checking that arc directions were not discarded.

Commands actually executed (Ubuntu binaries have the `nauty-` prefix):

```sh
nauty-amtog -z corpus.am amtog.d6
nauty-listg -A corpus.d6 listg.am
nauty-shortg -fa -k -v corpus.d6 rooted-representatives.d6
nauty-shortg -k -v corpus.d6 unrooted-representatives.d6
nauty-labelg -fa corpus.d6 rooted-canonical.d6
nauty-labelg corpus.d6 unrooted-canonical.d6
nauty-labelg -fa relabelled.d6 relabelled-canonical.d6
```

The `-v` logs preserve the membership of every shortg class. Their partitions agree with those recovered from labelg, both with and without `-fa`. `-k` preserves input labels; its output strings are not canonical labels. Class IDs N01..N12 are assigned by first corpus occurrence, not treated as mathematical invariants.

`-fa` distinguishes vertex 0 from the remaining vertices. On vertex-transitive graphs, any isomorphism can be followed by a target automorphism carrying the image of vertex 0 to vertex 0; the rooted restriction therefore preserves the unrooted classes on this corpus. This argument does not justify this optimisation for arbitrary graphs. Equality of rooted/unrooted partitions was checked explicitly, as was invariance of all 594 rooted canonical strings after deterministic random relabellings (seed 20261021).

## Comparison with the historical VF2 evidence

| Check | Outcome |
| --- | --- |
| Same 594 supports and right-directed matrices | Exact equality checked |
| Historical VF2 total 12; new nauty total 12 | Agrees independently |
| Historical 10 four-motif fibres | Recomputed without VF2: 10 |
| Number of motif fibres containing two nauty classes | 2; the other 8 contain one |
| {1,8,9} versus {9,10,11} | N05 versus N11; distinct |
| {1,9,12} versus {1,9,13} | N08 versus N09; distinct |
| Full historical VF2/nauty membership equality | **Not established: historical memberships unavailable** |

The frozen VF2 JSON stores 663 comparisons, the total number of classes and four witness supports. It does **not** store the class of each of the 594 supports. Agreement of class counts and witnesses must not be reported as equality of full partitions. No representation, orientation or labelling discrepancy was detected by the controls above; a full historical classification discrepancy cannot be excluded without the missing table.

The new comparator accepts an existing archived CSV with columns `support,class` (support written as a quoted comma-separated triple). It requires exactly the same support set, rejects duplicates/missing/extraneous supports and compares classes independently of their IDs. It records a contingency table, splits and merges, and fails on inequality. Its positive test permutes class IDs; negative tests introduce a split and a merge. Do not pass the new nauty CSV off as an old VF2 reference.

```sh
python3 reproducibility/verify_d9_nauty.py --out /tmp/d9-nauty
# Only if the actual historical membership table is recovered:
python3 reproducibility/verify_d9_nauty.py --out /tmp/d9-comparison \
  --vf2-partition /path/to/archived-vf2.csv
```

## Environment, replay and scope

The observed Ubuntu package is `nauty 2.8.8+ds-5`; its `--version` prints `Nauty&Traces version 2.8081 (64 bits)`. Both values are preserved rather than silently normalised. Package `libnauty-2.8.8` is `2.8.8+ds-5`, and `libcliquer1` is `1.21-3build1`. Exact package hashes, snapshot URLs, binary/library hashes and Python/platform details are archived. In the initial environment packages were downloaded and extracted into `/tmp/nauty-root`; no system-wide installation was required. Standard Ubuntu replay uses `sudo apt-get install nauty=2.8.8+ds-5`, then the command above. The script records the actual versions for each replay.

The dedicated CI workflow performs this nauty replay and compares its partition with the archived **nauty** partition; that check is explicitly not called an old VF2 comparison. Replayed outputs are separate artifacts and do not overwrite the initial evidence. Verify archived bytes with `sha256sum -c SHA256SUMS` inside the result directory. Absolute initial paths are in `commands.json`; the portable command forms are above.

**Scientific status:** independent computation using nauty rather than VF2 on this finite corpus. This is not an independent human peer review, a general mathematical theorem, an originality determination, or validation of the programme by Brendan McKay. His contribution is the recorded methodological advice. No new correspondence is sent. D10, D11, D12 and S4 remain untested here. PR #6 remains draft, and no stable release or publication claim is advanced.
