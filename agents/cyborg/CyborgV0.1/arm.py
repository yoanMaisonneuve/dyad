"""Cinematique du bras 2 articulations en 2D (forward kinematics exacte)."""
import numpy as np

L1 = 3.0  # epaule -> coude
L2 = 2.0  # coude -> end-effector

def forward(theta1, theta2):
    """Angles (rad) -> positions du coude et de l'effecteur (numpy arrays)."""
    elbow_x = L1 * np.cos(theta1)
    elbow_y = L1 * np.sin(theta1)
    end_x = elbow_x + L2 * np.cos(theta1 + theta2)
    end_y = elbow_y + L2 * np.sin(theta1 + theta2)
    return np.array([end_x, end_y]), np.array([elbow_x, elbow_y])
