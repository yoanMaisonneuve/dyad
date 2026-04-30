# `body_brain/` — Whole-body coordinator (à contribuer)

> Cerveau coordinateur qui orchestre tous les autres modules pour produire un comportement cohérent au niveau du corps entier.

**Status** : ⏳ Vide, à contribuer  
**Difficulté** : ⭐⭐⭐⭐  
**Estim solo** : 6-12 mois  
**Pour qui** : coordination experts, control PhDs

---

## Mission

ARM_BRAIN bouge le bras. LEG_BRAIN marche. GRASP_BRAIN saisit. Mais marcher tout en portant un verre d'eau sans le renverser nécessite une **coordination** entre tous ces modules. Le BODY_BRAIN orchestre.

## Pourquoi c'est nécessaire

Sans coordinateur, chaque module fait son truc indépendamment :
- LEG_BRAIN marche → secousses
- ARM_BRAIN tient verre statique → verre tremble → eau renversée

Avec BODY_BRAIN :
- LEG_BRAIN signale "je vais marcher avec amplitude X dans la direction Y"
- BODY_BRAIN compense en ajustant ARM_BRAIN pour stabiliser le verre
- Résultat : verre stable malgré la marche

## Fonctions à implémenter

### V0.1 — Standing balance avec ARM
- [ ] Détecter perturbations whole-body (push, déplacement de centre de masse)
- [ ] Compenser via micro-ajustements bras + jambes
- [ ] Demo : robot reste debout malgré bras qui bouge

### V0.5 — Walking with payload
- [ ] Stabiliser un objet porté pendant la marche
- [ ] Anticipation : ajuster bras AVANT le pas, pas après
- [ ] Demo : marcher avec un verre d'eau

### V1.0 — Multi-task coordination
- [ ] Plusieurs sous-tâches simultanées (marcher + parler en gestualisant)
- [ ] Priorité dynamique (si déséquilibre, abandonner gestes pour rééquilibrer)
- [ ] Demo : tâches complexes type "ramasse l'objet en marchant vers moi"

## Interface attendue

```python
from modules.body_brain import BodyBrain
from cerveau.agent_adaptive_v6 import CyborgAdaptiveV6
from modules.leg_brain import LegBrain
from modules.grasp_brain import GraspBrain

class BodyBrain:
    def __init__(self, sub_modules: dict[str, object], **coord_params):
        """Init avec dict de sous-modules : {'arm_left': ..., 'arm_right': ..., 
        'legs': ..., 'grasp_left': ..., 'grasp_right': ...}."""
        self.modules = sub_modules
        self.center_of_mass_estimator = ...

    def coordinate(self, intents: dict) -> None:
        """Orchestre les sous-modules selon intents.
        intents = {'arm_left': position_target, 'walk': direction, ...}
        Compense conflits + ajuste pour équilibre."""
        # 1. Estimer état whole-body actuel
        com = self.estimate_com()
        # 2. Prédire effet de chaque intent sur équilibre
        predicted_com = self.predict_com_after(intents)
        # 3. Si instable, ajouter compensation
        if not self.is_stable(predicted_com):
            intents = self.add_compensation(intents)
        # 4. Distribuer aux sous-modules
        for module_name, intent in intents.items():
            self.modules[module_name].step(intent)

    def estimate_com(self) -> np.ndarray:
        """Estimer centre de masse whole-body."""
        ...

    def is_stable(self, com: np.ndarray) -> bool:
        """COM dans le polygone de support ?"""
        ...
```

## État de l'art

- **Whole-body MPC** (Sleiman et al 2021)
- **Operational Space Formulation** (Khatib 1987, classique)
- **Hierarchical control** (multiple priority levels)
- **Diffusion-based whole-body** (papers récents 2024)

## Références

- [Khatib 1987 - Operational Space](https://ieeexplore.ieee.org/document/1087068)
- [Sleiman et al 2021 - Hybrid MPC whole-body](https://ieeexplore.ieee.org/document/9560769)
- [Atlas papers](https://www.bostondynamics.com/resources)

## Comment commencer

Difficile sans LEG_BRAIN existant. Workflow recommandé :
1. Attendre que LEG_BRAIN ait au moins V0.1 stand
2. Ou implémenter avec ARM_BRAIN seul + simulation legs hypothétique
3. V0.1 minimal : compensation ARM pendant petites perturbations
4. PR avec démo

---

*Issue/PR : `[body_brain]` prefix.*
