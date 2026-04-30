"""01_setup_test.py — Premier test setup MuJoCo

Charge un bras 2 DoF, lance le viewer, applique des contrôles sinusoïdaux pendant 30s.
Si tu vois une fenêtre avec un bras qui bouge : tout marche, on peut attaquer S2.
"""
import math
import os
import time

import mujoco
import mujoco.viewer

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
XML_MODEL_PATH = os.path.join(SCRIPT_DIR, "scenes", "arm_2dof_v0.xml")


def main():
    print(f"Chargement du modele MuJoCo : {XML_MODEL_PATH}")
    model = mujoco.MjModel.from_xml_path(XML_MODEL_PATH)
    data = mujoco.MjData(model)

    print(f"Modele charge. nq={model.nq} (DoF), nu={model.nu} (actuateurs).")
    print("Lancement du viewer (ferme la fenetre pour quitter, ou attends 30s)...")

    with mujoco.viewer.launch_passive(model, data) as viewer:
        start = time.time()
        while viewer.is_running() and time.time() - start < 30:
            step_start = time.time()

            t = time.time() - start
            data.ctrl[0] = 1.5 * math.sin(t * 0.7)
            data.ctrl[1] = 1.0 * math.sin(t * 1.3)

            mujoco.mj_step(model, data)
            viewer.sync()

            time_until_next_step = model.opt.timestep - (time.time() - step_start)
            if time_until_next_step > 0:
                time.sleep(time_until_next_step)

    print("Viewer ferme. Test setup termine.")


if __name__ == "__main__":
    try:
        main()
    finally:
        # Workaround segfault MuJoCo viewer Windows + Python 3.14
        # Force exit avant que les destructeurs C ne crashent
        import sys
        sys.exit(0)
