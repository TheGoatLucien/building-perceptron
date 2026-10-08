# building-perceptron

## Contexte et objectif

Projet pédagogique du MSc IA & Data de La Plateforme : développer en Python
une classe `Perceptron`, comprendre son apprentissage et l'appliquer à une
classification binaire. Il s'agit de distinguer les diagnostics bénins et malins
du jeu Breast Cancer Wisconsin (Diagnostic), et non de créer un outil médical.

## Livrables

- [perceptron.py](perceptron.py) : classe développée avec NumPy, sans utiliser le perceptron de scikit-learn.
- [eda.ipynb](eda.ipynb) : **seul notebook de rendu**, avec introduction, EDA, préparation, modélisation, tests AND/XOR, simulations, interprétations et conclusion.
- [Slide/building_perceptron.pptx](Slide/building_perceptron.pptx) : présentation de 15 diapositives, avec notes pour l'oral.
- [Slide/building_perceptron.pdf](Slide/building_perceptron.pdf) : version PDF des diapositives.
- [doc/Building_Perceptron_reponses.pdf](doc/Building_Perceptron_reponses.pdf) : réponses théoriques, exportées sans réécriture du contenu.
- Dossier `doc/` : énoncé et document Word original conservé.

Les expériences de l'ancien notebook de tests ont été intégrées dans la section 7
du notebook unique. Le fichier original a été sauvegardé hors du dépôt, sans
supprimer son contenu. Les scripts du dossier `Slide/` servent uniquement à
vérifier le notebook et à produire les livrables; ils ne sont pas des notebooks
supplémentaires.

Le dépôt public est [TheGoatLucien/building-perceptron](https://github.com/TheGoatLucien/building-perceptron).
Les modifications locales doivent être commitées puis poussées pour mettre le
rendu en ligne; la présence du dépôt public ne publie pas automatiquement les
fichiers locaux.

## Données et analyse

Les données sont chargées directement avec `sklearn.datasets.load_breast_cancer`.
Elles contiennent 569 observations, 30 mesures numériques de noyaux cellulaires
issus de prélèvements de masses mammaires, et un diagnostic connu.
Les mesures comprennent des valeurs moyennes, des erreurs standard et des
valeurs extrêmes (`worst`). Le notebook inverse le codage de scikit-learn :
`0 = bénigne`, `1 = maligne`.

Les contrôles ne trouvent ni valeur manquante ni ligne dupliquée. Aucune
imputation ni suppression n'est donc justifiée par ces contrôles. Les points
atypiques des boxplots ne sont pas supprimés automatiquement : ils peuvent
représenter des observations réelles, pas des erreurs.

Les classes sont modérément déséquilibrées : 357 cas bénins (62,7 %) et
212 cas malins (37,3 %). Le rayon moyen et les points concaves moyens présentent
une séparation plus nette que la texture moyenne dans les trois exemples
visualisés. Ce choix illustre les distributions, sans constituer une sélection
des trois meilleures variables. Certaines mesures, notamment de taille, sont
fortement corrélées. Une corrélation ne démontre pas une causalité.

## Méthode et outils

1. Exploration : pandas pour les tableaux, Seaborn et Matplotlib pour les visuels.
2. Préparation : séparation stratifiée 80/20 avec `random_state=42` (455 exemples d'apprentissage, 114 de test).
3. Standardisation : `StandardScaler` ajusté uniquement sur l'apprentissage; la cible n'est pas standardisée.
4. Compression optionnelle : ACP ajustée sur l'apprentissage standardisé, seuil de variance expliquée de 95 %.
5. Modélisation : perceptron maison (`learning_rate=0.01`, `n_epochs=50`), avec et sans ACP.
6. Comparaison : régression logistique scikit-learn avec et sans ACP, sur le même test.
7. Évaluation : accuracy, précision, rappel, F1 et matrices de confusion; attention particulière aux faux négatifs malins.

Le perceptron calcule un score linéaire, applique un seuil à zéro, puis corrige
ses poids et son biais lorsqu'il se trompe. Il ne garantit pas une convergence
sans erreur lorsque les classes ne sont pas linéairement séparables.

La section 7 valide AND, explique l'échec attendu de XOR et distingue
l'apprentissage du test sur des nuages simulés séparés (accuracy test de 100 %).
Elle compare aussi trois taux d'apprentissage : avec cette initialisation à zéro
et un taux positif constant, les courbes se superposent sur les deux expériences.
Cela ne démontre pas que le taux est sans effet dans tous les algorithmes.

## Résultats et conclusion

Sur la séparation décrite ci-dessus, l'ACP retient 10 composantes sur 30 et
conserve environ 95,2 % de la variance. Cela ne signifie pas 95,2 % de précision
diagnostique : les composantes sont des combinaisons des mesures, pas une
sélection directe de colonnes.

| Modèle | Accuracy | Rappel malin | Cas malins manqués | Fausses alertes |
| --- | ---: | ---: | ---: | ---: |
| Perceptron sans ACP | 94,7 % | 90,5 % | 4 | 2 |
| Perceptron avec ACP | 97,4 % | 95,2 % | 2 | 1 |
| Régression logistique sans ACP | 96,5 % | 92,9 % | 3 | 1 |
| Régression logistique avec ACP | 97,4 % | 92,9 % | 3 | 0 |

L'ACP améliore ici le perceptron tout en réduisant la dimension. Les deux modèles
avec ACP ont la même accuracy mais des erreurs différentes : le rappel malin
permet de les distinguer. Ce résultat reste exploratoire : un seul tirage, peu
d'observations et une EDA ayant examiné l'ensemble du jeu ne permettent pas de
conclure à une supériorité générale ni à une fiabilité clinique. La suite serait
une validation croisée sur l'apprentissage pour choisir les réglages, puis un
test final non consulté pendant le développement.

## Reproduire le travail

Python 3.12 a été utilisé. Depuis la racine du dépôt, sous PowerShell :

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install numpy pandas matplotlib seaborn scikit-learn ipykernel
```

Ouvrir `eda.ipynb` dans VS Code avec les extensions Python et Jupyter, sélectionner
le noyau `.venv`, puis exécuter toutes les cellules de haut en bas. Le chargement
scikit-learn ne nécessite pas de CSV local. Les versions de bibliothèques peuvent
entraîner de petites différences de résultats.

Pour vérifier les 19 cellules de code dans un processus neuf et régénérer les
figures utilisées dans les diapositives :

```powershell
.\.venv\Scripts\python.exe Slide\generer_visuels.py
```

Les tâches VS Code fournies automatisent cette vérification et la création des
diapositives. Le générateur PowerPoint nécessite Windows et Microsoft PowerPoint.
Les PPTX/PDF livrés restent consultables sans exécuter les générateurs.

Pour régénérer les livrables PDF et PowerPoint, installer aussi les dépendances
de conversion et utiliser la tâche de génération, ou les commandes suivantes :

```powershell
.\.venv\Scripts\python.exe -m pip install python-docx reportlab pypdf
powershell -NoProfile -ExecutionPolicy Bypass -File Slide\generer_livrables.ps1
```

Le PDF des réponses est une remise en page du document Word, avec ses textes,
ses caractères mathématiques et ses deux tableaux. La pagination peut différer
de Word. L'export vérifie que les 129 blocs de texte se retrouvent dans le PDF et
que le fichier Word n'a pas changé. Il ne réécrit pas les réponses ni ne valide
leur exactitude théorique.

## Bibliographie

- Rosenblatt, F. (1958). *The Perceptron: A Probabilistic Model for Information Storage and Organization in the Brain*. Psychological Review, 65(6), 386-408. https://doi.org/10.1037/h0042519
- UCI Machine Learning Repository. *Breast Cancer Wisconsin (Diagnostic)*. https://doi.org/10.24432/C5DW2B
- scikit-learn. Chargement et description du jeu : https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_breast_cancer.html
- scikit-learn. Standardisation : https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html
- scikit-learn. ACP : https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html
- scikit-learn. Mesures d'évaluation : https://scikit-learn.org/stable/modules/model_evaluation.html
- scikit-learn. Régression logistique : https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html
