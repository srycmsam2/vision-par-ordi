"""
Détection des marqueurs ArUco et estimation de leur pose 3D.
Projet : Métasurface programmable - LEME

Dictionnaire : DICT_6X6_50
Taille du marqueur : 79 mm

Prérequis :
    Exécuter calibration_camera.py pour générer les fichiers .npy.

Utilisation :
    python detection_aruco.py
"""

import cv2
import numpy as np
import math
from pathlib import Path

FICHIER_K = Path("result/camera_matrix.npy")
FICHIER_D = Path("result/dist_coeffs.npy")

if not FICHIER_K.exists() or not FICHIER_D.exists():
    raise FileNotFoundError(
        "Paramètres de calibration introuvables. "
        "Exécutez d'abord calibration_camera.py."
    )

matrice_camera = np.load(FICHIER_K)
distorsion = np.load(FICHIER_D)

TAILLE_MARQUEUR_M = 0.079
dictionnaire = cv2.aruco.getPredefinedDictionary(
    cv2.aruco.DICT_6X6_50
)
parametres = cv2.aruco.DetectorParameters()

# API récente (OpenCV récent) ou API historique.
if hasattr(cv2.aruco, "ArucoDetector"):
    detecteur = cv2.aruco.ArucoDetector(dictionnaire, parametres)
else:
    detecteur = None

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise RuntimeError("Impossible d'ouvrir la caméra.")

print("Détection ArUco en cours - ECHAP pour quitter")

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Erreur lors de la lecture de la caméra.")
            break

        gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if detecteur is not None:
            coins, identifiants, refuses = detecteur.detectMarkers(gris)
        else:
            coins, identifiants, refuses = cv2.aruco.detectMarkers(
                gris,
                dictionnaire,
                parameters=parametres
            )

        if identifiants is not None and len(identifiants) > 0:
            cv2.aruco.drawDetectedMarkers(frame, coins, identifiants)

            rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(
                coins,
                TAILLE_MARQUEUR_M,
                matrice_camera,
                distorsion
            )

            for i, identifiant in enumerate(identifiants.flatten()):
                rvec = rvecs[i]
                X, Y, Z = tvecs[i][0]

                # Angle horizontal par rapport à l'axe optique.
                theta_deg = math.degrees(math.atan2(X, Z))

                cv2.drawFrameAxes(
                    frame,
                    matrice_camera,
                    distorsion,
                    rvec,
                    tvecs[i][0],
                    0.05
                )

                texte = (
                    f"ID {identifiant} | "
                    f"X={X:.2f} m Y={Y:.2f} m Z={Z:.2f} m "
                    f"Theta={theta_deg:.1f} deg"
                )
                cv2.putText(
                    frame,
                    texte,
                    (15, 30 + 28 * i),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.55,
                    (0, 255, 0),
                    2
                )

                print(
                    f"ID={identifiant} | X={X:.3f} m | "
                    f"Y={Y:.3f} m | Z={Z:.3f} m | "
                    f"Theta={theta_deg:.2f} deg"
                )

        cv2.imshow("Detection ArUco - Pose 3D", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break
finally:
    cap.release()
    cv2.destroyAllWindows()
