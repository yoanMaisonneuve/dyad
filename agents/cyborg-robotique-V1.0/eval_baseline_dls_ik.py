"""eval_baseline_dls_ik.py -- Baseline DLS-IK Buss 2009 N=10 seeds sur 2 bras.

Meme protocole que eval_v6_stats.py (15 cibles x 8 steps multi-step) pour
comparaison fair V6 vs DLS-IK classique avec jacobienne MuJoCo connue.
"""
import os, sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
import mujoco
import numpy as np
from cerveau.baseline_dls_ik import BaselineDLSIK

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
N_TARGETS = 15
STEPS_PER_TARGET = 8
SEEDS = list(range(42, 52))


def sample(rng, box):
    return np.array([rng.uniform(*box[0]), rng.uniform(*box[1]), rng.uniform(*box[2])])


def run_one(scene, ee, tip_pair, target_box, seed):
    model = mujoco.MjModel.from_xml_path(scene)
    data = mujoco.MjData(model)
    n_dof = min(5, model.nq)
    agent = BaselineDLSIK(
        model, data, end_effector_body=ee, n_dof=n_dof,
        lambda_dls=0.05, step_size=0.5, tip_pair=tip_pair,
    )
    rng = np.random.default_rng(seed)
    final_errors = []
    for tg in range(N_TARGETS):
        target = sample(rng, target_box)
        last_err = None
        for s in range(STEPS_PER_TARGET):
            r = agent.step(target)
            last_err = r["distance"]
        final_errors.append(last_err)
    return np.array(final_errors)


def main():
    print("=" * 78)
    print(" EVAL BASELINE DLS-IK Buss 2009 -- N=10 seeds x 2 bras x 15 cibles x 8 steps")
    print(" Multi-step avec jacobienne MuJoCo exacte (oracle), DLS lambda=0.05")
    print(" Protocole identique a V6 pour comparaison fair")
    print("=" * 78)
    summary = {}
    for bras_name, cfg in CONFIGS.items():
        print(f"\n--- {bras_name} ---")
        per_run_means_5 = []
        per_run_means_all = []
        for seed in SEEDS:
            errs = run_one(cfg["scene"], cfg["ee"], cfg["tip_pair"], cfg["target_box"], seed)
            mean_5 = float(np.mean(errs[-5:]))
            mean_all = float(np.mean(errs))
            per_run_means_5.append(mean_5)
            per_run_means_all.append(mean_all)
            print(f"  seed {seed}: mean(last 5) = {mean_5:.4f} m  mean(all 15) = {mean_all:.4f}")
        per_run_means_5 = np.array(per_run_means_5)
        per_run_means_all = np.array(per_run_means_all)
        print(f"  >>> mean(last 5) inter-run : {per_run_means_5.mean():.4f} +/- {per_run_means_5.std():.4f} m")
        print(f"  >>> mean(all 15) inter-run : {per_run_means_all.mean():.4f} +/- {per_run_means_all.std():.4f} m")
        print(f"  >>> min/max seed mean(l5)  : {per_run_means_5.min():.4f} / {per_run_means_5.max():.4f}")
        summary[bras_name] = (per_run_means_5.mean(), per_run_means_5.std())
    print()
    print("=" * 78)
    print(" RESUME COMPARATIF V6 vs DLS-IK Buss")
    print("=" * 78)
    print("  V6 ADAPTIVE (warmup + DLS, J appris online) :")
    print("    SO-100 : 0.067 +/- 0.023 m")
    print("    Koch   : 0.082 +/- 0.031 m")
    print("  DLS-IK Buss 2009 (jacobienne MuJoCo exacte, J connu) :")
    for b, (m, s) in summary.items():
        print(f"    {b:6s} : {m:.4f} +/- {s:.4f} m")
    print()
    print("  Lecture : DLS-IK Buss = baseline AVEC oracle jacobienne, V6 = sans oracle")
    print("  Si V6 > DLS-IK Buss => agent autonome bat agent assiste")
    print("  Si DLS-IK Buss > V6 => oracle aide encore (attendu pour la litt)")
    print("=" * 78)


if __name__ == "__main__":
    try:
        main()
    finally:
        sys.exit(0)
