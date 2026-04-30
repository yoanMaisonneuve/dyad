"""05_champ_directionnel_3d.py -- Approche matchllm : champ directionnel local.

J+9 V2 -- approche tranchee par Yoan 2026-04-30 ~03h apres echec MLP.

Au lieu d'apprendre la cinematique f(theta) -> p globalement (MLP J+9 V1
qui n'a pas converge), on apprend la matrice M telle que Delta_p = M · Delta_theta
localement. C'est le "champ directionnel" du lineage matchllm.

Algo en 2 phases :
  PHASE 1 (cycles 1-5) : EXPLORATION canonique - varie 1 joint a la fois,
                         identifie M par moindres carres.
  PHASE 2 (cycles 6-30) : APPLICATION - Delta_theta = M^+ · (p* - p_observe).

Aucun acces a la jacobienne MuJoCo. L'agent apprend M par interaction (n_dof+1
essais theoriquement suffisants vs 30 pour MLP qui n'a pas converge).
"""
import os
import sys
import time

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

import mujoco
import mujoco.viewer
import numpy as np

from cerveau.agent_champ import CyborgChampAgent

MENAGERIE_PATH = os.path.join(SCRIPT_DIR, "external", "mujoco_menagerie")
SO100_SCENE = os.path.join(MENAGERIE_PATH, "trs_so_arm100", "scene.xml")

N_CYCLES = 30
PAUSE_PER_CYCLE = 1.0


def sample_target_3d(rng) -> np.ndarray:
    x = rng.uniform(0.10, 0.30)
    y = rng.uniform(-0.20, 0.20)
    z = rng.uniform(0.05, 0.30)
    return np.array([x, y, z])


def add_target_marker(viewer, target_pos: np.ndarray):
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
    for i in range(model.nbody):
        name = mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_BODY, i) or ""
        if any(kw in name.lower() for kw in ("jaw", "gripper", "ee", "end_effector")):
            return name
    return ""


def main():
    if not os.path.exists(SO100_SCENE):
        print(f"ERREUR : {SO100_SCENE} introuvable.")
        return

    print(f"Chargement SO-ARM100 : {SO100_SCENE}")
    model = mujoco.MjModel.from_xml_path(SO100_SCENE)
    data = mujoco.MjData(model)

    ee_body_name = find_end_effector_body(model)
    if not ee_body_name:
        print("ERREUR : impossible de trouver le body end-effector.")
        return
    print(f"End-effector body : {ee_body_name}")

    n_dof = 5
    agent = CyborgChampAgent(
        model,
        data,
        end_effector_body=ee_body_name,
        n_dof=n_dof,
        exploration_delta=0.15,
        application_step=0.5,
        learning_rate_M=0.3,
        seed=42,
    )

    rng = np.random.default_rng(42)

    print()
    print("=" * 78)
    print(" CyborgV1.0 CHAMP DIRECTIONNEL -- approche matchllm portee robotique")
    print(" Phase 1 (cycles 1-5) : exploration canonique 1 joint a la fois")
    print(" Phase 2 (cycles 6-30) : application M^+ . erreur")
    print("=" * 78)

    erreurs = []

    with mujoco.viewer.launch_passive(model, data) as viewer:
        for cycle in range(1, N_CYCLES + 1):
            if not viewer.is_running():
                break

            target = sample_target_3d(rng)
            add_target_marker(viewer, target)

            result = agent.cycle(target)
            erreurs.append(result["distance"])

            mujoco.mj_forward(model, data)
            viewer.sync()

            print()
            print(f"--- Cycle {cycle:3d} [{result['phase']:25s}] " + "-" * 30)
            print(f"  Cible 3D        : ({target[0]:+.3f}, {target[1]:+.3f}, {target[2]:+.3f}) m")
            print(f"  EE atteint      : ({result['p_observed'][0]:+.3f}, {result['p_observed'][1]:+.3f}, {result['p_observed'][2]:+.3f}) m")
            print(f"  Erreur          : {result['distance']:.4f} m", end="")
            if cycle >= 5:
                print(f"   (moy 5 derniers : {np.mean(erreurs[-5:]):.4f})", end="")
            print()
            print(f"  ||M||           : {result['M_norm']:.4f}  ({result['n_obs']} observations)")
            if result['phase'] == "APPLICATION":
                print(f"  ||correction||  : {result['correction_norm']:.4f}")

            time.sleep(PAUSE_PER_CYCLE)

    print()
    print("=" * 78)
    print(" BILAN J+9 V2 - CHAMP DIRECTIONNEL (matchllm)")
    print("=" * 78)
    n = len(erreurs)
    print(f"  Cycles executes      : {n}")
    if n >= 1:
        print(f"  Erreur initiale      : {erreurs[0]:.4f} m")

    # Phase 2 metrics (post-exploration)
    if n > n_dof:
        phase2_erreurs = erreurs[n_dof:]
        print(f"  Phase exploration    : {n_dof} cycles")
        print(f"  Phase application    : {n - n_dof} cycles")
        if phase2_erreurs:
            print(f"  Erreur 1ere applic   : {phase2_erreurs[0]:.4f} m")
            print(f"  Erreur finale (moy 5): {np.mean(phase2_erreurs[-5:]):.4f} m")
            if phase2_erreurs[0] > 1e-6:
                reduction = (1.0 - np.mean(phase2_erreurs[-5:]) / phase2_erreurs[0]) * 100.0
                print(f"  Reduction phase appli: {reduction:+.1f}%")

    print()
    print(f"  Comparaison 3 algos sur SO-ARM100 (memes seeds, protocole alpha) :")
    print(f"    [J+8] Baseline lineaire + IK oracle  : reduction +53.6%, finale 0.222 m")
    print(f"    [J+9 V1] EFE + MLP appris            : reduction +7.9%,  finale 0.401 m  (echec)")
    if n >= 5:
        moy_globale = np.mean(erreurs[-5:])
        print(f"    [J+9 V2] Champ directionnel matchllm : finale {moy_globale:.4f} m")
    print("=" * 78)


if __name__ == "__main__":
    try:
        main()
    finally:
        sys.exit(0)
