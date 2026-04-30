"""Modele interne lineaire 3D : theta = W*target + b.

Port de CyborgV0.1 (2D, 2 DoF) vers 3D N-DoF.
Generative model minimaliste : mapping lineaire cible 3D -> angles articulaires.
Ajuste par regression sur (target, theta_optimal_oracle) - cycle d'inference active baseline.
"""
import numpy as np


class ModeleLineaire:
    """Mapping lineaire theta = W*target + b ajuste par regression.

    Sera remplace en S2 J+9-10 par un vrai generative model AIF avec EFE
    (expected free energy minimization). Sert de baseline pour mesurer le gain.
    """

    def __init__(self, n_dof: int = 5, n_target: int = 3, lr: float = 0.05, seed: int = 42):
        self.n_dof = n_dof
        self.n_target = n_target
        self.lr = lr
        rng = np.random.default_rng(seed)
        self.W = rng.normal(scale=0.1, size=(n_dof, n_target))
        self.b = rng.normal(scale=0.1, size=n_dof)
        self.cycle_count = 0

    def predire(self, target: np.ndarray) -> np.ndarray:
        return self.W @ target + self.b

    def apprendre(self, target: np.ndarray, theta_optimal: np.ndarray) -> tuple[float, float]:
        """Pousse W et b vers la prediction optimale (theta_optimal).
        Retourne (||dW||, ||db||) pour le log."""
        theta_predit = self.predire(target)
        erreur = theta_optimal - theta_predit
        delta_W = self.lr * np.outer(erreur, target)
        delta_b = self.lr * erreur
        self.W += delta_W
        self.b += delta_b
        self.cycle_count += 1
        return float(np.linalg.norm(delta_W)), float(np.linalg.norm(delta_b))
