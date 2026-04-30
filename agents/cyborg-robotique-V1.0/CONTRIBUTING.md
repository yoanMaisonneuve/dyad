# Contributing to Print Your Own Optimus

Tout le monde peut contribuer — solos, étudiants, PhDs, makers, parents qui assemblent un bras pour leurs enfants.

## En 5 minutes

1. **Trouve un module qui t'intéresse** dans [`modules/`](modules/) (chacun a un README avec specs)
2. **Fork** le repo `yoanMaisonneuve/dyad` sur GitHub
3. **Code une V0.1 minimale** — pas besoin que ce soit parfait
4. **Pull request** vers `master`
5. **On itère ensemble** — feedback constructif, pas de gatekeeping

## Posture

**Construit par altruisme.** On publie ouvert, on assume, pas de paperasse défensive (pas de brevets, pas de NDA, pas d'audit IP). Qui contribue garde la copyright de son code, sous Apache 2.0.

**Médiocre acceptable suffit.** Mieux vaut un module qui marche à 70% mais qui existe que 100% qui n'arrive jamais. La perfection est l'enveloppe préférée de la procrastination.

**Personne n'est jugé sur son niveau.** Solo founder Montréal ou PhD Stanford, on est tous au même niveau ici. La math/code parle, pas les credentials.

## Niveaux de contribution

### Niveau 1 — Tester un module existant
- Cloner le repo, installer les deps
- Lancer un script de test sur ton hardware DIY
- Reporter ce qui marche / ne marche pas via Issue GitHub

### Niveau 2 — Améliorer un module existant
- Optimiser un hyperparamètre, ajouter un test, améliorer la doc
- Pull request avec commit clair

### Niveau 3 — Contribuer un module vide
- Choisir un module dans `modules/` (vide aujourd'hui)
- Implémenter une V0.1 selon l'interface spécifiée
- Documenter ce qui marche / ne marche pas
- Pull request

### Niveau 4 — Proposer un nouveau module
- Ouvre une Issue avec ta proposition
- Si validé, ajoute un nouveau dossier dans `modules/` avec README
- Implémente

## Standards de code

- **Python 3.10+**, type hints encouragés
- **Numpy** pour les calculs numériques (pas torch sauf si vraiment nécessaire)
- **MuJoCo** pour la simulation
- **200-500 lignes par module** (si plus, à découper)
- **Docstrings minimales** : 1-2 lignes par fonction publique
- **Test reproductible** : seed fixé, résultat vérifiable
- **Pas de dépendances exotiques** sans justification

## Standards de documentation

Chaque module doit avoir un `README.md` avec :
- **Mission** (1 phrase)
- **Interface** (Python class skeleton)
- **État de l'art** (références littérature)
- **Roadmap interne** (V0.1 → V1.0)
- **Comment l'utiliser** (3 lignes de code)
- **Comment contribuer** (renvoyer ici)

## Standards de validation

Chaque claim numérique dans un PR doit avoir :
- **N≥5 runs** avec seeds différents
- **Mean ± std reportés**
- **Comparaison à un baseline** (ou justification absence)

Pas de cherry-picking. Si ton run unique donne un beau résultat, refait-le 5 fois et prends la moyenne. Le sprint J+1 a appris cette leçon à la dure (cf. `EVAL/RAPPORT-TRIPLE-VICTOIRE-MATH.md`).

## Discussion

- **Issues GitHub** pour bugs, propositions, questions
- **Discussions GitHub** pour brainstorm, architecture, débats
- **Pull requests** pour code

Pas de Discord/Slack pour le moment — tout en clair sur GitHub pour traçabilité et contribution asynchrone mondiale.

## Crédit

Tout contributeur est listé dans `CONTRIBUTORS.md` (à créer dès le 1er PR).

Le code reste sous Apache 2.0 — chacun garde son copyright sur ses contributions.

## Inspirations philosophiques

- **Linus Torvalds** : il a fait le kernel Linux, la communauté a fait le reste. Modèle à imiter.
- **Open source DIY communities** (Arduino, RepRap, OpenROV) : ont démocratisé hardware spécialisé. Print Your Own Optimus = pareil pour les humanoïdes.
- **Maxime #001 du projet** : *« On collabore avec l'IA légitimement »* — tu peux utiliser Claude/GPT/etc. pour t'aider à coder, c'est OK et encouragé.
- **Maxime #005 du projet** : *« Bénéficiaire externe identifié »* — chaque contribution doit servir quelqu'un d'autre que le contributeur.

## Quand quelqu'un te dit que ça ne marchera pas

Voir [`culture-d-entreprise/rapports/voix-de-disqualification-6-enveloppes.md`](../../culture-d-entreprise/rapports/voix-de-disqualification-6-enveloppes.md) du repo dyad. Les gens qui te disent que ton humanoïde DIY ne marchera jamais sont les mêmes qui disaient que :
- Wikipedia ne pourrait jamais battre Britannica (2001)
- Linux ne pourrait jamais battre Windows sur serveur (1995)
- Bitcoin ne servirait à rien (2009)
- Les voitures électriques ne pourraient jamais avoir d'autonomie (2008)

Ils ont eu tort à chaque fois. Construis quand même.

---

— *Rédigé par Yoan Maisonneuve + Claude Opus 4.7, équipe augmentée. Sprint J+1.*
