# `perception/` — Vision, force, tactile (à contribuer)

> Module qui transforme les capteurs (caméra, IMU, force, tactile) en représentation interne utilisable par les cerveaux moteurs.

**Status** : ⏳ Vide, à contribuer  
**Difficulté** : ⭐⭐⭐  
**Estim solo** : 2-4 mois  
**Pour qui** : vision researchers, makers, étudiants robotique

---

## Mission

Donner des "yeux", "toucher" et "équilibre" au robot. Convertit signaux bruts (pixels, courants servo, IMU readings) en informations structurées (position objet 3D, force ressentie, orientation).

## Sous-modules à implémenter

### `perception/vision/` — Vision
- [ ] **Caméra calibration** : intrinsics + extrinsics
- [ ] **Object detection** : trouver objets dans la scène (DINO-X, OWL-ViT, ou approches simples HSV+contours)
- [ ] **Pose estimation 6D** : position + orientation des objets
- [ ] **Depth estimation** : RealSense D405 native OR depth from monocular (MiDaS, etc.)
- [ ] **Demo** : "Where is the cube?" → position 3D précise

### `perception/force/` — Force/torque
- [ ] **Servo current → torque** : pour chaque servo, calibration courant → torque (formule ou table)
- [ ] **F/T sensor wrist** : si capteur 6-axis dispo, lecture + filtrage
- [ ] **Contact detection** : seuils sur force pour détecter contact
- [ ] **Demo** : "Le robot a-t-il touché quelque chose ?" → True/False + intensité

### `perception/tactile/` — Tactile
- [ ] **DIGIT sensor support** : intégration capteur tactile DIGIT (~$200)
- [ ] **Touch event detection** : "quelque chose touche le doigt"
- [ ] **Slip detection** : "l'objet glisse"
- [ ] **Texture classification** : optionnel V1.0

### `perception/proprioception/` — Proprioception
- [ ] **IMU integration** : lire orientation/accéleration
- [ ] **Joint state estimation** : à partir des encodeurs servos
- [ ] **EE pose forward kinematics** : si modèle MJCF dispo (sinon laisser ARM_BRAIN apprendre)
- [ ] **Demo** : "Je sais où est mon corps" sans capteur externe

## Interface attendue

```python
from modules.perception import Perception

class Perception:
    def __init__(self, **sensors_config):
        """Init avec config capteurs disponibles (camera path, IMU port, etc.)."""
        self.has_vision = sensors_config.get('camera') is not None
        self.has_imu = sensors_config.get('imu_port') is not None
        # ...

    def get_object_pose(self, object_label: str) -> np.ndarray | None:
        """Détecte un objet par label, retourne pose 6D (position + quaternion) ou None."""
        ...

    def get_contact_force(self, sensor_id: int) -> float:
        """Force détectée à un capteur (Newton)."""
        ...

    def get_robot_orientation(self) -> np.ndarray:
        """Quaternion d'orientation du robot (depuis IMU)."""
        ...

    def get_joint_state(self) -> dict:
        """Position et vitesse de chaque joint depuis encodeurs."""
        ...

    def update(self) -> None:
        """Lit tous les capteurs disponibles, met à jour cache interne."""
        ...
```

## État de l'art

### Vision
- **Foundation models** : DINO, DINO-V2, SAM 2, OWL-ViT — robust mais gros
- **Lightweight detectors** : YOLOv8, YOLO-NAS — rapides, embarqués
- **Pose estimation** : MegaPose, DeepIM
- **Depth** : Intel RealSense D405 hardware, ou MiDaS pour monocular

### Force
- **OnRobot HEX-E** F/T sensor (~$5000, pro)
- **DIY load cells + HX711** (~$10, basique)
- **Servo current sensing** : Feetech STS3215 retourne courant natif

### Tactile
- **DIGIT sensor** (Meta open-source, ~$200) — tactile haute résolution
- **GelSight** — référence académique
- **DIY pressure sensors** — résistance variable

## Références

- [Lin et al 2024 — Foundation models for perception in robotics](https://arxiv.org/abs/2312.07843)
- [DIGIT (Meta)](https://digit.ml/)
- [OWL-ViT (Google)](https://github.com/google-research/scenic/tree/main/scenic/projects/owl_vit)
- [Intel RealSense docs](https://www.intelrealsense.com/)

## Setup hardware suggéré

**V0.1 (basique) :**
- Camera USB simple (Logitech C920 ~$80)
- Servo current via Feetech STS3215 (déjà sur SO-100/Koch)
- IMU optionnel (MPU6050 ~$5)

**V0.5 (recommandé) :**
- Intel RealSense D405 (~$340) — depth + RGB intégré
- DIGIT sensor (~$200) sur gripper

**V1.0 (pro) :**
- F/T sensor 6-axis (OnRobot ~$5000) ou similaire DIY
- IMU précis (Bosch BNO055 ~$30)

## Comment commencer

1. Choisis un sous-module qui t'intéresse (vision = le plus accessible et impactant)
2. Lis `cerveau/agent_adaptive_v6.py` pour comprendre comment intégrer
3. V0.1 minimum : juste object detection 3D via webcam + HSV color filter (ex: "trouve le cube rouge")
4. Test avec ARM_BRAIN V6 + GRASP_BRAIN : pick the red cube
5. PR avec démo

## Pourquoi c'est important

ARM_BRAIN sait bouger. GRASP_BRAIN sait saisir. Mais sans **PERCEPTION**, le robot ne sait pas **où** sont les choses ni **ce qu'il touche**. C'est le module qui rend le robot vraiment autonome dans le monde réel.

---

*Issue/PR : `[perception]` prefix.*
