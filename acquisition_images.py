"""
Acquisition des images pour la calibration de la caméra.
Projet : Métasurface programmable - LEME

Utilisation :
    python acquisition_images.py

Touches :
    ESPACE : enregistrer l'image affichée
    ECHAP  : quitter
"""

import cv2
from pathlib import Path

DOSSIER = Path("data/Calibration")
CAMERA_INDEX = 0

DOSSIER.mkdir(parents=True, exist_ok=True)

cap = cv2.VideoCapture(CAMERA_INDEX)

if not cap.isOpened():
    raise RuntimeError("Impossible d'ouvrir la caméra. Vérifiez CAMERA_INDEX.")

compteur = len(list(DOSSIER.glob("calibration_*.jpg")))

print("Acquisition des images de calibration")
print("ESPACE : enregistrer une image | ECHAP : quitter")

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Erreur lors de la lecture de la caméra.")
            break

        affichage = frame.copy()
        cv2.putText(
            affichage,
            f"Images enregistrees : {compteur}",
            (20, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )
        cv2.imshow("Acquisition - Damier", affichage)

        touche = cv2.waitKey(1) & 0xFF

        if touche == 32:  # Barre espace
            chemin = DOSSIER / f"calibration_{compteur:02d}.jpg"
            if cv2.imwrite(str(chemin), frame):
                print(f"Image sauvegardee : {chemin}")
                compteur += 1
            else:
                print(f"Impossible d'enregistrer : {chemin}")

        elif touche == 27:  # Echap
            break
finally:
    cap.release()
    cv2.destroyAllWindows()

print(f"Acquisition terminee : {compteur} image(s) dans {DOSSIER}.")
