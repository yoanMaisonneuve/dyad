"""Affichage ASCII du bras 2D et de la cible (CLI vivante)."""
import numpy as np

WIDTH = 36
HEIGHT = 14
ORIGIN_COL = WIDTH // 2
ORIGIN_ROW = HEIGHT - 1
SCALE_X = 2.8
SCALE_Y = 1.3


def to_pixel(x, y):
    col = ORIGIN_COL + int(round(x * SCALE_X))
    row = ORIGIN_ROW - int(round(y * SCALE_Y))
    return row, col


def _put(grid, r, c, ch):
    if 0 <= r < HEIGHT and 0 <= c < WIDTH:
        grid[r][c] = ch


def _draw_line(grid, r1, c1, r2, c2, ch):
    steps = max(abs(r2 - r1), abs(c2 - c1), 1)
    for i in range(1, steps):
        r = r1 + (r2 - r1) * i // steps
        c = c1 + (c2 - c1) * i // steps
        if 0 <= r < HEIGHT and 0 <= c < WIDTH and grid[r][c] == ' ':
            grid[r][c] = ch


def render(elbow, end_effector, target):
    grid = [[' '] * WIDTH for _ in range(HEIGHT)]

    # Origine epaule
    or_r, or_c = ORIGIN_ROW, ORIGIN_COL

    # Coordonnees pixel
    el_r, el_c = to_pixel(elbow[0], elbow[1])
    ef_r, ef_c = to_pixel(end_effector[0], end_effector[1])
    t_r, t_c = to_pixel(target[0], target[1])

    # Segments d'abord (pour ne pas ecraser les marqueurs)
    _draw_line(grid, or_r, or_c, el_r, el_c, '.')
    _draw_line(grid, el_r, el_c, ef_r, ef_c, '.')

    # Marqueurs
    _put(grid, t_r, t_c, 'X')      # cible
    _put(grid, or_r, or_c, 'O')    # epaule
    _put(grid, el_r, el_c, 'o')    # coude
    _put(grid, ef_r, ef_c, '@')    # end-effector

    border = '+' + '-' * WIDTH + '+'
    body = '\n'.join('|' + ''.join(row) + '|' for row in grid)
    legend = '    O=epaule  o=coude  @=effecteur  X=cible'
    return border + '\n' + body + '\n' + border + '\n' + legend
