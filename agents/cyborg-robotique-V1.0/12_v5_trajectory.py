"""12 V5 trajectory tracking -- DLS + suivi 3D continu lineaire.

Usage : python 12_v5_trajectory.py [so100|koch]   (defaut: so100)
"""
import os, sys, time
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
import mujoco, mujoco.viewer
import numpy as np
from cerveau.agent_adaptive_v5 import CyborgAdaptiveV5

BRAS = sys.argv[1].lower() if len(sys.argv) > 1 else "so100"

if BRAS == "so100":
    SCENE = os.path.join(SCRIPT_DIR, "external", "mujoco_menagerie", "trs_so_arm100", "scene.xml")
    EE = "Fixed_Jaw"
    TIP = ("Fixed_Jaw", "Moving_Jaw")
elif BRAS == "koch":
    SCENE = os.path.join(SCRIPT_DIR, "external", "mujoco_menagerie", "low_cost_robot_arm", "scene.xml")
    EE = "gripper_static_finger"
    TIP = ("gripper_static_finger", "gripper_moving_finger")
else:
    print(f"Bras inconnu: {BRAS}. Utiliser so100 ou koch.")
    sys.exit(1)

N_STEPS = 40
STEP_3D = 0.012  # 1.2 cm par step en 3D


def marker(v, p):
    v.user_scn.ngeom = 0
    mujoco.mjv_initGeom(v.user_scn.geoms[0], type=mujoco.mjtGeom.mjGEOM_SPHERE,
        size=np.array([0.012, 0, 0]), pos=p, mat=np.eye(3).flatten(),
        rgba=np.array([1.0, 0.2, 0.2, 0.9]))
    v.user_scn.ngeom = 1


def main():
    model = mujoco.MjModel.from_xml_path(SCENE)
    data = mujoco.MjData(model)
    n_dof = min(5, model.nq)
    agent = CyborgAdaptiveV5(model, data, end_effector_body=EE, n_dof=n_dof,
        buffer_size=12, step_size=0.4, noise_scale=0.01,
        lambda_dls=0.05, tip_pair=TIP, seed=42)
    rng = np.random.default_rng(42)

    p_init = agent.execute(data.qpos[:n_dof].copy())
    # Direction = vers un point cible loin pour avoir long parcours
    p_dest = np.array([0.18, 0.05, 0.18])
    v = p_dest - p_init
    if np.linalg.norm(v) > 1e-6:
        v = v / np.linalg.norm(v)

    print(f"=" * 70)
    print(f" V5 TRAJECTORY -- DLS + suivi continu sur {BRAS.upper()}")
    print(f" p_init={p_init.round(3)}, direction v={v.round(3)}")
    print(f" {N_STEPS} steps x {STEP_3D*100:.1f} cm/step")
    print(f"=" * 70)

    errors = []
    with mujoco.viewer.launch_passive(model, data) as viewer:
        for t in range(N_STEPS):
            if not viewer.is_running():
                break
            target = p_init + v * (t * STEP_3D)
            marker(viewer, target)
            r = agent.step(target)
            errors.append(r["distance"])
            mujoco.mj_forward(model, data)
            viewer.sync()
            print(f"t{t:3d}: tgt=({target[0]:+.3f},{target[1]:+.3f},{target[2]:+.3f}) err={r['distance']:.4f} ||J||={r['J_norm']:.3f}")
            time.sleep(0.1)

    print(f"=" * 70)
    print(f" BILAN V5 trajectory tracking sur {BRAS.upper()}")
    print(f"=" * 70)
    if errors:
        print(f"  Erreur tracking moy globale  : {np.mean(errors):.4f} m")
        print(f"  Erreur tracking moy 10 derniers: {np.mean(errors[-10:]):.4f} m")
        print(f"  Erreur tracking max          : {max(errors):.4f} m")
    print()
    print(f"  Comparaison cibles ponctuelles V4 :")
    print(f"    SO-100 : 0.034 m  (5 dernieres)")
    print(f"    Koch   : 0.177 m  (5 dernieres)")
    print(f"=" * 70)


if __name__ == "__main__":
    try:
        main()
    finally:
        sys.exit(0)
