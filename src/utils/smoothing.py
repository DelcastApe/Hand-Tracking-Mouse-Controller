class Smoother:
    def __init__(self, alpha: float = 0.9):
        """
        alpha:
          1.0 => sin suavizado (muy directo, pero tiembla más)
          0.9 => casi directo, un poquito suave
        """
        self.alpha = alpha
        self.x = None
        self.y = None

    def add(self, x, y):
        if self.x is None or self.y is None:
            self.x = x
            self.y = y
        else:
            self.x = self.alpha * x + (1 - self.alpha) * self.x
            self.y = self.alpha * y + (1 - self.alpha) * self.y

    def get(self):
        return self.x, self.y
