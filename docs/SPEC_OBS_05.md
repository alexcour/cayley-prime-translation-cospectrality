# SPEC-OBS-05 — 3-WL versus 3-FWL: a bounded exact witness

Status: exact finite reproduction and elementary proof; known antecedent for graph pair and WL hierarchy. No priority claimed. N = NON AUDITÉE for any new claim; external review open. Work remains on the draft research branch.

**Graphs.** Rook(4,4) and Shrikhande on G=(Z/4Z)^2 with supports specified in SPEC_OBS_04.md. Both have SRG parameters (16,6,2,2), with A²=4I+2J and AJ=6J. Hence identical two-point walk signatures for every horizon; nonisomorphism is established by K4 counts 8 and 0.

**Precise algorithms.** A k-tuple receives its complete initial equality/adjacency pattern. Standard k-WL updates the color using separately sorted multisets of the colors obtained by replacing each individual coordinate with w in V. Folklore k-FWL instead jointly records a multiset over w of the k-vector of all those replacement colors. Both algorithms assign colors canonically across the two graphs. They are different algorithms: 3-FWL has the distinguishing power of standard 4-WL, not standard 3-WL.

**Exact test:** standard 2-WL and 3-WL fail to distinguish; 2-FWL fails too; 3-FWL distinguishes at its first round (15 initial triple colors in both graphs; 15 versus 22 colors after one round). The decisive direct witness counts extensions of triangles to K4. Both graphs have 32 triangles. Every rook triangle has one fourth common neighbor; every Shrikhande triangle has zero. The common-neighbor induced-edge statistic for each of the 48 unoriented edges gives 1 in rook and 0 in Shrikhande. Permutation relabeling control passed.

**Proof:** an ordered triangle triple (u,v,w) has initial color coding three adjacencies. In the joint 3-FWL update the entries for a replacement vertex z encode whether z is adjacent to all of u,v,w simultaneously: all three replacement triples are triangles exactly when z is such a common neighbor. Thus at round one 3-FWL separates the triple-color histograms. Standard 3-WL separately aggregates the three lists, losing this cross-coordinate correlation. The stable 3-WL indistinguishability is confirmed by exact computation and consistent with published antecedents.

**Reference points (prior art, NOT novelty evidence):** https://www.cs.ox.ac.uk/files/12536/L6.pdf ; https://openreview.net/pdf?id=lxHgXYN4bwl ; https://proceedings.neurips.cc/paper/2021/file/157792e4abb490f99dbd738483e0d2d4-Supplemental.pdf .

**Boundary:** neither a novel graph pair nor a newly discovered algorithm. No universal theorem about all Cayley graphs, no modification to 10A6/10C3/10B1, no release change. Next: test 3-FWL on strictly preregistered noncyclic families and seek counterexamples; formalize the elementary triangle-extension argument in Lean only after the exact implementation is archived.
