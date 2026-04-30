"""11 V4 ADAPTIVE multi-step sur Koch arm (test portabilite)."""
import os, sys, time
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
import mujoco, mujoco.viewer
import numpy as np
from cerveau.agent_adaptive import CyborgAdaptiveAgent

SCENE = os.path.join(SCRIPT_DIR, "external", "mujoco_menagerie", "low_cost_robot_arm", "scene.xml")
N_TARGETS = 15
STEPS_PER_TARGET = 8


def sample(rng):
    # Workspace ADAPTE au reach reel du Koch (mesure empirique : reach max 0.318m)
    return np.array([rng.uniform(0.05, 0.14), rng.uniform(-0.14, 0.14), rng.uniform(0.06, 0.20)])


def marker(v, p):
    v.user_scn.ngeom = 0
    mujoco.mjv_initGeom(v.user_scn.geoms[0], type=mujoco.mjtGeom.mjGEOM_SPHERE,
        size=np.array([0.015, 0, 0]), pos=p, mat=np.eye(3).flatten(),
        rgba=np.array([1.0, 0.2, 0.2, 0.9]))
    v.user_scn.ngeom = 1


def find_ee_and_pair(model):
    """Trouve un body EE + paire (static, moving) finger pour le tip Koch."""
    static_id, moving_id = -1, -1
    for i in range(model.nbody):
        n = (mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_BODY, i) or "").lower()
        if "static" in n and "finger" in n:
            static_id = i
        elif "moving" in n and "finger" in n:
            moving_id = i
    if static_id >= 0 and moving_id >= 0:
        a = mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_BODY, static_id)
        b = mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_BODY, moving_id)
        return a, (a, b)
    # Fallback : pas de paire trouvée, utilise le dernier body
    return mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_BODY, model.nbody - 1) or "", None


def main():
    model = mujoco.MjModel.from_xml_path(SCENE)
    data = mujoco.MjData(model)
    ee_name, pair = find_ee_and_pair(model)
    print(f"EE: {ee_name}, tip pair: {pair}")
    n_dof = min(5, model.nq)

    agent = CyborgAdaptiveAgent(model, data, end_effector_body=ee_name, n_dof=n_dof,
        buffer_size=12, step_size=0.4, noise_scale=0.02,
        tip_pair=pair, seed=42)
    rng = np.random.default_rng(42)
    final_errors = []
    print("=" * 70)
    print(f" V4 ADAPTIVE -- {N_TARGETS} cibles x {STEPS_PER_TARGET} steps Koch arm")
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
        print(f" Comparaison V4 sur SO-100      : 0.034 m (5 dernieres)")
        print(f" Si V4 Koch ~ V4 SO-100 => PORTABILITE TOTALE V4")
    print("=" * 70)


if __name__ == "__main__":
    try:
        main()
    finally:
        sys.exit(0)
