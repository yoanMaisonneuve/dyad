"""V4 ADAPTIVE -- identification ONLINE de J(theta) en temps reel.

Insight Yoan 2026-04-30 : la jacobienne J n'est PAS constante, elle depend de theta.
Et les DoF sont COUPLES (pas independants). Solution : recalibrer J localement a
chaque step pendant le mouvement.

Algorithme :
1. Buffer roulant des K dernieres observations (theta, p)
2. A chaque step :
   a. Fit J locale par moindres carres sur les differences (delta_theta, delta_p) du buffer
   b. Correction = J_locale^+ . (target - p_current)
   c. Ajoute petit bruit (persistance d'excitation)
   d. Execute, observe, append au buffer
3. Goto 1

Capture implicitement les cross-terms H_ij car J(theta) varie selon la config.
Pas de phase exploration separee - on apprend EN BOUGEANT.
"""
from collections import deque

import mujoco
import numpy as np


class CyborgAdaptiveAgent:
    def __init__(self, model, data, end_effector_body, n_dof=5,
                 buffer_size=12,
                 step_size=0.3,
                 noise_scale=0.02,
                 tip_pair=None,
                 seed=42):
        self.model = model
        self.data = data
        self.n_dof = n_dof
        self.step_size = step_size
        self.noise_scale = noise_scale

        self.body_id = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, end_effector_body)
        if self.body_id == -1:
            raise ValueError(f"Body '{end_effector_body}' introuvable.")
        self.tip_id_a = -1
        self.tip_id_b = -1
        if tip_pair is not None:
            self.tip_id_a = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, tip_pair[0])
            self.tip_id_b = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, tip_pair[1])

        self.joint_limits = self._extract_joint_limits()
        self.buffer_theta = deque(maxlen=buffer_size)
        self.buffer_p = deque(maxlen=buffer_size)
        self.J_local = np.zeros((3, n_dof))
        self.rng = np.random.default_rng(seed)

    def _extract_joint_limits(self):
        low = np.zeros(self.n_dof)
        high = np.zeros(self.n_dof)
        for i in range(self.n_dof):
            if self.model.jnt_limited[i]:
                low[i] = self.model.jnt_range[i, 0]
                high[i] = self.model.jnt_range[i, 1]
            else:
                low[i] = -np.pi
                high[i] = np.pi
        return (low, high)

    def execute(self, theta):
        low, high = self.joint_limits
        self.data.qpos[:self.n_dof] = np.clip(theta, low, high)
        mujoco.mj_forward(self.model, self.data)
        if self.tip_id_a >= 0 and self.tip_id_b >= 0:
            return (self.data.xpos[self.tip_id_a] + self.data.xpos[self.tip_id_b]) / 2.0
        return self.data.xpos[self.body_id].copy()

    def _update_J_local(self):
        """Fit J locale par moindres carres sur les differences du buffer."""
        if len(self.buffer_theta) < 2:
            return
        thetas = np.array(self.buffer_theta)
        ps = np.array(self.buffer_p)
        # Differences consecutives
        dthetas = np.diff(thetas, axis=0)
        dps = np.diff(ps, axis=0)
        if len(dthetas) < self.n_dof:
            return
        # Solve dp = dtheta @ J^T pour chaque dim de p
        # J = lstsq(dthetas, dps)
        try:
            J_T, _, _, _ = np.linalg.lstsq(dthetas, dps, rcond=1e-3)
            self.J_local = J_T.T  # (3, n_dof)
        except np.linalg.LinAlgError:
            pass

    def step(self, target):
        """Un pas adaptive : update J locale + correction + execute + buffer."""
        theta_current = self.data.qpos[:self.n_dof].copy()
        p_current = self.execute(theta_current)
        e = target - p_current

        self._update_J_local()

        # Correction
        if np.linalg.norm(self.J_local) > 1e-6:
            try:
                J_pinv = np.linalg.pinv(self.J_local, rcond=1e-3)
                correction = J_pinv @ e
            except np.linalg.LinAlgError:
                correction = np.zeros(self.n_dof)
        else:
            correction = np.zeros(self.n_dof)

        # Action = step_size * correction + bruit (persistance excitation)
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
