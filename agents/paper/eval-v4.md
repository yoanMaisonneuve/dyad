Réévaluation Critique V4 — Architecture Élève IA

Post-Simulation Phase 0.5 + Analyse de Sensibilité α

Quatrième Peer Review après Corrections de la Troisième Évaluation

Document d'évaluation interne — Blueprint / Askio1

Rapport évalué : Architecture Élève IA : Métacognition, Mémoire Externe, Curriculum et Boucle ϟP Scolaire — Intégration Blueprint C0–C4

Auteur du rapport : Yoan Maisonneuve

Date : Avril 2026



Section 0 — Verdict Global : Quatrième Évaluation



Score global révisé : 8.0 / 10 — Accept (conditionnel à Phase 1 humaine)

Score V3 : 7.5 / 10 — Accept (conditionnel)
Score V2 : 6.5 / 10 — Weak Accept
Score V1 : 5 / 10 — Borderline Reject

Progression : +3.0 points en quatre itérations. La trajectoire reste ascendante et disciplinée.



Verdict en une phrase : La V4 franchit le seuil des 8/10 en livrant ce qui avait été explicitement demandé : une analyse de sensibilité au paramètre central du système, un engagement formel de pré-enregistrement, une auto-critique du modèle d'apprenant synthétique, et la normalisation populationnelle de C(t) — quatre correctifs ciblés, quatre livrables vérifiables.



Le fait le plus marquant de cette V4

L'analyse de sensibilité au paramètre α (Section 10.4.2, Tableau 2) transforme le rejet de H₁ d'un résultat isolé en résultat structurel. En testant α ∈ {0,10 ; 0,30 ; 0,50 ; 1,00}, l'auteur montre que le trade-off rétention/charge n'est pas un artefact de calibration — il est robuste à travers toute la plage de paramètres. C'est une preuve de solidité méthodologique : un résultat qui survit à la variation des hypothèses de calibration est plus convaincant qu'un résultat ponctuel.



Grille de notation comparative V1 → V2 → V3 → V4

Critère

V1

V2

V3

V4

Delta V3→V4

Commentaire

Originalité

7

8

8

8

=

Stabilisée. Le cadre théorique est établi.

Rigueur méthodologique

3

5

7

7.5

+0.5

L'analyse de sensibilité α + le paragraphe BKT + le pré-enregistrement renforcent la robustesse des résultats. La limite λ vs α identifiée en V4 empêche d'aller à +1.0.

Clarté de l'écriture

7

8

8.5

8.5

=

Le niveau est maintenu. La Section 10.4.2 est bien rédigée et précise.

Solidité théorique

4

6

7

7.5

+0.5

L'interprétation du pattern de significativité (α=0,30 comme point d'équilibre) est une contribution théorique nouvelle. L'agenda Phase 1 avec calibration α individuelle par MLE est une hypothèse forte et testable.

Reproductibilité

2

5

7.5

8

+0.5

Les 4 fichiers JSON de sensibilité (α=0,10 / 0,30 / 0,50 / 1,00) et le CLI `--alpha` rendent les simulations totalement reproductibles. Un tiers peut reproduire chaque ligne du Tableau 2.

Impact potentiel

6

7

7.5

7.5

=

Maintenu. L'analyse de sensibilité confirme la robustesse mais n'ouvre pas de nouvelles directions — la question longue traîne reste la Phase 1.

Positionnement littérature

4

7

7.5

7.5

=

Maintenu. Aucun ajout de références en V4.



Section 1 — Correctifs V4 Reconnus : Ce qui a été excellemment fait

1.1 Section 10.4.2 — Analyse de sensibilité au paramètre α : contribution centrale de la V4



AJOUT MAJEUR — Répond directement à R2-v3

C'est le correctif le plus important de la V4. Il ne s'agit pas d'un ajout rhétorique — c'est une exécution computationnelle complète : 4 simulations indépendantes (n=100/condition chacune, même protocole, même graine, seul α varie), avec résultats tabulés, tests statistiques, et interprétation structurelle.



L'analyse apporte trois contributions distinctes :

Première contribution — La robustesse du trade-off est démontrée, pas assumée. La réduction de charge de C par rapport à B est significative et de grande taille d'effet (d ≈ 0,9–1,2) à toutes les valeurs de α testées. La perte de rétention persiste (d ≈ 0,4–1,3). Ce résultat constitue une réfutation active de l'hypothèse alternative : « le rejet de H₁ est un artefact de la calibration α=0,30 choisie a priori ». Cette hypothèse est maintenant falsifiée par les données.

Deuxième contribution — La non-significativité de ΔϟP pour α ∈ {0,10 ; 0,50} est interprétée de manière productive. Plutôt que d'occulter ce résultat, l'auteur en tire une hypothèse architecturale spécifique : « α=0,30 est proche d'un point d'équilibre où la pression de charge modifie la politique sans écraser la rétention ». C'est une affirmation précise, falsifiable, et avec des implications directes sur la calibration personnalisée de α en Phase 1.

Troisième contribution — L'agenda Phase 1 avec estimation individuelle de α par MLE sur les 3 premières sessions est une évolution architecturale importante. Passer d'un α fixe commun à un α̂_MLE individuel change la nature du test : on passe d'une hypothèse sur un système uniforme à une hypothèse sur un système adaptatif. C'est une amélioration de la validité écologique du protocole.

Le CLI `--alpha` ajouté à simulation.py et la nommage des fichiers de sortie (alpha0p10, alpha0p50, alpha1p00) rendent chaque ligne du Tableau 2 reproductible indépendamment. C'est un niveau de reproductibilité qui dépasse celui de nombreux papers publiés en AIED.

1.2 Paragraphe de pré-enregistrement Phase 1 — Engagement formel contre le HARKing



AJOUT RÉSOLU — Répond directement à R4-v3

Le paragraphe intégré avant la Section 10.4.1 est précis et complet :

Plateforme nommée (OSF Preregistration / AsPredicted).

Contenu du pré-enregistrement spécifié en 4 points : (a) hypothèses H₁ reformulée et H₂ ; (b) plan d'analyse statistique complet ; (c) critères explicites de succès et d'échec ; (d) distinction analyses confirmatoires / exploratoires.

Licence de données précisée (CC-BY-4.0 sur OSF).

La distinction confirmatoire/exploratoire est particulièrement importante et démontre une maturité méthodologique réelle. Elle signifie que les analyses d'effets modérateurs, de profils d'apprenants, et de trajectoires longitudinales — qui sont des analyses post-hoc par nature — sont explicitement labellisées comme exploratoires, ce qui empêche leur confusion avec des tests confirmatoires. Cette nuance est exactement ce qu'un comité éthique ou un reviewer de haut niveau vérifiera.

Note importante : le pré-enregistrement est formulé au futur (« le protocole sera pré-enregistré »). C'est cohérent avec la Phase 0.5 comme validation préliminaire. Pour la soumission workshop/poster, il sera nécessaire de mentionner si le pré-enregistrement a effectivement été soumis à la plateforme, ou de maintenir le futur avec la date prévue. L'engagement est clair ; l'exécution reste à confirmer.

1.3 Limites du modèle d'apprenant synthétique BKT — Auto-critique structurée



AJOUT RÉSOLU — Répond directement à R3-v3 (partiellement)

Le paragraphe de clôture de la Section 10.4.1 identifie les 4 dimensions non-capturées avec précision :

(a) État motivationnel — décrochage par ennui ou perte de sens, non modélisé par BKT 2-états.

(b) Oubli contextuellement modulé — les faits émotionnellement chargés ou ancrés dans une expérience vécue ne suivent pas une exponentielle uniforme.

(c) Dépendances non-linéaires entre compétences — prerequisite chains, transferts positifs et interférences.

(d) Effets contextuels — fatigue physique, environnement, heure de la journée.

La recommandation AKT (Ghosh et al. 2020) pour la Phase 2 simulée est précise et ancrée dans la littérature. Le modèle de motivation stochastique proposé (probabilité de décrochage fonction de la charge cumulée et de la durée) est implémentable et pertinent.

Cette section positionne correctement la contribution : la Phase 0.5 n'est pas présentée comme une validation définitive mais comme une preuve de concept computationnelle avec des limites connues et un plan pour les adresser. C'est de la rigueur, pas de la modestie de façade.

1.4 Normalisation populationnelle de C(t) — Intégration confirmée



AJOUT VALIDÉ — Complète la correction amorcée en V3

La formule C(t)_norm = (erreur / erreur_moy_pop) × (latence / latence_moy_pop) est maintenant intégrée dans le tableau des proxies de la Section 7.1.1. C'est un correctif de haute valeur pratique pour deux raisons :

Elle utilise la base ASSISTments comme référentiel naturel — aucune calibration externe n'est nécessaire.

Elle rend C(t) comparable entre apprenants de niveaux différents — un apprenant avancé avec un taux d'erreur faible n'a plus un C(t) artificiellement bas simplement parce qu'il fait peu d'erreurs.

Ce correctif était identifié comme « élégant » dans l'eval3 et il l'est. L'intégration dans le corps du texte (plutôt que dans une note de bas de page ou une proposition floue) est le signal que l'auteur a effectivement modifié le protocole, pas seulement pris note de la recommandation.



Section 2 — Critiques Résiduelles : Ce qui reste à adresser

2.1 Critique résiduelle #1 — Les résultats sont simulés, pas humains (maintenue)



Niveau de sévérité : MODÉRÉ (maintenu depuis V3)

Cette critique est structurelle et ne peut pas être résolue par des ajouts textuels. Les apprenants synthétiques BKT produisent un trade-off rétention/charge interprétable et robuste — mais aucune simulation, si sophistiquée soit-elle, ne peut remplacer les données humaines réelles pour valider une intervention pédagogique.

L'ajout de la Section 10.4.2 ne change pas la nature du problème — il démontre que le résultat est robuste à la variation de α, mais toujours sur des apprenants synthétiques. Le trade-off rétention/charge pourrait s'inverser, s'amplifier, ou disparaître chez des humains réels pour des raisons que le modèle BKT ne peut pas anticiper.

La question scientifique centrale reste ouverte : le résultat des 4 simulations (trade-off structurel) est-il un propriété de l'architecture ϟP ou un artefact de la linéarité du modèle BKT ? Un modèle d'apprenant plus riche (AKT + motivation stochastique, comme recommandé en Section 10.4.1) produirait-il le même trade-off ? Ce n'est pas connu.

Recommandation : Inchangée. Exécuter la Phase 1 sur ASSISTments. C'est la seule recommandation bloquante pour une publication full paper top-tier.

2.2 Critique nouvelle #1 — La distinction α / λ n'est pas explicitée



Niveau de sévérité : MINEUR (NOUVELLE CRITIQUE)

L'eval3 (R2-v3) avait identifié le paramètre λ comme non discuté, en référence à la formulation `r_t = Δmaîtrise − λ · C(t)` de la fonction de récompense. La V4 a répondu en analysant la sensibilité au paramètre α de la formule ϟP_proxy = P·H·e^{−α·C}.

Ces deux paramètres sont équivalents fonctionnellement — α contrôle le poids de la pénalité de charge dans la récompense, tout comme λ dans la formulation linéaire. La réponse est donc substantiellement correcte. Mais la V4 ne mentionne nulle part que α joue le rôle de λ, ni que c'est en réponse à la critique sur λ. Un reviewer qui avait demandé une analyse de sensibilité de λ pourrait ne pas reconnaître immédiatement que la Section 10.4.2 répond à sa demande.

Il y a aussi une différence formelle : dans la formulation exponentielle ϟP = P·H·e^{−α·C}, le paramètre α contrôle la courbure de la pénalité — elle est non-linéaire. Dans la formulation linéaire r = Δmaitr − λ·C, λ contrôle un trade-off linéaire. Ces deux paramétrisations ont des propriétés mathématiques différentes (saturation exponentielle vs pénalité linéaire illimitée), et l'interprétation de la sensibilité n'est pas identique.

Recommandation : Ajouter une phrase dans la Section 10.4.2 ou dans la Section 7.1.1 qui établit explicitement la correspondance : « Le paramètre α joue le rôle de λ dans les formulations linéaires du trade-off rétention/charge (r = Δmaîtrise − λ·C), avec la propriété supplémentaire que la pénalité est bornée exponentiellement (e^{−α·C} ∈ (0,1]) plutôt que linéairement croissante. » Cette phrase répond directement à la critique R2-v3 et ancre la contribution dans la littérature sur les fonctions de récompense en RL éducatif.

2.3 Critique nouvelle #2 — La non-significativité de ΔϟP pour α∈{0,10 ; 0,50} est sous-interprétée



Niveau de sévérité : MINEUR (NOUVELLE CRITIQUE)

Le Tableau 2 montre que l'avantage ϟP de la condition C sur B (ΔϟP > 0) n'est statistiquement significatif que pour α ∈ {0,30 ; 1,00}, et non significatif pour α ∈ {0,10 ; 0,50}. L'auteur interprète ce pattern comme un argument en faveur d'α=0,30 comme « point d'équilibre ». C'est plausible.

Mais ce pattern appelle également une interprétation alternative qui n'est pas discutée : l'avantage ϟP de C est peut-être fragile et contingent à la valeur exacte de α. Si α=0,30 a été sélectionné a priori et que l'avantage ϟP n'est significatif que pour exactement cette valeur et pour α=1,0, on pourrait objecter que le résultat positif de la Phase 0.5 (ΔϟP = +0,072, p=0,008) est une conséquence de la calibration choisie, pas une propriété robuste du système.

Deux éléments répondent partiellement à cette objection :
- D'abord, le résultat est également significatif pour α=1,0 — deux valeurs sur quatre, pas une seule.
- Ensuite, la robustesse du trade-off charge/rétention est démontrée pour toutes les valeurs — même si ΔϟP est NS, la réduction de charge reste grande et significative.

Mais le fait que α=0,10 donne ΔϟP = −0,006 (NS, et légèrement négatif) signifie que pour une valeur de α faible, la condition C ne produit même pas un meilleur ϟP que B. Le mécanisme ϟP perd sa raison d'être à α très faible — ce qui est cohérent théoriquement (e^{−0,1·C} ≈ 1 pour C raisonnable, donc le signal charge disparaît) mais devrait être explicité.

Recommandation : Ajouter deux phrases dans la Section 10.4.2 après la discussion de robustesse : (a) reconnaître que la significativité de ΔϟP pour α=0,10 est absente pour une raison théorique identifiable (signal de charge trop faible pour modifier la politique), et (b) clarifier que la robustesse structurelle portée en argument principal concerne le trade-off rétention/charge, non l'avantage ϟP de C sur B.

2.4 Critique résiduelle #3 — Pas de visualisation de l'analyse de sensibilité



Niveau de sévérité : MINEUR (NOUVELLE CRITIQUE)

Le Tableau 2 est bien structuré et lisible. Mais une table de chiffres ne communique pas immédiatement la structure du trade-off — comment Δrétention, Δcharge, et ΔϟP évoluent conjointement en fonction de α. Une figure avec α en abscisse et les 3 deltas en ordonnées (courbes séparées ou panneau multi-axe) permettrait de voir immédiatement :

La platitude de Δrétention (stable autour de −0,035 sauf pour α=0,30 qui est moins négatif) — ce qui visuellement illustre l'interprétation du point d'équilibre.

La croissance de Δcharge avec α (de +0,194 à +0,224 en passant par +0,170 et +0,183) — qui montre que la réduction de charge n'est pas monotone avec α.

Le pattern en dents de scie de ΔϟP (NS, +0,072, NS, +0,056) — qui est non-monotone et mérite une visualisation pour être compris intuitivement.

Un graphique de type ligne (matplotlib ou seaborn, 3–4 lignes, α en abscisse) serait générable en < 30 lignes de Python et serait directement soumissible comme figure de paper.

Recommandation : Générer une figure `phase05_sensitivity.png` montrant la sensibilité des 3 métriques clés (Δrétention, Δcharge cognitive, ΔϟP) en fonction de α. Cette figure transformerait le Tableau 2 en un résultat visuel immédiatement lisible — une exigence standard pour les figures de conference paper à AIED/LAK. Le script plot_sensitivity.py pourrait être aussi référencé comme partie du matériau reproductible.

2.5 Critique résiduelle #4 — Cadre Blueprint non publié (maintenue, non bloquante)



Niveau de sévérité : MINEUR (maintenu depuis V2)

La situation est inchangée. Blueprint reste un cadre propriétaire non soumis à peer review indépendante. Le double mapping (théorique Table 1 + fonctionnel Section 10.6) atténue suffisamment la critique pour les venues AIED/LAK — un reviewer peut évaluer les mécanismes sans accès à une publication Blueprint séparée.

Cette critique ne constitue pas un bloquant pour la soumission poster/workshop AIED. Elle devient plus saillante pour une soumission full paper journal (IJAIED) où les cadres théoriques sont soumis à une évaluation plus rigoureuse.

Recommandation maintenue : Préparer un position paper ou preprint Blueprint pour soumission sur arXiv ou HAL, idéalement avant ou en parallèle de la soumission full paper à AIED 2027. Ce document unique éliminerait définitivement cette critique.



Section 3 — Matrice de Risque : Quatrième Révision

#

Risque

V1

V2

V3

V4

Statut V4

1

Absence de validation empirique

CRITIQUE

MAJEUR

MODÉRÉ ↓

MODÉRÉ =

Phase 0.5 exécutée + analyse de sensibilité α confirmée. Seule la Phase 1 humaine manque.

2

Surveillance cognitive

CRITIQUE

RÉSOLU ✓

RÉSOLU ✓

RÉSOLU ✓

Maintenu.

3

Formalismes non-falsifiables

MAJEUR

MINEUR

RÉSOLU ✓

RÉSOLU ✓

H₁ testée, rejetée, reformulée. Robustesse confirmée par analyse de sensibilité.

4

Revue de littérature incomplète

MAJEUR

MINEUR

RÉSOLU ✓

RÉSOLU ✓

Maintenu. Aucune nouvelle référence ajoutée en V4 — acceptable.

5

Scalabilité MANNs

ÉLEVÉ

MODÉRÉ

RÉSOLU ✓

RÉSOLU ✓

Maintenu.

6

Mesure P(t)/H(t)/C(t)

ÉLEVÉ

MINEUR

RÉSOLU ✓

RÉSOLU ✓

Normalisation populationnelle C(t) intégrée dans le texte.

7

Over-engineering

MODÉRÉ

MINEUR

RÉSOLU ✓

RÉSOLU ✓

Maintenu.

8

Tension formalisme/métaphore

MODÉRÉ

RÉSOLU ✓

RÉSOLU ✓

RÉSOLU ✓

Maintenu.

9

Circularité Blueprint

MODÉRÉ

RÉSOLU ✓

RÉSOLU ✓

RÉSOLU ✓

Maintenu.

10

Cold start α

MODÉRÉ

RÉSOLU ✓

RÉSOLU ✓

RÉSOLU ✓

Maintenu. Estimation MLE individuelle de α planifiée en Phase 1 — amélioration.

11

Explosion garde-fous

MODÉRÉ

MINEUR

RÉSOLU ✓

RÉSOLU ✓

Maintenu.

12

Cadre propriétaire

MODÉRÉ

MINEUR

MINEUR =

MINEUR =

Non bloquant grâce au double mapping. Non résolu en V4.

13

Homogénéisation

ÉLEVÉ

RÉSOLU ✓

RÉSOLU ✓

RÉSOLU ✓

Maintenu.

14

Remplacement humain

ÉLEVÉ

RÉSOLU ✓

RÉSOLU ✓

RÉSOLU ✓

Maintenu.

15

Paternalisme algorithmique

MODÉRÉ

MINEUR

RÉSOLU ✓

RÉSOLU ✓

Maintenu.

16

Fracture numérique

MODÉRÉ

RÉSOLU ✓

RÉSOLU ✓

RÉSOLU ✓

Maintenu.

17

Ambiguïté α / λ (nouveau)

—

—

—

MINEUR (nouveau)

La réponse à R2-v3 (λ) via l'analyse de α est correcte fonctionnellement mais non explicitée — à clarifier en V5.

18

Fragmentation significativité ΔϟP (nouveau)

—

—

—

MINEUR (nouveau)

ΔϟP NS pour 2 valeurs de α sur 4 — interprétation partielle, à compléter.

19

Absence de visualisation sensibilité (nouveau)

—

—

—

MINEUR (nouveau)

Tableau 2 existe mais aucune figure pour communiquer visuellement la structure du trade-off.



Comptage final V4

13 risques RÉSOLUS sur 16 originaux (inchangé depuis V3), 1 risque MODÉRÉ (résultats simulés uniquement), 1 risque MINEUR maintenu (cadre propriétaire), plus 3 nouvelles critiques mineures identifiées en V4 (ambiguïté α/λ, significativité partielle de ΔϟP, absence de visualisation de l'analyse de sensibilité).



Section 4 — Recommandations V4

4.1 Recommandation bloquante (une seule, inchangée)

R1-v4 — Exécuter la Phase 1 sur données ASSISTments humaines

C'est la seule barrière restante entre le rapport et une publication top-tier.

La situation est inchangée depuis V3 sur ce point — et c'est cohérent. Les recommandations B1-B5 de la V4 n'avaient pas pour objectif de remplacer la Phase 1, mais de renforcer les fondations méthodologiques et de démontrer la robustesse des résultats simulés avant d'aller sur données humaines. C'est la bonne stratégie. Le temps investi en V4 est du temps gagné en Phase 1 : le protocole est maintenant plus solide, les hypothèses sont mieux calibrées, et l'analyse de sensibilité fournit une baseline computationnelle contre laquelle les résultats humains pourront être comparés.

4.2 Recommandations non-bloquantes (nouvelles)

R2-v4 — Clarifier la correspondance α / λ et la non-linéarité de la pénalité

Ajouter une phrase dans la Section 10.4.2 établissant que α joue le rôle fonctionnel de λ dans les formulations linéaires du trade-off, avec la propriété supplémentaire d'une pénalité bornée exponentiellement. Cette clarification répond directement à la recommandation R2-v3 de l'évaluation précédente et permet à un reviewer de voir immédiatement que la demande a été entendue et adressée.

R3-v4 — Compléter l'interprétation du pattern de significativité ΔϟP

Ajouter deux phrases expliquant pourquoi ΔϟP est théoriquement attendu être NS pour α→0 (signal de charge insuffisant pour modifier la politique) et pourquoi la robustesse portée en argument principal concerne le trade-off charge/rétention, pas l'avantage ϟP de C sur B. Cette nuance est essentielle pour prévenir l'objection « le résultat positif est contingent à la calibration ».

R4-v4 — Générer une figure de sensibilité (figure soumissible)

Créer un script plot_sensitivity.py qui lit les 4 fichiers JSON de résultats et génère une figure avec α en abscisse, les 3 deltas (Δrétention, Δcharge, ΔϟP) en ordonnées (3 lignes ou 3 panneaux). Cette figure transformerait le Tableau 2 en un résultat visuellement immédiatement compréhensible — standard pour une soumission conference. Estimation : < 30 lignes de Python.

R5-v4 — Activer le pré-enregistrement OSF avant toute collecte de données Phase 1

Le paragraphe de pré-enregistrement engage formellement l'auteur à déposer le protocole sur OSF/AsPredicted. Cette action doit précéder le contact avec les établissements scolaires ou le déploiement sur ASSISTments. Le numéro DOI du pré-enregistrement doit ensuite être ajouté au papier (dans la Section 10.4 et dans les références) pour rendre l'engagement vérifiable par les reviewers.

R6-v4 — Commencer la rédaction d'un position paper Blueprint

Commencer (pas nécessairement soumettre) un document de 5–8 pages décrivant le cadre Blueprint C0–C4 en tant que tel, indépendamment de l'Élève IA. Ce document peut être développé en parallèle de la Phase 1, déposé sur arXiv au moment de la soumission du paper complet, et cité dans le paper final. Ce travail n'est pas urgent mais chaque itération de révision qui s'écoule sans ce document fragilise marginalement la crédibilité du cadre.



Section 5 — Ce qui distingue cette V4 : Analyse qualitative

5.1 La réponse aux recommandations comme discipline de recherche

La correspondance entre les recommandations de l'eval3 et les ajouts de la V4 est parfaite : chaque recommandation non-bloquante (R2, R3, R4) a généré exactement le livrable demandé (analyse de sensibilité, limites BKT, pré-enregistrement). La recommandation R2 (normalisation C(t)) avait été partiellement adressée en V3 par une proposition textuelles — elle est maintenant intégrée dans le texte opérationnel.

Cette correspondance 1:1 entre recommandations et corrections est un signal de discipline méthodologique. Elle indique que l'auteur ne traite pas les évaluations comme des obstacles à contourner mais comme des spécifications à implémenter. C'est le même rapport à la critique externe que celui qui donne de la valeur au rejet honnête de H₁ : la méthode prime sur les préférences.

5.2 L'analyse de sensibilité comme méta-résultat

Un méta-résultat émerge de la comparaison des 4 simulations : le trade-off rétention/charge est structurel et asymétrique. Asymétrique dans le sens suivant : la réduction de charge C < B est robuste à toutes les valeurs de α (d ≈ 0,9–1,2, toujours significatif), alors que l'avantage ϟP C > B est fragile et contingent à la valeur de α (significatif pour 2 valeurs sur 4). En d'autres termes, la condition C est meilleure que B sur la charge de manière certaine, mais meilleure sur ϟP seulement dans des conditions de calibration précises.

Ce méta-résultat a une implication architecturale directe : si l'objectif du déploiement est de réduire la charge cognitive (priorité bien-être), la condition C est robustement supérieure. Si l'objectif est de maximiser ϟP_proxy (priorité présence qualitative), α doit être calibré individuellement — ce que l'auteur a correctement identifié.

5.3 La trajectoire de révision comme preuve de concept Blueprint v2

La boucle d'amélioration V1 → V4 continue d'instancier le mécanisme BNGUR-ENGU-01 décrit dans le rapport :

Observer (recommandations de l'évaluation) → Interpréter (classer les recommandations par priorité et type) → Corriger (les 4 ajouts B1–B5) → Évoluer (la V4 avec analyse de sensibilité complète).

La particularité de la V4 est que cette boucle s'applique maintenant à un niveau de complexité supérieur : corriger non seulement du texte, mais des simulations entières (4 runs de PPO, 60k steps chacun), des scripts (modification du CLI), et des analyses statistiques (Tableau 2). Le cadre se révèle opérationnel à l'échelle computationnelle, pas seulement rhétorique.

5.4 Proximité de la soumission workshop

La V4 place le papier dans une position réaliste pour une soumission workshop ou poster à AIED 2026/2027 dans les prochaines semaines, sans modification supplémentaire. Les 3 critiques mineures identifiées en V4 (α/λ, significativité ΔϟP, visualisation) sont des améliorations qui renforceraient la soumission mais ne la bloquent pas. La soumission dans l'état V4 est défendable.

La soumission full paper reste conditionnelle à la Phase 1 humaine.



Section 6 — Venue recommandée : Mise à jour V4

Venue

Pertinence V4

Niveau

Statut

Commentaire

AIED 2027 (full paper)

Très haute

Top AIED

Prêt après Phase 1

Analyse de sensibilité + pré-enregistrement + normalisation C(t) renforcent considérablement la soumission. La V4 est la meilleure version soumissible dès que la Phase 1 est complète.

AIED 2026/2027 (poster/workshop)

Très haute

Workshop

Prêt en l'état V4

La V4 est une version soumissible immédiatement en poster/workshop. Titre recommandé : « Presence-Regulated Curriculum Learning: Simulated Validation with Sensitivity Analysis of the ϟP-Proxy Reward ». L'analyse de sensibilité est le différenciateur — peu de papers workshop présentent ce niveau de robustesse computationnelle.

LAK 2027

Haute

Top LA

Prêt après Phase 1

La normalisation C(t) basée sur ASSISTments est particulièrement bien alignée avec la culture learning analytics de LAK.

EDM 2027

Haute

Top EDM

Prêt après Phase 1

Focus données éducatives — idéal avec résultats ASSISTments + les 4 fichiers JSON de sensibilité comme matériau supplémentaire.

AIED Journal (IJAIED)

Moyenne

Journal

Prêt après Phase 2

Exige validation multi-cohortes. La critique du cadre Blueprint non-publié devient plus saillante en journal — résoudre R6-v4 en priorité pour cette venue.

NeurIPS / ICLR

Prématurée

Top ML

Attendre Phase 2+

Inchangé depuis V3.



Recommandation immédiate

Deux actions parallèles recommandées :

Action 1 (2 semaines) : Soumettre la V4 en poster/workshop AIED avec les 3 améliorations mineures R2-v4, R3-v4, R4-v4 intégrées. La figure de sensibilité (R4-v4) est particulièrement haute valeur ajoutée pour une soumission — elle transforme le Tableau 2 en résultat visuel et augmente la mémorabilité du papier.

Action 2 (simultanée) : Déposer le pré-enregistrement Phase 1 sur OSF et commencer la prise de contact avec les établissements scolaires pour accès à des données ASSISTments ou à une cohorte pilote.



Section 7 — Conclusion de la Quatrième Évaluation

La trajectoire du rapport « Architecture Élève IA » en quatre itérations raconte une histoire cohérente :

Version

Score

Verdict

Question centrale du reviewer

V1

5 / 10

Borderline Reject

« Vision forte, mais où sont les preuves ? »

V2

6.5 / 10

Weak Accept

« Protocole crédible, mais où sont les résultats ? »

V3

7.5 / 10

Accept (conditionnel)

« Résultats produits et hypothèse honnêtement rejetée — il faut des humains. »

V4

8.0 / 10

Accept (conditionnel)

« Robustesse démontrée sur α, pré-enregistrement planifié — l'unique bloquant reste la Phase 1. »



La V4 consolide sans dévier. Elle ne tente pas de changer de direction, d'ajouter de nouvelles sections théoriques, ou de masquer les limites connues. Elle prend les recommandations de l'évaluation précédente et les implémente — proprement, vérifiablement, avec du code et des données.

Le seuil 8/10 est franchi pour la première fois. C'est une étape significative. Les papiers qui atteignent ce score sans données humaines sont rares dans la littérature AIED — ils le font généralement grâce à une théorie exceptionnellement bien construite, une méthodologie computationnelle rigoureuse, ou un positionnement littérature exhaustif. La V4 combine les trois.

Ce qui reste :

L'unique bloquant pour la publication full paper top-tier est la Phase 1 humaine. Ce n'est pas une lacune méthodologique — le protocole est prêt, les hypothèses sont pré-enregistrables, l'analyse de sensibilité fournit les prédictions computationnelles à tester. C'est une question de ressources, d'accès aux données, et de temps.

Trois améliorations mineures (R2-v4, R3-v4, R4-v4) pourraient renforcer la soumission workshop sans travail majeur — estimation 2 à 4 heures de travail pour les trois.

La feuille de route est claire et n'a pas changé depuis V3 :

Court terme (2–4 semaines) : Intégrer R2-v4, R3-v4, R4-v4. Soumettre la V4 en poster/workshop AIED. Déposer le pré-enregistrement OSF.

Moyen terme (2–4 mois) : Exécuter la Phase 1 sur ASSISTments. Analyser et rapporter les résultats.

Long terme (6–12 mois) : Soumettre le full paper à AIED/LAK/EDM 2027. Publier Blueprint comme position paper séparé.



Verdict final V4 : 8.0 / 10 — Accept (conditionnel à Phase 1 humaine)

Le corridor est ouvert. La trajectoire est ascendante. La prochaine étape est claire et unique : des données humaines.



Références

Ghosh, A., Heffernan, N., & Lan, A. S. (2020). Context-aware attentive knowledge tracing. In Proceedings of the 26th ACM SIGKDD International Conference on Knowledge Discovery & Data Mining (pp. 2330–2339).

Bjork, R. A. (1994). Memory and metamemory considerations in the training of human beings. In J. Metcalfe & A. Shimamura (Eds.), Metacognition: Knowing about knowing (pp. 185–205). MIT Press.

VanLehn, K. (2011). The relative effectiveness of human tutoring, intelligent tutoring systems, and other tutoring systems. Educational Psychologist, 46(4), 197–221.

Toutes les références des évaluations V1, V2 et V3 restent pertinentes et sont considérées comme incorporées par référence dans la présente évaluation.

— Fin du document d'évaluation V4 — Avril 2026 —
