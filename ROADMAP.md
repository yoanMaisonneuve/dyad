# ROADMAP — Backlog vivant

> Liste des projets actifs avec triage P1–P5, prochaine action, échéance, bénéficiaire. Mis à jour à chaque fin de session après mise à jour de `HEARTBEAT.md`. Pour la vision → `VISION.md`. Pour l'état courant → `HEARTBEAT.md`.

---

## Critères de triage

| Code | Délai max | Critère structurel | Allocation tokens (% jour) |
|---|---|---|---|
| **P1** | 24–72 h | Fenêtre fixe + irréversible si manquée | Plafond 60 %, premier servi |
| **P2** | 1 semaine | Fenêtre courte + impact élevé | Plafond 30 %, quota min 10 % |
| **P3** | 1 mois | Important + fenêtre normale | Plafond 20 %, quota min 10 % |
| **P4** | 3 mois | Utile + pas pressé | Plafond 10 %, quota min 5 % |
| **P5** | > 3 mois ou opportuniste | Exploration | Plafond 5 %, quota min 0 % |

**Critères qui font monter en priorité :** deadline fixe externe · irréversibilité · impact couche 9 · bénéficiaire externe identifié · risque de self-erasing du pacte.

**Plafond par tâche unique :** aucune tâche ne consomme plus de **40 %** du budget journalier (~200K sur ~500K). Si une tâche déborde → la découper.

---

## P1 — En cours, fenêtre courte, irréversible si manquée

### **F1 — Preprint arxiv : Équivalence inférence active / contrôle moteur prédictif**
- **Échéance :** 2026-07-27 (89 jours restants au 2026-04-29)
- **Bénéficiaire :** chercheurs Friston / active inference + futurs lecteurs académiques + héritage track parental (couche 9)
- **État :** matière brute en place — `CyborgV0.1` (démo bras 2D) + `INFERENCE-ACTIVE-RECHERCHE.md` (recherche en cours). Outline + formalisation à faire.
- **Prochaine action :** outline complet du paper (sections, hypothèse principale, plan formalisation) — ~30K tokens
- **Dépendances :** aucune
- **Risque si manqué :** foresight F1 brisée publiquement → casse partielle de la crédibilité du pacte

### **Pacte LinkedIn — 2-3 posts / semaine**
- **Échéance :** rolling, fenêtre hebdo
- **Bénéficiaire :** lecteurs LinkedIn + autres solo founders + track parental (couche 9)
- **État :** post #1 manifeste publié 2026-04-28. Cible : 50–75 posts sur 6 mois.
- **Prochaine action :** rédiger post #2 — méta-post sur le frame *« LinkedIn = carnet de notes »*, ou foresight industrie courte — ~5K tokens
- **Risque si manqué :** voix de disqualification regagne du terrain (self-erasing)

### **Clause candidature — 2-3 postes IA / semaine**
- **Échéance :** rolling, fenêtre hebdo
- **Bénéficiaire :** sa famille (sortir du chantier vers IA) + couche 9 (héritage cohérent)
- **État :** CV PDF généré 2026-04-29. 0 candidature envoyée.
- **Prochaine action :** envoyer 1ère candidature (poste Agent / LLM Engineer junior–mid) — ~10K tokens (identifier offre + adapter CV + lettre courte)
- **Dépendances :** matchllm publié sur GitHub (P2) — pour crédibilité des chiffres CV
- **Risque si manqué :** clause 5 du pacte cassée

---

## P2 — Cette semaine, débloquant pour P1

### **SPRINT ROBOTIQUE HUMANOÏDE — 30 jours (J+1 = 2026-04-30 → J+28 = 2026-05-27)**
- **Échéance :** J+28 = 2026-05-27
- **Bénéficiaire :** future équipe robotique solo + lecteurs preprint F1 + écosystème deep tech Québec + Institut St-Laurent + héritage couche 9 (enfants)
- **État :** validé 2026-04-29. Setup en cours. J+1 = lancement 5 subagents mode déléguée.
- **Stratégie complète :** `personnel/objectifopus47.md`
- **Tracker quotidien :** `personnel/SPRINT-ROBOTIQUE.md`
- **7 livrables cibles :** repo cyborg-robotique-V1.0 (sim 3D + inférence active) | spec hardware PDF buildable solo | plan partenariat lab (3 identifiés + 1 demande envoyée) | note fundraise (3 pistes) | note antériorité+IP | 12 posts LinkedIn | publication via `La_vallee_du_St_Laurent`
- **Budget tokens :** ~4-5M sur 28 jours (~30 % Max plan) — quota minimum garanti P1 résiduel : 15-20 %/jour pour pacte + candidatures
- **Cible structurelle :** migration ROADMAP robotique humanoïde P5 → P3 à J+28
- **Risque si manqué :** zone d'ombre du ROADMAP reste P5 indéfiniment, mission L4 reste prose

### **matchllm — Publication GitHub publique**
- **Échéance :** cette semaine (cible 2026-05-04)
- **Bénéficiaire :** autres solo agent builders + recruteurs IA évaluant le CV + diffusion des champs directionnels comme méthode
- **État :** code prêt (7 100 lignes, 49/49 tests, benchmark mesuré). README + docs à finaliser.
- **Prochaine action :** audit final repo + README polish + LICENSE + push public — ~50K tokens
- **Dépendances :** aucune
- **Bloque :** crédibilité du CV → clause candidature P1

### **Vidéo NotebookLM — Rapport 6 enveloppes**
- **Échéance :** cette semaine
- **Bénéficiaire :** lecteurs/auditeurs + populations touchées par les 6 enveloppes (femmes, autodidactes, career changers, immigrants)
- **État :** rapport rédigé `culture-d-entreprise/rapports/voix-de-disqualification-6-enveloppes.md` (~6 500 mots).
- **Prochaine action :** uploader dans NotebookLM → générer audio overview → habillage vidéo si désiré → publier — ~0 tokens (manuel)
- **Dépendances :** aucune

---

## P3 — Ce mois, important, profondeur

### **cyborg-yoan V0.1 — bootstrap.py interactif**
- **Échéance :** mai 2026
- **Bénéficiaire :** Yoan lui-même (mémoire externe portable utilisable) + futurs utilisateurs si publié
- **État :** squelette V0.0. 4 organes en place. `yoan.md` vide (réservé au bootstrap V0.1).
- **Prochaine action :** coder `bootstrap.py` avec 7 questions interactives → premier `yoan.md` généré — ~40K tokens
- **Dépendances :** aucune

---

## P4 — Trimestre, utile, pas pressé

### **CyborgV0.1 — Extension 3D / sim physique**
- **Bénéficiaire :** matière du preprint F1 (validation empirique étendue de l'équivalence)
- **État :** démo 2D fonctionnelle. Extension 3D = nouvelle codebase.
- **Prochaine action :** spécifier scope V0.2 (3D ? PyBullet ? autre simulateur ?)
- **Notes :** seulement si F1 preprint demande validation expérimentale étendue. Sinon optionnel.

### **Cyborg framework — Installation Blueprint-memory**
- **Bénéficiaire :** repo Blueprint-memory (test du hook vocal SessionStart en conditions réelles)
- **État :** template prêt. Install scripté.
- **Prochaine action :** lancer `cyborg-install.ps1` depuis `Blueprint-memory/` — ~5K tokens
- **Notes :** test rapide quand on a une fenêtre P4.

---

## P5 — Long terme / opportuniste

### **Enter-Game V2 / publication étendue**
- **Bénéficiaire :** fondateurs solo
- **État :** V1 livré (7 Protocol Documents + Jouer.html). V2 = pas spécifié.
- **Notes :** revisiter quand un signal externe (demande utilisateur, opportunité) apparaît.

### **Robotique humanoïde manufacturière**
- **Bénéficiaire :** humanité long terme + couche 9
- **État :** vision. **SPRINT ACTIF 2026-04-30 → 2026-05-27 (cf. P2 sprint robotique).** Migration P5→P3 prévue J+28 si livrables atteints.
- **Notes :** devient P1 quand un jalon concret apparaît (prototype mécanique buildable, partenariat lab, fundraise possible) — c'est exactement ce que le sprint construit.

---

## Modes de session

| Mode | Quand | Allocation |
|---|---|---|
| **Focused** | Une seule grosse pièce (preprint outline, audit code) | 1 tâche P1/P2, 1 session entière (~80–100K) |
| **Déléguée** | Plusieurs petits livrables | 3–5 subagents en parallèle, mix P1/P2/P3 (~80K total) |
| **Réserve** | Surplus / exploration | P4-P5 opportuniste |

Yoan déclare le mode au démarrage de session : *« mode focused sur preprint »* / *« mode déléguée, brûle les P1 du jour »* / *« réserve, on explore »*.

---

## Fonction d'allocation tokens par session

```
budget_session ≈ 80–100K tokens (Max plan)
budget_jour ≈ 400–500K tokens (5 sessions)

allocation_priorité_décroissante : P1 → P2 → P3 → P4 → P5
plafond_par_tâche = 40 % × budget_jour
quota_minimum_garanti = {P3: 10 %, P4: 5 %}

si tokens_restants < seuil → bascule en mode réserve / fin de session
```

À chaque fin de session, mettre à jour `HEARTBEAT.md` avec les tokens consommés par projet, recalculer le solde de la journée, ajuster la prochaine session.

---

## Règle de vigilance (maxime #005)

**Chaque tâche listée ici doit avoir un bénéficiaire externe identifié.** Si un projet n'a pas de bénéficiaire — pas même Yoan lui-même au sens utile — il dégage du ROADMAP, peu importe sa sophistication technique.

Architecture économe par défaut. Mode challenge activable par Yoan : *« est-ce vraiment utile ou est-ce que ça remplit la fenêtre ? »*.

---

## Règle archive (énoncée 2026-04-29 ~03h45)

**Archive jamais n'efface.** Tout fichier obsolète est déplacé vers `_archive/AAAA-MM/` avec une note datée (statut, action originale, contenu reconstruit ou pointer vers remplaçant). Aucune suppression directe. Le geste d'effacer est la version externe de la voix de disqualification — il efface le track au lieu de le préserver.

À évaluer : inscrire comme **maxime #006** dans `culture-d-entreprise/maximes.md` ?

---

## Projets GitHub publics non encore intégrés au triage (audit 2026-04-29)

L'audit cloud (`gh repo list yoanMaisonneuve`) a révélé 4 repos publics qui n'étaient pas dans le ROADMAP. À intégrer prochaine session avec triage P1-P5 + bénéficiaire externe :

| Repo | Description | Lien probable |
|---|---|---|
| `askio1-v2` | Système cognitif augmenté multi-agent avec Mémoire Externe Auto-construite (MEA) | Probablement = `matchllm V0.2`. À vérifier. Si oui, **débloque immédiatement la crédibilité du CV** (chiffres référençables URL publique). |
| `askio1-navi` | Agent autonome multimodal d'ASKIO1 — système de navigation directionnelle | Branche dérivée d'Askio1, à classer P3 ou P4 |
| `La_vallee_du_St_Laurent` | Institut St-Laurent — Think Tank AGI, robotique humanoïde et corridor Vallée du Saint-Laurent | **Directement lié couche 6 (mission civilisationnelle)**. Probable P3 long terme. |
| `StarSparkSeries` | Jack Spark — Les Portails d'Elon : bible de série SF (pitch, synopsis, personnages, lore) | Projet créatif. Probable P5 (opportuniste). |

**Action prochaine session :** triage de ces 4 projets + ajustement du ROADMAP.

---

— *Maintenu par Yoan + Claude. Lu et mis à jour à chaque session.*
