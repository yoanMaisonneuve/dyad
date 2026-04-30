"""Baseline DLS-IK Buss 2009 avec jacobienne MuJoCo (ground truth).

Reference: Buss S.R. 2009 "Introduction to Inverse Kinematics with Jacobian
Transpose, Pseudoinverse and Damped Least Squares methods"
https://mathweb.ucsd.edu/~sbuss/ResearchWeb/ikmethods/SdlsPaper.pdf

Differences vs notre cerveau/ik_oracle.py:
  - ik_oracle.py : pseudoinverse pure + descente gradient simple, protocole 1-step
  - baseline_dls_ik.py : DLS classique (Buss) avec lambda Tikhonov, multi-step

C'est le vrai baseline academique de reference pour comparaison fair avec V6.
"""
import mujoco
import numpy as np


class BaselineDLSIK:
    """DLS-IK classique avec jacobienne MuJoCo exacte (oracle, ground truth)."""

    def __init__(self, model, data, end_effector_body, n_dof=5,
                 lambda_dls=0.05, step_size=0.5, tip_pair=None):
        self.model = model
        self.data = data
        self.n_dof = n_dof
        self.lambda_dls = lambda_dls
        self.step_size = step_size

        self.body_id = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, end_effector_body)
        if self.body_id == -1:
            raise ValueError(f"Body '{end_effector_body}' introuvable.")
        self.tip_id_a, self.tip_id_b = -1, -1
        if tip_pair is not None:
            self.tip_id_a = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, tip_pair[0])
            self.tip_id_b = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, tip_pair[1])

        self.joint_limits = self._extract_joint_limits()

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

    def get_ee_pos(self):
        if self.tip_id_a >= 0 and self.tip_id_b >= 0:
            return (self.data.xpos[self.tip_id_a] + self.data.xpos[self.tip_id_b]) / 2.0
        return self.data.xpos[self.body_id].copy()

    def get_jacobian_mujoco(self):
        """Jacobienne EXACTE via MuJoCo (oracle ground truth)."""
        if self.tip_id_a >= 0 and self.tip_id_b >= 0:
            jacp_a = np.zeros((3, self.model.nv))
            jacp_b = np.zeros((3, self.model.nv))
            mujoco.mj_jacBody(self.model, self.data, jacp_a, None, self.tip_id_a)
            mujoco.mj_jacBody(self.model, self.data, jacp_b, None, self.tip_id_b)
            jacp = (jacp_a + jacp_b) / 2.0
        else:
            jacp = np.zeros((3, self.model.nv))
            mujoco.mj_jacBody(self.model, self.data, jacp, None, self.body_id)
        return jacp[:, :self.n_dof]

    def step(self, target):
        """Un pas DLS-IK Buss 2009."""
        theta_current = self.data.qpos[:self.n_dof].copy()
        mujoco.mj_forward(self.model, self.data)
        p_current = self.get_ee_pos()
        e = target - p_current

        J = self.get_jacobian_mujoco()  # Vraie jacobienne (oracle)

        # DLS Buss 2009: delta_theta = J^T (J J^T + lambda^2 I)^(-1) e
        JJT = J @ J.T
        JJT_reg = JJT + (self.lambda_dls ** 2) * np.eye(3)
        try:
            delta_theta = J.T @ np.linalg.solve(JJT_reg, e)
        except np.linalg.LinAlgError:
            delta_theta = np.zeros(self.n_dof)

        low, high = self.joint_limits
        theta_new = np.clip(theta_current + self.step_size * delta_theta, low, high)
        self.data.qpos[:self.n_dof] = theta_new
        mujoco.mj_forward(self.model, self.data)
        p_observed = self.get_ee_pos()
        distance = float(np.linalg.norm(p_observed - target))

        return {
            "p_observed": p_observed,
            "distance": distance,
            "J_norm": float(np.linalg.norm(J)),
        }
