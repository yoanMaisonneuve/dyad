"""IK iteratif 3D via descente de gradient sur la jacobienne MuJoCo.

Equivalent de iterative_ik() de CyborgV0.1 mais 3D + jacobienne MuJoCo (mj_jacBody).
Sert d'oracle local pour generer le signal d'apprentissage du modele baseline.

Note : ce n'est PAS de l'inference active pure - c'est un raccourci pratique pour
la baseline. La vraie politique AIF (S2 J+9-10) minimisera directement l'EFE
sans passer par cet oracle.
"""
import mujoco
import numpy as np


def iterative_ik_mujoco(
    model: mujoco.MjModel,
    data: mujoco.MjData,
    target_pos: np.ndarray,
    end_effector_body_id: int,
    theta_init: np.ndarray,
    n_dof: int,
    max_iter: int = 100,
    lr: float = 0.5,
    tol: float = 0.005,
) -> np.ndarray:
    """Descente de gradient sur ||ee_pos(theta) - target||^2 via jacobienne MuJoCo.

    Args:
        model: MjModel charge.
        data: MjData (sera modifie pour les forward kinematics).
        target_pos: position cible 3D (3,).
        end_effector_body_id: id du body end-effector (via mj_name2id).
        theta_init: angles initiaux (n_dof,).
        n_dof: nombre d'articulations a optimiser.
        max_iter, lr, tol: hyperparams descente de gradient.

    Returns:
        theta_optimal (n_dof,) approchant target_pos.
    """
    theta = theta_init.copy()
    jacp = np.zeros((3, model.nv))
    jacr = np.zeros((3, model.nv))

    for _ in range(max_iter):
        data.qpos[:n_dof] = theta
        mujoco.mj_forward(model, data)
        ee_pos = data.xpos[end_effector_body_id].copy()
        err = ee_pos - target_pos
        if np.linalg.norm(err) < tol:
            break
        mujoco.mj_jacBody(model, data, jacp, jacr, end_effector_body_id)
        J = jacp[:, :n_dof]
        grad = J.T @ err
        theta = theta - lr * grad
    return theta
