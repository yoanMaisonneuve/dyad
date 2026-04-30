"""Modele interne du Cyborg : mapping target -> angles, ajuste par inference active."""
import numpy as np
from datetime import datetime

L1 = 3.0
L2 = 2.0


def _forward(theta1, theta2):
    x = L1 * np.cos(theta1) + L2 * np.cos(theta1 + theta2)
    y = L1 * np.sin(theta1) + L2 * np.sin(theta1 + theta2)
    return np.array([x, y])


def iterative_ik(target, theta0, max_iter=80, lr=0.05):
    """IK par descente de gradient sur la perte ||pos - target||^2.
    Utilisee comme 'verite locale' pour generer le signal d'apprentissage du modele lineaire global.
    """
    theta = theta0.copy().astype(float)
    for _ in range(max_iter):
        pos = _forward(theta[0], theta[1])
        err = pos - target
        if np.linalg.norm(err) < 0.005:
            break
        # Jacobien analytique 2x2
        s1 = np.sin(theta[0])
        c1 = np.cos(theta[0])
        s12 = np.sin(theta[0] + theta[1])
        c12 = np.cos(theta[0] + theta[1])
        J = np.array([
            [-L1 * s1 - L2 * s12, -L2 * s12],
            [ L1 * c1 + L2 * c12,  L2 * c12],
        ])
        grad = J.T @ err
        theta = theta - lr * grad
    return theta


class Modele:
    """Modele interne : approximation lineaire de l'inverse kinematics.
    Commence grossier, apprend par regression sur les exemples (target, theta_optimal)
    generes par IK iterative depuis la prediction courante.
    """

    def __init__(self):
        self.W = np.array([[0.20, 0.10], [-0.10, 0.20]])
        self.b = np.array([0.50, 0.30])
        self.lr = 0.10
        self.cycle_count = 0

    def predire(self, target):
        return self.W @ target + self.b

    def apprendre(self, target, theta_predit):
        """Trouve les meilleurs angles pour cette cible (oracle local par IK iterative),
        puis pousse W et b dans la direction qui aurait donne ce resultat.
        Retourne les normes des deltas pour le log."""
        theta_optimal = iterative_ik(target, theta_predit)
        erreur_angles = theta_optimal - (self.W @ target + self.b)
        delta_W = self.lr * np.outer(erreur_angles, target)
        delta_b = self.lr * erreur_angles
        self.W = self.W + delta_W
        self.b = self.b + delta_b
        self.cycle_count += 1
        return float(np.linalg.norm(delta_W)), float(np.linalg.norm(delta_b))

    def dump_modele(self, path):
        content = (
            "# Modele interne -- CyborgV0.1\n"
            f"**Derniere mise a jour :** {datetime.now().isoformat(timespec='seconds')}\n"
            f"**Cycles d'apprentissage :** {self.cycle_count}\n\n"
            "## Architecture cognitive\n"
            "Modele interne du cyborg = mapping lineaire `theta = W*target + b` qui predit les angles articulaires "
            "(theta1, theta2) a partir d'une cible (x, y). Ajuste par minimisation de l'erreur de prediction (Friston).\n\n"
            "## Parametres appris\n"
            "**W (matrice 2x2) :**\n"
            "```\n"
            f"[[{self.W[0,0]:+.4f}, {self.W[0,1]:+.4f}],\n"
            f" [{self.W[1,0]:+.4f}, {self.W[1,1]:+.4f}]]\n"
            "```\n\n"
            "**b (biais 2) :**\n"
            "```\n"
            f"[{self.b[0]:+.4f}, {self.b[1]:+.4f}]\n"
            "```\n\n"
            "## Constantes du bras (modele physique)\n"
            f"- L1 (epaule-coude) = {L1}\n"
            f"- L2 (coude-effecteur) = {L2}\n"
            "- Espace atteignable : couronne de rayons 1.0 a 5.0 dans le demi-plan superieur\n\n"
            "## Mission\n"
            "Apprendre a predire des angles qui amenent l'effecteur a une cible donnee, "
            "avec le moins d'erreur possible, en partant d'une initialisation volontairement mauvaise. "
            "Demontre empiriquement le cycle d'inference active de Friston/Clark sur un cas jouet "
            "de controle moteur -- premier pas vers la robotique humanoide manufacturiere et alimentaire.\n\n"
            "## Lien theorique\n"
            "Cf. `Blueprint-memory/workflow/INFERENCE-ACTIVE-RECHERCHE.md` -- premier livrable empirique repondant a Q1.\n"
        )
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
