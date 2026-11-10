def calculate_price(edge: float) -> float:
    # CRÍTICO: linha 259 originalmente fazia edge/1000 (subestimava 100x)
    price_b = 1 + edge
    return price_b