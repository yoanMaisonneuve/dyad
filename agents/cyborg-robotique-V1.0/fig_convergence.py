"""fig_convergence.py -- Genere figure de convergence V6 sur N=10 seeds.

Collecte erreur a chaque step (15 cibles x 8 steps x 10 seeds = 1200 points).
Plot : erreur moyenne vs step number GLOBAL (cible 1 step 1, ..., cible 15 step 8),
avec shaded band median +/- IQR (plus robuste que std).

Sortie : agents/cyborg-robotique-V1.0/figures/v6_convergence.png
"""
import os, sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
import mujoco
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from cerveau.agent_adaptive_v6 import CyborgAdaptiveV6

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


def run_one_collect_traj(cfg, seed):
    """Run V6 + collecte erreur a chaque step. Retourne shape (N_TARGETS * STEPS_PER_TARGET,)."""
    model = mujoco.MjModel.from_xml_path(cfg["scene"])
    data = mujoco.MjData(model)
    n_dof = min(5, model.nq)
    agent = CyborgAdaptiveV6(
        model, data, end_effector_body=cfg["ee"], n_dof=n_dof,
        buffer_size=12, step_size=0.4, noise_scale=0.02,
        lambda_dls=0.05, warmup_amplitude=0.15,
        tip_pair=cfg["tip_pair"], seed=seed,
    )
    rng = np.random.default_rng(seed)
    traj_errors = []
    for tg in range(N_TARGETS):
        target = sample(rng, cfg["target_box"])
        for s in range(STEPS_PER_TARGET):
            r = agent.step(target)
            traj_errors.append(r["distance"])
    return np.array(traj_errors)


def plot_convergence(all_runs_dict, out_path):
    """all_runs_dict : {bras_name: array (N_seeds, total_steps)}"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5), sharey=True)
    for ax, (bras_name, runs) in zip(axes, all_runs_dict.items()):
        # runs shape (N_seeds, total_steps)
        median = np.median(runs, axis=0)
        q25 = np.percentile(runs, 25, axis=0)
        q75 = np.percentile(runs, 75, axis=0)
        x = np.arange(len(median))
        ax.fill_between(x, q25, q75, alpha=0.3, label="IQR (Q25-Q75)")
        ax.plot(x, median, linewidth=1.5, label="Median")
        # Vertical lines pour separer cibles
        for t in range(1, N_TARGETS):
            ax.axvline(t * STEPS_PER_TARGET, color="gray", linestyle=":", alpha=0.3)
        ax.set_title(f"{bras_name} — V6 ADAPTIVE convergence (N=10 seeds)", fontsize=12)
        ax.set_xlabel("Global step (15 cibles × 8 steps)")
        ax.set_ylabel("Tracking error (m)")
        ax.set_ylim(0, max(0.5, runs.max() * 1.05))
        ax.legend(loc="upper right")
        ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(out_path, dpi=120, bbox_inches="tight")
    print(f"Figure sauvegardee : {out_path}")


def main():
    print("Generating convergence figure for V6 (N=10 seeds, 2 arms)...")
    all_runs = {}
    for bras_name, cfg in CONFIGS.items():
        print(f"  Running {bras_name}...")
        runs = []
        for seed in SEEDS:
            traj = run_one_collect_traj(cfg, seed)
            runs.append(traj)
        all_runs[bras_name] = np.array(runs)
        print(f"    shape : {all_runs[bras_name].shape}")

    out_dir = os.path.join(SCRIPT_DIR, "figures")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "v6_convergence.png")
    plot_convergence(all_runs, out_path)


if __name__ == "__main__":
    try:
        main()
    finally:
        sys.exit(0)
