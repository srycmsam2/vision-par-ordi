# Vision par ordinateur — Localisation d'une cible par marqueurs ArUco

Ce dépôt présente une sélection d'exemples de code Python illustrant la chaîne de vision par ordinateur développée dans le cadre du projet de stage **« Métasurface programmable pour le guidage d'une machine mobile en entrepôt par vision par ordinateur »**, réalisé au LEME.

L'objectif de cette partie est d'extraire la position d'une cible à partir d'images fournies par une caméra, puis d'estimer sa position tridimensionnelle par rapport à celle-ci.

> **Périmètre de publication :** ce dépôt contient des exemples pédagogiques sélectionnés et réorganisés pour présenter la méthodologie. Il ne constitue pas une copie intégrale du code du laboratoire. Les résultats expérimentaux, paramètres internes, données et scripts de commande non autorisés ne sont pas inclus.

## Organisation

```text
vision-par-ordinateur/
├── acquisition_images.py
├── calibration_camera.py
├── detection_aruco.py
├── requirements.txt
├── .gitignore
└── README.md
```

## 1. Acquisition des images

Le script `acquisition_images.py` ouvre la caméra et permet d'enregistrer des images d'un damier de calibration sous différentes orientations et positions dans le champ de vision.

- Appuyer sur **Espace** pour enregistrer une image.
- Appuyer sur **Échap** pour quitter.
- Les images sont enregistrées dans `data/Calibration/`.

Il est recommandé de varier l'inclinaison et la position du damier afin de disposer d'observations suffisamment diversifiées.

## 2. Calibration de la caméra

Le script `calibration_camera.py` exploite les images acquises pour :

1. détecter les coins internes du damier ;
2. affiner leur localisation ;
3. associer les coordonnées image aux coordonnées géométriques connues ;
4. calculer la matrice intrinsèque de la caméra et les coefficients de distorsion ;
5. sauvegarder les paramètres dans `result/`.

Paramètres utilisés dans la méthodologie présentée :

| Paramètre | Valeur |
|---|---:|
| Coins internes | 9 × 6 |
| Taille d'un carré | 29 mm |

Les fichiers `camera_matrix.npy` et `dist_coeffs.npy` sont générés localement et ne sont pas versionnés.

## 3. Détection ArUco et estimation de pose

Le script `detection_aruco.py` utilise les paramètres de calibration pour détecter les marqueurs et estimer leur pose par rapport à la caméra.

| Paramètre | Valeur |
|---|---|
| Dictionnaire | `DICT_6X6_50` |
| Taille du marqueur | 79 mm |
| Grandeurs estimées | X, Y, Z et angle horizontal θ |

La position est exprimée en mètres. L'angle horizontal est calculé à partir des coordonnées estimées avec `atan2(X, Z)`.

## Installation

Python 3 et les bibliothèques suivantes sont nécessaires :

```bash
pip install -r requirements.txt
```

## Exécution

Lancer les scripts dans cet ordre depuis la racine du dépôt :

```bash
python acquisition_images.py
python calibration_camera.py
python detection_aruco.py
```

La calibration doit être réalisée avant la détection 3D, car le troisième script charge les paramètres enregistrés par le deuxième.

## Limites et précautions

- Ces scripts sont des exemples de démonstration et peuvent nécessiter une adaptation à la caméra, au système d'exploitation et à la version d'OpenCV utilisés.
- La précision de l'estimation dépend notamment de la qualité des images, de la calibration et de la taille réelle du marqueur.
- Les fichiers de calibration sont générés localement et doivent correspondre à la caméra utilisée.
- Vérifier les droits de publication et l'accord du laboratoire avant de partager tout code, image, résultat ou information technique issue du stage.

## Contexte

Projet de stage réalisé au Laboratoire d'Électronique et des Matériaux pour l'Énergie (LEME), Université Paris Nanterre.

**Sujet :** Métasurface programmable pour le guidage d'une machine mobile en entrepôt par vision par ordinateur.
