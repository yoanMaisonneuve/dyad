"""V5 -- DLS (damped least squares) + heritage de V4 adaptive."""
import numpy as np
import mujoco

from cerveau.agent_adaptive import CyborgAdaptiveAgent


class CyborgAdaptiveV5(CyborgAdaptiveAgent):
    """V5 = V4 adaptive + DLS pour resoudre singularites cinematiques (Koch)."""

    def __init__(self, *args, lambda_dls=0.05, **kwargs):
        super().__init__(*args, **kwargs)
        self.lambda_dls = lambda_dls

    def _correction_dls(self, e):
        """Damped Least Squares : J^T (JJ^T + lambda^2 I)^-1 e."""
        if np.linalg.norm(self.J_local) < 1e-6:
            return np.zeros(self.n_dof)
        JJT = self.J_local @ self.J_local.T
        JJT_reg = JJT + (self.lambda_dls ** 2) * np.eye(3)
        try:
            return self.J_local.T @ np.linalg.solve(JJT_reg, e)
        except np.linalg.LinAlgError:
            return np.zeros(self.n_dof)

    def step(self, target):
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
            "p_observed": p_observed,
            "distance": distance,
            "J_norm": float(np.linalg.norm(self.J_local)),
            "buffer_size": len(self.buffer_theta),
            "correction_norm": float(np.linalg.norm(correction)),
        }
