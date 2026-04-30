#!/usr/bin/env python3
"""
CyborgV0.1 -- Bras robotique 2D apprenant a atteindre une cible.

Cycle d'inference active (Friston/Clark) sur un cas jouet de controle moteur :
  MODELE -> PREDICTION -> PERCEPTION -> ERREUR -> ajuste MODELE -> (boucle)

Usage:
    python eleve.py             # mode auto, 30 cycles, pause 0.4s entre
    python eleve.py --step      # pas-a-pas (Entree entre cycles)
    python eleve.py --cycles 50 # nombre de cycles personnalise
    python eleve.py --seed 42   # reproductibilite
"""

import argparse
import os
import random
import sys
import time
from datetime import datetime

import numpy as np

from arm import forward
from ascii_render import render
from modele import Modele

HERE = os.path.dirname(os.path.abspath(__file__))


def _path(name):
    return os.path.join(HERE, name)


def sample_target(rng):
    """Tire une cible accessible dans le demi-plan superieur."""
    rmax = 4.5  # < L1 + L2
    rmin = 1.0  # > |L1 - L2|
    r = rng.uniform(rmin, rmax)
    a = rng.uniform(0.15, np.pi - 0.15)  # demi-cercle haut, marges
    return np.array([r * np.cos(a), r * np.sin(a)])


def write_perception(target, end_effector_pos, cycle):
    content = (
        "# Perception -- etat observe du monde\n"
        f"**Cycle :** {cycle}\n"
        f"**Mise a jour :** {datetime.now().isoformat(timespec='seconds')}\n\n"
        "## Cible\n"
        f"({target[0]:+.3f}, {target[1]:+.3f})\n\n"
        "## End-effector observe\n"
        f"({end_effector_pos[0]:+.3f}, {end_effector_pos[1]:+.3f})\n"
    )
    with open(_path('PERCEPTION.md'), 'w', encoding='utf-8') as f:
        f.write(content)


def write_prediction(target, theta_pred, pos_predicted, cycle):
    content = (
        "# Prediction -- inference active\n"
        f"**Cycle :** {cycle}\n\n"
        "## Action proposee\n"
        f"Atteindre la cible ({target[0]:+.3f}, {target[1]:+.3f}) avec angles "
        f"theta1={np.degrees(theta_pred[0]):+.2f}deg, theta2={np.degrees(theta_pred[1]):+.2f}deg\n\n"
        "## Position attendue selon modele interne\n"
        f"({pos_predicted[0]:+.3f}, {pos_predicted[1]:+.3f})\n"
    )
    with open(_path('PREDICTION.md'), 'w', encoding='utf-8') as f:
        f.write(content)


def append_erreur(cycle, target, distance, dW_norm, db_norm):
    line = (
        f"### Cycle {cycle} -- distance {distance:.4f}\n"
        f"**Cible :** ({target[0]:+.3f}, {target[1]:+.3f})\n"
        f"**Ajustement :** ||dW||={dW_norm:.5f}, ||db||={db_norm:.5f}\n\n"
    )
    with open(_path('ERREUR.md'), 'a', encoding='utf-8') as f:
        f.write(line)


def append_pensee(cycle, text):
    with open(_path('log/pensees.md'), 'a', encoding='utf-8') as f:
        f.write(f"### Cycle {cycle} ({datetime.now().isoformat(timespec='seconds')})\n{text}\n\n")


def append_changement(cycle, text):
    with open(_path('log/changements.md'), 'a', encoding='utf-8') as f:
        f.write(f"### Cycle {cycle} ({datetime.now().isoformat(timespec='seconds')})\n{text}\n\n")


def reset_logs():
    """Reinitialise ERREUR.md et les logs pour cette session."""
    with open(_path('ERREUR.md'), 'w', encoding='utf-8') as f:
        f.write(
            "# Erreur de prediction -- historique\n"
            "> Chaque cycle ajoute une entree. La distance entre la position atteinte et la cible mesure l'erreur.\n\n"
            "---\n\n"
            "## Historique (session courante)\n\n"
        )
    for p in ('log/pensees.md', 'log/changements.md'):
        os.makedirs(os.path.dirname(_path(p)), exist_ok=True)
        with open(_path(p), 'w', encoding='utf-8') as f:
            title = "pensees de l'agent" if p.endswith('pensees.md') else "changements appliques"
            f.write(f"# Journal -- {title}\n\n")


def banner():
    print()
    print("=" * 64)
    print(" CyborgV0.1 -- Bras 2D + inference active (Friston/Clark)")
    print(" Cycle MODELE -> PREDICTION -> PERCEPTION -> ERREUR -> ajuste")
    print("=" * 64)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--step', action='store_true', help='pas-a-pas (Entree entre cycles)')
    parser.add_argument('--cycles', type=int, default=30)
    parser.add_argument('--seed', type=int, default=None)
    parser.add_argument('--pause', type=float, default=0.4, help='pause en mode auto (s)')
    args = parser.parse_args()

    rng = random.Random(args.seed)
    if args.seed is not None:
        np.random.seed(args.seed)

    reset_logs()
    modele = Modele()
    erreurs = []

    banner()

    for cycle in range(1, args.cycles + 1):
        target = sample_target(rng)

        # PREDICTION : ce que le modele propose
        theta_pred = modele.predire(target)
        pos_pred_par_modele = forward(theta_pred[0], theta_pred[1])[0]

        # PERCEPTION : le bras execute -> position reelle (cinematique exacte)
        end_effector, elbow = forward(theta_pred[0], theta_pred[1])

        # ERREUR : distance euclidienne entre cible visee et position atteinte
        distance = float(np.linalg.norm(end_effector - target))
        erreurs.append(distance)

        # AJUSTEMENT du modele interne
        dW_norm, db_norm = modele.apprendre(target, theta_pred)

        # AFFICHAGE CLI
        print()
        print(f"--- Cycle {cycle:3d} " + "-" * 44)
        print(f"  Cible           : ({target[0]:+.2f}, {target[1]:+.2f})")
        print(f"  Modele predit   : theta1={np.degrees(theta_pred[0]):+7.1f}deg  "
              f"theta2={np.degrees(theta_pred[1]):+7.1f}deg")
        print(f"  Position atteinte: ({end_effector[0]:+.2f}, {end_effector[1]:+.2f})")

        baseline_str = f"  (cycle 1 : {erreurs[0]:.3f})" if cycle > 1 else ""
        moy_str = f"  moy 5 derniers : {np.mean(erreurs[-5:]):.3f}" if cycle >= 5 else ""
        print(f"  Erreur          : {distance:.3f}{baseline_str}{moy_str}")
        print(f"  MODELE update   : ||dW||={dW_norm:.4f}  ||db||={db_norm:.4f}")
        print()
        print(render(elbow, end_effector, target))

        # Update fichiers organes
        write_perception(target, end_effector, cycle)
        write_prediction(target, theta_pred, pos_pred_par_modele, cycle)
        append_erreur(cycle, target, distance, dW_norm, db_norm)

        # Logs metacognitifs (note.md L17)
        pensee = (
            f"J'ai vise ({target[0]:+.2f}, {target[1]:+.2f}). "
            f"Selon mon modele, theta1={np.degrees(theta_pred[0]):+.1f}deg + theta2={np.degrees(theta_pred[1]):+.1f}deg "
            f"devraient amener l'effecteur a la cible. En realite il est arrive a "
            f"({end_effector[0]:+.2f}, {end_effector[1]:+.2f}). "
            f"Distance {distance:.3f}. "
            + ("L'erreur a baisse vs cycle 1 -- mon modele s'aligne." if cycle > 1 and distance < erreurs[0]
               else "L'erreur reste haute -- l'apprentissage continue.")
        )
        append_pensee(cycle, pensee)
        if dW_norm > 0.001 or db_norm > 0.001:
            append_changement(
                cycle,
                f"J'ai ajuste W (||dW||={dW_norm:.4f}) et b (||db||={db_norm:.4f}) "
                f"pour mieux mapper cible -> angles. "
                f"Benefice attendu : reduction de l'erreur sur cibles voisines de ({target[0]:+.2f}, {target[1]:+.2f}). "
                f"Limite : ce mapping reste lineaire -- il sature pour des cibles excentriques."
            )

        if args.step:
            try:
                input("  [Entree pour cycle suivant, Ctrl+C pour quitter] ")
            except (KeyboardInterrupt, EOFError):
                print("\n  Interrompu par l'utilisateur.")
                break
        else:
            time.sleep(args.pause)

    # Dump du modele final dans MODELE.md
    modele.dump_modele(_path('MODELE.md'))

    # Bilan final
    print()
    print("=" * 64)
    print(" BILAN")
    print("=" * 64)
    n = len(erreurs)
    print(f"  Cycles executes      : {n}")
    print(f"  Erreur initiale      : {erreurs[0]:.3f}")
    if n >= 5:
        print(f"  Erreur finale (moy 5): {np.mean(erreurs[-5:]):.3f}")
        reduction = (1.0 - np.mean(erreurs[-5:]) / erreurs[0]) * 100.0
        print(f"  Reduction            : {reduction:+.1f}%")
    print(f"  Fichiers mis a jour  : MODELE.md, PERCEPTION.md, PREDICTION.md, ERREUR.md, log/*")
    print("=" * 64)
    print()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n  Arret manuel.")
        sys.exit(0)
