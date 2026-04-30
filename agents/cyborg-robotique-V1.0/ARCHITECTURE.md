# Architecture — Print Your Own Optimus

> Framework modulaire opensource pour donner un cerveau à n'importe quel humanoïde DIY 3D-print.
> Chaque module = une fonction cognitive/motrice spécifique. L'idée commune : **chaque module apprend par interaction**, sans connaissance physique préalable du robot. Embodiment-agnostic.

---

## Vue d'ensemble

```
                    ┌─────────────────────────┐
                    │   PLANNER (haut-niveau) │   "fais un café"
                    │   (à contribuer)        │   → décompose en sous-tâches
                    └────────────┬────────────┘
                                 │
              ┌──────────────────┼──────────────────┐
              ▼                  ▼                  ▼
    ┌──────────────────┐  ┌─────────────┐  ┌──────────────────┐
    │ PERCEPTION       │  │ BODY_BRAIN  │  │ SAFETY           │
    │ (à contribuer)   │  │ (à contrib) │  │ (à contribuer)   │
    │ vision, force,   │  │ whole-body  │  │ limits, e-stop,  │
    │ tactile          │  │ coordinator │  │ collision avoid  │
    └────────┬─────────┘  └──────┬──────┘  └──────────────────┘
             │                   │
             └─────────┬─────────┘
                       ▼
        ┌──────────────────────────────┐
        │  CERVEAUX MOTEURS (par DoF)  │
        ├──────────────────────────────┤
        │  ARM_BRAIN     ← V6 (FAIT)   │   manipulation 5-7 DoF
        │  GRASP_BRAIN   ← à contrib   │   doigts, gripping, dexterous
        │  DYNAMIC_BRAIN ← à contrib   │   lancer, attraper, frapper
        │  LEG_BRAIN     ← à contrib   │   locomotion bipède
        └──────────────────────────────┘
                       │
                       ▼
              ┌────────────────┐
              │   HARDWARE     │   bras DIY 3D-print
              │  (ton bras)    │   + servos + Arduino + RPi
              └────────────────┘
```

## Principes communs à tous les modules

1. **Embodiment-agnostic** : le module ne suppose PAS de connaissance préalable du modèle (cinématique, dynamique). Il apprend par interaction.
2. **Identification online** : recursive least squares, recursive system identification, ou méthodes équivalentes. Pas de pré-training massif.
3. **Sample-efficient** : moins de 1000 actions pour converger sur un nouveau hardware. Pas des millions comme RL standard.
4. **Open source** : Apache 2.0 (code) + CC-BY 4.0 (docs). Pas de paperasse défensive.
5. **200-500 lignes Python par module** (modulo dépendances). Si un module fait 5000 lignes, c'est trop ambitieux pour un solo founder, à découper.
6. **Inspectable** : pas de black box deep learning géant. Math transparente, debuggable.

## Interface commune (contract)

Tous les modules doivent exposer :

```python
class BrainModule:
    """Interface contract pour tout module Print Your Own Optimus."""

    def __init__(self, model, data, hardware_interface, **hyperparams):
        """Init avec modèle MuJoCo (sim) ou interface hardware (réel)."""
        ...

    def warmup(self) -> None:
        """Phase de calibration / bootstrap initial."""
        ...

    def step(self, intent) -> dict:
        """Un pas de contrôle. 
        intent = ce que le module supérieur veut accomplir 
                 (target position, velocity, language goal, etc.).
        Retourne dict avec metrics (distance, error, internal state).
        """
        ...

    def is_ready(self) -> bool:
        """Le module est-il opérationnel (warmup fini, modèle calibré) ?"""
        ...

    def reset(self) -> None:
        """Reset état interne, garder calibration apprise."""
        ...
```

Modules de planification haut-niveau (PLANNER, BODY_BRAIN, SAFETY) implémentent en plus :

```python
    def coordinate(self, sub_modules: list[BrainModule], goal) -> None:
        """Orchestration : envoyer les bons intents aux bons sous-modules."""
        ...
```

## Roadmap modules

| Module | Status | Difficulté | Audience cible | Estim solo |
|---|---|---|---|---|
| `cerveau/` (ARM_BRAIN V6) | ✅ FAIT | ⭐⭐ | Solo founders, étudiants | 1 sprint |
| `modules/grasp_brain/` | ⏳ Vide | ⭐⭐⭐ | Étudiants robotique, makers | 2-3 mois |
| `modules/perception/` | ⏳ Vide | ⭐⭐⭐ | Vision researchers, makers | 2-4 mois |
| `modules/safety/` | ⏳ Vide | ⭐⭐ | Tout le monde (critique) | 1 mois |
| `modules/dynamic_brain/` | ⏳ Vide | ⭐⭐⭐⭐ | PhDs control, RL researchers | 6-12 mois |
| `modules/leg_brain/` | ⏳ Vide | ⭐⭐⭐⭐⭐ | Locomotion researchers | 1-2 ans |
| `modules/body_brain/` | ⏳ Vide | ⭐⭐⭐⭐ | Coordination experts | 6-12 mois |
| `modules/planner/` | ⏳ Vide | ⭐⭐⭐⭐ | LLM/VLA researchers | 6-12 mois |

## Pour contribuer

Voir [`CONTRIBUTING.md`](CONTRIBUTING.md). En résumé :
1. Pick un module dans `modules/` qui t'intéresse
2. Lis son `README.md` (specs, interface, état de l'art)
3. Implémente une V0.1 minimale (peut être très basique)
4. Pull request — pas besoin d'être parfait, mieux vaut 70% qui marche que 100% qui n'arrive jamais
5. La communauté itère

## Inspirations / lineage théorique

- **Adaptive control** (Åström, Wittenmark, Slotine, Li)
- **Active inference** (Friston, Lanillos, Pezzulo, Heins)
- **LeRobot ecosystem** (HuggingFace, Cadène, Soare)
- **mujoco_menagerie** (DeepMind)
- **Berkeley HumanoidLite** (premier humanoïde solo printable)

## Pourquoi cette architecture ?

**Modulaire** : chacun peut contribuer un seul module sans tout comprendre.
**Composable** : les modules se branchent ensemble pour faire émerger des comportements complexes.
**Embodiment-agnostic** : marche sur n'importe quel hardware DIY ou commercial.
**Solo-friendly** : chaque module = quelques mois de travail accessible.
**Communauté-friendly** : pas besoin de cluster GPU, pas besoin de dataset massif, pas besoin de millions de samples.

C'est l'inverse exact de ce que fait Tesla / Figure / OpenAI / DeepMind. **Distributed, accessible, transparent.**
