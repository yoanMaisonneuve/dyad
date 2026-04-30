"""03_aif_baseline_3d.py -- Test baseline AIF lineaire 3D sur SO-ARM100.

Adaptation 3D du CyborgV0.1 (bras 2D). Le bras apprend a atteindre des cibles 3D
aleatoires via mapping lineaire theta = W*target + b ajuste par IK oracle.

Lance le viewer + 30 cycles. Cible visualisee comme sphere rouge dans la scene.
Affiche metriques CLI a chaque cycle (distance, ||dW||, ||db||).

Cette version est une BASELINE - mapping lineaire + IK oracle, pas pure AIF.
La vraie politique AIF (EFE minimization sans oracle) viendra en S2 J+9-10.
"""
import os
import sys
import time

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

import mujoco
import mujoco.viewer
import numpy as np

from cerveau.agent import CyborgAgent

MENAGERIE_PATH = os.path.join(SCRIPT_DIR, "external", "mujoco_menagerie")
SO100_SCENE = os.path.join(MENAGERIE_PATH, "trs_so_arm100", "scene.xml")

N_CYCLES = 30
PAUSE_PER_CYCLE = 1.2  # secondes pour voir chaque cible/exec


def sample_target_3d(rng) -> np.ndarray:
    """Cible aleatoire dans une boite atteignable autour du bras SO-ARM100."""
    x = rng.uniform(0.10, 0.30)
    y = rng.uniform(-0.20, 0.20)
    z = rng.uniform(0.05, 0.30)
    return np.array([x, y, z])


def add_target_marker(viewer, target_pos: np.ndarray):
    """Ajoute une sphere rouge a target_pos dans le viewer (visualisation runtime)."""
    viewer.user_scn.ngeom = 0
    mujoco.mjv_initGeom(
        viewer.user_scn.geoms[0],
        type=mujoco.mjtGeom.mjGEOM_SPHERE,
        size=np.array([0.015, 0.0, 0.0]),
        pos=target_pos,
        mat=np.eye(3).flatten(),
        rgba=np.array([1.0, 0.2, 0.2, 0.9]),
    )
    viewer.user_scn.ngeom = 1


def find_end_effector_body(model: mujoco.MjModel) -> str:
    """Trouve un body end-effector (cherche 'Jaw' ou 'Moving_Jaw' ou 'gripper')."""
    candidates = []
    for i in range(model.nbody):
        name = mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_BODY, i) or ""
        if any(kw in name.lower() for kw in ("jaw", "gripper", "ee", "end_effector")):
            candidates.append(name)
    if not candidates:
        return ""
    return candidates[0]


def main():
    if not os.path.exists(SO100_SCENE):
        print(f"ERREUR : {SO100_SCENE} introuvable.")
        print("Etape manquante : git clone --depth=1 https://github.com/google-deepmind/mujoco_menagerie.git external/mujoco_menagerie")
        return

    print(f"Chargement SO-ARM100 : {SO100_SCENE}")
    model = mujoco.MjModel.from_xml_path(SO100_SCENE)
    data = mujoco.MjData(model)

    ee_body_name = find_end_effector_body(model)
    if not ee_body_name:
        print("ERREUR : impossible de trouver le body end-effector.")
        print("Bodies disponibles :")
        for i in range(model.nbody):
            print(f"  - {mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_BODY, i)}")
        return
    print(f"End-effector body detecte : {ee_body_name}")

    n_dof = 5  # 5 articulations effectives (sans le gripper Jaw)
    agent = CyborgAgent(model, data, end_effector_body=ee_body_name, n_dof=n_dof)
    rng = np.random.default_rng(42)

    print()
    print("=" * 70)
    print(" CyborgV1.0 BASELINE -- bras 5 DoF + AIF lineaire (port CyborgV0.1 3D)")
    print(" Cible rouge dans la scene. Le bras apprend a la viser cycle apres cycle.")
    print("=" * 70)

    erreurs = []

    with mujoco.viewer.launch_passive(model, data) as viewer:
        for cycle in range(1, N_CYCLES + 1):
            if not viewer.is_running():
                print("\nViewer ferme par l'utilisateur.")
                break

            target = sample_target_3d(rng)
            add_target_marker(viewer, target)

            result = agent.cycle(target)
            erreurs.append(result["distance"])

            mujoco.mj_forward(model, data)
            viewer.sync()

            print()
            print(f"--- Cycle {cycle:3d} " + "-" * 50)
            print(f"  Cible 3D        : ({target[0]:+.3f}, {target[1]:+.3f}, {target[2]:+.3f}) m")
            print(f"  EE atteint      : ({result['ee_pos'][0]:+.3f}, {result['ee_pos'][1]:+.3f}, {result['ee_pos'][2]:+.3f}) m")
            print(f"  Erreur          : {result['distance']:.4f} m", end="")
            if cycle >= 5:
                print(f"   (moy 5 derniers : {np.mean(erreurs[-5:]):.4f})", end="")
            print()
            print(f"  MODELE update   : ||dW||={result['dW_norm']:.5f}  ||db||={result['db_norm']:.5f}")

            time.sleep(PAUSE_PER_CYCLE)

    print()
    print("=" * 70)
    print(" BILAN")
    print("=" * 70)
    n = len(erreurs)
    print(f"  Cycles executes      : {n}")
    if n >= 1:
        print(f"  Erreur initiale      : {erreurs[0]:.4f} m")
    if n >= 5:
        moy_finale = np.mean(erreurs[-5:])
        print(f"  Erreur finale (moy 5): {moy_finale:.4f} m")
        if erreurs[0] > 1e-6:
            reduction = (1.0 - moy_finale / erreurs[0]) * 100.0
            print(f"  Reduction            : {reduction:+.1f}%")
    print("=" * 70)


if __name__ == "__main__":
    main()
