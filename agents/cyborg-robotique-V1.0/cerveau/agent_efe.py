"""Agent EFE J+9 - version separee du baseline (b dans option D+alpha+b).

Utilise GenerativeModelAppris (modele interne appris, pas la jacobienne MuJoCo)
+ EFEPolicy (selection action par minimisation Expected Free Energy).

C'est la premiere implementation du cerveau Print Your Own Optimus
qui n'a AUCUN acces a la verite physique du simulateur :
  - Pas de jacobienne MuJoCo
  - Pas de cinematique forward connue
  - Le modele interne apprend tout par interaction (cycle perception-action)

Le baseline (cerveau/agent.py) est preserve intact pour comparaison.
"""
from collections import deque

import mujoco
import numpy as np

from cerveau.efe_policy import EFEPolicy
from cerveau.generative_model_appris import GenerativeModelAppris


class CyborgEFEAgent:
    """Agent qui apprend a controler un bras par EFE + modele appris."""

    def __init__(
        self,
        model: mujoco.MjModel,
        data: mujoco.MjData,
        end_effector_body: str,
        n_dof: int = 5,
        n_candidates: int = 30,
        action_scale: float = 0.15,
        n_hidden: int = 32,
        learning_rate: float = 0.01,
        buffer_size: int = 300,
        n_grad_steps_per_cycle: int = 10,
        batch_size: int = 16,
        seed: int = 42,
    ):
        self.model = model
        self.data = data
        self.n_dof = n_dof
        self.batch_size = batch_size
        self.n_grad_steps_per_cycle = n_grad_steps_per_cycle

        self.body_id = mujoco.mj_name2id(
            model, mujoco.mjtObj.mjOBJ_BODY, end_effector_body
        )
        if self.body_id == -1:
            raise ValueError(f"Body '{end_effector_body}' introuvable dans le modele.")

        # Detecte les limites articulaires depuis le MJCF
        self.joint_limits = self._extract_joint_limits()

        # Generative model APPRIS (le code apprend son corps)
        self.gm = GenerativeModelAppris(
            n_dof=n_dof, n_obs=3, n_hidden=n_hidden, lr=learning_rate, seed=seed
        )

        # EFE policy
        self.policy = EFEPolicy(
            self.gm,
            n_dof=n_dof,
            joint_limits=self.joint_limits,
            n_candidates=n_candidates,
            scale=action_scale,
            seed=seed + 1,
        )

        # Buffer experience pour apprentissage online
        self.buffer_theta: deque = deque(maxlen=buffer_size)
        self.buffer_p: deque = deque(maxlen=buffer_size)

        self._rng = np.random.default_rng(seed + 2)

    def _extract_joint_limits(self) -> tuple:
        """Extrait les limites articulaires des n_dof premiers joints depuis le MJCF."""
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
        """Fixe qpos selon theta, calcule la cinematique forward, retourne ee_pos."""
        self.data.qpos[: self.n_dof] = theta
        mujoco.mj_forward(self.model, self.data)
        return self.data.xpos[self.body_id].copy()

    def cycle(self, target: np.ndarray) -> dict:
        """Un cycle EFE : etat courant -> selection action -> execution -> apprentissage."""
        # 1. Etat courant
        theta_current = self.data.qpos[: self.n_dof].copy()

        # 2. Selection action via EFE (sample K + argmin sur model appris)
        theta_chosen, efe_predicted = self.policy.select_action(theta_current, target)

        # 3. Execution + perception
        p_observed = self.execute(theta_chosen)
        distance = float(np.linalg.norm(p_observed - target))

        # 4. Buffer experience
        self.buffer_theta.append(theta_chosen.copy())
        self.buffer_p.append(p_observed.copy())

        # 5. Apprentissage online (mini-batch SGD sur le buffer)
        if len(self.buffer_theta) >= 5:
            n_sample = min(self.batch_size, len(self.buffer_theta))
            idx = self._rng.choice(len(self.buffer_theta), size=n_sample, replace=False)
            thetas_batch = np.array([self.buffer_theta[i] for i in idx])
            p_batch = np.array([self.buffer_p[i] for i in idx])
            loss = self.gm.update_batch(
                thetas_batch, p_batch, n_steps=self.n_grad_steps_per_cycle
            )
        else:
            loss = 0.0

        return {
            "target": target.copy(),
            "theta_chosen": theta_chosen,
            "p_observed": p_observed,
            "distance": distance,
            "efe_predicted": efe_predicted,
            "buffer_size": len(self.buffer_theta),
            "loss": loss,
            "model_updates": self.gm.update_count,
        }
