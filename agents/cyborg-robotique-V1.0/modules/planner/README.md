# `planner/` — Task planner haut-niveau (à contribuer)

> Cerveau qui prend une intention abstraite (langage, but, démo) et la décompose en séquence de sous-tâches pour les modules moteurs.

**Status** : ⏳ Vide, à contribuer  
**Difficulté** : ⭐⭐⭐⭐  
**Estim solo** : 6-12 mois  
**Pour qui** : LLM/VLA researchers, étudiants planning

---

## Mission

L'utilisateur dit "fais-moi un café". Le PLANNER décompose en :
1. Aller à la machine à café (LEG_BRAIN walk to coffee_machine)
2. Saisir une tasse vide (ARM_BRAIN + GRASP_BRAIN pick mug)
3. Mettre tasse sous la machine (ARM_BRAIN move + place)
4. Appuyer sur le bouton (ARM_BRAIN press button)
5. Attendre fin (timer)
6. Saisir tasse pleine (GRASP_BRAIN avec attention force, plus lourd)
7. Apporter à l'utilisateur (LEG_BRAIN walk + ARM_BRAIN handle)

C'est ce que font les VLA models (RT-2, π0, GR00T) end-to-end. PLANNER fait pareil mais en architecture **modulaire transparente**, pas un gros réseau opaque.

## Approches possibles

### Approche A — LLM-based planner
- LLM (Claude, GPT, Llama) reçoit la tâche en langage
- Génère une séquence de calls API vers les modules
- ✅ Flexible, généralise sur nouvelles tâches
- ❌ Hallucinations possibles, latence, dépendance API

### Approche B — VLA model intégré
- Foundation model vision-langage-action style π0/GR00T
- Génère directement les actions
- ✅ État de l'art, performance
- ❌ Énorme, opaque, coûteux à entraîner

### Approche C — Behavior trees / Task graphs (classique)
- Définir manuellement des scripts de tâches
- ✅ Transparent, debuggable
- ❌ Pas de généralisation

### Approche D — Hierarchical RL
- Apprendre la décomposition par RL
- ✅ Adaptatif
- ❌ Sample-inefficient

## Fonctions à implémenter

### V0.1 — Behavior tree manuel
- [ ] Format YAML/JSON pour définir tâches comme séquences
- [ ] Parser + executor qui appelle les modules dans l'ordre
- [ ] Demo : "pick_and_place_mug.yaml" exécuté correctement

### V0.5 — LLM planner
- [ ] Intégration Anthropic / OpenAI API
- [ ] Prompt qui décrit les modules disponibles + leur API
- [ ] LLM génère un plan, parser le plan, exécute
- [ ] Demo : "fais-moi un café" → plan généré + exécuté

### V1.0 — VLA integration
- [ ] Wrapper autour de GR00T N1.5 (NVIDIA, opensource)
- [ ] Adaptation à notre framework modulaire
- [ ] Demo : tâches complexes en langage naturel

## Interface attendue

```python
from modules.planner import TaskPlanner

class TaskPlanner:
    def __init__(self, available_modules: dict, planning_method='llm'):
        """Init avec modules disponibles + méthode de planning."""
        self.modules = available_modules
        self.method = planning_method  # 'llm', 'behavior_tree', 'vla', etc.

    def plan(self, task_description: str) -> list[dict]:
        """Décompose tâche en séquence d'actions modules.
        task_description = 'pick the red cube and put it in the box'
        Retourne : [{'module': 'arm_brain', 'method': 'step', 'args': ...}, ...]
        """
        ...

    def execute(self, plan: list[dict]) -> dict:
        """Exécute le plan séquentiellement, retourne metrics + success."""
        for action in plan:
            module = self.modules[action['module']]
            getattr(module, action['method'])(**action['args'])
        return metrics
```

## État de l'art

- **RT-2** (Google 2023) — VLA end-to-end pour manipulation
- **π0/π0.5** (Physical Intelligence 2024-2025) — VLA flow matching
- **GR00T N1.5** (NVIDIA 2025) — VLA humanoïde, **open weights**
- **Voxposer** (Stanford 2023) — LLM + 3D voxels for planning
- **SayCan** (Google 2022) — LLM + value functions
- **Behavior trees** : classique, utilisé dans game AI et robotique

## Références

- [SayCan Ahn et al 2022](https://say-can.github.io/)
- [Voxposer Huang et al 2023](https://voxposer.github.io/)
- [π0 Black et al 2024](https://www.physicalintelligence.company/blog/pi0)
- [GR00T NVIDIA 2025](https://developer.nvidia.com/isaac/gr00t)

## Comment commencer

**Recommandation : V0.1 behavior tree manuel D'ABORD.**

1. Définir 2-3 tâches simples en YAML
2. Implémenter parser + executor
3. Tester avec ARM_BRAIN + GRASP_BRAIN
4. Itérer vers LLM-based pour V0.5

**Pour ambitieux : forker GR00T N1.5.**
1. Cloner [Isaac GR00T N1.5](https://developer.nvidia.com/isaac/gr00t)
2. Adapter à notre interface
3. PR avec démo (humanoïde DIY qui obéit à instructions langage)

---

*Issue/PR : `[planner]` prefix.*
