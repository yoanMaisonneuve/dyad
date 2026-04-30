# agents/ — Carte d'ensemble

> **Vision long terme** : faire de l'élève IA un **agent émancipé** — local-first, budget contraint, identité propre, capable de gagner sa vie. Cf. [`VISION-eleve-emancipe.md`](VISION-eleve-emancipe.md).
>
> **But court terme** : continuer Enter-Game en poussant les limites de la **mémoire externe** et en améliorant le profil **power-user**.
>
> **Référence canonique** : [`REFERENCE-clark-cognition-augmentee.txt`](REFERENCE-clark-cognition-augmentee.txt) — la cognition étendue d'Andy Clark + l'inférence active de Friston.

---

## Structure

```
agents/
├── REFERENCE-clark-cognition-augmentee.txt    ← matrice théorique (Clark / Friston)
├── VISION-eleve-emancipe.md                   ← vision long terme (NOUVEAU 25 avril)
│
├── paper/                  ← rapport scientifique vivant + cycle d'évaluations
│   ├── architecture-eleve-ia.md  (paper actif, 142k)
│   ├── eval-v1.md → eval-v4.md   (V1: 5/10 → V4: 8/10 accept conditionnel)
│   └── (.docx mirrors)
│
├── brainstorms/            ← conversations IA brutes (matière première)
│   ├── chef-L4-orchestrateur.txt
│   ├── pipeline-multi-agents.md
│   └── chat.md             ← brain dumps Yoan en cours
│
├── agent-evolutif/         ← STACK PYTHON COMPLÈTE (depuis 19 avril)
│   ├── main.py + perception/memory/planner/executor/metacognition.py
│   ├── tools/ (file, search, shell, ast, patch)
│   └── phase05/   ← simulation scientifique + résultats expérimentaux
│
├── cyborg/                 ← FRAMEWORK MINIMAL (4 organes, transmissible)
│   ├── (template — MODELE/PERCEPTION/PREDICTION/ERREUR + cyborg-install.ps1)
│   ├── CyborgV0.1/
│   └── cyborg-yoan/
│
├── sourceBrut/
│   └── matchllm/           ← MOTEUR COGNITIF DIRECTIONNEL (NOUVEAU 25 avril - V0.2)
│       ├── askio1/         ← package Python (12 champs + 6 moteurs + 5 régulateurs)
│       │   ├── kernel.py · swarm.py · runtime.py · self_train.py
│       │   ├── engines/ · regulators/ · llm/ · embeddings/ · storage/
│       │   └── integration/  (CyborgIO + AgentEvolutifPlanner)
│       ├── api/            ← FastAPI REST (POST /askio1/run, etc.)
│       ├── examples/       (11 démos fonctionnelles, dont Anthropic réel + LLM-judge + E2E)
│       ├── benchmarks/     (Askio1 vs prompt brut : 4/4 wins réel, +24% global, +181% OPS)
│       ├── tests/          (49/49 verts)
│       ├── docs/           (7 docs + QUICKSTART + BRIDGE + benchmark-results)
│       └── matchLLM.md     (source brute 8051 lignes)
│
└── archive/
    └── mythos/             ← v0 abandonnée (renommée Cyborg le 23 avril)
```

---

## Carte conceptuelle des 4 sous-projets

| | `paper/` | `agent-evolutif/` | `cyborg/` | `matchllm/askio1/` |
|---|---|---|---|---|
| **Niveau** | Théorie scientifique | Stack Python complète | Framework minimal | Moteur cognitif directionnel |
| **Origine** | Yoan + 4 peer reviews | 19 avril | 23 avril (refonte Mythos) | 25 avril (depuis matchLLM.md) |
| **Scope** | 3 piliers Sens/Mémoire/Métacognition | Cycle Percevoir → Retenir → Planifier → Exécuter → Métacognition | Cycle MODELE → PRÉDICTION → PERCEPTION → ERREUR | 12 champs directionnels + 6 moteurs + 5 régulateurs |
| **Validation** | Score V4 = 8/10 | phase05/ : ablations alpha déjà faites | CyborgV0.1 : bras 2D testé | 49/49 tests + benchmark live 4/4 wins (+24%) |
| **Rôle dans l'élève émancipé** | **Légitimité** scientifique | **Corps** (action sur le monde) | **Mémoire externe** transmissible | **Cerveau** (orientation cognitive) |
| **Public** | Chercheurs / peer review | Devs Python / agents autonomes | Tout projet (humain ou IA) | Devs qui veulent piloter un LLM finement |

**Filiation** : `paper/` est la théorie qui fonde les 3 implémentations. `agent-evolutif/`, `cyborg/`, `matchllm/askio1/` sont **3 angles d'attaque** complémentaires sur le même problème — voir [`sourceBrut/matchllm/BRIDGE.md`](sourceBrut/matchllm/BRIDGE.md) pour le mapping détaillé.

---

## L'élève émancipé est l'intégration des 4

```
                    ┌──────────────────────────────┐
                    │   Élève IA émancipé          │
                    │   (vision long terme)        │
                    └──────────┬───────────────────┘
                               │
       ┌───────────────────────┼─────────────────────────┐
       │                       │                          │
       ▼                       ▼                          ▼
┌──────────┐           ┌──────────────┐           ┌──────────────┐
│  paper   │           │ matchllm/    │           │   cyborg     │
│ (théorie)│ ────────► │   askio1     │ ────────► │  (mémoire    │
│          │           │  (cerveau)   │           │ transmissib.)│
└──────────┘           └──────┬───────┘           └──────────────┘
                              │
                              ▼ pilote via AgentEvolutifPlanner
                       ┌──────────────┐
                       │ agent-       │
                       │  evolutif    │
                       │  (corps)     │
                       └──────────────┘
```

---

## État actuel (2026-04-25)

| Module | Version | État | Prochaine action |
|---|---|---|---|
| `paper/` | V4 (8/10) | ✅ stable | Phase 1 humaine quand budget |
| `agent-evolutif/` | depuis 19 avril | ⚠️ bugs identifiés (logs nuit 24/04) | Réparer ou remplacer son planner par AgentEvolutifPlanner |
| `cyborg/` | V0.1 fonctionnel | ✅ bras 2D testé | cyborg-yoan V0.1 (`bootstrap.py --interactive`) |
| `matchllm/askio1/` | **V0.2** | ✅ Anthropic réel + LLM-judge + benchmark wins | V0.3 = local-first (Ollama + budget tracker) |

---

## Prochaines actions (alignées sur la vision émancipation)

1. **Brancher AgentEvolutifPlanner sur agent-evolutif réel** — remplacer son `planner.py` buggy par un appel à Sonnet via Askio1. Premier vrai pas vers l'autonomie d'exécution.
2. **V0.3 askio1 = local-first** — `OllamaLLMClient` + `LLMRouter` (local par défaut, cloud en luxe). Invariant n°2 de la vision.
3. **`BudgetTracker`** dans `askio1/economics.py` — mesure tokens × prix en temps réel. Invariant n°3.
4. **Continuer Enter-Game** — but court terme reste pertinent.

---

## Liens externes (hors `agents/`)

- [Blueprint-memory/](../Blueprint-memory/) — workflow + recherche + IDEES.md
- [Enter-Game/](../Enter-Game/) — protocole d'entrée power-user (but central court terme)
- [ISL/](../ISL/) — Institut Saint-Laurent + GLOBAL-PLAN civilisationnel
- [note.md](../note.md) — capture brute des intuitions de Yoan

---

*Carte créée 2026-04-24, étendue 2026-04-25 avec `matchllm/` et `VISION-eleve-emancipe.md`.*
