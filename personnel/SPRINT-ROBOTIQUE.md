# SPRINT ROBOTIQUE HUMANOÏDE — Tracker J+1 → J+28

> Tracker quotidien du sprint validé 2026-04-29.
> **Lu et mis à jour à chaque session.** Source de vérité pour : où on en est dans le sprint, qui fait quoi, livrables atteints/manqués, métriques.
> Référence stratégique : `personnel/objectifopus47.md`.

---

## ⚡ STATUT POUR REPRISE — lu en PREMIER en cas de coupure

> Si Max plan a coupé la session, c'est ce bloc qui dit où reprendre. Mis à jour à chaque action significative (Claude la rafraîchit en checkpoint fréquent — pas attendre fin de session).

- **Dernière action faite :** 2026-04-29 soir — **5/5 subagents J+1 terminés**. Synthèse condensée écrite dans `personnel/SPRINT-J1-RAPPORTS.md`. Sprint S1 audit/scope = COMPLET.
- **Prochaine action prévue :** Yoan tranche **3 décisions critiques** (cf. `SPRINT-J1-RAPPORTS.md` section finale) :
  1. **Pivot vertical** : "humanoïde manuf générique" vs vertical aligné L4 (construction modulaire / énergie / alimentation) — Claude vote pivot construction modulaire (synergie chantier3D)
  2. **Commande SO-ARM101 J+5** (~600 CAD, livraison 3 sem) — Claude vote OUI conditionnel à décision 1
  3. **Technical disclosure IP.com J+5** (~250 CAD défensif IP) — Claude vote OUI sans condition
- **Subagents en background :** aucun (tous 5 terminés)
- **Tokens cumulés sprint :** ~120K / ~4-5M cible (5 subagents ~80K + overhead ~40K)
- **État fichiers en cours d'édition :** aucun
- **Bloqueurs :** 3 décisions Yoan en attente
- **Discipline git active :** commit + push après chaque action significative.
- **Stack technique cristallisé :** SO-ARM101 + MuJoCo + LeRobot framework + politique active inference custom (pymdp+PyTorch) + 3 contrôleurs comparés (AIF/iLQR/MPC CasADi). Licences : Apache 2.0 + CERN-OHL-P v2 + CC-BY 4.0 + CDLA-Permissive.
- **Thèse F1 cristallisée :** "AIF avec generative model gaussien horizon fini = NMPC sous régularité H1-H4 ; différence épistémique (uncertainty-seeking via EFE) pas algorithmique." Trou exploitable : nonlinéaire continu + démo robot side-by-side.
- **🚨 Risque IP critique signalé :** brevet VERSES US 12,393,581 B2 (août 2025) — éviter absolument UI "décris ton robot en NL → je génère agent AIF".

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
