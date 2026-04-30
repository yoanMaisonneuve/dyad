# Modele interne -- CyborgV0.1
**Derniere mise a jour :** 2026-04-23T23:48:53
**Cycles d'apprentissage :** 5

## Architecture cognitive
Modele interne du cyborg = mapping lineaire `theta = W*target + b` qui predit les angles articulaires (theta1, theta2) a partir d'une cible (x, y). Ajuste par minimisation de l'erreur de prediction (Friston).

## Parametres appris
**W (matrice 2x2) :**
```
[[-0.3682, +0.2497],
 [+0.3940, +0.5306]]
```

**b (biais 2) :**
```
[+0.4700, +0.4353]
```

## Constantes du bras (modele physique)
- L1 (epaule-coude) = 3.0
- L2 (coude-effecteur) = 2.0
- Espace atteignable : couronne de rayons 1.0 a 5.0 dans le demi-plan superieur

## Mission
Apprendre a predire des angles qui amenent l'effecteur a une cible donnee, avec le moins d'erreur possible, en partant d'une initialisation volontairement mauvaise. Demontre empiriquement le cycle d'inference active de Friston/Clark sur un cas jouet de controle moteur -- premier pas vers la robotique humanoide manufacturiere et alimentaire.

## Lien theorique
Cf. `Blueprint-memory/workflow/INFERENCE-ACTIVE-RECHERCHE.md` -- premier livrable empirique repondant a Q1.
