# SPRINT ROBOTIQUE HUMANOÏDE — Tracker J+1 → J+28

> Tracker quotidien du sprint validé 2026-04-29.
> **Lu et mis à jour à chaque session.** Source de vérité pour : où on en est dans le sprint, qui fait quoi, livrables atteints/manqués, métriques.
> Référence stratégique : `personnel/objectifopus47.md`.

---

## ⚡ STATUT POUR REPRISE — lu en PREMIER en cas de coupure

> Si Max plan a coupé la session, c'est ce bloc qui dit où reprendre. Mis à jour à chaque action significative (Claude la rafraîchit en checkpoint fréquent — pas attendre fin de session).

- **Dernière action faite :** 2026-04-30 ~02h — **EVAL-001 produite et sauvegardée** dans `EVAL/EVAL-001-2026-04-30.md`. Récap factuel J+1 : 9 commits dyad, 53 fichiers tracked, 428 lignes Python utiles dans cyborg-robotique-V1.0/, baseline AIF 3D fonctionnel (53.6% réduction erreur sur 30 cycles SO-ARM100), 6 memories nouvelles, ~320K tokens consommés. Sprint en avance calendaire (S2 démarré dès J+1).
- **Livrables S2 J+8 atteints :** setup MuJoCo + bras 2 DoF jouet + bras SO-ARM100 6 DoF + structure cerveau modulaire (model_lineaire + ik_oracle + agent) + baseline AIF lineaire 3D qui converge.
- **Prochaine action prévue :** option défaut = repos cognitif (2e session 6h+ depuis 2026-04-28). Demain matin frais : S2 J+9 = vraie politique AIF avec EFE direct (sans IK oracle) + auto-calibration corporelle + fix segfault cosmétique viewer.
- **Subagents en background :** aucun
- **Tokens cumulés sprint :** ~320K / ~5M cible (~6% du budget sprint utilisé)
- **État fichiers en cours d'édition :** aucun
- **Bloqueurs :** aucun
- **Bug connu non bloquant :** segfault MuJoCo viewer Windows à la fermeture (`03_aif_baseline_3d.py` exit 139 après bilan). Fix prévu next session : try/finally + cleanup explicite, ~5 min.
- **Discipline git active :** commit + push après chaque action significative.
- **Stack technique mise à jour :**
  - **Hardware :** matériel existant Yoan (servos, Arduino, RPi, bridge moteur) + impression 3D pièces structure. Démo support = tuiles magnétiques.
  - **Sim :** Isaac + Gazebo (choix Yoan, gratuits, parallèles). NB : rapport (c) avait flagué Isaac=lourd Windows + Gazebo=déprécié manipulation. **MuJoCo en backup possible** (Windows-friendly, à ajouter si problèmes Isaac/Gazebo).
  - **Framework :** LeRobot HF utilisable avec bras DIY via MJCF/URDF custom. Politiques pré-entraînées HF utilisables comme baseline.
  - **Politique :** active inference custom (pymdp + PyTorch) avec extension auto-calibration corporelle (Yoan définit AIF comme "le code apprend son corps").
  - **Comparaison preprint F1 :** 3 contrôleurs (AIF auto-calibrant / iLQR / MPC CasADi) sur même `forward_dynamics(x,u)`.
  - **Licences :** Apache 2.0 (code) + CC-BY 4.0 (docs) + CDLA-Permissive (datasets). Pas de CERN-OHL pour hardware (simplicité avant tout — Yoan : "pas de paperasse").
- **Thèse F1 enrichie :** "AIF avec generative model gaussien horizon fini = NMPC sous régularité H1-H4. Cas d'application puissant : auto-modélisation corporelle (le robot apprend son propre corps via AIF, lineage Lanillos iCub/rubber-hand)."
- **Vision civilisationnelle directe :** Print Your Own Optimus = chaque foyer imprime son humanoïde + installe le cerveau opensource. Démocratise la robotique humanoïde au lieu d'attendre Tesla/Figure.

**Phrase de reprise pour Yoan :** *« reprend le sprint »* → Claude lit ce bloc + HEARTBEAT.md + dernier fichier modifié dans `personnel/` + memory `project_sprint_robotique` → propose la reprise.

---

## Statut sprint

- **Démarré :** 2026-04-29 (J+0 = setup)
- **Fin prévue :** 2026-05-27 (J+28)
- **Jour actuel :** J+0 (setup en cours)
- **Mode actuel :** Setup
- **Tokens consommés sprint :** 0 / ~4-5M cible
- **Livrables atteints :** 0 / 7

---

## Livrables cibles (rappel)

| # | Livrable | Échéance | Statut |
|---|---|---|---|
| 1 | Repo `cyborg-robotique-V1.0` (sim 3D + politique inférence active) | J+14 | ⏳ |
| 2 | Spec hardware PDF buildable solo + budget contraint | J+21 | ⏳ |
| 3 | Plan partenariat lab (3 labs identifiés + 1 demande envoyée) | J+25 | ⏳ |
| 4 | Note fundraise (3 pistes documentées) | J+23 | ⏳ |
| 5 | Note antériorité + IP (espace libre cartographié) | J+2 | ⏳ |
| 6 | 12 posts LinkedIn (sprint matière éditoriale) | J+27 | 0/12 |
| 7 | Publication via `La_vallee_du_St_Laurent` activée | J+7 | ⏳ |

---

## Checklist Yoan vs Claude

### Setup J+0 (aujourd'hui)

| # | Action | Owner | Statut |
|---|---|---|---|
| 1 | Créer ce tracker | Claude | ✅ |
| 2 | Update HEARTBEAT (alerte sprint actif) | Claude | ✅ |
| 3 | Update ROADMAP (sprint en P2, robotique en cours) | Claude | ✅ |
| 4 | Memory "équipe augmentée" | Claude | ✅ |
| 5 | Activer Cyborg vocal SessionStart | Yoan + Claude | ⏳ (question setup en cours) |
| 6 | Décider repo séparé vs branche dans Cyborg framework | Yoan | ⏳ |
| 7 | Décider repo public/privé jusqu'à quand | Yoan | ⏳ |
| 8 | Initialiser repo `cyborg-robotique-V1.0` (créer GitHub) | Yoan | ⏳ |

### J+1 (demain — lancement)

| # | Action | Owner | Statut |
|---|---|---|---|
| 1 | Déclarer mode "déléguée, sprint robotique J+1" | Yoan | ⏳ |
| 2 | Lancer 5 subagents en parallèle (380K tokens) | Claude | ⏳ |
| 3 | Pendant subagents : post LinkedIn #2 du sprint | Yoan + Claude | ⏳ |
| 4 | Synthèse 5 rapports → choix sous-problème + carte IP | Claude | ⏳ |
| 5 | Update tracker + HEARTBEAT fin de journée | Claude | ⏳ |

### Touchpoint femme — J+13 prép, J+14 conversation

| # | Action | Owner | Statut |
|---|---|---|---|
| 1 | Préparer page 1-pager (où on en est, décisions, risque, couche 9) | Claude (J+13) | ⏳ |
| 2 | Choisir format conversation (marche, café, écrit) | Yoan | ⏳ |
| 3 | Conversation 15-30 min | Yoan + femme | ⏳ |
| 4 | Noter 1 décision/correction qui ressort (si Yoan veut) | Yoan | ⏳ |

---

## Métriques quotidiennes

À mettre à jour **à la fin de chaque session** :

| Date | Jour | Tokens session | Tokens cumulés sprint | Livrables avancés | Posts publiés | Candidatures envoyées |
|---|---|---|---|---|---|---|
| 2026-04-29 | J+0 | — | 0 | setup | 0 | 0 |

---

## Critères STOP — état de surveillance

| Condition | Seuil | État actuel |
|---|---|---|
| Burn rate tokens > 200K/jour × 3j | — | 🟢 |
| 0 livrable × 5j | — | 🟢 (sprint pas démarré) |
| Glissement S1 > 50 % | — | 🟢 |
| Signal cognitif rouge (brainfry) | — | 🟢 |
| Pacte raté 1 semaine | — | 🟢 |
| 0 candidature 1 semaine | — | 🟢 |
| Échec sim 3D J+12 | — | 🟢 |
| Espace IP totalement bloqué | — | 🟢 |

---

## Log de session

### 2026-04-29 — Session 2 (création sprint)

- **Mode :** Setup sprint
- **Tokens session estimés :** ~80-100K
- **Actions :**
  - Validation objectif maître par Yoan
  - Identification 7 trous + comblage
  - Création tracker, mise à jour HEARTBEAT/ROADMAP/MEMORY
  - Memory "équipe augmentée" sauvegardé
- **Décisions à valider par Yoan (questions setup en cours)** — voir conversation principale
- **Prochaine session :** lancement J+1 mode déléguée 5 subagents

---

## Notes libres

*(à remplir au fil du sprint — observations, surprises, pivots, signaux faibles)*

---

— *Maintenu par Yoan + Claude. Lu et mis à jour à chaque session du sprint.*
