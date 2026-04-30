"""Politique d'inference active : selection d'action par minimisation EFE.

Version J+9 (simple) :
  - EFE pragmatic only (squared distance a la cible) - pas d'epistemic value (J+10)
  - Horizon = 1 pas (J+10 etendra a horizon multi-pas)
  - Sampling : K perturbations candidates autour de theta courant
  - Selection : argmin EFE sur les candidates

Difference clef avec baseline :
  - Baseline : IK iteratif global via jacobienne MuJoCo (oracle externe)
  - EFE : sample + selection via le generative_model APPRIS de l'agent
    => l'agent n'a aucun acces a la jacobienne MuJoCo. Il decide avec son
       propre modele interne (qui apprend par interaction).
"""
import numpy as np

from cerveau.generative_model_appris import GenerativeModelAppris


class EFEPolicy:
    """Politique de selection d'action par minimisation Expected Free Energy."""

    def __init__(
        self,
        generative_model: GenerativeModelAppris,
        n_dof: int = 5,
        joint_limits: tuple | None = None,
        n_candidates: int = 30,
        scale: float = 0.15,
        seed: int = 43,
    ):
        self.gm = generative_model
        self.n_dof = n_dof
        self.joint_limits = joint_limits
        self.n_candidates = n_candidates
        self.scale = scale
        self.rng = np.random.default_rng(seed)

    def select_action(
        self, theta_current: np.ndarray, target: np.ndarray
    ) -> tuple[np.ndarray, float]:
        """Sample K candidates, calcule EFE pragmatic, retourne (theta_chosen, efe_min).

        EFE pragmatic = || p_pred(theta_candidate) - target ||^2
        avec p_pred = generative_model.forward(theta_candidate)  (modele appris).
        """
        # Sample K perturbations gaussiennes
        deltas = self.rng.normal(scale=self.scale, size=(self.n_candidates, self.n_dof))
        candidates = theta_current[None, :] + deltas

        # Clip aux limites articulaires
        if self.joint_limits is not None:
            low, high = self.joint_limits
            candidates = np.clip(candidates, low, high)

        # Predire EE position pour chaque candidate via le model APPRIS (vectorise)
        p_preds = self.gm.forward(candidates)  # shape (K, 3)

        # EFE pragmatic = squared distance to target
        efe = np.sum((p_preds - target[None, :]) ** 2, axis=1)

        idx_best = int(np.argmin(efe))
        return candidates[idx_best].copy(), float(efe[idx_best])
