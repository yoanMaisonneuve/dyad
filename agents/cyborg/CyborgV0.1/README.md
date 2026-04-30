# CyborgV0.1 — Bras robotique 2D par inférence active

Premier prototype empirique du framework Cyborg appliqué au contrôle moteur. Démontre **en CLI vivante** le cycle d'inférence active de Friston/Clark sur un cas jouet : un bras 2D à 2 articulations apprend à atteindre une cible aléatoire en partant d'un modèle interne volontairement grossier.

## Pourquoi ça compte

Cet agent est le premier livrable empirique répondant à **Q1** de [`Blueprint-memory/workflow/INFERENCE-ACTIVE-RECHERCHE.md`](../../Blueprint-memory/workflow/INFERENCE-ACTIVE-RECHERCHE.md) — l'équivalence formelle entre l'intuition de Yoan sur le contrôle moteur prédictif et la formalisation Friston.

C'est aussi la **première brique** vers la robotique humanoïde manufacturière + alimentation (axe stratégique long terme).

## Installation

```bash
cd c:\Users\Utilisateur\Documents\openClaude\agents\cyborg\CyborgV0.1
pip install numpy
```

## Lancement

```bash
python eleve.py             # auto, 30 cycles, pause 0.4s
python eleve.py --step      # pas-à-pas (Entrée entre chaque cycle)
python eleve.py --cycles 50 # nombre de cycles
python eleve.py --seed 42   # reproductibilité
```

## Ce que tu vois

À chaque cycle :
1. Une cible est tirée au hasard dans le demi-plan supérieur
2. Le **MODÈLE** prédit deux angles (θ1, θ2)
3. Le bras **exécute** le mouvement (cinématique exacte)
4. La **PERCEPTION** mesure la position atteinte
5. L'**ERREUR** est calculée (distance euclidienne)
6. Le MODÈLE est ajusté pour mieux prédire au prochain coup
7. Affichage ASCII du bras + cible + métriques

```
--- Cycle 12 --------------------------------------------
  Cible           : (+3.20, +1.80)
  Modèle prédit   : θ1=  +28.4°  θ2=  -47.1°
  Position atteinte: (+3.05, +1.95)
  Erreur          : 0.214  (cycle 1 : 1.823)  moy 5 derniers : 0.298
  MODÈLE update   : ‖ΔW‖=0.0034  ‖Δb‖=0.0021

+------------------------------------+
|                                    |
|                                    |
|                .X                  |
|             .@                     |
|         o.                         |
|       .                            |
|     .                              |
|   .                                |
| O                                  |
+------------------------------------+
    O=épaule  o=coude  @=effecteur  X=cible
```

## Architecture

```
CyborgV0.1/
├── MODELE.md           ← modèle interne (W, b appris) — réécrit en fin de session
├── PERCEPTION.md       ← état observé courant
├── PREDICTION.md       ← inférence courante
├── ERREUR.md           ← historique distance par cycle (append-only)
├── log/
│   ├── pensees.md      ← pensées de l'agent (note.md L17)
│   └── changements.md  ← modifications + bénéfices/limites (note.md L17)
├── arm.py              ← cinématique forward exacte
├── modele.py           ← modèle interne (mapping linéaire θ = W·target + b) + IK iterative locale
├── ascii_render.py     ← affichage CLI du bras
├── eleve.py            ← boucle de vie principale
└── README.md
```

## Le cycle d'inférence active implémenté

```
   MODÈLE ─────► PREDICTION ─────► (bras exécute)
      ▲                                  │
      │                                  ▼
   ajuste W,b ◄─── ERREUR ◄───── PERCEPTION
```

C'est exactement le cycle décrit dans [`../MODELE.md`](../MODELE.md) du template Cyborg — appliqué au domaine moteur.

## Ce qui sera testé empiriquement

- L'erreur initiale est-elle effectivement réduite après N cycles ? (réponse attendue : oui, ~70-80% de réduction en 30 cycles)
- Le modèle linéaire suffit-il, ou faut-il un réseau plus riche pour les cibles excentriques ?
- Qu'est-ce qui se passe si on étend à 3 articulations ? (= V0.2, plus proche d'un bras humanoïde)

## Limites assumées de la V0.1

- Modèle interne **linéaire** — saturera sur les cibles aux frontières de l'espace atteignable
- Pas de bruit sensoriel (la perception = position exacte du bras simulé)
- Pas d'obstacles
- Pas d'apprentissage des constantes physiques L1, L2 (supposées connues)
- 2D, pas 3D
- Une seule cible par cycle (pas de séquence pick-and-place)

Ces limites sont les **prochaines étapes** — chaque V0.x lève une de ces contraintes.

## Prochaines versions prévues

| Version | Lève la contrainte | Difficulté |
|---|---|---|
| V0.2 | 3 articulations | facile |
| V0.3 | Bruit sensoriel | facile |
| V0.4 | Obstacles à éviter | moyen |
| V0.5 | Pick-and-place (séquence d'opérations) | moyen |
| V0.6 | Apprentissage de L1, L2 (modèle physique appris aussi) | difficile |
| V0.7 | 3D + vraie vision (caméra simulée) | difficile |
| V1.0 | Bras humanoïde simulé (PyBullet/MuJoCo) | majeur |

---

*Créé : 2026-04-23 · Premier prototype empirique du framework Cyborg appliqué au contrôle moteur*
