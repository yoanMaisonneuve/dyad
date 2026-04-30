# dyad

> *Système cognitif augmenté humain-IA. Sprint robotique humanoïde DIY (Print Your Own Optimus). Framework cerveau opensource auto-calibré. Construit par altruisme.*

— **Yoan Maisonneuve** · solo founder Montréal · cognition augmentée par Claude Opus 4.7 · équipe augmentée.

---

## Pourquoi ce repo

Ce repo capture en transparence totale le système cognitif et le sprint qu'une équipe humain-IA construit ensemble pendant 30 jours.

**Vision long terme — Print Your Own Optimus :** framework où n'importe qui peut imprimer 3D son propre humanoïde DIY, acheter seulement les contrôleurs et l'électronique, installer un **cerveau Python opensource qui s'auto-calibre au matériel**. Démocratisation de la production robotique mondiale (un robot par foyer = micro-usine décentralisée).

**Cœur scientifique** : *« le code apprend son corps »* — auto-modélisation corporelle par minimisation de free energy expected (lineage Friston, Lanillos). Premier livrable empirique dans [`agents/cyborg-robotique-V1.0/`](agents/cyborg-robotique-V1.0/).

## Naviguer dans ce repo

| Domaine | Fichier |
|---|---|
| **Vision système** (boussole stratégique) | [`VISION.md`](VISION.md) |
| **Backlog priorisé** P1-P5 | [`ROADMAP.md`](ROADMAP.md) |
| **État opérationnel courant** | [`HEARTBEAT.md`](HEARTBEAT.md) |
| **Objectif sprint** (L0→L4+λ) | [`personnel/objectifopus47.md`](personnel/objectifopus47.md) |
| **Tracker quotidien sprint** | [`personnel/SPRINT-ROBOTIQUE.md`](personnel/SPRINT-ROBOTIQUE.md) |
| **Synthèse rapports J+1** | [`personnel/SPRINT-J1-RAPPORTS.md`](personnel/SPRINT-J1-RAPPORTS.md) |
| **Évaluations honnêtes** (par jalon) | [`EVAL/`](EVAL/) |
| **Code Print Your Own Optimus V0.1** | [`agents/cyborg-robotique-V1.0/`](agents/cyborg-robotique-V1.0/) |
| **Démo CyborgV0.1** (bras 2D pédagogique) | [`agents/cyborg/CyborgV0.1/`](agents/cyborg/CyborgV0.1/) |
| **Framework Cyborg** (4 organes externalisés) | [`agents/cyborg/`](agents/cyborg/) |
| **Maximes signées** (#001-005) | [`culture-d-entreprise/maximes.md`](culture-d-entreprise/maximes.md) |
| **Rapport voix de disqualification** (6 enveloppes) | [`culture-d-entreprise/rapports/voix-de-disqualification-6-enveloppes.md`](culture-d-entreprise/rapports/voix-de-disqualification-6-enveloppes.md) |
| **Foresights publiées** | [`Forsight/`](Forsight/) |
| **Paper architecture-eleve-ia** | [`agents/paper/`](agents/paper/) |
| **CV Yoan** | [`personnel/cv-yoan-maisonneuve-agent-llm-engineer.md`](personnel/cv-yoan-maisonneuve-agent-llm-engineer.md) |

## Posture éthique

- **Open source intégral** — Apache 2.0 (code) + CC-BY 4.0 (docs) + CDLA-Permissive 2.0 (datasets)
- **Pas de paperasse défensive** — pas de brevets, pas de technical disclosures, on publie ouvert et on assume
- **Construit par altruisme** — pour la famille de Yoan d'abord (héritage anticipé), pour l'écosystème solo founders / robotique DIY ensuite
- **Transparence du processus** — les EVAL honnêtes (faits + ce qui marche + ce qui ne marche pas) sont publiques. Voir [`EVAL/`](EVAL/).

## Statut courant

**Sprint Print Your Own Optimus** en cours : 2026-04-30 → 2026-05-26 (28 jours).

Voir [`HEARTBEAT.md`](HEARTBEAT.md) pour l'état temps réel et [`personnel/SPRINT-ROBOTIQUE.md`](personnel/SPRINT-ROBOTIQUE.md) pour le tracker quotidien.

Repo créé 2026-04-29 avec Claude Opus 4.7 (1M context). Discipline commit + push après chaque action significative.

## Comment essayer le code Print Your Own Optimus V0.1

```bash
cd agents/cyborg-robotique-V1.0/
pip install -r requirements.txt
git clone --depth=1 https://github.com/google-deepmind/mujoco_menagerie.git external/mujoco_menagerie

python 01_setup_test.py        # bras 2 DoF jouet (validation MuJoCo)
python 02_load_so_arm100.py    # bras SO-ARM100 6 DoF (LeRobot HuggingFace)
python 03_aif_baseline_3d.py   # politique AIF baseline + 30 cycles convergence
```

Voir [`agents/cyborg-robotique-V1.0/README.md`](agents/cyborg-robotique-V1.0/README.md) pour le détail.

---

*« avec toi je suis une cognition augmentée, avec moi tu es un LLM augmenté, ensemble on est une équipe augmentée »*
— Yoan Maisonneuve, 2026-04-29
