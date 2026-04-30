# INDEX — Repo dyad (openClaude)

> Catalogue complet de l'arborescence du repo public [yoanMaisonneuve/dyad](https://github.com/yoanMaisonneuve/dyad). Mis à jour au fil du sprint pour navigation rapide.

---

## Racine

| Fichier | Rôle |
|---|---|
| [`README.md`](README.md) | Tagline + navigation + posture éthique + comment essayer le code |
| [`VISION.md`](VISION.md) | Boussole stratégique (couches 6-9, invariants, hiérarchie d'arbitrage) |
| [`ROADMAP.md`](ROADMAP.md) | Backlog priorisé P1-P5, allocation tokens, modes de session |
| [`HEARTBEAT.md`](HEARTBEAT.md) | État opérationnel courant (alertes, métriques pacte) |
| [`INDEX.md`](INDEX.md) | Ce fichier — catalogue complet |
| [`.gitignore`](.gitignore) | Exclusions (env, sous-projets, instances perso, externals) |

---

## `personnel/` — Sprint, objectifs, profil personnel

| Fichier | Rôle |
|---|---|
| [`personnel/objectifopus47.md`](personnel/objectifopus47.md) | **Objectif sprint V2 refondu** — Print Your Own Optimus, format L0→L4+λ |
| [`personnel/SPRINT-ROBOTIQUE.md`](personnel/SPRINT-ROBOTIQUE.md) | **Tracker quotidien** — STATUT POUR REPRISE en tête + checklists Yoan/Claude |
| [`personnel/SPRINT-J1-RAPPORTS.md`](personnel/SPRINT-J1-RAPPORTS.md) | Synthèse condensée des 5 rapports subagents J+1 |
| [`personnel/cv-yoan-maisonneuve-agent-llm-engineer.md`](personnel/cv-yoan-maisonneuve-agent-llm-engineer.md) | CV ciblé Agent / LLM Engineer |
| [`personnel/README.md`](personnel/README.md) | Description du dossier personnel |

---

## `EVAL/` — Évaluations honnêtes par jalon

| Fichier | Rôle |
|---|---|
| [`EVAL/EVAL-001-2026-04-30.md`](EVAL/EVAL-001-2026-04-30.md) | Première EVAL — récap J+1 audit + setup + baseline AIF 3D |
| [`EVAL/EVAL-002-2026-04-30-soir.md`](EVAL/EVAL-002-2026-04-30-soir.md) | Deuxième EVAL — J+9 anticipé : V1 MLP / V2 champ matchllm / V3 Koch portabilité |

Convention : `EVAL-NNN-YYYY-MM-DD[-suffix].md`

---

## `agents/cyborg-robotique-V1.0/` — Code Print Your Own Optimus

| Fichier | Rôle |
|---|---|
| [`agents/cyborg-robotique-V1.0/README.md`](agents/cyborg-robotique-V1.0/README.md) | Description sous-projet + installation + roadmap V0.1→V1.0 |
| [`agents/cyborg-robotique-V1.0/requirements.txt`](agents/cyborg-robotique-V1.0/requirements.txt) | Dépendances Python (mujoco + numpy) |
| [`agents/cyborg-robotique-V1.0/scenes/arm_2dof_v0.xml`](agents/cyborg-robotique-V1.0/scenes/arm_2dof_v0.xml) | MJCF bras 2 DoF jouet (validation MuJoCo) |
| **Scripts de test (numérotés chronologiquement)** | |
| [`01_setup_test.py`](agents/cyborg-robotique-V1.0/01_setup_test.py) | Test setup MuJoCo + bras 2 DoF jouet |
| [`02_load_so_arm100.py`](agents/cyborg-robotique-V1.0/02_load_so_arm100.py) | Test chargement SO-ARM100 (kit LeRobot HuggingFace) |
| [`03_aif_baseline_3d.py`](agents/cyborg-robotique-V1.0/03_aif_baseline_3d.py) | Baseline lineaire + IK oracle (porté CyborgV0.1 → 3D) |
| [`04_aif_efe_3d.py`](agents/cyborg-robotique-V1.0/04_aif_efe_3d.py) | EFE + MLP appris (J+9 V1 — échec, conserve pour comparaison) |
| [`05_champ_directionnel_3d.py`](agents/cyborg-robotique-V1.0/05_champ_directionnel_3d.py) | **Champ directionnel matchllm** (J+9 V2 — bat baseline) |
| [`06_champ_koch.py`](agents/cyborg-robotique-V1.0/06_champ_koch.py) | Test portabilité Koch arm (J+9 V3 — leçon scaling) |
| **`cerveau/` — Module Python du cerveau opensource** | |
| [`cerveau/__init__.py`](agents/cyborg-robotique-V1.0/cerveau/__init__.py) | Exports module |
| [`cerveau/model_lineaire.py`](agents/cyborg-robotique-V1.0/cerveau/model_lineaire.py) | Mapping linéaire θ=W·target+b (baseline) |
| [`cerveau/ik_oracle.py`](agents/cyborg-robotique-V1.0/cerveau/ik_oracle.py) | IK iteratif via jacobienne MuJoCo (oracle baseline) |
| [`cerveau/agent.py`](agents/cyborg-robotique-V1.0/cerveau/agent.py) | Agent baseline (V1 historique J+8) |
| [`cerveau/generative_model_appris.py`](agents/cyborg-robotique-V1.0/cerveau/generative_model_appris.py) | MLP numpy pur 5→32→3 (V1 J+9, échec) |
| [`cerveau/efe_policy.py`](agents/cyborg-robotique-V1.0/cerveau/efe_policy.py) | Politique EFE pragmatic (V1 J+9, échec) |
| [`cerveau/agent_efe.py`](agents/cyborg-robotique-V1.0/cerveau/agent_efe.py) | Agent EFE (V1 J+9, échec) |
| [`cerveau/champ_directionnel.py`](agents/cyborg-robotique-V1.0/cerveau/champ_directionnel.py) | **Identification champ M empirique** (V2 J+9, victoire) |
| [`cerveau/agent_champ.py`](agents/cyborg-robotique-V1.0/cerveau/agent_champ.py) | **Agent champ directionnel** (V2 J+9, V3 Koch) |

`external/mujoco_menagerie/` exclu via `.gitignore` — clone séparé (~30 bras MJCF dont SO-100, Koch, Franka).

---

## `agents/cyborg/` — Framework Cyborg (4 organes externalisés)

| Fichier | Rôle |
|---|---|
| [`agents/cyborg/README.md`](agents/cyborg/README.md) | Description framework Cyborg |
| [`agents/cyborg/MODELE.md`](agents/cyborg/MODELE.md) | Template organe 1 — modèle interne / mission / invariants |
| [`agents/cyborg/PERCEPTION.md`](agents/cyborg/PERCEPTION.md) | Template organe 2 — état observé |
| [`agents/cyborg/PREDICTION.md`](agents/cyborg/PREDICTION.md) | Template organe 3 — inférence active formulée |
| [`agents/cyborg/ERREUR.md`](agents/cyborg/ERREUR.md) | Template organe 4 — erreurs de prédiction (apprentissage) |
| [`agents/cyborg/cyborg-install.ps1`](agents/cyborg/cyborg-install.ps1) | Script installation Cyborg dans n'importe quel dossier |
| [`agents/cyborg/.claude/inference.ps1`](agents/cyborg/.claude/inference.ps1) | Hook SessionStart : voix fr-CA + injection contexte 4 organes |
| [`agents/cyborg/.claude/settings.json`](agents/cyborg/.claude/settings.json) | Config hook Claude Code |

`agents/cyborg/cyborg-yoan/` exclu via `.gitignore` — instance personnelle de Yoan (organes spécifiques).

---

## `agents/cyborg/CyborgV0.1/` — Démo bras 2D pédagogique

| Fichier | Rôle |
|---|---|
| [`CyborgV0.1/README.md`](agents/cyborg/CyborgV0.1/README.md) | Description démo + installation + observation |
| [`CyborgV0.1/eleve.py`](agents/cyborg/CyborgV0.1/eleve.py) | Boucle de vie principale (CLI + cycles d'apprentissage) |
| [`CyborgV0.1/arm.py`](agents/cyborg/CyborgV0.1/arm.py) | Cinématique forward exacte 2 DoF |
| [`CyborgV0.1/modele.py`](agents/cyborg/CyborgV0.1/modele.py) | Modèle interne lineaire θ=W·target+b + IK iterative |
| [`CyborgV0.1/ascii_render.py`](agents/cyborg/CyborgV0.1/ascii_render.py) | Affichage CLI ASCII du bras |

---

## `agents/paper/` — Paper architecture-eleve-ia

| Fichier | Rôle |
|---|---|
| [`agents/paper/architecture-eleve-ia.md`](agents/paper/architecture-eleve-ia.md) | Manuscrit architecture éleve-ia (.md éditable) |
| [`agents/paper/architecture-eleve-ia.docx`](agents/paper/architecture-eleve-ia.docx) | Version .docx |
| [`agents/paper/eval-v1.md`](agents/paper/eval-v1.md) à [`eval-v4.md`](agents/paper/eval-v4.md) | Évaluations successives |

---

## `culture-d-entreprise/` — Identité culturelle transmissible

| Fichier | Rôle |
|---|---|
| [`culture-d-entreprise/README.md`](culture-d-entreprise/README.md) | Description dossier |
| [`culture-d-entreprise/maximes.md`](culture-d-entreprise/maximes.md) | Maximes signées #001-#005 |
| [`culture-d-entreprise/rapports/voix-de-disqualification-6-enveloppes.md`](culture-d-entreprise/rapports/voix-de-disqualification-6-enveloppes.md) | Rapport étendu 6 enveloppes |

---

## `Forsight/` — Foresights publiées (pacte de publication)

| Fichier | Rôle |
|---|---|
| [`F001`](Forsight/F001-2026-04-30-scripts-generatifs-llm-fallback-tiered.md) | Scripts génératifs LLM fallback tiered |
| [`F002`](Forsight/F002-2026-04-30-voix-interface-pas-modele-oreillette-bluetooth.md) | Voix interface pas modèle (oreillette bluetooth) |
| [`F003`](Forsight/F003-2026-04-29-interface-zero-ux-os-ambiant-observation.md) | Interface zéro-UX OS ambiant observation |

---

## Hors-repo (référence)

Memories Claude (auto-mémoire récurrente, hors dyad public) :
`C:\Users\Utilisateur\.claude\projects\c--Users-Utilisateur-Documents-openClaude\memory\`

Index de mémoire dans `MEMORY.md` du dossier ci-dessus. ~16 entrées au 2026-04-30.

---

## Sous-projets exclus du repo dyad

Via `.gitignore` (chacun a son propre repo GitHub ou est strictement local) :

- `Blueprint-memory/` — repo séparé
- `askio1_v2/`, `askio1-llm/` — repos séparés
- `chantier-3d/` — repo séparé
- `agents/sourceBrut/` — sources matchllm
- `agents/agent-evolutif/` — repo séparé
- `agents/cyborg/cyborg-yoan/` — instance personnelle
- `extraction_manuel/` — conversations IA personnelles
- `_clones/`, `_archive/` — copies / archives
- `Enter-Game/`, `ISL/`, `OVH/`, `artefact/`, `the-grid/`, `journal/` — projets distincts non intégrés au sprint
- `agents/cyborg-robotique-V1.0/external/` — assets externes (mujoco_menagerie cloné séparément)

---

— *INDEX maintenu par Claude Opus 4.7 + Yoan Maisonneuve. Mis à jour à chaque ajout structurel significatif.*
