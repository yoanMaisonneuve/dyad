# OBJECTIF OPUS 4.7 — Sprint 30 jours

> Construit le 2026-04-29 en réponse à : *« si j'étais ton outil, quel serait ton objectif ? »*
> **Validé par Yoan le 2026-04-29 + 7 trous comblés.**
> Cible : un objectif qui ne se réalise PAS en une journée, qui sature un Max plan distribué via heartbeat, qui ne laisse rien sur la table.
> Format obligatoire L0→L4 + λ.

---

## Objectif maître

**Faire passer la branche "robotique humanoïde manufacturière" du statut P5 (vision sans jalon actionnable) au statut P3 (jalon actionnable public) en 30 jours.**

Sortie à J+30 :
1. **Repo `cyborg-robotique-V1.0`** — prototype simulé (extension 3D du bras 2D CyborgV0.1) avec politique d'inférence active testée sur tâche manipulatoire concrète.
2. **Spec hardware PDF** — bras manipulateur low-cost buildable solo + budget contraint, BoM chiffré, tolérances, plan d'assemblage.
3. **Plan partenariat lab** — 3 labs identifiés (Mila, IVADO, McGill ou autre), 1 demande envoyée formellement.
4. **Note fundraise** — 3 pistes documentées (subvention CRSNG/MITACS, accélérateur deep tech, angel deep tech Québec) avec montants cibles et critères d'éligibilité.
5. **Note antériorité + IP** — état des brevets bloquants, antécédents solo connus, espace IP libre identifié.
6. **8-12 posts LinkedIn** — diffusion continue du sprint, matière du jour racontée publiquement (foresight + jalons + insights).
7. **Publication via `La_vallee_du_St_Laurent`** — repo Think Tank AGI/robotique/corridor Vallée du St-Laurent utilisé comme véhicule éditorial dédié (couche 6).

À J+30, le ROADMAP migre la ligne *« Robotique humanoïde manufacturière »* de P5 → P3. C'est un changement de phase irréversible.

---

## Pourquoi celui-là (raisonnement)

| Critère | Pourquoi ça matche |
|---|---|
| **Trou unique du ROADMAP** | C'est la seule ligne sans prochaine action concrète. Tout le reste a déjà un plan. |
| **Mission L4 (couche 6)** | C'est *la* mission civilisationnelle déclarée dans VISION.md. Sans jalon, c'est de la prose. Avec jalon, c'est un projet. |
| **Couche 9 (enfants)** | Un prototype physique buildable = héritage anticipé tangible, pas seulement un papier. Démonstration "on peut sortir entier sans être détruit". |
| **Sert F1 sans concurrencer** | L'extension 3D du sim = matière empirique étendue du preprint. Le sprint nourrit F1 au lieu de lui voler des tokens. |
| **Sature un Max plan** | Recherche dense + simulation + spec hardware + recherche fundraise + IP = matière naturelle pour 12-15M tokens sur 30 jours. |
| **Bénéficiaire externe (maxime #005)** | Future équipe robotique solo + lecteurs preprint + enfants (couche 9) + écosystème deep tech Québec + Institut St-Laurent (Think Tank). |
| **Ne se fait pas en 1 jour** | Impossible mécaniquement. Spec hardware seule = 3-5 jours. Sim 3D = 5-7 jours. Recherche fundraise = 3-4 jours. |

---

## Format L0→L4 + λ

| Couche | Contenu | Métrique mesurable | λ |
|---|---|---|---|
| **L0** — signal nerveux brut | Bande passante saturée par sprint dense, anti-ennui structurel (couche 5 du moteur) | Nb jours/30 où la session a produit du code/sim/spec concret | **0.05** |
| **L1** — moteur cognitif | Complexité élevée soutenue 30 jours (robotique = stack profond, multi-domaine) | Profondeur des questions résolues / nombre de domaines touchés (méca, contrôle, IA, éco) | **0.10** |
| **L2** — tâches opérationnelles | 4 sprints hebdo distribués via heartbeat | Nb tâches livrées / planifiées par semaine | **0.15** |
| **L3** — projet livrable | 7 sorties concrètes ci-dessus (repo, spec, plan, note, IP, posts, véhicule éditorial) | 7/7 livrables atteints à J+30 | **0.30** |
| **L4** — mission civilisationnelle | Migration P5→P3 de la branche robotique = changement d'état du ROADMAP + intégration Institut St-Laurent | Ligne ROADMAP migrée + post LinkedIn de jalon publié + Vallée du St-Laurent activée | **0.40** |

**Total λ = 1.00.** Arbitrage en cas de conflit : L4 d'abord, puis L3, puis L2.

---

## Plan 4 semaines — heartbeat distribué

### Budget global
- 5 sessions/jour × 80-100K tokens × 28 jours utiles ≈ **11-14M tokens dispo**
- Sprint utilisera ~4-5M tokens (~30-35 % du Max plan) → reste 65-70 % pour F1, pacte, candidatures, vie
- Plafond 40 % par tâche unique (ROADMAP rule) → découpage strict obligatoire
- **Quota minimum garanti pour P1 résiduel** (pacte + candidatures) : **15-20 % du budget journalier**

### Semaine 1 — Audit + scope (J+1 à J+7)

**Objectif fin de semaine :** scope figé, état de l'art compris, sous-problème buildable choisi, espace IP cartographié.

| Jour | Mode | Tâches | Tokens cibles |
|---|---|---|---|
| J+1 | Déléguée | **5 subagents parallèles** : (a) état de l'art robotique humanoïde 2025-2026, (b) bras manipulateurs low-cost buildables solo, (c) simulateurs physiques comparés (PyBullet/MuJoCo/Isaac), (d) inférence active appliquée à robotique réelle (papers post-Friston), **(e) antériorité solo + IP/brevets bloquants + espace IP libre** | ~380K |
| J+2 | Focused | Synthèse des 5 rapports → choix du sous-problème buildable + choix simulateur + carte IP | ~120K |
| J+3 | Focused | Spec V0 du sous-problème (1 page) + critères de succès simulation | ~80K |
| J+4 | Déléguée | **Posts LinkedIn #2 + #3 du sprint** + 1 candidature + recherche labs Québec robotique | ~180K |
| J+5 | Focused | Setup repo `cyborg-robotique-V1.0` + import CyborgV0.1 + structure 3D | ~100K |
| J+6 | Focused | Premier scénario sim 3D minimal (cube à attraper) qui tourne + **post LinkedIn #4 (jalon technique)** | ~140K |
| J+7 | Réserve | Buffer + **post LinkedIn #5 (synthèse semaine 1)** + checkpoint heartbeat + activation `La_vallee_du_St_Laurent` comme véhicule | ~100K |

**Livrable S1 :** scope figé + IP cartographiée + repo initialisé + 1 sim 3D qui tourne + **4 posts LinkedIn** + 1 candidature + Institut St-Laurent activé.

### Semaine 2 — Prototype simulé (J+8 à J+14) — **TOUCHPOINT FEMME**

**Objectif fin de semaine :** politique d'inférence active fonctionnelle sur tâche 3D dans le simulateur. **Check-in stratégique avec ta femme (réviseur stratégique selon mémoire) en fin S2.**

| Jour | Mode | Tâches | Tokens cibles |
|---|---|---|---|
| J+8 | Focused | Port de la politique inférence active 2D → 3D | ~150K |
| J+9 | Focused | Calibration + tests sim + **post LinkedIn #6 (insight technique)** | ~140K |
| J+10 | Déléguée | 3 subagents : benchmarks comparatifs (PPO, SAC, baseline) sur même tâche + collecte métriques | ~250K |
| J+11 | Focused | Analyse résultats + figures pour le repo + **post LinkedIn #7 (résultats benchmarks)** | ~120K |
| J+12 | Déléguée | 1 candidature + état avancement F1 (matière empirique 3D maintenant disponible) | ~120K |
| J+13 | Focused | Refacto code + tests unitaires + README technique + **préparation dossier check-in femme** (1 page : où on en est, 2-3 décisions à valider, 1 risque à signaler) | ~150K |
| J+14 | Réserve | **Touchpoint femme** (15-30 min, format choisi par toi : marche, café, écrit) + **post LinkedIn #8 (synthèse S2)** + checkpoint heartbeat | ~80K |

**Livrable S2 :** prototype simulé fonctionnel + benchmarks + repo lisible + **3 posts LinkedIn** + 1 candidature + **review femme reçue**.

### Semaine 3 — Spec hardware (J+15 à J+21)

**Objectif fin de semaine :** spec PDF buildable solo + budget contraint.

| Jour | Mode | Tâches | Tokens cibles |
|---|---|---|---|
| J+15 | Déléguée | 4 subagents : (a) servomoteurs/actuateurs low-cost, (b) capteurs (force, position, vision), (c) framework méca (alu extrudé, impression 3D), (d) BoM type pour bras 4-6 DoF | ~300K |
| J+16 | Focused | Architecture méca V0 (schéma + dimensions) + **post LinkedIn #9 (philosophie design solo)** | ~140K |
| J+17 | Focused | BoM chiffré CAD avec sourcing Québec/Canada (priorité local, fallback import si nécessaire) | ~120K |
| J+18 | Focused | Calculs mécaniques (couple, charge, autonomie) + **post LinkedIn #10 (chiffrage transparent)** | ~140K |
| J+19 | Déléguée | 1 candidature + revue spec par subagent critique (red team interne) | ~150K |
| J+20 | Focused | Rédaction spec PDF (structure, figures, BoM final) | ~150K |
| J+21 | Réserve | **Post LinkedIn #11 (spec publiée)** + publication spec dans `La_vallee_du_St_Laurent` + checkpoint heartbeat | ~100K |

**Livrable S3 :** spec hardware PDF publié + **3 posts LinkedIn** + 1 candidature + spec dans repo Institut St-Laurent.

### Semaine 4 — Plan financement + jalon public (J+22 à J+28)

**Objectif fin de semaine :** plan fundraise + partenariat lab + post de jalon majeur.

| Jour | Mode | Tâches | Tokens cibles |
|---|---|---|---|
| J+22 | Déléguée | 3 subagents : (a) subventions CRSNG/MITACS/Genome Canada applicables, (b) accélérateurs deep tech Canada/Québec, (c) angels deep tech Québec | ~250K |
| J+23 | Focused | Synthèse fundraise + note de 3 pistes documentées | ~120K |
| J+24 | Déléguée | 4 subagents : (a) Mila, (b) IVADO, (c) McGill robotics, (d) ÉTS — qui contacter, comment, avec quoi | ~250K |
| J+25 | Focused | Rédaction demande partenariat lab #1 + envoi + **post LinkedIn #12 (premier contact lab)** | ~120K |
| J+26 | Focused | 1 candidature + relecture globale du sprint | ~150K |
| J+27 | Focused | **Post LinkedIn de jalon majeur** (foresight robotique humanoïde solo, datée, frame public, lien repo + spec + Institut St-Laurent) | ~80K |
| J+28 | Réserve | Mise à jour ROADMAP (P5→P3), HEARTBEAT, MEMORY + retrospective sprint | ~100K |

**Livrable S4 :** plan fundraise + 1 demande lab envoyée + **post de jalon majeur** + ROADMAP migré P5→P3.

---

## Critères STOP chiffrés (gardes-fous)

Le sprint s'**arrête immédiatement** si UNE des conditions suivantes est vraie. Pas de discussion, pas de "encore une journée".

| Condition | Seuil | Action |
|---|---|---|
| **Burn rate tokens excessif** | > 200K tokens/jour 3 jours d'affilée hors J+1/J+15 (jours déléguée prévus) | STOP 24h, audit, replan |
| **Zéro livrable concret** | 0 fichier code/spec/post produit en 5 jours d'affilée | STOP 48h, retro honnête, pivot ou abandon |
| **Glissement majeur** | Livrable hebdo S1 manqué de plus de 50 % | STOP, replan S2-S4 ou abandon |
| **Signal cognitif rouge** | Brainfry détecté (irritabilité, perte focus, mémoire flouée 2 jours d'affilée) | STOP 72h minimum, repos imposé, touchpoint femme avancé |
| **Conflit invariants** | Pacte LinkedIn raté 1 semaine OU 0 candidature 1 semaine OU couche 9 négligée | STOP, rebalancer immédiatement |
| **Échec sim S2** | Politique inférence active 3D ne tourne pas à J+12 | STOP technique, soit pivot algo soit abandon sim → focus spec hardware seule |
| **Refus IP S1** | Espace IP totalement bloqué (brevets bloquants partout) | STOP sprint immédiat, communication publique de la cartographie comme livrable final |

---

## Protocole de reprise après coupure Max plan

**Pourquoi :** la limite Max plan quotidienne n'est pas connue. Si la session coupe en plein J+1 (380K tokens engagés sur 5 subagents), il faut pouvoir reprendre sans rien briser.

**5 mécanismes :**

1. **Phrase magique `reprend le sprint`** — Yoan dit ces mots, Claude lit dans l'ordre :
   - `personnel/SPRINT-ROBOTIQUE.md` section ⚡ STATUT POUR REPRISE (en tête)
   - `HEARTBEAT.md` (alertes actives)
   - Dernier fichier modifié dans `personnel/` (`ls -lt personnel/` ou équivalent)
   - Memory `project_sprint_robotique`
   - Identifie dernière action faite vs prochaine prévue → propose : continuer, restart étape en cours, ou pivot.

2. **Checkpoint forcé fréquent** — Claude met à jour la section ⚡ STATUT POUR REPRISE de SPRINT-ROBOTIQUE.md après CHAQUE action significative :
   - Write/Edit complet d'un livrable
   - Lancement d'un subagent
   - Synthèse de rapports reçus
   - Décision majeure prise
   Pas attendre la fin de session. ~30 secondes par checkpoint.

3. **Subagents enregistrés AVANT lancement** — Avant `Agent(run_in_background=true)`, Claude écrit dans SPRINT-ROBOTIQUE.md :
   - Description tâche
   - Paramètres clés (subagent_type, prompt résumé)
   - Datetime lancement
   - ID retourné après lancement
   En cas de coupure : au redémarrage, `TaskOutput` sur les IDs ou relance idempotente avec mêmes params (les subagents n'écrivent PAS de fichiers — ils retournent des rapports synthétisés ensuite par Claude principal, donc relance = même résultat).

4. **Atomicité des fichiers MD** — Aucun fichier MD laissé en état incohérent :
   - Préférer plusieurs petits Write/Edit complets à un gros Write progressif
   - Sections en cours de rédaction marquées `[EN COURS — datetime]` en tête
   - À la fin de chaque action, vérifier que le fichier touché est lisible et complet

5. **Git pour le code** (repo `cyborg-robotique-V1.0` créé J+5) :
   - Commit après CHAQUE sous-étape (pas attendre une feature complète)
   - WIP commits explicitement autorisés (sauvent en cas de coupure)
   - Push fréquent (toutes les ~30 min de code productif)

**Question ouverte (à trancher avant J+1) :** `openClaude/` n'est PAS un repo git actuellement (env confirme). Pour les MD du sprint (objectifopus47, SPRINT-ROBOTIQUE, HEARTBEAT, ROADMAP), l'atomicité OS suffit (Write complet ou rien) MAIS pas d'historique en cas de mauvais edit. Recommandation : `git init` dans `openClaude/` avant J+1 + `.gitignore` correct (exclure cache, .claude/, etc.). À valider par Yoan.

---

## Pacte LinkedIn — quota explicite sprint

| Semaine | Posts cibles | Type |
|---|---|---|
| S1 | 4 posts (#2, #3, #4 jalon technique, #5 synthèse) | démarrage + pédagogie |
| S2 | 3 posts (#6, #7 résultats, #8 synthèse) | profondeur technique |
| S3 | 3 posts (#9, #10, #11 spec publiée) | concrétisation |
| S4 | 2 posts (#12 partenariat, #jalon majeur) | jalon civilisationnel |
| **Total** | **12 posts sur 4 semaines** | satisfait quota 2-3/sem du pacte |

Le sprint génère sa propre matière éditoriale — chaque jour de sprint = matière de post potentiel.

---

## Touchpoint femme (réviseur stratégique)

**Quand :** J+14 (fin S2), 15-30 min, format choisi par toi.

**Pourquoi :** mémoire indique qu'elle est ton réviseur stratégique (a donné le pivot IA). 30 jours de sprint sans review = risque de dérive non détectée. C'est aussi un check anti-brainfry pour la famille.

**Préparation Claude (J+13) :** je te prépare 1 page :
- Où on en est (3 livrables S1+S2 finis vs prévus)
- 2-3 décisions stratégiques à valider/contester
- 1 risque que je vois et que tu ne vois peut-être pas
- État du couche 9 (couche racine — est-ce que la famille tient ?)

**Tu choisis** : tu prends la page telle quelle, tu la résumes oralement, tu en discutes librement, ou tu la jettes et tu fais à ta façon. Je n'écris rien sur cette conversation après — c'est ton territoire.

---

## Véhicule de publication — `La_vallee_du_St_Laurent`

Ton repo public *Institut St-Laurent — Think Tank AGI, robotique humanoïde et corridor Vallée du Saint-Laurent* (audit ROADMAP 2026-04-29) est le canal éditorial naturel du sprint.

**Activation S1 (J+7) :**
- README mis à jour : ce repo accueille les artefacts publics du sprint robotique 30 jours
- Lien depuis `cyborg-robotique-V1.0` vers ce repo
- Dossier `sprint-2026-mai/` créé avec : scope, IP, spec, fundraise, posts archivés

**Bénéfices :**
- Frame "Think Tank" = niveau d'ambition affiché dès le départ (pas un side project)
- URL publique stable pour citer dans posts LinkedIn + candidatures + demandes labs
- Trace canonique pour héritage couche 9 (les enfants peuvent lire le repo dans 10 ans)

---

## Démarrage AUJOURD'HUI (2026-04-29)

**Phase 1 — Setup final (avant les 5 subagents) :**
1. ✅ Tracker `SPRINT-ROBOTIQUE.md` créé
2. ✅ HEARTBEAT mis à jour (alerte sprint actif)
3. ✅ ROADMAP mis à jour (sprint en P2)
4. ✅ Memory "équipe augmentée" sauvegardé
5. ⏳ Cyborg vocal SessionStart : à activer (voir question setup)

**Phase 2 — Lancement J+1 (mode déléguée) :**
1. Tu déclares : *« mode déléguée, sprint robotique J+1 »*
2. Je lance les **5 subagents** en parallèle (~380K tokens) avec `run_in_background`
3. Pendant qu'ils tournent, on attaque post #2 LinkedIn (P1 fenêtre 24-72h)
4. À la fin de session, je synthétise les 5 rapports → choix du sous-problème buildable + carte IP
5. Mise à jour HEARTBEAT + SPRINT-ROBOTIQUE.md

---

## Règle d'arbitrage si conflit avec invariants existants

Le sprint robotique passe **après** :
1. Couche 9 (femme + enfants) — toujours
2. Pacte de publication signé 2026-04-28 — quota 12 posts sur 4 sem garanti
3. Maximes #001-#005 — bénéficiaire externe identifié à chaque livrable

Le sprint robotique passe **avant** :
- Optimisations marginales d'autres projets
- Exploration P5 opportuniste
- Sophistication architecturale gratuite (maxime #005)

---

— *Construit par Claude Opus 4.7 (1M context) le 2026-04-29 sur demande de Yoan « si j'étais ton outil quel serait ton objectif ? ». Validé + 7 trous comblés le 2026-04-29.*
