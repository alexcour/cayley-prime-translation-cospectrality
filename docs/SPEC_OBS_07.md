# SPEC-OBS-07 — Contre-exemples non abéliens de degré trois

**Statuts :** E = calcul fini exact, vérifié de manière indépendante par NetworkX VF2 et SymPy sur des témoins ; N = **NON AUDITÉE** pour l'antériorité ; Q = vérificateur Python reproductible. Cette note demeure dans la PR #6 *draft*, sans fusion ni publication stable.

## Corpus et conventions

Groupes diédraux D_m d'ordre **2m**, m=3,...,8 ; groupe quaternionique Q8 ; groupe alterné A4. Tous les supports **triples**, sans identité et générateurs, sont énumérés. Digraphes de Cayley de **multiplication à droite**, A[u,v]=1 si v=u*s. Connexes au sens fort, sans boucle, 3-sortants. Les groupes d'ordre égal sont comparés entre eux. Le produit non commutatif est utilisé directement et son associativité est contrôlée, afin de ne pas réutiliser indûment la convolution commutative.

La signature I_n est le multiensemble des vecteurs des marches ((A^k)[u,v], (A^k)[v,u]) pour 1<=k<=n et tous couples ordonnés. Elle est invariant d'isomorphisme ; Cayley–Hamilton permet de prolonger toute égalité entre matrices cospectrales à chaque horizon. Les véritables isomorphismes sont obtenus par permutations explicites préservant l'adjacence, avec contrôle indépendant de VF2.

## Résultats exacts par ordre

| Ordre | graphes | classes spectrales | classes I_n | classes isomorphes | paires cospectrales non isomorphes | non isomorphes que I_n ne sépare pas |
|---:|---:|---:|---:|---:|---:|---:|
|6|10|3|3|3|0|0|
|8|64|6|7|7|64|0|
|10|80|5|5|5|0|0|
|12|296|18|20|22|720|288|
|14|266|8|8|8|0|0|
|16|352|13|14|14|1024|0|

**Total :** 1 068 supports générateurs, 288 paires de supports non isomorphes dont la signature I_n ne distingue pas la structure. C'est un nombre de paires, non de phénomènes indépendants. Il y a 144 telles paires dans D6 et 144 dans A4, aucun autre cas indiscernable dans ce corpus. Les comptes sont exacts pour ce domaine, non une classification universelle. Le détail exhaustif du balayage est calculable par le script ci-dessous ; le fichier JSON gelé retient les résultats par ordre et les témoins.

## Témoins exacts

### Groupe D6 (ordre 12)

Codage r^a s^b, a mod 6, b mod 2, multiplié par (a,b)(c,d)=(a+(-1)^b c,b+d). Avec index identité 0, puis rotations r^1,...,r^5, puis s,rs,...,r^5s, prendre les supports **S={1,3,6}** et **T={1,6,8}**.

Même polynôme caractéristique (coefficients en puissances décroissantes) :
`[1,0,-12,0,30,0,-28,0,9,0,0,0,0]` soit x^4(x-3)(x-1)^3(x+1)^3(x+3). Même invariant I_12 et donc I_H pour tous les horizons H. Cependant le nombre d'ensembles indépendants de quatre sommets (sans arcs dans aucun sens entre leurs sommets) vaut **30 contre 33**. Il y a également égalité des histogrammes de motifs induits orientés à trois sommets, mais divergence à quatre sommets. La non-isomorphie a été confirmée indépendamment par NetworkX VF2.

### Groupe A4 (ordre 12)

Indices fixés par l'ordre lexicographique des 12 permutations paires de (0,1,2,3), l'identité d'abord ; composition p*q : (p[q[0]],...,p[q[3]]). Supports **S={1,3,5}** et **T={1,3,6}**.

Même polynôme caractéristique :
`[1,0,-6,-8,-9,0,44,48,-33,-64,-6,24,9]` soit (x-3)(x-1)^3(x+1)^6(x^2+3).
Même I_12 puis même I_H pour tout horizon. Non-isomorphes selon VF2 et selon un histogramme de motifs induits orientés à trois sommets : un motif « deux arcs issus d'un même sommet » apparaît 12 fois dans le premier, zéro fois dans le second.

## Pilote WL (non exhaustif)

Sur ces deux seuls témoins, sous la convention de couleurs initiales incluant les deux directions pour les paires :
- 2-WL à agrégats séparés ne distingue aucun témoin au premier état stabilisé.
- 2-FWL à substitutions corrélées distingue les deux témoins dès la première itération.
- 3-WL et 3-FWL distinguent le témoin D6 à l'itération 1 ; pour A4, les distributions initiales de configurations à trois sommets diffèrent déjà.

Ce pilote ne justifie aucun résultat universel sur WL.

## Fichiers et frontières épistémiques

- `reproducibility/verify_spec_obs_07.py` : construction explicite et tests exacts de tous les groupes ; script Python standard library, assertion des tableaux et des deux certificats locaux.
- `reproducibility/results/spec_obs_07_exact_summary.json` : comptes gelés et témoins.
- Audit indépendant local : NetworkX VF2 sur tous les ordres du corpus ; SymPy sur les polynômes des deux témoins.
- Documentation de référence : SPEC-OBS-01 à SPEC-OBS-06. Recherche d'antériorité inachevée, notamment sur les graphes de Cayley cospectraux et équivalences de distributions de marches.

**Conclusion :** la complétude de I_n observée sur les familles abéliennes finies précédentes ne s'étend pas sans conditions à des groupes non abéliens de valence trois. La question intéressante devient celle du degré minimal d'interaction relationnelle nécessaire, au-delà des seuls comptages de marches à deux points. Aucune nouveauté générale, aucune preuve Lean, aucune release stable et aucune modification du manuscrit 10A6/10C3/10B1 ne sont revendiquées.
