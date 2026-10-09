# SPEC-OBS-09 — D9: échec certifié de la complétude des motifs dirigés induits à quatre sommets

**Protocole gelé avant calcul :** `docs/SPEC_OBS_09_PREREG.md`. **Statut : E** pour la vérification exacte de D9 ; **N = NON AUDITÉE** pour toute nouveauté ; D10, D11, D12 et S4 explicitement **INCOMPLETE**. Pas de fusion de la PR #6 ni de changement des portes de publication.

## Corpus effectivement exécuté

Groupe diédral D9 d'ordre 18, représenté par les couples (a,b), a mod 9 et b mod 2, avec (a,b)(c,d)=(a+(-1)^b c,b+d). Indexation 0-8 pour rotations (a,0), 9-17 pour réflexions (a,1). Toutes les combinaisons de trois éléments distincts non identités qui engendrent le groupe. Digraphes dirigés de Cayley à droite, connexes au sens fort, sans boucle.

Les motifs induits sont calculés sur chacun des sous-ensembles NON ORDONNÉS de quatre sommets, puis canoniquement identifiés modulo toutes les 24 permutations des quatre sommets. Leurs histogrammes sont comparés exactement. Les véritables isomorphismes sont vérifiés séparément par NetworkX VF2 orienté, sans les inférer de l'égalité des motifs.

## Résultat exact D9

- 594 graphes correspondants aux supports générateurs.
- 10 classes pour l'histogramme des motifs induits dirigés à quatre sommets.
- 12 classes d'isomorphisme exactes, obtenues après 663 comparaisons VF2.
- Deux fibres distinctes de quatre-motifs contiennent chacune deux classes non isomorphes ; exemples : S={1,8,9} et T={9,10,11}, puis S={1,9,12} et T={1,9,13}.

## Certificat de non-isomorphisme indépendant de VF2

S={1,9,12}, T={1,9,13}. Même histogramme intégral de motifs induits à quatre sommets (vérification entière). Pourtant les comptes de sous-ensembles indépendants (aucun arc dans aucune direction) sont :

| Ordre du sous-ensemble | S | T |
|---|---:|---:|
| 5 | 342 | 360 |
| 6 | 87 | 129 |

Chaque nombre est préservé par isomorphisme ; ces valeurs distinctes CERTIFIENT donc que les deux graphes ne sont pas isomorphes. Il n'est pas nécessaire d'inférer cette conclusion à partir de VF2. Un deuxième exemple est disponible, mais sans certificat additionnel séparé à ce stade.

## Conséquence mathématique et limites

La propriété 'l'histogramme complet des motifs induits à quatre sommets détermine à isomorphisme près tout Cayley dirigé non abélien à trois connexions' est fausse, car le couple D9 constitue un contre-exemple fini. Ce résultat ne réfute pas les décomptes de SPEC-OBS-08 sur leur propre corpus (ordres au plus 16). Il ne prouve pas non plus qu'un invariant à cinq sommets suffise universellement : les comptes de sous-ensembles indépendants à cinq sommets ne sont qu'un certificat pour le témoin. Aucun antécédent bibliographique précis n'a été entièrement audité.

## Archive et reproductibilité

- `reproducibility/verify_spec_obs_09.py`: reconstruction D9, génération exhaustive, motif 4, VF2, assertions des décomptes et certificats indépendants. Dépendances : Python 3 et NetworkX.
- `reproducibility/results/spec_obs_09_D9_exact_summary.json`: résultats figés et états incomplets des autres groupes.
- `docs/SPEC_OBS_09_PREREG.md`: domaine, ordre D9,D10,D11,D12,S4, critère de réussite et règles d'arrêt enregistrés avant calcul.

**Important :** les groupes D10, D11, D12 et S4 ne sont PAS classifiés dans ce travail ; ne jamais traiter cette absence comme zéro contre-exemple. Poursuite SPEC-OBS-10 éventuelle : isoler la structure responsable du défaut ou développer des signatures de cinq sommets, avec nouveau protocole gelé. Les manuscrits 10A6/10C3/10B1 restent inchangés.
