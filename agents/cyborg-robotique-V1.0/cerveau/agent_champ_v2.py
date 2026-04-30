"""Agent Champ Directionnel V2 -- avec modele d'ordre 2 + sampling EFE.

Adaptation J+9 V4 sur intuition Yoan (3 mouvements/DoF + integration ordre 2).
Phase exploration : n_dof × 3 = 15 essais canoniques avec amplitudes croissantes.
Phase application : sample K candidates, predict via modele d'ordre 2, argmin EFE.
"""
import mujoco
import numpy as np

from cerveau.champ_directionnel_v2 import ChampDirectionnelV2


class CyborgChampV2Agent:
    def __init__(
        self,
        model: mujoco.MjModel,
        data: mujoco.MjData,
        end_effector_body: str,
        n_dof: int = 5,
        scales_exploration: tuple = (0.06, 0.12, 0.18),
        n_candidates_app: int = 80,
        sampling_scale: float = 0.20,
        seed: int = 42,
    ):
        self.model = model
        self.data = data
        self.n_dof = n_dof
        self.n_candidates = n_candidates_app
        self.sampling_scale = sampling_scale

        self.body_id = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, end_effector_body)
        if self.body_id == -1:
            raise ValueError(f"Body '{end_effector_body}' introuvable.")

        self.joint_limits = self._extract_joint_limits()

        self.champ = ChampDirectionnelV2(
            n_dof=n_dof, n_obs=3, scales=scales_exploration, seed=seed
        )

        self.theta_ref = None
        self.p_ref = None
        self._rng = np.random.default_rng(seed + 100)

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
        low, high = self.joint_limits
        theta_clipped = np.clip(theta, low, high)
        self.data.qpos[: self.n_dof] = theta_clipped
        mujoco.mj_forward(self.model, self.data)
        return self.data.xpos[self.body_id].copy()

    def reset_reference(self):
        self.theta_ref = self.data.qpos[: self.n_dof].copy()
        self.p_ref = self.data.xpos[self.body_id].copy()

    def cycle(self, target: np.ndarray) -> dict:
        if self.theta_ref is None:
            self.reset_reference()

        if self.champ.is_exploring():
            # Phase EXPLORATION
            theta_essai, dof_id, signed_amp = self.champ.explore_action(self.theta_ref)
            p_observed = self.execute(theta_essai)
            dp = p_observed - self.p_ref
            self.champ.observe(dof_id, signed_amp, dp)

            distance = float(np.linalg.norm(p_observed - target))
            phase = f"EXPL DoF{dof_id} amp{signed_amp:+.2f}"
            return {
                "target": target.copy(),
                "p_observed": p_observed,
                "distance": distance,
                "phase": phase,
                "n_obs": self.champ.n_observations_total,
                "J_norm": float(np.linalg.norm(self.champ.J)),
                "H_norm": float(np.linalg.norm(self.champ.H)),
                "best_efe": float("nan"),
            }

        # Phase APPLICATION : sample + argmin EFE avec modele ordre 2
        theta_current = self.data.qpos[: self.n_dof].copy()
        p_current = self.execute(theta_current)

        # Sample K candidates Δθ
        deltas = self._rng.normal(scale=self.sampling_scale, size=(self.n_candidates, self.n_dof))
        theta_candidates = theta_current[None, :] + deltas
        # Clip + recalcule deltas effectifs
        low, high = self.joint_limits
        theta_candidates = np.clip(theta_candidates, low, high)
        deltas_eff = theta_candidates - theta_current[None, :]

        # Predict Δp via modele ordre 2 (vectorise)
        dp_preds = self.champ.predict_dp_batch(deltas_eff)  # (K, 3)
        p_preds = p_current[None, :] + dp_preds

        # EFE pragmatic
        efe = np.sum((p_preds - target[None, :]) ** 2, axis=1)
        idx = int(np.argmin(efe))
        theta_chosen = theta_candidates[idx]
        best_efe = float(efe[idx])

        # Execute
        p_observed = self.execute(theta_chosen)
        distance = float(np.linalg.norm(p_observed - target))

        # Optionnel : ajouter cette nouvelle obs au modele (RLS-like - skip pour simplicite V2)

        return {
            "target": target.copy(),
            "p_observed": p_observed,
            "distance": distance,
            "phase": "APPLICATION",
            "n_obs": self.champ.n_observations_total,
            "J_norm": float(np.linalg.norm(self.champ.J)),
            "H_norm": float(np.linalg.norm(self.champ.H)),
            "best_efe": best_efe,
        }
