# PACK DE RELECTURE — Frédéric — Cayley / SPEC-OBS-09

**État : dossier de travail pour relecture externe, non approuvé pour dépôt stable.** La PR #6 reste en brouillon ; nouveauté **N = NON AUDITÉE**. Ne pas transformer ce pack en revendication de priorité, en DOI, en dépôt HAL/arXiv, ni en fusion sans une décision explicite de franchissement des portes de publication.

## Mode d'emploi pour Frédéric — coordination non scientifique
**Information confirmée par l'auteur : Frédéric n'a pas de formation mathématique et ne doit pas être présenté comme un relecteur mathématique.** Sa mission éventuelle est exclusivement éditoriale et logistique : transmettre un dossier avec ses réserves, demander des avis à des chercheurs qualifiés, centraliser les réponses, suivre les versions et préparer matériellement une soumission lorsque l'auteur l'autorise et que les conditions éditoriales sont remplies.

Frédéric n'a **pas** à certifier les preuves, refaire les calculs, affirmer l'originalité, approuver la CI ou endosser les résultats. Les six questions techniques ci-dessous sont destinées aux **relecteurs mathématiciens indépendants qu'il pourrait contacter**, pas à Frédéric lui-même.

**Procédure sans connaissances mathématiques :**
1. Partager le lien de cette branche et le manuscrit avec un mathématicien intéressé ; préciser « document de recherche non évalué, critiques et antériorités bienvenues ».
2. Demander au destinataire un retour écrit sur des passages précis, y compris en cas de résultat faux ou déjà connu.
3. Consigner le nom du relecteur seulement avec son accord, la date de réponse, les objections et les fichiers visés.
4. Transmettre les retours à l'auteur pour correction et nouvelle vérification ; ne pas modifier les formules ni les preuves lui-même.
5. Après validation explicite par l'auteur, suivre les formalités de soumission auprès de la plateforme choisie sans usurper une qualité d'auteur ou de garant scientifique. Ne jamais cliquer sur un dépôt stable par simple présence d'une CI verte.

**Message introductif suggéré :** « Je coordonne la transmission d'un dossier de recherche en théorie des graphes de Cayley. Je ne suis pas mathématicien et ne me prononce pas sur la validité ou la nouveauté des résultats. Les scripts, preuves et limites sont disponibles ; une relecture critique indépendante est recherchée. »

## Lecture rapide
- Manuscrit scientifique courant : `manuscript/structured_cayley.tex` et `manuscript/structured_cayley.pdf` (théorèmes 10A6/10C3, limites de portée à lire dans `CLAIM_BOUNDARY.md`).
- Théorèmes et témoins : `proofs/theorem_pge5_10A6.txt`, `proofs/theorem_p3_10C3.txt`, `proofs/theorem_cyclic_injectivity_10B1.txt`.
- État d'antériorité : `PRIOR_ART.md` et `PUBLICATION_STATUS.md`. Le chevauchement Brown/Mönius est déjà identifié ; Meng 1998 et Huang–Chang 2001 demandent encore confrontation primaire complète.
- Protocole pré-enregistré : `docs/SPEC_OBS_09_PREREG.md`.
- Rapport et calcul : `docs/SPEC_OBS_09.md`, `reproducibility/verify_spec_obs_09.py`, `reproducibility/results/spec_obs_09_D9_exact_summary.json`.
- D9 exclusivement : 594 digraphes, 10 signatures de motifs induits orientés à quatre sommets, 12 classes VF2 ; deux fibres ambiguës ont chacune un témoin intrinsèque de non-isomorphisme. Ne pas appeler ceci une classification de D10, D11, D12 ou S4.

## Deux certificats à auditer séparément
(A) Dans D9 indexé par rotations 0..8 et réflexions 9..17 : S={1,9,12}, T={1,9,13} ; histogrammes de quatre-motifs égaux ; nombre d'ensembles indépendants de cardinal 5 : 342 contre 360 ; cardinal 6 : 87 contre 129.
(B) S={1,8,9}, T={9,10,11} ; histogrammes de quatre-motifs égaux sur 3060 quadruplets ; comptes indépendants d'ordres 5 à 9 : S=(810,438,126,18,0), T=(810,438,126,18,2). Pour T, les deux ensembles indépendants de taille 9 sont {0,1,2,3,4,5,6,7,8} et {9,10,11,12,13,14,15,16,17}. La différence à neuf sommets sépare les graphes sans recours à VF2.
Important : les propriétés d'indépendance sont comptées sans arc dans *les deux sens*. Les couples sont des témoins de l'insuffisance générale de l'histogramme à quatre sommets, **pas** une preuve de suffisance universelle des motifs à cinq ou neuf sommets.

## Reproductibilité et CI
Depuis un clone propre de cette **branche**, installer Python 3 et NetworkX, puis exécuter :
```bash
python3 reproducibility/verify_spec_obs_09.py /tmp/spec_obs_09_recheck.json
python3 reproducibility/verify_exact.py --output /tmp/results_local.json
sha256sum -c SHA256SUMS.txt
```
Comparer le JSON recalculé au JSON figé : le générateur inclut les clés `second_certified_witness` et une convention de sortie qui doit rester stable ; signaler les différences de métadonnées préexistantes plutôt que forcer des fichiers identiques. Le workflow `verify` #87, sur commit ff3be2a26be6d69281ab43e3b7a434644855f808, est indiqué SUCCESS (contrôle du 9 octobre). Le job courant de CI n'exécute pas nécessairement le script SPEC-OBS-09 : un succès de CI n'est pas à lui seul un replay complet de ce module. Vérifier explicitement la commande SPEC-OBS-09 avant d'approuver.

## Questions à confier aux mathématiciens indépendants
1. Recalculer indépendamment les 3060 quadruplets et l'égalité intégrale des motifs dirigés à quatre sommets des deux couples.
2. Vérifier directement les deux certificats combinatoires (5/6 et 5..9), l'énumération explicite des ensembles de 9 et l'absence d'artefacts d'indexation.
3. Auditer la partition VF2 : définition de l'isomorphisme dirigé, classes/fibres, 594, 10 et 12 ; préciser les limites de l'exhaustivité.
4. Vérifier les preuves de 10A6, 10C3, 10B1, hypothèses et éventuels cas dégénérés, sans confondre essais finis et preuve générale.
5. Confronter précisément aux textes primaires Meng–Xu 1998, Huang–Chang 2001, Mans–Pappalardi–Shparlinski 2002, Brown 2009, Mönius 2020. Produire une matrice théorème / hypothèses / conclusions / intersection / antériorité.
6. Contrôler le statut des claims, les versions de sources et la reproductibilité dans un environnement vierge.

## Retour scientifique attendu des relecteurs indépendants (centralisé par Frédéric)
Pour chaque item : **confirmé / objection précise / non vérifié**, chemin source, numéro de théorème ou ligne, reproduction indépendante, référence bibliographique et conséquence éditoriale. Même une réfutation partielle est utile. Aucun endossement ne sera prêté à Frédéric sans avis explicite.

## Publication : séquence conditionnelle
1. Relecture indépendante documentée ; objections résolues ou incorporées.
2. Audit d'antériorité documenté sur sources primaires ; titres/résumés ajustés sans priorité infondée.
3. Relecture finale du manuscrit anglais, bibliographie, DOI/ORCID, attribution et licences ; table des résultats propre.
4. Validation explicite des portes `docs/RELEASE_GATE.md`, `PUBLICATION_STATUS.md`, `CLAIM_BOUNDARY.md` et de la CI/reproduction.
5. *Seulement alors* décision d'un dépôt scientifique (HAL, arXiv, Zenodo) sous responsabilité du déposant ; pas d'action automatique, pas de publication de travaux FCI/CONT/TRUST-LIFE/COSTGATE.

## Liens
PR #6 : https://github.com/alexcour/cayley-prime-translation-cospectrality/pull/6
CI #87 : https://github.com/alexcour/cayley-prime-translation-cospectrality/actions/runs/37924682732
Rapport Drive : https://docs.google.com/document/d/1db8ru0PdMv-JRh95uz2CgvcDJufb5sKe9LIREVy1Ze0/edit
