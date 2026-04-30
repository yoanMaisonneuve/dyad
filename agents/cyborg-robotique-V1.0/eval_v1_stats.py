"""eval_v1_stats.py -- V1 (champ directionnel ordre 1) N=10 seeds.

Protocole alpha : cible aleatoire chaque cycle, 1 step par cible, 30 cycles.
Mesure mean(last 5) +/- std inter-run sur N=10 seeds.
"""
import os, sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
import mujoco
import numpy as np
from cerveau.agent_champ import CyborgChampAgent

MENAGERIE = os.path.join(SCRIPT_DIR, "external", "mujoco_menagerie")
CONFIGS = {
    "SO-100": {
        "scene": os.path.join(MENAGERIE, "trs_so_arm100", "scene.xml"),
        "ee": "Fixed_Jaw",
        "tip_pair": ("Fixed_Jaw", "Moving_Jaw"),
        "target_box": [(0.10, 0.30), (-0.20, 0.20), (0.05, 0.30)],
    },
    "Koch": {
        "scene": os.path.join(MENAGERIE, "low_cost_robot_arm", "scene.xml"),
        "ee": "gripper_static_finger",
        "tip_pair": ("gripper_static_finger", "gripper_moving_finger"),
        "target_box": [(0.05, 0.14), (-0.14, 0.14), (0.06, 0.20)],
    },
}
N_CYCLES = 30
SEEDS = list(range(42, 52))


def sample(rng, box):
    return np.array([rng.uniform(*box[0]), rng.uniform(*box[1]), rng.uniform(*box[2])])


def run_one(scene, ee, tip_pair, target_box, seed):
    model = mujoco.MjModel.from_xml_path(scene)
    data = mujoco.MjData(model)
    n_dof = min(5, model.nq)
    agent = CyborgChampAgent(
        model, data,
        end_effector_body=ee, n_dof=n_dof,
        exploration_delta=0.15, application_step=0.5,
        learning_rate_M=0.3, seed=seed, tip_pair=tip_pair,
    )
    rng = np.random.default_rng(seed)
    errors = []
    for c in range(N_CYCLES):
        target = sample(rng, target_box)
        r = agent.cycle(target)
        errors.append(r["distance"])
    return np.array(errors)


def main():
    print("=" * 78)
    print(" EVAL V1 (champ directionnel ordre 1) -- N=10 seeds x 2 bras")
    print(" Protocole alpha : 30 cycles, 1 step/cible (5 expl + 25 application)")
    print("=" * 78)
    summary = {}
    for bras_name, cfg in CONFIGS.items():
        print(f"\n--- {bras_name} ---")
        per_run_means_5 = []
        per_run_means_25 = []  # phase application moy
        for seed in SEEDS:
            errs = run_one(cfg["scene"], cfg["ee"], cfg["tip_pair"], cfg["target_box"], seed)
            mean_5 = float(np.mean(errs[-5:]))
            mean_app = float(np.mean(errs[5:]))  # phase application (apres 5 expl)
            per_run_means_5.append(mean_5)
            per_run_means_25.append(mean_app)
            print(f"  seed {seed}: mean(last 5) = {mean_5:.4f} m  mean(application 25) = {mean_app:.4f}")
        per_run_means_5 = np.array(per_run_means_5)
        per_run_means_25 = np.array(per_run_means_25)
        print(f"  >>> mean(last 5) inter-run        : {per_run_means_5.mean():.4f} +/- {per_run_means_5.std():.4f} m")
        print(f"  >>> mean(application 25) inter-run: {per_run_means_25.mean():.4f} +/- {per_run_means_25.std():.4f} m")
        print(f"  >>> min/max seed mean(l5)         : {per_run_means_5.min():.4f} / {per_run_means_5.max():.4f}")
        summary[bras_name] = (per_run_means_5.mean(), per_run_means_5.std())
    print()
    print("=" * 78)
    print(" RESUME V1 ordre 1 (N=10 seeds, mean +/- std last 5)")
    print("=" * 78)
    for b, (m, s) in summary.items():
        print(f"  {b:6s} : {m:.4f} +/- {s:.4f} m")
    print()
    print(" Comparaison bras-par-bras ALL N=10 :")
    print("  V1 ordre 1   ?")
    print("  V4 ADAPTIVE  : SO-100 0.159 +/- 0.121, Koch 0.144 +/- 0.051")
    print("  V6 ADAPTIVE+ : SO-100 0.067 +/- 0.023, Koch 0.082 +/- 0.031")
    print("  Baseline IK  : SO-100 0.222 (1 seed deterministe)")
    print("=" * 78)


if __name__ == "__main__":
    try:
        main()
    finally:
        sys.exit(0)
