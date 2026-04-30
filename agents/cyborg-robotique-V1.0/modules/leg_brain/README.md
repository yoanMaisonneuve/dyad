# `leg_brain/` — Locomotion bipède (à contribuer)

> Cerveau pour marcher, sauter, monter les escaliers. **Module le plus difficile du framework.**

**Status** : ⏳ Vide, à contribuer  
**Difficulté** : ⭐⭐⭐⭐⭐ (recherche avancée)  
**Estim solo** : 1-2 ans (ou équipe + lab partenaire)  
**Pour qui** : locomotion researchers, PhDs, équipes universitaires

---

## Mission

Cerveau dédié aux **jambes** d'un humanoïde DIY. Apprend à équilibrer, marcher, monter escaliers, sauter, sans connaître exactement la masse et l'inertie du robot.

## Pourquoi c'est différent des autres modules

ARM_BRAIN, GRASP_BRAIN, DYNAMIC_BRAIN = manipulation = **single-contact** + EE bouge dans l'espace.

LEG_BRAIN = locomotion = **multi-contact alternatif** (pieds touchent/décollent) + **équilibre dynamique** (centre de masse au-dessus du polygone de support) + **interaction avec le sol non-déterministe** (terrains variables).

C'est un domaine de recherche actif depuis 50 ans avec des paradigmes mathématiques différents (Zero Moment Point, Capture Point, MPC whole-body, RL massif, etc.).

## Approches possibles (toutes valables)

### Approche A — Classique model-based (Boston Dynamics style)
- Modèle dynamique whole-body connu ou appris
- Footstep planning (où mettre le prochain pied ?)
- MPC pour stabilisation autour des trajectoires planifiées
- ZMP (Zero Moment Point) ou Capture Point pour contrôle équilibre
- ✅ Mathématiquement transparent, deterministic
- ❌ Nécessite modèle précis (notre framework veut éviter)

### Approche B — RL massif (Unitree, Tesla style)
- Politique apprise via RL en simulation (millions d'épisodes)
- Domain randomization pour transfert sim-to-real
- ✅ Marche sur hardware récent
- ❌ Compute-intensive, opaque, non aligné avec philosophie embodiment-agnostic

### Approche C — Adaptive control online (notre lineage)
- Étendre V6 ARM_BRAIN concepts (RLS, DLS, persistence excitation) à locomotion
- Apprendre dynamique whole-body en bougeant
- Plus accessible solo mais sujet de recherche ouvert
- 🎯 **C'est l'approche alignée avec le framework**, mais à inventer

### Approche D — Imitation depuis Berkeley HumanoidLite
- Forker le code de Berkeley HumanoidLite (le seul humanoïde solo open source qui marche)
- Adapter à notre framework
- Plus rapide pour avoir un V0.1 qui marche

## Fonctions à implémenter

### V0.1 — Stand (équilibre statique)
- [ ] Détecter pose stable (centre de masse au-dessus du polygone de support)
- [ ] Réagir aux perturbations (push) en compensant
- [ ] Demo : robot reste debout malgré poussées légères

### V0.5 — Walk (marche cyclique)
- [ ] Footstep planning basique (alternance pieds, longueur fixe)
- [ ] Coordination phase swing/stance
- [ ] Demo : robot marche en ligne droite sur terrain plat

### V1.0 — Locomotion robuste
- [ ] Adaptation à pente, escaliers
- [ ] Saut basique
- [ ] Récupération après trébuchement
- [ ] Demo : parcours obstacles

## Interface attendue

```python
from modules.leg_brain import LegBrain

class LegBrain:
    def __init__(self, model, data, hardware_interface, **leg_params):
        """Init avec modèle MuJoCo (sim) + interface hardware (réel).
        Suppose un humanoïde avec hanche/genou/cheville par jambe (au moins 6 DoF jambes)."""
        ...

    def stand(self) -> bool:
        """Met le robot en position debout stable. Retourne True si réussi."""
        ...

    def walk(self, direction: np.ndarray, speed: float, duration: float) -> dict:
        """Marche dans une direction donnée à une vitesse donnée pendant duration secondes."""
        ...

    def step_to(self, foot: str, target_position: np.ndarray) -> bool:
        """Place un pied (foot in ['left', 'right']) à une position cible."""
        ...

    def estimate_state(self) -> dict:
        """Estimation état : centre de masse, polygones de support, vitesses."""
        ...
```

## État de l'art

- [**Berkeley HumanoidLite**](https://github.com/HybridRobotics/Berkeley-Humanoid-Lite) — premier humanoïde DIY 3D-printable qui marche, code open source. **À forker comme baseline.**
- **Unitree H1/G1** — RL massif + sim-to-real, code partiellement open
- **Boston Dynamics Atlas** — MPC whole-body classique (pas open source)
- **MIT Cheetah** — locomotion quadrupède via convex MPC (open)
- **NVIDIA Isaac Lab** — framework training RL locomotion

## Références

- [Sleiman et al 2021 — Hybrid contact MPC](https://ieeexplore.ieee.org/document/9560769)
- [Hwangbo et al 2019 — RL ANYmal](https://arxiv.org/abs/1901.08652) — papier qui a popularisé sim-to-real
- [Berkeley HumanoidLite paper arxiv 2504.17249](https://arxiv.org/abs/2504.17249)
- [Tassa et al 2014 — Synthesis Atlas behaviors via DDP](https://homes.cs.washington.edu/~todorov/papers/TassaICRA14.pdf)

## Setup hardware suggéré

- Humanoïde **Berkeley HumanoidLite** (DIY, ~$5000, 12+ DoF jambes)
- Ou Unitree G1 (~16k$, plus pro)
- Capteurs : IMU obligatoire, encodeurs articulations, capteurs force sous pieds idéal
- Espace dégagé sécurisé + capteurs de chute

## Comment commencer

**Recommandation forte : forker Berkeley HumanoidLite.**

1. Cloner [Berkeley HumanoidLite](https://github.com/HybridRobotics/Berkeley-Humanoid-Lite)
2. Étudier leur stack (MJCF, contrôleur, simulation)
3. Adapter à notre interface `LegBrain` dans `modules/leg_brain/`
4. Garder la math (RL ou MPC) mais wrap dans notre framework
5. PR avec démo (robot qui se tient debout = déjà un V0.1)

**Alternative ambitieuse :** réinventer avec adaptive control online.
- Étendre les concepts V6 (RLS pour J, DLS regularization) à la dynamique whole-body
- Sujet de thèse PhD potentiel
- Très original mais long

## Avertissements

⚠️ **Hardware locomotion = risque chute** : besoin obligatoire de `safety/` module + filet/coussin physique pendant tests.

⚠️ **Locomotion seule sans body coordination ne suffit pas** : un humanoïde marche en coordonnant aussi bras/torse pour équilibre. Voir `body_brain/`.

⚠️ **C'est probablement le module le plus dur du framework**. Ne pas se décourager si V0.1 prend 6 mois.

---

*Issue/PR : `[leg_brain]` prefix.*
