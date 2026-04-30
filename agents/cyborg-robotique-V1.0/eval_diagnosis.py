"""Diagnostic seed 47 (worst) vs seed 43 (best) sur SO-100 V4 ADAPTIVE.

Pour chaque cible : log target, target_norm, final_err, ||J||_min/mean/max, theta_evolution.
Identifie patterns differents entre seed catastrophique et seed reussi.
"""
import os, sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
import mujoco
import numpy as np
from cerveau.agent_adaptive import CyborgAdaptiveAgent

SCENE = os.path.join(SCRIPT_DIR, "external", "mujoco_menagerie", "trs_so_arm100", "scene.xml")
TARGET_BOX = [(0.10, 0.30), (-0.20, 0.20), (0.05, 0.30)]
N_TARGETS = 15
STEPS_PER_TARGET = 8


def sample(rng):
    return np.array([rng.uniform(*TARGET_BOX[0]), rng.uniform(*TARGET_BOX[1]), rng.uniform(*TARGET_BOX[2])])


def joint_limit_saturation_frac(model, n_dof, theta):
    """Pour chaque DoF, fraction du range utilisée (0 = au milieu, 1 = à la limite)."""
    sats = []
    for i in range(n_dof):
        if model.jnt_limited[i]:
            low, high = model.jnt_range[i, 0], model.jnt_range[i, 1]
            mid = (low + high) / 2.0
            half_range = (high - low) / 2.0
            if half_range > 1e-6:
                sat = abs(theta[i] - mid) / half_range  # 0=mid, 1=at limit
                sats.append(sat)
    return sats


def diagnose(seed):
    print(f"\n{'='*78}")
    print(f" DIAGNOSTIC seed {seed} SO-100 V4 ADAPTIVE")
    print(f"{'='*78}")
    model = mujoco.MjModel.from_xml_path(SCENE)
    data = mujoco.MjData(model)
    n_dof = 5
    agent = CyborgAdaptiveAgent(
        model, data, end_effector_body="Fixed_Jaw", n_dof=n_dof,
        buffer_size=12, step_size=0.4, noise_scale=0.02,
        tip_pair=("Fixed_Jaw", "Moving_Jaw"), seed=seed)

    rng = np.random.default_rng(seed)
    target_results = []
    for tg in range(N_TARGETS):
        target = sample(rng)
        target_norm = float(np.linalg.norm(target))
        # Pre-step : measure init err
        theta_pre = data.qpos[:n_dof].copy()
        p_pre = agent.execute(theta_pre)
        init_err = float(np.linalg.norm(p_pre - target))

        j_norms = []
        max_sat_per_step = []
        for s in range(STEPS_PER_TARGET):
            r = agent.step(target)
            j_norms.append(r["J_norm"])
            sats = joint_limit_saturation_frac(model, n_dof, data.qpos[:n_dof])
            if sats:
                max_sat_per_step.append(max(sats))
        last_err = r["distance"]

        target_results.append({
            'target': target, 'target_norm': target_norm,
            'init_err': init_err, 'final_err': last_err,
            'j_norm_min': min(j_norms), 'j_norm_max': max(j_norms),
            'j_norm_mean': float(np.mean(j_norms)),
            'max_sat_mean': float(np.mean(max_sat_per_step)) if max_sat_per_step else 0.0,
            'max_sat_max': float(max(max_sat_per_step)) if max_sat_per_step else 0.0,
        })

    for i, r in enumerate(target_results, 1):
        marker = " [FAIL]" if r['final_err'] > 0.2 else (" [OK]" if r['final_err'] < 0.05 else "")
        print(f"  C{i:2d}: tgt({r['target'][0]:+.2f},{r['target'][1]:+.2f},{r['target'][2]:+.2f}) "
              f"||tgt||={r['target_norm']:.3f} "
              f"init={r['init_err']:.3f}->fin={r['final_err']:.4f}  "
              f"||J||={r['j_norm_mean']:.3f}(min{r['j_norm_min']:.3f})  "
              f"sat={r['max_sat_mean']:.2f}{marker}")

    finals = np.array([r['final_err'] for r in target_results])
    j_means = np.array([r['j_norm_mean'] for r in target_results])
    j_mins = np.array([r['j_norm_min'] for r in target_results])
    target_norms = np.array([r['target_norm'] for r in target_results])
    sats_max = np.array([r['max_sat_max'] for r in target_results])

    print(f"\n  --- Stats seed {seed} ---")
    print(f"  Mean last 5    : {np.mean(finals[-5:]):.4f} m")
    print(f"  Mean all 15    : {np.mean(finals):.4f} m")
    print(f"  ||J|| mean glob: {j_means.mean():.3f}  (min global = {j_means.min():.3f})")
    print(f"  ||tgt|| moy    : {target_norms.mean():.3f} m  (range {target_norms.min():.3f}-{target_norms.max():.3f})")
    print(f"  Sat max moy    : {sats_max.mean():.2f}  (max global = {sats_max.max():.2f})  // 1.0 = bras a la limite")
    print(f"  Cibles ||J||min < 0.1 (J dégénère)  : {(j_mins < 0.1).sum()}/{N_TARGETS}")
    print(f"  Cibles final > 0.2 (échec)           : {(finals > 0.2).sum()}/{N_TARGETS}")
    print(f"  Cibles final < 0.05 (réussi)         : {(finals < 0.05).sum()}/{N_TARGETS}")
    print(f"  Cibles ||tgt|| > 0.4 (limite WS)     : {(target_norms > 0.4).sum()}/{N_TARGETS}")
    print(f"  Cibles sat_max > 0.9 (bras a limite) : {(sats_max > 0.9).sum()}/{N_TARGETS}")

    return {'finals': finals, 'j_mins': j_mins, 'target_norms': target_norms, 'sats_max': sats_max, 'j_means': j_means}


def main():
    print(" Comparaison seed 43 (best, 0.012m) vs seed 47 (worst, 0.361m) sur SO-100")
    s43 = diagnose(43)
    s47 = diagnose(47)

    print(f"\n{'='*78}")
    print(f" COMPARAISON")
    print(f"{'='*78}")
    print(f"  Mean last 5         : seed43={np.mean(s43['finals'][-5:]):.4f}  vs  seed47={np.mean(s47['finals'][-5:]):.4f}")
    print(f"  ||tgt|| moyen       : seed43={s43['target_norms'].mean():.3f}  vs  seed47={s47['target_norms'].mean():.3f}")
    print(f"  ||J||min moyen      : seed43={s43['j_mins'].mean():.3f}  vs  seed47={s47['j_mins'].mean():.3f}")
    print(f"  Sat_max moyen       : seed43={s43['sats_max'].mean():.2f}   vs  seed47={s47['sats_max'].mean():.2f}")
    print(f"  Cibles dégénères J  : seed43={(s43['j_mins'] < 0.1).sum()}  vs  seed47={(s47['j_mins'] < 0.1).sum()}")
    print(f"  Cibles bras saturé  : seed43={(s43['sats_max'] > 0.9).sum()}  vs  seed47={(s47['sats_max'] > 0.9).sum()}")


if __name__ == "__main__":
    try:
        main()
    finally:
        sys.exit(0)
