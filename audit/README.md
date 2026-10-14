# Auditabilité Cayley — contrat pilote

**Version : 14 octobre 2026 · proposition en PR DRAFT, sans changement d'énoncés.**

Chaque claim 10A6, 10C3, 10B1 est associé à sa preuve canonique, son SHA-256 calculé sur octets GitHub bruts, son statut E interne, son état N non audité, sa relecture humaine ouverte et ses obligations.

Lancer `python3 audit/verify_claims.py` sur un clone propre. Le contrôle valide seulement les fichiers, les IDs et la **non-promotion automatique** des statuts. Il n'évalue ni la vérité mathématique des théorèmes, ni leur originalité. Des checks de contre-exemples et relectures indépendantes devront ensuite être liés à **chaque obligation** avec auteur, date, modèle/logiciel, version, journal, portée et conclusions.

## Définitions de clôture (par obligation)
- Source exacte : fichier, commit SHA, empreinte cryptographique.
- Hypothèses : domaine de validité, conventions de spectre, calcul exact vs flottant.
- Reproductibilité : commande, environnement, sorties, témoins négatifs.
- Contradiction : au moins un test adverse et une réponse documentée aux objections.
- Revue mathématique : signature/identité du lecteur externe et limites de sa revue ; non remplaçable par une IA.
- Antériorité : passages primaires et cartographie des sous-familles connues.
- Publication : décision séparée ; Gate Z reste HOLD.

Aucune annonce `PROUVÉ EXTERNEMENT`, `PRIORITÉ ÉTABLIE`, `CERTIFIÉ LEAN` ou `RELEASE APPROUVÉE` ne suit d'une CI verte.
