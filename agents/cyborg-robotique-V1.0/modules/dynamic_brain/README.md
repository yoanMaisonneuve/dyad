# `dynamic_brain/` — Manipulation dynamique (à contribuer)

> Cerveau pour mouvements dynamiques : lancer, attraper, frapper, balayer rapidement. Nécessite contrôle de vitesse/accélération, pas juste position.

**Status** : ⏳ Vide, à contribuer  
**Difficulté** : ⭐⭐⭐⭐ (recherche)  
**Estim solo** : 6-12 mois  
**Pour qui** : control PhDs, RL researchers, hobbyists ambitieux

---

## Mission

ARM_BRAIN (V6) optimise position finale. DYNAMIC_BRAIN optimise **trajectoire dynamique** : vitesse au moment de relâcher (lancer), timing de capture (attraper), force d'impact (frapper).

## Pourquoi c'est plus dur que V6

V6 = problème **cinématique** (positions à atteindre, dynamique du robot ignorée).
DYNAMIC_BRAIN = problème **dynamique** (forces, accélérations, timing).

Différences :
- Erreur position → erreur **vitesse + position + timing**
- Optimisation step-by-step → optimisation **trajectoire complète**
- Identification J(θ) → identification dynamique complète (M(θ), C(θ,dθ), G(θ))
- Adaptive control online → optimal control / DDP / iLQR avec model dynamique appris

## Fonctions à implémenter

### V0.1 — Lancer (release timing)
- [ ] **Trajectoire planifiée** : trajectoire θ(t) qui amène EE à atteindre position+vitesse cibles à un temps T
- [ ] **Identification dynamique** : étendre V6 pour apprendre M(θ), C(θ,dθ), G(θ)
- [ ] **Release control** : ouvrir gripper exactement au moment T optimal
- [ ] **Demo** : lancer un cube vers une boîte cible

### V0.5 — Attraper objet en mouvement
- [ ] **Tracking visuel** : suivre objet en l'air (intégration avec PERCEPTION)
- [ ] **Prédiction trajectoire** : ballistique simple (gravité connue)
- [ ] **Planification interception** : où sera l'objet à T+δt, comment y être ?
- [ ] **Demo** : attraper un cube lancé manuellement

### V1.0 — Manipulation dynamique fine
- [ ] **Frapper** : tâches type table tennis, hockey
- [ ] **Whipping motions** : balayer rapidement (multi-link)
- [ ] **Compliance dynamique** : adapter raideur en temps réel selon tâche

## Interface attendue

```python
from cerveau.agent_adaptive_v6 import CyborgAdaptiveV6
from modules.dynamic_brain import DynamicBrain

class DynamicBrain:
    def __init__(self, arm_brain: CyborgAdaptiveV6, **dynamic_params):
        """Init avec V6 ARM_BRAIN comme base + identification dynamique online."""
        self.arm = arm_brain
        # Modèle dynamique appris : M(θ) (inertie), C(θ,dθ) (Coriolis), G(θ) (gravité)
        self.M_estimator = ...
        self.C_estimator = ...
        self.G_estimator = ...

    def plan_throw(self, target_3d: np.ndarray, target_velocity: np.ndarray, T: float) -> dict:
        """Planifie une trajectoire de lancer.
        target_3d, target_velocity = position+vitesse de l'EE au moment T.
        Retourne {'trajectory': θ(t), 'release_time': T, 'controls': τ(t)}.
        """
        # Trajectory optimization (iLQR style)
        ...

    def execute_dynamic_trajectory(self, plan: dict, gripper_release_callback=None) -> dict:
        """Execute la trajectoire planifiée + appelle gripper_release_callback à T."""
        for t, theta_target in plan['trajectory']:
            self.arm.step(theta_target)
            if gripper_release_callback and t >= plan['release_time']:
                gripper_release_callback()
        return metrics
    
    def predict_object_trajectory(self, observed_positions: list[tuple[float, np.ndarray]]) -> callable:
        """Prédit où sera l'objet à un temps futur, basé sur observations.
        Retourne fonction t -> position_3d."""
        # V0.1 : balistique simple p(t) = p_0 + v_0 t + (1/2) g t²
        ...
```

## État de l'art

- **OptiState** (DeepMind 2022) — dynamic manipulation via trajectory optimization
- **Daniel et al 2021** — RL pour throwing
- **TossingBot** (Google 2019) — apprend à lancer via deep RL
- **Catching robots** (DLR, MIT) — recherche active depuis 20 ans

## Références

- [TossingBot Zeng et al 2019](https://tossingbot.cs.princeton.edu/)
- [DDP / iLQR Tassa et al 2014](https://homes.cs.washington.edu/~todorov/papers/TassaICRA14.pdf)
- [Catching trajectories Bauml et al 2010](https://ieeexplore.ieee.org/document/5509844)

## Setup hardware suggéré

- Bras 6+ DoF (SO-ARM100 + extensions, ou bras industriel utilisé)
- Caméra haute fréquence (60+ fps) pour tracking objet
- Espace dégagé (sécurité — voir `safety/` module obligatoire)

## Comment commencer

1. Maîtriser V6 (ARM_BRAIN) d'abord
2. Lire littérature dynamic manipulation (refs ci-dessus)
3. Créer `modules/dynamic_brain/dynamic_brain.py`
4. V0.1 minimal : trajectoire pré-planifiée fixe + release timing simple (sans optimisation)
5. Itérer vers V0.5 avec planning iLQR
6. Démo vidéo cruciale (lancers spectaculaires viraux pour LinkedIn)

---

*Issue/PR : `[dynamic_brain]` prefix.*
