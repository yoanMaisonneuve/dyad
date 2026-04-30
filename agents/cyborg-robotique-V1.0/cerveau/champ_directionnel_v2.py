"""Champ directionnel V2 -- modele d'ordre 2 (intuition Yoan : vitesse + acceleration du gradient).

Au lieu de Δp = J · Δθ (lineaire, V1), on capture l'ordre 2 :
  Δp = J · Δθ + (1/2) H_diag · Δθ²

Pour chaque DoF, on fait 3 essais a 3 amplitudes => fit J_i (gradient = vitesse moyenne)
ET H_ii (Hessien diagonal = acceleration du gradient = courbure locale).

Pas de cross-terms (modele separable par DoF) pour rester tractable avec 3 essais/DoF.
Total exploration : n_dof × 3 essais (ex: 15 pour 5 DoF).

Usage en phase application : sampling K candidates + argmin de l'EFE pragmatic
calcule via le modele d'ordre 2 (pas de pseudo-inverse car non-lineaire).
"""
import numpy as np


class ChampDirectionnelV2:
    """Champ avec modele d'ordre 2 par DoF."""

    def __init__(
        self,
        n_dof: int = 5,
        n_obs: int = 3,
        scales: tuple = (0.06, 0.12, 0.18),
        seed: int = 42,
    ):
        self.n_dof = n_dof
        self.n_obs = n_obs
        self.scales = scales
        self.n_essais_par_dof = len(scales)

        # Stockage : observations[dof_id] = list of (signed_amplitude, dp_observed)
        self.observations: dict[int, list] = {i: [] for i in range(n_dof)}

        # Modele d'ordre 2 : J shape (n_obs, n_dof), H shape (n_obs, n_dof)
        self.J = np.zeros((n_obs, n_dof))
        self.H = np.zeros((n_obs, n_dof))

        self.exploration_step = 0
        self.rng = np.random.default_rng(seed)

    def explore_action(self, theta_ref: np.ndarray) -> tuple:
        """Genere le prochain essai canonique avec amplitude variable.

        Retourne (theta_essai, dof_id, signed_amplitude).
        """
        total = self.n_dof * self.n_essais_par_dof
        if self.exploration_step >= total:
            return None, -1, 0.0

        # Ordre : on parcourt tous les DoF a la 1ere amplitude, puis 2eme, puis 3eme
        scale_id = self.exploration_step // self.n_dof
        dof_id = self.exploration_step % self.n_dof
        scale = self.scales[scale_id]
        sign = self.rng.choice([-1.0, 1.0])
        signed_amp = sign * scale

        delta = np.zeros(self.n_dof)
        delta[dof_id] = signed_amp
        self.exploration_step += 1
        return theta_ref + delta, dof_id, signed_amp

    def observe(self, dof_id: int, signed_amplitude: float, dp: np.ndarray):
        """Enregistre observation et fit J_i et H_ii si 3 obs dispo."""
        self.observations[dof_id].append((signed_amplitude, dp.copy()))
        if len(self.observations[dof_id]) >= 3:
            self._fit_dof(dof_id)

    def _fit_dof(self, dof_id: int):
        """Fit Δp_i = J_i · δθ_i + (1/2) H_ii · δθ_i² par moindres carres
        pour chaque dimension d'observation (x, y, z) independamment.
        """
        obs = self.observations[dof_id][-3:]  # 3 dernieres
        deltas = np.array([o[0] for o in obs])  # shape (3,)
        dps = np.array([o[1] for o in obs])  # shape (3, n_obs)

        # Matrice de design : [δθ, (1/2)·δθ²]
        X = np.column_stack([deltas, 0.5 * deltas ** 2])  # (3, 2)

        for d in range(self.n_obs):
            try:
                coeffs, _, _, _ = np.linalg.lstsq(X, dps[:, d], rcond=None)
                self.J[d, dof_id] = coeffs[0]
                self.H[d, dof_id] = coeffs[1]
            except np.linalg.LinAlgError:
                pass

    def predict_dp(self, dtheta: np.ndarray) -> np.ndarray:
        """Predit Δp pour Δθ candidat avec modele d'ordre 2 (sans cross-terms).

        p_pred = J · dtheta + (1/2) H · dtheta²
        """
        return self.J @ dtheta + 0.5 * (self.H @ (dtheta ** 2))

    def predict_dp_batch(self, dthetas: np.ndarray) -> np.ndarray:
        """Vectorise sur batch (K, n_dof) -> (K, n_obs)."""
        # dthetas shape (K, n_dof)
        linear = dthetas @ self.J.T  # (K, n_obs)
        quad = (dthetas ** 2) @ self.H.T  # (K, n_obs)
        return linear + 0.5 * quad

    def is_exploring(self) -> bool:
        return self.exploration_step < self.n_dof * self.n_essais_par_dof

    @property
    def n_observations_total(self) -> int:
        return sum(len(v) for v in self.observations.values())
