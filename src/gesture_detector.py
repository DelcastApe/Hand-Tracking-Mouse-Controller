import math


class GestureDetector:
    def __init__(self, config):
        self.config = config

    def _get_point(self, landmarks, index):
        """
        Devuelve (x, y) normalizados [0,1] de un landmark.
        """
        lm = landmarks.landmark[index]
        return lm.x, lm.y

    def _distance(self, p1, p2):
        """
        Distancia euclidiana entre dos puntos (x, y).
        """
        return math.dist(p1, p2)

    def _fingers_up(self, landmarks):
        """
        Devuelve qué dedos están levantados (True/False).
        Usamos comparación de y entre tip y pip (para mano vertical).
        Índices de MediaPipe:
          INDEX_TIP = 8,   INDEX_PIP = 6
          MIDDLE_TIP = 12, MIDDLE_PIP = 10
          RING_TIP = 16,   RING_PIP = 14
          PINKY_TIP = 20,  PINKY_PIP = 18
        """
        def tip_pip_up(tip_index, pip_index):
            tip = landmarks.landmark[tip_index]
            pip = landmarks.landmark[pip_index]
            # En la imagen, y crece hacia abajo -> dedo arriba => tip.y < pip.y
            return tip.y < pip.y

        fingers = {
            "index": tip_pip_up(8, 6),
            "middle": tip_pip_up(12, 10),
            "ring": tip_pip_up(16, 14),
            "pinky": tip_pip_up(20, 18),
        }
        return fingers

    def detect(self, landmarks):
        """
        Detecta gesto a partir de los landmarks de la mano.

        Gestos:
          - LEFT_CLICK  -> pulgar + índice (pinch)
          - RIGHT_CLICK -> pulgar + dedo medio (fuck u pinch)
          - MOVE_CURSOR -> solo índice levantado
          - NONE        -> ningún gesto reconocido
        """

        # Índices de MediaPipe
        thumb_tip_idx = 4       # THUMB_TIP
        index_tip_idx = 8       # INDEX_TIP
        middle_tip_idx = 12     # MIDDLE_TIP (dedo medio)

        # Coordenadas (normalizadas)
        thumb_tip = self._get_point(landmarks, thumb_tip_idx)
        index_tip = self._get_point(landmarks, index_tip_idx)
        middle_tip = self._get_point(landmarks, middle_tip_idx)

        # Distancias pulgar-índice y pulgar-medio
        dist_thumb_index = self._distance(thumb_tip, index_tip)
        dist_thumb_middle = self._distance(thumb_tip, middle_tip)

        # 1) Índice + pulgar -> LEFT_CLICK
        if dist_thumb_index < self.config.PINCH_THRESHOLD:
            return {
                "gesture": "LEFT_CLICK",
                "data": {"distance": dist_thumb_index}
            }

        # 2) Dedo medio + pulgar -> RIGHT_CLICK
        if dist_thumb_middle < self.config.PINCH_THRESHOLD:
            return {
                "gesture": "RIGHT_CLICK",
                "data": {"distance": dist_thumb_middle}
            }

        # 3) Solo índice levantado -> MOVE_CURSOR
        fingers = self._fingers_up(landmarks)
        # index arriba, los otros tres abajo
        if fingers["index"] and not (fingers["middle"] or fingers["ring"] or fingers["pinky"]):
            idx_x, idx_y = index_tip
            return {
                "gesture": "MOVE_CURSOR",
                "data": {"x": idx_x, "y": idx_y}
            }

        # 4) Ningún gesto detectado
        return {
            "gesture": "NONE",
            "data": {}
        }
