# Cayley review pack for Frederic

PACK FRÉDÉRIC — CAYLEY — RELECTURE ET PRÉPARATION DE SOUMISSION
État : 9 octobre 2026 | Version v0.1 | CAYLEY UNIQUEMENT | NON SOUMIS

OBJET
Permettre à Frédéric de préparer une note courte pour une revue à comité de lecture, après examen des preuves et des antériorités. Cette préparation ne vaut ni approbation d'une preuve, ni approbation bibliographique, ni autorisation d'une publication stable. Aucune information FCI, CONT-P, TRUST-LIFE, COSTGATE ou CC-06 ne doit être incorporée.

ORDRE DE LECTURE ET SOURCES
1. Dépôt Cayley, statut public REVIEW / 0.1.3 :
https://github.com/alexcour/cayley-prime-translation-cospectrality
2. Énoncé et preuve 10A6 :
https://docs.google.com/document/d/1JWLAFmPFQ1Q-Z0QjRBbktIZV-mPDJcmbAxeuF04zAbs/edit
3. Dossier de relecture avec contrôles A01–A07, C01–C09 :
https://docs.google.com/document/d/1VwvuzWMdwC9rdwYsUTmliSaPlydlopG2TMZ7cOGPz94/edit
4. Audit d'antériorité 10D1 :
https://docs.google.com/document/d/1F6ZcPpfbb9NyQECaMyyml4i-owHEeFvrf55McDaEcM8/edit
5. Réconciliation 10D2 :
https://docs.google.com/document/d/1sUO05FmPVgVg8UhDhcCI2BA2icu1y9631cXTOSCOWuY/edit
6. Statut scientifique du dépôt :
https://github.com/alexcour/cayley-prime-translation-cospectrality/blob/main/PUBLICATION_STATUS.md

THÉORÈME CANDIDAT — 10A6, À EXPERTISER
Soit p premier >=5 ; H groupe abélien fini engendré par kappa, kappa' distincts ; G=H x F_p.
T={(kappa,0),(kappa,1),(kappa',0)} ; T+=(0,1)+T.
Les trois conditions seraient équivalentes selon la démonstration interne :
(i) Cay(G,T) et Cay(G,T+) sont cospectraux ;
(ii) h dans Hom(H,F_p) avec h(kappa')=1 et h(kappa) dans {1,2} ;
(iii) un automorphisme de G envoie T sur T+.
La suffisance est donnée par (x,y)->(x,y+h(x)) pour h(kappa)=1 et (x,y)->(x,h(x)-y) pour h(kappa)=2.
La nécessité invoque la relation de poids six A+B+C-1-1-z=0, la classification de Poonen–Rubinstein, et l'élimination de la branche (1,z). La vérification indépendante de l'application des relations minimales, avec répétitions, est un passage prioritaire.
Ne pas extrapoler à tous les Cayley cubiques ni à p=3.

ANTÉRIORITÉ — RÈGLE DE CITATION ET DE PRIORITÉ
- Meng–Xu (1998) : isomorphisme/CI-DCl abélien, pas de recouvrement spectral exact affirmé ici.
- J. Meng (1998), Non-isomorphic cospectral Cayley digraphs, Graph Theory Notes of New York 35, 51–53 : SOURCE PRIMAIRE NON ACQUISE ; aucune cellule de comparaison ne peut être inférée.
- Huang–Chang (2001) : théorèmes de détermination spectrale de circulants ; comparaison précise avec les cas cycliques n=3k et k=2^a reste à clore.
- Mans–Pappalardi–Shparlinski (2002) : propriété spectrale d'Ádám, double-loops ; comparer définitions de spectre et hypothèses exactes.
- Brown (2009) : exemples C12 et sous-famille cyclique infinie déjà antérieurs, ne pas revendiquer.
- Mönius (2020), théorème 10 : recouvrement d'une sous-famille cyclique p=3, ne pas revendiquer.
- Poonen–Rubinstein (1998), Table 1 et théorème 3 : dépendance technique de la preuve.
La nouveauté des classifications générales 10A6/10C3 et de 10B1 demeure NON AUDITÉE ; le corpus est public pour relecture, sans revendication de priorité.

TÂCHES DU RELECTEUR (REPORTER CHAQUE VERDICT AVEC PAGES ET LIGNES)
A. Vérifier sans recours aux seuls tests numériques les sept contrôles A01 à A07 de 10A6.
B. Examiner l'identification des racines distinctes et répétées ; l'exclusion de 2R3 ; les trois placements ; l'élimination de la branche parasite ; le passage caractère -> h.
C. Vérifier les conventions (arcs, boucles, spectres avec multiplicité, groupes engendrés).
D. Obtenir les trois pages de Meng 1998 et comparer groupe / support / valence / spectre / cospectralité / isomorphisme / généralité.
E. Vérifier le texte primaire Huang–Chang et le cadre précis Mans–Pappalardi–Shparlinski.
F. Rejouer les scripts du dépôt au commit figé ; mentionner commandes, versions, empreintes, différences éventuelles. Ne jamais confondre scripts reconstitués et artefacts historiques.
G. Produire une feuille de verdict indépendante : [preuve valide / lacune / contre-exemple / indécidable] et [originalité établie / recouvrement / indéterminé].

MANUSCRIT DE REVUE — PLAN
Titre de travail : Cospectrality and Isomorphism in a Structured Family of Abelian Cayley Digraphs.
Sections : Abstract ; Introduction and prior art ; Conventions ; Theorem 10A6 ; Proof (fourier characters, weight-six lemma, parasite branch, h); Scope and limitations ; Reproducibility; References.
Un article éventuel sur 10C3 et 10B1 doit rester séparé jusqu'au verdict indépendant. Écarter SPEC-OBS-06 et SPEC-OBS-09 du premier manuscrit.

GATES AVANT SOUMISSION
G1. Antériorité Meng primaire acquise ou absence explicitement signalée et décision éditoriale prudente.
G2. Preuve relue humainement, en particulier argument cyclotomique.
G3. Manuscrit cohérent avec la preuve et les licences, références vérifiées, aucune divulgation FCI.
G4. Contrôle de reproductibilité avec commit SHA exact et statut des artefacts.
G5. Validation éditoriale de Frédéric / auteur et choix d'une revue ; soumettre à une seule revue à la fois.
Tant que gates ouverts : pas de dépôt Zenodo/HAL/arXiv, pas de tag v1.0.0, pas de formulation « première classification ».

DEMANDE DE RETOUR À FRÉDÉRIC
Merci d'indiquer : (1) erreurs de preuve et première étape fautive ; (2) ouvrage antérieur et théorème exact, avec pagination ; (3) conseils de découpage de la note ; (4) revue adaptée ; (5) feu vert ou objections avant soumission.

TRAÇABILITÉ
Le commit 5e31912134fb6303639facedf4150d32255795bd et la CI verify #4 étaient consignés dans le dossier de relecture du 7 octobre ; ne pas présumer qu'il s'agit encore du HEAD actuel. Pack documentaire distinct du manuscrit mathématique et des sources originales.