# SPEC-OBS-01 — Observations enracinées et limites de l'identification spectrale

Statut : **note exploratoire de recherche**, 2026-10-08. E = preuve élémentaire autonome pour les identités ci-dessous ; vérification finie exacte sur un exemple. N = NON AUDITÉE ; Q = expérimental / relecture ouverte. Aucun résultat de priorité, classification ou publication stable revendiqué. Cette note **ne modifie pas** la portée du manuscrit principal 10A6/10C3/10B1.

## Proposition 1 : obstacle aux observations en un sommet

Soit A la matrice d'adjacence (éventuellement orientée, avec boucles) d'un digraphe vertex-transitif d'ordre n, et p_A(x)=det(xI-A). La suppression de la ligne et colonne du sommet u produit le même polynôme q_A(x), quel que soit u. L'identité de Jacobi donne p_A'(x)=sum_u det((xI-A)_{\hat u,\hat u}); la transitivité rend tous ces cofacteurs égaux, donc q_A(x)=p_A'(x)/n. Pour tout scalaire t :

det(xI-A-t e_u e_u^T) = p_A(x) - t p_A'(x)/n.

Par conséquent, deux digraphes vertex-transitifs cospectraux de même ordre restent cospectraux après une **même perturbation diagonale de rang un** sur un sommet arbitraire de chacun. Pour chaque k, (A^k)_{uu}=tr(A^k)/n ; les statistiques de marches fermées enracinées à un seul sommet ne séparent donc pas ces graphes.

Ce résultat standard par calcul matriciel n'est pas une revendication de nouveauté. Il n'affirme pas la cospectralité après plusieurs boucles simultanées.

## Proposition 2 : séparation dépendante de l'étiquetage

Soient A et B deux matrices cospectrales réelles ou complexes de même taille, A≠B. Choisir (u,v) tel que A_uv≠B_uv et poser E=e_v e_u^T. Par expansion et cyclicité de la trace :

tr((A+tE)^2)-tr((B+tE)^2) = 2t(A_uv-B_uv)

pour tout t, puisque les traces des carrés initiaux sont égales et les termes t²E² s'annulent. Ainsi, pour t≠0 les matrices perturbées n'ont pas le même spectre.

**Restriction fondamentale** : ce test exploite une correspondance choisie entre sommets étiquetés. Il ne prouve pas la non-isomorphie, et il n'est pas un invariant intrinsèque de graphes non étiquetés.

## Exemple borné

Sur Z/12Z, pour S={1,3,9} et T={1,5,7}, la vérification entière fournit le même polynôme caractéristique [1,0,-12,0,36,0,-80,0,-12,0,36,0,-81]. Chaque perturbation diagonale simple conserve cette égalité. Avec u=0, v=3, A_uv=1, B_uv=0 ; la perturbation commune E=e_3 e_0^T donne une différence de trace quadratique 2 pour t=1. C'est une reprise calculée d'un exemple connu, pas un nouveau couple ni une preuve de non-isomorphie.

Script reproductible : `reproducibility/verify_spec_obs_01.py` (Python standard library, calcul entier).

## Nouvelle question, non résolue

Pour une classe finie de digraphes de Cayley, rechercher des **observables intrinsèques à deux sommets** : multiensembles d'entrées (A^k)_{uv} stratifiés par des relations pré-définies et invariantes, résolvantes à deux points ou invariants de configurations cohérentes. Fixer une classe, une notion d'équivalence, un horizon de marches et des témoins négatifs avant le balayage. Mesurer séparément capacité de distinction, coût et risques d'artefacts d'étiquetage. Comparer la littérature sur les graphes déterminés par leur spectre, les graphes de Cayley et les invariants de paires.

## Discipline scientifique

Conserver les frontières : E (validité démontrée), N (antériorité non auditée), Q (reproductibilité/documentation) ; aucune promotion des classifications ni de v1.0.0 ; relecture humaine indépendante toujours ouverte. La famille du manuscrit principal ne doit pas être élargie par cette note exploratoire.
