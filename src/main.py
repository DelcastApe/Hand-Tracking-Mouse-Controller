import cv2

from hand_tracker import HandTracker
from gesture_detector import GestureDetector
from mouse_controller import MouseController
from config import Config
from utils.smoothing import Smoother


def main():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("❌ No se pudo abrir la cámara (VideoCapture(0)).")
        return

    tracker = HandTracker()
    detector = GestureDetector(Config)
    mouse = MouseController()
    smoother = Smoother(alpha=0.9)

    prev_gesture = "NONE"

    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ No se pudo leer de la cámara.")
            break

        frame = cv2.flip(frame, 1)

        frame, landmarks = tracker.process(frame, draw=True)

        current_gesture = "NONE"
        text = "No se detecta mano"

        if landmarks is not None:
            result = detector.detect(landmarks)
            current_gesture = result["gesture"]

            # Texto del gesto
            if current_gesture == "LEFT_CLICK":
                text = "GESTO: LEFT_CLICK"
            elif current_gesture == "RIGHT_CLICK":
                text = "GESTO: RIGHT_CLICK"
            elif current_gesture == "MOVE_CURSOR":
                text = "GESTO: MOVE_CURSOR (solo índice)"
            else:
                text = "Mano detectada"

            # Mostrar texto
            cv2.putText(
                frame,
                text,
                (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.0,
                (0, 0, 255) if current_gesture != "NONE" else (0, 255, 0),
                2,
                cv2.LINE_AA
            )

            # ===== 1) Movimiento del cursor (cada frame) =====
            if current_gesture == "MOVE_CURSOR":
                x_norm = result["data"]["x"]
                y_norm = result["data"]["y"]

                smoother.add(x_norm, y_norm)
                sx, sy = smoother.get()
                if sx is not None:
                    mouse.move_cursor_normalized(sx, sy)

            # ===== 2) Clicks (solo al cambiar de gesto) =====
            if current_gesture != prev_gesture:
                if current_gesture == "LEFT_CLICK":
                    print("[ACTION] LEFT CLICK")
                    mouse.left_click()
                elif current_gesture == "RIGHT_CLICK":
                    print("[ACTION] RIGHT CLICK")
                    mouse.right_click()

        else:
            cv2.putText(
                frame,
                text,
                (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.0,
                (0, 0, 255),
                2,
                cv2.LINE_AA
            )

        # Mensaje ligero para recordarte que se autoajusta
        cv2.putText(
            frame,
            "Mueve el indice arriba/abajo unos segundos para auto-calibrar",
            (10, frame.shape[0] - 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (200, 200, 200),
            1,
            cv2.LINE_AA
        )

        cv2.imshow("Hand Mouse Controller", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or key == 27:  # ESC o q
            break

        prev_gesture = current_gesture

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
