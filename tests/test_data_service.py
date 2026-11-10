import pytest
from web.data_service import calculate_price


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