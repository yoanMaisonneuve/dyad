"""Agent Champ Directionnel - approche matchllm appliquee a la robotique.

Tranchee par Yoan 2026-04-30. Remplace le MLP appris (qui n'a pas converge en J+9)
par l'identification empirique d'une jacobienne locale M (champ directionnel).

Phase 1 (exploration) : n_dof essais canoniques pour identifier M
Phase 2 (application) : Delta_theta = M^+ · (p* - p_observe)

Aucun acces a la jacobienne MuJoCo. L'agent apprend M par interaction.
Theoriquement : convergence en n_dof+1 = 6 essais (vs 30 pour MLP qui n'a pas converge).
"""
from collections import deque

import mujoco
import numpy as np

from cerveau.champ_directionnel import ChampDirectionnel


class CyborgChampAgent:
    """Agent qui apprend a controler un bras via champ directionnel local."""

    def __init__(
        self,
        model: mujoco.MjModel,
        data: mujoco.MjData,
        end_effector_body: str,
        n_dof: int = 5,
        exploration_delta: float = 0.15,
        application_step: float = 0.5,
        learning_rate_M: float = 0.3,
        seed: int = 42,
    ):
        self.model = model
        self.data = data
        self.n_dof = n_dof
        self.application_step = application_step

        self.body_id = mujoco.mj_name2id(
            model, mujoco.mjtObj.mjOBJ_BODY, end_effector_body
        )
        if self.body_id == -1:
            raise ValueError(f"Body '{end_effector_body}' introuvable.")

        self.joint_limits = self._extract_joint_limits()

        # Champ directionnel local
        self.champ = ChampDirectionnel(
            n_dof=n_dof,
            n_obs=3,
            exploration_delta=exploration_delta,
            learning_rate_M=learning_rate_M,
            seed=seed,
        )

        # Etat reference pour les essais (theta_0, p_0)
        self.theta_ref = None
        self.p_ref = None

    def _extract_joint_limits(self) -> tuple:
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

    def execute(self, theta: np.ndarray) -> np.ndarray:
        # Clip aux limites
        low, high = self.joint_limits
        theta_clipped = np.clip(theta, low, high)
        self.data.qpos[: self.n_dof] = theta_clipped
        mujoco.mj_forward(self.model, self.data)
        return self.data.xpos[self.body_id].copy()

    def reset_reference(self):
        """Capture l'etat courant comme reference pour les prochains essais."""
        self.theta_ref = self.data.qpos[: self.n_dof].copy()
        self.p_ref = self.data.xpos[self.body_id].copy()

    def cycle(self, target: np.ndarray) -> dict:
        """Un cycle : si exploration -> essai canonique. Sinon -> correction par M^+."""
        # Reference pour mesurer Delta_p de cet essai
        if self.theta_ref is None:
            self.reset_reference()

        theta_current = self.data.qpos[: self.n_dof].copy()

        if self.champ.is_exploring():
            # Phase EXPLORATION : varie 1 joint canonique
            theta_essai, joint_id = self.champ.explore_action(self.theta_ref)
            p_observed = self.execute(theta_essai)
            dtheta = theta_essai - self.theta_ref
            dp = p_observed - self.p_ref
            self.champ.observe(dtheta, dp)
            distance = float(np.linalg.norm(p_observed - target))
            phase = f"EXPLORATION joint {joint_id}"
            correction_norm = 0.0
        else:
            # Phase APPLICATION : correction par M^+ · erreur
            p_current = self.execute(theta_current)
            error_3d = target - p_current
            dtheta_correction = self.champ.correction(error_3d)
            theta_new = theta_current + self.application_step * dtheta_correction
            p_observed = self.execute(theta_new)
            distance = float(np.linalg.norm(p_observed - target))

            # Met a jour M avec cette nouvelle observation
            dtheta_real = theta_new - theta_current
            dp_real = p_observed - p_current
            if np.linalg.norm(dtheta_real) > 1e-4:
                self.champ.observe(dtheta_real, dp_real)

            phase = "APPLICATION"
            correction_norm = float(np.linalg.norm(dtheta_correction))

        return {
            "target": target.copy(),
            "p_observed": p_observed,
            "distance": distance,
            "phase": phase,
            "correction_norm": correction_norm,
            "M_norm": float(np.linalg.norm(self.champ.M)),
            "n_obs": len(self.champ.buffer_dtheta),
        }
