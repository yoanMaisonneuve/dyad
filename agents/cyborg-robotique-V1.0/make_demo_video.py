"""make_demo_video.py -- Genere demo video V6 ADAPTIVE sur SO-ARM100.

Rendu offscreen MuJoCo + overlay PIL avec position target/erreur.

Output:
  figures/v6_demo.gif (LinkedIn-friendly)
  figures/v6_demo.mp4 (qualite preprint)
"""
import os, sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
import numpy as np
import mujoco
import imageio
from PIL import Image, ImageDraw, ImageFont
from cerveau.agent_adaptive_v6 import CyborgAdaptiveV6

SCENE_PATH = os.path.join(SCRIPT_DIR, "external", "mujoco_menagerie", "trs_so_arm100", "scene.xml")
OUT_DIR = os.path.join(SCRIPT_DIR, "figures")
os.makedirs(OUT_DIR, exist_ok=True)

WIDTH, HEIGHT = 640, 480  # framebuffer MuJoCo default max
FPS = 12
N_TARGETS = 8
STEPS_PER_TARGET = 8
FREEZE_FRAMES = 3  # frames de pause au start de chaque cible


def sample_target(rng):
    return np.array([rng.uniform(0.10, 0.25), rng.uniform(-0.18, 0.18), rng.uniform(0.08, 0.25)])


def project_3d_to_2d(model, data, point_3d, camera_id, width, height):
    """Approximation simple : projette point 3D sur image 2D via camera MuJoCo."""
    # MuJoCo camera matrix : on utilise une heuristique simple
    # Pour la demo, on retourne None (overlay texte seulement)
    return None


def add_overlay(pixel_array, text_lines, target_2d=None):
    img = Image.fromarray(pixel_array)
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("arial.ttf", 18)
        font_small = ImageFont.truetype("arial.ttf", 14)
    except (OSError, IOError):
        font = ImageFont.load_default()
        font_small = font

    # Background semi-transparent pour text
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    box_height = 22 * len(text_lines) + 12
    od.rectangle([(0, 0), (img.width, box_height)], fill=(0, 0, 0, 160))
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)

    y = 8
    for i, line in enumerate(text_lines):
        f = font if i == 0 else font_small
        draw.text((10, y), line, fill=(255, 255, 255), font=f)
        y += 20 if i == 0 else 18

    return np.array(img)


def main():
    print(f"Loading {SCENE_PATH}...")
    model = mujoco.MjModel.from_xml_path(SCENE_PATH)
    data = mujoco.MjData(model)

    print(f"Setup renderer {WIDTH}x{HEIGHT}...")
    renderer = mujoco.Renderer(model, height=HEIGHT, width=WIDTH)

    agent = CyborgAdaptiveV6(
        model, data, end_effector_body="Fixed_Jaw", n_dof=5,
        buffer_size=12, step_size=0.4, noise_scale=0.02,
        lambda_dls=0.05, warmup_amplitude=0.15,
        tip_pair=("Fixed_Jaw", "Moving_Jaw"), seed=43,
    )
    rng = np.random.default_rng(43)

    print(f"Generating {N_TARGETS} targets x ({FREEZE_FRAMES} freeze + {STEPS_PER_TARGET} steps)...")
    frames = []

    def render_with_target(target, text_lines):
        """Render frame avec marker target 3D ajoute via mjvScene."""
        renderer.update_scene(data)
        # Add target marker via runtime scene geom
        scene = renderer.scene
        if scene.ngeom < scene.maxgeom:
            mujoco.mjv_initGeom(
                scene.geoms[scene.ngeom],
                type=mujoco.mjtGeom.mjGEOM_SPHERE,
                size=np.array([0.018, 0, 0]),
                pos=target,
                mat=np.eye(3).flatten(),
                rgba=np.array([1.0, 0.15, 0.15, 1.0]),
            )
            scene.ngeom += 1
        pixel = renderer.render()
        return add_overlay(pixel, text_lines)

    for tg in range(N_TARGETS):
        target = sample_target(rng)

        # Freeze frames : montre nouvelle cible avant que le bras bouge
        for f in range(FREEZE_FRAMES):
            text_lines = [
                "V6 ADAPTIVE -- Print Your Own Optimus",
                f"Target {tg+1}/{N_TARGETS}  >>> NEW TARGET <<<",
                f"Target XYZ: ({target[0]:+.3f}, {target[1]:+.3f}, {target[2]:+.3f}) m",
                f"Apprentissage du corps en cours...",
            ]
            frames.append(render_with_target(target, text_lines))

        # Convergence steps
        for s in range(STEPS_PER_TARGET):
            r = agent.step(target)
            mujoco.mj_forward(model, data)
            err_mm = r["distance"] * 1000
            text_lines = [
                "V6 ADAPTIVE -- Print Your Own Optimus",
                f"Target {tg+1}/{N_TARGETS}  Step {s+1}/{STEPS_PER_TARGET}  Buffer {r['buffer_size']}",
                f"Target XYZ: ({target[0]:+.3f}, {target[1]:+.3f}, {target[2]:+.3f}) m",
                f"Error: {err_mm:.0f} mm    ||J||={r['J_norm']:.3f}",
            ]
            frames.append(render_with_target(target, text_lines))

    print(f"Captured {len(frames)} frames. Encoding...")

    gif_path = os.path.join(OUT_DIR, "v6_demo.gif")
    print(f"  GIF: {gif_path}")
    imageio.mimsave(gif_path, frames, fps=FPS, loop=0)

    mp4_path = os.path.join(OUT_DIR, "v6_demo.mp4")
    print(f"  MP4: {mp4_path}")
    imageio.mimsave(mp4_path, frames, fps=FPS, codec="libx264", quality=8)

    print(f"\nDone! {len(frames)} frames, {len(frames)/FPS:.1f}s @ {FPS} fps")
    print(f"Files in: {OUT_DIR}")


if __name__ == "__main__":
    main()
