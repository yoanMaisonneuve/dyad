"""Modele interne APPRIS de la cinematique du robot.

L'agent ne connait PAS la jacobienne MuJoCo. Il apprend forward(theta) -> p
par interaction avec l'environnement. C'est exactement "le code apprend son corps"
selon la definition de Yoan (vision Print Your Own Optimus).

MLP simple en numpy pur (zero dependance ajoutee) :
  Input  : theta ∈ R^n_dof  (config articulaire normalisee)
  Hidden : n_hidden unites, tanh
  Output : p ∈ R^n_obs  (position end-effector predite)

Optim : SGD avec mini-batch sur buffer d'experience.
"""
import numpy as np


class GenerativeModelAppris:
    """MLP simple qui apprend la cinematique forward du bras."""

    def __init__(
        self,
        n_dof: int = 5,
        n_obs: int = 3,
        n_hidden: int = 32,
        lr: float = 0.01,
        seed: int = 42,
    ):
        self.n_dof = n_dof
        self.n_obs = n_obs
        self.n_hidden = n_hidden
        self.lr = lr

        rng = np.random.default_rng(seed)
        # Init Xavier-ish (variance = 1/n_in)
        self.W1 = rng.normal(scale=1.0 / np.sqrt(n_dof), size=(n_hidden, n_dof))
        self.b1 = np.zeros(n_hidden)
        self.W2 = rng.normal(scale=1.0 / np.sqrt(n_hidden), size=(n_obs, n_hidden))
        self.b2 = np.zeros(n_obs)
        self.update_count = 0

    def forward(self, theta: np.ndarray) -> np.ndarray:
        """Predit la position EE depuis la config articulaire.

        Accepte theta de shape (n_dof,) OU (batch, n_dof) pour vectorisation.
        Retourne shape (n_obs,) OU (batch, n_obs).
        """
        if theta.ndim == 1:
            h = np.tanh(self.W1 @ theta + self.b1)
            return self.W2 @ h + self.b2
        else:
            h = np.tanh(theta @ self.W1.T + self.b1)
            return h @ self.W2.T + self.b2

    def _step(self, theta: np.ndarray, p_observe: np.ndarray) -> float:
        """Un pas de gradient sur une observation (theta, p). Retourne loss MSE."""
        # Forward
        z1 = self.W1 @ theta + self.b1
        h = np.tanh(z1)
        p_pred = self.W2 @ h + self.b2
        err = p_pred - p_observe
        loss = float(np.sum(err ** 2))

        # Backward (chain rule)
        dW2 = np.outer(err, h)
        db2 = err
        dh = self.W2.T @ err
        dz1 = dh * (1.0 - h ** 2)  # derivee tanh
        dW1 = np.outer(dz1, theta)
        db1 = dz1

        # Update
        self.W2 -= self.lr * dW2
        self.b2 -= self.lr * db2
        self.W1 -= self.lr * dW1
        self.b1 -= self.lr * db1
        self.update_count += 1
        return loss

    def update_batch(
        self, thetas: np.ndarray, p_observes: np.ndarray, n_steps: int = 5
    ) -> float:
        """Mini-batch SGD : n_steps passes sur le batch. Retourne loss moyenne finale."""
        losses = []
        for _ in range(n_steps):
            for i in range(len(thetas)):
                losses.append(self._step(thetas[i], p_observes[i]))
        return float(np.mean(losses[-len(thetas):])) if losses else 0.0
