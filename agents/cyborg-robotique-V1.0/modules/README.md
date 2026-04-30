# Modules — Print Your Own Optimus

Catalog des modules **vides à contribuer**. Chacun a son propre README.md avec specs, interface, état de l'art, roadmap.

Voir [`../ARCHITECTURE.md`](../ARCHITECTURE.md) pour la vue d'ensemble.
Voir [`../CONTRIBUTING.md`](../CONTRIBUTING.md) pour comment contribuer.

## Modules disponibles

| Module | Mission | Difficulté | Pour qui |
|---|---|---|---|
| [`leg_brain/`](leg_brain/README.md) | Locomotion bipède (marcher, sauter, escaliers) | ⭐⭐⭐⭐⭐ | Locomotion researchers, PhDs |
| [`grasp_brain/`](grasp_brain/README.md) | Manipulation dexterous (pinch, lift, rotate, twist) | ⭐⭐⭐ | Étudiants robotique, makers |
| [`dynamic_brain/`](dynamic_brain/README.md) | Manipulation dynamique (lancer, attraper, frapper) | ⭐⭐⭐⭐ | Control PhDs, RL researchers |
| [`perception/`](perception/README.md) | Vision, force, tactile (capteurs vers représentation interne) | ⭐⭐⭐ | Vision researchers, makers |
| [`body_brain/`](body_brain/README.md) | Whole-body coordinator (équilibre, posture, multi-modules) | ⭐⭐⭐⭐ | Coordination experts |
| [`planner/`](planner/README.md) | Task planning haut-niveau (LLM/VLA → séquence sous-tâches) | ⭐⭐⭐⭐ | LLM/VLA researchers |
| [`safety/`](safety/README.md) | Safety layer (limites, e-stop, collision avoidance) | ⭐⭐ | **Tout le monde** (critique) |

## Module déjà fait (référence)

[`../cerveau/`](../cerveau/) — **ARM_BRAIN V6** : manipulation 5-7 DoF, identification online de J(θ), warmup canonique + DLS. Validé statistiquement (N=10 seeds, 0.067 ± 0.023 m sur SO-ARM100). Voir [`../EVAL/RAPPORT-TRIPLE-VICTOIRE-MATH.md`](../../../EVAL/RAPPORT-TRIPLE-VICTOIRE-MATH.md).

Utilise ce module comme **référence d'implémentation** quand tu attaques un nouveau module.

## Quel module attaquer en premier ?

**Si tu es solo / maker** : [`safety/`](safety/) (critique pour tout DIY hardware) ou [`grasp_brain/`](grasp_brain/) (extension immédiate de V6).

**Si tu es étudiant robotique** : [`perception/`](perception/) ou [`grasp_brain/`](grasp_brain/) — accessibles avec un projet semestre.

**Si tu es PhD / chercheur** : [`leg_brain/`](leg_brain/), [`dynamic_brain/`](dynamic_brain/), [`body_brain/`](body_brain/), ou [`planner/`](planner/) — sujets de recherche actifs.

**Si tu veux juste essayer** : prends [`safety/`](safety/) — petit module accessible, contribution utile, montre comment marche le framework.
