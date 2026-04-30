# `safety/` — Safety Layer (à contribuer)

> Module CRITIQUE pour tout hardware DIY. Empêche le robot de se détruire ou de blesser quelqu'un.

**Status** : ⏳ Vide, à contribuer  
**Difficulté** : ⭐⭐ (accessible)  
**Estim solo** : 1-2 mois  
**Pour qui** : tout le monde (premier module recommandé pour s'initier au framework)

---

## Mission

Couche de sécurité qui s'interpose entre les cerveaux moteurs (ARM/LEG/GRASP/DYNAMIC) et le hardware. Vérifie chaque action avant exécution. Refuse, modifie ou ralentit les actions dangereuses.

## Pourquoi c'est essentiel

- Bras DIY = servos qui peuvent **brûler** si on demande couple > limite
- Bras DIY = peut **frapper l'utilisateur** ou des objets fragiles si pas de limites
- Pas de safety = projet abandonné après le 1er accident
- **Aucun framework opensource grand public n'a une couche safety dédiée pour DIY** — opportunité

## Fonctions à implémenter (V0.1 → V1.0)

### V0.1 (semaines)
- [ ] **Joint limit clipping** : refuse toute action qui sort des `jnt_range` du MJCF
- [ ] **Velocity limit** : refuse toute action qui demande δθ trop grand par step
- [ ] **Torque limit** : surveiller le courant servo (Feetech retourne courant), couper si > seuil
- [ ] **E-stop logiciel** : touche keyboard `q` arrête tout immédiatement
- [ ] **Watchdog** : si pas de heartbeat de l'agent depuis N ms, e-stop auto

### V0.5 (mois)
- [ ] **Workspace limits** : définir une boîte 3D où l'EE doit rester
- [ ] **Self-collision avoidance** : précalcul ou runtime, refuse actions qui mènent à auto-collision
- [ ] **Smooth deceleration** : au lieu de couper brutal, ralentir progressivement
- [ ] **Logging audit trail** : log toutes les interventions safety pour analyse post-mortem

### V1.0 (mois)
- [ ] **Obstacle avoidance** dynamique (avec PERCEPTION module)
- [ ] **Force-aware compliance** : si on rencontre une résistance inattendue, recule
- [ ] **Multi-DoF coordination** : empêcher mouvements simultanés dangereux

## Interface attendue

```python
from cerveau.agent_adaptive_v6 import CyborgAdaptiveV6
from modules.safety import SafetyLayer

class SafetyLayer:
    def __init__(self, model, data, **safety_params):
        """Init avec model + paramètres safety (limits, thresholds, etc.)."""
        self.joint_limits_strict = ...  # plus strict que MJCF
        self.max_velocity = ...
        self.max_torque = ...
        self.workspace_box = ...  # bbox 3D pour EE
        self.estop = False

    def filter_action(self, theta_proposed: np.ndarray, theta_current: np.ndarray) -> np.ndarray:
        """Filtre une action proposée. 
        Retourne theta_safe ou refuse (retourne theta_current si dangereux)."""
        if self.estop:
            return theta_current  # bras gelé
        
        # Joint limits stricts
        theta = np.clip(theta_proposed, self.joint_limits_strict[0], self.joint_limits_strict[1])
        
        # Velocity limit
        delta = theta - theta_current
        norm = np.linalg.norm(delta)
        if norm > self.max_velocity:
            theta = theta_current + delta * (self.max_velocity / norm)
        
        # Workspace check (si EE position calculable)
        # ...
        
        return theta

    def check_torque(self, current_reading: float) -> bool:
        """Surveille courant servo. Retourne False si > seuil."""
        if current_reading > self.max_torque:
            self.trigger_estop("torque exceeded")
            return False
        return True

    def trigger_estop(self, reason: str):
        """Active e-stop. Logger raison."""
        self.estop = True
        print(f"[SAFETY E-STOP] {reason}")
```

Usage avec ARM_BRAIN V6 :
```python
agent = CyborgAdaptiveV6(...)
safety = SafetyLayer(model, data, max_velocity=0.5, max_torque=2.0)

for step in range(N):
    theta_proposed = agent.compute_step(target)
    theta_safe = safety.filter_action(theta_proposed, current_theta)
    execute(theta_safe)
```

## État de l'art

- **ROS Industrial** : a un système de safety (`industrial_robot_status`) mais lourd, ROS-dependent
- **MoveIt!** : safety via `velocity_scaling_factor` mais pas runtime-adaptatif
- **PyRoboLearn** : safety filters basiques
- **Aucun framework DIY n'a une safety layer dédiée** — c'est ton ouverture

## Références

- ISO 13482 (robots de service personnels) — règles légales
- ISO/TS 15066 (cobots) — limites force/vitesse
- [Wahrburg et al 2018](https://ieeexplore.ieee.org/document/8534491) — collaborative robot safety overview

## Comment commencer

1. Cloner le repo, installer deps
2. Lire `cerveau/agent_adaptive_v6.py` (~120 lignes) pour comprendre style
3. Créer `modules/safety/safety_layer.py`
4. Implémenter V0.1 (joint clip + velocity limit + e-stop) en ~100 lignes
5. Test : modifier `10_adaptive_so100.py` pour passer agent.step() à travers safety.filter_action()
6. PR avec test reproductible

## Pourquoi c'est un bon premier module à contribuer

- ⭐⭐ difficulté = accessible
- 100% utile pour TOUT autre module
- Petit code (~100-300 lignes V0.1)
- Pas de math complexe, juste des conditions logiques
- Te fait comprendre le framework sans construire un cerveau complet

---

*Issue/PR : `[safety]` prefix dans le titre.*
