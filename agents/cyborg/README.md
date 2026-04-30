# Cyborg — Cognition étendue installable

## 📍 Position relative dans `agents/`

- **Framework minimal universel** (4 organes) — complémentaire à [`../agent-evolutif/`](../agent-evolutif/) qui est la stack complète Python.
- **Conçu pour la transmissibilité** : un enfant de 10 ans peut le lire, n'importe quel projet peut l'installer en 2 secondes.
- **Référence théorique :** [`../REFERENCE-clark-cognition-augmentee.txt`](../REFERENCE-clark-cognition-augmentee.txt) (Clark + Friston).
- **Filiation :** simplification radicale de l'architecture du paper [`../paper/architecture-eleve-ia.md`](../paper/architecture-eleve-ia.md). Là où le paper a 121 garde-fous (cf. eval V1), Cyborg en a 0 — juste 4 organes et 1 cycle.
- **Prototypes empiriques :** [`CyborgV0.1/`](CyborgV0.1/) (bras 2D fonctionnel) et [`cyborg-yoan/`](cyborg-yoan/) (squelette V0.0).

---

Un protocole de **cognition augmentée** au sens d'Andy Clark, conçu comme un cyborg externalisé en quatre organes :

- **simple à installer** (une commande, 2 secondes)
- **scientifiquement ancré** (Clark 1998-2024, Friston 2010, predictive processing)
- **transmissible** (un enfant de 10 ans peut le lire et l'utiliser)
- **profond sous le capot** (cycle d'inférence active complet, avec apprentissage par minimisation d'erreur)

---

## Les quatre organes externalisés

| Fichier | Fonction cognitive | Quand il bouge |
|---|---|---|
| `MODELE.md` | Modèle interne, invariants, mission | Rarement — seulement si l'erreur est structurelle |
| `PERCEPTION.md` | État observé du monde au temps *t* | À chaque fin de session |
| `PREDICTION.md` | Inférence active — action proposée | À chaque fin de session |
| `ERREUR.md` | Erreur de prédiction — apprentissage | Quand l'observation diverge de la prédiction |

Le cycle :

```
   MODÈLE ──génère──▶ PRÉDICTION ──action──▶ PERCEPTION ──comparée──▶ ERREUR ──ajuste──▶ MODÈLE
```

---

## Installation dans un nouveau projet (2 secondes)

1. Ouvrir un terminal PowerShell **dans le dossier du projet cible**.
2. Coller :

```powershell
powershell -ExecutionPolicy Bypass -File "C:\Users\Utilisateur\Documents\openClaude\agents\cyborg\cyborg-install.ps1"
```

3. La voix dit *« Cyborg installé. Quatre organes externalisés en place. »*
4. Ouvrir Claude Code dans ce dossier — le cycle d'inférence active démarre au prochain message.

---

## Pour rendre la commande encore plus courte (optionnel)

Ajouter à `$PROFILE` PowerShell :

```powershell
function cyborg { & "C:\Users\Utilisateur\Documents\openClaude\agents\cyborg\cyborg-install.ps1" }
```

Désormais, dans n'importe quel projet, taper simplement :

```
cyborg
```

---

## Ce qui est créé

```
projet/
├── MODELE.md         ← modèle interne (invariants + mission)
├── PERCEPTION.md     ← état observé du monde
├── PREDICTION.md     ← inférence active (action proposée)
├── ERREUR.md         ← erreur de prédiction (apprentissage)
└── .claude/
    ├── settings.json    ← active le hook au démarrage
    └── inference.ps1    ← lit les 4 organes, parle, injecte le contexte
```

---

## Comment ça fonctionne

**À l'ouverture de Claude Code** dans un projet équipé du Cyborg :

1. Le hook `SessionStart` se déclenche (silencieux, instantané)
2. PowerShell lit les 4 organes cognitifs
3. La voix énonce l'action prédite : *« Inférence active. Je propose : [action de PREDICTION.md] »*
4. L'IA reçoit le contexte cognitif complet **avant** ton premier message
5. L'IA compare PREDICTION (passée) avec PERCEPTION (actuelle), note l'écart dans ERREUR si nécessaire

**À la fin de session**, dis simplement *« fini »* / *« stop »* / *« à demain »* :
l'IA met à jour les 4 organes dans l'ordre PERCEPTION → ERREUR → MODELE → PREDICTION avant de partir.

---

## Pourquoi le 4ème organe (ERREUR.md) est essentiel

Sans erreur de prédiction enregistrée, le cyborg ne peut **pas apprendre**. Friston (2010) :

> *« Self-organising systems must minimise their free energy — equivalently, the long-term average of prediction error. »*

Un système qui ne mesure pas l'écart entre ce qu'il a prédit et ce qui s'est passé n'est pas cognitif — c'est un automate qui répète. L'erreur de prédiction est le seul mécanisme par lequel le modèle interne peut s'ajuster au réel.

C'est l'organe le moins glamour, et le plus indispensable.

---

## Origine théorique

| Œuvre | Année | Idée fondatrice utilisée ici |
|---|---|---|
| Clark & Chalmers, *The Extended Mind* | 1998 | **Parity principle** — les fichiers `.md` *sont* des organes cognitifs |
| Clark, *Natural-Born Cyborgs* | 2003 | **Cyborg natif** — l'humain est déjà un cyborg, on le rend explicite |
| Clark, *Supersizing the Mind* | 2008 | **Scaffolded cognition** — la structure externe porte la charge |
| Friston, *Free Energy Principle* | 2010 | **Minimisation de l'erreur de prédiction** — fonction objective du système |
| Clark, *Surfing Uncertainty* | 2015 | **Predictive processing** — le cycle MODÈLE→PRÉDICTION→PERCEPTION→ERREUR |
| Clark, *The Experience Machine* | 2024 | **Profiling effect** — le protocole installé sculpte la cognition future |
