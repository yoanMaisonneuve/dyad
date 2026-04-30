# `grasp_brain/` — Manipulation dexterous (à contribuer)

> Cerveau pour saisir, lever, tourner, visser des objets avec précision. Extension naturelle de `cerveau/` (ARM_BRAIN V6).

**Status** : ⏳ Vide, à contribuer  
**Difficulté** : ⭐⭐⭐  
**Estim solo** : 2-3 mois  
**Pour qui** : étudiants robotique, makers DIY, hobbyists

---

## Mission

ARM_BRAIN (V6) sait amener l'effecteur à une position 3D. GRASP_BRAIN sait **interagir avec un objet** : saisir avec force adaptée, lever sans glisser, tourner avec contrôle, relâcher sans casser.

## Pourquoi c'est dur (mais pas trop)

- Pas juste position — il faut contrôler **force de pinch**
- Détection de **contact** (capteur tactile, force sur servo, ou détection visuelle)
- Coordonner gripper (1-2 DoF) avec ARM_BRAIN (5-7 DoF)
- Adapter à la **rigidité de l'objet** (verre vs éponge)

Mais reste accessible : si V6 marche pour position, GRASP_BRAIN ajoute juste 1 boucle de contrôle force au-dessus.

## Fonctions à implémenter

### V0.1 — Pick and place basique
- [ ] **Approach** : utilise V6 ARM_BRAIN pour se positionner près de l'objet
- [ ] **Grip** : ferme gripper jusqu'à détection de contact (current spike sur servo Jaw)
- [ ] **Lift** : utilise V6 ARM_BRAIN pour lever
- [ ] **Move** : déplace vers cible
- [ ] **Place** : descend jusqu'à contact (force redevient max), puis ouvre gripper
- [ ] **Demo** : empilement de 3 cubes

### V0.5 — Adaptive gripping
- [ ] **Force-controlled grip** : ajuste force selon objet (apprend par essai/erreur)
- [ ] **Tactile feedback** : si capteur tactile dispo, ajuster en temps réel
- [ ] **Slip detection** : si l'objet glisse pendant transport, resserrer
- [ ] **Demo** : transport d'objets de masses/textures variées

### V1.0 — Dexterous manipulation
- [ ] **Twist/rotate** : visser un bouchon
- [ ] **In-hand manipulation** : repositionner objet dans la main
- [ ] **Two-handed coordination** (si bras + bras dispo)
- [ ] **Demo** : tâches multi-étapes (visser-dévisser, ouvrir-fermer boîte)

## Interface attendue

```python
from cerveau.agent_adaptive_v6 import CyborgAdaptiveV6
from modules.grasp_brain import GraspBrain

class GraspBrain:
    def __init__(self, arm_brain: CyborgAdaptiveV6, gripper_dof_idx: int):
        """Init avec un arm_brain V6 + index du DoF gripper (Jaw pour SO-100)."""
        self.arm = arm_brain
        self.gripper_idx = gripper_dof_idx
        self.contact_detected = False

    def pick(self, object_position: np.ndarray, approach_height: float = 0.05) -> bool:
        """Saisie complète : approach + grip + lift. Retourne True si succès."""
        # 1. Approach above object
        target_above = object_position + np.array([0, 0, approach_height])
        for _ in range(N_steps):
            self.arm.step(target_above)
        # 2. Descend
        for _ in range(N_steps):
            self.arm.step(object_position)
        # 3. Close gripper until contact
        while not self.contact_detected:
            self.close_gripper(delta=0.05)
            self.contact_detected = self.detect_contact()
        # 4. Lift
        for _ in range(N_steps):
            self.arm.step(target_above)
        return True

    def place(self, target_position: np.ndarray, drop_height: float = 0.05) -> bool:
        """Pose : déscendre + ouvrir gripper."""
        ...

    def close_gripper(self, delta: float):
        """Fermer gripper d'un delta donné."""
        # Manipule directement le DoF gripper via arm_brain.data.qpos
        ...

    def detect_contact(self) -> bool:
        """Détection contact via servo current OR force sensor OR vision."""
        # V0.1 : seuil sur servo current
        # V0.5+ : capteur tactile
        ...
```

## État de l'art

- **LeRobot** (HuggingFace) — pick-and-place avec ACT / Diffusion Policy, mais entrainement supervisé teleop
- **DexNet** (Berkeley) — grasp planning avec deep learning
- **GG-CNN** (QUT) — grasp prediction temps réel
- **Issac Manipulation** (NVIDIA) — sim grasping
- **OnRobot, Robotiq** (commercial) — grippers industriels avec force control

## Références

- [Bohg et al 2014](https://www.cmu.edu/srichter/learn-grasping.pdf) — Data-driven grasp synthesis review
- [Mahler et al 2017](https://berkeleyautomation.github.io/dex-net/) — DexNet 2.0
- [LeRobot pick and place tutorials](https://github.com/huggingface/lerobot)

## Setup hardware suggéré

- Bras SO-ARM100 ou Koch (déjà supporté par V6)
- Gripper natif (Jaw pour SO-100, fingers pour Koch)
- Optionnel : capteur tactile DIY (résistance mesurée à la pression) ou DIGIT (~$200)

## Comment commencer

1. Lire `cerveau/agent_adaptive_v6.py` pour comprendre comment V6 contrôle
2. Lire `10_adaptive_so100.py` pour voir intégration
3. Créer `modules/grasp_brain/grasp_brain.py` avec V0.1 (pick avec contact détection sur servo current)
4. Test sur cubes virtuels MuJoCo (créer un wrapper MJCF avec cubes mocap)
5. Si hardware réel dispo : tester sur objets variés
6. PR avec démo vidéo (réutilise `make_demo_video.py` pattern)

---

*Issue/PR : `[grasp_brain]` prefix.*
