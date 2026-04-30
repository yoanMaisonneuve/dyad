"""V6 = V4 ADAPTIVE + warmup canonique + DLS regularization.

Resout bootstrap problem identifie : sur certains seeds, les 12 premieres actions
aleatoires laissaient J degenere -> agent coince dans region singuliere.

Solution combinee:
  1. Warmup canonique : 5 essais (1 par DoF, sign aleatoire, amplitude moyenne)
     remplit le buffer avec observations diversifiees
  2. DLS regularization : J^T (JJ^T + lambda^2 I)^-1, protege quand J degenere
"""
import mujoco
import numpy as np

from cerveau.agent_adaptive import CyborgAdaptiveAgent


class CyborgAdaptiveV6(CyborgAdaptiveAgent):
    def __init__(self, *args, lambda_dls=0.05, warmup_amplitude=0.15, **kwargs):
        super().__init__(*args, **kwargs)
        self.lambda_dls = lambda_dls
        self.warmup_amplitude = warmup_amplitude
        self.warmup_done = False

    def warmup(self):
        """Warmup canonique : 1 essai par DoF, sign aleatoire, remplit buffer."""
        if self.warmup_done:
            return
        theta_init = self.data.qpos[:self.n_dof].copy()
        for i in range(self.n_dof):
            sign = float(self.rng.choice([-1.0, 1.0]))
            delta = np.zeros(self.n_dof)
            delta[i] = sign * self.warmup_amplitude
            theta_essai = theta_init + delta
            p_obs = self.execute(theta_essai)
            self.buffer_theta.append(theta_essai.copy())
            self.buffer_p.append(p_obs.copy())
        # Reset a init et update J avec les nouvelles obs
        self.execute(theta_init)
        self._update_J_local()
        self.warmup_done = True

    def _correction_dls(self, e):
        """DLS : J^T (JJ^T + lambda^2 I)^-1 e."""
        if np.linalg.norm(self.J_local) < 1e-6:
            return np.zeros(self.n_dof)
        JJT = self.J_local @ self.J_local.T
        JJT_reg = JJT + (self.lambda_dls ** 2) * np.eye(3)
        try:
            return self.J_local.T @ np.linalg.solve(JJT_reg, e)
        except np.linalg.LinAlgError:
            return np.zeros(self.n_dof)

    def step(self, target):
        if not self.warmup_done:
            self.warmup()
        theta_current = self.data.qpos[:self.n_dof].copy()
        p_current = self.execute(theta_current)
        e = target - p_current
        self._update_J_local()
        correction = self._correction_dls(e)
        noise = self.rng.normal(scale=self.noise_scale, size=self.n_dof)
        delta_theta = self.step_size * correction + noise
        theta_new = theta_current + delta_theta
        p_observed = self.execute(theta_new)
        distance = float(np.linalg.norm(p_observed - target))
        self.buffer_theta.append(theta_new.copy())
        self.buffer_p.append(p_observed.copy())
        return {
            "p_observed": p_observed, "distance": distance,
            "J_norm": float(np.linalg.norm(self.J_local)),
            "buffer_size": len(self.buffer_theta),
            "correction_norm": float(np.linalg.norm(correction)),
        }
