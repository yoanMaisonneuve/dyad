"""Champ directionnel local : identification empirique de la jacobienne M.

Approche tranchee par Yoan 2026-04-30 (lineage matchllm) :
  Au lieu d'apprendre la cinematique f(theta) -> p globalement (mon MLP qui n'a pas
  converge), on apprend la matrice M ∈ R^(3×n) telle que Delta_p = M · Delta_theta
  localement. C'est le "champ directionnel local" entre l'espace articulaire et
  l'espace observation.

Algorithme :
  1. Phase EXPLORATION (n_dof essais) : varier 1 joint a la fois (perturbations
     canoniques), observer Delta_p. Identifie chaque colonne de M.
  2. Construction M par moindres carres sur les observations accumulees.
  3. Phase APPLICATION : pour atteindre une cible p*, calculer la correction
     Delta_theta = M^+ · (p* - p_observe), appliquer.
  4. Mise a jour M continue (recursive least squares simple).

Inspire de matchllm (champs directionnels comme structure mathematique de base).
Equivalent a une identification online de jacobienne empirique (Broyden-like).
"""
import numpy as np


class ChampDirectionnel:
    """Identification empirique de la jacobienne M : Delta_p = M · Delta_theta."""

    def __init__(
        self,
        n_dof: int = 5,
        n_obs: int = 3,
        exploration_delta: float = 0.15,
        learning_rate_M: float = 0.3,
        seed: int = 42,
    ):
        self.n_dof = n_dof
        self.n_obs = n_obs
        self.exploration_delta = exploration_delta
        self.lr_M = learning_rate_M

        # Buffer des paires (Delta_theta, Delta_p) observees
        self.buffer_dtheta: list[np.ndarray] = []
        self.buffer_dp: list[np.ndarray] = []

        # Matrice M ∈ R^(n_obs × n_dof). Initialisee zero.
        self.M = np.zeros((n_obs, n_dof))
        self.exploration_step = 0  # compteur essais exploration (pour rotation joints)
        self.fully_explored = False

        self.rng = np.random.default_rng(seed)

    def explore_action(self, theta_current: np.ndarray) -> tuple[np.ndarray, int]:
        """Phase exploration : varie 1 joint a la fois (canonical perturbation).

        Retourne (theta_perturbed, joint_id_explore).
        """
        joint_id = self.exploration_step % self.n_dof
        delta = np.zeros(self.n_dof)
        # Direction aleatoire (+/- delta) pour le joint courant
        sign = self.rng.choice([-1.0, 1.0])
        delta[joint_id] = sign * self.exploration_delta
        self.exploration_step += 1
        return theta_current + delta, joint_id

    def observe(self, dtheta: np.ndarray, dp: np.ndarray):
        """Enregistre une observation (Delta_theta, Delta_p) et met a jour M."""
        self.buffer_dtheta.append(dtheta.copy())
        self.buffer_dp.append(dp.copy())

        # Si on a au moins n_dof observations, on peut estimer M par moindres carres
        if len(self.buffer_dtheta) >= self.n_dof:
            self._fit_M()
            if len(self.buffer_dtheta) >= self.n_dof:
                self.fully_explored = True

    def _fit_M(self):
        """Estimation M par moindres carres sur le buffer.

        Resout M = argmin_M sum_k ||Delta_p_k - M · Delta_theta_k||^2
        Solution analytique : M = (Dp^T · Dtheta) · (Dtheta^T · Dtheta + lambda·I)^-1
        avec petit lambda pour regulariser.
        """
        Dtheta = np.array(self.buffer_dtheta)  # (N, n_dof)
        Dp = np.array(self.buffer_dp)  # (N, n_obs)

        # Regression : M^T · Dtheta_i = Dp_i pour chaque i
        # En matrice : Dtheta · M^T = Dp
        # M^T = (Dtheta^T · Dtheta + lambda·I)^-1 · Dtheta^T · Dp
        lam = 1e-3
        gram = Dtheta.T @ Dtheta + lam * np.eye(self.n_dof)
        try:
            M_T = np.linalg.solve(gram, Dtheta.T @ Dp)
            M_new = M_T.T
            # Smooth update vers M_new (RLS-like simple)
            self.M = (1.0 - self.lr_M) * self.M + self.lr_M * M_new
        except np.linalg.LinAlgError:
            pass  # garde l'ancien M si singulier

    def correction(self, error_3d: np.ndarray) -> np.ndarray:
        """Calcule la correction articulaire pour reduire l'erreur 3D.

        Delta_theta = M^+ · error  (pseudo-inverse appliquee a l'erreur space)
        """
        if not self.fully_explored or np.allclose(self.M, 0):
            return np.zeros(self.n_dof)
        try:
            M_pinv = np.linalg.pinv(self.M, rcond=1e-3)
            return M_pinv @ error_3d
        except np.linalg.LinAlgError:
            return np.zeros(self.n_dof)

    def is_exploring(self) -> bool:
        """Retourne True si on est encore en phase exploration."""
        return self.exploration_step < self.n_dof
