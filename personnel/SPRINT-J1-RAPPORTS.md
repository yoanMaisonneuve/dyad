# SPRINT J+1 — Synthèse condensée des 5 rapports subagents

> 5 axes lancés 2026-04-29 soir, tous reçus. Synthèse condensée = base de décision + reprise robuste si session coupe.
> Rapports complets = task output files dans `%TEMP%/claude/.../tasks/` (non persistés en cas de coupure session).

---

## Axe (a) — État de l'art robotique humanoïde 2025-2026

**Recommandation tranchée :** NE PAS construire un humanoïde complet. Niche solo défendable = "VLA fine-tuning + simulation pipeline pour humanoïdes tiers, vertical manufacture HORS-AUTO". Stack : NVIDIA GR00T N1.5 + Isaac Lab + LeRobot + Unitree G1 (16k$ ou sim phase 1) + AgiBot World dataset.

**ANGLE CRITIQUE remonté :** ta L4 dit "robotique humanoïde manufacturière + alimentation pour 10x énergie" mais le marché humanoïde 2025-2026 ne fait PAS l'intersection robotique + énergie/alimentation. **PIVOT proposé :** choisir vertical aligné L4 — build-out infrastructure énergétique, agriculture intensive, OU **construction modulaire préfab (synergie chantier3D)**.

**Acteurs majeurs (en bref) :** Tesla Optimus, Figure AI (~1.7B$ levés), Apptronik Apollo (~700M$), Sanctuary AI (Vancouver — seul CA sérieux), Boston Dynamics Atlas, 1X, Unitree, Agility Digit, UBTech, XPENG, Fourier. Aucun n'a de valeur économique nette positive en manuf en 2025.

**Sources clés :**
- Figure AI Helix : figure.ai/news/helix
- NVIDIA GR00T N1.5 : developer.nvidia.com/isaac/gr00t
- Physical Intelligence π0 : physicalintelligence.company/blog/pi0
- Sanctuary AI : sanctuary.ai
- Glen Berseth UdeM (interlocuteur RL Mila) : mila.quebec/en/person/glen-berseth
- Open X-Embodiment : robotics-transformer-x.github.io
- IFR World Robotics 2025 + Morgan Stanley "Humanoid 100" report

---

## Axe (b) — Bras manipulateurs low-cost buildables solo

**Recommandation tranchée :** **SO-ARM101** (LeRobot HuggingFace).
- 6 DoF, **~600 CAD livré** au Québec via kit Seeed Studio
- Sourcing : kit Seeed (servos+cartes) + impression 3D pièces locales Montréal (Voxel Factory) + RealSense D405 chez Robotshop QC
- Stack matériel total (bras + vision Jetson Orin Nano) ≈ **1500-2000 CAD** = 30-40 % budget plafond 5000 CAD
- Buildable solo en 1 weekend (doc HF step-by-step, zéro soudure)
- MJCF officiel + LeRobot framework first-class

**Fallback :** MyCobot 320 Pi (~1500 CAD chez Robotshop QC, plug-and-play, livraison 3j). Sacrifie LeRobot first-class.

**À éviter :** WidowX/ViperX (budget x10), Stretch (x40), ROBSTRIDE DIY (3-6 mois solo), Reachy Mini (mauvais format).

**Sources clés :**
- LeRobot SO-ARM100 : github.com/TheRobotStudio/SO-ARM100
- HuggingFace doc SO-101 : huggingface.co/docs/lerobot/en/so101
- Kit Seeed Studio : seeedstudio.com/SO-ARM100.html
- Robotshop Canada : robotshop.com/ca/en

---

## Axe (c) — Simulateurs physiques 3D + politique custom

**Recommandation tranchée :** **MuJoCo** (binding officiel Python `mujoco`).
- Setup Windows 11 trivial : `pip install mujoco`, viewer inclus, zéro CUDA
- Bras low-cost natifs : MJCF officiels SO-100/Koch dans LeRobot
- Custom policy = boucle Python pure (pas de wrapper Gym imposé) — idéal pour brancher politique Friston
- Sim-to-real prouvé 2024-2025 : ALOHA, π0, DeepMind RT-X
- Continuité hardware S3 : LeRobot pont sim → robot réel

**Fallback :** PyBullet (encore plus simple install, paradigme similaire, asset SO-100 conversion manuelle).

**Non-recommandé sprint :** Isaac Lab (RTX 4080+ requis, 1-2j install pénibles), Genesis (bugs Windows persistants), Gazebo (déprécié manipulation), MJX (overhead JAX injustifié).

**Sources clés :**
- MuJoCo : mujoco.org
- mujoco_menagerie (DeepMind, ~30 robots calibrés MJCF) : github.com/google-deepmind/mujoco_menagerie
- LeRobot : github.com/huggingface/lerobot

---

## Axe (d) — Inférence active appliquée robotique réelle

**Thèse F1 reformulée précise :**
> *« Active Inference avec generative model gaussien à horizon fini est mathématiquement équivalent à Nonlinear Model Predictive Control sous régularité H1-H4 ; la différence n'est pas algorithmique mais épistémique (uncertainty-seeking via expected free energy vs cost-minimization pure). »*

**Trou exploitable :** aucun papier ne donne d'équivalence formelle complète AIF ↔ NMPC nonlinéaire continu + démo hardware side-by-side. Baltieri-Buckley (2019) a fait le linéaire. Da Costa (2022) a fait le discret. Watson et al. ont effleuré LQR. **Personne n'a fermé le nonlinéaire continu avec validation robot.**

**Sous-problème robotique sprint S2 (SPEC AFFINÉ) :**
- Bras **4 DoF MuJoCo** (Franka stripped ou custom URDF) — tâche reaching + grasping cube
- **3 contrôleurs** partageant même `forward_dynamics(x,u)` : (1) AIF pymdp custom + EFE H=10, (2) iLQR baseline, (3) MPC CasADi/acados
- Logger : trajectoires, coût cumulé, temps calcul, robustesse perturbations injectées
- Devient **Section 6 "Empirical Validation" du preprint F1**
- **PAS DE HARDWARE PHYSIQUE dans le sprint** — piège classique du roboticien solo

**Avertissement timing :** 30j théorème + 30j code + 30j rédaction = **89j pile, ZÉRO MARGE**.

**Stratégie publication :** arxiv first (preprint moyen-fort), journal Tier 1 après si extension hardware en sprint juin-juillet.

**Sources clés :**
- Lanillos et al "Active Inference in Robotics: Survey" — arxiv:2112.01871 (CITATION OBLIGATOIRE)
- Baltieri & Buckley (2019) "PID control as active inference" — Entropy 21(3):257
- Da Costa, Sajid et al (2022) "Relationship between dynamic programming and active inference" — Neural Computation
- Millidge, Tschantz, Buckley (2020) "Control-as-Inference" — arxiv:2006.12964
- Sancaktar, Lanillos (2020) "End-to-End Pixel-Based Deep AIF" — arxiv:2001.05847 (UR5)
- pymdp library Heins et al : github.com/infer-actively/pymdp

---

## Axe (e) — Antériorité solo + IP/brevets + espace IP libre

**Antériorité :** Yoan ne réinvente rien — fork SO-100/SO-101 + politique active inference au-dessus = **niche libre**. Personne dans les 15 acteurs solo identifiés ne fait simultanément (active inference + low-cost solo + preprint pédagogique).

**🚨 RISQUE IP CRITIQUE CACHÉ :**
**Brevet VERSES US 12,393,581 B2 (août 2025)** couvre la "spécification d'agents active inference via langage naturel + HSML knowledge graph + LLM-vers-paramètres POMDP". Yoan reste hors-champ TANT QUE la politique est codée à la main (paramètres fixés en Python, pas générés depuis prompt utilisateur). **À ÉVITER ABSOLUMENT :** UI "décris ton robot en NL → je génère l'agent active inference".

**Brevets autres** (Tesla Optimus hand WO2024/073138A1, Boston Dynamics, etc.) : risque négligeable pour open source non commercial. Audit IP pro ~3000 CAD nécessaire SEULEMENT si commercialisation.

**Stack licences recommandé :**
| Composant | Licence |
|---|---|
| Code Python | **Apache 2.0** (clause patent grant + retaliation, plus défensif que MIT) |
| Hardware (CAD/BOM) | **CERN-OHL-P v2** (Permissive) |
| Specs/docs/preprint | **CC-BY 4.0** |
| Datasets démo | **CDLA-Permissive 2.0** |

**Stratégie défensive J+5 (concrète) :**
1. Repo GitHub public daté avec README + licences en place
2. **Technical disclosure IP.com Prior Art Database (~250 CAD)** — indexé par examinateurs USPTO/EPO/OPIC dans 24h
3. À J+30 : preprint arxiv + tag git release v0.1 = double prior art horodaté irréfutable

**Cadre légal CA :** grace period 12 mois (Loi sur les brevets art. 28.2(1)(a)) — Yoan peut publier puis déposer brevet CA jusqu'à 12 mois après. Idem US (AIA). EPO/Chine/Japon = pas de grace period équivalent.

**15 acteurs antériorité solo (top 5) :**
- Alexander Koch — low_cost_robot (inspiration directe SO-100)
- Rémi Cadène + équipe LeRobot HuggingFace
- Phospho (Pierre-Louis Biojout + Paul-Louis Venard, YC W24, Paris francophone — bon angle FR)
- Berkeley Humanoid Lite (Yufeng Chi, ~3-4 pers) — humanoïde <5000$
- K-Scale Labs (Ben Bolte, YC W24)

**Sources clés :**
- LeRobot : github.com/huggingface/lerobot
- pymdp : github.com/infer-actively/pymdp
- Berkeley Humanoid Lite : github.com/HybridRobotics/Berkeley-Humanoid-Lite
- VERSES patent US 12,393,581 B2 : patents.google.com/patent/US12393581B2/en
- CERN OHL v2 : spdx.org/licenses/CERN-OHL-S-2.0.html
- Defensive publication IP.com : ip.com/innovation-power-suite/defensive-publishing/
- CIPO grace period : smartbiggar.ca/insights/publication/the-one-year-grace-period-for-patent-filing-in-canada

---

## Synthèse intégrée — Convergence forte des 5 axes

**Stack technique unanime :**
- **Hardware (post-sprint, pas dans S1-S4)** : SO-ARM101 fork + RealSense D405 + Jetson Orin Nano (~1500-2000 CAD)
- **Simulateur** : MuJoCo + LeRobot framework (Python, Windows-friendly)
- **Politique** : active inference custom basée pymdp + extension PyTorch continue
- **Comparaison** : 3 contrôleurs (AIF / iLQR / MPC CasADi) sur même `forward_dynamics(x,u)`
- **Licences** : Apache 2.0 (code) + CERN-OHL-P v2 (HW) + CC-BY 4.0 (docs) + CDLA-Permissive (datasets)

**Niche défendable identifiée :** "active inference + low-cost solo + preprint AIF=NMPC + démo manipulation 4 DoF + open source défensif". Personne dans les 15 acteurs listés ne couvre simultanément ces 5 dimensions.

**Spec sprint affinée (vs plan original) :**
- ✅ S1 (J+1-7) : audit fait, scope figé, choix outils tranché, IP cartographiée
- S2 (J+8-14) : sim 3D MuJoCo + bras 4 DoF + politique AIF (fonctionnel, pas optimal)
- S3 (J+15-21) : 2 contrôleurs baseline (iLQR + MPC) + benchmark + spec hardware SO-ARM101 + commande matériel pour post-sprint
- S4 (J+22-28) : rédaction Section 6 preprint + plan partenariat Mila/UdeM/Sanctuary + plan fundraise + post LinkedIn jalon

---

## 3 DÉCISIONS CRITIQUES À PRENDRE PAR YOAN

### Décision 1 — PIVOT VERTICAL (issu axe a)

**Question :** garder "humanoïde manuf générique" OU choisir vertical aligné L4 (énergie / alimentation / construction modulaire) ?

**Reco Claude :** **pivot construction modulaire préfab.** Synergie naturelle avec ton expérience construction + chantier3D, marché vide concurrence-wise, narratif fort solo "carpenter qui code le robot du futur de la construction". Énergie/alimentation OK aussi mais moins de leverage personnel.

**Impact :** change le narratif/positionnement public ET la tâche démo (cube neutre → empilage panneau préfab par exemple). Le théorème AIF=NMPC marche pour tout vertical, donc pas d'impact théorique.

### Décision 2 — COMMANDE HARDWARE J+5

**Question :** commander SO-ARM101 J+5 (livraison ~3 sem, arrive ~J+25) ou différer entièrement post-sprint ?

**Reco Claude :** **commander J+5.** Le bras arrive ~J+25, pas le temps de construire dans le sprint, mais prêt pour post-sprint (juin = construction physique + V0.3 hardware). Coût = ~600 CAD engagés. Conditionnel à décision 1 (si pivot vertical change format hardware, attendre).

### Décision 3 — STRATÉGIE DÉFENSIVE IP J+5

**Question :** technical disclosure IP.com (~250 CAD) ?

**Reco Claude :** **OUI.** Coût ridicule vs valeur défensive. Aligné stratégie publication ouverte du pacte. Action J+5 ou J+7 max.

---

## Tokens consommés sprint J+1

- 5 subagents : ~80K total (15-16K chacun)
- + overhead conversation principale : ~30-40K
- **Total estimé J+1 : ~120K** / budget journalier ~400-500K Max plan
- **Reste ~280-380K disponible aujourd'hui** si on continue

---

— *Synthèse Claude Opus 4.7, 2026-04-29.*
