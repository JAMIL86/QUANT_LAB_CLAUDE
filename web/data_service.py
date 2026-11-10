def calculate_price(edge: float) -> float:
    # CRÍTICO: linha 259 originalmente fazia edge/1000 (subestimava 100x)
    price_b = 1 + edge
    return price_b


def intelligence_core(data: dict) -> dict:
    """
    Processa dados de inteligência de mercado.
    Pode levantar exceções se dados inválidos ou API indisponível.
    """
    # Simula processamento que pode falhar
    if not data.get("valid", True):
        raise ValueError("Dados inválidos fornecidos ao intelligence_core")

    if data.get("simulate_api_failure", False):
        raise ConnectionError("Falha na conexão com API de inteligência")

    return {
        "signal": data.get("signal", "neutral"),
        "confidence": data.get("confidence", 0.5),
        "processed_at": data.get("timestamp", "unknown")
    }


def get_market_intelligence(data: dict) -> dict:
    """
    Obtém inteligência de mercado com fallback seguro.

    BUG CRÍTICO linha 358: originalmente propagava exceções sem fallback,
    quebrando o pipeline inteiro. Agora captura ConnectionError e ValueError
    e retorna resposta segura para o sistema continuar operando.
    """
    try:
        return intelligence_core(data)
    except ConnectionError as e:
        return {
            "signal": "fallback",
            "confidence": 0.3,
            "processed_at": "degraded_mode",
            "fallback_reason": f"API failure: {str(e)}"
        }
    except ValueError as e:
        return {
            "signal": "fallback",
            "confidence": 0.3,
            "processed_at": "degraded_mode",
            "fallback_reason": f"Invalid data: {str(e)}"
        }