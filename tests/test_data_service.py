import pytest
from web.data_service import calculate_price, intelligence_core, get_market_intelligence


def test_calculate_price_uses_1_plus_edge():
    """
    Teste de regressão para o bug CRÍTICO da linha 259.

    O bug: price_b = edge/1000 (subestimava 100x)
    Correção: price_b = 1 + edge

    Exemplo: edge = 0.05 (5%)
    - Bug: 0.05/1000 = 0.00005 (INCORRETO)
    - Correto: 1 + 0.05 = 1.05
    """
    edge = 0.05  # 5% edge
    result = calculate_price(edge)

    # Com o bug: result seria 0.00005
    # Correto: result deve ser 1.05
    assert result == 1.05, f"Esperado 1.05 (1 + 0.05), mas obteve {result}"


def test_calculate_price_various_edges():
    """Testa vários valores de edge para garantir a correção."""
    test_cases = [
        (0.01, 1.01),   # 1% edge
        (0.02, 1.02),   # 2% edge
        (0.10, 1.10),   # 10% edge
        (0.25, 1.25),   # 25% edge
        (0.50, 1.50),   # 50% edge
        (0.00, 1.00),   # 0% edge
        (-0.05, 0.95),  # -5% edge (negativo)
    ]

    for edge, expected in test_cases:
        result = calculate_price(edge)
        assert result == expected, f"Edge {edge}: esperado {expected}, obteve {result}"


def test_get_market_intelligence_returns_fallback_on_connection_error():
    """
    Teste de regressão para o bug CRÍTICO da linha 358.

    BUG: intelligence_core falha com ConnectionError e não tem fallback,
    propagando a exceção e quebrando o pipeline inteiro.

    Correção: get_market_intelligence deve capturar a exceção e
    retornar um fallback seguro para o sistema continuar operando.
    """
    failing_data = {
        "valid": True,
        "simulate_api_failure": True  # Força falha de API (ConnectionError)
    }

    # Com o fallback implementado, não deve lançar exceção
    result = get_market_intelligence(failing_data)

    # Deve retornar estrutura de fallback válida
    assert isinstance(result, dict)
    assert "signal" in result
    assert "confidence" in result
    assert "processed_at" in result
    assert result["signal"] == "fallback"
    assert result["confidence"] == 0.3
    assert result["processed_at"] == "degraded_mode"
    assert "fallback_reason" in result


def test_get_market_intelligence_returns_fallback_on_value_error():
    """Testa fallback quando intelligence_core levanta ValueError (dados inválidos)."""
    invalid_data = {
        "valid": False  # Força ValueError no intelligence_core
    }

    result = get_market_intelligence(invalid_data)

    assert isinstance(result, dict)
    assert result["signal"] == "fallback"
    assert "fallback_reason" in result


def test_get_market_intelligence_returns_normal_result_when_success():
    """Testa que o comportamento normal ainda funciona quando não há erro."""
    valid_data = {
        "signal": "buy",
        "confidence": 0.85,
        "timestamp": "2024-01-15T10:30:00Z"
    }

    result = get_market_intelligence(valid_data)

    assert result["signal"] == "buy"
    assert result["confidence"] == 0.85
    assert result["processed_at"] == "2024-01-15T10:30:00Z"