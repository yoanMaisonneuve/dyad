# Modèle interne — Cyborg

## Origine théorique

Andy Clark, *Natural-Born Cyborgs* (2003) :

> *« We are biological cyborgs, native users of cognitive technologies that fundamentally restructure our mental abilities. »*

Le cyborg n'est pas une fusion humain-machine futuriste. C'est ce que tu **es déjà**, dès que tu as appris à lire et à écrire. Ce projet rend l'extension cognitive **explicite, fiable et auditable** — au lieu de la laisser implicite et fragile.

---

## Architecture cognitive

Quatre **organes externalisés** implémentent le cycle d'inférence active de Friston/Clark :

| Organe (fichier) | Fonction cognitive |
|---|---|
| `MODELE.md` | **Modèle interne** — croyances génératives stables, invariants, mission |
| `PERCEPTION.md` | **État observé** du monde au temps *t* |
| `PREDICTION.md` | **Inférence active** — action proposée pour minimiser l'erreur attendue |
| `ERREUR.md` | **Erreur de prédiction** — divergence prédit vs observé, source d'apprentissage |

### Le cycle d'inférence active

```
   MODÈLE ──génère──▶ PRÉDICTION
      ▲                    │
      │                 (action)
      │                    │
      │                    ▼
   ajuste            PERCEPTION
      │                    │
      │                comparée
      │                    │
      └────── ERREUR ◀─────┘
```

**But du système :** minimiser l'erreur de prédiction *sur la durée*, pas « avoir raison » à chaque session. C'est le **principe de l'énergie libre** (Friston, 2010).

---

## Mission du projet

> *À remplir : qu'est-ce que ce cyborg étendu optimise ? En 3 lignes : quoi / pour qui / pourquoi maintenant.*

Cette section définit la **fonction objective** du modèle interne. Sans mission, l'inférence active n'a pas de direction — toute prédiction est arbitraire.

---

## Règles d'inférence (instructions pour l'IA)

### Au réveil (début de session)

Le hook `inference.ps1` a injecté les 4 organes dans le contexte. À exécuter :

1. **Comparer** la `PREDICTION.md` (ce qui était attendu) avec l'état réel observable maintenant
2. **Noter** tout écart significatif dans `ERREUR.md`
3. **Énoncer** à l'humain : *« dernière prédiction = X, observation actuelle = Y, je propose Z »*
4. **Attendre validation** avant d'agir

### Pendant la session

- **Décision importante** prise → ligne datée dans `PERCEPTION.md` sous « Décisions »
- **Information surprenante** (qui contredit `MODELE.md`) → ligne dans `ERREUR.md`

### À la fermeture (humain dit « fini » / « stop » / « à demain » / « on s'arrête »)

**Avant** de répondre, mettre à jour les 4 organes *dans cet ordre* :

1. `PERCEPTION.md` — état actuel du monde / projet
2. `ERREUR.md` — ce qui n'avait pas été prédit (si applicable)
3. `MODELE.md` — ajuster les invariants seulement si l'erreur est **structurelle** (pas conjoncturelle)
4. `PREDICTION.md` — nouvelle inférence active pour la prochaine session

### Principe de parsimonie (Clark & Chalmers, 1998)

Ne **jamais** demander à l'humain de répéter le contexte. S'il manque, c'est qu'il n'était pas dans les organes externalisés. Donc l'écrire maintenant.

---

## Sources

- Clark, A. & Chalmers, D. (1998). *The Extended Mind*. Analysis 58:1, 7–19.
- Clark, A. (2003). *Natural-Born Cyborgs: Minds, Technologies, and the Future of Human Intelligence*. Oxford University Press.
- Clark, A. (2008). *Supersizing the Mind: Embodiment, Action, and Cognitive Extension*. Oxford University Press.
- Friston, K. (2010). *The free-energy principle: a unified brain theory?*. Nature Reviews Neuroscience 11, 127–138.
- Clark, A. (2015). *Surfing Uncertainty: Prediction, Action, and the Embodied Mind*. Oxford University Press.
- Clark, A. (2024). *The Experience Machine: How Our Minds Predict and Shape Reality*. Pantheon.
