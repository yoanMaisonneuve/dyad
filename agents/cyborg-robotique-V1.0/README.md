# Print Your Own Optimus — Cerveau opensource auto-calibré

Framework Python opensource pour donner un **cerveau** à n'importe quel bras robotique DIY 3D-print.

Le code apprend son corps : il teste son nouveau bras, mesure sa force et ses limites, s'auto-calibre, puis exécute des tâches.

> *« Chaque foyer peut imprimer son humanoïde et installer le cerveau opensource. »*

## Vision

- N'importe qui imprime 3D un bras (ou humanoïde complet plus tard) avec ses propres pièces et servomoteurs
- Achète seulement les contrôleurs/électronique (Arduino, Raspberry Pi, bridges moteurs, ESP32)
- Installe ce cerveau Python opensource
- Le code s'auto-calibre au matériel via inférence active (auto-modélisation corporelle)
- Le bras est prêt à exécuter des tâches

## Cœur scientifique

**Inférence active appliquée à l'auto-modélisation corporelle.** Le cerveau minimise la free energy expected entre ses prédictions sur son propre corps et ses observations sensorielles. Lineage théorique : Friston, Lanillos (iCub, illusion bras caoutchouc), Buckley.

Thèse associée (preprint F1 en cours) : *« Active Inference avec generative model gaussien à horizon fini = Nonlinear Model Predictive Control sous régularité H1-H4 ; cas d'application puissant : auto-modélisation corporelle. »*

## Statut — V0.1 en construction

Sprint 30 jours du 2026-04-30 au 2026-05-26. Détail : `personnel/objectifopus47.md` du repo parent.

- ✅ S1 (J+1-7) : audit + scope figé + pivot Print Your Own Optimus tranché
- 🔄 S2 (J+8-14) : cerveau Python + auto-calibration sim sur 1 bras MuJoCo
- ⏳ S3 (J+15-21) : portabilité 3 bras LeRobot + Isaac/Gazebo
- ⏳ S4 (J+22-28) : démo hardware réelle (assemblage tuiles magnétiques)

## Installation (en cours de définition)

Prérequis : Python 3.10+ (testé 3.14), pip.

```bash
pip install -r requirements.txt
python 01_setup_test.py
```

Si tout fonctionne : une fenêtre s'ouvre avec un bras 2 DoF qui bouge en sinusoïde dans MuJoCo.

## Roadmap V0.1 → V1.0

- **V0.1** (J+28) : cerveau monolithique + auto-cal + 3 bras LeRobot supportés en sim + 1 bras DIY hardware
- **V0.2** (post-sprint, juin) : refacto modulaire + ajout 2-3 bras supplémentaires
- **V1.0** (~6 mois) : framework grand public + guide impression 3D + communauté

## Licence

Apache 2.0 (code) + CC-BY 4.0 (docs) + CDLA-Permissive 2.0 (datasets démo). Pas de paperasse défensive — on construit par altruisme.

## Lien repo parent

Système heartbeat + vision + sprint complet : [yoanMaisonneuve/dyad](https://github.com/yoanMaisonneuve/dyad).
