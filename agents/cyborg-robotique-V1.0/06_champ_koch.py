"""06_champ_koch.py -- Test PORTABILITE du champ directionnel sur Koch arm.

S2 J+9 V3 -- demo portabilite multi-bras (objectif S3 du sprint).

Reutilise EXACTEMENT le meme cerveau que 05_champ_directionnel_3d.py
(cerveau/agent_champ.py + cerveau/champ_directionnel.py) sans aucune modification.
Seul le path MJCF change : SO-ARM100 -> Koch arm (low_cost_robot_arm de Alexander Koch).

Si l'algorithme converge aussi bien sur Koch que sur SO-100 :
  => DEMO PORTABILITE reussie
  => Le cerveau Print Your Own Optimus est independant du hardware specifique
  => Aligne avec la vision : "n'importe quel bras DIY + ce cerveau opensource"
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
KOCH_SCENE = os.path.join(MENAGERIE_PATH, "low_cost_robot_arm", "scene.xml")

N_CYCLES = 30
PAUSE_PER_CYCLE = 1.0


def sample_target_3d(rng) -> np.ndarray:
    # Bornes adaptees au workspace du Koch (similaire SO-100 mais a verifier)
    x = rng.uniform(0.05, 0.25)
    y = rng.uniform(-0.20, 0.20)
    z = rng.uniform(0.05, 0.25)
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
        if any(kw in name.lower() for kw in ("jaw", "gripper", "ee", "end_effector", "claw")):
            return name
    # Fallback : dernier body (souvent l'effecteur)
    last_name = mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_BODY, model.nbody - 1) or ""
    return last_name


def list_bodies(model: mujoco.MjModel):
    """Pour debug : liste tous les bodies."""
    print("Bodies dans le modele :")
    for i in range(model.nbody):
        name = mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_BODY, i)
        print(f"  {i:3d}: {name}")


def main():
    if not os.path.exists(KOCH_SCENE):
        print(f"ERREUR : {KOCH_SCENE} introuvable.")
        return

    print(f"Chargement Koch arm : {KOCH_SCENE}")
    model = mujoco.MjModel.from_xml_path(KOCH_SCENE)
    data = mujoco.MjData(model)

    print(f"Modele charge. nq={model.nq} (DoF), nu={model.nu} (actuateurs).")

    ee_body_name = find_end_effector_body(model)
    print(f"End-effector body detecte : {ee_body_name}")
    if not ee_body_name:
        list_bodies(model)
        return

    # Detection auto du n_dof (premier nq, en supposant pas de free joint)
    n_dof = min(5, model.nq)  # cap a 5 pour rester aligne SO-100
    print(f"n_dof utilise : {n_dof}")

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
    print(" CyborgV1.0 PORTABILITE -- meme cerveau, bras Koch (low_cost_robot_arm)")
    print(" Test : si convergence aussi bonne que SO-100, portabilite demontree")
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
            print(f"  ||M||           : {result['M_norm']:.4f}  ({result['n_obs']} obs)")
            if result['phase'] == "APPLICATION":
                print(f"  ||correction||  : {result['correction_norm']:.4f}")

            time.sleep(PAUSE_PER_CYCLE)

    print()
    print("=" * 78)
    print(" BILAN J+9 V3 - PORTABILITE (Koch arm vs SO-ARM100)")
    print("=" * 78)
    n = len(erreurs)
    print(f"  Cycles executes      : {n}")
    if n >= 1:
        print(f"  Erreur initiale      : {erreurs[0]:.4f} m")

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
    print(f"  Comparaison portabilite SO-ARM100 vs Koch arm (meme algo, meme seed) :")
    print(f"    [J+9 V2] SO-ARM100 champ directionnel : reduction +47.3%, finale 0.144 m")
    if n >= 5:
        moy = np.mean(erreurs[-5:])
        print(f"    [J+9 V3] Koch arm   champ directionnel : finale {moy:.4f} m")
    print()
    print(f"  Si Koch converge similairement => PORTABILITE DEMONTREE")
    print(f"  => Cerveau Print Your Own Optimus independant du hardware specifique")
    print("=" * 78)


if __name__ == "__main__":
    try:
        main()
    finally:
        sys.exit(0)
