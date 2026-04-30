"""09 : V3 (corr itérative + régul H) sur SO-100. Doit >= V1 (0.144m)."""
import os, sys, time
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
import mujoco, mujoco.viewer
import numpy as np
from cerveau.agent_champ_v3 import CyborgChampV3Agent

SCENE = os.path.join(SCRIPT_DIR, "external", "mujoco_menagerie", "trs_so_arm100", "scene.xml")


def sample(rng):
    return np.array([rng.uniform(0.10, 0.30), rng.uniform(-0.20, 0.20), rng.uniform(0.05, 0.30)])


def marker(viewer, p):
    viewer.user_scn.ngeom = 0
    mujoco.mjv_initGeom(viewer.user_scn.geoms[0], type=mujoco.mjtGeom.mjGEOM_SPHERE,
        size=np.array([0.015, 0, 0]), pos=p, mat=np.eye(3).flatten(),
        rgba=np.array([1.0, 0.2, 0.2, 0.9]))
    viewer.user_scn.ngeom = 1


def find_ee(model):
    for i in range(model.nbody):
        n = mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_BODY, i) or ""
        if any(k in n.lower() for k in ("jaw", "gripper")):
            return n
    return ""


def main():
    model = mujoco.MjModel.from_xml_path(SCENE)
    data = mujoco.MjData(model)
    ee = find_ee(model)
    print(f"EE: {ee}")
    agent = CyborgChampV3Agent(model, data, ee, n_dof=5,
        scales_exploration=(0.06, 0.12, 0.18), application_step=0.5,
        h_relative_threshold=0.3, seed=42)
    rng = np.random.default_rng(42)
    err = []
    print("=" * 70)
    print(" V3 (corr iterative + regul H) sur SO-ARM100")
    print("=" * 70)
    with mujoco.viewer.launch_passive(model, data) as viewer:
        for cycle in range(1, 31):
            if not viewer.is_running():
                break
            t = sample(rng)
            marker(viewer, t)
            r = agent.cycle(t)
            err.append(r["distance"])
            mujoco.mj_forward(model, data)
            viewer.sync()
            print(f"C{cycle:3d} [{r['phase']:25s}] err={r['distance']:.4f} ||J||={r['J_norm']:.3f} ||H||={r['H_norm']:.3f} h_used={r['h_used']}")
            time.sleep(0.5)
    print("=" * 70)
    print(" BILAN V3 sur SO-ARM100")
    print("=" * 70)
    n_exp = 15
    if len(err) > n_exp:
        p2 = err[n_exp:]
        print(f"  Erreur 1ere applic   : {p2[0]:.4f} m")
        print(f"  Erreur finale (moy 5): {np.mean(p2[-5:]):.4f} m")
        if p2[0] > 1e-6:
            red = (1.0 - np.mean(p2[-5:]) / p2[0]) * 100.0
            print(f"  Reduction phase appli: {red:+.1f}%")
    print()
    print(f"  Comparaison SO-ARM100 :")
    print(f"    [J+9 V1] Champ ordre 1        : 0.144 m  (champion precedent)")
    print(f"    [J+9 V2] Champ ordre 2 sample : 0.267 m  (echec)")
    if len(err) >= 5:
        print(f"    [J+10 V3] Corr iter + regul H : {np.mean(err[-5:]):.4f} m")
    print(f"  Si V3 <= V1 (0.144m) => theorie Yoan validee (regul H + iter resout overfit)")
    print("=" * 70)


if __name__ == "__main__":
    try:
        main()
    finally:
        sys.exit(0)
