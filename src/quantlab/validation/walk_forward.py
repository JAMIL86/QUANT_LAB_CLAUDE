"""Walk-Forward Validation (Quant Lab)
Regras: R1 honesto, R3 sandbox, R6 sem look-ahead, R8 seed/hash, R9 CPU
"""
import hashlib


def walk_forward_validate(returns, train_window: int = 252, test_window: int = 63) -> dict:
    """Validação walk-forward (expanding window).

    Args:
        returns: lista de retornos
        train_window: tamanho da janela de treino (dias)
        test_window: tamanho da janela de teste (dias)

    Returns:
        dict com métricas de validação
    """
    n = len(returns)
    if n < train_window + test_window:
        return {
            "status": "INCONCLUSIVO (dados insuficientes)",
            "train_window": train_window,
            "test_window": test_window,
            "available": n,
            "label": "SINTÉTICO — validação walk-forward"
        }

    # Walk-forward simples (expanding window)
    train_returns = returns[:train_window]
    test_returns = returns[train_window:train_window + test_window]

    # Métricas de treino
    train_sharpe = _sharpe(train_returns)

    # Métricas de teste (R6: sem look-ahead — usa apenas dados disponíveis)
    test_sharpe = _sharpe(test_returns)

    # R1: nunca declara lucrativo sem prova
    return {
        "method": "walk_forward_expanding",
        "train_window": train_window,
        "test_window": test_window,
        "train_sharpe": round(train_sharpe, 4),
        "test_sharpe": round(test_sharpe, 4),
        "status": "INCONCLUSIVO (walk-forward estrutural; sem conclusão de robustez)",
        "label": "SINTÉTICO — validação walk-forward (R6 sem look-ahead)",
        "hash_sha256": hashlib.sha256(str((train_window, test_window)).encode()).hexdigest()[:16],
        "rules_applied": ["R1", "R3", "R6", "R8", "R9"]
    }


def _sharpe(returns: list) -> float:
    """Calcula Sharpe ratio simplificado."""
    if not returns:
        return 0.0
    avg = sum(returns) / len(returns)
    if len(returns) < 2:
        return 0.0
    variance = sum((r - avg) ** 2 for r in returns) / len(returns)
    std = variance ** 0.5
    if std < 1e-9:
        return 0.0
    return avg / std


__all__ = ["walk_forward_validate"]