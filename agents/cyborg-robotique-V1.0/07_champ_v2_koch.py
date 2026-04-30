"""07_champ_v2_koch.py -- Champ directionnel V2 (modele ordre 2) sur Koch arm.

Idee Yoan 2026-04-30 : 3 mouvements par DoF + integration vitesse + acceleration
des gradients. Mathematiquement : capture J (gradient) ET H_diag (Hessien) par DoF
via Taylor d'ordre 2.

Sur Koch arm V1 (06_champ_koch.py) : reduction -166.8% (instabilite, M trop petit).
Hypothese V2 : modele ordre 2 + sampling EFE = corrections moins explosives +
plus precis sur geometrie compacte du Koch.

Phase exploration : 5 DoF × 3 amplitudes = 15 cycles
Phase application : 15 cycles (16-30)
"""
import os
import sys
import time

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

import mujoco
import mujoco.viewer
import numpy as np

from cerveau.agent_champ_v2 import CyborgChampV2Agent

MENAGERIE_PATH = os.path.join(SCRIPT_DIR, "external", "mujoco_menagerie")
KOCH_SCENE = os.path.join(MENAGERIE_PATH, "low_cost_robot_arm", "scene.xml")

N_CYCLES = 30
PAUSE_PER_CYCLE = 0.8


def sample_target_3d(rng):
    x = rng.uniform(0.05, 0.25)
    y = rng.uniform(-0.20, 0.20)
    z = rng.uniform(0.05, 0.25)
    return np.array([x, y, z])


def add_target_marker(viewer, target_pos):
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


def find_end_effector_body(model):
    for i in range(model.nbody):
        name = mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_BODY, i) or ""
        if any(kw in name.lower() for kw in ("jaw", "gripper", "ee", "end_effector", "claw")):
            return name
    return mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_BODY, model.nbody - 1) or ""


def main():
    if not os.path.exists(KOCH_SCENE):
        print(f"ERREUR : {KOCH_SCENE} introuvable.")
        return

    print(f"Chargement Koch arm : {KOCH_SCENE}")
    model = mujoco.MjModel.from_xml_path(KOCH_SCENE)
    data = mujoco.MjData(model)

    ee_body_name = find_end_effector_body(model)
    print(f"End-effector body : {ee_body_name}")

    n_dof = min(5, model.nq)
    agent = CyborgChampV2Agent(
        model,
        data,
        end_effector_body=ee_body_name,
        n_dof=n_dof,
        scales_exploration=(0.06, 0.12, 0.18),  # 3 amplitudes croissantes
        n_candidates_app=80,
        sampling_scale=0.20,
        seed=42,
    )

    rng = np.random.default_rng(42)

    print()
    print("=" * 78)
    print(" CyborgV1.0 CHAMP V2 -- ordre 2 (J+H) + sampling EFE -- Koch arm")
    print(" Phase 1 (cycles 1-15) : exploration 3 amplitudes par DoF")
    print(" Phase 2 (cycles 16-30) : application via modele ordre 2 + sampling")
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
            print(f"--- Cycle {cycle:3d} [{result['phase']:25s}]")
            print(f"  Cible 3D        : ({target[0]:+.3f}, {target[1]:+.3f}, {target[2]:+.3f}) m")
            print(f"  EE atteint      : ({result['p_observed'][0]:+.3f}, {result['p_observed'][1]:+.3f}, {result['p_observed'][2]:+.3f}) m")
            print(f"  Erreur          : {result['distance']:.4f} m", end="")
            if cycle >= 5:
                print(f"   (moy 5 derniers : {np.mean(erreurs[-5:]):.4f})", end="")
            print()
            print(f"  ||J||={result['J_norm']:.4f}  ||H||={result['H_norm']:.4f}  ({result['n_obs']} obs)")

            time.sleep(PAUSE_PER_CYCLE)

    print()
    print("=" * 78)
    print(" BILAN J+9 V4 - CHAMP V2 ORDRE 2 sur KOCH")
    print("=" * 78)
    n = len(erreurs)
    n_explore = n_dof * 3
    print(f"  Cycles executes      : {n}")
    print(f"  Phase exploration    : {n_explore} cycles (3 amplitudes × {n_dof} DoF)")
    print(f"  Phase application    : {max(0, n - n_explore)} cycles")

    if n > n_explore:
        phase2 = erreurs[n_explore:]
        if phase2:
            print(f"  Erreur 1ere applic   : {phase2[0]:.4f} m")
            print(f"  Erreur finale (moy 5): {np.mean(phase2[-5:]):.4f} m")
            if phase2[0] > 1e-6:
                reduction = (1.0 - np.mean(phase2[-5:]) / phase2[0]) * 100.0
                print(f"  Reduction phase appli: {reduction:+.1f}%")

    print()
    print(f"  Comparaison sur KOCH (memes seeds) :")
    print(f"    [J+9 V3] Champ V1 ordre 1 (lineaire)  : finale 0.223 m, reduction -166.8% (instable)")
    if n >= 5:
        print(f"    [J+9 V4] Champ V2 ordre 2 (J+H)       : finale {np.mean(erreurs[-5:]):.4f} m")
    print("=" * 78)


if __name__ == "__main__":
    try:
        main()
    finally:
        sys.exit(0)
