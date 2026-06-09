import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe.tasks.python.vision import RunningMode
import numpy as np
import cv2
import os

class FingerCountModel:
    def __init__(self, model_path="model/hand_landmarker.task"):
        # current workdir
        base_options = python.BaseOptions(model_asset_path=model_path)
        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            num_hands=1,
            min_hand_detection_confidence=0.5,
            running_mode=RunningMode.IMAGE
        )

        self.mp_hands = vision.HandLandmarker.create_from_options(options)
        self.tip_ids = [4, 8, 12, 16, 20]

    def predict(self, image_bytes: bytes):

        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if img is None:
            raise ValueError("No se pudo decodificar la imagen.")

        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=img_rgb)

        results = self.mp_hands.detect(mp_image)

        mano_detectada = results.handedness[0][0].category_name

        if results.hand_landmarks:
            hand_landmarks = results.hand_landmarks[0]
            return self.count_fingers(hand_landmarks, mano_detectada)
        else:
            return 0

    def count_fingers(self, hand_landmarks, mano_detectada):
        count = []

        if mano_detectada == "Right":
            # Para mano derecha: Si la punta está más hacia un lado que la articulación
            if hand_landmarks[self.tip_ids[0]].x > hand_landmarks[self.tip_ids[0] - 1].x:
                count.append(1)
            else:
                count.append(0)
        else: 
            # Para mano izquierda (Left): Invertimos el signo para que lea la dirección opuesta
            if hand_landmarks[self.tip_ids[0]].x < hand_landmarks[self.tip_ids[0] - 1].x:
                count.append(1)
            else:
                count.append(0)

        # Resto de los dedos (Índice, Medio, Anular, Meñique)
        for id in range(1, 5):
            if hand_landmarks[self.tip_ids[id]].y < hand_landmarks[self.tip_ids[id] - 2].y:
                count.append(1)
            else:
                count.append(0)

        return count.count(1)