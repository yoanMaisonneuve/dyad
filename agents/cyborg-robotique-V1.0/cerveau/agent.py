"""Agent Cyborg V1.0 : boucle perception-action sur bras MuJoCo.

Implemente le cycle d'inference active baseline (CyborgV0.1 porte en 3D) :
  MODELE -> PREDICTION -> EXECUTION -> PERCEPTION -> ERREUR -> ajuste MODELE

Pour S2 J+8 : version baseline avec mapping lineaire + IK oracle.
Pour S2 J+9-10 : remplacer par vrai AIF avec EFE minimization.
"""
import mujoco
import numpy as np

from cerveau.ik_oracle import iterative_ik_mujoco
from cerveau.model_lineaire import ModeleLineaire


class CyborgAgent:
    """Agent qui apprend a controler un bras MuJoCo via inference active baseline."""

    def __init__(
        self,
        model: mujoco.MjModel,
        data: mujoco.MjData,
        end_effector_body: str,
        n_dof: int = 5,
        learning_rate: float = 0.05,
    ):
        self.model = model
        self.data = data
        self.end_effector_body = end_effector_body
        self.n_dof = n_dof

        self.body_id = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, end_effector_body)
        if self.body_id == -1:
            raise ValueError(f"Body '{end_effector_body}' introuvable dans le modele MuJoCo.")

        self.modele = ModeleLineaire(n_dof=n_dof, n_target=3, lr=learning_rate)

    def executer(self, theta: np.ndarray) -> np.ndarray:
        """Fixe qpos selon theta, calcule la cinematique forward, retourne ee_pos."""
        self.data.qpos[:self.n_dof] = theta
        mujoco.mj_forward(self.model, self.data)
        return self.data.xpos[self.body_id].copy()

    def cycle(self, target: np.ndarray) -> dict:
        """Un cycle complet : predire -> executer -> percevoir -> apprendre.

        Returns:
            dict avec target, theta_predit, ee_pos, distance, theta_optimal, dW_norm, db_norm.
        """
        # 1. PREDICTION : modele propose des angles
        theta_predit = self.modele.predire(target)

        # 2. EXECUTION + PERCEPTION : bras execute, on observe la position atteinte
        ee_pos = self.executer(theta_predit)
        distance = float(np.linalg.norm(ee_pos - target))

        # 3. ORACLE LOCAL : trouve les "vrais" angles pour cette cible (signal apprentissage)
        theta_optimal = iterative_ik_mujoco(
            self.model, self.data, target, self.body_id, theta_predit, self.n_dof
        )

        # 4. APPRENTISSAGE : ajuste W et b pour reduire l'erreur
        dW_norm, db_norm = self.modele.apprendre(target, theta_optimal)

        # 5. Repositionne le bras a la prediction (pour visualisation viewer)
        self.executer(theta_predit)

        return {
            "target": target.copy(),
            "theta_predit": theta_predit.copy(),
            "ee_pos": ee_pos,
            "distance": distance,
            "theta_optimal": theta_optimal,
            "dW_norm": dW_norm,
            "db_norm": db_norm,
        }
