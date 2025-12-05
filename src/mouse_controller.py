import pyautogui


class MouseController:
    def __init__(self):
        pyautogui.FAILSAFE = False
        self.screen_width, self.screen_height = pyautogui.size()

        # Margen horizontal (izquierda/derecha) para no depender de toda la imagen
        self.margin_x = 0.10  # 10% a cada lado

        # Auto-calibración vertical
        self.y_min = None
        self.y_max = None

        # Parámetros de adaptación
        self.min_range = 0.10    # rango mínimo aceptable para considerar calibrado
        self.expand_factor = 0.02  # cuánto expandir el rango al ver nuevos extremos

    def _update_vertical_range(self, y: float):
        """
        Actualiza automáticamente y_min y y_max con el valor observado de y.
        Se adapta poco a poco al rango real que usas con tu mano.
        """
        if self.y_min is None or self.y_max is None:
            # Primera vez: inicializamos
            self.y_min = y
            self.y_max = y
            return

        # Expandir el rango si vemos nuevos mínimos/máximos
        if y < self.y_min:
            # nuevo "más arriba" -> ajustamos ligeramente
            self.y_min = y - self.expand_factor
        elif y > self.y_max:
            # nuevo "más abajo" -> ajustamos ligeramente
            self.y_max = y + self.expand_factor

        # Clampear
        self.y_min = max(0.0, self.y_min)
        self.y_max = min(1.0, self.y_max)

        # Asegurar que haya un rango mínimo
        if self.y_max - self.y_min < self.min_range:
            center = (self.y_min + self.y_max) / 2
            half = self.min_range / 2
            self.y_min = max(0.0, center - half)
            self.y_max = min(1.0, center + half)

    def _remap(self, x, y):
        """
        x, y en [0,1] de MediaPipe.
        - x: usa margen fijo.
        - y: usa auto-calibración vertical dinámica.
        Devuelve x_norm, y_norm en [0,1].
        """
        # --- Eje X (horizontal) con margen ---
        x_clamped = min(max(x, self.margin_x), 1.0 - self.margin_x)
        x_norm = (x_clamped - self.margin_x) / (1.0 - 2 * self.margin_x)
        x_norm = min(max(x_norm, 0.0), 1.0)

        # --- Eje Y (vertical) con auto-calibración ---
        # Primero actualizamos el rango observado
        self._update_vertical_range(y)

        if self.y_min is not None and self.y_max is not None and (self.y_max - self.y_min) > 1e-3:
            y_clamped = min(max(y, self.y_min), self.y_max)
            y_norm = (y_clamped - self.y_min) / (self.y_max - self.y_min)
        else:
            # fallback por si pasa algo raro
            y_norm = y

        y_norm = min(max(y_norm, 0.0), 1.0)
        return x_norm, y_norm

    def move_cursor_normalized(self, x, y):
        """
        Recibe x,y normalizados de MediaPipe (0-1) y los convierte a pixeles.
        """
        x_norm, y_norm = self._remap(x, y)

        px = x_norm * self.screen_width
        py = y_norm * self.screen_height

        pyautogui.moveTo(px, py)

    def left_click(self):
        pyautogui.click()

    def right_click(self):
        pyautogui.rightClick()

    def scroll(self, amount):
        pyautogui.scroll(amount)

    def close_window(self):
        pyautogui.hotkey('alt', 'f4')
