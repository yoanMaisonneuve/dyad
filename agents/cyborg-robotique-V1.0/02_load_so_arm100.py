"""02_load_so_arm100.py — Test load SO-ARM100 (LeRobot) via mujoco_menagerie

Charge le MJCF officiel du bras SO-ARM100 (6 DoF, kit LeRobot HuggingFace).
Lance le viewer et applique des contrôles aléatoires lissés pendant 30s.
Si tu vois le bras 6 segments bouger doucement : on est prêts pour la politique AIF.
"""
import os
import time

import mujoco
import mujoco.viewer
import numpy as np

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MENAGERIE_PATH = os.path.join(SCRIPT_DIR, "external", "mujoco_menagerie")
SO100_SCENE = os.path.join(MENAGERIE_PATH, "trs_so_arm100", "scene.xml")


def main():
    if not os.path.exists(SO100_SCENE):
        print(f"ERREUR : {SO100_SCENE} introuvable.")
        print("Etape manquante : git clone --depth=1 https://github.com/google-deepmind/mujoco_menagerie.git external/mujoco_menagerie")
        return

    print(f"Chargement SO-ARM100 : {SO100_SCENE}")
    model = mujoco.MjModel.from_xml_path(SO100_SCENE)
    data = mujoco.MjData(model)

    print(f"Modele charge. nq={model.nq} (DoF), nu={model.nu} (actuateurs).")
    print("Joints :")
    for i in range(model.njnt):
        joint_name = mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_JOINT, i)
        print(f"  - {joint_name}")
    print("Lancement du viewer (ferme pour quitter, ou attends 30s)...")

    rng = np.random.default_rng(42)

    with mujoco.viewer.launch_passive(model, data) as viewer:
        start = time.time()
        last_ctrl_update = 0.0
        target_ctrl = np.zeros(model.nu)

        while viewer.is_running() and time.time() - start < 30:
            step_start = time.time()
            t = time.time() - start

            # Cible aleatoire renouvelee toutes les 2.5s
            if t - last_ctrl_update > 2.5:
                target_ctrl = rng.uniform(-0.5, 0.5, size=model.nu)
                last_ctrl_update = t

            # Lissage vers la cible (controle doux)
            data.ctrl[:] = 0.97 * data.ctrl[:] + 0.03 * target_ctrl

            mujoco.mj_step(model, data)
            viewer.sync()

            time_until_next_step = model.opt.timestep - (time.time() - step_start)
            if time_until_next_step > 0:
                time.sleep(time_until_next_step)

    print("Viewer ferme. Test SO-ARM100 termine.")


if __name__ == "__main__":
    main()
