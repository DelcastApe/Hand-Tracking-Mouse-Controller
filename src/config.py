class Config:
    # Umbral para detectar pinch (pulgar con otro dedo)
    PINCH_THRESHOLD = 0.05   # ajustable

    # Umbral para detectar puño (distancia media dedos-muñeca)
    FIST_THRESHOLD = 0.25    # súbelo/bájalo si hace falta

    DEBUG_DRAW = True
