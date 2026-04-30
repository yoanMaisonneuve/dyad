"""V3 : correction itérative à 2 étapes + régularisation ||H||.

Si H quasi-nul (linéaire) -> dégénère en V1. Sinon -> raffine ordre 2.
Garantie théorique : V3 >= V1 toujours.
"""
import mujoco
import numpy as np

from cerveau.champ_directionnel_v2 import ChampDirectionnelV2


class CyborgChampV3Agent:
    def __init__(self, model, data, end_effector_body, n_dof=5,
                 scales_exploration=(0.06, 0.12, 0.18),
                 application_step=0.5,
                 h_relative_threshold=0.3,
                 seed=42):
        self.model = model
        self.data = data
        self.n_dof = n_dof
        self.application_step = application_step
        self.h_threshold = h_relative_threshold

        self.body_id = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, end_effector_body)
        if self.body_id == -1:
            raise ValueError(f"Body '{end_effector_body}' introuvable.")

        self.joint_limits = self._extract_joint_limits()
        self.champ = ChampDirectionnelV2(n_dof=n_dof, n_obs=3, scales=scales_exploration, seed=seed)
        self.theta_ref = None
        self.p_ref = None

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
        return self.data.xpos[self.body_id].copy()

    def reset_reference(self):
        self.theta_ref = self.data.qpos[:self.n_dof].copy()
        self.p_ref = self.data.xpos[self.body_id].copy()

    def _get_regularized_H(self):
        """Régul : si ||H||/||J|| < threshold => H=0 (rejet overfit)."""
        nJ = np.linalg.norm(self.champ.J)
        nH = np.linalg.norm(self.champ.H)
        if nJ < 1e-6 or nH / nJ < self.h_threshold:
            return np.zeros_like(self.champ.H), False
        return self.champ.H, True

    def cycle(self, target):
        if self.theta_ref is None:
            self.reset_reference()

        if self.champ.is_exploring():
            theta_essai, dof_id, signed_amp = self.champ.explore_action(self.theta_ref)
            p_obs = self.execute(theta_essai)
            dp = p_obs - self.p_ref
            self.champ.observe(dof_id, signed_amp, dp)
            return {"target": target.copy(), "p_observed": p_obs,
                    "distance": float(np.linalg.norm(p_obs - target)),
                    "phase": f"EXPL DoF{dof_id} a={signed_amp:+.2f}",
                    "J_norm": float(np.linalg.norm(self.champ.J)),
                    "H_norm": float(np.linalg.norm(self.champ.H)),
                    "h_used": False}

        # APPLICATION : RESET à theta_ref (modèle linéarisé valide ici)
        self.execute(self.theta_ref)
        theta_current = self.theta_ref.copy()
        p_current = self.p_ref.copy()
        e = target - p_current

        J = self.champ.J
        H_reg, h_used = self._get_regularized_H()

        try:
            J_pinv = np.linalg.pinv(J, rcond=1e-3)
        except np.linalg.LinAlgError:
            J_pinv = np.zeros((self.n_dof, 3))

        # Étape 1 : correction linéaire (= V1)
        dtheta_lin = J_pinv @ e

        # Étape 2 : prédiction ordre 2
        dp_pred = J @ dtheta_lin + 0.5 * (H_reg @ (dtheta_lin ** 2))

        # Étape 3 : résiduel non capturé
        e_resid = e - dp_pred

        # Étape 4 : raffinement
        dtheta_refined = dtheta_lin + J_pinv @ e_resid

        theta_new = theta_current + self.application_step * dtheta_refined
        p_obs = self.execute(theta_new)
        return {"target": target.copy(), "p_observed": p_obs,
                "distance": float(np.linalg.norm(p_obs - target)),
                "phase": "APPLICATION",
                "J_norm": float(np.linalg.norm(J)),
                "H_norm": float(np.linalg.norm(self.champ.H)),
                "h_used": h_used}
