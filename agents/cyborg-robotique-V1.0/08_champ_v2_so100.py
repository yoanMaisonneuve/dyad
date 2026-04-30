"""08_champ_v2_so100.py -- Champ V2 ordre 2 sur SO-ARM100 (test cross-bras)."""
import os, sys, time
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
import mujoco, mujoco.viewer
import numpy as np
from cerveau.agent_champ_v2 import CyborgChampV2Agent

SCENE = os.path.join(SCRIPT_DIR, "external", "mujoco_menagerie", "trs_so_arm100", "scene.xml")
N_CYCLES = 30


def sample_target(rng):
    return np.array([rng.uniform(0.10, 0.30), rng.uniform(-0.20, 0.20), rng.uniform(0.05, 0.30)])


def add_marker(viewer, pos):
    viewer.user_scn.ngeom = 0
    mujoco.mjv_initGeom(viewer.user_scn.geoms[0], type=mujoco.mjtGeom.mjGEOM_SPHERE,
        size=np.array([0.015, 0, 0]), pos=pos, mat=np.eye(3).flatten(),
        rgba=np.array([1.0, 0.2, 0.2, 0.9]))
    viewer.user_scn.ngeom = 1


def find_ee(model):
    for i in range(model.nbody):
        n = mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_BODY, i) or ""
        if any(k in n.lower() for k in ("jaw", "gripper", "ee")):
            return n
    return ""


def main():
    model = mujoco.MjModel.from_xml_path(SCENE)
    data = mujoco.MjData(model)
    ee = find_ee(model)
    print(f"SO-ARM100 EE: {ee}")
    agent = CyborgChampV2Agent(model, data, ee, n_dof=5,
        scales_exploration=(0.06, 0.12, 0.18), n_candidates_app=80,
        sampling_scale=0.20, seed=42)
    rng = np.random.default_rng(42)
    erreurs = []
    print("=" * 70)
    print(" CyborgV1.0 CHAMP V2 ORDRE 2 sur SO-ARM100")
    print("=" * 70)
    with mujoco.viewer.launch_passive(model, data) as viewer:
        for cycle in range(1, N_CYCLES + 1):
            if not viewer.is_running():
                break
            target = sample_target(rng)
            add_marker(viewer, target)
            r = agent.cycle(target)
            erreurs.append(r["distance"])
            mujoco.mj_forward(model, data)
            viewer.sync()
            print(f"C{cycle:3d} [{r['phase']:25s}] err={r['distance']:.4f} ||J||={r['J_norm']:.3f} ||H||={r['H_norm']:.3f}")
            time.sleep(0.6)
    print("=" * 70)
    print(" BILAN V4 sur SO-ARM100")
    print("=" * 70)
    n_explore = 5 * 3
    if len(erreurs) > n_explore:
        p2 = erreurs[n_explore:]
        print(f"  Phase explore        : {n_explore} cycles")
        print(f"  Phase application    : {len(p2)} cycles")
        print(f"  Erreur 1ere applic   : {p2[0]:.4f} m")
        print(f"  Erreur finale (moy 5): {np.mean(p2[-5:]):.4f} m")
        if p2[0] > 1e-6:
            red = (1.0 - np.mean(p2[-5:]) / p2[0]) * 100.0
            print(f"  Reduction phase appli: {red:+.1f}%")
    print()
    print(f"  Comparaison SO-ARM100 :")
    print(f"    [J+8]    Baseline + IK oracle    : 0.222 m")
    print(f"    [J+9 V2] Champ ordre 1 (V1)      : 0.144 m  (champion precedent)")
    if len(erreurs) >= 5:
        print(f"    [J+9 V4] Champ ordre 2 (J+H)     : {np.mean(erreurs[-5:]):.4f} m")
    print("=" * 70)


if __name__ == "__main__":
    try:
        main()
    finally:
        sys.exit(0)
