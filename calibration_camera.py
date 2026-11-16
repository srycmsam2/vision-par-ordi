"""
Calibration de la caméra à partir d'images d'un damier.
Projet : Métasurface programmable - LEME

Paramètres issus de la méthodologie du rapport :
- 9 x 6 coins internes
- taille d'un carré : 29 mm

Utilisation :
    python calibration_camera.py
"""

import cv2
import numpy as np
from pathlib import Path

NB_COINS = (9, 6)
TAILLE_CARRE_M = 0.029
DOSSIER_IMAGES = Path("data/Calibration")
DOSSIER_RESULTATS = Path("result")

criteres = (
    cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER,
    30,
    0.001
)

# Coordonnées 3D théoriques des coins du damier, exprimées en mètres.
points_objet_modele = np.zeros(
    (NB_COINS[0] * NB_COINS[1], 3),
    dtype=np.float32
)
points_objet_modele[:, :2] = np.mgrid[
    0:NB_COINS[0], 0:NB_COINS[1]
].T.reshape(-1, 2)
points_objet_modele *= TAILLE_CARRE_M

points_3D = []
points_2D = []
taille_image = None

images = sorted(DOSSIER_IMAGES.glob("*.jpg"))
if not images:
    raise FileNotFoundError(
        f"Aucune image JPG trouvée dans {DOSSIER_IMAGES.resolve()}"
    )

for chemin in images:
    image = cv2.imread(str(chemin))
    if image is None:
        print(f"Image illisible : {chemin}")
        continue

    gris = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    taille_image = gris.shape[::-1]

    trouve, coins = cv2.findChessboardCorners(
        gris,
        NB_COINS,
        None
    )

    if trouve:
        coins_fins = cv2.cornerSubPix(
            gris,
            coins,
            (11, 11),
            (-1, -1),
            criteres
        )

        points_3D.append(points_objet_modele.copy())
        points_2D.append(coins_fins)

        apercu = image.copy()
        cv2.drawChessboardCorners(apercu, NB_COINS, coins_fins, trouve)
        cv2.imshow("Coins du damier detectes", apercu)
        cv2.waitKey(250)
        print(f"Damier detecte : {chemin.name}")
    else:
        print(f"Damier non detecte : {chemin.name}")

cv2.destroyAllWindows()

if len(points_3D) < 3 or taille_image is None:
    raise RuntimeError(
        "Calibration impossible : moins de trois images valides. "
        "Reprenez des images nettes du damier sous différents angles."
    )

erreur, matrice_camera, distorsion, rvecs, tvecs = cv2.calibrateCamera(
    points_3D,
    points_2D,
    taille_image,
    None,
    None
)

DOSSIER_RESULTATS.mkdir(parents=True, exist_ok=True)
np.save(DOSSIER_RESULTATS / "camera_matrix.npy", matrice_camera)
np.save(DOSSIER_RESULTATS / "dist_coeffs.npy", distorsion)

print("\\n===== RESULTATS DE CALIBRATION =====")
print("\\nMatrice caméra K :")
print(matrice_camera)
print("\\nCoefficients de distorsion D :")
print(distorsion)
print(f"Erreur de reprojection renvoyée par OpenCV : {erreur:.5f}")
print(f"Paramètres sauvegardés dans : {DOSSIER_RESULTATS.resolve()}")
