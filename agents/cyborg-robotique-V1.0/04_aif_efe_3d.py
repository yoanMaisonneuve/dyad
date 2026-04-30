"""04_aif_efe_3d.py -- Vraie politique AIF avec EFE direct sur SO-ARM100.

J+9 du sprint Print Your Own Optimus.

Difference clef avec 03_aif_baseline_3d.py :
  - 03 (baseline) : utilise IK iteratif via jacobienne MuJoCo (oracle externe)
  - 04 (EFE) : aucun acces a la jacobienne MuJoCo. L'agent apprend la cinematique
              forward du bras par interaction (modele MLP appris) + selectionne
              les actions via EFE pragmatic (sampling + argmin distance predite).

Protocole alpha (cible changeante chaque cycle, comparable directement au baseline) :
  - 30 cycles, nouvelle cible aleatoire chaque cycle, 1 step par cycle
  - Memes graines que baseline (seed=42 cibles, seed=42 model init)
  - Comparaison directe : reduction% erreur sur 30 cycles

Resultat attendu :
  - Au debut, modele interne mauvais => erreur grande
  - Au fil des cycles, modele apprend la cinematique => erreur diminue
  - Final : erreur comparable ou meilleure que baseline (modele non-lineaire
    capture des relations que le mapping lineaire ne peut pas)
"""
import os
import sys
import time

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

import mujoco
import mujoco.viewer
import numpy as np

from cerveau.agent_efe import CyborgEFEAgent

MENAGERIE_PATH = os.path.join(SCRIPT_DIR, "external", "mujoco_menagerie")
SO100_SCENE = os.path.join(MENAGERIE_PATH, "trs_so_arm100", "scene.xml")

N_CYCLES = 30
PAUSE_PER_CYCLE = 1.2  # secondes pour voir chaque cible/exec


def sample_target_3d(rng) -> np.ndarray:
    """Cible aleatoire dans une boite atteignable (memes bornes que baseline)."""
    x = rng.uniform(0.10, 0.30)
    y = rng.uniform(-0.20, 0.20)
    z = rng.uniform(0.05, 0.30)
    return np.array([x, y, z])


def add_target_marker(viewer, target_pos: np.ndarray):
    """Ajoute une sphere rouge a target_pos (visualisation runtime user_scn)."""
    viewer.user_scn.ngeom = 0
    mujoco.mjv_initGeom(
        viewer.user_scn.geoms[0],
        type=mujoco.mjtGeom.mjGEOM_SPHERE,
        size=np.array([0.015, 0.0, 0.0]),
        pos=target_pos,
        mat=np.eye(3).flatten(),
        rgba=np.array([1.0, 0.2, 0.2, 0.9]),
    )
    viewer.user_scn.ngeom = 1


def find_end_effector_body(model: mujoco.MjModel) -> str:
    """Trouve un body end-effector ('Jaw', 'gripper', 'ee')."""
    for i in range(model.nbody):
        name = mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_BODY, i) or ""
        if any(kw in name.lower() for kw in ("jaw", "gripper", "ee", "end_effector")):
            return name
    return ""


def main():
    if not os.path.exists(SO100_SCENE):
        print(f"ERREUR : {SO100_SCENE} introuvable.")
        return

    print(f"Chargement SO-ARM100 : {SO100_SCENE}")
    model = mujoco.MjModel.from_xml_path(SO100_SCENE)
    data = mujoco.MjData(model)

    ee_body_name = find_end_effector_body(model)
    if not ee_body_name:
        print("ERREUR : impossible de trouver le body end-effector.")
        return
    print(f"End-effector body : {ee_body_name}")

    n_dof = 5
    agent = CyborgEFEAgent(
        model,
        data,
        end_effector_body=ee_body_name,
        n_dof=n_dof,
        n_candidates=30,
        action_scale=0.18,
        n_hidden=32,
        learning_rate=0.015,
        buffer_size=300,
        n_grad_steps_per_cycle=10,
        seed=42,
    )

    rng = np.random.default_rng(42)  # meme seed cibles que baseline

    print()
    print("=" * 78)
    print(" CyborgV1.0 EFE -- vraie politique AIF (modele appris + EFE direct)")
    print(" Aucun acces jacobienne MuJoCo. Le code apprend son corps par interaction.")
    print("=" * 78)

    erreurs = []

    with mujoco.viewer.launch_passive(model, data) as viewer:
        for cycle in range(1, N_CYCLES + 1):
            if not viewer.is_running():
                print("\nViewer ferme par l'utilisateur.")
                break

            target = sample_target_3d(rng)
            add_target_marker(viewer, target)

            result = agent.cycle(target)
            erreurs.append(result["distance"])

            mujoco.mj_forward(model, data)
            viewer.sync()

            print()
            print(f"--- Cycle {cycle:3d} " + "-" * 58)
            print(f"  Cible 3D        : ({target[0]:+.3f}, {target[1]:+.3f}, {target[2]:+.3f}) m")
            print(f"  EE atteint      : ({result['p_observed'][0]:+.3f}, {result['p_observed'][1]:+.3f}, {result['p_observed'][2]:+.3f}) m")
            print(f"  Erreur reelle   : {result['distance']:.4f} m", end="")
            if cycle >= 5:
                print(f"   (moy 5 derniers : {np.mean(erreurs[-5:]):.4f})", end="")
            print()
            print(f"  EFE predit      : {result['efe_predicted']:.5f}  (sqrt: {np.sqrt(result['efe_predicted']):.4f} m predit par modele appris)")
            print(f"  Buffer / Updates: {result['buffer_size']:3d} obs  /  {result['model_updates']:5d} updates MLP")
            print(f"  Loss MLP recente: {result['loss']:.5f}")

            time.sleep(PAUSE_PER_CYCLE)

    print()
    print("=" * 78)
    print(" BILAN J+9 EFE")
    print("=" * 78)
    n = len(erreurs)
    print(f"  Cycles executes      : {n}")
    if n >= 1:
        print(f"  Erreur initiale      : {erreurs[0]:.4f} m")
    if n >= 5:
        moy_finale = np.mean(erreurs[-5:])
        print(f"  Erreur finale (moy 5): {moy_finale:.4f} m")
        if erreurs[0] > 1e-6:
            reduction = (1.0 - moy_finale / erreurs[0]) * 100.0
            print(f"  Reduction            : {reduction:+.1f}%")
            print()
            print(f"  Comparaison BASELINE (03_aif_baseline_3d.py) :")
            print(f"    Baseline lineaire + IK oracle  -> reduction +53.6%, erreur finale 0.222 m")
            print(f"    EFE modele appris + EFE direct -> reduction {reduction:+.1f}%, erreur finale {moy_finale:.4f} m")
            print()
            print(f"  Note : EFE part SANS la jacobienne MuJoCo. Le modele apprend la")
            print(f"         cinematique du bras par interaction. C'est 'le code apprend son corps'.")
    print("=" * 78)


if __name__ == "__main__":
    try:
        main()
    finally:
        # Workaround segfault MuJoCo viewer Windows + Python 3.14
        sys.exit(0)
