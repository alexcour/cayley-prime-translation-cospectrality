# SPEC-OBS-09 — FROZEN preregistration (before results)

Research branch, draft PR #6. Date: 2026-10-09. N = NON AUDITÉE.

Question: Does the complete induced directed four-vertex motif histogram distinguish all nonisomorphic degree-three Cayley digraphs in this new finite corpus?

Primary predeclared corpus in order: D9 (order 18), D10 (20), D11 (22), D12 (24), and S4 (24). Enumerate every three-element support not containing the identity and generating G. Edges g -> g*s (right Cayley), directed, no loops, strongly connected. Dm has order 2m, r^m=s²=1 and srs=r^-1. S4 uses lexicographically ordered permutations of (0,1,2,3). At order 24, compare graphs across D12 and S4.

Primary observables: exact adjacency characteristic polynomial (integer Newton identities); two-point walk signature I_n through length n (then Cayley–Hamilton); induced directed 3/4-vertex motif histograms canonicalized over all vertex permutations; graph isomorphism independently confirmed via directed NetworkX VF2.

Exact automorphism orbit reduction is permitted only with explicit orbit completeness and weighted multiplicities retained. Count unordered distinct support pairs within each fiber; distinguish support-pair counts from pairs of iso classes.

Success requires distinct isomorphism classes in one identical four-motif fiber, with explicitly indexed generator triples and exact VF2 plus a second nonisomorphism certificate. A zero count is negative evidence for the *completed* group alone.

Stop when computation impractical, transparently marking untouched groups INCOMPLETE. Never quietly modify corpus, edge conventions, no-loop/connectedness conditions, or decision criteria. Existing SPEC-OBS-08 D6 example is a regression control; sample motif relabeling invariance, exact orbit weights and support generation are required. Novelty not audited, no generalized theorem or priority claim.

Preserve main manuscripts and 10A6/10C3/10B1, stable-release NO-GO. Keep PR #6 draft.
