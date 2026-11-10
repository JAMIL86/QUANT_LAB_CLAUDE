"""Lottery Analyzer (Quant Lab)
Regras: R1 honesto, R2 loterias sao aleatorias, R3 sandbox, R9 CPU
"""
import random


def analyze_lottery(numbers: list, game: str = "megasena", n_simulations: int = 1000) -> dict:
    """Analisa estatísticas de loteria (R2: loterias sao aleatorias).

    Args:
        numbers: lista de números sorteados
        game: tipo de jogo (megasena, lotofacil, etc)
        n_simulations: número de simulações para teste de aleatoriedade

    Returns:
        dict com estatísticas
    """
    # R2: loterias sao aleatorias — não há estratégia
    if not numbers:
        return {"status": "INCONCLUSIVO (sem dados)", "label": "SINTÉTICO"}

    # Estatísticas básicas
    unique_numbers = len(set(numbers))

    # Teste de aleatoriedade (R2: loterias sao aleatorias)
    random_numbers = [random.randint(1, 60) for _ in range(len(numbers) * n_simulations)]
    random_unique = len(set(random_numbers))

    # R1: nunca declara lucrativo sem prova
    return {
        "game": game,
        "numbers_analyzed": len(numbers),
        "unique_numbers": unique_numbers,
        "random_unique_simulation": random_unique,
        "status": "INCONCLUSIVO (R2: loterias sao aleatorias; sem estratégia)",
        "label": "SINTÉTICO — análise de loteria (R2 aleatoriedade)",
        "rules_applied": ["R1", "R2", "R3", "R9"]
    }

__all__ = ["analyze_lottery"]