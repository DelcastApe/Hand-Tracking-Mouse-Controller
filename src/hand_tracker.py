import cv2
import mediapipe as mp


class HandTracker:
    def __init__(self,
                 max_num_hands: int = 1,
                 detection_confidence: float = 0.5,
                 tracking_confidence: float = 0.5):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=max_num_hands,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence
        )
        self.mp_drawing = mp.solutions.drawing_utils

    def process(self, frame, draw: bool = True):
        """
        Procesa un frame de OpenCV, detecta la mano y devuelve:
        - frame (posiblemente con dibujado)
        - landmarks (objeto de MediaPipe) o None si no hay mano
        """

        # Convertir BGR -> RGB para MediaPipe
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        rgb.flags.writeable = False

        results = self.hands.process(rgb)

        landmarks = None
        if results.multi_hand_landmarks:
            # Por ahora usamos solo la primera mano
            landmarks = results.multi_hand_landmarks[0]

            if draw:
                self.mp_drawing.draw_landmarks(
                    frame,
                    landmarks,
                    self.mp_hands.HAND_CONNECTIONS
                )

        return frame, landmarks

    def __del__(self):
        # Cerrar el recurso de MediaPipe
        self.hands.close()
