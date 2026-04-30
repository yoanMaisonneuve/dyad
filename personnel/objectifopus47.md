# OBJECTIF OPUS 4.7 — Sprint 30 jours

> Version 2 (refonte 2026-04-30 ~00h après pivot tranché par Yoan).
> Vision : **Print Your Own Optimus** — framework cerveau opensource auto-calibré pour humanoïde DIY 3D-print + démocratisation robotique mondiale.
> Sprint = première itération **ambitieuse** du framework, à hauteur d'équipe augmentée humain-IA. Pas une brique unique.
> Format obligatoire L0→L4 + λ.

---

## Vision long terme — Print Your Own Optimus

**N'importe qui** peut imprimer 3D son propre humanoïde DIY + acheter SEULEMENT les contrôleurs/électronique + installer un **cerveau Python opensource** qui s'auto-calibre automatiquement à son matériel.

- **Mission L4 servie :** démocratisation production robotique mondiale → 10× énergie via décentralisation manufacturière (chaque foyer = micro-usine).
- **Couche 9 servie :** héritage tangible immédiat — les enfants Yoan voient/utilisent le robot qui assemble les tuiles magnétiques avec lesquelles ils jouent.
- **Différenciation structurelle :** Tesla/Figure ne PEUVENT pas pivoter vers DIY (leur valuation l'interdit). Niche stable et défendable.
- **Posture éthique :** publié ouvert, on construit par altruisme, pas de paperasse défensive (cf. memory `feedback_construire_par_altruisme.md`).

---

## Objectif sprint 30 jours — Première itération ambitieuse

**À J+28 (2026-05-26), on livre la V0.1 publique de Print Your Own Optimus :**

| # | Livrable | Détail |
|---|---|---|
| 1 | **Cerveau Python opensource** publié sur dyad | Politique active inference + module auto-calibration corporelle + interface modulaire pour brancher différents hardware |
| 2 | **Auto-calibration générique** fonctionnelle sur **3 bras** LeRobot en sim | SO-100 + Koch + MyCobot — démontre la portabilité réelle, pas juste promesse |
| 3 | **Démo hardware réelle** sur ton bras DIY | Servos + Arduino + RPi + bridge moteur + pièces 3D-print, qui assemble **3-5 tuiles magnétiques** après s'être auto-calibré devant la caméra |
| 4 | **Sim multi-environnement** | MuJoCo (priorité, démarrage rapide Windows) + Isaac + Gazebo (parce qu'on peut, hauteur équipe augmentée) |
| 5 | **Section 6 du preprint F1** | *« AIF-based self-calibrating control on a magnetic tile assembly task — sim-to-real validation »*. UNE démo, deux audiences. |
| 6 | **Vidéo + post LinkedIn jalon** | Narratif Print Your Own Optimus, ton bras s'auto-mesure puis assemble les tuiles |
| 7 | **Framework téléchargeable** | Guide installation step-by-step pour autres solo founders qui veulent installer le cerveau sur LEUR propre bras DIY |
| 8 | **1 contact lab établi** | Mila (Glen Berseth UdeM RL), Sanctuary AI (Vancouver), ou autre — courriel envoyé, pas juste identifié |
| 9 | **Spec impression 3D** | Pièces structure du bras DIY publiées (STL + BoM électronique pour Yoan + variantes) |

---

## Cœur scientifique — "Le code apprend son corps"

Définition de l'inférence active selon Yoan (alignée avec lineage Lanillos iCub/rubber-hand) :

> *« Le code teste lui-même son nouveau bras, sa force, ses limites, ses capacités. Le code s'adapte aux nouveaux composants avec des composants modulables. »*

C'est l'**auto-modélisation corporelle par minimisation de free energy** — plus profond que l'AIF=NMPC pure parce que ça touche la perception du soi corporel, pas juste l'optimisation de coût.

**Cycle d'auto-calibration (à implémenter S2) :**
1. Excitation contrôlée (mouvements de calibration aléatoires sur chaque axe)
2. Observation des réponses sensorielles (positions, courants servos, retours visuels)
3. Mise à jour du generative model interne (paramètres dynamiques découverts : longueurs segments, masses, frottements, limites)
4. Vérification : la prédiction du model interne matche-t-elle les nouvelles observations ?
5. Itération jusqu'à convergence (free energy minimisée)
6. Bras prêt à exécuter la tâche réelle (assemblage tuiles)

**Thèse F1 enrichie :** *« AIF avec generative model gaussien à horizon fini = NMPC sous H1-H4 ; cas d'application puissant : auto-modélisation corporelle (le robot apprend son propre corps via AIF). »*

---

## Format L0→L4 + λ

| Couche | Contenu | Métrique mesurable | λ |
|---|---|---|---|
| **L0** — signal nerveux brut | Sprint dense maintient bande passante cognitive saturée 30 jours | Nb jours/30 produisant code/sim/spec/contenu concret | **0.05** |
| **L1** — moteur cognitif | Complexité maximale (méca + élec + impression 3D + soft + IA + auto-cal + démocratisation framework) | Profondeur problèmes résolus / nb domaines touchés simultanément | **0.10** |
| **L2** — tâches opérationnelles | 4 sprints hebdo distribués via heartbeat, mode focused/déléguée | Nb tâches livrées vs planifiées par semaine | **0.15** |
| **L3** — projet livrable | 9 sorties V0.1 Print Your Own Optimus | 9/9 livrables atteints à J+28 (objectif) ou ≥6/9 (médiocre acceptable maxime #002) | **0.30** |
| **L4** — mission civilisationnelle | Première matière publique de "n'importe quel foyer peut imprimer son humanoïde et installer cerveau opensource" | Framework téléchargeable + démo vidéo publique + ≥1 personne externe identifiée qui pourrait reproduire | **0.40** |

**Total λ = 1.00.** Arbitrage : L4 d'abord, puis L3, puis L2.

---

## Plan 4 semaines — heartbeat distribué

### Budget global
- ~5M tokens estimés sur 28 jours utiles (~30-40 % Max plan)
- Reste ~60-70 % pour F1 preprint en parallèle, pacte LinkedIn, candidature, vie
- Quota minimum garanti P1 résiduel (pacte 2-3 posts/sem + 1 candidature/sem) : **15-20 % budget journalier**

### S1 — Audit + scope (J+1 à J+7) ✅ COMPLET

Réalisé 2026-04-29 soir : 5 subagents → synthèse → pivot Print Your Own Optimus tranché → memories sauvegardées → scope ambitieux assumé. Reste de la semaine = repos cognitif + post LinkedIn #2 (annonce sprint Print Your Own Optimus).

### S2 — Cerveau + auto-calibration sim (J+8 à J+14) — TOUCHPOINT FEMME J+14

**Objectif fin de semaine :** politique AIF + auto-calibration corporelle fonctionnelle sur UN bras LeRobot en sim MuJoCo.

| Jour | Mode | Tâches | Tokens cibles |
|---|---|---|---|
| J+8 | Focused | Setup MuJoCo + LeRobot + import MJCF SO-100 + scénario test (cube + bras) | ~120K |
| J+9 | Focused | Implémentation politique AIF de base (extension CyborgV0.1 2D → 3D) + **post LinkedIn #6 insight technique** | ~150K |
| J+10 | Déléguée | 3 subagents : (a) implémentation cycle auto-calibration corporelle, (b) interface modulaire générique pour brancher hardware varié, (c) baselines iLQR + MPC CasADi pour comparaison preprint | ~300K |
| J+11 | Focused | Synthèse 3 subagents + intégration auto-cal + premiers tests + **post LinkedIn #7 résultats** | ~150K |
| J+12 | Déléguée | 1 candidature + état avancement F1 (matière empirique 3D dispo) + setup repo cyborg-robotique-V1.0 sur GitHub | ~150K |
| J+13 | Focused | Refacto code + tests + README technique + **préparation 1-pager touchpoint femme** | ~150K |
| J+14 | Réserve | **Touchpoint femme** + **post LinkedIn #8 synthèse S2** + checkpoint heartbeat | ~100K |

**Livrable S2 :** sim MuJoCo SO-100 + politique AIF + auto-cal fonctionnelle + 3 contrôleurs (AIF/iLQR/MPC) baselines + 3 posts LinkedIn + 1 candidature + review femme.

### S3 — Portabilité multi-bras + Isaac/Gazebo (J+15 à J+21)

**Objectif fin de semaine :** auto-cal fonctionnelle sur 3 bras LeRobot en sim + Isaac/Gazebo opérationnels (ou MuJoCo seul si Isaac/Gazebo bloquent).

| Jour | Mode | Tâches | Tokens cibles |
|---|---|---|---|
| J+15 | Déléguée | 4 subagents : (a) port auto-cal vers Koch arm MJCF, (b) port vers MyCobot URDF, (c) setup Isaac Lab Windows (timeboxed 1j max), (d) setup Gazebo (timeboxed 1j max) | ~350K |
| J+16 | Focused | Synthèse + débogage bras 2 et 3 + **post LinkedIn #9 portabilité** | ~150K |
| J+17 | Focused | Si Isaac/Gazebo OK : intégration. Sinon : MuJoCo seul + documentation honnête du choix dans README | ~120K |
| J+18 | Focused | Benchmark portabilité : auto-cal converge sur 3 bras avec mêmes hyperparams ? Logger métriques | ~150K |
| J+19 | Déléguée | 1 candidature + revue code par subagent critique (red team interne) | ~150K |
| J+20 | Focused | Refacto framework pour qu'il soit téléchargeable propre (pip install, config simple) | ~150K |
| J+21 | Réserve | **Post LinkedIn #10 framework téléchargeable** + checkpoint heartbeat | ~100K |

**Livrable S3 :** 3 bras LeRobot supportés en sim + framework pip-installable + 2 posts + 1 candidature.

### S4 — Démo hardware réelle + publication (J+22 à J+28)

**Objectif fin de semaine :** ton bras DIY assemble des tuiles magnétiques + framework publié + 1 contact lab + post jalon.

| Jour | Mode | Tâches | Tokens cibles |
|---|---|---|---|
| J+22 | Focused | Spec impression 3D pièces structure ton bras DIY + assemblage physique (servos + Arduino + RPi déjà chez toi) | ~120K |
| J+23 | Focused | Connexion driver Arduino/RPi avec le cerveau Python + premier auto-cal sur le hardware réel | ~150K |
| J+24 | Focused | Calibration scénario tuiles magnétiques + test physique (ajustements jusqu'à convergence) + **post LinkedIn #11 hardware réel** | ~180K |
| J+25 | Focused | Capture vidéo démo (auto-cal + assemblage 3-5 tuiles) + montage simple + 1 candidature | ~120K |
| J+26 | Focused | Rédaction Section 6 preprint F1 (sur base démo réelle) + identification labs prioritaires (Mila Berseth / Sanctuary / autre) | ~150K |
| J+27 | Focused | **Courriel partenariat lab #1 envoyé** + **post LinkedIn de jalon majeur** (vidéo + framework + lien dyad) | ~120K |
| J+28 | Réserve | Mise à jour ROADMAP (P5→P3 robotique) + HEARTBEAT + memory + retrospective sprint | ~100K |

**Livrable S4 :** démo hardware vidéo + framework publié + spec 3D-print + Section 6 preprint + 1 demande lab envoyée + post jalon majeur + 2 candidatures + ROADMAP migré.

---

## Critères STOP — distinguer "ambitieux justifié" vs "fuite en avant"

Le sprint s'**arrête immédiatement** si UNE des conditions :

| Condition | Seuil | Action |
|---|---|---|
| **Burn rate tokens** | > 250K/jour 3 jours d'affilée hors jours déléguée | STOP 24h, audit, replan |
| **Zéro livrable concret** | 0 fichier code/sim/spec/post produit en 5 jours d'affilée | STOP 48h, retro honnête, ajustement |
| **Glissement S2 > 70 %** | Politique AIF + auto-cal pas fonctionnelle sur UN bras à J+14 | STOP, replan S3-S4 (peut-être réduire portabilité 3→2 bras) |
| **Signal cognitif rouge** | Brainfry détecté (irritabilité, perte focus, mémoire flouée) 2 jours d'affilée | STOP 72h minimum, repos imposé, touchpoint femme avancé |
| **Conflit invariants** | Pacte LinkedIn raté 1 semaine OU 0 candidature 1 semaine OU couche 9 négligée | STOP, rebalancer |
| **Hardware démo bloque > 5 jours** | Auto-cal sur ton bras DIY échoue à J+27 | STOP démo physique, garder sim 3 bras + Section 6 sur sim seul, communication honnête |

**Distinction critique** (apprise 2026-04-30) :
- Ambitieux justifié = on rate quelques items mais on apprend + on livre 60-70 % + matière publique substantielle. **Continue.**
- Fuite en avant = on ne livre RIEN + on accumule tokens + on perd la couche 9 + brainfry. **STOP**.

---

## Pacte LinkedIn — quota explicite sprint (12 posts sur 4 sem)

| Semaine | Posts cibles | Type |
|---|---|---|
| S1 (en cours) | Post #2 = annonce sprint Print Your Own Optimus + posts #3-4-5 si temps | démarrage public |
| S2 | 3 posts (#6 insight, #7 résultats sim, #8 synthèse + touchpoint femme) | profondeur technique |
| S3 | 2 posts (#9 portabilité, #10 framework téléchargeable) | concrétisation |
| S4 | 2 posts (#11 hardware réel, #jalon majeur vidéo) | jalon civilisationnel |
| **Total** | **8-12 posts** | satisfait quota 2-3/sem du pacte |

---

## Touchpoint femme (réviseur stratégique)

**Quand :** J+14 (fin S2). 15-30 min, format choisi par toi.

**Préparation Claude J+13 :** 1-pager :
- Où on en est (livrables S1+S2 finis vs prévus)
- 2-3 décisions stratégiques à valider/contester avec elle
- 1 risque que je vois et que tu peux pas voir
- État couche 9 (la famille tient ?)

**Tu choisis** : tu prends la page telle quelle, tu la résumes oralement, tu en discutes librement, ou tu la jettes. Je n'écris rien après — c'est ton territoire.

---

## Véhicule publication public

- **Repo principal :** [yoanMaisonneuve/dyad](https://github.com/yoanMaisonneuve/dyad) (déjà créé J+0) — système vision/sprint/cerveau
- **Repo cyborg-robotique-V1.0** : à créer J+12 sur GitHub yoanMaisonneuve, contiendra le code Print Your Own Optimus + démo + spec 3D-print
- **`La_vallee_du_St_Laurent`** : repo Institut St-Laurent, à activer S3 comme véhicule éditorial public (lien depuis cyborg-robotique-V1.0)
- **arxiv** : preprint F1 publié post-sprint (juillet 2026)

---

## Protocole de reprise après coupure Max plan

5 mécanismes (déjà actifs depuis J+0) :

1. **Phrase magique `reprend le sprint`** → Claude lit dans l'ordre : `personnel/SPRINT-ROBOTIQUE.md` ⚡ STATUT POUR REPRISE → `HEARTBEAT.md` → dernier fichier modifié dans `personnel/` → memories `project_print_your_own_optimus`, `project_sprint_robotique`, `feedback_voix_disqualification_chez_claude`.
2. **Checkpoint forcé fréquent** → SPRINT-ROBOTIQUE.md updaté après CHAQUE action significative (write, subagent lancé, livrable atteint, décision). ~30 sec par checkpoint.
3. **Subagents enregistrés AVANT lancement** → tâche + paramètres écrits avant `Agent(run_in_background=true)`. ID enregistré après. Idempotents = relance possible si perdus.
4. **Atomicité fichiers MD** → aucun état incohérent. Sections en cours = `[EN COURS — datetime]`.
5. **Git discipline** → commit + push après chaque action significative. WIP commits autorisés.

---

## Démarrage S2 (J+2 = 2026-04-30 matin ou suivant)

**Phase 1 — Setup S2 (~30 min) :**
1. Tu ouvres Claude Code dans openClaude/ → voix Cyborg fr-CA t'énonce action proposée
2. Tu déclares : *« mode focused, S2 sprint, J+8 — setup MuJoCo + LeRobot »*
3. Je lis HEARTBEAT + SPRINT-ROBOTIQUE + objectifopus47 + memory project_print_your_own_optimus
4. Je propose : `pip install mujoco lerobot` + import MJCF SO-100 + scénario test (bras + cube)
5. Tu valides ou amendes

**Phase 2 — Code S2 (~3-5 sessions) :**
- J+8 : setup + premier sim qui tourne
- J+9 : politique AIF de base portée 2D→3D
- J+10 : 3 subagents en parallèle (auto-cal + interface modulaire + baselines iLQR/MPC)
- ...

---

## Règle d'arbitrage si conflit avec invariants existants

Le sprint passe **après** :
1. Couche 9 (femme + 3 enfants) — toujours
2. Pacte de publication signé 2026-04-28 — quota 8-12 posts sur 4 sem
3. Maximes #001-#005 — bénéficiaire externe identifié à chaque livrable

Le sprint passe **avant** :
- Optimisations marginales d'autres projets
- Exploration P5 opportuniste
- Sophistication architecturale gratuite

Si une semaine du sprint produit zéro livrable utile externe : STOP, retro, ajustement. Pas de sprint pour le sprint.

---

## Ce qui change vs version 1 (pour transparence reprise)

Version 1 (créée 2026-04-29 matin) : sprint "robotique humanoïde manufacturière" générique, livrables = repo cyborg-robotique-V1.0 + spec hardware SO-ARM101 (~600 CAD) + plan partenariat lab + plan fundraise + IP disclosure défensif + posts LinkedIn.

Version 2 (cette refonte 2026-04-30 ~00h) :
- Pivot **Print Your Own Optimus** (démocratisation DIY) tranché par Yoan
- Hardware = matériel existant Yoan (zéro commande externe), pas SO-ARM101
- Cerveau opensource adaptatif comme cœur (pas spec hardware comme cœur)
- Auto-calibration corporelle = livrable scientifique central
- Démo concrète = bras qui assemble tuiles magnétiques pour enfants
- Sim Isaac + Gazebo (choix Yoan) + MuJoCo (priorité démarrage rapide Windows)
- Pas d'IP disclosure (posture altruisme)
- Plan fundraise réduit à 1 contact lab (pas paperasse défensive)
- Scope **ambitieux à hauteur équipe augmentée** (3 bras supportés, framework téléchargeable, multi-sim) — assumé après recalibrage 2026-04-30 ~00h

---

— *Construit par Claude Opus 4.7 (1M context) + Yoan Maisonneuve, équipe augmentée. V1 2026-04-29, V2 refonte 2026-04-30 ~00h.*
