"""eval_v4_stats.py -- Evaluation statistique V4 ADAPTIVE.

3 runs (seeds 42/43/44) x 2 bras (SO-100 + Koch workspace adapte) x 15 cibles x 8 steps.
Report mean ± std intra-run (variance sur les 15 cibles) et inter-run (variance sur 3 runs).

HEADLESS (pas de viewer) -> rapide, focus stats.
"""
import os, sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
import mujoco
import numpy as np
from cerveau.agent_adaptive import CyborgAdaptiveAgent

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
        "target_box": [(0.05, 0.14), (-0.14, 0.14), (0.06, 0.20)],  # workspace adapte
    },
}

N_TARGETS = 15
STEPS_PER_TARGET = 8
SEEDS = list(range(42, 52))  # 10 seeds (42-51) pour vraie distribution


def sample_target(rng, box):
    return np.array([rng.uniform(*box[0]), rng.uniform(*box[1]), rng.uniform(*box[2])])


def run_one(scene, ee, tip_pair, target_box, seed, return_detail=False):
    """Un run : 15 cibles x 8 steps. Retourne final_errors (15,) et eventuellement detail."""
    model = mujoco.MjModel.from_xml_path(scene)
    data = mujoco.MjData(model)
    n_dof = min(5, model.nq)
    agent = CyborgAdaptiveAgent(
        model, data, end_effector_body=ee, n_dof=n_dof,
        buffer_size=12, step_size=0.4, noise_scale=0.02,
        tip_pair=tip_pair, seed=seed,
    )
    rng = np.random.default_rng(seed)
    final_errors = []
    detail = []  # liste de (init_err, final_err) par cible
    for tg in range(N_TARGETS):
        target = sample_target(rng, target_box)
        first_err = None
        last_err = None
        for s in range(STEPS_PER_TARGET):
            r = agent.step(target)
            if first_err is None:
                first_err = r["distance"]
            last_err = r["distance"]
        final_errors.append(last_err)
        detail.append((first_err, last_err))
    if return_detail:
        return np.array(final_errors), detail
    return np.array(final_errors)


def main():
    print("=" * 78)
    print(" EVAL STATISTIQUE V4 ADAPTIVE")
    print(f" {len(SEEDS)} runs (seeds {SEEDS}) x 2 bras x {N_TARGETS} cibles x {STEPS_PER_TARGET} steps")
    print("=" * 78)

    summary = {}
    for bras_name, cfg in CONFIGS.items():
        print(f"\n--- {bras_name} ---")
        per_run_means_5 = []
        per_run_means_all = []
        per_run_intra_std_5 = []
        all_final_errors_concat = []
        for seed in SEEDS:
            errs = run_one(cfg["scene"], cfg["ee"], cfg["tip_pair"], cfg["target_box"], seed)
            mean_5 = float(np.mean(errs[-5:]))
            mean_all = float(np.mean(errs))
            std_5 = float(np.std(errs[-5:]))
            per_run_means_5.append(mean_5)
            per_run_means_all.append(mean_all)
            per_run_intra_std_5.append(std_5)
            all_final_errors_concat.extend(errs[-5:].tolist())
            print(f"  seed {seed}: mean(last 5) = {mean_5:.4f} m  (intra-run std = {std_5:.4f})  mean(all 15) = {mean_all:.4f}")

        per_run_means_5 = np.array(per_run_means_5)
        per_run_means_all = np.array(per_run_means_all)
        per_run_intra_std_5 = np.array(per_run_intra_std_5)
        all_final_errors_concat = np.array(all_final_errors_concat)

        print(f"  >>> mean(last 5) across runs : {per_run_means_5.mean():.4f} ± {per_run_means_5.std():.4f} m  (n={len(SEEDS)})")
        print(f"  >>> mean(all 15) across runs : {per_run_means_all.mean():.4f} ± {per_run_means_all.std():.4f} m")
        print(f"  >>> intra-run std avg        : {per_run_intra_std_5.mean():.4f} m")
        print(f"  >>> all 15 last errors pooled: median={np.median(all_final_errors_concat):.4f}, min={all_final_errors_concat.min():.4f}, max={all_final_errors_concat.max():.4f}")

        summary[bras_name] = {
            "mean_last5_inter": per_run_means_5.mean(),
            "std_last5_inter": per_run_means_5.std(),
            "mean_last5_intra_std_avg": per_run_intra_std_5.mean(),
            "mean_all_inter": per_run_means_all.mean(),
            "std_all_inter": per_run_means_all.std(),
        }

    print()
    print("=" * 78)
    print(" RESUME STATISTIQUE")
    print("=" * 78)
    for bras_name, s in summary.items():
        print(f"  {bras_name}:")
        print(f"    Mean last 5 (inter-run)   : {s['mean_last5_inter']:.4f} ± {s['std_last5_inter']:.4f} m")
        print(f"    Mean all 15 (inter-run)   : {s['mean_all_inter']:.4f} ± {s['std_all_inter']:.4f} m")
        print(f"    Intra-run std avg (last 5): {s['mean_last5_intra_std_avg']:.4f} m")
    print("=" * 78)

    # Detail seed 42 SO-100 pour le rapport (le run "magique")
    print()
    print("=" * 78)
    print(" DETAIL seed 42 SO-100 (le run magique 0.034m que le rapport reportait)")
    print("=" * 78)
    cfg = CONFIGS["SO-100"]
    errs42, detail42 = run_one(cfg["scene"], cfg["ee"], cfg["tip_pair"], cfg["target_box"], 42, return_detail=True)
    for i, (init, fin) in enumerate(detail42, 1):
        print(f"  C{i:2d}: init={init:.4f} -> final={fin:.4f} m")
    print(f"  Mean last 5 = {np.mean(errs42[-5:]):.4f} m  (std intra-run last 5 = {np.std(errs42[-5:]):.4f})")
    print(f"  Mean all 15 = {np.mean(errs42):.4f} m       (std all 15 = {np.std(errs42):.4f})")
    print(f"  Median last 5 = {np.median(errs42[-5:]):.4f} m")
    print(f"  Min/Max last 5 : {errs42[-5:].min():.4f} / {errs42[-5:].max():.4f}")


if __name__ == "__main__":
    try:
        main()
    finally:
        sys.exit(0)
