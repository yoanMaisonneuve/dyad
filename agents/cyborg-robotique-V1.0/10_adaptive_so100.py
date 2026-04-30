"""10 V4 ADAPTIVE multi-step sur SO-ARM100."""
import os, sys, time
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
import mujoco, mujoco.viewer
import numpy as np
from cerveau.agent_adaptive import CyborgAdaptiveAgent

SCENE = os.path.join(SCRIPT_DIR, "external", "mujoco_menagerie", "trs_so_arm100", "scene.xml")
N_TARGETS = 15
STEPS_PER_TARGET = 8


def sample(rng):
    return np.array([rng.uniform(0.10, 0.30), rng.uniform(-0.20, 0.20), rng.uniform(0.05, 0.30)])


def marker(v, p):
    v.user_scn.ngeom = 0
    mujoco.mjv_initGeom(v.user_scn.geoms[0], type=mujoco.mjtGeom.mjGEOM_SPHERE,
        size=np.array([0.015, 0, 0]), pos=p, mat=np.eye(3).flatten(),
        rgba=np.array([1.0, 0.2, 0.2, 0.9]))
    v.user_scn.ngeom = 1


def main():
    model = mujoco.MjModel.from_xml_path(SCENE)
    data = mujoco.MjData(model)
    agent = CyborgAdaptiveAgent(model, data, end_effector_body="Fixed_Jaw", n_dof=5,
        buffer_size=12, step_size=0.4, noise_scale=0.02,
        tip_pair=("Fixed_Jaw", "Moving_Jaw"), seed=42)
    rng = np.random.default_rng(42)
    final_errors = []
    print("=" * 70)
    print(f" V4 ADAPTIVE -- {N_TARGETS} cibles x {STEPS_PER_TARGET} steps SO-ARM100")
    print("=" * 70)
    with mujoco.viewer.launch_passive(model, data) as viewer:
        for tg in range(1, N_TARGETS + 1):
            if not viewer.is_running():
                break
            target = sample(rng)
            marker(viewer, target)
            errs = []
            r = None
            for s in range(STEPS_PER_TARGET):
                if not viewer.is_running():
                    break
                r = agent.step(target)
                errs.append(r["distance"])
                mujoco.mj_forward(model, data)
                viewer.sync()
                time.sleep(0.12)
            final_errors.append(errs[-1] if errs else 999.0)
            jn = r["J_norm"] if r else 0.0
            bs = r["buffer_size"] if r else 0
            print(f"C{tg:3d}: init={errs[0]:.3f} -> final={errs[-1]:.4f} m  ||J||={jn:.3f} buf={bs}")
    print("=" * 70)
    if final_errors:
        print(f" Final moyenne globale          : {np.mean(final_errors):.4f} m")
        print(f" Final moyenne 5 dernieres cible: {np.mean(final_errors[-5:]):.4f} m")
        print(f" Comparaison V1 (1 step/cible)  : 0.144 m")
        print(f" Si V4 < V1 => ADAPTIVE + multi-step + cross-terms cap = WIN")
    print("=" * 70)


if __name__ == "__main__":
    try:
        main()
    finally:
        sys.exit(0)
